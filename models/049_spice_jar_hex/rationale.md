# 049 Hexagonal spice jar

A spice jar of about 110 ml: a hexagonal body 48 across the flats and 80 high under a round dark screw lid Ø48 × 16. Jars stand
together flat to flat in a drawer or on a shelf, and each flat takes a label. The lid is round on purpose: a screw lid stops wherever
its thread ends, so a hexagonal lid would almost never line up with the body. Its diameter equals the width across the flats, so it
touches the middle of each flat and the six corners of the body's top show round it. The thread is 12_threaded_jar's on a smaller neck.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Body | Hexagon 48 across the flats (54.2 across the rounded corners), 80 high | About 110 ml inside; flats 27.7 wide for a label |
| Lid | Ø48 × 16 | Ø = width across the flats; body : lid = 5 : 1, 96 overall = 2 × the flats |
| Body edges | R4 vertical edges | Soft in the hand; the corners do not chip |
| Wall / floor | 2.52 / 2.4 | Line width × 6; 12 layers |
| Neck | Thread root Ø40, 12 high; bore Ø35 | 4 under the lid's outside, as 12_threaded_jar; a measuring spoon goes in |
| Thread | Pitch 4, height 1.2, 45° flanks, 2 turns on the body, 2.25 in the lid | As 12_threaded_jar; 0.4 radial clearance |
| Cavity ceiling | A 45° cone from the hexagon's inner corners to the neck bore | Prints upright without support; spice pours out over it |
| Cavity floor | A 45° edge, 2 at the flats | Nothing lodges in the floor's corners; a fillet there meshed open |
| Lid grip | 42 ribs 1.0 × 0.8 on its upper 8.5 | As 12_threaded_jar; the band at the seam stays smooth |
| Seal | A Ø41 × 2 silicone disc in the lid | The neck's rim stops 1.6 under the lid's top, so the disc is squeezed 0.4 (20 %) when the lid seats on the body |
| Edges | C0.5; C0.6 on bed faces | One chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down | Off-white |
| lid | Top down | Dark grey |
| (silicone disc Ø41 × 2, food grade) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| body / lid | The lid's top cleared the neck's rim by 1.6: the jar was not airtight, and spices go stale | Defect | A Ø41 × 2 silicone disc in the lid, held by the thread crests (Ø40.8), squeezed 0.4 between rim and lid |
| body | A fillet round the cavity's floor (on the rounded hexagon) made a mesh that was not closed; a chamfer there made an invalid solid | Defect | The floor's edge is cut by a 45° cone instead |

Use cases:
- **Fill:** unscrew the lid, pour through a small funnel or spoon in (the bore is Ø35).
- **Close:** screw the lid on, 2.25 turns, until it seats on the body's top and squeezes the disc (swept: the thread holds it 1 up,
  it stops 0.3 down on the body's top, 0.2 radial play).
- **Use:** tip to shake or spoon out; the shoulder inside is 45°, so nothing stays behind it.
- **Store:** jars stand flat to flat; label a flat.
- **Print:** body bottom down (thread flanks, cavity ceiling and floor edge all 45°); lid top down. No supports.

verify.py: all parts valid and watertight, one solid each, no interference, fit a 256 bed.

Compared with well-known products in this style: radios, a calculator and a loudspeaker; none is a jar or a container.
Hexagonal spice jars are a common kind of object; no product was used as a model.

Safety (food): for dry spices only. Print in a food-contact grade PETG with a stainless steel nozzle; layer lines hold residue, so
wash by hand in warm water and dry fully, not in a dishwasher (it softens the plastic). The printed parts are not certified as food
contact materials.

Not verified:
- Not printed on a real printer.
- How airtight the jar is with the disc.
- Whether the lid's internal thread prints clean at this smaller diameter (Ø43.2).
