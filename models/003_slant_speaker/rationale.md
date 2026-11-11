# 003 Slant speaker

A passive speaker for one 2-inch full-range driver. The front leans back at 1:4 and carries a square field of
slots; the rest of the shell is plain. The bottom plate is held by four hidden M2 screws whose heads sit under
the rubber feet.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Width × height | 80 × 128 | 5:8; grid 4 |
| Depth at the bottom / top | 96 / 64 | The front leans back 32 over 128 = 1:4 (14°); 96 gives a stance wider than the width |
| Plan radius | R10 | 12.5% of the width; the same on the front (sloped) and back (vertical) edges |
| Wall, top, bottom plate | 2.52 | 6 lines |
| Grille | 13 slots, 1.6 × 48, pitch 4 | Field 49.6 wide, about square; covers a Ø53 driver |
| Grille margins | 15.2 at the sides, 15.2 above along the slope | (80 − 49.6) / 2, repeated above: margins with the same role |
| Screw bosses | Ø6 at x ±28, y −8 and +40, full height | Vertical from the top wall; clear of the front wall at every height and of the driver |
| Screws | M2: pilot Ø1.8, clearance Ø2.4, head counterbore Ø4.4 inside a Ø10.2 × 1 foot recess | The rubber feet cover the screw heads |
| Cable hole | Ø6 teardrop, 16 above the desk on the back | Horizontal hole, apex up in the print |
| Accent | none | A passive speaker has no control |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Top face down (open bottom up) | Off-white |
| bottom_plate | Outer face down | Off-white |
| driver_ref | Reference only, do not print (Ø53 frame, Ø30 magnet) | Dark grey |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| body | `shell()` on the already chamfered solid returned the solid unchanged, so the body was solid (found as 16 400 mm³ of interference with the plate) | Defect | Shell first, then chamfer |
| bottom_plate | The plate was cut to the bottom outline, but the front wall leans back 0.63 mm over the plate's thickness: 30 mm³ of interference | Defect | The plate's front edge follows the lean (0.63 shorter, shifted back) |

Use cases:
- **Place:** stands on four rubber feet on the bottom plate; ground contact 79 × 95, the leaning front keeps the centre of gravity behind the front feet.
- **Assemble:** glue the driver behind the slot field with a foam gasket ring, run the cable out through the back, then screw the plate on from below and stick the feet over the screws.
- **Print:** body upside down: the front wall leans 14°, the bosses stand on the top wall, the slots run along the slope, the cable hole is a teardrop. No supports.

verify.py: all parts valid and watertight, no interference (the driver reference included), fits a 256 bed, ground contact
6688 mm² over 79.1 × 95.1 mm.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): the L 2 and other speakers of that family are upright boxes with
a perforated front; this has a leaning front, a slot field square to the slope and no visible panel or frame. No product was used
as a model.

Not verified:
- Not printed on a real printer.
- Acoustics: the enclosure volume (about 0.7 L) and the absence of a port were not calculated for any driver.
- The fit of the screws and of your driver (frames differ; check the outline).
