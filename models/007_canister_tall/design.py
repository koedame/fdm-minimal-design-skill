"""007 Tall canister: a Ø72 x 144 screw-top canister for dry goods; the lid is flush with the body.

Height is twice the diameter and the lid is an eighth of it. The threads are the 45-deg flanked ones of
12_threaded_jar, so the body prints upright and the lid top face down without supports.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, OFF, DARK, cyl, rx, feet, thread_solid)  # noqa: E402

RO, HB, HL = 36.0, 128.0, 16.0     # Ø72; body 128 + lid 16 = 144 = 2 x 72
NECK_R = RO - 4.0                  # thread root on the body: 2.4 lid wall + 1.2 thread + 0.4 clearance
PITCH, DEPTH = 4.0, 1.2
LID_WALL = 2.4
R_IN = 6.0                         # inside floor fillet


def canister_tall():
    body = cyl(RO, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    body = body.union(cyl(NECK_R, HB - 0.01, 12.0))
    ri, rn = RO - T, NECK_R - T
    shoulder = cq.Workplane("XY").add(cq.Solid.makeCone(ri, rn, ri - rn, pnt=cq.Vector(0, 0, HB - 4.0)))  # 45 deg
    inner = cyl(ri, 2.4, HB - 6.4).union(shoulder).union(cyl(rn, HB - 4.0 + (ri - rn) - 0.01, 20))
    body = body.cut(inner)
    body = body.faces(cq.selectors.NearestToPointSelector((0, 0, 2.4))).edges().fillet(R_IN)   # nothing lodges in the corner
    body = body.faces(">Z").chamfer(CH)
    body = body.union(thread_solid(NECK_R, HB + 2.0, 2.0, PITCH, DEPTH, 2.8, 0.4, external=True))
    body = feet(body, [(sx * 18, sy * 18) for sx in (-1, 1) for sy in (-1, 1)])

    rl = RO - LID_WALL
    lid = cyl(RO, HB, HL).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    lid = lid.cut(cyl(rl, HB - 1, HL - 2.4 + 1))
    lid = lid.union(thread_solid(rl, HB + 2.0 + PITCH / 2, 2.25, PITCH, DEPTH, 2.4, 0.4, external=False)
                    .intersect(cyl(RO - 0.5, HB + 0.5, HL - 3)))
    ribs = cq.Workplane("XY").workplane(offset=HB + 7).polarArray(RO, 0, 360, 64).rect(1.0, 0.8).extrude(HL - 7.5)
    lid = lid.cut(ribs)                # grip on the upper band; the band at the seam stays smooth
    return {
        "body": Part(body, body, OFF),
        "lid": Part(lid, rx(lid, 180), DARK),
    }


SAMPLES["007_canister_tall"] = canister_tall
