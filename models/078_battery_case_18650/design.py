"""078 18650 battery case: four 18650 cells standing in bores in a round case under a flush screw lid.

The 12_threaded_jar body and lid (45-deg flanked threads, pitch 4) around a solid rack: the cells stand in four bores on a 21 pitch,
each bore its own cell, so no two cells touch and nothing metal can reach their ends while the lid is on. The lid's inside stops 0.6
over a 70 long protected cell; a bare 65 cell stands lower in the same bore.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, OFF, DARK, ACC, cyl, rx, feet, copies, thread_solid)  # noqa: E402

RO, HB, HL = 32.0, 64.0, 16.0      # Ø64; body 64 + lid 16 = 80 (5 : 4 of the diameter); body : lid = 4 : 1
NECK_R = RO - 4.0                  # thread root on the body: 2.4 lid wall + 1.2 thread + 0.4 clearance
PITCH, DEPTH = 4.0, 1.2
LID_WALL = 2.4
CELL_R, CELL_L = 9.3, 70.0         # Ø18.6, up to 70 long (protected cells; a bare cell is 18.4 x 65)
BORE_R = CELL_R + 0.25
P = 21.0                           # bore pitch: 1.9 of wall between bores
FLOOR = 7.0                        # bore floor: HB + HL - 2.4 (lid inside) - 0.6 - CELL_L
RACK = 40.0                        # top of the rack: 33 of each cell in its bore, 37 above it


def battery_case_18650():
    pts = [(sx * P / 2, sy * P / 2) for sx in (-1, 1) for sy in (-1, 1)]
    body = cyl(RO, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    body = body.union(cyl(NECK_R, HB - 0.01, 12.0))
    ri, rn = RO - T, NECK_R - T
    shoulder = cq.Workplane("XY").add(cq.Solid.makeCone(ri, rn, ri - rn, pnt=cq.Vector(0, 0, HB - 4.0)))  # 45 deg
    inner = cyl(ri, RACK, HB - 4.0 - RACK).union(shoulder).union(cyl(rn, HB - 4.0 + (ri - rn) - 0.01, 20))
    body = body.cut(inner)
    body = body.faces(">Z").chamfer(CH)
    for (x, y) in pts:
        body = body.cut(cyl(BORE_R, FLOOR, RACK, x, y))
        body = body.cut(cq.Workplane("XY").add(cq.Solid.makeCone(BORE_R, BORE_R + CH + 0.01, CH + 0.01,
                                                                 pnt=cq.Vector(x, y, RACK - CH))))
    body = body.union(thread_solid(NECK_R, HB + 2.0, 2.0, PITCH, DEPTH, 2.8, 0.4, external=True))
    body = feet(body, [(sx * 16, sy * 16) for sx in (-1, 1) for sy in (-1, 1)])

    rl = RO - LID_WALL
    lid = cyl(RO, HB, HL).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    lid = lid.cut(cyl(rl, HB - 1, HL - 2.4 + 1))
    lid = lid.union(thread_solid(rl, HB + 2.0 + PITCH / 2, 2.25, PITCH, DEPTH, 2.4, 0.4, external=False)
                    .intersect(cyl(RO - 0.5, HB + 0.5, HL - 3)))
    ribs = cq.Workplane("XY").workplane(offset=HB + 7).polarArray(RO, 0, 360, 64).rect(1.0, 0.8).extrude(HL - 7.5)
    lid = lid.cut(ribs)                # grip on the upper band; the band at the seam stays smooth
    cells = copies([cyl(CELL_R, FLOOR, CELL_L, x, y) for (x, y) in pts])
    return {
        "body": Part(body, body, OFF),
        "lid": Part(lid, rx(lid, 180), DARK),
        "cells_ref": Part(cells, None, ACC, qty=4, ref=True),
    }


SAMPLES["078_battery_case_18650"] = battery_case_18650
