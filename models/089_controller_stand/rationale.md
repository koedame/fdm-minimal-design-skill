# 089 Controller stand

A wedge 100 deep, 72 wide and 67 high on which a game controller lies face up at 30°, its lower edge in the corner of a front lip, so it
stays on show and in reach on a desk or a shelf. In the right-hand side of the wedge, behind a flush cover held by two pairs of 6 × 3
magnets, is a small store for the controller's wireless dongle or a short coiled cable. The stand is one profile printed on its side,
like the stand sample.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Footprint | 100 deep × 72 wide (25 × 18 modules) | A controller is about 153 × 104 × 61; it overhangs both sides, so its grips can be taken from either side |
| Seat | 30° from horizontal, from z 20 at the lip to z 67 at the back | The controller lies with its face toward the viewer and its weight on the seat; buttons and sticks touch nothing |
| Lip | 8 thick, its inner face square to the seat and 10 high | A controller's end is square to its back: a vertical lip would run 5.8 into it at the top (see Review); 10 holds its edge without hiding the face |
| Lip corner | R2 | Small, so the controller's edge sits right in the corner |
| Free ends | R3.8 (lip top, back top, the two bottom edges) | Near a full round of the 8 thick lip, as in the stand sample |
| Store | Recess 50 × 24 × 4.4, R3.8; pocket 32 × 24 × 12 below it; 13 above the table, 6 from the back | Holds a USB dongle or a 30 cm cable coiled to about Ø25; in the lowest, thickest part of the wedge |
| Cover | 49.5 × 23.5 × 4.15, R3.55 (concentric), 0.25 clearance, flush | The recess less the clearance; C0.5 on its outer edges and a C0.5 flare on the recess outline make one V line |
| Magnets | 2 + 2 × Ø6 × 3 in Ø6.2 × 3.2 pockets at the recess's ends, beyond the pocket; 0.95 of the cover over each | Take no room from the store; both sets of pockets open upward in the print (stand on its side, cover outer face down) |
| Fingertip scoop | R7 into the recess's upper edge | Where a fingertip lifts the cover against the magnets |
| Edges | C0.5 on the right-hand side and the cover; C0.6 on the bed face (the left-hand side) | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| stand | On its left side (the profile on the bed) | Off-white |
| cover | Outer face down | Off-white |
| magnet_ref (4 × Ø6 × 3 neodymium discs) | Bought, glued | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| stand × controller | Checked against an envelope of the controller (104 × 61 lying on the seat): with a vertical lip the controller's square end ran into the lip, 2008 mm³ | Defect | The lip's inner face is square to the seat; the seat's front end moved back 5 to keep the lip 8 thick. 53 mm³ remain: the envelope's sharp corner in the R2 fillet, where a real controller is rounded |
| stand | Four radii: R3.8 ends, R2 corner, R4 recess, R7 scoop | Violation | The recess takes R3.8, the radius of the free ends; three radii remain (R3.8, R2, R7) |

Dos and Don'ts: one visible chamfer value (C0.6 only on the bed face); three radii, one per role (R3.8 free ends and recess, R2 the lip
corner, R7 the scoop); plain, with the hidden store as the one worked-out spot; off-white, no accent.

Use cases:
- **Put the controller down:** face up, its lower edge (the grips' end) into the lip's corner, its back on the seat. It stays by its
  weight; the lip takes the part of the weight along the slope (half of it at 30°).
- **Pick it up:** from either side; the stand is narrower than the controller, so both grips stand free.
- **Store the dongle or the cable:** lift the cover at the scoop with a fingertip; the magnets let go once its edge is up. Put the cover
  back the way round its magnets attract (see Safety). With the cover flush, the store does not show from the front.
- **Stability:** the controller's centre of mass lies about 43 behind the front and 57 in front of the back (checked on the envelope), inside the footprint; pressing
  a button pushes it into the seat. Ground contact 6614 mm² over 71 × 94.
- **Print:** on its left side, the profile on the bed, so the seat is a vertical wall (no layer steps on it) and the store's pockets open
  upward; the cover outer face down. No supports. Glue the magnets in after the print.

verify.py: stand and cover valid, watertight; fits a 256 bed; no interference with the magnets; the cover lifts free and stops
sideways at 0.4.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): radios, a pocket radio, a calculator and a loudspeaker; none is a stand.
A wedge with a lip is the common form of a display stand; no product was used as a model.

Safety (magnets): neodymium magnets are dangerous if swallowed (two can pinch through the gut); glue them in with epoxy or
cyanoacrylate, check the polarity before the glue sets (each cover magnet must attract the stand magnet under it), and keep loose magnets
away from children and pets. Keep the stand away from pacemakers and from cards with a magnetic stripe.

Not verified:
- Not printed on a real printer.
- The controller's shape: checked as a 104 × 61 box; a controller whose grips reach further below its back may sit higher on the seat.
- How hard the two pairs of magnets hold the cover through the 0.25 clearance and 0.95 of cover.
