"""032 Slim tube lamp: a translucent tube 40 across and 160 tall on a low disc, lit by two runs of 5 V LED
strip on a flat spine down its axis and powered through a USB-C receptacle in the back of the disc.

The disc is printed bottom down. A lip ring on its top locates the tube; inside the ring a pocket holds a
boss with a slot for the spine. The USB-C breakout board lies in a channel that runs from the pocket to
the back wall; the channel has a 45-deg gabled roof, so it prints inside the disc without support. The
board slides out over a small ridge that keeps a plug's push from moving it back; its receptacle sits 0.25 behind the wall, thinned to 1.68 there, so a plug seats fully. The cap,
printed top face down, locates on the tube with the same lip and holds the top of the spine in a socket.
"""
import os
import sys

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, cyl, rx, feet, plane_xz, plane_yz)

D = 40.0                    # tube
HT = 4 * D                  # 160: the tube is four diameters
DB = 64.0                   # disc: the tube plus a rim of 12 (three modules) all round
HB = 16.0                   # disc height = cap height; total 16 + 160 + 16 = 192 = 3 x 64
HC = HB
FLOOR = 2.4
LIP_H = 4.0
R_LIP = D / 2 - DIV - GAP   # 18.07: the lip ring's outside, 0.25 inside the tube wall
SPINE_W, SPINE_T = 12.0, 3.36
SOCKET = 8.0                # depth of the spine in the cap
Z0 = HB                     # tube bottom
Z1 = HB + HT                # tube top
DIF = (0.99, 0.94, 0.80)    # translucent white, shown lit

# USB-C power breakout (a generic 5 V board with the CC resistors; check yours)
BRD = (10.0, 12.0, 1.0)     # width, length, thickness
RCP = (8.94, 7.35, 3.26)    # receptacle width, depth, height, flush with the board's end
RIDGE = 0.6                 # detent ridge in the channel: the plug's push cannot move the board back
WIN_CL = 0.4                # window clearance per side around the receptacle


def lip(z0, h):
    return cyl(R_LIP, z0, h).cut(cyl(R_LIP - DIV, z0 - 1, h + 2))


def tube_lamp_slim():
    # disc
    base = cyl(DB / 2, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    pocket_r = R_LIP - DIV
    base = base.cut(cyl(pocket_r, FLOOR, HB + 1))
    base = base.union(lip(HB - 0.01, LIP_H + 0.01))
    base = base.union(cyl(8.0, FLOOR - 0.01, HB + LIP_H - FLOOR + 0.01))          # spine boss
    base = base.cut(box(-SPINE_W / 2 - GAP, SPINE_W / 2 + GAP, -SPINE_T / 2 - GAP, SPINE_T / 2 + GAP, 6.0, HB + LIP_H + 1))
    # board channel toward the back (+Y): rectangle with a 45-deg gabled roof, from the pocket to the thinned wall
    y_wall = DB / 2 - DIV                                    # inner face of the thinned wall
    hw = BRD[0] / 2 + GAP
    z_top = FLOOR + BRD[2] + RCP[2] + 1.0                    # room for the board to ride over the ridge
    prof = [(-hw, FLOOR), (hw, FLOOR), (hw, z_top), (0, z_top + hw), (-hw, z_top)]
    base = base.cut(plane_xz(y_wall).polyline(prof).close().extrude(y_wall - pocket_r + 1))
    zc = FLOOR + BRD[2] + RCP[2] / 2
    base = base.cut(plane_xz(y_wall - 1).center(0, zc).slot2D(RCP[0] + 2 * WIN_CL, RCP[2] + 2 * WIN_CL, 0).extrude(-(DIV + 3)))
    # detent ridge behind the board: 45-deg ramp toward the pocket, a vertical face against the board's rear edge
    yb1 = y_wall - GAP                                       # receptacle face, 0.25 behind the wall
    yr = yb1 - BRD[1] - 0.1
    base = base.union(plane_yz(-hw).polyline([(yr - RIDGE, FLOOR - 0.01), (yr, FLOOR - 0.01), (yr, FLOOR + RIDGE)])
                      .close().extrude(2 * hw))
    base = feet(base, [(sx * 16, sy * 16) for sx in (-1, 1) for sy in (-1, 1)])

    # tube
    tube = cyl(D / 2, Z0, HT).cut(cyl(D / 2 - DIV, Z0 - 1, HT + 2))
    tube = tube.faces("<Z").edges().chamfer(CH).faces(">Z").edges().chamfer(CH)

    # cap: open below, lip into the tube, socket boss for the spine
    cap = cyl(D / 2, Z1, HC).cut(cyl(D / 2 - T, Z1 - 1, HC - FLOOR + 1))
    cap = cap.faces("<Z").edges().chamfer(CH).faces(">Z").edges().chamfer(CH_BED)
    cap = cap.union(lip(Z1 - LIP_H, LIP_H + 0.01))
    z_boss = Z1 + 4.0                                        # socket bottom 8 below the cap's inner top
    cap = cap.union(cyl(5.0, z_boss, Z1 + HC - FLOOR - z_boss + 0.01).union(
        box(-SPINE_W / 2 - GAP - DIV, SPINE_W / 2 + GAP + DIV, -SPINE_T / 2 - GAP - DIV, SPINE_T / 2 + GAP + DIV,
            z_boss, Z1 + HC - FLOOR + 0.01)))
    cap = cap.cut(box(-SPINE_W / 2 - GAP, SPINE_W / 2 + GAP, -SPINE_T / 2 - GAP, SPINE_T / 2 + GAP, z_boss - 1, z_boss + SOCKET))

    # spine: a flat bar from the boss to the cap's socket
    s0, s1 = 6.0 + GAP, z_boss + SOCKET - GAP
    spine = box(-SPINE_W / 2, SPINE_W / 2, -SPINE_T / 2, SPINE_T / 2, s0, s1).edges("|Z").chamfer(CH)

    strips = None
    for sy in (-1, 1):
        y0 = sy * SPINE_T / 2
        st = box(-4.0, 4.0, min(y0, y0 + sy * 1.0), max(y0, y0 + sy * 1.0), Z0 + LIP_H + 2, Z1 - 4)
        strips = st if strips is None else strips.union(st)

    board = box(-BRD[0] / 2, BRD[0] / 2, yb1 - BRD[1], yb1, FLOOR, FLOOR + BRD[2])
    board = board.union(box(-RCP[0] / 2, RCP[0] / 2, yb1 - RCP[1], yb1, FLOOR + BRD[2] - 0.01, FLOOR + BRD[2] + RCP[2]))
    spine_prn = spine.rotate((0, 0, 0), (1, 0, 0), 90)
    return {
        "base": Part(base, base, OFF),
        "tube": Part(tube, tube, DIF),
        "cap": Part(cap, rx(cap, 180), OFF),
        "spine": Part(spine, spine_prn, OFF),
        "led_strips_ref": Part(strips, None, DARK, ref=True),
        "usb_board_ref": Part(board, None, DARK, ref=True),
    }


SAMPLES["032_tube_lamp_slim"] = tube_lamp_slim
