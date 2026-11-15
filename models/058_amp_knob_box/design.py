"""058 Amp knob box: a 96 x 72 x 44.8 headphone-amplifier box with one volume knob on the front.

The body (floor and four walls) is printed floor down; the only feature on its front is the knob, centred on the face with the
same 8 margin below it and above it to the seam. The knob turns a 16 mm potentiometer (M7 bushing) that clamps against a boss
behind the front wall; its nut sits in a recess in the front face, under the knob. The cover is a 4.8 plate held by four 6 x 3
magnets in posts in the body's corners, and located by a lip that drops 2.4 inside the walls. The amplifier board stands on four
posts on the floor, its holes on their pins. The back carries three panel jacks in a row: power, input, headphones, and a shallow scoop under the cover's edge for a
fingertip.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK, ACC,  # noqa: E402
                         box, cyl, rrect, rx, feet, plane_xz, knob_local)

W, D, R = 96.0, 72.0, 8.0                 # 12 x 9 modules
HB, CT = 40.0, 4.8                        # body height, cover thickness
FLOOR = 2.4
KNOB_R, KNOB_H, KNOB_GAP = 12.0, 12.0, 0.4
KNOB_Z = HB / 2                           # 8 below the knob and 8 above it to the seam
BOSS = (10.0, 2.6)                        # boss behind the front wall: radius, depth
NUT_R = 6.2
POT = (8.0, 7.0, 7.0, 15.0)               # 16 mm pot: body radius, body depth, bushing length, shaft length (from the mounting face)
POST = 8.0                                # corner posts for the magnets
MAG_D, MAG_H = 6.2, 3.2
LIP = (DIV, 2.4)                          # cover lip: width, depth
BOARD = (50.0, 40.0, 1.6, 12.0)           # amplifier board: w, d, t, tallest part
BOARD_Y = 0.0                             # centred: clear of the jacks' bodies behind the back wall
JACK_DEPTH = 14.0                         # panel jacks reach 14 in from the back wall
STAND = 3.6
PINS = [(sx * 22.0, BOARD_Y + sy * 17.0) for sx in (-1, 1) for sy in (-1, 1)]
SCOOP = (12.0, 9.0)                       # finger scoop in the back wall's top: radius, centre above the seam (3 deep, 16 wide)
JACKS = [(-24.0, 4.1), (0.0, 3.1), (24.0, 3.1)]   # back: power (M8 panel jack), input and headphones (M6), at the knob's height


def teardrop_y(y0, length, x, z, r):
    """Horizontal round hole along -Y from y0 with a 45-deg roof (apex up)."""
    k = 0.70710678
    c = plane_xz(y0).center(x, z).circle(r).extrude(length)
    return c.union(plane_xz(y0).polyline([(x - r * k, z + r * k), (x, z + r * 1.41421356), (x + r * k, z + r * k), (x, z)])
                   .close().extrude(length))


def amp_knob_box():
    yf = -D / 2                                                # front face
    y_mount = yf + T + BOSS[1]                                 # pot mounting face
    body = rrect(W, D, R, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    body = body.cut(rrect(W - 2 * T, D - 2 * T, R - T, FLOOR, HB + 1))
    px, py = W / 2 - T - POST / 2, D / 2 - T - POST / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            post = box(sx * px - POST / 2, sx * px + POST / 2, sy * py - POST / 2, sy * py + POST / 2, FLOOR - 0.1, HB)
            body = body.union(post.intersect(rrect(W - 0.1, D - 0.1, R, 0, HB)))
            body = body.cut(cyl(MAG_D / 2, HB - MAG_H, MAG_H + 1, sx * px, sy * py))
    body = body.union(plane_xz(yf + T - 0.01).center(0, KNOB_Z).circle(BOSS[0]).extrude(-(BOSS[1] + 0.01)))
    body = body.cut(teardrop_y(y_mount + 1, T + BOSS[1] + 2, 0, KNOB_Z, 3.6))           # M7 bushing
    body = body.cut(teardrop_y(yf + 2.4, 3.4, 0, KNOB_Z, NUT_R))                         # nut recess, under the knob
    for (x, r) in JACKS:
        body = body.cut(teardrop_y(D / 2 + 1, T + 2, x, KNOB_Z, r))
    body = body.cut(plane_xz(D / 2 + 1).center(0, HB + SCOOP[1]).circle(SCOOP[0]).extrude(T + 2))   # finger scoop under the cover
    body = body.edges(cq.selectors.BoxSelector((-9, D / 2 - T - 0.05, HB - 3.5), (9, D / 2 + 0.05, HB - 0.6))).chamfer(CH)
    for (x, y) in PINS:
        body = body.union(cyl(3.0, FLOOR - 0.01, STAND + 0.01, x, y).faces(">Z").chamfer(CH * 0.6))
        body = body.union(cyl(1.4, FLOOR + STAND - 0.01, 2.0, x, y).faces(">Z").chamfer(0.3))
    body = feet(body, [(sx * 36.0, sy * 24.0) for sx in (-1, 1) for sy in (-1, 1)])

    cov = rrect(W, D, R, HB, CT).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    lw, ld, lr = W - 2 * (T + GAP), D - 2 * (T + GAP), R - T - GAP
    lip = rrect(lw, ld, lr, HB - LIP[1], LIP[1] + 0.01).cut(rrect(lw - 2 * LIP[0], ld - 2 * LIP[0], lr - LIP[0], 0, 100))
    for sx in (-1, 1):
        for sy in (-1, 1):                                     # the lip stops short of the corner posts
            x0, x1 = sorted((sx * (px - POST / 2 - GAP), sx * W))
            y0, y1 = sorted((sy * (py - POST / 2 - GAP), sy * D))
            lip = lip.cut(box(x0, x1, y0, y1, 0, 100))
    cov = cov.union(lip.faces("<Z").chamfer(CH * 0.6))
    for sx in (-1, 1):
        for sy in (-1, 1):
            cov = cov.cut(cyl(MAG_D / 2, HB - 0.01, MAG_H + 0.01, sx * px, sy * py))

    mags = None
    for sx in (-1, 1):
        for sy in (-1, 1):
            for z0 in (HB - MAG_H, HB):
                mg = cyl(3.0, z0 + 0.05, 3.0 - 0.1, sx * px, sy * py)
                mags = mg if mags is None else mags.union(mg)
    zb = FLOOR + STAND
    brd = box(-BOARD[0] / 2, BOARD[0] / 2, BOARD_Y - BOARD[1] / 2, BOARD_Y + BOARD[1] / 2, zb, zb + BOARD[2])
    for (x, y) in PINS:
        brd = brd.cut(cyl(1.6, zb - 1, 4, x, y))
    brd = brd.union(box(-BOARD[0] / 2 + 6, BOARD[0] / 2 - 6, BOARD_Y - BOARD[1] / 2 + 6, BOARD_Y + BOARD[1] / 2 - 6,
                        zb + BOARD[2] - 0.01, zb + BOARD[2] + BOARD[3]))
    pot = plane_xz(y_mount + POT[1]).center(0, KNOB_Z).circle(POT[0]).extrude(POT[1])
    pot = pot.union(plane_xz(y_mount + 0.01).center(0, KNOB_Z).circle(3.5).extrude(POT[2]))
    pot = pot.union(plane_xz(yf + 2.4).center(0, KNOB_Z).circle(5.75).extrude(2.0))       # nut
    shaft = plane_xz(y_mount - POT[2] + 0.01).center(0, KNOB_Z).circle(3.0).extrude(POT[3] - POT[2])
    pot = pot.union(shaft.intersect(box(-4, 1.5, -100, 0, 0, 100)))

    jacks = None
    for (x, r) in JACKS:
        j = plane_xz(D / 2 - T + 0.01).center(x, KNOB_Z).circle(r - 0.1).extrude(-T + 0.02)
        j = j.union(plane_xz(D / 2 - T).center(x, KNOB_Z).circle(r + 1.0).extrude(JACK_DEPTH))
        jacks = j if jacks is None else jacks.union(j)

    k = knob_local(KNOB_R, KNOB_H, 8.4, (3.6, 7.6), 32, KNOB_H - 4.0)
    k = k.cut(cyl(4.0, KNOB_H - 2.0, 3.0))                     # room for the bushing's end above the nut
    k = k.cut(cq.Workplane("XY").add(cq.Solid.makeCone(3.05, 4.0, 0.95, pnt=cq.Vector(0, 0, KNOB_H - 2.95))))
    knob_asm = rx(k, -90).translate((0, yf - KNOB_GAP - KNOB_H, KNOB_Z))
    return {
        "body": Part(body, body, OFF),
        "cover": Part(cov, rx(cov, 180), OFF),
        "knob": Part(knob_asm, rx(k, 180), OFF),
        "magnet_ref": Part(mags, None, ACC, qty=8, ref=True),
        "board_ref": Part(brd, None, DARK, ref=True),
        "pot_ref": Part(pot, None, DARK, ref=True),
        "jacks_ref": Part(jacks, None, DARK, qty=3, ref=True),
    }


SAMPLES["058_amp_knob_box"] = amp_knob_box
