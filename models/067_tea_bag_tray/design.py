"""067 Tea bag tray: a small dish beside the cup for a used tea bag.

One part, printed bottom down. 96 x 64 x 12, R12, on a floating plinth. Seven low ribs cross the floor with equal gaps:
the bag lies on their tops and the tea it drips runs off into the floor between them, so the bag does not sit in a
puddle. A notch in the rim of one short wall takes the string, so the tag hangs outside and stays dry.
"""
import os
import sys

import cadquery as cq
from cadquery.selectors import BoxSelector

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, OFF, rrect, feet, plane_xz, plane_yz)  # noqa: E402

W, D, H = 96.0, 64.0, 12.0        # 24 x 16 x 3 modules
R = 12.0                          # 12.5 % of the width; the inside takes R - T
FLOOR = 2.4
R_IN = 3.0                        # floor edge inside
PL, INSET = 2.4, 1.2              # floating plinth
RIB_H = 3.2                       # rib tops 3.2 over the floor, 6.4 under the rim
N_RIB = 7                         # across the whole floor: the bag lies anywhere
GAP_RIB = (W - 2 * T - N_RIB * DIV) / (N_RIB + 1)   # 9.9: equal gaps, walls included
NOTCH_R = 3.0                     # string notch: 6 wide, 3 deep


def bag():
    """Envelope of a used flat tea bag, 60 x 50 x 8, lying on the ribs."""
    z = FLOOR + RIB_H
    return cq.Workplane("XY").box(60, 50, 8, centered=(True, True, False)).translate((0, 0, z + 0.01))


def tea_bag_tray():
    body = rrect(W - 2 * INSET, D - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    body = body.union(rrect(W, D, R, PL, H - PL).faces("<Z").chamfer(INSET))
    cav = rrect(W - 2 * T, D - 2 * T, R - T, FLOOR, H).faces("<Z").edges().fillet(R_IN)
    body = body.cut(cav)
    body = body.faces(">Z").edges().chamfer(CH)                     # rim, inner and outer

    top, w = FLOOR + RIB_H, DIV / 2
    inner = rrect(W - 2 * T + 0.02, D - 2 * T + 0.02, R - T + 0.01, FLOOR - 0.5, RIB_H + 0.5)
    for i in range(N_RIB):
        x = -W / 2 + T + GAP_RIB + w + i * (GAP_RIB + DIV)
        rib = (plane_xz(D / 2)
               .polyline([(x - w, FLOOR - 0.5), (x + w, FLOOR - 0.5), (x + w, top - CH),
                          (x + w - CH, top), (x - w + CH, top), (x - w, top - CH)]).close().extrude(D))
        body = body.union(rib.intersect(inner))

    notch = plane_yz(W / 2 - T - 1).center(0, H).circle(NOTCH_R).extrude(T + 2)
    body = body.cut(notch)
    for x in (W / 2 - T, W / 2):
        body = body.edges(BoxSelector((x - 0.05, -NOTCH_R - 0.1, H - NOTCH_R - 0.1),
                                      (x + 0.05, NOTCH_R + 0.1, H - CH - 0.05))).chamfer(CH)
    body = feet(body, [(sx * 36, sy * 20) for sx in (-1, 1) for sy in (-1, 1)])
    return {"tray": Part(body, body, OFF)}


SAMPLES["067_tea_bag_tray"] = tea_bag_tray
