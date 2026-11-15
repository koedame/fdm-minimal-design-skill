"""030 Pi Zero case: a 72 x 40 x 16 case for a Raspberry Pi Zero-size board, closed by a sliding lid.

The lid runs in the 45-deg dovetail of 08 on three sides of the top and slides out through the right
end, where a low ridge on the end wall clicks into a groove under it. The lid rests on a narrow ring
with a 45-deg underside. The board's mini HDMI and two micro USB receptacles look out through stadium
windows in the front, its microSD slot through the left end; the board sits 0.25 behind both walls,
which are thinned to 1.68 from the inside along the board, so each receptacle face is within 2 of the
outside. Four M2.5 self-tapping screws hold the board on posts. A field of holes over the board lets
the warm air out through the lid.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, cyl, rrect, plane_yz, plane_xz, stadium_x)

# board (Raspberry Pi Zero / Zero W / Zero 2 W, no GPIO header; check yours)
BL, BW, PCB = 65.0, 30.0, 1.4
HOLES = [(3.5, 3.5), (61.5, 3.5), (3.5, 26.5), (61.5, 26.5)]   # from the board's front-left corner
PORTS = [(12.4, 11.2, 3.3), (41.4, 7.5, 2.6), (54.0, 7.5, 2.6)]  # front edge: x, width, height (mini HDMI, USB, power)
SD_Y, SD = 16.9, (11.0, 1.4)      # microSD on the left end: centre from the front edge; card width, socket height
PORT_CL = 0.4                     # window clearance per side around a receptacle

L, W, H, R = 72.0, 40.0, 16.0, 5.0   # 9 : 5; R = 12.5 % of 40. W: the board passes the dovetail lips (32.6 open)
FLOOR = 2.4
POST, POST_H, PILOT = 6.0, 3.0, 2.2  # posts Ø6 x 3, pilot hole for M2.5 x 5 self-tapping screws, 4.6 deep
LIP = 1.2                         # the wall top steps 1.2 inward: the dovetail's upper half (as 08)
ZL0, DT = H - 3.6, 1.2            # lid bottom, dovetail height (45 deg, 1.2 out); the lid is 3.6 thick
ZD = ZL0 + DT
SLOPE_GAP = GAP * 2 ** 0.5
XO = L / 2 + 20                   # the lid and its clearance run out past the right end
RIDGE_H = 0.4
RING = 1.6                        # lid seat inside the walls; its tip is 0.45 over the mini HDMI
X0 = -L / 2 + DIV + GAP           # board's left edge: 0.25 behind the thinned left wall
Y0 = -W / 2 + DIV + GAP           # board's front edge: 0.25 behind the thinned front wall
ZB = FLOOR + POST_H               # board underside
ZT = ZB + PCB                     # board top
HOLE_D, HOLE_P = 2.4, 4.0         # vent field in the lid: 9 x 3 holes at pitch 4


def outline_wire(w, d, r, z):
    return rrect(w, d, r, z, 1.0).faces("<Z").wires().val()


def lid_plan(off, z0, h):
    """Lid outline grown by off: left end in the case, right end past the case."""
    x0 = -(L / 2 - T - LIP - GAP) - off
    w = W - 2 * (T + LIP + GAP) + 2 * off
    return rrect(XO - x0, w, R - T - LIP - GAP + off, z0, h, (XO + x0) / 2, 0)


def wire(off, z):
    return lid_plan(off, z, 1.0).faces("<Z").wires().val()


def loft(off0, z0, off1, z1):
    return cq.Workplane("XY").add(cq.Solid.makeLoft([wire(off0, z0), wire(off1, z1)], True))


def stadium_y(y0, length, xc, zc, w, h):
    """Horizontal stadium hole through a wall normal to Y, from y0 toward -Y."""
    return plane_xz(y0).center(xc, zc).slot2D(w, h, 0).extrude(length)


def prism_y(x, z, pts, length):
    """45-deg prism along Y: pts in local (x, z) around (x, z)."""
    return plane_xz(length / 2).polyline([(x + a, z + b) for a, b in pts]).close().extrude(length)


def pi_zero_case():
    outline = rrect(L, W, R, -1, H + 2)
    body = rrect(L, W, R, 0, H)
    body = body.cut(rrect(L - 2 * T, W - 2 * T, R - T, FLOOR, ZL0 - FLOOR))
    clear = lid_plan(GAP, ZD + 0.1, H + 1 - ZD).union(loft(DT + SLOPE_GAP + GAP, ZL0 - GAP, GAP, ZD + 0.1))
    body = body.cut(clear)
    z1 = ZL0 - GAP                    # the lid rests on a ring with a 45-deg underside
    ring = rrect(L - 2 * T, W - 2 * T, R - T, z1 - RING, RING)
    cone = cq.Solid.makeLoft([outline_wire(L - 2 * T + 0.02, W - 2 * T + 0.02, R - T, z1 - RING - 0.001),
                              outline_wire(L - 2 * T - 2 * RING, W - 2 * T - 2 * RING, R - T - RING, z1 + 0.001)], True)
    body = body.union(ring.cut(cq.Workplane("XY").add(cone)))
    # the front and left walls thinned to DIV along the board, up to the ring
    band = z1 - RING
    body = body.cut(box(X0 - GAP, X0 + BL + 1.0, -W / 2 + DIV, -W / 2 + T + 0.01, FLOOR, band))
    body = body.cut(box(-L / 2 + DIV, -L / 2 + T + 0.01, Y0 - GAP, Y0 + BW + 1.0, FLOOR, band))
    body = body.cut(box(X0 - GAP, X0 + R, Y0 - GAP, Y0 + R, FLOOR, band))            # and the inside corner between them
    body = body.faces("<Z").edges().chamfer(CH_BED)
    body = body.edges(cq.selectors.BoxSelector((-L, -W, H - 0.01), (L, W, H + 0.01))).chamfer(CH)
    for x, w, h in PORTS:
        body = body.cut(stadium_y(-W / 2 + T + 1, T + 2, X0 + x, ZT + h / 2, w + 2 * PORT_CL, h + 2 * PORT_CL))
    body = body.cut(stadium_x(-L / 2 - 1, T + 2, Y0 + SD_Y, ZT + SD[1] / 2, SD[0] + 2 * PORT_CL, SD[1] + 2 * PORT_CL))
    for hx, hy in HOLES:
        body = body.union(cyl(POST / 2, FLOOR - 0.01, POST_H + 0.01, X0 + hx, Y0 + hy))
        body = body.cut(cyl(PILOT / 2, FLOOR - 1.6, POST_H + 2.6, X0 + hx, Y0 + hy))
    xr = L / 2 - T / 2                # detent ridge across the right end wall
    ridge = prism_y(xr, z1 - 0.01, [(-RIDGE_H, 0), (RIDGE_H, 0), (0, RIDGE_H + 0.01)], 20.0)
    body = body.union(ridge)

    lid = lid_plan(0, ZD, H - ZD).union(loft(DT, ZL0, 0, ZD)).intersect(outline)
    lid = lid.faces("<Z").edges().chamfer(CH_BED)
    lid = lid.faces(">Z").edges().chamfer(CH)
    lid = lid.cut(prism_y(xr, ZL0 - 0.01, [(-0.8, 0), (0.8, 0), (0, 0.81)], 21.0))
    lid = lid.cut(rrect(8.0, 20.0, 4.0 - 0.001, H - 1.2, 2.0, L / 2 - 10.0, 0))     # thumb dent near the open end
    xc, yc = (-(L / 2 - T - LIP - GAP) + L / 2 - 14.0) / 2, 0   # centred between the lid's end and the dent
    for i in range(-4, 5):
        for j in range(-1, 2):
            lid = lid.cut(cyl(HOLE_D / 2, ZL0 - 1, H, xc + i * HOLE_P, yc + j * HOLE_P))

    board = box(X0, X0 + BL, Y0, Y0 + BW, ZB, ZT)
    for hx, hy in HOLES:
        board = board.cut(cyl(1.375, ZB - 1, PCB + 2, X0 + hx, Y0 + hy))
    for x, w, h in PORTS:
        board = board.union(box(X0 + x - w / 2, X0 + x + w / 2, Y0, Y0 + 7.5, ZT - 0.01, ZT + h))
    board = board.union(box(X0, X0 + 12.0, Y0 + SD_Y - 6.5, Y0 + SD_Y + 6.5, ZT - 0.01, ZT + SD[1]))
    return {
        "body": Part(body, body, OFF),
        "lid": Part(lid, lid, OFF),
        "board_ref": Part(board, None, DARK, ref=True),
    }


SAMPLES["030_pi_zero_case"] = pi_zero_case
