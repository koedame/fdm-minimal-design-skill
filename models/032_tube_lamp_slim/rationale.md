# 032 Slim tube lamp

A translucent tube (Ø40, 160 tall) on a low disc (Ø64 × 16), closed by a cap of the same height as the disc. Two runs of 5 V LED strip
on a flat spine down the axis light the tube from inside; a USB-C power breakout in the back of the disc feeds them. The disc's lip ring
locates the tube, the cap locates on the tube with the same lip, and the spine stands in a slotted boss in the disc and in a socket in
the cap. The board lies in a channel with a 45° gabled roof that runs from the pocket inside the lip to the back wall; it slides out over
a small ridge, which then keeps a plug's push from moving it back, and its receptacle sits 0.25 behind the wall (thinned to 1.68 there).
No accent: the lamp has no switch.

The board and the strip are generic; set `BRD`, `RCP` and the spine size in `design.py` to yours before printing.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Tube | Ø40, 160 tall, wall 1.68 | Four diameters tall; the 4-line wall of the lantern's diffuser for an even glow |
| Disc | Ø64 × 16 | The tube plus a rim of 12 (three modules) all round; wide enough to stand a 192 tall lamp |
| Cap | Ø40 × 16 | The height of the disc: the two ends match. Total 16 + 160 + 16 = 192 = 3 × the disc |
| Lip rings | 1.68 wide, 4 tall, 0.25 inside the tube | Location of 10 lantern, the same ring at both ends |
| Spine | 12 × 3.36 flat bar, 181.5 long, C0.5 on the long edges | Carries an 8 mm strip on each face; 8 lines thick; prints flat on the bed |
| Spine boss and socket | slot 0.25 clear all round; 14 deep in the disc, 8 in the cap | Holds the bar upright; the cap's socket keeps the top centred |
| Board channel | 10.5 wide (board + 0.25 per side), 45° gabled roof | A pocket inside a solid disc prints without support only with a roof that rises at 45° |
| Detent ridge | 0.6, a 45° ramp toward the pocket and a vertical face behind the board | The board rides over it on the way out; a plug pushed in cannot move it back |
| USB-C window | receptacle + 0.4 per side (9.74 × 4.06), board 0.25 behind the wall, wall 1.68 there | The connector rule: the receptacle face within about 2 of the outside |
| Feet | Ø10.2 × 1 recesses at (±16, ±16) | The rubber foot rule, on the 4 mm grid |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| base | Bottom down, 100 % infill | Off-white |
| tube | Bottom down | Translucent white |
| cap | Top face down | Off-white |
| spine | Flat | Off-white |
| led_strips_ref | Bought part, not printed | — |
| usb_board_ref | Bought part, not printed | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| base | Nothing held the board in its channel: pushing a plug in slid the board back into the pocket | Defect | A 0.6 ridge behind the board (45° ramp in, vertical face out); the channel is 0.5 taller so the board can ride over it (swept: pushed back 0.3, the board meets the ridge) |
| base | With the disc printed at a common 20–25 % infill, the centre of gravity is about 85 up and the lamp tips at about 21° | Defect | Print the disc solid (100 % infill): the centre of gravity drops to about 64 and the tipping angle rises to about 27° (estimated from the part volumes) |

Use cases:
- **Place:** the disc stands flat on the desk (2776 mm²) with four rubber feet; the cable leaves the back 5 above the desk, so a pull on
  it does not tip the lamp.
- **Assemble:** lower the board into the pocket at the channel, receptacle first, slightly tilted past the spine boss, and push it out
  until it drops behind the ridge. Stick the strips on the spine, solder their leads to the board, stand the spine in the boss, slide the
  tube over the lip and press the cap on (its socket takes the top of the spine).
- **Plug in:** hold the disc and push the USB-C plug in; the ridge takes the push (swept: board stopped 0.3 back and 0.4 forward).
- **Print:** disc bottom down (vertical boss and lip, gabled channel, a stadium window); tube standing; cap top face down; spine flat. No supports.

verify.py: all printed parts valid and watertight, no interference with each other, the strips or the board; fit a 256 bed; ground
contact 2776 mm². Tube and cap located by the lips (stopped 0.4 sideways); the cap seats on the tube.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a lamp; this is a plain tube on a disc. Tube lamps of
this kind are common; no product was used as a model.

Safety (LED, electricity, heat): use a certified USB power supply and a breakout board with the CC resistors (without them a USB-C
charger gives no power). The strips give off some heat inside the closed tube (about 1.5 W for 0.3 m of a common 5 V strip; not
measured); print the tube in PETG, not PLA, and do not cover the lamp. The printed parts are not certified for anything.

Not verified:
- Not printed on a real printer.
- The temperature inside the tube when lit for hours (not measured).
- The tipping angles are estimates from part volumes and an assumed infill, not weighed.
- How evenly the tube glows with two strips on a flat spine (the ends behind the lip rings will be darker).
