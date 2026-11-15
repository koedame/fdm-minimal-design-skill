# 030 Pi Zero case

A 72 × 40 × 16 case (9 : 5, R5) for a Raspberry Pi Zero-size board, closed by a lid that slides out through the right end in the 45°
dovetail of 08, on three sides of the top; a low ridge on the end wall clicks into a groove under the lid so it stays shut, and the lid
rests on a narrow ring with a 45° underside. The board's mini HDMI and two micro USB receptacles look out through stadium windows in
the front, its microSD slot through the left end. The board sits 0.25 behind the front and left walls, which are thinned to 1.68 from
the inside along the board, so each receptacle face is 1.93 from the outside and a plug seats fully. Four M2.5 self-tapping screws hold
the board on posts. A field of Ø2.4 holes in the lid lets the warm air out. No accent: the ports are the detail.

The board's outline and holes are the Zero's (65 × 30, holes 58 × 23 apart); the connector positions are approximate. Set `BL`, `BW`, `PCB`, `HOLES`,
`PORTS` and `SD_Y` in `design.py` to your board before printing.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Case | 72 × 40 × 16, R5 | 9 : 5; R = 12.5 % of 40. 40 wide so the 30 board passes between the dovetail lips (32.6 open) and the ring (31.8) |
| Board place | 0.25 behind the thinned front and left walls, on posts Ø6 × 3 | The connector rule: receptacle faces 1.93 from the outside |
| Thinned walls | 1.68 from the inside, the board's length (front) and width (left end), from the floor to under the ring | A plug's moulding stops at the wall; the receptacle must be within about 2 |
| Port windows | receptacle + 0.4 per side, horizontal stadiums: mini HDMI 12.0 × 4.1, micro USB 8.3 × 3.4, microSD 11.8 × 2.2 | Only the flat part of each roof bridges |
| Screws | M2.5 × 5 self-tapping into Ø2.2 pilots 4.6 deep | The board (1.4) and 3.6 of thread in the post and floor |
| Lid | 3.6 thick, dovetail 1.2 at 45°, 0.25 clearance, ring 1.6 | As 08; the ring's tip is 0.45 over the mini HDMI, so the board slides under it |
| Detent | ridge 0.4 on the end wall, groove 0.8 in the lid | As 08 |
| Vent field | 9 × 3 holes Ø2.4 at pitch 4 | The perforation rule; centred between the lid's end and the thumb dent |
| Thumb dent | 8 × 20, 1.2 deep, 10 from the open end | As 08 |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down, as used | Off-white |
| lid | Bottom down, as used | Off-white |
| board_ref | Bought part, not printed | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| body | The board's front-left corner ran into the cavity's corner radius left between the two thinned walls (verify.py: 1.8 mm³ interference) | Defect | The thinned walls meet in a cut-out corner |
| body | The first pilot holes were 3 deep, in the posts only: too short for a common M2.5 × 5 screw through the board | Defect | 4.6 deep, into the floor (0.8 left under them) |
| lid | The first vent field was placed by eye, with unequal margins to the lid's end and the thumb dent | Violation (03_dos_donts: equal margins) | Centred between them |

Use cases:
- **Fit the board:** lower it in at the back right, slide it left and forward until its edges touch the thinned walls (it passes under
  the ring), then screw it down through the open top.
- **Open, close:** push the thumb dent toward the right end; the lid clicks over the ridge and slides out (swept: stops at −0.3, the
  ridge drags 0.44 mm³ under it all the way, free from 70; 0.3 up, 0.3 down and 0.4 sideways are stopped).
- **Plug in:** HDMI, USB and power from the front, the microSD card from the left end through its window (how far the card stands out depends on the socket).
- **Heat:** the holes in the lid let warm air out at the top; keep the lid clear.
- **Print:** both parts bottom down, no supports; the dovetail faces are 45°.

verify.py: body and lid valid and watertight, no interference with the board, fit a 256 bed; ground contact 2736 mm².

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): they are radios, a pocket radio and a calculator; this is a closed
case with ports and no controls. Small single-board computer cases with a sliding lid are common; no product was used as a model.

Safety (heat, electricity): a Zero 2 W under load gets hot; the case has no fan. PLA softens at about 55–60 °C, so print in PETG if the
board runs busy, keep the holes clear, and power it from a supply made for it.

Not verified:
- Not printed on a real printer.
- The connector and card positions are approximate, not measured on a board; check them against yours.
- The temperature of a busy Zero 2 W in the closed case (not measured).
- A board with a GPIO header does not fit under the lid.
