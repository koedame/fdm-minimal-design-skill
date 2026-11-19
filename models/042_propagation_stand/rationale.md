# 042 Propagation stand

A stand for rooting cuttings in water: three 16 mm test tubes stand in a row, their round bottoms in shallow seats in a floating base
and their necks through a bridge, an inverted U of 8 thick plate. The bridge's legs end in tenons that locate in pockets in the base,
so the bridge lifts straight off and the base can be wiped. Seen from the front the object is one line drawn in plate: a U with R12
outside corners standing on a plain slab.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Bridge | 128 × 32 × 96 | 4 : 1 in plan; the depth = the tube pitch |
| Base | 128 × 64 × 12 | 2 : 1, twice the bridge's depth: the stand with full tubes tips only past about 29° (estimated) |
| Plate | 8, top bar and legs | One thickness for the whole U |
| Bridge corners | R12 outside at the top, R4 inside under the bar | 1.5 × and 0.5 × the plate; two radii, one per role |
| Tube pitch | 32 | The clear gaps between tubes (15.5) and from the outer tubes to the legs (15.75) are equal within 0.25 |
| Tube holes | Ø16.5 (tube + 0.25 per side), teardrops in the bar | The bridge prints on its front face, so the holes are horizontal in the print |
| Seats | Ø16.5 × 6 deep, C0.5 rim | Takes the round bottom of a tube; 6 keeps 6 of floor under it |
| Bar height | Top at 108 | A 150 tube stands 48 above the bar, about a third of its length, for the cutting's leaves |
| Tenons | 4.64 thick (the plate less DIV on each side), full depth, 4 long | Location: pockets 0.25 wider and deeper |
| Plinth | Set in 1.2 with 45° | Shadow line, the base reads as floating |
| Rubber feet | Four Ø10 at ±48, ±20 | Under the corners of the area the bridge stands on |
| Edges | C0.5, C0.6 on the bed side | One chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| base | Bottom down | Off-white |
| bridge | On its front face | Off-white |
| (3 × 16 × 150 test tubes, 4 rubber feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| base | With a base as deep as the bridge (32) the stand tipped at about 13° with full tubes: a push of about 0.2 N at the top of a tube knocks it over | Defect | Base 64 deep (2 : 1): about 29° and 0.4 N |
| bridge | Printed bar down, the R12 corners would start at the bed as a radius (elephant's foot, an overhang right at the first layers) | Violation | Print on the front face: the profile lies in the layers; the tube holes become teardrops |
| bridge | The tenons were inset on all sides, so printed on the front face they began 1.68 above the bed, an unsupported face | Defect | Tenons stepped only across the leg, flush front and back |

Use cases:
- **Place:** the base stands flat (about 7700 mm², four rubber feet); the tubes are checked against the parts in their seats with no
  overlap (`tube()` in `design.py`).
- **Fill:** take a tube out through the bar, fill it, put it back: the hole guides it into its seat.
- **Clean:** lift the bridge off with the tubes in it (swept: free upward, located 0.4 sideways and front to back, resting on the base);
  wipe the base.
- **Print:** base bottom down (vertical seats and pockets); bridge on its front face, holes as teardrops. No supports.

verify.py: both parts valid and watertight, one solid each, no interference, fit a 256 bed.

Compared with well-known products in this style: radios, a pocket radio, a calculator and a loudspeaker; none is a
stand for tubes. Test-tube racks and propagation stations are common objects; no product was used as a model.

Safety (water): the printed parts are not watertight and not certified for anything; the water stays in the glass tubes. Wipe the
base after spills; PETG takes the damp better than PLA.

Not verified:
- Not printed on a real printer.
- The tipping angle and force are estimated from part volumes and an assumed 60 % fill, not weighed.
- Test tubes vary in diameter; match `TUBE_D` to the tubes you have before printing.
- From above, the teardrop points of the holes show as small notches behind the tubes.
