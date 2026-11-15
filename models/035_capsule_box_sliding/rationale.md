# 035 Capsule box

A small box, 120 × 40 × 20 (6 : 2 : 1), round at both ends, for earplugs, SD cards, pins or spare buttons. The lid is the sliding lid
of 08: a 45° dovetail along the walls, out through the right end, held shut by a low ridge that clicks into a groove under it. Two
dividers split the inside into thirds and reach up to the underside of the lid, so a small thing cannot wander into the next cell with
the lid shut. With the lid closed the top reads as one flat stadium with a single thumb dent; the seam at the right end is the only
sign of how it opens.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Box | 120 × 40 × 20, full round ends (R20) | 6 : 2 : 1; a capsule outline |
| Wall | 2.52, C0.5 on the top edges, C0.6 on the bed edges | 6 lines; one chamfer value per side |
| Floor | 2.4 | 12 layers at 0.2 |
| Lid | 3.6 thick, its lower 1.2 a 45° dovetail; 0.25 clear (0.35 on the slope) | As 08 |
| Lid seat | Ring 1.6 wide inside the walls, 45° underside | Carries the lid without a bridge or support |
| Dividers | 1.68 (4 lines) at x = ±20, from the floor to 0.25 under the lid | Three cells of 36.6 / 38.3 / 36.6 along the axis, on the 4 mm grid |
| Cells | 34.96 wide, 13.75 deep | Two fingers reach the floor |
| Detent | Ridge 0.4 on the right divider, 31 long; groove 0.8 in the lid | As 08; the divider top carries it, so no extra post |
| Thumb dent | 8 × 20, 1.2 deep, 10 from the open end | As 08 |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down, as used | Off-white |
| lid | Bottom down, as used | Off-white |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| — | No defect or rule violation found; the checks below passed as first built | — | — |

Use cases:
- **Open, close:** push the thumb dent toward the right end; the lid clicks over the ridge and slides out (swept: stops at −0.3, the
  ridge drags 0.68 mm³ under it until the lid's end passes the divider, free from 120; 0.3 down, 0.4 up and 0.4 sideways are stopped).
- **Take one thing out:** the lid uncovers from the left end. Slide it out 36 and only the left cell is open; 76 and two are; the
  rest stay covered.
- **Carry:** the lid is held only by the detent; in a bag it can be pushed open by a hard knock (see Not verified).
- **Print:** both parts bottom down, no supports; the dovetail, the ring's underside and the groove's flanks are 45°.

verify.py: body and lid valid and watertight, no interference, fit a 256 bed; ground contact 4293 mm².

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): radios, a pocket radio, a calculator and a loudspeaker; none is a
box. Small boxes with a sliding lid and fixed compartments are common; no product was used as a model.

Safety (food): this is not a pill box. Printed PLA or PETG has layer gaps that hold dirt and cannot be cleaned like a moulded part; do
not keep medicine or food in it unprotected.

Not verified:
- Not printed on a real printer.
- How hard a knock opens the lid in a bag (the detent force depends on the printer's tolerance).
