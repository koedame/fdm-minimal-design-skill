"""068 Under-desk drawer: a shallow drawer that hangs under a desk top on two dovetail ledges.

Two parts. The housing is a 4 thick plate screwed to the underside of the desk with two side walls and a back
wall; each side wall ends in a ledge with a 45-deg top face. The drawer is an open box whose top edge widens 2.4
on both sides with a 45-deg underside, so it hangs on the ledges and centres itself on them; the plate keeps it
from lifting. The drawer slides out to the front. A small bump under the plate rides in a shallow channel along
the top of each drawer side; the channel ends 120 back, so the drawer stops there with 40 still in the housing,
and a firm pull takes it past the bump and out. A U notch in the front wall's top edge takes the fingers.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, GAP, OFF, rrect, box, rx, plane_xz, plane_yz)  # noqa: E402

W, D, H = 140.0, 160.0, 52.0      # housing width and depth, overall height (desk underside at z = H)
TP = 4.0                          # plate: takes 90-deg countersunk M4 wood screws flush
WD = 128.0                        # drawer width (32 modules)
R = 8.0                           # drawer corners; the housing's back corners are concentric
E = 2.4                           # dovetail: the drawer's top edge widens E on each side at 45 deg
BAND = 1.2                        # straight part of the widened edge above the slope
LEDGE = 2.4                       # ledge thickness under the slope
FLOOR = 2.4
R_IN = 3.0
HD = WD / 2
ZT = H - TP - GAP                 # drawer top, GAP under the plate
Z0 = ZT - BAND - E                # foot of the drawer's slope
SG = GAP * 2 ** 0.5               # vertical offset that gives GAP across a 45-deg face
ZL = Z0 - SG + GAP                # housing slope at x = HD + GAP: the drawer's slope moved SG down
ZB = ZL - LEDGE                   # housing bottom
WT = W / 2 - HD - E - GAP         # housing side wall, 3.35
DD = D - T - GAP                  # drawer depth: up to GAP before the housing's back wall
YD = -D / 2 + DD / 2              # drawer centre, closed
NOTCH_R = 16.0                    # finger notch (as 062)
XC = HD + (E - T) / 2             # centre of the drawer's top edge
YB = -D / 2 + 6.0                 # bump under the plate, near the front
STOP = 120.0                      # travel to the stop: 40 of the 157 drawer stays in the housing
BUMP = 0.6                        # bump height; the channel is as deep, so 0.25 stays above the bump
SCREWS = [(sx * (HD - 16), sy * (D / 2 - 24)) for sx in (-1, 1) for sy in (-1, 1)]


def housing():
    hb = rrect(W, D, R + E + GAP + WT, ZB, H - ZB)
    hb = hb.cut(box(-W, W, -D - 1, -D / 2, ZB - 1, H + 1))                    # square front: the channel's cut end
    hb = hb.union(box(-W / 2, W / 2, -D / 2, 0, ZB, H))
    a, b = HD + GAP, HD + E + GAP
    cav = plane_xz(D / 2 - T).polyline([(-a, ZB - 1), (a, ZB - 1), (a, ZL), (b, ZL + E), (b, H - TP),
                                        (-b, H - TP), (-b, ZL + E), (-a, ZL)]).close().extrude(D)
    hb = hb.cut(cav)
    hb = hb.edges("|Z").edges(cq.selectors.BoxSelector((-W, -D, ZB - 1), (W, -D / 2 + 0.1, H + 1))).chamfer(CH)
    hb = hb.faces(">Z").edges().chamfer(CH_BED).faces("<Z").edges().chamfer(CH)
    for (x, y) in SCREWS:                                                     # through Ø4.5, 90-deg countersink Ø8.5
        hb = hb.cut(cq.Workplane("XY").workplane(offset=H - TP - 1).center(x, y).circle(2.25).extrude(TP + 2))
        hb = hb.cut(cq.Workplane("XY").add(cq.Solid.makeCone(4.25 + 0.01, 0, 4.26, pnt=cq.Vector(x, y, H - TP - 0.01))))
    for s in (-1, 1):
        bump = plane_yz(s * XC - 0.8).polyline([(YB - BUMP, H - TP + 0.01), (YB + BUMP, H - TP + 0.01),
                                               (YB, H - TP - BUMP)]).close().extrude(1.6)
        hb = hb.union(bump)
    return hb


def drawer():
    dr = rrect(WD, DD, R, 0, ZT, 0, YD)
    band = plane_xz(D).polyline([(-HD, Z0 - 0.01), (HD, Z0 - 0.01), (HD + E, Z0 + E), (HD + E, ZT),
                                 (-HD - E, ZT), (-HD - E, Z0 + E)]).close().extrude(2 * D)
    dr = dr.union(band.intersect(rrect(WD + 2 * E, DD, R + E, Z0 - 1, ZT - Z0 + 1, 0, YD)))
    dr = dr.cut(rrect(WD - 2 * T, DD - 2 * T, R - T, FLOOR, ZT, 0, YD).faces("<Z").edges().fillet(R_IN))
    dr = dr.faces(">Z").edges().chamfer(CH).faces("<Z").edges().chamfer(CH_BED)
    dr = dr.cut(plane_xz(-D / 2 + T + 1).center(0, ZT).circle(NOTCH_R).extrude(T + 2))
    for y in (-D / 2, -D / 2 + T):
        dr = dr.edges(cq.selectors.BoxSelector((-NOTCH_R - 0.1, y - 0.05, ZT - NOTCH_R - 0.1),
                                               (NOTCH_R + 0.1, y + 0.05, ZT - CH - 0.05))).chamfer(CH)
    ye = YB + STOP                                                            # channel end, closed position
    for s in (-1, 1):
        ch = plane_yz(s * XC - 1.2).polyline([(-D, ZT + 0.01), (ye + BUMP, ZT + 0.01), (ye, ZT - BUMP),
                                              (-D, ZT - BUMP)]).close().extrude(2.4)
        dr = dr.cut(ch)
    return dr


def under_desk_drawer():
    hb, dr = housing(), drawer()
    return {
        "housing": Part(hb, rx(hb, 180), OFF),
        "drawer": Part(dr, dr, OFF),
    }


SAMPLES["068_drawer_under_desk"] = under_desk_drawer
