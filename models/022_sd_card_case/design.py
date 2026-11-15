"""022 SD card case: a 44 x 44 x 36 case for eight SD cards standing in slots, the lid held by two snap tabs.

The body is low (12) and its wall steps in at the top into a neck that the lid (24) slides over. Two
cantilever tabs are freed from the front and back of the neck by U-shaped slits; a 45-deg bump on each
drops into a 45-deg groove inside the lid wall, so the lid clicks shut and pulls off without a button.
The tabs and grooves are hidden inside the closed case. The cards stand in a slotted block, their tops
11.6 above the neck, so they can be picked out by the edge.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF, box, rrect, rx, plane_yz  # noqa: E402

S, R = 44.0, 6.0                  # plan 44 (grid 4), R = 13.6 % of 44
HB, HL = 12.0, 24.0               # body : lid = 1 : 2, total 36
FLOOR = TOP = 2.4
NECK = 9.0                        # neck height: room for a tab long enough to flex 0.4 within 2 % strain
NO = S - 2 * (T + GAP)            # neck outside: the lid's inside less the clearance
NI = NO - 2 * DIV                 # neck inside
STEP = (S - 2 * T - NI) / 2
# SD card 32 x 24 x 2.1 standing on its long edge; slot = card + 0.25 per side, rib = DIV
CARD = (32.0, 24.0, 2.1)
N, SLOT = 8, CARD[2] + 2 * GAP
PITCH = SLOT + DIV                # 4.28
Z_CARD = HB + HL - TOP - 1.0 - CARD[1]   # 8.6: card top 1.0 under the lid top
Z_BLOCK = Z_CARD + 8.0            # cards held 8 deep
TAB_W, SLIT, BUMP = 12.0, 1.0, 0.4
Z_BUMP = HB + NECK - 1.5          # bump centre 1.5 under the top of the tab


def wire(w, r, z):
    return rrect(w, w, r, z, 1.0).faces("<Z").wires().val()


def prism_x(y, z, pts, length):
    """45-deg prism along X: pts in local (y, z) around (y, z)."""
    return plane_yz(-length / 2).polyline([(y + a, z + b) for a, b in pts]).close().extrude(length)


def sd_card_case():
    body = rrect(S, S, R, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").edges().chamfer(CH)
    body = body.union(rrect(NO, NO, R - T - GAP, HB - 0.01, NECK + 0.01).faces(">Z").chamfer(CH))
    ri, rni = R - T, R - T - GAP - DIV
    z_cone = HB - STEP
    cone = cq.Solid.makeLoft([wire(S - 2 * T, ri, z_cone - 0.001), wire(NI, rni, HB + 0.001)], True)   # 45 deg
    body = body.cut(rrect(S - 2 * T, S - 2 * T, ri, FLOOR, z_cone - FLOOR + 0.01))
    body = body.cut(cq.Workplane("XY").add(cone)).cut(rrect(NI, NI, rni, HB, NECK + 1))

    by = (N * SLOT + (N - 1) * DIV) / 2 + 0.8          # block: the slots and a 0.8 margin, clear of the tabs
    block = box(-NI / 2 - 0.01, NI / 2 + 0.01, -by, by, FLOOR - 0.01, Z_BLOCK)
    for i in range(N):
        y = (i - (N - 1) / 2) * PITCH
        block = block.cut(box(-CARD[0] / 2 - GAP, CARD[0] / 2 + GAP, y - SLOT / 2, y + SLOT / 2, Z_CARD, Z_BLOCK + 1))
        h = SLOT / 2                                   # lead-in: C0.5 on both long edges of the slot
        block = block.cut(prism_x(y, Z_BLOCK, [(-h, -CH), (h, -CH), (h + CH + 0.01, 0.01), (-h - CH - 0.01, 0.01)],
                                  CARD[0] + 2 * GAP))
    body = body.union(block)

    yt = NO / 2 - DIV / 2                              # mid-plane of the neck wall
    for s in (-1, 1):
        for x in (-TAB_W / 2 - SLIT, TAB_W / 2):      # U-shaped slit: two sides, the top is open
            body = body.cut(box(x, x + SLIT, s * yt - DIV / 2 - 0.1, s * yt + DIV / 2 + 0.1, HB + 0.5, HB + NECK + 1))
        bump = prism_x(0, Z_BUMP, [(0, -BUMP), (BUMP, 0), (0, BUMP)], TAB_W)
        body = body.union((bump if s > 0 else bump.mirror("XZ")).translate((0, s * (NO / 2 - 0.01), 0)))

    lid = rrect(S, S, R, HB, HL).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    lid = lid.cut(rrect(S - 2 * T, S - 2 * T, R - T, HB - 1, HL - TOP + 1))
    g = 2 * BUMP
    for s in (-1, 1):
        groove = prism_x(0, Z_BUMP, [(0, -g), (g, 0), (0, g)], TAB_W + 2)
        lid = lid.cut((groove if s > 0 else groove.mirror("XZ")).translate((0, s * (S / 2 - T - 0.01), 0)))
    return {
        "body": Part(body, body, OFF),
        "lid": Part(lid, rx(lid, 180), OFF),
    }


SAMPLES["022_sd_card_case"] = sd_card_case
