"""088 AA battery box: a 76 x 68 x 24 enclosure for a bought 4 x AA holder with wire leads, its lid sliding in a dovetail and
held by a printed snap tab.

The holder lies on the floor (stuck with its own foam tape). The lid slides in along X from the +X end: a 45-deg-ish dovetail in two
rails at the top of the long walls keeps it from lifting, the rails' flat tops below the groove seat it from below, and its +X end
fills the outline as the top of the end wall. A block inside the +X end wall carries a notch across its top; a cantilever tab freed
from the lid by a U slit drops a 45-deg bump into it. The leads leave through a small stadium hole in the -X end.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, box, rrect, plane_yz, plane_xz  # noqa: E402

L, W, H, R = 76.0, 68.0, 24.0, 12.0     # 19 x 17 modules; R12 = 15.8 %
FLOOR = 2.4
DT = 2.4                                 # lid thickness
DOVE = 1.2                               # dovetail undercut over DT (27 deg from vertical)
xi, yi = L / 2 - T, W / 2 - T            # inner faces
yr = yi - DIV                            # rails' inner face
ZL = H - DT                              # lid bottom
ZG = ZL - GAP                            # groove floor = the rails' and the block's top under the lid (the seat)
ZR = ZG - 1.4                            # rail's flat inner face ends here; 45 deg below to the wall
BLOCK = 4.2                              # latch block inside the +X end wall
xb = xi - BLOCK
XN = xb + BLOCK / 2                      # notch centre
BUMP = 0.85                              # catch = BUMP - GAP = 0.6, for a cover that is handled
TAB_L, TAB_W = 16.0, 10.0                # tab: root at XN - TAB_L + 1.5, free end just past the bump
HOLDER = (63.0, 57.5, 15.5)              # a common 4 x AA flat holder; measure yours
WIRE = (4.0, 2.0, 21.75, FLOOR + 8.0)    # stadium w x h at (y, z): two 26 AWG leads side by side


def holder_ref():
    hl, hw, hh = HOLDER
    x0 = xb - 0.5 - hl                  # against the block: its square corners clear the R9.48 corners at -X
    h = box(x0, x0 + hl, -hw / 2, hw / 2, FLOOR, FLOOR + hh)
    for y in (-21.75, -7.25, 7.25, 21.75):
        cell = plane_yz(x0 + 6.25).center(y, FLOOR + 1.0 + 7.25).circle(7.25).extrude(50.5)
        h = h.cut(plane_yz(x0 + 2).center(y, FLOOR + 1.0 + 7.25).circle(7.6).extrude(hl - 4)).union(cell)
    return h


def trap(h_top, h_bot, z_bot, z_top, x_a, x_b):
    """Dovetail section, half width h_top at z_top and h_bot at z_bot, extruded along X."""
    return plane_yz(x_a).polyline([(-h_bot, z_bot), (h_bot, z_bot), (h_top, z_top), (-h_top, z_top)]).close().extrude(x_b - x_a)


def wire_wp(x):
    w, h, y, z = WIRE
    return plane_yz(x).center(y, z).slot2D(w, h, 0)


def battery_box_aa():
    outline = rrect(L, W, R, -1, H + 2)
    cav = rrect(L - 2 * T, W - 2 * T, R - T, FLOOR, H + 1)
    body = rrect(L, W, R, 0, H).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH).cut(cav)
    for s in (-1, 1):                                                       # rails: flat seat, 45-deg underside
        prof = [(s * yr, H), (s * (yi + .01), H), (s * (yi + .01), ZR - DIV), (s * yr, ZR)]
        body = body.union(plane_yz(-L / 2).polyline(prof).close().extrude(L).intersect(outline))
    body = body.union(box(xb, xi + .01, -W, W, FLOOR - .01, H).intersect(rrect(L - 2 * T, W - 2 * T, R - T, FLOOR - .01, H)))

    k = DOVE / DT
    env = trap(yr, yr + k * (DT + GAP), ZG, H + .01, -L / 2, L / 2 + 5)    # the lid's path: clipped to the cavity at -X
    env = env.intersect(cav.union(box(0, L, -W, W, 0, H + 2)))
    body = body.cut(env)
    w0 = env.faces(">Z").wires().val().translate(cq.Vector(0, 0, -CH - .01))   # the groove's top edges: a 45-deg flare (half of the V)
    w1 = env.faces(">Z").wires().val().translate(cq.Vector(0, 0, -.01))
    w1 = cq.Workplane("XY").add(w1).toPending().offset2D(CH + .01, "intersection").wires().val()
    body = body.cut(cq.Workplane("XY").add(cq.Solid.makeLoft([w0, w1], True)))
    body = body.cut(box(XN - 0.9, XN + 0.9, -yr, yr, ZG - BUMP - 0.1, ZG + .01))   # notch for the bump, open upward
    body = body.cut(wire_wp(-L / 2 - 1).extrude(T + 2))                     # leads out through the -X end
    w0 = wire_wp(-L / 2 + CH).wires().val()
    w1 = wire_wp(-L / 2 - .01).offset2D(CH + .01, "intersection").wires().val()
    body = body.cut(cq.Workplane("XY").add(cq.Solid.makeLoft([w0, w1], True)))

    hw_top, hw_bot = yr - GAP, yr - GAP + DOVE
    lid = trap(hw_top, hw_bot, ZL, H, -L / 2, L / 2 + 1)
    lid = lid.intersect(rrect(L - 2 * (T + GAP), W - 2 * (T + GAP), R - T - GAP, 0, H + 1).intersect(box(-L, 0, -W, W, 0, H + 1))
                        .union(rrect(L, W, R, 0, H + 1).intersect(box(0, L, -W, W, 0, H + 1))))
    lid = lid.faces(">Z").chamfer(CH)
    tx1 = XN + 1.5
    tx0 = tx1 - TAB_L
    tw = TAB_W / 2
    for c in (box(tx0, tx1 + 1, tw, tw + 1, ZL - 1, H + 1), box(tx0, tx1 + 1, -tw - 1, -tw, ZL - 1, H + 1),
              box(tx1, tx1 + 1, -tw - 1, tw + 1, ZL - 1, H + 1)):
        lid = lid.cut(c)
    bump = plane_xz(-(tw - 0.5)).polyline([(XN - BUMP, ZL), (XN + BUMP, ZL), (XN, ZL - BUMP)]).close().extrude(-(2 * tw - 1))
    lid = lid.union(bump)
    lid = lid.cut(box(tx1 - 7, tx1 - 3, -3, 3, H - 0.6, H + .01))         # thumb grip on the tab
    lid_print = lid.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, H))

    return {
        "body": Part(body, body, OFF),
        "lid": Part(lid, lid_print, OFF),
        "holder_ref": Part(holder_ref(), None, (0.25, 0.25, 0.27), ref=True),
    }


SAMPLES["088_battery_box_aa"] = battery_box_aa
