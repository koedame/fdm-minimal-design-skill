"""037 Small shelf bracket: an 80 x 80 L, 28 wide, that hangs on a wall plate and hides its screws.

The plate is screwed to the wall with two countersunk screws. Its section is a 45-deg dovetail; the
bracket's back carries the matching pocket, open at the bottom, and slides down over it, so the screws
sit behind the bracket and the dovetail takes the pull at the top of the leg. A screw from below,
through a counterbore in the arm, fixes the shelf board to the bracket and keeps it from lifting off.
The bracket prints lying on its side, so the layers run along the L.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, CH, CH_BED, GAP, OFF, rx, plane_yz  # noqa: E402

W, D, H = 28.0, 80.0, 80.0          # width, arm length from the wall, height
TH = 12.0                           # leg and arm thickness
WEB = 28.0                          # 45-deg web in the inside corner, 28 along each leg
PB, PT = 12.0, 4.0                  # plate: width at the wall, thickness; 45-deg flanks -> 20 at the front
PZ0, PZ1 = 8.0, 64.0                # plate height 56
SCREW_Z = (PZ0 + 12.0, PZ1 - 12.0)  # wall screws, 4 mm countersunk
SHELF_Y = D - 24.0                  # board screw, 3.5 mm, from below
K = 0.70710678


def trap(hb, y0, y1, z0, z1):
    """Prism along Z of a 45-deg dovetail section: half-width hb at y = 0, growing 1 per 1 in y."""
    pts = [(-(hb + y0), y0), (hb + y0, y0), (hb + y1, y1), (-(hb + y1), y1)]
    return cq.Workplane("XY").workplane(offset=z0).polyline(pts).close().extrude(z1 - z0)


def teardrop_z(x, y, z0, h, r):
    """Round hole along Z with a 45-deg roof toward +X (up when the bracket lies on its side)."""
    tri = [(x + r * K, y - r * K), (x + r * 1.41421356, y), (x + r * K, y + r * K), (x, y)]
    w = cq.Workplane("XY").workplane(offset=z0)
    return w.center(x, y).circle(r).extrude(h).union(w.polyline(tri).close().extrude(h))


def shelf_bracket_small():
    prof = [(0, 0), (TH, 0), (TH, H - TH - WEB), (TH + WEB, H - TH), (D, H - TH), (D, H), (0, H)]
    br = plane_yz(-W / 2).polyline(prof).close().extrude(W)
    br = br.edges("|X").chamfer(CH)
    br = br.faces("<X").edges().chamfer(CH_BED).faces(">X").edges().chamfer(CH)
    c = GAP * 1.41421356                                    # 0.25 normal to the 45-deg flanks
    br = br.cut(trap(PB / 2 + c, -1, PT + GAP, -1, PZ1 + GAP))
    br = br.cut(teardrop_z(0, SHELF_Y, H - TH - 1, TH + 2, 2.0))          # 3.5 screw: Ø4 clearance
    br = br.cut(teardrop_z(0, SHELF_Y, H - TH - 1, 1 + TH - 4.0, 4.2))    # head Ø8.4, 4 left under the board

    plate = trap(PB / 2, 0, PT, PZ0, PZ1)
    plate = plate.faces("<Z or >Z").edges().chamfer(CH)
    for z in SCREW_Z:
        plate = plate.cut(cq.Workplane("XZ").workplane(offset=1).center(0, z).circle(2.25).extrude(-PT - 2))
        plate = plate.cut(cq.Workplane("XY").add(cq.Solid.makeCone(
            2.25, 4.5, 2.26, cq.Vector(0, PT - 2.25, z), cq.Vector(0, 1, 0))))
    return {
        "bracket": Part(br, br.rotate((0, 0, 0), (0, 1, 0), -90), OFF),
        "wall_plate": Part(plate, rx(plate, 90), OFF),
    }


SAMPLES["037_shelf_bracket_small"] = shelf_bracket_small
