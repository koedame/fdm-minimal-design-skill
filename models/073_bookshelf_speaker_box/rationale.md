# 073 Bookshelf speaker box

A sealed box for one 3-inch full-range driver, 112 × 128 × 168. The body is a sleeve with a back, printed back face down, so the front
outline's R12 lies in the layer plane and the open front faces up. The baffle is a separate 4.8 plate that drops onto a ledge inside the
front and is glued in, sealing the box; the driver screws to it from the front. The perforated grille fills the front flush with a
reveal line round it; four posts on its back reach the baffle, and 6 × 3 magnets in the posts and in pockets in the back of the baffle
hold it with 1.9 between them. Two binding posts go through the back.

Drivers differ: set `DRV_F`, `DRV_CUT`, `DRV_B`, `DRV_BD` and `DRV_PCD` in `design.py` to the one you have.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Front | 112 × 168 (2 : 3) | The Ø80 driver frame + 2 × 16 side margin; height 1.5 × width |
| Depth | 128 | Inside about 1.9 l, the order of a sealed box for a 3-inch full-range driver |
| Outline radius | R12 on the front outline (11 % of 112) | The large radius; it lies in the layer plane in the print |
| Inside corners | R3 (and the concentric R9.48 / R9.23 inside the outline) | The small radius |
| Walls | 2.52 (T) | 6 lines |
| Back and baffle | 4.8 | Two plates of 2.4: the two panels that carry the driver and the terminals, stiffer than the walls |
| Grille | 4 thick, 0.25 inside the walls, flush with the front, C0.5 | The seam is one V line round the front |
| Air space behind the grille | 8 | The driver's 5 frame + 3 |
| Perforation | Ø2.5 at pitch 4, 21 × 35 holes, 13.2 margin on all sides | The perforation rule; the margin holds the posts, so the field is unbroken and its margins are equal |
| Posts | 4 × Ø8, 6 in from the grille's edge in the middle of each side, 8 long | In the margin, clear of the driver frame (3.25 at the side posts) |
| Magnets | Ø6.2 × 3.2 pockets in the post ends and in the back of the baffle (1.6 of plastic in front) | The Magnets rule; both pockets open upward in their prints |
| Ledge | 1.68 (DIV) round the inside, 45° underside | Seats the baffle; prints without support |
| Driver | Cut-out Ø70, 4 × Ø2.5 pilots on a Ø74 circle | M3 self-tapping screws through the driver frame |
| Push hole | Ø8 teardrop through the bottom under the air space | A fingertip pushes the grille off from behind |
| Terminals | 2 × Ø4.2, 19 apart, 24 above the bottom, in the back | M4 binding posts at the usual banana-plug spacing |
| Edges | C0.5; C0.6 on the back (bed) face | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Back face down | Off-white |
| baffle | Front face down | Dark grey |
| grille | Front face down | Dark grey |
| magnet_ref × 8 | Bought: 6 × 3 disc magnets | — |
| driver_ref | Bought: 3-inch full-range driver, Ø80 frame | — |
| (2 × M4 binding posts, 4 × M3 self-tapping screws, speaker wire, a little polyester wadding, 4 stick-on bumpers) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| body / baffle | The ledge started 0.01 in front of the baffle's back face (verify.py: 7.4 mm³ interference) | Defect | Ledge starts at the baffle's back face |
| baffle | The driver's pilot holes were blind from the back; the screws come from the front through the driver frame | Defect | Pilots through the baffle |
| grille | The posts sat in the perforation field and left four gaps in the dots | Violation | Field margin 12 (13.2 as built), posts in the middle of each margin; the field is unbroken |
| body / grille | The grille sat flush in a 0.25 gap held by magnets with nothing to take hold of: it could not be removed to reach the driver | Defect | Ø8 teardrop hole in the bottom under the air space, for a fingertip to push the grille off from behind |

Dos and Don'ts: one visible chamfer value; two radii (R12 outline and its concentric inside, R3); equal margins of the perforation field;
small holes in a dense array; the grille is one reveal line in the front; no fastener shows (the driver screws are behind the grille);
body off-white, baffle and grille the secondary dark grey; no accent.

Use cases:
- **Place:** stands on its bottom (contact 11303 mm² over 90.2 × 127) on stick-on bumpers on a shelf.
- **Listen:** the box is sealed: the baffle is glued on its ledge and the binding posts seal with their washers. Fill it loosely with
  wadding behind the driver.
- **Remove the grille:** tip the speaker back, push the grille's back through the hole in the bottom; the magnets let go and the grille
  comes forward (swept: free from 0 to 20 out; it stops against the baffle 0.5 further in).
- **Assemble:** glue the magnets into the baffle's back pockets; fit the binding posts; wire the driver; glue the baffle onto the ledge;
  screw the driver on; glue the magnets into the grille's posts with opposite poles facing; press the grille in.
- **Print:** body back face down: walls and the open front up, the ledge with a 45° underside, the push hole a teardrop pointing up.
  Baffle and grille front face down: the holes and the cut-out vertical, the magnet pockets opening upward, the posts standing up.
  No supports.

verify.py: all printed parts valid and watertight, one solid each; no interference (the driver and the magnets included); fit a 256 bed.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): L 2 is a loudspeaker; this box is not drawn from it or from any other
product. A rounded box with a perforated front is the common form of a small speaker; the proportions here (2 : 3 front, depth 128), the
flush magnetic grille in a reveal and the dark grille on an off-white body come from the driver size and the rules.

Safety (magnets): keep the magnets and the grille away from small children who could swallow a magnet that comes loose; glue them in.
The driver's own magnet is strong: keep cards and watches away from the front.

Not verified:
- Not printed on a real printer.
- The sound: the box volume suits a 3-inch full-range driver in general; check it against your driver's parameters. The walls are thin
  for a speaker and may resonate; damp them with wadding.
- The magnets' hold through 1.9 of gap and whether the push hole is enough to remove the grille.
