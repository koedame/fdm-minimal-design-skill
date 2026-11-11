"""010 Letter rack: three upright dividers, 48, 72 and 96 high, doweled into a low base.

The dividers are printed flat on their sides, so their faces are smooth and their layers run along
their length (strong in bending), and joined to the base with two 3 mm steel dowels each, glued. The rack
rises toward the back so every compartment shows what is in it.
"""
import os
import sys

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, CH, CH_BED, OFF, DARK, box, cyl, rrect, rx, feet, teardrop_x,  # noqa: E402
                         copies)

BL, BD, BH, BR = 160.0, 96.0, 8.0, 12.0  # base 5:3; R = 12.5 % of 96
DT = 6.0                                 # divider thickness: a Ø3.2 hole leaves 1.4 each side
DL = BL - 16.0                           # divider length: 8 in from each end
HEIGHTS = [48.0, 72.0, 96.0]             # front to back, steps of 24; the tallest = the base depth
YS = [-30.0, 0.0, 30.0]                  # pitch 30: 24 compartments
DOWEL_X = [-48.0, 48.0]
PIN_R, PIN_L = 1.6, 16.0                 # Ø3 x 16 steel dowel; hole +0.2 and glue, as the split joint rule
B_DEPTH, D_DEPTH = 6.5, 10.0             # hole depths in the base and the divider (16.5 for a 16 pin)


def divider(y, h):
    d = box(-DL / 2, DL / 2, y - DT / 2, y + DT / 2, BH, BH + h)
    d = d.edges("|Z").fillet(DT / 2 - 0.01)                 # full round ends
    d = d.faces(">Z").edges().fillet(DT / 2 - 0.1)         # and a full round top
    d = d.faces("<Z").edges().chamfer(CH)                   # the joint: half of a V line
    for x in DOWEL_X:                                       # horizontal in the print: 45-deg roof up (+Y)
        hole = teardrop_x(0, D_DEPTH + 0.01, 0, 0, PIN_R, apex=(1, 0)).rotate((0, 0, 0), (0, 1, 0), -90)
        d = d.cut(hole.translate((x, y, BH - 0.01)))
    return d


def letter_rack():
    base = rrect(BL, BD, BR, 0, BH).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    for y in YS:
        for x in DOWEL_X:
            base = base.cut(cyl(PIN_R, BH - B_DEPTH, B_DEPTH + 1, x, y))
    base = feet(base, [(sx * 64, sy * 36) for sx in (-1, 1) for sy in (-1, 1)])

    parts = {"base": Part(base, base, OFF)}
    for i, (y, h) in enumerate(zip(YS, HEIGHTS)):
        d = divider(y, h)
        parts[f"divider_{int(h)}"] = Part(d, rx(d, 90), OFF)  # on its side: the -Y face on the bed
    pins = copies(cyl(1.5, BH - B_DEPTH + 0.25, PIN_L, x, y) for y in YS for x in DOWEL_X)
    parts["dowels_steel_ref"] = Part(pins, None, DARK, qty=len(YS) * len(DOWEL_X), ref=True)
    return parts


SAMPLES["010_letter_rack"] = letter_rack
