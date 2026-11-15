"""051 Wall remote holder: an open cup that hangs on two screws and holds a TV or air-conditioner remote upright.

One part, printed bottom down. The cup is 64 x 36 in plan with R8 at the two front corners; the back stands
flat against the wall and its two vertical corners are cut back 1.2 at 45 deg, so the cup sits on a thin
shadow line at each side. The back wall is 6.4 thick: two keyholes are cut into it from the wall side (head
pocket and 45-deg seat inside the wall, nothing shows in the cup). The front wall has a U opening running to
the rim, as wide as the keyholes are apart, so the remote's face shows and a thumb reaches it.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, OFF, DARK,  # noqa: E402
                         box, rrect, rx, keyhole_local, plane_xz, plane_yz)

W, D, H = 64.0, 36.0, 96.0        # 16 x 9 x 24 modules; H = 1.5 W
R = 8.0                           # front corners: 12.5 % of the width
SHADOW = 1.2                      # back corners cut back at 45 deg
BACK = 6.4                        # back wall at the keyholes: ledge 2 + head pocket 3 + 1.4
Z_BACK = H - 12.0                 # above it the back wall steps back to T on a 45-deg face, so the rim is T all round
FLOOR = 2.4
U_W = 32.0                        # U opening = W / 2 = the keyhole spacing
U_DEPTH = H / 2                   # bottom of the U at half height
KEY_X = U_W / 2
KEY_Z, TRAVEL = H - 28.0, 6.0     # keyhole entry centre, slot rising 6 toward the rim

REMOTE = (52.0, 22.0, 180.0)      # a common TV remote, as an envelope (check yours)


def outline(z0, h):
    """Plan: R8 at the front corners, square at the back, back corners cut 1.2 x 45 deg."""
    s = rrect(W, D, R, z0, h).union(box(-W / 2, W / 2, 0, D / 2, z0, z0 + h))
    k = (cq.Workplane("XY").workplane(offset=z0 - 1)
         .polyline([(W / 2 - SHADOW, D / 2 + 0.01), (W / 2 + 0.01, D / 2 + 0.01), (W / 2 + 0.01, D / 2 - SHADOW)])
         .close().extrude(h + 2))
    return s.cut(k).cut(k.mirror("YZ"))


def remote():
    """The held remote as an envelope standing on the floor against the back wall (not a part: it is
    taller than the holder, and size_mm would become its size)."""
    w, d, h = REMOTE
    yb = D / 2 - BACK
    return box(-w / 2, w / 2, yb - d - 0.3, yb - 0.3, FLOOR, FLOOR + h)


def remote_holder_wall():
    cup = outline(0, H)
    cav = box(-W / 2 + T, W / 2 - T, -D / 2 + T, D / 2 - T, FLOOR, H + 1).edges("|Z").fillet(R - T)
    cup = cup.cut(cav)
    yb, yt = D / 2 - BACK, D / 2 - T
    thick = (plane_yz(-W / 2).polyline([(yb, FLOOR - 0.01), (yt + 0.01, FLOOR - 0.01), (yt + 0.01, Z_BACK),
                                         (yb, Z_BACK - (BACK - T))]).close().extrude(W))
    cup = cup.union(thick.intersect(cav))
    # U opening through the front wall, open at the rim, semicircular bottom
    zc = H - U_DEPTH + U_W / 2
    u = (plane_xz(-D / 2 - 1).center(0, zc).circle(U_W / 2).extrude(-(T + 2))
         .union(box(-U_W / 2, U_W / 2, -D / 2 - 1, -D / 2 + T + 1, zc, H + 1)))
    cup = cup.cut(u)
    cup = cup.faces("<Z").chamfer(CH_BED)
    cup = cup.faces(">Z").edges().chamfer(CH)
    for y in (-D / 2, -D / 2 + T):                            # the U's edges on the outer and inner face of the wall
        cup = cup.edges(cq.selectors.BoxSelector((-U_W / 2 - 0.1, y - 0.05, H - U_DEPTH - 0.1),
                                                 (U_W / 2 + 0.1, y + 0.05, H - CH - 0.05))).chamfer(CH)
    for sx in (-1, 1):
        cup = cup.cut(rx(keyhole_local(TRAVEL), 90).translate((sx * KEY_X, D / 2, KEY_Z)))
    return {"cup": Part(cup, cup, OFF)}


SAMPLES["051_remote_holder_wall"] = remote_holder_wall
