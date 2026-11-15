# 011 Utensil crock

A square crock that stands by the stove and holds spatulas, ladles and whisks. Water that runs off the utensils drops through
five slots in the floor into five channels under it, which run out through the bottom of two opposite walls, so the floor dries
and air reaches it. It is one part with no mechanism; the drain is the one worked-out detail.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Crock | 104 × 104 × 156 | Height : width = 3 : 2, grid 4; about half the length of a 300 mm utensil |
| Plan radius | R14 | 13.5 % of 104 |
| Inside corner radius | R11.48 | R14 − wall: concentric, so the wall is even all round |
| Wall | 2.52 | 6 lines |
| Floor | 4.8 | 2.4 for the channel under it + 2.4 over the channel |
| Floor fillet | R6 | Nothing lodges in the corner; easy to wipe |
| Floor slots | 5 × 2.4 × 80, pitch 16 | Narrower than a utensil tip; pitch 16 (4 × grid) leaves no point of the floor more than 8 from a slot; 80 stops short of the fillet |
| Channels | 5 × 4 wide, 2.4 high, semicircular top, pitch 16 | Under the slots, open to the bed and out through the ±X walls; the round top is the only ceiling and is 4 wide |
| Rim | C0.5 inside and outside | The one visible chamfer value |
| Bottom edge | C0.6 | Bed side |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| crock | Bottom down, as used | Off-white |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| crock | Three slots 24 apart: water stood on the flat floor between them, up to 12 from a slot | Defect | Five slots 16 apart (no point over 8 from a slot), one channel under each |

Use cases:
- **Place:** stands on its bottom; the contact face is 8366 mm² over 102.9 × 102.9 between the channels (verify.py). Put it where
  the two channel ends can let water out, not against a wall on the ±X sides.
- **Use:** utensils stand head up; a ladle leaning on the rim keeps its weight inside the 104 square footprint.
- **Drain and clean:** water runs through the slots and out of the channel ends; rinse the crock upside down and let it dry on its
  rim. The inside has no undercuts.
- **Print:** bottom down, no support; the channels are open to the bed and their 4 wide round tops are the only ceilings.

verify.py: valid and watertight, fits a 256 bed, ground contact 8366 mm² over 102.9 × 102.9, narrowest patch 12.0.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a container. A square utensil crock is a common
kitchen form; the slot-and-channel drain is not taken from any product, and no product was used as a model.

Safety (food, heat): the crock holds utensils that touch food. An FDM print is not food-safe: the layer lines hold residue and
bacteria that washing does not remove, and most filaments are not certified for food contact. Do not put food in it. Utensils put
in straight from a hot pan can soften PLA (about 55 °C); print it in PETG, keep it away from the hob, and do not put it in a
dishwasher.

Not verified:
- Not printed on a real printer.
- How fast the floor drains and dries in use.
