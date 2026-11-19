# 041 Under-desk cable tray

A tray 200 long that hangs under a desk top and takes the loose cables, adapters and chargers behind a desk. Its section is the
design: a 64 high back, a 48 floor and a front that leans out at 45°, so a cable dropped from above or pushed in from the front stays
in, and the front reads as one 45° plane in which the front wall's top and the end walls' front edges lie. It hangs on two short C
rails screwed to the underside of the desk. Each end wall carries a hook arm along its top that slides into a rail and sits on the
rail's ledge; a V rib under the arm drops into a V notch in the ledge, so the tray has to be lifted before it slides out. The rail
screws sit above the arms, hidden from below.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Tray | 200 long, 80 deep, 64 high | 200 fits a 256 bed with the arms; 80 deep = 48 floor + 32 front rise |
| Section | Back 64, floor 48, front rising 32 at 45° | Floor : back = 3 : 4, grid 4; 45° so the front holds what falls in and prints without support on the tray's back |
| Front plane | The front wall's top and the end walls' front edges in one 45° plane, square to the front wall | One plane instead of three edges; the front wall ends square to itself |
| Section corners | R12 outside, R9.48 inside | 15 % of the 80 depth; the inside corner is the outside one less the wall |
| Walls | 2.52 | Line width × 6 throughout |
| Rim | 6 below the desk | Headroom 2 + flange 4; the arm is flush with the rim |
| Hook arm | 8 reach, 4 thick, 48 long (the flat top of the end wall) | 4 = the rail's plate thickness; 48 hides the rail from below |
| Rail | C section 12 wide × 14 high, 48 long; flange, web and ledge 4 | One plate thickness; 0.5 side play to the arm and to the end wall |
| Ledge | Only the middle 30 of the rail | The screws beyond its ends can be driven straight up; 30 keeps the tray's centre of gravity over the ledge |
| Headroom | 2 over the arm | Lets the 1.5 rib lift out of the notch; limits a forward tilt to 2.9° |
| Rib / notch | 1.5 high 45° V under the arm, notch 1.75 deep (rib + 0.25 normal to its flanks) | Locates the tray along the rail; 45° prints both ways |
| Rail screws | 4 mm countersunk, Ø4.5 teardrop hole, 90° countersink to Ø9, 38 apart | Heads flush with the flange underside, out of the arm's way |
| Edges | C0.5, C0.6 on the tray's back (bed) | One chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| tray | On its back | Off-white |
| rail_left, rail_right | Outer face (the web) down | Off-white |
| (4 × 4 mm countersunk wood screws) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| rail | The ledge stopped 0.6 short of the web and was a separate solid: it would print loose (found by the new loose-piece check in `verify.py`) | Defect | The ledge reaches 0.6 into the web |
| rail | The ledge ran only from 14 to 34 behind the back face, but the tray's centre of gravity is about 26–30 behind it (more with a power strip at the front): the tray could tip forward until the arm's back met the flange (4 headroom, about 7°) | Defect | Ledge 10 to 40, headroom 2: the centre of gravity stays over the ledge and a tilt is limited to 2.9° |
| rail | Pan-head screws would stand 3 below the flange, into the arm's headroom | Defect | Countersunk screws, heads flush; the holes are teardrops for the print on the web |

Use cases:
- **Mount:** hold the tray with both rails on its arms against the underside of the desk and draw round the rails; take the rails off
  and screw them inside the marks (two screws each, driven straight up past the ends of the ledge). Slide the tray's arms in from the
  front, lifted 2, and let it drop: the ribs fall into the notches (swept: free lifting to 1.9, stops at 2.5 against the flange, held
  0.3 down by the ledge, 1 forward and back by the notch, 0.8 sideways by the webs).
- **Fill:** drop cables in from above behind the desk or push them in over the 45° front.
- **Take down:** lift the tray 2 and pull it forward.
- **Print:** tray on its back (every wall stands up or leans at 45°, the arms are prisms standing up, the ribs are 45° V's); rails on
  the web, flange and ledge standing up. No supports.

verify.py: all parts valid and watertight, one solid each, no interference, fit a 256 bed.

Compared with well-known products in this style: radios, a pocket radio, a calculator and a loudspeaker; none is a
tray or hangs under a desk. Under-desk cable trays are a common kind of object; no product was used as a model.

Safety (electricity, heat, load): a power strip or adapters in the tray stay warm; leave room around them, print in PETG, and do not
cover the tray. The printed parts are not certified for anything. The tray's strength has not been calculated or tested: keep it to
cables, a power strip and small adapters, drive the rail screws into solid wood or a solid board (not a glass, metal, hollow-core or
thin-panel top), and pull down on the filled tray by hand before you leave it.

Not verified:
- Not printed on a real printer.
- The load the arms and ledges take; keep it to cables, a power strip and small adapters (about 1 kg).
- The centre of gravity is estimated from the section, not weighed.
- Whether the rails can be placed accurately enough by drawing round them; 0.5 side play is the margin.
