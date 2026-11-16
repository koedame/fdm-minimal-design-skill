# 018 Wall sconce

A half cylinder (Ø96, 48 deep) on the wall in three tiers, as 10_lantern cut in half: an opaque base 48, a translucent diffuser 64
and a cap 16, 128 tall. The base hangs on two keyholes in pads on its flat back; the tiers stack on lips. A slide switch runs in a
vertical slot in the middle of the curved front of the base, and its knob is the one accent.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Sconce | Ø96 half cylinder, 48 deep, 128 tall | Depth = radius; height = 4 × 32 |
| Base : diffuser : cap | 48 : 64 : 16 | 3 : 4 : 1, as 10_lantern; the light band is the largest |
| Wall | 2.52 base and cap, 1.68 diffuser | 6 lines; 4 lines for an even glow |
| Floor, cap top | 2.4 | 12 layers |
| Lips | 1.68 wall, 0.25 clearance, 3 high | As 10_lantern; the diffuser sits on the base lip, the cap on the diffuser |
| Keyholes | 2 × at ±24, entry Ø8.4 20 up, slot 4.2 rising 8 | Half the width apart; a pan-head screw (head ≤ 8) goes in the entry and the lamp drops 8 onto the shank |
| Keyhole pads | 16 wide, 6 deep inside the back wall | 2 mm ledge for the screw head, a 3 mm pocket behind it for the head |
| Slot | 3 wide, 11 long, centred on the base height | Mid-travel at mid-height (the slide switch rule); the top bridge is 3 long |
| Switch travel | 8 | A common miniature slide switch |
| Neck | Ø2.5 round | Slot width − 2 × clearance |
| Knob | 10 × 20, 2.4 thick, curved with the wall, 0.25 off it | 20 = 11 slot + 8 travel + 1: covers the slot at both ends of the travel |
| Cable hole | Ø6 in the floor, 12 from the wall | The USB cable leaves downward along the wall |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| base | Bottom down, as used | Off-white |
| diffuser_translucent | Bottom down | Translucent white |
| cap | Top face down | Off-white |
| slider_carrier | Plate down, neck up | Dark grey |
| slider_knob | Front (convex) face down | Accent orange |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| slider_carrier | The neck was too long and ran through the base wall beside the slot (verify: 7.95 mm³ interference) | Defect | Neck length from the carrier face to 1.8 inside the knob |
| slider_knob | The neck hole went through the knob and showed as a dot on its face | Violation | Blind hole, 0.55 skin left on the face |
| slider_knob | At 18 tall the knob left 0.5 of the slot showing at each end of the travel | Violation | 20 tall (slot length + travel + 1) |

Use cases:
- **Hang:** drive two pan-head screws 48 apart, heads 4 mm proud of the wall; set the entries over the heads and let the lamp drop 8.
  The back is flat and stands on the wall over its whole width.
- **Switch:** the knob moves 8 mm up and down; the carrier inside forks over the lever of a small slide switch (for example SS-12D00)
  that you mount on the inside of the base wall below it. Down is off.
- **Assemble:** push the carrier's neck out through the slot from inside, press or glue the knob on, then set the LED module, the
  switch and the USB lead in the base. The diffuser and cap lift off their lips to reach them.
- **Print:** base bottom down (the keyhole entries have 45° roofs, the head pockets round tops, the slot a 3 mm bridge); diffuser
  bottom down; cap top face down; carrier on its plate; the knob on its convex face, which is a shallow arc (2.6 high in the print)
  and needs a brim or glue stick to stay down.

verify.py: all printed parts valid and watertight, no interference, fit a 256 bed, ground contact 3450 mm² on the base; the knob
slides +8 mm along the slot against the base with 0 overlap.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a light. Half-cylinder wall lights are a common
form; this one follows 10_lantern's tiers and was not modelled on a product.

Safety (light, electronics, wall mounting): this sconce holds an LED module and a switch powered over USB. Use a certified USB power
supply and LED module, use LEDs only (no filament or halogen bulbs: the parts are PLA/PETG and soften from about 60 °C), keep the LEDs
at least 10 mm from the diffuser, and do not run mains voltage inside it. Hang it on screws in a stud, or in plugs or plasterboard
anchors made for your wall, not over a bed or a cot; the hold of the printed keyholes has not been tested, so pull the lamp down by
hand before you leave it.

Not verified:
- Not printed on a real printer.
- The position of the real slide switch under the carrier (match it to the switch you use).
- How evenly the 1.68 diffuser wall glows with a given LED module.
- Whether the knob, printed on its curved face, keeps its curve and stays on the bed without a brim.
