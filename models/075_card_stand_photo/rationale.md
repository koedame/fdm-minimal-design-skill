# 075 Photo and card stand

A 64 × 48 × 24 block whose side profile is a ramp with one slot leaning back at 1 : 3. One part, printed on its side, so the profile, the
design of this object, is drawn in the layer plane and comes out crisp. The slot runs parallel to the sloped front, 2 wide: a photo, a
postcard or a card up to about 1.5 thick stands in it leaning back 18.4°, its bottom edge on a floor square to the slope. The 4 thick
lamella in front of the slot ends in a full round level with the flat top behind the slot.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Block | 64 × 48 × 24 | 16 × 12 × 6 modules (8 : 6 : 3) |
| Lean | 1 : 3 (18.4°), front face and slot parallel | A 127 tall photo stands with its centre of gravity 4.9 in front of the block's middle, well inside the 48 base |
| Slot | 2 wide, its floor square to the slope, lowest corner 8 above the table, 16.9 deep along the back face | Up to about 1.5 thick; the floor at a third of the height keeps the base solid |
| Lamella | 4 thick, ends in a full round R2 level with the top (24) | A plate end floating in the air: nearly full round (thickness / 2) |
| Back top corner | R8 | The outline radius of the profile (a third of the height) |
| Long edges | C0.5 on the toe, the heel and the slot's mouth | One visible chamfer value; the mouth's chamfer is a lead-in |
| Profile faces | C0.5; C0.6 on the bed face | The bed face takes the elephant's foot |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| stand | Side down (profile on the bed) | Off-white |

## Review

No defects or violations found. Checked with a 0.3 thick 89 × 127 photo standing in the slot (`photo()` in `design.py`, not a part): no
overlap with the stand, its top at 128.6, its centre of gravity at y 4.9 (the block spans ±24); a 1.5 thick card in a sleeve fits too.

Dos and Don'ts: one visible chamfer value (C0.6 only on the bed face); two radii (R8 corner, R2 lamella end); the ground face is flat with
chamfers only; the slot's floor and faces follow one slope; no accent (nothing has a function to point at).

Use cases:
- **Place:** stands on its flat 48 deep bottom (ground contact 2961 mm² over 63 × 47.1); felt pads can go anywhere underneath.
- **Put a photo in:** drop it into the slot; it slides down the back face to the floor and leans back on the mouth's edge.
- **Take it out:** lift it by its top; nothing holds it but its weight.
- **Hold:** the rounded lamella end and the R8 corner are the edges the hand meets.
- **Print:** on its side with the profile on the bed: the slot runs through the 64 print height, the lamella is a 4 wall, no overhangs.

verify.py: valid and watertight, one solid; fits a 256 bed; ground contact 2961 mm².

Compared with well-known products in this style: none is a card or photo stand. A block with a leaning slot is the common
form of a card stand; no product was used as a model.

Not verified:
- Not printed on a real printer.
- Whether thin or curled photo paper stays upright at 18.4° without bowing.
