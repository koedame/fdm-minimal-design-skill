# 098 Vertical router stand

A low block 128 × 80 × 32 with one straight slot across it, 36 wide and 24 deep, open at both ends. A Wi-Fi router that may stand
on edge (most say so in their manual) stands in it on its long edge: it takes a quarter of the footprint it took lying down, air rises
along both its faces, and the cables leave from its upper edge as before. One printed part.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | 128 × 80, R10; 32 high | 32 × 20 modules; R10 = 12.5 % of the depth; 80 deep is half the height of a 160-high router, so it stands with its centre of gravity well inside the block |
| Slot | 36 wide, 24 deep (floor 8 thick), straight through along the length | Routers 30–35 thick (check yours); 24 deep holds three quarters of the block's height; open ends take a router longer than the block |
| Cheeks | 22 thick, solid | Solid enough at 25 % infill to hold a 1 kg router upright against a knock |
| Edges | C0.5 on the top edges and the slot's outline on both end faces; C0.6 on the bed edge | One visible chamfer value; the slot's top edges are the lead-in |
| Feet | Four Ø10.2 × 1 pockets at (±48, ±28) for rubber feet | Keeps the block from sliding when a cable is pulled |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| stand | Bottom down | Off-white |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| — | No defect or violation found: a 33-thick router (30 and 35 too) stands in the slot without overlap, the block prints without supports, every edge has C0.5 or C0.6 | — | — |

Dos and Don'ts: one radius R10 (plan), one visible chamfer value, one slot, one module; plain, the slot being the only feature;
off-white, no accent.

Use cases:
- **Set up:** stand the stand behind the monitor or on a shelf, unplug the router, stand it in the slot on the edge that has no ports,
  plug the cables back in from the top.
- **Thinner router:** a 30-thick router leans up to 14° in the 36 slot; its top moves 39 sideways and its centre of gravity stays
  inside the block. A strip of felt on one cheek takes up the play.
- **Port on the lower edge:** the slot's open ends let a cable out if the port is within about 10 of the router's end; a port in the
  middle of the edge needs a different stand.
- **Clean:** lift the router out and wipe the slot; the floor is flat and open at both ends.
- **Print:** bottom down; the slot is cut straight down; no supports.

verify.py: stand valid, watertight, fits a 256 bed; it stands on 9 599 mm² of its base. A router 30, 33 or 35 thick placed in the
slot overlaps nothing.

Safety:
- Stand the router upright only if its manual allows it; keep its vents clear of the cheeks, which cover the lowest 24 of its faces.

Compared with well-known products in this style: radios, a pocket radio, a calculator and a loudspeaker; none is a
stand. A block with a slot is the common form of a router or book stand; no product was used as a model.

Not verified:
- Not printed on a real printer.
- How firmly a router of your thickness sits in the 36 slot.
- Whether the router runs cooler on edge.
