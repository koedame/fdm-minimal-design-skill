"""053 Coaster set with holder: four square coasters that stack in a low square holder.

The holder is a 96 x 96 x 20 cup on a floating plinth, printed bottom down; its inside locates the coasters
with 0.25 clearance all round, and two shallow arcs cut into opposite walls let a finger and
thumb take the stack or one coaster. Each coaster is a 4 mm plate with a 0.8 deep drip recess inside a 4 mm
rim, printed top face up (its visible face has a recess). Coasters dark grey, holder off-white.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, rrect, copies, plane_yz)

S, H, R = 96.0, 20.0, 12.0          # holder: 24 modules square, 5 high; R = 12.5 %
PL, INSET = 2.4, 1.2                # floating plinth; the floor is as thick as the plinth
FLOOR = PL
N, CT = 4, 4.0                      # four coasters, 4 thick (stack 16 = 4 modules)
CS = S - 2 * T - 2 * GAP            # 90.46: the holder's inside less the clearance
CR = R - T - GAP                    # 9.23: concentric with the holder
RIM, RECESS = 4.0, 0.8              # drip recess inside a 4 rim (one module), 0.8 deep (two layers of 0.4)
U_R = 16.0                          # finger openings: R16 arcs ...
U_Z = FLOOR + CT + U_R              # ... centred 2.4 above the rim, so they reach down to the top of the first coaster (6.4)


def coaster(z0):
    c = rrect(CS, CS, CR, z0, CT).faces("<Z").chamfer(CH_BED)
    c = c.cut(rrect(CS - 2 * RIM, CS - 2 * RIM, CR - RIM, z0 + CT - RECESS, 1))
    return c.faces(">Z").edges().chamfer(CH)


def coaster_set_holder():
    h = rrect(S - 2 * INSET, S - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    h = h.union(rrect(S, S, R, PL, H - PL).faces("<Z").chamfer(INSET))
    h = h.cut(rrect(S - 2 * T, S - 2 * T, R - T, FLOOR, H))
    u = plane_yz(-S / 2 - 1).center(0, U_Z).circle(U_R).extrude(S + 2)
    h = h.cut(u)
    h = h.faces(">Z").edges().chamfer(CH)
    for x in (-S / 2, -S / 2 + T, S / 2 - T, S / 2):          # the U's arcs on both faces of both walls
        h = h.edges(cq.selectors.BoxSelector((x - 0.05, -U_R - 0.1, U_Z - U_R - 0.1),
                                             (x + 0.05, U_R + 0.1, H - CH - 0.05))).chamfer(CH)
    cs = [coaster(FLOOR + i * CT) for i in range(N)]
    return {
        "holder": Part(h, h, OFF),
        "coaster": Part(copies(cs), coaster(0), DARK, qty=N),
    }


SAMPLES["053_coaster_set_holder"] = coaster_set_holder
