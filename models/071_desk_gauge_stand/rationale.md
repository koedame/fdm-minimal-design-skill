# 071 Desk gauge stand

An upright frame that puts a round panel gauge (a thermometer, hygrometer, barometer or a meter with a Ø52 body behind a Ø60
bezel) on the desk. The frame is a sleeve open at the back, 76 × 40 × 92, on a dark 8 high base with a floating plinth. The gauge
goes in from the front; its own clamp bracket grips the 4 thick front wall from inside, and its cable or hose leaves through the
open back. Two M2 screws come up through counterbores in the base into the solid lower band of the frame, so no fastener shows.

Gauges differ: set `G_BODY`, `G_BEZEL` and `G_DEPTH` in `design.py` to the one you have before printing.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Band round the bezel | 8 (top and sides) | One margin for one role; also the base height and the outline radius |
| Band below the bezel | 24 | 3 × the band: the dial sits in the upper part, the frame stands on the lower |
| Frame | 76 × 40 × 92 | Ø60 bezel + 2 × 8; 8 + 60 + 24; depth: the gauge's 36 behind the bezel stays 4 inside the open back |
| Outline radius | R8 on the frame's top corners and the base's plan corners | = the band (10.5 % of 76); the frame's bottom corners stay square where it sits on the base |
| Inside corners | R3 | The small radius for inside corners |
| Bore | Ø52.5 with a C0.5 lead-in | The Ø52 body + 0.25 per side; the lead-in hides under the bezel |
| Front wall | 4 | 20 layers; thin enough for the clamp bracket that comes with a panel gauge |
| Walls | 2.52 (T) | 6 lines |
| Solid lower band | 16 (z 8–24) | Takes the 10 deep pilot holes; ends 11.75 under the bore |
| Base | 76 × 56 × 8, plinth inset 1.2 at 45° | 8 beyond the frame in front and behind; the shadow line of the floating plinth |
| Screws | 2 × M2 at x ±24: pilot Ø1.8 × 10, clearance Ø2.4, counterbore Ø4.2 × 1.8 | The Hidden screws rule; M2 × 12: 6.2 through the base, about 6 into the frame |
| Rubber feet | 4 × Ø10.2 at (±26, ±18) | Clear of the counterbores |
| Edges | C0.5; C0.6 on the base's bed face | One visible chamfer value; frame and base meet in a V line |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| frame | Front face down | Off-white |
| base | Bottom down | Dark grey |
| gauge_ref | Bought: round panel gauge, Ø52 body, Ø60 bezel | — |
| (2 × M2 × 12 pan-head screws, 4 × Ø10 stick-on feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| frame | The print orientation turned the frame back face down (`rx(…, -90)`), which would have put the open back on the bed and the front, with its outline radii, on top as the last layers | Defect | `rx(…, 90)`: the front face is on the bed, the open back faces up |
| frame | The rim of the bore was a bare edge | Violation | C0.5 lead-in cut as a cone; it also guides the gauge in and hides under the bezel |

Dos and Don'ts: one visible chamfer value; two radii (R8 outline, R3 inside); margins round the bezel are equal on three sides and the
lower band is 3 × that; no fastener shows; frame off-white, base the secondary dark grey; no accent (the gauge's own pointer is the
functional mark).

Use cases:
- **Place:** stands on four rubber feet; the base runs 8 beyond the frame in front, so a pull on the cable at the back does not tip it.
  Ground contact 3412 mm² over 72.5 × 52.5.
- **Read:** the dial centre is 62 above the desk and the face is vertical, for reading from a seat at the desk.
- **Fit the gauge:** remove the gauge's bracket, push the gauge in from the front until the bezel sits on the face, refit the bracket
  from the open back and tighten it against the inside of the front wall. Pass the cable or hose out of the back.
- **Assemble:** set the frame on the base flush at the sides, drive the two M2 × 12 screws up from below.
- **Print:** frame front face down: bore, cavity and the open back are vertical; the outline radii lie in the layer plane; the pilot
  holes are horizontal and Ø1.8 (small enough to stay round). Base bottom down; the shoulder in each counterbore is a 0.9 wide ring of
  bridging.

verify.py: both printed parts valid and watertight, one solid each; no interference (the gauge included); fit a 256 bed; ground contact
3412 mm².

Compared with well-known products in this style, including small alarm clocks: a round dial in a rectangular front
is common to many clocks and instruments, including those alarm clocks. This one differs in its proportions (an upright 76 × 92 front
with the dial in the top and a 3 × band below), the open-back sleeve and the separate dark plinth; it holds a bought gauge, has no
clock face of its own, and no product was used as a model.

Not verified:
- Not printed on a real printer.
- Whether your gauge's bracket clamps a 4 thick wall; gauges with a deeper body need a deeper frame (`DF`).
- The pilot holes' hold in the frame's lower band (printed with the hole horizontal).
