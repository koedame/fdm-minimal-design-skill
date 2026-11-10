"""
Check and export the models in models/ (the directory format is described in models/README.md).

  python tools/models.py check                       # every model
  python tools/models.py check 001_pen_cup
  python tools/models.py export --out build/models   # STL (print + assembled), STEP, _colors.json

`check` exits with 1 if any model has a problem, and prints every problem it found.
"""
import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT / "models"
SCRIPTS = ROOT / "skills" / "fdm-minimal-design" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import fdm_samples   # noqa: E402
import verify        # noqa: E402

ID_RE = re.compile(r"^\d{3}_[a-z0-9]+(?:_[a-z0-9]+)*$")
REQUIRED_FILES = ("design.py", "rationale.md", "model.json", "preview.png")
RATIONALE_SECTIONS = ("## Dimensions", "## Parts", "## Review")
SIZE_TOLERANCE = 0.5
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
FIELDS = {   # field: (type, check on the value or None)
    "id": (str, None),
    "title": (str, lambda v: v.strip() != ""),
    "summary": (str, lambda v: v.strip() != ""),
    "based_on": (list, lambda v: all(isinstance(s, str) for s in v)),
    "size_mm": (list, lambda v: len(v) == 3 and all(isinstance(x, (int, float)) and x > 0 for x in v)),
    "parts": (list, lambda v: len(v) > 0 and all(isinstance(p, dict) for p in v)),
    "mechanisms": (list, lambda v: all(isinstance(s, str) for s in v)),
    "tags": (list, lambda v: all(isinstance(s, str) for s in v)),
    "printed": (bool, None),
    "license": (str, lambda v: v == "CC-BY-4.0"),
}
PART_FIELDS = {"name": str, "qty": int, "orientation": str, "material": str}


def model_dirs(models_dir, ids=None):
    dirs = sorted(p for p in Path(models_dir).iterdir() if p.is_dir() and not p.name.startswith((".", "_")))
    if ids:
        known = {d.name for d in dirs}
        missing = [i for i in ids if i not in known]
        if missing:
            raise SystemExit(f"no such model: {', '.join(missing)}")
        dirs = [d for d in dirs if d.name in ids]
    return dirs


def load_design(model_dir):
    spec = importlib.util.spec_from_file_location(f"model_{model_dir.name}", model_dir / "design.py")
    spec.loader.exec_module(importlib.util.module_from_spec(spec))


def check_metadata(model_dir, meta):
    problems = []
    for field, (typ, ok) in FIELDS.items():
        if field not in meta:
            problems.append(f"model.json: missing field '{field}'")
        elif not isinstance(meta[field], typ) or (typ is not bool and isinstance(meta[field], bool)):
            problems.append(f"model.json: '{field}' must be {typ.__name__}")
        elif ok and not ok(meta[field]):
            problems.append(f"model.json: '{field}' has an invalid value: {meta[field]!r}")
    for field in sorted(set(meta) - set(FIELDS)):
        problems.append(f"model.json: unknown field '{field}'")
    if meta.get("id") != model_dir.name:
        problems.append(f"model.json: id {meta.get('id')!r} does not match the directory name {model_dir.name!r}")
    for s in meta.get("based_on", []) if isinstance(meta.get("based_on"), list) else []:
        if s not in fdm_samples.SAMPLES or ID_RE.match(str(s)):
            problems.append(f"model.json: based_on {s!r} is not one of the skill's samples")
    for i, p in enumerate(meta.get("parts", []) if isinstance(meta.get("parts"), list) else []):
        if not isinstance(p, dict):
            continue
        for field, typ in PART_FIELDS.items():
            if not isinstance(p.get(field), typ) or isinstance(p.get(field), bool):
                problems.append(f"model.json: parts[{i}].{field} must be {typ.__name__}")
        if isinstance(p.get("qty"), int) and p["qty"] < 1:
            problems.append(f"model.json: parts[{i}].qty must be 1 or more")
    return problems


def check_against_design(model_dir, meta, parts):
    problems = []
    declared = {p.get("name"): p.get("qty") for p in meta.get("parts", []) if isinstance(p, dict)}
    built = {name: p.qty for name, p in parts.items()}
    for name in sorted(set(built) - set(declared)):
        problems.append(f"model.json: part '{name}' is in design.py but not in parts")
    for name in sorted(set(declared) - set(built)):
        problems.append(f"model.json: part '{name}' is in parts but not in design.py")
    for name in sorted(set(built) & set(declared)):
        if declared[name] != built[name]:
            problems.append(f"model.json: part '{name}' qty {declared[name]} but design.py makes {built[name]}")
    size = meta.get("size_mm")
    if isinstance(size, list) and len(size) == 3:
        boxes = [p.asm.val().BoundingBox() for p in parts.values()]
        actual = (max(b.xmax for b in boxes) - min(b.xmin for b in boxes),
                  max(b.ymax for b in boxes) - min(b.ymin for b in boxes),
                  max(b.zmax for b in boxes) - min(b.zmin for b in boxes))
        if any(abs(a - s) > SIZE_TOLERANCE for a, s in zip(actual, size)):
            got = " x ".join(f"{a:.1f}" for a in actual)
            problems.append(f"model.json: size_mm {size} but the assembled model measures {got}")
    return problems


def check_model(model_dir, bed=256.0):
    """Return the list of problems found in one model directory (empty when it passes)."""
    if not ID_RE.match(model_dir.name):
        return [f"directory name {model_dir.name!r} is not NNN_slug (three digits, lowercase snake_case)"]
    problems = [f"missing file: {f}" for f in REQUIRED_FILES if not (model_dir / f).is_file()]
    if problems:
        return problems
    try:
        meta = json.loads((model_dir / "model.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"model.json: not valid JSON ({e})"]
    if not isinstance(meta, dict):
        return ["model.json: must be a JSON object"]
    problems += check_metadata(model_dir, meta)
    rationale = (model_dir / "rationale.md").read_text(encoding="utf-8")
    positions = [rationale.find(s) for s in RATIONALE_SECTIONS]
    if -1 in positions or positions != sorted(positions):
        problems.append(f"rationale.md: needs the sections {', '.join(RATIONALE_SECTIONS)} in this order")
    if (model_dir / "preview.png").read_bytes()[:8] != PNG_MAGIC:
        problems.append("preview.png: not a PNG file")

    load_design(model_dir)
    if model_dir.name not in fdm_samples.SAMPLES:
        problems.append(f"design.py: does not register SAMPLES[{model_dir.name!r}]")
        return problems
    parts = fdm_samples.SAMPLES[model_dir.name]()
    problems += check_against_design(model_dir, meta, parts)
    if not verify.check(model_dir.name, bed):
        problems.append("verify.py: needs attention (see its output above)")
    return problems


def cmd_check(a):
    failed = 0
    dirs = model_dirs(a.models_dir, a.ids)
    for d in dirs:
        problems = check_model(d, a.bed)
        print(f"{d.name}: {'OK' if not problems else 'FAILED'}")
        for p in problems:
            print(f"  - {p}")
        failed += bool(problems)
    print(f"{len(dirs) - failed} of {len(dirs)} models passed")
    return 1 if failed else 0


def cmd_export(a):
    dirs = model_dirs(a.models_dir, a.ids)
    for d in dirs:
        load_design(d)
    Path(a.out).mkdir(parents=True, exist_ok=True)
    fdm_samples.export(a.out, [d.name for d in dirs])
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument("--models-dir", default=str(MODELS_DIR), help=argparse.SUPPRESS)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="check model directories and run verify.py on each")
    c.add_argument("ids", nargs="*")
    c.add_argument("--bed", type=float, default=256.0, help="bed size in mm (cube)")
    e = sub.add_parser("export", help="write STL, STEP and _colors.json for each model")
    e.add_argument("ids", nargs="*")
    e.add_argument("--out", default=str(ROOT / "build" / "models"))
    a = ap.parse_args(argv)
    return cmd_check(a) if a.cmd == "check" else cmd_export(a)


if __name__ == "__main__":
    sys.exit(main())
