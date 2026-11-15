"""054 Phone charging dock: a block with a slot that holds a phone leaning back, on the end of a USB-C cable.

One part, printed bottom down. The phone slot runs across the whole width and leans back at 1 : 4; its floor is
square to the slope. Under the floor, on the line of the phone's port, a stadium pocket holds the moulding of an
ordinary USB-C cable plug with its tip standing up out of the floor; the plug seats on two shoulders at the
bottom of the pocket. From there a slit, narrower than the moulding, runs back and down to the bottom face and
out through the back: the cable is laid into it from underneath, then the plug is pulled down into the pocket.
"""
import math
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, CH, CH_BED, OFF, DARK,  # noqa: E402
                         box, rrect, rx, feet, plane_yz)

W, D, H = 64.0, 64.0, 40.0       # 16 x 16 x 10 modules
R = 8.0                          # plan radius: 12.5 %
PL, INSET = 2.4, 1.2             # floating plinth
SLOT_W, SLOT_D = 12.0, 12.0      # phone slot: horizontal width at the mouth (a phone up to about 11 thick), depth at the front line
SLOPE = 0.25                     # 1 : 4 back lean
YF = -16.0                       # front line of the slot at the top: the front wall is a quarter of the depth
PORT_OFF = 5.0                   # plug axis in front of the slot's back face: half of an 8 phone + 1 for a thin case (check yours)
POCKET = (12.4, 6.8, 12.0)       # plug moulding 12 x 6.4 + 0.2 per side, 12 of it held (match your plug)
SLIT = 6.4                       # cable slit: narrower than the moulding's 12, so the plug sits on two 3 shoulders
SLIT_TOP = 20.0                  # slit ceiling (45-deg roof above it, apex 2 under the slot floor): room for the cable to bend
TIP = (8.3, 2.5, 6.6)            # USB-C plug shell standing out of the moulding
A = math.atan(SLOPE)
C, S = math.cos(A), math.sin(A)


def lean(wp, origin):
    """A shape built along +Z (axis at the origin) leaned back with the slot and moved to origin (y, z)."""
    return rx(wp, -math.degrees(A)).translate((0, origin[0], origin[1]))


def floor_points():
    fb = (YF - SLOT_D * SLOPE, H - SLOT_D)                      # front corner of the slot floor
    bb = (fb[0] + SLOT_W * C * C, fb[1] - SLOT_W * C * S)       # back corner: floor square to the slope
    return fb, bb


def plug_axis():
    _, bb = floor_points()
    return (bb[0] - PORT_OFF * C, bb[1] + PORT_OFF * S)


def phone(t=8.0, w=72.0, h=150.0):
    """The phone as an envelope (not a part: it is larger than the dock), standing on the floor against the back face."""
    _, bb = floor_points()
    p0 = (bb[0] - 0.2 * C, bb[1] + 0.2 * S)
    pts = [p0, (p0[0] - t * C, p0[1] + t * S)]
    pts += [(pts[1][0] + h * S, pts[1][1] + h * C), (p0[0] + h * S, p0[1] + h * C)]
    return plane_yz(-w / 2).polyline(pts).close().extrude(w)


def phone_dock_charger():
    b = rrect(W - 2 * INSET, D - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    b = b.union(rrect(W, D, R, PL, H - PL).faces("<Z").chamfer(INSET))
    fb, bb = floor_points()
    up = 2.0
    slot = plane_yz(-W / 2 - 1).polyline([fb, bb, (bb[0] + (H + up - bb[1]) * SLOPE, H + up),
                                          (fb[0] + (H + up - fb[1]) * SLOPE, H + up)]).close().extrude(W + 2)
    b = b.cut(slot)
    b = b.faces(">Z").edges().chamfer(CH)
    for x in (-W / 2, W / 2):                                   # the slot's ends in the side faces
        b = b.edges(cq.selectors.BoxSelector((x - 0.05, fb[0] - 0.1, bb[1] - 0.1),
                                             (x + 0.05, fb[0] + (H - fb[1]) * SLOPE + SLOT_W + 0.1, H - CH - 0.05))).chamfer(CH)
    ax = plug_axis()
    pw, pt, pd = POCKET
    pocket = cq.Workplane("XY").workplane(offset=-pd).slot2D(pw, pt, 0).extrude(pd + 3)
    b = b.cut(lean(pocket, ax))
    y0 = ax[0] - pd * S - pt / 2 * C                            # front of the pocket at its bottom
    roof = SLIT / 2
    slit = (cq.Workplane("YZ").workplane(offset=-SLIT / 2)
            .polyline([(y0, -1), (D / 2 + 1, -1), (D / 2 + 1, SLIT_TOP), (y0, SLIT_TOP)]).close().extrude(SLIT))
    slit = slit.union(cq.Workplane("XZ").workplane(offset=-(D / 2 + 1))
                      .polyline([(-roof, SLIT_TOP - 0.01), (roof, SLIT_TOP - 0.01), (0, SLIT_TOP + roof)]).close()
                      .extrude(D / 2 + 1 - y0))
    b = b.cut(slit)
    b = b.edges(cq.selectors.BoxSelector((-roof - 0.1, D / 2 - 0.05, CH_BED + 0.05),     # the slit's edges in the back face
                                         (roof + 0.1, D / 2 + 0.05, SLIT_TOP + roof + 0.1))).chamfer(CH)
    b = feet(b, [(sx * 22, sy * 22) for sx in (-1, 1) for sy in (-1, 1)])

    plug = cq.Workplane("XY").workplane(offset=-pd).slot2D(pw - 0.4, pt - 0.4, 0).extrude(pd)
    plug = plug.union(box(-TIP[0] / 2, TIP[0] / 2, -TIP[1] / 2, TIP[1] / 2, -0.01, TIP[2]))
    return {
        "dock": Part(b, b, OFF),
        "usb_c_plug_ref": Part(lean(plug, ax), None, DARK, ref=True),
    }


SAMPLES["054_phone_dock_charger"] = phone_dock_charger
