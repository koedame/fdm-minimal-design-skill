"""006 Coin tray stack: round shallow trays that stack, each one seated by a 45-deg cone on the rim below.

Under each tray a foot drops into the tray below, and the 45-deg step between the foot and the outer
wall lands on the inner rim chamfer of that tray: the two 45-deg faces meet, so the stack centres
itself. Alone on a desk the tray stands on the foot and the wall floats on a shadow line.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, GAP, OFF)  # noqa: E402

RO, H = 40.0, 20.0                 # 80 across, 20 high (4:1)
RI = RO - T                        # 37.48: inside of the wall
RF = RI - GAP                      # foot radius: 0.25 inside the wall of the tray below
FOOT = 2.4                         # foot height before the 45-deg step
FLOOR = FOOT + 2.4                 # floor top: a 2.4 floor over the foot
R_IN = 6.0                         # floor fillet: coins slide up it into the fingers
N = 3
# the cone (z = FOOT + r - RF above the tray bottom) lies on the chamfer below
# (z = H - CH + r - RI above that tray's bottom), so each tray sits this much higher:
PITCH = H - CH - RI + RF - FOOT    # 16.85


def tray():
    prof = [(0, 0), (RF, 0), (RF, FOOT), (RO, FOOT + RO - RF), (RO, H), (0, H)]
    t = cq.Workplane("XZ").polyline(prof).close().revolve(360, (0, 0, 0), (0, 1, 0))
    t = t.cut(cq.Workplane("XY").workplane(offset=FLOOR).circle(RI).extrude(H))
    t = t.faces(cq.selectors.NearestToPointSelector((0, 0, FLOOR))).edges().fillet(R_IN)
    t = t.faces("<Z").edges().chamfer(CH_BED)
    t = t.faces(">Z").edges().chamfer(CH)            # outer and inner rim; the inner one is the seat
    return t


def coin_tray_stack():
    one = tray()
    # kept as separate solids (a union would fuse them on the seats)
    stack = cq.Workplane("XY").add(cq.Compound.makeCompound(
        [one.translate((0, 0, i * PITCH)).val() for i in range(N)]))
    return {"tray": Part(stack, one, OFF, qty=N)}


SAMPLES["006_coin_tray_stack"] = coin_tray_stack
