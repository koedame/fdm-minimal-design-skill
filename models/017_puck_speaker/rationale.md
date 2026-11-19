# 017 Puck speaker

A low Ø96 × 48 cylinder for a 50 mm full-range driver: body 32 and a screw-on lid 16 whose top is a dense field of small holes. The
threads are those of 12_threaded_jar, so the body prints upright and the lid top face down without supports. The driver faces up
under the holes; it sits on three posts standing from the floor, and a ring under the lid top holds it down when the lid is screwed
home. The lid is the one dark part, as a grille.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Speaker | Ø96 × 48 | Height = half the diameter, grid 4 |
| Body : lid | 32 : 16 | 2 : 1; the seam sits on the smooth band of the lid, the grip ribs above it |
| Wall | 2.52 body, 2.4 lid wall, floor and top | 6 lines; 12 layers |
| Neck | thread root Ø88, 45° shoulder inside | 2.4 lid wall + 1.2 thread + 0.4 clearance under the outer radius (as 007); the shoulder prints upright |
| Thread | pitch 4, height 1.2, 45° flanks, 2 turns | As 12_threaded_jar; lid thread offset half a pitch, 0.4 radial clearance |
| Perforation | Ø2.4 holes at pitch 4 within Ø44 | The perforation rule; the field covers the driver cone and no more |
| Driver | Ø52 frame, top 4 under the lid top | A common 50 mm driver; set `FR`, `FT` and the basket to yours |
| Posts | 3 × Ø4 at r 24, 0.05 under the frame | Under the frame rim, outside the basket; vertical in the print |
| Ring | Ø52, 1.68 wall, 0.25 over the frame | Holds the driver down; a 1 mm foam gasket on the frame takes up the gaps and seals it |
| Grip | 64 ribs 1.0 × 0.8 on the upper 8.5 of the lid | As 007; the band at the seam stays smooth |
| Cable hole | Ø4.4 teardrop at the back, 8 up | A speaker cable; the teardrop apex points up in the print |
| Rubber feet | 4 × Ø10.2 at ±24 | Inside the bed chamfer |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down, as used | Off-white |
| lid | Top face down | Dark grey |
| driver_ref | Bought part, not printed | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| body | The cable hole was on the −X side, in full view from the front left | Violation | Moved to the back (+Y) |

Use cases:
- **Assemble:** solder the cable to the driver through the back hole, stick a 1 mm foam ring on the frame, set the driver on the three
  posts and screw the lid on. Hold the driver while the lid makes its last quarter turn, so the ring does not twist it on the wires.
- **Listen:** the holes face up; the body is closed except for the cable hole.
- **Place:** stands on four rubber feet; the cable leaves at the back.
- **Print:** body bottom down, lid top face down; the threads and the shoulder are 45°, and the posts and the ring stand vertically.

verify.py: both printed parts valid and watertight, no interference (the driver included), fit a 256 bed, ground contact 6739 mm²
over Ø94.9.

Compared with well-known products in this style: they are boxes and a pocket radio; none is a low cylinder with a
screw-on perforated lid. Round perforated speakers are a common form; no product was used as a model.

Safety (electronics): this is a passive speaker. If an amplifier or a battery is put inside, use certified modules, keep the battery
away from the driver magnet's heat and from the threads, and do not leave a charging battery unattended.

Not verified:
- Not printed on a real printer.
- How the threads engage on a real print (settle with a test ring).
- How it sounds: the closed volume (about 0.25 l) suits small drivers only, and the field of holes has not been measured.
