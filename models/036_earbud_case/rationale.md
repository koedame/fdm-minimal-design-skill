# 036 Earbud case

A pocket case for a pair of wireless earbuds without their charging case, 68 × 48 × 28 (17 : 12 : 7), corners R16. The lid lifts
straight off: a lip on it drops 3 into the base all round and locates it, and two pairs of 6 × 3 magnets hold it down. The magnets
stand on the divider, in the middle, so each earbud has a cell clear out to the walls. The dark lid and the off-white base meet at one
V line; a shallow scoop at the front of the seam is the only place to put a fingertip.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Case | 68 × 48 × 28, corners R16 | 17 : 12 : 7; the size the earbuds set (below) |
| Base : lid | 20 : 8 (5 : 2) | The seam low enough that the lid is a lid, high enough that the cells are deep |
| Wall, floor, top | 2.52, 2.4, 2.4; C0.5 on both sides of the seam, C0.6 on the bed edges | 6 lines, 12 layers |
| Inside | 62.96 × 42.96 × 23.2 | Each cell takes an earbud up to 24 × 31 × 22 lying down (checked with `bud()` in design.py) |
| Lip | 1.68 (4 lines) × 3 high, 0.25 clear, all round | Location as 07 |
| Divider | 1.68, to the seam, stepped down 3.25 under the lip | Keeps the two earbuds apart; clears the lip |
| Magnet posts | 8 × 8 on the divider at y = ±12, Ø6.2 × 3.2 pockets meeting at the seam | 6 × 3 magnets (02_rules); two pairs so the lid cannot rock |
| Scoop | R6 (3/4 of the lid height), 1.2 deep, centred on the front seam | Room for a fingertip to lift the lid |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| base | Bottom down, as used | Off-white |
| lid | Top face down | Dark grey |
| (4 × magnet 6 × 3) | Bought, glued into the pockets | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| case | First built 24 high: 19.2 inside, lower than a common earbud lying down (about 22) | Defect | 28 high (base 16 → 20) |
| base, lid | The magnet posts stood on the short ends, where they took 8 of each cell's length exactly where an earbud lies, and broke the lip at both ends | Defect | Posts moved onto the divider; the lip now runs unbroken |
| case | With the posts on the divider, a 24 wide earbud ran 0.95 into the lip at the end wall (`bud()` against the lid: 62.9 mm³) | Defect | 64 → 68 long |
| base | The divider, raised to the seam, ran into the lid's lip at both walls (verify.py: 16.9 mm³ interference) | Defect | Stepped down under the lip |

Use cases:
- **Put the earbuds away:** one in each cell, lying down; the divider keeps them from knocking together.
- **Close:** set the lid on; the lip finds the opening and the magnets pull it down the last few millimetres (swept: lid free upward
  from 0, stops 0.2 down and 0.4 to each side, free at 0.2).
- **Open:** a fingertip in the scoop lifts the lid off the magnets.
- **Carry:** no edge sharper than C0.5, no corner to catch in a pocket.
- **Assemble:** glue the four magnets in their pockets, poles paired so that each pair attracts; check before the glue sets.
- **Print:** base bottom down, lid top face down (the lip upward); no supports.

verify.py: base and lid valid and watertight, no interference, fit a 256 bed; ground contact 2928 mm².

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): radios, a pocket radio, a calculator and a loudspeaker; none is a
case. A small rounded box with a dark lid is a common form for earbud and jewellery cases; no product was used as a model.

Safety (magnets): neodymium magnets are dangerous if swallowed, above all two or more. Glue them in fully and do not use the case if
one comes loose; keep it out of reach of small children. Keep it away from cards with magnetic stripes and from pacemakers.

Not verified:
- Not printed on a real printer.
- How firmly two pairs of 6 × 3 magnets hold the lid through 0.4 of gap (0.2 recess on each side).
- Fit for a particular model of earbud: the cells are checked against a 24 × 31 × 22 envelope, not against real earbuds.
