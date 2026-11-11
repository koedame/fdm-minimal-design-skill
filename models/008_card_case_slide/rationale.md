# 008 Card case with a sliding lid

A case for business cards whose lid slides out through the right end. The lid runs in a 45° dovetail on three sides of the
top, rests on a ring inside the walls, and clicks shut over a low ridge on the end wall. The top is one flat face: the lid sits
flush with the walls behind a 0.25 reveal.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Case | 102 × 68 × 24 | 3:2 plan; holds 91 × 55 cards (Japanese size; 85 × 55 fits too) |
| Plan radius | R8.5 | 12.5% of 68 |
| Wall / floor | 2.52 / 2.4 | 6 lines |
| Inside | 96.96 × 62.96, 18 deep under the lid | About 50 cards; 2–3 mm around them for the fingers |
| Lid | 3.6 thick: 2.4 straight, then a 1.2 × 45° dovetail | The top is flush with the walls |
| Wall lip over the dovetail | 1.2 | The upper half of the dovetail; 3.72 of wall shows round the lid |
| Clearance | 0.25 square to every face (0.35 in plan on the 45° faces) | Lid moves 0.25 down onto the ring and 0.35 up into the lip |
| Lid seat | 2.4 ring with a 45° underside inside the walls | The dovetail only stops lifting; something has to carry the lid |
| Detent | 0.4 ridge across the end wall, 0.8 V-groove under the lid | The lid lifts 0.15 over it, inside its 0.35 of play |
| Thumb dent | 8 × 20 × 1.2, 10 from the open end | Where the thumb pushes the lid out |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down, as used | Off-white |
| lid | Bottom down, as used (the 45° dovetail narrows upward) | Off-white |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| body | Nothing carried the lid: its dovetail sat inside the line of the walls, so it could drop into the case | Defect | 2.4 ring with a 45° underside under the lid's edge |
| body, lid | The detent ridge and groove were built 2 mm long instead of across the end (found by sliding the lid in the check) | Defect | Built across 40 of the end |

Use cases:
- **Open:** push the thumb dent toward the open end; the lid lifts 0.15 over the ridge and slides out.
- **Close:** slide the lid in until it stops on the left end; it clicks over the ridge.
- **Take a card:** with the lid off, cards come out from the top; 2–3 mm of room round them.
- **Print:** both parts bottom down; the lip and the seat ring have 45° undersides; no supports.

verify.py: both parts valid and watertight, no interference, fit a 256 bed, ground contact 6688 mm² over 100.9 × 66.9 mm.
Slide check (lid moved against the body, with a short script, since verify.py only sweeps hinges): along the slide, 0 mm³
at the closed position, 0.88 mm³ (the ridge under the lid) from 1 to 60 mm out, free at 100; 0.3 further in, 5 mm³ (the stop).
Down 0.25 free, 0.3 on the ring; up 0.3 free, 0.4 against the lip.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a case; a box with a sliding lid is a generic
form, and no product was used as a model.

Not verified:
- Not printed on a real printer.
- How firmly the 0.15 detent holds and how freely the lid slides on real layer lines.
