"""087 Slotted soap dish: a 112 x 80 tray whose bar of soap rests on ribs, the water running out through slots in the front wall.

The floor falls 2 from the back to the front. Eight ribs with round tops run from the back toward the front and hold the soap level,
8 above the floor at the back; they stop 4 short of the front wall, leaving a gutter along it. Seven vertical slots with round ends
through the front wall drain the gutter, their lower ends below the floor so no water stands at them. Placed with the slotted side
toward the basin, the dish dries between uses. No mechanism: one printed part.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, DIV, CH, CH_BED, OFF, box, rrect, plane_xz, plane_yz  # noqa: E402

L, W, R, H = 112.0, 80.0, 12.0, 24.0   # 28 x 20 modules, R12 = 10.7 %; 24 high
PL, INSET = 2.4, 1.2                   # floating plinth
Z_FRONT, Z_BACK = 4.0, 6.0             # floor top at the front and at the back: 2 of fall over 75
Z_RIB = 12.0                           # rib tops, level: the soap sits 12 deep in the walls
PITCH, N_RIB = 12.0, 8                 # ribs at x = +-6, +-18, +-30, +-42
GUTTER = 4.0                           # the ribs stop 4 short of the front wall
SLOT_W = 3.2                           # drain slots: wide enough that water does not bridge them
SLOT_X = (-36.0, -24.0, -12.0, 0.0, 12.0, 24.0, 36.0)   # one at the end of every channel between the ribs


def slot_wp(y, x):
    """One drain slot's outline on the plane y: round bottom 1.6 below the front floor, straight up to the rib tops, 45-deg roof."""
    r, k = SLOT_W / 2, 0.70710678
    zb, zt = Z_FRONT, Z_RIB                                                # centres of the bottom arc and of the roof's circle
    return (plane_xz(y).moveTo(x - r, zb).lineTo(x - r, zt)
            .threePointArc((x - r * 0.92388, zt + r * 0.38268), (x - r * k, zt + r * k))
            .lineTo(x, zt + r * 1.41421356).lineTo(x + r * k, zt + r * k)
            .threePointArc((x + r * 0.92388, zt + r * 0.38268), (x + r, zt))
            .lineTo(x + r, zb).threePointArc((x, zb - r), (x - r, zb)).close())


def soap_dish_slotted():
    xi, yi = L / 2 - T, W / 2 - T
    b = rrect(L - 2 * INSET, W - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    b = b.union(rrect(L, W, R, PL, H - PL).faces("<Z").chamfer(INSET))
    b = b.cut(rrect(L - 2 * T, W - 2 * T, R - T, Z_FRONT, H))
    ramp = plane_yz(-L / 2).polyline([(-yi - 1, Z_FRONT - 1), (yi + 1, Z_FRONT - 1), (yi + 1, Z_BACK),
                                      (-yi - 1, Z_FRONT)]).close().extrude(L)
    b = b.union(ramp.intersect(rrect(L - 2 * T + 0.02, W - 2 * T + 0.02, R - T + 0.01, Z_FRONT - 1, Z_BACK + 1)))
    b = b.faces(">Z").edges().chamfer(CH)                                  # outer and inner rim
    y0, y1 = -yi + GUTTER, yi + 0.5
    r = DIV / 2
    for i in range(N_RIB):
        x = (i - (N_RIB - 1) / 2) * PITCH
        rib = box(x - r, x + r, y0, y1, Z_FRONT - 0.5, Z_RIB - r)
        rib = rib.union(plane_xz(y1).center(x, Z_RIB - r).circle(r).extrude(y1 - y0))   # plane_xz extrudes toward -Y
        b = b.union(rib)
    for x in SLOT_X:                                                       # teardrop tops (Ø3.2 > 2); C0.5 flares at both faces
        b = b.cut(slot_wp(-yi + 1.0, x).extrude(T + 2))
        for y0f, y1f in ((-W / 2 + CH, -W / 2 - 0.01), (-yi - CH, -yi + 0.01)):
            w0 = slot_wp(y0f, x).wires().val()
            w1 = slot_wp(y1f, x).offset2D(CH + 0.01, "intersection").wires().val()
            b = b.cut(cq.Workplane("XY").add(cq.Solid.makeLoft([w0, w1], True)))
    return {"dish": Part(b, b, OFF)}


SAMPLES["087_soap_dish_slotted"] = soap_dish_slotted
