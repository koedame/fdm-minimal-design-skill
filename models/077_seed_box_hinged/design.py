"""077 Seed sorting box: twelve cells for loose seeds under a lid that swings up on a pin hinge and closes on magnets.

The 07_hinged_case arrangement, with one change for seeds: the lid is a solid 8 plate, so its underside lies 0.25 over
the tops of the dividers and closes every cell; small seeds cannot wander from cell to cell when the box is carried.
Twelve cells (4 x 3) with R3 corners and coved floors, so seeds slide out to a fingertip. Seven knuckles on a 1.75
filament pin along the back seam; two magnets in posts where the dividers meet the front wall; a lip round the front
half of the lid, the dividers notched round it; a finger scoop across the front seam.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK, ACC,  # noqa: E402
                         box, copies, cyl, rrect, rx, feet, plane_yz, plane_xz)

W, D, R = 128.0, 80.0, 12.0             # 32 x 20 modules (8 : 5); R12 = 15 % of the depth
HB, HL = 24.0, 8.0                      # 3 : 1, 32 overall
FLOOR = 2.4
NX, NY = 4, 3                           # twelve cells
RC = 3.0                                # cell corners and floor coves
KR, KL, KG, NK = 4.0, 12.0, 0.4, 7      # knuckles as 07_hinged_case, seven along the 104 straight back
PIN = 1.9
POST = 8.0
LIP = 3.0
MAG = (6.2, 3.2)


def _cells():
    wi, di = W - 2 * T, D - 2 * T
    cw, cd = (wi - (NX - 1) * DIV) / NX, (di - (NY - 1) * DIV) / NY
    xs = [-wi / 2 + cw / 2 + i * (cw + DIV) for i in range(NX)]
    ys = [-di / 2 + cd / 2 + j * (cd + DIV) for j in range(NY)]
    return cw, cd, xs, ys


def seed_box_hinged():
    yb = D / 2
    x0 = -(NK * KL + (NK - 1) * KG) / 2
    segs = [(x0 + i * (KL + KG), x0 + i * (KL + KG) + KL) for i in range(NK)]
    base_k, lid_k = segs[0::2], segs[1::2]
    cw, cd, xs, ys = _cells()
    ring = lambda off, z0, h: rrect(W - 2 * off, D - 2 * off, R - off, z0, h)   # noqa: E731

    base = rrect(W, D, R, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    for x in xs:
        for y in ys:
            # clipped to the cavity first: a corner cell takes the wall's own R - T corner, not R3 (R3 would cut through R12)
            cell = rrect(cw, cd, RC, FLOOR, HB, x, y).intersect(ring(T, FLOOR, HB))
            base = base.cut(cell.faces("<Z").edges().fillet(RC - 0.01))
    # the dividers stop 0.25 under the lid; near the walls of the front half they are notched round the lid's lip
    base = base.cut(ring(T, HB - GAP, 1))
    notch = ring(T, HB - LIP - GAP, LIP + 1).cut(ring(T + GAP + DIV + GAP, 0, 100)).cut(box(-W, W, 0, D, 0, 100))
    base = base.cut(notch)
    xm = [(xs[i] + xs[i + 1]) / 2 for i in range(NX - 1)]       # divider centres
    px = (xm[0], xm[-1])
    fy = -D / 2 + T + POST / 2 - 0.5
    for x in px:                                                # magnet posts where the dividers meet the front wall
        base = base.union(box(x - POST / 2, x + POST / 2, fy - POST / 2, fy + POST / 2, FLOOR, HB))

    lid = rrect(W, D, R, HB, HL).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    lip = ring(T + GAP, HB - LIP, LIP + 0.01).cut(ring(T + GAP + DIV, 0, 100)).cut(box(-W, W, 0, D, 0, 100))
    for x in px:
        lip = lip.cut(box(x - POST / 2 - GAP, x + POST / 2 + GAP, fy - POST / 2 - GAP, fy + POST / 2 + GAP, 0, HB))
    lid = lid.union(lip)

    def knuckle(xa, xb, sign):
        k = 2.828427
        web = [(yb - 0.6, HB), (yb + k, HB + sign * k), (yb, HB + sign * 2 * k), (yb - 0.6, HB + sign * 2 * k)]
        s = plane_yz(xa).center(yb, HB).circle(KR).extrude(xb - xa)
        return s.union(plane_yz(xa).polyline(web).close().extrude(xb - xa))

    for (xa, xb) in base_k:
        base = base.union(knuckle(xa, xb, -1))
    for (xa, xb) in lid_k:
        lid = lid.union(knuckle(xa, xb, +1))
    for (xa, xb) in lid_k:
        base = base.cut(plane_yz(xa - .2).center(yb, HB).circle(KR + 0.4).extrude(xb - xa + .4))
    for (xa, xb) in base_k:
        lid = lid.cut(plane_yz(xa - .2).center(yb, HB).circle(KR + 0.4).extrude(xb - xa + .4))
    pin = plane_yz(-W).center(yb, HB).circle(PIN / 2).extrude(2 * W)
    base, lid = base.cut(pin), lid.cut(pin)

    scoop = plane_xz(-D / 2 + 1.2).center(0, HB).circle(0.75 * HL).extrude(3)
    base, lid = base.cut(scoop), lid.cut(scoop)
    for x in px:                                                # pockets last, after every union on both parts
        base = base.cut(cyl(MAG[0] / 2, HB - MAG[1], MAG[1] + 1, x, fy))
        lid = lid.cut(cyl(MAG[0] / 2, HB - 0.1, MAG[1] + 0.1, x, fy))
    base = feet(base, [(sx * 48.0, sy * 24.0) for sx in (-1, 1) for sy in (-1, 1)])
    mags = [cyl(3.0, HB - 3.15, 3.0, x, fy) for x in px] + [cyl(3.0, HB + 0.15, 3.0, x, fy) for x in px]
    return {
        "base": Part(base, base, OFF),
        "lid": Part(lid, rx(lid, 180), DARK),
        "magnets_ref": Part(copies(mags), None, ACC, qty=4, ref=True),
    }


SAMPLES["077_seed_box_hinged"] = seed_box_hinged
