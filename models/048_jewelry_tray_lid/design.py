"""048 Jewelry tray with lid: a 120 x 80 tray, 24 high, and an 8 high lid that locates on it with a lip.

The tray is the 03_tray layout at a smaller scale: a column on the left for rings and two equal cells on the right. The ring
column holds nine rounded ridges with 3 wide gaps between them, the first and last against the walls, so ten rings stand in
a row facing the front. The tray floats on the same 45-deg shadow line. The lid's wall is thickened inside down to the rim and
continues below it as a 1.68 lip that drops 4 inside the tray's wall; the lid's outside stays flush with the tray's.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, rrect, rx, feet, fillet_at)

W, D, H, R = 120.0, 80.0, 24.0, 10.0     # tray: 3 : 2; R = 12.5 % of the depth
HL, TOP = 8.0, 2.4                       # lid height (tray : lid = 3 : 1), lid top
FLOOR, PL, INSET = 2.4, 2.4, 1.2
LIPD = 4.0                               # lip depth below the rim
WL = T + GAP + DIV                       # lid wall down to the rim: its inner part continues as the lip
DIV_H = H - LIPD - 2.0                   # divider tops 2 under the lip
RIDGE = (5.0, 3.0, 12.0)                 # ring ridges: width, gap, height above the floor (rounded top)
N_GAP = 10


def jewelry_tray_lid():
    ri, r_in = R - T, 3.0
    xi, yi = W / 2 - T, D / 2 - T
    col_w = (2 * xi - DIV) / 3
    xd = -xi + col_w + DIV / 2                               # divider between the ring column and the cells

    tr = rrect(W - 2 * INSET, D - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    tr = tr.union(rrect(W, D, R, PL, H - PL).faces("<Z").chamfer(INSET))

    def cell(x0, x1, y0, y1, radii):
        c = box(x0, x1, y0, y1, FLOOR, H + 1)
        for xy, r in radii.items():
            c = fillet_at(c, xy, r, H + 2)
        return c.faces("<Z").edges().fillet(r_in - 0.05)

    a, b = xd - DIV / 2, xd + DIV / 2
    left = cell(-xi, a, -yi, yi, {(-xi, -yi): ri, (-xi, yi): ri, (a, -yi): r_in, (a, yi): r_in})
    back = cell(b, xi, DIV / 2, yi, {(xi, yi): ri, (b, yi): r_in, (b, DIV / 2): r_in, (xi, DIV / 2): r_in})
    front = cell(b, xi, -yi, -DIV / 2, {(xi, -yi): ri, (b, -yi): r_in, (b, -DIV / 2): r_in, (xi, -DIV / 2): r_in})
    tr = tr.cut(left).cut(back).cut(front)
    tr = tr.cut(rrect(W - 2 * T, D - 2 * T, ri, DIV_H, H))
    tr = tr.faces(">Z").chamfer(CH)
    c = 0.4                                                  # divider tops: the same 45-deg edge, as in 03_tray
    pxz = cq.Plane(origin=(0, yi, 0), xDir=(1, 0, 0), normal=(0, -1, 0))
    for xe, s_ in ((a, 1), (b, -1)):
        tr = tr.cut(cq.Workplane(pxz).polyline([(xe - s_ * .01, DIV_H + .01), (xe + s_ * c, DIV_H + .01),
                                                (xe - s_ * .01, DIV_H - c)]).close().extrude(2 * yi))
    pyz = cq.Plane(origin=(b, 0, 0), xDir=(0, 1, 0), normal=(1, 0, 0))
    for ye, s_ in ((DIV / 2, -1), (-DIV / 2, 1)):
        tr = tr.cut(cq.Workplane(pyz).polyline([(ye - s_ * .01, DIV_H + .01), (ye + s_ * c, DIV_H + .01),
                                                (ye - s_ * .01, DIV_H - c)]).close().extrude(xi - b))

    rw, _, rh = RIDGE
    rg = (2 * yi - (N_GAP - 1) * rw) / N_GAP                # 2.996: gaps and ridges fill the column exactly
    pitch = rw + rg
    for i in range(N_GAP - 1):
        yc = -yi + rg + rw / 2 + i * pitch
        prof = (cq.Workplane(cq.Plane(origin=(-xi - 0.5, 0, 0), xDir=(0, 1, 0), normal=(1, 0, 0)))
                .center(yc, FLOOR - 0.5).rect(rw, 2 * (rh + 0.5 - rw / 2), centered=True))
        ridge = prof.extrude(a - (-xi) + 1.0).union(
            cq.Workplane(cq.Plane(origin=(-xi - 0.5, 0, 0), xDir=(0, 1, 0), normal=(1, 0, 0)))
            .center(yc, FLOOR + rh - rw / 2).circle(rw / 2).extrude(a - (-xi) + 1.0))
        tr = tr.union(ridge.intersect(box(-xi - 0.5, a + 0.5, -yi, yi, FLOOR - 0.5, FLOOR + rh)))
    tr = feet(tr, [(sx * 44.0, sy * 24.0) for sx in (-1, 1) for sy in (-1, 1)])

    ld = rrect(W, D, R, H, HL).faces(">Z").chamfer(CH_BED).faces("<Z").chamfer(CH)
    ld = ld.union(rrect(W - 2 * (T + GAP), D - 2 * (T + GAP), R - T - GAP, H - LIPD, LIPD + 0.01).faces("<Z").chamfer(CH))
    ld = ld.cut(rrect(W - 2 * WL, D - 2 * WL, R - WL, H - LIPD - 1, LIPD + HL - TOP + 1))
    return {
        "tray": Part(tr, tr, OFF),
        "lid": Part(ld, rx(ld, 180), DARK),
    }


SAMPLES["048_jewelry_tray_lid"] = jewelry_tray_lid
