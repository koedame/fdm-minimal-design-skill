# 072 E-paper display frame

A standing frame for a bare 4.2-inch e-paper panel (91 × 77 × 1.2 outline), 120 × 32 × 100. The body is a sleeve open at the back,
printed front face down. A clear PETG window with a flange fits the 88 × 68 opening from behind and sits flush with the front, a V line
round it; the panel lies on the flange inside a locating rim; a back cover clicks into the open back on two 45° hooks, and two ribs on
the cover hold the panel against the window. A driver board taped to the inside of the cover, between the ribs, takes the panel's flex
tail; the USB cable leaves through a notch in the cover's bottom edge.

Panels differ: set `PW`, `PH`, `PT`, `WIN_W` and `WIN_H` in `design.py` to the panel you have and the position of its view area.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Window | 88 × 68, R3 | Shows the 84.8 × 63.6 view area of a 4.2-inch panel with 1.6–2.2 to spare |
| Margin | 16 on all four sides | Margins with one role, one width |
| Front | 120 × 100 (6 : 5), R12 | Window + 2 × 16; R12 = 10 % of 120 |
| Depth | 32 | 8 modules; the frame stands on it (tips at about 18°) and the board fits behind the panel |
| Walls, front plate, cover | 2.52 (T), 2.4, 2.4 | One wall, one plate |
| Window part | Plug 87.5 × 67.5 × 2.4 (0.25 per side), flange 91 × 77 × 1.2 | Flush with the front; the flange is the panel's outline, so the two stack in the rim |
| Locating rim | 1.68 (DIV) round 91.5 × 77.5, 2.4 high, a 32 gap at the bottom | Panel + 0.25 per side; the gap lets the flex tail out |
| Cover | 0.25 inside the walls, flush with the back, C0.5 | The seam is a V line round the back |
| Hooks | 2 × 16 wide × 16 long, 1.68 thick, at the side walls | Free length 13 to the barb: about 0.9 % strain at 0.6 deflection |
| Barbs and grooves | Barb 0.85 at 45°, 0.6 of it past the 0.25 gap; groove = barb + 0.25 | The Snap (hook) rule; comes off when pulled |
| Panel ribs | 2 × 1.68 at x ±40, 50 high, 0.1 short of the panel | Hold the panel to the window near its side edges, clear of the board |
| Cable notch | 8 wide, 4 high, round top | A USB cable; doubles as the place to pull the cover |
| Rubber feet | 2 × Ø10.2 at x ±44 | Under the bottom wall |
| Edges | C0.5 | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Front face down | Off-white |
| window_clear | Front face down | Clear PETG |
| back_cover | Outer face down | Off-white |
| panel_ref | Bought: 4.2-inch e-paper panel, 91 × 77 × 1.2 | — |
| (driver board and USB cable, 2 × Ø10 stick-on feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| window_clear | The flange started 0.01 inside the front plate (verify.py: 10.3 mm³ interference with the body) | Defect | Flange starts at the inside of the plate; the plug reaches 0.01 into the flange instead |
| back_cover | With a 0.6 barb, only 0.35 of it reached past the 0.25 gap into the wall (the snap sweep showed 3.9 mm³ for both barbs), a weak catch | Defect | Barb 0.85 (0.6 into the wall, 11.4 mm³ swept); hooks lengthened from 12 to 16 so the strain stays about 0.9 % |
| body | The locating rim ran all round the panel and blocked the flex tail at its bottom edge | Defect | 32 wide gap in the rim's bottom side |
| back_cover | The cable notch had square corners | Violation | Round top (an elongated hole with a semicircular end) |

Dos and Don'ts: one visible chamfer value; two radii (R12 outline, R3 window and inside); equal margins round the window; the window
and the cover meet the body in V lines; no fastener shows; no accent (nothing on a picture frame has a function to point at); the window
is the clear functional part.

Use cases:
- **Place:** stands on its 32 deep bottom with two rubber feet; ground contact 2865 mm² over 98.2 × 31.1. It tips at about 18°, so it
  is for a desk or shelf, not a place where it is knocked.
- **Read:** the view area sits in the window with an even 16 margin; e-paper needs no backlight, so the window is clear.
- **Assemble:** drop the window into the opening from behind, lay the panel on its flange inside the rim with the tail through the gap,
  connect it to the board, tape the board to the cover between the ribs, run the cable through the notch and push the cover in until
  both hooks click (swept: free at 0 and 20 out, 11.4 mm³ of barb being pushed over in between; the ribs stop 0.1 short of the panel and
  catch it at 0.5 further in).
- **Open:** pull the cover out at the cable notch; the 45° barbs let go.
- **Print:** body front face down: the window is cut in the first layers, the rim and walls stand up, the V grooves have 45° faces above
  and below. Cover outer face down: hooks and ribs stand up, barbs are 45° both ways. Window front face down in clear PETG. No supports.

verify.py: all printed parts valid and watertight, one solid each; no interference (the panel included); fit a 256 bed.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): a radio, a record player, a calculator, a loudspeaker and a radio
with a perforated front; none is a picture or display frame. A rounded frame round a rectangular window is a common kind of object;
no product was used as a model.

Safety (electronics): the printed frame is not certified for anything. Power the board from a USB supply from a trustworthy source;
the board is closed in, so do not use a board that gets warm in normal use.

Not verified:
- Not printed on a real printer.
- How firmly the hooks hold and how often they can be opened before they weaken.
- Whether your panel's view area is centred in its outline; most are not quite, and the window may need to move.
