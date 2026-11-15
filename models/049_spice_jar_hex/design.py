"""049 Hexagonal spice jar: a hexagonal body 48 across the flats and 80 high, under a round screw lid Ø48 x 16.

The body is a hexagonal prism with rounded edges, so jars stand together flat to flat in a drawer or on a shelf, and each flat
takes a label. The lid is round, not hexagonal: a screw lid stops at whatever angle the thread ends, so a hexagonal lid would
almost never line up with the body. Its diameter is the body's width across the flats, so it touches the middle of each flat
and the six corners of the body's top show round it. The thread is that of 12_threaded_jar on a smaller neck; the cavity's
ceiling is a 45-deg cone cut into the hexagon, so the body prints upright without supports.
"""
import math
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, OFF, DARK,  # noqa: E402
                         cyl, rx, thread_solid)

AF, HB, RE = 48.0, 80.0, 4.0            # across flats, body height, edge radius
RO, HL = AF / 2, 16.0                   # lid: Ø = across flats; body : lid = 5 : 1
NECK_R, NECK_H = RO - 4.0, 12.0         # thread root, as 12_threaded_jar: 4 under the lid's outside
PITCH, DEPTH = 4.0, 1.2
FLOOR = 2.4


def hexagon(af, z0, h, r):
    """Hexagonal prism, flats facing +-Y, `af` across the flats, vertical edges rounded r."""
    ac = af / math.cos(math.radians(30))
    return (cq.Workplane("XY").workplane(offset=z0).polygon(6, ac).extrude(h).edges("|Z").fillet(r))


def spice_jar_hex():
    body = hexagon(AF, 0, HB, RE).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    body = body.union(cyl(NECK_R, HB - 0.01, NECK_H + 0.01))
    ai = AF / 2 - T                                          # inner apothem
    rc = ai / math.cos(math.radians(30))                     # inner corner radius of the hexagon
    rn = NECK_R - T
    zs = HB - 2.4 - (rc - rn)                                # the cone reaches the neck bore 2.4 under the body's top
    hollow = cyl(rc + 1, FLOOR, zs - FLOOR).union(cq.Workplane("XY").add(
        cq.Solid.makeCone(rc + 1, rn, rc + 1 - rn, pnt=cq.Vector(0, 0, zs - 1))))
    floor_cone = cq.Workplane("XY").add(cq.Solid.makeCone(ai - 2.0, ai - 2.0 + HB, HB, pnt=cq.Vector(0, 0, FLOOR)))
    hollow = hollow.intersect(hexagon(2 * ai, FLOOR, HB, RE - T)).intersect(floor_cone)   # a 45-deg edge round the floor
    hollow = hollow.union(cyl(rn, HB - 4.0, NECK_H + 5))
    body = body.cut(hollow)
    body = body.faces(">Z").chamfer(CH)
    body = body.union(thread_solid(NECK_R, HB + 2.0, 2.0, PITCH, DEPTH, 2.8, 0.4, external=True))

    rl = RO - 2.4
    lid = cyl(RO, HB, HL).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    lid = lid.cut(cyl(rl, HB - 1, HL - 2.4 + 1))
    lid = lid.union(thread_solid(rl, HB + 2.0 + PITCH / 2, 2.25, PITCH, DEPTH, 2.4, 0.4, external=False)
                    .intersect(cyl(RO - 0.5, HB + 0.5, HL - 3)))
    ribs = (cq.Workplane("XY").workplane(offset=HB + 7).polarArray(RO, 0, 360, 42).rect(1.0, 0.8).extrude(HL - 7.5))
    lid = lid.cut(ribs)                                      # grip on the upper band; the band at the seam stays smooth
    return {
        "body": Part(body, body, OFF),
        "lid": Part(lid, rx(lid, 180), DARK),
    }


SAMPLES["049_spice_jar_hex"] = spice_jar_hex
