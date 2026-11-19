# 014 Glasses case

A hard case for a pair of glasses, a 168 × 64 stadium in plan: body 36 + lid 12. The lid turns on the pin hinge of 07_hinged_case
along the straight back, and two magnets at the round ends hold it shut. The lid is the one dark part; a shallow finger scoop across
the front seam is the one worked-out detail.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Plan | 168 × 64 stadium (ends R32) | The shape of folded glasses; one radius only. Departs from the 8–16 % plan radius on purpose: the full-round end is the form |
| Height | body 36 + lid 12 = 48 | 3 : 1, the proportion of 07_hinged_case; 43.2 inside |
| Inside | 162.96 × 58.96 × 43.2 | Folded glasses up to about 146 × 56 × 38 (between the magnet posts) |
| Walls, floor, top | 2.52, 2.4, 2.4 | 6 lines; 12 layers |
| Hinge | axis on the back face at the seam, 5 knuckles 12 long, 0.4 gaps, R4 | As 07_hinged_case; 61.6 long, centred on the 104 straight of the back |
| Pin | 1.75 filament in Ø1.9 | As the Pin hinge rule; small enough to stay round |
| Magnets | 2 × 6 × 3 in Ø6.2 × 3.2 pockets in 8 × 8 posts at the round ends | At the ends the posts leave the full 58.96 width for the lenses; at the front they would narrow it to 51 |
| Lid lip | 1.68, 3 high, 0.25 clearance, front half only | The Location rule; the back half would block the swing |
| Finger scoop | R9 across the front seam | 0.75 × lid height, so it stays below the top edge of the lid (as 07) |
| Rubber feet | 4 × Ø10.2 at (±52, ±16) | Under the straight part of the floor |
| Edges | C0.5, C0.6 on the bed side | As every part |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| base | Bottom down | Off-white |
| lid | Top face down | Dark grey |
| magnets_ref × 4 | Bought: 6 × 3 disc magnets | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| lid | Found later by a new check in verify.py: the lip, offset inward by the clearance, touched the lid nowhere and would have printed as a loose piece | Defect | The lid wall is thickened on the inside down to the rim and the lip hangs from it |
| lid | Found later: the lid's magnet pockets were cut before the lip was joined; the lip's wall, thickened inside down to the rim, filled 5.5 mm³ of each pocket and a Ø6 × 3 magnet did not fit | Defect | Pockets cut after the lip is joined; the lid and the magnet's Ø6.2 × 3.2 space no longer overlap |

Use cases:
- **Open, close:** the lid swings free from 0 to 150° and comes to rest at about 158°, where the lid knuckles meet the base webs
  (motions: free at 0 to −150°, stop at −170° and at +1°). That stop sits close to the axis, so it is fit only for the weight of the
  lid; do not lean on the open lid.
- **Closed:** the two magnets meet face to face at the seam and hold the lid; the lip keeps it from shifting sideways.
- **Carry:** no edge is sharper than C0.5; the stadium has no corner to catch in a bag.
- **Assemble:** glue the four magnets in their pockets, poles paired so that they attract; push the filament pin through the knuckles
  and flatten both ends with heat.
- **Print:** body bottom down, lid top face down; the knuckles stand on 45° webs, no support.

verify.py: both parts valid and watertight, no interference, fit a 256 bed, ground contact 9312 mm² over 166.9 × 62.9; hinge free
at 0 to −150°, overlap 10.9 mm³ at −170° (stop) and 519.3 mm³ at +1° (closed stop).

Compared with well-known products in this style: none of them is a case. A stadium hard case with a dark lid is a
common form for glasses cases; no product was used as a model.

Safety (magnets): neodymium magnets are dangerous if swallowed, above all two or more. Glue them in fully and do not use the case
if one comes loose. Keep the case away from cards with magnetic stripes and from pacemakers.

Not verified:
- Not printed on a real printer.
- How freely the hinge turns and how strongly the magnets hold through the print (settle with a test piece of the knuckles).
