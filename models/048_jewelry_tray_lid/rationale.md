# 048 Jewelry tray with lid

A 120 × 80 tray, 24 high, under a dark 8 high lid. Inside, the layout of 03_tray at a smaller scale: a column on the left a third of
the width, and two equal cells on the right. The column is for rings: nine rounded ridges with 3 wide gaps between them, the first and
last gap against the walls, so ten rings stand in a row facing the front. The cells take earrings, a watch or a bracelet. The tray
floats on the same 45° shadow line as 03_tray. The lid's outside is flush with the tray's; inside, its wall continues below the rim as
a lip that drops 4 inside the tray's wall, so the lid finds its place and cannot slide off.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Tray | 120 × 80 × 24, R10 | 3 : 2; R10 = 12.5 % of the depth |
| Lid | 8 high, top 2.4 | Tray : lid = 3 : 1 |
| Walls / floor | 2.52 / 2.4 | Line width × 6; 12 layers |
| Layout | Ring column = (inner width − 1.68) / 3; two equal cells to the right | 03_tray's proportions |
| Dividers | 1.68, tops 2 under the lid's lip | DIV; the lip passes over them |
| Ring ridges | 5 wide, 12 high, round tops; gaps 3.0 (exactly 74.96 / 10 after the nine ridges) | A ring's band (1.5–2.5) goes into a gap, its head stands above the round tops |
| Lip | 1.68 thick, 4 deep, 0.25 inside the tray's wall | The location rule; the lid's wall is 2.52 + 0.25 + 1.68 thick down to the rim, so the lip is part of it, not a band hanging free |
| Shadow line | 2.4 plinth, 1.2 inset at 45° | As 03_tray |
| Corners inside | R7.48 (outer radius − wall) at the walls, R3 at the dividers and the floor | Two inner radii, as 03_tray |
| Rubber feet | 4 × Ø10.2 at ±44, ±24 | On the plinth |
| Edges | C0.5; C0.4 on divider tops; C0.6 on bed faces | As 03_tray |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| tray | Bottom down | Off-white |
| lid | Top down | Dark grey |
| (4 × Ø10 rubber feet; optional felt for the cells) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| tray | The divider tops were square while every other edge is chamfered | Violation | C0.4 prisms along the divider tops, as in 03_tray |

Use cases:
- **Store:** push rings into the gaps, head up; lay earrings and a watch in the cells.
- **Close:** set the lid on: the lip finds the tray's wall (swept: lifts freely, stops 0.3 down on the rim, 0.4 sideways).
- **Open:** pinch the lid's sides (8 high) and lift.
- **Print:** tray bottom down (ridges stand along their length with round tops, the shadow line is 45°); lid top down, the lip
  standing up as the continuation of the wall. No supports.

verify.py: all parts valid and watertight, one solid each, no interference, fit a 256 bed.

Compared with well-known products in this style: radios, a calculator and a loudspeaker; none is a tray or a box with
compartments. Jewelry boxes with ring slots are a common kind of object; no product was used as a model.

Not verified:
- Not printed on a real printer.
- Wide rings (bands over 3) do not fit the gaps; change `RIDGE` for them.
- How firmly the ridges hold thin rings: they stand in the gaps by their own weight.
