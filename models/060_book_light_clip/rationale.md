# 060 Book light clip

A reading light that clips onto the top edge of a book cover. The body is one profile, 30 wide: a U clip with a thin front jaw that
flexes, and a neck that rises to two knuckles. The back jaw holds a CR2032 holder with its own switch, pressed in from the back. A
56 long head hangs on the middle knuckle; under its own weight it leans forward until its underside lands on the clip's front top
edge, 29.5° down, and the light shines down and back onto the page. The head is a tray: its window part (a translucent diffuser with
a flange) and the LED board go in from above, and a cover plate is glued into a seat in the top. The pin is 1.75 mm filament.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Width | 30, all parts | The CR2032 holder (26) + two 2 walls |
| Clip gap | 3.0 wide, 28 deep; a 0.6 bump with 45° faces at 4 from the tip | Grips covers about 2.4–3.4 thick; at 3.0 the jaw bends 0.6: about 9 N in PETG (3EIδ/L³, L 24) |
| Front jaw | 2.4 thick | Flexes 0.6–1.0 at 0.3–0.5 % strain |
| Back jaw | 11 deep (y 3–14); holder pocket 26.5 × 8 × 22.5, open at the back, 45° roof | The holder's switch faces the back; the roof prints without support |
| Lead-in | 45° × 1.2 on the back jaw's tip | The cover finds the gap |
| Hinge | Axis 12 above the clip, 9 behind its front; knuckles R5, gap 0.4, pin hole Ø1.9 | Head clear of the clip at rest; the body has the two outer knuckles (9.6), the head the middle one (10) |
| Notch between the body's knuckles | Down to z 34.8 | The head's root swings down to 35.3 when it rests |
| Head | 56 × 30 × 12, floor 2.4, walls 2.52 | One plate and one wall; long enough to put the light over the page |
| Rest angle | 29.5° down; the head lands on the clip's front top edge, 14 from the axis | The stop takes the head's weight away from the knuckles |
| Window | 18 × 6 in the head floor, 46 from the axis | Under the LED board |
| Diffuser | Plug 17.5 × 5.5 × 2.4, flange 1.2 all round, 1.2 thick | Fitted from behind, its face flush with the floor |
| Cover seat | 1 wide ledge, 2.4 deep | The cover plate (2.4) sits flush in the top and is glued |
| Wires | Ø3 holes: head floor near the hinge, and the body from the notch to the holder pocket | The pair loops through the gap under the hinge |
| Edges | C0.5; C0.6 on the bed faces | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Upright, jaws down (the bridge over the 3.0 gap is the only bridge) | Off-white |
| head | Floor down | Off-white |
| head_cover | Outer face down | Off-white |
| diffuser_translucent | Flange down | Translucent white |
| led_board_ref, battery_holder_ref, pin_ref | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| body / head | The notch between the body's knuckles stopped at the knuckles' radius; the head's root ran into the neck from 5° down (83 mm³ at rest) | Defect | Notch down to z 34.8; swept: free from 0 to 29.5°, stops at the clip's front edge |
| body | The profile's corners along the width (jaw tips, bridge, back) were left sharp | Violation | C0.5, C0.6 at the jaw tips on the bed |
| diffuser | Coloured as an accent, and drawn flange up: the flange would print as a 1.2 overhang | Defect | Translucent white, printed flange down |
| body | The lead-in was first drawn in the gap, not on the back jaw, and left a sliver that broke the chamfers | Defect | 45° lead-in cut from the back jaw's tip |

Dos and Don'ts: one visible chamfer; one radius (the knuckles' R5); the window is the only opening on the head's underside; the
switch is on the holder at the back; no visible fasteners; no accent colour.

Use cases:
- **Clip on:** push the clip down over the top edge of the cover (the back jaw's lead-in finds it); the bump presses the cover against
  the back jaw.
- **Read:** the head rests 29.5° down on the clip's front edge and lights the page below and in front (swept: free from the rest up
  through 229° back; 1° further down it is on its stop).
- **Carry:** swing the head back over the hinge; it rests on the back of the clip, 20–30° below horizontal behind it (swept: free to
  −229° from the rest, stops by −241°). The window then faces up.
- **Switch:** the holder's switch is on the back face of the clip.
- **Change the battery:** pull the holder out of its pocket backward (it is held by friction; a spot of glue on one side if loose).
- **Assemble:** drop the diffuser into the window from above, the LED board on its flange, glue the cover into its seat; run the pair
  of wires from the head's floor hole into the notch and down to the holder; push the filament pin through the three knuckles.
- **Print:** body upright, jaws down: the gap's bridge is 3 wide, the knuckles stand on the neck, the pocket's roof is 45°; head floor
  down with the window on the bed; cover outer face down; diffuser flange down. No supports.

verify.py: valid, watertight, one solid per part, no interference, fits a 256 bed. Its ground-contact line refers to standing the clip on
a table; in use it hangs on the cover.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a clip light. Clip-on reading lights are a common kind
of object (usually on a gooseneck); this one is a block clip with a rigid head that rests on a stop. No product was used as a model.

Safety: a CR2032 coin cell and an LED. **Keep coin cells away from children: a swallowed coin cell can cause severe internal burns within
hours.** The holder here is pressed in and its cell is reachable; use a holder whose cover locks (screw or latch), and keep the light out
of children's reach. The LED board must have its own current-limiting resistor; it runs cool.

Not verified:
- Not printed on a real printer.
- The grip of the front jaw in PETG on real covers, and whether it marks them.
- The head stays only at its rest angle (the pin hinge has no friction); the light's aim is set by where the clip sits on the cover.
- CR2032 holders with switches differ in size; change `BAT` to match.
