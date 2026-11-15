# 068 Under-desk drawer

A shallow drawer for pens and small things that hangs under a desk top, 140 × 160 × 52. The housing is a plate screwed to the underside
of the desk with two side walls and a back wall; each side wall ends in a ledge with a 45° top face. The drawer's top edge widens 2.4
on both sides with a 45° underside, so the drawer hangs on the ledges, centres itself on them and slides out to the front; the plate
keeps it from lifting. A small bump under the plate rides in a shallow channel along each drawer side and stops the drawer at 120 of
travel; a firm pull takes it past the bump and out. A U notch in the front wall's top edge takes the fingers.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Housing | 140 × 160 × 10.4; plate 4 | Plate thick enough for 90° countersunk M4 wood screws flush; the housing is only as tall as the dovetail and the ledge |
| Drawer | 128 × 157.2 × 47.8 (inside 123 × 152 × 45.4) | 32 modules wide; the depth runs up to 0.25 before the housing's back wall; the height is the overall 52 less the plate and its gap |
| Corners | Drawer R8 (inside R5.48, R3 at the floor); the housing's back corners concentric (R14); front corners square | The housing's front is the cut end of the channel the drawer runs in; a round there would cut through its walls |
| Dovetail | The drawer's top edge widens 2.4 per side at 45°, then 1.2 straight; the ledges follow with 0.25 across every face | 45° prints without supports on both parts (08); 0.25 is the sliding clearance |
| Ledge | 2.4 thick under its slope; housing side wall 3.35 | The wall is what remains of 140 after the drawer, the dovetail and the clearance |
| Stop | 0.6 bump (45° flanks) under the plate 6 behind the front; 0.6 deep, 2.4 wide channel along each drawer side, ending 120 from the bump with a 45° ramp | The bump rides with 0.25 over it; at 120, 40 of the drawer is still in the housing, enough to carry it |
| Finger notch | R16 in the front wall's top edge, C0.5 | As 062; the fingers enter under the plate |
| Screws | 4 × Ø4.5 with 90° countersinks Ø8.5, at x ±48, y ±56 | Over the drawer, so the heads are hidden with the drawer in |
| Edges | C0.5; C0.6 on bed faces | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| housing | Plate down (the desk face on the bed) | Off-white |
| drawer | Bottom down | Off-white |
| (4 × M4 × 16 countersunk wood screws) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| housing | The ledge's slope was moved both 0.25 sideways and 0.35 down from the drawer's slope: 0.43 across the 45° face and 0.6 of vertical play, so a loaded drawer would sag and rock (`verify.py`: still free at 0.5 down) | Defect | The slope is moved only 0.35 down (0.25 across the face); the drawer now stops 0.4 down |
| drawer | The finger notch was extruded away from the front wall into the drawer and cut nothing | Defect | Extruded through the front wall; its edges chamfered C0.5 |

Dos and Don'ts: one visible chamfer value; one plan radius on the drawer (R8, concentric inside) and the housing's back; equal 0.25
clearances on every sliding face; screws hidden behind the drawer; no accent (the contents are the colour).

Use cases:
- **Fit it:** hold the housing under the desk top, screw it on with 4 countersunk wood screws, slide the drawer in from the front: its back
  passes the bumps with a click, then it runs free to the back wall (`verify.py`: stops at 0.3 into the back wall).
- **Open:** fingers in the notch, pull: the drawer runs free to 119 and stops on the bump at 120 (soft: 0.23–0.39 mm³ of overlap while
  being pushed over), with 40 still on the ledges.
- **Take it out:** pull past the stop; the bump drags until the drawer's back passes it at 151, and the drawer is free (`verify.py`: free at
  165).
- **Hang:** the drawer stops 0.3 up against the plate, 0.4 down on the ledges and 0.4 sideways; free at 0.2 in each.
- **Print:** housing plate down: the walls stand on the plate and the ledges' slopes grow inward at 45° at the top of the print; the
  countersinks open upward. Drawer bottom down: the widened edge grows outward at 45° at the top. No supports.

verify.py: both parts valid, watertight, one solid each; no interference closed; motions as above.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a drawer; they are housings with controls and grilles.
Under-desk drawers on rails are a common kind of object; no product was used as a model.

Safety: no batteries, LEDs, magnets, heat or food. Screw the housing into solid wood or a solid board with screws that suit it; do not
hang it from a glass or thin-panel desk top. Keep the load light (stationery).

Not verified:
- Not printed on a real printer.
- How much load the 2.4 ledges carry over time; the drawer is meant for stationery, well under 1 kg.
- How hard the pull past the stop is on your printer: the bump's 0.35 overlap is taken by the drawer's side walls bending inward.
- Countersink and hole sizes for your screws.
