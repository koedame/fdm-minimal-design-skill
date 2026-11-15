# 051 Wall remote holder

An open cup, 64 × 36 × 96, that hangs on two screws beside a sofa or a bed and holds a TV or air-conditioner remote upright. The
front corners take R8 in plan; the back stands flat against the wall with its two vertical corners cut back 1.2 at 45°, so the cup
sits on a thin shadow line at each side. A U opening, half the width, runs down the front wall to half the height: the remote's top
half shows and a thumb reaches it. The keyholes are cut into the back wall from the wall side and do not show in the cup.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 64 × 36 × 96 | 16 × 9 × 24 modules; height = 1.5 × width; the depth follows from the remote + the keyhole wall |
| Plan radius | R8 at the front corners | 12.5 % of the width; the back corners stay square so the back lies flat on the wall |
| Shadow line | Back corners cut 1.2 × 45° | Same inset as the floating plinth; separates the cup from the wall with one thin shadow |
| Walls | 2.52 (T) at the sides, front and rim | One wall thickness wherever it shows |
| Back wall | 6.4 up to 84, then back to 2.52 on a 45° face | Keyhole ledge 2 + head pocket 3 + 1.4; stepping back below the rim keeps the rim 2.52 all round |
| Floor | 2.4 | Same as the other cups in the set |
| Inner corners | R5.48 (= R8 − T) | Concentric with the outline, so the wall is even round the corners |
| U opening | 32 wide (= W / 2), bottom at 48 (= H / 2), R16 semicircle | Half the width and half the height; as wide as the keyholes are apart |
| Keyholes | Two, x ±16, entry at 68, 6 travel | Head Ø8.4, shank Ø4.2; 32 apart (the U width) so the cup cannot turn on the screws; under the rim so the screw heads are hidden behind the stepped wall |
| Cavity | 58.96 × 27.08 at the remote | A remote up to about 56 wide and 26 thick drops in; the common 52 × 22 one has 4.8 mm to spare front to back |
| Edges | C0.5, C0.6 at the bed | One visible chamfer value; the U's edges take it on both faces of the wall |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| cup | Bottom down | Off-white |
| (2 × 4 mm pan-head or countersunk screws and wall plugs) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| cup | The U opening came out with a flat bottom: the rectangle above the semicircle started at its bottom, not its centre | Defect | The rectangle starts at the circle's centre; the bottom is the R16 semicircle as intended |
| cup | The back wall was 6.4 up to the rim, so the rim read 6.4 at the back and 2.52 on the other three sides | Violation | The back wall steps back to 2.52 on a 45° face 12 below the rim (upward-facing, prints without support); the rim is one width all round |
| cup | The U's vertical edges and semicircle had no chamfer while every other edge had C0.5 | Violation | C0.5 on the U's edges on the outer and inner face of the front wall |

Dos and Don'ts: one visible chamfer (C0.5) plus C0.6 at the bed and the 1.2 shadow line; three radii (R8 outline, R5.48 inner,
R16 U); the U is inside the front face and runs to the rim; no fasteners show; no accent (nothing on the cup has a function to point
at).

Use cases:
- **Hang:** drive two screws 32 apart, level, standing about 3 out of the wall. Put the keyhole entries over the heads and let the cup
  drop 6; the heads seat on the 45° seats inside the back wall. The cup's weight and the remote's press the bottom of the back
  against the wall.
- **Put the remote in:** drops in from above; a 52 × 22 × 180 envelope stands on the floor against the back wall with no overlap,
  lifts out freely (checked at 20 and 100 mm up) and has 4.8 mm to spare toward the front.
- **Take it out:** the top of the remote stands 84 above the rim; the U lets the thumb reach the face of the remote down to half the
  height of the cup.
- **Clean:** the floor is open from above; dust is wiped out with a cloth.
- **Print:** bottom down, no supports. The U is open at the top; the keyholes print with the wall face vertical (the tool's 45° roofs
  point up); the step in the back wall is a 45° face looking up.

verify.py: valid, watertight, one solid, fits a 256 bed, contact area 2166 mm².

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a wall cup; the radio, calculator and speaker are
closed housings with controls or perforation, and this has neither. Open wall pockets for remotes are a common kind of object; no
product was used as a model.

Safety: the holder has no batteries, LEDs, magnets or heat of its own. Fix the screws into wall plugs suited to the wall; the cup is
not made to carry more than a remote.

Not verified:
- Not printed on a real printer.
- The remote size is one common size; measure yours. A remote thicker than about 26 does not fit; make `D` larger by the difference.
- How well the keyhole seats hold on the screws you use (head shape and how far they stand out).
