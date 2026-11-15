"""055 Cable comb raceway: a short open-ended channel with two combs that keep four cables in order, and a lid that snaps on.

The ends are open and square in plan: a plan radius would run the walls out to a knife edge at the open ends.
Drawn as mounted on a wall or under a desk: the floor on the surface (z = 0), the lid away from it. The base
is a U channel open at both ends, printed floor down; two comb plates near the ends have four round-bottomed
notches each, one cable per notch. Two countersunk screws through the floor, between the combs, hold it (or
double-sided tape). The lid is a plate with the base's outline; four vertical hooks hang from it inside the
walls, and their 45-deg barbs drop into V grooves in the walls. The seam is a V line with C0.5 on both sides.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF,  # noqa: E402
                         box, cyl, rx, plane_yz)

L, W, H = 128.0, 40.0, 16.0      # 32 x 10 x 4 modules
FLOOR = LID = 2.4                # one plate thickness
Z_SEAM = H - LID                 # 13.6
N, P = 4, 8.0                    # four cables at a pitch of two modules
NOTCH = 5.6                      # cables up to about 5.2 (USB, laptop power, audio)
COMB_X = L / 2 - 12.0            # comb plates 12 in from the ends (= 1.5 pitches)
COMB_T = T
HOOK_X, HOOK_W = 32.0, 8.0       # hooks at the quarter points of the length
HOOK_Z0 = 3.0                    # hook bottom
BARB_Z, BARB = 4.4, 0.6          # barb: centre, height (free length 9.2: strain about 1.8 %)
SCREW_X = 16.0                   # two countersunk screws through the floor (3.5 wood screw, head 7)


def cable(i, d=5.2):
    """A cable lying in notch i as an envelope (not a part), running out of both ends."""
    y = -(N - 1) * P / 2 + i * P
    return plane_yz(-L / 2 - 10).center(y, FLOOR + d / 2 + 0.05).circle(d / 2).extrude(L + 20)


def cable_comb_raceway():
    b = box(-L / 2, L / 2, -W / 2, W / 2, 0, Z_SEAM).edges("|Z").chamfer(CH)
    b = b.faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    b = b.cut(box(-L / 2 - 1, L / 2 + 1, -W / 2 + T, W / 2 - T, FLOOR, H))
    for x in (-L / 2, L / 2):                                 # the channel's outline in the open ends
        b = b.edges(cq.selectors.BoxSelector((x - 0.05, -W / 2 + T - 0.05, FLOOR - 0.05),
                                             (x + 0.05, W / 2 - T + 0.05, Z_SEAM - CH - 0.05))).chamfer(CH)
    yi = W / 2 - T
    for sx in (-1, 1):                                        # comb plates with round-bottomed notches open at the top
        plate = box(sx * COMB_X - COMB_T / 2, sx * COMB_X + COMB_T / 2, -yi - 0.01, yi + 0.01, FLOOR - 0.01, Z_SEAM - GAP)
        for i in range(N):
            y = -(N - 1) * P / 2 + i * P
            plate = plate.cut(plane_yz(sx * COMB_X - COMB_T).center(y, FLOOR + NOTCH / 2).circle(NOTCH / 2).extrude(2 * COMB_T))
            plate = plate.cut(box(sx * COMB_X - COMB_T, sx * COMB_X + COMB_T, y - NOTCH / 2, y + NOTCH / 2,
                                  FLOOR + NOTCH / 2, H))
        b = b.union(plate.faces(">Z").edges().chamfer(CH))
    for sx in (-1, 1):
        b = b.cut(cyl(1.9, -1, FLOOR + 2, sx * SCREW_X, 0))
        b = b.cut(cq.Workplane("XY").add(cq.Solid.makeCone(1.9, 3.6, 1.7, pnt=cq.Vector(sx * SCREW_X, 0, FLOOR - 1.7 + 0.001))))
    # V grooves for the barbs: barb + 0.25 all round, 45 deg above and below
    for sx in (-1, 1):
        for sy in (-1, 1):
            g = plane_yz(sx * HOOK_X - HOOK_W / 2 - GAP).polyline(
                [(sy * (yi - 0.01), BARB_Z - BARB - 0.35), (sy * (yi + BARB + 0.25), BARB_Z - 0.1),
                 (sy * (yi + BARB + 0.25), BARB_Z + 0.1), (sy * (yi - 0.01), BARB_Z + BARB + 0.35)])
            b = b.cut(g.close().extrude(HOOK_W + 2 * GAP))          # 0.25 beside the hook: the lid's ends stay flush

    lid = box(-L / 2, L / 2, -W / 2, W / 2, Z_SEAM, H).edges("|Z").chamfer(CH).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    yo = yi - GAP                                             # hook outer face
    for sx in (-1, 1):
        for sy in (-1, 1):
            y0, y1 = sorted((sy * (yo - DIV), sy * yo))
            hook = box(sx * HOOK_X - HOOK_W / 2, sx * HOOK_X + HOOK_W / 2, y0, y1, HOOK_Z0, Z_SEAM + 0.01)
            barb = (plane_yz(sx * HOOK_X - HOOK_W / 2)
                    .polyline([(sy * (yo - 0.01), BARB_Z - BARB), (sy * (yo + BARB), BARB_Z), (sy * (yo - 0.01), BARB_Z + BARB)])
                    .close().extrude(HOOK_W))
            lid = lid.union(hook).union(barb)
    return {
        "base": Part(b, b, OFF),
        "lid": Part(lid, rx(lid, 180), OFF),
    }


SAMPLES["055_cable_comb_raceway"] = cable_comb_raceway
