"""099 Salt cellar: a rounded-square pot (72 x 72 x 48) whose flat lid swings aside about a vertical pin in one corner.

The pin is a piece of 1.75 filament glued into a blind hole in the body's back-right corner, where the cavity's corner is R16 to leave
room for it; the lid turns on it in a blind hole from below, so its top stays plain. The lid lies flat on the rim. One stud under the
lid, near the front-left inner corner, gives both stops: closed it bears on the left inner wall with the lid square over the body;
swung anticlockwise (seen from above) it reaches the front inner wall at about 40 deg, while the lid's centre of gravity is still
over the rim, so the open lid never tips on the pin. Two printed parts.
"""
import math
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, CH, CH_BED, OFF, box, cyl, rrect, rx, feet  # noqa: E402

S, R = 72.0, 10.0               # 18 modules square; R10 = 13.9 %
HB, LT = 43.2, 4.8              # body and lid: 48 together
FLOOR = 2.4
PX = PY = 31.0                  # pin axis, on the diagonal of the back-right corner: 2.9 from the outside
RP = 16.0                       # the cavity's corner round the pin: 3.1 from the pin
PIN = 1.9                       # 1.75 filament pin
PIN_BODY, PIN_LID = 16.0, 3.6   # blind hole depths; the lid keeps a 1.2 skin over its hole
STUD_R, STUD_H = 3.0, 4.0       # stud under the lid: radius, drop below the rim
STUD_DIST = 67.5                # from the pin: sets the opening angle (about 40 deg)


def body():
    b = rrect(S, S, R, 0, HB).faces("<Z").chamfer(CH_BED)
    wi = S / 2 - T
    c = wi - RP
    cav = rrect(2 * wi, 2 * wi, R - T, FLOOR, HB + 1).cut(box(c, S, c, S, 0, 99))
    cav = cav.union(cyl(RP, FLOOR, HB + 1 - FLOOR, c, c).intersect(box(c, S, c, S, 0, 99)))
    b = b.cut(cav).faces(">Z").chamfer(CH)                   # outer and inner rim edges
    b = b.cut(cyl(PIN / 2, HB - PIN_BODY, PIN_BODY + 1, PX, PY))
    return feet(b, [(sx * 24, sy * 24) for sx in (-1, 1) for sy in (-1, 1)])


def stud_xy():
    """The stud touches the left inner wall with the lid closed."""
    x = -(S / 2 - T) + STUD_R
    return x, PY - math.sqrt(STUD_DIST ** 2 - (PX - x) ** 2)


def lid():
    plate = rrect(S, S, R, HB, LT).faces(">Z").chamfer(CH_BED).faces("<Z").chamfer(CH)
    sx, sy = stud_xy()
    stud = cyl(STUD_R, HB - STUD_H, STUD_H + 0.01, sx, sy).faces("<Z").chamfer(CH)
    return plate.union(stud).cut(cyl(PIN / 2, HB - 0.01, PIN_LID + 0.01, PX, PY))


def salt_cellar_swivel():
    b, l = body(), lid()
    return {
        "body": Part(b, b, OFF),
        "lid": Part(l, rx(l, 180), OFF),
    }


SAMPLES["099_salt_cellar_swivel"] = salt_cellar_swivel
