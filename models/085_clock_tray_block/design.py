"""085 Clock tray block: a desk clock whose front half is a shallow tray for keys, rings and coins.

One body, 96 square in plan and printed bottom down: a tray 12 high in front, a block 80 high behind it. The block is a sleeve
open at the top; the quartz movement goes in from above and is clamped to the inside of its front wall by the shaft nut, through
the dial disc on the outside. A lid with a lip inside the walls locates on top (the way to the battery). The dial faces the
room over the tray.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, PLATE, DARK, ACC,  # noqa: E402
                         CLOCK_SHAFT_HOLE, HAND_HOLES, box, cyl, rrect, rx, rz, feet, fillet_at)

S, R = 96.0, 12.0                   # plan 96 square, R12 = 12.5 %
PL, INSET = 2.4, 1.2                # floating plinth
HT, HB = 12.0, 80.0                 # tray rim height, block height
YB = 8.0                            # the block's front face: the block is 40 deep, the tray 56
FLOOR = 4.0                         # tray floor (8 deep) and the block's inside floor
RI = 3.0                            # inside corners
DIAL_D, DIAL_T = 48.0, 2.4          # dial: 10 of margin above it (to the top) and below it (to the tray rim)
ZC = (HT + HB) / 2                  # dial centre, z 46
MOVE, MOVE_T = 56.0, 16.0           # common quartz movement (check yours)
LID_T, LIP = 2.4, 4.0
K = 0.70710678


def block_plan(w, r, y0, z0, h):
    """The plan of the outline (or an offset of it) behind y0."""
    return rrect(w, w, r, z0, h).intersect(box(-S, S, y0, S, z0 - 1, z0 + h + 1))


def teardrop_y(x, z, y0, length, r):
    """Round hole along +Y with a 45-deg roof toward +Z."""
    tri = [(x - r * K, z + r * K), (x, z + r * 1.41421356), (x + r * K, z + r * K), (x, z)]
    wp = cq.Workplane("XZ").workplane(offset=-y0 - length)
    return wp.center(x, z).circle(r).extrude(length).union(wp.polyline(tri).close().extrude(length))


def at_xy(wp, x, y, r):
    return fillet_at(wp, (x, y), r)


def clock_tray_block():
    b = rrect(S - 2 * INSET, S - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    b = b.union(rrect(S, S, R, PL, HT - PL).faces("<Z").chamfer(INSET))
    b = b.union(block_plan(S, R, YB, HT - 0.01, HB - HT + 0.01))
    b = b.edges("|Z").edges(cq.selectors.BoxSelector((-S, YB - 0.01, HT + 1), (S, YB + 0.01, HB))).chamfer(CH)   # block's front corners
    b = b.edges(cq.selectors.BoxSelector((-S, -S, HT - 0.01), (S, YB - 0.5, HT + 0.01))).chamfer(CH)   # tray's outer rim
    xi = S / 2 - T
    tray = box(-xi, xi, -xi, YB, FLOOR, HB)
    tray = at_xy(at_xy(tray, -xi, -xi, R - T), xi, -xi, R - T)                   # front: concentric with the outline
    tray = at_xy(at_xy(tray, -xi, YB, RI), xi, YB, RI)
    b = b.cut(tray.intersect(box(-S, S, -S, YB, FLOOR, HT + 1)))
    b = b.cut(block_plan(S - 2 * T, R - T, YB + T, FLOOR, HB))                   # the sleeve, open at the top
    b = b.faces(">Z").edges().chamfer(CH)
    w0 = tray.faces("<Z").wires().val().translate(cq.Vector(0, 0, HT - CH - FLOOR))
    w1 = w0.offset2D(CH + 0.01, "arc")[0].translate(cq.Vector(0, 0, CH + 0.01))
    rim = cq.Workplane("XY").add(cq.Solid.makeLoft([w0, w1], True))            # the tray's inner rim: C0.5 cut as a 45-deg flare
    b = b.cut(rim.intersect(box(-S, S, -S, YB, 0, HB)))
    b = b.cut(teardrop_y(0, ZC, YB - 1, T + 2, CLOCK_SHAFT_HOLE / 2))
    b = feet(b, [(sx * 36.0, sy * 36.0) for sx in (-1, 1) for sy in (-1, 1)])

    lid = block_plan(S, R, YB, HB, LID_T).faces(">Z").edges().chamfer(CH_BED).faces("<Z").edges().chamfer(CH)
    lip = block_plan(S - 2 * (T + GAP), R - T - GAP, YB + T + GAP, HB - LIP, LIP + 0.01)
    lip = lip.cut(block_plan(S - 2 * (T + GAP + DIV), R - T - GAP - DIV, YB + T + GAP + DIV, HB - LIP - 1, LIP + 2))
    lid = lid.union(lip)

    # dial, built face up in XY (centre at the origin), then stood on the front face
    dial = cyl(DIAL_D / 2, 0, DIAL_T).faces(">Z").edges().chamfer(CH)
    marks = top = None
    for i in range(12):
        w, r0 = (2.4, 15.0) if i % 3 == 0 else (1.2, 18.0)       # majors 2.4 x 6, minors 1.2 x 3, ending 3 inside the rim
        bar = rz(box(-w / 2, w / 2, r0, 21.0, DIAL_T - 0.4, DIAL_T), -30 * i)
        if i == 0:
            top = bar
        else:
            marks = bar if marks is None else marks.union(bar)
    dial = dial.cut(marks).cut(top).cut(cyl(CLOCK_SHAFT_HOLE / 2, -1, DIAL_T + 2))

    def hand(w, tip, hub, hole):
        h = box(-w / 2, w / 2, 0, tip - w / 2, 0, 1.0).union(cyl(w / 2, 0, 1.0, 0, tip - w / 2))
        return h.union(cyl(hub, 0, 1.0)).cut(cyl(hole / 2, -1, 3))

    minute = hand(1.2, 18.0, 3.4, HAND_HOLES["minute"])       # ends on the inner ends of the minor bars
    hour = hand(2.4, 13.5, 4.4, HAND_HOLES["hour"])           # 3/4 of the minute hand

    def on_face(wp, out, ang=0):
        """XY frame, +Z out of the face -> the front face of the block, out mm in front of y = YB."""
        return rx(rz(wp, ang), 90).translate((0, YB - out, ZC))

    move = box(-MOVE / 2, MOVE / 2, YB + T, YB + T + MOVE_T, ZC - MOVE / 2, ZC + MOVE / 2)
    move = move.union(rx(cyl(3.5, 0, T + DIAL_T), 90).translate((0, YB + T, ZC)))   # threaded shaft through wall and dial
    return {
        "body": Part(b, b, OFF),
        "lid": Part(lid, rx(lid, 180), OFF),
        "dial": Part(on_face(dial, 0), rx(dial, 180), PLATE),
        "dial_marks_inlay": Part(on_face(marks, 0), rx(marks, 180), DARK, anchor="dial"),
        "dial_top_mark_inlay": Part(on_face(top, 0), rx(top, 180), ACC, anchor="dial"),
        "hand_hour": Part(on_face(hour, DIAL_T + 0.6, 300), hour, DARK),
        "hand_minute": Part(on_face(minute, DIAL_T + 1.8, 48), minute, DARK),
        "movement_ref": Part(move, None, DARK, ref=True),
    }


SAMPLES["085_clock_tray_block"] = clock_tray_block
