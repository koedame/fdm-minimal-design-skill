"""072 E-paper display frame: a standing frame for a bare 4.2-inch e-paper panel behind a clear window.

The body is a sleeve open at the back, printed front face down. A clear window with a flange fits the opening
from behind (flush with the front, a V line round it), the panel lies on the flange inside a locating rim, and
a back cover clicks into the open back on two 45-deg hooks; two ribs on the cover hold the panel against the
window. The cover comes off by pulling at the cable notch in its bottom edge.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, PLATE,  # noqa: E402
                         box, rx, feet, plane_xz)

CLEAR = (0.80, 0.85, 0.86)              # clear PETG
# the panel (match yours): 91 x 77 x 1.2 outline, the view area centred in a 88 x 68 window
PW, PH, PT = 91.0, 77.0, 1.2
WIN_W, WIN_H = 88.0, 68.0
M = 16.0                                # margin round the window, the same on all four sides
W, H = WIN_W + 2 * M, WIN_H + 2 * M     # 120 x 100
D = 32.0                                # depth: stands on 32 (tipping angle about 18 deg)
R, RI = 12.0, 3.0                       # outline (10 % of 120); window and inside corners
FP = 2.4                                # front plate
FL = 1.2                                # window flange
CP = 2.4                                # back cover plate
HOOK_W, HOOK_L = 16.0, 16.0             # free length 13 to the barb: strain about 0.9 % at 0.6 deflection
BARB = 0.85                             # 0.6 of it past the 0.25 gap, into the wall
FPC = 32.0                              # gap in the locating rim for the panel's flex tail (24 wide on most panels)
NOTCH_W, NOTCH_H = 8.0, 4.0             # cable notch in the cover's bottom edge (a USB cable, 4 thick)


def _front(wp_y, w, h, r, t):
    """A rounded rectangle in XZ centred on the frame, from y = wp_y back by t (+Y)."""
    return plane_xz(wp_y + t).center(0, H / 2).rect(w, h).extrude(t).edges("|Y").fillet(r)


def display_frame_eink():
    yf, yb = -D / 2, D / 2
    yi = yf + FP                                    # inside of the front plate
    xi = W / 2 - T                                  # inside of the side walls

    body = _front(yf, W, H, R, D)
    body = body.cut(_front(yi, W - 2 * T, H - 2 * T, R - T, D))
    body = body.cut(plane_xz(yi + 1).center(0, H / 2).rect(WIN_W, WIN_H).extrude(FP + 2).edges("|Y").fillet(RI))
    body = body.faces("<Y").chamfer(CH).faces(">Y").chamfer(CH)
    rim_o = _front(yi - 0.01, PW + 0.5 + 2 * DIV, PH + 0.5 + 2 * DIV, 1.0 + DIV, FL + PT + 0.01)
    rim = rim_o.cut(_front(yi - 1, PW + 0.5, PH + 0.5, 1.0, FL + PT + 2))
    zr = H / 2 - PH / 2                             # the panel's flex tail leaves its bottom edge: a gap in the rim
    body = body.union(rim.cut(box(-FPC / 2, FPC / 2, yi - 1, yi + 5, zr - 5, zr + 1)))
    body = feet(body, [(sx * 44, 0) for sx in (-1, 1)])

    y_barb = yb - CP - HOOK_L + 3.0
    for s in (-1, 1):                               # V grooves in the side walls: barb + 0.25 all round, 45 deg
        body = body.cut(groove(s, xi, y_barb))

    win = _front(yf, WIN_W - 2 * GAP, WIN_H - 2 * GAP, RI - GAP, FP + 0.01).faces("<Y").chamfer(CH)
    win = win.union(_front(yi, PW, PH, 1.0, FL))

    cw, chh = W - 2 * (T + GAP), H - 2 * (T + GAP)
    cov = _front(yb - CP, cw, chh, R - T - GAP, CP).faces(">Y").chamfer(CH)
    zn = T + GAP + NOTCH_H - NOTCH_W / 2            # round top: an elongated hole keeps semicircular ends
    cov = cov.cut(box(-NOTCH_W / 2, NOTCH_W / 2, yb - CP - 1, yb + 1, T + GAP - 1, zn))
    cov = cov.cut(plane_xz(yb + 1).center(0, zn).circle(NOTCH_W / 2).extrude(CP + 2))
    y_panel = yi + FL + PT
    for s in (-1, 1):                               # ribs that hold the panel against the window, 0.1 short of it
        cov = cov.union(box(s * 40 - DIV / 2, s * 40 + DIV / 2, y_panel + 0.1, yb - CP + 0.01, H / 2 - 25, H / 2 + 25))
    xo = xi - GAP                                   # hook outer face
    for s in (-1, 1):
        x0, x1 = sorted((s * (xo - DIV), s * xo))
        cov = cov.union(box(x0, x1, yb - CP - HOOK_L, yb - CP + 0.01, H / 2 - HOOK_W / 2, H / 2 + HOOK_W / 2))
        cov = cov.union(barb(s, xo, y_barb))

    panel = _front(yi + FL, PW, PH, 0.5, PT)
    return {
        "body": Part(body, rx(body, 90), OFF),
        "window_clear": Part(win, rx(win, 90), CLEAR),
        "back_cover": Part(cov, rx(cov, -90), OFF),
        "panel_ref": Part(panel, None, PLATE, ref=True),
    }


def groove(s, xi, y_barb):
    """V groove in the side wall at x = s * xi, running HOOK_W + 2 GAP in Z round the frame's centre height."""
    pts = [(s * (xi - 0.01), y_barb - BARB - 0.35), (s * (xi + BARB + 0.25), y_barb - 0.1),
           (s * (xi + BARB + 0.25), y_barb + 0.1), (s * (xi - 0.01), y_barb + BARB + 0.35)]
    z0 = H / 2 - HOOK_W / 2 - GAP
    return cq.Workplane("XY").workplane(offset=z0).polyline(pts).close().extrude(HOOK_W + 2 * GAP)


def barb(s, xo, y_barb):
    """45-deg barb on the outer face of a hook at x = s * xo."""
    pts = [(s * (xo - 0.01), y_barb - BARB), (s * (xo + BARB), y_barb), (s * (xo - 0.01), y_barb + BARB)]
    return cq.Workplane("XY").workplane(offset=H / 2 - HOOK_W / 2).polyline(pts).close().extrude(HOOK_W)


SAMPLES["072_display_frame_eink"] = display_frame_eink
