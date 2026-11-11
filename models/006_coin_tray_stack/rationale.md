# 006 Coin tray stack

Round shallow trays for coins and small things that stack. Under each tray a foot drops into the tray below, and the 45° step
between the foot and the outer wall lands on the inner rim chamfer of that tray. The two 45° faces meet, so the stack centres
itself without a separate lip. Alone on a desk a tray stands on its foot and the wall floats on a shadow line.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Tray | Ø80 × 20 | 4:1; three stacked are 54 high |
| Wall | 2.52 | 6 lines |
| Floor | 2.4 over a 2.4 foot (4.8 at the centre) | The foot is solid, so the floor never bridges |
| Foot | Ø74.46, 0.25 inside the wall of the tray below | Drops into the tray below without touching its wall |
| Step from the foot to the wall | 45° cone | Prints without supports; it is also the seat |
| Rim chamfers | 0.5 inside and out | The inner one is the seat for the tray above |
| Stack pitch | 16.85 | Where the cone lies on the chamfer: 20 − 0.5 − (37.48 − 37.23) − 2.4 |
| Floor fillet | R6 | Coins slide up it into the fingers |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| tray (× 3) | Bottom down, as used | Off-white |

## Review

No defects or rule violations found.

Use cases:
- **Use:** coins, keys, rings; the R6 floor fillet lets a coin be slid out with one finger.
- **Stack:** put one tray on another; the cone settles on the rim chamfer and centres it. Overlap check between two trays at the
  stack pitch: 0 mm³; 0.05 lower: 6.2 mm³, so they touch on the seat and nowhere else.
- **Clean:** no undercuts inside; one revolved shape.
- **Print:** bottom down, no supports; the 45° cone is the only overhang.

verify.py: valid and watertight, no interference, fits a 256 bed, ground contact 4221 mm² over 73.4 mm.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a tray; stacking dishes on a conical seat are a
common household form, and no product was used as a model.

Not verified:
- Not printed on a real printer.
- How well the stack centres with real chamfers (the bed-side chamfer and the elephant foot change the foot edge).
