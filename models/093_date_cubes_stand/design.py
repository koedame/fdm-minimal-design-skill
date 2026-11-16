"""093 Date cubes and stand: two 31.5 cubes with a seven-segment digit on every face, standing in a 76 x 40 plinth.

The two cubes show every day of the month: one carries 0 1 2 3 4 5, the other 0 1 2 6 7 8, and its 6 turned over reads 9
(a seven-segment 6 upside down is a 9). Every digit is the same seven stadium segments, 20 high, inlaid 0.4 in dark in the
off-white cube (the inlay is printed as layers of another colour, so no face has a recess to bridge). The plinth has two
square pockets 4 deep, 0.25 round each cube, and floats on a 1.2 shadow line as 03_tray.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, CH, CH_BED, GAP, OFF, PLATE, DARK, box, rrect, rx, rz  # noqa: E402

M = 4.0                                   # margin round and between the pockets
P = 32.0                                  # pocket: 8 modules
S = P - 2 * GAP                           # cube 31.5, 0.25 inside its pocket
W, D, H, R = 2 * P + 3 * M, P + 2 * M, 8.0, 6.0   # 76 x 40 x 8; R6 = 15 % of the depth
PL, INSET = 2.4, 1.2                      # floating plinth
DEPTH = H / 2                             # pockets 4 deep
XC = P / 2 + M / 2                        # cube centres at x = ±18
ZC = H - DEPTH + S / 2
DH, DW, SW, SG = 20.0, 12.0, 2.4, 1.6     # digit height, width (5 : 3), segment width, gap at each end
INLAY = 0.4
SEGS = {"a": ((-1, 1), (1, 1)), "b": ((1, 0), (1, 1)), "c": ((1, -1), (1, 0)), "d": ((-1, -1), (1, -1)),
        "e": ((-1, -1), (-1, 0)), "f": ((-1, 0), (-1, 1)), "g": ((-1, 0), (1, 0))}
DIGITS = {0: "abcdef", 1: "bc", 2: "abdeg", 3: "abcdg", 4: "bcfg", 5: "acdfg", 6: "acdefg", 7: "abc", 8: "abcdefg"}
# faces: front (-Y, shown), top, back, left, right, bottom
CUBES = {"cube_a": (-XC, (1, 0, 2, 3, 4, 5)), "cube_b": (XC, (6, 0, 1, 2, 7, 8))}


def digit(n, z0, h):
    """A seven-segment digit in the XY plane, centred on the origin, z0 to z0 + h: one stadium per segment."""
    out = None
    for s in DIGITS[n]:
        (x0, y0), (x1, y1) = SEGS[s]
        p0 = (x0 * DW / 2, y0 * DH / 2)
        p1 = (x1 * DW / 2, y1 * DH / 2)
        horiz = y0 == y1
        c = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
        length = abs(p1[0] - p0[0]) if horiz else abs(p1[1] - p0[1])
        seg = (cq.Workplane("XY").workplane(offset=z0).center(*c)
               .slot2D(length - 2 * SG + SW, SW, 0 if horiz else 90).extrude(h))
        out = seg if out is None else out.union(seg)
    return out


def on_faces(digits, z0, h):
    """The six digits moved onto the faces of a cube centred on the origin (side digits upright, the top's head to +Y)."""
    front = lambda s: rx(s, 90).translate((0, -S / 2, 0))   # noqa: E731
    moves = (front, lambda s: s.translate((0, 0, S / 2)), lambda s: rz(front(s), 180),
             lambda s: rz(front(s), -90), lambda s: rz(front(s), 90), lambda s: rx(s, 180).translate((0, 0, -S / 2)))
    out = None
    for n, mv in zip(digits, moves):
        d = mv(digit(n, z0, h))
        out = d if out is None else out.union(d)
    return out


def date_cubes_stand():
    stand = rrect(W - 2 * INSET, D - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    stand = stand.union(rrect(W, D, R, PL, H - PL).faces("<Z").chamfer(INSET))
    for sx in (-1, 1):
        stand = stand.cut(box(sx * XC - P / 2, sx * XC + P / 2, -P / 2, P / 2, H - DEPTH, H + 1))
    stand = stand.faces(">Z").edges().chamfer(CH)                # the outline and the pockets' rims
    parts = {"stand": Part(stand, stand, PLATE)}
    for name, (xc, digits) in CUBES.items():
        c = cq.Workplane("XY").box(S, S, S).edges("|Z").chamfer(CH).faces(">Z").edges().chamfer(CH)
        c = c.faces("<Z").edges().chamfer(CH_BED)
        c = c.cut(on_faces(digits, -INLAY, INLAY + 1))
        inlay = on_faces(digits, -INLAY, INLAY)
        place = (xc, 0, ZC)
        down = (0, 0, S / 2)
        parts[name] = Part(c.translate(place), c.translate(down), OFF)
        parts[name + "_digits_inlay"] = Part(inlay.translate(place), inlay.translate(down), DARK, anchor=name)
    return parts


SAMPLES["093_date_cubes_stand"] = date_cubes_stand
