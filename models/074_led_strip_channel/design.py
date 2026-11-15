"""074 LED strip channel: a 192 long, 20 x 20 channel for LED tape up to 12 wide, closed by a translucent diffuser that snaps on.

The channel is a U profile open at both ends (square in plan, so lengths butt into a longer run), printed floor down.
The tape sticks to the floor; two countersunk screws under it hold the channel (or double-sided tape). The diffuser
is a 1.68 translucent plate with the channel's width; eight vertical hooks hang from it inside the walls and their
45-deg barbs drop into V grooves that run the whole length of the walls. The seam is a V line with C0.5 on both sides.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF,  # noqa: E402
                         box, copies, cyl, rx, plane_yz)

TRANSLUCENT = (0.96, 0.95, 0.90)          # natural / translucent PLA
L, W, H = 192.0, 20.0, 20.0              # 48 x 5 x 5 modules
FLOOR = 2.4
Z_SEAM = H - DIV                         # the diffuser is DIV thick (an even glow)
TAPE_W, TAPE_T = 12.0, 2.0               # widest tape it takes; tape + adhesive
HOOK_X, HOOK_W = (24.0, 72.0), 16.0      # hooks at x ±24 and ±72 (pitch 48), 16 wide
HOOK_Z0 = 8.0                            # hook bottom: 3.6 above the tape's top
BARB_Z, BARB = 9.4, 0.6                  # barb centre and height; free length about 9: strain about 1.1 % at 0.35 deflection
SCREW_X = 48.0                           # between the hooks; 3.5 countersunk wood screws, head 7


def led_strip_channel():
    yi = W / 2 - T
    b = box(-L / 2, L / 2, -W / 2, W / 2, 0, Z_SEAM)
    b = b.faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    b = b.cut(box(-L / 2 - 1, L / 2 + 1, -yi, yi, FLOOR, H))
    for x in (-L / 2, L / 2):                                 # the channel's inside edges in the open ends
        b = b.edges(cq.selectors.BoxSelector((x - 0.05, -yi - 0.05, FLOOR - 0.05),
                                             (x + 0.05, yi + 0.05, Z_SEAM - CH - 0.05))).chamfer(CH)
    for sx in (-1, 1):
        b = b.cut(cyl(1.9, -1, FLOOR + 2, sx * SCREW_X, 0))
        b = b.cut(cq.Workplane("XY").add(cq.Solid.makeCone(1.9, 3.6, 1.7, pnt=cq.Vector(sx * SCREW_X, 0, FLOOR - 1.7 + 0.001))))
    for sy in (-1, 1):                                        # V grooves the whole length: barb + 0.25 all round, 45 deg
        g = plane_yz(-L / 2 - 1).polyline(
            [(sy * (yi - 0.01), BARB_Z - BARB - 0.35), (sy * (yi + BARB + 0.25), BARB_Z - 0.1),
             (sy * (yi + BARB + 0.25), BARB_Z + 0.1), (sy * (yi - 0.01), BARB_Z + BARB + 0.35)])
        b = b.cut(g.close().extrude(L + 2))

    d = box(-L / 2, L / 2, -W / 2, W / 2, Z_SEAM, H).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    yo = yi - GAP
    for hx in HOOK_X:
        for sx in (-1, 1):
            for sy in (-1, 1):
                x = sx * hx
                y0, y1 = sorted((sy * (yo - DIV), sy * yo))
                d = d.union(box(x - HOOK_W / 2, x + HOOK_W / 2, y0, y1, HOOK_Z0, Z_SEAM + 0.01))
                d = d.union(plane_yz(x - HOOK_W / 2).polyline(
                    [(sy * (yo - 0.01), BARB_Z - BARB), (sy * (yo + BARB), BARB_Z), (sy * (yo - 0.01), BARB_Z + BARB)])
                    .close().extrude(HOOK_W))

    tape = box(-L / 2, L / 2, -TAPE_W / 2, TAPE_W / 2, FLOOR, FLOOR + TAPE_T)
    return {
        "channel": Part(b, b, OFF),
        "diffuser": Part(d, rx(d, 180), TRANSLUCENT),
        "tape_ref": Part(tape, None, TRANSLUCENT, ref=True),
    }


SAMPLES["074_led_strip_channel"] = led_strip_channel
