"""TouchDesigner UI-state bridge for metrics-driven panel text.

This module translates ``metrics_output`` into panel-ready strings and a
compact UI state payload that TouchDesigner panels can consume without knowing
the full metrics schema.

Design goals:
- Keep rendering scripts simple: they should read short strings, not parse
  nested metrics payloads.
- Support both the current lightweight TD scaffold and Leo's 9-panel layout.
- Stay testable outside TouchDesigner.

Typical TouchDesigner usage:
1. Paste this file into a Text DAT named ``ui_state`` and enable Module ON.
2. After metrics recompute, call ``compute_and_store_touchdesigner_ui()``.
3. Read ``parent().fetch('text_right_phase_preview', '')`` or the other stored
   panel strings from Text TOP expressions.
"""
from __future__ import annotations

from typing import Any


METHOD_LABELS = {
    "masonry": "Masonry",
    "3d_printed": "3D Printed",
    "prefab": "Prefab",
    "reclaimed_brick": "Reclaimed Brick",
}

MATERIAL_LABELS = {
    "fired_clay_brick": "Fired clay brick",
    "printed_concrete_or_earth_proxy": "Printed concrete / earth proxy",
    "timber_clt_prefab": "CLT timber prefab",
    "modular_concrete_prefab": "Modular concrete prefab",
    "reclaimed_fired_clay_brick": "Reclaimed fired clay brick",
}

METHOD_NOTES = {
    "masonry": [
        "Layered brick assembly drives most wall impact.",
        "Structure and finishing usually dominate local labor.",
        "Good for low- to mid-rise comparisons in this prototype.",
    ],
    "3d_printed": [
        "Foundation and roof still rely on conventional trades.",
        "Wall metrics focus on the printed shell and surface.",
        "Some values stay estimated where research is incomplete.",
    ],
    "prefab": [
        "Factory production stays separate from transport and assembly.",
        "Lifecycle data replaces the usual construction phases.",
        "Switch CLT and modular concrete to compare strategies.",
    ],
    "reclaimed_brick": [
        "Reclaimed brick currently behaves like an overlay mode.",
        "Comparisons still rely on partial logistics assumptions.",
        "Best used as a baseline reference until fuller data lands.",
    ],
}

METHOD_RANGE_LABELS = {
    "masonry": "1-5 floors",
    "3d_printed": "1-2 floors",
    "prefab:clt": "1-8 floors",
    "prefab:modular_concrete": "1-12 floors",
    "prefab": "CLT 1-8 floors or modular concrete 1-12 floors",
    "reclaimed_brick": "Baseline / overlay mode",
}

DATA_MODEL_LABELS = {
    "phase_based": "Phase Mode",
    "lifecycle_based": "Lifecycle Mode",
    "overlay": "Overlay Mode",
}

DISPLAY_MODE_LABELS = {
    "construction_phase_view": "Phase Comparison",
    "prefab_lifecycle_card": "Prefab Lifecycle View",
}

STATUS_LABELS = {
    "ok": "OK",
    "partial": "Partial",
    "fallback": "Fallback",
}

WARNING_LABELS = {
    "unknown_source_key": "Source Pending",
    "default_prefab_sub_method": "Default Prefab Mode",
}

PANEL_IDS = (
    "top_phase_navigation",
    "left_info",
    "left_assembly_sequence",
    "method_selection",
    "right_comparison",
    "right_cost_chart",
    "right_phase_preview",
    "bar_bottom_status",
    "stats_text",
)


def _humanize_token(value: str) -> str:
    return value.replace("_", " ").replace("-", " ").title()


def _method_label(method_key: str | None) -> str:
    if not method_key:
        return "Awaiting Method"
    return METHOD_LABELS.get(method_key, _humanize_token(method_key))


def _material_label(value: str | None) -> str:
    if not value:
        return "Pending"
    return MATERIAL_LABELS.get(value, _humanize_token(value))


def _status_label(status: str | None) -> str:
    if not status:
        return "Pending"
    return STATUS_LABELS.get(status, _humanize_token(status))


def _data_model_label(value: str | None) -> str:
    if not value:
        return "Unknown Mode"
    return DATA_MODEL_LABELS.get(value, _humanize_token(value))


def _display_mode_label(value: str | None) -> str:
    if not value:
        return "Unknown View"
    return DISPLAY_MODE_LABELS.get(value, _humanize_token(value))


def _warning_label(value: str) -> str:
    if value in WARNING_LABELS:
        return WARNING_LABELS[value]
    if value.startswith("missing_normalized_data"):
        return "Data Pending"
    if value.startswith("unsupported_basis"):
        return "Unsupported Basis"
    if value.startswith("unexpected_stage"):
        return "Unexpected Stage"
    if value.startswith("selected_material is recorded"):
        return "Selected Material Pending"
    if value.startswith("shape_factor is still applied"):
        return "Shape Factor Compatibility Mode"
    if " " in value:
        return value.rstrip(".")
    return _humanize_token(value)


def _format_number(value: float | int | None, digits: int = 0) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):,.{digits}f}"


def _format_area(value: float | int | None, digits: int = 1) -> str:
    if value is None:
        return "n/a"
    return f"{_format_number(value, digits)} m2"


def _format_range(metric_entry: dict[str, Any] | None, unit_suffix: str = "") -> str:
    if not metric_entry:
        return "n/a"
    low = metric_entry.get("low")
    high = metric_entry.get("high")
    if low is None or high is None:
        return "n/a"
    suffix = f" {unit_suffix}".rstrip() if unit_suffix else ""
    return f"{_format_number(low, 1)}-{_format_number(high, 1)}{suffix}"


def _format_midpoint(metric_entry: dict[str, Any] | None, unit_suffix: str = "") -> str:
    if not metric_entry:
        return "n/a"
    low = metric_entry.get("low")
    high = metric_entry.get("high")
    if low is None or high is None:
        return "n/a"
    midpoint = (float(low) + float(high)) / 2.0
    suffix = f" {unit_suffix}".rstrip() if unit_suffix else ""
    return f"{_format_number(midpoint, 1)}{suffix}"


def _sequence_summary(metrics_output: dict[str, Any], active_stage_key: str | None) -> str:
    stage_sequence = metrics_output.get("stage_sequence", [])
    if not stage_sequence:
        return "No stage sequence available"

    stage_labels = metrics_output.get("stage_labels", {})
    parts = []
    for stage in stage_sequence:
        label = stage_labels.get(stage, stage)
        parts.append(f"[{label}]" if stage == active_stage_key else label)
    return " | ".join(parts)


def _compact_sequence_summary(metrics_output: dict[str, Any], active_stage_key: str | None) -> str:
    summary = _sequence_summary(metrics_output, active_stage_key)
    replacements = {
        "Structure / Walls": "Walls",
        "Foundation": "Foundation",
        "Openings": "Openings",
        "Finishing": "Finishing",
    }
    for old, new in replacements.items():
        summary = summary.replace(old, new)
    return summary


def _warning_summary(warnings: list[str], limit: int = 3) -> str:
    if not warnings:
        return "No warnings"
    labels = [_warning_label(warning) for warning in warnings[:limit]]
    if len(warnings) > limit:
        labels.append(f"+{len(warnings) - limit} more")
    return " | ".join(labels)


def _sub_method_summary(metrics_output: dict[str, Any]) -> str:
    sub_method_label = metrics_output.get("sub_method_label")
    if not sub_method_label:
        return "None"
    return str(sub_method_label)


def _active_stage(metrics_output: dict[str, Any]) -> dict[str, Any]:
    return metrics_output.get("active_stage") or {}


def _method_notes(method_key: str | None) -> list[str]:
    if not method_key:
        return [
            "Choose a method to unlock the scale controls.",
            "Floor limits are method-specific in this prototype.",
            "Building-part interaction can be wired after TD state hookup.",
        ]
    return METHOD_NOTES.get(method_key, [])


def _method_range_label(method_key: str | None, sub_method: str | None) -> str:
    if not method_key:
        return "Select a method first"
    if method_key == "prefab" and sub_method:
        return METHOD_RANGE_LABELS.get(f"{method_key}:{sub_method}", METHOD_RANGE_LABELS[method_key])
    return METHOD_RANGE_LABELS.get(method_key, "Range pending")


def _path_focus_copy(metrics_output: dict[str, Any], active_stage_label: str) -> str:
    data_model = metrics_output.get("data_model")
    if data_model == "lifecycle_based":
        return "Lifecycle mode active. Construction phases stay disabled."
    return f"Current focus: {active_stage_label}."


def _next_action_copy(method_key: str | None, floors_label: str, data_model: str | None) -> str:
    if not method_key:
        return "Select a construction method."
    if floors_label in {"0", "n/a"}:
        return "Set floors for this method, then continue."
    if data_model == "lifecycle_based":
        return "Switch CLT / Modular Concrete or inspect another building part."
    return "Change phase or inspect another building part."


def _method_selection_lines(selected_method: str | None, selected_sub_method: str | None) -> list[str]:
    method_rows = _method_rows(selected_sub_method)
    lines = ["CHOOSE METHOD", ""]
    for method_key, model_label, material_label, range_label in method_rows:
        prefix = ">" if method_key == selected_method else "-"
        lines.append(
            f"{prefix} {_method_label(method_key).upper()} | {model_label} | {range_label}"
        )
        lines.append(f"  {material_label}")
    return lines


def _method_rows(selected_sub_method: str | None) -> list[tuple[str, str, str, str]]:
    return [
        ("masonry", "Phase Mode", "Fired clay brick", METHOD_RANGE_LABELS["masonry"]),
        ("3d_printed", "Phase Mode", "Printed concrete / earth proxy", METHOD_RANGE_LABELS["3d_printed"]),
        (
            "prefab",
            "Lifecycle Mode",
            "CLT / modular concrete prefab",
            _method_range_label("prefab", selected_sub_method),
        ),
    ]


def _method_card_text(method_key: str, selected_sub_method: str | None) -> str:
    for key, model_label, material_label, range_label in _method_rows(selected_sub_method):
        if key == method_key:
            compact_range = range_label
            compact_material = material_label
            if key == "prefab" and selected_sub_method is None:
                compact_range = "CLT 1-8 | Mod 1-12"
                compact_material = "CLT / modular prefab"
            return (
                f"{model_label.upper()}\n"
                f"{_method_label(key).upper()}\n"
                f"{compact_material}\n"
                f"Range {compact_range}"
            )
    return ""


def _build_panel_texts(
    metrics_output: dict[str, Any],
    live_state: dict[str, Any],
    method_label: str,
    active_stage: dict[str, Any],
    warning_labels: list[str],
) -> dict[str, str]:
    scenario = metrics_output.get("scenario", {})
    method_key = scenario.get("construction_method")
    status_label = _status_label(metrics_output.get("data_status"))
    data_model_label = _data_model_label(metrics_output.get("data_model"))
    display_mode_label = _display_mode_label(metrics_output.get("display_mode"))
    area_label = _format_area(live_state.get("area_m2") or scenario.get("area_m2"), 1)
    floors_label = _format_number(
        live_state.get("number_of_floors") or scenario.get("number_of_floors"),
        0,
    )
    floor_height_m = float(live_state.get("floor_height_m") or 3.2)
    building_height_m = float(
        live_state.get("building_height_m")
        or max(1.0, float(live_state.get("number_of_floors") or scenario.get("number_of_floors") or 1))
        * floor_height_m
    )
    active_stage_label = active_stage.get("label") or "Awaiting Stage"
    path_label = metrics_output.get("path_label", "Path")
    selected_material = _material_label(metrics_output.get("selected_material"))
    sub_method_summary = _sub_method_summary(metrics_output)
    selected_sub_method = metrics_output.get("sub_method")
    selected_part_label = live_state.get("selected_part_label") or "Whole Building"
    selected_parts_count = int(live_state.get("selected_parts_count") or 0)
    if selected_parts_count <= 0:
        selected_parts_count = 1
    range_label = _method_range_label(method_key, selected_sub_method)
    notes = _method_notes(method_key)
    next_action = _next_action_copy(method_key, floors_label, metrics_output.get("data_model"))

    top_phase_navigation = _compact_sequence_summary(metrics_output, active_stage.get("stage"))

    left_info = "YOUR SELECTION"
    left_info_hero = (
        "METHOD\n"
        f"{method_label.upper()}\n"
        f"{data_model_label} | {floors_label} floors"
    )
    left_info_details = (
        "BUILDING PART\n"
        f"{selected_part_label}\n\n"
        "FOOTPRINT AREA\n"
        f"{area_label}\n\n"
        "MATERIAL SYSTEM\n"
        f"{selected_material}"
    )
    left_info_scale = (
        "BUILDING SCALE\n"
        f"Range {range_label}\n"
        f"Floor h { _format_number(floor_height_m, 1) } m\n"
        f"Total { _format_number(building_height_m, 1) } m"
    )
    left_info_scale_minus = "−"
    left_info_scale_value = floors_label
    left_info_scale_plus = "+"

    left_assembly_sequence = (
        "METHOD NOTES\n\n"
        f"- {notes[0] if len(notes) > 0 else 'Notes pending.'}\n"
        f"- {notes[1] if len(notes) > 1 else 'More TD notes can be added here.'}\n"
        "\n"
        f"FOCUS\n{active_stage_label}"
    )

    method_selection = "CHOOSE METHOD"
    method_card_masonry = _method_card_text("masonry", selected_sub_method)
    method_card_3d_printed = _method_card_text("3d_printed", selected_sub_method)
    method_card_prefab = _method_card_text("prefab", selected_sub_method)

    right_comparison = "SELECTED PART IMPACT"
    right_comparison_summary = (
        f"METHOD {method_label.upper()}\n"
        f"{active_stage_label} | {floors_label} floors"
    )
    right_comparison_metrics = (
        f"CARBON { _format_range(active_stage.get('co2'), 'kg') }\n"
        f"COST { _format_range(active_stage.get('cost'), 'EUR') }\n"
        f"TIME { _format_range(active_stage.get('time'), 'days') }\n"
        f"LABOR { _format_range(active_stage.get('labor'), 'hours') }\n"
        f"BASIS { _format_area(active_stage.get('phase_quantity_m2'), 1) }"
    )

    right_cost_chart = "TOTAL PROJECT IMPACT"
    right_cost_scope = (
        "SCOPE\n"
        f"{selected_parts_count} selected"
    )
    right_cost_hero = (
        "TOTAL COST\n"
        f"{_format_range(metrics_output.get('cost_estimate'), 'EUR')}"
    )
    right_cost_grid_left = (
        "CO2\n"
        f"{_format_range(metrics_output.get('co2_estimate'), 'kg')}\n\n"
        "TIME\n"
        f"{_format_range(metrics_output.get('construction_time'), 'd')}"
    )
    right_cost_grid_right = (
        "LABOR\n"
        f"{_format_range(metrics_output.get('labor_hours'), 'h')}\n\n"
        "STATUS\n"
        f"{status_label}"
    )

    right_phase_preview = "CURRENT STATE"
    right_phase_preview_state = (
        f"{method_label.upper()}\n"
        f"{display_mode_label} | {status_label}"
    )
    right_phase_preview_left = (
        "PARTS\n"
        f"{selected_parts_count} selected\n\n"
        "FLOORS\n"
        f"{floors_label}"
    )
    right_phase_preview_right = (
        "FOCUS\n"
        f"{active_stage_label}\n\n"
        "RANGE\n"
        f"{sub_method_summary if method_key == 'prefab' else range_label}"
    )

    hb_label = "LIVE" if int(live_state.get("hb_alive", 1) or 0) else "OFFLINE"
    bar_bottom_status = (
        "1 CHOOSE METHOD | 2 SET FLOORS | 3 "
        f"{'LIFECYCLE MODE' if metrics_output.get('data_model') == 'lifecycle_based' else 'CHOOSE PHASE'} "
        f"| 4 CLICK BUILDING PART || NEXT: {next_action} || VISION {hb_label}"
    )

    return {
        "top_phase_navigation": top_phase_navigation,
        "left_info": left_info,
        "left_info_hero": left_info_hero,
        "left_info_details": left_info_details,
        "left_info_scale": left_info_scale,
        "left_info_scale_minus": left_info_scale_minus,
        "left_info_scale_value": left_info_scale_value,
        "left_info_scale_plus": left_info_scale_plus,
        "left_assembly_sequence": left_assembly_sequence,
        "method_selection": method_selection,
        "method_card_masonry": method_card_masonry,
        "method_card_3d_printed": method_card_3d_printed,
        "method_card_prefab": method_card_prefab,
        "right_comparison": right_comparison,
        "right_comparison_summary": right_comparison_summary,
        "right_comparison_metrics": right_comparison_metrics,
        "right_cost_chart": right_cost_chart,
        "right_cost_scope": right_cost_scope,
        "right_cost_hero": right_cost_hero,
        "right_cost_grid_left": right_cost_grid_left,
        "right_cost_grid_right": right_cost_grid_right,
        "right_phase_preview": right_phase_preview,
        "right_phase_preview_state": right_phase_preview_state,
        "right_phase_preview_left": right_phase_preview_left,
        "right_phase_preview_right": right_phase_preview_right,
        "bar_bottom_status": bar_bottom_status,
        "stats_text": bar_bottom_status,
    }


def build_ui_state(
    metrics_output: dict[str, Any] | None,
    live_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a compact UI payload from ``metrics_output``.

    Parameters
    ----------
    metrics_output:
        Payload produced by ``touchdesigner.scripts.metrics_engine``.
    live_state:
        Optional lightweight TD state such as ``hb_alive`` or ``area_m2``.
    """
    live_state = dict(live_state or {})

    if not metrics_output:
        panel_texts = {
            panel_id: "Awaiting metrics input" for panel_id in PANEL_IDS
        }
        panel_texts["top_phase_navigation"] = (
            "CHOOSE PHASE\n\nSelect a method, then set floors to unlock phases."
        )
        panel_texts["left_info"] = "YOUR SELECTION"
        panel_texts["left_info_hero"] = (
            "METHOD\nCHOOSE A METHOD\nSelect a construction method to unlock the interface."
        )
        panel_texts["left_info_details"] = (
            "BUILDING PART\nWhole Building\n\nFOOTPRINT AREA\nPending\n\nMATERIAL SYSTEM\nPending"
        )
        panel_texts["left_info_scale"] = (
            "BUILDING SCALE\nRange pending\nFloor h 3.2 m\nTotal pending"
        )
        panel_texts["left_info_scale_minus"] = "−"
        panel_texts["left_info_scale_value"] = "?"
        panel_texts["left_info_scale_plus"] = "+"
        panel_texts["left_assembly_sequence"] = (
            "METHOD NOTES\n\nChoose a method to reveal the active path."
        )
        panel_texts["method_selection"] = "CHOOSE METHOD"
        panel_texts["method_card_masonry"] = _method_card_text("masonry", None)
        panel_texts["method_card_3d_printed"] = _method_card_text("3d_printed", None)
        panel_texts["method_card_prefab"] = _method_card_text("prefab", None)
        panel_texts["right_comparison"] = "SELECTED PART IMPACT"
        panel_texts["right_comparison_summary"] = "METHOD AWAITING METHOD\nSelect a method first."
        panel_texts["right_comparison_metrics"] = (
            "CARBON n/a\nCOST n/a\nTIME n/a\nLABOR n/a\nBASIS n/a"
        )
        panel_texts["right_cost_chart"] = "TOTAL PROJECT IMPACT"
        panel_texts["right_cost_scope"] = "SCOPE\nAwaiting selection"
        panel_texts["right_cost_hero"] = "TOTAL COST\nn/a"
        panel_texts["right_cost_grid_left"] = "TOTAL CO2\nn/a\n\nTOTAL TIME\nn/a"
        panel_texts["right_cost_grid_right"] = "TOTAL LABOR\nn/a\n\nSTATUS\nPending"
        panel_texts["right_phase_preview"] = "CURRENT STATE"
        panel_texts["right_phase_preview_state"] = "AWAITING METHOD\nNo method selected"
        panel_texts["right_phase_preview_left"] = (
            "BUILDING PARTS\nWhole Building\n\nFLOORS\nPending"
        )
        panel_texts["right_phase_preview_right"] = (
            "CURRENT FOCUS\nNo method selected\n\nMETHOD RANGE\nPending"
        )
        panel_texts["bar_bottom_status"] = (
            "1 CHOOSE METHOD | 2 SET FLOORS | 3 CHOOSE PHASE | 4 CLICK BUILDING PART"
        )
        panel_texts["stats_text"] = panel_texts["bar_bottom_status"]
        return {
            "method_label": "Awaiting Method",
            "status_label": "Pending",
            "path_label": "Awaiting Path",
            "active_stage_label": "Awaiting Stage",
            "warning_labels": [],
            "panel_texts": panel_texts,
        }

    scenario = metrics_output.get("scenario", {})
    method_key = scenario.get("construction_method")
    method_label = _method_label(method_key)
    active_stage = _active_stage(metrics_output)
    warning_labels = [
        _warning_label(warning) for warning in metrics_output.get("warnings", [])
    ]
    panel_texts = _build_panel_texts(
        metrics_output,
        live_state,
        method_label=method_label,
        active_stage=active_stage,
        warning_labels=warning_labels,
    )

    return {
        "method_label": method_label,
        "status_label": _status_label(metrics_output.get("data_status")),
        "path_label": metrics_output.get("path_label", "Path"),
        "data_model_label": _data_model_label(metrics_output.get("data_model")),
        "display_mode_label": _display_mode_label(metrics_output.get("display_mode")),
        "active_stage_key": active_stage.get("stage"),
        "active_stage_label": active_stage.get("label") or "Awaiting Stage",
        "sub_method_label": metrics_output.get("sub_method_label"),
        "warning_labels": warning_labels,
        "sequence_summary": _sequence_summary(
            metrics_output,
            active_stage.get("stage"),
        ),
        "panel_texts": panel_texts,
        "available_sub_methods": metrics_output.get("available_sub_methods", []),
        "stage_selection": metrics_output.get("stage_selection"),
        "stage_summaries": metrics_output.get("stage_summaries", []),
        "totals": {
            "co2_estimate": metrics_output.get("co2_estimate"),
            "cost_estimate": metrics_output.get("cost_estimate"),
            "construction_time": metrics_output.get("construction_time"),
            "labor_hours": metrics_output.get("labor_hours"),
        },
    }


def live_state_from_touchdesigner(owner: Any | None = None) -> dict[str, Any]:
    if owner is None:
        try:
            owner = parent()
        except NameError as exc:  # pragma: no cover - TD only
            raise RuntimeError("TouchDesigner owner not available outside TD.") from exc

    return {
        "current_method": owner.fetch("current_method", None),
        "area_m2": owner.fetch("area_m2", 0.0),
        "number_of_floors": owner.fetch("number_of_floors", 1),
        "floor_height_m": owner.fetch("floor_height_m", 3.2),
        "building_height_m": owner.fetch("building_height_m", None),
        "hb_alive": owner.fetch("hb_alive", 1),
        "current_phase_name": owner.fetch("current_phase_name", None),
        "selected_part_label": owner.fetch("selected_part_label", None),
        "selected_parts_count": owner.fetch("selected_parts_count", 0),
    }


def compute_and_store_touchdesigner_ui(
    owner: Any | None = None,
    metrics_output: dict[str, Any] | None = None,
    live_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build panel-ready UI state and store it on the TD owner."""
    if owner is None:
        try:
            owner = parent()
        except NameError as exc:  # pragma: no cover - TD only
            raise RuntimeError("TouchDesigner owner not available outside TD.") from exc

    payload = metrics_output or owner.fetch("metrics_output", None)
    live_payload = live_state or live_state_from_touchdesigner(owner)
    ui_state = build_ui_state(payload, live_state=live_payload)

    owner.store("ui_state", ui_state)
    owner.store("ui_panel_texts", ui_state["panel_texts"])
    for panel_id, text in ui_state["panel_texts"].items():
        owner.store(f"text_{panel_id}", text)
    return ui_state
