"""086 Dev board tray: a low tray with an interchangeable deck that holds a single-board computer on four standoffs.

The base is a tray 108 x 80 with a 10 high rim and rubber feet. The deck drops inside the rim and carries the standoffs for the
board (here the 58 x 49 hole pattern of a Raspberry Pi 4 or 5) and two bosses beside its long sides. Two M2 screws come up from the
bottom of the base, through counterbores, into the bosses, so nothing shows from above. A deck for another board fits the same base.
The board sits 2.4 above the rim, so cables reach every connector over it.
"""
import os
import sys

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, CH, CH_BED, GAP, OFF, DARK, box, cyl, rrect, feet  # noqa: E402

L, W, R = 108.0, 80.0, 12.0         # base: 27 x 20 modules, R12 = 11 % of 108
HR, FL = 10.0, 4.0                  # rim height, floor thickness
DT = 2.4                            # deck
BOARD = (85.0, 56.0, 1.6)           # Raspberry Pi 4 / 5
HOLES = (58.0, 49.0)                # its M2.5 hole pattern, centred on the board here (offset 3.5 from the edges)
HOLE_DX = -(BOARD[0] / 2 - 3.5 - HOLES[0] / 2)   # the pattern sits toward one end of the board
SO_D, SO_H = 6.0, 6.0               # standoffs: board bottom 2.4 above the rim
SO_PILOT = 2.2                      # M2.5 self-tapping
BOSS_Y, BOSS_D, BOSS_H = 32.5, 6.0, 4.0   # deck bosses beside the board's long sides, midway between its edge and the rim
PILOT, CLEAR, CB_D, CB_H = 1.8, 2.4, 4.2, 2.0   # M2: pilot, clearance, counterbore


def dev_board_tray():
    base = rrect(L, W, R, 0, HR).faces("<Z").chamfer(CH_BED)
    base = base.cut(rrect(L - 2 * T, W - 2 * T, R - T, FL, HR))
    base = base.faces(">Z").edges().chamfer(CH)
    for sx in (-1, 1):
        base = base.cut(cyl(CB_D / 2, -0.01, CB_H + 0.01, 0, sx * BOSS_Y)).cut(cyl(CLEAR / 2, 0, FL + 1, 0, sx * BOSS_Y))
    base = feet(base, [(sx * 36.0, sy * 28.0) for sx in (-1, 1) for sy in (-1, 1)])

    dl, dw, dr = L - 2 * (T + GAP), W - 2 * (T + GAP), R - T - GAP
    deck = rrect(dl, dw, dr, FL, DT).faces("<Z").chamfer(CH_BED).faces(">Z").edges().chamfer(CH)
    top = FL + DT
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = HOLE_DX + sx * HOLES[0] / 2, sy * HOLES[1] / 2
            so = cyl(SO_D / 2, top - 0.01, SO_H + 0.01, x, y).faces(">Z").chamfer(CH)
            deck = deck.union(so).cut(cyl(SO_PILOT / 2, top + SO_H - 5.0, 6.0, x, y))
        boss = cyl(BOSS_D / 2, top - 0.01, BOSS_H + 0.01, 0, sx * BOSS_Y).faces(">Z").chamfer(CH)
        deck = deck.union(boss).cut(cyl(PILOT / 2, FL - 1, 1 + DT + BOSS_H - 1.0, 0, sx * BOSS_Y))

    zb = top + SO_H
    board = box(-BOARD[0] / 2, BOARD[0] / 2, -BOARD[1] / 2, BOARD[1] / 2, zb, zb + BOARD[2])
    for sx in (-1, 1):
        for sy in (-1, 1):
            board = board.cut(cyl(1.35, zb - 1, 4, HOLE_DX + sx * HOLES[0] / 2, sy * HOLES[1] / 2))
    return {
        "base": Part(base, base, OFF),
        "deck": Part(deck, deck.translate((0, 0, -FL)), DARK),
        "board_ref": Part(board, None, (0.20, 0.45, 0.25), ref=True),
    }


SAMPLES["086_dev_board_tray"] = dev_board_tray
