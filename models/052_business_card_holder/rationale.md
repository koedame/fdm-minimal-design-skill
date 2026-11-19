# 052 Business card holder

A low block, 104 × 32 × 24, on a floating plinth, with one slot that holds a stack of about forty business cards leaning back at
1 : 4. The slot's floor is square to the slope, so the cards sit on their bottom edge instead of on a corner. A semicircular scoop
in the front wall, centred, is the only other feature: a finger and thumb reach the front card there.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 104 × 32 × 24 | 26 × 8 × 6 modules; width = card + 2 × (1.5 clearance + end wall 5) rounded to the grid |
| Plan radius | R8 | 25 % of the depth; the corners stay clear of the slot ends by 3 |
| Plinth | 2.4 high, 1.2 inset, 45° | The floating plinth: a shadow line under the block |
| Slot length | 94 | A 91 mm Japanese card + 1.5 at each end; 85 mm (EU) and 89 mm (US) cards fit too |
| Slot width | 12 at the mouth (11.6 square to the slope) | 3 modules; about 40 cards of 0.28 |
| Slot depth | 16 at the front line | Two thirds of the height; the floor stays 5.2 above the bed at its lowest corner |
| Lean | 1 : 4 (14°) | Enough that the cards stay leaning against the back face and face the viewer; the front wall overhangs by 14°, well inside 45° |
| Front wall | 8 at the top, 4 at the bottom | The slot's front line set 8 back from the face; never thinner than T |
| Scoop | R10, centred | Reaches 10 down, so 2 of the slot's front wall stays below it; wide enough for a fingertip |
| Feet | Four Ø10.2 × 1 recesses at (±40, ±6) | Inside the plinth with 3.7 to its edge |
| Edges | C0.5, C0.6 at the bed | One visible chamfer value, on the rim, the slot mouth and both arcs of the scoop |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| holder | Bottom down | Off-white |
| (4 × Ø10 × 1 rubber feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| holder | The scoop's arcs on both faces of the front wall had no chamfer, while the rim and the slot mouth had C0.5 | Violation | C0.5 on both arcs (selected by a box round the scoop) |

Dos and Don'ts: one visible chamfer; three radii (R8 outline, R6.8 plinth = R8 − inset, R10 scoop); the scoop stays inside the front
face and the rim it opens; no accent (no function to point at); no fasteners.

Use cases:
- **Place:** the plinth stands flat (contact area 2498 mm², 100.5 × 28.5); the cards lean back, and the top of a 55 mm card ends
  12.6 behind the centre line, inside the 16 of the back half, so the centre of gravity stays over the plinth.
- **Fill:** a stack of 40 cards (an 11.2 mm envelope) stands in the slot against the back face with no overlap.
- **Take a card:** the cards come out along the slope (free at 5, 10, 20 and 60 mm along it); straight up they catch the front wall,
  which is what keeps them from falling forward. The scoop gives the fingers the front card.
- **Print:** bottom down, no supports. The slot's front face overhangs 14°; the floor tilts down toward the back; the scoop is open at
  the top.

verify.py: valid, watertight, one solid, fits a 256 bed.

Compared with well-known products in this style: none of them is a desk block with a slot; the shared traits are
only the general language (rounded plan, one chamfer, no ornament). Card holders with a slanted slot are a common kind of object; no
product was used as a model.

Safety: no batteries, LEDs, magnets, heat or food contact.

Not verified:
- Not printed on a real printer.
- Card thickness varies (0.2–0.35); the slot holds fewer thick cards.
- Whether a part-empty slot lets the last few cards slide flat: with 11.6 of space they lean further than 14°.
