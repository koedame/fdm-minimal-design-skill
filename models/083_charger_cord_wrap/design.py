"""083 Charger cord wrap: a flat bobbin, 96 x 48 x 16, for winding a charger's cord to carry it flat in a bag.

Two flanges on a stadium core. One piece would not print (the upper flange would overhang the core by 12 all round), so the
winder is two halves split under the upper flange. The base carries the hollow core; the cap's flange carries a plug that goes
down inside it, and two cantilever tabs freed from the plug's long sides by U-shaped slits click their 45-deg bumps into grooves
inside the core. The joint is hidden inside and pulls apart without tools. The cord starts in a slot in the base flange, is wound
round the core and its end is pinched in a slot in the cap flange at the other end.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, box, rrect, rx, plane_yz  # noqa: E402

L, W, R = 96.0, 48.0, 12.0          # flanges: 2 : 1 on the grid, R12 = 12.5 % of 96
H, FL = 16.0, 2.4                   # total height; flange thickness
CL, CW = 72.0, 24.0                 # core: a stadium with R12 ends (the flange's radius), 12 of winding room all round
Z_SPLIT = H - FL                    # the cap is the upper flange; the base's core ends under it
PLUG = 10.0                         # plug depth inside the core, 1.2 above its floor
TAB_W, SLIT, BUMP = 12.0, 1.0, 0.65   # bump 0.65: 0.4 of it reaches past the 0.25 clearance
Z_BUMP = Z_SPLIT - PLUG + 1.5       # bump centre 1.5 above the plug's lower end
CORD = 3.2                          # cord slot width: pinches a Ø3.5 cord; set it 0.3 under your cord's diameter
SLOT_L = 10.0                       # slot length from the flange's end, its round end 2 short of the core


def stadium(length, width, z0, h):
    return cq.Workplane("XY").workplane(offset=z0).slot2D(length, width).extrude(h)


def prism_x(y, z, pts, length):
    """45-deg prism along X: pts in local (y, z) around (y, z)."""
    return plane_yz(-length / 2).polyline([(y + a, z + b) for a, b in pts]).close().extrude(length)


def flange(z0, slot_x):
    f = rrect(L, W, R, z0, FL)
    s = 1 if slot_x > 0 else -1
    return f.cut(cq.Workplane("XY").workplane(offset=z0 - 1).center(slot_x - s * SLOT_L / 2, 0)
                 .slot2D(SLOT_L + CORD, CORD).extrude(FL + 2))


def charger_cord_wrap():
    ci_l, ci_w = CL - 2 * T, CW - 2 * T                 # core inside
    po_l, po_w = ci_l - 2 * GAP, ci_w - 2 * GAP         # plug outside
    base = flange(0, -L / 2).faces("<Z").edges().chamfer(CH_BED).faces(">Z").edges().chamfer(CH)
    core = stadium(CL, CW, FL - 0.01, Z_SPLIT - FL + 0.01).faces(">Z").edges().chamfer(CH)
    base = base.union(core).cut(stadium(ci_l, ci_w, FL, H))
    g = 2 * BUMP
    for s in (-1, 1):
        groove = prism_x(0, Z_BUMP, [(0, -g), (g, 0), (0, g)], TAB_W + 2)
        base = base.cut((groove if s > 0 else groove.mirror("XZ")).translate((0, s * (ci_w / 2 - 0.01), 0)))

    cap = flange(Z_SPLIT, L / 2).faces("<Z").edges().chamfer(CH).faces(">Z").edges().chamfer(CH_BED)
    plug = stadium(po_l, po_w, Z_SPLIT - PLUG, PLUG + 0.01).cut(stadium(po_l - 2 * DIV, po_w - 2 * DIV, Z_SPLIT - PLUG - 1, H))
    plug = plug.faces("<Z").edges().chamfer(CH)
    yt = po_w / 2 - DIV / 2                             # mid-plane of the plug's long walls
    for s in (-1, 1):
        for x in (-TAB_W / 2 - SLIT, TAB_W / 2):        # U-shaped slit: two sides, open at the lower end
            plug = plug.cut(box(x, x + SLIT, s * yt - DIV, s * yt + DIV, Z_SPLIT - PLUG - 1, Z_SPLIT - 0.5))
        bump = prism_x(0, Z_BUMP, [(0, -BUMP), (BUMP, 0), (0, BUMP)], TAB_W)
        plug = plug.union((bump if s > 0 else bump.mirror("XZ")).translate((0, s * (po_w / 2 - 0.01), 0)))
    cap = cap.union(plug)
    return {
        "base": Part(base, base, OFF),
        "cap": Part(cap, rx(cap, 180), OFF),
    }


SAMPLES["083_charger_cord_wrap"] = charger_cord_wrap
