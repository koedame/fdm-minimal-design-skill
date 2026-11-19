# 016 USB hub case

A case for a bare 4-port USB hub board (72 × 28, four M2 holes in the corners, four USB-A receptacles on the front edge and a
USB-C input at one end). The body is a sleeve with a top, printed top face down, so the four bosses that hang from the top stand up
in the print. Four M2 screws come up through counterbores in the bottom plate, through standoffs and the board's corner holes, into
the bosses: the board is clamped between them and no screw shows from above or the sides.

Boards differ: set `BL`, `BD`, `HOLE_IN`, `PORT_X` and `USBC` in `design.py` to the board you have before printing.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Case | 84 × 40 × 20 | Height = half the depth, grid 4; 84 so the square corners of a 72 board clear the inside corner radius |
| Plan radius | R6 | 15 % of 40 |
| Walls, top, bottom plate | 2.52, 2.4, 2.4 | 6 lines; 12 layers |
| Board position | 3 above the plate, 0.25 behind the front wall | Standoffs under the holes; the receptacles as close to the front as the clearance rule allows |
| Front wall behind the ports | 1.68 (thinned from the inside) | A plug whose moulding is larger than the window must reach the receptacle: its face sits 0.25 + 1.68 = 1.93 behind the outside, inside the 2 mm or so of shell a USB-A plug leaves showing |
| Port windows | 4 × 14.0 × 6.6, R1, pitch 15 | The receptacle (13.2 × 5.8) + 0.4 per side; the pitch is the board's |
| USB-C window | 12 × 6.4 stadium at the −X end | The Connectors rule; the moulding of the plug passes through it |
| Bosses | Ø6 from the top down to 0.05 over the board, pilot Ø1.8 | The Hidden screws rule (M2); the screw closes the 0.05 when tightened |
| Standoffs and counterbores | Ø6 × 3, clearance Ø2.4, counterbore Ø4.2 × 1.8 | M2 × 12 pan head: 2.4 plate + 3 standoff + 1.6 board, about 6 into the boss |
| Plate | 0.25 clearance all round, C0.5 on the body's bottom edges | The seam is one V line round the bottom |
| Rubber feet | 4 × Ø10.2 at (±20, ±10) | Clear of the counterbores |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Top face down | Off-white |
| bottom_plate | Outer face down | Off-white |
| hub_board_ref | Bought part, not printed | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| body | At 80 long the front corners of the board ran into the inside corner radius (verify.py: 0.04 mm³ overlap) | Defect | 84 long |
| body | The receptacles sat 3 behind the outside face; a plug whose moulding is larger than the 14 × 6.6 window could not go fully in | Defect | Board 0.25 behind the wall, and the wall thinned to 1.68 behind the ports (1.93 recess) |

Use cases:
- **Assemble:** lay the board on the standoffs, put the body over it, turn it over and drive four M2 × 12 screws up through the plate
  and the board into the bosses.
- **Plug in:** USB-A plugs go in through the front windows; the webs between the windows are 1.0 wide (the board's 15 pitch), so do
  not lever a plug sideways. The input cable enters at the −X end.
- **Place:** stands on four rubber feet; the screws are underneath.
- **Print:** body top face down: the bosses stand up and the window tops are 14 long bridges. Plate outer face down: the counterbores
  open on the bed, and the 0.9 wide shoulder inside each is a small ring of bridging.

verify.py: both printed parts valid and watertight, no interference (the board included), fit a 256 bed, ground contact 2522 mm²
over 83.1 × 39.1.

Compared with well-known products in this style: none of them is a USB hub. A plain rounded box with port windows
is a generic electronics case; no product was used as a model.

Safety (electronics): the printed case is not certified for anything. Use a hub board from a trustworthy source with its own
protection; a hub with four loaded ports gets warm, and the case has no vents, so do not run it at its limit for long, and do not
cover it.

Not verified:
- Not printed on a real printer.
- Whether a real board's receptacles line up with the windows (measure yours).
- Whether the 1.0 webs between the windows survive repeated plugging.
