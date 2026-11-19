# 026 Cable box for a power strip

A 240 × 96 × 96 box (5 : 2 in plan, a square section) that hides a power strip and its plugs. The cover is a sleeve with a top, printed
top face down; the strip sits on a base plate, and the cover lifts off it, located by a lip on the plate. Each end of the cover has a
U-slot for the cords that runs to the bottom edge, so in the print it is open at the top and needs no bridge; the lip is cut where the
slots are, so the cords lie flat on the plate. A field of Ø2.4 holes on the top lets warm air out; its margin is 40 on every side, so
the field is a band along the middle. No accent.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Box | 240 × 96 × 96, R12 | 5 : 2 in plan, a square section; R = 12.5 % of 96; 240 fits a 256 bed |
| Inside | 234.96 × 90.96, 91.2 high over the plate | A strip up to 210 × 48 × 36, with room for upright plugs and their bends |
| Wall, top, plate | 2.52, 2.4, 2.4 | 6 lines; 12 layers |
| Lip | 1.68 × 4, 0.25 clearance, C0.5 lead-in | The Location rule |
| Cord slots | 16 wide, 24 high with a round top, both ends | Grid 4; the strip's own cord at one end, the device cords at the other |
| Vent field | Ø2.4 at pitch 4, 41 × 5 holes, margin 40 on every side | The perforation rule; equal margins make it a band; with the end slots low, warm air rises out of it |
| Rubber feet | 4 × Ø10.2 at x ±100, y ±32 | Inside the bed chamfer |
| Chamfers | C0.5 at the seam (V line) and top edge of the plate; C0.6 on the bed sides | One visible value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| cover | Top face down | Off-white |
| base | Bottom down, as used | Off-white |
| power_strip_ref | Bought part, not printed | — |

## Review

Defects and violations: none found. Checked against 03_dos_donts.md chapters 1–6: one plan radius and its concentric insides, one
visible chamfer value, equal margins round the vent field, the seam is one V line, no accent, the slots run to an edge.

Use cases:
- **Set up:** lay the strip on the plate with its cord through one slot position and the device cords through the other, then lower the
  cover over it; the lip locates it (swept: lifts free, stops 0.3 down and 0.4 sideways in X and Y).
- **Hold, lift:** grip the cover across its 96 width; nothing holds it down but its weight.
- **Place:** stands on the full plate with four rubber feet; ground contact 22216 mm².
- **Heat:** the end slots let air in low, the field of holes lets it out at the top.
- **Print:** cover top face down (the slots open upward, the holes are in the first layers), plate bottom down; no supports. The 240
  long cover may warp in PETG or ASA: use a brim.

verify.py: cover and base valid and watertight, no interference (the strip included), fit a 256 bed.

Compared with well-known products in this style: they are radios, a pocket radio and a calculator; this is a closed
storage box with no controls. Cable boxes of this shape are common; no product was used as a model.

Safety (electricity, heat): printed PLA, PETG and ASA are not flame-retardant. Use a certified power strip with overcurrent protection,
do not load it near its rating or put high-power chargers or heaters inside, keep the vent field and the slots clear, and do not cover the
box. PLA softens at about 55–60 °C, so use PETG or ASA.

Not verified:
- Not printed on a real printer.
- How warm the inside gets with chargers plugged in (not measured).
- Whether the slots take all your cords (16 wide holds about four Ø5 cords).
