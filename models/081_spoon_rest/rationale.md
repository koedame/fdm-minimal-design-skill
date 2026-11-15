# 081 Spoon rest

A tray 144 × 72 × 16 on a floating plinth, for a cooking spoon or a ladle put down between stirs. The bowl of the spoon lies in a well
12 deep that keeps the drips; the handle crosses the right-hand end wall in a half-round notch and rests there 4 above the floor, so it
stays off the worktop and the spoon cannot roll out sideways. One printed part, no mechanism.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 144 × 72, R12; 16 high | 2 : 1 on the 4 mm grid; R12 = 8.3 % of the length; a ladle's bowl (about 70 across) lies in the well |
| Wall | 5.04 (2 × T, 12 lines) all round | One margin for one role; a line-width multiple |
| Well | 133.92 × 61.92, R6.96, 12 deep | The outline less the wall; its corners concentric with the outline (R12 − 5.04) |
| Floor | 4 above the table (plinth 2.4 + 1.6) | Weight low down, so a handle resting on the end does not tip the tray |
| Handle notch | R8 on the top edge of the end wall, through that wall only | Up to a 16 wide handle sits in it; its bottom (z 8) is 4 above the floor, so the handle slopes gently down to the bowl |
| Floating plinth | 2.4 high, inset 1.2 at 45° | The shadow line that lifts the tray off the worktop |
| Rubber feet | 4 × Ø10.2 at (±56, ±20) | Stop the tray sliding when the spoon is put down |
| Edges | C0.5 on both rims and on both edges of the notch; C0.6 on the bed face | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| rest | Bottom down | Off-white |
| (4 × Ø10 stick-on rubber feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| rest | The wall was 6 thick: on the grid, but not a multiple of the line width, so the slicer would fill a sliver of infill along every wall | Violation | Wall 5.04 (2 × T); the well follows from the outline, its radius stays concentric |

Dos and Don'ts: one visible chamfer value (C0.6 only on the bed face); three radii, one per role (R12 outline, its concentric R6.96 in the
well, R8 for the notch the handle rests in); one margin all round; plain, with the notch as the one worked-out spot; off-white, no accent.

Use cases:
- **Put the spoon down:** bowl in the well, handle in the notch. The spoon is held at two points, the bowl on the floor and the handle on
  the notch, so its balance point must lie between them: true for spoons and ladles, whose wet bowl is the heavy end. A spoon whose
  balance point lies in the handle beyond the notch tips back; lay it lengthwise in the well instead (133 long inside).
- **Drips:** stay in the well; it holds about 33 ml before liquid reaches the bottom of the notch (4 above the floor) and runs out over
  the end, far more than a spoon drips.
- **Place:** stands on four rubber feet; ground contact 9197 mm² over 140.5 × 68.5. The tray weighs about 80 g in PETG with solid
  infill; the floor is low, so a handle pressing on the notch end does not lift the far end.
- **Clean:** wipe or rinse by hand; the well's corners are R6.96 vertically, its floor is flat.
- **Print:** bottom down; the notch is open at the top and the plinth has a 45° step. No supports.

verify.py: valid, watertight, one solid; fits a 256 bed; ground contact 9197 mm² over 140.5 × 68.5.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): radios, a pocket radio, a calculator and a loudspeaker; none is a
kitchen tray or a spoon rest. A shallow tray with a notch for the handle is the common form of a spoon rest; no product was used as a
model.

Safety (food, heat): the spoon goes back into the food after it has lain in the tray. Printed parts are not certified for food contact
and their layer lines hold residue that washing does not fully remove; use a filament sold as food-contact compliant if that matters to
you, wash the tray after cooking and do not put it in a dishwasher. PETG softens at about 75–80 °C: a wooden, silicone or nylon spoon
is fine, but a metal spoon straight out of a boiling pot can mark it; for that, print in ASA or PC. Keep the tray off the hob and away
from the flame.

Not verified:
- Not printed on a real printer.
- How warm a metal spoon from boiling liquid makes the floor of a PETG print.
- How cooking oil and coloured sauces (tomato, turmeric) stain the chosen filament.
