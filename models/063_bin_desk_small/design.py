"""063 Small desk bin: a square bin for paper scraps, used bare or with a small bag held by a rubber band.

One part, printed bottom down. 96 x 96 x 128 (3 : 4), R12 in plan, on a floating plinth. A V groove runs round the
outside 12 below the rim: a small bag folded over the rim is held there with a rubber band, which drops into the
groove and does not slide off; without a bag it is the one line on the walls. The floor's inner edge is rounded
R3 so crumbs do not collect in the corners.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, OFF, rrect, feet)  # noqa: E402

S, H = 96.0, 128.0                # 24 x 24 x 32 modules; height = 4/3 of the side
R = 12.0                          # 12.5 % of the side
FLOOR = 2.4
R_IN = 3.0                        # floor edge inside
PL, INSET = 2.4, 1.2              # floating plinth
ZG = H - 12.0                     # groove centre: 12 below the rim (= R)
GV = 0.8                          # groove depth; 45-deg flanks, 1.6 tall, leaving 1.72 (4 lines) of wall


def wire(off, z):
    return rrect(S - 2 * off, S - 2 * off, R - off, z, 1).faces("<Z").wires().val()


def bin_desk_small():
    body = rrect(S - 2 * INSET, S - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    body = body.union(rrect(S, S, R, PL, H - PL).faces("<Z").chamfer(INSET))
    cav = rrect(S - 2 * T, S - 2 * T, R - T, FLOOR, H).faces("<Z").edges().fillet(R_IN)
    body = body.cut(cav)
    body = body.faces(">Z").edges().chamfer(CH)                     # rim, inner and outer
    keep = cq.Solid.makeLoft([wire(-0.01, ZG - GV - 0.01), wire(GV, ZG), wire(-0.01, ZG + GV + 0.01)], True)
    groove = rrect(S + 4, S + 4, R + 2, ZG - GV, 2 * GV).cut(cq.Workplane("XY").add(keep))
    body = body.cut(groove)
    body = feet(body, [(sx * 32, sy * 32) for sx in (-1, 1) for sy in (-1, 1)])
    return {"bin": Part(body, body, OFF)}


SAMPLES["063_bin_desk_small"] = bin_desk_small
