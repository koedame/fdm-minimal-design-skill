# 088 AA battery box

An enclosure 76 × 68 × 24 for a bought flat holder of four AA cells with wire leads, the kind that powers a small project. The holder
lies on the floor; the whole top is a lid that slides out toward the +X end in a dovetail, so all four cells are reached at once, and a
printed snap tab clicks it shut. The leads leave through a small stadium hole in the -X end.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 76 × 68, R12; 24 high | 19 × 17 modules; R12 = 15.8 % of the length; the holder (63 × 57.5 × 15.5, a common size: measure yours) fits inside with room for the leads |
| Wall, floor | T (2.52), inner corners R9.48; floor 2.4 | One margin, concentric corners (R12 − T); a line-width multiple |
| Holder place | Against the latch block, 3.3 free at the -X end | The holder's square corners would hit the R9.48 inner corners at the -X end; the free end leaves room for the leads to bend to the hole |
| Lid | 2.4 thick, dovetail flanks 1.2 over 2.4 (27° from vertical), as in the power-bank sample | Keeps the lid from lifting; the flanks print without supports (lid top face down, body upright) |
| Lid seat | The rails' flat tops under the groove (1.4 deep, 45° underside to the wall) and the latch block | The dovetail alone would let the lid drop in; the seat carries it from below |
| Rails | DIV (1.68) inside the long walls, the groove cut into them; 0.25 clearance | The rail width of the sample; clear of the holder (rails at ±29.8, holder ±28.75) |
| Latch block | 4.2 inside the +X end wall, full height from the floor; notch 1.8 wide, 0.95 deep across its top | The notch opens upward in the print, no bridge |
| Snap tab | 16 long × 10 wide, freed by a 1 wide U slit; 45° bump 0.85 | Catch = bump − clearance = 0.6, for a cover that is handled; strain at full deflection 1.5 × 2.4 × 0.85 ÷ 16² = 1.2 % |
| Thumb grip | 4 × 6 × 0.6 on the tab | Where the thumb pushes the lid out |
| Lead hole | Stadium 4 × 2 at z 10.4, y 21.75, C0.5 flare outside | Two 26 AWG leads side by side; round ends of Ø2 need no teardrop |
| Edges | C0.5 on the top rim, on the lid's top edges and as a flare on the groove's top edges (a V seam); C0.6 on the bed face | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down | Off-white |
| lid | Top face down | Off-white |
| holder_ref (4 × AA flat holder with leads) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| body × holder | `verify.py` found 271 mm³ of interference: the holder's square corners ran into the R9.48 inner corners at the -X end (outline was 76 × 64) | Defect | Outline 76 × 68; the holder sits against the latch block, where the corners are square; the leads moved to the -X end, where the room is |
| lid | The bump was 0.8: it caught the notch by 0.55, less than the 0.6 for a cover that is handled | Violation | Bump 0.85 into a 0.95 notch; catch 0.6, strain 1.2 % |

Dos and Don'ts: one visible chamfer value (C0.6 only on the bed face); radii R12 outline with its concentric R9.48 and R9.23 (lid end),
R1 lead-hole ends; one margin; plain, with the latch as the one worked-out spot; off-white, no accent. The tab's slits and the thumb grip
stay sharp: a C0.5 would make the 1 wide slit a 2 wide V and take the 0.6 deep grip away.

Use cases:
- **Change the cells:** thumb in the grip, push the lid toward +X. The bump rides out of the notch over its 45° flank (the tab bends
  0.85 up) and drags over the top of the end wall for 5 mm, then the lid slides freely; pull it out. All four cells are open at once.
  Slide the lid back in from the +X end until it clicks; it stops against the -X wall.
- **Fit the holder:** stick it to the floor with the foam tape most holders carry (or a pad of double-sided tape) against the latch
  block, leads toward the -X end, and push the leads out through the hole. Tie a loose knot in the leads inside the box so a pull on the
  wire does not reach the holder's solder tags.
- **In use:** the box lies on its bottom or stands on any side; the lid is held by the dovetail on both sides and the snap at the end.
  It can lift 0.5 in the dovetail when pushed from below (the play of the clearance along a 27° flank); it does not rattle out.
- **Print:** body bottom down (the rails have a 45° underside, the notch is open at the top); lid top face down (the bump points up).
  No supports.

verify.py: body and lid valid, watertight; fits a 256 bed; no interference with the holder; the lid slides free from 8 to 80, snaps from
0.5 to 5 (3.2 mm³ at most), stops at −0.3, and stops sideways at 0.4 and upward at 0.8.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): radios, a pocket radio, a calculator and a loudspeaker. The ET 66
calculator holds its cells behind a cover on its back; this box is a plain rounded slab whose whole top slides off. A sliding-lid
battery box is a common enclosure; no product was used as a model.

Safety (batteries): do not short the leads: insulate the bare ends before the cells go in, and add a fuse or a switch in the circuit you
power. Put all four cells in the same way round and do not mix old and new cells, or alkaline and rechargeable; a reversed or mixed cell
can leak or heat up. Do not charge rechargeable cells in this box. Take the cells out when the project is put away for a long time;
leaking alkaline cells damage the holder's springs. PETG softens at about 75–80 °C: keep the box out of a hot car and off radiators.

Not verified:
- Not printed on a real printer.
- The holder's size: 63 × 57.5 × 15.5 is a common size, but holders vary by a millimetre or two; measure yours before printing.
- How many times the snap tab clicks before the bump wears in PETG.
