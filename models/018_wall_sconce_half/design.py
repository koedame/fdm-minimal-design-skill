"""018 Wall sconce: a half cylinder (R48) on the wall in three tiers: base 48, translucent diffuser 64, cap 16.

The tiers stack on lips as in 10_lantern. The base hangs on two keyholes in pads on its back wall; the
entry holes have 45-deg shoulders and the head pockets round tops, so the base prints bottom down
without support. A slide switch runs in a vertical slot in the middle of the curved front; its knob is
curved to the wall, and its neck is round, as the slide switch rule asks.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK, ACC,  # noqa: E402
                         box, cyl, rx, plane_xz)

R = 48.0                           # Ø96 half cylinder: 96 wide, 48 deep
HB, HD, HC = 48.0, 64.0, 16.0      # base : diffuser : cap = 3 : 4 : 1, total 128 = 4 x 32
FLOOR = TOP = 2.4
WD = DIV                           # diffuser wall 1.68 (an even glow)
KX, KZ, TRAVEL = 24.0, 20.0, 8.0   # keyholes 48 apart (half the width); entry 20 up, the lamp drops 8
HEAD, SHANK, LEDGE, POCKET, PAD = 8.4, 4.2, 2.0, 3.0, 6.0
SW_TRAVEL, SLOT_W = 8.0, 3.0       # switch: mid-travel at mid-height of the base
NECK_D = SLOT_W - 2 * GAP          # round neck, 2.5
DIF = (0.99, 0.94, 0.80)           # translucent white, shown lit


def dsh(d, z0, h, r=R):
    """Half disc against the wall (y <= 0), offset inward by d (also from the wall), from z0 up h."""
    return cyl(r - d, z0, h).intersect(box(-r, r, -r, -d, z0 - 1, z0 + h + 1))


def keyhole_profile(y0, depth, x, z, r, slot_len, slot_w):
    """In the XZ plane at y0, extruded toward -y: an entry circle with 45-deg shoulders and a slot rising slot_len."""
    k = 0.70710678
    entry = plane_xz(y0).center(x, z).circle(r).extrude(depth)
    roof = plane_xz(y0).polyline([(x - r * k, z + r * k), (x, z + r * 1.41421356), (x + r * k, z + r * k), (x, z)]).close().extrude(depth)
    slot = plane_xz(y0).center(x, z + slot_len / 2).slot2D(slot_len + slot_w, slot_w, 90).extrude(depth)
    return entry.union(roof).union(slot)


def wall_sconce_half():
    lo, li = WD + GAP, WD + GAP + DIV           # lip offsets, as 10_lantern
    base = dsh(0, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    base = base.cut(dsh(T, FLOOR, HB))
    base = base.union(dsh(lo, HB - 1, 4.01).cut(dsh(li, HB - 2, 7)))
    for sx in (-1, 1):
        x = sx * KX
        base = base.union(box(x - 8, x + 8, -PAD, -T + 0.01, FLOOR - 0.01, HB - 4))
        base = base.cut(keyhole_profile(1.0, LEDGE + 1.0, x, KZ, HEAD / 2, TRAVEL, SHANK))      # through the ledge
        base = base.cut(plane_xz(-LEDGE).center(x, KZ + TRAVEL / 2).slot2D(TRAVEL + HEAD, HEAD, 90).extrude(POCKET))
    base = base.cut(cyl(3.0, -1, FLOOR + 2, 0, -12.0))                         # cable, down the wall

    zc = HB / 2
    z0, z1 = zc - SW_TRAVEL / 2 - SLOT_W / 2, zc + SW_TRAVEL / 2 + SLOT_W / 2
    base = base.cut(box(-SLOT_W / 2, SLOT_W / 2, -R - 1, -R + T + 1, z0, z1).edges("|Y").fillet(SLOT_W / 2 - 0.05))
    zs = zc - SW_TRAVEL / 2                     # the knob at the "off" end
    yi = -(R - T)
    carrier = box(-6, 6, yi + 0.6, yi + 3.8, zs - 7, zs + 7).cut(box(-1.0, 1.0, yi + 2.2, yi + 3.9, zs - 7.1, zs + 7.1))   # fork over the switch lever
    neck_l = (yi + 0.61) - (-R - 1.8)           # from the carrier through the slot, 1.8 into the knob
    carrier = carrier.union(rx(cyl(NECK_D / 2, 0, neck_l), 90).translate((0, yi + 0.61, zs)))
    shell = cyl(R + GAP + 2.4, zs - 11, 22).cut(cyl(R + GAP, zs - 12, 24))
    knob = plane_xz(0).center(0, zs).rect(10, 20).extrude(R + 4).edges("|Y").fillet(2.0).intersect(shell)   # 20: covers the slot at both ends
    knob = knob.cut(rx(cyl(NECK_D / 2 + 0.1, 0, 2.0), 90).translate((0, -R - 0.1, zs)))   # blind: 0.55 skin on the face

    dif = dsh(0, HB, HD).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH).cut(dsh(WD, HB - 1, HD + 2))
    cap = dsh(0, HB + HD, HC).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    cap = cap.cut(dsh(T, HB + HD - 1, HC - TOP + 1))
    cap = cap.union(dsh(lo, HB + HD - 3, 3.01).cut(dsh(li, HB + HD - 4, 5)))
    return {
        "base": Part(base, base, OFF),
        "diffuser_translucent": Part(dif, dif.translate((0, 0, -HB)), DIF),
        "cap": Part(cap, rx(cap, 180), OFF),
        "slider_carrier": Part(carrier, rx(carrier, -90), DARK),
        "slider_knob": Part(knob, rx(knob, 90), ACC),
    }


SAMPLES["018_wall_sconce_half"] = wall_sconce_half
