# 062 Sorting tray with handle notches

A tray for sorting screws, washers and small parts, 144 × 96 × 32. Two dividers across and one along split the inside into three
columns and two rows of equal cells; the cells' floor edges and corners are rounded R3, so a fingertip sweeps the last screw out of a
corner. Each long wall has a U notch at its middle, as wide as the tray is high and half as deep: the fingers go in over the wall at
the notch and the thumb stays outside, so the tray lifts level out of a drawer or off a crowded bench. One part on a floating plinth.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 144 × 96 × 32, R12 | 3 : 2 in plan, height = depth / 3; 36 × 24 modules; R12 is 12.5 % of the depth |
| Walls, dividers, floor | 2.52 (T), 1.68 (DIV), 2.4 | Six and four lines; one floor plate |
| Cells | Three equal columns × two equal rows (45.2 × 44.6 inside) | Equal cells for equal kinds of part; the dividers stop 4 below the rim, as in the sample tray |
| Cell corners and floor edges | R3 | The small radius of the inside; a fingertip sweeps a screw out of a corner |
| Outer cells' corners at the outline | R9.48 (= R12 − T) | Concentric with the outline, so the wall is even round the corner |
| Notches | Semicircle R16 centred on the rim of each long wall, at x = 0 | 32 wide = the tray's height, down to half the height; inside the middle column, clear of the cross dividers by 6.6 |
| Plinth | 2.4 high, set in 1.2 with a 45° face | Floating base, the same as the sample tray |
| Edges | C0.5 on the rim, the notches (both faces of the wall) and the divider tops; C0.6 at the bed | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| tray | Bottom down | Off-white |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| tray | The notches were not cut at all: the cutting tool was extruded away from the wall (the rendering showed a plain rim) | Defect | One cylinder through the +Y wall, mirrored to the −Y wall; checked in the rendering and by the edges at the notch |
| tray | The divider tops were left square while the rim had C0.5 (`chamfer()` on the divider edges failed) | Violation | A 45° prism cut along each divider top edge, ending at the crossing divider (the method of the sample tray) |

Dos and Don'ts: one visible chamfer value; three radii by role (R12 outline and its concentric R9.48, R3 inside, R16 notch); the notch
stays inside the long wall and does not reach a divider or a corner; no accent (nothing has a function to point at); the notches are the
one worked-out detail, with C0.5 on both faces of the wall.

Use cases:
- **Sort:** six cells of 45 × 45 take a handful of screws each; the dividers 4 below the rim let a full cell be seen from the side.
- **Take out the last part:** the R3 floor edges and corners guide a fingertip or a magnet to the screw.
- **Lift:** two fingers of each hand go in at the notches over the 2.52 wall, the thumbs outside; the notch bottoms are at half the height,
  so the hold is low and the tray stays level. The notch edges have C0.5 on both faces.
- **Place:** stands on 12895 mm² inside the plinth (140.5 × 92.5).
- **Print:** bottom down, no supports. The notches are open at the rim, so there is no bridge; the semicircle's sides are steepest near the
  rim and meet the bottom gently.

verify.py: valid, watertight, one solid; contact area 12895 mm².

Compared with well-known products in this style: none of them is a tray; they are housings with controls and grilles.
Divided trays with hand notches are a common kind of object; no product was used as a model.

Safety: the tray has no batteries, LEDs, magnets or heat of its own. It is not meant for food.

Not verified:
- Not printed on a real printer.
- How much a full tray of steel parts weighs in the hand: 2.52 walls pinched at the notches are fine for a few hundred grams; for heavier
  loads, print with more perimeters.
- The small marks where the divider-top chamfers meet at the crossings (0.5 deep) on a real print.
