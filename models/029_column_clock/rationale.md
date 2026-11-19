# 029 Column clock

A Ø96 × 64 column (3 : 2) lying on its side: the round end is the dial, the back is a round lid that screws in flush. The body prints
dial down, so the dial is the bed face and its 12 bars are inlaid in the first layers, as in 015. The lid uses the 45° flanked thread of
12_threaded_jar (pitch 4, half-pitch offset, 0.4 clearance) turned inside out: the thread is on a boss behind the lid and inside the
body's mouth, so the lid sits inside the back face and the column stays one cylinder, unbroken by a cap. The boss bottoms on a ledge,
which sets the lid flush; a coin in the slot turns it. A 16 wide flat along the bottom keeps the column from rolling. One accent: the
12 o'clock bar.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Column | Ø96 × 64 | Diameter : depth = 3 : 2; Ø96 is the smallest grid size whose bore passes the movement's 79.2 diagonal past the thread |
| Dial plate | 2.4 | A movement bushing clamps up to about 5 |
| Bars | 4 × (2.4 × 10), 8 × (1.2 × 5), ending 6 inside the rim | 2 : 1 both ways, as 015 at this size |
| Hands | hour 2.4 wide to 27.75, minute 1.6 wide to 37 | The minute hand reaches the inner ends of the minor bars; hour = 0.75 of it |
| Thread | pitch 4, depth 1.2, 45° flanks; body 1.75 turns (root = the bore, 45.48), lid 1.5 turns (root 43.88) | 12_threaded_jar; 0.4 radial clearance both ways, half-pitch offset, 0.8 axial play |
| Lid | plate Ø90.16 × 2.4 in the bore (0.4 clear), boss 12 long, 2.52 wall | Flush in the back face; the boss guides the lid straight before the thread catches |
| Ledge | Ø82 inside, flat on top, 45° underneath, 0.1 under the boss | Stops the lid flush; prints upright without support; passes the movement |
| Coin slot | 24 × 2.4 × 1.2 | A coin or a flat screwdriver turns it |
| Flat | 16 wide, 0.67 deep | Stops rolling; the wall there keeps 1.85 (the bore is concentric) |
| Chamfers | C0.6 on the dial edge and the lid face (bed faces), C0.5 on the back rim and the mouth | One visible value at each end |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Dial face down | Off-white |
| dial_marks_inlay | Inlaid in the dial (multi-material) | Dark grey |
| dial_top_mark_inlay | Inlaid in the dial (multi-material) | Accent |
| lid | Outer face down | Off-white |
| hand_hour, hand_minute | Flat | Dark grey |
| movement_ref | Bought part, not printed | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| body | The first ledge was a cone with its flat face underneath, a 4.5 wide ring overhanging in the print | Defect | Flat on top for the boss, 45° underneath |
| hand_minute | Taken from the minor bar width it was 1.2 wide: three lines, too fragile to press onto the movement shaft | Defect | 1.6 (four lines) |

Use cases:
- **Read:** bars only, two dark hands, the accent at 12; nothing else on the dial.
- **Battery, set the time:** unscrew the lid with a coin, reach through the Ø82 opening to the movement's battery and knob, screw the lid
  back until it stops on the ledge (swept: the thread holds it, it stops 1.5 out and 0.3 in, 0.6 sideways).
- **Place:** stands on its 16 × 64 flat; ground contact 1038 mm².
- **Assemble:** the movement goes in from the back and clamps to the dial with its own nut; then the hands press on.
- **Print:** body dial down, lid face down, hands flat; no supports (the thread flanks and the ledge are 45°).

verify.py: all parts valid and watertight, no interference (the movement included), fit a 256 bed.

Compared with well-known products in this style, including small travel alarm clocks: the travel alarms are small square
or round cases with numerals and a coloured second hand; this is a column on its side with bar indices, an accent at 12 instead of on a
hand, and no second hand. No product was used as a model.

Safety (battery): the movement takes one AA cell. Keep the lid screwed in where small children are; remove the cell if the clock is
stored, and do not use a leaking cell.

Not verified:
- Not printed on a real printer.
- The thread is checked only by sliding the lid along its axis (it holds) and by the half-pitch offset; turning it in was not simulated.
- Movements differ: check the shaft thread, the hand holes and the 56 × 56 × 16 size against yours before printing.
