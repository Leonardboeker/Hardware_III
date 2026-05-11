"""lca_data — Script DAT.

Single source of truth bridge between data/methods_db.json and the TD network.
Paste into a Script DAT named 'lca_data'. Other operators read from it via
op('lca_data').

Table layout:
  Row 0          : column headers
  Rows 1-5       : one row per method  (type = 'method')
  Rows 6-10      : one row per phase   (type = 'phase')

Method columns:
  type | id | name | rfid_tag | r | g | b | co2_range | labor_range |
  time_range | cost_range | confidence_level | confidence_low |
  confidence_high | description | data_csv

Phase columns use: type | id | name | description (other cols are empty)

Usage from another Script:
  m = op('lca_data').findCell('MASONRY', cols=['name']).row
  color = (float(op('lca_data')[m, 'r']), float(op('lca_data')[m, 'g']), ...)

  phases = [op('lca_data')[r, 'name']
            for r in range(1, op('lca_data').numRows)
            if op('lca_data')[r, 'type'] == 'phase']
"""
import json
import os

DB_PATH = 'data/methods_db.json'   # relative to the .toe project folder

COLS = [
    'type', 'id', 'name', 'rfid_tag',
    'r', 'g', 'b',
    'co2_range', 'labor_range', 'time_range', 'cost_range',
    'confidence_level', 'confidence_low', 'confidence_high',
    'description', 'data_csv',
]


def cook(dat):
    dat.clear()
    dat.appendRow(COLS)

    toe_dir = project.folder
    db_file = os.path.join(toe_dir, DB_PATH)

    try:
        with open(db_file, 'r', encoding='utf-8') as f:
            db = json.load(f)
    except Exception as e:
        dat.appendRow(['ERROR'] + [str(e)] + [''] * (len(COLS) - 2))
        return

    for m in db.get('methods', []):
        r, g, b = m.get('color_rgb', [0.4, 0.4, 0.4])
        conf = m.get('confidence_range') or {}
        dat.appendRow([
            'method',
            m['id'],
            m['name'],
            m.get('rfid_tag') or '',
            f'{r:.4f}', f'{g:.4f}', f'{b:.4f}',
            m.get('co2_per_m2_range') or '',
            m.get('labor_hours_range') or '',
            m.get('time_range') or '',
            m.get('cost_per_m2_range') or '',
            conf.get('level', ''),
            f'{conf["score_low"]:.2f}' if 'score_low' in conf else '',
            f'{conf["score_high"]:.2f}' if 'score_high' in conf else '',
            m.get('description') or '',
            m.get('data_csv') or '',
        ])

    for p in db.get('phases', []):
        dat.appendRow([
            'phase',
            p['id'],
            p['name'],
            '',                          # rfid_tag
            '', '', '',                  # r g b
            '', '', '', '',              # metric ranges
            '', '', '',                  # confidence
            p.get('description', ''),
            '',                          # data_csv
        ])
