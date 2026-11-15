# 033 Tablet stand

A low block, 128 × 96 × 24 (4 : 3, R12), with one slot across it. A tablet stands with its bottom edge in the slot and its back flat
on the slot's back wall, which leans back 1 for 3 up (18.4°); the floor of the slot is square to the back wall, so the tablet leans at
the wall's angle whatever its thickness, and the front wall only keeps the edge from sliding forward. The slot sits in the front of the
block, so the tablet's centre of gravity falls well inside it. One part, no accent: the slot is the only detail, with C0.5 on its
whole outline, on top and where it leaves the two ends.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Block | 128 × 96 × 24, R12 | 4 : 3 in plan; R = 12.5 % of the depth; 96 deep so a portrait tablet's centre of gravity is 36 inside the back edge |
| Lean | 18.4° (tan = 1/3) | 1 back for 3 up: a common viewing angle for a tablet on a desk |
| Slot | 12 wide, back wall 18 long, floor square to it | Tablets up to about 11.5 thick with a case; 18 of the back is supported |
| Front strip | 16 at the top | Four modules; it holds the edge and carries the R12 of the outline at the ends |
| Slot edges | C0.5 lead-in on top, a 45° flare where the slot leaves the ends | The one visible chamfer value on every edge of the slot |
| Feet | Ø10.2 × 1 recesses at (±48, ±32) | The rubber foot rule, on the 4 mm grid |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| stand | Bottom down, 25 % infill or more (solid for touch use, see below) | Off-white |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| stand | At 80 deep, a 500 g portrait tablet tipped the stand back with a tap of about 0.5 N at 80 % of its height | Defect | 96 deep: about 1.2 N at 25 % infill, 1.7 N printed solid; 2.2–2.9 N in landscape (estimated from the part volume and a 500 g tablet) |
| stand | The slot's outline was left sharp where it leaves the two ends (CadQuery cannot chamfer those edges) | Violation (03_dos_donts: untreated edges) | A 45° flare: the slot's profile lofted to its outline grown by 0.5 at each end |
| tablet | Shown as a bought part, the tablet set the model's size (240 wide, 170 tall) and filled the preview | Violation (the size is the object's) | Left out of the parts; `tablet_fit()` in `design.py` places one for checks |

Use cases:
- **Place:** the whole bottom stands on the desk (11593 mm²) with four rubber feet.
- **Stand a tablet:** drop its edge into the slot and let it lean back; checked with `tablet_fit()` for 6, 8 and 11.5 thick tablets,
  170 (landscape) and 250 (portrait) tall: no overlap with the stand, centre of gravity 3.7 in front of to 11.6 behind the block's centre.
- **Touch:** a tap at the top pushes the tablet back. Landscape takes about 2 N before the stand rocks; portrait about 1.2 N (1.7 N
  printed solid). For touch use in portrait, print the stand solid.
- **Charge:** in landscape the tablet's port is at the side and free; in portrait the port at the bottom edge is in the slot.
- **Print:** bottom down; the slot's front wall overhangs 18.4° from vertical and the floor faces up. No supports.

verify.py: stand valid and watertight, fits a 256 bed; ground contact 11593 mm².

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a stand; this is a plain block with one slot.
Slot stands for tablets are common; no product was used as a model.

Not verified:
- Not printed on a real printer.
- The tipping forces are estimates from the part volume, an assumed infill and a 500 g tablet, not measured.
- Whether a thick rubber case grips the slot's walls (the slot is 12 wide).
