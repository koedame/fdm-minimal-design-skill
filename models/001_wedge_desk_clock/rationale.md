# 001 Wedge desk clock

A square clock face leaning back on a wedge. The body is a tube square to the face, cut flat by the desk
and by a vertical back, so every wall rises straight from the bed when it is printed face down.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Slope | rise 96, run 28 | A 7:24:25 right triangle × 4, so the face is exactly 100 long (73.7° from the desk) |
| Face | 100 × 100 | Width = face length: the face is a square |
| Face corner radius | R12 | 12% of the face; the same as the dial margin, so the dial is concentric with the corners' arcs |
| Dial | Ø76 × 2.4 | Face 100 − 2 × 12 margin |
| Depth on the desk | 48 | Grid 4; the smallest that keeps a 56 × 56 × 16 movement clear of the back plate |
| Total height | 96 | The rise of the slope; the top slopes down 16.3° to the back, square to the face |
| Wall, back plate | 2.52 | 6 lines |
| Index bars | majors 2.4 × 8, minors 1.2 × 4 | 2:1 in width and in length; all end 4 (grid) inside the dial rim |
| Hands | hour 2.4 wide to r22, minute 1.2 wide to r30 | Widths = the two bar widths; the minute hand ends on the inner end of the minor bars, the hour hand 4 inside the majors |
| Magnet bosses | Ø10 at x ±36, 24 up the face | Clear of the movement (±28) and of the wall; pocket Ø6.2 × 3.2 for 6 × 3 magnets |
| Lip of the back plate | 1.68 × 4, clearance 0.25 | Location rule of `02_rules.md` |
| Accent | none | A clock without a second hand has no part whose function needs pointing at |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Face down (the walls rise square to the bed) | Off-white |
| back_plate | Outer face down | Off-white |
| dial | Front face down | Light grey |
| dial_marks_inlay | Layers 1–2 of the dial, in another colour | Dark grey |
| hand_hour | Flat | Dark grey |
| hand_minute | Flat | Dark grey |
| movement_ref | Reference only, do not print (a 56 × 56 × 16 quartz movement) | Dark grey |
| magnets_ref × 4 | Bought: 6 × 3 disc magnets | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| back_plate | The plate reached the desk as well as the body, so a lip that sat 0.25 off would rock the clock | Defect | The plate stops 0.25 above the desk; only the body stands (ground contact 100 × 44.5) |

Use cases:
- **Place:** the body stands on its whole bottom wall, 100 × 44.5; the centre of gravity of the leaning face stays over it.
- **Fit the movement:** it goes in through the back opening and its shaft through the Ø7.6 hole at the centre of the face; the nut clamps the face wall and the dial (2.52 + 2.4 = 4.9 mm). Choose a movement whose thread takes that stack.
- **Change the battery:** pull the back plate off its two magnets; the lip locates it again.
- **Print:** the body face down needs no supports: the walls are vertical, the bottom wall leans 16°, the bosses stand vertical and their magnet pockets lean 16°.

verify.py: all parts valid and watertight, no interference (the movement reference included), every part fits a 256 bed,
ground contact 100.0 × 44.5 mm.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2, and the BC and AB alarm clocks): those clocks are small square
or round cases with numerals and a coloured second hand; this is a 100 mm leaning slab with bar indices on a raised disc and
no second hand. No product was used as a model.

Safety: the clock runs on a battery-powered quartz movement. Use a certified movement and battery; the printed parts are not
certified for anything.

Not verified:
- Not printed on a real printer.
- The fit of the magnets, the lip and the shaft stack on a real movement (movements differ; check yours).
- Whether the 1.2 mm minute hand is stiff enough in PLA.
