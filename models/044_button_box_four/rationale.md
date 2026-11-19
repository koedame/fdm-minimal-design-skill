# 044 Four-button control box

A 120 × 48 × 22 desk box with four round buttons in a row, for shortcuts, a stream or a smart-home scene. The top carries nothing but
the four buttons: every margin from a button's edge to the box's edge is 16, front, back and sides, so the row sits exactly in the
middle and the box's size follows from the buttons. The shell (top and walls) is one piece; a bottom plate closes it and is held by four
M2 screws from below into bosses hanging from the top, so no fastener shows from above or the sides. The plate's standoffs locate a
board with four 12 × 12 tactile switches; each button rests on its switch, and the cable leaves through a USB-C opening in the back.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Buttons | Ø16, pitch 24, 1.2 proud | A thumb-sized target; 8 between buttons = half a button |
| Margins | 16 on all four sides | One margin = one button: W = 3 × 24 + 16 + 2 × 16 = 120, D = 16 + 2 × 16 = 48 |
| Height | 22 | The standoffs (3.6, room for through-hole legs), board 1.6, switch 4.3, the button's stem and flange, the 6 guide |
| Corners | R8 | One sixth of the depth |
| Top / bottom plate | 2.4 | One plate thickness |
| Walls | 2.52 | Line width × 6 |
| Button holes | Ø16.6 | Button + 0.6 |
| Button guide | 6 long: the 2.4 top plate and a 1.68 sleeve under it | Tilt in the 0.3 clearance about 5.7° instead of 14° with the plate alone, so an edge press still pushes the switch |
| Button flange | Ø20 under a 45° cone, 1 thick | Keeps the button in; the cone prints face down without support |
| Switches | 12 × 12 tactile, 4.3 high | A common size with a large actuator |
| Bosses | Ø6, at the centres of the inner corner radii (x ±52, y ±16), split 5.4 above the bottom | Screw head in a Ø4.4 counterbore through the plate, bearing on the plate's boss; Ø1.8 pilot for M2 × 8 self-tapping screws |
| Standoffs | Ø6 × 3.6 with Ø2.8 × 2 pins, 88 × 24 apart | Locate the 96 × 32 board through Ø3.2 holes; the buttons resting on the switches keep the board on the pins |
| USB-C opening | 9.6 × 4 stadium, centred in the back wall | Takes a USB-C plug; the board's back edge sits 0.48 inside the wall |
| Feet | Four Ø10 rubber bumpers in 1 deep recesses | Keep the box from sliding under a press |
| Edges | C0.5; C0.6 on the top and on the plate's bottom (bed) | One chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| shell | Top down | Off-white |
| bottom_plate | Bottom down | Off-white |
| button × 4 | Top down | Dark grey |
| board_ref (96 × 32 board with four 12 × 12 tactile switches, a USB-C receptacle at the back edge and a microcontroller) | Bought / hand-built | — |
| (4 × M2 × 8 self-tapping screws, 4 × Ø10 rubber feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| shell / button | A Ø16 button guided only by the 2.4 top plate with 0.3 clearance tilts about 14°: it rattles, and a press near its edge tips it instead of pressing the switch | Defect | A sleeve under the top plate makes the guide 6 long (tilt about 5.7°); the switches became 4.3 high to keep the height at 22 |
| bottom_plate | Its bed edge was C0.5, unlike every other bed edge | Violation | C0.6 |

Use cases:
- **Assemble:** lay the shell top down, drop the four buttons into their holes, lay the board switches down onto the buttons' stems,
  then the plate: its pins go through the board's holes. Drive the four screws in from below and stick on the feet (swept: a button
  is free 0.2 up and stops at 0.5 on its cone, is free 3 down in the shell, and stops 0.3 down on its switch; the plate comes off
  straight down and stops 0.3 up against the bosses, 0.4 sideways).
- **Use:** press any button anywhere on its top; the guide keeps it square, the switch clicks.
- **Plug in:** a USB-C cable into the back.
- **Open:** four screws from below.
- **Print:** shell top down (walls, sleeves and bosses stand up, the USB-C opening's small arcs need no support); plate bottom down;
  buttons top down (the cone under the flange is 45°). No supports.

verify.py: all parts valid and watertight, one solid each, no interference, fit a 256 bed.

Compared with well-known products in this style: the calculator has a grid of many small round keys under a display;
the radios have dials and a few keys among a grille. This is a single row of four large equal buttons on a plain box, with no display
or grille. Button boxes and macro pads are a common kind of object; no product was used as a model.

Safety (electronics): the box holds a board powered over USB. Use a certified USB power source or computer port; the printed parts
are not certified for anything.

Not verified:
- Not printed on a real printer.
- The board is not designed here: its size, hole positions and the receptacle's height (`PCB`, `PIN_XY`, `z_usb`) must match yours.
- The press feel: the buttons sit on the switches under their own weight and can lift 0.3 when the box is turned over (they rattle
  only then).
- Whether the M2 pilots hold in PLA after several openings.
