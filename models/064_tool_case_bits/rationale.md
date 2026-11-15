# 064 Bit case

A pocket case for twelve 1/4-inch hex driver bits, 88 × 48 × 32 (52 deep with the knuckles). The bits stand upright in two rows of six
in hex pockets in a solid rack that fills the lower half of the base; each 25 bit stands 10 deep, shows 15 above the rack and stays 2.6
under the lid. The lid swings up on a pin hinge along the back seam, the 07_hinged_case arrangement: five knuckles on a 1.75 filament pin,
two 6 × 3 magnets in posts in the front corners, a lip round the front half of the lid and a finger scoop across the front seam.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 88 × 48, R12; base 24 + lid 8 = 32 | 22 × 12 modules; base : lid = 3 : 1, as the sample case |
| Rack | Solid to z 12 (half the base) | A 25 bit stands 10 deep with 2 of floor under the pocket, and shows 15 to pick it out by |
| Bit pockets | Hex 6.85 across flats (6.35 + 0.25 per side), 10 deep, C0.5 lead-in | Location clearance; the lead-in guides a bit in |
| Bit pitch | 12 (3 modules), two rows at y ±6, six columns at x ±6 / ±18 / ±30 | 4.7 between bits for the fingertips; the block is centred in the case |
| End margin | 7.8 from the last bit to the wall | The same at both ends |
| Lid clearance over the bits | 2.6 | The bit tops (z 27.05) stay under the lid's inside (z 29.6) |
| Walls, lid top | 2.52 (T), 2.4 | One wall, one plate |
| Knuckles | 5 × 12 long, R4, 0.4 gaps, pin Ø1.9 for 1.75 filament | As the sample case; 61.6 fits the straight part of the back (64) |
| Magnets | 6 × 3 in Ø6.2 × 3.2 pockets in 8 × 8 posts, centred 3.5 in from the corner radius's centre along both axes | Inside the R12 corners, the pocket keeps 3.95 of wall to the outside; 1.6 clear of the front row's lead-ins |
| Lip | 1.68 (DIV) × 3 below the seam, 0.25 inside the walls, front half only, stopping 0.25 short of the posts | Locates the lid; at the back it would block the swing |
| Finger scoop | Disc R6 (0.75 × lid height) across the front seam, 1.8 deep | Stays below the lid's top edge |
| Edges | C0.5; C0.6 on the bed faces | One visible chamfer value; the seam is a V line |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| base | Bottom down | Off-white |
| lid | Top down | Dark grey |
| bits_ref × 12 | Bought: 1/4-inch hex bits, 25 long | — |
| magnets_ref × 4 | Bought: 6 × 3 disc magnets | — |
| (1.75 filament, about 64 long, as the pin; 4 × Ø10 stick-on feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| lid | The lid's magnet pockets were cut before the lip was joined; the lip's wall, thickened inside down to the rim, filled 8.4 mm³ of each pocket and the magnets did not fit (found with the magnets added as bought parts) | Defect | Pockets cut after the lip is joined; the magnets sit with no overlap. The sample case 07 had the same order and the same fault; fixed there too |
| base / lid | The 8 × 8 magnet posts, set against the walls as in the sample, stuck out through the R12 front corners (two light strips in the rendering) | Defect | Posts moved onto the corners' diagonals, 3.5 in from the radius's centre; the case depth went from 44 to 48 so they clear the front row of bits |

Dos and Don'ts: one visible chamfer value; two radii in plan (R12 outline and its concentric inside) plus the knuckles' R4; no fasteners
show (the pin ends are flush in the knuckles); the lid is the secondary dark grey, no accent; the scoop stays inside the front faces of the
two parts.

Use cases:
- **Take a bit:** open the lid; each bit shows 15 above the rack; pinch it and lift. 4.7 between bits leaves room for two fingertips.
- **Put a bit back:** the C0.5 lead-in finds the pocket; the 0.25 clearance lets it drop to the floor of the pocket.
- **Open:** a fingertip in the scoop lifts the lid off the magnets; it swings back to 150° and the case stays standing (swept: free from 0°
  to −150°, stops at −170° and at +1°; the lid also clears the standing bits at every angle to −90°).
- **Close:** the lid falls; the lip finds the base and the magnets pull it shut. The bits do not rattle out: the lid is 2.6 over them.
- **Carry:** in a tool bag or a pocket; closed, the bits cannot leave their pockets (the lid stops them after 2.6).
- **Assemble:** glue the magnets in the posts and the lid with opposite poles facing; push the filament pin through the knuckles; melt or
  glue its ends.
- **Print:** base bottom down: the pockets are vertical, the lead-ins open upward; lid top down with the lip and posts standing up; the
  knuckles stand on 45° webs both ways up. No supports.

verify.py: all printed parts valid, watertight, one solid each; no interference with the bits or the magnets; contact area 3630 mm².

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): radios, a calculator and a loudspeaker; none is a case with a lid.
Bit cases with a hinged lid are a common kind of object; no product was used as a model.

Safety (magnets): the magnets are small; keep the case away from small children who could swallow a magnet that comes loose, and glue
the magnets in. Steel bits are attracted by the magnets near the front corners; this does not affect the case.

Not verified:
- Not printed on a real printer.
- How the 0.25 clearance of the hex pockets holds bits from different makers (some are 6.3, some 6.4 across flats).
- The magnets' pull through the gap, and the pin's wear after many openings.
