# 055 Cable comb raceway

A short raceway, 128 × 40 × 16, for a wall or the underside of a desk, that keeps four cables side by side and in order. The base is a
U channel open at both ends; two comb plates near the ends have four round-bottomed notches each, one cable per notch, so the cables
leave the raceway in the order they came in. Two countersunk screws through the floor, between the combs, hold it (double-sided tape
works too), and the lid hides them. The lid is a plate with the base's outline; four vertical hooks hang from it inside the walls and
their 45° barbs drop into V grooves in the walls. The seam is a V line with C0.5 on both sides, the only line on the long faces.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 128 × 40 × 16 | 32 × 10 × 4 modules; width = four cables at a pitch of 8 + the walls and hooks |
| Plan | Square ends | The ends are open; a plan radius ran the side walls out to a knife edge there (see the review) |
| Walls | 2.52 (T); floor and lid 2.4 | One wall thickness, one plate thickness |
| Seam | 13.6 from the mounting face (lid 2.4) | The lid is one plate thickness; V line from C0.5 on both parts |
| Notches | Four, 5.6 wide, round bottom on the floor, pitch 8 | Cables up to about 5.2 (USB, laptop power, audio); pitch = two modules; teeth 2.4 between them |
| Comb plates | 2.52 thick, 12 in from the ends, 0.25 under the lid | 1.5 pitches from the end; they are also the stiffeners of the open ends |
| Hooks | Four, 1.68 (DIV) × 8, at x ±32 (the quarter points), 0.25 inside the walls | Free length 9.2 above a 0.6 barb: bending strain about 1.8 % (1.5 × 1.68 × 0.6 / 9.2²), inside PLA's range |
| Barb grooves | Barb + 0.25 deep and tall, hook width + 0.25 each side | The lid cannot shift along the raceway: its ends stay flush with the base |
| Screws | Two, x ±16, Ø3.8 with a 90° countersink to Ø7.2 | 3.5 wood screws or M3 countersunk; between the combs, under the lid |
| Edges | C0.5, C0.6 at the mounting face | One visible chamfer value, including the vertical corners and the channel's outline at the open ends |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| base | Mounting face down (floor down) | Off-white |
| lid | Outer face down, hooks up | Off-white |
| (2 × 3.5 countersunk wood screws, or double-sided foam tape) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| base / lid | With R6 corners in plan, the outer outline curved in past the inside of the walls at the open ends: the walls ended in a knife edge | Defect | Square ends in plan; the raceway is a profile, and the ends are where it is cut |
| base / lid | The barb grooves were 1 wider than the hooks on each side, so the lid could slide 1 along the raceway and stand out of line at the ends | Defect | Grooves = hook width + 0.25 each side (swept: free at 0.2, stops at 0.4) |
| base / lid | The vertical corners and the channel's outline in the open ends were left sharp | Violation | C0.5 on them |

Dos and Don'ts: one visible chamfer; one radius (the notches' round bottoms, R2.8); the screws are hidden under the lid; no accent; the
seam is one V line.

Use cases:
- **Mount:** screw the base to the wall or desk through the two countersunk holes, or tape it.
- **Lay the cables:** press each cable into its notch at both combs; four Ø5.2 envelopes lie in the notches and run out of both ends
  with no overlap with base or lid.
- **Close:** press the lid on; the hooks flex inward and the barbs click into the grooves (swept: the lid is free 0.2 above its seat,
  catches at 0.6 and rides over at 1–8 with a small overlap; it stops at 0.4 sideways and 0.2 toward the floor).
- **Open:** pull the lid off from one open end; the 45° barbs ride out of the grooves.
- **Print:** base floor down: walls and combs stand up, the notches are open at the top, the grooves are 45° V's in the walls; lid outer
  face down, hooks standing up with 45° barbs. No supports.

verify.py: valid, watertight, one solid per part, no interference, fits a 256 bed.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a raceway; a plain box with one V seam shares only the
general language. Cable raceways and cable combs are common kinds of object; no product was used as a model.

Safety: no batteries, LEDs, magnets or heat. Do not run mains cables with damaged insulation through it, and do not pinch cables under
the lid.

Not verified:
- Not printed on a real printer.
- The snap force of the hooks in PLA, and how many openings they take before they set.
- Cable diameters: a cable thicker than about 5.4 does not drop into a notch; make `NOTCH` and `P` larger.
