# 053 Coaster set with holder

Four square coasters that stack in a low square holder. The holder is a 96 × 96 × 20 cup on a floating plinth; its inside locates
the coasters with 0.25 clearance all round, and two shallow R16 arcs cut into opposite walls give a finger and thumb the stack, down
to the top of the first coaster. Each coaster is a 4 mm plate with a 0.8 deep drip recess inside a 4 mm rim. Coasters dark grey,
holder off-white: closed, the set reads as a dark square inside a light frame.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Holder | 96 × 96 × 20, R12 | 24 × 24 × 5 modules; R = 12.5 % of the outline |
| Plinth | 2.4 high, 1.2 inset, 45° | The floating plinth; the floor is the same 2.4 |
| Holder wall | 2.52 (T) | One wall thickness |
| Coaster | 90.46 square, R9.23, 4 thick | The holder's inside less 0.25 clearance per side, concentric radius; 4 = one module, so four make 16 |
| Stack | 4 × 4 = 16, top at 18.4 | 1.6 below the rim: the rim stands proud of the top coaster as one thin line |
| Drip recess | 0.8 deep, inside a 4 rim | Two layers of 0.4; the rim is one module wide; catches condensation from a glass |
| Finger arcs | R16, centre 2.4 above the rim, 31.6 wide at the rim | Reach down to 6.4, the top of the first coaster; kept 2.8 above the plinth's 45° face |
| Edges | C0.5, C0.6 at the bed | One visible chamfer value, on the rims, the recess and the arcs |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| holder | Bottom down | Off-white |
| coaster ×4 | Top face up (its visible face has the recess) | Dark grey |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| holder | With the arcs centred on the rim (down to 4), the C0.5 on their outer edge ran into the plinth's 45° face (2.4 to 3.6) and CadQuery could not build the chamfer | Defect | Arcs centred 2.4 above the rim, down to the top of the first coaster (6.4): a reason for the depth, and 2.8 clear of the plinth |
| coaster | The recess and outer rim took C0.3 while the holder took C0.5 | Violation | C0.5 on the coasters too |

Dos and Don'ts: one visible chamfer; three radii (R12 holder, R9.48 / R9.23 concentric inside and coaster, R16 arcs; the plinth's
R10.8 is the outline set in); dark grey is the secondary colour, no accent (nothing to point at); the arcs stay inside the side faces.

Use cases:
- **Place:** the plinth stands flat, 8457 mm² of contact.
- **Take a coaster:** pinch the top coaster at the two arcs and lift (swept: the stack is free 10 and 30 mm up; it stops at 0.4
  sideways against the walls and at 0.2 down on the floor). The arcs reach the second coaster too.
- **The last coaster:** it lies below the arcs; tip the holder over a hand and it drops out (0.25 clearance all round, nothing holds it).
- **Put back:** wet coasters stack on each other; water that runs off collects on the holder's floor, so dry them first.
- **Use:** a glass stands inside the 82.46 recess; drips stay in the 0.8 recess.
- **Print:** holder bottom down, the arcs open at the top; coasters top face up, recess open upward. No supports.

verify.py: valid, watertight, one solid per part, 4 separate coasters, no interference.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a tray or a coaster; the dark plate in a light
frame is a general contrast of secondary and body colour, not any product's layout. Coaster sets in a holder are a common kind of
object; no product was used as a model.

Safety (heat): PLA softens from about 55 °C. A mug of hot tea or coffee can mark or warp a PLA coaster; print the coasters in PETG or
ASA if they will take hot drinks, and do not put a pot or kettle on them.

Not verified:
- Not printed on a real printer.
- Whether a coaster sticks to a wet glass and lifts with it (a light coaster does; cork or felt under it is the usual answer).
- Warping of a 90 mm plate printed flat in the material you choose.
