"""014 Glasses case: a 168 x 64 stadium, body 36 + lid 12, on a pin hinge along the back.

The hinge is the one of 07_hinged_case: the axis on the line where the back face meets the parting
line, five knuckles with 45-deg webs, a 1.75 mm filament pin. Two magnets in posts at the round ends
hold it shut; at the ends the posts leave the full inside width free for the lenses.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, cyl, rx, feet, plane_yz, plane_xz)

L, W = 168.0, 64.0                # stadium: the ends are full rounds (R32), 21 : 8
HB, HL = 36.0, 12.0               # body : lid = 3 : 1, total 48
FLOOR = TOP = 2.4
YB = W / 2                        # hinge axis: back face at the parting line
KR, KL, KG, NK = 4.0, 12.0, 0.4, 5
PIN = 1.9                         # 1.75 filament
POST = 8.0
MAG_X = L / 2 - T - POST / 2      # magnet posts at the round ends, on the centre line
SCOOP_R = 0.75 * HL               # finger scoop: stays below the top edge of the lid


def stadium(l, w, z0, h):
    return cq.Workplane("XY").workplane(offset=z0).slot2D(l, w, 0).extrude(h)


def glasses_case():
    x0 = -(NK * KL + (NK - 1) * KG) / 2
    segs = [(x0 + i * (KL + KG), x0 + i * (KL + KG) + KL) for i in range(NK)]
    base_k, lid_k = segs[0::2], segs[1::2]

    base = stadium(L, W, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    base = base.cut(stadium(L - 2 * T, W - 2 * T, FLOOR, HB))
    lid = stadium(L, W, HB, HL).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    lid = lid.cut(stadium(L - 2 * T, W - 2 * T, HB - 1, HL - TOP + 1))

    for sx in (-1, 1):
        x = sx * MAG_X
        xo = sx * (L / 2 - T + 1.0)               # into the wall
        base = base.union(box(min(x - sx * POST / 2, xo), max(x - sx * POST / 2, xo), -POST / 2, POST / 2, FLOOR - .1, HB))
        base = base.cut(cyl(3.1, HB - 3.2, 3.3, x, 0))
        lid = lid.union(box(min(x - sx * POST / 2, xo), max(x - sx * POST / 2, xo), -POST / 2, POST / 2, HB, HB + HL - TOP + .1))

    c = GAP                                       # lid lip along the front half only: the back must swing
    lip = stadium(L - 2 * (T + c), W - 2 * (T + c), HB - 3, 3.01) \
        .union(stadium(L - 2 * T + 1, W - 2 * T + 1, HB, HL - TOP + 0.01)) \
        .cut(stadium(L - 2 * (T + c + DIV), W - 2 * (T + c + DIV), HB - 4, HL + 5)).cut(box(-L, L, 0, W, 0, 100))
    for sx in (-1, 1):                            # the wall is thickened inside down to the rim, so the lip is part of it
        lip = lip.cut(box(sx * MAG_X - POST / 2 - c - 4, sx * MAG_X + POST / 2 + 4, -POST / 2 - c, POST / 2 + c, 0, HB))
    lid = lid.union(lip)
    for sx in (-1, 1):                            # after the lip: its thickened wall would otherwise refill part of each pocket
        lid = lid.cut(cyl(3.1, HB - 0.1, 3.3, sx * MAG_X, 0))

    def knuckle(xa, xb, sign):
        k = 2.828427
        web = [(YB - 0.6, HB), (YB + k, HB + sign * k), (YB, HB + sign * 2 * k), (YB - 0.6, HB + sign * 2 * k)]
        s = plane_yz(xa).center(YB, HB).circle(KR).extrude(xb - xa)
        return s.union(plane_yz(xa).polyline(web).close().extrude(xb - xa))

    for (xa, xb) in base_k:
        base = base.union(knuckle(xa, xb, -1))
    for (xa, xb) in lid_k:
        lid = lid.union(knuckle(xa, xb, +1))
    for (xa, xb) in lid_k:
        base = base.cut(plane_yz(xa - .2).center(YB, HB).circle(KR + 0.4).extrude(xb - xa + .4))
    for (xa, xb) in base_k:
        lid = lid.cut(plane_yz(xa - .2).center(YB, HB).circle(KR + 0.4).extrude(xb - xa + .4))
    pin = plane_yz(-L).center(YB, HB).circle(PIN / 2).extrude(2 * L)
    base, lid = base.cut(pin), lid.cut(pin)

    scoop = plane_xz(-W / 2 + 1.2).center(0, HB).circle(SCOOP_R).extrude(3)
    base, lid = base.cut(scoop), lid.cut(scoop)
    base = feet(base, [(sx * 52, sy * 16) for sx in (-1, 1) for sy in (-1, 1)])
    mags = [cyl(3.0, HB - 3.15, 3.0, sx * MAG_X, 0) for sx in (-1, 1)] + \
           [cyl(3.0, HB + 0.15, 3.0, sx * MAG_X, 0) for sx in (-1, 1)]
    return {
        "base": Part(base, base, OFF),
        "lid": Part(lid, rx(lid, 180), DARK),
        "magnets_ref": Part(cq.Workplane("XY").add(cq.Compound.makeCompound([m.val() for m in mags])), None, (0.5, 0.5, 0.52),
                            qty=4, ref=True),
    }


SAMPLES["014_glasses_case"] = glasses_case
