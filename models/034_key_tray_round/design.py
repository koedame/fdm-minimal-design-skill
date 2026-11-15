"""034 Round key tray: a dish 120 across and 24 high that floats on a plinth set 1.2 inward, with a soft
TPU liner in its floor.

The floor runs up into the wall on a cove of R12, half the height, so keys slide up it into the fingers.
The liner sits flush in a recess in the flat of the floor, with C0.5 on both edges of the seam, so keys
land on something soft and quiet and the seam reads as one V line. Under the dish, the plinth's 45-deg
step makes a shadow line all round.
"""
import os
import sys

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, CH, CH_BED, GAP, OFF, DARK, cyl, feet, chamfer_rim  # noqa: E402

DIA, H = 120.0, 24.0        # 5 : 1
R_OUT = DIA / 2
PL, INSET = 2.4, 1.2        # floating plinth (as 03): 2.4 high, set 1.2 inward, joined at 45 deg
FLOOR = 3.6                 # 2.4 under the liner + the liner's 1.2
COVE = H / 2                # 12: floor-to-wall radius
LINER_T = 1.2
R_REC = 44.0                # liner recess: 11 modules, 1.48 inside the start of the cove


def key_tray_round():
    body = cyl(R_OUT - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    body = body.union(cyl(R_OUT, PL, H - PL).faces("<Z").chamfer(INSET))
    body = body.cut(cyl(R_OUT - T, FLOOR, H).faces("<Z").edges().fillet(COVE))
    body = body.faces(">Z").chamfer(CH)                      # rim: inner and outer edge, same value
    body = body.cut(cyl(R_REC, FLOOR - LINER_T, LINER_T + 1))
    body = chamfer_rim(body, R_REC, FLOOR)
    body = feet(body, [(sx * 28, sy * 28) for sx in (-1, 1) for sy in (-1, 1)])

    liner = cyl(R_REC - GAP, FLOOR - LINER_T, LINER_T).faces(">Z").chamfer(CH)
    return {
        "tray": Part(body, body, OFF),
        "liner_tpu": Part(liner, liner, DARK),          # bottom down: the C0.5 edge is the top, not the bed side
    }


SAMPLES["034_key_tray_round"] = key_tray_round
