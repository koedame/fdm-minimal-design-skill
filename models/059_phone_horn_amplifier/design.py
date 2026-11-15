"""059 Phone horn amplifier: a 112 x 64 x 40 block that holds a phone upright and turns its bottom speaker toward the listener.

No electronics: the phone stands in a slot leaned back 1:4, its back against the slot's back wall and its front corner on a
45-deg floor. Under the back of the slot a 6 wide throat runs the length of the slot, so the speaker on the phone's bottom edge
fires into it wherever along the edge it is. Below, a horn opens forward and downward to an 84 x 12 mouth at the bottom of the
front face; the horn is open at the bottom and the table closes it. That makes the block print top down with no supports: every
face of the horn and the throat faces up in the print or is steeper than 45 deg.
"""
import math
import os
import sys

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
import cadquery as cq  # noqa: E402
from fdm_samples import (Part, SAMPLES, CH, CH_BED, OFF,  # noqa: E402
                         rrect, rx, feet, plane_yz)

W, D, H, R = 112.0, 64.0, 40.0, 8.0     # 14 x 8 x 5 modules
L = 84.0                                # slot and horn length: phones up to about 80 wide in a case
SW = 14.0                               # slot: horizontal width (a phone up to about 13 thick in a case)
SLOPE = 0.25                            # 1 : 4 back lean
YF = -10.0                              # slot's front line at the top
SLOT_D = 10.0                           # front wall of the slot: depth down to the 45-deg floor
THROAT = 6.0                            # throat: horizontal width from the back wall (a speaker up to 6 from the back)
ZR = 15.0                               # throat's bottom = the horn's roof at the back
MOUTH_H = 12.0                          # mouth height at the front face
TONGUE = 0.6                            # the horn's floor (the solid under the throat): 0.6 horizontal per 1 down (59 deg)
A = math.atan(SLOPE)
C, S = math.cos(A), math.sin(A)


def y_front(z):
    return YF - (H - z) * SLOPE


def y_back(z):
    return YF + SW - (H - z) * SLOPE


def floor_corner():
    """Where the 45-deg floor (falling back from the front wall at H - SLOT_D) meets the back wall."""
    zv = H - SLOT_D
    yv = y_front(zv)
    # z = zv - (y - yv) and y = y_back(z) = YF + SW - (H - z) * SLOPE
    z = (zv + yv - YF - SW + H * SLOPE) / (1 + SLOPE)
    return y_back(z), z


def phone(t=8.0, w=76.0, h=160.0):
    """The phone as an envelope (it is larger than the block): back 0.2 off the back wall, front corner 0.2 above the floor."""
    zv = H - SLOT_D
    yv = y_front(zv)
    gap = 0.2
    # back-bottom corner B on the back wall (moved 0.2 forward); front-bottom corner F = B + t * (-C, S) on the floor (+0.2)
    # B = (y_back(zb) - gap / C, zb); F.z = zv - (F.y - yv) + gap
    zb = (zv + gap - (YF + SW - H * SLOPE - gap / C - t * C) + yv - t * S) / (1 + SLOPE)
    b = (y_back(zb) - gap / C, zb)
    f = (b[0] - t * C, b[1] + t * S)
    pts = [b, f, (f[0] + h * S, f[1] + h * C), (b[0] + h * S, b[1] + h * C)]
    return plane_yz(-w / 2).polyline(pts).close().extrude(w)


def phone_horn_amplifier():
    b = rrect(W, D, R, 0, H).faces(">Z").chamfer(CH_BED).faces("<Z").chamfer(CH)
    zv = H - SLOT_D
    yv = y_front(zv)
    yc, zc = floor_corner()
    up = 2.0
    slot = [(y_front(H + up), H + up), (yv, zv), (yc, zc), (y_back(H + up), H + up)]
    b = b.cut(plane_yz(-L / 2).polyline(slot).close().extrude(L))
    yt = y_back(ZR)                                              # throat's back at the bottom
    throat = [(y_back(H + up), H + up), (y_back(H + up) - THROAT, H + up), (yt - THROAT, ZR - 0.01), (yt, ZR - 0.01)]
    b = b.cut(plane_yz(-L / 2).polyline(throat).close().extrude(L))
    horn = [(-D / 2 - 1, -1), (-D / 2 - 1, MOUTH_H), (yt - THROAT, ZR), (yt, ZR), (yt - (ZR + 1) * TONGUE, -1)]
    b = b.cut(plane_yz(-L / 2).polyline(horn).close().extrude(L))
    b = b.faces(">Z").edges(cq.selectors.BoxSelector((-L / 2 - 0.1, -D / 2, H - 0.1), (L / 2 + 0.1, D / 2, H + 0.1))).chamfer(CH)
    b = b.edges(cq.selectors.BoxSelector((-L / 2 - 0.1, -D / 2 - 0.05, CH + 0.05), (L / 2 + 0.1, -D / 2 + 0.05, MOUTH_H + 0.1))).chamfer(CH)
    b = feet(b, [(sx * 49.0, sy * 22.0) for sx in (-1, 1) for sy in (-1, 1)])
    return {"horn": Part(b, rx(b, 180), OFF)}


SAMPLES["059_phone_horn_amplifier"] = phone_horn_amplifier
