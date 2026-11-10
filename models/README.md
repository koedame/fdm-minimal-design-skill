# models/

Models designed with the skill, one directory per model. Every directory has the same shape, so tools
(the checks in CI, the 3D viewer, the website) can read any model without knowing anything about it.

```
models/
  001_pen_cup/
    design.py       # CadQuery code that builds the model (MIT)
    rationale.md    # why every dimension is what it is, part table, review result
    model.json      # metadata for tools and the website
    preview.png     # rendered with render.py (CC BY 4.0)
```

STEP and STL files are **not committed**. They are generated from `design.py` (see "Generated files" below)
and published through releases and the website. Committing them would add about 1 MB per model to every clone
for files anyone can regenerate.

## Directory name and id

`NNN_slug`: a three-digit number and a lowercase snake_case name, for example `001_pen_cup`.
The directory name is the model id; it is used in `design.py`, `model.json` and file names.
The numbers do not overlap with the 12 samples in the skill (`01_clock` … `12_threaded_jar`), which stay inside
`skills/fdm-minimal-design/` and are not repeated here.

## design.py

Start from `skills/fdm-minimal-design/scripts/template_new_object.py`. The file must:

- define one function that returns `{part_name: Part(asm, prn, color, ...)}`, using the helpers and constants of
  `fdm_samples.py`;
- register it under the model id: `SAMPLES["001_pen_cup"] = pen_cup`.

Import the helpers like this, so the file works both from the tools and when run directly:

```python
import os
import sys

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, CH, CH_BED, OFF, rrect, feet  # noqa: E402
```

## rationale.md

Three sections, in this order:

1. `## Dimensions` — the table from Step 1 of `references/04_review.md`: `| Dimension | Value | Reason |`,
   one row per major dimension.
2. `## Parts` — `| Part | Orientation | Colour |`, one row per part, same names as in `design.py`.
3. `## Review` — the result of the review procedure: the defect / violation table (or "none found"),
   the output summary of `verify.py`, and a list of what has not been verified (always including
   "not printed on a real printer" until it has been).

## model.json

```json
{
  "id": "001_pen_cup",
  "title": "Pen cup",
  "summary": "A square cup for pens on a floating plinth.",
  "based_on": ["03_tray"],
  "size_mm": [72, 72, 108],
  "parts": [
    {"name": "cup", "qty": 1, "orientation": "Bottom down", "material": "PLA, matte"}
  ],
  "mechanisms": [],
  "tags": ["desk"],
  "printed": false,
  "license": "CC-BY-4.0"
}
```

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Same as the directory name |
| `title` | string | Short English name for lists and the website |
| `summary` | string | One sentence |
| `based_on` | list of strings | Sample names from the skill (`05_catalog.md`) whose form or mechanism this builds on. May be empty |
| `size_mm` | 3 numbers | Bounding box of the assembled model, width × depth × height (X, Y, Z), in mm. Checked against `design.py` to ±0.5 mm |
| `parts` | list of objects | One per part in `design.py`, same names and quantities. `orientation` and `material` are free text |
| `mechanisms` | list of strings | Mechanisms used, in the words of the mechanism table in `05_catalog.md` (for example "Pin hinge"). May be empty |
| `tags` | list of strings | Free keywords for search and filtering. May be empty |
| `printed` | boolean | `true` only after the model has been printed and checked on a real printer |
| `license` | string | Always `"CC-BY-4.0"` (the model and its images; `design.py` itself is MIT) |

Colours are not repeated here: they are part of `design.py` and are written to `_colors.json` when the model is exported.

## preview.png

```bash
python skills/fdm-minimal-design/scripts/render.py 001_pen_cup --module models/001_pen_cup/design.py --out models/001_pen_cup
mv models/001_pen_cup/001_pen_cup.png models/001_pen_cup/preview.png
```

## Generated files

```bash
python tools/models.py export --out build/models              # every model
python tools/models.py export --out build/models 001_pen_cup
```

writes, under `build/models/001_pen_cup/`:

- `print_<part>.stl` (`print_<part>_x<qty>.stl` when qty > 1): each part in print orientation, on z = 0
- `_asm_<part>.stl`: each part in the assembled position (for viewers)
- `001_pen_cup_assembly.step`: the coloured assembly

and adds the part colours to `build/models/_colors.json` (`{"001_pen_cup": {"cup": {"color": [r, g, b]}}}`, 0–1).

## Checking

```bash
python tools/models.py check            # every model
python tools/models.py check 001_pen_cup
```

checks the files above against each other (id, required fields, part names and quantities, size, licence,
the three sections of `rationale.md`) and runs `verify.py` on the design. CI runs it on every pull request;
a model that does not pass is not merged.
