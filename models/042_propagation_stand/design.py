"""042 Propagation stand: three 16 mm test tubes of water for cuttings, held by a bridge on a floating base.

The base is a 128 x 64 block on a plinth set 1.2 in, twice as deep as the bridge; three shallow seats take the round bottoms of the
tubes. The bridge is an inverted U of 8 thick plate: the top bar has three holes the tubes pass through,
and the two legs end in tenons that locate in pockets in the base (a step of DIV, 0.25 clearance), so
the bridge lifts off to clean the base. The bridge prints on its front face, so its profile lies in the
layers and the holes are teardrops; the base prints bottom down.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, DIV, CH, CH_BED, GAP, OFF, box, cyl, rx,  # noqa: E402
                         chamfer_rim, feet, plane_xz)

L, D, DB = 128.0, 32.0, 64.0  # bridge 4 : 1, its depth the tube pitch; base 2 : 1, twice as deep, so it does not tip
RO, R = 12.0, 4.0             # bridge: outside top corners (1.5 x the plate), inside corners under the bar (half the plate)
HB = 12.0                     # base height
INSET = 1.2                   # floating plinth
PL = 8.0                      # bridge plate: top bar and legs
HBR = 96.0                    # bridge height above the base
PITCH = 32.0
TUBE_D, TUBE_L = 16.0, 150.0  # a common 16 x 150 test tube (check yours)
HOLE = TUBE_D + 2 * GAP
SEAT = 6.0                    # seat depth in the base
TEN = 4.0                     # tenon length; pocket 0.25 deeper and 0.25 wider per side
XS = (-PITCH, 0.0, PITCH)


def tube(x):
    """A test tube in place: a Ø16 cylinder with a round bottom resting on the seat floor (not a part)."""
    r = TUBE_D / 2
    z0 = HB - SEAT
    return cyl(r, z0 + r, TUBE_L - r, x).union(
        cq.Workplane("XZ").sphere(r).translate((x, 0, z0 + r)))


def propagation_stand():
    base = box(-L / 2 + INSET, L / 2 - INSET, -DB / 2 + INSET, DB / 2 - INSET, 0, INSET + 0.01).faces("<Z").chamfer(CH_BED)
    base = base.union(box(-L / 2, L / 2, -DB / 2, DB / 2, INSET, HB).faces("<Z").chamfer(INSET)
                      .faces(">Z").chamfer(CH).edges("|Z").chamfer(CH))
    for x in XS:
        base = chamfer_rim(base.cut(cyl(HOLE / 2, HB - SEAT, SEAT + 1, x)).translate((-x, 0, 0)), HOLE / 2, HB).translate((x, 0, 0))
    xl = L / 2 - PL / 2                                       # leg centre
    tw, td = PL - 2 * DIV, D                                  # tenon: stepped in DIV across, flush front and back
    for s in (-1, 1):
        base = base.cut(box(s * xl - tw / 2 - GAP, s * xl + tw / 2 + GAP, -td / 2 - GAP, td / 2 + GAP, HB - TEN - GAP, HB + 1))
    base = feet(base, [(sx * 48, sy * 20) for sx in (-1, 1) for sy in (-1, 1)])

    top = HB + HBR
    xi = L / 2 - PL
    prof = [(-L / 2, HB), (-L / 2, top), (L / 2, top), (L / 2, HB), (xi, HB), (xi, top - PL), (-xi, top - PL), (-xi, HB)]
    br = plane_xz(D / 2).polyline(prof).close().extrude(D)
    for (x, z, r) in ((-L / 2, top, RO), (L / 2, top, RO), (-xi, top - PL, R), (xi, top - PL, R)):
        br = br.edges("|Y").edges(cq.selectors.BoxSelector((x - .05, -D, z - .05), (x + .05, D, z + .05))).fillet(r)
    br = br.faces("<Y").edges().chamfer(CH_BED).faces(">Y").edges().chamfer(CH)
    br = br.faces("<Z").edges("|Y").chamfer(CH)
    k = 0.70710678
    r = HOLE / 2
    for x in XS:                                              # teardrops: the bridge prints on its front face, +Y up
        roof = [(x - r * k, r * k), (x, r * 1.41421356), (x + r * k, r * k), (x, 0)]
        br = br.cut(cyl(r, top - PL - 1, PL + 2, x)).cut(
            cq.Workplane("XY").workplane(offset=top - PL - 1).polyline(roof).close().extrude(PL + 2))
    for s in (-1, 1):
        br = br.union(box(s * xl - tw / 2, s * xl + tw / 2, -td / 2, td / 2, HB - TEN, HB + 0.01).faces("<Z").chamfer(CH))
    return {
        "base": Part(base, base, OFF),
        "bridge": Part(br, rx(br, 90), OFF),
    }


SAMPLES["042_propagation_stand"] = propagation_stand
