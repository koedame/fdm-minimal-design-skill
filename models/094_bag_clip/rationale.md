# 094 Bag clip

A clip for the folded top of a bag of crisps or coffee: two jaws 120 × 20, 8 thick, joined at one end by a pin hinge and closed at the
other by a snap hook. Closed, the jaws stand 0.25 apart and a 45° ridge on the lower jaw runs 0.25 inside a groove in the upper one, so
the film is held along a bent path rather than pinched flat. The hinge is 07_hinged_case's on a long, narrow box: three knuckles across
the width, a 1.75 filament pin, 45° webs. Two printed parts and a piece of filament.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Jaws | 120 × 20, 8 thick each; 124 long with the knuckles | 6 : 1; holds a bag top folded to about 105 between the hinge and the hook |
| Hinge axis | At the -X end, on the upper jaw's underside | Where the end face meets the parting line, as in the rules |
| Knuckles | R4 (half the jaw), 3 × 6.4 with 0.4 gaps; pin Ø1.9 for 1.75 filament | Fills the 20 width exactly; the knuckle is the jaw's full round end |
| Film gap | 0.25 between the jaws; groove = ridge offset 0.25 | One clearance value; about two layers of bag film folded twice |
| Ridge | 2 high, 45° flanks, 0.8 flat top, from 4 past the knuckles to 4 short of the end | Bends the film across its width, so it cannot slide out sideways |
| Hook | DIV thick, 20 wide, hanging from the upper jaw's 2.4 top skin; a 0.85 slit frees it from the jaw | Free length 11 (13.6 − 2.6), so the catch can be the full 0.6 |
| Barb and groove | Barb 0.85 at 45°, centre 2.6 up; groove barb + 0.25 all round in the lower jaw's end face | Engagement 0.6 (a clip that is handled); strain 1.5 × 1.68 × 0.6 ÷ 11² = 1.25 % |
| Edges | C0.5 on every visible edge; C0.6 on the bed faces (lower jaw's bottom, upper jaw's top) | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| lower | Bottom down | Off-white |
| upper | Top face down | Off-white |

## Review

No defects or violations found. Checked in particular: the upper jaw swings free from closed to 110° open; closing past the closed position
stops at once (634 mm³ at +0.5°: the jaws meet across their length); between 0.6° and 2° short of closed only the barb's engaged tip
overlaps (about 5 mm³: swept as a snap), so the hook rides over the lower jaw's end edge and drops into its groove; the ridge clears the
groove by 0.25 all along.

Dos and Don'ts: one visible chamfer value; no plan radii (a bar), the knuckles' R4 is the jaw's full round end; one seam line round the
clip; plain off-white, no accent; no fasteners (the pin is filament inside the knuckles).

Use cases:
- **Close on a bag:** fold the top over twice, open the clip, lay the fold across the lower jaw between the hinge and the hook, and press
  the far end down until the hook clicks.
- **Open:** lift the far end at the seam with a fingernail or thumb; the 45° barb cams the hook outward.
- **In the cupboard:** the clip is a plain bar 16 high; it lies flat on either jaw.
- **Assemble:** push 1.75 filament through the knuckles and flatten both ends with a warm iron, as 07_hinged_case.
- **Print:** lower bottom down (the barb groove's upper flank at 45°); upper top face down (the hook stands up, the slit opens upward).
  The knuckles' 45° webs carry them in both orientations. No supports.

verify.py: both parts valid, watertight; fits a 256 bed; the hinge sweep is free at 0, 3, 10, 30, 60, 90 and 110°, a snap at 1–2° and a
stop past closed.

Food: the clip touches the outside of the bag only. Do not use it to close a bag with the food against the jaws: printed PLA or PETG is
not certified for food contact, and its layer lines hold dirt.

Compared with well-known products in this style: none is a clip or has a hinge of this kind. A hinged bar clip with a
latch is the common form of a bag clip; no product was used as a model.

Not verified:
- Not printed on a real printer.
- How well the bent path holds thin, slippery film (coffee bags with a foil layer) and thick paper bags (the gap is 0.25).
- Whether the hook keeps its spring after many closings in PLA; PETG is the safer choice.
