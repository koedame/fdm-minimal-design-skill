"""076 Modular desk organiser: open trays on a 64 grid that cling to each other side by side by magnets in their walls.

Two sizes, 64 x 64 and 128 x 64, 48 high; any side of one meets any side of another on the grid. Each 64 of every
side carries two 6 x 3 magnets standing on edge in slots that open at the top of small posts inside the wall, so
the slots open upward in the print and the magnets face the neighbour through 0.84 of wall. Seen from outside, the
left magnet of each pair has its north pole out and the right one its south pole, so two sides that meet always pair
north with south, whichever way round the trays stand. Each tray is a floating plinth; between two trays the plinths
leave one shadow groove.
"""
import os
import sys

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, OFF, ACC,  # noqa: E402
                         box, copies, cyl, rrect, rz, feet, plane_yz)

U, H = 64.0, 48.0                # grid unit 16 modules; height 3 : 4 of the unit
R = 8.0                          # plan radius 12.5 % of the unit
RI = 3.0                         # floor edge inside
FLOOR, PL, INSET = 2.4, 2.4, 1.2
MAG_X = 16.0                     # magnets at ±16 from the middle of each 64 (on the grid, inside the straight part of the side)
SKIN = 0.84                      # wall between magnet and outside: 2 lines
SLOT = (3.2, 6.4, 6.6)           # across the wall, along it, deep (a 6 x 3 disc standing on edge)
POST_W = 10.0                    # post along the wall
POST_H = 14.0                    # post top above the floor
POST_IN = SKIN + SLOT[0] + 1.0   # post reaches 5.04 in from the outside (1.0 behind the slot)


def _mag_spots(nx):
    """(x, y, angle) of every magnet on a tray nx units long: the slot centre on the outside face's normal."""
    w, d = nx * U, U
    spots = []
    for i in range(nx):
        xc = -w / 2 + U / 2 + i * U
        for s in (-1, 1):
            spots += [(xc + s * MAG_X, -d / 2, 0), (xc + s * MAG_X, d / 2, 180)]
    for s in (-1, 1):
        spots += [(-w / 2, s * MAG_X, 270), (w / 2, s * MAG_X, 90)]
    return spots


def tray(nx):
    w, d = nx * U, U
    b = rrect(w - 2 * INSET, d - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    b = b.union(rrect(w, d, R, PL, H - PL).faces("<Z").chamfer(INSET))
    cav = rrect(w - 2 * T, d - 2 * T, R - T, FLOOR, H).faces("<Z").edges().fillet(RI)
    b = b.cut(cav)
    zt = FLOOR + POST_H
    for (x, y, a) in _mag_spots(nx):
        # build at the -Y side (outside face y = 0, inside toward +y), then turn and move to the spot
        post = box(-POST_W / 2, POST_W / 2, T - 0.5, POST_IN, FLOOR - 0.1, zt)
        b = b.union(rz(post, a).translate((x, y, 0)) if a else post.translate((x, y, 0)))
    b = b.faces(">Z").chamfer(CH)
    for (x, y, a) in _mag_spots(nx):                 # after every union: nothing refills the slots
        slot = box(-SLOT[1] / 2, SLOT[1] / 2, SKIN, SKIN + SLOT[0], zt - SLOT[2], zt + 1)
        b = b.cut(rz(slot, a).translate((x, y, 0)) if a else slot.translate((x, y, 0)))
    centres = [-w / 2 + U / 2 + i * U for i in range(nx)]
    b = feet(b, [(xc + sx * 18, sy * 18) for xc in centres for sx in (-1, 1) for sy in (-1, 1)])
    return b


def magnets(nx, at):
    zt = FLOOR + POST_H
    out = []
    for (x, y, a) in _mag_spots(nx):
        m = plane_yz(-1.5 + 0.05).center(0, zt - SLOT[2] + 3.15).circle(3.0).extrude(3.0 - 0.1)
        m = rz(m, 90).translate((0, SKIN + SLOT[0] / 2, 0))      # disc axis across the wall
        m = rz(m, a) if a else m
        out.append(m.translate((x + at[0], y + at[1], 0)))
    return out


def desk_organiser_modular():
    sq = tray(1)
    lg = tray(2)
    squares = [sq.translate((-U / 2, U / 2, 0)), sq.translate((U / 2, U / 2, 0))]
    mags = magnets(1, (-U / 2, U / 2)) + magnets(1, (U / 2, U / 2)) + magnets(2, (0, -U / 2))
    return {
        "tray_square": Part(copies(squares), sq, OFF, qty=2),
        "tray_long": Part(lg.translate((0, -U / 2, 0)), lg, OFF),
        "magnet_ref": Part(copies(mags), None, ACC, qty=len(mags), ref=True),
    }


SAMPLES["076_desk_organiser_modular"] = desk_organiser_modular
