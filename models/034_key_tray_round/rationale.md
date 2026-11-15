# 034 Round key tray

A round dish, Ø120 × 24 (5 : 1), for keys by the door. It floats on a plinth set 1.2 inward and joined at 45°, the shadow line of 03
tray drawn round. Inside, the floor runs up into the wall on a cove of R12, half the height, so a key pushed against the wall slides up
into the fingers. A dark grey TPU liner lies flush in a recess in the flat of the floor: keys land on something soft and quiet, and with
C0.5 on both edges of its seam the liner's outline is one V line. No accent: nothing on a tray has a function to mark.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Dish | Ø120 × 24 | 5 : 1 |
| Wall | 2.52, C0.5 on both rim edges | 6 lines; one chamfer value |
| Plinth | 2.4 high, 1.2 inward, 45° step | The floating plinth of 03 tray |
| Cove | R12 | Half the height: keys slide up it; the flat of the floor is Ø90.96 |
| Floor | 3.6 = 2.4 under the liner + the liner's 1.2 | The liner sits flush |
| Liner recess | Ø88 (11 modules), 1.2 deep, C0.5 rim | 1.48 inside the start of the cove, so the cove stays whole |
| Liner | Ø87.5 (0.25 clear), 1.2 thick, C0.5 on its top edge | With the recess's C0.5 the seam is one V line |
| Feet | Ø10.2 × 1 recesses at (±28, ±28) | The rubber foot rule, on the 4 mm grid |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| tray | Bottom down, as used | Off-white |
| liner_tpu | Bottom down | Dark grey (TPU) |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| liner_tpu | Printed top face down (visible face on the bed), its C0.5 edge would be the bed-side edge, which wants C0.6, and the V line would be uneven | Violation (02_rules: C0.6 only on the bed side) | Printed bottom down; a soft liner's top surface does not need the bed finish |

Use cases:
- **Place:** the plinth stands flat (10324 mm²) with four rubber feet; nothing sticks out of the round.
- **Drop keys in, take them out:** they land on the liner; push them to the wall and they ride up the cove.
- **Clean:** lift the liner out by its edge (0.25 clear in the recess) and wash it.
- **Print:** tray bottom down (the plinth's 45° step and the cove need no supports); liner flat.

verify.py: tray and liner valid and watertight, no interference, fit a 256 bed; ground contact 10324 mm².

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): radios, a pocket radio, a calculator and a loudspeaker; none is a tray.
Round dishes on a plinth are a common form; no product was used as a model.

Not verified:
- Not printed on a real printer.
- Whether the liner stays in the recess without glue when keys are swept out (it is held only by its fit).
