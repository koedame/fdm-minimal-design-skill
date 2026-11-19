# 077 Seed sorting box

A box for sorting loose seeds, 128 × 80 × 32 (84 deep with the knuckles). Twelve cells in four columns and three rows, each 29.5 × 23.9
and 21.6 deep with R3 corners and coved floors, so the last seeds slide to a fingertip. The lid swings up on a pin hinge along the back
seam, the 07_hinged_case arrangement: seven knuckles on a 1.75 filament pin, two 6 × 3 magnets in posts where two dividers meet the front
wall, a lip round the front half of the lid and a finger scoop across the front seam. Unlike the sample, the lid is one flat plate: the
dividers stop 0.25 under it, so with the lid shut every cell is closed and seeds do not wander from cell to cell when the box is carried.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 128 × 80, R12; base 24 + lid 8 = 32 | 32 × 20 modules (8 : 5); base : lid = 3 : 1, as the sample case |
| Cells | 4 × 3, 29.48 × 23.87, R3, floor coves R3 | The inside (122.96 × 74.96) split evenly by 1.68 dividers; the small radius in both places |
| Corner cells | The outer corner takes R9.48, concentric with the R12 outline | An R3 corner there would cut through the wall (found in review, below) |
| Cell depth | 21.6 (floor 2.4) | About 15 ml a cell: a packet's worth of most vegetable and flower seeds |
| Dividers | 1.68 (DIV), tops 0.25 under the lid | Clearance, not contact; seeds larger than 0.25 stay in their cell |
| Walls, floor | 2.52 (T), 2.4 | One wall, one plate |
| Lid | Solid 8 plate; the slicer fills it with sparse infill | A flat underside that covers every divider top |
| Knuckles | 7 × 12 long, R4, 0.4 gaps, pin Ø1.9 for 1.75 filament | As the sample case; 86.4 fits the straight part of the back (104) |
| Magnets | 6 × 3 in Ø6.2 × 3.2 pockets, in 8 × 8 posts on the first and last dividers (x ±31.16), 0.5 into the front wall | The posts stand on a divider, so they take 3.2 from each of the two cells beside them, not a whole corner |
| Magnet gap | 0.3 (0.15 of skin each side of the seam) | The magnets almost touch with the lid shut |
| Lip | 1.68 (DIV) × 3 below the seam, 0.25 inside the walls, front half only, stopping 0.25 short of the posts | Locates the lid; at the back it would block the swing |
| Lip notches | The dividers cut back 2.18 from the walls and 3.25 down, front half only | 0.25 clearance on each side of the lip |
| Finger scoop | Disc R6 (0.75 × lid height) across the front seam, 1.8 deep | Stays below the lid's top edge |
| Edges | C0.5; C0.6 on the bed faces | One visible chamfer value; the seam is a V line |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| base | Bottom down | Off-white |
| lid | Top down | Dark grey |
| magnets_ref × 4 | Bought: 6 × 3 disc magnets | — |
| (1.75 filament, about 88 long, as the pin; 4 × Ø10 stick-on feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| base | The cells were R3 rounded rectangles cut out of a solid block; at the four corners the cell's R3 corner reached 0.16 past the R12 outline and cut a slot through the wall from top to floor (seen in a close rendering; verify.py reported the part valid and watertight, since a slot is still a closed solid) | Defect | Each cell is clipped to the cavity (the outline inset by T, R9.48) before its floor is coved, so the corner cells take the wall's concentric radius. Added a line to the Dos and Don'ts |

Dos and Don'ts: one visible chamfer value; radii by role: R12 outline and its concentric inside R9.48, R3 for the cells, R4 for the
knuckles; equal cells and equal dividers; no fasteners show (the pin ends are flush in the knuckles); the lid is the secondary dark grey, no
accent; the scoop stays inside the front faces of the two parts.

Use cases:
- **Fill:** open the lid and tip a packet into a cell; a label on the lid's underside above each cell or a list in the box says which.
- **Take seeds out:** a fingertip slides seeds up the R3 cove of the floor and out over the divider; seeds are taken by hand, not poured
  (tipping the box would mix the cells).
- **Open:** a fingertip in the scoop lifts the lid off the magnets; it swings back to 150° and the box stays standing (swept: free from 0°
  to −150°, stops at −170° and at +1°).
- **Close and carry:** the lid falls; the lip finds the base and the magnets pull it shut. Every divider stops 0.25 under the flat lid, so a
  seed larger than that cannot cross to the next cell when the box is carried or turned over.
- **Assemble:** glue the magnets in the posts and the lid with opposite poles facing; push the filament pin through the knuckles; melt or
  glue its ends.
- **Print:** base bottom down: the cells open upward, the coves need no support; lid top down with the lip standing up; the knuckles stand
  on 45° webs both ways up. No supports.

verify.py: both printed parts valid, watertight, one solid each; no interference with the magnets; contact area 9563 mm².

Compared with well-known products in this style: radios, a calculator and a loudspeaker; none is a box with cells or a
lid. Divided boxes with a hinged lid are a common kind of object; no product was used as a model.

Safety (magnets, seeds): the magnets are small; keep the box away from small children who could swallow a magnet that comes loose, and
glue the magnets in. Bought seeds are often treated with a fungicide (coloured seeds); keep them, and the box, away from food and from
children and pets, and wash your hands after sorting them.

Not verified:
- Not printed on a real printer.
- Whether seeds smaller than the 0.25 gap (begonia, lobelia) stay in their cells, and how the magnets hold through the 0.3 gap.
- The pin's wear after many openings.
