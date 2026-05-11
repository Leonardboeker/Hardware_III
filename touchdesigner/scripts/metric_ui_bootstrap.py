"""Bootstrap a 1280x720 TouchDesigner network for the metrics UI.

Usage inside TouchDesigner:
1. Add a Text DAT named ``bootstrap_metric_ui``
2. Paste this file and enable Module ON
3. Run ``op('bootstrap_metric_ui').module.bootstrap_metric_ui()``
4. Optional: run ``op('bootstrap_metric_ui').module.seed_demo_state()``

The builder creates the current shared TD layout:
- Leo's 9-panel geometry at 1280x720
- normalized metrics engine module
- ui_state bridge
- text_<panel_id> TOPs
- callback DATs for compute_state, render_footprint, and lca_data

The builder is intentionally idempotent: running it again updates existing
nodes instead of duplicating them.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROJ_W = 1280
PROJ_H = 720
FALLBACK_REPO_ROOT = Path("O:/Hardware_III")

PANEL_LAYOUT = {
    "top_phase_navigation": (271, 15, 600, 67),
    "left_info": (17, 15, 213, 467),
    "left_assembly_sequence": (17, 493, 307, 173),
    "main_plan_simulation": (245, 108, 652, 373),
    "method_selection": (337, 493, 560, 173),
    "right_comparison": (910, 15, 353, 292),
    "right_cost_chart": (910, 321, 353, 160),
    "right_phase_preview": (910, 493, 353, 173),
    "bar_bottom_status": (0, 687, 1280, 33),
}

TEXT_TOP_SPECS = {
    "top_phase_navigation": {"font_size": 12, "alignx": "center", "aligny": "center"},
    "left_info": {"font_size": 15, "alignx": "left", "aligny": "top"},
    "left_assembly_sequence": {"font_size": 9, "alignx": "left", "aligny": "top"},
    "method_selection": {"font_size": 12, "alignx": "left", "aligny": "top"},
    "right_comparison": {"font_size": 15, "alignx": "left", "aligny": "top"},
    "right_cost_chart": {"font_size": 14, "alignx": "left", "aligny": "top"},
    "right_phase_preview": {"font_size": 14, "alignx": "left", "aligny": "top"},
    "bar_bottom_status": {"font_size": 8, "alignx": "center", "aligny": "center"},
}

TEXT_BLOCK_SPECS = {
    "left_info_hero": {"width": 181, "height": 94, "font_size": 11, "alignx": "left", "aligny": "top"},
    "left_info_details": {"width": 181, "height": 168, "font_size": 8, "alignx": "left", "aligny": "top"},
    "left_info_scale": {"width": 181, "height": 108, "font_size": 7, "alignx": "left", "aligny": "top"},
    "left_info_scale_minus": {"width": 24, "height": 24, "font_size": 10, "alignx": "center", "aligny": "center"},
    "left_info_scale_value": {"width": 44, "height": 24, "font_size": 10, "alignx": "center", "aligny": "center"},
    "left_info_scale_plus": {"width": 24, "height": 24, "font_size": 10, "alignx": "center", "aligny": "center"},
    "method_card_masonry": {"width": 164, "height": 102, "font_size": 8, "alignx": "left", "aligny": "top"},
    "method_card_3d_printed": {"width": 164, "height": 102, "font_size": 8, "alignx": "left", "aligny": "top"},
    "method_card_prefab": {"width": 164, "height": 102, "font_size": 7, "alignx": "left", "aligny": "top"},
    "right_comparison_summary": {"width": 321, "height": 54, "font_size": 8, "alignx": "left", "aligny": "top"},
    "right_comparison_metrics": {"width": 321, "height": 162, "font_size": 7, "alignx": "left", "aligny": "top"},
    "right_cost_scope": {"width": 96, "height": 28, "font_size": 6, "alignx": "left", "aligny": "center"},
    "right_cost_hero": {"width": 321, "height": 40, "font_size": 9, "alignx": "left", "aligny": "center"},
    "right_cost_grid_left": {"width": 152, "height": 52, "font_size": 5.8, "alignx": "left", "aligny": "top"},
    "right_cost_grid_right": {"width": 153, "height": 52, "font_size": 5.8, "alignx": "left", "aligny": "top"},
    "right_phase_preview_state": {"width": 321, "height": 40, "font_size": 7.2, "alignx": "left", "aligny": "center"},
    "right_phase_preview_left": {"width": 152, "height": 58, "font_size": 5.8, "alignx": "left", "aligny": "top"},
    "right_phase_preview_right": {"width": 153, "height": 58, "font_size": 5.8, "alignx": "left", "aligny": "top"},
}

SCRIPT_SOURCES = {
    "metrics_engine": "touchdesigner/scripts/metrics_engine.py",
    "ui_state": "touchdesigner/scripts/ui_state.py",
    "compute_state_callbacks": "touchdesigner/scripts/state_chop_v1.py",
    "render_footprint_callbacks": "touchdesigner/scripts/footprint_viz_v5.py",
    "lca_data_callbacks": "touchdesigner/scripts/lca_data_reader.py",
    "rfid_serial_callbacks": "touchdesigner/scripts/serial_rfid_v1.py",
    "vision2_state_callbacks": "touchdesigner/scripts/vision2_state_chop.py",
}

METHOD_FLOOR_CONSTRAINTS = {
    "masonry": {
        "min_floors": 1,
        "max_floors": 5,
        "default_floors": 2,
        "floor_height_m": 3.2,
        "label": "Masonry",
        "user_note": "Low-rise masonry assumption.",
    },
    "3d_printed": {
        "min_floors": 1,
        "max_floors": 2,
        "default_floors": 1,
        "floor_height_m": 3.2,
        "label": "3D Printed",
        "user_note": "Limited to low-rise 3D printed construction in this prototype.",
    },
    "prefab_clt": {
        "min_floors": 1,
        "max_floors": 8,
        "default_floors": 3,
        "floor_height_m": 3.2,
        "label": "CLT / Timber Prefab",
        "user_note": "Mid-rise prefab timber assumption.",
    },
    "prefab_modular_concrete": {
        "min_floors": 1,
        "max_floors": 12,
        "default_floors": 4,
        "floor_height_m": 3.2,
        "label": "Modular Concrete Prefab",
        "user_note": "Higher floor range for modular concrete prefab in this prototype.",
    },
}

PREFAB_SUB_METHOD_MATERIALS = {
    "clt": "timber_clt_prefab",
    "modular_concrete": "modular_concrete_prefab",
}


@dataclass(frozen=True)
class NodeSpec:
    name: str
    td_type: str
    node_x: int
    node_y: int


NETWORK_SPECS = (
    NodeSpec("vision_in", "oscinCHOP", -900, 40),
    NodeSpec("rfid_in", "constantCHOP", -900, 180),
    NodeSpec("compute_state", "scriptCHOP", -620, 40),
    NodeSpec("compute_state_callbacks", "textDAT", -620, 190),
    NodeSpec("lca_data", "scriptDAT", -620, 330),
    NodeSpec("lca_data_callbacks", "textDAT", -620, 470),
    NodeSpec("metrics_engine", "textDAT", -310, -70),
    NodeSpec("ui_state", "textDAT", -310, 70),
    NodeSpec("refresh_metrics_ui", "textDAT", -310, 210),
    NodeSpec("render_footprint", "scriptTOP", 40, 40),
    NodeSpec("render_footprint_callbacks", "textDAT", 40, 210),
    NodeSpec("projector_out", "windowCOMP", 350, 40),
    NodeSpec("rfid_serial_callbacks", "textDAT", -900, 330),
    NodeSpec("vision2_state_callbacks", "textDAT", -900, 470),
)


def text_top_name(panel_id: str) -> str:
    return f"text_{panel_id}"


def panel_text_expression() -> str:
    return 'parent().fetch(me.name, "")'


def bootstrap_manifest() -> dict[str, Any]:
    return {
        "resolution": (PROJ_W, PROJ_H),
        "panels": PANEL_LAYOUT,
        "text_tops": [
            {
                "name": text_top_name(panel_id),
                "panel_id": panel_id,
                "bounds": PANEL_LAYOUT[panel_id],
                **TEXT_TOP_SPECS[panel_id],
            }
            for panel_id in TEXT_TOP_SPECS
        ],
        "text_block_tops": [
            {
                "name": text_top_name(block_id),
                "block_id": block_id,
                **TEXT_BLOCK_SPECS[block_id],
            }
            for block_id in TEXT_BLOCK_SPECS
        ],
        "nodes": [spec.__dict__ for spec in NETWORK_SPECS],
    }


def refresh_metrics_module_text() -> str:
    return """\"\"\"Refresh helper for metrics + ui_state inside TouchDesigner.\"\"\"
def refresh(owner=None):
    if owner is None:
        owner = parent()
    owner.op('metrics_engine').module.compute_and_store_touchdesigner(owner=owner)
    owner.op('ui_state').module.compute_and_store_touchdesigner_ui(owner=owner)
    return owner.fetch('ui_state', {})
"""


def _resolve_owner(owner: Any | None) -> Any:
    if owner is None:
        try:
            owner = parent()
        except NameError as exc:  # pragma: no cover - TD only
            raise RuntimeError("TouchDesigner owner not available outside TD.") from exc
    return owner


def _discover_repo_root() -> Path:
    try:  # pragma: no branch - TD only
        start = Path(project.folder).resolve()
    except NameError:
        return FALLBACK_REPO_ROOT if FALLBACK_REPO_ROOT.exists() else Path.cwd()

    candidates = [start, *start.parents]
    for candidate in candidates:
        if (candidate / "data" / "methods_db.json").exists():
            return candidate
    if FALLBACK_REPO_ROOT.exists():
        return FALLBACK_REPO_ROOT
    return start


def _read_repo_text(relative_path: str) -> str:
    repo_root = _discover_repo_root()
    path = repo_root / relative_path
    return path.read_text(encoding="utf-8")


def _get_or_create(owner: Any, type_name: str, name: str) -> Any:
    node = owner.op(name)
    if node is not None:
        return node
    try:
        return owner.create(type_name, name)
    except Exception as exc:  # pragma: no cover - TD only
        raise RuntimeError(
            f"TouchDesigner could not create operator type '{type_name}'."
        ) from exc


def _set_par_value(node: Any, par_name: str, value: Any) -> bool:
    parameter = getattr(node.par, par_name, None)
    if parameter is None:
        return False
    try:
        parameter.val = value
        return True
    except Exception:
        pass
    try:
        parameter.expr = repr(value)
        return True
    except Exception:
        return False


def _set_par_expr(node: Any, par_name: str, expression: str) -> bool:
    parameter = getattr(node.par, par_name, None)
    if parameter is None:
        return False
    try:
        parameter.expr = expression
        return True
    except Exception:
        return False


def _set_any_par_value(node: Any, par_names: tuple[str, ...], value: Any) -> bool:
    for par_name in par_names:
        if _set_par_value(node, par_name, value):
            return True
    return False


def _apply_node_position(node: Any, node_x: int, node_y: int) -> None:
    try:
        node.nodeX = node_x
        node.nodeY = node_y
    except Exception:
        pass


def _set_dat_text(node: Any, text: str) -> None:
    try:
        node.text = text
    except Exception as exc:  # pragma: no cover - TD only
        raise RuntimeError(f"Could not write text into DAT '{node.name}': {exc}") from exc


def _configure_text_dat_module(node: Any) -> None:
    _set_par_value(node, "module", True)
    _set_par_value(node, "language", "python")


def _configure_vision_in(node: Any) -> None:
    _set_par_value(node, "port", 7000)
    _set_par_value(node, "active", True)
    _set_par_value(node, "protocol", "udp")


def _configure_rfid_constant(node: Any) -> None:
    _set_par_value(node, "name0", "method_id")
    _set_par_value(node, "value0", 0)


def _bind_callbacks(script_node: Any, callbacks_dat_name: str) -> bool:
    for par_name in ("callbacksdat", "callbackdat", "callbacks"):
        if _set_par_value(script_node, par_name, callbacks_dat_name):
            return True
    return False


def _configure_script_top(node: Any) -> None:
    _set_par_value(node, "resolutionw", PROJ_W)
    _set_par_value(node, "resolutionh", PROJ_H)


def _configure_text_top(node: Any, panel_id: str) -> None:
    spec = TEXT_TOP_SPECS[panel_id]
    bounds = PANEL_LAYOUT[panel_id]
    _configure_text_like_node(
        node,
        width=bounds[2],
        height=bounds[3],
        font_size=spec["font_size"],
        alignx=spec["alignx"],
        aligny=spec["aligny"],
    )


def _configure_text_like_node(
    node: Any,
    *,
    width: int,
    height: int,
    font_size: int | float,
    alignx: str,
    aligny: str,
) -> None:
    _set_par_expr(node, "text", panel_text_expression())
    _set_any_par_value(node, ("resolutionw", "resw"), width)
    _set_any_par_value(node, ("resolutionh", "resh"), height)
    _set_any_par_value(node, ("fontsize", "fontsizex"), font_size)
    _set_any_par_value(node, ("fontsizey",), font_size)
    _set_any_par_value(node, ("keepfontratio",), True)
    _set_any_par_value(node, ("alignx", "horizontalalign"), alignx)
    _set_any_par_value(node, ("aligny", "verticalalign"), aligny)
    _set_any_par_value(node, ("wordwrap",), True)
    _set_any_par_value(node, ("bgcolorr",), 0.0)
    _set_any_par_value(node, ("bgcolorg",), 0.0)
    _set_any_par_value(node, ("bgcolorb",), 0.0)
    _set_any_par_value(node, ("bgcolora",), 0.0)
    _set_any_par_value(node, ("fontcolorr",), 0.96)
    _set_any_par_value(node, ("fontcolorg",), 0.94)
    _set_any_par_value(node, ("fontcolorb",), 0.90)
    _set_any_par_value(node, ("fontcolora",), 1.0)


def _configure_text_block_top(node: Any, block_id: str) -> None:
    spec = TEXT_BLOCK_SPECS[block_id]
    _configure_text_like_node(
        node,
        width=spec["width"],
        height=spec["height"],
        font_size=spec["font_size"],
        alignx=spec["alignx"],
        aligny=spec["aligny"],
    )


def bootstrap_metric_ui(owner: Any | None = None) -> dict[str, Any]:
    """Create or update the TouchDesigner network in the current component."""
    owner = _resolve_owner(owner)
    created = []
    updated = []
    notes = []

    for spec in NETWORK_SPECS:
        node = owner.op(spec.name)
        action = "updated" if node is not None else "created"
        node = _get_or_create(owner, spec.td_type, spec.name)
        _apply_node_position(node, spec.node_x, spec.node_y)
        if action == "created":
            created.append(spec.name)
        else:
            updated.append(spec.name)

    for dat_name, source_path in SCRIPT_SOURCES.items():
        dat_node = owner.op(dat_name)
        _set_dat_text(dat_node, _read_repo_text(source_path))
        if dat_name in {"metrics_engine", "ui_state"}:
            _configure_text_dat_module(dat_node)

    refresh_node = owner.op("refresh_metrics_ui")
    _set_dat_text(refresh_node, refresh_metrics_module_text())
    _configure_text_dat_module(refresh_node)

    _configure_vision_in(owner.op("vision_in"))
    _configure_rfid_constant(owner.op("rfid_in"))
    _configure_script_top(owner.op("render_footprint"))

    if not _bind_callbacks(owner.op("compute_state"), "compute_state_callbacks"):
        notes.append("Bind compute_state to compute_state_callbacks manually if needed.")
    if not _bind_callbacks(owner.op("render_footprint"), "render_footprint_callbacks"):
        notes.append("Bind render_footprint to render_footprint_callbacks manually if needed.")
    if not _bind_callbacks(owner.op("lca_data"), "lca_data_callbacks"):
        notes.append("Bind lca_data to lca_data_callbacks manually if needed.")

    text_top_base_x = 40
    text_top_base_y = 430
    text_gap_y = 110
    for index, panel_id in enumerate(TEXT_TOP_SPECS):
        name = text_top_name(panel_id)
        node = owner.op(name)
        action = "updated" if node is not None else "created"
        node = _get_or_create(owner, "textTOP", name)
        _apply_node_position(node, text_top_base_x + (index % 2) * 260, text_top_base_y + (index // 2) * text_gap_y)
        _configure_text_top(node, panel_id)
        if action == "created":
            created.append(name)
        else:
            updated.append(name)

    block_base_x = 620
    block_base_y = 430
    block_gap_y = 70
    for index, block_id in enumerate(TEXT_BLOCK_SPECS):
        name = text_top_name(block_id)
        node = owner.op(name)
        action = "updated" if node is not None else "created"
        node = _get_or_create(owner, "textTOP", name)
        _apply_node_position(
            node,
            block_base_x + (index % 3) * 230,
            block_base_y + (index // 3) * block_gap_y,
        )
        _configure_text_block_top(node, block_id)
        if action == "created":
            created.append(name)
        else:
            updated.append(name)

    notes.extend(
        [
            "Text TOPs read parent().fetch(me.name, '').",
            "Run op('refresh_metrics_ui').module.refresh() after changing owner storage.",
            "Wire render_footprint to projector_out inside TouchDesigner if it is not already linked.",
            "Replace rfid_in with a Serial DAT later and use rfid_serial_callbacks when hardware is ready.",
        ]
    )

    return {
        "created": created,
        "updated": updated,
        "notes": notes,
        "manifest": bootstrap_manifest(),
    }


def configure_text_tops_only(owner: Any | None = None) -> dict[str, Any]:
    """Re-apply text TOP sizes/fonts without touching the rest of the network."""
    owner = _resolve_owner(owner)
    created = []
    updated = []

    for panel_id in TEXT_TOP_SPECS:
        name = text_top_name(panel_id)
        node = owner.op(name)
        action = "updated" if node is not None else "created"
        node = _get_or_create(owner, "textTOP", name)
        _configure_text_top(node, panel_id)
        if action == "created":
            created.append(name)
        else:
            updated.append(name)

    for block_id in TEXT_BLOCK_SPECS:
        name = text_top_name(block_id)
        node = owner.op(name)
        action = "updated" if node is not None else "created"
        node = _get_or_create(owner, "textTOP", name)
        _configure_text_block_top(node, block_id)
        if action == "created":
            created.append(name)
        else:
            updated.append(name)

    return {"created": created, "updated": updated}


def _current_constraint_key(owner: Any) -> str | None:
    method_key = owner.fetch("current_method", None)
    selected_material = str(owner.fetch("selected_material", "") or "").lower()
    if method_key == "prefab":
        if "modular_concrete" in selected_material or "modular-concrete" in selected_material:
            return "prefab_modular_concrete"
        return "prefab_clt"
    if method_key in ("masonry", "3d_printed"):
        return method_key
    return None


def floor_constraint_summary(owner: Any | None = None) -> dict[str, Any]:
    owner = _resolve_owner(owner)
    constraint_key = _current_constraint_key(owner)
    if constraint_key is None:
        return {
            "constraint_key": None,
            "current_method": owner.fetch("current_method", None),
            "selected_material": owner.fetch("selected_material", None),
            "number_of_floors": owner.fetch("number_of_floors", 1),
        }

    constraint = METHOD_FLOOR_CONSTRAINTS[constraint_key]
    return {
        "constraint_key": constraint_key,
        "current_method": owner.fetch("current_method", None),
        "selected_material": owner.fetch("selected_material", None),
        "number_of_floors": owner.fetch("number_of_floors", 1),
        **constraint,
    }


def _refresh_and_render(owner: Any) -> None:
    refresh = owner.op("refresh_metrics_ui")
    if refresh is not None:
        try:
            refresh.module.refresh(owner=owner)
        except Exception:
            pass

    renderer = owner.op("render_footprint")
    if renderer is not None:
        try:
            renderer.cook(force=True)
        except Exception:
            pass


def set_floor_count(floor_count: int, owner: Any | None = None) -> dict[str, Any]:
    """Clamp and store floor count using the active method constraints."""
    owner = _resolve_owner(owner)
    requested = int(floor_count)
    summary = floor_constraint_summary(owner=owner)
    constraint_key = summary.get("constraint_key")

    min_floors = int(summary.get("min_floors", 1) or 1)
    max_floors = int(summary.get("max_floors", 12) or 12)
    floor_height_m = float(summary.get("floor_height_m", 3.2) or 3.2)

    clamped = max(min_floors, min(max_floors, requested))
    owner.store("number_of_floors", clamped)
    owner.store("floor_height_m", floor_height_m)
    owner.store("building_height_m", round(clamped * floor_height_m, 2))

    if requested != clamped and constraint_key is not None:
        owner.store(
            "floor_notice",
            f"Allowed range for {summary['label']}: {min_floors}-{max_floors} floors.",
        )
    else:
        owner.store("floor_notice", None)

    _refresh_and_render(owner)
    return {
        **floor_constraint_summary(owner=owner),
        "requested_floors": requested,
        "applied_floors": clamped,
        "clamped": requested != clamped,
        "building_height_m": owner.fetch("building_height_m", None),
    }


def step_floor_count(delta: int, owner: Any | None = None) -> dict[str, Any]:
    """Increment/decrement floors with clamping."""
    owner = _resolve_owner(owner)
    current_value = int(owner.fetch("number_of_floors", 1) or 1)
    return set_floor_count(current_value + int(delta), owner=owner)


def set_prefab_sub_method(sub_method: str, owner: Any | None = None) -> dict[str, Any]:
    """Switch prefab between CLT and modular concrete assumptions."""
    owner = _resolve_owner(owner)
    normalized = str(sub_method).strip().lower().replace("-", "_").replace(" ", "_")
    if normalized not in PREFAB_SUB_METHOD_MATERIALS:
        raise ValueError("sub_method must be 'clt' or 'modular_concrete'")

    owner.store("current_method", "prefab")
    owner.store("selected_material", PREFAB_SUB_METHOD_MATERIALS[normalized])
    owner.store("current_phase_name", "A1-A3")

    summary = floor_constraint_summary(owner=owner)
    default_floors = int(summary.get("default_floors", 3) or 3)
    current_value = int(owner.fetch("number_of_floors", default_floors) or default_floors)
    result = set_floor_count(current_value, owner=owner)
    if result["clamped"] and current_value <= 0:
        result = set_floor_count(default_floors, owner=owner)
    return {"sub_method": normalized, **result}


def set_current_phase(phase_name: str, owner: Any | None = None) -> dict[str, Any]:
    """Store a phase/lifecycle stage name and refresh the TD UI."""
    owner = _resolve_owner(owner)
    owner.store("current_phase_name", str(phase_name))
    _refresh_and_render(owner)
    return {
        "current_phase_name": owner.fetch("current_phase_name", None),
        "current_method": owner.fetch("current_method", None),
    }


def debug_set_method(method_id: int, owner: Any | None = None) -> dict[str, Any]:
    """Force a method selection for TD debugging without relying on a specific CHOP parameter name."""
    owner = _resolve_owner(owner)
    method_id = int(method_id)
    rfid = owner.op("rfid_in")
    if rfid is not None:
        try:
            rfid.store("method_id", method_id)
        except Exception:
            pass
        try:
            rfid["method_id"][0] = method_id
        except Exception:
            pass

    compute_state = owner.op("compute_state")
    if compute_state is not None:
        try:
            compute_state.cook(force=True)
        except Exception:
            pass

    summary = floor_constraint_summary(owner=owner)
    default_floors = int(summary.get("default_floors", owner.fetch("number_of_floors", 1) or 1) or 1)
    current_value = int(owner.fetch("number_of_floors", default_floors) or default_floors)
    set_floor_count(current_value if current_value > 0 else default_floors, owner=owner)

    return {
        "method_id": method_id,
        "current_method": owner.fetch("current_method", None),
        "selected_material": owner.fetch("selected_material", None),
        "current_phase_name": owner.fetch("current_phase_name", None),
        "number_of_floors": owner.fetch("number_of_floors", None),
    }


def seed_demo_state(owner: Any | None = None) -> dict[str, Any]:
    """Store a small demo scenario so the UI can be previewed immediately."""
    owner = _resolve_owner(owner)
    owner.store("current_method", "masonry")
    owner.store("area_m2", 68.0)
    owner.store("number_of_floors", 2)
    owner.store("current_phase_name", "finishing")
    owner.store("selected_material", "fired_clay_brick")
    owner.store("hb_alive", 1)
    owner.store("selected_part_label", "North Wing")
    owner.store("selected_parts_count", 1)
    return owner.op("refresh_metrics_ui").module.refresh(owner=owner)
