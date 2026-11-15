# 076 Modular desk organiser

Open trays on a 64 grid that cling to each other side by side by magnets in their walls. Two sizes, 64 × 64 and 128 × 64, both 48 high;
any side of one meets any side of another on the grid (shown: two squares beside one long tray, 128 × 128). Each 64 of every side carries
two 6 × 3 magnets standing on edge in slots that open at the top of small posts inside the wall: the slots open upward in the print, and
each magnet faces the neighbour through 0.84 of wall. Seen from outside, the left magnet of each pair has its north pole out and the
right one its south pole, so two sides that meet always pair north with south, whichever way round the trays stand. Each tray stands on
a floating plinth; between two trays the plinths leave one shadow groove.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Grid unit | 64 | 16 modules; trays are 1 × 1 or 2 × 1 units |
| Height | 48 | 3 : 4 of the unit |
| Plan radius | R8 | 12.5 % of the unit; where two trays meet, the corners leave one V notch at each end of the seam |
| Floor edge inside | R3 | The small radius |
| Walls, floor | 2.52 (T), 2.4 | One wall, one plate |
| Plinth | 2.4 high, inset 1.2 at 45° | The floating plinth; between trays it reads as one groove |
| Magnets | 2 per 64 of side, at ±16 from its middle, centre 11.5 above the table | On the grid, inside the straight part of the side (±24) |
| Magnet slots | 3.2 × 6.4 × 6.6 deep, from the top of a post, 0.84 from the outside | A 6 × 3 disc on edge; 2 lines of wall toward the neighbour; open upward in the print |
| Posts | 10 along the wall, 5.04 in from the outside, 14 above the floor | 1.0 of wall behind the slot; the slot is cut after every union |
| Rubber feet | 4 per unit at ±18 | Clear of the plinth's edge |
| Edges | C0.5; C0.6 on the bed face | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| tray_square × 2 | Bottom down | Off-white |
| tray_long | Bottom down | Off-white |
| magnet_ref × 28 | Bought: 6 × 3 disc magnets (8 per square, 12 per long tray) | — |
| (stick-on feet, 4 per unit) | Bought | — |

## Review

No defects or violations found. Checked in particular: every magnet sits inside its slot with no overlap (verify.py, the 28 magnets
included); the slots are cut after the posts and the rim chamfer are joined, so nothing refills them; the posts join the wall (0.5
overlap); every pair of facing sides lines up its magnets (±16 in each 64 on both sides of every seam on the grid).

Dos and Don'ts: one visible chamfer value; two radii (R8 outline and its concentric inside, R3 floor edge); one shape repeated in two
sizes; the seams between trays are the designed groove of the plinths; no fastener shows; off-white, no accent.

Use cases:
- **Arrange:** set trays side by side on the grid; the magnets pull the walls together and line them up. Any side meets any side.
- **Rearrange:** slide a tray sideways or lift it out; the pull of two pairs per 64 is enough to keep a row together when one tray is
  pushed, not to lift the others.
- **Fill:** pens, clips and cards in the open trays; the posts take 10 × 2.5 of each side's foot of wall, below 16.4.
- **Assemble:** glue the magnets into the slots, north out on the left of each pair and south out on the right as seen from outside;
  mark one tray first and check each new one against it before the glue sets.
- **Print:** bottom down: the slots open upward, the posts stand on the floor, the plinth's 45° needs no support.

verify.py: both printed parts valid and watertight, one solid each; no interference (the magnets included); fit a 256 bed; ground contact
13996 mm² for the three trays.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none is an organiser. Square trays on a grid are a common kind of object;
no product was used as a model.

Safety (magnets): 28 small magnets. Keep the trays away from small children who could swallow a magnet that comes loose, and glue every
magnet in. Keep cards with magnetic stripes out of the slots' neighbourhood.

Not verified:
- Not printed on a real printer.
- The magnets' pull through 1.68 of wall and whether two pairs per 64 keep a row together in daily use.
