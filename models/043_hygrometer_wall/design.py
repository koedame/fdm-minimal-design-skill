"""043 Wall hygrometer frame: a 64 x 96 frame for a small digital thermo-hygrometer, a window over its display.

The housing is a shallow sleeve printed face down: the window opening and a field of eleven vertical
slots (air for the sensor) go through the face, and the back steps in 1.2 on a 45-deg face, so it
stands off the wall on a shadow line. A smoked window with a flange fits the opening from behind. The
back plate hangs on two screws through keyholes; a DIV lip round its edge locates the housing over it,
and a frame on it holds the bought thermo-hygrometer against the window's flange.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, cyl, rrect, rx, keyhole_local, plane_xz)

W, H, DEP, R = 64.0, 96.0, 24.0, 8.0     # 2 : 3; R = 12.5 % of the width
FRONT = PB = 2.4                         # face plate; back plate
INSET = 1.2                              # shadow line at the wall
M = 11.2                                 # every margin on the face: sides, top, between window and slots, bottom
FIELD = 41.6                             # window width = slot field width: 11 slots at pitch 4, 1.6 wide
WH = 24.0                                # window height
SL = H - 3 * M - WH                      # 38.4: slot length
SLOT_W, PITCH, N = 1.6, 4.0, 11
WY = H / 2 - M - WH / 2                  # window centre
SY = -H / 2 + M + SL / 2                 # slot field centre
FL = 3.0                                 # window flange beyond the opening
DEV = (48.0, 28.6, 15.2)                 # a common small LCD thermo-hygrometer (check yours)
LIP = 6.0                                # back plate lip depth
KEY_X, KEY_Y, TRAVEL = 16.0, -12.0, 6.0  # two keyholes under the device
BOSS = 6.4                               # back plate thickness at the keyholes: ledge 2 + pocket 3 + 1.4
HOOK_Y, HOOK_Z = 5.0, 18.0               # snap hooks: half width, top
BARB = (14.0, 0.8)                       # barb: bottom, height (45-deg faces above and below)


def hygrometer_wall():
    # local frame: the wall at z = 0, the face at z = DEP, y up; disp() stands it on the wall (face toward -Y)
    hs = rrect(W - 2 * INSET, H - 2 * INSET, R - INSET, 0, INSET + 0.01)
    hs = hs.union(rrect(W, H, R, INSET, DEP - INSET).faces("<Z").chamfer(INSET)).faces(">Z").chamfer(CH_BED)
    hs = hs.cut(rrect(W - 2 * T, H - 2 * T, R - T, -1, DEP - FRONT + 1))
    hs = hs.cut(rrect(FIELD, WH, 2.0, DEP - FRONT - 1, FRONT + 2, 0, WY))
    for i in range(N):
        x = -FIELD / 2 + SLOT_W / 2 + i * PITCH
        hs = hs.cut(cq.Workplane("XY").workplane(offset=DEP - FRONT - 1).center(x, SY)
                    .slot2D(SL, SLOT_W, 90).extrude(FRONT + 2))
    xi = W / 2 - T                                            # housing inner wall
    b0, bh = BARB
    for s in (-1, 1):                                         # grooves for the hooks' barbs: barb + 0.25 all round
        g = plane_xz(-HOOK_Y - 1).polyline([(s * (xi - 0.01), b0 - 0.35), (s * (xi + bh), b0 - 0.35 + bh + 0.01),
                                             (s * (xi + bh), b0 + 2.2 + 0.35 - 0.01), (s * (xi - 0.01), b0 + 3.0 + 0.35)])
        hs = hs.cut(g.close().extrude(-2 * (HOOK_Y + 1)))

    win = rrect(FIELD - 2 * GAP, WH - 2 * GAP, 2.0 - GAP, DEP - FRONT, FRONT).faces(">Z").chamfer(CH)
    win = win.union(rrect(FIELD + 2 * FL, WH + 2 * FL, 2.0 + FL, DEP - FRONT - 1.2, 1.2)).translate((0, WY, 0))

    pw, ph, pr = W - 2 * T - 2 * GAP, H - 2 * T - 2 * GAP, R - T - GAP
    bp = rrect(pw, ph, pr, 0, PB).faces("<Z").chamfer(CH_BED)
    bp = bp.union(rrect(pw, ph, pr, PB - 0.01, LIP + 0.01).cut(rrect(pw - 2 * DIV, ph - 2 * DIV, pr - DIV, 0, 20))
                  .faces(">Z").chamfer(CH))
    dz0 = DEP - FRONT - 1.2 - DEV[2]                          # back of the device: pressed onto the window flange
    dw, dh = DEV[0] + 2 * GAP, DEV[1] + 2 * GAP
    ring = (box(-dw / 2 - DIV, dw / 2 + DIV, -dh / 2 - DIV, dh / 2 + DIV, PB - 0.01, dz0 + 4)
            .cut(box(-dw / 2, dw / 2, -dh / 2, dh / 2, 0, 30)).faces(">Z").chamfer(CH * 0.6))
    bp = bp.union(ring.translate((0, WY, 0)))
    for sx in (-1, 1):
        for sy in (-1, 1):                                    # pads under the device's corners
            bp = bp.union(cyl(3.0, PB - 0.01, dz0 - PB + 0.01, sx * 18, WY + sy * 8))
    xo = pw / 2                                               # lip outer face = hook outer face
    for s in (-1, 1):                                         # a hook rises out of each long side of the lip, slit free
        x0, x1 = sorted((s * (xo - DIV), s * (xo + 1)))
        bp = bp.cut(box(x0, x1, -HOOK_Y - 1, HOOK_Y + 1, PB, LIP + 1))
        x0, x1 = sorted((s * (xo - DIV), s * xo))
        bp = bp.union(box(x0, x1, -HOOK_Y, HOOK_Y, PB - 0.01, HOOK_Z).faces(">Z").chamfer(CH))
        barb = plane_xz(-HOOK_Y).polyline([(s * (xo - 0.01), b0), (s * (xo + bh), b0 + bh), (s * (xo + bh), b0 + 2.2),
                                           (s * (xo - 0.01), b0 + 3.0)]).close().extrude(-2 * HOOK_Y)
        bp = bp.union(barb)
    for sx in (-1, 1):
        x = sx * KEY_X
        bp = bp.union(rrect(14, 24, 3.0, PB - 0.01, BOSS - PB + 0.01, x, KEY_Y + 4).faces(">Z").chamfer(CH))
        bp = bp.cut(keyhole_local(TRAVEL).translate((x, KEY_Y, 0)))

    dev = box(-DEV[0] / 2, DEV[0] / 2, WY - DEV[1] / 2, WY + DEV[1] / 2, dz0, dz0 + DEV[2])
    disp = lambda wp: rx(wp, 90)                              # noqa: E731
    return {
        "housing": Part(disp(hs), rx(hs, 180), OFF),
        "window_smoke": Part(disp(win), rx(win, 180), DARK),
        "back_plate": Part(disp(bp), bp, OFF),
        "hygrometer_ref": Part(disp(dev), None, DARK, ref=True),
    }


SAMPLES["043_hygrometer_wall"] = hygrometer_wall
