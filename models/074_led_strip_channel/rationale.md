# 074 LED strip channel

A 192 long, 20 × 20 channel for LED tape up to 12 wide. The channel is a U profile open at both ends, square in plan, so lengths butt into
a longer run; it is printed floor down. The tape sticks to the floor; two countersunk screws under the tape hold the channel (or
double-sided tape). The diffuser is a 1.68 plate of translucent PLA with the channel's width; eight vertical hooks hang from it inside the
walls and their 45° barbs drop into V grooves that run the whole length of the walls, so it also slides in from an end. The seam is a V
line with C0.5 on both sides.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Profile | 20 × 20 | 5 × 5 modules; the inside (14.96) takes 10 and 12 tape |
| Length | 192 | 48 modules; fits a 256 bed with room, and two make 384 |
| Walls, floor | 2.52 (T), 2.4 | One wall, one plate |
| Diffuser | 1.68 (DIV) | The Light rule: a 4-line layer glows evenly; it sits 13.9 above the tape's top |
| Hooks | 8 × 16 wide, 1.68 thick, at x ±24 and ±72 (pitch 48), down to z 8 | Pitch 12 modules; the bottoms stay 3.6 above the tape |
| Barbs | 0.6 at 45°, 0.35 past the 0.25 gap; free length about 9 | About 1.1 % strain when pushed on; the diffuser weighs about 10 g, so a shallow catch holds it even upside down |
| Grooves | Barb + 0.25 all round, 45°, the whole length | Hooks catch anywhere, and the diffuser slides in from an end |
| Screws | 2 × 3.5 countersunk at x ±48, head Ø7 flush with the floor | Between the hooks, under the tape |
| Ends | Open and square in plan, inside edges C0.5 | Open profiles stay square at the ends; lengths butt |
| Edges | C0.5; C0.6 on the bed faces | One visible chamfer value; the seam is a V line |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| channel | Floor down | Off-white |
| diffuser | Top face down | Natural (translucent) |
| tape_ref | Bought: LED tape up to 12 wide | — |
| (2 × 3.5 countersunk wood screws, or double-sided tape) | Bought | — |

## Review

No defects or violations found. Checked in particular: the barb engagement (0.35, the same as the cable raceway 055; enough for a
10 g diffuser, and the diffuser slides out along the grooves without unhooking), the hooks' clearance over the tape (3.6), and that the
grooves have 45° faces above and below in the print.

Dos and Don'ts: one visible chamfer value (C0.6 only on the bed faces); no radii (an open profile stays square at its ends); the seam
is one V line along both sides; no fastener shows (the screws are under the tape); channel off-white, diffuser natural; no accent.

Use cases:
- **Mount:** screw the channel to a wall, under a shelf or a cabinet through the two countersunk holes (or use double-sided tape), then
  stick the tape on the floor over the screw heads.
- **Light:** the tape shines on the diffuser 13.9 above it; the 1.68 layer spreads the dots into a line. The ends are open, so the last
  few millimetres show the tape from the end.
- **Close:** press the diffuser on; the hooks click into the grooves (swept: free at 0 and 15 up, 15.4 mm³ of barb being pushed over in
  between, stops 0.5 further down on the walls). Or slide it in from an end (swept: free along the length at 10 and 50).
- **Open:** slide the diffuser out along the grooves, or pull it up.
- **Join:** butt two channels end to end; the square ends meet in a line.
- **Print:** channel floor down: walls stand up, the grooves have 45° faces, the countersinks open upward. Diffuser top face down: hooks
  stand up, barbs are 45° both ways. No supports.

verify.py: both printed parts valid and watertight, one solid each; no interference (the tape included); fit a 256 bed.

Compared with well-known products in this style: none is a light channel. A U profile with a snap-on diffuser is the
generic form of an LED profile; no product was used as a model.

Safety (LEDs, heat): PLA softens at about 55 °C. Use LED tape of moderate power (check its rating and how warm it gets), from a power
supply of a trustworthy source with its own protection, and do not cover the channel. The printed parts are not certified for anything.

Not verified:
- Not printed on a real printer.
- How warm the tape gets inside the closed channel, and how evenly the 1.68 diffuser spreads your tape's dots.
- How firmly the hooks hold in translucent PLA.
