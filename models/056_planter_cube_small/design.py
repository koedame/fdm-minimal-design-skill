"""056 Small cube planter: a 64 mm cube with a round bore, for a succulent or a small cutting.

One part, printed bottom down. Outside a cube with R8 corners in plan; inside a round bore three quarters of
the width, so the top reads as a circle in a square. The floor falls 1 : 8 to a drain hole in the centre. On the
underside, a floating plinth with two crossing V channels, kept inside its height, carries the water from the hole out
to the four sides, onto whatever saucer the cube stands on.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, CH, CH_BED, OFF, chamfer_rim, cyl, rrect, rz, plane_yz)  # noqa: E402

S = 64.0                     # cube: width = depth = height
R = 8.0                      # plan radius: 12.5 %
PL, INSET = 2.4, 1.2         # floating plinth
BORE = 0.75 * S              # 48: the soil
Z_FLOOR = 9.6                # floor top at the bore wall
FALL = 1 / 8                 # floor falls toward the drain
DRAIN = 6.0                  # drain hole
CHAN_TOP = PL - 0.4          # channels under the floor: 45-deg roofs whose ridge stays 0.4 inside the plinth


def planter_cube_small():
    p = rrect(S - 2 * INSET, S - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    p = p.union(rrect(S, S, R, PL, S - PL).faces("<Z").chamfer(INSET))
    r = BORE / 2
    z_c = Z_FLOOR - (r - DRAIN / 2) * FALL                  # floor at the drain: 7.0
    prof = [(0, z_c), (DRAIN / 2, z_c), (r, Z_FLOOR), (r, S + 1), (0, S + 1)]
    bore = cq.Workplane("XZ").polyline(prof).close().revolve(360, (0, 0, 0), (0, 1, 0))
    p = p.cut(bore)
    p = p.faces(">Z").edges().chamfer(CH)
    h = CHAN_TOP + 1
    chan = plane_yz(-S / 2 - 1).polyline([(-h, -1), (h, -1), (0, CHAN_TOP)]).close().extrude(S + 2)
    p = p.cut(chan).cut(rz(chan, 90))
    p = p.cut(cyl(DRAIN / 2, -1, z_c + 2))                   # through the floor and out where the channels cross
    return {"planter": Part(p, p, OFF)}


SAMPLES["056_planter_cube_small"] = planter_cube_small
