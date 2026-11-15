"""021 Square tea caddy: a 72 x 72 x 120 caddy, body 96 + lid 24, the lid located by a neck on the body.

The body's wall steps in at the top into a neck (DIV thick) that the lid slides over with 0.25 clearance,
as the lip of the Location rule; a 45-deg cone inside the wall joins the step, so the body prints upright
without support. The lid sits on the shoulder of the wall, flush with the body, and the seam is one V
line. The bottom steps in 1.2 on a 45-deg face, so the caddy stands on a shadow line.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK, rrect, rx  # noqa: E402

S, R = 72.0, 8.0                  # plan 72 (grid 4), R = 11 % of 72
HB, HL = 96.0, 24.0               # body : lid = 4 : 1; total 120 : 72 = 5 : 3
FLOOR = TOP = 2.4
NECK = 12.0                       # the lid slides 12 over the neck: half the lid height
INSET, PL = 1.2, 2.4              # floating plinth, as 03_tray
NO = S - 2 * (T + GAP)            # neck outside: the lid's inside less the clearance
NI = NO - 2 * DIV                 # neck inside
STEP = (S - 2 * T - NI) / 2       # 1.93: the inside of the wall steps in by this at the top


def wire(w, r, z):
    return rrect(w, w, r, z, 1.0).faces("<Z").wires().val()


def tea_caddy_square():
    body = rrect(S - 2 * INSET, S - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    body = body.union(rrect(S, S, R, PL, HB - PL).faces("<Z").chamfer(INSET))
    body = body.faces(">Z").edges().chamfer(CH)
    body = body.union(rrect(NO, NO, R - T - GAP, HB - 0.01, NECK + 0.01).faces(">Z").chamfer(CH))
    ri, rni = R - T, R - T - GAP - DIV
    z_cone = HB - STEP
    cone = cq.Solid.makeLoft([wire(S - 2 * T, ri, z_cone - 0.001), wire(NI, rni, HB + 0.001)], True)   # 45 deg
    body = body.cut(rrect(S - 2 * T, S - 2 * T, ri, FLOOR, z_cone - FLOOR + 0.01))
    body = body.cut(cq.Workplane("XY").add(cone)).cut(rrect(NI, NI, rni, HB, NECK + 1))

    lid = rrect(S, S, R, HB, HL).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    lid = lid.cut(rrect(S - 2 * T, S - 2 * T, R - T, HB - 1, HL - TOP + 1))
    return {
        "body": Part(body, body, OFF),
        "lid": Part(lid, rx(lid, 180), DARK),
    }


SAMPLES["021_tea_caddy_square"] = tea_caddy_square
