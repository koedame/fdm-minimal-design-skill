"""
Build the installable skill bundle: dist/fdm-minimal-design.skill (a zip).

  python tools/build_skill.py                 # with the sample STEP files (needs CadQuery)
  python tools/build_skill.py --no-step       # documents, scripts and images only
  python tools/build_skill.py --out somewhere

The zip holds one folder, fdm-minimal-design/, with the contents of
skills/fdm-minimal-design/. The sample STEP files are not committed to the
repository; they are generated from scripts/fdm_samples.py here and placed at
assets/samples/<name>/<name>_assembly.step, next to each preview.
"""
import argparse
import os
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = "fdm-minimal-design"
SKILL_DIR = ROOT / "skills" / SKILL_NAME
SKIP_DIRS = {"__pycache__"}
SKIP_SUFFIXES = {".pyc"}
ZIP_DATE = (1980, 1, 1, 0, 0, 0)   # fixed timestamps: same inputs give the same zip entries


def skill_files(skill_dir):
    for path in sorted(skill_dir.rglob("*")):
        rel = path.relative_to(skill_dir)
        if path.is_file() and not SKIP_DIRS & set(rel.parts) and path.suffix not in SKIP_SUFFIXES:
            yield rel, path


def sample_steps(skill_dir, work):
    sys.path.insert(0, str(skill_dir / "scripts"))
    import fdm_samples
    fdm_samples.export(str(work))
    for name in fdm_samples.SAMPLES:
        yield Path("assets/samples") / name / f"{name}_assembly.step", Path(work) / name / f"{name}_assembly.step"


def add(zf, arcname, path):
    info = zipfile.ZipInfo(f"{SKILL_NAME}/{arcname.as_posix()}", ZIP_DATE)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, path.read_bytes())


def build(out_dir, with_step=True, skill_dir=SKILL_DIR):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{SKILL_NAME}.skill"
    with tempfile.TemporaryDirectory() as work:
        entries = list(skill_files(skill_dir))
        if with_step:
            entries += list(sample_steps(skill_dir, work))
        with zipfile.ZipFile(target, "w") as zf:
            for arcname, path in sorted(entries):
                add(zf, arcname, path)
    return target


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument("--out", default=str(ROOT / "dist"), help="output directory (default: dist/)")
    ap.add_argument("--no-step", action="store_true", help="leave out the generated sample STEP files")
    a = ap.parse_args()
    target = build(a.out, with_step=not a.no_step)
    with zipfile.ZipFile(target) as zf:
        n = len(zf.namelist())
    print(f"wrote {os.path.relpath(target)} ({n} files, {target.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
