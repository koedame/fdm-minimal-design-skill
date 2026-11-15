"""027 Desk edge cable clip: a C that pushes onto a 20 mm desk edge, with a U-hook behind it for cables.

The side profile is the design, so the clip prints lying on its side and every radius lies in the layer
plane: R5 on the two outer back corners, R1.6 on everything else (the plate ends come out nearly round).
The jaws are 3.36 thick and carry a 45-deg ridge near their tips that narrows the 20 mouth to 19.2, so each
jaw flexes 0.4 onto the desk and holds by spring. Cables run along the back of the desk in the hook;
several clips along the edge carry a bundle.
"""
import os
import sys

import cadquery as cq
from cadquery.selectors import BoxSelector

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, CH, CH_BED, OFF, DARK, cyl, rx, plane_xz, copies  # noqa: E402

DESK = 20.0                       # desk thickness (match yours)
J = 3.36                          # jaws, spine and hook: 8 lines of 0.42 (the jaw stiffness, see rationale)
JAW = 24.0                        # jaw length on the desk
HW, HD = 12.0, 12.0               # hook inside: two Ø5 cables side by side, 12 deep
W = 24.0                          # clip width along the edge
R_OUT, R_IN = 5.0, 1.6            # outer back corners (J + R_IN: even wall round the bend); all other corners
RIDGE, RIDGE_X = 0.4, JAW - 4.0   # ridge height and position: mouth 19.2
ZB = -DESK - J                    # underside of the clip
XO = -J - HW - J                  # back face of the hook


def profile():
    """Side profile in XZ (x into the desk from its edge face, z up from the desk top), W wide along Y."""
    p = (cq.Workplane("XZ").moveTo(JAW, J).lineTo(-J, J).lineTo(-J, ZB + J)       # top jaw, spine back face
         .lineTo(XO + J, ZB + J).lineTo(XO + J, ZB + J + HD).lineTo(XO, ZB + J + HD)  # hook floor, hook wall
         .lineTo(XO, ZB).lineTo(JAW, ZB).lineTo(JAW, -DESK)                          # underside, bottom jaw tip
         .lineTo(0, -DESK).lineTo(0, 0).lineTo(JAW, 0).close())                     # the faces on the desk
    return p.extrude(W / 2, both=True)


def corner(wp, x, z, r):
    return wp.edges("|Y").edges(BoxSelector((x - 0.05, -W, z - 0.05), (x + 0.05, W, z + 0.05))).fillet(r)


def ridge(z, sgn):
    """45-deg ridge on a jaw face at height z, pointing sgn (+1 up, -1 down), 1 short of each side."""
    tri = [(RIDGE_X - RIDGE, z - sgn * 0.01), (RIDGE_X + RIDGE, z - sgn * 0.01), (RIDGE_X, z + sgn * RIDGE)]
    return plane_xz(W / 2 - 1).polyline(tri).close().extrude(W - 2)


def cable_clip_desk():
    c = profile()
    for x, z in ((-J, J), (XO, ZB)):
        c = corner(c, x, z, R_OUT)
    for x, z in ((JAW, J), (JAW, 0), (JAW, -DESK), (JAW, ZB), (XO, ZB + J + HD), (XO + J, ZB + J + HD),
                 (XO + J, ZB + J), (-J, ZB + J), (0, 0), (0, -DESK)):
        c = corner(c, x, z, R_IN)
    c = c.faces(">Y").edges().chamfer(CH_BED).faces("<Y").edges().chamfer(CH)
    c = c.union(ridge(0, -1)).union(ridge(-DESK, 1))
    xm = XO + J + HW / 2
    cables = copies([rx(cyl(2.5, -20, 40, xm + s * 2.8, ZB + J + 2.6), 90) for s in (-1, 1)])
    return {
        "clip": Part(c, rx(c, -90), OFF),
        "cables_ref": Part(cables, None, DARK, qty=2, ref=True),
    }


SAMPLES["027_cable_clip_desk"] = cable_clip_desk
