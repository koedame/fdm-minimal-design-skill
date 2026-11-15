# 05 Sample catalogue (12 objects)

Pick the sample closest to what you want to make, and adapt its function in `scripts/fdm_samples.py`.
Choose the form from the "kind of object" table and the structure from the "mechanism" table separately; combining them is fine.

The state of every sample:
- Valid solids, closed meshes, and no interference in the assembled state (checked with `scripts/verify.py`).
- **Not printed on a real printer.**

Preview images are in `assets/samples/<name>/`, with the STEP files next to them in the `.skill` bundle. Running `scripts/fdm_samples.py` generates the STEP and the STLs, placed in print orientation.

## Quick table: what you want to make → sample

| What you want to make | Sample |
|---|---|
| Clocks, gauges, round displays, thermo-hygrometers | 01 clock |
| Remote controls, calculators, controllers, cases with a keypad | 02 remote |
| Trays for small things, organisers, dividers, pen holders | 03 tray |
| Cylindrical speakers, diffusers, lights, bottle-shaped housings | 04 cylinder |
| Phone and tablet stands, bookends, charging docks | 05 stand |
| Box-shaped electronics (radios, speakers, amplifiers, power supplies, routers) | 06 radio |
| Boxes with an opening lid (small-item boxes, tool cases, glasses cases, card cases) | 07 hinged_case |
| Portable devices with batteries or connectors (power banks, sensors, meters) | 08 power_bank |
| Things fixed to a wall or furniture (thermostats, sensors, switches, label holders) | 09 wall_unit |
| Things that glow, or stack different materials (lamps, night lights, indicator lights) | 10 lantern |
| Things that do not fit the bed (monitor risers, shelves, long trays, signs) | 11 split_riser |
| Things that screw on (containers, canisters, bottle caps, lens caps) | 12 threaded_jar |

### Quick table: mechanisms and joints

| Mechanism needed | Sample | Key point |
|---|---|---|
| Opens by rotating | 07 | Pin hinge. 45° webs support the knuckles from below. The pin is 1.75 mm filament |
| Slides off | 08 | A dovetail of about 45°. Prints without supports in both orientations |
| Fastens without tools (removable) | 08, 09 | Printed snaps (cantilever tab + 45° bump, 45° hook) |
| Held by magnets | 06, 07 | Ø6.2 × 3.2 pockets in vertical posts |
| Held by screws (hidden) | 02 | M2 from the bottom, into bosses behind the face plate |
| Locating | 06, 07, 10 | A lip (a step on the inside of the wall), 0.25 mm clearance per side |
| Screws on | 12 | Threads with 45° flanks, pitch 4, engaged with a half-pitch offset |
| Split and joined | 11 | Ø4 steel dowels, teardrop dowel holes, the seam shown as a V line |
| Hangs on a wall | 09 | Keyhole slots (head relief on the wall side), two parts: bracket and cover |
| Lets light through, shows something | 09, 10 | A clear window fitted from behind, a translucent layer as a separate part |
| Brings out a connector | 08 | USB-C as a horizontal stadium (only the flat part becomes a bridge) |
| Moving controls | 01, 06, 10 | Buttons, dial, slide switch |

---


## 01 clock — arched body + round dial

- **Rationale for dimensions:** decided on a 4 mm grid. Width 104, depth 36, dial Ø88.
  - The top of the body is a half circle (R52) concentric with the dial, so the frame around the dial is one even band of 8.
  - Below the dial the frame doubles to 16, which puts the dial above the middle of the body. Height 112.
  - The bottom stands flat. Its two corners take R8, the same as the frame width, so the object uses two radii.
- **Print strategy:** the housing prints back face down, with a through bore and a counterbore on the front side. The step becomes a shelf seen from above, so no bridge forms.
- **Details:**
  - The indices are 12 round dots inlaid in the dial; major and minor dots have diameters of 2:1 (Ø4.8 and Ø2.4) on one circle of Ø72.
  - The hands are round-ended bars, the same circle drawn out. Their widths are the two dot diameters. The minute hand stops 1.6 mm short of the major dots, and the hour hand is 3/4 of the minute hand.
  - There is no second hand. The accent goes on the 12 o'clock dot only: it tells which way is up on a dial without numerals.

| Part | Orientation | Colour |
|---|---|---|
| housing | Back face down | Off-white |
| dial + dial_marks_inlay + dial_top_mark_inlay | Front face down (layers 1–2 in other colours) | Light grey + dark + accent |
| hand_hour / hand_minute | Flat | Dark |

**Notes:**
- Shaft diameters of movements and hand holes differ from product to product. Match `CLOCK_SHAFT_HOLE` and `HAND_HOLES` to the parts you have.
- Use a movement without a seconds shaft, or leave its second hand off.

## 02 remote — one-piece body + face plate

- **Rationale for dimensions:** outline 52×152×14 (grid 4 mm). Key pitch 12 (3 × grid). The margin above the IR window equals the side margins of the key block. From there downwards, the power key sits 1.5 pitches below the IR window, and the key block 2 pitches below the power key. The IR window is as wide as the key block.
- **Print strategy:**
  - The face plate prints **front face down**. The key holes and IR window come out most accurate.
  - The body prints bottom down. The step that receives the face plate is an upward-facing shelf, so no supports are needed.
  - Screws (M2) go from the bottom into bosses behind the face plate.
- **Details:** no lines on the sides; the 0.25 mm reveal around the face plate is the only line. The lower half is kept empty as the place to hold.

| Part | Orientation | Colour |
|---|---|---|
| face_plate + ir_window_inlay | Front face down | Off-white + dark |
| body | Bottom down | Off-white |
| key ×12 | Front face down | Dark |
| key_power | Front face down | Accent |

## 03 tray — a container with no extra parts

- **Rationale for dimensions:**
  - Outline 2:1 (200×100).
  - Inner widths: trough : column = 2:1. The column is split into two cells of equal size.
  - Dividers are 4 mm lower than the outer wall.
  - The bottom is a plinth set 1.2 mm inward and joined with a 45° face. The shadow line makes the object look as if it floats.
- **Radii:** only two. R11.48, derived from the outline, and R3 for the inside (shared by the divider corners and the floor corners).
- **Walls:** outer wall 2.52 (6 lines), dividers 1.68 (4 lines).
- **Accent:** none. An example of the decision not to add colour to an object with no function to emphasise.

## 04 cylinder — a tall cylinder

- **Rationale for dimensions:**
  - Height : diameter = 2:1 (144:72).
  - The plain areas top and bottom are the same 24 mm (bottom: a 24 mm band; top: a 14 mm band + a 10 mm cap).
  - The button sits midway between the rim of the knob and the rim of the cap.
- **Print strategy:**
  - The body prints standing up.
  - The grille is **vertical slots with semicircular ends**. Bridges are only as long as the slot width, and the ends come out round.
  - The cap prints top face down; the knob prints front face up.

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down | Off-white |
| top_cap | Top face down | Off-white |
| knob | Front face up | Off-white |
| button_on | Front face down | Accent |

## 05 stand — a wedge printed on its side

- **Rationale for dimensions:** plate thickness 8 mm throughout; lip height 3 × plate thickness (24 mm). Depth 96, height 80, width 80, channel width 12 (all on the 4 mm grid). The back plate leans at 70°.
- **Radii:** three, split by role.
  - Plate ends (including the top of the back plate): R3.8 (nearly full round)
  - The load-bearing inner corner at the root of the back plate: R10
  - Channel: R2 (so the floor that takes the pad stays flat)
- **Print strategy:** lay the side profile on the bed and print it on its side. The cable channel is a trapezoid with 45° on both sides.
- **Accent:** a TPU anti-slip pad in the bottom of the channel.

| Part | Orientation | Colour |
|---|---|---|
| stand | Side down | Off-white |
| grip_pad_tpu × 2 (one each side of the groove) | Flat | Accent (TPU) |

## 06 radio — box-shaped electronics

- **Rationale for dimensions:**
  - Front 144×96, 3:2.
  - The frame around the front plate is 14 mm on the left, right and bottom.
  - Dial Ø32 equals the distance between the centres of the two outer buttons.
  - Wall 2.52 (6 lines), hole pitch 4 mm.
- **Print strategy:**
  - The body is a sleeve with no top, printed bottom down. It is not a closed box, so the top does not become a ceiling that needs supports.
  - The front opening runs to the top, and the front plate slides down into grooves. This avoids a bridge of about 120 mm.
  - The top cover is located by a lip and four magnets.
- **Front plate layout:** decided by alignment lines, not by positions.
  - The perforation is a band of 25 × 4 holes across the top of the plate. Its margin is equal on the left, top and right, and the same margin is left below the dial.
  - The left edge of the dial aligns with the left edge of the perforation, the right edge of the last button with its right edge.
  - The dial and the three buttons share one centre line; the labels sit under the buttons.
  - The dial is a low disc (height 8) with one step and one dot as the indicator; the grip ribs are on the back band only.
  - Chamfers are C0.5 throughout.

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down | Off-white |
| front_plate + label_inlay | Front face down (layers 1–2 in another colour) | Silver grey + mid grey |
| top_cover | Top face down | Off-white |
| dial | Front face up (avoids a ceiling under the step) | Off-white |
| button ×2 | Front face down | Dark |
| button_on | Front face down | Accent |

---

## 07 hinged_case — a box with an opening lid

- **Rationale for dimensions:** 96×64, body 24 mm + lid 8 mm (3:1). Knuckle length 12 mm, gap 0.4 mm, 5 knuckles.
- **Mechanism:**
  - The pin hinge axis lies on the line where the back face meets the parting line. Checked to be free of interference from 0 to 110°.
  - The knuckles are cylinders with a 45° web joining them to the wall. Neither the body side (printed upward) nor the lid side (printed downward) needs supports.
  - Two magnets at the front hold it closed. The lid lip runs only along the front and sides (at the back it would block the rotation).
- **Details:** a shallow round finger scoop straddling the front seam is the one worked-out detail. Its radius is 0.75 × the lid height, so it does not reach the rim of the top face.
- **Pin:** insert 1.75 mm filament and flatten both ends with heat.

## 08 power_bank — sliding lid, snap and connector window

- **Rationale for dimensions:** 120×64×24. The button sits at a quarter of the length. The LED holes are spaced on the 4 mm grid pitch, and the end of the row is 2 pitches from the button.
- **Print strategy:** the body prints top face down, open at the bottom. The bottom lid prints outer face down.
- **Mechanism:**
  - The bottom lid slides in from the +X side along dovetail rails. The rails are made by adding 1.68 mm to the inside of the wall.
  - A 45° bump on a cantilever tab of the bottom lid drops into a groove in the partition wall and holds. The partition is full height, so no bridge forms even when printed upside down.
  - The +X end of the bottom lid follows the outline, so when closed it looks like part of the body.
- **Connector:** the USB-C window is a 12×6.4 horizontal stadium (adjust it to the outline of your connector). LED holes are Ø1.6 (a rough minimum that does not close up on FDM).

## 09 wall_unit — a wall-mounted unit

- **Rationale for dimensions:** front 84 square, depth 16. The margins above and beside the window and below the button are all 22 mm.
- **Mechanism:**
  - The bracket has two keyholes. The head relief channels are on the wall-side face, open towards the build plate, so they print.
  - The cover is held by two 45° hooks on the bracket. Being 45°, it comes off when pulled (for battery changes).
  - The hooks, pads and grooves are all shaped to need no supports in their print direction.
- **Window:** a smoked (or clear) PETG window with a flange, fitted from behind.
- **Details:** the back is set 1.2 mm inward and joined with 45°, making a shadow line against the wall (the same technique as the plinth of 03 tray).

## 10 lantern — stacked materials

- **Rationale for dimensions:** 64 square. Base 48 + diffuser 64 + cap 16 = 128 (2:1).
- **Composition:** three tiers: an opaque base, a translucent diffuser tube (1.68 wall = 4 lines, for an even glow), and a cap. The seams are V lines with C0.5 on both sides.
- **Mechanism:**
  - The slide switch runs in a vertical slot. As an elongated vertical hole, its top bridge is only as long as the slot width. The middle of the travel aligns with the middle of the base height.
  - Two parts: an inner carrier and an outer knob. The carrier goes in from inside, and the knob is press-fitted onto it.
- **Accent:** the slide knob (the one point with a functional meaning).

## 11 split_riser — larger than the bed

- **Rationale for dimensions:** 400×200×80, plate thickness 12. The inner corners of the legs are R12, the outer corners R16. The bottom ends of the legs that stand on the ground stay flat, with only a chamfer and Ø10 rubber feet.
- **Print strategy:**
  - Each half prints on its side with the profile (L shape) on the bed (print height 200 mm).
  - The large flat plate is printed standing vertically, so it does not warp.
- **Joint:** three Ø4 steel dowels and glue. The dowel holes are horizontal, so they are teardrops.
- **Details:** with C0.5 on both sides, the seam becomes a V line and reads as one intended line running through the centre.
- `dowels_steel_ref` (× 3) are bought steel dowels, shown for fit only: they have no print STL.

## 12 threaded_jar — screw-on lid

- **Rationale for dimensions:** Ø80, body 64 + lid 16 (4:1). Total height and diameter are both 80 mm. Threads: pitch 4, thread height 1.2, flanks 45°.
- **Print strategy:**
  - The body prints standing up; the lid prints top face down. Both threads have 45° flanks, so no supports are needed.
  - The step on the inside of the neck is joined with a 45° cone.
- **Mechanism:** the lid thread is offset half a pitch from the body thread. There is a clearance of 0.4 mm radially and 0.45 mm axially on each side.
- **Details:** the lid has the same outer diameter as the body, so when closed they form one cylinder. Knurling only on the upper band; the band at the seam stays plain.

---

## Areas not covered yet

These 12 do not cover the following. Each needs separate study.

- **Freeform handheld items** (shavers, mice and the like): outside the scope of this rule system.
- **Waterproofing and sealing:** needs gasket grooves or O-rings.
- **Devices that need cooling:** needs ventilation calculations.
- **Moulding with flexible materials in one piece:** TPU living hinges and the like.
- **Moving mechanisms other than threads:** gears, cams, latches and the like.

---

## Guidelines for adapting

- **To change the size:** rewrite the dimensions at the top of each function, without breaking the proportions and grid relationships. A 2:1 object, for example, stays 2:1 when scaled.
- **Values to keep fixed:** do not change the wall `T=2.52`, the chamfer `CH=0.5` or the clearance `GAP=0.25`.
- **Reusable pieces:**
  - `knob_local()`: knob
  - `button_local()`: button
  - `feet()`: rubber foot recesses
  - `chamfer_rim()`: chamfer the rim of a circular counterbore
  - `fillet_at()`: put a radius only on the given corner
  - `teardrop_x()`: horizontal teardrop hole
  - `stadium_x()`: horizontal window for USB-C and the like
  - `thread_solid()`: threads with 45° flanks
