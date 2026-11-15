"""090 Cotton swab holder: a 56 x 56 rounded-square jar, 84 high, in which about a hundred cotton swabs stand on end, with a cap
that locates on a lip.

The body is 64 high; the swabs (75 long) stand 13 above its rim, so one can be taken by its end. The cap, 20 high, covers them; a
DIV lip on the body's rim fits 0.25 inside the cap's wall and keeps it in place. The lip hangs from a band that thickens the body's
wall at the rim, with a 45-deg underside so it prints upright.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, rrect  # noqa: E402

S, R = 56.0, 8.0                         # 14 modules; R8 = 14.3 %
HB, HL = 64.0, 20.0                      # body and cap: the seam at 64 of 84
FLOOR, TOP = 2.4, 2.4
LIP = 4.0                                # the lip stands 4 above the body's rim
BAND = 4.0                               # the thickened wall below the rim that carries the lip
I_LIP = T + GAP                          # lip's outer face, inset from the outline
I_IN = T + GAP + DIV                     # lip's and band's inner face


def inset(i, z0, t):
    return rrect(S - 2 * i, S - 2 * i, R - i, z0, t)


def cotton_swab_holder():
    body = rrect(S, S, R, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    body = body.union(inset(I_LIP, HB - 1, LIP + 1))                               # the lip's outside, before the cavity
    z_band = HB - BAND
    dz = I_IN - T                                                                   # the band's 45-deg underside
    w0 = inset(T, z_band - dz, 1).faces("<Z").wires().val()
    w1 = inset(I_IN, z_band, 1).faces("<Z").wires().val()
    under = cq.Workplane("XY").add(cq.Solid.makeLoft([w0, w1], True))
    body = body.cut(inset(T, FLOOR, z_band - dz - FLOOR + .01)).cut(under).cut(inset(I_IN, z_band - .01, HB + LIP))
    body = body.faces(">Z").edges().chamfer(CH)                                     # the lip's top edges

    cap = rrect(S, S, R, HB, HL).faces(">Z").chamfer(CH_BED).faces("<Z").chamfer(CH)   # the top is its bed face
    cap = cap.cut(inset(T, HB - 1, HL - TOP + 1))
    cap_print = cap.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, HB + HL))
    return {"body": Part(body, body, OFF), "cap": Part(cap, cap_print, OFF)}


SAMPLES["090_cotton_swab_holder"] = cotton_swab_holder
