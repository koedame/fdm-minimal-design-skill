# 03 Dos and Don'ts (checklist)

`02_rules.md` compressed for judging. Review with the procedure in `04_review.md`, checking this table from top to bottom.
The numbers are rules of thumb, not an official standard of any manufacturer.

---

## 1. Dimensions and layout

| Do | Don't |
|---|---|
| Derive every dimension from the grid (4 mm etc.) or a ratio (2:1, 3:2) | Use CAD defaults or round numbers without a reason |
| Align elements to shared reference lines (top edge, bottom edge, centre line) | Centre things for now and leave the rest as margin |
| Give margins with the same role the same width | Let the top, bottom, left and right margins differ |
| Relate the dimensions of elements to each other (e.g. dial diameter = distance between the centres of the outer buttons) | Decide each element's dimensions independently |
| Unify plate and wall thicknesses within an object | Make only some parts a different thickness |

## 2. Form and edges

| Do | Don't |
|---|---|
| Large radii in plan (outline), sharp edges | A large fillet on every edge (a bar of soap) |
| One visible chamfer value (C0.5) throughout | Chamfer values that differ from place to place, or edges left untreated |
| At most 2–3 radii, one per role | The same radius mechanically on every corner, or a different radius each time |
| Plate ends nearly full round (R ≈ plate thickness / 2) | A half-hearted small radius on the ends |
| **Ends and faces that touch the ground stay flat** (chamfer only) | A full round even on the ground end, so it stands on a line |
| Keep recesses (finger grips etc.) inside the face they belong to | A recess cutting into the rim or chamfer of the neighbouring face |
| Forms made from extrusions, cuts and revolutions | Freeform surfaces, organic shapes |

## 3. Details

| Do | Don't |
|---|---|
| Keep most of it plain and work out only a few spots precisely | Detail the whole thing uniformly and shallowly |
| Small holes in a dense array | A few large holes |
| Repeat one shape and show differences with colour | A different shape for each button |
| Make each seam between parts one intended reveal line | A line simply appears wherever the parts were split |
| Hide fasteners (back or bottom, magnets, snaps) | Screws on the front |
| Semicircular ends on elongated holes | Slots with square corners |

## 4. Colour, labels and materials

| Do | Don't |
|---|---|
| Body off-white or light grey, secondary parts dark grey | Pure white, primary colours, many colours |
| One accent colour, one place, only on a part with a functional meaning | Decorative accents, accents in several places |
| Labels tiny, in a light grey close to the background | Big black lettering, logos |
| Functional indication (indicators, windows) may be dark | No distinction between labels and indication |
| Use matte materials | Glossy PLA |

## 5. FDM printing

| Do | Don't |
|---|---|
| Put the visible face on the build plate | Print the visible face up and show layer lines |
| Exception: a part whose visible face has steps or recesses prints face up | Make the ceiling of a recess as a bridge |
| Make housings sleeves with a separate lid | A closed box printed bottom down (the top becomes a ceiling) |
| Run wall openings to the top, or make them slide-in | Make the top edge of a long opening a bridge |
| Stand posts and bosses vertically (in Z) | Horizontal bosses |
| Teardrop horizontal holes, 45° under projections | Round horizontal holes, 90° overhangs |
| Vertical slots instead of round holes on vertical walls | Rows of round holes on vertical walls |
| Print objects whose side profile is the design lying on their side | Build sloped faces in the layer direction |
| Wall thicknesses as multiples of the line width (2.52 / 1.68 / 0.84) | Wall thicknesses unrelated to the line width |
| Clearance 0.2–0.3 mm per side | Design fits with zero clearance |
| C0.6 on edges at the build plate side | A radius on the bed side (elephant's foot shows) |
| Move the Z seam to a back corner | A seam on a rounded front corner |

## 6. Working process

| Do | Don't |
|---|---|
| Be able to give a reason for every dimension | Leave "felt right" or "left at the default" |
| Verify use cases (place, hold, open, remove, hang), not only the look | End the review after checking proportions, alignment and radii |
| Measure interference, contact width and opening angles as numbers | Look at an image and decide "seems fine" |
| Apply each rule together with its reason | Apply rules mechanically everywhere |
| Settle dimensions with a test piece of just the mating features | Print the whole thing straight away |
| Judge on the gaps and edges of a full-size print | Judge good or bad on the CAD screen alone |
