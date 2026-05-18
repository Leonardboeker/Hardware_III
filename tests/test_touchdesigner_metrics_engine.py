import unittest

from touchdesigner.scripts.metrics_engine import compute_metrics


class TouchDesignerMetricsEngineTests(unittest.TestCase):
    def test_masonry_metrics_use_normalized_pipeline(self) -> None:
        result = compute_metrics(
            {
                "construction_method": "masonry",
                "area_m2": 100,
                "number_of_floors": 2,
            }
        )

        self.assertEqual(result["data_model"], "phase_based")
        self.assertEqual(
            result["stage_sequence"],
            ["foundation", "structure", "roof", "openings", "finishing"],
        )
        self.assertEqual(result["path_label"], "Phase Path")
        self.assertTrue(result["phase_navigation_enabled"])
        self.assertEqual(result["stage_selection"]["resolved_stage"], "foundation")
        self.assertEqual(result["active_stage"]["stage"], "foundation")
        self.assertIn("structure", result["phase_breakdown"])
        self.assertIsNotNone(result["co2_estimate"]["low"])
        self.assertIsNotNone(result["cost_estimate"]["high"])

    def test_prefab_metrics_expose_lifecycle_stage_sequence(self) -> None:
        result = compute_metrics(
            {
                "construction_method": "prefab",
                "area_m2": 100,
                "number_of_floors": 3,
            }
        )

        self.assertEqual(result["data_model"], "lifecycle_based")
        self.assertEqual(result["sub_method"], "clt")
        self.assertEqual(result["sub_method_label"], "CLT")
        self.assertEqual(result["path_label"], "Lifecycle Path")
        self.assertFalse(result["phase_navigation_enabled"])
        self.assertEqual(result["stage_sequence"], ["A1-A3", "A4", "A5", "B", "C"])
        self.assertEqual(result["stage_labels"]["A1-A3"], "Production")
        self.assertEqual(result["stage_selection"]["resolved_stage"], "A1-A3")
        self.assertEqual(result["active_stage"]["label"], "Production")
        self.assertEqual(
            result["available_sub_methods"],
            [
                {"key": "clt", "label": "CLT"},
                {"key": "modular_concrete", "label": "Modular Concrete"},
            ],
        )
        self.assertEqual(len(result["stage_summaries"]), 5)
        self.assertTrue(result["stage_summaries"][0]["is_active"])
        self.assertIn("A1-A3", result["phase_breakdown"])

    def test_shape_factor_still_scales_structure_for_td_compatibility(self) -> None:
        base = compute_metrics(
            {
                "construction_method": "masonry",
                "area_m2": 100,
                "number_of_floors": 2,
                "shape_factor": 1.0,
            }
        )
        adjusted = compute_metrics(
            {
                "construction_method": "masonry",
                "area_m2": 100,
                "number_of_floors": 2,
                "shape_factor": 1.5,
            }
        )

        base_structure = base["phase_breakdown"]["structure"]["co2_kg_per_m2"]["low"]
        adjusted_structure = adjusted["phase_breakdown"]["structure"]["co2_kg_per_m2"]["low"]
        self.assertGreater(adjusted_structure, base_structure)

    def test_current_phase_selects_active_stage_when_available(self) -> None:
        result = compute_metrics(
            {
                "construction_method": "masonry",
                "area_m2": 100,
                "number_of_floors": 2,
                "current_phase": "roof",
            }
        )

        self.assertEqual(result["stage_selection"]["selection_mode"], "explicit")
        self.assertEqual(result["active_stage"]["stage"], "roof")
        self.assertEqual(result["active_stage"]["label"], "3 Roof")

    def test_prefab_defaults_to_first_lifecycle_stage_when_legacy_phase_is_requested(self) -> None:
        result = compute_metrics(
            {
                "construction_method": "prefab",
                "area_m2": 100,
                "number_of_floors": 3,
                "current_phase": "structure",
            }
        )

        self.assertEqual(
            result["stage_selection"]["selection_mode"],
            "unmatched_default_first",
        )
        self.assertEqual(result["active_stage"]["stage"], "A1-A3")
        self.assertEqual(result["active_stage"]["label"], "Production")


if __name__ == "__main__":
    unittest.main()
