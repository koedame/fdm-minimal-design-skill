"""029 Column clock: a Ø96 x 64 column lying on its side, the round end its dial, the back a screw-in lid.

The body prints face down: the dial is the bed face, its 12 bars inlaid in the first layers, and the
quartz movement goes in from the back. The back is closed by a round lid that screws into the body
with the 45-deg flanked thread of 12_threaded_jar (pitch 4, 0.4 clearance) turned inside out: the
thread is on the lid's boss and inside the body's mouth, so the lid sits flush in the back face and
the column stays one cylinder. The boss bottoms on a ledge, which sets the lid flush. A coin turns it
in a slot to reach the movement's battery. A 16 wide flat along the bottom keeps the column from rolling.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, OFF, DARK, ACC,  # noqa: E402
                         CLOCK_SHAFT_HOLE, HAND_HOLES, box, cyl, rx, rz, thread_solid)

RO, DEP = 48.0, 64.0              # Ø96 x 64: diameter : depth = 3 : 2
FACE = TOP = 2.4                  # dial plate (the movement bushing clamps up to about 5); lid plate
RI = RO - T                       # 45.48: the bore; the body's internal thread root
PITCH, DEPTH, CLR = 4.0, 1.2, 0.4
R_LID = RI - CLR                  # 45.08: lid plate in the bore
R_BOSS = RI - DEPTH - CLR         # 43.88: lid thread root (0.4 under the body's crest)
BOSS = 12.0                       # boss length: the lid bottoms on the ledge 12 under its plate
Z_LEDGE = DEP - TOP - BOSS - 0.1  # 49.5: the boss rests 0.1 over it (contact)
R_LEDGE = 41.0                    # ledge inside: the movement's 79.2 diagonal passes
Z_THR = Z_LEDGE + 2.5             # body thread: first crest centre; the lid's is half a pitch higher
FLAT = 16.0                       # flat along the bottom
Y_FLAT = (RO ** 2 - (FLAT / 2) ** 2) ** 0.5   # 47.33: the wall keeps 1.85 there
MARGIN = 6.0
MAJ, MIN = (2.4, 10.0), (1.2, 5.0)  # bar width x length, 2 : 1 both ways
R_OUT = RO - MARGIN               # 42
MIN_TIP = R_OUT - MIN[1]          # 37: the minute hand reaches the inner ends of the minor bars
HOUR_TIP = 0.75 * MIN_TIP
MOVE, MOVE_T = 56.0, 16.0         # common quartz movement (check yours)
SLOT = (24.0, 2.4, 1.2)           # coin slot: length, width, depth


def revolve(pts):
    return cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0))


def column_clock():
    # print frame: the dial on z = 0 (the bed), the back at z = DEP, local y up
    body = cyl(RO, 0, DEP).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    body = body.cut(cyl(RI, FACE, DEP)).cut(cq.Workplane("XY").add(cq.Solid.makeCone(RI, RI + CH, CH, pnt=cq.Vector(0, 0, DEP - CH))))
    run = RI - R_LEDGE                # ledge: flat on top for the boss, 45 deg underneath
    body = body.union(revolve([(R_LEDGE, Z_LEDGE), (RI + 0.01, Z_LEDGE), (RI + 0.01, Z_LEDGE - run - 0.01)]))
    body = body.union(thread_solid(RI, Z_THR, 1.75, PITCH, DEPTH, 2.8, 0.4, external=False))
    body = body.cut(box(-RO, RO, -RO - 1, -Y_FLAT, -1, DEP + 1))
    body = body.cut(cyl(CLOCK_SHAFT_HOLE / 2, -1, FACE + 2))

    marks = top = None
    for i in range(12):
        w, ln = MAJ if i % 3 == 0 else MIN
        bar = rz(box(-w / 2, w / 2, R_OUT - ln, R_OUT, 0, 0.4), -30 * i)
        if i == 0:
            top = bar                     # 12 o'clock: the one accent, tells which way is up
        else:
            marks = bar if marks is None else marks.union(bar)
    body = body.cut(marks).cut(top)

    z_boss = DEP - TOP - BOSS
    lid = cyl(R_LID, DEP - TOP, TOP).faces(">Z").chamfer(CH_BED)
    lid = lid.union(cyl(R_BOSS, z_boss, BOSS + 0.01).cut(cyl(R_BOSS - T, z_boss - 1, BOSS + 1)))
    lid = lid.union(thread_solid(R_BOSS, Z_THR + PITCH / 2, 1.5, PITCH, DEPTH, 2.8, 0.4, external=True))
    lid = lid.cut(box(-SLOT[0] / 2, SLOT[0] / 2, -SLOT[1] / 2, SLOT[1] / 2, DEP - SLOT[2], DEP + 1))

    def hand(w, tip, hub, hole):
        h = box(-w / 2, w / 2, 0, tip - w / 2, 0, 1.0).union(cyl(w / 2, 0, 1.0, 0, tip - w / 2))
        return h.union(cyl(hub, 0, 1.0)).cut(cyl(hole / 2, -1, 3))
    hour = hand(MAJ[0], HOUR_TIP, 4.4, HAND_HOLES["hour"])
    minute = hand(1.6, MIN_TIP, 3.4, HAND_HOLES["minute"])      # 1.6: four lines, a 1.2 hand would be fragile
    move = box(-MOVE / 2, MOVE / 2, -MOVE / 2, MOVE / 2, FACE, FACE + MOVE_T).union(cyl(3.5, 0, FACE + 0.01))
    world = lambda wp: rz(rx(wp, 90), 180)            # dial toward -Y, 12 o'clock up, back on y = +DEP
    in_front = lambda wp, z, ang: world(rz(rx(wp, 180), ang).translate((0, 0, -z)))   # ang = clockwise - 180: 10:08
    return {
        "body": Part(world(body), body, OFF),
        "dial_marks_inlay": Part(world(marks), marks, DARK, anchor="body"),
        "dial_top_mark_inlay": Part(world(top), top, ACC, anchor="body"),
        "lid": Part(world(lid), rx(lid, 180), OFF),
        "hand_hour": Part(in_front(hour, 0.6, 124), hour, DARK),
        "hand_minute": Part(in_front(minute, 1.8, -132), minute, DARK),
        "movement_ref": Part(world(move), None, DARK, ref=True),
    }


SAMPLES["029_column_clock"] = column_clock
