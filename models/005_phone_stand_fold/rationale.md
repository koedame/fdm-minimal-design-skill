# 005 Folding phone stand

A base and a leg joined by a pin hinge. Open, the leg leans forward at 50° and stops against a heel at the back of the base;
a phone stands behind the front ridge and leans on the round end of the leg. Folded, the leg lies on the base.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Base | 72 × 96 × 8 | 3:4 plan; 72 is about the width of a phone |
| Plate thickness P | 8 | Base, leg, ridge and knuckles share it; folded the leg is 16 high like the ridge |
| Knuckles | Ø8 (the full round end of the leg), 5 × 12 with 0.4 gaps | As 07_hinged_case; the knuckle is the plate's own round end |
| Pin | Ø1.9 hole for 1.75 mm filament | No bought hardware |
| Hinge axis | 24 behind the centre, on the base top (z 12) | Leaves 72 in front of the axis for the phone |
| Leg | 56 from the axis to the centre of its far end | The far end sits at about 55 high, 12 in front of the centre |
| Open angle | 50° from the base | A phone resting on the ridge and the leg end leans back about 18° |
| Front ridge | 8 × 8, full round top | Holds the phone's lower edge; the round top is the only edge the hand meets |
| Heel | everything behind the open leg's back face, up to 24 (3 × P), 0.1 clear of the leg | The leg bears on it over 12 mm of its length |
| Webs under the base knuckles | 45° | The knuckles grow from the plate without an overhang in either print direction |
| Chamfers | 0.6 on the bed side, 0.5 on the top side | As every part |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| base | On its side (the left side face down); the pin hole is vertical | Off-white |
| leg | On its side (the left side face down); the pin hole is vertical | Off-white |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| heel | 16 high, the heel met the leg only within 1.8 of the axis: a phone pushing on the leg end (lever 56) loaded the pin and knuckles about 30 times over | Defect | Heel 24 high; the leg bears on it over 12 mm |
| heel | Its face was exactly on the open leg's back face (0.010 mm³ of overlap in the check) | Defect | 0.1 clear; the leg comes to rest on it after 0.5° |

Use cases:
- **Open:** lift the leg's far end; it turns on the pin and stops on the heel at 50°.
- **Use:** stand the phone on the base behind the ridge, leaning back on the leg end; portrait or landscape.
- **Fold:** push the leg down until it lies on the base (16 high, with the heel standing 24 at the back).
- **Assemble:** push a 72 mm length of 1.75 mm filament through the knuckles; trim it flush.
- **Print:** both parts on their sides with the pin hole vertical, so the round ends, the ridge and the 45° webs are in the layer plane.

verify.py: both parts valid and watertight, no interference, fit a 256 bed; ground contact 6811 mm² over 71 × 96 mm.
Hinge sweep about the pin axis: no overlap from the open pose to folded (0, 10, 20, 30, 40, 50°); 2° past open the leg
enters the heel by 108 mm³, which is the stop working.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a phone stand; the plate-on-plate fold with a
round-ended leg and a heel stop is not taken from any product. No product was used as a model.

Not verified:
- Not printed on a real printer.
- The leg prints 72 high on an 8 wide side; it may need a brim.
- How tightly the filament pin holds the leg at angles between folded and open (there is no detent).
