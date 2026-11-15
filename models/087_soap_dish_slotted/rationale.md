# 087 Slotted soap dish

A tray 112 × 80 × 24 on a floating plinth for a bar of soap by a basin or a kitchen sink. The bar rests on eight round-topped ribs,
level 12 above the table, so its underside touches the dish only along eight thin lines. Beneath it the floor falls 2 from the back to
the front; the ribs stop 4 short of the front wall, leaving a gutter, and seven vertical slots through the front wall let the water out.
Placed with the slotted side toward the basin, the dish dries between uses. One printed part, no mechanism.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 112 × 80, R12; 24 high | 28 × 20 modules on the 4 mm grid; R12 = 10.7 % of the length; a hotel-size to a large bar (up to about 100 × 70) lies inside |
| Wall | T (2.52) all round, inner corners R9.48 | One margin; concentric with the outline (R12 − T); a line-width multiple |
| Floor | 4 above the table at the front, 6 at the back | 2 of fall over 75 (1.5°) carries the water to the front; the layer steps all drop toward the front, so none holds a pool |
| Ribs | 8 × DIV (1.68) wide at pitch 12, round tops (R0.84) at z 12, from the back wall to 4 short of the front wall | Line contact keeps the bar's underside dry and stops it from sticking; level tops so the bar does not slide off the front; DIV is the inner-divider thickness |
| Gutter | 4 wide along the front wall | Collects the water from every channel between the ribs and leads it to the slots |
| Drain slots | 7 × 3.2 wide, at x = 0, ±12, ±24, ±36 (one at the end of every channel), round bottom 1.6 below the front floor, 45° roof at z 14.3 | Wider than the 1.6 decorative slot in the rules: water bridges a 1.6 slot and stands behind it. The bottom reaches into a 1 deep sump in the floor, so the floor drains to its last drop |
| Floating plinth | 2.4 high, inset 1.2 at 45° | The shadow line that lifts the dish off the worktop; the water from the slots drips into the recess, clear of the floor |
| Edges | C0.5 on both rims and as a flare on the slot outlines on both faces of the wall; C0.6 on the bed face | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| dish | Bottom down | Off-white, matte PETG |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| dish | The slots' outlines on the front face were sharp: the only unchamfered visible edges | Violation | A 45° flare (the outline lofted to its offset by CH) cut at the outer and the inner face of the wall |
| dish | The slots had round tops of Ø3.2: a horizontal hole over Ø2 needs a teardrop roof, or its top sags | Violation | The top end of each slot is a 45° roof (apex 14.26), the bottom stays round |

Dos and Don'ts: one visible chamfer value (C0.6 only on the bed face); three radii, one per role (R12 outline with its concentric R9.48
inside and the R10.8 plinth; R1.6 slot ends; R0.84 rib tops); one margin all round; plain, with the drainage as the one worked-out spot
(the slots line up with the channels and reach below the floor); off-white, no accent.

Use cases:
- **Put the soap down:** the bar lies on the ribs, any way round; with the inside 107 × 75 and the ribs 8 above the front floor, a wet bar
  of up to about 100 × 70 sits clear of the water.
- **Drain:** water off the bar runs down the ribs onto the floor, along the channels to the gutter and out through the slot at the end of
  each channel. The slot bottoms lie 1.6 below the front floor, so no film stands in the dish. Place the dish with the slots over the
  basin's edge or toward the sink; the water drips into the plinth recess and runs off there.
- **Dry:** the bar touches eight lines only, and air reaches its underside along the channels and through the slots.
- **Clean:** rinse under the tap; the channels are open at the front, so soap residue washes out through the gutter. The ribs are 12
  apart, wide enough for a brush.
- **Place:** ground contact 8201 mm² over 108.5 × 76.5; the dish weighs about 60 g in PETG. On a wet, smooth worktop it can slide when
  knocked; four Ø10 rubber feet would stop that but would also lift it out of the water it sheds (not added).
- **Print:** bottom down; the ribs stand up, the slots are vertical with 45° roofs, the plinth has a 45° step. No supports.

verify.py: valid, watertight, one solid; fits a 256 bed; ground contact 8201 mm² over 108.5 × 76.5.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): radios, a pocket radio, a calculator and a loudspeaker. The vertical
slots echo the loudspeaker grilles of that family in idea only; none of them is a dish or a tray, and the slots here are drains sized for
water. A tray with ribs and a drain is the common form of a soap dish; no product was used as a model.

Not verified:
- Not printed on a real printer.
- Whether 3.2 slots drain fully with soap scum in them, or need a wider slot after weeks of use.
- How the chosen filament stands up to soap and limescale cleaners.
