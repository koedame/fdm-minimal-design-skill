# 019 Headphone stand

A plate column 64 wide, 24 thick and 228 tall on a 128 × 96 slab, 240 overall. The top of the column is a shallow arc for the
headband, and the outline of both faces is bevelled 2 mm. The column and the base are separate prints joined by two Ø4 steel dowels
and glue: the column then prints on its side, strong along its length and without support, and the joint is a designed shadow line
at its foot.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Stand | 128 × 96 × 240 | Base 4 : 3 on the grid 16; the height puts the cups of full-size headphones about 40 above the desk |
| Base | 12 thick, R16 corners | Heavy enough to read as a base; a 1 : 1 slab under the column would tip |
| Column | 64 × 24 × 228 | Half the base width, a quarter of its depth; the cups (about 120–160 apart) hang clear of its sides |
| Top arc | sagitta 8 over 64 (R68), R12 into the sides | Tighter than a headband (R 75–90), so the band rests on the crown and does not rock |
| Bevel | 45°, 2 on the outlines of both faces | The headband pad rests on a 20 flat, not on an edge; it also prints on the bed side |
| Shadow line | C0.5 round the foot of the column | Half of a V, against the flat top of the base (the split joint rule) |
| Dowels | 2 × Ø4 × 20 steel at ±16; holes Ø4.2, 10 in the base, 11 in the column | A quarter of the column width apart; 0.5 free at each end for glue |
| Dowel holes in the column | teardrops, roof toward the back | Horizontal in the print |
| Rubber feet | 4 × Ø10.2 at ±48, ±32 | Inside the bed chamfer |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| base | Bottom down, as used | Off-white |
| column | On its side, front face down | Off-white |
| dowels_steel_ref | Bought part, not printed | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| column | The headband pad rested on a 24 mm top with 0.5 chamfers; a padded band left hanging there creases along the edges | Violation | 2 mm 45° bevel on the outlines of both faces (a 20 flat on top) |

Use cases:
- **Hang:** drop the headband over the arc; the cups hang either side of the column, clear of the base unless the headphones are
  longer than about 220 from band to cup.
- **Take off:** lift; nothing holds the headband, and the base stays down under its own weight and the rubber feet.
- **Bump:** a 10 N push at the top puts about 0.4 MPa on the glued 64 × 24 joint; epoxy or a cyanoacrylate gel takes this, and the
  two dowels take the shear.
- **Assemble:** glue the dowels into the base, put glue on the foot and the dowels, push the column on and keep it square for the
  cure time. Wipe out any squeeze-out so the shadow line stays clean.
- **Print:** base bottom down (round holes); column front face down, with the bevels at 45° and the dowel teardrops pointing up. Use
  40 % infill or more in the base for weight.

Why split when the column would fit the bed upright: an upright plate 240 tall breaks along its layers when bumped, and the base
around its foot would be an overhang.

verify.py: both printed parts valid and watertight, no interference (the dowels included), fit a 256 bed, ground contact 11501 mm²
over 126.9 × 94.9.

Compared with well-known products in this style: none is a stand. Plate-on-slab headphone stands are a common form;
no product was used as a model.

Not verified:
- Not printed on a real printer.
- How well the base holds the stand down with heavy headphones at a given infill.
- The glue joint's strength on a real print.
