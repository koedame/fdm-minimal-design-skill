# 024 Weighted tape dispenser

A 40 × 120 × 48 block (1 : 3 in plan) for a roll of 18 mm tape on a 1-inch core. The roll turns on a printed hub whose stubs drop into
two U-slots in the cheeks: the hub is located by the slots and lifts straight out to change the roll. The trough under the roll is round
and concentric with the hub. In front of and behind the trough the block is hollow: two cavities with 45° gable roofs (they print bottom
down without support) take a weight, and a bottom plate closes them, located by lips that fit inside the cavities with 0.25 clearance.
A row of teeth across the front edge cuts the tape. The hub is the one dark part; there is no accent.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Block | 40 × 120 × 48, R5 | 1 : 3 in plan; R = 12.5 % of 40; the hub axis 8 under the top keeps the roll low |
| Trough | 20 wide, R30 round bottom concentric with the hub | Tape 18 + 1 each side; 2 under the largest roll (Ø56) |
| Hub | Ø25 × 19.5, stubs Ø6 × 3 | 0.2 under the 25.4 core radius; 0.25 short of the trough at each end; stand on one end to print |
| U-slots | 6.5 wide, 3.5 deep, round bottom at the axis | Stub + 0.25 per side; 0.5 deeper than the stub; open at the top so the hub lifts out |
| Cavities | 2 × 34.96 × 24.96, 45° roof 2.4 under the top | The inside of the walls, a wall from the trough; about 32 ml each |
| Bottom plate | 2.4, recessed 2.4, lips 1.68 × 4 into the cavities | The Location rule (`DIV` lip, 0.25 clearance); the plate is flush with the bottom |
| Teeth | 12 at pitch 1.68, 1.2 high, across the front | Pitch = `DIV`; they cover the 20 trough width |
| Chamfers | C0.5 top rim, trough and slots; C0.6 on the bed | One visible value |
| Rubber feet | 4 × Ø10.2 at x ±10, y ±48 | On the plate, inside the bed chamfer |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| body | Bottom down, as used | Off-white |
| bottom_plate | Outer face down | Off-white |
| hub | Standing on one end | Dark grey |
| tape_roll_ref | Bought part, not printed | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| body | The trough and slot rims were left as sharp edges (the top was chamfered before they were cut) | Violation | C0.5 on the rims after the cuts |
| body | The block was first laid out 120 along X while the trough ran across it, so the teeth stood off the end | Defect | Plan turned to 40 × 120 (x × y); teeth on the front edge |

Use cases:
- **Change the roll:** lift the hub out of the U-slots (swept free over 20 mm), slide on a new roll, drop it back.
- **Cut:** pull the tape forward over the teeth and down; the weight (about 64 ml of cavity: steel shot in a bag, nuts or coins, about
  300–450 g) keeps the block from lifting. The tape end rests on the teeth row.
- **Fill the weight:** take the bottom plate off, fill both cavities, press the plate back; its lips locate it (swept: free downward,
  stopped at 0.3 upward and 0.4 sideways). A drop of glue or the rubber feet keep it from falling out when lifted.
- **Print:** body bottom down (the cavities have 45° roofs, the slots open upward), plate outer face down, hub on one end.

verify.py: body, plate and hub valid and watertight, no interference (the tape roll included), fit a 256 bed; ground contact 4027 mm²
over 38.9 × 118.9. Motions as above: the hub stops 0.4 down and 0.5 sideways, the plate is located by its lips.

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none is a tape dispenser. A weighted block with a roll in a trough is
a common desk form; no product was used as a model.

Not verified:
- Not printed on a real printer.
- Whether printed teeth cut cleanly (PLA teeth dull; a strip of a metal cutter from a spare dispenser can be glued in front of them).
- Whether the hub turns freely on a real core and whether the plate holds by friction alone.
