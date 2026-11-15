"""066 Stamp and pad box: a seal and a round ink pad kept together under a lift-off lid.

Two printed parts. The base is a solid 96 x 76 x 12 block with a round pocket for the ink pad and a half-round trough
for a seal lying down, the same margin round both; the pad stands 10 out of its pocket and the seal half out of its
trough, so both are picked out with the fingers. A lip rises 3 from the base, 0.25 inside the lid's walls, and locates
the lid, a 16 high cap; the seam is one V line 12 up.
"""
import os
import sys

import cadquery as cq
from cadquery.selectors import BoxSelector

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, cyl, rrect, rx, feet, chamfer_rim, plane_xz)

W, D, R = 96.0, 76.0, 12.0        # 24 x 19 modules; R12 = 12.5 % of the width
HB, HL = 12.0, 16.0               # base : lid = 3 : 4, 28 overall
TOP = 2.4
LIP = 3.0                         # the lip rises 3 above the base
LIP_IN = T + GAP + DIV            # inside face of the lip from the outline (4.45)
PAD_D, PAD_H = 57.0, 16.0         # a round ink pad (check yours)
POCKET_D, POCKET = PAD_D + 1.0, 6.0   # pad pocket: 0.5 round, 6 deep, the pad stands 10 out
SEAL_D, SEAL_L = 15.0, 60.0       # a 15 x 60 seal
TROUGH_R = SEAL_D / 2 + 0.25      # trough: 0.25 round the seal, centred so the seal lies half out of the base
MARGIN = D / 2 - LIP_IN - POCKET_D / 2          # 4.55 from the lip to the pocket, the same everywhere
PX = -W / 2 + LIP_IN + MARGIN + POCKET_D / 2    # pad pocket centre
SX = W / 2 - LIP_IN - MARGIN - TROUGH_R         # seal trough centre


def tray_ring(off, z0, h):
    return rrect(W - 2 * off, D - 2 * off, R - off, z0, h)


def stamp_pad_box():
    sz = HB                                                       # trough centred on the top face: the seal lies half out
    base = rrect(W, D, R, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    base = base.union(tray_ring(T + GAP, HB - 0.01, LIP + 0.01).cut(tray_ring(LIP_IN, HB - 1, LIP + 2)))
    base = base.faces(">Z").edges().chamfer(CH)                   # the lip's top, both edges
    base = base.cut(cyl(POCKET_D / 2, HB - POCKET, POCKET + 1, PX, 0))
    base = chamfer_rim(base.translate((-PX, 0, 0)), POCKET_D / 2, HB).translate((PX, 0, 0))
    trough = plane_xz(SEAL_L / 2 + 0.5).center(SX, sz).circle(TROUGH_R).extrude(SEAL_L + 1)
    base = base.cut(trough)
    base = base.edges(BoxSelector((SX - TROUGH_R - 0.5, -SEAL_L, HB - 0.05), (SX + TROUGH_R + 0.5, SEAL_L, HB + 0.05))) \
        .chamfer(CH)
    base = feet(base, [(sx * 36, sy * 26) for sx in (-1, 1) for sy in (-1, 1)])

    lid = rrect(W, D, R, HB, HL).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    lid = lid.cut(tray_ring(T, HB - 1, HL - TOP + 1))
    pad = cyl(PAD_D / 2, HB - POCKET + 0.05, PAD_H, PX, 0)
    seal = plane_xz(SEAL_L / 2).center(SX, sz).circle(SEAL_D / 2).extrude(SEAL_L)
    return {
        "base": Part(base, base, OFF),
        "lid": Part(lid, rx(lid, 180), OFF),
        "pad_ref": Part(pad, None, (0.62, 0.2, 0.18), ref=True),
        "seal_ref": Part(seal, None, (0.55, 0.42, 0.3), ref=True),
    }


SAMPLES["066_stamp_pad_box"] = stamp_pad_box
