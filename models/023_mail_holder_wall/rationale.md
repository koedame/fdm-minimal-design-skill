# 023 Wall mail holder

A 128 × 160 back plate on the wall with a pocket 32 deep and 80 high in front of its lower half, for letters, postcards and flyers
standing on end. The plate's top corners take R16 and the pocket's front corners R4, one radius for each outline. The back face steps
in 1.2 on 45°, so the plate stands off the wall on a shadow line. The holder hangs on two keyholes cut in pads on the inside of the back
wall, below the top of the pocket: from the front they are behind the pocket wall and the letters, and the outside shows no fastener.
The entries and head pockets have 45° roofs, so the holder prints bottom down, as used, without support.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Back plate | 128 × 160, top corners R16 | 4 : 5; R = 12.5 % of the width; 128 takes a 120 wide envelope (Japanese long no. 3) with 1.5 per side |
| Pocket | 32 deep, 80 high | Depth = a quarter of the width; height = half the plate, so the letters show above it |
| Pocket corners | R4 outside, R1.48 inside | 12.5 % of the depth; the inside concentric |
| Wall, floor | 2.52, 2.4 | 6 lines; 12 layers |
| Shadow line | back stepped in 1.2 at 45° | As 09_wall_unit |
| Keyholes | x ±32 (64 apart), entry Ø8.4 at 40 up, slot 4.2 rising 8 | The wall mounting rule; half the width apart; the holder drops 8 onto the screws |
| Keyhole pocket | ledge 2.0, head pocket 3.0 with a 45° seat, 45° roofs | `keyhole_local()`; prints with the wall face vertical |
| Pads | 16 wide, 6 deep (1.0 in front of the head pocket), up to 64 | Carry the keyhole depth that the 2.52 wall lacks; 16 under the rim, so the front hides them |
| Chamfers | C0.5 rim, plate and pads; C0.6 on the bed; 1.2 at the back | One visible value; the back's 1.2 is the shadow line |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| holder | Bottom down, as used | Off-white |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| holder | The pads inside the pocket had sharp edges, seen from above among C0.5 rims | Violation | C0.5 on their top and front edges |
| skill | No helper for a keyhole: 009, 015 and 018 each wrote their own, and a teardrop entry joined to a stadium pocket made a mesh that was not closed | Skill gap | Added `keyhole_local()` to `fdm_samples.py` (one closed tool with 45° roofs and seat) and used it here |

Use cases:
- **Hang:** put two screws 64 apart in the wall, leave the heads standing 2.5 out, set the entries over them from the front (reach in
  over the pocket rim) and push the holder down 8. The centre of gravity is in front of the wall, so the screw heads pull the plate in
  and the bottom of the plate bears on the wall; the 1.2 step makes the shadow line all round.
- **Put in, take out:** letters stand on end in 26.96 of depth (23.5 at the pads); anything taller than 80 shows above the rim.
- **Print:** bottom down; the walls and pads stand vertically, the keyhole entries and pocket tops have 45° roofs. The plate above the
  pocket is a free 2.52 wall 80 high: print it slowly or with a brim if your printer shakes tall walls.

verify.py: valid and watertight, fits a 256 bed (160 high), ground contact 3832 mm² over 126.9 × 30.3.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none is a wall pocket. A wall pocket for mail is a common form; no
product was used as a model.

Safety (wall mounting): the holder is made for letters, postcards and flyers; its strength has not been calculated or tested, so it
has no rated load and is not for books or tools. How well it holds depends on the material, the print (perimeters, infill) and above
all on the screws and the wall: drive them into a stud, or into plugs or plasterboard anchors made for your wall. Do not hang it over
a bed, a sofa or a cot. Before you fill it, push the empty holder down and pull it away from the wall by hand, harder than a full
pocket would; if a keyhole slips or the plate cracks, remount it or do not use it.

Not verified:
- Not printed on a real printer.
- Whether the keyholes hold on your screws (the head must fit the 8.4 entry and seat on the 45° cone; test on a piece of the pad).
- How far the 160 plate bends when the pocket is full.
