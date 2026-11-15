"""079 Shelf label holder: a 64 long holder that clips onto the front edge of an 18 shelf board, a paper label behind a clear cover.

The body is one profile, printed lying on its end: a C that takes the board's front edge (a 45-deg ridge on the lower flange
clamps it), and in front of the edge a block with a 0.5 slot for a 60 x 16 paper label that slides in from either end.
The clear cover in front of the label carries four vertical hooks, as 074_led_strip_channel: they run back in two slots above
and below the label and their 45-deg barbs drop into V grooves that run the whole length, so the cover snaps on from the
front or slides on from an end. The seam round the cover is a V line with C0.5 on both sides.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, box, plane_yz  # noqa: E402

CLEAR = (0.80, 0.85, 0.86)               # clear PETG
L, H = 64.0, 28.0                        # 16 x 7 modules
BT = 18.0                                # shelf board thickness
Z1 = BT + T                              # top: the top flange and the front block in one line
Z0 = Z1 - H
F = 12.52                                # front face, in front of the board's edge: T + 10 of inside depth
FL = 12.0                                # flanges' reach over and under the board
RIDGE_Y, RIDGE = FL - 2.0, 0.4           # clamping ridge on the lower flange: 45-deg flanks
LBL = 0.5                                # label slot depth
FLEX = 0.85                              # room under each hook to flex: barb 0.6 + 0.25
HOOK_X, HOOK_W = 16.0, 12.0              # hooks at x ±16, 12 wide
BARB = 0.6                               # free length about 8: strain about 1.1 % at 0.35 deflection, as 074


def label_holder_shelf():
    zt, zb = Z1 - T, Z0 + T                              # inner faces of the top and bottom walls
    yc = -F + DIV                                        # back of the cover
    tip = -T - GAP                                       # hook tips, 0.25 short of the back plate
    by = tip - 1.4                                       # barb centre
    b = box(-L / 2, L / 2, -F, 0, Z0, Z1)
    b = b.union(box(-L / 2, L / 2, -0.01, FL, BT, Z1)).union(box(-L / 2, L / 2, -0.01, FL, -T, 0))
    for (z0, z1) in ((zt - GAP - DIV - FLEX, zt + 0.01), (zb - 0.01, zb + GAP + DIV + FLEX)):   # hook slots
        b = b.cut(box(-L, L, -F - 1, tip + 0.01, z0, z1))
    b = b.cut(box(-L, L, -F - 1, yc + LBL, zb, zt))       # cover and label slot
    b = b.union(plane_yz(-L / 2).polyline([(RIDGE_Y - RIDGE - 0.2, -0.01), (RIDGE_Y - 0.2, RIDGE), (RIDGE_Y + 0.2, RIDGE),
                                           (RIDGE_Y + RIDGE + 0.2, -0.01)]).close().extrude(L))
    for (zi, s) in ((zt, 1), (zb, -1)):                  # V grooves the whole length: barb + 0.25 all round, 45 deg
        g = plane_yz(-L / 2 - 1).polyline([(by - BARB - 0.35, zi - s * 0.01), (by - 0.1, zi + s * (BARB + 0.25)),
                                           (by + 0.1, zi + s * (BARB + 0.25)), (by + BARB + 0.35, zi - s * 0.01)])
        b = b.cut(g.close().extrude(L + 2))
    for (sel, ch) in (("<X", CH_BED), (">X", CH)):        # the profile faces' outline: bed side and top side
        rim = [e for e in b.faces(sel).val().outerWire().Edges() if e.Length() > 1.5]
        b = b.newObject(rim).chamfer(ch)
    for (y, z) in ((-F, Z1), (-F, Z0), (-F, zt), (-F, zb), (FL, Z1), (FL, BT), (FL, 0), (FL, -T), (0, Z0)):
        b = b.edges(cq.selectors.BoxSelector((-L, y - 0.05, z - 0.05), (L, y + 0.05, z + 0.05))).chamfer(CH)

    c = box(-L / 2, L / 2, -F, yc, zb + GAP, zt - GAP).faces("<Y").chamfer(CH_BED).faces(">Y").chamfer(CH)
    for sx in (-1, 1):
        x = sx * HOOK_X
        for (z0, z1, s) in ((zt - GAP - DIV, zt - GAP, 1), (zb + GAP, zb + GAP + DIV, -1)):
            c = c.union(box(x - HOOK_W / 2, x + HOOK_W / 2, yc - 0.01, tip, z0, z1))
            ze = z1 if s > 0 else z0
            c = c.union(plane_yz(x - HOOK_W / 2).polyline([(by - BARB, ze - s * 0.01), (by, ze + s * BARB),
                                                            (by + BARB, ze - s * 0.01)]).close().extrude(HOOK_W))
    label = box(-30, 30, yc + 0.1, yc + 0.3, (zt + zb) / 2 - 8, (zt + zb) / 2 + 8)
    return {
        "body": Part(b, b.rotate((0, 0, 0), (0, 1, 0), -90), OFF),
        "cover": Part(c, c.rotate((0, 0, 0), (1, 0, 0), 90), CLEAR),
        "label_ref": Part(label, None, (0.95, 0.95, 0.93), ref=True),
    }


SAMPLES["079_label_holder_shelf"] = label_holder_shelf
