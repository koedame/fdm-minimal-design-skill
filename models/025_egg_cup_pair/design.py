"""025 Egg cup pair: two Ø48 x 32 cylinders, each with a spherical seat 14 deep, standing on a shadow line.

The seat is a sphere of R18 centred 4 above the top, so it opens to Ø35: a medium egg (about Ø43) rests
on the rim ring 12 down its side, not on the bottom of the seat, and a smaller egg sits deeper on the
same ring. The bottom steps in 1.2 on a 45-deg face, so each cup floats on a shadow line. Two identical
cups make the pair: one part printed twice.
"""
import math
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, CH, CH_BED, OFF, cyl, copies  # noqa: E402

RO, H = 24.0, 32.0                # Ø48 x 32: width : height = 3 : 2
R_SEAT, Z_SEAT = 18.0, H + 4.0    # sphere R18 centred 4 above the top: 14 deep, rim Ø35
INSET, PL = 1.2, 2.4              # floating plinth, as 03_tray
PITCH = 60.0                      # the pair stands 12 apart (a quarter of the width)
EGG_A, EGG_C = 21.5, 28.5         # medium egg Ø43 x 57, as an ellipsoid


def egg_cup():
    cup = cyl(RO - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    cup = cup.union(cyl(RO, PL, H - PL).faces("<Z").chamfer(INSET))
    # poles to the sides: a sphere's pole at the bottom of the seat meshes open (verify.py: watertight=False)
    cup = cup.cut(cq.Workplane("XZ").sphere(R_SEAT).translate((0, 0, Z_SEAT)))
    return cup.faces(">Z").edges().chamfer(CH)         # both edges of the rim ring


def egg(x):
    """The egg resting on the lower edge of the rim chamfer (CH down the seat from the rim), 0.1 clear in radius."""
    r_rim, dz = math.sqrt(R_SEAT ** 2 - (Z_SEAT - H) ** 2), Z_SEAT - H
    r_c, z_c = r_rim - CH * dz / R_SEAT, H - CH * r_rim / R_SEAT
    zc = z_c + EGG_C * math.sqrt(1 - ((r_c - 0.1) / EGG_A) ** 2)
    m = cq.Matrix([[EGG_A, 0, 0, x], [0, EGG_A, 0, 0], [0, 0, EGG_C, zc]])
    return cq.Workplane("XY").add(cq.Solid.makeSphere(1.0, angleDegrees1=-90, angleDegrees2=90).transformGeometry(m))


def egg_cup_pair():
    cup = egg_cup()
    xs = (-PITCH / 2, PITCH / 2)
    return {
        "cup": Part(copies([cup.translate((x, 0, 0)) for x in xs]), cup, OFF, qty=2),
        "egg_ref": Part(egg(xs[1]), None, (0.96, 0.92, 0.84), ref=True),
    }


SAMPLES["025_egg_cup_pair"] = egg_cup_pair
