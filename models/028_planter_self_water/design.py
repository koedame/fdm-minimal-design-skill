"""028 Self-watering planter: a Ø96 x 120 cylinder, a water reservoir 48 high with the pot hanging in it.

The pot's lower part is a spigot that drops inside the reservoir wall with 0.25 clearance (the Location
lip) and steps out on a 45-deg cone that sits on a 45-deg chamfer inside the reservoir rim, so the pot
hangs centred with its floor 36 up, above the water. The outside is one cylinder broken by a V seam.
A slotted tube stands in the middle of the reservoir and rises through a hole in the pot floor: soil
packed into it is the wick that draws water up into the pot. Water goes in through a tube in the pot
that runs down through its floor, and an overflow hole 4 under the pot floor keeps the soil out of the
water.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK, box, cyl, rz, teardrop_x  # noqa: E402

D, H = 96.0, 120.0                # width : height = 4 : 5
HR = 48.0                         # reservoir : visible pot = 2 : 3
FLOOR = 2.4
INSET, PL = 1.2, 2.4              # floating plinth, as 03_tray
RO = D / 2                        # 48
RI = RO - T                       # 45.48: reservoir inside, pot inside above the seam
RS = RI - GAP                     # 45.23: pot spigot outside
SEAT = 0.8                        # 45-deg chamfer inside the reservoir rim: the pot's seat
REST = 0.1                        # the pot cone rests 0.1 over the seat (contact)
ZC = HR - SEAT - (RI - RS) + REST # 47.05: the pot cone starts here, at the spigot radius
STEP = RO - RS                    # 2.77: the cone's run (and rise)
ZF = 36.0                         # pot floor underside: the spigot reaches 11 into the reservoir
Z_OVER = ZF - 4.0                 # overflow hole centre
WICK_R = 12.0                     # wick tube outside radius; wall DIV
FILL_R = 8.0                      # fill tube outside radius; wall DIV, top 4 under the rim


def revolve(pts):
    return cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0))


def planter_self_water():
    r_pl = RO - INSET
    res = revolve([(0, 0), (r_pl - CH_BED, 0), (r_pl, CH_BED), (r_pl, PL), (RO, PL + INSET), (RO, HR - CH), (RO - CH, HR),
                   (RI + SEAT, HR), (RI, HR - SEAT), (RI, FLOOR), (0, FLOOR)])
    wick = cyl(WICK_R, FLOOR - 0.01, ZF + 0.01)        # up to the top of the pot floor
    wick = wick.cut(cyl(WICK_R - DIV, FLOOR, ZF + 1))
    for i in range(8):                # slots from the floor up let the water in, 1.2 wide so the soil stays in
        wick = wick.cut(rz(box(WICK_R - DIV - 0.5, WICK_R + 0.5, -0.6, 0.6, FLOOR - 0.01, FLOOR + 16.0), i * 45))
    res = res.union(wick).cut(teardrop_x(RI - 0.5, T + 1, 0, Z_OVER, 2.0))

    ri_sp = RS - T                    # spigot inside: the wall runs through the cone at the same width
    pot = revolve([(0, ZF), (RS - CH_BED, ZF), (RS, ZF + CH_BED), (RS, ZC), (RO, ZC + STEP), (RO, H - CH), (RO - CH, H),
                   (RI + CH, H), (RI, H - CH), (RI, ZC + STEP), (ri_sp, ZC), (ri_sp, ZF + FLOOR), (0, ZF + FLOOR)])
    pot = pot.cut(cyl(WICK_R + 2 * GAP, ZF - 1, FLOOR + 2))
    xf = ri_sp - FILL_R + 0.6         # fill tube fused to the spigot wall
    fill = cyl(FILL_R, ZF, H - 4 - ZF, xf, 0).faces(">Z").chamfer(CH)
    pot = pot.union(fill).cut(cyl(FILL_R - DIV, ZF - 1, H, xf, 0))
    return {
        "pot": Part(pot, pot.translate((0, 0, -ZF)), OFF),
        "reservoir": Part(res, res, DARK),
    }


SAMPLES["028_planter_self_water"] = planter_self_water
