"""082 Under-desk headphone hook: a C profile 40 wide that hangs under a desk top, opening toward the chair.

A flat plate is screwed to the underside of the desk with two wood screws. Its section is a trapezoid with 45-deg flanks and it carries
two vertical bosses underneath. The hook's top block sits over it, the plate in a matching pocket and the bosses in two holes, so the
plate and its screws are covered. Two M3 screws come up from below through counterbores behind the stem, where the stem hides them
from the chair, into pilot holes in the bosses.
The headband rests on the arm, between the stem and a raised lip at the tip. The hook prints lying on its side, so every layer is the
whole C.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, CH, CH_BED, GAP, OFF, box, rx  # noqa: E402

W = 40.0                            # hook width: a headband up to 40 wide
Y0, Y1 = -72.0, 0.0                 # top block 72 deep; +Y toward the chair
TB = 16.0                           # top block thickness
SY0, SY1 = -48.0, -36.0             # stem 12 thick
Z_BOT = -72.0                       # the arm's underside, 72 under the desk: the profile is 72 square
ARM = 12.0                          # arm and stem thickness: 3 modules
LIP_Y, LIP_TOP = -12.0, -44.0       # lip 12 thick like the arm and stem, rising 16 above the arm
R_OUT, R_IN, R_END = 12.0, 6.0, 5.8   # outer bends, inner corners, the lip's round top (about half its 12)
PB, PT = 16.0, 4.0                  # plate: half-width 16 at the desk, 4 thick, 45-deg flanks -> 24 wide at the bottom
PY0, PY1 = -68.0, -4.0              # plate 64 long, 4 inside the block at both ends
WOOD_Y = (-40.0, -16.0)             # 2 x 4 mm countersunk wood screws, 24 apart, up into the desk
BOSS_Y, BOSS_X = -60.0, (-8.0, 8.0)   # behind the stem: reached from below, hidden from the chair
BOSS_R, BOSS_L = 3.5, 6.0           # Ø7 boss, 6 long, M3 pilot Ø2.5 through boss and plate
K = 0.70710678


def trap_y(hb, z0, z1, y0, y1):
    """Prism along Y of a 45-deg trapezoid section: half-width hb at z = 0, shrinking 1 per 1 downward."""
    pts = [(-(hb + z0), z0), (hb + z0, z0), (hb + z1, z1), (-(hb + z1), z1)]
    return cq.Workplane("XZ").workplane(offset=-y1).polyline(pts).close().extrude(y1 - y0)


def teardrop_z(x, y, z0, h, r):
    """Round hole along Z with a 45-deg roof toward +X (up when the hook lies on its side)."""
    tri = [(x + r * K, y - r * K), (x + r * 1.41421356, y), (x + r * K, y + r * K), (x, y)]
    w = cq.Workplane("XY").workplane(offset=z0)
    return w.center(x, y).circle(r).extrude(h).union(w.polyline(tri).close().extrude(h))


def at(y, z):
    return cq.selectors.BoxSelector((-W, y - 0.01, z - 0.01), (W, y + 0.01, z + 0.01))


def headphone_hook_under_desk():
    hk = box(-W / 2, W / 2, Y0, Y1, -TB, 0)
    hk = hk.union(box(-W / 2, W / 2, SY0, SY1, Z_BOT + 1, -TB + 0.01))
    hk = hk.union(box(-W / 2, W / 2, SY0, Y1, Z_BOT, Z_BOT + ARM))
    hk = hk.union(box(-W / 2, W / 2, LIP_Y, Y1, Z_BOT + ARM - 0.01, LIP_TOP))
    for y, z, r in ((SY0, Z_BOT, R_OUT), (Y1, Z_BOT, R_OUT),
                    (SY1, -TB, R_IN), (SY0, -TB, R_IN), (SY1, Z_BOT + ARM, R_IN), (LIP_Y, Z_BOT + ARM, R_IN),
                    (LIP_Y, LIP_TOP, R_END), (Y1, LIP_TOP, R_END)):
        hk = hk.edges(at(y, z)).fillet(r)
    hk = hk.faces("<X").edges().chamfer(CH_BED).faces(">X").edges().chamfer(CH)
    c = GAP * 1.41421356                                               # 0.25 normal to the 45-deg flanks
    hk = hk.cut(trap_y(PB + c, 1.0, -(PT + GAP), PY0 - GAP, PY1 + GAP))
    for x in BOSS_X:
        hk = hk.cut(teardrop_z(x, BOSS_Y, -(PT + BOSS_L + GAP), BOSS_L + 1, BOSS_R + GAP))   # boss holes
        hk = hk.cut(teardrop_z(x, BOSS_Y, -TB - 1, TB, 1.7))                                # M3 clearance
        hk = hk.cut(teardrop_z(x, BOSS_Y, -TB - 1, 4.0, 3.1))                               # head Ø6.2, 3 deep

    plate = trap_y(PB, 0, -PT, PY0, PY1)
    plate = plate.faces("<Y or >Y").edges().chamfer(CH)
    for y in WOOD_Y:
        plate = plate.cut(cq.Workplane("XY").workplane(offset=-PT - 1).center(0, y).circle(2.25).extrude(PT + 2))
        plate = plate.cut(cq.Workplane("XY").add(cq.Solid.makeCone(
            4.5, 2.25, 2.26, cq.Vector(0, y, -PT - 0.01), cq.Vector(0, 0, 1))))
    for x in BOSS_X:
        boss = cq.Workplane("XY").workplane(offset=-PT - BOSS_L).center(x, BOSS_Y).circle(BOSS_R).extrude(BOSS_L + 0.5)
        plate = plate.union(boss.faces("<Z").chamfer(CH))
        plate = plate.cut(cq.Workplane("XY").workplane(offset=-PT - BOSS_L - 1).center(x, BOSS_Y).circle(1.25)
                          .extrude(BOSS_L + PT + 2))
    return {
        "hook": Part(hk, hk.rotate((0, 0, 0), (0, 1, 0), -90), OFF),
        "desk_plate": Part(plate, rx(plate, 180), OFF),
    }


SAMPLES["082_headphone_hook_under_desk"] = headphone_hook_under_desk
