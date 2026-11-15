"""016 USB hub case: an 84 x 40 x 20 case for a bare 4-port USB hub board, closed by screws from below.

The body is a sleeve with a top, printed top face down, so the four bosses that hang from the top stand
up in the print. Four M2 screws come up through counterbores in the bottom plate, through standoffs and
the board's corner holes, into the bosses: the board is clamped between them and no screw shows. The
ports look out through windows in the front, the USB-C input through a stadium at the end.
"""
import os
import sys

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, cyl, rrect, rx, feet, stadium_x, plane_xz)

L, W, H, R = 84.0, 40.0, 20.0, 6.0     # 84: the board corners clear the inside corner radius; height = half the depth; R = 15 % of 40
TOP = BP = 2.4                         # top and bottom plate
STAND = 3.0                            # standoff under the board
# the board (match yours): 72 x 28 x 1.6, M2 holes 3.5 in from the corners, 4 USB-A on the front edge
BL, BD, BT = 72.0, 28.0, 1.6
HOLE_IN = 3.5
PORT_X, PORT = (-22.5, -7.5, 7.5, 22.5), (13.2, 14.0, 5.8)   # the board's port pitch 15; receptacle w x d x h
PORT_CL = 0.4                          # window clearance per side around the receptacle
USBC = (8.9, 7.3, 3.2)                 # input receptacle at the -X end, standing out 1 from the board
BOSS_R, PILOT, CLEAR, CB_D, CB_H = 3.0, 1.8, 2.4, 4.2, 1.8   # M2: pilot, clearance, counterbore


def usb_hub_case():
    yf = -(W / 2 - T) + GAP               # board front edge, 0.25 behind the front wall
    zb = BP + STAND                       # underside of the board
    zt = zb + BT                          # top of the board
    holes = [(sx * (BL / 2 - HOLE_IN), y) for sx in (-1, 1) for y in (yf + HOLE_IN, yf + BD - HOLE_IN)]

    body = rrect(L, W, R, 0, H).faces(">Z").chamfer(CH_BED)
    body = body.cut(rrect(L - 2 * T, W - 2 * T, R - T, -1, H - TOP + 1))
    body = body.faces("<Z").chamfer(CH)    # both edges of the open bottom: half of the V line round the plate
    for (x, y) in holes:
        body = body.union(cyl(BOSS_R, zt + 0.05, H - TOP - zt - 0.04, x, y)).cut(cyl(PILOT / 2, zt, 8, x, y))   # 0.05 over the board: the screw closes it
    zc = zt + PORT[2] / 2
    for x in PORT_X:
        win = plane_xz(-W / 2 + T + 1).center(x, zc).rect(PORT[0] + 2 * PORT_CL, PORT[2] + 2 * PORT_CL).extrude(T + 2)
        body = body.cut(win.edges("|Y").fillet(1.0))
    # the front wall is DIV thick behind the ports, so a plug whose moulding is larger than the window
    # still goes fully in: the receptacle face sits 0.25 + 1.68 = 1.93 behind the outside
    band_top = zt + PORT[2] + PORT_CL + DIV
    body = body.cut(box(PORT_X[0] - PORT[0], PORT_X[-1] + PORT[0], -W / 2 + DIV, -W / 2 + T + 0.01, -1, band_top))
    body = body.cut(stadium_x(-L / 2 - 1, T + 2, yf + BD / 2, zt + USBC[2] / 2, 12.0, 6.4))

    pw, pd = L - 2 * (T + GAP), W - 2 * (T + GAP)
    plate = rrect(pw, pd, R - T - GAP, 0, BP).faces("<Z").chamfer(CH_BED)
    for (x, y) in holes:
        plate = plate.union(cyl(BOSS_R, BP - 0.01, STAND + 0.01, x, y))
        plate = plate.cut(cyl(CLEAR / 2, -1, zb + 2, x, y)).cut(cyl(CB_D / 2, -1, CB_H + 1, x, y))
    plate = feet(plate, [(sx * 20, sy * 10) for sx in (-1, 1) for sy in (-1, 1)])

    board = box(-BL / 2, BL / 2, yf, yf + BD, zb, zt)
    for (x, y) in holes:
        board = board.cut(cyl(1.1, zb - 1, BT + 2, x, y))
    for x in PORT_X:
        board = board.union(box(x - PORT[0] / 2, x + PORT[0] / 2, yf, yf + PORT[1], zt - 0.01, zt + PORT[2]))
    yc = yf + BD / 2
    board = board.union(box(-BL / 2 - 1, -BL / 2 - 1 + USBC[1], yc - USBC[0] / 2, yc + USBC[0] / 2, zt - 0.01, zt + USBC[2]))
    return {
        "body": Part(body, rx(body, 180), OFF),
        "bottom_plate": Part(plate, plate, OFF),
        "hub_board_ref": Part(board, None, DARK, ref=True),
    }


SAMPLES["016_usb_hub_case"] = usb_hub_case
