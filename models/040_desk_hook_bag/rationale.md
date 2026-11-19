# 040 Desk bag hook

A hook for a bag, hung under the edge of a desk: 32 wide, 56 deep, 60 down. It is one J, its top a block that lies against the
underside of the desk and its round bottom 60 below, where the strap rests. The hook hangs on a plate screwed to the underside of the
desk; the plate's section is a 45° dovetail, and the pocket in the hook's top is open at the back and closed at the front, so the hook
is pushed back onto it from the desk edge and covers the plate and both screws. Seen from the chair, the front of the hook is a whole
face. The hook prints lying on its side, so every layer is a complete J.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Hook | 32 × 56 × 60 | Top block 56 deep (holds the 48 plate and a 3.75 front wall), J 40 deep and 60 down |
| Top block | 16 thick, its front 4 behind the desk edge | The pocket (4.25) and 4 under it for the locking screw's head seat |
| Arm, tip | 12 thick | 3 modules; the J carries the bag |
| Strap seat | 16 wide, round bottom R8 | A bag strap or handle up to about 16 |
| Opening | 20 high over the tip, under the top block | The strap goes in from the front over the tip |
| Fillets | R12 on the J's two outer bottom corners, R3 on the tip's top edges (4 of straight under them) | The J reads as one bend; nothing to catch the strap |
| Desk plate | 48 long, 4 thick, 12 wide at the desk, 20 at the bottom (45° flanks) | Bag load hangs on the flanks |
| Pocket | Plate + 0.25 normal to every face, open at the back | Clearance between parts |
| Wood screws | 2 × 4 mm countersunk, 24 apart | Into the underside of the desk |
| Locking screw | M3 × 8 from below, Ø3.4 clearance, Ø6.2 counterbore, into a Ø2.5 pilot through the plate | Keeps the hook from sliding forward off the plate |
| Edges | C0.5, C0.6 on the bed side | One chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| hook | On its side (the left face down) | Off-white |
| desk_plate | Desk side down | Off-white |
| (2 × 4 mm countersunk wood screw, 1 × M3 × 8 screw) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| hook | The first description had the hook sliding forward onto the plate; with the pocket closed at the front it can only go on backward from the desk edge, and the motion sweep showed it (overlap 230 mm³ sliding back) | Defect (wrong assembly direction) | Description and motions corrected: on backward, off forward, the locking screw holds the forward direction |

Use cases:
- **Mount:** screw the plate to the underside of the desk, its long side square to the edge, its front 8 behind the edge. Push the
  hook back onto it from the edge until it stops (swept: free forward to 70, stops 0.5 back, 0.5 down, 0.5 up and 0.5 sideways), then
  drive the M3 screw up through the hook into the plate.
- **Hang a bag:** slip the strap in from the front over the tip; it drops into the round bottom.
- **Load:** a hanging bag pulls straight down, under the plate; the dovetail's flanks carry it. A strap pulled toward the chair is
  held by the locking screw alone.
- **Remove:** take out the M3 screw and pull the hook forward off the plate; the plate stays.
- **Print:** hook on its side, no supports (the pocket's flanks are 45°, the screw hole is a teardrop pointing up); plate flat.

verify.py: hook and plate valid and watertight, no interference, fit a 256 bed.

Compared with well-known products in this style: radios, a pocket radio, a calculator and a loudspeaker; none is a
hook. Under-desk bag hooks are a common item; no product was used as a model.

Safety (load): the hook's strength has not been calculated or tested, so it has no rated load. It depends on the material (PETG; PLA
creeps under a bag left hanging for days), on printing the hook on its side as given, on the walls and infill, and on the desk: drive
the wood screws into solid wood or a solid board thick enough for them, not into a glass, metal, hollow-core or thin-panel top. Before
you hang a bag, pull down on the hook by hand, harder than the bag weighs; check from time to time that the plate screws are still
tight.

Not verified:
- Not printed on a real printer.
- The weight the hook takes before it bends; print in PETG and keep to an everyday bag (about 5 kg).
- The locking screw is driven from below with a screwdriver at least about 80 long (the J is below it).
