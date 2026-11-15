"""039 Napkin holder: a U of two upright walls on a base, 128 long x 48 x 96 high, napkins stood in the slot.

The U is one profile run straight through 128, so the holder prints lying on one end: every layer is the
whole U, the uprights are as strong as the plastic along their height, and nothing overhangs. The base
floats on a plinth set 1.2 inward at 45 deg (03); inside, the floor runs into the walls on a cove.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, CH, CH_BED, OFF, box, rx, plane_xz  # noqa: E402

L, W, H = 128.0, 48.0, 96.0         # 8 : 3 : 6
TW = 3.36                           # upright walls: 8 lines
PL, INSET = 2.4, 1.2                # plinth: 2.4 high, 1.2 inward at 45 deg
FLOOR = 6.0                         # a heavy foot under a tall, light load
COVE = 8.0
K = 0.70710678


def foot_recess(x, y):
    """Ø10.2 x 1 rubber foot recess with a 45-deg point toward +Y (up when the holder lies on its end)."""
    r = 5.1
    w = cq.Workplane("XY").workplane(offset=-0.01)
    tri = [(x - r * K, y + r * K), (x, y + r * 1.41421356), (x + r * K, y + r * K), (x, y)]
    return w.center(x, y).circle(r).extrude(1.01).union(w.polyline(tri).close().extrude(1.01))


def napkin_holder():
    a = W / 2 - INSET                           # the plinth step along the long sides only: the ends are
    prof = [(-a, 0), (a, 0), (a, PL), (W / 2, PL + INSET), (W / 2, H),          # flat, so the profile runs
            (-W / 2, H), (-W / 2, PL + INSET), (-a, PL)]                        # unchanged from end to end
    body = plane_xz(L / 2).polyline(prof).close().extrude(L)
    slot = box(-W / 2 + TW, W / 2 - TW, -L, L, FLOOR, H + 10).edges("|Y and <Z").fillet(COVE)
    body = body.cut(slot)
    body = body.faces(">Z").edges().chamfer(CH)
    body = body.faces("<Y").edges().chamfer(CH_BED).faces(">Y").edges().chamfer(CH)
    for sx in (-1, 1):
        for sy in (-1, 1):
            body = body.cut(foot_recess(sx * 14, sy * 48))
    return {"holder": Part(body, rx(body, 90), OFF)}


SAMPLES["039_napkin_holder"] = napkin_holder
