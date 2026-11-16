# 065 Wall headphone hook

A hook for one pair of over-ear headphones, 48 × 86.4 × 96. A plate 48 × 96 hangs on two keyholes cut into its wall face; one arm,
32 × 16 in section, reaches 80 forward from two-thirds of the plate's height, and its last 6 rise 6 on a 45° ramp so the headband does
not slide off the end. The plate is set 1.2 in from the wall at 45°, so it sits on a shadow line. One radius, R6, rounds the plate's
corners, the arm's corners and the arm's root. The part prints with the wall face down: the plate and the arm's section are then in the
layer plane, every radius is a curve in plan, and the keyholes print face down.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Plate | 48 × 96 × 6.4 | 12 × 24 modules (1 : 2); 6.4 = keyhole ledge 2 + head pocket 3 + 1.4 |
| Shadow line | Wall face set in 1.2 at 45° | Separates the plate from the wall with one thin shadow, as the sample wall unit |
| Arm section | 32 × 16 (2 : 1), R6 corners | 32 ≈ the width of a headband; the band's arch rests on the two R6 top corners |
| Arm height | Centre at 64 (two-thirds of 96) | The keyholes sit above and below it on the centre line |
| Arm reach | 80 from the plate (5 × its thickness) | The band hangs about 50 from the wall, so ear cups up to about 90 across clear the wall |
| End ramp | Rises 6 over 6 at 45°, then 6 flat | Keeps the band on; prints as a 45° overhang |
| Radius | R6 for the plate's corners, the arm's corners and the arm's root | One radius in the object; 12.5 % of the plate's width; the root R6 leaves 2 of flat plate beside the arm |
| Keyholes | Two on the centre line, entries at z 24 and 80, 6 travel | Head Ø8.4, shank Ø4.2; one above and one below the arm, so the plate cannot turn on the screws |
| Edges | C0.5 on the plate's front edge and the arm's end; C0.6 and the 1.2 shadow line at the wall face | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| hook | Wall face down | Off-white |
| (2 × 4 mm pan-head or countersunk screws and wall plugs) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| hook | The arm reached 56: the headband hung about 30 from the wall and ear cups of 90 across ran into the wall | Defect | Reach 80; the band hangs about 50 from the wall |
| hook | The raised end was the arm and a raised copy of its section joined by a union: the end face read as a figure 8 and the mesh was not closed (`verify.py`: not watertight) | Defect | Ramp and end as one ruled loft through three sections (start of the ramp, top of the ramp, end); closed mesh, a plain end face |
| hook | Three radii (R8 plate, R8 arm ends, R6 root) where one role covers them all | Violation | R6 for the plate, the arm and the root |

Dos and Don'ts: one visible chamfer value plus C0.6 and the 1.2 shadow line at the wall face; one radius; no fasteners show (the screw
heads sit in the keyholes behind the plate); no accent (nothing has a function to point at).

Use cases:
- **Hang the hook:** drive two screws 56 apart on a vertical line, standing about 3 out of the wall. Put the keyhole entries over the
  heads and let the hook drop 6; the heads seat on the 45° seats inside the plate.
- **Hang the headphones:** put the headband over the arm. A band envelope (36 wide along the arm, R60 inside) rests on the arm's two top
  corners with no overlap and touches them when lowered 0.3; the ramp stops it 6 short of the end.
- **Take them off:** lift the band; the arm's top is open from above.
- **Load:** 400 g of headphones 50 out put about 0.2 N·m on the plate; the top screw takes about 2.5 N, the bottom of the plate presses on
  the wall. The arm is printed across its layers (the layers run across the arm), so the root is in bending across layer lines: the
  stress at the R6 root is about 0.1 MPa for 400 g, far below what layer bonds carry; do not hang a bag on it.
- **Print:** wall face down. The plate is the first 6.4; the arm stands up from it as a prism with its R6 corners in plan; the root R6
  flares out at the arm's foot; the ramp is a 45° overhang. The keyholes' head pockets print face down without support.

verify.py: valid, watertight, one solid. (The ground-contact line is the arm's end and not meaningful for a wall-mounted part.)

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a wall fitting; they are housings with controls,
grilles or perforation. Wall hooks for headphones are a common kind of object; no product was used as a model.

Safety: the hook has no batteries, LEDs, magnets or heat of its own. Fix the screws into wall plugs suited to the wall. The arm is
sized for 400 g of headphones (about 0.1 MPa at the root, see Load); the hold of the printed keyholes on your screws has not been
tested, so before use pull down on the arm by hand, clearly harder than the headphones weigh, and do not hang a bag on it.

Not verified:
- Not printed on a real printer.
- How the keyhole seats hold on the screws you use.
- How much load the arm takes on a real print before the layers part at the root.
