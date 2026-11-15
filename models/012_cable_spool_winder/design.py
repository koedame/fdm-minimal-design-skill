"""012 Cable spool winder: two Ø64 flanges on a Ø32 hub, for winding up a spare cable.

One flange carries the hub; the other locates on it with a lip inside the hub and is glued there. One
piece would not print: the second flange would overhang the hub by 16 mm all round. The cable starts in
a radial slot in the first flange, with its connector outside, and its other end is pinched in a notch
in the rim of the second.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK, cyl, box, rx  # noqa: E402

RF, RH, WIDTH = 32.0, 16.0, 24.0   # Ø64 flanges, Ø32 hub (1 : 2), 24 overall (8 : 3 against Ø64)
RHI = RH - T                       # hub bore 13.48
LIP_O = RHI - GAP                  # lip outside 13.23: 0.25 clearance in the hub bore
LIP_I = LIP_O - DIV                # lip inside 11.55 = the hole through both flanges
LIP_H = 4.0
SLOT_W = 4.4                       # cable start: a cable up to Ø4 lies in it
NOTCH_W, NOTCH_L = 3.0, 8.0        # cable end: pinches a Ø3-4 jacket
Z_B = WIDTH - T                    # underside of the second flange


def flange(z0, bed_down):
    f = cyl(RF, z0, T).cut(cyl(LIP_I, z0 - 1, T + 2))
    lo, hi = (CH_BED, CH) if bed_down else (CH, CH_BED)
    return f.faces("<Z").chamfer(lo).faces(">Z").chamfer(hi)


def cable_spool_winder():
    a = flange(0, True).union(cyl(RH, T - 0.01, Z_B - T + 0.01).cut(cyl(RHI, 0, WIDTH)))
    a = a.cut(cq.Workplane("XY").center((RH + RF + 1) / 2, 0).slot2D(RF + 1 - RH + SLOT_W, SLOT_W, 0)
              .extrude(T + 1).translate((0, 0, -0.5)).intersect(box(RH, RF + 2, -RF, RF, -1, T + 1)))

    b = flange(Z_B, False).union(cyl(LIP_O, Z_B - LIP_H, LIP_H + 0.01).cut(cyl(LIP_I, Z_B - LIP_H - 1, LIP_H + 2)))
    notch = cq.Workplane("XY").workplane(offset=Z_B - 1).center(-(RF - NOTCH_L / 2), 0) \
        .slot2D(NOTCH_L + NOTCH_W, NOTCH_W, 0).extrude(T + 2)
    lead = cq.Workplane("XY").workplane(offset=Z_B - 1).polyline(
        [(-RF - 1, NOTCH_W / 2 + 2), (-RF + 2, NOTCH_W / 2), (-RF + 2, -NOTCH_W / 2), (-RF - 1, -NOTCH_W / 2 - 2)]).close().extrude(T + 2)
    b = b.cut(notch.union(box(-RF - 1, -RF + NOTCH_L / 2, -NOTCH_W / 2, NOTCH_W / 2, Z_B - 1, WIDTH + 1))).cut(lead)
    return {
        "flange_hub": Part(a, a, OFF),
        "flange_cap": Part(b, rx(b, 180).translate((0, 0, WIDTH)), DARK),
    }


SAMPLES["012_cable_spool_winder"] = cable_spool_winder
