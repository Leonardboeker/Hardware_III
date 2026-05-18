"""lca_data - Script DAT.

Single source of truth bridge between data/methods_db.json and the
TouchDesigner network.

Paste into a Script DAT named "lca_data". Other operators can then read
rows from op("lca_data").
"""
import json
import os

DB_PATH = "data/methods_db.json"

COLS = [
    "type",
    "id",
    "name",
    "rfid_tag",
    "r",
    "g",
    "b",
    "co2_range",
    "labor_range",
    "time_range",
    "cost_range",
    "confidence_level",
    "confidence_low",
    "confidence_high",
    "description",
    "data_csv",
]


def cook(dat):
    dat.clear()
    dat.appendRow(COLS)

    toe_dir = project.folder
    db_file = os.path.join(toe_dir, DB_PATH)

    try:
        with open(db_file, "r", encoding="utf-8") as handle:
            database = json.load(handle)
    except Exception as exc:
        dat.appendRow(["ERROR", str(exc)] + [""] * (len(COLS) - 2))
        return

    for method in database.get("methods", []):
        red, green, blue = method.get("color_rgb", [0.4, 0.4, 0.4])
        confidence = method.get("confidence_range") or {}
        dat.appendRow([
            "method",
            method["id"],
            method["name"],
            method.get("rfid_tag") or "",
            f"{red:.4f}",
            f"{green:.4f}",
            f"{blue:.4f}",
            method.get("co2_per_m2_range") or "",
            method.get("labor_hours_range") or "",
            method.get("time_range") or "",
            method.get("cost_per_m2_range") or "",
            confidence.get("level", ""),
            f"{confidence['score_low']:.2f}" if "score_low" in confidence else "",
            f"{confidence['score_high']:.2f}" if "score_high" in confidence else "",
            method.get("description") or "",
            method.get("data_csv") or "",
        ])

    for phase in database.get("phases", []):
        dat.appendRow([
            "phase",
            phase["id"],
            phase["name"],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            phase.get("description", ""),
            "",
        ])
