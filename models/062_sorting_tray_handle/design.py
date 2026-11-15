"""062 Sorting tray with handle notches: six equal cells for screws and small parts, lifted by two notches.

One part, printed bottom down. 144 x 96 x 32 (3 : 2, height = depth / 3) on a floating plinth. Two dividers
across and one along split the inside into three columns and two rows of equal cells; the cells' floor
edges are rounded R3 so a fingertip sweeps the last screw out. The long walls have a U notch at the middle,
as wide as the tray is high and half as deep: fingers go in over the wall at the
notch and the thumb stays outside, so the tray is lifted level from a full drawer or a crowded bench.
"""
import os
import sys

from cadquery.selectors import BoxSelector

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, OFF, box, rrect, fillet_at, plane_xz, plane_yz)  # noqa: E402

W, D, H = 144.0, 96.0, 32.0       # 3 : 2, height = D / 3; 36 x 24 modules
R = 12.0                          # 12.5 % of the depth
FLOOR = 2.4
DIV_H = H - 4.0                   # dividers 4 below the rim, as in the sample tray
R_IN = 3.0                        # cell corners and floor edges
PL, INSET = 2.4, 1.2              # floating plinth
NOTCH_W = 32.0                    # U notch: 32 wide, R16 bottom, to half the height
NOTCH_R = NOTCH_W / 2


def sorting_tray_handle():
    xi, yi = W / 2 - T, D / 2 - T
    col = (2 * xi - 2 * DIV) / 3                         # three equal columns
    row = (2 * yi - DIV) / 2                             # two equal rows
    body = rrect(W - 2 * INSET, D - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    body = body.union(rrect(W, D, R, PL, H - PL).faces("<Z").chamfer(INSET))
    xs = [-xi, -xi + col, -xi + col + DIV, -xi + 2 * col + DIV, -xi + 2 * col + 2 * DIV, xi]
    ys = [-yi, -yi + row, -yi + row + DIV, yi]
    for i in range(3):
        for j in range(2):
            x0, x1, y0, y1 = xs[2 * i], xs[2 * i + 1], ys[2 * j], ys[2 * j + 1]
            c = box(x0, x1, y0, y1, FLOOR, H + 1)
            for (x, y) in ((x0, y0), (x0, y1), (x1, y0), (x1, y1)):
                r = R - T if abs(x) > xi - 0.01 and abs(y) > yi - 0.01 else R_IN
                c = fillet_at(c, (x, y), r, H + 2)
            body = body.cut(c.faces("<Z").edges().fillet(R_IN - 0.05))
    body = body.cut(rrect(2 * xi, 2 * yi, R - T, DIV_H, H))             # dividers stop 4 below the rim
    # U notches in the long walls: a semicircle centred on the rim, down to half the height
    u = plane_xz(D / 2 + 1).center(0, H).circle(NOTCH_R).extrude(T + 2)
    body = body.cut(u).cut(u.mirror("XZ"))
    body = body.faces(">Z").edges().chamfer(CH)                          # rim, inner and outer
    # divider tops: a 45-deg prism along each top edge (chamfer() fails on this many edges), ending at the crossing divider
    def lead(plane, u, s, length):
        return plane.polyline([(u - s * 0.01, DIV_H + 0.01), (u + s * CH, DIV_H + 0.01), (u - s * 0.01, DIV_H - CH)]) \
            .close().extrude(length)
    for (xa, xb) in ((xs[0], xs[1]), (xs[2], xs[3]), (xs[4], xs[5])):
        for y, s in ((ys[1], -1), (ys[2], 1)):
            body = body.cut(lead(plane_yz(xa), y, s, xb - xa))
    for (ya, yb) in ((ys[0], ys[1]), (ys[2], ys[3])):
        for x, s in ((xs[1], -1), (xs[2], 1), (xs[3], -1), (xs[4], 1)):
            body = body.cut(lead(plane_xz(yb), x, s, yb - ya))
    for y in (-D / 2, -yi, yi, D / 2):                                   # the notches' edges on both faces of the wall
        body = body.edges(BoxSelector((-NOTCH_R - 0.1, y - 0.05, H / 2 - 0.1),
                                      (NOTCH_R + 0.1, y + 0.05, H - CH - 0.05))).chamfer(CH)
    return {"tray": Part(body, body, OFF)}


SAMPLES["062_sorting_tray_handle"] = sorting_tray_handle
