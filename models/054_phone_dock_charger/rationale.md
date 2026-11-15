# 054 Phone charging dock

A 64 × 64 × 40 block on a floating plinth that holds a phone leaning back on the end of an ordinary USB-C cable. The phone slot runs
across the whole width and leans back at 1 : 4, its floor square to the slope. Under the floor, on the line of the phone's port, a
stadium pocket holds the plug's moulding with the metal tip standing 6.6 out of the floor; the moulding seats on two shoulders at the
bottom of the pocket. A slit, narrower than the moulding, runs from the pocket back and down to the bottom face and out through the
back: the cable is laid into it from underneath and the plug pulled down into the pocket. The slit is the one worked-out spot; from
the front the dock is a plain block with a groove.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 64 × 64 × 40, R8 | 16 × 16 × 10 modules; R = 12.5 %; the height leaves room for the 12 slot, the 12 pocket and a cable bend below |
| Plinth | 2.4 high, 1.2 inset, 45° | The floating plinth |
| Slot | 12 wide at the mouth (11.6 square to the slope), 12 deep at the front line, through the width | A phone up to about 11 thick; through the width so any phone width fits |
| Lean | 1 : 4 (14°) | Reading angle; the slot's front face overhangs 14° in the print |
| Front wall | 16 at the top | A quarter of the depth; the slot sits in the front half so the leaning phone's weight falls over the block |
| Plug axis | 5.0 in front of the slot's back face, centred in x | Half of an 8 mm phone + 1 for a thin case: the port of a phone leaning on the back face |
| Pocket | Stadium 12.4 × 6.8, 12 deep along the slope | A common 12 × 6.4 plug moulding + 0.2 per side; holds 12 of it; the tip stands 6.6 out of the floor |
| Slit | 6.4 wide, from the pocket's front to the back face, up to 20 with a 45° roof | Narrower than the moulding (two 3 shoulders carry the plug); the roof's apex stays 2 under the slot floor; 14.7 of height for the cable to bend |
| Feet | Four Ø10.2 × 1 recesses at (±22, ±22) | Clear of the slit by 13 |
| Edges | C0.5, C0.6 at the bed | One visible chamfer value: the rim, the slot's ends and the slit's edges at the back |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| dock | Bottom down | Off-white |
| usb_c_plug_ref (the plug of a USB-C cable, moulding about 12 × 6.4) | Bought | Dark |
| (4 × Ø10 × 1 rubber feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| dock | The slit's 45° roof reached 25.2, 0.02 above the back corner of the slot floor: a sliver of a hole in the floor | Defect | Slit ceiling lowered to 20; the apex stays 2 below the floor |
| dock | The slit's edges in the back face had no chamfer while every other visible edge had C0.5 | Violation | C0.5 on the slit's edges in the back face |
| dock (use) | Lifting the phone pulls the plug: a USB-C plug takes roughly 8–20 N to unplug, several times the weight of the dock (about 177 g at 100 % infill in PLA), so the plug and the dock come up with the phone | Defect | Not fixable by the shape alone: the plug is glued into the pocket (written in the use cases), and the phone is lifted with the other hand on the dock. Written as a limit, not hidden |

Dos and Don'ts: one visible chamfer; two radii (R8 outline, R6.8 plinth = R8 − inset, plus the stadium ends of the pocket that do not
show); no fasteners; no accent (the plug tip is the function and is dark already).

Use cases:
- **Fit the cable:** lay the cable into the slit from underneath, with the plug end out of the slot above; pull the cable from the back
  until the moulding drops into the pocket and stands on the shoulders. Glue it there with a drop of hot glue or a strip of
  double-sided tape round the moulding: the pocket only stops the plug going down.
- **Dock the phone:** put the phone's port over the tip and lower it along the slope; the phone ends leaning on the back face. A
  72 × 150 × 8 envelope stands in the slot with no overlap with the dock (it overlaps only the tip, which is in its port) and leaves
  along the slope freely (checked at 20 mm).
- **Undock:** hold the dock with one hand and lift the phone with the other (see the review).
- **Place:** the plinth stands flat (2981 mm² of contact); the phone's centre of gravity, 75 up the slope, is about 18 behind the slot,
  well inside the 64 square.
- **Print:** bottom down, no supports. The slot's front face overhangs 14°; the pocket leans 14°; the slit is open at the bottom and
  back and has a 45° roof.

verify.py: valid, watertight, one solid; no interference with the plug.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a dock; the block with a groove shares only the
general language. Phone docks with a cable led through the base are a common kind of object; no product was used as a model.

Safety (electrical): the dock carries no electronics; it holds the plug of a cable. Use a certified cable and charger. Do not use a
cable whose moulding or wire is damaged, and keep the slit free so the cable is not pinched under the dock.

Not verified:
- Not printed on a real printer.
- The plug's moulding and the phone's port position differ between cables, phones and cases: measure them and change `POCKET` and
  `PORT_OFF` before printing.
- Whether a phone case's bottom opening admits the moulding's top; with a thick case the tip may not reach far enough into the port.
