"""045 Tube speaker and cradle: a Ø64 x 128 tube lying on its side, a 57 mm driver in its front end, resting in a low cradle.

The tube prints standing on its closed back. A front cap closes it: its face is a field of small holes over the driver cone, and
its spigot, sealed and held by an O-ring, clamps the driver's frame against a ledge inside the tube. The cradle is a 56 x 96 block
with a saddle; a V rib across the saddle drops into a V groove round the tube, so the tube cannot slide out forward or back, yet
lifts straight off. The cap's seam is the same 45-deg V as the groove, so the tube carries two equal lines, and a fingernail in
the seam levers the cap out.
"""
import math
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, cyl, rrect, rx, feet)

RO, L = 32.0, 128.0                     # tube: Ø64 x 128 overall (2 : 1)
PLT = 2.4                               # cap plate, back floor
LT = L - PLT                            # tube body length; the cap plate makes up the rest
RB = RO - T                             # bore radius 29.48
DRV = (57.0, 3.0, 30.0)                 # driver: frame Ø, frame thickness, depth behind the frame (check yours)
SP = 8.0                                # cap spigot length
SPI = 26.0                              # spigot inner radius: its end presses the frame between r 26 and 28.5
OR_D = 2.0                              # O-ring cord; groove 1.4 deep, so the cord is squeezed 0.35 (17.5 %)
GD, GW = 1.4, 2.6
LEDGE_R = 25.5                          # ledge inner radius: the basket passes, the frame rests on r 25.5..28.5
HOLE_D, HOLE_P, FIELD_R = 2.4, 4.0, 22.0
VH = 0.8                                # cradle V rib height; the groove is 0.25 larger normal to its flanks
CW, CL, CHT, CR = 56.0, 96.0, 14.0, 8.0   # cradle width, length, height, plan corner radius
BASE = 6.0                              # tube bottom above the desk
ZA = BASE + RO + GAP                    # tube axis above the desk


def rev(pts):
    """A solid of revolution about Z from an (r, z) outline."""
    return cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0))


def ring_v(r_out, depth, z):
    """A 45-deg V ring of the given depth at height z, pointing in from a cylinder of radius r_out (axis Z)."""
    return rev([(r_out, z - depth), (r_out - depth, z), (r_out, z + depth)])


def tube_speaker_cradle():
    # tube, local: axis Z, back face on z = 0, front end at z = LT
    z_frame = LT - SP                                        # front face of the driver frame (pressed by the spigot)
    z_ledge = z_frame - DRV[1]                               # ledge face
    gd = VH + 0.35                                           # groove depth; the seam with the cap is the same V
    tb = cyl(RO, 0, LT).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(gd)
    tb = tb.cut(cyl(RB, PLT, LT))
    z1 = z_ledge - 2.4
    z0 = z1 - (RB - LEDGE_R)
    tb = tb.union(rev([(LEDGE_R, z_ledge), (RB + 0.5, z_ledge), (RB + 0.5, z0), (RB, z0), (LEDGE_R, z1)]))   # 45-deg underside
    z_g = L / 2                                              # the groove under the cradle's middle
    tb = tb.union(rev([(RB + 0.5, z_g - 4.2), (RB, z_g - 4.2), (RB - 1.2, z_g - 3.0), (RB - 1.2, z_g + 3.0),
                       (RB, z_g + 4.2), (RB + 0.5, z_g + 4.2)]))   # wall thickened inside behind the groove
    tb = tb.cut(ring_v(RO + 0.01, gd + 0.01, z_g))
    tb = tb.cut(cyl(2.2, -1, PLT + 2, 0, -RO + 10))          # cable, low in the back

    # cap, local: front face on z = 0 (printed face down), spigot up
    cp = cyl(RO, 0, PLT).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(VH + 0.35)   # half of the seam's V: a nail lifts it
    cp = cp.union(cyl(RB - GAP, PLT - 0.01, SP + 0.01).faces(">Z").chamfer(CH)).cut(cyl(SPI, PLT, SP + 1))
    zg = PLT + SP / 2
    groove = (cq.Workplane("XZ").polyline([(RB - GAP - GD, zg - GW / 2), (RB, zg - GW / 2), (RB, zg + GW / 2 + GD),
                                           (RB - GAP - GD, zg + GW / 2)]).close().revolve(360, (0, 0, 0), (0, 1, 0)))
    cp = cp.cut(groove)                                      # flat bottom flank, 45-deg top flank: no overhang printed face down
    n = int(FIELD_R // HOLE_P)
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            x, y = i * HOLE_P, j * HOLE_P
            if math.hypot(x, y) <= FIELD_R:
                cp = cp.cut(cyl(HOLE_D / 2, -1, PLT + 2, x, y))

    drv = cyl(DRV[0] / 2, z_ledge, DRV[1]).union(cyl(23.0, z_ledge - DRV[2], DRV[2] + 0.01))

    # cradle, local = world: axis along Y at z = ZA
    cr = rrect(CW, CL, CR, 0, CHT).faces("<Z").chamfer(CH_BED).edges(">Z").chamfer(CH)
    saddle = rx(cyl(RO + GAP, -CL, 2 * CL), 90).translate((0, 0, ZA))
    cr = cr.cut(saddle)
    rib = ring_v(RO + GAP + 0.01, VH + 0.01, 0)
    rib = rx(rib, 90).translate((0, 0, ZA)).intersect(box(-CW / 2, CW / 2, -4, 4, 0, CHT))
    cr = cr.union(rib)
    cr = feet(cr, [(sx * 18.0, sy * 36.0) for sx in (-1, 1) for sy in (-1, 1)])

    def place(wp, z0):                                       # local axis Z -> world -Y; local z0 on world y = 0
        return rx(wp.translate((0, 0, -z0)), 90).translate((0, 0, ZA))
    cap_d = rx(cp, 180).translate((0, 0, L))                 # face at z = L, spigot down into the tube
    return {
        "tube": Part(place(tb, L / 2), tb, OFF),
        "cap": Part(place(cap_d, L / 2), cp, DARK),
        "cradle": Part(cr, cr, OFF),
        "driver_ref": Part(place(drv, L / 2), None, DARK, ref=True),
    }


SAMPLES["045_tube_speaker_cradle"] = tube_speaker_cradle
