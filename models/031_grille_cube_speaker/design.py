"""031 Grille cube speaker: a 96 mm cube for one 2-inch full-range driver, with a field of vertical slots on
all four faces of its upper half.

The body is a cup printed bottom down. A baffle sits on a 45-deg ledge at half height and is glued there:
below it is the sealed back chamber of the driver, above it the open front chamber whose sound leaves
through the slots. The driver faces up and is screwed to the baffle. The top cap snaps on with four
vertical hooks that drop into grooves in posts standing in the four inner corners; being 45 deg, the
barbs let the cap be pulled off again to reach the driver. The speaker wire leaves through a teardrop
hole low in the back; a shallow finger scoop across the seam at the back is where the cap is lifted.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, cyl, rrect, rz, feet, teardrop_x, plane_xz)

S = 96.0                    # cube: width = depth = height
R = S / 8                   # 12: 12.5 % of the outline
FLOOR = 2.4
Z_BAF = S / 2               # baffle top: the slots take the half above it, the back chamber the half below
BAF = 3.36                  # baffle: 8 lines
LEDGE = 1.6                 # ledge under the baffle, 45-deg underside
Z_CAP = S - 4.0             # seam of the cap (cap 4 thick)
SW, SP = 1.6, 4.0           # slot width, pitch
FIELD = 8.0                 # slot centre lines two modules inside the flat of each face, the baffle line and the seam
SCOOP = 0.75 * (S - Z_CAP)  # finger scoop across the seam at the back: 3, clear of the cap's top edge (as 07)
U0 = 54.0                   # corner posts: their inner face, along the diagonal from the centre
HOOK_W, HOOK_L = 8.0, 16.0  # hook width and length below the cap
ZB = Z_CAP - 14.0           # barb centre
BARB = 1.0                  # barb height out of the hook (it reaches 0.75 into the post)

# driver (a generic 2-inch / 50 mm full-range driver with a square frame; check yours)
DRV_FRAME, DRV_FLANGE, DRV_CUT = 53.0, 3.0, 46.0
DRV_HOLES = 23.0            # screw holes at (+-23, +-23), M2.5 self-tapping
DRV_BASKET, DRV_MAG, DRV_DEPTH = 44.0, 36.0, 30.0


def diag(wp, k):
    """Move a shape built around the +X axis (u along +X) to corner k (0..3) of the cube's diagonals."""
    return rz(wp, 45 + 90 * k)


def post_region(u, z0, z1):
    return box(u, 80, -30, 30, z0, z1)


def grille_cube_speaker():
    cav = rrect(S - 2 * T, S - 2 * T, R - T, FLOOR, S)
    body = rrect(S, S, R, 0, Z_CAP).cut(cav)

    # ledge under the baffle (45-deg underside) and the four corner posts, floor to seam
    zl = Z_BAF - BAF
    ring = rrect(S - 2 * T, S - 2 * T, R - T, zl - LEDGE, LEDGE)
    w0 = rrect(S - 2 * T + 0.02, S - 2 * T + 0.02, R - T, zl - LEDGE - 0.001, 1).faces("<Z").wires().val()
    w1 = rrect(S - 2 * T - 2 * LEDGE, S - 2 * T - 2 * LEDGE, R - T - LEDGE, zl + 0.001, 1).faces("<Z").wires().val()
    body = body.union(ring.cut(cq.Workplane("XY").add(cq.Solid.makeLoft([w0, w1], True))))
    for k in range(4):
        body = body.union(diag(post_region(U0, FLOOR - 0.01, Z_CAP), k).intersect(cav))
        groove = plane_xz(HOOK_W / 2 + 1).polyline([(U0 - 0.01, ZB - 1.25), (U0 + 1.0, ZB - 0.25), (U0 + 1.0, ZB + 0.25),
                                                    (U0 - 0.01, ZB + 1.25)]).close().extrude(HOOK_W + 2)
        body = body.cut(diag(groove, k))

    body = body.faces("<Z").edges().chamfer(CH_BED)
    body = body.edges(cq.selectors.BoxSelector((-S, -S, Z_CAP - 0.01), (S, S, Z_CAP + 0.01))).chamfer(CH)

    # slots: vertical, semicircular ends, on the flat of every face
    flat = S / 2 - R
    n = int(round(2 * (flat - FIELD) / SP)) + 1             # 15
    z0, z1 = Z_BAF + FIELD, Z_CAP - FIELD                     # slot end centres 56 .. 84
    slot = (cq.Workplane("XZ").workplane(offset=-(S / 2 - T - 1)).center(0, (z0 + z1) / 2)
            .slot2D(z1 - z0 + SW, SW, 90).extrude(-(T + 2)))
    for k in range(4):
        for i in range(n):
            body = body.cut(rz(slot.translate((-(n - 1) * SP / 2 + i * SP, 0, 0)), 90 * k))
    body = body.cut(rz(teardrop_x(S / 2 - T - 1, T + 2, 0, 10.0, 2.0), 90))      # speaker wire, low in the back
    body = feet(body, [(sx * 32, sy * 32) for sx in (-1, 1) for sy in (-1, 1)])

    scoop = plane_xz(S / 2 - 1.2).center(0, Z_CAP).circle(SCOOP).extrude(-3)
    body = body.cut(scoop)

    # baffle: the cavity less the posts, 0.25 clear all round; driver cut-out and pilot holes
    baffle = rrect(S - 2 * (T + GAP), S - 2 * (T + GAP), R - T - GAP, zl, BAF)
    for k in range(4):
        baffle = baffle.cut(diag(post_region(U0 - GAP, zl - 1, Z_BAF + 1), k))
    baffle = baffle.faces(">Z").edges().chamfer(CH)
    baffle = baffle.cut(cyl(DRV_CUT / 2, zl - 1, BAF + 2))
    for sx in (-1, 1):
        for sy in (-1, 1):
            baffle = baffle.cut(cyl(1.1, zl - 1, BAF + 2, sx * DRV_HOLES, sy * DRV_HOLES))

    # cap: plate with a C0.5 seam edge, four hooks down to the posts' grooves
    cap = rrect(S, S, R, Z_CAP, S - Z_CAP).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    for k in range(4):
        u1 = U0 - GAP
        hook = box(u1 - DIV, u1, -HOOK_W / 2, HOOK_W / 2, Z_CAP - HOOK_L, Z_CAP + 0.01)
        barb = plane_xz(HOOK_W / 2).polyline([(u1 - 0.01, ZB - BARB), (u1 + BARB, ZB), (u1 - 0.01, ZB + BARB)]) \
            .close().extrude(HOOK_W)
        cap = cap.union(diag(hook.union(barb), k))
    cap = cap.cut(scoop)

    drv = box(-DRV_FRAME / 2, DRV_FRAME / 2, -DRV_FRAME / 2, DRV_FRAME / 2, Z_BAF, Z_BAF + DRV_FLANGE)
    drv = drv.union(cyl(DRV_BASKET / 2, Z_BAF - 14.0, 14.01)).union(cyl(DRV_MAG / 2, Z_BAF + DRV_FLANGE - DRV_DEPTH, 16.01))
    cone = cq.Solid.makeCone(DRV_BASKET / 2 - 3, 8.0, 12.0, pnt=cq.Vector(0, 0, Z_BAF + DRV_FLANGE + 0.01),
                             dir=cq.Vector(0, 0, -1))
    drv = drv.cut(cq.Workplane("XY").add(cone))
    return {
        "body": Part(body, body, OFF),
        "baffle": Part(baffle, baffle.rotate((0, 0, 0), (1, 0, 0), 180), DARK),
        "cap": Part(cap, cap.rotate((0, 0, 0), (1, 0, 0), 180), OFF),
        "driver_ref": Part(drv, None, DARK, ref=True),
    }


SAMPLES["031_grille_cube_speaker"] = grille_cube_speaker
