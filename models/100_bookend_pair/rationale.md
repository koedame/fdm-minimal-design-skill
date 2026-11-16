# 100 Bookend pair

Two identical L-shaped bookends, 120 wide, 144 high and 96 deep, for a row of paperbacks and A5 books on a shelf or desk. The books
stand on the bases; their weight keeps each upright from tipping and the base from sliding. The upright is 5.04 thick; the base tapers
from 5.04 at the corner to 1.68 at its front edge, so the books on it lean 2° towards the upright and a book standing across the edge
steps down only 1.68. Two printed parts, the same part twice.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 120 × 144 × 96 | 30 × 36 × 24 modules; 144 holds A5 and paperbacks (about 150–210 high) above their middle; 96 deep takes three or four books on the base |
| Upright | 5.04 (2 × T) | Bends about 1.3 at the top under 5 N from leaning books (PETG, E ≈ 3.5 GPa); stress about 1.6 MPa |
| Base | 5.04 at the corner to 1.68 (DIV) at the front | Thick where the upright's moment goes into it, thin where books step onto it; the 2° slope leans the books into the upright |
| Corner | R12 outside, R6.96 inside, concentric | Even thickness round the bend; R12 = 8.3 % of the height |
| Edges | C0.5 on the upright's top, the base's front and the side away from the bed; C0.6 on the side on the bed | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| bookend (× 2) | On its side, L outline on the bed | Off-white |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| bookend | The first base was 5.04 thick all over: the books between the two bases stand 5 lower than those on them, and a book across a base's front edge tilts about 10° | Defect | The base tapers to 1.68 at the front edge; the step is 1.68 and the books on the base lean 2° into the upright |
| bookend | Rubber-feet pockets under the base would lift it by the feet's height and make the step higher | Defect | No feet: the books' weight on the base holds it; a slippery shelf takes a thin felt sheet under the whole base |

Dos and Don'ts: one thickness for the upright and its concentric corner; one radius pair; one visible chamfer value; plain, the taper
being the one worked-out spot; off-white, no accent.

Use cases:
- **Set up:** stand one bookend against the row's end with its base under the end books, the other at the other end, and push them
  together until the books stand upright; the uprights' 5.04 faces bear on the covers.
- **Few books:** two books between the bookends: both stand on the bases, leaning 2° outwards against the uprights.
- **Many books:** a full row of 240 between the uprights; the books between the bases stand on the shelf 1.68 lower than the end ones.
- **Take a book out:** tilt it out by its top; the row stays up because the end books still lean on the uprights.
- **Print:** each on its side, L outline on the bed, 120 high; lines run round the corner. No supports. 4 walls so the upright is solid
  round its perimeter.

verify.py: bookend valid, watertight, fits a 256 bed on its side; the two copies do not touch; both stand on their bases.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): radios, a pocket radio, a calculator and a loudspeaker; none is a
bookend. An L-shaped bookend is the common form; no product was used as a model.

Not verified:
- Not printed on a real printer.
- How far a printed 5.04 upright creeps over months under a row of heavy books.
- Whether a row of A4 books (about 300 high) stays up against a 144 upright; they are taller than it is meant for.
