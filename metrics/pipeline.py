from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data"
RAW_IMPORTS_ROOT = DATA_ROOT / "imports" / "treethreetree"
NORMALIZED_METHODS_ROOT = DATA_ROOT / "methods"
NORMALIZATION_RULES_PATH = DATA_ROOT / "normalization_rules.json"
METHODS_DB_PATH = DATA_ROOT / "methods_db.json"
SOURCES_MD_PATH = DATA_ROOT / "SOURCES.md"

PHASE_STAGES = ["foundation", "structure", "roof", "openings", "finishing"]
PREFAB_STAGES = ["A1-A3", "A4", "A5", "B", "C"]

MISSING_TOKENS = {"", "na", "n/a", "null", "none", "unknown", "-"}

NORMALIZED_HEADER = [
    "method",
    "data_model",
    "display_mode",
    "phase",
    "lifecycle_stage",
    "sub_method",
    "metric",
    "value_low",
    "value_high",
    "unit",
    "basis",
    "source_key",
    "confidence_min",
    "confidence_max",
    "selected_material",
    "notes",
    "metadata",
]

METHOD_ALIASES = {
    "masonry": "masonry",
    "brick": "masonry",
    "3d_printed": "3d_printed",
    "3d-printed": "3d_printed",
    "3dp": "3d_printed",
    "prefab": "prefab",
    "prefab_timber": "prefab",
    "modular_concrete": "prefab",
    "clt": "prefab",
    "reclaimed_brick": "reclaimed_brick",
    "reclaimed-brick": "reclaimed_brick",
}

NORMALIZED_FILE_MAP = {
    "masonry": "masonry.csv",
    "3d_printed": "3d-printed.csv",
    "prefab": "prefab.csv",
    "reclaimed_brick": "reclaimed-brick.csv",
}

METHOD_CONTRACTS = {
    "masonry": {
        "display_name": "MASONRY",
        "data_model": "phase_based",
        "display_mode": "construction_phase_view",
        "stages": PHASE_STAGES,
        "selected_material_default": "fired_clay_brick",
    },
    "3d_printed": {
        "display_name": "3D PRINTED",
        "data_model": "phase_based",
        "display_mode": "construction_phase_view",
        "stages": PHASE_STAGES,
        "selected_material_default": "printed_concrete_or_earth_proxy",
    },
    "prefab": {
        "display_name": "PREFAB",
        "data_model": "lifecycle_based",
        "display_mode": "prefab_lifecycle_card",
        "stages": PREFAB_STAGES,
        "sub_methods": ["clt", "modular_concrete"],
        "default_sub_method": "clt",
        "selected_material_defaults": {
            "clt": "timber_clt_prefab",
            "modular_concrete": "modular_concrete_prefab",
        },
    },
    "reclaimed_brick": {
        "display_name": "RECLAIMED BRICK",
        "data_model": "overlay",
        "display_mode": "construction_phase_view",
        "stages": PHASE_STAGES,
        "base_method": "masonry",
        "selected_material_default": "reclaimed_fired_clay_brick",
    },
}

RAW_IMPORT_SPECS = {
    "masonry.csv": {
        "method": "masonry",
        "data_model": "phase_based",
        "display_mode": "construction_phase_view",
    },
    "3d-printed.csv": {
        "method": "3d_printed",
        "data_model": "phase_based",
        "display_mode": "construction_phase_view",
    },
    "prefab.csv": {
        "method": "prefab",
        "data_model": "lifecycle_based",
        "display_mode": "prefab_lifecycle_card",
    },
    "reclaimed-brick.csv": {
        "method": "reclaimed_brick",
        "data_model": "overlay",
        "display_mode": "construction_phase_view",
        "base_method": "masonry",
    },
}

SOURCE_REGISTRY = {
    "unknown_import": {
        "citation": "Imported raw source string could not be normalized into a reliable single source key.",
        "tier": "provisional",
        "notes": "Use when raw import data had missing, compound, or unresolved citations.",
    },
    "bedec-2026": {
        "citation": "ITeC Banco BEDEC 2025/2026 release.",
        "tier": "1",
        "notes": "Catalonia baseline for cost, material quantity, and proxy construction rates.",
    },
    "bedec-2026-proxy": {
        "citation": "ITeC Banco BEDEC 2025/2026 release used as an explicit proxy row.",
        "tier": "2",
        "notes": "Use when the imported row is a BEDEC-derived analogue rather than a direct method match.",
    },
    "masonry-strand-01": {
        "citation": "Imported masonry strand 01 synthesis from Rafik's branch.",
        "tier": "provisional",
        "notes": "Internal imported synthesis used as a carry-over proxy for non-printed 3D-printing phases.",
    },
    "en-15804": {
        "citation": "EN 15804 reference mentioned in the imported source string.",
        "tier": "methodology",
        "notes": "Methodology-standard anchor preserved when the import cited the standard directly.",
    },
    "izaola-2023": {
        "citation": "Izaola 2023 as cited in Rafik's imported masonry strand.",
        "tier": "1-2",
        "notes": "Masonry foundation, roof, openings, and finishing proxy values.",
    },
    "mateus-2023": {
        "citation": "Mateus 2023 as cited in Rafik's imported masonry strand.",
        "tier": "1-2",
        "notes": "Masonry embodied-carbon and finishing-range triangulation.",
    },
    "cype-spain-fef010": {
        "citation": "CYPE Spain FEF010 cost/labour reference line.",
        "tier": "1-2",
        "notes": "Masonry load-bearing perforated-brick labour and cost proxy.",
    },
    "cype-spain-ffz010": {
        "citation": "CYPE Spain FFZ010 facade reference line.",
        "tier": "1-2",
        "notes": "Masonry facade labour and cost proxy.",
    },
    "hispalyt-008-001": {
        "citation": "Hispalyt GlobalEPD 008-001.",
        "tier": "1",
        "notes": "Spanish clay roof-tile embodied-carbon reference.",
    },
    "hispalyt-008-016": {
        "citation": "Hispalyt GlobalEPD 008-016.",
        "tier": "1",
        "notes": "Spanish fired-clay brick / transport proxy for masonry.",
    },
    "hispalyt-008-017": {
        "citation": "Hispalyt GlobalEPD 008-017.",
        "tier": "1",
        "notes": "Spanish perforated-brick structural masonry embodied-carbon reference.",
    },
    "rejected-cype-roof": {
        "citation": "Imported roof-rate proxy where the original CYPE fetch was unavailable.",
        "tier": "3",
        "notes": "Retained as a provisional import proxy only.",
    },
    "de-wolf-2017": {
        "citation": "De Wolf 2017 as referenced in the imported masonry/openings notes.",
        "tier": "2",
        "notes": "Openings embodied-carbon proxy.",
    },
    "mohammad-2020": {
        "citation": "Mohammad et al. 2020.",
        "tier": "1",
        "notes": "Primary 3D-printed concrete structure row and printer-electricity references.",
    },
    "motalebi-2024-review": {
        "citation": "Motalebi 2024 review.",
        "tier": "1",
        "notes": "3D-printed concrete material-level per-m3 range.",
    },
    "rossi-2024": {
        "citation": "Rossi 2024.",
        "tier": "1",
        "notes": "3D-printed whole-building comparison sanity-check row.",
    },
    "alhumayani-2020": {
        "citation": "Alhumayani 2020.",
        "tier": "1",
        "notes": "3D-printed earth proxy row and local-material argument.",
    },
    "allouzi-2020": {
        "citation": "Allouzi 2020.",
        "tier": "1",
        "notes": "3D-printed labour and cost directionality.",
    },
    "cybe-cobod-vendor": {
        "citation": "CyBe / COBOD vendor claims as cited in imported 3D-printed notes.",
        "tier": "3",
        "notes": "Vendor-only labour/time/cost sibling rows.",
    },
    "apis-cor": {
        "citation": "Apis Cor / ICON vendor-style demonstrator references cited in imported 3D-printing notes.",
        "tier": "3",
        "notes": "Vendor-style shell-duration and cost references; use as directional only.",
    },
    "wikipedia-tecla-icon-press": {
        "citation": "Imported TECLA / ICON press synthesis row.",
        "tier": "mixed",
        "notes": "3D-printed structure total-duration proxy from mixed sources.",
    },
    "wikipedia-tecla": {
        "citation": "Imported TECLA summary source string from Rafik's 3D-printing strand.",
        "tier": "mixed",
        "notes": "Used when the imported row names TECLA first in a mixed-source duration proxy.",
    },
    "iaac-tova-wasp-tecla": {
        "citation": "IAAC TOVA and WASP TECLA project references.",
        "tier": "2-3",
        "notes": "3D-printed material-origin notes and Catalonia-relevant earth proxy context.",
    },
    "iaac-tova": {
        "citation": "IAAC TOVA project reference.",
        "tier": "2-3",
        "notes": "Catalonia-specific earth-printing material-origin reference.",
    },
    "andersen-2022": {
        "citation": "Andersen 2022.",
        "tier": "1",
        "notes": "Prefab / CLT embodied-carbon and lifecycle references.",
    },
    "hemmati-2024": {
        "citation": "Hemmati 2024.",
        "tier": "1-2",
        "notes": "Prefab / CLT site assembly and reuse notes.",
    },
    "stora-enso-epd": {
        "citation": "Stora Enso EPD.",
        "tier": "1",
        "notes": "CLT panel carbon, transport, and end-of-life references.",
    },
    "klh-epd": {
        "citation": "KLH EPD.",
        "tier": "1",
        "notes": "CLT panel fossil and biogenic references.",
    },
    "binderholz-epd": {
        "citation": "Binderholz EPD.",
        "tier": "1",
        "notes": "CLT panel embodied-carbon triangulation.",
    },
    "wei-2024": {
        "citation": "Wei 2024.",
        "tier": "1",
        "notes": "Modular-concrete lifecycle references and reuse sensitivity.",
    },
    "wei-2024-footnote": {
        "citation": "Wei 2024 footnote / appendix reference as cited in imported prefab notes.",
        "tier": "1-2",
        "notes": "Use when the imported row explicitly relies on the reuse-sensitivity footnote instead of the main table.",
    },
    "pan-hon-2012": {
        "citation": "Pan and Hon 2012.",
        "tier": "2",
        "notes": "Prefab factory, transport, and site labour/time references.",
    },
    "industry-data": {
        "citation": "Imported industry-data placeholder without a single citable publication.",
        "tier": "provisional",
        "notes": "Keep as a low-confidence manufacturing proxy until a real plant dataset replaces it.",
    },
    "moodul-vendor": {
        "citation": "Moodul / modular-concrete vendor references cited in imported prefab notes.",
        "tier": "3",
        "notes": "Spanish prefab transport and cost proxies.",
    },
    "liu-2021": {
        "citation": "Liu 2021.",
        "tier": "1-2",
        "notes": "Prefab end-of-life and methodological allocation notes.",
    },
    "rbc-epd-2024": {
        "citation": "RBC EPD 2024.",
        "tier": "1",
        "notes": "Reclaimed-brick default cut-off baseline and finishing references.",
    },
    "salmio-huuhka-2026": {
        "citation": "Salmio and Huuhka 2026.",
        "tier": "1",
        "notes": "Reclaimed-brick allocation-rule, labour, and transport-sensitivity references.",
    },
    "de-wolf-2020": {
        "citation": "De Wolf 2020.",
        "tier": "1-2",
        "notes": "Reclaimed-brick avoided-burden / system-expansion comparison.",
    },
    "devenes-2022": {
        "citation": "Devenes 2022 as cited in the imported reclaimed-brick strand.",
        "tier": "1-2",
        "notes": "Reclaimed-brick scoping and regional sourcing context.",
    },
    "devenes-2022-analogous-scoping": {
        "citation": "Devenes 2022 analogous-scoping reference as cited in imported reclaimed-brick notes.",
        "tier": "1-2",
        "notes": "Out-of-scope reclaimed-foundation qualitative placeholder.",
    },
    "brutting-2020": {
        "citation": "Brutting 2020.",
        "tier": "1-2",
        "notes": "Reclaimed-brick structure duration / stock-matching design overhead reference.",
    },
    "iaac-mat-mining": {
        "citation": "IAAC material-mining project reference as cited in imported reclaimed-brick notes.",
        "tier": "2-3",
        "notes": "Reclaimed-brick structure and finishing context.",
    },
    "restado-2026": {
        "citation": "Restado 2026 as cited in the imported reclaimed-brick cost proxy.",
        "tier": "2",
        "notes": "Reclaimed-brick cost proxy input.",
    },
    "concular-2026": {
        "citation": "Concular 2026 as cited in the imported reclaimed-brick cost proxy.",
        "tier": "2",
        "notes": "Reclaimed-brick cost proxy input.",
    },
    "k118-insitu": {
        "citation": "K.118 / in situ project reference as cited in imported reclaimed-brick notes.",
        "tier": "2",
        "notes": "Reclaimed lintel / urban-mining opening reference.",
    },
    "devos-2024": {
        "citation": "Devos 2024 as cited in imported reclaimed-brick finishing notes.",
        "tier": "1-2",
        "notes": "Hydraulic-lime compatibility note for reclaimed-brick finishing.",
    },
    "engineering-judgement-import": {
        "citation": "Imported engineering-judgement row without a single resolvable citation token.",
        "tier": "provisional",
        "notes": "Use only as explicit low-confidence proxy data.",
    },
}

SOURCE_KEY_ALIASES = {
    "apis-cor-t3-sibling": "apis-cor",
    "bedec-2026-proxy": "bedec-2026-proxy",
    "cobod-vendor": "cybe-cobod-vendor",
    "cybe-t3-sibling": "cybe-cobod-vendor",
    "devenes-2022-analogous-scoping": "devenes-2022-analogous-scoping",
    "iaac-tova": "iaac-tova",
    "icon-press": "wikipedia-tecla",
    "icon-vendor": "apis-cor",
    "industry-data": "industry-data",
    "k-118": "k118-insitu",
    "k-118-insitu": "k118-insitu",
    "masonry-strand-01": "masonry-strand-01",
    "vendor-sibling": "engineering-judgement-import",
    "wasp-tecla": "iaac-tova-wasp-tecla",
    "wei-2024-footnote": "wei-2024-footnote",
    "wikipedia-tecla": "wikipedia-tecla",
}


@dataclass
class ScenarioInput:
    method: str
    area_m2: float = 0.0
    floors: int = 1
    sub_method: str | None = None
    selected_material: str | None = None


@dataclass
class NormalizedRow:
    method: str
    data_model: str
    display_mode: str
    phase: str | None
    lifecycle_stage: str | None
    sub_method: str | None
    metric: str
    value_low: str | None
    value_high: str | None
    unit: str
    basis: str
    source_key: str
    confidence_min: float | None
    confidence_max: float | None
    selected_material: str | None
    notes: str
    metadata: dict[str, Any]


def canonical_method_name(method_name: str | None) -> str:
    if not method_name:
        raise ValueError("method is required")
    normalized = method_name.strip().lower().replace(" ", "_")
    if normalized not in METHOD_ALIASES:
        known = ", ".join(sorted(set(METHOD_ALIASES)))
        raise ValueError(f"Unknown method '{method_name}'. Known: {known}")
    return METHOD_ALIASES[normalized]


def load_normalization_rules(path: Path = NORMALIZATION_RULES_PATH) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_methods_db(path: Path = METHODS_DB_PATH) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_missing(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if text.lower() in MISSING_TOKENS:
        return None
    return text


def parse_float(value: Any) -> float | None:
    text = normalize_missing(value)
    if text is None:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "unknown-import"


def canonicalize_source_key(source_key: str) -> str:
    return SOURCE_KEY_ALIASES.get(source_key, source_key)


def extract_source_keys(raw_source: str | None) -> list[str]:
    text = normalize_missing(raw_source)
    if text is None:
        return ["unknown_import"]
    if text.upper() == "NA":
        return ["unknown_import"]
    parts = [part.strip() for part in re.split(r"\s*[+;]\s*", text) if part.strip()]
    keys = []
    for part in parts:
        if part.lower() in {"na", "unknown"}:
            continue
        if part.lower().startswith("engineering judgement"):
            keys.append("engineering-judgement-import")
            continue
        keys.append(canonicalize_source_key(slugify(part)))
    return keys or ["unknown_import"]


def primary_source_key(raw_source: str | None) -> str:
    return extract_source_keys(raw_source)[0]


def confidence_for_method(method: str, methods_db: dict[str, Any]) -> tuple[float | None, float | None]:
    for entry in methods_db.get("methods", []):
        if entry.get("name", "").strip().lower().replace(" ", "_") == method:
            confidence = entry.get("confidence_range") or {}
            return confidence.get("score_low"), confidence.get("score_high")
    return None, None


def contract_for_method(method: str) -> dict[str, Any]:
    return METHOD_CONTRACTS[method]


def selected_material_default(method: str, sub_method: str | None = None) -> str | None:
    contract = contract_for_method(method)
    if method == "prefab":
        actual_sub_method = sub_method or contract["default_sub_method"]
        return contract["selected_material_defaults"].get(actual_sub_method)
    return contract.get("selected_material_default")


def determine_unit_and_basis(raw_unit: str | None, metric: str) -> tuple[str, str]:
    unit_text = normalize_missing(raw_unit) or ""
    lowered = unit_text.lower()
    metric_lower = metric.lower()

    if metric_lower == "material_origin" or "qualitative" in lowered:
        return "label", "qualitative_label"
    if "km radius" in lowered:
        return "km", "qualitative_label"
    if lowered == "km":
        return "km", "distance_km"
    if lowered == "years":
        return "years", "total_years"
    if lowered == "second-life cycles":
        return "cycles", "count"
    if lowered == "calendar days":
        return "days", "calendar_days"
    if lowered == "days":
        return "days", "total_days"
    if "days / m2 gfa" in lowered:
        return "days", "days_per_m2_gfa"
    if "days / m2 wall" in lowered:
        return "days", "days_per_m2_wall"
    if "days / m2 roof" in lowered:
        return "days", "days_per_m2_roof_area"
    if "days / m2 opening" in lowered:
        return "days", "days_per_m2_opening_area"
    if "days / m2 finished" in lowered:
        return "days", "days_per_m2_finished_surface"
    if "days / m2" in lowered:
        return "days", "days_per_m2"
    if "h / m2 gfa" in lowered:
        return "hours", "hours_per_m2_gfa"
    if "h / m2 wall" in lowered:
        return "hours", "hours_per_m2_wall"
    if "h / m2 roof" in lowered:
        return "hours", "hours_per_m2_roof_area"
    if "h / m2 opening" in lowered:
        return "hours", "hours_per_m2_opening_area"
    if "h / m2 finished" in lowered:
        return "hours", "hours_per_m2_finished_surface"
    if lowered == "h / m2":
        return "hours", "hours_per_m2"
    if "eur / m2 gfa" in lowered:
        return "EUR", "eur_per_m2_gfa"
    if "eur / m2 wall" in lowered:
        return "EUR", "eur_per_m2_wall"
    if "eur / m2 roof" in lowered:
        return "EUR", "eur_per_m2_roof_area"
    if "eur / m2 opening" in lowered:
        return "EUR", "eur_per_m2_opening_area"
    if "eur / m2 finished" in lowered:
        return "EUR", "eur_per_m2_finished_surface"
    if lowered == "eur / m2":
        return "EUR", "eur_per_m2"
    if "kg co2eq / m2 gfa" in lowered:
        return "kg CO2eq", "per_m2_gfa"
    if "kg co2eq / m2 wall" in lowered:
        return "kg CO2eq", "per_m2_wall"
    if "kg co2eq / m2 roof" in lowered:
        return "kg CO2eq", "per_m2_roof_area"
    if "kg co2eq / m2 opening" in lowered:
        return "kg CO2eq", "per_m2_opening_area"
    if "kg co2eq / m2 finished" in lowered:
        return "kg CO2eq", "per_m2_finished_surface"
    if "kg co2eq / m3" in lowered:
        return "kg CO2eq", "per_m3"
    if "kg / m2 gfa" in lowered:
        return "kg", "kg_per_m2_gfa"
    if lowered == "kg / m2":
        return "kg", "kg_per_m2"
    return unit_text or "value", "raw_value"


def primary_flag(method: str, raw_row: dict[str, str]) -> bool:
    metric = raw_row.get("parameter", "").strip().lower()
    unit = (raw_row.get("unit") or "").lower()
    assumption = (raw_row.get("assumption") or "").lower()
    allocation = (raw_row.get("allocation_rule") or "").lower()
    source = (raw_row.get("source") or "").lower()

    if metric.endswith("_vendor") or "vendor claim" in assumption or "vendor" in source:
        return False
    if method == "3d_printed":
        if metric == "co2_kg_per_m2" and "/ m2 wall" in unit:
            return True
        if metric in {"co2_kg_per_m2_material", "co2_kg_per_m2_earth", "co2_kg_per_m2_catalan"}:
            return False
    if method == "reclaimed_brick" and metric == "co2_kg_per_m2":
        return allocation == "cut-off"
    return True


def row_variant(method: str, raw_row: dict[str, str]) -> str | None:
    metric = raw_row.get("parameter", "").strip().lower()
    allocation = normalize_missing(raw_row.get("allocation_rule"))
    if method == "3d_printed":
        if metric == "co2_kg_per_m2_material":
            return "material_level_proxy"
        if metric == "co2_kg_per_m2_earth":
            return "earth_proxy"
        if metric == "co2_kg_per_m2_catalan":
            return "catalonia_gap"
        if metric.endswith("_vendor"):
            return "vendor_sibling"
    if method == "reclaimed_brick" and allocation:
        return allocation.lower().replace(" ", "_")
    return None


def metadata_for_row(method: str, raw_row: dict[str, str]) -> dict[str, Any]:
    known_columns = {"phase", "parameter", "value_low", "value_high", "unit", "assumption", "source", "source_tier"}
    extras = {key: value for key, value in raw_row.items() if key not in known_columns and normalize_missing(value) is not None}
    metadata: dict[str, Any] = {
        "raw_source": normalize_missing(raw_row.get("source")),
        "source_keys": extract_source_keys(raw_row.get("source")),
        "source_tier": normalize_missing(raw_row.get("source_tier")),
        "raw_unit": normalize_missing(raw_row.get("unit")),
        "primary": primary_flag(method, raw_row),
    }
    variant = row_variant(method, raw_row)
    if variant:
        metadata["variant"] = variant
    if extras:
        metadata["extra_fields"] = extras
    if method == "reclaimed_brick":
        metadata["base_method"] = "masonry"
    return metadata


def normalized_filename_for_method(method: str) -> Path:
    return NORMALIZED_METHODS_ROOT / NORMALIZED_FILE_MAP[method]


def _serialize_value(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, float):
        text = f"{value:.6f}".rstrip("0").rstrip(".")
        return text or "0"
    return str(value)


def normalize_row(
    method: str,
    raw_row: dict[str, str],
    methods_db: dict[str, Any],
) -> dict[str, str]:
    contract = contract_for_method(method)
    confidence_min, confidence_max = confidence_for_method(method, methods_db)
    metric = raw_row["parameter"].strip()
    unit, basis = determine_unit_and_basis(raw_row.get("unit"), metric)
    metadata = metadata_for_row(method, raw_row)
    phase = raw_row["phase"].strip() if contract["data_model"] != "lifecycle_based" else ""
    lifecycle_stage = raw_row["phase"].strip() if contract["data_model"] == "lifecycle_based" else ""
    sub_method = normalize_missing(raw_row.get("sub_method"))
    selected_material = selected_material_default(method, sub_method)
    return {
        "method": method,
        "data_model": contract["data_model"],
        "display_mode": contract["display_mode"],
        "phase": phase,
        "lifecycle_stage": lifecycle_stage,
        "sub_method": sub_method or "",
        "metric": metric,
        "value_low": _serialize_value(normalize_missing(raw_row.get("value_low"))),
        "value_high": _serialize_value(normalize_missing(raw_row.get("value_high"))),
        "unit": unit,
        "basis": basis,
        "source_key": primary_source_key(raw_row.get("source")),
        "confidence_min": _serialize_value(confidence_min),
        "confidence_max": _serialize_value(confidence_max),
        "selected_material": selected_material or "",
        "notes": normalize_missing(raw_row.get("assumption")) or "",
        "metadata": json.dumps(metadata, sort_keys=True),
    }


def generate_normalized_rows(methods_db: dict[str, Any] | None = None) -> dict[str, list[dict[str, str]]]:
    methods_db = methods_db or load_methods_db()
    outputs: dict[str, list[dict[str, str]]] = {}
    for raw_name, spec in RAW_IMPORT_SPECS.items():
        method = spec["method"]
        rows: list[dict[str, str]] = []
        raw_path = RAW_IMPORTS_ROOT / raw_name
        with raw_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for raw_row in reader:
                rows.append(normalize_row(method, raw_row, methods_db))
        outputs[method] = rows
    return outputs


def write_normalized_csv(method: str, rows: list[dict[str, str]], methods_root: Path = NORMALIZED_METHODS_ROOT) -> Path:
    methods_root.mkdir(parents=True, exist_ok=True)
    path = methods_root / NORMALIZED_FILE_MAP[method]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=NORMALIZED_HEADER)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return path


def write_sources_registry(path: Path = SOURCES_MD_PATH) -> None:
    lines = [
        "# data/SOURCES.md",
        "",
        "This registry is used by the normalized metrics pipeline under `data/methods/`.",
        "Each `source_key` below maps to a citation label or an explicit import placeholder.",
        "",
        "Format:",
        "",
        "`source-key - citation - tier - notes`",
        "",
    ]
    for key in sorted(SOURCE_REGISTRY):
        entry = SOURCE_REGISTRY[key]
        lines.append(f"{key} - {entry['citation']} - Tier {entry['tier']} - {entry['notes']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def missing_source_registry_keys(methods_root: Path = NORMALIZED_METHODS_ROOT) -> list[str]:
    missing: set[str] = set()
    for path in methods_root.glob("*.csv"):
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                source_key = normalize_missing(row.get("source_key"))
                if source_key and source_key not in SOURCE_REGISTRY:
                    missing.add(source_key)
    return sorted(missing)


def generate_normalized_datasets() -> list[Path]:
    methods_db = load_methods_db()
    outputs = generate_normalized_rows(methods_db=methods_db)
    written = [write_normalized_csv(method, rows) for method, rows in outputs.items()]
    write_sources_registry()
    return written


def load_normalized_rows(method: str, methods_root: Path = NORMALIZED_METHODS_ROOT) -> list[NormalizedRow]:
    method_key = canonical_method_name(method)
    path = methods_root / NORMALIZED_FILE_MAP[method_key]
    if not path.exists():
        return []
    rows: list[NormalizedRow] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for raw in reader:
            rows.append(
                NormalizedRow(
                    method=raw["method"],
                    data_model=raw["data_model"],
                    display_mode=raw["display_mode"],
                    phase=normalize_missing(raw["phase"]),
                    lifecycle_stage=normalize_missing(raw["lifecycle_stage"]),
                    sub_method=normalize_missing(raw["sub_method"]),
                    metric=raw["metric"],
                    value_low=normalize_missing(raw["value_low"]),
                    value_high=normalize_missing(raw["value_high"]),
                    unit=raw["unit"],
                    basis=raw["basis"],
                    source_key=raw["source_key"],
                    confidence_min=parse_float(raw["confidence_min"]),
                    confidence_max=parse_float(raw["confidence_max"]),
                    selected_material=normalize_missing(raw["selected_material"]),
                    notes=raw["notes"],
                    metadata=json.loads(raw["metadata"] or "{}"),
                )
            )
    return rows


def quantity_for_basis(
    basis: str,
    scenario: ScenarioInput,
    rules: dict[str, Any],
) -> tuple[float | None, str | None]:
    gfa = max(0.0, scenario.area_m2) * max(1, int(scenario.floors))
    footprint_area = max(0.0, scenario.area_m2)
    wall_to_gfa_ratio = float(rules.get("wall_to_gfa_ratio", 1.8))
    thickness_map = rules.get("default_wall_thickness_m", {})
    method_key = canonical_method_name(scenario.method)
    thickness = float(thickness_map.get(method_key, 0.2))

    if basis in {"per_m2_gfa", "hours_per_m2_gfa", "eur_per_m2_gfa", "kg_per_m2_gfa", "days_per_m2_gfa"}:
        return gfa, None
    if basis in {"per_m2_wall", "hours_per_m2_wall", "eur_per_m2_wall", "days_per_m2_wall"}:
        return gfa * wall_to_gfa_ratio, None
    if basis in {
        "per_m2_roof_area",
        "hours_per_m2_roof_area",
        "eur_per_m2_roof_area",
        "days_per_m2_roof_area",
    }:
        return footprint_area, None
    if basis in {
        "per_m2_opening_area",
        "hours_per_m2_opening_area",
        "eur_per_m2_opening_area",
        "days_per_m2_opening_area",
    }:
        return gfa, None
    if basis in {
        "per_m2_finished_surface",
        "hours_per_m2_finished_surface",
        "eur_per_m2_finished_surface",
        "days_per_m2_finished_surface",
    }:
        return gfa * wall_to_gfa_ratio, None
    if basis == "per_m3":
        wall_area = gfa * wall_to_gfa_ratio
        return wall_area * thickness, None
    if basis in {"per_m2", "hours_per_m2", "eur_per_m2", "kg_per_m2", "days_per_m2"}:
        return footprint_area, None
    if basis in {"per_m2_footprint", "hours_per_m2_footprint", "eur_per_m2_footprint"}:
        return footprint_area, None
    if basis in {"calendar_days", "total_days", "total_years", "count", "distance_km"}:
        return 1.0, None
    if basis == "qualitative_label":
        return None, None
    return None, f"unsupported_basis:{basis}"


def scale_numeric_range(
    basis: str,
    low: float | None,
    high: float | None,
    scenario: ScenarioInput,
    rules: dict[str, Any],
) -> tuple[float | None, float | None, str | None]:
    quantity, warning = quantity_for_basis(basis, scenario, rules)
    if low is None or high is None:
        return None, None, warning
    if quantity is None:
        return None, None, warning
    return low * quantity, high * quantity, warning


def serialize_row_for_output(
    row: NormalizedRow,
    scenario: ScenarioInput,
    rules: dict[str, Any],
) -> dict[str, Any]:
    numeric_low = parse_float(row.value_low)
    numeric_high = parse_float(row.value_high)
    scaled_low, scaled_high, scale_warning = scale_numeric_range(row.basis, numeric_low, numeric_high, scenario, rules)
    output = {
        "method": row.method,
        "data_model": row.data_model,
        "display_mode": row.display_mode,
        "phase": row.phase,
        "lifecycle_stage": row.lifecycle_stage,
        "sub_method": row.sub_method,
        "metric": row.metric,
        "unit": row.unit,
        "basis": row.basis,
        "source_key": row.source_key,
        "confidence_min": row.confidence_min,
        "confidence_max": row.confidence_max,
        "selected_material": row.selected_material,
        "notes": row.notes,
        "metadata": row.metadata,
        "raw_low": numeric_low if numeric_low is not None else row.value_low,
        "raw_high": numeric_high if numeric_high is not None else row.value_high,
        "scaled_low": scaled_low,
        "scaled_high": scaled_high,
        "scale_warning": scale_warning,
    }
    return output


def skeleton_output(method: str, sub_method: str | None = None) -> dict[str, Any]:
    contract = contract_for_method(method)
    selected_material = selected_material_default(method, sub_method)
    return {
        "method": method,
        "data_model": contract["data_model"],
        "display_mode": contract["display_mode"],
        "stages": list(contract["stages"]),
        "selected_material": selected_material,
        "warnings": ["using_dev_fallback", "missing_normalized_data"],
        "stage_data": {stage: [] for stage in contract["stages"]},
        "primary_rows": {stage: [] for stage in contract["stages"]},
        "source_quality": None,
        "sub_method": sub_method,
        "base_method": contract.get("base_method"),
    }


def build_method_output(
    method: str,
    area_m2: float = 0.0,
    floors: int = 1,
    sub_method: str | None = None,
    selected_material: str | None = None,
    methods_root: Path = NORMALIZED_METHODS_ROOT,
    rules_path: Path = NORMALIZATION_RULES_PATH,
) -> dict[str, Any]:
    method_key = canonical_method_name(method)
    contract = contract_for_method(method_key)
    methods_db = load_methods_db()
    warnings: list[str] = []
    actual_sub_method = sub_method

    if method_key == "prefab" and not actual_sub_method:
        actual_sub_method = contract["default_sub_method"]
        warnings.append("default_prefab_sub_method")

    rows = load_normalized_rows(method_key, methods_root=methods_root)
    if method_key == "prefab":
        rows = [row for row in rows if row.sub_method in {actual_sub_method, "both", None}]

    if not rows:
        output = skeleton_output(method_key, sub_method=actual_sub_method)
        output["warnings"] = list(dict.fromkeys(output["warnings"] + warnings))
        return output

    scenario = ScenarioInput(
        method=method_key,
        area_m2=area_m2,
        floors=floors,
        sub_method=actual_sub_method,
        selected_material=selected_material or selected_material_default(method_key, actual_sub_method),
    )
    rules = load_normalization_rules(rules_path)
    stage_key = "lifecycle_stage" if contract["data_model"] == "lifecycle_based" else "phase"
    stage_data = {stage: [] for stage in contract["stages"]}
    primary_rows = {stage: [] for stage in contract["stages"]}

    for row in rows:
        rendered = serialize_row_for_output(row, scenario, rules)
        stage = rendered[stage_key]
        if stage not in stage_data:
            warnings.append(f"unexpected_stage:{stage}")
            continue
        if rendered["scale_warning"]:
            warnings.append(rendered["scale_warning"])
        if row.source_key == "unknown_import" or row.source_key not in SOURCE_REGISTRY:
            warnings.append("unknown_source_key")
        stage_data[stage].append(rendered)
        if row.metadata.get("primary"):
            primary_rows[stage].append(rendered)

    for stage in contract["stages"]:
        if not stage_data[stage]:
            warnings.append(f"missing_normalized_data:{stage}")

    confidence_min, confidence_max = confidence_for_method(method_key, methods_db)
    output = {
        "method": method_key,
        "data_model": contract["data_model"],
        "display_mode": contract["display_mode"],
        "stages": list(contract["stages"]),
        "selected_material": scenario.selected_material,
        "warnings": sorted(set(warnings)),
        "stage_data": stage_data,
        "primary_rows": primary_rows,
        "source_quality": {
            "confidence_min": confidence_min,
            "confidence_max": confidence_max,
        },
        "sub_method": actual_sub_method,
        "base_method": contract.get("base_method"),
    }
    if method_key == "prefab":
        output["available_sub_methods"] = list(contract["sub_methods"])
    return output


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Standalone metrics normalization and output pipeline.")
    parser.add_argument("--build-normalized", action="store_true", help="Generate normalized CSVs under data/methods/.")
    parser.add_argument("--method", help="Method to inspect (masonry, 3d_printed, prefab, reclaimed_brick).")
    parser.add_argument("--area", type=float, default=0.0, help="Footprint area in square meters.")
    parser.add_argument("--floors", type=int, default=1, help="Number of floors.")
    parser.add_argument("--sub-method", dest="sub_method", default=None, help="Prefab sub-method: clt or modular_concrete.")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.build_normalized:
        written = generate_normalized_datasets()
        print(json.dumps({"written": [str(path) for path in written]}, indent=2))
        return
    if not args.method:
        raise SystemExit("--method is required unless --build-normalized is used")
    output = build_method_output(
        method=args.method,
        area_m2=args.area,
        floors=args.floors,
        sub_method=args.sub_method,
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
