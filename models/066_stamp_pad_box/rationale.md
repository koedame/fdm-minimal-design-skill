# 066 Stamp and pad box

A box that keeps a personal seal and its round ink pad together on a desk, 96 × 76 × 28. The base is a solid block with a round pocket
for the pad and a half-round trough for the seal lying down, with the same 4.55 margin round both inside the lip. The pad stands 10 out
of its 6 deep pocket and the seal lies half out of its trough, so both are picked out with the fingers. A lip rises 3 from the base,
0.25 inside the lid's walls, and locates the lid, a 16 high cap that lifts straight off; the seam between them is one V line 12 up.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 96 × 76, R12; base 12 + lid 16 = 28 | 24 × 19 modules; base : lid = 3 : 4; R12 is 12.5 % of the width |
| Pad pocket | Ø58 (pad Ø57 + 0.5 round), 6 deep, C0.5 rim | Holds the pad in place; the pad stands 10 out to be pinched |
| Seal trough | R7.75 (seal Ø15 + 0.25 round), 61 long, centred on the top face, C0.5 edges | The seal lies half out; 60 is the common length of a seal |
| Layout | 4.55 from the lip's inside to the pocket and to the trough, and between them | One margin for the same role; it also sets the depth: 76 = 2 × (4.45 + 4.55) + 58 |
| Lip | 1.68 (DIV) wide, 3 high, its outside 0.25 inside the lid's wall | Location clearance; the lid drops 3 over it |
| Lid | 2.52 (T) walls, 2.4 top; inside top 3.6 over the pad | One wall and one plate thickness |
| Rubber feet | 4 × Ø10.2 × 1 recesses at x ±36, y ±26 | On the 4 mm grid, inside the bed chamfer |
| Edges | C0.5; C0.6 on the bed faces | One visible chamfer value; the seam is a V line |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| base | Bottom down | Off-white |
| lid | Top down | Off-white |
| pad_ref | Bought: round ink pad, 57 × 16 | — |
| seal_ref | Bought: seal, 15 × 60 | — |
| (4 × Ø10 stick-on rubber feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| base / seal_ref | The trough and the seal were built on the wrong side of their workplane: the trough ran outside the box and the seal stood through the lid (`verify.py`: 56 and 152 mm³ of interference) | Defect | Built from `plane_xz()` toward −Y through the box; no interference |
| base | The trough's bottom was set on a 2.4 floor, so the seal stood only 5.65 of its 15 out: too little to pinch | Defect | Trough centred on the top face; the seal lies half out (7.5) |

Dos and Don'ts: one visible chamfer value; one radius in plan (R12 and its concentric insides) plus the pocket's and the trough's circles,
which are the contents' own; one margin round the contents; no fasteners; no accent (the box has no function to point at; the pad's colour
is the pad's).

Use cases:
- **Use the seal:** lift the lid off; pinch the seal from the trough (7.5 shows), stamp on the pad and on the paper, lay it back.
- **Change the pad:** the pad stands 10 out of its pocket; lift it by its sides.
- **Close:** set the lid on; it drops 3 over the lip and stays square (swept: free upward from 0 to 20; stops at 0.3 downward and at 0.4
  sideways, free at 0.2). Pad, seal and lid stay clear of each other (no interference with the bought parts).
- **Place:** stands on 6661 mm² (94.9 × 74.9).
- **Print:** base bottom down: the pocket and the trough open upward (the trough is a half circle, steepest at the rim, no overhang); the lip
  stands on the top face. Lid top down. No supports.

verify.py: both printed parts valid, watertight, one solid each; no interference with the pad or the seal; motions as above.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a box for small things; they are housings with
controls and grilles. Boxes for a seal and an ink pad are a common kind of object; no product was used as a model.

Safety: the box has no batteries, LEDs, magnets or heat of its own. Ink pads contain oil-based ink; the box is not meant for food.

Not verified:
- Not printed on a real printer.
- The pad and seal sizes are common ones; measure yours and change `PAD_D`, `PAD_H`, `SEAL_D` and `SEAL_L` (the margins follow).
- How the 0.25 clearance of the lip fits on your printer.
