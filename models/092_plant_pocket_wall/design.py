"""092 Wall plant pocket: a 72 cube that hangs on two screws and hides a 60 mm nursery pot (Japanese size 2) inside.

One part, printed bottom down, the 051_remote_holder_wall arrangement for a plant: R10 at the two front corners, the back
flat against the wall with its vertical corners cut back 1.2 at 45 deg for a shadow line, and the back wall thickened to 6.4
so two keyholes are cut into it from the wall side (nothing shows inside). The floor is closed, so water that runs out of the
pot stays in the pocket; two ribs 4 high keep the pot out of it.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, OFF, GAP,  # noqa: E402
                         box, rrect, rx, cyl, keyhole_local, plane_yz)

S = 72.0                                  # a 72 cube: 18 modules
R = 10.0                                  # front corners: 14 % of the side
SHADOW = 1.2                              # back corners cut back at 45 deg
BACK = 6.4                                # back wall at the keyholes: ledge 2 + head pocket 3 + 1.4
Z_BACK = S - 12.0                         # above it the back wall steps back to T on a 45-deg face: the rim is T all round
FLOOR = 2.4
RIB_H, RIB_X = 4.0, 12.0                  # two ribs under the pot, 24 apart (half its base)
KEY_X = S / 4                             # keyholes 36 apart = half the width
KEY_Z, TRAVEL = S - 28.0, 6.0             # entry centre, slot rising 6 toward the rim

POT = (60.0, 45.0, 55.0)                  # size-2 nursery pot: rim Ø60, base Ø45, 55 high (check yours)


def outline(z0, h):
    s = rrect(S, S, R, z0, h).union(box(-S / 2, S / 2, 0, S / 2, z0, z0 + h))
    k = (cq.Workplane("XY").workplane(offset=z0 - 1)
         .polyline([(S / 2 - SHADOW, S / 2 + 0.01), (S / 2 + 0.01, S / 2 + 0.01), (S / 2 + 0.01, S / 2 - SHADOW)])
         .close().extrude(h + 2))
    return s.cut(k).cut(k.mirror("YZ"))


def pot():
    """The nursery pot as an envelope, standing on the ribs in the middle of the cavity (not a part: a bought pot whose
    size varies; checked against the pocket in the review)."""
    rt, rb, h = POT[0] / 2, POT[1] / 2, POT[2]
    yc = (-S / 2 + T + S / 2 - BACK) / 2
    return cq.Workplane("XY").add(cq.Solid.makeCone(rb, rt, h, pnt=cq.Vector(0, yc, FLOOR + RIB_H)))


def plant_pocket_wall():
    p = outline(0, S).faces("<Z").chamfer(CH_BED)
    cav = box(-S / 2 + T, S / 2 - T, -S / 2 + T, S / 2 - T, FLOOR, S + 1).edges("|Z").fillet(R - T)
    p = p.cut(cav)
    yb, yt = S / 2 - BACK, S / 2 - T
    thick = (plane_yz(-S / 2).polyline([(yb, FLOOR - 0.01), (yt + 0.01, FLOOR - 0.01), (yt + 0.01, Z_BACK),
                                         (yb, Z_BACK - (BACK - T))]).close().extrude(S))
    p = p.union(thick.intersect(cav))
    p = p.faces(">Z").edges().chamfer(CH)                         # the rim, outside and in
    for sx in (-1, 1):                    # ribs from the front wall to the thickened back wall
        rib = box(sx * RIB_X - DIV / 2, sx * RIB_X + DIV / 2, -S / 2 + T - .01, yb + .01, FLOOR - .01, FLOOR + RIB_H)
        p = p.union(rib.faces(">Z").edges("|Y").chamfer(CH))
    for sx in (-1, 1):
        p = p.cut(rx(keyhole_local(TRAVEL), 90).translate((sx * KEY_X, S / 2, KEY_Z)))
    return {"pocket": Part(p, p, OFF)}


SAMPLES["092_plant_pocket_wall"] = plant_pocket_wall
