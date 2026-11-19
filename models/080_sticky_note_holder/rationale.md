# 080 Sticky note holder

A block 88 square and 22 high with a pocket for a pad of sticky notes, 75 or 76 square. The pocket is half the block's height; the pad
stands on its flat floor and sticks to it by the adhesive on the back of its own last sheet, so the top note can be peeled without lifting
the pad. A half-round notch in the front wall, as deep as the pocket, leaves the last notes of a pad reachable. One printed part, no
mechanism.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 88 × 88, R8; 22 high | 22 modules; height 1 : 4 of the side; R8 about 9 % of the side |
| Pocket | 78 square, R3, 11 deep | A 76 pad + 1 per side (a 75 pad has 1.5); R3 clears the pad's square corners (0.88 in against 1.41 of room); half the height |
| Pocket floor | Flat to the walls, no cove | The pad lies flat to its edges (found in review, below) |
| Walls | 5 | (88 − 78) / 2 |
| Notch | R11 centred on the top edge of the front wall, through that wall only | Its bottom meets the pocket floor: the last sheet can still be reached |
| Rubber feet | 4 × Ø10 at ±32 | Inside the walls, clear of the bed chamfer |
| Edges | C0.5, also on both rims of the notch; C0.6 on the bed face | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| holder | Bottom down | Off-white |
| pad_ref | Bought: a pad of sticky notes, 75 or 76 square (shown 76, 10 high) | — |
| (4 × Ø10 stick-on feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| holder | The pocket floor had an R3 cove; the pad, 1 in from the walls, stood on the cove and overlapped it (145 mm³, verify.py with the pad added) | Defect | Floor edge left square: the pad lies flat to its edges |
| holder | The notch was cut after the chamfers, so its two rims were bare edges | Violation | The notch's rims take the same C0.5, cut by two 45° cones with the notch |

Dos and Don'ts: one visible chamfer value; three radii by role (R8 outline, R3 pocket corners, R11 notch); the notch stays inside the front
wall, its rims chamfered as the rest; off-white, no accent; no fasteners.

Use cases:
- **Place:** the flat bottom stands on 7169 mm² and four rubber feet.
- **Peel a note:** the pad's last sheet holds it to the floor; peel the top note from the front corner. A full pad (10–20 high) stands at or
  above the rim.
- **Reach the last notes:** below the rim, the notch gives a fingertip the front edge of the pad down to the floor.
- **Change the pad:** lift the old last sheet off the floor with a fingernail in the notch; put a new pad in; the 1 of play lets it drop in.
- **Print:** bottom down: the pocket opens upward; the notch's lower half-round faces up. No supports.

verify.py: valid, watertight, one solid; no interference with the pad; contact area 7169 mm².

Compared with well-known products in this style: none is a holder or a tray. Square trays for sticky notes are a common
kind of object; no product was used as a model.

Not verified:
- Not printed on a real printer.
- Whether the pad's last sheet sticks to a printed floor well enough (it may need a smooth floor, or the bed face if printed upside down).
