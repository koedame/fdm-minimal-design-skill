# 002 Vented sensor box

A small upright box for a room sensor (temperature, humidity, air quality) on a microcontroller board.
Air comes in through slots in the bottom plate and leaves through a slot field on each side, so the sensor
reads room air rather than the warmth of its own board. The top and the front stay plain.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Plan | 48 × 48 | Grid 4; inside 43 × 43 takes a board up to about 40 × 40 |
| Height | 72 | 3:2 to the plan |
| Plan radius | R6 | 12.5% of the plan |
| Wall, top, bottom plate | 2.52 | 6 lines, one thickness throughout |
| Side slots | 7 × (1.6 × 48), pitch 4 | Vertical slots with round ends on vertical walls; 12 margin above and below |
| Intake slots | 7 × (1.6 × 24), pitch 4 | The same pitch and width as the sides, half the length |
| Status LED hole | Ø1.6 on the front, at the height of the slot tops | Smallest hole that stays open; aligned to the slot field's top line |
| USB-C window | 12 × 6.4 stadium, 4 above the plate, 12 right of centre on the back | Clear of the back rib; match your connector |
| Plate inset | 1.2 | Only the rim stands on the desk; the plate never carries the weight |
| Snap | tab 6 × 1.68 × 14, bump 0.8 at 45° | Bending strain about 1% in PLA at full deflection (1.5 × 1.68 × 0.8 / 14²) |
| Ribs | 8 × 2.52, full height | Stops for the plate and seats for the grooves; full height so the upside-down print has no ceiling |
| Accent | none | Nothing on the outside is a control |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Top face down (open bottom up) | Off-white |
| bottom_plate | Outer face down, tabs up | Off-white |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| body | The bump of the snap met the square bottom end of the rib, with nothing to push it aside | Defect | 1 mm 45° lead-in on the rib end |
| body | The bottom rim was chamfered inside and out, which left a ring 1.5 mm wide to stand on (190 mm²) | Violation | Inner edge left square (it is never seen); ring area 352 mm² |

Use cases:
- **Place:** the rim stands, span 47 × 47; the plate is 1.2 clear of the desk.
- **Open:** a fingernail or coin in the notch at the back right pries the plate; both faces of the bumps are 45°, so it comes out when pulled and snaps back when pushed.
- **Assemble:** the board goes in from below on the plate (fix it with double-sided foam tape or add bosses for your board); the cable goes through the USB-C window.
- **Print:** body upside down: walls and ribs vertical, grooves are 45° triangles, the USB-C window bridges only its 5.6 mm flat; plate face down with vertical tabs.

verify.py: both parts valid and watertight, no interference, fits a 256 bed, ground contact 352 mm² over 47.1 × 47.1 mm.

Compared with well-known products in this style: none of them is a small upright vented box; the slot fields
are vertical, plain-walled and not arranged like any of their grilles. No product was used as a model.

Safety: this box holds electronics powered over USB. Use a certified power supply; the printed parts are not certified for anything.

Not verified:
- Not printed on a real printer.
- How firmly the snaps hold and how often they can be opened.
- Whether the slots give enough air for the sensor you use (no airflow calculation was made).
