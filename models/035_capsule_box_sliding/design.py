"""035 Capsule box: a 120 x 40 x 20 box, round at both ends, with two dividers and a sliding lid.

The lid runs in the 45-deg dovetail of 08 along the walls and slides out through the right end. It rests
on a narrow ring with a 45-deg underside and on the tops of the two dividers, which reach up to it, so a
small thing cannot cross from one cell into the next with the lid shut. A low ridge on the right divider
clicks into a groove under the lid and holds it closed. The dividers split the length into thirds.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, box, plane_xz  # noqa: E402

L, W, H = 120.0, 40.0, 20.0         # 6 : 2 : 1; full round ends (R = W / 2)
FLOOR = 2.4
LIP = 1.2                           # the wall top steps 1.2 inward: the dovetail's upper half (as 08)
ZL0, DT = H - 3.6, 1.2              # lid bottom, dovetail height; the lid is 3.6 thick
ZD = ZL0 + DT
SLOPE_GAP = GAP * 2 ** 0.5
XO = L / 2 + 20                     # the lid and its clearance run out past the right end
RING = 1.6                          # lid seat inside the walls
RIDGE_H = 0.4
XD = L / 6                          # dividers at +-20: three cells of equal length, on the grid


def stad(length, width, z0, h, cx=0.0):
    """Stadium (full round ends) of overall length x width, from z0 up h, centred on x = cx."""
    return cq.Workplane("XY").workplane(offset=z0).center(cx, 0).slot2D(length, width, 0).extrude(h)


def stad_wire(length, width, z, cx=0.0):
    return cq.Workplane("XY").workplane(offset=z).center(cx, 0).slot2D(length, width, 0).wires().val()


def lid_span(off):
    x0 = -(L / 2 - T - LIP - GAP) - off
    w = W - 2 * (T + LIP + GAP) + 2 * off
    return x0, w


def lid_plan(off, z0, h):
    x0, w = lid_span(off)
    return stad(XO - x0, w, z0, h, (XO + x0) / 2)


def loft(off0, z0, off1, z1):
    (a0, w0), (a1, w1) = lid_span(off0), lid_span(off1)
    return cq.Workplane("XY").add(cq.Solid.makeLoft(
        [stad_wire(XO - a0, w0, z0, (XO + a0) / 2), stad_wire(XO - a1, w1, z1, (XO + a1) / 2)], True))


def prism_y(x, z, pts, length):
    return plane_xz(length / 2).polyline([(x + a, z + b) for a, b in pts]).close().extrude(length)


def capsule_box_sliding():
    outline = stad(L, W, -1, H + 2)
    body = stad(L, W, 0, H).cut(stad(L - 2 * T, W - 2 * T, FLOOR, ZL0 - FLOOR))
    body = body.cut(lid_plan(GAP, ZD + 0.1, H + 1 - ZD).union(loft(DT + SLOPE_GAP + GAP, ZL0 - GAP, GAP, ZD + 0.1)))
    z1 = ZL0 - GAP                  # the lid rests on the ring and the dividers
    ring = stad(L - 2 * T, W - 2 * T, z1 - RING, RING)
    cone = cq.Solid.makeLoft([stad_wire(L - 2 * T + 0.02, W - 2 * T + 0.02, z1 - RING - 0.001),
                              stad_wire(L - 2 * T - 2 * RING, W - 2 * T - 2 * RING, z1 + 0.001)], True)
    body = body.union(ring.cut(cq.Workplane("XY").add(cone)))
    cav = stad(L - 2 * T, W - 2 * T, FLOOR - 0.01, z1 - FLOOR + 0.01)
    for x in (-XD, XD):
        body = body.union(box(x - DIV / 2, x + DIV / 2, -W, W, FLOOR - 0.01, z1).intersect(cav))
    body = body.faces("<Z").edges().chamfer(CH_BED)
    body = body.edges(cq.selectors.BoxSelector((-L, -W, H - 0.01), (L, W, H + 0.01))).chamfer(CH)
    hw = W / 2 - T - 2.0            # ridge across the right divider's top, clear of the ring
    body = body.union(prism_y(XD, z1 - 0.01, [(-RIDGE_H, 0), (RIDGE_H, 0), (0, RIDGE_H + 0.01)], 2 * hw))

    lid = lid_plan(0, ZD, H - ZD).union(loft(DT, ZL0, 0, ZD)).intersect(outline)
    lid = lid.faces("<Z").edges().chamfer(CH_BED)
    lid = lid.faces(">Z").edges().chamfer(CH)
    lid = lid.cut(prism_y(XD, ZL0 - 0.01, [(-0.8, 0), (0.8, 0), (0, 0.81)], 2 * hw + 1))
    lid = lid.cut(stad(20.0, 8.0, H - 1.2, 2.0, L / 2 - 14.0).rotate((L / 2 - 14.0, 0, 0), (L / 2 - 14.0, 0, 1), 90))
    return {
        "body": Part(body, body, OFF),
        "lid": Part(lid, lid, OFF),
    }


SAMPLES["035_capsule_box_sliding"] = capsule_box_sliding
