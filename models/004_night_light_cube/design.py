"""004 Night light cube: a translucent 64 mm cube on a low base that runs 16 mm further back.

The strip of base left behind the cube carries the slide switch on top, so the switch is found by
touch in the dark without moving the light. Side profile: 80 deep and 80 high.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK, ACC,  # noqa: E402
                         box, cyl, rrect, rx, feet, plane_xz)

C, R = 64.0, 8.0                   # cube; R = 12.5 % of 64
LEDGE = 16.0                       # the base runs 16 further back: switch strip
D = C + LEDGE                      # base depth 80
HB = 16.0                          # base height; total 16 + 64 = 80 = depth
yc = -LEDGE / 2                    # cube centre (front flush with the base)
TRAVEL, NECK = 8.0, 2.4
YS = C / 2 + yc + (LEDGE - T) / 2  # switch on the middle of the visible strip
DIF = (0.99, 0.94, 0.80)           # translucent white, shown lit


def outline_wire(w, d, r, z):
    return rrect(w, d, r, z, 1.0).faces("<Z").wires().val()


def seat_ring(z_top):
    """Ring inside the base walls, top at z_top, 1.68 wide, with a 45-deg underside (prints bottom up)."""
    w, d, r = C - 2 * T, D - 2 * T, R - T
    band = rrect(w, d, r, z_top - DIV, DIV)
    cone = cq.Solid.makeLoft([outline_wire(w + 0.02, d + 0.02, r, z_top - DIV - 0.001),
                              outline_wire(w - 2 * DIV, d - 2 * DIV, r - DIV, z_top + 0.001)], True)
    return band.cut(cq.Workplane("XY").add(cone))


def night_light_cube():
    # base: sleeve with floor, printed bottom down
    zl = HB - T                                           # deck seat
    base = rrect(C, D, R, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    base = base.cut(rrect(C - 2 * T, D - 2 * T, R - T, T, HB))
    base = base.union(seat_ring(zl))
    base = base.cut(plane_xz(D / 2 + 1).center(0, (T + zl - DIV) / 2).slot2D(12.0, 6.4, 0).extrude(T + 2))  # USB-C
    base = feet(base, [(sx * 20, sy * 28) for sx in (-1, 1) for sy in (-1, 1)])

    # deck: closes the base inside its rim; window under the cube, a lip that locates the cube,
    # and the switch slot on the strip behind it
    deck = rrect(C - 2 * (T + GAP), D - 2 * (T + GAP), R - T - GAP, zl, T)
    lo = C - 2 * (T + GAP)                                # lip = deck edge: the cube wall is T, like the base
    win = lo - 2 * DIV
    deck = deck.cut(rrect(win, win, R - T - GAP - DIV, zl - 1, T + 2, 0, yc))
    lip = rrect(lo, lo, R - T - GAP, HB - 0.01, 4.0, 0, yc).cut(rrect(win, win, R - T - GAP - DIV, HB - 1, 6, 0, yc))
    lip = lip.intersect(rrect(C - 2 * (T + GAP), D - 2 * (T + GAP), R - T - GAP, 0, 40))
    deck = deck.union(lip)
    slot_l = TRAVEL + NECK + 0.6
    deck = deck.cut(rrect(slot_l, NECK + 0.6, (NECK + 0.6) / 2 - 0.001, zl - 1, T + 2, 0, YS))

    # diffuser: an open-bottomed cube printed top face down, walls and top 2.52 like the base
    dif = rrect(C, C, R, HB, C, 0, yc).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    dif = dif.cut(rrect(C - 2 * T, C - 2 * T, R - T, HB - 1, C - T + 1, 0, yc))

    # slide switch: knob on the strip (the accent), carrier under the deck, joined by a neck
    xs = -TRAVEL / 2                                      # shown at the "off" end
    knob = rrect(16.0, 8.0, 4.0 - 0.001, HB + 0.3, 2.4, xs, YS).faces(">Z").chamfer(CH)
    neck = cyl(NECK / 2, zl - 1.0, HB + 0.31 - zl + 1.0, xs, YS)       # round: the slot ends are round
    knob = knob.union(neck)
    cz1 = zl - 0.3                                        # carrier top, 0.3 under the deck
    carrier = box(xs - 8, xs + 8, YS - 4, YS + 4, cz1 - DIV, cz1)
    carrier = carrier.cut(cyl(NECK / 2 + 0.05, cz1 - 3, 4, xs, YS))   # glued or pressed on the neck
    carrier = carrier.cut(box(xs - 0.8, xs + 0.8, YS - 5, YS + 5, cz1 - DIV - 0.01, cz1 - 0.6))   # fork for the lever

    return {
        "base": Part(base, base, OFF),
        "deck": Part(deck, deck, OFF),
        "diffuser_translucent": Part(dif, rx(dif, 180), DIF),
        "slider_knob": Part(knob, rx(knob, 180), ACC),
        "slider_carrier": Part(carrier, carrier, DARK),
    }


SAMPLES["004_night_light_cube"] = night_light_cube
