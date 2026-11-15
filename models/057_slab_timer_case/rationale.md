# 057 Slab timer case

A kitchen timer as a slab, 92 × 52 × 20, lying on the counter. The top carries two things on its centre line: a four-digit window on
the left and one dial on the right, the same width (28) and the same distance (12) from the ends. Turning the dial sets the time;
the electronics (a 0.36" four-digit LED module, a 12 mm rotary encoder, a small controller board with USB-C and a 12 mm buzzer) are
bought. The shell (top and walls) is one piece; the bottom plate snaps in from below with two hooks, so no fastener shows anywhere.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 92 × 52 × 20, R8 | Window + dial + three 12 margins in length (12 + 28 + 12 + 28 + 12); 52 = the dial + two 12 margins; 20 holds the 15.2 tall inside |
| Window | 28 × 12, R1.2, centred at x −20 | The digits of a 0.36" module (display body 30 × 14): the body's edge stays behind the plate |
| Dial | Ø28 × 12, centred at x +20, 0.4 above the top | Diameter = window width; 12 tall gives a 4 grip band of 36 ribs at the back and a 4.7 long D-shaft engagement |
| Dial face | One step (Ø20 recess 0.8) and one line from r4 to r9 toward the front | One indicator, one step |
| Top plate, bottom plate | 2.4 | One plate thickness |
| Walls | 2.52 (T) | One wall thickness |
| Encoder sleeve | Ø16 under the top plate, 2.6 deep; bushing hole Ø7.2 | The encoder's mounting face clamps against it; wider than the nut recess so it stays joined to the plate |
| Nut recess | Ø12.4, 2.4 deep in the top face, under the dial | The M7 nut (across corners 11.5, 2 thick) sits below the top surface; the dial covers it |
| Dial bore | D shaft (Ø6.1, flat at 1.55) from 2.5 under the face; Ø8 counterbore 2 deep with a 45° cone above | The bushing's top stands 2 above the nut; the cone prints without support face up |
| Display | Pressed against the plate by four Ø5 pads (to 8.8); a DIV frame 2 deep round the body | The frame locates the module under the window; the pads hold it there |
| Controller board | 21 × 17.8, 4.4 tall, on the floor in a low frame at the right end; USB-C opening 9.6 × 4 in the end wall | The socket's centre 5.2 above the bottom = opening centre |
| Buzzer | Ø12 in a ring on the floor, three Ø2 holes under it | Sounds downward into the 1 gap the feet leave |
| Hooks | Two, 10 × 1.68 (DIV), at the middle of the long sides, top at 12; barb 0.8 at 8–11 | Free length 5.6 below the barb: strain about 2.6 % (1.5 × 1.68 × 0.8 / 5.6²), in PLA's range; the barbs drop into V grooves (barb + 0.25) |
| Coin slot | 12 × 1.6, 1.2 deep, in the plate's left edge | A coin pries the plate out |
| Edges | C0.5; C0.6 on the bed face | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| shell | Top down | Off-white |
| bottom_plate | Bottom down | Off-white |
| dial | Front face up (back on the bed: the counterbore opens at the bed, its cone narrows upward) | Off-white |
| display_ref, encoder_ref, controller_ref, buzzer_ref | Bought | — |
| (4 × Ø10 stick-on feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| shell | The nut recess (Ø12.4) was wider than the encoder sleeve (Ø12) and cut through the plate above it: the sleeve was a loose piece | Defect | Sleeve Ø16; the plate above it keeps a ring 1.8 wide |
| shell / controller_ref | The controller board ran into the inner corner radius of the walls and into the plate's lip | Defect | Board moved 2.6 toward the centre; the lip is cut away round the board |
| bottom_plate | Flush with the walls, the plate had nothing to pull on: the hooks could not be released | Defect | Coin slot in the plate's left edge |
| bottom_plate | The controller board's frame ran to 0.05 from the end wall: the plate could not move its 0.25 clearance sideways | Defect | Frame ends 0.25 short of the wall |
| shell | The USB-C opening was 0.6 below the socket (the socket sits on top of the 1.2 board) | Defect | Opening centre 5.2 above the bottom |

Dos and Don'ts: one visible chamfer; one radius in plan (R8) and the dial's circle; the window and the dial are the only features on
the top, the same width and the same margin; no screws visible; no accent colour (the dial is the slab's colour, the display is the only
dark area).

Use cases:
- **Set:** turn the dial; the 36 ribs on its back band give grip with wet fingers, and the encoder's detents count the minutes
  (swept: the dial turns freely about its axis at 0–270°, is 0.4 above the top and stops at 0.6 when pressed).
- **Read:** the four digits show through the window; the module is held against the plate, its body's edge 1 behind the window's edge.
- **Hear:** the buzzer sounds through the three holes in the bottom plate and the gap under the slab.
- **Power:** a USB-C cable into the opening at the right end.
- **Assemble:** cut the encoder shaft to 14.5 from its mounting face and break off the small locating tab on its face (the sleeve has no
  hole for it); push the bushing up through the sleeve and tighten the nut in the recess; press the dial onto the shaft. Lay the
  display module in its frame, the controller board and the buzzer on the plate, and press the plate in until both barbs click
  (swept: the plate is free 0.2 below its seat, catches at 0.8 and rides over at 2–8, the overlap being the two barbs' own volume (about 21 mm³); it stops at 0.4 sideways).
- **Open:** a coin in the slot at the left end levers the plate out; the 45° barbs ride out of the grooves.
- **Print:** shell top down: the window is a through cut, the nut recess opens at the bed, the sleeve and the display frame grow up from
  the plate; plate bottom down with its hooks and pads standing; dial front face up. No supports.

verify.py: valid, watertight, one solid per part, no interference, fits a 256 bed.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2) and Braun's travel alarms: ET 66 is a slab with a display and a grid of
buttons; the BC and AB alarms are small squares with an analogue face. This is a slab with one window and one large dial of the same
width; it shares only the general language (a plain block, one material, one dial). No product was used as a model.

Safety: an LED display and electronics, powered over USB-C (5 V); no batteries inside. Keep it away from the hob and oven (PLA softens at
about 55 °C; PETG at about 75 °C), do not wash it in water, and use a USB power supply with the usual approvals.

Not verified:
- Not printed on a real printer.
- The LED module's board size and the position of its header: modules differ; the frame round the display locates it, the pads under the
  board may need moving. Solder the wires directly instead of a pin header.
- The encoder's detent feel through the dial, and the snap force of the two hooks in PLA.
- How loud the buzzer is through the bottom plate on a soft surface.
