# 021 Square tea caddy

A 72 × 72 × 120 caddy for loose tea: body 96 and a lid 24 (4 : 1). The body's wall steps in at the top into a neck that the lid
slides over with 0.25 clearance, which is the lip of the Location rule turned the other way: the lid keeps one even wall, and a 45°
cone inside the body joins the step, so the body prints upright without support. The lid sits on the shoulder of the wall, flush
with the body, and the seam is one V line. The bottom steps in 1.2 on a 45° face, so the caddy stands on a shadow line. The lid is
the one dark part; there is no accent, because nothing on a caddy needs one.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Plan | 72 × 72, R8 | Grid 4; R = 11 % of the outline |
| Height | 120 = body 96 + lid 24 | Body : lid = 4 : 1; total : width = 5 : 3; both on the grid |
| Wall | 2.52 body and lid, 2.4 floor and lid top | 6 lines; 12 layers |
| Neck | 66.46 outside, 1.68 wall, 12 high | The lid's inside (66.96) less 0.25 per side; `DIV` as a lip; half the lid height of engagement |
| Step inside the wall | 1.93 on a 45° cone | 0.25 + 1.68 of the neck; 45° so the body prints upright without support |
| Lid cavity | 21.6 deep | Clears the 12 neck; the lid bears on the shoulder of the wall, not on the neck |
| Plinth | stepped in 1.2 at 45°, 2.4 high | As 03_tray: the shadow line under the body |
| Seam | C0.5 on both edges | One V line at 4 : 1 |
| Opening | 63.1 square | The neck inside: a tea scoop and a hand's fingers go in |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down, as used | Off-white |
| lid | Top face down | Dark grey |

## Review

Defects and violations: none found. The form was checked against 03_dos_donts.md chapters 1–6 (one chamfer value where visible,
C0.6 only on the print-bed edges; one plan radius and its concentric insides; equal walls; no accent; the seam is the only line).

Use cases:
- **Open, close:** the lid lifts straight up; it is located over the full 12 of the neck and catches sideways at 0.4 (swept below).
- **Fill, scoop:** the 63.1 opening takes a tea scoop; the inside corners are concentric with the outline.
- **Keep:** with 0.25 clearance the lid is not airtight. Keep the tea in its sealed bag inside the caddy, or settle a tighter fit on a
  test ring of the neck (0.1–0.15 per side) if the lid should seal by friction.
- **Place:** stands on the 68.5 square plinth; the centre of gravity is over the middle of it.
- **Print:** body bottom down (the neck stands up, the step is a 45° cone), lid top face down (open side up); no ceilings, no support.

verify.py: both parts valid and watertight, no interference, fit a 256 bed; ground contact 4652 mm² over 68.5 × 68.5.
Motions: the lid lifts free over 0–13 mm, stops on the shoulder (0.3 down: 167 mm³ overlap), and the neck catches it sideways at
0.4 in X and Y (free at 0.2).

Compared with well-known products in this style: they are radios, a pocket radio and a calculator; none is a
container. A square caddy with a flush lid is a common form; no product was used as a model.

Safety (food): printed PLA or PETG is not certified for food contact, and layer lines hold dust and oils. Keep loose tea in a
food-grade bag or liner inside the caddy, do not put wet leaves in it, and clean it dry.

Not verified:
- Not printed on a real printer.
- How tight the lid feels on the neck with 0.25 clearance (settle with a test ring of the neck).
- Whether the 72 × 120 body stays square at the top when printed (thin walls can pull in at the corners).
