# 025 Egg cup pair

Two Ø48 × 32 cylinders (3 : 2), each with a spherical seat 14 deep. The seat is a sphere of R18 centred 4 above the top, so it opens to
Ø35: a medium egg (about Ø43) rests on the rim 12 down its side, on a ring, not on the bottom of the seat, and a smaller egg sits deeper
on the same ring. The flat ring of the rim is the one worked-out spot; the bottom steps in 1.2 on a 45° face, so each cup floats on a
shadow line. The pair is one part printed twice. No accent: nothing on an egg cup needs one.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Cup | Ø48 × 32 | Width : height = 3 : 2; grid 4 |
| Seat | sphere R18 centred 4 above the top: Ø35 at the rim, 14 deep | The opening is 8 under a medium egg's width, so the egg rests on the rim ring; the seat clears the egg below it (bottom 1.9 under the egg) |
| Rim ring | 6.5 wide, C0.5 on both edges | (48 − 35) / 2; the egg sits on the inner chamfer |
| Plinth | stepped in 1.2 at 45°, 2.4 high | As 03_tray: the shadow line |
| Pair | 60 apart (12 between the cups) | A quarter of the width between them |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| cup ×2 | Bottom down, as used | Off-white |
| egg_ref | Reference, not printed | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| cup | The first seat (R22, centred 8 above the top, Ø41 rim) was wider than the egg's end, so the egg touched only the bottom of the seat at one point | Defect | R18 centred 4 above: the egg rests on the rim ring 12 up its side |
| cup | The seat sphere had its pole at the bottom of the seat, and the print mesh came out not closed (verify.py) | Defect | Sphere turned so its poles are to the sides |

Use cases:
- **Place, eat:** the egg stands on a ring of Ø35, its centre of gravity over the Ø44.5 plinth; cracking the top pushes the egg down onto
  the ring, not sideways.
- **Hold:** the cup is lifted by its side; every edge is C0.5.
- **Clean:** the seat is a smooth bowl without corners; rinse it by hand.
- **Print:** bottom down; the seat opens upward, nothing overhangs.

verify.py: valid and watertight, the two copies separate, no interference with the egg (it rests 0.1 clear of the rim chamfer), fit a
256 bed; ground contact 3104 mm² over two Ø44.5 plinths.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none is tableware. A cylindrical egg cup is a common form; no product
was used as a model.

Safety (food, heat): printed PETG or PLA is not certified for food contact; the cup only touches the shell. Let a boiled egg cool for a
minute before setting it in (PLA softens at about 55–60 °C, PETG at about 75–80 °C), wash by hand, not in a dishwasher.

Not verified:
- Not printed on a real printer.
- Whether eggs of every size sit steadily on the Ø35 ring (large eggs ride higher, small ones deeper).
