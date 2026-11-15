"""033 Tablet stand: a low block (128 x 96 x 24) with one slot across it, leaning back 3 : 1.

The tablet's bottom edge stands in the slot and its back lies flat on the slot's back wall, so it leans
at the wall's angle whatever its thickness; the front wall only keeps the edge from sliding forward.
The floor of the slot is square to the back wall. The slot sits in the front third, so a tablet's
centre of gravity falls well inside the block in portrait and landscape. One part, printed bottom down:
the front wall of the slot overhangs only 18.4 deg from vertical.
"""
import math
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, CH, CH_BED, OFF,  # noqa: E402
                         box, rrect, feet, plane_yz)

W, D, H = 128.0, 96.0, 24.0     # 4 : 3 in plan; deep enough behind the slot for a portrait tablet
R = D / 8                       # 12: 12.5 % of the depth
LEAN = math.atan(1 / 3)         # 18.4 deg: 1 back for 3 up
SLOT = 12.0                     # tablets with a thin case, up to about 11.5
DEPTH = 18.0                    # along the back wall
FRONT = 16.0                    # front strip at the top: four modules
TAB = (240.0, 8.0, 170.0)       # a 10-11 inch tablet in landscape (width, thickness, height), for tablet_fit()


def stand_block():
    s, c = math.sin(LEAN), math.cos(LEAN)
    yf = -D / 2 + FRONT                     # slot's front edge on the top face
    yb = yf + SLOT / c                      # back edge on the top face
    # slot in the YZ profile: back wall from (yb, H) down-forward DEPTH, floor square to it, front wall parallel
    p_back_bot = (yb - DEPTH * s, H - DEPTH * c)
    p_front_bot = (p_back_bot[0] - SLOT * c, p_back_bot[1] + SLOT * s)
    up = 2.0                                # carry the cut above the top
    prof = [(yb + up * s, H + up * c), p_back_bot, p_front_bot,
            (yf + up * s, H + up * c)]
    block = rrect(W, D, R, 0, H).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    slot = plane_yz(-W).polyline(prof).close().extrude(2 * W)
    block = block.cut(slot)
    for y, d in ((yf, 1), (yb, -1)):        # C0.5 lead-in on both slot edges: a 45-deg prism along X
        lead = plane_yz(-W).polyline([(y, H + 0.01), (y - d * CH, H + 0.01), (y, H - CH)]).close().extrude(2 * W)
        block = block.cut(lead)
    for sx in (-1, 1):                      # C0.5 on the slot's outline where it leaves the two ends: a 45-deg flare
        x0, x1 = sx * (W / 2 - CH), sx * (W / 2 + 0.01)
        w0 = plane_yz(x0).polyline(prof).close().wires().val()
        w1 = plane_yz(x1).polyline(prof).close().offset2D(CH + 0.01, "intersection").wires().val()
        block = block.cut(cq.Workplane("XY").add(cq.Solid.makeLoft([w0, w1], True)))
    block = feet(block, [(sx * 48, sy * 32) for sx in (-1, 1) for sy in (-1, 1)])
    return block, p_back_bot


def tablet_fit(thickness=TAB[1], height=TAB[2]):
    """A tablet standing in the slot, its back on the back wall and its edge on the floor (for checks; it is
    not a part: it would set the model's size)."""
    s, c = math.sin(LEAN), math.cos(LEAN)
    _, p_back_bot = stand_block()

    tab = box(-TAB[0] / 2, TAB[0] / 2, 0, thickness, 0, height).edges("|Y").fillet(6.0)
    tab = tab.rotate((0, 0, 0), (1, 0, 0), -math.degrees(LEAN))
    # the tilt keeps the front-bottom corner at the origin: move the back-bottom corner onto the slot's
    off = 0.1                               # 0.1 off the wall and the floor, so the fit check sees no touch
    tab = tab.translate((0, p_back_bot[0] - thickness * c - off * c + off * s, p_back_bot[1] + thickness * s + off * s + off * c))
    return tab


def tablet_stand_slot():
    block, _ = stand_block()
    return {"stand": Part(block, block, OFF)}


SAMPLES["033_tablet_stand_slot"] = tablet_stand_slot
