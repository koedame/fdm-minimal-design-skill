"""044 Four-button control box: a 120 x 48 x 22 desk box with four round buttons in a row.

The shell (top and walls) is one piece printed top down; the only lines on it are the four buttons. A bottom plate closes it and
is held by four M2 screws from below into bosses hanging from the top, so no fastener shows from above or the sides. Each button runs
in a 6 long guide (the top plate and a sleeve under it), so a press near its edge does not tip it. The plate
carries four standoffs whose pins locate a 96 x 32 board with four 12 x 12 tactile switches; each button rests on its switch's
actuator, which traps the board on the pins. The cable leaves through a USB-C opening in the back.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, cyl, rrect, rx, feet, plane_xz, button_local)

BTN_D, PITCH = 16.0, 24.0                 # buttons; pitch = button + 8
M = 16.0                                  # margin from a button's edge to the box's edge, all four sides
W = 3 * PITCH + BTN_D + 2 * M             # 120
D = BTN_D + 2 * M                         # 48
H, R = 22.0, 8.0
PT = PB = 2.4                             # top plate, bottom plate
BOSS = [(sx * 52.0, sy * 16.0) for sx in (-1, 1) for sy in (-1, 1)]   # on the inner corner radii's centres
SPLIT = PB + 3.0                          # where the plate's bosses meet the shell's
PCB = (96.0, 32.0, 1.6)
PCB_Y = 5.0                               # the board's back edge sits 0.48 inside the back wall, at the USB-C opening
STAND = 3.6                               # standoff height: room for the switches' through-hole legs
PIN_XY = [(sx * 44.0, PCB_Y + sy * 12.0) for sx in (-1, 1) for sy in (-1, 1)]
SW = (12.0, 3.5, 4.3)                     # 12 x 12 tactile switch: body height, overall height
GUIDE = 6.0                               # button guide: the top plate and a sleeve under it
FLANGE_R = BTN_D / 2 + 2.0


def button_box_four():
    xs = [PITCH * (i - 1.5) for i in range(4)]
    z_pcb = PB + STAND
    z_act = z_pcb + PCB[2] + SW[2]                                # actuator top: the buttons rest on it
    stem = H - GUIDE - (FLANGE_R - BTN_D / 2) - 1.0 - z_act       # flange bottom to actuator

    sh = rrect(W, D, R, 0, H).faces(">Z").chamfer(CH_BED).faces("<Z").chamfer(CH)
    sh = sh.cut(rrect(W - 2 * T, D - 2 * T, R - T, -1, H - PT + 1))
    for (x, y) in BOSS:
        sh = sh.union(cyl(3.0, SPLIT, H - PT - SPLIT + 0.01, x, y)).cut(cyl(0.9, SPLIT - 1, 8.0, x, y))
    for x in xs:
        sh = sh.union(cyl(BTN_D / 2 + 0.3 + DIV, H - GUIDE, GUIDE - PT + 0.01, x, 0))
        sh = sh.cut(cyl(BTN_D / 2 + 0.3, H - GUIDE - 1, GUIDE + 2, x, 0))
    z_usb = z_pcb + PCB[2] + 1.6
    sh = sh.cut(plane_xz(D / 2 - T - 1).center(0, z_usb).slot2D(9.6, 4.0, 0).extrude(-(T + 2)))

    pw, pd, pr = W - 2 * (T + GAP), D - 2 * (T + GAP), R - T - GAP
    pl = rrect(pw, pd, pr, 0, PB).faces("<Z").chamfer(CH_BED)
    for (x, y) in BOSS:
        pl = pl.union(cyl(3.0, PB - 0.01, SPLIT - PB + 0.01, x, y))
        pl = pl.cut(cyl(1.2, -1, SPLIT + 1, x, y)).cut(cyl(2.2, -1, PB + 1, x, y))
    for (x, y) in PIN_XY:
        pl = pl.union(cyl(3.0, PB - 0.01, STAND + 0.01, x, y).faces(">Z").chamfer(CH))
        pl = pl.union(cyl(1.4, z_pcb - 0.01, 2.0, x, y).faces(">Z").chamfer(0.3))
    pl = feet(pl, [(sx * 36.0, sy * 12.0) for sx in (-1, 1) for sy in (-1, 1)])

    pcb = box(-PCB[0] / 2, PCB[0] / 2, PCB_Y - PCB[1] / 2, PCB_Y + PCB[1] / 2, z_pcb, z_pcb + PCB[2])
    for (x, y) in PIN_XY:
        pcb = pcb.cut(cyl(1.6, z_pcb - 1, 4, x, y))
    for x in xs:
        z1 = z_pcb + PCB[2]
        pcb = pcb.union(box(x - SW[0] / 2, x + SW[0] / 2, -SW[0] / 2, SW[0] / 2, z1 - 0.01, z1 + SW[1]))
        pcb = pcb.union(cyl(2.0, z1 + SW[1] - 0.01, SW[2] - SW[1] + 0.01, x, 0))
    yb = PCB_Y + PCB[1] / 2
    pcb = pcb.union(box(-4.5, 4.5, yb - 7.3, yb, z_pcb + PCB[2] - 0.01, z_pcb + PCB[2] + 3.2))   # USB-C receptacle

    key_l = button_local(BTN_D, 1.2, GUIDE, FLANGE_R, stem_r=1.5, stem_len=stem)
    keys = None
    for x in xs:
        k = rx(key_l, 180).translate((x, 0, H + 1.2))
        keys = k if keys is None else keys.union(k)
    return {
        "shell": Part(sh, rx(sh, 180), OFF),
        "bottom_plate": Part(pl, pl, OFF),
        "button": Part(keys, key_l, DARK, qty=4),
        "board_ref": Part(pcb, None, DARK, ref=True),
    }


SAMPLES["044_button_box_four"] = button_box_four
