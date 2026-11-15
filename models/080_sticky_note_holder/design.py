"""080 Sticky note holder: an 88 square block, 22 high, with a pocket for a 75 or 76 square pad of sticky notes.

The pad stands in a pocket half the block's height and sticks to its floor by the adhesive on the back of its own last sheet.
A half-round notch in the front wall, as deep as the pocket, leaves the last notes reachable. No mechanism: one printed part.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, CH, CH_BED, OFF, rrect, feet, plane_xz  # noqa: E402

W, H, R = 88.0, 22.0, 8.0               # 22 modules square; height 1 : 4 of the side; R8 = 9 % of the side
POCKET, RP, DEPTH = 78.0, 3.0, 11.0     # 76 pad + 1 per side; R3 clears the pad's square corners; half the height
PAD = (76.0, 10.0)                      # a 76 square pad, about 100 sheets


def sticky_note_holder():
    b = rrect(W, W, R, 0, H).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    b = b.cut(rrect(POCKET, POCKET, RP, H - DEPTH, DEPTH + 1))          # square floor edge: the pad lies flat to its edges
    yf, yi = -W / 2, -POCKET / 2                                          # the front wall's two faces
    b = b.cut(plane_xz(yi + 0.01).center(0, H).circle(DEPTH).extrude(yi - yf + 1))   # notch, front wall only (plane_xz extrudes to -Y)
    for (y0, r0, r1) in ((yf - 0.01, DEPTH + CH + 0.01, DEPTH), (yi - CH, DEPTH, DEPTH + CH + 0.01)):   # its rims: C0.5
        b = b.cut(cq.Workplane("XY").add(cq.Solid.makeCone(r0, r1, CH + 0.01, pnt=cq.Vector(0, y0, H), dir=cq.Vector(0, 1, 0))))
    b = feet(b, [(sx * 32.0, sy * 32.0) for sx in (-1, 1) for sy in (-1, 1)])
    pad = rrect(PAD[0], PAD[0], 0.01, H - DEPTH, PAD[1])
    return {
        "holder": Part(b, b, OFF),
        "pad_ref": Part(pad, None, (0.95, 0.90, 0.55), ref=True),
    }


SAMPLES["080_sticky_note_holder"] = sticky_note_holder
