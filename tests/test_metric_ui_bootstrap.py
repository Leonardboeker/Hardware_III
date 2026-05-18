import unittest

from touchdesigner.scripts.metric_ui_bootstrap import (
    bootstrap_manifest,
    building_part_summary,
    set_current_phase,
    set_floor_count,
    set_floor_count_from_scroller,
    set_phase_from_scroller,
    select_building_part_at,
    set_selected_building_parts,
    toggle_selected_building_part,
)


class _OwnerStub:
    def __init__(self) -> None:
        self.storage: dict[str, object] = {}

    def store(self, key: str, value: object) -> None:
        self.storage[key] = value

    def fetch(self, key: str, default: object = None) -> object:
        return self.storage.get(key, default)

    def op(self, _name: str) -> None:
        return None


class MetricUiBootstrapSelectionTests(unittest.TestCase):
    def test_whole_building_summary_uses_all_zone_totals(self) -> None:
        owner = _OwnerStub()

        summary = building_part_summary(owner=owner)

        self.assertEqual(summary["selected_part_label"], "Whole Building")
        self.assertEqual(summary["selected_parts_count"], 0)
        self.assertEqual(summary["area_m2"], 342.0)
        self.assertEqual(summary["selected_wall_area_m2"], 775.0)
        self.assertEqual(summary["selected_perimeter_m"], 253.0)

    def test_setting_single_zone_updates_selected_area(self) -> None:
        owner = _OwnerStub()

        summary = set_selected_building_parts(["zone_north_wing"], owner=owner)

        self.assertEqual(summary["selected_zone_ids"], ["zone_north_wing"])
        self.assertEqual(summary["selected_part_label"], "North Wing")
        self.assertEqual(summary["selected_parts_count"], 1)
        self.assertEqual(summary["area_m2"], 68.0)
        self.assertEqual(owner.fetch("area_m2"), 68.0)
        self.assertEqual(owner.fetch("building_part_interacted"), 1)

    def test_toggling_same_zone_without_additive_clears_selection(self) -> None:
        owner = _OwnerStub()
        set_selected_building_parts(["zone_north_wing"], owner=owner)

        summary = toggle_selected_building_part(
            "zone_north_wing",
            owner=owner,
        )

        self.assertEqual(summary["selected_zone_ids"], [])
        self.assertEqual(summary["selected_part_label"], "Whole Building")
        self.assertEqual(summary["area_m2"], 342.0)

    def test_hit_test_prefers_more_specific_inner_zone(self) -> None:
        owner = _OwnerStub()

        summary = select_building_part_at(420, 230, owner=owner)

        self.assertEqual(summary["selected_zone_ids"], ["zone_courtyard"])
        self.assertEqual(summary["selected_part_label"], "Courtyard")
        self.assertEqual(summary["area_m2"], 36.0)

    def test_floor_scroller_maps_segment_to_method_aware_floor_count(self) -> None:
        owner = _OwnerStub()
        owner.store("current_method", "masonry")
        owner.store("selected_material", "fired_clay_brick")

        summary = set_floor_count_from_scroller(65, owner=owner)

        self.assertEqual(summary["applied_floors"], 4)
        self.assertEqual(owner.fetch("number_of_floors"), 4)
        self.assertEqual(owner.fetch("floor_control_dirty"), 1)

    def test_phase_scroller_maps_construction_segments(self) -> None:
        owner = _OwnerStub()
        owner.store("current_method", "masonry")
        owner.store("selected_material", "fired_clay_brick")

        summary = set_phase_from_scroller(44, owner=owner)

        self.assertEqual(summary["selected_stage"], "roof")
        self.assertEqual(owner.fetch("current_phase_name"), "roof")
        self.assertEqual(owner.fetch("phase_control_dirty"), 1)

    def test_prefab_phase_scroller_switches_sub_method_track(self) -> None:
        owner = _OwnerStub()
        owner.store("current_method", "prefab")
        owner.store("selected_material", "timber_clt_prefab")
        owner.store("number_of_floors", 3)

        summary = set_phase_from_scroller(72, owner=owner)

        self.assertEqual(summary["scroller_mode"], "prefab_lifecycle")
        self.assertEqual(summary["sub_method"], "modular_concrete")
        self.assertEqual(summary["selected_stage"], "A5")
        self.assertEqual(owner.fetch("selected_material"), "modular_concrete_prefab")
        self.assertEqual(owner.fetch("current_phase_name"), "A5")

    def test_direct_floor_and_phase_setters_mark_guidance_progress(self) -> None:
        owner = _OwnerStub()
        owner.store("current_method", "masonry")
        owner.store("selected_material", "fired_clay_brick")

        set_floor_count(3, owner=owner)
        set_current_phase("roof", owner=owner)

        self.assertEqual(owner.fetch("floor_control_dirty"), 1)
        self.assertEqual(owner.fetch("phase_control_dirty"), 1)

    def test_manifest_exposes_method_preview_assets(self) -> None:
        manifest = bootstrap_manifest()

        previews = manifest["method_previews"]
        self.assertEqual(len(previews), 3)
        self.assertEqual(previews[0]["node_name"], "method_preview_masonry")
        self.assertTrue(previews[0]["relative_path"].endswith("masonry_mode.gif"))


if __name__ == "__main__":
    unittest.main()
