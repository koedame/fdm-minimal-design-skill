# 015 Wall clock disc

A Ø192 × 20 disc on the wall. The face itself is the dial: twelve bars inlaid in its first layers, the bar at 12 the one accent.
The disc is a shallow dish printed face down, so the face is the smooth bed face, and the open back takes a common quartz movement.
The back steps in 1.2 mm on a 45° face, so the disc stands off the wall on a shadow line. One keyhole in a post at the top hangs it
on one screw.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Disc | Ø192 × 20 | Grid 4; the depth is about a tenth of the diameter, as little as the movement allows |
| Face plate | 2.4 | A movement bushing clamps a dial up to about 5 |
| Rim wall | 2.52, stepping in 1.2 on 45° at the back | 6 lines; the wall follows the shadow line, so it stays one thickness |
| Floating back | inset 1.2, 2.4 deep | The floating plinth rule, turned to the wall: a shadow line all round |
| Bars | 12, majors 3.2 × 16, minors 1.6 × 8 | 2 : 1 in width and length; all end 8 (2 × grid) inside the rim |
| Inlay depth | 0.4 | The inlay rule (two layers) |
| Minute hand | 1.6 wide, reaches r 80 | The width of a minor bar; ends on the inner ends of the minor bars |
| Hour hand | 3.2 wide, reaches r 60 | The width of a major bar; 3/4 of the minute hand (as 01_clock) |
| Movement | 56 × 56 × 16 behind the face, shaft hole Ø7.6 | A common quartz movement; check yours (CLOCK_SHAFT_HOLE, HAND_HOLES) |
| Keyhole | entry Ø8.4 at 64 above the centre, slot 4.2 rising 8, in a 24 × 32 post | The wall mounting rule's sizes; above the movement, on the vertical centre line |
| Keyhole pocket | head pocket 3 deep, 45° seat, 2.0 ledge at the wall | As 009_key_hook_rail: the pocket opens toward the wall, which is up in the print; the 45° seat needs no support and seats a countersunk head |
| Edges | C0.6 on the face (bed side), C0.5 at the wall | As every part |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| disc | Face down (layers 1–2 in other colours) | Off-white |
| dial_marks_inlay | Inlaid in the face | Dark grey |
| dial_top_mark_inlay | Inlaid in the face | Accent |
| hand_hour / hand_minute | Flat | Dark grey |
| movement_ref | Bought part, not printed | — |

## Review

No defects or violations found.

Use cases:
- **Hang:** drive one countersunk screw (head up to Ø8) leaving about 2.5 mm of the head standing off the wall; put the entry hole
  over the head and let the clock drop 8 mm. With one screw above the centre, the clock hangs plumb under its own weight.
- **Against the wall:** only the 2.52 wide back ring and the post touch the wall; the 45° step leaves a shadow line all round.
- **Battery:** lift the clock off the screw; the movement is open at the back.
- **Assemble:** push the movement bushing through the face from behind, fit the washer and nut on the front, then the hour and the
  minute hand.
- **Print:** face down; the rim, the 45° step, the post and the keyhole seat rise from the face without support.

verify.py: every part valid and watertight, no interference (the movement included), every part fits a 256 bed. (The ground contact
line is not meaningful: the clock hangs on the wall.)

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2) and Braun's BC and AB travel alarms: the travel alarms are small
desk cases with a dial set into a frame; this is a wall disc whose face is the dial,
with no bezel, no numerals, no second hand and inlaid bars. A round wall clock is a common form; no product was used as a model.

Safety (battery, wall mounting): the movement takes an AA cell. Use a certified movement, and keep spare cells away from children.
Hang it on a screw in a stud, or in a plug or plasterboard anchor made for your wall, not over a bed or a cot; the hold of the printed
keyhole has not been tested, so pull the clock down by hand before you leave it.

Not verified:
- Not printed on a real printer.
- Whether the Ø192 face stays flat on the bed (the 20 mm rim stiffens it; use a textured plate or a brim if it lifts).
- Whether the hand holes fit your movement (they differ from product to product).
