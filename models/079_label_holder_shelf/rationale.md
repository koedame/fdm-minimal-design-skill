# 079 Shelf label holder

A label holder 64 long and 28 high that clips onto the front edge of an 18 shelf board. The body is one constant profile: a C that takes
the board's edge, with a 45° ridge on the lower flange that clamps the board, and in front of the edge a block carrying a paper label in a
0.5 slot that runs the whole length, so a 60 × 16 label slides in from either end and can be changed with the holder in place. A clear
cover in front of the label is held by four vertical hooks, as 074_led_strip_channel: they run back in two slots above and below the
label, and their 45° barbs drop into V grooves along the whole length, so the cover snaps on from the front or slides on from an end.
The top of the holder is one line with the top of its flange on the shelf.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Length × height | 64 × 28 | 16 × 7 modules; a 60 label with 2 at each end |
| Board | 18 | The most common shelf board thickness; the only dimension to change for another board |
| Flanges | 2.52 (T), reaching 12 over and under the board | Long enough to flex; the top flange is the top of the holder |
| Clamping ridge | 0.4 high, 45° flanks, 10 from the edge, on the lower flange | The flange flexes 0.4 over the board: strain 1.5 × 2.52 × 0.4 / 10² = 1.5 % |
| Front depth | 12.52 in front of the edge (T + 10 inside) | The hooks' free length (8) and the cover |
| Cover | 1.68 (DIV) clear plate between the walls, 0.25 clearance, front face flush | The seam is a V line with C0.5 on the wall and C0.6 on the cover's bed face |
| Hooks | 4, 12 wide, at x ±16, 1.68 thick, 8 long from the cover | As 074: 0.6 barbs, 45° both sides |
| Barb engagement | 0.35 (barb 0.6 − 0.25 clearance) | Strain about 1.1 % to pass; enough for a cover of about 3 g, and it comes off when pulled |
| Hook slots | Hook + 0.25 clearance + 0.85 to flex | Room for the barb to pass |
| V grooves | Barb + 0.25 all round, 45°, the whole length | The cover also slides along them, and the profile stays constant for the print |
| Label slot | 0.5 deep, 17.4 high between the slots | Paper or thin card, 60 × 16 |
| Edges | C0.5; C0.6 on the bed faces | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | On its end, the profile down | Off-white |
| cover | Front face down | Clear |
| label_ref | Paper, 60 × 16 | — |

## Review

No defects or violations found. Checked in particular: the hooks' barbs sit in the grooves with no overlap; pulling the cover off the front
overlaps only the barbs' engaged tips (5.5 mm³, swept as a snap from 1 to 4), it is free at 13 and stops when pushed 1.0 into the block;
the cover and the label both slide the whole length (swept along x: free); the label clears the cover and the block.

Dos and Don'ts: one visible chamfer value; no radii (an extruded profile, square in plan so holders butt into a row); no fasteners; plain
off-white with the clear cover, no accent; the seam round the cover is one intended V line.

Use cases:
- **Hang:** push the holder onto the board's edge from the front; the ridge's 45° flank rides under the edge and the lower flange flexes
  0.4. Slide it along the edge to where it is wanted.
- **Change the label:** push the old label out from one end with the new one, or with a fingernail; the cover stays on.
- **Remove the cover:** slide it out from an end along the grooves, or pull it at the seam.
- **Bump:** a knock from the front pushes the holder against the board; a knock from below is taken by the clamp. A row of holders butts
  end to end.
- **Print:** body on its end, the profile on the bed: a constant section with no overhangs; the flanges bend within the layers, not across
  them. Cover front face down: the hooks stand up and their barbs have 45° faces. No supports.

verify.py: both printed parts valid, watertight, one solid each; no interference with the label.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none is a label holder or a clip. Clip-on shelf label holders are a
common kind of object; no product was used as a model.

Not verified:
- Not printed on a real printer.
- The clamp on real boards: melamine boards with edge banding, rounded edges and boards of 17 or 19.
- Whether a 0.35 catch keeps the cover on through cleaning.
