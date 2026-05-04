"""Footprint visualizer — Script TOP callbacks for TouchDesigner.

Reads per-puck OSC data from oscin1, draws:
  - Circles at each detected puck center
  - Lines connecting pucks in ID order (polygon)
  - Distance labels on each edge
  - Area of the polygon (Shoelace formula)

Paste the entire contents into a Script TOP DAT in TD (1280x720 resolution).
oscin1 must be on port 7000 and receive the /puck/N protocol from osc_send.py.

Channel names from OSC In CHOP:
  puck/N:0  = frame number when last seen
  puck/N:1  = projector x
  puck/N:2  = projector y
  vision/heartbeat:0 = current frame counter
"""
from PIL import Image, ImageDraw
import numpy

PROJ_W = 1280
PROJ_H = 720
FOOTPRINT_IDS = list(range(10))  # ArUco IDs 0-9 are footprint pucks
LIVENESS_FRAMES = 10             # frames before a puck is considered lost

COLOR_LINE    = (255, 255, 255, 200)
COLOR_PUCK    = (0, 255, 100, 255)
COLOR_DIST    = (255, 220, 0, 255)
COLOR_AREA    = (100, 200, 255, 255)
COLOR_STATUS  = (180, 180, 180, 255)


def cook(scriptOp):
    osc = op('oscin1')

    try:
        hb = int(osc['vision/heartbeat:0'][0])
    except Exception:
        hb = -1

    pucks = {}
    for pid in FOOTPRINT_IDS:
        try:
            puck_frame = int(osc[f'puck/{pid}:0'][0])
            if hb >= 0 and abs(hb - puck_frame) <= LIVENESS_FRAMES:
                px = float(osc[f'puck/{pid}:1'][0])
                py = float(osc[f'puck/{pid}:2'][0])
                pucks[pid] = (px, py)
        except Exception:
            pass

    img = Image.new('RGBA', (PROJ_W, PROJ_H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    ids_sorted = sorted(pucks.keys())
    pts = [pucks[i] for i in ids_sorted]

    if len(pts) >= 2:
        for i in range(len(pts)):
            p1 = pts[i]
            p2 = pts[(i + 1) % len(pts)]
            draw.line([(p1[0], p1[1]), (p2[0], p2[1])], fill=COLOR_LINE, width=2)

            dist_px = ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
            mid = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
            draw.text((mid[0] + 5, mid[1] - 16), f"{dist_px:.0f}px", fill=COLOR_DIST)

    for pid, (px, py) in pucks.items():
        r = 12
        draw.ellipse([px - r, py - r, px + r, py + r], outline=COLOR_PUCK, width=3)
        draw.text((px + 16, py - 10), f"#{pid}", fill=COLOR_PUCK)

    if len(pts) >= 3:
        area = _shoelace(pts)
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        draw.text((cx - 60, cy - 10), f"Area: {area:.0f} px²", fill=COLOR_AREA)

    draw.text((20, 20), f"Pucks: {len(pucks)} / 10", fill=COLOR_STATUS)
    if hb < 0:
        draw.text((20, 50), "Vision: OFFLINE", fill=(255, 80, 80, 255))

    img_np = numpy.array(img).astype(numpy.float32) / 255.0
    scriptOp.copyNumpyArray(img_np)


def _shoelace(points):
    n = len(points)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    return abs(area) / 2.0
