"""052 Business card holder: a low block on a floating plinth with one slot that holds a stack of cards leaning back.

One part, printed bottom down. The slot leans back at 1 : 4 (about 14 deg), so the cards stand at a reading angle
and stay put; its floor is square to the slope, so the cards sit on their bottom edge. A semicircular scoop in
the front wall, centred, lets a finger and thumb take the front card. Four rubber feet in recesses underneath.
"""
import math
import os
import sys

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from cadquery.selectors import BoxSelector  # noqa: E402
from fdm_samples import (Part, SAMPLES, CH, CH_BED, OFF, box, rrect, feet, plane_yz, plane_xz)  # noqa: E402

W, D, H = 104.0, 32.0, 24.0      # 26 x 8 x 6 modules
R = 8.0                          # plan radius: 25 % of the depth, 7.7 % of the width
PL, INSET = 2.4, 1.2             # floating plinth
CARD = (91.0, 55.0)              # Japanese business card (EU 85 x 55 and US 89 x 51 fit too)
SLOT_L = CARD[0] + 2 * 1.5       # 94: 1.5 clear at each end
SLOT_W = 12.0                    # horizontal width at the mouth: about 40 cards
SLOT_D = 16.0                    # vertical depth at the front line
SLOPE = 0.25                     # 1 : 4 back lean
YF = -8.0                        # front line of the slot at the top: front wall 8 at the top, 4 at the bottom
SCOOP = 10.0                     # scoop radius in the front wall
A = math.atan(SLOPE)


def card_stack(n=40):
    """The cards as an envelope (not a part): n cards of 0.28, leaning back on the slot's back face."""
    t = n * 0.28
    c, s = math.cos(A), math.sin(A)
    yb, zb = YF - SLOT_D * SLOPE + SLOT_W * c * c, H - SLOT_D - SLOT_W * c * s       # back corner of the floor
    p0 = (yb - 0.2 * c, zb + 0.2 * s)
    pts = [p0, (p0[0] - t * c, p0[1] + t * s)]
    pts += [(pts[1][0] + CARD[1] * s, pts[1][1] + CARD[1] * c), (p0[0] + CARD[1] * s, p0[1] + CARD[1] * c)]
    return plane_yz(-CARD[0] / 2).polyline(pts).close().extrude(CARD[0])


def business_card_holder():
    b = rrect(W - 2 * INSET, D - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    b = b.union(rrect(W, D, R, PL, H - PL).faces("<Z").chamfer(INSET))
    c, s = math.cos(A), math.sin(A)
    fb = (YF - SLOT_D * SLOPE, H - SLOT_D)                    # front corner of the floor
    bb = (fb[0] + SLOT_W * c * c, fb[1] - SLOT_W * c * s)     # back corner: floor square to the slope
    up = 2.0
    slot = plane_yz(-SLOT_L / 2).polyline([fb, bb, (bb[0] + (H + up - bb[1]) * SLOPE, H + up),
                                           (fb[0] + (H + up - fb[1]) * SLOPE, H + up)]).close().extrude(SLOT_L)
    b = b.cut(slot)
    b = b.cut(plane_xz(-D / 2 - 1).center(0, H).circle(SCOOP).extrude(-(D / 2 + YF + 2)))
    b = b.faces(">Z").edges().chamfer(CH)
    b = b.edges(BoxSelector((-SCOOP - 0.1, -D / 2 - 0.1, H - SCOOP - 0.1),          # the scoop's arcs, both faces of the wall
                            (SCOOP + 0.1, YF + 0.1, H - CH - 0.05))).chamfer(CH)
    b = feet(b, [(sx * 40, sy * 6) for sx in (-1, 1) for sy in (-1, 1)])
    return {"holder": Part(b, b, OFF)}


SAMPLES["052_business_card_holder"] = business_card_holder
