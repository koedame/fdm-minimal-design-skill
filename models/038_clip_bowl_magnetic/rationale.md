# 038 Magnetic clip bowl

A bowl for paper clips, Ø72 × 36 (2 : 1). A Ø20 × 3 disc magnet sits in the middle of the floor under a dark cover disc, glued flush:
clips dropped in gather on the disc, and a knocked-over bowl keeps its clips. The dark
disc is the only accent and it marks the one thing the bowl does. The floor runs up into the wall on a cove of R16 so clips slide to
the middle; the bottom edge is cut back 45° by 6, so the bowl stands on a Ø60 circle and its wall floats above the desk.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Bowl | Ø72 × 36 | 2 : 1 |
| Wall | 2.52, C0.5 on both rim edges | 6 lines; one chamfer value |
| Bottom bevel | 45°, 6 | The bowl stands on Ø60; the wall reads as lifted |
| Cove | R16 | The flat of the floor is Ø34.96: room for the cover and nothing else |
| Floor | 5.6 = 1.2 under the magnet + 3.2 pocket + 1.2 cover | The magnet as near the clips as a printable cover allows |
| Magnet pocket | Ø20.2 × 3.2 | Ø20 × 3 disc magnet, the pocket rule scaled up (0.1 per side, 0.2 deep) |
| Cover | Ø32 (8 modules) × 1.2, 0.25 clear, C0.5 on its top edge and on the recess rim | A disc in the floor, not a lid over the magnet; V line at the seam |
| Feet | Ø10.2 × 1 recesses at (±17, ±17) | Inside the Ø60 stand, clear of the pocket |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| bowl | Bottom down, as used | Off-white |
| cover | Bottom down | Dark grey |
| magnet_ref | Bought, glued into the pocket | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| bowl | First built with the magnet put in from below and a cap glued into the bottom: printed bottom down, the pocket's Ø20 ceiling and the cap's ledge were bridges | Violation (03_dos_donts: no bridge for the ceiling of a recess) | The magnet goes in from above, under a cover disc in the floor; pocket and recess both open upward |
| preview | From the default view the floor, and with it the dark disc, was hidden behind the rim | Presentation | View raised (direction −0.6, −1, 1.6) |

Use cases:
- **Drop clips in:** they slide down the cove onto the disc and stay there.
- **Take clips out:** pinch a few off the disc; the magnet holds the rest.
- **Knock it over:** the clips over the disc stay in (about 1.4 between magnet and clip: 1.2 cover + 0.2 left in the pocket).
- **Assemble:** glue the magnet onto the floor of the pocket, let it set, glue the cover over it, flush.
- **Print:** both parts bottom down, no supports, no bridges.

verify.py: bowl and cover valid and watertight, no interference with the magnet, fit a 256 bed; ground contact 2400 mm².

Compared with well-known products in this style: radios, a pocket radio, a calculator and a loudspeaker; none is a
bowl. Magnetic clip holders are a common desk item; no product was used as a model.

Safety (magnets): a Ø20 neodymium magnet is strong; it is dangerous if swallowed and pinches skin between itself and steel. Keep it
glued under its cover and keep the bowl away from small children, pacemakers, cards with magnetic stripes and mechanical watches.

Not verified:
- Not printed on a real printer.
- How many clips the magnet holds through 1.4 of plastic, and how far out from the disc its pull reaches.
