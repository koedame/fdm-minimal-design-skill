# 085 Clock tray block

A desk clock, 96 square in plan, whose front half is a shallow tray for keys, rings and coins; the back half is a block 80 high with the
dial on its front, facing the room over the tray. The body is one part printed bottom down. The block is a sleeve open at the top: the
quartz movement goes in from above and is clamped to the inside of the front wall by its shaft nut, through the dial disc on the outside.
A lid with a lip inside the walls locates on top; lifting it is the way to the battery. A floating plinth runs under the whole body.

Movements differ: set `CLOCK_SHAFT_HOLE`, `HAND_HOLES` (in `fdm_samples.py`) and `MOVE`, `MOVE_T` to the one you have, and choose one whose
thread suits a 4.9 thick dial and wall.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Plan | 96 × 96, R12 | 24 modules; R12 = 12.5 % |
| Block | 40 deep, 80 high | Holds a 56 × 56 × 16 movement with 19 behind it for fingers at the battery |
| Tray | 56 deep, rim 12 high, floor 4 (8 deep) | Keys and rings; its rim is the dial's lower reference line |
| Dial | Ø48 × 2.4, centred 46 up | 10 of margin above it to the top and below it to the tray rim (one margin for one role) |
| Marks | Majors 2.4 × 6, minors 1.2 × 3 (2 : 1 both ways), ending 3 inside the rim; inlaid 0.4 | The dial language of sample 01; the 12 o'clock mark in the accent |
| Hands | Minute 18 (to the minors' inner ends), hour 13.5 (3/4), widths 1.2 and 2.4 | The two mark widths, drawn out |
| Walls | 2.52 (T) | 6 lines |
| Radii | R12 outline; R9.48 concentric at the tray's front corners; R3 at its back corners | Two radii by role plus the concentric inside of the outline |
| Lid | 2.4 thick, lip 1.68 (DIV) × 4 deep, 0.25 inside the walls | The Location rule; the lip ends 2 above the movement |
| Shaft hole | Ø7.6 teardrop through the front wall | The movement's thread; horizontal in the print |
| Floating plinth | 2.4 high, inset 1.2 at 45° | The shadow line under the whole body |
| Rubber feet | 4 × Ø10.2 at (±36, ±36) | Inside the plinth |
| Edges | C0.5, also the tray's inner rim and the block's front corners; C0.6 on the bed faces | One visible chamfer value; the lid's seam is a V line |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down | Off-white |
| lid | Top face down | Off-white |
| dial + dial_marks_inlay + dial_top_mark_inlay | Front face down (layers 1–2 in other colours) | Light grey + dark + accent |
| hand_hour / hand_minute | Flat | Dark |
| movement_ref | Bought: quartz clock movement, 56 × 56 × 16, without a seconds shaft | — |
| (AA battery, 4 × Ø10 stick-on feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| body | The two vertical edges where the block's front face meets its sides were left sharp | Violation | C0.5 on both |
| body | The C0.5 on the tray's inner rim failed in CadQuery (the rim runs into the block's front face) and was first left off | Violation | Cut as a 45° flare: the rim's outline lofted to its 0.5 offset over the last 0.5 |
| movement_ref | The movement's shaft was drawn through the hands (17 and 29 mm³ of interference) | Defect (in the check) | Shaft through the wall and the dial only; the hands sit in front of it on their bushes |

Dos and Don'ts: one visible chamfer value (C0.6 on the bed faces only); R12 and its concentric inside, R3 inside corners; the dial's
margins above and below are equal and its lower one is the tray rim; one accent (the 12 o'clock mark); no fastener shows; dial light grey
with dark marks; plain outside, the work in the dial.

Use cases:
- **Place:** stands on four rubber feet; ground contact 8130 mm² over 92.5 × 92.5; the block's weight at the back keeps it steady when
  keys are dropped into the tray.
- **Read:** the dial centre is 46 above the desk, behind the tray; the hands are dark on a light grey dial, the 12 o'clock mark tells
  which way is up.
- **Drop things in:** the tray is 8 deep with rounded corners, 90.96 × 53 inside.
- **Change the battery:** lift the lid (swept: free from 0 up; it rests on the walls and stops 0.4 sideways and forward), reach in behind
  the movement (19 of room).
- **Assemble:** lower the movement into the sleeve behind the front wall, push its shaft through the hole, fit the dial over the thread
  and tighten the nut; push the hands on; put the lid on.
- **Print:** body bottom down: the walls stand up, the tray and the sleeve open upward, the shaft hole a teardrop. Lid top face down, the
  lip standing up. Dial front face down with the marks in the first two layers. No supports.

verify.py: every printed part valid and watertight, one solid each; no interference (the movement included); fit a 256 bed; the lid's
motions as recorded.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2, and Braun's BC and AB clocks): a round dial in a rectangular front is
common to many clocks, including those. This one differs in its plan (a square split into a tray in front and a block behind), the dial
set in the block's front with a tray below, and its proportions; no product was used as a model.

Safety (battery): the movement takes an AA cell; keep spare cells away from the keys and coins in the tray, where their terminals can be
shorted, and away from children.

Not verified:
- Not printed on a real printer.
- Whether your movement's thread is long enough for the 2.52 wall and the 2.4 dial; many are made for dials up to about 5.
- Whether the dial stays square when the nut is tightened (it is held by the nut only).
