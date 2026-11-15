# 056 Small cube planter

A 64 mm cube for a succulent or a small cutting. Outside a cube with R8 corners in plan; inside a round bore three quarters of the
width, so the top reads as one circle in a square, the only figure on the object. The floor falls 1 : 8 to a drain hole in the centre.
Underneath, a floating plinth carries two crossing V channels, kept inside the plinth's height, that let the water from the hole out to
the four sides onto whatever saucer the cube stands on.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 64 × 64 × 64, R8 | A cube on the 4 mm grid; R = 12.5 % |
| Bore | Ø48 | Three quarters of the width: the circle in the square; leaves 8 at the middle of each side |
| Floor | 9.6 at the bore wall, falling 1 : 8 to 7.0 at the drain | Water runs to the hole; the floor stays 4.6 thick over the plinth at its thinnest |
| Drain | Ø6 through the floor and the plinth, in the centre | One hole where both channels cross; small enough that a stone or a scrap of mesh covers it |
| Plinth | 2.4 high, 1.2 inset, 45° | The floating plinth; also the space the channels live in |
| Channels | Two crossing V channels, ridge at 2.0, 45° sides, 6 wide at the bed | Stay 0.4 inside the plinth, so they open only below the shadow line; the V prints without a bridge |
| Soil | About 98 ml | Ø48 × 54.4 |
| Edges | C0.5 on the rim and bore, C0.6 at the bed | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| planter | Bottom down | Off-white |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| planter | The channels first had 45° roofs above the plinth (ridge at 5.6): their mouths cut notches into the side faces above the shadow line | Violation | V channels with the ridge at 2.0, inside the plinth; the drain hole runs through to the bottom where the channels cross |

Dos and Don'ts: one visible chamfer; three radii (R8 outline, R6.8 plinth = R8 − inset, R24 bore); the side walls are 8 at their
thinnest, not 2.52: the round bore in a square outline is the design, and the corners print as infill (a deliberate exception to "one
wall thickness", which is about walls of the same role); no accent.

Use cases:
- **Plant:** cover the hole with a stone or a scrap of mesh, add a layer of grit, then soil; a small succulent's root ball (up to about
  Ø45) fits.
- **Water:** water runs down the 1 : 8 floor to the hole and out along the channels to the four sides; stand the cube on a saucer or a
  tile, since water leaves under it.
- **Place:** the plinth stands flat, 3159 mm² of contact between the channels.
- **Hold:** lifted by the top: the rim is 8 wide at the middle of each side, chamfered C0.5 inside and out.
- **Print:** bottom down, no supports. The bore is a vertical cylinder; the floor faces up; the channels are V's with 45° sides; the hole
  is vertical.

verify.py: valid, watertight, one solid, fits a 256 bed.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a planter; a circle in a square is a general figure
and appears on none of them as the main element. Cube planters with a round bore are a common kind of object; no product was used as a
model.

Safety: no batteries, LEDs, magnets or heat. Not for edible plants unless the filament is suitable for contact with food and soil water;
PLA slowly degrades when kept wet and warm.

Not verified:
- Not printed on a real printer.
- Whether water stands in the layer lines of the floor instead of running to the hole.
- How long PLA lasts in constantly damp soil; PETG is the safer choice for a planter.
