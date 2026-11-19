# 027 Desk edge cable clip

A C-shaped clip, 42.7 × 26.7 in profile and 24 wide, that pushes onto the edge of a 20 mm desk and holds cables in a U-hook behind the
edge. The side profile is the whole design, so the clip prints lying on its side: every bend lies in the layer plane, the jaws flex
along the layers instead of across them, and all the radii come out round. One wall (3.36) runs through the jaws, the spine and the
hook; the outer back corners are R5 and every other corner R1.6, so the wall keeps its thickness round each bend. Several clips along
the edge carry a bundle. No accent: the cables are the only other colour.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Wall | 3.36 (8 lines of 0.42) | The jaw stiffness: each jaw pushes on the desk with about 23 N when sprung 0.4 (cantilever 20 long, 24 wide, PETG E ≈ 2 GPa), at 0.5 % strain |
| Mouth | 20 (desk), narrowed to 19.2 by a ridge on each jaw | Each jaw flexes 0.4; a 19.5–20.5 desk still grips (0.15–0.65 per jaw, under 0.8 % strain). Set `DESK` for another desk |
| Ridges | 45° triangles 0.4 high, 4 from the jaw tips, 1 short of each side | Push on and pull off over the same 45° flanks; they sit outside the side chamfers |
| Jaws | 24 long | Reach past the edge banding of a desk top and grip on a flat face |
| Hook | 12 wide × 12 deep inside | Two Ø5 cables side by side, or a bundle of four to five; its top is 8 under the desk top, out of sight from a chair |
| Radii | R5 on the two outer back corners, R1.6 elsewhere | R5 = wall + R1.6: concentric bends keep the wall even where the jaws bend most; R1.6 twice is under the wall, so the plate ends are almost round. R5 is 12 % of the 42.7 profile |
| Width | 24 | Grid 4; a wide jaw spreads the grip over the desk finish |
| Chamfer | C0.6 on the bed face, C0.5 on the top face | The side faces are the visible ones |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| clip | On its side (the profile on the bed) | Off-white |
| cables_ref ×2 | Reference, not printed | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| clip | The first jaws (4.2 thick, 0.6 ridges) pushed on the desk with about 67 N each: pushing the clip on over 45° ridges would have taken about 250 N | Defect | Wall 3.36 and ridges 0.4: about 23 N per jaw, about 85 N to push on (cantilever estimate, the spine flexing makes it softer) |
| clip | The first outer back corners (R6) were not concentric with the inner R2 corners, so the wall thinned to 2.9 at the bend that carries the jaw load | Violation (03_dos_donts 1: concentric radii) | R_OUT = wall + R_IN |

Use cases:
- **Fit:** push the clip straight onto the desk edge; the rounded jaw tips lead the edge in and the ridges ride over it, then grip.
  Pull it off the same way.
- **Load:** drop cables into the hook from above, behind the desk edge. A few Ø5 cables weigh little against the grip; the hook levers
  the clip about 14 off the spine, and the jaws hold it by the ridges.
- **Move:** slide the clip along the edge to where the cables need to go; the ridges slide with it.
- **Print:** on its side, no supports; the bed face is the whole profile.

verify.py: valid and watertight, no interference with the cables, fits a 256 bed; prints 42.7 × 26.7 × 24.

Compared with well-known products in this style: they are radios, a pocket radio and a calculator; this is a single
bent clip with no controls. Desk edge clips of this C shape are common; no product was used as a model.

Safety: none of the listed hazards (no battery, light, heat, food contact or magnet). Do not hang heavy loads on the hook: the grip is
for cables.

Not verified:
- Not printed on a real printer.
- The grip and the push-on force are cantilever estimates; they depend on the material, the infill and the desk finish.
- Whether the ridges mark a soft desk finish.
