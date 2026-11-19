# 099 Salt cellar with swivel lid

A rounded-square pot 72 × 72 × 48 for salt by the stove. Its flat lid swings aside about a vertical pin in the back-right corner: a
finger pushes the lid's front edge to the right and the lid turns about 40°, opening a wedge from the back-left corner wide enough to
take a pinch; pushed back, it stops square over the body. The pin is a piece of 1.75 filament. Two printed parts.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 72 × 72, R10; 48 high (body 43.2, lid 4.8) | 18 × 18 × 12 modules; R10 = 13.9 %; holds about 150 g of salt with room for fingers above it |
| Wall, floor | T (2.52), inner corners R7.48; floor 2.4 | One margin, concentric corners |
| Pin | Ø1.75 filament in Ø1.9 holes at (31, 31): 16 deep in the body (glued), 3.6 deep in the lid from below (1.2 skin over it) | The pin hinge's pin and hole; on the corner's diagonal it has 2.9 of material to the outside; the lid's top stays plain |
| Cavity corner at the pin | R16 (instead of R7.48) | Leaves 3.1 of material between the pin and the cavity |
| Stud | Ø6, 4 below the lid, 67.5 from the pin, touching the left inner wall when closed | One stud gives both stops: the left inner wall closed, the front inner wall at 41.5° open |
| Opening | 41.5° | The lid's centre of gravity stays 8 inside the right wall at that angle, so the lid lies on the rim and does not hang on the pin |
| Edges | C0.5 on the rim (outside and in), the lid's lower edge and the stud's end; C0.6 on the body's bed edge and the lid's top (printed face down) | One visible chamfer value; one V seam round the lid |
| Feet | Four Ø10.2 × 1 pockets for rubber feet | A wet worktop |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down | Off-white |
| lid | Top face down (stud up) | Off-white |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| body | The first cavity had its pin corner rounded with the circle centred on the pin: the pin hole was cut in the cavity, with no material round it | Defect | Pin on the corner's diagonal at (31, 31), the cavity's corner there R16: 2.9 and 3.1 of material either side |
| lid | The first lid opened to 225° with a thumb tab outside the right face as the closed stop. Past about 50° its centre of gravity leaves the rim and the lid hangs on a 3.6-long pin in a 1.9 hole: it tips and the pin's hole wears | Defect | The tab is gone; a stud under the lid stops it closed on the left inner wall and open at 41.5° on the front inner wall, where the centre of gravity is still over the rim. Written into the rules |

Dos and Don'ts: one radius R10 outside (R7.48 inside, R16 only where the pin needs it); one visible chamfer value; one seam; no
visible pin or tab: the lid is a plain square; off-white, no accent.

Use cases:
- **Take a pinch:** push the lid's front-left edge to the right with one finger: it turns on the corner pin and stops at 41.5° with the
  back-left half of the pot open. Push it back: it stops square.
- **Fill:** turn the lid open and pour salt in through the wedge, or lift the lid off the pin (it only rests on it) and fill from a bag.
- **Clean:** lift the lid off; wash both parts by hand in warm water and let them dry completely before refilling: salt cakes in a damp pot.
- **Print:** body bottom down; lid top face down, stud up. No supports. Cut a 1.75 filament piece 19 long, glue it into the body's hole
  with 3 standing proud of the rim, let it set, then drop the lid onto it.

verify.py: body and lid valid, watertight, fit a 256 bed; the lid turns free from 0° to 38°, stops at −0.6° and at 42° (contact at 41.5°),
and rests on the rim.

Safety:
- **Food contact:** print with a filament sold as food-contact grade (many PETG grades are), with a clean nozzle; layer lines hold
  residue, so use it for dry salt only, wash it by hand and replace it if it stains or smells. Not for the dishwasher.
- The pin is plastic on purpose: a steel pin rusts in salt.

Compared with well-known products in this style: radios, a pocket radio, a calculator and a loudspeaker; the record player's lid is a hinged clear cover, not a swivel. A salt box with a lid turning on a corner pin is a common form; no product was used as a model.

Not verified:
- Not printed on a real printer.
- How smoothly the lid turns on its 4.8-wide rim contact with salt grains on the rim.
- Whether the glue holds the filament pin in PETG over months of turning.
