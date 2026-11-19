# 013 Square planter on a saucer

A 96 mm cube in two parts for a small house plant: a square pot standing in a 16 mm high saucer. The pot is the saucer's outline
less a wall and a clearance all round, so it drops inside the saucer rim, which locates it. It stands on four posts 8 mm above the
saucer floor, so the water that drains through its floor collects under it instead of standing in the soil.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Overall | 96 × 96 × 96 | A cube: total height = width, grid 4 |
| Saucer | 96 × 96 × 16, R12 | R = 12.5 % of 96; 16 = 1/6 of the height |
| Pot | 90.46 × 90.46 × 85.6, R9.23 | Saucer less one wall and 0.25 clearance per side (the Location rule); corners concentric with the saucer |
| Pot in the saucer | 5.6 | Saucer rim 16 − floor 2.4 − posts 8: enough to locate it |
| Walls and floors | 2.52 walls, 2.4 floors | 6 lines; 12 layers at 0.2 |
| Posts | 4 × Ø8 × 8 at ±36 | Under the outer ring of the pot floor, clear of the holes; about 65 ml of water fits under the pot |
| Drain holes | 49 × Ø4, 7 × 7 at pitch 8 | Small and dense; out to ±24 so no corner of the floor is far from a hole |
| Pot floor fillet | R6 | The soil leaves the corner when the plant is repotted |
| Edges | C0.5 rims, C0.6 on the bed side | As every part |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| pot | Bottom down, as used | Off-white |
| saucer | Bottom down, as used | Dark grey |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| pot | 25 drain holes in the middle 36 mm: water stood on the outer ring of the floor, up to 29 from a hole | Defect | 49 holes out to ±24; the posts moved out to ±36 to clear them |

Use cases:
- **Plant:** lay a piece of mesh or a pot shard over the holes, then the soil; Ø4 holes would let loose soil through.
- **Water:** about 65 ml collects under the pot before it touches the pot floor; empty the saucer if it fills higher.
- **Remove:** lift the pot by its rim; the 0.25 clearance lets it out without catching.
- **Print:** both parts bottom down, no support; the posts stand vertically.

verify.py: both parts valid and watertight, no interference, fit a 256 bed, ground contact 8884 mm² over 94.9 × 94.9.

Compared with well-known products in this style: none of them is a planter. A square pot in a saucer is a generic
form; no product was used as a model.

Not verified:
- Not printed on a real printer.
- Whether the printed saucer holds water without seeping. An FDM print is not reliably watertight; print the saucer in PETG with
  at least 3 walls and solid bottom layers, and check it with water on a towel before putting it on furniture.
