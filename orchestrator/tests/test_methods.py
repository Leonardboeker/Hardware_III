"""MethodDB unit tests. Uses a temp JSON file so the real methods_db.json
in the repo stays untouched.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from orchestrator.methods import (
    DEFAULT_MAX_FLOORS,
    DEFAULT_N_PHASES,
    Method,
    MethodDB,
)


@pytest.fixture
def minimal_db(tmp_path) -> Path:
    """A methods_db.json missing the new n_phases / phase_names fields —
    matches the current repo state pre-Plan-03-Task-1."""
    db = {
        "methods": [
            {"id": 0, "name": "NONE",            "rfid_tag": None,             "min_pucks": 0,  "max_pucks": 10, "color_rgb": [0.4, 0.4, 0.4]},
            {"id": 1, "name": "MASONRY",         "rfid_tag": "0430BF011F5713", "min_pucks": 3,  "max_pucks": 10, "color_rgb": [0.6, 0.3, 0.2]},
            {"id": 2, "name": "3D PRINTED",      "rfid_tag": "AAAAAAAA",       "min_pucks": 3,  "max_pucks": 10, "color_rgb": [0.2, 0.6, 0.8]},
        ]
    }
    p = tmp_path / "methods_db.json"
    p.write_text(json.dumps(db), encoding="utf-8")
    return p


@pytest.fixture
def full_db(tmp_path) -> Path:
    """A methods_db.json with the new fields filled in — what we want after Plan 03 Task 1."""
    db = {
        "methods": [
            {"id": 0, "name": "NONE", "rfid_tag": None, "min_pucks": 0, "max_pucks": 10,
             "color_rgb": [0.4, 0.4, 0.4], "max_floors": 5, "n_phases": 5,
             "phase_names": ["Foundation", "Structure", "Roof", "Openings", "Finishing"]},
            {"id": 1, "name": "MASONRY", "rfid_tag": "0430BF011F5713", "min_pucks": 3, "max_pucks": 10,
             "color_rgb": [0.6, 0.3, 0.2], "max_floors": 5, "n_phases": 5,
             "phase_names": ["Foundation", "Structure", "Roof", "Openings", "Finishing"]},
            {"id": 2, "name": "3D PRINTED", "rfid_tag": "AAAAAAAA", "min_pucks": 3, "max_pucks": 10,
             "color_rgb": [0.2, 0.6, 0.8], "max_floors": 1, "n_phases": 3,
             "phase_names": ["Foundation", "Print", "Finishing"]},
            {"id": 3, "name": "PREFAB", "rfid_tag": "BBBBBBBB", "min_pucks": 3, "max_pucks": 10,
             "color_rgb": [0.3, 0.5, 0.4], "max_floors": 4, "n_phases": 4,
             "phase_names": ["Foundation", "Assemble", "Roof", "Openings"]},
        ]
    }
    p = tmp_path / "methods_db.json"
    p.write_text(json.dumps(db), encoding="utf-8")
    return p


# ----- Loading -----

class TestLoading:
    def test_loads_full_db(self, full_db):
        mdb = MethodDB(path=full_db)
        assert len(mdb.all_methods()) == 4

    def test_loads_minimal_db_with_defaults(self, minimal_db):
        mdb = MethodDB(path=minimal_db)
        masonry = mdb.by_id(1)
        # Missing fields fall back to safe defaults
        assert masonry.max_floors == DEFAULT_MAX_FLOORS
        assert masonry.n_phases == DEFAULT_N_PHASES
        assert masonry.phase_names == ["Foundation", "Structure", "Roof", "Openings", "Finishing"]

    def test_loads_missing_file(self, tmp_path):
        mdb = MethodDB(path=tmp_path / "does_not_exist.json")
        assert mdb.all_methods() == []
        none = mdb.none_method()
        assert none.id == 0 and none.name == "NONE"


# ----- Lookups -----

class TestLookups:
    def test_by_id(self, full_db):
        mdb = MethodDB(path=full_db)
        assert mdb.by_id(1).name == "MASONRY"
        assert mdb.by_id(2).name == "3D PRINTED"
        # Unknown -> NONE
        assert mdb.by_id(999).name == "NONE"

    def test_by_tag(self, full_db):
        mdb = MethodDB(path=full_db)
        assert mdb.by_tag("0430BF011F5713").id == 1
        # Case-insensitive
        assert mdb.by_tag("aaaaaaaa").id == 2
        # Unknown tag -> None
        assert mdb.by_tag("DEADBEEF") is None


# ----- Per-method n_phases truncation/padding -----

class TestPhaseNamesNormalization:
    def test_truncates_too_long_list(self, tmp_path):
        db = {"methods": [{
            "id": 1, "name": "X", "rfid_tag": None, "n_phases": 3,
            "phase_names": ["A", "B", "C", "D", "E"]
        }]}
        p = tmp_path / "db.json"
        p.write_text(json.dumps(db))
        mdb = MethodDB(path=p)
        assert mdb.by_id(1).phase_names == ["A", "B", "C"]

    def test_pads_too_short_list(self, tmp_path):
        db = {"methods": [{
            "id": 1, "name": "X", "rfid_tag": None, "n_phases": 5,
            "phase_names": ["A", "B"]
        }]}
        p = tmp_path / "db.json"
        p.write_text(json.dumps(db))
        mdb = MethodDB(path=p)
        # Padded with default phase names
        names = mdb.by_id(1).phase_names
        assert len(names) == 5
        assert names[:2] == ["A", "B"]
