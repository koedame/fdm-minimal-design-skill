"""057 Slab timer case: a 92 x 52 x 20 kitchen-timer slab with a four-digit window on the left and one dial on the right.

The shell (top and walls) is one piece printed top down. The window and the dial are the same width (28) and sit 12 in from
the ends, on the slab's centre line. The window is an open cut-out; a 0.36" four-digit LED module is pressed against the top
plate from below by four pads on the bottom plate and located by a frame round the display. The dial turns a 12 mm rotary
encoder (EC11) whose bushing passes through a sleeve under the top plate; its nut sits in a recess in the top face, under
the dial, so nothing but the dial shows. A small controller board (21 x 17.8, USB-C) lies on the bottom plate with its
socket at an opening in the right end; a 12 mm buzzer sounds through three holes in the bottom plate. The bottom plate is
held by two snap hooks rising from its lip; their 45-deg barbs drop into V grooves in the long walls. A coin in the slot at
the left end of the plate pries it out.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, cyl, rrect, rx, feet, plane_xz, plane_yz, knob_local)

W, D, H, R = 92.0, 52.0, 20.0, 8.0
PT = PB = 2.4                             # top plate, bottom plate
M = 12.0                                  # margin: window and dial to the slab's ends
WIN = (28.0, 12.0)                        # window = the digits of a 0.36" module (display 30 x 14)
DIAL_R = WIN[0] / 2                       # dial diameter = window width
WIN_X, DIAL_X = -W / 2 + M + WIN[0] / 2, W / 2 - M - DIAL_R      # -20, +20
DISP = (30.0, 14.0, 7.2)                  # display body
BOARD = (42.0, 24.0, 1.6)                 # module board
KNOB_H, KNOB_GAP = 12.0, 0.4
SLEEVE = (8.0, 2.6)                       # sleeve under the top plate: radius (wider than the nut recess), depth
NUT_R = 6.2                               # recess for the M7 nut (across corners 11.5) in the top face
ENC = (12.0, 6.5, 7.0, 14.5)              # EC11: body side, body height, bushing length, shaft length (all from the mounting face)
CTRL = (21.0, 17.8, 4.4)                  # controller board: 1.2 board + 3.2 USB-C socket on top
CTRL_X, CTRL_Y = W / 2 - T - CTRL[0] / 2 - 0.3, 10.0     # clear of the inner corner radius
BUZ = (6.0, 9.5)                          # 12 mm buzzer: radius, height
BUZ_X, BUZ_Y = DIAL_X, -14.0
LIP = 3.0
HOOK_X, HOOK_W, HOOK_Z = 0.0, 10.0, 12.0  # two hooks at the middle of the long sides
BARB = (8.0, 0.8)                         # barb: bottom, height


def slab_timer_case():
    z_in = H - PT                                              # top plate's underside, 17.6
    z_mount = z_in - SLEEVE[1]                                 # encoder mounting face, 15.0
    sh = rrect(W, D, R, 0, H).faces(">Z").chamfer(CH_BED).faces("<Z").chamfer(CH)
    sh = sh.cut(rrect(W - 2 * T, D - 2 * T, R - T, -1, z_in + 1))
    sh = sh.cut(rrect(WIN[0], WIN[1], 1.2, z_in - 1, PT + 2, WIN_X, 0))
    sh = sh.edges(cq.selectors.BoxSelector((WIN_X - 15, -7, H - 0.05), (WIN_X + 15, 7, H + 0.05))).chamfer(CH)
    dw, dd = DISP[0] + 2 * GAP, DISP[1] + 2 * GAP              # frame round the display, under the top plate
    sh = sh.union(box(WIN_X - dw / 2 - DIV, WIN_X + dw / 2 + DIV, -dd / 2 - DIV, dd / 2 + DIV, z_in - 2.0, z_in + 0.01)
                  .cut(box(WIN_X - dw / 2, WIN_X + dw / 2, -dd / 2, dd / 2, 0, H)).faces("<Z").chamfer(CH * 0.6))
    sh = sh.union(cyl(SLEEVE[0], z_mount, SLEEVE[1] + 0.01, DIAL_X, 0))
    sh = sh.cut(cyl(3.6, z_mount - 1, H, DIAL_X, 0))          # M7 bushing
    sh = sh.cut(cyl(NUT_R, z_in, PT + 1, DIAL_X, 0))           # nut recess, hidden under the dial
    yi = D / 2 - T
    b0, bh = BARB
    for s in (-1, 1):                                          # V grooves for the barbs: barb + 0.25 all round
        g = plane_yz(HOOK_X - HOOK_W / 2 - GAP).polyline([(s * (yi - 0.01), b0 - 0.35), (s * (yi + bh + 0.25), b0 - 0.35 + bh + 0.25),
                                                          (s * (yi + bh + 0.25), b0 + 2.2 + 0.1), (s * (yi - 0.01), b0 + 3.0 + 0.35)])
        sh = sh.cut(g.close().extrude(HOOK_W + 2 * GAP))
    z_usb = PB + 1.2 + 1.6                                     # USB-C centre: socket on top of the 1.2 board
    sh = sh.cut(plane_yz(W / 2 - T - 1).center(CTRL_Y, z_usb).slot2D(9.6, 4.0, 0).extrude(T + 2))

    pw, pd, pr = W - 2 * (T + GAP), D - 2 * (T + GAP), R - T - GAP
    bp = rrect(pw, pd, pr, 0, PB).faces("<Z").chamfer(CH_BED)
    lip = rrect(pw, pd, pr, PB - 0.01, LIP + 0.01).cut(rrect(pw - 2 * DIV, pd - 2 * DIV, pr - DIV, 0, 20))
    lip = lip.cut(box(W / 2 - 20, W / 2, CTRL_Y - CTRL[1] / 2 - 1, CTRL_Y + CTRL[1] / 2 + 1, PB, 20))   # room for the controller board
    bp = bp.union(lip.faces(">Z").chamfer(CH * 0.6))
    xo = pd / 2                                                # lip outer face = hook outer face
    for s in (-1, 1):
        y0, y1 = sorted((s * (xo - DIV), s * (xo + 1)))
        bp = bp.cut(box(HOOK_X - HOOK_W / 2 - 1, HOOK_X + HOOK_W / 2 + 1, y0, y1, PB, LIP + 1))
        y0, y1 = sorted((s * (xo - DIV), s * xo))
        bp = bp.union(box(HOOK_X - HOOK_W / 2, HOOK_X + HOOK_W / 2, y0, y1, PB - 0.01, HOOK_Z).faces(">Z").chamfer(CH))
        barb = plane_yz(HOOK_X - HOOK_W / 2).polyline([(s * (xo - 0.01), b0), (s * (xo + bh), b0 + bh), (s * (xo + bh), b0 + 2.2),
                                                       (s * (xo - 0.01), b0 + 3.0)]).close().extrude(HOOK_W)
        bp = bp.union(barb)
    z_board = z_in - DISP[2] - BOARD[2]                        # 8.8: the module's board, display against the top plate
    for sx in (-1, 1):
        for sy in (-1, 1):                                     # pads under the board's corners
            bp = bp.union(cyl(2.5, PB - 0.01, z_board - PB + 0.01, WIN_X + sx * 18.0, sy * 9.0).faces(">Z").chamfer(CH * 0.6))
    cw, cd = CTRL[0] + 2 * GAP, CTRL[1] + 2 * GAP              # a low frame for the controller board
    bp = bp.union(box(CTRL_X - cw / 2 - DIV, W / 2 - T - GAP, CTRL_Y - cd / 2 - DIV, CTRL_Y + cd / 2, PB - 0.01, PB + 1.6)
                  .cut(box(CTRL_X - cw / 2, CTRL_X + cw / 2 + 1, CTRL_Y - cd / 2, CTRL_Y + cd / 2 + 1, 0, 10)).faces(">Z").chamfer(CH * 0.6))
    bp = bp.union(cyl(BUZ[0] + GAP + DIV, PB - 0.01, 1.6, BUZ_X, BUZ_Y).cut(cyl(BUZ[0] + GAP, 0, 10, BUZ_X, BUZ_Y)))
    for i in (-1, 0, 1):
        bp = bp.cut(cyl(1.0, -1, PB + 2, BUZ_X + i * 3.0, BUZ_Y))
    bp = bp.cut(box(-pw / 2 - 1, -pw / 2 + 1.6, -6.0, 6.0, -1, 1.2))   # coin slot at the left end: pry the plate out
    bp = feet(bp, [(sx * 32.0, sy * 14.0) for sx in (-1, 1) for sy in (-1, 1)])

    mod = box(WIN_X - BOARD[0] / 2, WIN_X + BOARD[0] / 2, -BOARD[1] / 2, BOARD[1] / 2, z_board, z_board + BOARD[2])
    mod = mod.union(box(WIN_X - DISP[0] / 2, WIN_X + DISP[0] / 2, -DISP[1] / 2, DISP[1] / 2, z_board + BOARD[2] - 0.01, z_in))
    e = ENC[0] / 2
    enc = box(DIAL_X - e, DIAL_X + e, -e, e, z_mount - ENC[1], z_mount)
    enc = enc.union(cyl(3.5, z_mount - 0.01, ENC[2], DIAL_X, 0))
    enc = enc.union(cyl(5.75, z_in, 2.0, DIAL_X, 0))                                # nut
    enc = enc.union(cyl(3.0, z_mount + ENC[2] - 0.01, ENC[3] - ENC[2], DIAL_X, 0)
                    .intersect(box(DIAL_X - 4, DIAL_X + 1.5, -4, 4, 0, 40)))       # D shaft
    ctrl = box(CTRL_X - CTRL[0] / 2, CTRL_X + CTRL[0] / 2, CTRL_Y - CTRL[1] / 2, CTRL_Y + CTRL[1] / 2, PB, PB + CTRL[2])
    buz = cyl(BUZ[0], PB, BUZ[1], BUZ_X, BUZ_Y)

    k = knob_local(DIAL_R, KNOB_H, 10.0, (4.0, 9.0), 36, KNOB_H - 4.0)
    k = k.cut(cyl(4.0, KNOB_H - 2.0, 3.0))                     # room for the bushing's top above the nut
    k = k.cut(cq.Workplane("XY").add(cq.Solid.makeCone(3.05, 4.0, 0.95, pnt=cq.Vector(0, 0, KNOB_H - 2.95))))
    knob_asm = rx(k, 180).translate((DIAL_X, 0, H + KNOB_GAP + KNOB_H))
    return {
        "shell": Part(sh, rx(sh, 180), OFF),
        "bottom_plate": Part(bp, bp, OFF),
        "dial": Part(knob_asm, rx(k, 180), OFF),
        "display_ref": Part(mod, None, DARK, ref=True),
        "encoder_ref": Part(enc, None, DARK, ref=True),
        "controller_ref": Part(ctrl, None, DARK, ref=True),
        "buzzer_ref": Part(buz, None, DARK, ref=True),
    }


SAMPLES["057_slab_timer_case"] = slab_timer_case
