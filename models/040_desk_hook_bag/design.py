"""040 Desk bag hook: a J hook that hangs under the edge of a desk on a hidden plate.

The plate is screwed to the underside of the desk, just behind the edge. Its section is a 45-deg
dovetail; the hook's top carries the matching pocket, open at the back and closed at the front, and is
pushed back onto it from the desk edge until the pocket's front wall meets the plate, so the plate and
its screws are covered and the front face is whole. One M3 screw from below, in a counterbore in the
hook, goes up into the plate and keeps the hook from sliding forward off it.
The strap of a bag goes in from the front over the tip and rests in the round bottom of the J. The hook
prints lying on its side, so the layers run round the J.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, CH, CH_BED, GAP, OFF, box, rx, plane_yz  # noqa: E402

W = 32.0                            # hook width
Y0, Y1 = -60.0, -4.0                # top block: 56 deep, its front 4 behind the desk edge (y = 0)
TB = 16.0                           # top block thickness
JY0, JY1, JZ = -60.0, -20.0, -60.0  # the J: 40 deep, its bottom 60 under the desk
ARM = 12.0                          # arm and tip thickness
SLOT_R = 8.0                        # strap rests in a round bottom, 16 wide
TIP_Z = -36.0                       # the opening over the tip: 20 high, under the top block
PB, PT = 12.0, 4.0                  # plate: 12 wide at the desk, 4 thick, 45-deg flanks -> 20
PY0, PY1 = -56.0, -8.0              # plate 48 long
WOOD_Y = (-24.0, -48.0)             # 4 mm countersunk wood screws, up into the desk
LOCK_Y = -14.0                      # M3 locking screw, clear of the tip below it
K = 0.70710678


def trap_y(hb, z0, z1, y0, y1):
    """Prism along Y of a 45-deg dovetail section: half-width hb at z = 0, growing 1 per 1 downward."""
    pts = [(-(hb - z0), z0), (hb - z0, z0), (hb - z1, z1), (-(hb - z1), z1)]
    return cq.Workplane("XZ").workplane(offset=-y1).polyline(pts).close().extrude(y1 - y0)


def teardrop_z(x, y, z0, h, r):
    """Round hole along Z with a 45-deg roof toward +X (up when the hook lies on its side)."""
    tri = [(x + r * K, y - r * K), (x + r * 1.41421356, y), (x + r * K, y + r * K), (x, y)]
    w = cq.Workplane("XY").workplane(offset=z0)
    return w.center(x, y).circle(r).extrude(h).union(w.polyline(tri).close().extrude(h))


def at(y, z):
    return cq.selectors.BoxSelector((-W, y - 0.01, z - 0.01), (W, y + 0.01, z + 0.01))


def desk_hook_bag():
    hk = box(-W / 2, W / 2, Y0, Y1, -TB, 0).union(box(-W / 2, W / 2, JY0, JY1, JZ, -TB + 0.01))
    yc, zc = JY0 + ARM + SLOT_R, JZ + ARM + SLOT_R                      # centre of the round bottom
    hk = hk.cut(box(-W, W, yc - SLOT_R, yc + SLOT_R, zc, -TB + 0.01))
    hk = hk.cut(plane_yz(-W).center(yc, zc).circle(SLOT_R).extrude(2 * W))
    hk = hk.cut(box(-W, W, yc + SLOT_R, JY1 + 1, TIP_Z, -TB + 0.01))  # the opening over the tip
    hk = hk.edges(at(JY0, JZ)).fillet(12.0).edges(at(JY1, JZ)).fillet(12.0)
    hk = hk.edges(at(JY1 - ARM, TIP_Z)).fillet(3.0).edges(at(JY1, TIP_Z)).fillet(3.0)   # 4 of straight under it
    hk = hk.faces("<X").edges().chamfer(CH_BED).faces(">X").edges().chamfer(CH)
    c = GAP * 1.41421356                                                # 0.25 normal to the 45-deg flanks
    hk = hk.cut(trap_y(PB / 2 + c, 1.0, -(PT + GAP), Y0 - 1, PY1 + GAP))
    hk = hk.cut(teardrop_z(0, LOCK_Y, -TB - 1, TB + 1 - PT, 1.7))       # M3 clearance, through to the plate
    hk = hk.cut(teardrop_z(0, LOCK_Y, -TB - 1, 1 + TB - PT - GAP - 4.0, 3.1))  # head Ø6.2; 4 left under the plate

    plate = trap_y(PB / 2, 0, -PT, PY0, PY1)
    plate = plate.faces("<Y or >Y").edges().chamfer(CH)
    for y in WOOD_Y:
        plate = plate.cut(cq.Workplane("XY").workplane(offset=-PT - 1).center(0, y).circle(2.25).extrude(PT + 2))
        plate = plate.cut(cq.Workplane("XY").add(cq.Solid.makeCone(
            4.5, 2.25, 2.26, cq.Vector(0, y, -PT - 0.01), cq.Vector(0, 0, 1))))
    plate = plate.cut(cq.Workplane("XY").workplane(offset=-PT - 1).center(0, LOCK_Y).circle(1.25).extrude(PT + 2))
    return {
        "hook": Part(hk, hk.rotate((0, 0, 0), (0, 1, 0), -90), OFF),
        "desk_plate": Part(plate, rx(plate, 180), OFF),
    }


SAMPLES["040_desk_hook_bag"] = desk_hook_bag
