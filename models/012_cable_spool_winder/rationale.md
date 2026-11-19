# 012 Cable spool winder

A small spool for a spare USB or audio cable: two Ø64 flanges on a Ø32 hub. One flange carries the hub; the other locates on it
with a lip inside the hub bore and is glued there. One piece would not print, because the second flange would overhang the hub by
16 mm all round. The cable starts in a radial slot in the first flange, with its connector outside, and its other end is pinched in
a notch in the rim of the second.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Flanges | Ø64 × 2.52 | Grid 4; the flange is one wall thick (6 lines), the same as the hub wall |
| Hub | Ø32, wall 2.52 | Half the flange; a 16 radius is 4 × a Ø4 cable, a common minimum bend radius |
| Overall width | 24 | 8 : 3 against Ø64; 18.96 between the flanges |
| Lip | 4 long, 1.68 wall, 0.25 clearance in the hub bore | The Location rule; it centres the cap while the glue sets |
| Centre hole | Ø23.1 on both faces | The inside of the lip; the same hole through both flanges, and it hangs on a peg |
| Start slot | 4.4 wide, rim to hub, round inner end | A cable up to Ø4 lies in it flush with the flange; ends at the hub surface so the first turn starts there |
| End notch | 3.0 wide, 8 deep, 45° lead-in from 7 | Pinches a Ø3–4 jacket; the lead-in guides it in |
| Edges | C0.5, C0.6 on the bed side | As every part |
| Capacity | about 3.7 m of a Ø3.5 cable | π (32² − 16²) × 18.96 / 3.5² |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| flange_hub | Flange down, hub up | Off-white |
| flange_cap | Outer face down, lip up | Dark grey |

## Review

No defects or violations found.

Use cases:
- **Assemble:** put a thin ring of cyanoacrylate on the lip and press the cap onto the hub; the lip keeps it centred.
- **Wind:** lay the cable in the start slot with its connector outside the hub flange, wind it on, and press the last 10 cm into
  the end notch.
- **Store:** lay it on the cap side (the connector stands out from the hub flange) or hang it on a peg through the centre hole.
- **Print:** both flanges outer face down; the hub and the lip stand up from them, no support.

verify.py: both parts valid and watertight, no interference, fit a 256 bed, ground contact 2573 mm² over Ø62.8.

Compared with well-known products in this style: none of them is a cable spool. A flanged spool is a generic
form; no product was used as a model.

Not verified:
- Not printed on a real printer.
- How firmly the 3.0 notch holds a given cable (jackets differ in diameter and softness).
