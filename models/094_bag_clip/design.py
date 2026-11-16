"""094 Bag clip: two 120 x 20 jaws on a pin hinge at one end, closed by a snap hook at the other, with a ridge that presses the
folded top of a bag into a groove.

The 07_hinged_case hinge on a long, narrow box: three knuckles across the 20 width (the outer two on the lower jaw), a 1.75
filament pin, 45-deg webs. Closed, the jaws stand 0.25 apart and a 45-deg ridge on the lower jaw runs 0.25 inside a groove in
the upper one, so the film is held along a bent path. At the far end a hook hangs from the upper jaw's top skin (a slit frees
it from the jaw, for a free length of 11) and its 45-deg barb drops into a V groove in the lower jaw's end face.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, DIV, CH, CH_BED, GAP, OFF, box, plane_xz, plane_yz  # noqa: E402

L, W, J = 120.0, 20.0, 8.0                # jaw length, width (6 : 1), thickness
ZA = J                                    # hinge axis on the upper jaw's underside, at the -X end
XA = -L / 2
KR = J / 2                                # knuckle = full round end of the 8 jaw
KL, KG = 6.4, 0.4                         # three knuckles across the 20: 3 x 6.4 + 2 x 0.4
PIN = 1.9
SKIN = 2.4                                # top skin of the upper jaw that carries the hook
ENG = 0.6                                 # catch for a clip that is handled; the barb is 0.25 more
BARB = ENG + GAP
ZB = 2.6                                  # barb centre above the bottom
XE = L / 2 - DIV - GAP                    # lower jaw's end face
RH = 2.0                                  # ridge height, 45-deg flanks, 0.8 flat on top
RX0, RX1 = XA + 2 * KR + 4, XE - 4        # ridge from past the knuckles to 4 short of the end


def segs():
    y0 = -W / 2
    return [(y0 + i * (KL + KG), y0 + i * (KL + KG) + KL) for i in range(3)]


def knuckle(ya, yb, sign):
    """Knuckle on the axis with a 45-deg web to the jaw's end face (sign -1: below the axis, +1: above)."""
    k = 2.828427
    web = [(XA + 0.6, ZA), (XA - k, ZA + sign * k), (XA, ZA + sign * 2 * k), (XA + 0.6, ZA + sign * 2 * k)]
    s = plane_xz(yb).center(XA, ZA).circle(KR).extrude(yb - ya)
    return s.union(plane_xz(yb).polyline(web).close().extrude(yb - ya))


def bag_clip():
    zl = J - GAP                                                   # lower jaw's top: 0.25 under the upper jaw
    lower = box(XA, XE, -W / 2, W / 2, 0, zl).edges("|Z").chamfer(CH).faces(">Z").edges().chamfer(CH)
    lower = lower.faces("<Z").edges().chamfer(CH_BED)
    ridge = [(-RH - 0.4, zl - .01), (-0.4, zl + RH), (0.4, zl + RH), (RH + 0.4, zl - .01)]
    lower = lower.union(plane_yz(RX0).polyline(ridge).close().extrude(RX1 - RX0))
    g = [(XE + .01, ZB - BARB - .35), (XE - BARB - GAP, ZB - .1), (XE - BARB - GAP, ZB + .1), (XE + .01, ZB + BARB + .35)]
    lower = lower.cut(plane_xz(W).polyline(g).close().extrude(2 * W))     # V groove for the barb, barb + 0.25 all round

    upper = box(XA, L / 2, -W / 2, W / 2, J, 2 * J).edges("|Z").chamfer(CH).faces("<Z").edges().chamfer(CH)
    upper = upper.faces(">Z").edges().chamfer(CH_BED)
    s = 0.354                                                      # 0.25 normal to a 45-deg flank, across
    groove = [(-RH - 0.4 - s + GAP, J - .01), (-0.4 - s + GAP, J + RH), (0.4 + s - GAP, J + RH),
              (RH + 0.4 + s - GAP, J - .01)]
    upper = upper.cut(plane_yz(RX0 - GAP).polyline(groove).close().extrude(RX1 - RX0 + 2 * GAP))
    xh = L / 2 - DIV                                               # hook's inner face
    upper = upper.cut(box(xh - BARB, xh, -W, W, J - 1, 2 * J - SKIN))   # slit that frees the hook from the jaw
    hook = box(xh, L / 2, -W / 2, W / 2, ZB - BARB - 1.0, J + .01).edges("|Z").chamfer(CH).faces("<Z").edges().chamfer(CH)
    upper = upper.union(hook)
    b = [(xh + .01, ZB - BARB), (xh - BARB, ZB), (xh + .01, ZB + BARB)]
    upper = upper.union(plane_xz(W / 2).polyline(b).close().extrude(W))

    lk, uk = segs()[0::2], segs()[1::2]
    for (ya, yb) in lk:
        lower = lower.union(knuckle(ya, yb, -1))
        upper = upper.cut(plane_xz(yb + .2).center(XA, ZA).circle(KR + KG).extrude(yb - ya + .4))
    for (ya, yb) in uk:
        upper = upper.union(knuckle(ya, yb, +1))
        lower = lower.cut(plane_xz(yb + .2).center(XA, ZA).circle(KR + KG).extrude(yb - ya + .4))
    pin = plane_xz(W).center(XA, ZA).circle(PIN / 2).extrude(2 * W)
    lower, upper = lower.cut(pin), upper.cut(pin)
    return {
        "lower": Part(lower, lower, OFF),
        "upper": Part(upper, upper.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, 2 * J)), OFF),
    }


SAMPLES["094_bag_clip"] = bag_clip
