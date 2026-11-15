# 070 Herb trough

A long trough for a window sill that holds four herbs in 9 cm nursery pots, 400 × 104 × 96: longer than the bed, so it prints as two
200 halves joined at the centre with four Ø4 steel dowels and glue. Each half is closed at the joint by its own 8 thick end wall, so
each half is a watertight vessel for two pots and the water that drains from them never reaches the glued seam. The two end walls
together are the 16 divider in the middle, and the joint is one V line round the outside and across the divider's top. Two low ribs
along each floor keep the pots out of the water at the bottom.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 400 × 104 × 96, R12, on a 2.4 floating plinth | 100 × 26 × 24 modules; two 200 halves fit a 256 bed; R12 is 12.5 % of the height |
| Compartments | 2 × 189.5 × 99 inside, 93.6 deep; R9.48 at the outer corners, R3 at the divider and the floor | Two 9 cm pots (Ø90 rim) per half with about 9.5 to spare; the outer corners follow the outline, the divider corners take the floor radius |
| Pots | Centred at the quarter points of each compartment; a pot 80 high stands 8.8 under the rim | The pots hide in the trough; the herbs stand above it |
| Ribs | 2 per compartment, 1.68 (DIV) wide, 4.8 high, 48 apart, C0.5 on top | Under the base of a 9 cm pot (about Ø66); about 90 ml of water per half stays under the pots |
| Joint walls | 8 per half, 16 together | Deep enough for the dowel holes with 2 left behind them, so the holes never open into the soil side |
| Dowels | 4 × Ø4 × 10 steel at y ±32, z 24 and 72; holes Ø4.2 teardrop, 6 deep in each half | 5 of each dowel in each half, 1 free for glue; spread over the joint face so the halves cannot twist |
| Seam | C0.5 on the joint face of each half | A V line, the one line that crosses the trough |
| Rubber feet | 8 × Ø10.2 × 1 recesses, at x ±20 and ±180, y ±32 | On the 4 mm grid, inside the plinth |
| Edges | C0.5; C0.6 on the bed face | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| half_left | Bottom down | Off-white |
| half_right | Bottom down (the left half mirrored) | Off-white |
| dowels_steel_ref ×4 | Bought part, not printed | — |
| (8 × Ø10 stick-on rubber feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| half_left / half_right | At 384 long, two Ø90 pots left 0.37 to each wall and 0.7 between them: the pots would not go in side by side | Defect | Length 400 (100 modules, still two halves under the bed); 9.5 to spare per half |
| half_left / half_right | The divider met the floor and the walls in square corners while every other inside corner was round: soil and water would collect there | Defect | Each compartment cut as one cell: R9.48 at the outer corners, R3 at the divider, R3 along the floor |

Dos and Don'ts: one visible chamfer value; one outer radius (R12 and its concentric insides) and R3 for inside corners; the seam is the one
line across the trough; dowels hidden; no fasteners showing; no accent (the herbs are the colour).

Use cases:
- **Assemble:** put glue in the holes and on the joint face of one half, press the four dowels in, put glue on the other face and push
  the halves together on a flat surface; keep them pressed until the glue sets (verify.py: no interference with the dowels).
- **Plant:** stand four 9 cm pots on the ribs, two per half (the pots' envelope clears the trough everywhere).
- **Water:** water the pots; what drains collects under them, about 90 ml per half, under the ribs' tops. Pour out any more.
- **Move:** lift it with a hand under each half; do not lift a full trough by one end, which bends the joint.
- **Place:** stands on 38985 mm² of plinth (396.5 × 100.5).
- **Print:** each half bottom down; the dowel teardrops point up, the walls stand straight. No supports.

verify.py: both halves valid, watertight, one solid each, each fits a 256 bed; no interference.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a planter; they are housings with controls and grilles.
Long window troughs are a common kind of object; no product was used as a model.

Safety (water, food): print in PETG, not PLA (PLA softens and breaks down when wet for months). Printed parts are not certified for food
contact: the herbs grow in their own nursery pots and soil, not in the print. Wipe up water under the trough; keep it away from electrics
on the sill.

Not verified:
- Not printed on a real printer.
- Whether the glued joint stays tight under the weight of four wet pots over months; the dowels take the shear, the glue keeps the
  faces together.
- Whether PETG printed at a common wall count is watertight without a sealant; seal the inside with a food-safe coating if it seeps.
- Pot sizes: 9 cm pots vary; check `POT`, `POT_BASE` and `POT_H`.
