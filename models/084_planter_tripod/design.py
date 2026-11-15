"""084 Planter on a tripod: a round cache pot, Ø104 x 96, standing on three tapered legs joined with steel dowels and glue.

The pot holds a 9 cm nursery pot (it has no drainage hole, so the water stays in the pot). Each leg is a flat tapered plate that
prints lying on its side, its outline on the bed, so it is strong along its length; two Ø4 steel dowels and glue join its flat top
to the pot's thick floor. In the leg the dowel holes are horizontal in the print and are teardrops; in the pot they are vertical.
The seam is a V line, C0.5 on both sides.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, CH, CH_BED, OFF, DARK, cyl, rx, rz, copies  # noqa: E402

D, HP = 104.0, 96.0                 # pot: Ø104, 96 high (height : diameter about 1 : 1)
HL = 48.0                           # legs: half the pot's height; the whole is 144 = 3 : 2 of the pot
FLOOR = 8.0                         # thick floor: takes the dowels and keeps the weight low
LT = 12.0                           # leg plate thickness
TOP = (26.0, 50.0)                  # leg top under the pot, radially: 24 long, 2 inside the pot's edge
FOOT = (52.0, 64.0)                 # leg foot, radially: 12 long, the outer end 12 beyond the pot
PINS = (32.0, 44.0)                 # two dowels per leg, 12 apart
PIN_D, PIN_DEPTH, PIN_L = 4.2, 6.25, 12.0   # Ø4 dowel in a Ø4.2 hole; 12 long, 6 in each part
ANGLES = (90.0, 210.0, 330.0)
K = 0.70710678


def teardrop_zy(x, y, z0, h, r):
    """Round hole along Z with a 45-deg roof toward +Y (up when the leg lies on its side)."""
    tri = [(x - r * K, y + r * K), (x, y + r * 1.41421356), (x + r * K, y + r * K), (x, y)]
    w = cq.Workplane("XY").workplane(offset=z0)
    return w.center(x, y).circle(r).extrude(h).union(w.polyline(tri).close().extrude(h))


def leg_local():
    """One leg in its radial plane: local +X outward, Z up, the top face at z = HL."""
    pts = [(TOP[0], HL), (TOP[1], HL), (FOOT[1], 0), (FOOT[0], 0)]
    lg = cq.Workplane("XZ").workplane(offset=-LT / 2).polyline(pts).close().extrude(LT)
    lg = lg.faces("<Y").edges().chamfer(CH_BED).faces(">Y").edges().chamfer(CH)   # -Y face on the bed in the print
    lg = lg.edges("|Y").chamfer(CH)                                       # the outline's corners; the top: its half of the V line
    for x in PINS:
        lg = lg.cut(teardrop_zy(x, 0, HL - PIN_DEPTH, PIN_DEPTH + 1, PIN_D / 2))
    return lg


def planter_tripod():
    pot = cyl(D / 2, HL, HP).faces("<Z").chamfer(CH_BED).faces(">Z").edges().chamfer(CH)
    pot = pot.cut(cyl(D / 2 - T, HL + FLOOR, HP)).faces(">Z").edges().chamfer(CH)
    pins = []
    for a in ANGLES:
        for x in PINS:
            pot = pot.cut(rz(cyl(PIN_D / 2, HL - 1, PIN_DEPTH + 1, x), a))
            entry = cq.Solid.makeCone(PIN_D / 2 + CH_BED + 0.01, PIN_D / 2, CH_BED + 0.01, pnt=cq.Vector(x, 0, HL - 0.01))
            pot = pot.cut(rz(cq.Workplane("XY").add(entry), a))              # the hole's mouth on the bed face: C0.6
            pins.append(rz(cyl(2.0, HL - PIN_L / 2, PIN_L, x), a))
    lg = leg_local()
    return {
        "pot": Part(pot, pot.translate((0, 0, -HL)), OFF),
        "leg": Part(copies([rz(lg, a) for a in ANGLES]), rx(lg, 90).translate((0, 0, LT / 2)), DARK, qty=3),
        "dowels_steel_ref": Part(copies(pins), None, (0.6, 0.6, 0.62), qty=6, ref=True),
    }


SAMPLES["084_planter_tripod"] = planter_tripod
