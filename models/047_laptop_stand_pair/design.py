"""047 Laptop stand, set of two: two flat triangular frames, 192 deep and 32 wide, that tilt a laptop 15 deg.

Each stand is one side profile, a right triangle with its slope on top, printed lying flat so every member is laid down
along its length. A laptop rests on the two slopes, one stand under each side, and its front edge sits against a 6 lip square
to the slope at the front. The middle of the triangle is open, so the stand is three 8 wide members and a solid front block.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, CH, CH_BED, OFF,  # noqa: E402
                         box, rx, rz, copies)

DEP, HB, WID = 192.0, 60.0, 32.0         # depth, height at the back, width (the print height): 4 members
YF, ZF = 12.0, 12.0                      # where the slope starts at the front: lip root
K = (HB - ZF) / (DEP - YF)               # slope 48 / 180: 14.9 deg
LIP = 6.0                                # lip, square to the slope
MEM = 8.0                                # member width
YO = 48.0                                # back face of the solid front block
RO_, RI = 2.0, 2.0                       # outer and inner corner radii
LAPTOP = (300.0, 215.0, 16.0)            # an example laptop: width, depth, thickness
X_STAND = 100.0                          # stand centre lines under the laptop


def stand_profile():
    import math
    c, s = 1 / math.hypot(1, K), K / math.hypot(1, K)       # slope direction (cos, sin)
    lx, ly = YF - s * LIP, ZF + c * LIP                     # lip top, back corner
    outer = cq.Workplane("XY").polyline([(0, 0), (DEP, 0), (DEP, HB), (YF, ZF), (lx, ly), (0, ly)]).close().extrude(WID)
    convex = [e for e in outer.edges("|Z").vals()                # the lip root stays square: the laptop's edge sits in it
              if abs(e.Center().x - YF) > 0.1 or abs(e.Center().y - ZF) > 0.1]
    outer = cq.Workplane("XY").add(outer.val().fillet(RO_, convex))
    zt = lambda y: ZF - MEM / c + (y - YF) * K               # noqa: E731  lower edge of the top member
    inner = (cq.Workplane("XY").polyline([(YO, MEM), (DEP - MEM, MEM), (DEP - MEM, zt(DEP - MEM)), (YO, zt(YO))]).close()
             .extrude(WID + 2).translate((0, 0, -1)).edges("|Z").fillet(RI))
    p = outer.cut(inner).faces("<Z").chamfer(CH_BED)
    return p.faces(">Z").chamfer(CH)


def laptop():
    """The example laptop lying on the stands, its front bottom edge on the lip roots. It is larger than the stands, so it
    is not returned as a ref part (size_mm would become its size); the review checks it against the stands."""
    import math
    lw, ld, lt = LAPTOP
    lap = box(-lw / 2, lw / 2, 0, ld, 0, lt)
    return rx(lap, math.degrees(math.atan(K))).translate((0, YF - DEP / 2, ZF))


def laptop_stand_pair():
    p = stand_profile()                                      # print frame: profile on the bed, x = depth, y = height
    disp = lambda wp, x0: rz(rx(wp, 90), 90).translate((x0 - WID / 2, -DEP / 2, 0))   # noqa: E731
    stands = copies([disp(p, -X_STAND), disp(p, X_STAND)])
    return {"stand": Part(stands, p, OFF, qty=2)}


SAMPLES["047_laptop_stand_pair"] = laptop_stand_pair
