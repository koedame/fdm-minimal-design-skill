# 046 LED candle tube

A Ø56 × 144 column that glows like a candle. A short dark base holds a bought LED tea light on top of its neck; a translucent shade,
a closed tube five times the base's height, screws over it. The column has one line: the seam between base and shade. The threads are
those of 12_threaded_jar, so neither part needs supports. A finger reaches the tea light's switch through a hole in the bottom of the
base, so the shade comes off only to change the cell.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Column | Ø56 × 144 | A slim candle proportion (about 2.6 : 1); Ø56 takes a Ø38 tea light with the thread round it |
| Base : shade | 24 : 120 | 1 : 5; the dark band reads as the candle's foot |
| Neck | Thread root Ø48, 12 high | 4 under the outside, as 12_threaded_jar: 2.4 shade wall + 1.2 thread + 0.4 clearance |
| Thread | Pitch 4, height 1.2, 45° flanks, 2 turns on the base, 2.25 in the shade | As 12_threaded_jar; the shade's thread is offset half a pitch, 0.4 radial clearance |
| Shade wall | 1.68, 2.4 at the thread, 45° step between | The diffuser rule; thicker only where the thread needs it |
| Shade top | 2.4 | 12 layers; printed on the bed |
| Pocket | Ø38.6 × 8 in the neck top | A Ø38 LED tea light + 0.3 all round (check yours) |
| Finger notches | 12 wide × 6 deep, across the neck | Two fingertips lift the tea light out |
| Switch hole | Ø28 through the base to the pocket | A finger reaches the switch under the tea light; the light rests on a 5.3 ledge (an upward step, no overhang) |
| Rubber feet | 4 × Ø10.2 on r 21 | Between the switch hole and the bed chamfer |
| Edges | C0.5; C0.6 on bed faces (base bottom, shade top) | One chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| base | Bottom down | Dark grey |
| shade | Top down | Natural or white translucent PETG |
| tea_light_ref (LED tea light, Ø38) | Bought | — |
| (4 × Ø10 rubber feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| base | LED tea lights switch on their bottom: every switching on or off meant unscrewing the shade and lifting the light out | Defect | A Ø28 hole from below reaches the switch; the tea light rests on a ledge; the feet moved out to r 21 |

Use cases:
- **Set up:** put the tea light into the pocket, flame up; screw the shade on, 2.25 turns (swept: the shade is held by the thread
  1 up and stops 0.3 down on the shoulder; 0.2 radial play).
- **Switch on / off:** tip the column a little and reach the switch through the hole in the bottom with a finger.
- **Change the cell:** unscrew the shade, lift the tea light out by the notches (swept: free straight up, 0.3 radial play).
- **Print:** base bottom down (the thread's 45° flanks, the pocket and the hole need no support); shade on its closed top (the step
  above the thread band is 45°, the internal thread's flanks are 45°). No supports.

verify.py: all parts valid and watertight, one solid each, no interference, fit a 256 bed.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): radios, a calculator and a loudspeaker, all boxes; none is a light or
a column. Translucent LED candle tubes are a common kind of object; no product was used as a model.

Safety (battery, light): **only an LED tea light; never a real candle** — PLA and PETG soften and burn. The tea light runs on a coin
cell: coin cells are dangerous if swallowed, and the screw shade is not a child-resistant closure, so keep the light and spare cells
out of reach of small children.

Not verified:
- Not printed on a real printer.
- How evenly the shade glows: the light sits in the lower third, so the top of the tube stays dimmer (like a candle); the 2.4 band at
  the thread shows a little darker.
- The size of your tea light: change `LIGHT` before printing.
