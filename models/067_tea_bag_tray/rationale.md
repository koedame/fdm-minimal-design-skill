# 067 Tea bag tray

A small dish beside the cup for a used tea bag, 96 × 64 × 12. Seven low ribs cross the floor with equal gaps: the bag lies on their tops
and the tea it drips runs down between them, so the bag does not sit in its own puddle and the tag stays clean. A notch in the rim of one
short wall takes the string, so the tag hangs outside. One part on a floating plinth; nothing else.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 96 × 64 × 12, R12 | 24 × 16 × 3 modules (3 : 2 in plan); takes a flat bag (about 50 × 60) or a pyramid bag with room round it; R12 is 12.5 % of the width |
| Walls / floor | 2.52 (T) / 2.4; inside R9.48 and R3 at the floor | One wall thickness; the inside follows the outside |
| Ribs | 7 × 1.68 (DIV) wide, 3.2 over the floor, C0.5 on the top edges; 9.9 gaps, the walls included | Equal gaps across the whole floor, so the bag lies anywhere; the gaps hold about 15 ml under the rib tops, several bags' drips |
| Rib tops | 6.4 under the rim | The bag sits inside the rim and does not slide off |
| String notch | R3 (6 wide, 3 deep) in one short wall, C0.5 edges | Holds the string so the tag hangs outside; the radius is the one-thumb small radius, not a feature to look at |
| Plinth | 2.4 high, 1.2 in, C0.6 on the bed | The tray floats on a shadow line |
| Rubber feet | 4 × Ø10.2 × 1 recesses at x ±36, y ±20 | On the 4 mm grid; keep a wet tray from sliding |
| Edges | C0.5; C0.6 on the bed face | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| tray | Bottom down | Off-white |
| (4 × Ø10 stick-on rubber feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| tray | Five ribs at pitch 12 covered only the middle 50 of the 91 floor: a bag laid off-centre sat on the flat floor in its drips, and the ends looked empty | Defect | Seven ribs with equal 9.9 gaps across the whole floor, the walls included |

Dos and Don'ts: one visible chamfer value; one radius in plan (R12 and its concentric inside) plus R3 for the floor edge and the notch;
equal gaps; no accent colour (the tea is the colour); no text or logo; nothing a bag can catch on.

Use cases:
- **Put the bag down:** lay the squeezed bag on the ribs with the string in the notch; the tag hangs outside the wall. The bag
  (envelope 60 × 50 × 8) fits on the ribs inside the rim with no overlap.
- **Drips:** run into the eight gaps between the ribs, 3.2 deep, about 15 ml in all.
- **Clean:** rinse by hand; the gaps are open from end to end with R3 at the floor, so a brush reaches everything.
- **Place:** stands on 5172 mm² (92.5 × 60.5) of plinth.
- **Print:** bottom down; the ribs and the walls stand straight up from the floor, the notch is a half circle open at the top. No supports.

verify.py: valid, watertight, one solid; fits the bed.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a dish; they are housings with controls and grilles.
Ribbed dishes for tea bags and soap are a common kind of object; no product was used as a model.

Safety (food, heat): print in PETG, not PLA; a tea bag straight from the pot can be near 90 °C and PLA softens at about 55–60 °C. Printed
parts are not certified for food contact and layer lines hold residue: use the tray only for used bags, not for food, rinse it after use,
let it dry, and do not put it in a dishwasher.

Not verified:
- Not printed on a real printer.
- Whether PETG keeps its shape under hot bags in daily use (its glass transition is about 80 °C).
- Whether the R3 notch holds every kind of string; a thicker string may need a larger `NOTCH_R`.
