# 090 Cotton swab holder

A rounded-square jar 56 × 56 × 84 for the bathroom shelf, in which about a hundred cotton swabs stand on end. The body is 64 high, so the
swabs (75 long) stand 13 above its rim and one is taken by its end without tipping the rest out. A cap 20 high covers them and keeps the
dust off; a DIV lip on the body's rim fits 0.25 inside the cap's wall and locates it. Two printed parts.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 56 × 56, R8; 84 high | 14 modules; R8 = 14.3 % of the side; tall enough for 75 swabs standing with 4 of air under the cap |
| Seam | At 64 of 84: body 64, cap 20 | The swabs' upper ends (13 above the rim) are free to take hold of; the cap is a quarter of the height |
| Wall, floor, cap top | T (2.52), inner corners R5.48; floor 2.4; cap top 2.4 | One margin, concentric corners; line-width multiples |
| Lip | DIV (1.68), 4 above the rim, 0.25 inside the cap's wall (outer face inset T + 0.25) | Location as in the rules; 4 high keeps the cap from sliding off when knocked |
| Band | The wall thickened inside to T + 0.25 + DIV (4.45) for 4 below the rim, 45° underside | Joins the lip to the body (a lip inset by the clearance would stand clear of the wall); prints upright |
| Opening | 47.1 square inside the lip | About 100 swabs with Ø5 heads; the band's 45° underside guides a swab from the corners up through it |
| Edges | C0.5 on the rim and the cap's lower edge (one V seam), on the lip's top edges; C0.6 on both bed faces (body bottom, cap top) | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down | Off-white |
| cap | Top face down | Off-white |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| body × cap | `verify.py` found 6 mm³ of interference with the cap in place, and the cap could not move its 0.25: chamfering the rim after the lip was on also chamfered the concave edge at the lip's root, which filled the clearance | Defect | The rim is chamfered on the plain body, then the lip is added |
| cap | The cap's top had C0.5, but it prints top face down: its top is a bed face | Violation | C0.6 (CH_BED) on the top, C0.5 on the lower edge |

Dos and Don'ts: one visible chamfer value (C0.6 only on the bed faces); one radius R8 with its concentric R5.48, R3.75 and R3.55 inside;
one margin; one seam line; plain, with the lip as the one worked-out spot; off-white, no accent.

Use cases:
- **Fill:** take the cap off and stand a pack of swabs in on end; a hundred fill the opening. Any that lie across the top go back on end.
- **Take one:** lift the cap off (it locates only, nothing to undo) and pull a swab by its end; the rest stand 13 proud of the rim, the
  jar weighs about 75 g in PETG, so a swab comes out without lifting the jar.
- **Cap off:** put it top down on the shelf: it stands on its flat top. Cap on: it sits on the rim, the lip keeps it from sliding off.
- **Clean:** wipe or rinse; the inside corners are R5.48. Dry it before refilling: the swabs are cotton.
- **Print:** body bottom down (the band's underside is 45°); cap top face down. No supports.

verify.py: body and cap valid, watertight; fits a 256 bed; the cap lifts free, sits on the rim, and stops sideways at 0.4.

Compared with well-known products in this style: radios, a pocket radio, a calculator and a loudspeaker; the loudspeaker among them is a tall box, but a loudspeaker with a front grille, not a jar with a cap. A rounded-square jar with a cap is the common form of a swab
holder; no product was used as a model.

Not verified:
- Not printed on a real printer.
- Whether a full jar of swabs (packed tight) lets one out of the corner under the band without pulling others with it.
- How the 0.25 lip clearance feels on your printer: loose enough to lift off, firm enough not to rattle.
