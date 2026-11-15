"""017 Puck speaker: a Ø96 x 48 cylinder, body 32 + a screw-on lid 16 whose top is a dense field of holes.

The threads are the 45-deg flanked ones of 12_threaded_jar, so the body prints upright and the lid top
face down without supports. A 50 mm full-range driver faces up under the holes; it sits on three posts
standing from the floor, and a ring under the lid top holds it down when the lid is screwed home.
"""
import math
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         cyl, rx, rz, feet, thread_solid, teardrop_x)

RO, HB, HL = 48.0, 32.0, 16.0      # Ø96; body 32 + lid 16 = 48 = half the diameter; body : lid = 2 : 1
NECK_R = RO - 4.0                  # thread root: 2.4 lid wall + 1.2 thread + 0.4 clearance
PITCH, DEPTH = 4.0, 1.2
FLOOR = TOP = LID_WALL = 2.4
# driver (match yours): Ø52 frame 3 thick, basket to Ø30 over 10, magnet Ø30 x 10
FR, FT = 26.0, 3.0
Z_FRAME = HB + HL - TOP - 4.0      # frame top 4 under the lid top: room for the ring
HOLE_D, HOLE_P, FIELD_R = 2.4, 4.0, 22.0   # perforation rule; the field covers the cone (about Ø44)
POST_R, POST_D = 24.0, 4.0         # three posts under the frame rim, outside the basket


def puck_speaker():
    body = cyl(RO, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    body = body.union(cyl(NECK_R, HB - 0.01, 12.0))
    ri, rn = RO - T, NECK_R - T
    shoulder = cq.Workplane("XY").add(cq.Solid.makeCone(ri, rn, ri - rn, pnt=cq.Vector(0, 0, HB - 4.0)))   # 45 deg
    body = body.cut(cyl(ri, FLOOR, HB - 4.0 - FLOOR + 0.01).union(shoulder).union(cyl(rn, HB - 0.01, 20)))
    body = body.faces(">Z").chamfer(CH)
    body = body.union(thread_solid(NECK_R, HB + 2.0, 2.0, PITCH, DEPTH, 2.8, 0.4, external=True))
    z_post = Z_FRAME - FT - 0.05
    for i in range(3):
        a = math.radians(90 + 120 * i)
        body = body.union(cyl(POST_D / 2, FLOOR - 0.01, z_post - FLOOR + 0.01, POST_R * math.cos(a), POST_R * math.sin(a)))
    body = body.cut(rz(teardrop_x(-RO - 1, T + 3, 0, 8.0, 2.2), -90))  # cable, at the back (+Y)
    body = feet(body, [(sx * 24, sy * 24) for sx in (-1, 1) for sy in (-1, 1)])

    rl = RO - LID_WALL
    lid = cyl(RO, HB, HL).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    lid = lid.cut(cyl(rl, HB - 1, HL - TOP + 1))
    lid = lid.union(thread_solid(rl, HB + 2.0 + PITCH / 2, 2.25, PITCH, DEPTH, 2.4, 0.4, external=False)
                    .intersect(cyl(RO - 0.5, HB + 0.5, HL - 3)))
    z_top = HB + HL - TOP
    lid = lid.union(cyl(FR, Z_FRAME + GAP, z_top - Z_FRAME - GAP + 0.01).cut(cyl(FR - DIV, Z_FRAME, 10)))
    n = int(FIELD_R // HOLE_P)
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            x, y = i * HOLE_P, j * HOLE_P
            if math.hypot(x, y) <= FIELD_R:
                lid = lid.cut(cyl(HOLE_D / 2, z_top - 1, TOP + 2, x, y))
    ribs = cq.Workplane("XY").workplane(offset=HB + 7).polarArray(RO, 0, 360, 64).rect(1.0, 0.8).extrude(HL - 7.5)
    lid = lid.cut(ribs)                # grip on the upper band; the band at the seam stays smooth

    drv = cyl(FR, Z_FRAME - FT, FT).union(cq.Workplane("XY").add(
        cq.Solid.makeCone(15.0, 22.0, 10.0, pnt=cq.Vector(0, 0, Z_FRAME - FT - 10.0)))).union(cyl(15.0, Z_FRAME - FT - 20.0, 10.01))
    return {
        "body": Part(body, body, OFF),
        "lid": Part(lid, rx(lid, 180), DARK),
        "driver_ref": Part(drv, None, DARK, ref=True),
    }


SAMPLES["017_puck_speaker"] = puck_speaker
