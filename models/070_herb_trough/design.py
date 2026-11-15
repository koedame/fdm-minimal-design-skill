"""070 Herb trough: a long trough for four herbs in 9 cm nursery pots, for a window sill, longer than the bed.

Two halves, each printed bottom down, joined at the centre with four Ø4 steel dowels and glue. 400 x 104 x 96, R12,
on a floating plinth. Each half is closed at the joint by its own 8 thick end wall, so each half is a watertight
vessel for two pots and no water reaches the glued seam; the two end walls together make the 16 divider in the
middle, and the joint is one V line round the outside and across the divider. Two low ribs along each floor keep
the pots out of the water that drains from them.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, OFF, DARK, rrect, box, feet, copies,  # noqa: E402
                         fillet_at, plane_yz, teardrop_x)

L, D, H = 400.0, 104.0, 96.0      # 100 x 26 x 24 modules; each half 200 long fits a 256 bed
R = 12.0                          # 12.5 % of the height
FLOOR = 2.4
R_IN = 3.0
PL, INSET = 2.4, 1.2              # floating plinth
SEAM_T = 8.0                      # each half's end wall at the joint
POT, POT_BASE, POT_H = 90.0, 66.0, 80.0   # 9 cm nursery pot; inside 98.96 wide, 189.5 long per half (two pots)
RIB_H, RIB_Y = 4.8, 24.0          # ribs 48 apart, under the pot's base
PIN_D, PIN_DEPTH = 4.2, 6.0       # Ø4 x 10 dowels: 5 in each half, 1 free for glue; 2 left behind the hole
PINS = [(y, z) for y in (-32.0, 32.0) for z in (24.0, 72.0)]


def pot_x():
    """Pot centres in the left half: the compartment split in two equal lengths."""
    a, b = -L / 2 + T, -SEAM_T
    return [a + (b - a) / 4, a + 3 * (b - a) / 4]


def pots():
    """Envelope of four 9 cm nursery pots standing on the ribs."""
    out = cq.Workplane("XY")
    for x in pot_x() + [-v for v in pot_x()]:
        out = out.union(cq.Workplane("XY").add(cq.Solid.makeCone(POT_BASE / 2, POT / 2, POT_H,
                                                                 pnt=cq.Vector(x, 0, FLOOR + RIB_H + 0.01))))
    return out


def cell(sx, z0, z1, floor_r):
    """One half's inside: R - T at the outer corners (concentric with the outline), R3 at the divider."""
    xo, xs, yi = sx * (L / 2 - T), sx * SEAM_T, D / 2 - T
    c = box(min(xo, xs), max(xo, xs), -yi, yi, z0, z1)
    for y in (-yi, yi):
        c = fillet_at(c, (xo, y), R - T, z1 + 1)
        c = fillet_at(c, (xs, y), R_IN, z1 + 1)
    return c.faces("<Z").edges().fillet(R_IN - 0.05) if floor_r else c


def whole():
    body = rrect(L - 2 * INSET, D - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    body = body.union(rrect(L, D, R, PL, H - PL).faces("<Z").chamfer(INSET))
    top, w = FLOOR + RIB_H, DIV / 2
    for sx in (-1, 1):
        body = body.cut(cell(sx, FLOOR, H + 1, True))
        inner = cell(sx, FLOOR - 0.5, H, False)
        for y in (-RIB_Y, RIB_Y):
            rib = plane_yz(-L / 2).polyline([(y - w, FLOOR - 0.5), (y + w, FLOOR - 0.5), (y + w, top - CH),
                                             (y + w - CH, top), (y - w + CH, top), (y - w, top - CH)]).close().extrude(L)
            body = body.union(rib.intersect(inner))
    return body.faces(">Z").edges().chamfer(CH)                         # rims and the divider's top


def herb_trough():
    left = whole().intersect(box(-L, 0, -D, D, -1, H + 1))
    left = left.faces(">X").edges().chamfer(CH)                          # half of the V line
    for (y, z) in PINS:
        left = left.cut(teardrop_x(-PIN_DEPTH, PIN_DEPTH + 0.01, y, z, PIN_D / 2))
    left = feet(left, [(x, y) for x in (-L / 2 + 20, -20.0) for y in (-32.0, 32.0)])
    right = left.mirror("YZ")
    pins = copies([plane_yz(-5.0).center(y, z).circle(2.0).extrude(10.0) for (y, z) in PINS])
    return {
        "half_left": Part(left, left, OFF),
        "half_right": Part(right, right, OFF),
        "dowels_steel_ref": Part(pins, None, DARK, qty=4, ref=True),
    }


SAMPLES["070_herb_trough"] = herb_trough
