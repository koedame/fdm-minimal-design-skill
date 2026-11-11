# 007 Tall canister

A Ø72 × 144 screw-top canister for dry goods such as tea, coffee beans or pasta. The lid is flush with the body and is the
one dark part. The threads are those of 12_threaded_jar, so neither part needs supports.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Canister | Ø72 × 144 | Height = 2 × diameter |
| Body : lid | 128 : 16 | 8:1; the seam sits low on the lid band, which is smooth, and the grip ribs are above it |
| Wall | 2.52 | 6 lines |
| Floor | 2.4 with an R6 fillet inside | Nothing lodges in the corner; easy to wipe |
| Shoulder inside the neck | 45° | Prints upright without supports, and the contents pour out without a ledge |
| Neck | thread root Ø64, opening Ø59 | 2.4 lid wall + 1.2 thread + 0.4 clearance under the outer radius; a measuring scoop fits |
| Thread | pitch 4, height 1.2, 45° flanks, 2 turns | As 12_threaded_jar; lid thread offset half a pitch, 0.4 radial clearance |
| Grip | 64 ribs 1.0 × 0.8 on the upper 8.5 of the lid | About 3.5 apart; the band at the seam stays smooth |
| Rubber feet | 4 × Ø10.2 at ±18 | Inside the bed chamfer |
| Volume | about 0.43 l | Ø67 × 122 inside |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down, as used | Off-white |
| lid | Top face down | Dark grey |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| body | Square inside corner at the floor: dry goods and dust lodge in it and it cannot be wiped | Defect | R6 fillet (prints upright without supports) |

Use cases:
- **Fill and pour:** unscrew the lid (two turns); the 45° shoulder lets the contents run out without catching.
- **Close:** the lid seats flush with the body; there is no seal, so the canister is not airtight.
- **Clean:** hand wash with lukewarm water; no undercuts inside.
- **Print:** body upright, lid top face down, no supports.

verify.py: both parts valid and watertight, no interference, fit a 256 bed, ground contact 3616 mm² over Ø70.9.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a container; a plain cylinder with a flush lid is
a common form, and no product was used as a model.

Safety (food): an FDM print is not a food-safe container. The layer lines hold residue and bacteria that washing does not remove,
and most filaments and colourants are not certified for food contact. Keep food in its own bag inside the canister, or use the
canister only for things that are not eaten. Do not put it in a dishwasher or fill it with anything hot (PLA softens at about 55 °C).

Not verified:
- Not printed on a real printer.
- How the threads engage on a real print (settle the clearance with a test ring).
