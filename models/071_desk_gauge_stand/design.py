"""071 Desk gauge stand: an upright frame for a round panel gauge (a Ø52 body behind a Ø60 bezel) on a low base.

The frame is a sleeve open at the back, printed front face down, so the gauge bore, the cavity behind it and the
open back are all vertical in the print. The gauge goes in from the front and its own clamp bracket grips the
4 thick front wall from inside; the cable leaves through the open back. Two M2 screws come up through
counterbores in the base into pilot holes in the solid lower band of the frame, so no screw shows.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, OFF, DARK,  # noqa: E402
                         box, cyl, rrect, rx, feet, plane_xz)

# the gauge (match yours): Ø52 body, Ø60 bezel 6 deep, 36 deep behind the bezel
G_BODY, G_BEZEL, G_BEZ_H, G_DEPTH = 52.0, 60.0, 6.0, 36.0
BAND = 8.0                              # frame round the bezel (top and sides); the base height
W = G_BEZEL + 2 * BAND                  # 76
LOW = 3 * BAND                          # 24 below the bezel
HF = BAND + G_BEZEL + LOW               # 92 frame height
DF = 40.0                               # frame depth: the gauge (36 behind the bezel) stays 4 inside the open back
R = BAND                                # outline radius = band width (frame top corners, base plan corners)
RI = 3.0                                # inside corners
FRONT = 4.0                             # front wall: 20 layers, inside the clamp range of a panel gauge's bracket
SOLID = 16.0                            # solid lower band of the frame that takes the screws
HB, DB = BAND, 56.0                     # base: 8 high, 8 beyond the frame in front and behind
INSET = 1.2                             # floating plinth
HOLE = G_BODY + 0.5                     # 0.25 per side
SX = 24.0                               # screw positions x ±24 (6 modules)
PILOT, CLEAR, CB_D, CB_H = 1.8, 2.4, 4.2, 1.8


def desk_gauge_stand():
    zc = HB + HF - BAND - G_BEZEL / 2   # dial centre: 62
    yf = -DF / 2                        # front face of the frame
    # frame: front outline in XZ with R on the top corners, square at the bottom where it sits on the base
    prof = (plane_xz(DF / 2).moveTo(-W / 2, HB).lineTo(W / 2, HB).lineTo(W / 2, HB + HF - R)
            .threePointArc((W / 2 - R * 0.29289, HB + HF - R * 0.29289), (W / 2 - R, HB + HF))
            .lineTo(-W / 2 + R, HB + HF)
            .threePointArc((-W / 2 + R * 0.29289, HB + HF - R * 0.29289), (-W / 2, HB + HF - R)).close())
    frame = prof.extrude(DF)
    frame = frame.faces("<Y").chamfer(CH)                   # front face edges (the bed side in the print: CH there is
    frame = frame.faces(">Y").chamfer(CH)                   # the visible value; the elephant's foot hides in it)
    frame = frame.faces("<Z").chamfer(CH)                   # the seam to the base: half of a V line
    cav = (plane_xz(DF / 2 + 1).center(0, (HB + SOLID + HB + HF - T) / 2)
           .rect(W - 2 * T, HF - SOLID - T).extrude(DF - FRONT + 1).edges("|Y").fillet(RI))
    frame = frame.cut(cav)
    frame = frame.cut(plane_xz(yf + FRONT + 1).center(0, zc).circle(HOLE / 2).extrude(FRONT + 2))
    lead = cq.Solid.makeCone(HOLE / 2 + CH + 0.01, HOLE / 2, CH + 0.01, pnt=cq.Vector(0, yf - 0.01, zc), dir=cq.Vector(0, 1, 0))
    frame = frame.cut(cq.Workplane("XY").add(lead))          # C0.5 on the bore's rim, under the bezel
    for s in (-1, 1):
        frame = frame.cut(cyl(PILOT / 2, HB - 0.01, 10.0, s * SX, 0))

    base = rrect(W - 2 * INSET, DB - 2 * INSET, R - INSET, 0, INSET).faces("<Z").chamfer(CH_BED)
    base = base.union(rrect(W, DB, R, INSET, HB - INSET).faces("<Z").chamfer(INSET)).faces(">Z").chamfer(CH)
    for s in (-1, 1):
        base = base.cut(cyl(CLEAR / 2, -1, HB + 2, s * SX, 0)).cut(cyl(CB_D / 2, -1, CB_H + 1, s * SX, 0))
    base = feet(base, [(sx * 26, sy * 18) for sx in (-1, 1) for sy in (-1, 1)])

    gauge = (plane_xz(yf).center(0, zc).circle(G_BEZEL / 2).extrude(G_BEZ_H)
             .union(plane_xz(yf + G_DEPTH).center(0, zc).circle(G_BODY / 2).extrude(G_DEPTH)))
    return {
        "frame": Part(frame, rx(frame, 90), OFF),
        "base": Part(base, base, DARK),
        "gauge_ref": Part(gauge, None, DARK, ref=True),
    }


SAMPLES["071_desk_gauge_stand"] = desk_gauge_stand
