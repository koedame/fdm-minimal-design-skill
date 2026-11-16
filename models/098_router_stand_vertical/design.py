"""098 Vertical router stand: a low block (128 x 80 x 32) with one straight slot across it in which a Wi-Fi router stands
on its long edge.

The slot is open at both ends, so a router longer than the block, or one with a port on its lower edge, still fits; the cables
leave from the upper edge. Standing the router up frees the desk and lets air rise along both its faces. One part, printed bottom
down without supports.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, CH, CH_BED, OFF, box, rrect, feet  # noqa: E402

W, D, H = 128.0, 80.0, 32.0     # 32 x 20 modules; 4 high for every 10 deep
R = 10.0                        # 12.5 % of the depth
SLOT = 36.0                     # routers 30-35 thick (check yours)
FLOOR = 8.0                     # slot floor: the slot is 24 deep, three quarters of the height
ROUTER = (200.0, 33.0, 160.0)   # a router standing on its long edge (length, thickness, height), for router_fit()


def stand():
    block = rrect(W, D, R, 0, H).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    block = block.cut(box(-W, W, -SLOT / 2, SLOT / 2, FLOOR, H + 1))
    mouth = cq.selectors.BoxSelector((-W, -SLOT / 2 - 0.1, FLOOR + 0.1), (W, SLOT / 2 + 0.1, H + 0.1))
    ends = cq.selectors.BoxSelector((-W / 2 - 0.1, -SLOT / 2 - 0.1, FLOOR - 0.1), (W / 2 + 0.1, SLOT / 2 + 0.1, H - CH - 0.1))
    block = block.edges(mouth).edges("|X").chamfer(CH)            # slot's top edges: lead-in
    block = block.edges(ends).edges("not |X").chamfer(CH)         # slot's outline on the two end faces
    return feet(block, [(sx * 48, sy * 28) for sx in (-1, 1) for sy in (-1, 1)])


def router_fit(thickness=ROUTER[1]):
    """A router standing in the slot on its long edge, centred (for checks; it is not a part)."""
    return box(-ROUTER[0] / 2, ROUTER[0] / 2, -thickness / 2, thickness / 2, FLOOR, FLOOR + ROUTER[2]).edges("|Y").fillet(8)


def router_stand_vertical():
    s = stand()
    return {"stand": Part(s, s, OFF)}


SAMPLES["098_router_stand_vertical"] = router_stand_vertical
