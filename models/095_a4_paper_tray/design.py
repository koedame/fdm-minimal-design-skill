"""095 A4 paper tray: a 236 x 320 x 40 desk tray for A4 sheets, longer than the bed, in two halves joined on Ø4 steel dowels.

Each half is 236 x 160 and prints bottom down. The walls are 8 thick: thick enough to take the dowels (two in each side wall,
1.9 of wall round each hole) and to read as one solid frame round the thin 2.4 floor. A U 160 wide drops the front wall to 16,
so a sheet is taken from the front. The joint across the middle is one V line, C0.5 on both halves, as 11_split_riser; the tray
floats on a 1.2 shadow line, as 03_tray.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, CH, CH_BED, OFF, DARK, rrect, box, feet, copies,  # noqa: E402
                         teardrop_x, plane_xz)

W, D, H = 236.0, 320.0, 40.0              # 59 x 80 x 10 modules; each half 236 x 160 fits a 256 bed
WALL = 8.0                                # Ø4.2 dowel hole + 1.9 each side
R = 20.0                                  # 8.5 % of the width; the inner R12 clears an A4 corner
FLOOR = 2.4
PL, INSET = 2.4, 1.2                      # floating plinth
U_W, LIP, UR = 160.0, 16.0, 8.0           # front U: half the depth wide, down to 16, corners R8 (= the wall)
PIN_D, PIN_DEPTH = 4.2, 6.0               # Ø4 x 10 dowels: 5 in each half, 1 free for glue
PIN_X, PIN_Z = W / 2 - WALL / 2, (H / 4, 3 * H / 4)
A4 = (210.0, 297.0)


def sheet():
    """An A4 sheet (a stack 10 high) lying in the middle of the floor; checked against the tray in the review."""
    return box(-A4[0] / 2, A4[0] / 2, -A4[1] / 2, A4[1] / 2, FLOOR + 0.01, FLOOR + 10)


def whole():
    body = rrect(W - 2 * INSET, D - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    body = body.union(rrect(W, D, R, PL, H - PL).faces("<Z").chamfer(INSET))
    body = body.cut(rrect(W - 2 * WALL, D - 2 * WALL, R - WALL, FLOOR, H))
    body = body.faces(">Z").edges().chamfer(CH)                     # the rim, outside and in
    u = (plane_xz(-D / 2 + WALL + 1).center(0, (LIP + H + 2 * UR) / 2).rect(U_W, H + 2 * UR - LIP).extrude(WALL + 2)
         .edges("|Y").fillet(UR))                                    # its top corners lie above the rim
    body = body.cut(u)
    for y in (-D / 2, -D / 2 + WALL):                                # the U's outline on the outer and inner face
        body = body.edges(cq.selectors.BoxSelector((-U_W / 2 - 0.1, y - 0.05, LIP - 0.1),
                                                   (U_W / 2 + 0.1, y + 0.05, H - CH - 0.05))).chamfer(CH)
    return body


def a4_paper_tray():
    front = whole().intersect(box(-W, W, -D, 0, -1, H + 1))
    front = front.faces(">Y").edges().chamfer(CH)                    # half of the V line
    for sx in (-1, 1):
        for z in PIN_Z:
            hole = teardrop_x(-PIN_DEPTH, PIN_DEPTH + 0.01, -sx * PIN_X, z, PIN_D / 2).rotate((0, 0, 0), (0, 0, 1), 90)
            front = front.cut(hole)
    front = feet(front, [(sx * (W / 2 - 24), y) for sx in (-1, 1) for y in (-D / 2 + 24, -24.0)])
    back = whole().intersect(box(-W, W, 0, D, -1, H + 1))
    back = back.faces("<Y").edges().chamfer(CH)
    for sx in (-1, 1):
        for z in PIN_Z:
            hole = teardrop_x(-0.01, PIN_DEPTH + 0.01, -sx * PIN_X, z, PIN_D / 2).rotate((0, 0, 0), (0, 0, 1), 90)
            back = back.cut(hole)
    back = feet(back, [(sx * (W / 2 - 24), y) for sx in (-1, 1) for y in (24.0, D / 2 - 24)])
    pins = copies([plane_xz(5.0).center(sx * PIN_X, z).circle(2.0).extrude(10.0) for sx in (-1, 1) for z in PIN_Z])
    return {
        "half_front": Part(front, front.translate((0, D / 4, 0)), OFF),
        "half_back": Part(back, back.translate((0, -D / 4, 0)), OFF),
        "dowels_steel_ref": Part(pins, None, DARK, qty=4, ref=True),
    }


SAMPLES["095_a4_paper_tray"] = a4_paper_tray
