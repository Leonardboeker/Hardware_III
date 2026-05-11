import unittest

from touchdesigner.scripts.metric_ui_bootstrap import (
    PANEL_LAYOUT,
    PROJ_H,
    PROJ_W,
    bootstrap_manifest,
    panel_text_expression,
    text_top_name,
)


class TouchDesignerBootstrapTests(unittest.TestCase):
    def test_manifest_uses_1280x720_projection_resolution(self) -> None:
        manifest = bootstrap_manifest()
        self.assertEqual(manifest["resolution"], (PROJ_W, PROJ_H))
        self.assertEqual((PROJ_W, PROJ_H), (1280, 720))

    def test_panel_layout_matches_scaled_simulation_geometry(self) -> None:
        self.assertEqual(PANEL_LAYOUT["top_phase_navigation"], (271, 15, 600, 67))
        self.assertEqual(PANEL_LAYOUT["method_selection"], (337, 493, 560, 173))
        self.assertEqual(PANEL_LAYOUT["bar_bottom_status"], (0, 687, 1280, 33))

    def test_text_top_manifest_uses_expected_names(self) -> None:
        manifest = bootstrap_manifest()
        names = [entry["name"] for entry in manifest["text_tops"]]
        self.assertIn("text_top_phase_navigation", names)
        self.assertIn("text_method_selection", names)
        self.assertEqual(text_top_name("right_phase_preview"), "text_right_phase_preview")

    def test_all_text_tops_share_the_same_storage_expression(self) -> None:
        self.assertEqual(panel_text_expression(), 'parent().fetch(me.name, "")')


if __name__ == "__main__":
    unittest.main()
