"""046 LED candle tube: a Ø56 x 144 column, an opaque base 24 high and a translucent shade 120 high screwed onto it.

A bought LED tea light sits in a pocket on top of the base's neck; the shade, a closed tube in translucent PETG with a 1.68 wall,
screws over it and glows. A finger reaches the tea light's switch through a hole in the bottom of the base. The threads are
those of 12_threaded_jar scaled to the column, so the base prints upright and the shade prints on its closed top without
supports; the shade's wall thickens to 2.4 only at the thread. Unscrew the shade to change the cell; two notches in the
pocket's rim let fingers lift the tea light out.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, DIV, CH, CH_BED, OFF, DARK,  # noqa: E402
                         box, cyl, rx, feet, thread_solid)

RO, HB, HS = 28.0, 24.0, 120.0          # Ø56; base : shade = 1 : 5
NECK_R, NECK_H = 24.0, 12.0             # thread root on the base (as 12_threaded_jar: 4 under the outside)
PITCH, DEPTH = 4.0, 1.2
TOP = 2.4                               # shade's closed top
RL = RO - 2.4                           # shade wall at the thread: 2.4
RS = RO - DIV                           # shade wall elsewhere: 1.68, the diffuser rule
LIGHT = (38.0, 16.0)                    # LED tea light: body Ø and height without the flame (check yours)
POCKET = 8.0                            # pocket depth in the neck
NOTCH = (12.0, 6.0)                     # finger notches: width, depth
REACH_R = 14.0                          # hole from below to the tea light's switch: a finger fits; the light rests on a 5.3 ledge


def candle_led_holder():
    zt = HB + NECK_H                                         # neck top
    base = cyl(RO, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    base = base.union(cyl(NECK_R, HB - 0.01, NECK_H + 0.01).faces(">Z").chamfer(CH))
    base = base.union(thread_solid(NECK_R, HB + 2.0, 2.0, PITCH, DEPTH, 2.8, 0.4, external=True))
    base = base.cut(cyl(LIGHT[0] / 2 + 0.3, zt - POCKET, POCKET + 1))
    base = base.cut(box(-NOTCH[0] / 2, NOTCH[0] / 2, -NECK_R - 2, NECK_R + 2, zt - NOTCH[1], zt + 1))
    base = base.cut(cyl(REACH_R, -1, zt - POCKET + 1))
    base = feet(base, [(sx * 14.85, sy * 14.85) for sx in (-1, 1) for sy in (-1, 1)])   # on r 21, between hole and edge

    zb = zt - 1.2                                            # top of the 2.4 band; a 45-deg step to the 1.68 wall above it
    sh = cyl(RO, HB, HS).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    inner = cyl(RL, HB - 1, zb - HB + 1).union(cq.Workplane("XY").add(
        cq.Solid.makeCone(RL, RS, RS - RL, pnt=cq.Vector(0, 0, zb)))).union(cyl(RS, zb + (RS - RL) - 0.01, HS - TOP - (zb - HB) - (RS - RL)))
    sh = sh.cut(inner)
    sh = sh.union(thread_solid(RL, HB + 2.0 + PITCH / 2, 2.25, PITCH, DEPTH, 2.4, 0.4, external=False)
                  .intersect(cyl(RO - 0.5, HB + 0.5, zb - HB - 0.5)))

    z0 = zt - POCKET
    light = cyl(LIGHT[0] / 2, z0, LIGHT[1]).union(cyl(4.0, z0 + LIGHT[1] - 0.01, 18.0))
    return {
        "base": Part(base, base, DARK),
        "shade": Part(sh, rx(sh, 180), OFF),
        "tea_light_ref": Part(light, None, OFF, ref=True),
    }


SAMPLES["046_candle_led_holder"] = candle_led_holder
