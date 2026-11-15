# 02 Design rules (with numbers)

Design rules for FDM (0.4 mm nozzle, 0.42 mm line width). With resin printing most of the constraints relax.
**Every number is a rule of thumb: neither an official standard of any manufacturer nor a value confirmed on real prints.** Settle fits, snaps and threads with test pieces.

Contents
1. Base constants
2. Form and dimensions
3. Colour, labels and materials
4. Details
5. Print orientation
6. Structure
7. Mechanisms and joints
8. Dimension cheat sheet
9. Modelling notes (CadQuery)

---

## 1. Base constants

The same values as the sample code (`scripts/fdm_samples.py`).

| Name | Value | Meaning |
|---|---|---|
| `T` | 2.52 mm | Outer wall (line width × 6) |
| `DIV` | 1.68 mm | Dividers, lips, rails (line width × 4) |
| `CH` | 0.5 mm | **The only visible chamfer value** |
| `CH_BED` | 0.6 mm | Edges on the build plate side (against elephant's foot) |
| `GAP` | 0.25 mm | Reveal / clearance (per side) |
| Grid | 4 mm | The basis for outlines, pitches and positions (5 mm is fine for some objects) |

---

## 2. Form and dimensions

- **Large radii in plan, sharp edges.**
  - Plan radius: about 8–16% of the outline (e.g. outline 100 → R12–16)
  - Edges: C0.5 (C0.6 only on the build plate side)
- **At most 2–3 radii, one per role.** Examples of roles:
  - Outline corners (large)
  - Inner corners and grooves (small, R2–3)
  - Inner corners that carry load (medium, around R10)
  - Ends of plates floating in the air (nearly full round, R ≈ plate thickness / 2)
- **Ends and faces that touch the ground stay flat.** Chamfer only; no full round (a full round touches the ground along a line).
- **Derive every dimension from the grid or a ratio.** Example ratios: 2:1, 3:2, 4:1, total height = diameter.
- **Align elements to reference lines.**
  - Let them share a top edge, bottom edge or centre line.
  - Relate the dimensions of elements to each other (e.g. dial diameter = distance between the centres of the outer buttons).
- **Margins with the same role get the same width.** The frame of a front plate, the surround of a window, the margin of a perforation field, and so on.
- **Unify plate and wall thicknesses within an object.**
- Limit forms to what extrusions, cuts and revolutions can make. No freeform surfaces.

## 3. Colour, labels and materials

| Item | Rule |
|---|---|
| Body | Off-white or light grey. Not pure white |
| Secondary | Dark grey |
| Accent | One colour, one place. Only on a part with a functional meaning: power, second hand, a switch. If no function deserves emphasis, leave it out |
| Labels | Tiny, sans-serif, **a light to mid grey close to the background colour** |
| Functional indication | Indicators and windows may be dark (to tell them apart from labels) |
| Material changes | Switch by face (an aluminium-look front plate, a translucent layer and so on) |
| Filament | Matte. Glossy PLA shows layer lines |

## 4. Details

- **Keep most of it plain and work out only a few spots precisely.** Decide one to three "this is where the effort goes" spots per object.
- **Perforation:** small holes in a dense array. On vertical walls, cut vertical slots with semicircular ends instead of round holes.
- **Reveal lines:** a seam between parts should be one intended line.
  - When made with a gap: 0.25 mm per side.
  - With C0.5 on both parts, it becomes a V-shaped line.
- **Dials:** one step between the rim and the top face; one line or one dot as the indicator. Put grip ribs only on a band at the back side.
- **Buttons:** repeat one shape; show differences with colour.
- **Floating plinth:** set the bottom 1.2 mm inward and join it with 45°; the shadow line makes the object look as if it floats (trays, wall-mounted units).
- **Keep recesses (finger grips and the like) inside the face they belong to.** Do not cut into the rim or chamfer of the neighbouring face.
- **Do not show fasteners.** Use screws on the back or bottom, magnets and snaps.

## 5. Print orientation

- **Principle: the visible face goes on the build plate.**
- **Exception: a part whose visible face has steps or recesses prints with the visible face up** (a stepped dial, for example).

| Kind of part | Orientation |
|---|---|
| Housing (with large radii in plan) | Bottom down (the radii lie in the layer plane) |
| Front plate, face plate, window | Visible face down |
| Lid, top plate | Top face down |
| Button (flat top) | Front face down |
| Dial (stepped top) | Front face up |
| Objects whose side profile is the design (stand, L shape) | Side down (lying on its side) |
| Large flat plate | Stand it up (no warping) |

## 6. Structure

- **Do not make closed boxes.** Make the body a sleeve and the lid or top plate a separate part.
- **Run large openings in a wall all the way to the top** (a U-shaped cutout). Slide the front plate in from above.
- **Stand posts and bosses vertically (in Z).** A horizontal boss is an overhang.
- **Make horizontal holes teardrops** (apex pointing up in the print). Small holes (Ø2 or less) may stay round.
- **Give the underside of projections (flanges and the like) 45°.**
- **Join steps on the inside of walls with a 45° cone** (the neck of a container, for example).
- **Split anything larger than the bed.** Place the seam as a design line (in the centre, on a reference line and so on).
- **A bottom plate between walls that lean inward toward the top** (a front that leans back): the opening narrows over the
  plate's thickness, so a plate cut to the outline at the bottom runs into the leaning wall at its top edge. Make it shorter
  on that side by thickness × the slope of the wall (horizontal / vertical; 2.52 × 0.25 = 0.63 for a wall leaning 14°).

## 7. Mechanisms and joints

| Mechanism | How to make it | Samples |
|---|---|---|
| Location | A lip (a step on the inside of the wall, `DIV` thick) on one part fits inside the other. Clearance 0.25 | 06, 07, 10 |
| Magnets | A Ø6.2 × 3.2 deep pocket in a vertical post (for 6 × 3 mm magnets) | 06, 07 |
| Hidden screws | A counterbored hole through the bottom, into a pilot hole (Ø1.8 for M2) in a vertical boss of the other part | 02 |
| Pin hinge | Put the axis on the line where the back face meets the parting line. Knuckles are a circle + 45° web. The pin is 1.75 mm filament (hole Ø1.9). Check interference at each opening angle. **Place the stop where the load is:** a stop that touches only near the axis multiplies the load on it by (loaded arm ÷ distance of the stop from the axis), tens of times for a leg loaded at its far end, and the pin and knuckles take it. Let the moving part bear on the stop at a distance from the axis comparable to the loaded arm (a heel or a ledge it leans on). **A lid is the exception:** its open stop can only be near the axis (knuckle against web), so it is fit for the lid's own weight only; say so in the use cases ("do not lean on the open lid"), or let the open lid rest on the table | 07 |
| Sliding lid | A dovetail of about 45° on both sides. Add a rail to the inside of the wall and cut the groove into it. **The dovetail only keeps the lid from lifting:** give the lid a seat from below as well (a ring inside the walls with a 45° underside, so it prints without supports), or the lid drops into the box | 08 |
| Snap (tab) | A U-shaped slit frees a cantilever tab; a 45° bump drops into a groove in the other part. Put that groove where it does not become a bridge (at the end of a full-height wall) | 08 |
| Snap (hook) | A vertical hook (`DIV` thick) with 45° barbs above and below. Being 45°, it comes off when pulled (for battery changes) | 09 |
| Slide switch | A vertical slot. Two parts, an inner carrier and an outer knob, press-fitted or glued. **Make the neck that runs in the slot round** (its diameter = the slot width − 2 × clearance): a square neck catches its corners on the round ends of the slot before it reaches the end. **Make the knob cover the slot at both ends of the travel:** knob length along the slot ≥ slot length + travel + 1, and a blind neck hole in the knob (no dot on its face) | 10 |
| Screw lid | Threads with 45° flanks (pitch 4, thread height 1.2). Offset the mating thread by half a pitch, with 0.4 radial clearance | 12 |
| Split joint | Steel dowels (Ø4, hole Ø4.2, teardrop) + glue. C0.5 on both sides of the seam makes it a V line | 11 |
| Wall mounting | Keyholes (head Ø8.4, slot width 4.2). Cut the head relief channel into the wall-side face (the build plate side) | 09 |
| Light, windows | Give the window part a flange and fit it from behind. Make the diffuser layer a separate part with a 1.68 wall | 09, 10 |
| Connectors | USB-C: a horizontal stadium window (about 12 × 6.4; match the outline of the connector you use). **The receptacle face sits within about 2 mm of the outside:** a plug's moulding is larger than a window sized to the receptacle and stops at the wall, so set the board 0.25 behind the wall and thin the wall to 1.68 from the inside around the windows; a receptacle further back needs a window that admits the moulding | 08 |

## 8. Dimension cheat sheet

| Item | Value |
|---|---|
| Perforation holes | Ø2.2–2.5, pitch 4, wall between holes 0.8 or more |
| Holes that let light through | Ø1.6 (a rough minimum that does not close up on FDM) |
| Vertical slots | Width 1.6, semicircular ends |
| Clearance between parts | 0.25 per side |
| Button holes | Button diameter + 0.6 |
| Inlay / engraving depth | 0.4 |
| Label text height | About 3 at minimum |
| Magnet pocket | Ø6.2 × 3.2 (for 6 × 3 magnets) |
| Rubber foot recess | Ø10.2 × 1 deep |
| D-shaft hole | Ø6.1, flat 1.55 from the centre |
| Potentiometer bushing hole | Ø7.2 |

## 9. Modelling notes (CadQuery)

Things the code does without saying so, found while building models with `scripts/fdm_samples.py`.

- **Shell first, then chamfer and fillet the edges.** `shell()` on a solid whose edges are already chamfered fails
  silently in CadQuery and returns the solid unchanged (still solid inside). Check the volume after shelling.
- **Several copies of one part (qty > 1): build the assembled shape with `copies()`, not with a union.** A union fuses
  copies that touch (stacked trays, a pin in a row) into one solid, and the tools can no longer tell the copies apart;
  `verify.py` reports it.
- **Bought parts** (a movement, a driver, steel dowels) shown for fit: `Part(asm, None, colour, ref=True)`. They are checked
  for interference with the printed parts, but get no print STL and no place in the print layout.
- **Features on a sloped face:** build them in the XY frame with the usual helpers (local y up the slope, +Z out of the
  face) and move them with `on_slope(shape, tilt, origin)`; `tilt` is the angle of the face from the desk.
