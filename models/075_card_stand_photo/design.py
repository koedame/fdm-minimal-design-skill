"""075 Photo and card stand: a 64 wide block whose side profile is a ramp with one slot leaning back at 1 : 3.

One part, printed on its side so the profile (the design of this object) is drawn in the layer plane and comes out
crisp. The slot runs parallel to the sloped front, 2 wide, so a photo, a postcard or a card up to about 1.5 thick
stands in it leaning back about 18 deg; its floor is square to the slope, so the card sits on its bottom edge. The
4 thick lamella in front of the slot ends in a full round, level with the flat top behind the slot.
"""
import math
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, CH, CH_BED, OFF, plane_yz  # noqa: E402

W, D, H = 64.0, 48.0, 24.0       # 16 x 12 x 6 modules (8 : 6 : 3)
SLOPE = 1 / 3                    # front face and slot lean back 1 : 3 (18.4 deg): a tall photo leans enough to stay
LAM = 4.0                        # lamella in front of the slot (square to the slope)
SLOT = 2.0                       # slot width: a photo, a postcard, a card in a thin sleeve up to about 1.5
SLOT_Z = 8.0                     # the slot's floor stays 8 above the table (a third of the height)
R = 8.0                          # back top corner
PHOTO = (89.0, 127.0)            # L-size photo, portrait (a 100 x 148 postcard stands too)

A = math.atan(SLOPE)
U = (math.sin(A), math.cos(A))   # up the slope, in (y, z)
N = (math.cos(A), -math.sin(A))  # into the block, square to the slope


def _p(s, t):
    """A point at s up the slope and t into the block from the front toe."""
    return (-D / 2 + s * U[0] + t * N[0], s * U[1] + t * N[1])


def photo(t=0.3):
    """A photo (not a part) standing in the slot, leaning on its back face, sitting on its floor."""
    s0 = _s0() + 0.05
    t1, t0 = LAM + SLOT - 0.05, LAM + SLOT - 0.05 - t
    pts = [_p(s0, t0), _p(s0, t1), _p(s0 + PHOTO[1], t1), _p(s0 + PHOTO[1], t0)]
    return plane_yz(-PHOTO[0] / 2).polyline(pts).close().extrude(PHOTO[0])


def _s0():
    """Where the slot's floor (square to the slope) crosses the slope, so its lowest corner is at SLOT_Z."""
    return (SLOT_Z - (LAM + SLOT) * N[1]) / U[1]


def card_stand_photo():
    s0 = _s0()
    s_lam = (H - LAM / 2 * N[1]) / U[1] - LAM / 2       # the lamella's round end reaches H
    s_back = (H - (LAM + SLOT) * N[1]) / U[1]           # the slot's back face meets the top
    c, k = _p(s_lam, LAM / 2), 0.70710678
    top_arc = (c[0] + LAM / 2 * U[0], c[1] + LAM / 2 * U[1])
    prof = (plane_yz(-W / 2).moveTo(-D / 2, 0).lineTo(*_p(s_lam, 0))
            .threePointArc(top_arc, _p(s_lam, LAM))
            .lineTo(*_p(s0, LAM)).lineTo(*_p(s0, LAM + SLOT)).lineTo(*_p(s_back, LAM + SLOT))
            .lineTo(D / 2 - R, H).threePointArc((D / 2 - R + R * k, H - R + R * k), (D / 2, H - R))
            .lineTo(D / 2, 0).close())
    b = prof.extrude(W)
    b = b.faces("<X").chamfer(CH_BED).faces(">X").chamfer(CH)          # the profile faces: bed side and top side
    yb = _p(s_back, LAM + SLOT)[0]
    for (y, z) in ((-D / 2, 0), (D / 2, 0), (yb, H)):                     # the sharp long edges: toe, heel, slot mouth
        b = b.edges(cq.selectors.BoxSelector((-W, y - 0.05, z - 0.05), (W, y + 0.05, z + 0.05))).chamfer(CH)
    return {"stand": Part(b, b.rotate((0, 0, 0), (0, 1, 0), -90), OFF)}


SAMPLES["075_card_stand_photo"] = card_stand_photo
