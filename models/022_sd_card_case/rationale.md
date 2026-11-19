# 022 SD card case

A 44 × 44 × 36 case for eight SD cards: a low body (12) and a lid (24). The body's wall steps in at the top into a neck that the lid
slides over, and two cantilever tabs are freed from the front and back of that neck by U-shaped slits. A 45° bump on each tab drops
into a 45° groove inside the lid wall, so the lid clicks shut and pulls off without a button; tabs and grooves are hidden inside the
closed case, and the outside is two plain blocks on one V line. The cards stand on their long edge in a slotted block, their tops 8.6
above the neck, so each can be picked out by its edge.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Plan | 44 × 44, R6 | Grid 4; the neck inside (35.1) clears eight cards across and a card's 32 length; R = 13.6 % |
| Height | 36 = body 12 + lid 24 | Body : lid = 1 : 2; the lid covers the cards with 1.0 to spare |
| Wall | 2.52 body and lid, 2.4 floor and lid top | 6 lines; 12 layers |
| Neck | 38.46 outside, 1.68 wall, 12 high, 45° step inside | The lid's inside less 0.25 per side; `DIV`; tall enough for a tab that flexes the 0.85 bump within 2 % strain |
| Slots | 8 × 2.6 at pitch 4.28, 8 deep, C0.5 lead-in | SD card 2.1 + 0.25 per side; the ribs are `DIV`; the lead-in is the one chamfer value |
| Card tops | 1.0 under the lid top, 8.6 above the neck | Picked by the edge when the lid is off |
| Tabs | 12 wide, 11.5 long, 1.68 thick, slits 1.0 | Bending strain for the 0.85 bump: 1.5 × 1.68 × 0.85 / 11.5² = 1.6 %, under the about 2 % PLA takes repeatedly |
| Bump / groove | 0.85 / 0.95 deep, 45° both flanks, bump centre 1.5 under the tab top | Catch = bump − clearance = 0.6, for a lid that is handled; the groove is 0.35 deeper than the bump reaches and leaves 1.57 of lid wall. Pushes over both ways (the lid pulls off); the groove is a 45° V, so the lid prints top down without support |
| Seam | C0.5 on both edges | One V line at 1 : 2 |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down, as used | Off-white |
| lid | Top face down | Off-white |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| body | The U-slits were cut 3.4 wide across the neck wall and nicked the end of the card block | Defect | Cut them only through the wall (1.88 wide), the block stays whole |
| body, lid | The bumps were 0.4: across the 0.25 clearance between the neck and the lid they caught the grooves by 0.15 (0.47 mm³ swept for both), too little to feel the lid close | Defect | Bump 0.85 (catch 0.6, 8.35 mm³ swept), groove 0.95 deep, and the neck 12 high so the 11.5 tab keeps the strain at 1.6 % |

Use cases:
- **Open, close:** pull the lid straight up; the tabs flex inward 0.6 as the bumps leave the grooves (swept below). The card block
  reaches only 4.1 up the tabs, where they bend about 0.13 into its 0.47 margin; above it the outermost card is 1.5 from a tab,
  which bends at most about 0.75 at its free end.
- **Remove, fit a card:** the cards stand 8.6 above the neck; the C0.5 lead-ins guide a card into its slot.
- **Hold:** the case is pocket-sized; every vertical edge is R6 and the horizontal edges C0.5.
- **Print:** body bottom down (the neck, tabs and slots stand up; the step is a 45° cone), lid top face down; the grooves are 45° Vs.

verify.py: both parts valid and watertight, no interference, fit a 256 bed; ground contact 1811 mm² over 42.9 × 42.9.
Motions: the lid lifts with the bumps pushed over the lid wall at 1–10 mm (8.35 mm³, under 10), is free at 11.5–14 mm, stops on the
shoulder (0.3 down) and is located sideways by the neck (free at 0.2, stopped at 0.4).

Compared with well-known products in this style: they are radios, a pocket radio and a calculator; none is a small
storage case. Card cases with a lift-off lid are common; no product was used as a model.

Not verified:
- Not printed on a real printer.
- How firmly the tabs hold and how much force pulls the lid off (settle with a test piece of the neck and one lid wall).
- Whether the 2.6 slots hold the cards without rattling on your printer (a 0.1 change in slot width matters).
