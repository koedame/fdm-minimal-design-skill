"""011 Utensil crock: a 104 x 104 x 156 square crock for kitchen utensils with drain slots in the floor.

Water that runs off the utensils drops through five slots in the floor into five channels under it,
which run out through the bottom of two opposite walls, so the floor dries and air reaches it.
The channels are open to the bed, so the crock prints bottom down with no support: the only
ceilings are the round tops of the 4 mm channels.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, CH, CH_BED, OFF, rrect, plane_yz  # noqa: E402

W, H, R = 104.0, 156.0, 14.0      # height : width = 3 : 2; R = 13.5 % of 104
FLOOR = 4.8                       # 2.4 channel + 2.4 floor over it
R_IN = 6.0                        # floor fillet inside: nothing lodges in the corner
CH_W = 4.0                        # channel width (grid); round top, r = 2
CH_Y = (-32.0, -16.0, 0.0, 16.0, 32.0)   # pitch 16 = 4 x grid: no point of the floor is over 8 from a slot
SLOT_W, SLOT_L = 2.4, 80.0        # floor slots over the channels: narrower than a utensil tip


def channel(y):
    """Along X under the floor: a 4 wide groove open to the bed with a semicircular top."""
    r = CH_W / 2
    z_c = FLOOR / 2 - r              # top of the arch at 2.4
    groove = plane_yz(-W).center(y, (z_c - 1) / 2).rect(CH_W, z_c + 1).extrude(2 * W)
    return groove.union(plane_yz(-W).center(y, z_c).circle(r).extrude(2 * W))


def utensil_crock():
    body = rrect(W, W, R, 0, H).faces("<Z").chamfer(CH_BED)
    cavity = rrect(W - 2 * T, W - 2 * T, R - T, FLOOR, H).faces("<Z").edges().fillet(R_IN)
    body = body.cut(cavity)
    body = body.faces(">Z").chamfer(CH)            # both rim edges, inner and outer
    for y in CH_Y:
        body = body.cut(channel(y))
        slot = cq.Workplane("XY").workplane(offset=FLOOR / 2 - 0.5).center(0, y).slot2D(SLOT_L, SLOT_W, 0)
        body = body.cut(slot.extrude(FLOOR))
    return {"crock": Part(body, body, OFF)}


SAMPLES["011_utensil_crock"] = utensil_crock
