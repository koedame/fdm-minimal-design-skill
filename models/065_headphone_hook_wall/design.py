"""065 Wall headphone hook: a plate on two hidden keyholes with one round-ended arm that a headband hangs on.

One part, printed with the wall face down. The plate is 48 x 96 (1 : 2), set 1.2 in from the wall at 45 deg so
it sits on a shadow line. The arm, 32 x 16, runs 80 forward at two-thirds of the plate's height; its last 6 rise 6
on a 45-deg ramp, so a headband stays on. One radius, R6, for the plate's corners, the arm's corners and the arm's
root. In the print the plate and the arm's section lie in the layer plane: every radius is a
curve in plan, and the keyholes in the wall face print face down.
"""
import os
import sys

import cadquery as cq
from cadquery.selectors import BoxSelector

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, CH, CH_BED, OFF, rrect, rx, keyhole_local)  # noqa: E402

W, H, R = 48.0, 96.0, 6.0         # plate 12 x 24 modules; R6 (12.5 % of the width) for the plate, the arm and its root
PT = 6.4                          # plate: keyhole ledge 2 + head pocket 3 + 1.4
INSET = 1.2                       # shadow line against the wall
AW, AT = 32.0, 16.0               # arm section, R6 corners: 2 : 1, a headband's width
AZ = H * 2 / 3                    # arm centre at two-thirds of the height (64)
AL = 80.0                         # arm reach from the plate = 5 x its thickness: the cups (to 90) clear the wall
LIP = 6.0                         # the last 6 rise 6 at 45 deg
R_ROOT = R                        # arm to plate; leaves 2 of flat plate beside it
KEY_Z, TRAVEL = (24.0, 80.0), 6.0  # keyhole entries on the centre line, below and above the arm


def section(z0, h, rise=0.0):
    """The arm's section, 32 x 16 with R6 corners; `rise` raises its top and keeps its bottom."""
    return rrect(AW, AT + rise, R, z0, h, cy=AZ + rise / 2)


def headphones():
    """A headband over the arm as an envelope: 36 wide (along the arm), 6 thick, R60 inside, resting on the arm's two
    top corners (its arch is tangent to their R6); not a part."""
    zc = AZ + AT / 2 - R - ((60 - R) ** 2 - (AW / 2 - R) ** 2) ** 0.5 + 0.05
    band = (cq.Workplane("XZ").circle(66).circle(60).extrude(18, both=True)
            .intersect(cq.Workplane("XY").box(200, 200, 200).translate((0, 0, 100 - 20))))
    return band.translate((0, -(PT + AL / 2 + 6), zc))


def headphone_hook_wall():
    # print frame: x = across, y = up the wall, z = out from the wall (wall face at z = 0)
    plate = rrect(W - 2 * INSET, H - 2 * INSET, R - INSET, 0, INSET, cy=H / 2).faces("<Z").chamfer(CH_BED)
    plate = plate.union(rrect(W, H, R, INSET, PT - INSET, cy=H / 2).faces("<Z").chamfer(INSET))
    z0 = PT + AL - 2 * LIP                                           # the ramp starts here
    hook = plate.union(section(PT - 0.01, z0 - PT + 0.01))
    hook = hook.edges(BoxSelector((-AW / 2 - 1, AZ - AT / 2 - 1, PT - 0.05), (AW / 2 + 1, AZ + AT / 2 + 1, PT + 0.05))) \
        .fillet(R_ROOT)
    hook = hook.edges(BoxSelector((-W, -1, PT - 0.05), (W, H + 1, PT + 0.05))).edges(
        cq.selectors.InverseSelector(BoxSelector((-AW / 2 - R_ROOT - 1, AZ - AT / 2 - R_ROOT - 1, PT - 0.1),
                                                 (AW / 2 + R_ROOT + 1, AZ + AT / 2 + R_ROOT + 1, PT + 0.1)))).chamfer(CH)
    end = cq.Solid.makeLoft([section(z, 1, r).faces("<Z").wires().val()                # ramp and lip, one loft
                             for z, r in ((z0, 0), (z0 + LIP, LIP), (z0 + 2 * LIP, LIP))], True)
    hook = hook.union(cq.Workplane("XY").add(end))
    hook = hook.faces(">Z").edges().chamfer(CH)                       # the arm's end face
    for z in KEY_Z:
        hook = hook.cut(keyhole_local(TRAVEL).translate((0, z, 0)))
    return {"hook": Part(rx(hook, 90).translate((0, 0, 0)), hook, OFF)}


SAMPLES["065_headphone_hook_wall"] = headphone_hook_wall
