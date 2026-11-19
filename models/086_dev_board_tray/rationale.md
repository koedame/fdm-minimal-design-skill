# 086 Dev board tray

A low tray, 108 × 80, for a single-board computer on the desk. The base is a tray with a 10 high rim and rubber feet; a dark deck drops
inside the rim with a 0.25 reveal round it and carries four standoffs for the board, here the 58 × 49 hole pattern of a Raspberry Pi 4 or
5. Two M2 screws come up from the bottom of the base through counterbores into two vertical bosses on the deck, beside the board's long
sides, so no fastener shows from above. A deck drawn for another board fits the same base. The board sits 2.4 above the rim, so a cable
reaches every connector over it, and the rim keeps the board's edges from being knocked.

Boards differ: set `BOARD`, `HOLES` and `HOLE_DX` in `design.py` for another board (keep it inside the deck, 102.46 × 74.46).

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Base | 108 × 80, R12, rim 10 high | 27 × 20 modules; the 85 × 56 board with about 9 round it; R12 = 11 % of 108 |
| Floor | 4 | Takes a Ø4.2 × 2 counterbore and 2 of web for the screw head |
| Walls | 2.52 (T) | 6 lines |
| Deck | 102.46 × 74.46, R9.23, 2.4 thick | The base's inside less 0.25 per side (the reveal); its corners concentric with the outline |
| Standoffs | 4 × Ø6, 6 high, Ø2.2 pilot 5 deep | The board's M2.5 self-tapping screws; the board's underside ends 2.4 above the rim |
| Deck bosses | 2 × Ø6, 4 high, at y ±32.5 (between the board's long sides and the rim); Ø1.8 pilot through deck and boss | The Hidden screws rule; below the board's level and clear of its underside |
| Screws | 2 × M2 × 8 from below: Ø4.2 × 2 counterbore, Ø2.4 clearance | 6 of thread in the deck and the boss |
| Rubber feet | 4 × Ø10.2 at (±36, ±28) | Clear of the counterbores |
| Edges | C0.5; C0.6 on the bed faces | One visible chamfer value |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| base | Bottom down | Off-white |
| deck | Bottom down | Dark grey |
| board_ref | Bought: Raspberry Pi 4 or 5, 85 × 56 | — |
| (2 × M2 × 8 screws, 4 × M2.5 × 6 self-tapping screws, 4 × Ø10 stick-on feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| deck | The two bosses were beside the board's short ends; at one end the boss sat under the microSD card, 0.6 below it, where the fingers reach for the card | Defect | Bosses moved beside the long sides (y ±32.5), where nothing on the board's underside reaches |
| base | The outline radius was R8, 7.4 % of the length, below the 8–16 % of the rule | Violation | R12 (11 %); the deck's corners follow it concentrically |

Dos and Don'ts: one visible chamfer value; R12 and its concentric insides only; the deck's reveal is the one line inside the rim; no
fastener shows from above (the board's own screws are the board's); base off-white, deck dark grey, no accent.

Use cases:
- **Place:** stands on four rubber feet; ground contact 8023 mm² over 106.9 × 78.9; cables pulled sideways do not tip it.
- **Connect:** every connector of the board is 2.4 or more above the rim; plugs go in over it. The microSD card at the end of the board
  is reached over the rim.
- **Cool:** the board stands on 6 standoffs with open air under it and above it; the tray does not enclose it.
- **Change the board:** take the two M2 screws out from below, lift the deck out by its standoffs (swept: free from 0 up; it stops on the
  floor and 0.4 sideways), fit another deck.
- **Assemble:** screw the board to the standoffs, set the deck in the base, drive the two M2 screws from below.
- **Print:** both bottom down. The counterbores open at the bed, with a 0.9 wide ring of bridging at their shoulders; the standoffs and
  bosses stand up. No supports.

verify.py: base and deck valid and watertight, one solid each; no interference with the board; fit a 256 bed; the deck's motions as
recorded.

Compared with well-known products in this style: radios, a pocket radio, a calculator and a loudspeaker; none is a
board mount. A tray with standoffs is the common way to hold a board; no product was used as a model.

Safety (electronics): the printed parts are not certified for anything. Power the board from a supply of a trustworthy source with its
own protection. The board is open: keep liquids and metal objects (paper clips, screws) off it, and give a board that runs hot a heat sink
or a fan; PETG softens at about 75–80 °C.

Not verified:
- Not printed on a real printer.
- How the M2.5 screws hold in printed standoffs; drive them by hand and stop when snug.
- The deck dimensions for boards other than the Raspberry Pi 4 and 5.
