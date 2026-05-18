"""Method-database loader. Reads data/methods_db.json.

Provides lookup by id, RFID tag, or name. Tolerates the current JSON shape
(min_pucks, max_pucks, rfid_tag, color_rgb) plus the planned Slider B
amendment fields (n_phases, phase_names) — falls back to safe defaults if
those aren't there yet.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from . import config

logger = logging.getLogger(__name__)


# Locked from PROJECT.md and Plan 02 CONTEXT
DEFAULT_PHASE_NAMES = [
    "Foundation", "Structure", "Roof", "Openings", "Finishing",
]
DEFAULT_N_PHASES = 5
DEFAULT_MAX_FLOORS = 5


@dataclass
class Method:
    """One construction method as understood by the runtime."""
    id: int
    name: str
    color_rgb: tuple[float, float, float]
    rfid_tag: Optional[str]
    min_pucks: int
    max_pucks: int
    max_floors: int
    n_phases: int
    phase_names: list[str]
    # Free-form pass-through of any extra keys for forward-compat
    extras: dict = field(default_factory=dict)

    @classmethod
    def from_db_entry(cls, entry: dict) -> "Method":
        n_phases = int(entry.get("n_phases", DEFAULT_N_PHASES))
        phase_names = entry.get("phase_names")
        if not phase_names or not isinstance(phase_names, list):
            phase_names = DEFAULT_PHASE_NAMES[:n_phases]
        # If phase_names is shorter than n_phases, pad with defaults; if longer, truncate
        if len(phase_names) < n_phases:
            phase_names = list(phase_names) + DEFAULT_PHASE_NAMES[len(phase_names):n_phases]
        elif len(phase_names) > n_phases:
            phase_names = phase_names[:n_phases]

        color = entry.get("color_rgb") or [0.5, 0.5, 0.5]
        if len(color) >= 3:
            color_rgb = (float(color[0]), float(color[1]), float(color[2]))
        else:
            color_rgb = (0.5, 0.5, 0.5)

        known_keys = {
            "id", "name", "color_rgb", "rfid_tag",
            "min_pucks", "max_pucks", "max_floors",
            "n_phases", "phase_names",
        }
        extras = {k: v for k, v in entry.items() if k not in known_keys}

        return cls(
            id=int(entry.get("id", -1)),
            name=str(entry.get("name", "UNKNOWN")),
            color_rgb=color_rgb,
            rfid_tag=(str(entry["rfid_tag"]).upper() if entry.get("rfid_tag") else None),
            min_pucks=int(entry.get("min_pucks", 3)),
            max_pucks=int(entry.get("max_pucks", 10)),
            max_floors=int(entry.get("max_floors", DEFAULT_MAX_FLOORS)),
            n_phases=n_phases,
            phase_names=phase_names,
            extras=extras,
        )


class MethodDB:
    """Holds all methods + lookups. Reload-safe."""

    def __init__(self, path: Path = config.METHODS_DB_PATH):
        self.path = Path(path)
        self._methods_by_id: dict[int, Method] = {}
        self._methods_by_tag: dict[str, Method] = {}
        self.load()

    def load(self) -> None:
        try:
            with self.path.open("r", encoding="utf-8") as f:
                raw = json.load(f)
        except FileNotFoundError:
            logger.error("methods_db.json not found at %s — using empty DB", self.path)
            self._methods_by_id = {}
            self._methods_by_tag = {}
            return
        except json.JSONDecodeError as e:
            logger.error("methods_db.json invalid JSON: %s — using empty DB", e)
            return

        self._methods_by_id.clear()
        self._methods_by_tag.clear()
        for entry in raw.get("methods", []):
            m = Method.from_db_entry(entry)
            self._methods_by_id[m.id] = m
            if m.rfid_tag:
                self._methods_by_tag[m.rfid_tag] = m

        logger.info("methods_db loaded: %d methods (%s)",
                    len(self._methods_by_id),
                    ", ".join(m.name for m in self._methods_by_id.values()))

    def by_id(self, method_id: int) -> Method:
        return self._methods_by_id.get(int(method_id), self.none_method())

    def by_tag(self, rfid_tag: str) -> Optional[Method]:
        return self._methods_by_tag.get(str(rfid_tag).upper())

    def none_method(self) -> Method:
        """Safe fallback for unknown / unset method."""
        return self._methods_by_id.get(0) or Method(
            id=0, name="NONE", color_rgb=(0.5, 0.5, 0.5),
            rfid_tag=None, min_pucks=3, max_pucks=10,
            max_floors=DEFAULT_MAX_FLOORS,
            n_phases=DEFAULT_N_PHASES,
            phase_names=list(DEFAULT_PHASE_NAMES),
        )

    def all_methods(self) -> list[Method]:
        return list(self._methods_by_id.values())
