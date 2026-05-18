"""
Hardware III — ESP32 + RC522 RFID Housing Render
=================================================
blender --background --python render_enclosure.py
Output: cad/enclosure/render_enclosure.png
"""

import bpy
import math
import os

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "render_enclosure.png")

# ── Dimensions (mm) ───────────────────────────────────────────────────────────
BASE_W, BASE_D, BASE_H = 160, 126,  9
BODY_W, BODY_D, BODY_H = 140, 110, 54
TRAY_W, TRAY_D, TRAY_H =  92,  66,  3   # recessed token landing pad
TRAY_Y                  =  -4            # tray shifted slightly toward front


# ── Helpers ───────────────────────────────────────────────────────────────────

def clear():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=True)


def prim_box(name, w, d, h, z0, cx=0, cy=0):
    """Blender primitive cube — correct normals guaranteed."""
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(cx, cy, z0 + h / 2)
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (w, d, h)
    bpy.ops.object.transform_apply(scale=True)
    return obj


def assign(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def mat(name, r, g, b, rough=0.72):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (r, g, b, 1.0)
    bsdf.inputs["Roughness"].default_value  = rough
    for k in ("Specular IOR Level", "Specular"):
        if k in bsdf.inputs:
            bsdf.inputs[k].default_value = 0.02
            break
    return m


def soft_edge(obj, width=1.2, segs=3):
    mod = obj.modifiers.new("Bevel", 'BEVEL')
    mod.width    = width
    mod.segments = segs
    mod.limit_method = 'ANGLE'
    mod.angle_limit  = math.radians(80)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier="Bevel")


# ── Build ─────────────────────────────────────────────────────────────────────

def build():
    M_white  = mat("White",  0.92, 0.91, 0.90, rough=0.68)
    M_tray   = mat("Tray",   0.62, 0.62, 0.61, rough=0.84)
    M_rim    = mat("Rim",    0.80, 0.80, 0.79, rough=0.76)
    M_ground = mat("Ground", 0.96, 0.96, 0.97, rough=1.00)

    # Ground
    bpy.ops.mesh.primitive_plane_add(size=1400, location=(0, 0, -0.5))
    assign(bpy.context.active_object, M_ground)

    # Base slab — slightly wider foot
    base = prim_box("Base", BASE_W, BASE_D, BASE_H, z0=0)
    soft_edge(base, width=2.0)
    assign(base, M_white)

    # Main body
    body_z = BASE_H
    body = prim_box("Body", BODY_W, BODY_D, BODY_H, z0=body_z)
    soft_edge(body, width=1.2)
    assign(body, M_white)

    # ── Tray landing pad ──────────────────────────────────────────────────────
    # Instead of a boolean cut: place a thin dark panel on the top face,
    # set 0.1mm above to avoid z-fighting. Gives a clean visual "recess" zone.
    body_top = body_z + BODY_H

    # Outer tray frame strip (rim around the pad — slightly lighter)
    rim = prim_box("TrayRim", TRAY_W + 4, TRAY_D + 4, 0.6,
                   z0=body_top, cx=0, cy=TRAY_Y)
    assign(rim, M_rim)

    # Inner pad (the actual surface where the token sits — darker)
    pad = prim_box("TrayPad", TRAY_W, TRAY_D, 0.4,
                   z0=body_top + 0.3, cx=0, cy=TRAY_Y)
    assign(pad, M_tray)

    # Small raised border around pad to define the slot edge
    for dx, dy, sw, sd in [
        (0,                    (TRAY_D/2 + 1.5)/1, TRAY_W + 8, 3),   # front
        (0,                   -(TRAY_D/2 + 1.5)/1, TRAY_W + 8, 3),   # back
        (-(TRAY_W/2 + 1.5)/1,  0,                  3, TRAY_D + 8),   # left
        ( (TRAY_W/2 + 1.5)/1,  0,                  3, TRAY_D + 8),   # right
    ]:
        pass  # clean design without raised rails

    housing_mid = body_z + BODY_H / 2
    return housing_mid


# ── Lighting ──────────────────────────────────────────────────────────────────

def lighting():
    def area(loc, rot_deg, energy, size):
        bpy.ops.object.light_add(type='AREA', location=loc)
        lt = bpy.context.active_object
        lt.data.energy = energy
        lt.data.size   = size
        lt.rotation_euler = [math.radians(r) for r in rot_deg]

    area(( 200, -170, 340), ( 52,  0,  30), 32000, 180)  # key
    area((-280,  -60, 220), ( 38,  0, -48),  9000, 300)  # fill
    area((   0,  270, 260), (-42,  0,   0), 16000, 150)  # rim
    area((   0,    0, 480), (  0,  0,   0),  4500, 460)  # top


# ── Camera ────────────────────────────────────────────────────────────────────

def camera(mid_z):
    bpy.ops.object.camera_add(location=(340, -300, 140))
    cam = bpy.context.active_object
    cam.data.lens = 75

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, mid_z))
    tgt = bpy.context.active_object

    con = cam.constraints.new('TRACK_TO')
    con.target     = tgt
    con.track_axis = 'TRACK_NEGATIVE_Z'
    con.up_axis    = 'UP_Y'

    bpy.context.scene.camera = cam


# ── World + render ────────────────────────────────────────────────────────────

def setup():
    s = bpy.context.scene
    s.render.engine         = 'CYCLES'
    s.cycles.samples        = 256
    s.cycles.use_denoising  = True
    s.render.resolution_x   = 1920
    s.render.resolution_y   = 1080
    s.render.filepath       = OUTPUT_PATH
    s.render.image_settings.file_format = 'PNG'

    w = s.world or bpy.data.worlds.new("W")
    s.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value    = (0.90, 0.90, 0.92, 1.0)
        bg.inputs["Strength"].default_value = 0.5


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    clear()
    setup()
    mid_z = build()
    lighting()
    camera(mid_z)
    print(f"[Enclosure] Rendering → {OUTPUT_PATH}")
    bpy.ops.render.render(write_still=True)
    print("[Enclosure] Done.")


main()
