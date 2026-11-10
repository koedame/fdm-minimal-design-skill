# fdm-minimal-design

An agent skill for designing minimal, refined products for FDM 3D printing, with example models.

[日本語](README.ja.md)

![The 12 sample objects](skills/fdm-minimal-design/assets/samples/overview.png)

The skill teaches Claude a design language — large radii in plan with sharp edges, a grid, achromatic colours with a
single accent, repetition of one shape — and how to fit it to the constraints of FDM printing. The language is inspired
by the design language seen in Braun products of the 1960s and 1970s (Dieter Rams). **This project is not affiliated
with, endorsed by or sponsored by Braun or its trademark owners**, and it does not reproduce the form, names or logos of
any Braun product.

## What it does

- **Advises** on an object you model yourself: grid, proportions, radii, chamfers, print orientation, part split, with numbers.
- **Builds** 3D models with [CadQuery](https://github.com/CadQuery/cadquery): STL per part in print orientation, a coloured STEP assembly and preview images.
- **Reviews** a design with a fixed procedure: a dimension rationale table, Dos and Don'ts, use cases, numeric checks and a rendering.

It comes with:

| | |
|---|---|
| `references/` | Principles, numeric design rules, Dos and Don'ts, the review procedure and a catalogue of the samples |
| `scripts/fdm_samples.py` | A helper library and 12 sample objects (clock, remote, tray, speaker, stand, radio, hinged case, power bank, wall unit, lantern, split riser, threaded jar) |
| `scripts/verify.py` | Numeric checks: solid validity, interference, watertight meshes, bed fit, ground contact, hinge sweep |
| `scripts/render.py` | Preview images (VTK, off-screen) |
| `scripts/template_new_object.py` | The starting point for a new object |
| `assets/` | Figures and the sample previews (the `.skill` bundle also holds the sample STEP files) |

## Install

### Claude Code

Copy the skill folder into your skills directory:

```bash
git clone https://github.com/koedame/fdm-minimal-design-skill.git
cp -r fdm-minimal-design-skill/skills/fdm-minimal-design ~/.claude/skills/
```

Use `.claude/skills/` inside a project instead of `~/.claude/skills/` to install it for that project only.
The folder from the repository has no STEP files; Claude can generate them with `scripts/fdm_samples.py` when CadQuery
is installed (see [Environment](#environment)).

### Claude.ai

1. Get `fdm-minimal-design.skill` (see [Building the .skill file](#building-the-skill-file)). It is a ZIP file;
   rename it to `fdm-minimal-design.zip` if the upload dialog does not accept it.
2. Code execution must be on: **Settings → Capabilities**.
3. Open **Customize → Skills**, click **+**, choose **Create skill → Upload a skill**, and upload the file.

## Environment

The scripts need Python 3.11 or later. The tested versions are pinned in `requirements.txt`:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

python skills/fdm-minimal-design/scripts/fdm_samples.py --out out     # STL + STEP for all samples
python skills/fdm-minimal-design/scripts/verify.py --all
python skills/fdm-minimal-design/scripts/render.py --all --out previews
```

## Building the .skill file

```bash
python tools/build_skill.py              # dist/fdm-minimal-design.skill, with the sample STEP files
python tools/build_skill.py --no-step    # without STEP (no CadQuery needed)
```

CI builds the same file on every pull request and keeps it as a workflow artifact.

## Repository layout

```
skills/fdm-minimal-design/   the skill (SKILL.md, references, scripts, assets)
models/                      models designed with the skill, one directory each (format: models/README.md)
tools/                       build_skill.py (the .skill bundle), models.py (check and export models/)
tests/                       tests for the tools
```

Generated 3D files (STEP, STL) are not committed. They are regenerated from the scripts and published through the
`.skill` bundle and releases, which keeps clones small as the number of models grows.

## Licence

- **Code and skill documents — [MIT](LICENSE).** Python files (`*.py`), `SKILL.md`, `references/`, the READMEs and
  other documentation.
- **3D models and images — [CC BY 4.0](LICENSE-CC-BY-4.0.txt).** STEP, STL and other model files published from this
  repository (including those generated from the samples and from `models/`), and all images (PNG, SVG).
  Attribute as "fdm-minimal-design by koedame, CC BY 4.0", link to this repository and say if you changed anything.

## No warranty and safety

Everything here is provided as is, without warranty (see the licences). In particular:

- The dimensions (clearances, snaps, threads, holes) are rules of thumb and **the samples have not been printed on a
  real printer**. Print a test piece of the mating features before printing a whole object.
- **Printed parts are not certified for anything.** For objects that hold batteries or LEDs, get hot, or touch food,
  the safety of the printed parts is not guaranteed. Use certified electronic components (batteries, chargers, LED
  drivers, power supplies) and check the materials and the electrical design yourself.
