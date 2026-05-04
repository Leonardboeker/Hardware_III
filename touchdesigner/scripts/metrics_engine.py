"""CSV-ready metrics engine for the TouchDesigner construction exhibit.

This module is designed to be useful before the research CSV files arrive.

What it does today:
- Loads per-method CSV files from ``data/methods/`` when they exist.
- Falls back to a provisional development dataset when CSVs are still missing.
- Aggregates a scenario into CO2, labor, time, cost, revenue, profit, and
  material-origin outputs.
- Can be called from plain Python or from TouchDesigner storage ``fetch/store``.

What it does NOT assume:
- Final source values.
- Final material-variant logic.
- Final program/revenue model.

The goal is to lock the software contract now so the research group can drop in
real CSV files later without changing the engine API.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
METHODS_ROOT = REPO_ROOT / "data" / "methods"

PHASES = ("foundation", "structure", "roof", "openings", "finishing")
NUMERIC_PARAMETERS = (
    "co2_kg_per_m2",
    "labor_hours_per_m2",
    "time_days",
    "cost_eur_per_m2",
)
TEXT_PARAMETERS = ("material_origin",)
CSV_HEADER = (
    "phase",
    "parameter",
    "value_low",
    "value_high",
    "unit",
    "assumption",
    "source",
    "source_tier",
)

METHOD_FILE_MAP = {
    "masonry": "masonry.csv",
    "brick": "masonry.csv",
    "3d_printed": "3d-printed.csv",
    "3d-printed": "3d-printed.csv",
    "3dp": "3d-printed.csv",
    "concrete_3dp": "3d-printed.csv",
    "prefab": "prefab.csv",
    "prefab_timber": "prefab.csv",
    "clt": "prefab.csv",
    "reclaimed_brick": "reclaimed-brick.csv",
    "reclaimed-brick": "reclaimed-brick.csv",
}

PHASE_AREA_MODE = {
    "foundation": "footprint",
    "structure": "gross_floor_area",
    "roof": "footprint",
    "openings": "gross_floor_area",
    "finishing": "gross_floor_area",
}

TOTAL_UNITS = {
    "co2_kg_per_m2": "kg CO2eq",
    "labor_hours_per_m2": "hours",
    "time_days": "days",
    "cost_eur_per_m2": "EUR",
}


@dataclass
class MetricRow:
    phase: str
    parameter: str
    value_low: str
    value_high: str
    unit: str
    assumption: str
    source: str
    source_tier: str


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
    if normalized not in METHOD_FILE_MAP:
        known = ", ".join(sorted(set(METHOD_FILE_MAP)))
        raise ValueError(f"Unknown construction method '{method_name}'. Known: {known}")
    return normalized


def _to_float(value: str | float | int | None) -> float | None:
    if value is None:
        return None
    if isinstance(value, (float, int)):
        return float(value)
    text = str(value).strip()
    if not text or text.upper() == "UNKNOWN":
        return None
    return float(text)


def _round_or_none(value: float | None, digits: int = 2) -> float | None:
    if value is None:
        return None
    return round(value, digits)


def _scenario_from_any(scenario: ScenarioInput | dict[str, Any]) -> ScenarioInput:
    if isinstance(scenario, ScenarioInput):
        return scenario
    payload = dict(scenario)
    payload["construction_method"] = normalize_method_name(payload.get("construction_method"))
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


def _dev_row(
    phase: str,
    parameter: str,
    low: str | float,
    high: str | float,
    unit: str,
    assumption: str,
) -> MetricRow:
    return MetricRow(
        phase=phase,
        parameter=parameter,
        value_low=str(low),
        value_high=str(high),
        unit=unit,
        assumption=assumption,
        source="dev-fallback",
        source_tier="dev",
    )


def _build_dev_fallback_rows(method_name: str) -> list[MetricRow]:
    method_key = normalize_method_name(method_name)
    structure_values = {
        "masonry": {
            "co2_kg_per_m2": (150, 250, "kg CO2eq/m2"),
            "labor_hours_per_m2": (4, 8, "hours/m2"),
            "time_days": (0.05, 0.10, "days/m2"),
            "cost_eur_per_m2": (80, 140, "EUR/m2"),
            "material_origin": ("local", "local", "label"),
        },
        "brick": {
            "co2_kg_per_m2": (150, 250, "kg CO2eq/m2"),
            "labor_hours_per_m2": (4, 8, "hours/m2"),
            "time_days": (0.05, 0.10, "days/m2"),
            "cost_eur_per_m2": (80, 140, "EUR/m2"),
            "material_origin": ("local", "local", "label"),
        },
        "3d_printed": {
            "co2_kg_per_m2": (60, 150, "kg CO2eq/m2"),
            "labor_hours_per_m2": (0.5, 2.0, "hours/m2"),
            "time_days": (0.03, 0.15, "days/m2"),
            "cost_eur_per_m2": (90, 160, "EUR/m2"),
            "material_origin": ("regional", "global", "label"),
        },
        "3d-printed": {
            "co2_kg_per_m2": (60, 150, "kg CO2eq/m2"),
            "labor_hours_per_m2": (0.5, 2.0, "hours/m2"),
            "time_days": (0.03, 0.15, "days/m2"),
            "cost_eur_per_m2": (90, 160, "EUR/m2"),
            "material_origin": ("regional", "global", "label"),
        },
        "3dp": {
            "co2_kg_per_m2": (60, 150, "kg CO2eq/m2"),
            "labor_hours_per_m2": (0.5, 2.0, "hours/m2"),
            "time_days": (0.03, 0.15, "days/m2"),
            "cost_eur_per_m2": (90, 160, "EUR/m2"),
            "material_origin": ("regional", "global", "label"),
        },
        "concrete_3dp": {
            "co2_kg_per_m2": (60, 150, "kg CO2eq/m2"),
            "labor_hours_per_m2": (0.5, 2.0, "hours/m2"),
            "time_days": (0.03, 0.15, "days/m2"),
            "cost_eur_per_m2": (90, 160, "EUR/m2"),
            "material_origin": ("regional", "global", "label"),
        },
        "prefab": {
            "co2_kg_per_m2": (130, 200, "kg CO2eq/m2"),
            "labor_hours_per_m2": (1, 3, "hours/m2"),
            "time_days": (0.01, 0.05, "days/m2"),
            "cost_eur_per_m2": (120, 180, "EUR/m2"),
            "material_origin": ("regional", "global", "label"),
        },
        "prefab_timber": {
            "co2_kg_per_m2": (130, 200, "kg CO2eq/m2"),
            "labor_hours_per_m2": (1, 3, "hours/m2"),
            "time_days": (0.01, 0.05, "days/m2"),
            "cost_eur_per_m2": (120, 180, "EUR/m2"),
            "material_origin": ("regional", "global", "label"),
        },
        "clt": {
            "co2_kg_per_m2": (130, 200, "kg CO2eq/m2"),
            "labor_hours_per_m2": (1, 3, "hours/m2"),
            "time_days": (0.01, 0.05, "days/m2"),
            "cost_eur_per_m2": (120, 180, "EUR/m2"),
            "material_origin": ("regional", "global", "label"),
        },
        "reclaimed_brick": {
            "co2_kg_per_m2": (30, 100, "kg CO2eq/m2"),
            "labor_hours_per_m2": (8, 16, "hours/m2"),
            "time_days": (0.10, 0.20, "days/m2"),
            "cost_eur_per_m2": (90, 150, "EUR/m2"),
            "material_origin": ("local", "local", "label"),
        },
        "reclaimed-brick": {
            "co2_kg_per_m2": (30, 100, "kg CO2eq/m2"),
            "labor_hours_per_m2": (8, 16, "hours/m2"),
            "time_days": (0.10, 0.20, "days/m2"),
            "cost_eur_per_m2": (90, 150, "EUR/m2"),
            "material_origin": ("local", "local", "label"),
        },
    }[method_key]

    rows = [
        _dev_row("foundation", "co2_kg_per_m2", 30, 60, "kg CO2eq/m2", "Provisional shared fallback for footing impact."),
        _dev_row("foundation", "labor_hours_per_m2", 1, 2, "hours/m2", "Provisional shared fallback for footing labor."),
        _dev_row("foundation", "time_days", 0.02, 0.05, "days/m2", "Provisional shared fallback for footing duration."),
        _dev_row("foundation", "cost_eur_per_m2", 40, 80, "EUR/m2", "Provisional shared fallback for footing cost."),
        _dev_row("foundation", "material_origin", "regional", "regional", "label", "Provisional shared fallback for concrete supply."),
        _dev_row("roof", "co2_kg_per_m2", 20, 50, "kg CO2eq/m2", "Provisional shared fallback for roof impact."),
        _dev_row("roof", "labor_hours_per_m2", 1, 3, "hours/m2", "Provisional shared fallback for roof labor."),
        _dev_row("roof", "time_days", 0.01, 0.04, "days/m2", "Provisional shared fallback for roof duration."),
        _dev_row("roof", "cost_eur_per_m2", 35, 75, "EUR/m2", "Provisional shared fallback for roof cost."),
        _dev_row("roof", "material_origin", "regional", "global", "label", "Provisional shared fallback for roof materials."),
        _dev_row("openings", "co2_kg_per_m2", 8, 15, "kg CO2eq/m2", "Provisional shared fallback for windows and doors."),
        _dev_row("openings", "labor_hours_per_m2", 0.5, 1.5, "hours/m2", "Provisional shared fallback for openings labor."),
        _dev_row("openings", "time_days", 0.01, 0.03, "days/m2", "Provisional shared fallback for openings duration."),
        _dev_row("openings", "cost_eur_per_m2", 20, 45, "EUR/m2", "Provisional shared fallback for windows and doors cost."),
        _dev_row("openings", "material_origin", "regional", "global", "label", "Provisional shared fallback for openings supply."),
        _dev_row("finishing", "co2_kg_per_m2", 10, 20, "kg CO2eq/m2", "Provisional shared fallback for finishing impact."),
        _dev_row("finishing", "labor_hours_per_m2", 1, 2, "hours/m2", "Provisional shared fallback for finishing labor."),
        _dev_row("finishing", "time_days", 0.01, 0.04, "days/m2", "Provisional shared fallback for finishing duration."),
        _dev_row("finishing", "cost_eur_per_m2", 25, 60, "EUR/m2", "Provisional shared fallback for finishing cost."),
        _dev_row("finishing", "material_origin", "regional", "regional", "label", "Provisional shared fallback for finishing supply."),
    ]

    rows.extend(
        [
            _dev_row(
                "structure",
                "co2_kg_per_m2",
                structure_values["co2_kg_per_m2"][0],
                structure_values["co2_kg_per_m2"][1],
                structure_values["co2_kg_per_m2"][2],
                "Provisional method-specific structure CO2 range until research CSV is added.",
            ),
            _dev_row(
                "structure",
                "labor_hours_per_m2",
                structure_values["labor_hours_per_m2"][0],
                structure_values["labor_hours_per_m2"][1],
                structure_values["labor_hours_per_m2"][2],
                "Provisional method-specific structure labor range until research CSV is added.",
            ),
            _dev_row(
                "structure",
                "time_days",
                structure_values["time_days"][0],
                structure_values["time_days"][1],
                structure_values["time_days"][2],
                "Provisional method-specific structure duration range until research CSV is added.",
            ),
            _dev_row(
                "structure",
                "cost_eur_per_m2",
                structure_values["cost_eur_per_m2"][0],
                structure_values["cost_eur_per_m2"][1],
                structure_values["cost_eur_per_m2"][2],
                "Provisional method-specific structure cost range until research CSV is added.",
            ),
            _dev_row(
                "structure",
                "material_origin",
                structure_values["material_origin"][0],
                structure_values["material_origin"][1],
                structure_values["material_origin"][2],
                "Provisional method-specific structure origin label until research CSV is added.",
            ),
        ]
    )
    return rows


def _validate_header(fieldnames: list[str] | None):
    if fieldnames is None:
        raise ValueError("CSV is empty")
    if tuple(fieldnames) != CSV_HEADER:
        expected = ",".join(CSV_HEADER)
        found = ",".join(fieldnames)
        raise ValueError(f"Unexpected CSV header. Expected '{expected}', found '{found}'")


def load_method_rows(
    method_name: str,
    methods_root: Path = METHODS_ROOT,
    allow_fallback: bool = True,
) -> tuple[list[MetricRow], dict[str, Any]]:
    normalized = normalize_method_name(method_name)
    csv_name = METHOD_FILE_MAP[normalized]
    csv_path = methods_root / csv_name

    if not csv_path.exists():
        if not allow_fallback:
            raise FileNotFoundError(csv_path)
        return _build_dev_fallback_rows(normalized), {
            "dataset_path": str(csv_path),
            "fallback_used": True,
            "dataset_status": "fallback_missing_csv",
        }

    rows: list[MetricRow] = []
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        filtered_lines = (
            line for line in handle if line.strip() and not line.lstrip().startswith("#")
        )
        reader = csv.DictReader(filtered_lines)
        _validate_header(reader.fieldnames)
        for raw in reader:
            rows.append(
                MetricRow(
                    phase=raw["phase"].strip().lower(),
                    parameter=raw["parameter"].strip(),
                    value_low=raw["value_low"].strip(),
                    value_high=raw["value_high"].strip(),
                    unit=raw["unit"].strip(),
                    assumption=raw["assumption"].strip(),
                    source=raw["source"].strip(),
                    source_tier=raw["source_tier"].strip(),
                )
            )

    return rows, {
        "dataset_path": str(csv_path),
        "fallback_used": False,
        "dataset_status": "csv_loaded",
    }


def _group_rows(rows: list[MetricRow]) -> dict[tuple[str, str], list[MetricRow]]:
    grouped: dict[tuple[str, str], list[MetricRow]] = {}
    for row in rows:
        grouped.setdefault((row.phase, row.parameter), []).append(row)
    return grouped


def _phase_quantities(scenario: ScenarioInput) -> dict[str, float]:
    footprint_area = max(0.0, float(scenario.area_m2))
    floors = max(1, int(scenario.number_of_floors))
    shape_factor = max(0.75, float(scenario.shape_factor or 1.0))

    quantities: dict[str, float] = {}
    for phase in PHASES:
        mode = PHASE_AREA_MODE[phase]
        if mode == "footprint":
            quantity = footprint_area
        else:
            quantity = footprint_area * floors
            if phase in ("structure", "openings"):
                quantity *= shape_factor
        quantities[phase] = quantity
    return quantities


def _aggregate_numeric_rows(rows: list[MetricRow], quantity: float) -> dict[str, Any]:
    lows = []
    highs = []
    sources = []
    assumptions = []
    unit = None
    source_unit = None

    for row in rows:
        low = _to_float(row.value_low)
        high = _to_float(row.value_high)
        if low is None or high is None:
            continue
        lows.append(low)
        highs.append(high)
        sources.append(row.source)
        assumptions.append(row.assumption)
        unit = TOTAL_UNITS.get(row.parameter, row.unit)
        source_unit = row.unit

    if not lows or not highs:
        return {
            "low": None,
            "high": None,
            "unit": unit,
            "source_unit": source_unit,
            "sources": sorted(set(sources)),
            "assumptions": sorted(set(assumptions)),
            "missing": True,
        }

    return {
        "low": _round_or_none(min(lows) * quantity),
        "high": _round_or_none(max(highs) * quantity),
        "unit": unit,
        "source_unit": source_unit,
        "sources": sorted(set(sources)),
        "assumptions": sorted(set(assumptions)),
        "missing": False,
    }


def _aggregate_text_rows(rows: list[MetricRow]) -> dict[str, Any]:
    low_values = []
    high_values = []
    sources = []
    assumptions = []

    for row in rows:
        low_text = row.value_low.strip()
        high_text = row.value_high.strip()
        if not low_text or not high_text or low_text.upper() == "UNKNOWN" or high_text.upper() == "UNKNOWN":
            continue
        low_values.append(low_text)
        high_values.append(high_text)
        sources.append(row.source)
        assumptions.append(row.assumption)

    if not low_values or not high_values:
        return {
            "low": None,
            "high": None,
            "summary": "unknown",
            "sources": sorted(set(sources)),
            "assumptions": sorted(set(assumptions)),
            "missing": True,
        }

    low_unique = sorted(set(low_values))
    high_unique = sorted(set(high_values))
    summary = " / ".join(sorted(set(low_unique + high_unique)))
    return {
        "low": low_unique,
        "high": high_unique,
        "summary": summary,
        "sources": sorted(set(sources)),
        "assumptions": sorted(set(assumptions)),
        "missing": False,
    }


def _sum_numeric_phase_values(phase_breakdown: dict[str, dict[str, Any]], parameter: str) -> dict[str, Any]:
    total_low = 0.0
    total_high = 0.0
    sources: list[str] = []
    assumptions: list[str] = []
    units: list[str] = []
    missing_phases: list[str] = []

    for phase in PHASES:
        entry = phase_breakdown[phase][parameter]
        if entry["low"] is None or entry["high"] is None:
            missing_phases.append(phase)
            continue
        total_low += entry["low"]
        total_high += entry["high"]
        sources.extend(entry["sources"])
        assumptions.extend(entry["assumptions"])
        if entry["unit"]:
            units.append(entry["unit"])

    return {
        "low": _round_or_none(total_low),
        "high": _round_or_none(total_high),
        "unit": units[0] if units else TOTAL_UNITS.get(parameter),
        "sources": sorted(set(sources)),
        "assumptions": sorted(set(assumptions)),
        "missing_phases": missing_phases,
        "is_partial": bool(missing_phases),
    }


def _summarize_material_origin(phase_breakdown: dict[str, dict[str, Any]]) -> dict[str, Any]:
    summary_values = []
    by_phase = {}
    sources: list[str] = []

    for phase in PHASES:
        entry = phase_breakdown[phase]["material_origin"]
        by_phase[phase] = entry["summary"]
        if not entry["missing"]:
            summary_values.extend(entry["low"])
            summary_values.extend(entry["high"])
            sources.extend(entry["sources"])

    if not summary_values:
        summary = "unknown"
    else:
        summary = " / ".join(sorted(set(summary_values)))

    return {
        "summary": summary,
        "by_phase": by_phase,
        "sources": sorted(set(sources)),
    }


def _coverage_report(grouped: dict[tuple[str, str], list[MetricRow]], fallback_used: bool) -> dict[str, Any]:
    expected_keys = [(phase, parameter) for phase in PHASES for parameter in NUMERIC_PARAMETERS + TEXT_PARAMETERS]
    populated_keys = []
    missing_keys = []

    for key in expected_keys:
        rows = grouped.get(key, [])
        if not rows:
            missing_keys.append(f"{key[0]}:{key[1]}")
            continue
        has_known = False
        for row in rows:
            if key[1] in TEXT_PARAMETERS:
                has_known = row.value_low.upper() != "UNKNOWN" and row.value_high.upper() != "UNKNOWN"
            else:
                has_known = _to_float(row.value_low) is not None and _to_float(row.value_high) is not None
            if has_known:
                break
        if has_known:
            populated_keys.append(f"{key[0]}:{key[1]}")
        else:
            missing_keys.append(f"{key[0]}:{key[1]}")

    total_expected = len(expected_keys)
    total_populated = len(populated_keys)
    coverage = total_populated / total_expected if total_expected else 0.0

    if fallback_used:
        status = "fallback"
    elif total_populated == total_expected:
        status = "ok"
    else:
        status = "partial"

    return {
        "status": status,
        "row_coverage": round(coverage, 3),
        "populated_keys": populated_keys,
        "missing_keys": missing_keys,
        "total_expected": total_expected,
        "total_populated": total_populated,
        "fallback_used": fallback_used,
    }


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


def compute_metrics(
    scenario: ScenarioInput | dict[str, Any],
    methods_root: Path = METHODS_ROOT,
    allow_fallback: bool = True,
) -> dict[str, Any]:
    scenario_input = _scenario_from_any(scenario)
    rows, dataset_meta = load_method_rows(
        scenario_input.construction_method,
        methods_root=methods_root,
        allow_fallback=allow_fallback,
    )
    grouped = _group_rows(rows)
    phase_quantities = _phase_quantities(scenario_input)
    phase_breakdown: dict[str, dict[str, Any]] = {}

    for phase in PHASES:
        phase_entry: dict[str, Any] = {
            "phase_quantity_m2": _round_or_none(phase_quantities[phase]),
            "quantity_mode": PHASE_AREA_MODE[phase],
        }
        for parameter in NUMERIC_PARAMETERS:
            phase_entry[parameter] = _aggregate_numeric_rows(
                grouped.get((phase, parameter), []),
                phase_quantities[phase],
            )
        phase_entry["material_origin"] = _aggregate_text_rows(
            grouped.get((phase, "material_origin"), [])
        )
        phase_breakdown[phase] = phase_entry

    total_co2 = _sum_numeric_phase_values(phase_breakdown, "co2_kg_per_m2")
    total_labor = _sum_numeric_phase_values(phase_breakdown, "labor_hours_per_m2")
    total_time = _sum_numeric_phase_values(phase_breakdown, "time_days")
    total_cost = _sum_numeric_phase_values(phase_breakdown, "cost_eur_per_m2")
    material_origin = _summarize_material_origin(phase_breakdown)
    confidence_range = _coverage_report(grouped, dataset_meta["fallback_used"])
    revenue, profit = _calculate_revenue_and_profit(scenario_input, total_cost)

    warnings: list[str] = []
    if dataset_meta["fallback_used"]:
        warnings.append(
            "Using provisional development fallback values. Replace with research CSV files as soon as they are available."
        )
    if scenario_input.selected_material:
        warnings.append(
            "selected_material is recorded in the scenario trace but does not yet alter lookup values. Material-variant CSV logic is still pending."
        )
    if confidence_range["missing_keys"]:
        warnings.append(
            f"Metrics coverage is {confidence_range['row_coverage']:.0%}. Missing keys remain in the dataset."
        )

    result = {
        "computed_at_ms": int(time.time() * 1000),
        "scenario": asdict(scenario_input),
        "dataset_path": dataset_meta["dataset_path"],
        "data_status": confidence_range["status"],
        "fallback_used": dataset_meta["fallback_used"],
        "confidence_range": confidence_range,
        "phase_breakdown": phase_breakdown,
        "co2_estimate": total_co2,
        "labor_hours": total_labor,
        "construction_time": total_time,
        "cost_estimate": total_cost,
        "material_origin": material_origin,
        "revenue_estimate": revenue,
        "profit_estimate": profit,
        "warnings": warnings,
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
        help="Fail if the research CSV does not exist instead of using provisional fallback values.",
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
