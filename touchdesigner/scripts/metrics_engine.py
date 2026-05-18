"""TouchDesigner metrics adapter for the normalized metrics pipeline.

This module keeps the existing TouchDesigner-facing contract stable while
delegating dataset loading and basis-aware scaling to ``metrics.pipeline``.

What stays stable for TD:
- ``scenario_from_touchdesigner()`` still reads the same storage keys.
- ``compute_and_store_touchdesigner()`` still stores ``metrics_output``,
  ``metrics_timestamp``, ``data_status``, and ``material_origin_summary``.
- The returned payload still exposes the familiar top-level summary fields such
  as ``co2_estimate``, ``cost_estimate``, ``construction_time``, and
  ``phase_breakdown``.

What changes internally:
- Normalized CSV files under ``data/methods/`` are now read through
  ``metrics.pipeline`` instead of the legacy 8-column CSV reader.
- Per-stage rows are adapted into the older TD result shape so existing
  TouchDesigner consumers do not have to change all at once.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


FALLBACK_REPO_ROOT = Path("O:/Hardware_III")


def _discover_repo_root() -> Path:
    file_path_text = str(globals().get("__file__", "") or "")
    if file_path_text:
        file_path = Path(file_path_text)
        try:
            resolved = file_path.resolve()
        except Exception:
            resolved = file_path

        search_roots = []
        if resolved.suffix:
            search_roots.extend([resolved.parent, *resolved.parent.parents])
        else:
            search_roots.extend([resolved, *resolved.parents])

        for candidate in search_roots:
            if (candidate / "data" / "methods_db.json").exists():
                return candidate

    try:  # pragma: no branch - TouchDesigner only
        project_root = Path(project.folder).resolve()
        for candidate in [project_root, *project_root.parents]:
            if (candidate / "data" / "methods_db.json").exists():
                return candidate
    except Exception:
        pass

    if FALLBACK_REPO_ROOT.exists():
        return FALLBACK_REPO_ROOT
    return Path.cwd()


REPO_ROOT = _discover_repo_root()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from metrics import pipeline as normalized_pipeline


METHODS_ROOT = REPO_ROOT / "data" / "methods"

PHASES = tuple(normalized_pipeline.PHASE_STAGES)
LIFECYCLE_STAGES = tuple(normalized_pipeline.PREFAB_STAGES)
PHASE_LABELS = {
    "foundation": "1 Foundation",
    "structure": "2 Structure / Walls",
    "roof": "3 Roof",
    "openings": "4 Openings",
    "finishing": "5 Finishing",
}
LIFECYCLE_LABELS = {
    "A1-A3": "Production",
    "A4": "Transport",
    "A5": "Assembly",
    "B": "Use phase",
    "C": "End of Life",
}

TD_METHOD_ALIASES = {
    "masonry": "masonry",
    "brick": "masonry",
    "3d_printed": "3d_printed",
    "3d-printed": "3d_printed",
    "3dp": "3d_printed",
    "concrete_3dp": "3d_printed",
    "prefab": "prefab",
    "prefab_timber": "prefab",
    "prefab_clt": "prefab",
    "clt": "prefab",
    "modular_concrete": "prefab",
    "prefab_modular_concrete": "prefab",
    "reclaimed_brick": "reclaimed_brick",
    "reclaimed-brick": "reclaimed_brick",
}

PREFAB_SUB_METHOD_ALIASES = {
    "prefab_timber": "clt",
    "prefab_clt": "clt",
    "clt": "clt",
    "modular_concrete": "modular_concrete",
    "prefab_modular_concrete": "modular_concrete",
}

METHOD_FILE_MAP = {
    "masonry": "masonry.csv",
    "3d_printed": "3d-printed.csv",
    "prefab": "prefab.csv",
    "reclaimed_brick": "reclaimed-brick.csv",
}

SUMMARY_METRIC_KEYS = (
    "co2_kg_per_m2",
    "labor_hours_per_m2",
    "time_days",
    "cost_eur_per_m2",
    "material_origin",
)

NUMERIC_METRIC_SPECS = {
    "co2_kg_per_m2": {
        "preferred_metrics": ("co2_kg_per_m2",),
        "unit": "kg CO2eq",
    },
    "labor_hours_per_m2": {
        "preferred_metrics": ("labor_hours_per_m2",),
        "unit": "hours",
    },
    "time_days": {
        "preferred_metrics": ("time_days",),
        "unit": "days",
    },
    "cost_eur_per_m2": {
        "preferred_metrics": ("cost_eur_per_m2",),
        "unit": "EUR",
    },
}


@dataclass
class ScenarioInput:
    construction_method: str
    area_m2: float
    number_of_floors: int = 1
    shape_factor: float = 1.0
    selected_material: str | None = None
    selected_program: str | None = None
    current_phase: str | None = None
    sales_price_per_m2: float | None = None
    rental_price_per_m2: float | None = None
    rent_months: int | None = None


def normalize_method_name(method_name: str | None) -> str:
    if not method_name:
        raise ValueError("construction_method is required")
    normalized = method_name.strip().lower().replace(" ", "_")
    if normalized not in TD_METHOD_ALIASES:
        known = ", ".join(sorted(TD_METHOD_ALIASES))
        raise ValueError(
            f"Unknown construction method '{method_name}'. Known: {known}"
        )
    return TD_METHOD_ALIASES[normalized]


def _prefab_sub_method_for_scenario(
    method_name: str | None,
    selected_material: str | None,
) -> str | None:
    if method_name:
        normalized = method_name.strip().lower().replace(" ", "_")
        if normalized in PREFAB_SUB_METHOD_ALIASES:
            return PREFAB_SUB_METHOD_ALIASES[normalized]

    material = (selected_material or "").strip().lower()
    if "modular_concrete" in material or "modular-concrete" in material:
        return "modular_concrete"
    if "clt" in material or "timber" in material:
        return "clt"
    return None


def _round_or_none(value: float | None, digits: int = 2) -> float | None:
    if value is None:
        return None
    return round(value, digits)


def _to_float(value: str | float | int | None) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text or text.lower() == "null":
        return None
    return float(text)


def _humanize_token(value: str) -> str:
    return value.replace("_", " ").replace("-", " ").title()


def _scenario_from_any(scenario: ScenarioInput | dict[str, Any]) -> ScenarioInput:
    if isinstance(scenario, ScenarioInput):
        return scenario
    payload = dict(scenario)
    payload["construction_method"] = normalize_method_name(
        payload.get("construction_method")
    )
    payload["area_m2"] = float(payload.get("area_m2", 0.0))
    payload["number_of_floors"] = int(payload.get("number_of_floors", 1) or 1)
    payload["shape_factor"] = float(payload.get("shape_factor", 1.0) or 1.0)
    if payload.get("sales_price_per_m2") is not None:
        payload["sales_price_per_m2"] = float(payload["sales_price_per_m2"])
    if payload.get("rental_price_per_m2") is not None:
        payload["rental_price_per_m2"] = float(payload["rental_price_per_m2"])
    if payload.get("rent_months") is not None:
        payload["rent_months"] = int(payload["rent_months"])
    return ScenarioInput(**payload)


def _shape_factor_multiplier(stage: str, scenario: ScenarioInput) -> float:
    if stage not in {"structure", "openings"}:
        return 1.0
    return max(0.75, float(scenario.shape_factor or 1.0))


def _apply_shape_factor_to_row(
    row: dict[str, Any],
    stage: str,
    scenario: ScenarioInput,
) -> dict[str, Any]:
    multiplier = _shape_factor_multiplier(stage, scenario)
    if multiplier == 1.0:
        return dict(row)

    adjusted = dict(row)
    if isinstance(adjusted.get("scaled_low"), (int, float)):
        adjusted["scaled_low"] = _round_or_none(adjusted["scaled_low"] * multiplier)
    if isinstance(adjusted.get("scaled_high"), (int, float)):
        adjusted["scaled_high"] = _round_or_none(adjusted["scaled_high"] * multiplier)
    adjusted["shape_factor_applied"] = multiplier
    return adjusted


def _unit_quantity_mode(basis: str) -> str:
    if basis in {
        "per_m2_gfa",
        "hours_per_m2_gfa",
        "eur_per_m2_gfa",
        "kg_per_m2_gfa",
        "days_per_m2_gfa",
    }:
        return "gross_floor_area"
    if basis in {
        "per_m2_wall",
        "hours_per_m2_wall",
        "eur_per_m2_wall",
        "days_per_m2_wall",
    }:
        return "wall_surface"
    if basis in {"per_m2_roof_area", "hours_per_m2_roof_area", "eur_per_m2_roof_area"}:
        return "roof_area"
    if basis in {
        "per_m2_opening_area",
        "hours_per_m2_opening_area",
        "eur_per_m2_opening_area",
        "days_per_m2_opening_area",
    }:
        return "opening_area"
    if basis in {
        "per_m2_finished_surface",
        "hours_per_m2_finished_surface",
        "eur_per_m2_finished_surface",
        "days_per_m2_finished_surface",
    }:
        return "finished_surface"
    if basis == "per_m3":
        return "derived_volume"
    if basis in {"calendar_days", "total_days"}:
        return "total_duration"
    if basis == "qualitative_label":
        return "qualitative"
    if basis == "distance_km":
        return "distance_km"
    if basis == "total_years":
        return "total_years"
    if basis == "count":
        return "count"
    return basis


def _quantity_for_stage(
    basis: str,
    stage: str,
    scenario: ScenarioInput,
) -> float | None:
    pipeline_scenario = normalized_pipeline.ScenarioInput(
        method=normalize_method_name(scenario.construction_method),
        area_m2=scenario.area_m2,
        floors=scenario.number_of_floors,
        sub_method=_prefab_sub_method_for_scenario(
            scenario.construction_method,
            scenario.selected_material,
        ),
        selected_material=scenario.selected_material,
    )
    rules = normalized_pipeline.load_normalization_rules()
    quantity, _warning = normalized_pipeline.quantity_for_basis(
        basis,
        pipeline_scenario,
        rules,
    )
    if quantity is None:
        return None
    return _round_or_none(quantity * _shape_factor_multiplier(stage, scenario))


def _row_sort_key(row: dict[str, Any]) -> tuple[int, int]:
    primary = 0 if row.get("metadata", {}).get("primary") else 1
    source_penalty = 1 if row.get("source_key") == "unknown_import" else 0
    return (primary, source_penalty)


def _select_row_by_metric(
    rows: list[dict[str, Any]],
    preferred_metrics: tuple[str, ...],
) -> dict[str, Any] | None:
    exact_matches = [row for row in rows if row["metric"] in preferred_metrics]
    if exact_matches:
        return sorted(exact_matches, key=_row_sort_key)[0]
    return None


def _select_row_by_unit(
    rows: list[dict[str, Any]],
    unit: str,
) -> dict[str, Any] | None:
    matches = [row for row in rows if row.get("unit") == unit]
    if not matches:
        return None
    return sorted(matches, key=_row_sort_key)[0]


def _select_text_row(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    matches = [
        row
        for row in rows
        if row.get("unit") == "label"
        or row.get("metric", "").startswith("material_origin")
    ]
    if not matches:
        return None
    return sorted(matches, key=_row_sort_key)[0]


def _selected_metric_rows(
    stage_rows: list[dict[str, Any]],
) -> dict[str, dict[str, Any] | None]:
    selections: dict[str, dict[str, Any] | None] = {}
    for metric_key, spec in NUMERIC_METRIC_SPECS.items():
        row = _select_row_by_metric(stage_rows, spec["preferred_metrics"])
        if row is None:
            row = _select_row_by_unit(stage_rows, spec["unit"])
        selections[metric_key] = row
    selections["material_origin"] = _select_text_row(stage_rows)
    return selections


def _numeric_entry(
    selected_row: dict[str, Any] | None,
    stage: str,
    scenario: ScenarioInput,
    fallback_unit: str,
) -> dict[str, Any]:
    if selected_row is None:
        return {
            "low": None,
            "high": None,
            "unit": fallback_unit,
            "source_unit": None,
            "sources": [],
            "assumptions": [],
            "missing": True,
        }

    row = _apply_shape_factor_to_row(selected_row, stage, scenario)
    return {
        "low": _round_or_none(_to_float(row.get("scaled_low"))),
        "high": _round_or_none(_to_float(row.get("scaled_high"))),
        "unit": row.get("unit", fallback_unit),
        "source_unit": row.get("basis"),
        "sources": [row.get("source_key")] if row.get("source_key") else [],
        "assumptions": [row.get("notes")] if row.get("notes") else [],
        "missing": False,
        "selected_metric": row.get("metric"),
    }


def _text_entry(selected_row: dict[str, Any] | None) -> dict[str, Any]:
    if selected_row is None:
        return {
            "low": None,
            "high": None,
            "summary": "unknown",
            "sources": [],
            "assumptions": [],
            "missing": True,
        }

    low = selected_row.get("raw_low")
    high = selected_row.get("raw_high")
    low_values = [str(low)] if low not in (None, "null", "") else []
    high_values = [str(high)] if high not in (None, "null", "") else []
    summary_parts = sorted(set(low_values + high_values))
    summary = " / ".join(summary_parts) if summary_parts else "unknown"
    return {
        "low": low_values or None,
        "high": high_values or None,
        "summary": summary,
        "sources": [selected_row.get("source_key")] if selected_row.get("source_key") else [],
        "assumptions": [selected_row.get("notes")] if selected_row.get("notes") else [],
        "missing": False,
        "selected_metric": selected_row.get("metric"),
    }


def _extra_stage_rows(
    stage_rows: list[dict[str, Any]],
    selected_rows: dict[str, dict[str, Any] | None],
) -> list[dict[str, Any]]:
    selected_ids = {id(row) for row in selected_rows.values() if row is not None}
    extras = []
    for row in stage_rows:
        if id(row) in selected_ids:
            continue
        extras.append(
            {
                "metric": row.get("metric"),
                "unit": row.get("unit"),
                "basis": row.get("basis"),
                "source_key": row.get("source_key"),
                "scaled_low": row.get("scaled_low"),
                "scaled_high": row.get("scaled_high"),
                "notes": row.get("notes"),
                "primary": row.get("metadata", {}).get("primary", False),
            }
        )
    return extras


def _stage_breakdown(
    output: dict[str, Any],
    scenario: ScenarioInput,
) -> dict[str, dict[str, Any]]:
    breakdown: dict[str, dict[str, Any]] = {}
    data_model = output["data_model"]

    for stage in output["stages"]:
        stage_rows = output["stage_data"].get(stage, [])
        selected_rows = _selected_metric_rows(stage_rows)

        quantity_row = next(
            (row for row in selected_rows.values() if row and row.get("basis")),
            None,
        )
        quantity_basis = quantity_row.get("basis") if quantity_row else None
        quantity_value = (
            _quantity_for_stage(quantity_basis, stage, scenario)
            if quantity_basis
            else None
        )

        breakdown[stage] = {
            "phase_quantity_m2": quantity_value,
            "quantity_mode": _unit_quantity_mode(quantity_basis) if quantity_basis else None,
            "co2_kg_per_m2": _numeric_entry(
                selected_rows["co2_kg_per_m2"],
                stage,
                scenario,
                "kg CO2eq",
            ),
            "labor_hours_per_m2": _numeric_entry(
                selected_rows["labor_hours_per_m2"],
                stage,
                scenario,
                "hours",
            ),
            "time_days": _numeric_entry(
                selected_rows["time_days"],
                stage,
                scenario,
                "days",
            ),
            "cost_eur_per_m2": _numeric_entry(
                selected_rows["cost_eur_per_m2"],
                stage,
                scenario,
                "EUR",
            ),
            "material_origin": _text_entry(selected_rows["material_origin"]),
            "stage_label": stage,
            "stage_kind": "lifecycle_stage" if data_model == "lifecycle_based" else "phase",
            "extra_metrics": _extra_stage_rows(stage_rows, selected_rows),
        }

    return breakdown


def _stage_label(stage: str, stage_kind: str) -> str:
    if stage_kind == "lifecycle_stage":
        return LIFECYCLE_LABELS.get(stage, stage)
    return PHASE_LABELS.get(stage, _humanize_token(stage))


def _resolve_active_stage(
    stage_sequence: list[str],
    requested_stage: str | None,
) -> dict[str, Any]:
    if not stage_sequence:
        return {
            "requested_stage": requested_stage,
            "resolved_stage": None,
            "selection_mode": "none_available",
        }

    requested = (requested_stage or "").strip()
    if requested:
        for stage in stage_sequence:
            if stage == requested:
                return {
                    "requested_stage": requested_stage,
                    "resolved_stage": stage,
                    "selection_mode": "explicit",
                }
        requested_normalized = requested.lower().replace(" ", "_")
        for stage in stage_sequence:
            stage_normalized = stage.lower().replace(" ", "_")
            if stage_normalized == requested_normalized:
                return {
                    "requested_stage": requested_stage,
                    "resolved_stage": stage,
                    "selection_mode": "normalized_match",
                }
        return {
            "requested_stage": requested_stage,
            "resolved_stage": stage_sequence[0],
            "selection_mode": "unmatched_default_first",
        }

    return {
        "requested_stage": requested_stage,
        "resolved_stage": stage_sequence[0],
        "selection_mode": "default_first",
    }


def _midpoint(metric_entry: dict[str, Any]) -> float | None:
    low = metric_entry.get("low")
    high = metric_entry.get("high")
    if low is None or high is None:
        return None
    return _round_or_none((float(low) + float(high)) / 2.0)


def _stage_entry_warnings(stage_entry: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    for metric_key in (
        "co2_kg_per_m2",
        "cost_eur_per_m2",
        "time_days",
        "labor_hours_per_m2",
        "material_origin",
    ):
        if stage_entry[metric_key]["missing"]:
            warnings.append(f"missing_{metric_key}")
    return warnings


def _stage_summary(
    stage: str,
    stage_entry: dict[str, Any],
    is_active: bool,
) -> dict[str, Any]:
    return {
        "stage": stage,
        "label": _stage_label(stage, stage_entry["stage_kind"]),
        "stage_kind": stage_entry["stage_kind"],
        "is_active": is_active,
        "quantity_mode": stage_entry["quantity_mode"],
        "phase_quantity_m2": stage_entry["phase_quantity_m2"],
        "co2": stage_entry["co2_kg_per_m2"],
        "cost": stage_entry["cost_eur_per_m2"],
        "time": stage_entry["time_days"],
        "labor": stage_entry["labor_hours_per_m2"],
        "material_origin": stage_entry["material_origin"],
        "co2_total": _midpoint(stage_entry["co2_kg_per_m2"]),
        "cost_total": _midpoint(stage_entry["cost_eur_per_m2"]),
        "time_days": _midpoint(stage_entry["time_days"]),
        "labor_hours": _midpoint(stage_entry["labor_hours_per_m2"]),
        "warnings": _stage_entry_warnings(stage_entry),
        "extra_metrics": stage_entry["extra_metrics"],
    }


def _stage_summaries(
    stage_breakdown: dict[str, dict[str, Any]],
    active_stage_key: str | None,
) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for stage, stage_entry in stage_breakdown.items():
        summaries.append(
            _stage_summary(stage, stage_entry, is_active=(stage == active_stage_key))
        )
    return summaries


def _available_sub_method_options(output: dict[str, Any]) -> list[dict[str, str]]:
    options = []
    for sub_method in output.get("available_sub_methods", []):
        label = "CLT" if sub_method == "clt" else _humanize_token(sub_method)
        options.append({"key": sub_method, "label": label})
    return options


def _sum_numeric_stage_values(
    stage_breakdown: dict[str, dict[str, Any]],
    metric_key: str,
) -> dict[str, Any]:
    total_low = 0.0
    total_high = 0.0
    sources: list[str] = []
    assumptions: list[str] = []
    missing_stages: list[str] = []
    units: list[str] = []

    for stage, stage_entry in stage_breakdown.items():
        metric_entry = stage_entry[metric_key]
        if metric_entry["low"] is None or metric_entry["high"] is None:
            missing_stages.append(stage)
            continue
        total_low += metric_entry["low"]
        total_high += metric_entry["high"]
        sources.extend(metric_entry["sources"])
        assumptions.extend(metric_entry["assumptions"])
        if metric_entry["unit"]:
            units.append(metric_entry["unit"])

    return {
        "low": _round_or_none(total_low),
        "high": _round_or_none(total_high),
        "unit": units[0] if units else None,
        "sources": sorted(set(sources)),
        "assumptions": sorted(set(assumptions)),
        "missing_phases": missing_stages,
        "is_partial": bool(missing_stages),
    }


def _summarize_material_origin(
    stage_breakdown: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    summary_values: list[str] = []
    by_phase: dict[str, str] = {}
    sources: list[str] = []

    for stage, stage_entry in stage_breakdown.items():
        material_entry = stage_entry["material_origin"]
        by_phase[stage] = material_entry["summary"]
        if not material_entry["missing"]:
            if material_entry["low"]:
                summary_values.extend(material_entry["low"])
            if material_entry["high"]:
                summary_values.extend(material_entry["high"])
            sources.extend(material_entry["sources"])

    return {
        "summary": " / ".join(sorted(set(summary_values))) if summary_values else "unknown",
        "by_phase": by_phase,
        "sources": sorted(set(sources)),
    }


def _coverage_report(
    stage_breakdown: dict[str, dict[str, Any]],
    fallback_used: bool,
) -> dict[str, Any]:
    expected_keys = [
        f"{stage}:{metric}"
        for stage in stage_breakdown
        for metric in SUMMARY_METRIC_KEYS
    ]
    populated_keys: list[str] = []
    missing_keys: list[str] = []

    for stage, stage_entry in stage_breakdown.items():
        for metric in SUMMARY_METRIC_KEYS:
            entry = stage_entry[metric]
            key = f"{stage}:{metric}"
            if entry["missing"]:
                missing_keys.append(key)
            else:
                populated_keys.append(key)

    total_expected = len(expected_keys)
    total_populated = len(populated_keys)
    row_coverage = total_populated / total_expected if total_expected else 0.0

    if fallback_used:
        status = "fallback"
    elif missing_keys:
        status = "partial"
    else:
        status = "ok"

    return {
        "status": status,
        "row_coverage": round(row_coverage, 3),
        "populated_keys": populated_keys,
        "missing_keys": missing_keys,
        "total_expected": total_expected,
        "total_populated": total_populated,
        "fallback_used": fallback_used,
    }


def _data_status(output: dict[str, Any], coverage: dict[str, Any]) -> str:
    warnings = set(output.get("warnings", []))
    if "using_dev_fallback" in warnings or coverage["fallback_used"]:
        return "fallback"
    if any(
        warning == "unknown_source_key"
        or warning.startswith("missing_normalized_data")
        or warning.startswith("unsupported_basis")
        or warning.startswith("unexpected_stage")
        for warning in warnings
    ):
        return "partial"
    return coverage["status"]


def _prefab_sub_method(output: dict[str, Any]) -> str | None:
    sub_method = output.get("sub_method")
    return sub_method if isinstance(sub_method, str) else None


def _calculate_revenue_and_profit(
    scenario: ScenarioInput,
    total_cost: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    gross_floor_area = max(0.0, scenario.area_m2) * max(1, scenario.number_of_floors)
    revenue = None
    profit = None

    if scenario.sales_price_per_m2 is not None:
        value = gross_floor_area * scenario.sales_price_per_m2
        revenue = {
            "low": _round_or_none(value),
            "high": _round_or_none(value),
            "unit": "EUR",
            "mode": "sale",
        }
    elif scenario.rental_price_per_m2 is not None and scenario.rent_months:
        value = gross_floor_area * scenario.rental_price_per_m2 * scenario.rent_months
        revenue = {
            "low": _round_or_none(value),
            "high": _round_or_none(value),
            "unit": "EUR",
            "mode": "rent",
        }

    if revenue and total_cost["low"] is not None and total_cost["high"] is not None:
        profit = {
            "low": _round_or_none(revenue["low"] - total_cost["high"]),
            "high": _round_or_none(revenue["high"] - total_cost["low"]),
            "unit": "EUR",
        }

    return revenue, profit


def _normalized_dataset_path(method_name: str) -> str:
    return str(METHODS_ROOT / METHOD_FILE_MAP[method_name])


def compute_metrics(
    scenario: ScenarioInput | dict[str, Any],
    methods_root: Path = METHODS_ROOT,
    allow_fallback: bool = True,
) -> dict[str, Any]:
    del methods_root, allow_fallback  # compatibility placeholders

    scenario_input = _scenario_from_any(scenario)
    method_name = normalize_method_name(scenario_input.construction_method)
    sub_method = _prefab_sub_method_for_scenario(
        scenario_input.construction_method,
        scenario_input.selected_material,
    )

    output = normalized_pipeline.build_method_output(
        method=method_name,
        area_m2=scenario_input.area_m2,
        floors=scenario_input.number_of_floors,
        sub_method=sub_method,
        selected_material=scenario_input.selected_material,
    )

    stage_breakdown = _stage_breakdown(output, scenario_input)
    stage_sequence = list(output.get("stages", []))
    stage_selection = _resolve_active_stage(stage_sequence, scenario_input.current_phase)
    stage_summaries = _stage_summaries(
        stage_breakdown,
        active_stage_key=stage_selection["resolved_stage"],
    )
    active_stage_summary = next(
        (
            summary
            for summary in stage_summaries
            if summary["stage"] == stage_selection["resolved_stage"]
        ),
        None,
    )
    total_co2 = _sum_numeric_stage_values(stage_breakdown, "co2_kg_per_m2")
    total_labor = _sum_numeric_stage_values(stage_breakdown, "labor_hours_per_m2")
    total_time = _sum_numeric_stage_values(stage_breakdown, "time_days")
    total_cost = _sum_numeric_stage_values(stage_breakdown, "cost_eur_per_m2")
    material_origin = _summarize_material_origin(stage_breakdown)

    fallback_used = "using_dev_fallback" in output.get("warnings", [])
    confidence_range = _coverage_report(stage_breakdown, fallback_used)
    data_status = _data_status(output, confidence_range)
    revenue, profit = _calculate_revenue_and_profit(scenario_input, total_cost)
    resolved_sub_method = _prefab_sub_method(output)

    warnings = list(output.get("warnings", []))
    if scenario_input.selected_material:
        warnings.append(
            "selected_material is recorded in the scenario trace but does not yet alter lookup values. Material-variant CSV logic is still pending."
        )
    if scenario_input.shape_factor and scenario_input.shape_factor != 1.0:
        warnings.append(
            "shape_factor is still applied as a TD-side compatibility multiplier for structure and openings until the geometry-driven model is ported."
        )

    result = {
        "computed_at_ms": int(time.time() * 1000),
        "scenario": asdict(scenario_input),
        "dataset_path": _normalized_dataset_path(method_name),
        "data_status": data_status,
        "fallback_used": fallback_used,
        "confidence_range": {
            **confidence_range,
            "confidence_min": output.get("source_quality", {}).get("confidence_min"),
            "confidence_max": output.get("source_quality", {}).get("confidence_max"),
        },
        "phase_breakdown": stage_breakdown,
        "stage_sequence": stage_sequence,
        "stage_labels": {
            stage: _stage_label(stage, stage_breakdown[stage]["stage_kind"])
            for stage in stage_sequence
            if stage in stage_breakdown
        },
        "stage_selection": stage_selection,
        "active_stage": active_stage_summary,
        "stage_summaries": stage_summaries,
        "path_label": (
            "Lifecycle Path"
            if output.get("data_model") == "lifecycle_based"
            else "Phase Path"
        ),
        "phase_navigation_enabled": output.get("data_model") != "lifecycle_based",
        "data_model": output.get("data_model"),
        "display_mode": output.get("display_mode"),
        "sub_method": resolved_sub_method,
        "sub_method_label": (
            "CLT"
            if resolved_sub_method == "clt"
            else _humanize_token(resolved_sub_method)
            if resolved_sub_method
            else None
        ),
        "available_sub_methods": _available_sub_method_options(output),
        "selected_material": output.get("selected_material"),
        "source_quality": output.get("source_quality"),
        "co2_estimate": total_co2,
        "labor_hours": total_labor,
        "construction_time": total_time,
        "cost_estimate": total_cost,
        "material_origin": material_origin,
        "revenue_estimate": revenue,
        "profit_estimate": profit,
        "warnings": sorted(set(warnings)),
    }
    return result


def scenario_from_touchdesigner(owner: Any | None = None) -> dict[str, Any]:
    if owner is None:
        try:
            owner = parent()
        except NameError as exc:  # pragma: no cover - only meaningful inside TD
            raise RuntimeError("TouchDesigner owner not available outside TD.") from exc

    return {
        "construction_method": owner.fetch("current_method", None),
        "area_m2": owner.fetch("area_m2", 0.0),
        "number_of_floors": owner.fetch("number_of_floors", 1),
        "shape_factor": owner.fetch("shape_factor", 1.0),
        "selected_material": owner.fetch("selected_material", None),
        "selected_program": owner.fetch("selected_program", None),
        "current_phase": owner.fetch("current_phase_name", None),
        "sales_price_per_m2": owner.fetch("sales_price_per_m2", None),
        "rental_price_per_m2": owner.fetch("rental_price_per_m2", None),
        "rent_months": owner.fetch("rent_months", None),
    }


def compute_and_store_touchdesigner(
    owner: Any | None = None,
    scenario: dict[str, Any] | None = None,
    methods_root: Path = METHODS_ROOT,
    allow_fallback: bool = True,
) -> dict[str, Any]:
    if owner is None:
        try:
            owner = parent()
        except NameError as exc:  # pragma: no cover - only meaningful inside TD
            raise RuntimeError("TouchDesigner owner not available outside TD.") from exc

    payload = scenario or scenario_from_touchdesigner(owner)
    result = compute_metrics(payload, methods_root=methods_root, allow_fallback=allow_fallback)
    owner.store("metrics_output", result)
    owner.store("metrics_timestamp", result["computed_at_ms"])
    owner.store("data_status", result["data_status"])
    owner.store("material_origin_summary", result["material_origin"]["summary"])
    return result


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Hardware III metrics engine.")
    parser.add_argument("--method", required=True, help="masonry, 3d_printed, prefab, reclaimed_brick")
    parser.add_argument("--area", type=float, required=True, help="Footprint area in square meters")
    parser.add_argument("--floors", type=int, default=1, help="Number of floors")
    parser.add_argument("--shape-factor", type=float, default=1.0, help="Envelope complexity multiplier")
    parser.add_argument("--material", default=None, help="Selected material token")
    parser.add_argument("--program", default=None, help="Selected program token")
    parser.add_argument("--phase", default=None, help="Current phase name")
    parser.add_argument("--sale-price", type=float, default=None, help="Sale price per m2")
    parser.add_argument("--rent-price", type=float, default=None, help="Rent price per m2 per month")
    parser.add_argument("--rent-months", type=int, default=None, help="Months used for rental revenue estimate")
    parser.add_argument(
        "--no-fallback",
        action="store_true",
        help="Compatibility flag. Normalized pipeline now handles fallback internally.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    scenario = {
        "construction_method": args.method,
        "area_m2": args.area,
        "number_of_floors": args.floors,
        "shape_factor": args.shape_factor,
        "selected_material": args.material,
        "selected_program": args.program,
        "current_phase": args.phase,
        "sales_price_per_m2": args.sale_price,
        "rental_price_per_m2": args.rent_price,
        "rent_months": args.rent_months,
    }
    result = compute_metrics(scenario, allow_fallback=not args.no_fallback)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
