# 083 Charger cord wrap

A flat bobbin, 96 × 48 × 16, for winding up the cord of a charger so it lies flat in a bag. Two flanges with the outline's R12 sit on a
stadium core whose ends have the same R12, leaving 12 of winding room all round. One piece would not print: the upper flange would
overhang the core by 12. So the winder is two halves, split under the upper flange. The base carries the hollow core; the cap's flange
carries a plug that goes down inside it. Two cantilever tabs freed from the plug's long sides by U-shaped slits click their 45° bumps into
grooves inside the core. The joint is hidden inside, and the halves pull apart without tools. The cord starts through a slot in the base
flange, is wound round the core, and its end is pinched in a slot in the cap flange at the other end.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Flanges | 96 × 48 (2 : 1), R12, 2.4 thick | Grid 4; R12 = 12.5 % of 96; 2.4 = 12 layers |
| Core | Stadium 72 × 24 with R12 ends, 11.2 between the flanges | The ends share the flanges' R12, so the outline uses one radius; 12 of winding room on every side |
| Height | 16 | Flange 2.4 + core 11.2 + flange 2.4; three turns of a Ø3.5 cord side by side |
| Core wall | 2.52 (T) | 6 lines |
| Plug | Core inside less 0.25 per side, 1.68 (DIV) wall, 10 deep | Clearance between parts; ends 1.2 above the core's floor |
| Tabs | 2 × 12 wide, U-slits 1 wide, free length 9.5, bump 8 from the root | About 1.6 % strain at 0.4 deflection (1.5 × 1.68 × 0.4 ÷ 8²) |
| Bump, groove | Bump 0.65 at 45°; groove 2 × bump, 45° both ways | 0.4 of the bump reaches past the 0.25 clearance (the catch) |
| Cord slots | 3.2 wide, 10 long with a round end, one in each flange at opposite ends | Pinches a Ø3.5 cord; set `CORD` 0.3 under your cord's diameter |
| Edges | C0.5, also round the slots; C0.6 on the two outer faces (the bed faces) | One visible chamfer value |

Capacity: about 9 turns of a Ø3.5 cord (3 side by side, 3 layers), at an average of about 210 per turn: some 1.9 m.

## Parts

| Part | Orientation | Colour |
|---|---|---|
| base | Bottom down | Off-white |
| cap | Top face down | Off-white |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| cap | The bumps were 0.4, as in the usual tab snap, but 0.25 of that is taken by the clearance between the plug and the core, so they caught by 0.15 (the snap sweep showed 0.47 mm³ for both bumps): the halves would fall apart | Defect | Bump 0.65 (0.4 caught, 3.65 mm³ swept) and the plug 1 deeper, so the longer tab keeps the strain at about 1.6 % |

Dos and Don'ts: one visible chamfer value; one outline radius (R12 on the flanges and the core's ends) plus the round ends of the slots;
the winding room is the same 12 on every side; the joint and its tabs are hidden inside the core; off-white, no accent.

Use cases:
- **Assemble:** push the cap's plug into the base's core until the tabs click (swept: free at 0, 9 and 14 out, 3.65 mm³ of bump being
  pushed over in between; the cap stops on the core's top 0.3 further in and the plug stops 0.4 sideways).
- **Wind:** put the cord through the base's slot from below, the charger left outside, wind it round the core and press the last bit into
  the cap's slot at the other end, the plug left outside.
- **Unwind:** pull the end out of the cap's slot and unwind; the start stays in its slot.
- **Carry:** flat, 16 thick, the size of a phone; the flanges keep the turns from sliding off.
- **Open:** pull the flanges apart; the 45° bumps let go (to clean it or reprint one half).
- **Print:** base bottom down: the core's walls stand up and the grooves have 45° faces above and below. Cap top face down: the plug and
  its tabs stand up, the bumps are 45° both ways. No supports.

verify.py: both parts valid and watertight, one solid each; no interference; fit a 256 bed; every motion as recorded.

Compared with well-known products in this style: radios, a pocket radio, a calculator and a loudspeaker; none is a cord
winder. Flat bobbins for cords are a common kind of object; no product was used as a model.

Not verified:
- Not printed on a real printer.
- How firmly the tabs hold in PLA and PETG, and how often they can be pulled apart.
- Whether your cord is held by the 3.2 slots; a softer or thinner cord needs `CORD` smaller.
