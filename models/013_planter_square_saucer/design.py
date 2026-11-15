"""013 Square planter on a saucer: a 96 cube in two parts, the pot standing in a 16 high saucer.

The pot is the saucer's outline less a wall and a clearance all round, so it drops inside the saucer
rim, which locates it. It stands on four posts 8 above the saucer floor, so the water that drains
through the holes in its floor collects under it instead of standing in the soil.
"""
import os
import sys

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, CH, CH_BED, GAP, OFF, DARK, cyl, rrect  # noqa: E402

S, R, H = 96.0, 12.0, 96.0        # saucer outline, R = 12.5 % of 96; total height = width (a cube)
HS = 16.0                         # saucer height: 1/6 of the total
FLOOR = 2.4
POST = 8.0                        # the pot stands 8 above the saucer floor: about 65 ml of water under it
P = S - 2 * (T + GAP)             # pot outline 90.46: inside the saucer wall with 0.25 clearance
RP = R - T - GAP                  # 9.23: concentric with the saucer corners
R_IN = 6.0                        # pot floor fillet
HOLE_D, HOLE_P, HOLE_N = 4.0, 8.0, 7   # drain holes: a 7 x 7 field at pitch 8 (2 x grid), out to ±24
POST_XY = 36.0                    # posts under the outer ring of the pot floor, clear of the hole field


def planter_square_saucer():
    saucer = rrect(S, S, R, 0, HS).faces("<Z").chamfer(CH_BED)
    saucer = saucer.cut(rrect(S - 2 * T, S - 2 * T, R - T, FLOOR, HS))
    saucer = saucer.faces(">Z").chamfer(CH)
    for sx in (-1, 1):
        for sy in (-1, 1):
            saucer = saucer.union(cyl(POST / 2, FLOOR - 0.01, POST + 0.01, sx * POST_XY, sy * POST_XY))

    z0 = FLOOR + POST
    pot = rrect(P, P, RP, z0, H - z0).faces("<Z").chamfer(CH_BED)
    pot = pot.cut(rrect(P - 2 * T, P - 2 * T, RP - T, z0 + FLOOR, H).faces("<Z").edges().fillet(R_IN))
    pot = pot.faces(">Z").chamfer(CH)
    off = (HOLE_N - 1) / 2 * HOLE_P
    for i in range(HOLE_N):
        for j in range(HOLE_N):
            pot = pot.cut(cyl(HOLE_D / 2, z0 - 1, FLOOR + 2, i * HOLE_P - off, j * HOLE_P - off))
    return {
        "pot": Part(pot, pot.translate((0, 0, -z0)), OFF),
        "saucer": Part(saucer, saucer, DARK),
    }


SAMPLES["013_planter_square_saucer"] = planter_square_saucer
