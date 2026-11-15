# 069 Cable weight block

A block for the desk, 96 × 48 × 36, that keeps the ends of charging cables where the hand finds them. A cable pushed down into one of
the three seats across the top snaps past a narrow neck and stays there when the device end is unplugged, instead of sliding off the desk
under the weight of the part that hangs over the edge. The weight comes from coins: the body has two wells for stacks of coins up to
26.5 across, and a solid cap, located by a lip, lifts straight off to fill them. Body and cap meet on one V line 24 up.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 96 × 48, R12; body 24 + cap 12 = 36 | 24 × 12 × 9 modules; body : cap = 2 : 1; R12 is 12.5 % of the width |
| Coin wells | 2 × Ø27 (coins ≤ Ø26.5 + 0.25 round), 21.6 deep, C0.5 rims, at x ±24 | Centred in the two 48 × 48 halves: 10.5 from the outline on every side. 12 coins of 1.8 per well |
| Weight | About 210 g: 24 coins of about 7 g (168 g) and the printed block at 15 % infill | Holds cables that hang over the edge (tens of grams); not a plug puller: unplugging USB-C takes 8–20 N (rules, Connectors) |
| Cable seats | 3 × Ø4.4 at pitch 16, centres 3.4 under the top; 3.2 neck, C0.5 lead-in; 45° roof downward | Cables of about 3.6–4.4 squeeze 0.4–1.2 through the neck and snap into the seat; the roof points up in the print |
| Lip | 1.68 (DIV) wide, 3 high, 0.25 inside the cap's skirt | Location clearance; the cap drops 3 over it |
| Cap | Solid 8.75 above a 3.25 skirt of T | Deep enough for the seats; a solid slab adds weight |
| Rubber feet | 4 × Ø10.2 × 1 recesses at x ±40, y ±16 | On the 4 mm grid, clear of the wells, inside the bed chamfer |
| Edges | C0.5; C0.6 on bed faces | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down | Off-white |
| cap | Top down | Off-white |
| coins_ref ×2 | Bought: stack of 12 coins, Ø26.5 × 21.5 | — |
| cables_ref ×3 | Bought: cable, Ø4 | — |
| (4 × Ø10 stick-on rubber feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| cap | The necks were built as a rectangle moved after it was drawn, which left them closed: the seats were holes through the cap with no way in from the top | Defect | Necks drawn in place as polylines up through the top; checked in a section at y 0 |
| body | The feet recesses at x ±36, y ±12 lay under the wells and thinned the floor under the coins to 1.4 | Defect | Feet moved to x ±40, y ±16, clear of the wells |
| summary | It said the block held a cable while the plug was pulled out of the device; 210 g gives about 2 N against 8–20 N | Defect | The claim now says what the weight does: keeps hanging cables from sliding off the desk |

Dos and Don'ts: one visible chamfer value; one plan radius (R12 and its concentric insides) plus the wells' circles; equal margins round
the wells; no fasteners; no accent (the cables are the colour).

Use cases:
- **Fill:** lift the cap off, drop stacks of coins into the wells, set the cap on: it drops 3 over the lip and stays square (swept: free
  upward 0–20, stops 0.3 down and 0.4 sideways, free at 0.2). The coins (stacks Ø26.5 × 21.5) clear the cap.
- **Hold a cable:** press the cable down into a seat; it snaps past the neck into the Ø4.4 seat (the cables lie in the seats without
  touching the cap at Ø4).
- **Take it out:** pull the cable up through the neck.
- **Place:** stands on 4005 mm² (94.9 × 46.9).
- **Print:** body bottom down; the wells open upward, the lip stands on the top. Cap top down: the seats run along the bed with their
  45° roofs pointing up and the skirt open upward. No supports.

verify.py: both printed parts valid, watertight, one solid each; no interference with the coins or the cables; motions as above.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a cable holder; they are housings with controls and
grilles. Weighted cable holders for the desk are a common kind of object; no product was used as a model.

Safety: no batteries, LEDs, magnets, heat or food. Coins are small parts: keep the filled block away from small children, who could open
the cap. The block is not heavy enough to stop a cable from being pulled hard; do not use it to anchor anything that must not fall.

Not verified:
- Not printed on a real printer.
- How hard a cable snaps into the seat on your printer: the neck does not flex, the cable jacket is squeezed. Change `NECK` and `CABLE_D` for your cables.
- The coin sizes: check `COIN_D` against your coins (the wells take 26.5; smaller coins rattle a little).
