"""050 Flat pencil case: a 200 x 64 x 24 case whose lid swings up on a pin hinge along the back.

The 07_hinged_case built long and flat for pencils and pens up to 190 long: a base 16 high and a lid 8 high (2 : 1), seven
knuckles on a 1.75 filament pin along the back seam, two magnets at the front, and a finger scoop across the front seam. A lip
round the front half of the lid locates it on the base; the lid's wall is thickened inside down to the rim there, so the lip
is part of the wall.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, cyl, rrect, rx, feet, plane_yz, plane_xz)

W, D, R = 200.0, 64.0, 12.0             # inside 194.96 long: a 190 pencil
HB, HL = 16.0, 8.0                      # 2 : 1, 24 overall
FLOOR, TOP = 2.4, 2.4
KR, KL, KG, NK = 4.0, 24.0, 0.4, 7      # knuckles: radius, length, gap, count
PIN = 1.9                               # hole for a 1.75 filament pin
MAG_X, POST = 64.0, 8.0                 # magnet posts at the front
LIP = 3.0


def pencil_case_flat():
    yb = D / 2
    x0 = -(NK * KL + (NK - 1) * KG) / 2
    segs = [(x0 + i * (KL + KG), x0 + i * (KL + KG) + KL) for i in range(NK)]
    base_k, lid_k = segs[0::2], segs[1::2]

    base = rrect(W, D, R, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    base = base.cut(rrect(W - 2 * T, D - 2 * T, R - T, FLOOR, HB))
    lid = rrect(W, D, R, HB, HL).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    lid = lid.cut(rrect(W - 2 * T, D - 2 * T, R - T, HB - 1, HL - TOP + 1))

    fy = -D / 2 + T + POST / 2
    for sx in (-1, 1):
        x = sx * MAG_X
        base = base.union(box(x - POST / 2, x + POST / 2, fy - POST / 2, fy + POST / 2, FLOOR - .1, HB))
        base = base.cut(cyl(3.1, HB - 3.2, 3.3, x, fy))
        lid = lid.union(box(x - POST / 2, x + POST / 2, fy - POST / 2, fy + POST / 2, HB + 0.0, HB + HL - TOP + .1))
        lid = lid.cut(cyl(3.1, HB - 0.1, 3.3, x, fy))

    # lip on the front half: the lid's wall thickened inside to T + GAP + DIV down to the rim, continuing LIP below it
    c = GAP
    ring = lambda off, z0, h: rrect(W - 2 * off, D - 2 * off, R - off, z0, h)   # noqa: E731
    lip = ring(T + c, HB - LIP, LIP + 0.01).union(ring(T - 0.5, HB, HL - TOP + 0.01)) \
        .cut(ring(T + c + DIV, HB - LIP - 1, LIP + HL + 1)).cut(box(-W, W, 0, D, 0, 100))
    for sx in (-1, 1):
        x = sx * MAG_X
        lip = lip.cut(box(x - POST / 2 - c, x + POST / 2 + c, fy - POST / 2 - c, fy + POST / 2 + c, 0, HB))
    lid = lid.union(lip)

    def knuckle(xa, xb, sign):                               # circle + 45-deg web to the wall, as 07_hinged_case
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
    base = feet(base, [(sx * 80.0, sy * 20.0) for sx in (-1, 1) for sy in (-1, 1)])
    return {
        "base": Part(base, base, OFF),
        "lid": Part(lid, rx(lid, 180), DARK),
    }


SAMPLES["050_pencil_case_flat"] = pencil_case_flat
