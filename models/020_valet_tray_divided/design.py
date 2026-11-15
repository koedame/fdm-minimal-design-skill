"""020 Valet tray: a deep front cell for a phone and a wallet, a back row of three small cells for keys, coins and a watch.

Built as 03_tray: one body, a 45-deg undercut plinth so it floats on a shadow line, dividers 4 lower than the
rim. The floors meet the walls in R6, so a fingertip pushes a coin into the curve and it tips up to be picked out.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, DARK,  # noqa: E402
                         box, rrect, fillet_at, feet)

W, Dp, H, R = 192.0, 128.0, 24.0, 16.0     # 3 : 2, grid 16; low enough to see into from a chair
FLOOR, DIV_H = 2.4, H - 4.0                # dividers 4 below the rim
RF = 6.0                                   # floor fillet; also the radius of the corners at the dividers
PL, INSET = 2.4, 1.2                       # plinth, as 03_tray
xi, yi = W / 2 - T, Dp / 2 - T
ri = R - T
yd = -yi + (2 * yi - DIV) * 2 / 3 + DIV / 2   # long divider: front cell : back row = 2 : 1
cw = (2 * xi - 2 * DIV) / 3                   # three equal back cells


def cell(x0, x1, y0, y1, outer):
    """A pocket from the floor up; corners on the outer wall take ri, corners at dividers RF."""
    c = box(x0, x1, y0, y1, FLOOR, H + 1)
    for xy in ((x0, y0), (x0, y1), (x1, y0), (x1, y1)):
        c = fillet_at(c, xy, ri if xy in outer else RF, H + 2)
    return c.faces("<Z").edges().fillet(RF - 0.05)


def valet_tray():
    body = rrect(W - 2 * INSET, Dp - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    body = body.union(rrect(W, Dp, R, PL, H - PL).faces("<Z").chamfer(INSET))
    y0b = yd + DIV / 2
    front = cell(-xi, xi, -yi, yd - DIV / 2, {(-xi, -yi), (xi, -yi)})
    body = body.cut(front)
    backs = [-xi + i * (cw + DIV) for i in range(3)]
    for x0 in backs:
        x1 = x0 + cw
        outer = {(x, yi) for x in (x0, x1) if abs(abs(x) - xi) < 1e-6}
        body = body.cut(cell(x0, x1, y0b, yi, outer))
    body = body.cut(rrect(2 * xi, 2 * yi, ri, DIV_H, H))
    body = body.faces(">Z").chamfer(CH)                                   # the rim, inside and out
    # divider tops: one pocket's rim at a time (all at once, OCCT fails where the chains end on the wall)
    for x0, x1, y0, y1 in [(-xi, xi, -yi, yd - DIV / 2)] + [(x0, x0 + cw, y0b, yi) for x0 in backs]:
        lo = (max(x0 - 0.01, -xi + 0.1), max(y0 - 0.01, -yi + 0.1), DIV_H - 0.01)   # not the short edges on the walls
        hi = (min(x1 + 0.01, xi - 0.1), min(y1 + 0.01, yi - 0.1), DIV_H + 0.01)
        rim = cq.selectors.BoxSelector(lo, hi)
        body = body.edges(rim).chamfer(0.4)
    body = feet(body, [(sx * 80, sy * 48) for sx in (-1, 1) for sy in (-1, 1)])
    return {"tray": Part(body, body, DARK)}


SAMPLES["020_valet_tray_divided"] = valet_tray
