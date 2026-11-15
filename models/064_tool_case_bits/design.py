"""064 Bit case: twelve 1/4-inch hex driver bits standing in a case whose lid swings up on a pin hinge.

Two printed parts, the 07_hinged_case arrangement: a base 24 high and a lid 8 high (3 : 1). The base's lower half is a solid
rack with twelve hex pockets in two rows of six on a 12 pitch; each 25 bit stands 10 deep and its top stays 2.6 under the lid.
Five knuckles on a 1.75 filament pin along the back seam, two magnets in posts in the front corners, a lip round the front
half of the lid, and a finger scoop across the front seam.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, cyl, rrect, rx, feet, plane_yz, plane_xz)

W, D, R = 88.0, 48.0, 12.0              # 22 x 12 modules; the bits plus 7.8 to the wall at the ends
HB, HL = 24.0, 8.0                      # 3 : 1, 32 overall
TOP = 2.4
RACK = 12.0                             # rack top = half the base
POCKET = 10.0                           # a 25 bit stands 10 deep; floor 2 under the pockets
HEX = 6.35 + 2 * GAP                    # across flats: 1/4-inch bit + 0.25 per side
PITCH = 12.0                            # 3 modules
BIT_L = 25.0
KR, KL, KG, NK = 4.0, 12.0, 0.4, 5      # knuckles as 07_hinged_case
PIN = 1.9                               # hole for a 1.75 filament pin
POST = 8.0
MAG_X, MAG_Y = W / 2 - R + 3.5, -(D / 2 - R + 3.5)   # on the front corners' diagonals, inside the R12
LIP = 3.0
XS = [PITCH * (i - 2.5) for i in range(6)]
YS = [-PITCH / 2, PITCH / 2]


def hexagon(af, z, h):
    return cq.Workplane("XY").workplane(offset=z).polygon(6, af / 0.8660254).extrude(h)


def bits():
    """The twelve bits as hex prisms standing in their pockets (bought parts)."""
    return [hexagon(6.35, RACK - POCKET + 0.05, BIT_L).translate((x, y, 0)) for x in XS for y in YS]


def tool_case_bits():
    yb = D / 2
    x0 = -(NK * KL + (NK - 1) * KG) / 2
    segs = [(x0 + i * (KL + KG), x0 + i * (KL + KG) + KL) for i in range(NK)]
    base_k, lid_k = segs[0::2], segs[1::2]

    base = rrect(W, D, R, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    base = base.cut(rrect(W - 2 * T, D - 2 * T, R - T, RACK, HB))
    for x in XS:
        for y in YS:
            p = hexagon(HEX, RACK - POCKET, POCKET + 1).translate((x, y, 0))
            lead = cq.Solid.makeLoft([
                cq.Workplane("XY").workplane(offset=RACK - CH).polygon(6, HEX / 0.8660254).wires().val(),
                cq.Workplane("XY").workplane(offset=RACK + 0.01).polygon(6, (HEX + 2 * CH + 0.02) / 0.8660254).wires().val()],
                True)
            base = base.cut(p).cut(cq.Workplane("XY").add(lead).translate((x, y, 0)))
    lid = rrect(W, D, R, HB, HL).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    lid = lid.cut(rrect(W - 2 * T, D - 2 * T, R - T, HB - 1, HL - TOP + 1))

    fy = MAG_Y
    for sx in (-1, 1):
        x = sx * MAG_X
        base = base.union(box(x - POST / 2, x + POST / 2, fy - POST / 2, fy + POST / 2, RACK - .1, HB))
        base = base.cut(cyl(3.1, HB - 3.2, 3.3, x, fy))
        lid = lid.union(box(x - POST / 2, x + POST / 2, fy - POST / 2, fy + POST / 2, HB + 0.0, HB + HL - TOP + .1))

    # lip on the front half: the lid's wall thickened inside to T + GAP + DIV down to the rim, continuing LIP below it
    c = GAP
    ring = lambda off, z0, h: rrect(W - 2 * off, D - 2 * off, R - off, z0, h)   # noqa: E731
    lip = ring(T + c, HB - LIP, LIP + 0.01).union(ring(T - 0.5, HB, HL - TOP + 0.01)) \
        .cut(ring(T + c + DIV, HB - LIP - 1, LIP + HL + 1)).cut(box(-W, W, 0, D, 0, 100))
    for sx in (-1, 1):
        x = sx * MAG_X
        lip = lip.cut(box(x - POST / 2 - c, x + POST / 2 + c, fy - POST / 2 - c, fy + POST / 2 + c, 0, HB))
    lid = lid.union(lip)
    for sx in (-1, 1):                                       # after the lip: its thickened wall would fill part of the pocket
        lid = lid.cut(cyl(3.1, HB - 0.1, 3.3, sx * MAG_X, fy))

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
    base = feet(base, [(sx * 32.0, sy * 16.0) for sx in (-1, 1) for sy in (-1, 1)])
    mags = [cyl(3.0, HB - 3.15, 3.0, sx * MAG_X, fy) for sx in (-1, 1)] + \
           [cyl(3.0, HB + 0.15, 3.0, sx * MAG_X, fy) for sx in (-1, 1)]
    return {
        "base": Part(base, base, OFF),
        "lid": Part(lid, rx(lid, 180), DARK),
        "bits_ref": Part(cq.Workplane("XY").add(cq.Compound.makeCompound([b.val() for b in bits()])), None, (0.6, 0.6, 0.62),
                         qty=12, ref=True),
        "magnets_ref": Part(cq.Workplane("XY").add(cq.Compound.makeCompound([m.val() for m in mags])), None, (0.5, 0.5, 0.52),
                            qty=4, ref=True),
    }


SAMPLES["064_tool_case_bits"] = tool_case_bits
