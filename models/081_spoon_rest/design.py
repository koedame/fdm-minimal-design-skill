"""081 Spoon rest: a 144 x 72 tray on a floating plinth for a cooking spoon or ladle laid down between uses.

The bowl of the spoon lies in a well 12 deep that keeps what drips from it; the handle crosses one end wall in a half-round
notch and rests there, 4 above the floor, so it stays off the worktop. No mechanism: one printed part.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, CH, CH_BED, OFF, rrect, feet, plane_yz  # noqa: E402

L, W, H, R = 144.0, 72.0, 16.0, 12.0    # 2 : 1, grid 4; R12 = 8.3 % of the length
PL, INSET = 2.4, 1.2                    # floating plinth
M = 2 * T                               # wall: one margin all round the well, 12 lines (5.04)
FLOOR = 4.0                             # well floor; the well is 12 deep
NOTCH = 8.0                             # handle notch: R8 on the top edge of the +X end wall, its bottom 4 above the floor


def spoon_rest():
    b = rrect(L - 2 * INSET, W - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    b = b.union(rrect(L, W, R, PL, H - PL).faces("<Z").chamfer(INSET))
    b = b.cut(rrect(L - 2 * M, W - 2 * M, R - M, FLOOR, H))           # concentric with the outline
    b = b.faces(">Z").chamfer(CH)                                       # outer and inner rim
    xi, xo = L / 2 - M, L / 2                                           # the end wall's two faces
    b = b.cut(plane_yz(xi - 0.01).center(0, H).circle(NOTCH).extrude(M + 1))
    for (x0, r0, r1) in ((xo + 0.01, NOTCH + CH + 0.01, NOTCH), (xi + CH, NOTCH, NOTCH + CH + 0.01)):   # its rims: C0.5
        b = b.cut(cq.Workplane("XY").add(cq.Solid.makeCone(r0, r1, CH + 0.01, pnt=cq.Vector(x0, 0, H),
                                                           dir=cq.Vector(-1, 0, 0))))
    b = feet(b, [(sx * 56.0, sy * 20.0) for sx in (-1, 1) for sy in (-1, 1)])
    return {"rest": Part(b, b, OFF)}


SAMPLES["081_spoon_rest"] = spoon_rest
