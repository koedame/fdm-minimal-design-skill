"""009 Key rail: a plain 160 x 32 bar on the wall that holds keys by their steel rings on hidden magnets.

Five magnets sit in blind holes from the back, 0.84 behind the front face, so the front is one
unbroken face. Two keyholes for countersunk screws are pocketed in the back: the screw head seats
on a 45-deg cone, which is also what lets the bar print face down without supports.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, CH, CH_BED, OFF, cyl, rrect, rx, rz)  # noqa: E402

L, H, D, R = 160.0, 32.0, 12.0, 4.0      # 5:1 face; R = 12.5 % of 32
SKIN = 0.84                              # in front of the magnets: 4 layers at 0.2
MAG_D = 10.2                             # Ø10 x 3 magnets
MAG_X = [-64.0, -32.0, 0.0, 32.0, 64.0]  # pitch 32, 16 from the ends
KEY_X, KZ0, TRAVEL = 48.0, 12.0, 8.0     # keyholes: entry centre 12 up, the bar drops 8 onto the screws
HEAD, SHANK = 8.4, 4.4                   # countersunk screw, head up to Ø8
LEDGE = 2.0                              # back ledge the head hooks behind


def stadium(w, z0, t, x, y0, y1):
    return rrect(w, (y1 - y0) + w, w / 2 - 0.001, z0, t, x, (y0 + y1) / 2)


def stadium_wire(w, z, x, y0, y1):
    return stadium(w, z, 1.0, x, y0, y1).faces("<Z").wires().val()


def key_rail():
    # local frame: front view in XY (y up), z = depth, front face on z = 0 (the print bed)
    bar = rrect(L, H, R, 0, D, 0, H / 2)
    bar = bar.faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    for x in MAG_X:
        bar = bar.cut(cyl(MAG_D / 2, SKIN, D, x, H / 2))
    for x in (-KEY_X, KEY_X):
        y0, y1 = KZ0, KZ0 + TRAVEL
        zl = D - LEDGE                                      # ledge face, inside
        zc = zl - (HEAD - SHANK) / 2                        # start of the 45-deg seat
        bar = bar.cut(stadium(SHANK, zl - 0.01, LEDGE + 1, x, y0, y1))          # slot through the ledge
        bar = bar.cut(cyl(HEAD / 2, zc - 3.0, D, x, y0))                         # entry hole
        bar = bar.cut(stadium(HEAD, zc - 3.0, 3.01, x, y0, y1))                  # head pocket
        seat = cq.Solid.makeLoft([stadium_wire(HEAD, zc, x, y0, y1), stadium_wire(SHANK, zl + 0.001, x, y0, y1)], True)
        bar = bar.cut(cq.Workplane("XY").add(seat))
    to_wall = lambda wp: rz(rx(wp, 90), 180)                # front faces -Y, back on the wall at y = +D
    return {"rail": Part(to_wall(bar), bar, OFF)}


SAMPLES["009_key_hook_rail"] = key_rail
