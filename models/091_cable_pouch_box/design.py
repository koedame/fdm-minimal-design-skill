"""091 Cable pouch box: a 120 x 80 x 40 travel box for a charger and its cables, with a lid held by four snap hooks.

The 07_hinged_case proportions without the hinge: a body 32 high and a lid 8 high (4 : 1), one V seam round the box. A
divider 4 under the rim splits the body 1 : 2, a cell for the charger and one for coiled cables. Four vertical hooks, one
in the middle of each of the lid's walls, run down 0.25 inside the body's walls; their 45-deg barbs drop into short V grooves
in those walls, so the lid snaps on from above and comes off when pulled at the finger scoop across the front seam.
"""
import os
import sys

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, box, rrect, plane_xz  # noqa: E402

W, D, R = 120.0, 80.0, 12.0              # 3 : 2 on the 4 grid; R12 = 15 % of the depth
HB, HL = 32.0, 8.0                       # 4 : 1, 40 overall
FLOOR, TOP = 2.4, 2.4
DROP = 4.0                               # the divider stops 4 under the rim, as 03_tray
HOOK_W = 16.0                            # hook width (along y)
FREE = 12.0                              # hook free length below the seam
ENG = 0.6                                # catch for a lid that is handled; the barb is 0.25 more
BARB = ENG + GAP
ZB = HB - FREE + BARB + 1.0              # barb centre, 1 above the hook's tip


def hook_and_groove(w):
    """The hook on the lid and the groove in the body for a wall whose inner face is at x = w (built for +x)."""
    xo, xi = w - GAP, w - GAP - DIV                                 # hook's faces, its outer face 0.25 inside the wall
    zt = HB + HL - TOP
    hook = box(xi, xo, -HOOK_W / 2, HOOK_W / 2, HB - FREE, zt + .01)
    hook = hook.union(box(xo - .01, w + .01, -HOOK_W / 2, HOOK_W / 2, HB, zt + .01))   # joined to the lid's wall
    b = [(xo - .01, ZB - BARB), (xo + BARB, ZB), (xo - .01, ZB + BARB)]
    hook = hook.union(plane_xz(HOOK_W / 2).polyline(b).close().extrude(HOOK_W))
    g = [(w - .01, ZB - BARB - .35), (w + BARB + GAP, ZB - .1), (w + BARB + GAP, ZB + .1), (w - .01, ZB + BARB + .35)]
    groove = plane_xz(HOOK_W / 2 + GAP).polyline(g).close().extrude(HOOK_W + 2 * GAP)   # barb + 0.25 all round, 45 deg
    return hook, groove


def cable_pouch_box():
    xw, yw = W / 2 - T, D / 2 - T        # inner faces of the walls
    body = rrect(W, D, R, 0, HB).faces("<Z").chamfer(CH_BED)
    body = body.cut(rrect(W - 2 * T, D - 2 * T, R - T, FLOOR, HB))
    body = body.faces(">Z").edges().chamfer(CH)                     # the rim, outside and in (a lead-in for the hooks)
    xd = -xw + (W - 2 * T - DIV) / 3                                # divider: charger cell 1, cable cell 2
    body = body.union(box(xd, xd + DIV, -yw - .01, yw + .01, FLOOR - .01, HB - DROP).faces(">Z").edges("|Y").chamfer(CH))
    lid = rrect(W, D, R, HB, HL).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    lid = lid.cut(rrect(W - 2 * T, D - 2 * T, R - T, HB - 1, HL - TOP + 1))
    for (w, a) in ((xw, 0), (xw, 180), (yw, 90), (yw, -90)):        # one hook in the middle of each wall
        hook, groove = (s.rotate((0, 0, 0), (0, 0, 1), a) for s in hook_and_groove(w))
        lid, body = lid.union(hook), body.cut(groove)
    scoop = plane_xz(-D / 2 + 1.2).center(0, HB).circle(0.75 * HL).extrude(3)   # finger scoop across the front seam
    body, lid = body.cut(scoop), lid.cut(scoop)
    return {
        "body": Part(body, body, OFF),
        "lid": Part(lid, lid.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, HB + HL)), OFF),
    }


SAMPLES["091_cable_pouch_box"] = cable_pouch_box
