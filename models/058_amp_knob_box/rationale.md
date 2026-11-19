# 058 Amp knob box

A box for a small headphone amplifier, 96 × 72 × 44.8, with one volume knob on the front and nothing else on the front, top or sides.
The knob is centred on the body's front face with the same 8 margin below it and above it to the seam. It turns a 16 mm potentiometer
that clamps against a boss behind the front wall; its nut sits in a recess in the front face, covered by the knob. The cover is a 4.8
plate held by four 6 × 3 magnets in posts in the body's corners and located by a lip that drops 2.4 inside the walls. The back carries
three panel jacks at the knob's height (power, input, headphones) and a shallow scoop under the cover's edge for a fingertip.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 96 × 72 × 44.8, R8 | 12 × 9 modules in plan; a 50 × 40 board and the pot fit with room for wiring |
| Body, cover | 40 and 4.8 | The cover is two plate thicknesses: the magnet pockets (3.2) leave a 1.6 skin above them |
| Knob | Ø24 × 12, centred at the body's mid-height (z 20), 0.4 off the face | 8 margin below and above to the seam; 12 long gives a 4 grip band (32 ribs) at the back and the D-shaft engagement |
| Knob face | One step (Ø16.8 recess 0.8), one line from r3.6 to r7.6, pointing up at rest | One indicator, one step |
| Walls, floor | 2.52 (T), 2.4 | One wall, one plate |
| Pot boss | Ø20 behind the front wall, 2.6 deep; bushing hole Ø7.2 teardrop | The pot's mounting face clamps against 5.1 of material |
| Nut recess | Ø12.4 teardrop, 2.4 deep in the front face, under the knob | The M7 nut (2 thick) stays below the face; the knob covers it |
| Knob bore | D shaft from 2.5 under the face; Ø8 counterbore 2 deep with a 45° cone | The bushing's end stands 1.9 out of the face; cone prints without support face up |
| Magnet posts | 8 × 8 in the corners, Ø6.2 × 3.2 pockets at the top; matching pockets in the cover | The corners hold nothing else; both pockets open upward in their print orientations |
| Cover lip | 1.68 (DIV) × 2.4, 0.25 inside the walls, stopping 0.25 short of the posts | Locates the cover on the body; the magnets only hold it down |
| Board | 50 × 40 on four Ø6 posts 3.6 tall with Ø2.8 pins, centred | Through-hole legs clear the floor; the parts stay 4 from the jacks' bodies |
| Jacks | Ø8.2 (M8 power) and two Ø6.2 (M6), teardrops, at x −24 / 0 / +24, z 20 | One row at the knob's height, on the back |
| Finger scoop | R12 arc in the back wall's top, 3 deep, 16 wide, C0.5 | A fingertip lifts the cover's back edge against the magnets |
| Edges | C0.5; C0.6 on the bed faces | One visible chamfer value; the seam is a V line |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Floor down | Off-white |
| cover | Top down (the pockets and the lip face up) | Off-white |
| knob | Front face up | Off-white |
| magnet_ref × 8, board_ref, pot_ref, jacks_ref × 3 | Bought | — |
| (4 × Ø10 stick-on feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| cover | The lip's ends next to two of the corner posts were cut flush with the posts: no clearance there | Defect | The lip stops 0.25 short of every post |
| body / cover | The cover sat flush on four magnets with nothing to lift it by | Defect | Finger scoop in the back wall's top, under the cover's edge |
| board_ref / jacks_ref | The jacks reach 14 in from the back wall; with the board 8 toward the back they ran into its parts (58 mm³) | Defect | Board centred; jacks added as bought parts so the check sees them |
| knob | A dark knob read as an accent on the off-white box | Violation | Knob in the box's colour |

Dos and Don'ts: one visible chamfer; one radius in plan (R8) and the knob's circle; one feature on the front; no visible fasteners (the
nut is under the knob, the jacks' nuts are on the back); no accent colour; the seam is one V line.

Use cases:
- **Volume:** turn the knob; the ribs at its back give grip and the step and line on its face show the position (swept: free about its
  axis at 0–270°, 0.4 off the face, stops at 0.6 when pressed).
- **Connect:** power, input and headphones plug into the back, at the same height in one row.
- **Open:** a fingertip in the scoop lifts the cover's back edge; the magnets let go and the lip clears the walls (swept: free upward
  from 0; stops at 0.3 downward and at 0.4 sideways, free at 0.2).
- **Assemble:** glue the magnets in the posts and in the cover with opposite poles facing; push the pot's bushing through the boss
  from inside (break off its small locating tab; the boss has no hole for it), tighten the nut in the recess and press the knob on; screw
  the jacks into the back; lay the board on its pins and wire it.
- **Print:** body floor down: the walls, posts and pins stand up, the horizontal holes are teardrops with the apex up; cover top down with
  the lip and the pockets up; knob front face up. No supports.

verify.py: valid, watertight, one solid per part, no interference, fits a 256 bed.

Compared with well-known products in this style: the radios among them have grilles and several controls, and one is a loudspeaker. This is a plain box with a single knob on its front; it shares the general language (one material, rounded rectangle, one
control) and no specific layout. No product was used as a model.

Safety: magnets: keep the loose magnets away from children (swallowed magnets are dangerous) and glue them in. Electronics on a 5–12 V
adapter: use a board of a few watts; a larger amplifier needs ventilation, and PLA softens at about 55 °C (PETG at about 75 °C). Use an
adapter with the usual approvals.

Not verified:
- Not printed on a real printer.
- The holding force of four 6 × 3 magnets across the 1.6 skins, and how firmly the cover sits.
- Board hole positions and pot shaft lengths vary between suppliers; change `PINS` and cut the shaft to 15 from the mounting face.
