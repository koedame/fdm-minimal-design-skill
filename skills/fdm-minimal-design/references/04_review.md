# 04 Review procedure

Always run a design through this before handing it over. In past reviews, things were missed when only the look (proportions, alignment, radii) was checked, and use cases and numbers were not.

Do the five steps in order. Record the results in the format of the table at the end.

---

## Step 1 Write the dimension rationale table

List every major dimension and give its reason in one line. **A dimension whose reason you cannot write is a candidate for a spot that looks lazy.**

| Dimension | Value | Reason |
|---|---|---|
| Outline | 144×96 | 3:2, grid 4 |
| Front plate frame | 14 | Left/right = bottom (margins with the same role) |
| Dial diameter | 32 | Same as the distance between the centres of the outer buttons |
| … | … | … |

## Step 2 Check the Dos and Don'ts from the top

Check the tables in `03_dos_donts.md` line by line, chapters 1 to 6 in order. Record every Don't that applies.

Items that are easy to miss:
- Are chamfer values mixed (is C0.5 the only one where visible)?
- Are there more than three radii?
- Are margin widths equal (left/right, top/bottom, around windows)?
- Have labels turned black?
- Is the accent in two or more places?
- Does a recess cut into the rim of the neighbouring face?

## Step 3 Check the use cases

Imagine each situation in which the object is actually used, one at a time, and check that the form holds up.

| Situation | What to check |
|---|---|
| **Place** | Is the contact face flat and wide enough (not a line contact)? Is the centre of gravity inside the contact area? Do the rubber feet fit? |
| **Hold** | Are the edges the hand touches too sharp? Is the place to hold left free? |
| **Open, close** | Do the hinge and lid stay clear over the whole opening range? Is the closed state held (magnets, snaps)? |
| **Remove, fit** | Is the slide path free of obstacles? Are the snap's catch position and release direction right? |
| **Assemble** | Can the parts go in in the actual order (e.g. buttons must go in before the front plate; the carrier goes in from inside)? |
| **Hang, attach** | Which way do the keyhole slots run (does it catch when slid down)? Is there a shadow line against the wall? |
| **Print** | Does it fit the bed? In the print orientation, are there ceilings, horizontal holes or 90° overhangs? |

## Step 4 Verify with numbers

Use `scripts/verify.py`. Do not settle for "looks fine" from an image.

```bash
python scripts/verify.py <sample_name> [--bed 256] [--hinge "moving:fixed:x1,y1,z1:x2,y2,z2:deg1,deg2,..."]
```

What it checks:
- **Solid validity** (`isValid`): invalid shapes break in slicers and CAD
- **Interference between parts**: 0 in the assembled state (contact between an inlay and its parent part excluded)
- **Closed mesh** (watertight): the print STL is closed
- **Lowest point in print orientation**: sits on z=0
- **Fits the bed**
- **Contact width**: in the assembled state, the width and area of the section near z=0
- **Interference of moving parts** (optional): give the moving part, the fixed part, two points on the rotation axis (assembly frame) and the angles, to see the interference at each angle. Example for the hinged case: `--hinge "lid:base:0,32,24:1,32,24:-30,-60,-90,-110"`

## Step 5 Look at the whole in a rendering

Draw previews with `scripts/render.py` and look at:
- The proportions of the silhouette
- Whether reference lines align
- Whether there is a single accent
- The position and number of reveal lines

**Looking clean on screen is not a reason to pass.** Use the rendering only to check proportions and alignment.

---

## Recording format

Record the problems you find split into **defects** and **violations**.

| Target | Problem | Kind | Fix |
|---|---|---|---|
| 11 split_riser | The bottom end of the leg was a full round, so the contact width was 1.9 mm | Defect | Keep the ground end flat with a chamfer only (contact width 11.1 mm) |
| 12 jar | Body to lid was 60:16, with no reason | Violation | 64:16 = 4:1, total height = diameter |

- **Defect:** unusable, breaks, or cannot be printed. Always fix.
- **Violation:** goes against the Dos and Don'ts and lowers the visual quality. Fix as a rule.

**When a review finds a new kind of problem, add a line to the Dos and Don'ts too,** so the same problem does not repeat next time.

## Checking on real prints

Verification on the model cannot tell you the following. Print a test piece cut down to just the mating features to settle them.
- Whether the clearances actually fit
- How well the snaps work
- How the threads engage
- How stiff the slides are
- Surface quality (layer lines, Z seam, colour)
