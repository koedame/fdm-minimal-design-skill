"""023 Mail holder: a 128 x 160 back plate on the wall with a pocket 32 deep and 80 high for letters.

The back plate stands twice as high as the pocket and its top corners take R16; the pocket's front
corners take R4, a radius for each outline. The back face steps in 1.2 on 45 deg, so the plate stands
off the wall on a shadow line. Two keyholes sit in pads on the inside of the back wall, below the top of
the pocket, so they are hidden behind the front and the letters; their entries and head pockets have
45-deg roofs, so the holder prints bottom down without support.
"""
import os
import sys

from cadquery.selectors import BoxSelector

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, OFF, box, rx, fillet_at, keyhole_local)  # noqa: E402

W, H, D = 128.0, 160.0, 32.0      # back plate 128 x 160 (4 : 5), pocket depth = a quarter of the width
HF = H / 2                        # pocket front 80: half the plate
R_TOP, R_FRONT = 16.0, 4.0        # 12.5 % of the plate width / of the pocket depth
FLOOR = 2.4
INSET = 1.2                       # shadow line against the wall
KX, KZ, TRAVEL = 32.0, 40.0, 8.0  # keyholes 64 apart (half the width), entry 40 up, the holder drops 8
LEDGE, POCKET, PAD = 2.0, 3.0, 6.0


def sel(x0, x1, y0, y1, z0, z1):
    return BoxSelector((x0, y0, z0), (x1, y1, z1))


def mail_holder_wall():
    plate = box(-W / 2, W / 2, -T, 0, 0, H).edges("|Y").edges(sel(-W, W, -T - 1, 1, H - 1, H + 1)).fillet(R_TOP)
    pocket = box(-W / 2, W / 2, -D, -T + 0.01, 0, HF)
    for sx in (-1, 1):
        pocket = fillet_at(pocket, (sx * W / 2, -D), R_FRONT)
    body = plate.union(pocket)
    inner = box(-W / 2 + T, W / 2 - T, -D + T, -T, FLOOR, HF + 1)
    for sx in (-1, 1):
        inner = fillet_at(inner, (sx * (W / 2 - T), -D + T), R_FRONT - T, HF + 2)
    body = body.cut(inner)
    body = body.edges(sel(-W, W, -0.01, 0.01, -1, H + 1)).chamfer(INSET)          # back face: the shadow line
    body = body.edges(sel(-W, W, -D - 1, -T - 0.01, HF - 0.01, HF + 0.01)).chamfer(CH)   # rim of the pocket
    body = body.edges(sel(-W, W, -T - 0.01, -T + 0.01, HF + 0.01, H + 1)).chamfer(CH)    # front of the plate above it
    body = body.edges(sel(-W, W, -D - 1, -INSET - 0.01, -0.01, 0.01)).chamfer(CH_BED)
    for sx in (-1, 1):
        x = sx * KX
        pad = box(x - 8, x + 8, -PAD, -T + 0.01, FLOOR - 0.01, HF - 16).edges("|Z and <Y").chamfer(CH)
        body = body.union(pad.faces(">Z").edges("not >Y").chamfer(CH))          # its edges take C0.5 like the rim
        body = body.cut(rx(keyhole_local(TRAVEL, LEDGE, POCKET), 90).translate((x, 0, KZ)))
    return {"holder": Part(body, body, OFF)}


SAMPLES["023_mail_holder_wall"] = mail_holder_wall
