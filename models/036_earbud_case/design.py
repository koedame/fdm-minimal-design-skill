"""036 Earbud case: a 68 x 48 x 28 rounded block, base 20 + lid 8, the lid lifted straight off.

A lip on the lid drops 3 into the base all round and locates it (07). A divider splits the base into one
cell per earbud; two posts on it carry two pairs of 6 x 3 magnets that hold the lid down, so the cells
are clear out to the walls. A shallow scoop at the front of the seam gives a fingertip something to lift.
"""
import os
import sys

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, cyl, rrect, rx, plane_xz)

L, W, R = 68.0, 48.0, 16.0          # 17 : 12 : 7 with the height; corners R16 (a third of the width)
HB, HL = 20.0, 8.0                  # base : lid = 5 : 2, total 28: 23.2 inside, for a bud up to 31 x 24 x 22
FLOOR = TOP = 2.4
POST = 8.0
MAG_Y = 12.0                        # magnet posts on the divider, a quarter of the width either side
LIP_H = 3.0
SCOOP_R = 0.75 * HL


def bud(sx):
    """Envelope of one earbud lying in a cell: 24 x 31 x 22, vertical edges R8. For checking the fit, not a part."""
    return rrect(24.0, 31.0, 8.0, FLOOR, 22.0, sx * (POST / 2 + 0.75 + 12.0), 0)


def earbud_case():
    ri = R - T
    base = rrect(L, W, R, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    base = base.cut(rrect(L - 2 * T, W - 2 * T, ri, FLOOR, HB))
    lid = rrect(L, W, R, HB, HL).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    lid = lid.cut(rrect(L - 2 * T, W - 2 * T, ri, HB - 1, HL - TOP + 1))

    c = GAP
    lip_room = rrect(L, W, R, HB - LIP_H - c, LIP_H + c + 1) \
        .cut(rrect(L - 2 * (T + DIV + 2 * c), W - 2 * (T + DIV + 2 * c), ri - DIV - 2 * c, 0, HB + 2))
    base = base.union(box(-DIV / 2, DIV / 2, -W / 2 + 1, W / 2 - 1, FLOOR - .1, HB)
                      .intersect(rrect(L - 2 * T + .02, W - 2 * T + .02, ri, 0, HB)).cut(lip_room))
    for sy in (-1, 1):
        y = sy * MAG_Y
        base = base.union(box(-POST / 2, POST / 2, y - POST / 2, y + POST / 2, FLOOR - .1, HB))
        base = base.cut(cyl(3.1, HB - 3.2, 3.3, 0, y))
        lid = lid.union(box(-POST / 2, POST / 2, y - POST / 2, y + POST / 2, HB, HB + HL - TOP + .1))
        lid = lid.cut(cyl(3.1, HB - 0.1, 3.3, 0, y))

    # the lip runs all round; the divider steps down under it
    lid = lid.union(rrect(L - 2 * (T + c), W - 2 * (T + c), ri - c, HB - LIP_H, LIP_H + 0.01)
                    .cut(rrect(L - 2 * (T + c + DIV), W - 2 * (T + c + DIV), ri - c - DIV, HB - LIP_H - 1, LIP_H + 2)))

    scoop = plane_xz(-W / 2 + 1.2).center(0, HB).circle(SCOOP_R).extrude(3)
    base, lid = base.cut(scoop), lid.cut(scoop)
    return {
        "base": Part(base, base, OFF),
        "lid": Part(lid, rx(lid, 180), DARK),
    }


SAMPLES["036_earbud_case"] = earbud_case
