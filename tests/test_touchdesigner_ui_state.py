import unittest

from touchdesigner.scripts.metrics_engine import compute_metrics
from touchdesigner.scripts.ui_state import (
    build_ui_state,
    compute_and_store_touchdesigner_ui,
)


class _DummyOwner:
    def __init__(self, initial: dict[str, object] | None = None) -> None:
        self._storage = dict(initial or {})

    def fetch(self, key: str, default: object = None) -> object:
        return self._storage.get(key, default)

    def store(self, key: str, value: object) -> None:
        self._storage[key] = value


class TouchDesignerUiStateTests(unittest.TestCase):
    def test_build_ui_state_for_masonry_exposes_phase_path_text(self) -> None:
        metrics_output = compute_metrics(
            {
                "construction_method": "masonry",
                "area_m2": 100,
                "number_of_floors": 2,
            }
        )

        ui_state = build_ui_state(
            metrics_output,
            live_state={"hb_alive": 1, "area_m2": 100, "number_of_floors": 2},
        )

        self.assertEqual(ui_state["method_label"], "Masonry")
        self.assertEqual(ui_state["path_label"], "Phase Path")
        self.assertEqual(ui_state["active_stage_label"], "1 Foundation")
        self.assertEqual(ui_state["phase_navigation_mode"], "phase")
        self.assertEqual(ui_state["guidance_target"], "floor_control")
        self.assertIn("left_info_scale_value", ui_state["guidance_highlight_blocks"])
        self.assertEqual(ui_state["phase_navigation_items"][0]["label"], "1 Foundation")
        self.assertEqual(ui_state["panel_texts"]["top_phase_chip_2"], "2 Walls")
        self.assertIn("YOUR SELECTION", ui_state["panel_texts"]["left_info"])
        self.assertIn("MASONRY", ui_state["panel_texts"]["method_card_masonry"])
        self.assertIn("1 CHOOSE METHOD", ui_state["panel_texts"]["bar_bottom_status"])

    def test_build_ui_state_for_prefab_exposes_lifecycle_mode_and_sub_method(self) -> None:
        metrics_output = compute_metrics(
            {
                "construction_method": "prefab",
                "area_m2": 100,
                "number_of_floors": 3,
            }
        )

        ui_state = build_ui_state(
            metrics_output,
            live_state={"hb_alive": 1, "area_m2": 100, "number_of_floors": 3},
        )

        self.assertEqual(ui_state["method_label"], "Prefab")
        self.assertEqual(ui_state["path_label"], "Lifecycle Path")
        self.assertEqual(ui_state["active_stage_label"], "Production")
        self.assertEqual(ui_state["phase_navigation_mode"], "lifecycle")
        self.assertEqual(ui_state["guidance_target"], "floor_control")
        self.assertEqual(ui_state["panel_texts"]["top_phase_chip_1"], "A1-A3")
        self.assertIn("Production", ui_state["panel_texts"]["right_phase_preview_right"])
        self.assertIn("PREFAB", ui_state["panel_texts"]["method_card_prefab"])
        self.assertIn("CLT", ui_state["panel_texts"]["right_phase_preview_right"])
        self.assertEqual(
            ui_state["available_sub_methods"],
            [
                {"key": "clt", "label": "CLT"},
                {"key": "modular_concrete", "label": "Modular Concrete"},
            ],
        )

    def test_compute_and_store_touchdesigner_ui_writes_panel_text_storage(self) -> None:
        metrics_output = compute_metrics(
            {
                "construction_method": "masonry",
                "area_m2": 120,
                "number_of_floors": 2,
                "current_phase": "roof",
            }
        )
        owner = _DummyOwner(
            {
                "metrics_output": metrics_output,
                "hb_alive": 1,
                "area_m2": 120,
                "number_of_floors": 2,
            }
        )

        ui_state = compute_and_store_touchdesigner_ui(owner=owner)

        self.assertIn("ui_state", owner._storage)
        self.assertIn("ui_panel_texts", owner._storage)
        self.assertIn("text_top_phase_navigation", owner._storage)
        self.assertIn("text_top_phase_chip_3", owner._storage)
        self.assertIn("text_right_phase_preview", owner._storage)
        self.assertEqual(ui_state["active_stage_label"], "3 Roof")
        self.assertIn("3 Roof", owner._storage["text_right_phase_preview_right"])
        self.assertEqual(owner._storage["text_top_phase_chip_3"], "3 Roof")
        self.assertIn("TOTAL PROJECT IMPACT", owner._storage["text_right_cost_chart"])
        self.assertEqual(
            owner._storage["text_stats_text"],
            owner._storage["ui_panel_texts"]["stats_text"],
        )

    def test_guidance_advances_from_floor_to_phase_to_plan(self) -> None:
        metrics_output = compute_metrics(
            {
                "construction_method": "masonry",
                "area_m2": 120,
                "number_of_floors": 3,
                "current_phase": "roof",
            }
        )

        floor_guided = build_ui_state(
            metrics_output,
            live_state={
                "hb_alive": 1,
                "area_m2": 120,
                "number_of_floors": 3,
            },
        )
        self.assertEqual(floor_guided["guidance_target"], "floor_control")

        phase_guided = build_ui_state(
            metrics_output,
            live_state={
                "hb_alive": 1,
                "area_m2": 120,
                "number_of_floors": 3,
                "floor_control_dirty": 1,
            },
        )
        self.assertEqual(phase_guided["guidance_target"], "phase_navigation")
        self.assertIn("top_phase_chip_3", phase_guided["guidance_highlight_blocks"])

        plan_guided = build_ui_state(
            metrics_output,
            live_state={
                "hb_alive": 1,
                "area_m2": 120,
                "number_of_floors": 3,
                "floor_control_dirty": 1,
                "phase_control_dirty": 1,
            },
        )
        self.assertEqual(plan_guided["guidance_target"], "main_plan_simulation")
        self.assertIn("main_plan_simulation", plan_guided["guidance_highlight_blocks"])


if __name__ == "__main__":
    unittest.main()
