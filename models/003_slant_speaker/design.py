"""003 Slant speaker: a passive speaker whose front leans back at 1:4, printed top face down.

The body is one shell with an open bottom. The bottom plate is held by four M2 screws whose heads
sit under the rubber feet, so no fastener shows anywhere. The grille is a field of slots on the
sloped front, square to the slope.
"""
import math
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         cyl, rrect, rx, rz, plane_yz, teardrop_x)

W, H = 80.0, 128.0                 # 8:5
D_BOT, D_TOP = 96.0, 64.0          # front leans back 32 over 128 = 1:4
R = 10.0                           # 12.5 % of the width
N, PITCH, SLOT_W, SLOT_L = 13, 4.0, 1.6, 48.0
SPAN = (N - 1) * PITCH + SLOT_W    # 49.6
MARGIN = (W - SPAN) / 2            # 15.2: side margin, repeated above the field along the slope
DRIVER_D, FRAME_T, MAG_D, MAG_T = 53.0, 4.0, 30.0, 12.0   # a common 2-inch full-range driver
BOSS_XY = [(sx * 28.0, y) for sx in (-1, 1) for y in (-8.0, 40.0)]


def front_plane(offset=0.0):
    """Plane on the sloped front: x across, local y up the slope, normal outward; origin at the top edge."""
    a = math.atan2(D_BOT - D_TOP, H)                     # 14.04 deg from vertical
    n = cq.Vector(0, -math.cos(a), math.sin(a))
    o = cq.Vector(0, -D_BOT / 2 + (D_BOT - D_TOP), H) + n * offset
    return cq.Workplane(cq.Plane(origin=o, xDir=(1, 0, 0), normal=n))


def slant_speaker():
    y0, y1 = -D_BOT / 2, D_BOT / 2
    prof = [(y0, 0), (y1, 0), (y1, H), (y1 - D_TOP, H)]
    body = plane_yz(-W / 2).polyline(prof).close().extrude(W)
    body = body.edges("not(|X or |Y)").fillet(R)         # the plan corners, back and front
    body = body.faces("<Z").shell(-T)                    # shell first: CadQuery does not shell the chamfered solid
    body = body.faces(">Z").edges().chamfer(CH_BED)
    body = body.faces("<Z").edges().chamfer(CH)

    fc = -(MARGIN + SLOT_L / 2)                          # field centre, along the slope from the top edge
    for i in range(N):
        x = (i - (N - 1) / 2) * PITCH
        body = body.cut(front_plane(1.0).center(x, fc).slot2D(SLOT_L, SLOT_W, 90).extrude(-(T + 2.0)))
    # cable: teardrop through the back, apex down in use = up in the upside-down print
    body = body.cut(rz(teardrop_x(y1 - T - 1, T + 2, 0, 16.0, 3.0, apex=(0, -1)), 90))

    for (x, y) in BOSS_XY:                               # vertical bosses from the top wall down to the plate
        body = body.union(cyl(3.0, T, H - 2 * T + 0.1, x, y)).cut(cyl(0.9, T - 0.01, 12.0, x, y))

    lean = T * (D_BOT - D_TOP) / H                       # the front wall moves back 0.63 over the plate thickness
    plate = rrect(W - 2 * (T + GAP), D_BOT - 2 * (T + GAP) - lean, R - T - GAP, 0, T, 0, lean / 2)
    plate = plate.faces("<Z").chamfer(CH)
    for (x, y) in BOSS_XY:
        plate = plate.cut(cyl(5.1, -0.01, 1.01, x, y))   # rubber foot, which also covers the screw head
        plate = plate.cut(cyl(2.2, -0.01, 2.6, x, y)).cut(cyl(1.2, -1, T + 2, x, y))

    driver = front_plane(-T).center(0, fc).circle(DRIVER_D / 2).extrude(-FRAME_T)
    driver = driver.union(front_plane(-T - FRAME_T).center(0, fc).circle(MAG_D / 2).extrude(-MAG_T))
    return {
        "body": Part(body, rx(body, 180), OFF),
        "bottom_plate": Part(plate, plate, OFF),
        "driver_ref": Part(driver, rx(driver, 0), DARK),
    }


SAMPLES["003_slant_speaker"] = slant_speaker
