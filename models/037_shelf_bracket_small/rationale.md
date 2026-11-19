# 037 Small shelf bracket

An L bracket, 80 × 80 and 28 wide, for a small shelf board up to about 100 deep. Seen from the room it is one solid L with a 45° web
in the inside corner and no screw anywhere: it hangs on a wall plate. The plate is screwed to the wall; its section is a 45° dovetail,
and the bracket's back carries the matching pocket, open at the bottom, so the bracket slides down over the plate and covers it. A
screw from below, in a counterbore under the arm, holds the board to the bracket. The bracket prints lying on its side, so every
layer is a whole L and the bending load runs along the layers, not across them.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Bracket | 80 × 80 × 28 | 1 : 1 L; 28 wide covers the 20 wide plate with 3.4 walls either side of the pocket |
| Leg, arm | 12 thick | 3 × 4 module; the arm carries the board |
| Web | 45°, 28 along each leg | Stiffens the corner; 45° so it reads as the 45° language of the dovetail and prints without support either way |
| Wall plate | 56 high, 4 thick, 12 wide at the wall, 20 at the front (45° flanks) | Two screws 32 apart; the dovetail takes the pull at the top of the leg |
| Pocket | Plate + 0.25 normal to every face, open at the bottom, 0.25 above the plate top | Clearance between parts; the pocket top rests on the plate |
| Wall screws | 4 mm countersunk, Ø4.5 hole, 90° countersink to Ø9 | Common wood screw or anchor screw |
| Board screw | 3.5 mm, Ø4 clearance, Ø8.4 counterbore, 4 left under the board, 24 from the arm's tip | Holds the board down; hidden under the arm |
| Edges | C0.5, C0.6 on the bed side | One chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| bracket | On its side (the left face down) | Off-white |
| wall_plate | Wall side down | Off-white |
| (2 × 4 mm countersunk screw, 1 × 3.5 mm wood screw) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| — | No defect or rule violation found; the checks below passed as first built | — | — |

Use cases:
- **Mount:** screw the plate to the wall, upright, with its narrow face against the wall (anchors in plasterboard). Lower the bracket
  onto it from 64 above until the pocket top sits on the plate (swept: free upward to 70, stops 0.5 down, 0.5 away from the wall and
  0.5 sideways).
- **Shelf:** two brackets, the board on top, one screw up into the board through each arm. Choose the screw length as 4 + the board
  thickness − 3 (3.5 × 16 for a 15 mm board).
- **Take the shelf down:** lift the board straight up; the brackets come off with it and the plates stay.
- **Load:** the board's weight turns the bracket about the foot of the leg; the dovetail at the top of the plate takes the pull (about
  17 N for 25 N on the middle of the arm) and the leg's foot presses on the wall.
- **Print:** bracket on its side, no supports (the pocket's flanks are 45°, the board screw holes are teardrops pointing up); plate
  flat.

verify.py: bracket and plate valid and watertight, no interference, fit a 256 bed.

Compared with well-known products in this style: radios, a pocket radio, a calculator and a loudspeaker; none is a
bracket. Plain L brackets with a corner web are a common form; no product was used as a model.

Safety (load): a shelf can fall with everything on it. The bracket's strength has not been calculated or tested, so it has no rated
load: keep to light things, nothing heavy, breakable or hot. The pull on the plate's top is about two-thirds of the weight on the
middle of the arm (17 N for 25 N, see Load), and what the bracket takes before it lets go depends on the material (PETG; PLA creeps
under a constant load), on printing it on its side as given (printed on its back, the layers would split at the corner), on the walls
and infill, and on the wall: two screws per plate into a stud, or anchors rated for your wall (plasterboard anchors, plugs in
masonry). Do not put the shelf over a bed, a sofa, a cot or a place where you sit. Before loading it, press down on the board's front
edge by hand, harder than what you mean to put on it, and look again after a few days that the brackets have not tilted.

Not verified:
- Not printed on a real printer.
- The load a bracket takes before it bends or the dovetail lets go; print in PETG and keep to light things (books, a plant, a few
  kilograms per pair).
- From directly below, the open end of the pocket shows as a notch in the back of the leg's foot.
