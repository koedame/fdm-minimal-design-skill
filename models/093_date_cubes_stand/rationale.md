# 093 Date cubes and stand

Two cubes that show any day of the month, standing in a low plinth on the desk. One cube carries 0 1 2 3 4 5, the other 0 1 2 6 7 8, and
its 6 turned upside down reads 9 (a seven-segment 6 rotated 180° is a 9), so every date from 01 to 31 can be set; for 03–09 and 13–19 the
cubes swap pockets. Every digit is the same seven stadium segments, 20 high, inlaid 0.4 in dark: the inlay is printed as layers of another
colour, so no face has a recess whose ceiling would be bridged. The plinth floats on a 1.2 shadow line, as 03_tray. Three printed parts
(the inlays are printed with their cubes).

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Pockets | 32 × 32, 4 deep, square corners | 8 modules; half the plinth's height |
| Cubes | 31.5 | The pocket less 0.25 per side |
| Plinth | 76 × 40 × 8, R6 | Two pockets with one margin of 4 round and between them (2 × 32 + 3 × 4, 32 + 2 × 4); R6 = 15 % of the depth |
| Floating plinth | Bottom 2.4 inset 1.2, joined at 45° | As 03_tray |
| Digits | 20 × 12 (5 : 3), segments 2.4 wide, 1.6 short of each corner | A seven-segment digit made of one shape repeated; 20 high is 5/8 of the face, read across a desk |
| Digit placement | Centred on the face; the 1 uses the right-hand segments | Every digit sits in the same cell, as on a segment display, so the pair reads as one number |
| Inlay | 0.4 deep, dark | Inlay depth from the rules; dark because it is the indication, not a label |
| Edges | C0.5 on the cubes and the plinth's top (outline and pocket rims); C0.6 on each bed face | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| stand | Bottom down | Light grey |
| cube_a | A face down (the 5) | Off-white |
| cube_a_digits_inlay | Printed with cube_a, in another colour | Dark |
| cube_b | A face down (the 8) | Off-white |
| cube_b_digits_inlay | Printed with cube_b, in another colour | Dark |

## Review

No defects or violations found. Checked in particular: the 0.4 inlays on the bed face, the sides and the top are filled by the inlay
colour, so nothing is bridged; the cubes sit on the pocket floors with no overlap and stop at 0.4 sideways; the sets of digits give every
day 01–31 (tens 0–3 from either cube, units 3 4 5 from cube_a and 6 7 8 9 from cube_b).

Dos and Don'ts: one visible chamfer value (C0.6 only on the four edges that were on the bed; when a cube is turned, those edges show, 0.1
larger); radii R6 with the plinth's concentric R4.8, and the segments' round ends; margins of 4 round the pockets; one shape repeated for
every digit; dark only for the digits; no accent.

Use cases:
- **Set the date:** lift a cube out (4 of it is in the pocket, nothing to undo), turn the wanted digit to the front, drop it back. For 9,
  roll cube_b's 6 upside down.
- **Swap:** for 03–09 and 13–19, cube_b (with the 0 and the 1) goes to the left pocket; the pockets are the same.
- **Knock:** a cube sits 4 deep with 0.25 round it; a knock moves it 0.25 and it stays in.
- **Print:** each cube with a face down and the digits as a colour change (AMS or a filament swap per layer for the top and bottom; the side
  digits need a multi-colour printer). Without one, print the cubes plain with the 0.4 recesses and fill them with paint; the recess in the
  bed face then has a 0.4 ceiling over segments 2.4 wide. Stand bottom down. No supports.

verify.py: every part valid, watertight; fits a 256 bed; no interference; the cubes lift free and stop at 0.4 sideways in their pockets.

Compared with well-known products in this style: the calculator among them has a display, but it is a flat slab with round
keys, nothing like a pair of cubes. Date cubes with digits on their faces are a common desk object; the seven-segment digits made of
stadium segments are drawn for this model, and no product was used as a model.

Not verified:
- Not printed on a real printer.
- How sharp a 0.4 inlay comes out on the side faces of your multi-colour printer (the colour boundary is one or two lines wide).
