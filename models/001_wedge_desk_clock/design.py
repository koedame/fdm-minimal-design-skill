"""001 Wedge desk clock: a square face leaning back on a 7:24:25 slope, the body a tube square to the face.

The body is printed face down, so its four walls rise straight from the bed and the plan radii of
the face lie in the layer plane. The back is cut vertical and closed by a plate on a lip and two
magnets, which is also the way to the movement and its battery.
"""
import math
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, GAP, OFF, PLATE, DARK,  # noqa: E402
                         CLOCK_SHAFT_HOLE, HAND_HOLES, box, cyl, rrect, rx, rz, on_slope)

# slope: a 7:24:25 right triangle x 4. The face rises 96 over a run of 28 and is exactly 100 long.
RUN, RISE, FACE = 28.0, 96.0, 100.0
TILT = math.degrees(math.atan2(RISE, RUN))          # 73.74 deg from the desk
DEPTH = 48.0                                        # ground depth (grid 4), room for the movement
R = 12.0                                            # face corners = dial margin
DIAL_D, DIAL_T = 76.0, 2.4                          # face 100 - 2 x 12
MOVE, MOVE_T = 56.0, 16.0                           # common quartz movement (check yours)
PAD, MAG_D, MAG_H = 2.4, 6.2, 3.2
BOSS_U, BOSS_X, BOSS_R = 24.0, 36.0, 5.0


def to_world(wp):
    """Face frame (face on z=0, body toward -z, u up the face along +y) -> use frame."""
    return on_slope(wp, TILT)


def to_face(wp):
    return on_slope(wp, -TILT)


def prism(w, r, z0, z1, cu=FACE / 2):
    """Rounded square of the face plan, extruded along the face normal between z0 and z1 (face frame)."""
    return rrect(w, w, r, z0, z1 - z0, 0, cu)


def wedge_desk_clock():
    yb = DEPTH                                     # back plane (use frame)
    big = 400.0
    keep = box(-big, big, -big, yb - T, 0, big)    # above the desk, in front of the back plate

    outer = to_world(prism(FACE, R, -120, 0)).intersect(keep)
    inner = to_world(prism(FACE - 2 * T, R - T, -120, -T)).intersect(box(-big, big, -big, big, T, big))
    body = outer.cut(inner)
    body = to_face(body)                           # chamfer in the face frame: face edge is on the bed
    body = body.faces(">Z").edges().chamfer(CH_BED)
    body = to_world(body)
    body = body.faces(">Y").edges().chamfer(CH)    # back rim, inner and outer

    # magnet bosses: vertical in the print (along the face normal), cut square to the back plate
    stop = yb - T - PAD
    for sx in (-1, 1):
        boss = to_world(cyl(BOSS_R, -120, 120 - T + 0.1, sx * BOSS_X, BOSS_U)).intersect(
            box(-big, big, -big, stop, T - 0.1, big))
        body = body.union(boss)
        body = body.cut(cq_y_cyl(MAG_D / 2, stop - MAG_H, stop + 0.1, sx * BOSS_X, boss_z(sx)))
    shaft = to_world(cyl(CLOCK_SHAFT_HOLE / 2, -T - 1, T + 2, 0, FACE / 2))
    body = body.cut(shaft)

    # back plate: the section of the outer tube, a lip inside the opening, two magnet pads
    plate = to_world(prism(FACE, R, -120, 0)).intersect(box(-big, big, yb - T, yb, GAP, big))   # clear of the desk: only the body stands
    lip = to_world(prism(FACE - 2 * (T + GAP), R - T - GAP, -120, 0)).cut(
        to_world(prism(FACE - 2 * (T + GAP + 1.68), R - T - GAP - 1.68, -120, 0)))
    lip = lip.intersect(box(-big, big, yb - T - 4, yb - T + 0.1, T + GAP, big))
    plate = plate.union(lip)
    for sx in (-1, 1):
        plate = plate.union(cq_y_cyl(BOSS_R, stop, yb - T + 0.1, sx * BOSS_X, boss_z(sx)))
        plate = plate.cut(cq_y_cyl(MAG_D / 2, stop - 0.1, stop + MAG_H, sx * BOSS_X, boss_z(sx)))
    plate = plate.faces(">Y").edges().chamfer(CH)

    # dial: a disc proud of the face, bars inlaid 0.4. Majors 2.4 x 8, minors 1.2 x 4 (2:1 both ways),
    # all ending 4 (grid) inside the rim.
    dial = cyl(DIAL_D / 2, 0, DIAL_T, 0, FACE / 2).faces(">Z").chamfer(CH)
    marks = None
    for i in range(12):
        major = i % 3 == 0
        w, r0 = (2.4, 26.0) if major else (1.2, 30.0)
        bar = rz(box(-w / 2, w / 2, r0, 34.0, DIAL_T - 0.4, DIAL_T), -30 * i).translate((0, FACE / 2, 0))
        marks = bar if marks is None else marks.union(bar)
    dial = dial.cut(marks).cut(cyl(CLOCK_SHAFT_HOLE / 2, -1, DIAL_T + 2, 0, FACE / 2))

    def hand(w, tip, hub, hole):
        h = box(-w / 2, w / 2, 0, tip - w / 2, 0, 1.0).union(cyl(w / 2, 0, 1.0, 0, tip - w / 2))
        return h.union(cyl(hub, 0, 1.0)).cut(cyl(hole / 2, -1, 3))

    # minute hand ends on the inner ends of the minor bars (r 30), the hour hand 4 inside the majors (r 22)
    hour = hand(2.4, 22.0, 4.4, HAND_HOLES["hour"])
    minute = hand(1.2, 30.0, 3.4, HAND_HOLES["minute"])

    def on_face(wp, z0, ang=0):
        return to_world(rz(wp, ang).translate((0, FACE / 2, z0)))

    move = box(-MOVE / 2, MOVE / 2, FACE / 2 - MOVE / 2, FACE / 2 + MOVE / 2, -T - MOVE_T, -T)
    move = move.union(cyl(3.5, -T, T + DIAL_T, 0, FACE / 2))

    face_down = lambda wp: rx(to_face(wp), 180)    # face frame, flipped so the body stands on its face
    dial_w = to_world(dial)
    marks_w = to_world(marks)
    mags = [cq_y_cyl(3.0, y0, y0 + 3.0, sx * BOSS_X, boss_z(sx)) for sx in (-1, 1) for y0 in (stop - 3.15, stop + 0.15)]
    return {
        "body": Part(body, face_down(body), OFF),
        "back_plate": Part(plate, rx(plate, -90), OFF),
        "dial": Part(dial_w, rx(dial, 180), PLATE),
        "dial_marks_inlay": Part(marks_w, rx(marks, 180), DARK, anchor="dial"),
        "hand_hour": Part(on_face(hour, DIAL_T + 0.6, 300), hour, DARK),
        "hand_minute": Part(on_face(minute, DIAL_T + 1.8, 48), minute, DARK),
        "movement_ref": Part(to_world(move), None, DARK, ref=True),
        "magnets_ref": Part(cq.Workplane("XY").add(cq.Compound.makeCompound([m.val() for m in mags])), None, (0.5, 0.5, 0.52),
                            qty=4, ref=True),
    }


def boss_z(sx):
    """Height (use frame) where a boss axis meets the plane of the magnet faces."""
    y_stop = DEPTH - T - PAD
    a = math.radians(TILT)
    # boss axis: face point (u = BOSS_U) moving inward along the face normal (cos a, -sin a) in (y, z)
    y0, z0 = BOSS_U * math.cos(a), BOSS_U * math.sin(a)
    s = (y_stop - y0) / math.sin(a)
    return z0 - s * math.cos(a)


def cq_y_cyl(r, y0, y1, x, z):
    """Cylinder along +Y from y0 to y1 at (x, z)."""
    return rx(cyl(r, 0, y1 - y0, x, -z), -90).translate((0, y0, 0))


SAMPLES["001_wedge_desk_clock"] = wedge_desk_clock
