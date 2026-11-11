"""005 Folding phone stand: a base and a leg joined by a pin hinge, both 8 mm plates printed on their sides.

Open, the leg leans forward at 50 deg and stops against a heel on the base; the phone stands
against the front ridge and leans on the round end of the leg. Folded, the leg lies on the base,
16 high like the ridge, in front of the 24 high heel. The heel is 3 x P high so the leg bears on it
over 12 mm of its length, not only at the knuckles.
"""
import math
import os
import sys

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, CH, CH_BED, OFF, box, rx, plane_yz)  # noqa: E402

W, DEP, P = 72.0, 96.0, 8.0        # width, base depth (4:3), plate thickness
KR = P / 2                         # knuckle = full round end of the plate
YA, ZA = 24.0, P + KR              # hinge axis: on the base top, 24 behind the centre
LEG = 56.0                         # axis to the centre of the leg's far end
OPEN = 50.0                        # leg angle from the base when open
KL, KG, NK = 12.0, 0.4, 5          # knuckles as in 07_hinged_case
PIN = 1.9                          # 1.75 mm filament
RIDGE = (-DEP / 2, -DEP / 2 + P)   # front ridge, P thick, P high
HEEL = 3 * P                       # heel top: 24


def segs():
    x0 = -(NK * KL + (NK - 1) * KG) / 2
    return [(x0 + i * (KL + KG), x0 + i * (KL + KG) + KL) for i in range(NK)]


def extrude_x(pts, x0=-W / 2, x1=W / 2):
    return plane_yz(x0).polyline(pts).close().extrude(x1 - x0)


def circle_x(y, z, r, x0=-W / 2, x1=W / 2):
    return plane_yz(x0).center(y, z).circle(r).extrude(x1 - x0)


def phone_stand_fold():
    y0, y1 = -DEP / 2, DEP / 2
    a = math.radians(OPEN)
    n = (math.sin(a), math.cos(a))                 # back face normal of the open leg, (y, z)
    d = (-math.cos(a), math.sin(a))                # leg direction, (y, z)

    base = box(-W / 2, W / 2, y0, y1, 0, P)
    # front ridge with a full round top (an end in the air), flat where it meets the plate
    base = base.union(box(-W / 2, W / 2, RIDGE[0], RIDGE[1], P - 0.01, 2 * P - KR))
    base = base.union(circle_x((RIDGE[0] + RIDGE[1]) / 2, 2 * P - KR, KR))
    # heel: everything behind the open leg's back face, up to HEEL (the leg never sweeps that wedge)
    py, pz = YA + (KR + 0.1) * n[0], ZA + (KR + 0.1) * n[1]      # 0.1 clear: the leg comes to rest on it
    t_lo, t_hi = (P - pz) / d[1], (HEEL - pz) / d[1]
    heel = [(py + t_lo * d[0], P - 0.01), (y1, P - 0.01), (y1, HEEL), (py + t_hi * d[0], HEEL)]
    base = base.union(extrude_x(heel))

    leg = box(-W / 2, W / 2, YA - LEG, YA, ZA - KR, ZA + KR)        # folded: lying on the base
    leg = leg.union(circle_x(YA - LEG, ZA, KR)).union(circle_x(YA, ZA, KR))

    s = segs()
    base_k, leg_k = s[0::2], s[1::2]
    for (xa, xb) in base_k:
        k = 2.828427                               # 45-deg web from the knuckle to the plate
        web = [(YA - k - 1.17, P - 0.01), (YA + k + 1.17, P - 0.01), (YA + k, ZA - k), (YA - k, ZA - k)]
        base = base.union(circle_x(YA, ZA, KR, xa, xb)).union(extrude_x(web, xa, xb))
        leg = leg.cut(circle_x(YA, ZA, KR + KG, xa - KG / 2, xb + KG / 2))
        leg = leg.cut(box(xa - KG / 2, xb + KG / 2, YA - KR - 2.0, YA + KR, P - 1, ZA))   # room for the web
    for (xa, xb) in leg_k:
        base = base.cut(circle_x(YA, ZA, KR + KG, xa - KG / 2, xb + KG / 2))
        base = base.cut(box(xa - KG / 2, xb + KG / 2, YA - KR - 2.0, YA + KR + KG, P - 1, ZA))
    pin = circle_x(YA, ZA, PIN / 2, -W, W)
    base, leg = base.cut(pin), leg.cut(pin)

    base = base.faces("<X").edges().chamfer(CH_BED).faces(">X").edges().chamfer(CH)
    leg = leg.faces("<X").edges().chamfer(CH_BED).faces(">X").edges().chamfer(CH)

    # shown open; rotate about the hinge axis by -OPEN (folded is the as-built position)
    leg_open = leg.translate((0, -YA, -ZA)).rotate((0, 0, 0), (1, 0, 0), -OPEN).translate((0, YA, ZA))
    side_down = lambda wp: wp.rotate((0, 0, 0), (0, 1, 0), -90)      # -X side face on the bed
    return {
        "base": Part(base, side_down(base), OFF),
        "leg": Part(leg_open, side_down(leg), OFF),
    }


SAMPLES["005_phone_stand_fold"] = phone_stand_fold
