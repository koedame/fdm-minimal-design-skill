---
name: fdm-minimal-design
description: Design, review and 3D-model minimal, refined products for FDM 3D printing, in a design language inspired by 1960s-70s Braun products (Dieter Rams); not affiliated with Braun or its trademark owners. Includes design principles, numeric design rules, Dos and Don'ts, a review procedure, 12 sample objects (STEP) and CadQuery scripts to generate, verify and render models. Use this skill whenever someone wants to make an enclosure, case, small object, stand, clock, lamp, container or similar with 3D CAD or a 3D printer in a style described as "Braun-like", "Rams-like", "like a minimal appliance" or "simple but not cheap-looking", and whenever they ask why their own shape looks lazy or amateurish, even if the word Braun never comes up.
---

# FDM minimal design

A skill for designing objects in a specific design language and fitting it to the constraints of FDM 3D printing.
The language: large radii in plan with sharp edges, a grid, achromatic colours plus a single accent, and repetition of one shape.

The goal is a form that is "simple, but does not look lazy". The fewer the elements, the more precision and justification they demand, so the skill is built around two habits: **give every dimension a reason, and always review the design after making it**.

## Reference documents (read when needed)

| File | When to read it |
|---|---|
| `references/01_principles.md` | Once at the start. When a judgement call is unclear. When explaining why something looks lazy |
| `references/02_rules.md` | When deciding dimensions, colours, print orientation and mechanisms (with numbers) |
| `references/03_dos_donts.md` | The review checklist. Always check a design against it at the end |
| `references/04_review.md` | The review procedure (rationale table → Dos and Don'ts → use cases → numbers → rendering) |
| `references/05_catalog.md` | When looking for a sample close to the object or the mechanism you need |

Figures are in `assets/figures/` (SVG and PNG). Sample previews are in `assets/samples/<name>/`; the STEP files sit next to them in the `.skill` bundle, and `scripts/fdm_samples.py` regenerates them (and the STLs) anywhere CadQuery is installed.

## Types of request and how to proceed

### A. Advice (the user models it in their own CAD)

1. Confirm the object and its constraints. If something is unknown, state your assumption and carry on.
   - Purpose
   - Rough size
   - Printer bed size
   - Material
   - Moving parts, if any
2. From `05_catalog.md`, pick a sample with a similar form and a sample with a similar mechanism, and explain the thinking behind them.
3. Answer with concrete numbers, following `02_rules.md`.
   - Grid
   - Proportions
   - Radii
   - Chamfers
   - Print orientation
   - Part split
4. If a figure would help, show one from `assets/figures/` or draw one on the same principles.

### B. Build a 3D model (CadQuery is available)

1. **Write the dimension rationale table first** (`04_review.md` Step 1). A dimension you cannot justify becomes a spot that looks lazy.
2. Copy `scripts/template_new_object.py` and write a function.
   - Reuse the helpers in `scripts/fdm_samples.py` (`rrect`, `cyl`, `box`, `button_local`, `knob_local`, `feet`, `teardrop_x`, `stadium_x`, `thread_solid`, `fillet_at`, `chamfer_rim`) and its constants (`T`, `DIV`, `CH`, `CH_BED`, `GAP`).
   - Adapting the function of a nearby sample directly is fine too.
3. For each part, define the assembled shape (orientation in use, Z up) and the print-oriented shape with `Part(asm, prn, color)`. Choose the print orientation according to chapter 5 of `02_rules.md`.
4. Export and verify.
   ```bash
   python scripts/template_new_object.py --out out
   python scripts/verify.py <name> --module scripts/template_new_object.py [--bed 220] [--hinge ...]
   python scripts/render.py  <name> --module scripts/template_new_object.py --out previews
   ```
5. Review with every step of `04_review.md`, and fix defects and violations before handing over.

### C. Review an existing design

Check it with the procedure in `04_review.md` and return the problems in a table split into "defect" and "violation". Give the fixes as numbers.

## What to hand over

- **STL in print orientation** (one per part) and **STEP** (coloured assembly)
- **Preview images**
- **Dimension rationale table**
- **Table of print orientation and colour per part**
- **Review results** (including the verification numbers)
- **An explicit list of what has not been verified**

## Honesty

- The numbers (clearances, snaps, threads, hole diameters) are rules of thumb, not values confirmed on real prints. Always say so when handing them over, and tell the user to settle them with a test piece of the mating features.
- Do not reproduce the form of a specific Braun product, or any trademark or logo. Make original forms by applying the principles.
- Do not vouch for quality based on how it looks on screen. Tell the user to judge gaps and edges on the real print.
- Printed parts are not certified for anything. For objects that hold batteries or LEDs, get hot, or touch food, do not claim the printed part is safe; tell the user to use certified electronic components and to check the material and the electrical design themselves.

## Environment

- **What the scripts need:** Python 3.11 or later and `cadquery`. `trimesh` and `vtk` are optional and are used for mesh checks and rendering. Install with `pip install cadquery trimesh` (vtk comes with cadquery). The repository this skill comes from pins tested versions in `requirements.txt`.
- **If CadQuery is not available:** give advice in the style of A and point to the STEP files of the samples as reference shapes. STEP opens in common CAD software, which can export STL from it.
