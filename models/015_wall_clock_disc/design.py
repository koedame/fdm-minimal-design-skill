"""015 Wall clock disc: a Ø192 x 20 disc on the wall, the face itself the dial, hung on one keyhole.

The disc is a shallow dish printed face down: the face is the bed face, the 12 bars are inlaid in its
first layers, and the open back takes the movement. The back steps in 1.2 on a 45-deg face, so the
disc stands off the wall on a shadow line. One keyhole in a post at the top hangs it on one screw; the
countersunk head seats on a 45-deg cone, which also lets the pocket print without support.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, OFF, DARK, ACC,  # noqa: E402
                         CLOCK_SHAFT_HOLE, HAND_HOLES, box, cyl, rrect, rx, rz)

R, DEP = 96.0, 20.0               # Ø192 (grid 4), depth 20: 1 : 9.6 against the diameter
FACE = 2.4                        # face plate: a movement bushing clamps up to about 5
INSET, PL = 1.2, 2.4              # floating back: stepped in 1.2 on 45 deg, 2.4 deep
MARGIN = 8.0                      # bars end 8 inside the rim (2 x grid)
MAJ, MIN = (3.2, 16.0), (1.6, 8.0)    # bar width x length, 2 : 1 both ways
R_OUT = R - MARGIN                # 88: outer ends of all bars
MIN_TIP = R_OUT - MIN[1]          # 80: the minute hand reaches the inner ends of the minor bars
HOUR_TIP = 0.75 * MIN_TIP         # 60
MOVE, MOVE_T = 56.0, 16.0         # common quartz movement (check yours)
KY = 64.0                         # keyhole entry: 64 above the centre, clear of the movement
POST_W, POST_H = 24.0, 32.0       # post carrying the keyhole
HEAD, SHANK, TRAVEL, LEDGE = 8.4, 4.2, 8.0, 2.0   # the wall mounting rule; countersunk screw


def stadium(w, z0, t, x, y0, y1):
    return rrect(w, (y1 - y0) + w, w / 2 - 0.001, z0, t, x, (y0 + y1) / 2)


def stadium_wire(w, z, x, y0, y1):
    return stadium(w, z, 1.0, x, y0, y1).faces("<Z").wires().val()


def wall_clock_disc():
    # print frame: face on z = 0 (the bed), wall side at z = DEP, local y up
    disc = cyl(R, 0, DEP - PL).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(INSET)
    disc = disc.union(cyl(R - INSET, DEP - PL - 0.01, PL + 0.01)).faces(">Z").chamfer(CH)
    ri = R - T
    cone = cq.Workplane("XY").add(cq.Solid.makeCone(ri, ri - INSET, INSET, pnt=cq.Vector(0, 0, DEP - PL - INSET)))
    cavity = cyl(ri, FACE, DEP - PL - INSET - FACE + 0.01).union(cone).union(cyl(ri - INSET, DEP - PL - 0.01, PL + 1))
    disc = disc.cut(cavity)

    y0, y1 = KY, KY + TRAVEL
    post = rrect(POST_W, POST_H, 4.0, FACE - 0.01, DEP - FACE + 0.01, 0, (y0 + y1) / 2)
    disc = disc.union(post)
    zl = DEP - LEDGE
    zc = zl - (HEAD - SHANK) / 2
    disc = disc.cut(stadium(SHANK, zl - 0.01, LEDGE + 1, 0, y0, y1))      # slot through the ledge
    disc = disc.cut(cyl(HEAD / 2, zc - 3.0, DEP, 0, y0))                   # entry hole
    disc = disc.cut(stadium(HEAD, zc - 3.0, 3.01, 0, y0, y1))              # head pocket
    seat = cq.Solid.makeLoft([stadium_wire(HEAD, zc, 0, y0, y1), stadium_wire(SHANK, zl + 0.001, 0, y0, y1)], True)
    disc = disc.cut(cq.Workplane("XY").add(seat))
    disc = disc.cut(cyl(CLOCK_SHAFT_HOLE / 2, -1, FACE + 2))

    marks = top = None
    for i in range(12):
        w, ln = MAJ if i % 3 == 0 else MIN
        bar = rz(box(-w / 2, w / 2, R_OUT - ln, R_OUT, 0, 0.4), -30 * i)
        if i == 0:
            top = bar                     # 12 o'clock: the one accent, tells which way is up
        else:
            marks = bar if marks is None else marks.union(bar)
    disc = disc.cut(marks).cut(top)

    def hand(w, tip, hub, hole):
        h = box(-w / 2, w / 2, 0, tip - w / 2, 0, 1.0).union(cyl(w / 2, 0, 1.0, 0, tip - w / 2))
        return h.union(cyl(hub, 0, 1.0)).cut(cyl(hole / 2, -1, 3))

    hour = hand(MAJ[0], HOUR_TIP, 4.4, HAND_HOLES["hour"])
    minute = hand(MIN[0], MIN_TIP, 3.4, HAND_HOLES["minute"])
    move = box(-MOVE / 2, MOVE / 2, -MOVE / 2, MOVE / 2, FACE, FACE + MOVE_T).union(cyl(3.5, 0, FACE + 0.01))

    to_wall = lambda wp: rz(rx(wp, 90), 180)          # face toward -Y, wall side on y = +DEP
    in_front = lambda wp, z, ang: to_wall(rz(rx(wp, 180), ang).translate((0, 0, -z)))   # ang = clockwise - 180: 10:08
    return {
        "disc": Part(to_wall(disc), disc, OFF),
        "dial_marks_inlay": Part(to_wall(marks), marks, DARK, anchor="disc"),
        "dial_top_mark_inlay": Part(to_wall(top), top, ACC, anchor="disc"),
        "hand_hour": Part(in_front(hour, 0.6, 124), hour, DARK),
        "hand_minute": Part(in_front(minute, 1.8, -132), minute, DARK),
        "movement_ref": Part(to_wall(move), None, DARK, ref=True),
    }


SAMPLES["015_wall_clock_disc"] = wall_clock_disc
