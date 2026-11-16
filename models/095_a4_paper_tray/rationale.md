# 095 A4 paper tray

A desk tray for a stack of A4 sheets, 236 × 320 × 40: longer than the bed, so it is printed as two halves of 236 × 160 and joined across
the middle on four Ø4 steel dowels and glue, as 11_split_riser. The walls are 8 thick, enough to take the dowels with 1.9 of wall round
each hole, and they read as one solid frame round the thin floor. A U 160 wide drops the front wall to 16, so a sheet is slid out from the
front. The tray floats on a 1.2 shadow line, as 03_tray. Two printed parts and four dowels.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Inside | 220 × 304 | A4 (210 × 297) with 5 at the sides and 3.5 front and back: room for a finger at the sides, and for sheets a little out of square |
| Outline | 236 × 320 × 40 | The inside plus two 8 walls; 59 × 80 × 10 modules; each half 236 × 160 fits a 256 bed |
| Walls | 8 | A Ø4.2 dowel hole with 1.9 of wall on each side; all four walls the same |
| Floor | 2.4 | Carries paper only; line-width multiple |
| Plan radius | R20 outside, R12 inside | 8.5 % of the width; R12 is the largest concentric inner corner an A4 corner clears (by 1.0) |
| Front U | 160 wide (half the depth), down to 16 (0.4 × H), corners R8 (the wall's thickness) | Reaches a stack from the front; stays inside the flat part of the front wall, ends 30 from the corners |
| Joint | Across the middle (y = 0); four dowels Ø4 × 10, two in each side wall at H/4 and 3H/4 | Each half's holes 6 deep (5 + 1 for glue), teardrops; one V line, C0.5 on both halves |
| Floating plinth | Bottom 2.4 inset 1.2, joined at 45° | As 03_tray; Ø10.2 rubber foot recesses at the eight corners of the halves |
| Edges | C0.5 on the rim (outside and in), the U's outline and the joint; C0.6 on the bottom | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| half_front | Bottom down | Off-white |
| half_back | Bottom down | Off-white |
| dowels_steel_ref (× 4) | Bought: steel dowel Ø4 × 10 | Dark |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| half_front | The U was cut with a rounded rectangle that ended 1 above the rim, so its top corners (R8) narrowed the U at the rim into two lumps | Defect | The rounded rectangle runs R8 + 1 above the rim, so only its bottom corners stay in the part |

Dos and Don'ts: one visible chamfer value; radii R20 with its concentric R12 and R18.8 (plinth), and the U's R8 = the wall; one wall
thickness all round; the joint is one intended V line through the middle; plain off-white, no accent; the dowels are hidden in the joint.

Use cases:
- **Fill:** lay a stack of A4 in; it sits 3–5 from the walls, the corners clear the inner R12.
- **Take a sheet:** a finger reaches over the 16 lip in the U (13.6 above the floor) and slides the top sheet out.
- **Lift:** the tray is held at the side walls; the joint across the middle is carried by the walls' dowels and glue (the 2.4 floor is
  glued edge to edge only).
- **Assemble:** glue the dowels into one half, glue both joint faces and press the halves together on a flat table, so the floor lines up.
- **Print:** each half bottom down; the dowel holes are teardrops (apex up). No supports.

verify.py: both halves valid, watertight; fit a 256 bed; no interference with the dowels; a stack of A4 10 high lying in the middle does not
touch the tray (checked in the review, 0 mm³).

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none is a tray. An open desk tray for A4 is a common object; no product
was used as a model.

Not verified:
- Not printed on a real printer.
- Whether two halves glued on a flat table give a floor flat enough that sheets lie without a ridge at the joint.
- The fit of the dowels in the teardrop holes (Ø4.2) on your printer.
