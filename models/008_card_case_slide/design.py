"""008 Card case with a sliding lid: the lid runs in a 45-deg dovetail on three sides of the top.

The case is 102 x 68 (3:2) and 24 high. The lid slides out through the right end, where the end wall
stops under it and a low ridge on that wall clicks into a groove under the lid, so the lid stays shut.
The top is one flat face: the lid's top sits flush with the walls behind a 0.25 reveal.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, GAP, OFF, box, rrect, plane_yz)  # noqa: E402

L, W, H, R = 102.0, 68.0, 24.0, 8.5     # 3:2; R = 12.5 % of 68
FLOOR = 2.4
LIP = 1.2                               # the wall top steps 1.2 inward: the dovetail's upper half
ZL0, DT = 20.4, 1.2                     # lid bottom, dovetail height (45 deg, 1.2 out)
ZD = ZL0 + DT                           # top of the dovetail; the lid is 3.6 thick
SLOPE_GAP = GAP * 2 ** 0.5              # plan offset that gives 0.25 square to a 45-deg face
XO = L / 2 + 20                         # the lid and its clearance run out past the right end
RIDGE_H = 0.4
RING = 2.4                              # lid seat inside the walls


def outline_wire(w, d, r, z):
    return rrect(w, d, r, z, 1.0).faces("<Z").wires().val()


def lid_plan(off, z0, h):
    """Lid outline grown by off: left end in the case, right end past the case."""
    x0 = -(L / 2 - T - LIP - GAP) - off
    w = W - 2 * (T + LIP + GAP) + 2 * off
    return rrect(XO - x0, w, R - T - LIP - GAP + off, z0, h, (XO + x0) / 2, 0)


def wire(off, z):
    return lid_plan(off, z, 1.0).faces("<Z").wires().val()


def loft(off0, z0, off1, z1):
    return cq.Workplane("XY").add(cq.Solid.makeLoft([wire(off0, z0), wire(off1, z1)], True))


def card_case_slide():
    outline = rrect(L, W, R, -1, H + 2)
    body = rrect(L, W, R, 0, H)
    body = body.cut(rrect(L - 2 * T, W - 2 * T, R - T, FLOOR, ZL0 - FLOOR))
    clear = lid_plan(GAP, ZD + 0.1, H + 1 - ZD).union(loft(DT + SLOPE_GAP + GAP, ZL0 - GAP, GAP, ZD + 0.1))
    body = body.cut(clear)
    # the lid rests on a 2.4 ring with a 45-deg underside: the dovetail only keeps it from lifting
    z1 = ZL0 - GAP
    ring = rrect(L - 2 * T, W - 2 * T, R - T, z1 - RING, RING)
    cone = cq.Solid.makeLoft([outline_wire(L - 2 * T + 0.02, W - 2 * T + 0.02, R - T, z1 - RING - 0.001),
                              outline_wire(L - 2 * T - 2 * RING, W - 2 * T - 2 * RING, R - T - RING, z1 + 0.001)], True)
    body = body.union(ring.cut(cq.Workplane("XY").add(cone)))
    body = body.faces("<Z").edges().chamfer(CH_BED)
    body = body.edges(cq.selectors.BoxSelector((-L, -W, H - 0.01), (L, W, H + 0.01))).chamfer(CH)
    # detent ridge across the right end wall
    xr = L / 2 - T / 2
    ridge = plane_yz(-30).polyline([(-RIDGE_H, ZL0 - GAP - 0.01), (RIDGE_H, ZL0 - GAP - 0.01), (0, ZL0 - GAP + RIDGE_H)])
    ridge = ridge.close().extrude(60).rotate((0, 0, 0), (0, 0, 1), 90)   # now a prism along Y
    ridge = ridge.translate((xr, 0, 0)).intersect(box(xr - 2, xr + 2, -20.0, 20.0, 0, H))
    body = body.union(ridge)

    lid = lid_plan(0, ZD, H - ZD).union(loft(DT, ZL0, 0, ZD)).intersect(outline)
    lid = lid.faces("<Z").edges().chamfer(CH_BED)
    lid = lid.faces(">Z").edges().chamfer(CH)
    groove = plane_yz(-30).polyline([(-0.8, ZL0 - 0.01), (0.8, ZL0 - 0.01), (0, ZL0 + 0.8)]).close()
    groove = groove.extrude(60).rotate((0, 0, 0), (0, 0, 1), 90).translate((xr, 0, 0))
    lid = lid.cut(groove.intersect(box(xr - 2, xr + 2, -21.0, 21.0, 0, H)))
    dent = rrect(8.0, 20.0, 4.0 - 0.001, H - 1.2, 2.0, L / 2 - 10.0, 0)            # thumb dent near the open end
    lid = lid.cut(dent)
    return {
        "body": Part(body, body, OFF),
        "lid": Part(lid, lid, OFF),
    }


SAMPLES["008_card_case_slide"] = card_case_slide
