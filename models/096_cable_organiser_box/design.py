"""096 Cable organiser box: a 144 x 96 x 64 box that hides the slack of cables, with U notches that let them out, and a lid
that locates on a lip.

The body is 48 high and the lid 16 (3 : 1). Four U notches, the same shape (10 wide, a round bottom, 16 deep), run down from
the rim: three in the front wall for charging cables, one in the back wall for a cord. They run to the rim, so a cable is laid
in from above and the lid closes over them; the lid's lip, 4 deep, passes 12 above a cable lying in a notch. The lip hangs
from the lid's wall, thickened inside down to the rim, as 07_hinged_case.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, box, rrect, feet, plane_xz  # noqa: E402

W, D, R = 144.0, 96.0, 12.0               # 3 : 2 on the 4 grid; R12 = 12.5 % of the depth
HB, HL = 48.0, 16.0                       # 3 : 1, 64 overall
FLOOR, TOP = 2.4, 2.4
LIP = 4.0                                 # the lip reaches 4 below the seam
NW, ND = 10.0, 16.0                       # notch width (a round bottom R5) and depth from the rim
FRONT_X = (-24.0, 0.0, 24.0)              # three notches on the grid, 24 apart
BACK_X = (0.0,)


def ring(off, z0, h):
    return rrect(W - 2 * off, D - 2 * off, R - off, z0, h)


def notch(x, y_lo, y_hi):
    """A U notch through a wall that lies between y_lo and y_hi (the tool runs 1 past both faces)."""
    zc = HB - ND + NW / 2
    u = plane_xz(y_hi).center(x, zc).circle(NW / 2).extrude(y_hi - y_lo)
    return u.union(box(x - NW / 2, x + NW / 2, y_lo, y_hi, zc, HB + 1))


def cable_organiser_box():
    body = ring(0, 0, HB).faces("<Z").chamfer(CH_BED)
    body = body.cut(ring(T, FLOOR, HB))
    for x in FRONT_X:
        body = body.cut(notch(x, -D / 2 - 1, -D / 2 + T + 1))
    for x in BACK_X:
        body = body.cut(notch(x, D / 2 - T - 1, D / 2 + 1))
    body = body.faces(">Z").edges().chamfer(CH)                     # the rim, outside and in, round the notches' tops
    for y in (-D / 2, -D / 2 + T, D / 2, D / 2 - T):                # the notches' outlines on both faces of the walls
        body = body.edges(cq.selectors.BoxSelector((-W / 2, y - 0.05, HB - ND - 0.1),
                                                   (W / 2, y + 0.05, HB - CH - 0.05))).chamfer(CH)
    body = feet(body, [(sx * (W / 2 - 16), sy * (D / 2 - 16)) for sx in (-1, 1) for sy in (-1, 1)])

    lid = ring(0, HB, HL).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    lid = lid.cut(ring(T, HB - 1, HL - TOP + 1))
    lip = (ring(T + GAP, HB - LIP, LIP + .01).union(ring(T - 0.5, HB, HL - TOP + .01))
           .cut(ring(T + GAP + DIV, HB - LIP - 1, HL + LIP + 2)))
    lid = lid.union(lip)
    return {
        "body": Part(body, body, OFF),
        "lid": Part(lid, lid.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, HB + HL)), OFF),
    }


SAMPLES["096_cable_organiser_box"] = cable_organiser_box
