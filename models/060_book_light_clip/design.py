"""060 Book light clip: a clip for the top edge of a book cover and a lamp head on a pin hinge that leans over the page.

The body is one profile 30 wide: a U clip (a 3.0 gap with a 45-deg bump on the thin front jaw, for covers about 2.4-3.4 thick)
and a neck rising to two knuckles. The back jaw holds a CR2032 holder with its own switch, pressed in from the back. The head is a
56 long tray on the middle knuckle; at rest it leans forward until its underside lands on the body's front top edge, 29 deg down,
the light pointing down and back toward the page. Its window part (a diffuser plate with a flange) and the LED board go in from
above, and a cover plate is glued into a seat in the tray's top. The pin is 1.75 mm filament.
"""
import math
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, rx, plane_yz)

W = 30.0                                  # all parts
DIF = (0.99, 0.94, 0.80)                  # translucent white, shown lit
GAP_Y = (0.0, 3.0)                        # the clip's gap (the cover goes here)
FJ = 2.4                                  # thin front jaw
BJ = 14.0                                 # back of the back jaw = back of the neck (AY + KR)
ZB = 32.0                                 # top of the clip (bridge)
BUMP = (0.6, 4.0)                         # bump on the front jaw: height, centre z
AY, AZ, KR, KG = 9.0, 44.0, 5.0, 0.4      # hinge axis, knuckle radius, gap
KL = 10.0                                 # middle (head) knuckle
PIN = 1.9
NOTCH_Z = 34.8                            # bottom of the notch between the body's knuckles: the head's root swings down to 35.3 at rest
HEAD = (56.0, 12.0)                       # head length (from y = 0 forward), thickness
HZ0 = AZ - KR                             # head underside at rest (39)
BAT = (26.0, 7.5, 22.0)                   # CR2032 holder with switch: x, y, z (match yours)
BAT_Y0, BAT_Z0 = BJ - BAT[1], 3.0
WIN = (18.0, 6.0, -46.0)                  # head window: x, y, centre y
FL = 1.2                                  # diffuser flange
PB = 2.4                                  # head floor and cover
OPEN = 29.5                               # rest angle: the head's underside lands on the body's front top edge (29.8)


def ext(pts, x0=-W / 2, x1=W / 2):
    return plane_yz(x0).polyline(pts).close().extrude(x1 - x0)


def circle_x(y, z, r, x0=-W / 2, x1=W / 2):
    return plane_yz(x0).center(y, z).circle(r).extrude(x1 - x0)


def tilt(wp, deg):
    """Rotate about the hinge axis; positive tips the head's front down."""
    return wp.translate((0, -AY, -AZ)).rotate((0, 0, 0), (1, 0, 0), deg).translate((0, AY, AZ))


def book_light_clip():
    y0, y1 = GAP_Y
    prof = [(y0 - FJ, 0), (y0, 0), (y0, ZB - 4.0), (y1, ZB - 4.0), (y1, 0), (BJ, 0),
            (AY + KR, AZ), (AY - KR, AZ), (AY - KR, ZB), (y0 - FJ, ZB)]
    body = ext(prof)
    body = body.edges("|X").edges(cq.selectors.BoxSelector((-W, -50, 0.05), (W, 50, AZ - 1))).chamfer(CH)
    body = body.edges("|X").edges(cq.selectors.BoxSelector((-W, -50, -0.05), (W, 50, 0.05))).chamfer(CH_BED)
    body = body.union(circle_x(AY, AZ, KR))
    body = body.union(ext([(y0 - 0.01, BUMP[1] - BUMP[0] - 1.0), (y0 + BUMP[0], BUMP[1] - 1.0),
                           (y0 + BUMP[0], BUMP[1] + 1.0), (y0 - 0.01, BUMP[1] + BUMP[0] + 1.0)]))
    body = body.cut(ext([(y1 - 0.01, 1.21), (y1 - 0.01, -1), (y1 + 2.2, -1)]))           # 45-deg lead-in on the back jaw
    body = body.faces("<X").edges().chamfer(CH).faces(">X").edges().chamfer(CH)
    body = body.cut(box(-KL / 2 - KG, KL / 2 + KG, AY - KR - 1, AY + KR + 1, NOTCH_Z, AZ + KR + 1))   # room for the head's knuckle and its root as it tips
    bx = BAT[0] / 2 + GAP
    body = body.cut(box(-bx, bx, BAT_Y0 - GAP, BJ + 1, BAT_Z0, BAT_Z0 + BAT[2] + 2 * GAP))
    rz = BAT_Z0 + BAT[2] + 2 * GAP                                # 45-deg roof over the holder, rising to the back
    body = body.cut(ext([(BAT_Y0 - GAP, rz - 0.01), (BJ + 1, rz - 0.01), (BJ + 1, rz + BJ + 1 - BAT_Y0 + GAP)], -bx, bx))
    body = body.cut(cq.Workplane("XY").workplane(offset=rz - 1).center(0, AY).circle(1.5).extrude(NOTCH_Z - rz + 2))  # wire

    hl, ht = HEAD
    head = box(-W / 2, W / 2, -hl, -9.0 + AY, HZ0, HZ0 + ht)
    head = head.edges("|Z").chamfer(CH).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    head = head.cut(box(-W / 2 + T + 1, W / 2 - T - 1, -hl + T + 1, -T - 1, HZ0 + PB, HZ0 + ht + 1))
    head = head.cut(box(-W / 2 + T, W / 2 - T, -hl + T, -T, HZ0 + ht - PB, HZ0 + ht + 1))     # seat for the cover
    head = head.union(box(-KL / 2, KL / 2, -9.0 + AY - 0.01, AY, HZ0, AZ + KR).union(circle_x(AY, AZ, KR, -KL / 2, KL / 2)))
    wx, wy, wc = WIN
    head = head.cut(box(-wx / 2, wx / 2, wc - wy / 2, wc + wy / 2, HZ0 - 1, HZ0 + PB + 1))
    head = head.cut(cq.Workplane("XY").workplane(offset=HZ0 - 1).center(0, -6.0).circle(1.5).extrude(PB + 2))    # wire
    pin = circle_x(AY, AZ, PIN / 2, -W, W)
    body, head = body.cut(pin), head.cut(pin)

    cov = box(-W / 2 + T + GAP, W / 2 - T - GAP, -hl + T + GAP, -T - GAP, HZ0 + ht - PB, HZ0 + ht).faces(">Z").chamfer(CH)
    dif = box(-wx / 2 + GAP, wx / 2 - GAP, wc - wy / 2 + GAP, wc + wy / 2 - GAP, HZ0, HZ0 + PB)
    dif = dif.union(box(-wx / 2 - FL, wx / 2 + FL, wc - wy / 2 - FL, wc + wy / 2 + FL, HZ0 + PB, HZ0 + PB + FL))
    led = box(-10.0, 10.0, wc - 4.0, wc + 4.0, HZ0 + PB + FL, HZ0 + PB + FL + 1.6)
    bat = box(-BAT[0] / 2, BAT[0] / 2, BAT_Y0, BJ, BAT_Z0 + GAP, BAT_Z0 + GAP + BAT[2])
    pin_r = circle_x(AY, AZ, 0.875, -W / 2 + 0.3, W / 2 - 0.3)

    return {
        "body": Part(body, body, OFF),
        "head": Part(tilt(head, OPEN), head, OFF),
        "head_cover": Part(tilt(cov, OPEN), rx(cov, 180), OFF),
        "diffuser_translucent": Part(tilt(dif, OPEN), rx(dif, 180), DIF),
        "led_board_ref": Part(tilt(led, OPEN), None, DARK, ref=True),
        "battery_holder_ref": Part(bat, None, DARK, ref=True),
        "pin_ref": Part(tilt(pin_r, OPEN), None, DARK, ref=True),
    }


SAMPLES["060_book_light_clip"] = book_light_clip
