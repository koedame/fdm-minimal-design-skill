# 028 Self-watering planter

A Ø96 × 120 cylinder (4 : 5) in two parts: a reservoir 48 high and a pot that hangs in it, 72 of it showing (2 : 3). The pot's lower
part is a spigot that drops inside the reservoir wall with 0.25 clearance and steps out on a 45° cone; the cone sits on a 45° chamfer
inside the reservoir rim, so the pot hangs centred with its floor 36 up, over the water. Outside, the two parts read as one cylinder
broken by a V seam, the reservoir dark like a saucer. A slotted tube stands in the middle of the reservoir and rises through a hole in
the pot floor: soil packed into it is the wick that draws the water up. Water goes in through a tube in the pot that runs down through
its floor; an overflow hole 4 under the pot floor keeps the water out of the soil.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Planter | Ø96 × 120 | Width : height = 4 : 5; grid 4 |
| Reservoir | 48 high | Reservoir : visible pot = 2 : 3 |
| Plinth | stepped in 1.2 at 45°, 2.4 high | As 03_tray: the shadow line |
| Spigot | outside Ø90.46 (the reservoir's inside less 0.25 per side), wall 2.52, 11 into the reservoir | The Location lip. It is the pot's own wall and carries the wet soil, so it keeps the full wall instead of a DIV lip; the wall runs through the cone at the same width |
| Seat | 45° cone on the pot over a 45° C0.8 chamfer inside the reservoir rim | Prints upright without support on both parts, and centres the pot as it is lowered; the cone rests on the chamfer, not on the rim, so the outside seam stays an open V |
| Pot floor | 36 up, 2.4 thick | Above the overflow; no drain holes, so the soil stays out of the water |
| Overflow | Ø4 teardrop, centre 32 | The water stops 4 under the pot floor (about 180 ml) |
| Wick tube | Ø24, wall 1.68, through a Ø25 hole in the pot floor; eight slots 1.2 × 16 from the reservoir floor up | Packed with the potting soil, it wicks from the bottom of the water up; 1.2 slots let the water in and keep most of the soil in. The hole is 0.5 clear per side so the spigot, not the tube, locates the pot |
| Fill tube | Ø16, wall 1.68, top 4 under the rim, fused to the pot wall | A watering-can spout fits its Ø12.6 bore; it ends at the pot floor, over the water, and shows the level when you look down it |
| Chamfers | C0.5 on the rims and the seam, C0.6 on the bed edges | One visible value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| pot | Bottom down, as used | Off-white |
| reservoir | Bottom down, as used | Dark grey |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| reservoir | The wick slots started 2 above the reservoir floor, so the last 2 of water (about 13 ml) could not reach the soil in the tube | Defect | Slots run from the reservoir floor up |
| model.json | `based_on` named two models instead of skill samples (tools/models.py check caught it) | Violation (models/README.md) | 03_tray and 04_cylinder_speaker |

Use cases:
- **Plant:** lift the pot out, pack soil into the wick tube through the hole in the pot floor, put the pot back, then fill the pot and
  plant. The pot lifts straight out (swept: free up to 40, stops 0.3 down on the seat and 0.4 sideways).
- **Water:** pour into the fill tube; water running out of the overflow at the back means the reservoir is full, so keep the planter on
  a tray. Water the soil from above only for the first days, until the wick is wet through.
- **Lift, move:** grip the reservoir, not the pot rim; the pot only rests on its seat.
- **Clean:** the two parts come apart; the reservoir has no corners inside.
- **Print:** both bottom down, no supports; the pot's cone and the overflow's roof are 45°.

verify.py: both parts valid and watertight, no interference, fit a 256 bed; ground contact 6713 mm² on the Ø92.5 plinth.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): they are radios, a pocket radio and a calculator; none is a planter.
Self-watering planters with a wick and a reservoir are common; no product was used as a model.

Safety (water, food): print in PETG, not PLA (PLA softens and breaks down when wet for months). Printed parts are not certified for food
contact; if you grow herbs to eat, treat the planter as a plant pot, not a food container. Standing water breeds algae and mosquitoes:
empty and rinse the reservoir now and then.

Not verified:
- Not printed on a real printer.
- Whether the parts hold water: FDM walls can seep; print the reservoir with at least three walls and solid bottom layers, or seal it.
- How well the soil wicks through the tube, and how long the 180 ml lasts (depends on the plant and the soil).
