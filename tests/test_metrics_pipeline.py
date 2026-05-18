import csv
import json
import tempfile
import unittest
from pathlib import Path

from metrics.pipeline import (
    NORMALIZED_HEADER,
    PREFAB_STAGES,
    PHASE_STAGES,
    ScenarioInput,
    build_method_output,
    generate_normalized_rows,
    load_methods_db,
    load_normalization_rules,
    missing_source_registry_keys,
    normalize_missing,
    normalize_row,
    scale_numeric_range,
    write_normalized_csv,
)


class MetricsPipelineTests(unittest.TestCase):
    def test_missing_tokens_become_null(self) -> None:
        for token in ("NA", "N/A", "na", "", "unknown", "-"):
            self.assertIsNone(normalize_missing(token))

    def test_normalize_row_preserves_prefab_sub_method_and_nulls(self) -> None:
        methods_db = load_methods_db()
        row = normalize_row(
            "prefab",
            {
                "phase": "A1-A3",
                "parameter": "material_origin",
                "value_low": "NA",
                "value_high": "",
                "unit": "qualitative",
                "assumption": "Imported qualitative note",
                "source": "NA",
                "source_tier": "missing",
                "sub_method": "clt",
            },
            methods_db,
        )

        metadata = json.loads(row["metadata"])
        self.assertEqual(row["data_model"], "lifecycle_based")
        self.assertEqual(row["display_mode"], "prefab_lifecycle_card")
        self.assertEqual(row["sub_method"], "clt")
        self.assertEqual(row["value_low"], "null")
        self.assertEqual(row["value_high"], "null")
        self.assertEqual(row["source_key"], "unknown_import")
        self.assertEqual(metadata["extra_fields"]["sub_method"], "clt")

    def test_normalize_row_preserves_reclaimed_allocation_rule_metadata(self) -> None:
        methods_db = load_methods_db()
        row = normalize_row(
            "reclaimed_brick",
            {
                "phase": "structure",
                "parameter": "co2_kg_per_m2",
                "value_low": "8",
                "value_high": "25",
                "unit": "kg CO2eq / m2 GFA",
                "allocation_rule": "cut-off",
                "assumption": "Default overlay row",
                "source": "RBC EPD 2024 + Salmio & Huuhka 2026",
                "source_tier": "1",
            },
            methods_db,
        )

        metadata = json.loads(row["metadata"])
        self.assertEqual(row["data_model"], "overlay")
        self.assertEqual(row["display_mode"], "construction_phase_view")
        self.assertEqual(metadata["extra_fields"]["allocation_rule"], "cut-off")
        self.assertEqual(metadata["base_method"], "masonry")

    def test_calendar_days_are_not_multiplied_by_area(self) -> None:
        rules = load_normalization_rules()
        scenario = ScenarioInput(method="masonry", area_m2=100, floors=3)
        low, high, warning = scale_numeric_range("calendar_days", 3.0, 7.0, scenario, rules)
        self.assertEqual((low, high, warning), (3.0, 7.0, None))

    def test_days_per_m2_are_multiplied_by_area(self) -> None:
        rules = load_normalization_rules()
        scenario = ScenarioInput(method="masonry", area_m2=100, floors=3)
        low, high, warning = scale_numeric_range("days_per_m2", 0.4, 1.0, scenario, rules)
        self.assertEqual((low, high, warning), (40.0, 100.0, None))

    def test_days_per_m2_gfa_are_multiplied_by_area_and_floors(self) -> None:
        rules = load_normalization_rules()
        scenario = ScenarioInput(method="prefab", area_m2=100, floors=3, sub_method="clt")
        low, high, warning = scale_numeric_range(
            "days_per_m2_gfa",
            0.4,
            1.0,
            scenario,
            rules,
        )
        self.assertEqual((low, high, warning), (120.0, 300.0, None))

    def test_m2_wall_values_use_wall_to_gfa_ratio(self) -> None:
        rules = load_normalization_rules()
        scenario = ScenarioInput(method="masonry", area_m2=100, floors=2)
        low, high, warning = scale_numeric_range("per_m2_wall", 1.0, 2.0, scenario, rules)
        self.assertEqual((low, high, warning), (360.0, 720.0, None))

    def test_roof_area_values_use_footprint_area(self) -> None:
        rules = load_normalization_rules()
        scenario = ScenarioInput(method="masonry", area_m2=100, floors=3)
        low, high, warning = scale_numeric_range(
            "per_m2_roof_area",
            1.0,
            2.0,
            scenario,
            rules,
        )
        self.assertEqual((low, high, warning), (100.0, 200.0, None))

    def test_opening_area_values_use_gross_floor_area(self) -> None:
        rules = load_normalization_rules()
        scenario = ScenarioInput(method="masonry", area_m2=100, floors=3)
        low, high, warning = scale_numeric_range(
            "per_m2_opening_area",
            1.0,
            2.0,
            scenario,
            rules,
        )
        self.assertEqual((low, high, warning), (300.0, 600.0, None))

    def test_finished_surface_values_use_wall_surface_proxy(self) -> None:
        rules = load_normalization_rules()
        scenario = ScenarioInput(method="masonry", area_m2=100, floors=2)
        low, high, warning = scale_numeric_range(
            "per_m2_finished_surface",
            1.0,
            2.0,
            scenario,
            rules,
        )
        self.assertEqual((low, high, warning), (360.0, 720.0, None))

    def test_gfa_rows_scale_with_floor_count(self) -> None:
        floors_1 = build_method_output("masonry", area_m2=100, floors=1)
        floors_3 = build_method_output("masonry", area_m2=100, floors=3)
        row_1 = next(
            row for row in floors_1["stage_data"]["foundation"] if row["metric"] == "co2_kg_per_m2"
        )
        row_3 = next(
            row for row in floors_3["stage_data"]["foundation"] if row["metric"] == "co2_kg_per_m2"
        )
        self.assertEqual(row_3["scaled_low"], row_1["scaled_low"] * 3)
        self.assertEqual(row_3["scaled_high"], row_1["scaled_high"] * 3)

    def test_wall_rows_scale_with_floor_count(self) -> None:
        floors_1 = build_method_output("masonry", area_m2=100, floors=1)
        floors_3 = build_method_output("masonry", area_m2=100, floors=3)
        row_1 = next(
            row for row in floors_1["stage_data"]["structure"] if row["metric"] == "co2_kg_per_m2"
        )
        row_3 = next(
            row for row in floors_3["stage_data"]["structure"] if row["metric"] == "co2_kg_per_m2"
        )
        self.assertEqual(row_3["scaled_low"], row_1["scaled_low"] * 3)
        self.assertEqual(row_3["scaled_high"], row_1["scaled_high"] * 3)

    def test_calendar_days_do_not_change_with_floor_count_in_output(self) -> None:
        floors_1 = build_method_output("masonry", area_m2=100, floors=1)
        floors_4 = build_method_output("masonry", area_m2=100, floors=4)
        row_1 = next(
            row for row in floors_1["stage_data"]["foundation"] if row["metric"] == "time_days"
        )
        row_4 = next(
            row for row in floors_4["stage_data"]["foundation"] if row["metric"] == "time_days"
        )
        self.assertEqual(row_1["scaled_low"], row_4["scaled_low"])
        self.assertEqual(row_1["scaled_high"], row_4["scaled_high"])

    def test_prefab_output_uses_lifecycle_contract(self) -> None:
        output = build_method_output("prefab", area_m2=100, floors=2, sub_method="clt")
        self.assertEqual(output["method"], "prefab")
        self.assertEqual(output["data_model"], "lifecycle_based")
        self.assertEqual(output["display_mode"], "prefab_lifecycle_card")
        self.assertEqual(output["sub_method"], "clt")
        self.assertEqual(output["stages"], PREFAB_STAGES)
        self.assertEqual(list(output["stage_data"].keys()), PREFAB_STAGES)
        self.assertNotIn("foundation", output["stage_data"])

    def test_phase_based_output_uses_construction_phase_contract(self) -> None:
        output = build_method_output("masonry", area_m2=100, floors=1)
        self.assertEqual(output["data_model"], "phase_based")
        self.assertEqual(output["display_mode"], "construction_phase_view")
        self.assertEqual(output["stages"], PHASE_STAGES)
        self.assertEqual(list(output["stage_data"].keys()), PHASE_STAGES)

    def test_prefab_sub_methods_preserve_sub_method_and_change_values(self) -> None:
        clt = build_method_output("prefab", area_m2=100, floors=3, sub_method="clt")
        modular = build_method_output(
            "prefab",
            area_m2=100,
            floors=3,
            sub_method="modular_concrete",
        )
        self.assertEqual(clt["sub_method"], "clt")
        self.assertEqual(modular["sub_method"], "modular_concrete")
        clt_row = next(
            row for row in clt["stage_data"]["A1-A3"] if row["metric"] == "embodied_carbon_with_biogenic"
        )
        modular_row = next(
            row
            for row in modular["stage_data"]["A1-A3"]
            if row["metric"] == "embodied_carbon_spread"
        )
        self.assertNotEqual(clt_row["scaled_low"], modular_row["scaled_low"])
        self.assertNotEqual(clt_row["scaled_high"], modular_row["scaled_high"])

    def test_unknown_source_key_warning_does_not_crash(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            methods_root = Path(temp_dir)
            path = methods_root / "masonry.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=NORMALIZED_HEADER)
                writer.writeheader()
                writer.writerow(
                    {
                        "method": "masonry",
                        "data_model": "phase_based",
                        "display_mode": "construction_phase_view",
                        "phase": "foundation",
                        "lifecycle_stage": "",
                        "sub_method": "",
                        "metric": "time_days",
                        "value_low": "3",
                        "value_high": "7",
                        "unit": "days",
                        "basis": "calendar_days",
                        "source_key": "mystery-source",
                        "confidence_min": "0.5",
                        "confidence_max": "0.7",
                        "selected_material": "fired_clay_brick",
                        "notes": "Synthetic test row",
                        "metadata": json.dumps({"primary": True}),
                    }
                )

            output = build_method_output("masonry", area_m2=100, floors=2, methods_root=methods_root)
            self.assertIn("unknown_source_key", output["warnings"])
            self.assertEqual(len(output["stage_data"]["foundation"]), 1)

    def test_generated_normalized_source_keys_are_registered(self) -> None:
        rows_by_method = generate_normalized_rows()
        with tempfile.TemporaryDirectory() as temp_dir:
            methods_root = Path(temp_dir)
            for method, rows in rows_by_method.items():
                write_normalized_csv(method, rows, methods_root=methods_root)
            self.assertEqual(missing_source_registry_keys(methods_root), [])


if __name__ == "__main__":
    unittest.main()
