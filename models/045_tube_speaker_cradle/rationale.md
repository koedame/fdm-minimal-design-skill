# 045 Tube speaker and cradle

A Ø64 × 128 tube that lies on its side and points a 57 mm full-range driver at the listener. The front cap is the one dark part, a
field of small holes over the driver cone; the tube rests in a low cradle that it overhangs on both sides. A V rib across the cradle's
saddle drops into a V groove round the tube, so the tube cannot slide off forward or back but lifts straight out. The seam between the
cap and the tube is the same 45° V as the groove, so the tube carries exactly two equal lines, and the seam doubles as a nail slot for
taking the cap off. Inside, the cap's spigot clamps the driver's frame against a ledge and seals the box with an O-ring.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Tube | Ø64 × 128 overall (body 125.6 + cap plate 2.4) | Length = 2 × diameter; about 0.3 l inside, a usual sealed volume for a 57 mm driver |
| Wall / floor / cap plate | 2.52 / 2.4 / 2.4 | Line width × 6; 12 layers |
| Driver | Ø57 frame, 3 thick, 30 deep behind it | A common 57 mm (2¼") full-range driver; set `DRV` to yours |
| Ledge | Inner Ø51, 2.4 thick, 45° underside | The basket passes; the frame rests on r 25.5–28.5; prints standing |
| Cap spigot | 8 long, Ø58.46 outside (0.25 in the bore), Ø52 inside | Its end presses the frame between r 26 and 28.5 |
| O-ring | 2 mm cord, about 55 mm inside; groove 1.4 deep, 2.6 wide | Squeeze 0.35 (17.5 %): holds the cap and seals the box; the groove's top flank is 45° for the face-down print |
| Perforation | Ø2.4 holes at pitch 4 within Ø44 | The perforation rule; the field covers the cone and no more |
| Groove and seam | 45° V, 1.15 deep (the rib + 0.35, i.e. 0.25 normal to the flanks) | One line shape for both; the wall is thickened 1.2 inside behind the groove, so 2.57 stays under it |
| Cradle | 56 × 96 × 14, R8 in plan | Narrower than the tube, so the tube overhangs it by 4 each side; 96 = ¾ of the tube's length |
| Saddle | R32.25 (tube + 0.25), its edge meets the top 21.3 off the centre line | Holds the tube 6 above the desk; the edge meets the top at 139°, no sharp edge |
| V rib | 0.8 high, across the middle of the saddle | Locates the tube front to back; 45° flanks print without support |
| Centre of gravity | About 42 from the front (tube about 90 g at 64, driver about 120 g at 30) | Inside the cradle (which starts 16 from the front) by 26 |
| Cable hole | Ø4.4 in the back floor, 10 above the tube's bottom | A speaker cable; a drop of glue seals it |
| Rubber feet | 4 × Ø10.2 at x ±18, y ±36 | Inside the bed chamfer |
| Edges | C0.5; C0.6 on bed faces | One chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| tube | Standing on its back | Off-white |
| cap | Face down | Dark grey |
| cradle | Bottom down | Off-white |
| driver_ref (57 mm full-range driver) | Bought | — |
| (O-ring 2 mm cord, about 55 mm inside diameter; speaker cable; 4 × Ø10 rubber feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| cap | Flush with the tube and held by an O-ring, it had nothing to grip: there was no way to take it off | Defect | The seam is a 45° V (tube's front edge and cap's back edge chamfered 1.15): a fingernail levers the cap out, and the seam matches the groove |
| tube | The ledge and the band behind the groove were rings 0.01 into the wall with a separate cone: the mesh was not watertight | Defect | Each is one solid of revolution reaching 0.5 into the wall |

Use cases:
- **Assemble:** thread the cable through the back hole and seal it; solder it to the driver; set the driver into the tube from the
  front onto the ledge; roll the O-ring into the cap's groove and push the cap in until its plate meets the tube: the spigot clamps
  the frame (swept: the cap stops 0.3 in against the tube and leaves freely forward, held 0.4 sideways).
- **Place:** lay the tube in the cradle with the cable hole at the bottom; the rib drops into the groove (swept: lifts freely 20,
  stops 0.4 down on the saddle, stops at 1 forward and back on the rib, 1 sideways in the saddle).
- **Listen / aim:** the tube can be turned in the saddle; the round grille looks the same at any angle.
- **Open:** a fingernail in the seam levers the cap out against the O-ring.
- **Print:** tube standing on its back (the ledge and the band have 45° undersides, the groove is a 45° V); cap face down; cradle
  bottom down. No supports.

verify.py: all parts valid and watertight, one solid each, no interference, fit a 256 bed.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): the L 2 is an upright box loudspeaker with a grille across its whole
front, and the radios are boxes with a perforated or slotted area; none is a tube on its side in a cradle. Cylindrical speakers are a
common kind of object; no product was used as a model.

Safety (electronics): the driver is fed from an amplifier; keep within its rated power. The printed parts are not certified for
anything.

Not verified:
- Not printed on a real printer.
- The sound: the volume and the driver's parameters were not matched beyond a rough size; there is no damping material in the model
  (a loose wad of polyester fibre inside helps).
- The O-ring's hold and how hard the cap is to lever out.
- The centre of gravity is estimated, not weighed.
