# 043 Wall hygrometer frame

A 64 × 96 frame that hangs a small bought digital thermo-hygrometer on the wall. The face carries only two openings, one above the
other at the same width: a smoked window over the display and a field of eleven vertical air slots for the sensor. Every margin on the
face (sides, top, between window and slots, bottom) is 11.2, so the two openings read as one column. The housing is a shallow sleeve
that steps in 1.2 at the wall on a 45° face, so it floats on a shadow line. A back plate hangs on two screws through keyholes; a lip
round its edge locates the housing, two snap hooks hold it, and a frame on the plate presses the hygrometer against the window's flange.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Housing | 64 × 96 × 24, R8 | 2 : 3; R8 = 12.5 % of the width; 24 = the 15.2 device + the window flange + the plate, rounded to the grid |
| Face plate | 2.4 | The window and slots are cut through it; same as the sample wall unit |
| Shadow line | 1.2 inset at the wall, 45° | Lifts the housing off the wall visually; prints as a 45° chamfer on the top of the face-down print |
| Margins | 11.2 everywhere on the face | One margin; the window width then follows: 64 − 2 × 11.2 = 41.6 |
| Window | 41.6 × 24, R2 | Covers a 48 × 28.6 device's display area (check yours) |
| Window flange | 3 beyond the opening, 1.2 thick | Holds the window from behind; the device presses on it |
| Slots | 11 × 1.6 wide, pitch 4, 38.4 long (= 96 − 3 × 11.2 − 24) | Same width as the window; 1.6 keeps fingers out and prints clean |
| Back plate | 2.4 thick, 0.25 inside the housing walls all round | One plate thickness; GAP for the fit |
| Lip | 1.68 (DIV) thick, 6 deep | Locates the housing over the plate in X and Y |
| Snap hooks | 1.68 × 10, rising to 18 from the wall; 45° barb 0.8 high at 14–17 | Root 11.6 below the barb: bending strain about 1.5 % (1.5 × 1.68 × 0.8 / 11.6²); 45° both sides, so the housing pulls off for a battery change |
| Barb grooves | Barb + 0.25 all round, 0.8 deep in the 2.52 wall (1.72 left) | Clearance for the fit; the wall stays three lines thick at the groove |
| Device frame | 1.68 ring, 4 high, 0.25 round the device; four Ø6 pads under it | Holds the device square to the window; the pads set its face on the flange |
| Keyholes | Two, x ±16 under the device, 6 travel; bosses 6.4 thick | Head Ø8.4, shank Ø4.2; ledge 2 + pocket 3 + 1.4; 32 apart so the plate cannot turn on the screws |
| Edges | C0.5, C0.6 on the face (bed) | One chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| housing | Face down | Off-white |
| window_smoke | Face down | Smoked translucent (PETG) |
| back_plate | Wall side down | Off-white |
| hygrometer_ref (digital thermo-hygrometer, about 48 × 28.6 × 15.2) | Bought | — |
| (2 × 4 mm pan-head screws and wall plugs) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| housing / back_plate | Nothing held the housing on the plate: the lip only located it, and a pull or a knock would have taken it off the wall | Defect | Two snap hooks rise out of the long sides of the lip (slit free of it) into grooves in the housing walls; 45° barbs, so it still pulls off by hand |
| housing | The slot length was first taken as 96 − 4 × 11.2 − 24, which left the bottom margin larger than the others | Defect | 38.4 = 96 − 3 × 11.2 − 24: every margin 11.2 |

Use cases:
- **Hang:** mark two holes 32 apart, level; drive the screws in, standing 3 out. Put the plate's keyhole heads over them and slide it
  down 6.
- **Fit the hygrometer:** drop the window into the housing from behind, then the device into the frame on the plate, display up. Push
  the housing straight on: the lip finds it, the hooks click into the grooves, and the device presses the window's flange against the
  face (swept: the housing is free 0.3 off the wall and stops at 1 on the barbs; it stops at 0.4 against the plate sideways and
  toward the wall; the window is held 0.3 against the face).
- **Read:** the display shows through the smoked window; room air reaches the sensor through the slots.
- **Change the battery:** pull the housing off (the barbs ride out on their 45° faces), lift the device out, change the cell, put back.
- **Print:** housing face down (walls stand up, the shadow line is a 45° chamfer at the top, the grooves are 45° V's); window face down,
  flange up; plate wall side down, hooks and lip standing up, barbs at 45°. No supports.

verify.py: all parts valid and watertight, one solid each, no interference, fit a 256 bed.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2) and Braun's BC and AB travel alarms: the travel alarms are small
square cases standing on a desk with a dial; the calculator has a display window over a grid of keys, but here the second field is air
slots, not keys, and the object hangs flat on a wall. Wall thermo-hygrometer cases with a window and vents are a common kind of object;
no product was used as a model.

Safety (battery, wall mounting): the bought hygrometer runs on a coin cell. Coin cells are dangerous if swallowed; the snap hooks are
not a child-resistant lock, so hang it out of reach of small children and keep spare cells away from them. Drive the screws into wall
plugs or plasterboard anchors made for your wall; the hold of the printed keyholes has not been tested, so pull the frame down by hand
before you leave it.

Not verified:
- Not printed on a real printer.
- The device size is one common size; measure yours and change `DEV` before printing.
- How fast the reading follows the room: the sensor is in a closed housing that exchanges air only through the slots, so it lags
  behind an open device.
- The snap force of the hooks in PLA.
