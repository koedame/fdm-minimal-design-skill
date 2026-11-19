# 047 Laptop stand, set of two

Two identical stands that tilt a laptop 15° for typing and raise its back for air. Each is a single side profile — a right triangle
with its slope on top — 192 deep, 60 high at the back and 32 wide, open in the middle so it reads as three 8 wide members round a
triangular window and a solid block at the front. One stand goes under each side of the laptop; the laptop lies on the two slopes and
its front edge sits against a 6 lip square to the slope. The stands print lying flat, so every member is laid down along its length.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Stand | 192 deep × 60 high × 32 wide | 192 < the depth of a 13–15" laptop (about 210–250), so it does not stick out in front; fits a 256 bed lying flat |
| Slope | From 12 high at the front to 60 at the back: 48 / 180 = 14.9° | A usual typing tilt; low enough that the laptop's weight presses it onto the lip, not off it |
| Lip | 6 square to the slope, at the front | Higher than the thinnest laptop edges (about 4); below the keyboard |
| Members | 8 wide; the window's corners R2 | Grid 4; 32 = 4 members wide |
| Front block | Solid to 48 from the front | Where the front of the laptop and the wrists press |
| Outer corners | R2, except the lip's root | The root stays square so the laptop's edge sits fully in it |
| Width | 32 | A sideways push tips a stand only past about 0.44 × its load (16 / 36, at the slope's mean height), above the friction between laptop and stand (about 0.3), so the laptop slides first |
| Spacing | Free; the example puts them 200 apart under a 300 wide laptop | Outside the laptop's middle, where the vents usually are |
| Edges | C0.5; C0.6 on the bed face | One chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| stand × 2 | On its side (the profile on the bed) | Off-white |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| stand | The lip's root was filleted R2 with the other corners: the fillet lifted the laptop's square front edge out of the corner (an interference with the laptop) | Defect | The root stays square; only the convex corners are rounded |
| stand | 24 wide, a stand tipped sideways at about 0.33 × its load, close to the friction (about 0.3) that a sideways push on the laptop passes on | Defect | 32 wide: about 0.44 |
| design | The example laptop was returned as a ref part, so `size_mm` and the catalogue showed the laptop's size (300 × 220), not the stands' | Defect | `laptop()` builds it without returning it; the review checked it against the stands (below) |

Use cases:
- **Set up:** stand the two stands on the desk, slope rising toward the back, about two thirds of the laptop's width apart; lay the
  laptop on them with its front edge against both lips (swept: it lifts off freely, slides up the slope freely, and stops 0.3 down
  the slope against the lips).
- **Type:** the keyboard tilts 15°; pressing keys pushes the laptop down the slope onto the lips.
- **Carry:** the two stands lie side by side, 192 × 60 × 64.
- **Print:** each on its side; no supports, no bridges (the window is a hole through the part lying flat).

verify.py: all parts valid and watertight, one solid each, no interference, fit a 256 bed. The example laptop from `laptop()`
(300 × 215 × 16) against the two stands with `verify.motion_check`: no overlap at rest, lifting 0 / 5 / 30 and sliding up the
slope 0 / 20 / 100 free, 0.3 down the slope 97 mm³ (the lips stop it).

Compared with well-known products in this style: radios, a calculator and a loudspeaker; none is a stand. Laptop stands
of two wedges are a common kind of object; no product was used as a model.

Not verified:
- Not printed on a real printer.
- Whether the stands creep on a smooth desk while typing; a strip of rubber tape under each stops it.
- The load: a laptop of about 2 kg is assumed; leaning on the laptop with the arms was not calculated.
