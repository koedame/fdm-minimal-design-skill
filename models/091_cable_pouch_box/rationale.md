# 091 Cable pouch box

A rounded box 120 × 80 × 40 for a travel bag: a charger in one cell, its coiled cables in the other, and a lid that snaps on so nothing
spills when the bag is turned over. The body is 32 high and the lid 8 (4 : 1); four vertical hooks, one in the middle of each of the lid's
walls, run down 0.25 inside the body's walls and their 45° barbs drop into short V grooves. The lid comes off when pulled up at the finger
scoop across the front seam. Two printed parts.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 120 × 80, R12; 40 high | 3 : 2 on the 4 grid; R12 = 15 % of the depth; holds a 35 mm charger cube with the lid on |
| Seam | At 32 of 40: body 32, lid 8 | 4 : 1; the lid as low as 07_hinged_case's so the box reads as one block with one V line |
| Wall, floor, lid top | T (2.52), inner corners R9.48; floor 2.4; lid top 2.4 | One margin, concentric corners; line-width multiples |
| Divider | DIV (1.68) at a third of the inside width, 4 under the rim | Cells 1 : 2: 37.8 for a charger, 75.6 for cables coiled to about Ø60; 4 under the rim as 03_tray |
| Hooks | DIV thick, 16 wide, free length 12 below the seam; outer face 0.25 inside the wall | The 09_wall_unit hook; four, so the lid is located 0.25 on every side by the hooks themselves |
| Barb and groove | Barb 0.85 at 45°, groove barb + 0.25 all round, 16.5 long | Engagement 0.6 (a lid that is handled); strain 1.5 × 1.68 × 0.6 ÷ 12² = 1.05 % |
| Barb height | Centre 21.85 (1 above the hook's tip) | Lowest place on the hook, so the free length is the whole 12 |
| Finger scoop | R6 (0.75 × lid height), 1.2 deep, centred on the front seam | As 07_hinged_case: stays below the lid's top edge |
| Edges | C0.5 on the rim (outside and in: a lead-in for the barbs), the lid's lower edge (one V seam) and the divider's top; C0.6 on both bed faces | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down | Off-white |
| lid | Top face down | Off-white |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| lid | With two hooks at the ends only, the lid was held sideways (along the long walls) by nothing but the ends of the barbs in their grooves: 0.1 mm³ of overlap when pushed 0.4 | Defect | Four hooks, one per wall: the lid now stops at 0.4 in every direction on a hook's face (22.5 mm³) |
| divider | Its top edges were left square | Violation | C0.5 |

Dos and Don'ts: one visible chamfer value (C0.6 only on the bed faces); radii R12 with its concentric R9.48 and the scoop's R6; one margin;
one seam line; plain, with the hooks as the one worked-out spot; off-white, no accent; no fasteners.

Use cases:
- **Pack:** charger in the small cell (up to about 35 × 70 × 34 with the lid on: the hook at that end takes 2 of the cell's width over its
  16), cables coiled in the large one. Press the lid down: the barbs ride over the inner chamfer of the rim and click in.
- **Carry:** turned over in a bag, the contents rest on the lid, which is held by four hooks each catching 0.6. A knock sideways moves it
  0.25 at most, onto a hook.
- **Open:** a fingertip in the scoop lifts the front; the 45° barbs cam the hooks inward and the lid comes off. Put it down top face down.
- **Print:** body bottom down, the grooves' upper flanks at 45°; lid top face down, the hooks standing up with 45° barbs. No supports.

verify.py: both parts valid, watertight; fits a 256 bed; the lid is free closed and 20 up, overlaps only the barbs' engaged tips (22.8 mm³)
while being pulled off (swept as a snap from 1 to 9), stops on the rim when pushed down, and stops at 0.4 sideways in x and y.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): radios, a pocket radio, a calculator and a loudspeaker, none a box with a
lid. A rounded box with a shallow lid is the common form of a small case; no product was used as a model.

Not verified:
- Not printed on a real printer.
- How hard four 0.6 catches are to pull off with one fingertip in the scoop; with 0.35 barbs (0.6 total) it would be lighter.
- Whether the hooks keep their spring in PETG after many openings.
