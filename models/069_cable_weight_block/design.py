"""069 Cable weight block: a block for the desk that holds cable ends where the hand finds them, weighted with coins.

Two parts. The body has two wells for stacks of coins up to 26.5 across; a lip on its top locates the cap, a solid
slab that lifts straight off to fill the wells. Three seats run across the cap's top: a cable pushed down through
the 3.2 neck snaps into the 4.4 seat below it (cables of about 3.6-4.4) and stays there when the device end is
unplugged, instead of sliding off the desk with the weight of the hanging part. With 24 coins of about 7 g the
block weighs about 210 g: enough to hold cables that hang over the edge, not to hold against pulling a plug out.
"""
import os
import sys

import cadquery as cq
from cadquery.selectors import BoxSelector

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, rrect, cyl, rx, feet, chamfer_rim,  # noqa: E402
                         plane_xz)

W, D, R = 96.0, 48.0, 12.0        # 24 x 12 modules; R12 = 12.5 % of the width
HB, HC = 24.0, 12.0               # body : cap = 2 : 1, 36 overall
FLOOR = 2.4
LIP = 3.0
LIP_IN = T + GAP + DIV            # inside face of the lip from the outline (4.45)
COIN_D = 26.5                     # the largest coin the wells take (check yours)
WELL_D = COIN_D + 0.5             # 0.25 round the stack
WX = W / 4                        # wells centred in the two 48 x 48 halves: 10.5 to the outline on every side
CABLE_D = 4.4                     # seat; takes cables of about 3.6-4.4
NECK = 3.2                        # the cable squeezes through this and snaps into the seat
SEAT_Z = HB + HC - 3.4            # seat centre, 3.4 under the top: the neck is 1.2 long
CX = [-16.0, 0.0, 16.0]           # seats at pitch 16 (4 modules)


def ring(off, z0, h):
    return rrect(W - 2 * off, D - 2 * off, R - off, z0, h)


def seat(x):
    """Cable seat along Y: round, with a 45-deg roof pointing down (up in the print) and a neck to the top."""
    r, k = CABLE_D / 2, 0.70710678
    p = plane_xz(D / 2 + 1)
    s = p.center(x, SEAT_Z).circle(r).extrude(D + 2)
    s = s.union(p.polyline([(x - r * k, SEAT_Z - r * k), (x, SEAT_Z - r * 2 ** 0.5), (x + r * k, SEAT_Z - r * k),
                            (x, SEAT_Z)]).close().extrude(D + 2))
    n = NECK / 2
    return s.union(p.polyline([(x - n, SEAT_Z), (x + n, SEAT_Z), (x + n, HB + HC + 1), (x - n, HB + HC + 1)])
                   .close().extrude(D + 2))


def cable_weight_block():
    body = ring(0, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    body = body.union(ring(T + GAP, HB - 0.01, LIP + 0.01).cut(ring(LIP_IN, HB - 1, LIP + 2)))
    body = body.faces(">Z").edges().chamfer(CH)
    for s in (-1, 1):
        body = body.cut(cyl(WELL_D / 2, FLOOR, HB, s * WX, 0))
        body = chamfer_rim(body.translate((-s * WX, 0, 0)), WELL_D / 2, HB).translate((s * WX, 0, 0))
    body = feet(body, [(sx * 40, sy * 16) for sx in (-1, 1) for sy in (-1, 1)])   # clear of the wells

    cap = ring(0, HB, HC).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    cap = cap.cut(ring(T, HB - 1, LIP + GAP + 1))
    for x in CX:
        cap = cap.cut(seat(x))
    cap = cap.edges(BoxSelector((-W, -D, HB + HC - 0.05), (W, D, HB + HC + 0.05))).edges("|Y").chamfer(CH)

    coins = cyl(COIN_D / 2, FLOOR + 0.05, HB - FLOOR - 0.1, -WX, 0).union(cyl(COIN_D / 2, FLOOR + 0.05, HB - FLOOR - 0.1, WX, 0))
    cables = cq.Workplane("XY")
    for x in CX:
        cables = cables.union(plane_xz(D / 2).center(x, SEAT_Z).circle(CABLE_D / 2 - 0.2).extrude(D))
    return {
        "body": Part(body, body, OFF),
        "cap": Part(cap, rx(cap, 180), OFF),
        "coins_ref": Part(coins, None, (0.75, 0.6, 0.35), qty=2, ref=True),
        "cables_ref": Part(cables, None, (0.2, 0.2, 0.22), qty=3, ref=True),
    }


SAMPLES["069_cable_weight_block"] = cable_weight_block
