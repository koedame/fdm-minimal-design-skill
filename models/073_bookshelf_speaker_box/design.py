"""073 Bookshelf speaker box: a sealed 112 x 128 x 168 box for one 3-inch full-range driver, its grille held by magnets.

The body is a sleeve with a back, printed back face down: the front outline's radii lie in the layer plane and the
open front faces up. The baffle is a separate 4.8 plate, printed front face down, that drops onto a ledge inside
the front and is glued in (it seals the box); the driver screws to it from the front. The perforated grille fills
the front flush, a reveal line round it; four posts on its back reach the baffle, and magnets in the posts and in
pockets in the back of the baffle (1.6 of plastic between them) hold it. Two binding posts go through the back.
"""
import math
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK, ACC,  # noqa: E402
                         box, copies, plane_xz)

# the driver (match yours): Ø80 frame 5 thick, cut-out Ø70, Ø66 basket 35 deep, 4 screws on a Ø74 circle
DRV_F, DRV_FT, DRV_CUT, DRV_B, DRV_BD, DRV_PCD = 80.0, 5.0, 70.0, 66.0, 35.0, 74.0
M = 16.0                                 # side margin round the driver
W = DRV_F + 2 * M                        # 112
H = 1.5 * W                              # 168: 2 : 3 front
D = 128.0                                # inside about 1.9 l: a sealed box for a 3-inch full-range driver
R, RI = 12.0, 3.0                        # front outline (11 % of 112); inside corners
PLATE = 4.8                              # back and baffle: two plates of 2.4, stiffer than the walls
GT = 4.0                                 # grille plate
AIR = 8.0                                # grille to baffle: the driver's 5 frame + 3
HOLE_D, HOLE_P = 2.5, 4.0                # perforation
FIELD_M = 12.0                           # margin of the perforation field: holds the posts, so the field is unbroken
POST_D = 8.0                             # 0.9 of wall round a magnet pocket
POST_IN = 6.0                            # posts centred 6 in from the grille's edge, in the middle of each side's margin
MAG_D, MAG_H = 6.2, 3.2
PILOT = 2.5                              # driver screws: M3 self-tapping
PUSH = 8.0                               # push hole under the grille: the air space is 8 deep
TERM_D, TERM_P = 4.2, 19.0               # two M4 binding posts, 19 apart (the usual banana-plug spacing)


def _xz(y_front, w, h, r, t):
    """Rounded rectangle in XZ centred on the front, from y_front back (+Y) by t."""
    return plane_xz(y_front + t).center(0, H / 2).rect(w, h).extrude(t).edges("|Y").fillet(r)


def bookshelf_speaker_box():
    yf = -D / 2
    yb_front = yf + GT + AIR                         # baffle front face
    yb_back = yb_front + PLATE
    zc = H / 2
    wi, hi = W - 2 * T, H - 2 * T

    body = _xz(yf, W, H, R, D)
    body = body.cut(_xz(yf - 1, wi, hi, R - T, D - PLATE + 1))
    body = body.faces("<Y").chamfer(CH).faces(">Y").chamfer(CH_BED)
    # ledge under the baffle: DIV wide, with a 45-deg underside (it prints facing up, the underside leans back to the wall)
    ledge_o = _xz(yb_back, wi + 0.02, hi + 0.02, R - T, DIV + DIV)
    lw, lh = wi - 2 * DIV, hi - 2 * DIV
    inner = cq.Solid.makeLoft([
        _xz(yb_back, lw, lh, R - T - DIV, 0.1).faces("<Y").wires().val(),
        _xz(yb_back + DIV, wi + 0.02, hi + 0.02, R - T, 0.1).faces("<Y").wires().val()], True)
    ledge = ledge_o.cut(_xz(yb_back - 1, lw, lh, R - T - DIV, DIV + 1.01)).cut(cq.Workplane("XY").add(inner))
    ledge = ledge.cut(_xz(yb_back + DIV, wi + 1, hi + 1, R - T, 10))
    body = body.union(ledge)
    # a hole in the bottom under the air space behind the grille: a fingertip pushes the grille off from behind.
    # A teardrop pointing to the front, which is up in the print (the hole is horizontal there)
    yp, rp = yf + GT + AIR / 2, PUSH / 2
    tear = cq.Workplane("XY").workplane(offset=-1).center(0, yp).circle(rp).extrude(T + 2).union(
        cq.Workplane("XY").workplane(offset=-1).polyline(
            [(-rp * 0.7071, yp - rp * 0.7071), (0, yp - rp * 1.4142), (rp * 0.7071, yp - rp * 0.7071), (0, yp)])
        .close().extrude(T + 2))
    body = body.cut(tear)
    for s in (-1, 1):
        body = body.cut(plane_xz(D / 2 + 1).center(s * TERM_P / 2, 24.0).circle(TERM_D / 2).extrude(PLATE + 2))

    bw, bh = wi - 2 * GAP, hi - 2 * GAP
    baffle = _xz(yb_front, bw, bh, R - T - GAP, PLATE).faces("<Y").chamfer(CH)
    baffle = baffle.cut(plane_xz(yb_back + 1).center(0, zc).circle(DRV_CUT / 2).extrude(PLATE + 2))
    for i in range(4):
        a = 0.78539816 + i * 1.57079633
        x, z = DRV_PCD / 2 * math.cos(a), zc + DRV_PCD / 2 * math.sin(a)
        baffle = baffle.cut(plane_xz(yb_back + 1).center(x, z).circle(PILOT / 2).extrude(PLATE + 2))
    gw, gh = wi - 2 * GAP, hi - 2 * GAP
    posts = [(s * (gw / 2 - POST_IN), zc) for s in (-1, 1)] + [(0, zc + s * (gh / 2 - POST_IN)) for s in (-1, 1)]
    for (x, z) in posts:                              # pockets from the back: open upward in the print, 1.6 to the front
        baffle = baffle.cut(plane_xz(yb_back + 0.01).center(x, z).circle(MAG_D / 2).extrude(MAG_H + 0.01))

    grille = _xz(yf, gw, gh, R - T - GAP, GT).faces("<Y").chamfer(CH)
    nx = int((gw - 2 * FIELD_M) // HOLE_P) + 1
    nz = int((gh - 2 * FIELD_M) // HOLE_P) + 1
    pts = [((i - (nx - 1) / 2) * HOLE_P, zc + (j - (nz - 1) / 2) * HOLE_P) for i in range(nx) for j in range(nz)]
    grille = grille.cut(plane_xz(yf + GT + 1).pushPoints(pts).circle(HOLE_D / 2).extrude(GT + 2))
    for (x, z) in posts:
        p = plane_xz(yb_front).center(x, z).circle(POST_D / 2).extrude(AIR + 0.01)
        grille = grille.union(p.faces("<Y").chamfer(CH)).cut(
            plane_xz(yb_front + 0.01).center(x, z).circle(MAG_D / 2).extrude(MAG_H + 0.01))

    mags = []
    for (x, z) in posts:
        mags.append(plane_xz(yb_front - 0.05).center(x, z).circle(3.0).extrude(3.0 - 0.1))
        mags.append(plane_xz(yb_back - 0.05).center(x, z).circle(3.0).extrude(3.0 - 0.1))
    drv = plane_xz(yb_front).center(0, zc).circle(DRV_F / 2).extrude(DRV_FT)
    drv = drv.union(plane_xz(yb_front + DRV_BD).center(0, zc).circle(DRV_B / 2).extrude(DRV_BD))
    return {
        "body": Part(body, body.rotate((0, 0, 0), (1, 0, 0), -90), OFF),
        "baffle": Part(baffle, baffle.rotate((0, 0, 0), (1, 0, 0), 90), DARK),
        "grille": Part(grille, grille.rotate((0, 0, 0), (1, 0, 0), 90), DARK),
        "magnet_ref": Part(copies(mags), None, ACC, qty=8, ref=True),
        "driver_ref": Part(drv, None, DARK, ref=True),
    }


SAMPLES["073_bookshelf_speaker_box"] = bookshelf_speaker_box
