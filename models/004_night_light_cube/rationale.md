# 004 Night light cube

A translucent 64 mm cube on a low base. The base runs 16 mm further back than the cube, and that strip carries the
slide switch on top, where a hand finds it in the dark without moving the light. Powered over USB-C at the back.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Cube | 64 × 64 × 64 | Grid 4 |
| Base | 64 × 80 × 16 | The cube plus a 16 strip behind it; total height 16 + 64 = 80 = the base depth, so the side profile fits an 80 square |
| Plan radius | R8 | 12.5% of 64; shared by the cube and the base |
| Walls, floor, deck, cube top | 2.52 | 6 lines, one thickness throughout |
| Deck seat | 1.68 ring with a 45° underside | Prints bottom up without supports |
| Lip under the cube | 1.68 × 4, flush with the deck edge | Locates the cube with 0.25 clearance |
| Switch | knob 16 × 8 × 2.4 on the strip, travel 8, Ø2.4 neck | Centred on the visible strip and on the cube's centre line |
| USB-C window | 12 × 6.4 stadium, centred on the back | Midway between the floor and the deck seat |
| Rubber feet | 4 × Ø10.2 at x ±20, y ±28 | Inside the floor, clear of the walls |
| Accent | the switch knob | The one control |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| base | Bottom down | Off-white |
| deck | Bottom face down (the lip is a step on its top, so the top prints up) | Off-white |
| diffuser_translucent | Top face down | Translucent white (shown lit) |
| slider_knob | Top face down, neck up | Accent |
| slider_carrier | Flat | Dark grey |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| slider_knob | The neck was square in a slot with round ends: at the end of the travel its corners (1.70 from the end centre) hit the 1.5 radius | Defect | Round neck Ø2.4 |
| deck, diffuser | With a 1.68 cube wall the lip had to sit 0.84 outside the deck edge, unsupported in the print | Defect | Cube walls 2.52 like the base; the lip is flush with the deck edge (and wall thickness is now one value) |

Use cases:
- **Place:** stands on four rubber feet, 63 × 79; the cube sits over the front of the base.
- **Switch:** the knob slides 8 mm along the strip; the carrier under the deck forks over the lever of a small slide switch (for example SS-12D00) that you mount below it.
- **Open:** lift the cube off the lip; lift the deck by the knob, which takes the carrier off the switch lever.
- **Print:** base bottom up with a 45° seat, cube top down, deck and knob as listed; no supports.

verify.py: all parts valid and watertight, no interference, fits a 256 bed, ground contact 4582 mm² over 62.9 × 78.9 mm.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a light; the stepped profile with the switch strip
behind a cube is not taken from any product. No product was used as a model.

Safety: this light holds LEDs and electronics powered over USB. Use a certified USB power supply and LED module, keep the LEDs'
heat low (a few hundred milliwatts), and check the electrical design yourself; the printed parts are not certified for anything.

Not verified:
- Not printed on a real printer.
- How evenly a 2.52 translucent wall glows, and with how much light.
- The position of the real slide switch under the carrier (match it to the switch you use).
