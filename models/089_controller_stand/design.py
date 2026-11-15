"""089 Controller stand: a wedge 100 deep x 72 wide on which a game controller lies face up at 30 deg, its grips against a front lip,
with a small store for its cable or wireless dongle behind a cover held by two magnets.

The stand is one profile (side view) printed on its side, like the stand sample: the 30-deg seat, the 8-thick lip 10 above the
seat, a vertical back. The store is cut into the right-hand (+X) side, which is the top in the print: a 32 x 24 x 12 pocket in a
4-deep recess. A 4-thick cover lies flush in the recess; two 6 x 3 magnets at its ends meet two in the recess floor. A scoop in the
recess edge gives a fingertip the cover's edge.
"""
import math
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, CH, CH_BED, GAP, OFF, copies, rrect, cyl, fillet_at  # noqa: E402

WID = 72.0                               # 18 modules; the controller (about 153 wide) overhangs both sides
Y0, Y1 = -48.0, 52.0                     # front and back: 100 deep
ANG = math.radians(30)
LIP_T, LIP_H = 8.0, 10.0                 # lip 8 thick, 10 above the seat's front end
Z_SEAT = 20.0                            # the seat's front end, at the lip
YS = Y0 + LIP_T + LIP_H * math.sin(ANG)  # the seat's front end; the lip's inner face is square to the seat


def z_seat(y):
    return Z_SEAT + (y - YS) * math.tan(ANG)


END = LIP_T / 2 - 0.2                    # free ends: near full round (stand sample)
R_IN = 2.0                               # the lip's inside corner: small, so the controller's edge sits right in it
# store, in print coordinates (X = assembled y, Y = assembled z, Z = assembled x + WID/2: the +X side is up)
REC = (-2.0, 48.0, 6.0, 30.0)            # recess 50 x 24 (X0, X1, Y0, Y1), R3.8 = the free ends
REC_D, REC_R = 4.4, 3.8                  # cover 4.15 thick: 0.95 over its magnets
POCKET = (7.0, 39.0, 6.0, 30.0, 12.0)    # pocket 32 x 24, 12 deep below the recess floor
MAG_X = (2.5, 43.5)                      # magnet centres: in the recess ends beyond the pocket
MAG_Y = 18.0
MAG_R, MAG_D = 3.1, 3.2


def display(wp):
    """Print coordinates -> assembled: X_print -> y, Y_print -> z, Z_print -> x + WID/2."""
    return wp.rotate((0, 0, 0), (1, 1, 1), 120).translate((-WID / 2, 0, 0))


def rec_plan(x0, x1, y0, y1, r, z0, t):
    return rrect(x1 - x0, y1 - y0, r, z0, t, (x0 + x1) / 2, (y0 + y1) / 2)


def controller_envelope():
    """A controller lying face up on the seat, its edge in the lip's corner: 104 along the slope, 61 thick (print coordinates)."""
    c, s = math.cos(ANG), math.sin(ANG)
    p0 = (YS, Z_SEAT)
    pts = [p0, (p0[0] + 104 * c, p0[1] + 104 * s), (p0[0] + 104 * c - 61 * s, p0[1] + 104 * s + 61 * c), (p0[0] - 61 * s, p0[1] + 61 * c)]
    return cq.Workplane("XY").polyline(pts).close().extrude(153).translate((0, 0.05, WID / 2 - 76.5))


def controller_stand():
    P = {"fb": (Y0, 0), "bb": (Y1, 0), "bt": (Y1, z_seat(Y1)), "sf": (YS, Z_SEAT),
         "li": (YS - LIP_H * math.sin(ANG), Z_SEAT + LIP_H * math.cos(ANG)), "lf": (Y0, Z_SEAT + LIP_H * math.cos(ANG))}
    order = ["fb", "bb", "bt", "sf", "li", "lf"]
    s = cq.Workplane("XY").polyline([P[k] for k in order]).close().extrude(WID)
    for k, r in {"fb": END, "bb": END, "bt": END, "li": END, "lf": END, "sf": R_IN}.items():
        s = fillet_at(s, P[k], r, WID + 1)
    s = s.faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)

    x0, x1, y0, y1 = REC
    def opening(z0, t):                                                      # the recess with its fingertip scoop at the upper edge
        return rec_plan(x0, x1, y0, y1, REC_R, z0, t).union(cyl(7.0, z0, t, (x0 + x1) / 2, y1))
    s = s.cut(opening(WID - REC_D, REC_D + 1))
    w0 = opening(WID - CH - .01, 1).faces("<Z").wires().val()
    w1 = w0.offset2D(CH + .01, "arc")[0].translate(cq.Vector(0, 0, CH + .02))
    s = s.cut(cq.Workplane("XY").add(cq.Solid.makeLoft([w0, w1], True)))        # its outline: C0.5 as a flare, half of the V
    px0, px1, py0, py1, pd = POCKET
    s = s.cut(rec_plan(px0, px1, py0, py1, REC_R, WID - REC_D - pd, pd + 1))
    for mx in MAG_X:
        s = s.cut(cyl(MAG_R, WID - REC_D - MAG_D, MAG_D + .01, mx, MAG_Y))      # opens upward in the print

    g = GAP
    cover = rec_plan(x0 + g, x1 - g, y0 + g, y1 - g, REC_R - g, WID - REC_D + g, REC_D - g)
    cover = cover.faces(">Z").chamfer(CH)
    for mx in MAG_X:
        cover = cover.cut(cyl(MAG_R, WID - REC_D + g - .01, MAG_D + .01, mx, MAG_Y))
    cover_print = cover.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, WID))

    mags = []
    for mx in MAG_X:
        mags.append(cyl(3.0, WID - REC_D - MAG_D + 0.1, 3.0, mx, MAG_Y))       # in the stand
        mags.append(cyl(3.0, WID - REC_D + g + 0.1, 3.0, mx, MAG_Y))           # in the cover
    return {
        "stand": Part(display(s), s, OFF),
        "cover": Part(display(cover), cover_print, OFF),
        "magnet_ref": Part(display(copies(mags)), None, (0.55, 0.56, 0.6), ref=True, qty=4),
    }


SAMPLES["089_controller_stand"] = controller_stand
