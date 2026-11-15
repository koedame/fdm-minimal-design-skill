"""019 Headphone stand: a plate column on a slab base, joined by two steel dowels and glue.

The column is a plate 64 wide and 24 thick with a shallow arc on top for the headband. It prints on
its side (its outline on the bed), so it is strong along its length and needs no support; the dowel
holes are then horizontal and are teardrops. The base prints bottom down with round holes. The seam
is a designed shadow line: the column's foot has a C0.5 on all four edges, as 11_split_riser.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, CH, CH_BED, OFF, DARK,  # noqa: E402
                         rrect, cyl, rx, feet, copies, plane_xz)

BW, BD, BH, BR = 128.0, 96.0, 12.0, 16.0   # base slab, 4 : 3, grid 16
CW, CT, H = 64.0, 24.0, 240.0              # column 64 x 24 (half the base width, quarter of its depth); overall 240
SAG = 8.0                                  # arc on top: sagitta 8 over 64 -> R 68
TOP_R = 12.0                               # where the arc meets the sides
BEVEL = 2.0                                # 45-deg bevel round the face outlines: the headband pad rests on a 20 flat, not on an edge
PIN_D, PIN_IN_BASE, PIN_IN_COL = 4.2, 10.0, 11.0
PIN_X = 16.0                               # two dowels at +-16 (a quarter of the column width)
DOWEL_L = 20.0


def teardrop_z(x, y, z0, h, r):
    """Vertical round hole with a 45-deg roof toward +Y (up when the column lies on its back)."""
    k = 0.70710678
    hole = cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(r).extrude(h)
    roof = (cq.Workplane("XY").workplane(offset=z0)
            .polyline([(x - r * k, y + r * k), (x, y + r * 1.41421356), (x + r * k, y + r * k), (x, y)]).close().extrude(h))
    return hole.union(roof)


def headphone_stand():
    base = rrect(BW, BD, BR, 0, BH).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    base = feet(base, [(sx * 48.0, sy * 32.0) for sx in (-1, 1) for sy in (-1, 1)])
    for sx in (-1, 1):
        base = base.cut(cyl(PIN_D / 2, BH - PIN_IN_BASE, PIN_IN_BASE + 0.01, sx * PIN_X))
    hs = H - SAG                               # where the arc meets the sides
    prof = (plane_xz(CT / 2).moveTo(-CW / 2, BH).lineTo(CW / 2, BH).lineTo(CW / 2, hs)
            .threePointArc((0, H), (-CW / 2, hs)).close())
    col = prof.extrude(CT)
    for sx in (-1, 1):
        col = col.edges("|Y").edges(cq.selectors.BoxSelector((sx * CW / 2 - .05, -CT, hs - .05), (sx * CW / 2 + .05, CT, hs + .05))).fillet(TOP_R)
    above_foot = cq.selectors.BoxSelector((-CW, -CT, BH + 1), (CW, CT, H + 1))
    col = col.faces("<Y").edges(above_foot).chamfer(BEVEL).faces(">Y").edges(above_foot).chamfer(BEVEL)
    col = col.faces("<Z").chamfer(CH)                                  # the foot: half of the shadow line
    for sx in (-1, 1):
        col = col.cut(teardrop_z(sx * PIN_X, 0, BH - 0.01, PIN_IN_COL + 0.01, PIN_D / 2))

    pins = copies([cyl(2.0, BH - DOWEL_L / 2, DOWEL_L, sx * PIN_X) for sx in (-1, 1)])
    return {
        "base": Part(base, base, OFF),
        "column": Part(col, rx(col, 90), OFF),          # front (-Y) face on the bed; the teardrop roofs point up
        "dowels_steel_ref": Part(pins, None, DARK, qty=2, ref=True),
    }


SAMPLES["019_headphone_stand"] = headphone_stand
