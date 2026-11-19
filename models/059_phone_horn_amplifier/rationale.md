# 059 Phone horn amplifier

A passive speaker for a phone: a 112 × 64 × 40 block that holds the phone upright, leaned back 1:4, and turns the sound from the
speaker on its bottom edge forward, toward the listener. The phone's back rests on the slot's back wall and its front-bottom corner on
a 45° floor. Along the back of the slot a 6 wide throat runs the full 84 length, so the speaker is over it wherever it sits on the
edge. Under the throat a horn opens forward and downward to an 84 × 12 mouth at the bottom of the front face. The horn is open at the
bottom and the table closes it; that lets the block print top down with no supports.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 112 × 64 × 40, R8 | 14 × 8 × 5 modules; end walls 14 beside the 84 slot; deep enough that a 160 tall phone leaned back keeps its centre over the block |
| Slot | 84 long, 14 wide (horizontal), leaned 1:4; front wall 10 deep | Phones up to about 80 wide and 13 thick in a case |
| Floor | 45°, falling back from the front wall to the back wall (corner at z 18.8) | The phone slides back against the wall; in the top-down print it is a 45° overhang |
| Throat | 6 wide (horizontal) along the back wall, the full slot length, down to z 15 | Covers a speaker up to 6 from the phone's back (an 8 phone in a 2 case); a 7.5 phone's front corner still lands 1.9 past it on the floor |
| Horn roof | From the throat's front (z 15) to the mouth's top (z 12) at the front face | Faces up in the print, so any slope prints |
| Horn floor | The solid under the throat falls forward 0.6 per 1 (59°) to the table | Steeper than 45° as an overhang in the print; the passage widens from 6 at the throat to 12 at the mouth |
| Mouth | 84 × 12 at the bottom of the front face, C0.5 on its edges | The slot's length; the table is its floor |
| Edges | C0.6 on the top face (on the bed), C0.5 elsewhere, including the slot's and the mouth's outlines | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| horn | Top down | Off-white |
| (4 × Ø10 stick-on feet, under the end walls) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| horn | The first throat was cut only from 2 above the floor corner, so the floor left a 45° lip that narrowed its opening to 2.5 | Defect | The throat is cut up through the slot: its opening is the full 6 along the back wall |
| horn | A 5 wide throat missed the speaker of a phone in a thick case (about 6 from the phone's back) | Defect | Throat 6; checked that a 7.5 thick phone's front corner still rests on the floor in front of it |

Dos and Don'ts: one visible chamfer; one radius in plan (R8); two openings (the slot on top, the mouth on the front), both the same
84 length and centred; no accent; no fasteners.

Use cases:
- **Play:** stand the phone in the slot with its screen toward you; its back rests on the back wall and its front corner on the floor
  (checked with phone envelopes 7.5, 8, 10 and 12.5 thick, 76 wide, 160 tall: no overlap at rest; 0.4 lower or 0.4 further back
  they touch the block, so the phone rests on the floor and the wall). The sound goes down the throat and leaves through the mouth.
- **Phones:** the speaker must be on the bottom edge; phones up to about 80 wide in a case fit the 84 slot.
- **Surface:** on a hard table the horn is closed; on a cloth or a bed the bottom of the horn is soft and the effect drops.
- **Print:** top down: the slot opens at the bed, the throat and horn open upward; the floor (45°) and the horn floor (59°) are the
  only overhangs. No supports. Feet go under the end walls, outside the horn.

verify.py: valid, watertight, one solid, fits a 256 bed.

Compared with well-known products in this style: none of them is a phone horn; the loudspeaker among them is a powered speaker. Passive phone
horns are a common kind of object; this one is a plain block with one slot and one mouth. No product was used as a model.

Safety: no batteries, LEDs, magnets or heat; the phone may warm up while playing, which PLA tolerates. Do not charge the phone in it with
a cable forced into the slot.

Not verified:
- Not printed on a real printer.
- The gain of the horn: it is short (about 35 from throat to mouth) and is expected to add a few dB in the mid range, not bass.
- Phones whose speaker is not on the bottom edge (top or front speakers) get little from it.
