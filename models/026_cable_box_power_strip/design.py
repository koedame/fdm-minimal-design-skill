"""026 Cable box: a 240 x 96 x 96 cover over a power strip, located on a base plate by a lip.

The cover is a sleeve with a top, printed top face down; the strip sits on the base plate, and the cover
lifts off it. Each end has a U-slot for the cords that runs to the bottom edge, so it is open at the top
in the print and needs no bridge. The lip on the base plate is cut where the slots are, so the cords lie
flat on the plate. A field of small holes on the top lets warm air out; its margin is 40 on every side.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, cyl, rrect, rx, feet, plane_yz)

L, W, H, R = 240.0, 96.0, 96.0, 12.0   # 5 : 2 in plan, a square section; R = 12.5 % of 96
BASE = TOP = 2.4
LIP = 4.0
SLOT_W, SLOT_H = 16.0, 24.0            # cord slot: 16 wide, 24 high including the round end
MARGIN = 40.0                          # around the vent field, the same on every side
HOLE_D, HOLE_P = 2.4, 4.0
STRIP = (210.0, 48.0, 36.0)            # the power strip (match yours): up to 210 x 48 x 36


def u_slot(x0, length):
    """Through a wall normal to X, from the bottom of the cover up to SLOT_H with a round top."""
    r = SLOT_W / 2
    s = plane_yz(x0).center(0, BASE + SLOT_H - r).circle(r).extrude(length)
    return s.union(box(min(x0, x0 + length), max(x0, x0 + length), -r, r, BASE - 1, BASE + SLOT_H - r))


def cable_box_power_strip():
    cover = rrect(L, W, R, BASE, H - BASE).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    cover = cover.cut(rrect(L - 2 * T, W - 2 * T, R - T, BASE - 1, H - BASE - TOP + 1))
    for sx in (-1, 1):
        cover = cover.cut(u_slot(sx * (L / 2 + 1), -sx * (T + 2)))
    nx, ny = int((L - 2 * MARGIN) / HOLE_P) + 1, int((W - 2 * MARGIN) / HOLE_P) + 1
    pts = [((i - (nx - 1) / 2) * HOLE_P, (j - (ny - 1) / 2) * HOLE_P) for i in range(nx) for j in range(ny)]
    holes = cq.Workplane("XY").workplane(offset=H - TOP - 1).pushPoints(pts).circle(HOLE_D / 2).extrude(TOP + 2)
    cover = cover.cut(holes)

    base = rrect(L, W, R, 0, BASE).faces("<Z").chamfer(CH_BED).faces(">Z").edges().chamfer(CH)
    lo, li = L - 2 * (T + GAP), W - 2 * (T + GAP)
    ring = rrect(lo, li, R - T - GAP, BASE - 0.01, LIP + 0.01).cut(rrect(lo - 2 * DIV, li - 2 * DIV, R - T - GAP - DIV, 0, 10))
    for sx in (-1, 1):
        x0, x1 = sorted((sx * (L / 2 - 2 * T), sx * L / 2))
        ring = ring.cut(box(x0, x1, -SLOT_W / 2, SLOT_W / 2, 0, 10))     # the cords lie flat where the slots are
    base = base.union(ring.faces(">Z").edges().chamfer(CH))             # lead-in for the cover
    base = feet(base, [(sx * 100, sy * 32) for sx in (-1, 1) for sy in (-1, 1)])

    strip = box(-STRIP[0] / 2, STRIP[0] / 2, -STRIP[1] / 2, STRIP[1] / 2, BASE, BASE + STRIP[2])
    strip = strip.union(rx(cyl(3.5, 0, 20), -90).rotate((0, 0, 0), (0, 0, 1), 90).translate((-STRIP[0] / 2, 0, BASE + 8)))
    return {
        "cover": Part(cover, rx(cover, 180), OFF),
        "base": Part(base, base, OFF),
        "power_strip_ref": Part(strip, None, (0.9, 0.9, 0.88), ref=True),
    }


SAMPLES["026_cable_box_power_strip"] = cable_box_power_strip
