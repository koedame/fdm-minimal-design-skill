# 031 Grille cube speaker

A 96 mm cube (R12) for one 2-inch full-range driver. A baffle on a 45° ledge at half height divides it: below is the sealed back
chamber of the driver, above is the front chamber, and its sound leaves through a field of vertical slots on all four faces. The
driver faces up and is screwed to the baffle, which is glued onto the ledge. The top cap snaps on with four vertical hooks that drop
into grooves in posts standing in the four inner corners; the barbs are 45°, so the cap can be pulled off again at a finger scoop
across the seam at the back. The baffle is dark grey, so the slots read as dark lines. No accent: there is no control to mark.

The driver is generic (53 mm square frame, Ø46 cut-out, screw holes 46 apart); set `DRV_*` in `design.py` to yours before printing.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Cube | 96 × 96 × 96, R12 | Width = depth = height; R = 12.5 % of the outline |
| Baffle line | top of the baffle at 48 | Half the height: the slots take the upper half, the back chamber (about 0.34 l, enough to seal a 2-inch driver) the lower half |
| Baffle | 3.36 (8 lines), 0.25 clear of the walls and posts, on a 1.6 ledge with a 45° underside | The ledge prints without support; the baffle is glued for an airtight back chamber |
| Cap | 4 thick, seam at 92, C0.5 on both sides of the seam | The seam is one V line; the cap's top edge is the bed side (C0.6) |
| Slots | 1.6 wide, pitch 4, 15 per face, end centres at 56 and 84 | Vertical slots with semicircular ends on vertical walls; their centre lines lie 8 (two modules) inside the flat of each face, above the baffle line and below the seam: one margin on all four sides |
| Corner posts | inner face 54 from the centre along each diagonal, floor to seam | Outside the slot fields (2.1 clear of the last slot), so a post never covers a slot |
| Hooks | 1.68 thick, 8 wide, 16 long, barb 1.0 at 45°, 0.25 clear of the post, reaching 0.75 into a groove 1.0 deep | Snap (hook) of 09. Long enough to bend 0.75 at about 0.7 % strain; the cap rises 0.5 before a barb catches |
| Finger scoop | R3 (0.75 × the cap), 1.2 deep, centred on the seam at the back | As 07: half in each part, clear of the cap's top edge and 4.2 above the slots |
| Wire hole | Ø4 teardrop, 10 up, in the back | Low, into the back chamber where the driver's terminals are; teardrop because it is horizontal |
| Feet | Ø10.2 × 1 recesses at ±32 | The rubber foot rule, on the 4 mm grid |
| Driver | 53 square frame on the baffle, Ø46 cut-out, M2.5 self-tapping into Ø2.2 pilots at ±23 | A common 2-inch driver; check yours |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down, as used | Off-white |
| baffle | Top face down | Dark grey |
| cap | Top face down (hooks up) | Off-white |
| driver_ref | Bought part, not printed | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| cap | The cap sat flush on the walls with nothing to lift it by; pulling four barbs out of their grooves needs a grip | Defect | A finger scoop across the seam at the back (R3, as 07); to fit it under the slots, the slot fields are measured from the seam instead of the top, so all four margins stay 8 |
| body | The first slot field ran 8 below the top of the cube, so the top margin included the cap and differed from the others in meaning | Violation (03_dos_donts: margins with the same role) | All margins measured from the lines that bound the field: the baffle line, the seam and the flat of the face |

Use cases:
- **Place:** the whole bottom stands on the desk (8558 mm²), with four rubber feet; the driver's weight sits in the centre.
- **Assemble:** solder the wire to the driver, lead it out of the back hole, screw the driver to the baffle, lower the baffle past the
  posts onto the ledge and glue it all round (and seal the wire hole). Press the cap on; the hooks click into the posts' grooves.
- **Open, close:** lift the cap at the finger scoop; the 45° barbs let go (swept: pressed on, the barbs overlap the posts by 17.8 mm³,
  the bend of the hooks; seated, the cap is free, rises 0.5 before a barb catches at 0.6, and is stopped 0.2 down and 0.8 sideways).
- **Print:** body bottom down (vertical slots, vertical posts, 45° ledge and grooves, a teardrop hole); baffle and cap flat, top face
  down; the hooks stand up on the cap with 45° barbs. No supports.

verify.py: body, baffle and cap valid and watertight; no interference with each other or the driver; fit a 256 bed; ground contact
8558 mm².

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): L 2 is a box loudspeaker with a perforated front; this is a cube
that sounds to all four sides through slot fields on its upper half and is closed by a plain cap. The others are radios, a pocket radio
and a calculator. Cube speakers are a common type; no product was used as a model.

Safety: a passive speaker; use it with an amplifier rated for the driver, and keep the wire's joints insulated inside the box.

Not verified:
- Not printed on a real printer.
- The force to press the cap on and pull it off (the hook stiffness is an estimate).
- The sound: the back chamber volume suits a typical 2-inch driver, but the response was not measured.
- That the glued baffle seals the back chamber.
