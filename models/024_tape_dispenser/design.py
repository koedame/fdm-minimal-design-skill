"""024 Tape dispenser: a 120 x 40 x 48 block that holds a roll of 18 mm tape on a 1-inch core and a weight.

The roll turns on a printed hub whose stubs drop into two U-slots in the cheeks, so the hub is located
and lifts straight out to change the roll. The trough under the roll is round, concentric with the hub.
In front of and behind the trough the block is hollow: two cavities with 45-deg roofs (they print bottom
down without support) take a weight, and a bottom plate closes them, located by lips that fit inside
the cavities. A row of teeth across the front edge cuts the tape.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, DARK,  # noqa: E402
                         box, cyl, rrect, feet, plane_yz, plane_xz)

W, L, H, R = 40.0, 120.0, 48.0, 5.0   # 1 : 3 in plan (x : y); R = 12.5 % of 40
ZA = H - 8.0                          # hub axis 8 under the top
TAPE_W, CORE_ID, ROLL_OD = 18.0, 25.4, 56.0   # 18 mm tape on a 1-inch core, up to Ø56
SLOT_W = TAPE_W + 2.0                 # trough 20: 1 each side of the tape
R_TROUGH = ROLL_OD / 2 + 2.0          # 30: 2 under the largest roll
STUB_D, STUB_L = 6.0, 3.0
PLATE, LIP = 2.4, 4.0
TOOTH, TOOTH_H = 1.68, 1.2            # tooth pitch = DIV, 45-deg flanks would be 0.84 high; 1.2 makes them sharper


def trough_cut():
    c = plane_yz(-SLOT_W / 2).center(0, ZA).circle(R_TROUGH).extrude(SLOT_W)
    return c.union(box(-SLOT_W / 2, SLOT_W / 2, -R_TROUGH, R_TROUGH, ZA, H + 1))


def cavity(y0, y1):
    """Open at the bottom, up to a 45-deg gable roof 2.4 under the top."""
    hw = W / 2 - T
    z_eave = H - 2.4 - hw
    prof = [(-hw, -1), (hw, -1), (hw, z_eave), (0, z_eave + hw), (-hw, z_eave)]
    return plane_xz(y1).polyline(prof).close().extrude(y1 - y0)


def tape_dispenser():
    body = rrect(W, L, R, 0, H).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    body = body.cut(trough_cut())
    yc = R_TROUGH + T                         # cavities start a wall away from the trough
    cav = [(-L / 2 + T, -yc), (yc, L / 2 - T)]
    for y0, y1 in cav:
        body = body.cut(cavity(y0, y1))
    body = body.cut(rrect(W - 2 * T, L - 2 * T, R - T, -1, PLATE + 1))          # recess for the bottom plate
    for sx in (-1, 1):                        # U-slots for the hub stubs, 0.5 deeper than the stubs
        x0 = sx * SLOT_W / 2
        slot = plane_yz(min(x0, x0 + sx * (STUB_L + 0.5))).center(0, ZA).circle(STUB_D / 2 + GAP).extrude(STUB_L + 0.5)
        slot = slot.union(box(min(x0, x0 + sx * (STUB_L + 0.5)), max(x0, x0 + sx * (STUB_L + 0.5)),
                              -STUB_D / 2 - GAP, STUB_D / 2 + GAP, ZA, H + 1))
        body = body.cut(slot)
    rim = cq.selectors.BoxSelector((-SLOT_W / 2 - STUB_L - 1, -R_TROUGH - 1, H - 0.01), (SLOT_W / 2 + STUB_L + 1, R_TROUGH + 1, H + 0.01))
    body = body.edges(rim).chamfer(CH)        # the rim of the trough and the slots, as the outer rim
    teeth = None
    n = int(SLOT_W // TOOTH) + 1
    y_t = -L / 2 + CH + 0.2
    for i in range(n):
        x = (i - (n - 1) / 2) * TOOTH
        t = plane_xz(y_t).polyline([(x - TOOTH / 2, H - 0.01), (x + TOOTH / 2, H - 0.01), (x, H + TOOTH_H)]).close().extrude(-TOOTH)
        teeth = t if teeth is None else teeth.union(t)
    body = body.union(teeth)

    pw, pd, pr = W - 2 * (T + GAP), L - 2 * (T + GAP), R - T - GAP
    plate = rrect(pw, pd, pr, 0, PLATE).faces("<Z").chamfer(CH_BED)
    hw = W / 2 - T
    for y0, y1 in cav:
        ring = box(-hw + GAP, hw - GAP, y0 + GAP, y1 - GAP, PLATE - 0.01, PLATE + LIP)
        plate = plate.union(ring.cut(box(-hw + GAP + DIV, hw - GAP - DIV, y0 + GAP + DIV, y1 - GAP - DIV, 0, PLATE + LIP + 1)))
    plate = feet(plate, [(sx * 10, sy * 48) for sx in (-1, 1) for sy in (-1, 1)])

    hl = SLOT_W - 2 * GAP
    hub = cyl(CORE_ID / 2 - 0.2, 0, hl).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH)
    hub = hub.union(cyl(STUB_D / 2, -STUB_L, STUB_L + 0.01)).union(cyl(STUB_D / 2, hl - 0.01, STUB_L + 0.01))
    hub = hub.faces("<Z").chamfer(CH).faces(">Z").chamfer(CH)
    hub_asm = hub.translate((0, 0, -hl / 2)).rotate((0, 0, 0), (0, 1, 0), 90).translate((0, 0, ZA))
    roll = cyl(ROLL_OD / 2, -TAPE_W / 2, TAPE_W).cut(cyl(CORE_ID / 2, -TAPE_W, 2 * TAPE_W))
    roll = roll.rotate((0, 0, 0), (0, 1, 0), 90).translate((0, 0, ZA))
    return {
        "body": Part(body, body, OFF),
        "bottom_plate": Part(plate, plate, OFF),
        "hub": Part(hub_asm, hub.translate((0, 0, STUB_L)), DARK),
        "tape_roll_ref": Part(roll, None, (0.85, 0.83, 0.70), ref=True),
    }


SAMPLES["024_tape_dispenser"] = tape_dispenser
