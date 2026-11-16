"""
Build the website: one static page that introduces the skill and shows every model in 3D.

  python tools/build_site.py --out build/site                      # the 12 samples and every model in models/
  python tools/build_site.py --out build/site 06_radio 001_pen_cup # only these (quick checks)

The list is built from models/ (model.json, preview.png, design.py) and from the samples of the skill, so a
new model needs no change here. The output is plain files for any static host:

  index.html                 the page; the list is in the HTML, the data for the 3D view inline
  site.js                    opens a model, loads the 3D view on first use
  viewer/                    three.min.js, fdm-viewer.js (the 3D view of scripts/viewer.py), three.js licence
  models/<id>/thumb.webp     list image
  models/<id>/model.glb      meshes for the 3D view, read when the model is opened
  models/<id>/<id>_assembly.step, <id>_print_stl.zip, <id>_viewer.html   downloads
  _headers                   response headers for Cloudflare (CSP with the hashes of the inline style and script)
  .well-known/security.txt   where to report a vulnerability

Nothing on the page is read from another server: no fonts, scripts or analytics from outside.
"""
import argparse
import base64
import hashlib
import json
import multiprocessing
import os
import re
import shutil
import sys
import tempfile
import zipfile
from concurrent.futures import ProcessPoolExecutor
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "fdm-minimal-design"
SCRIPTS = SKILL_DIR / "scripts"
SITE_DIR = ROOT / "site"
CATALOG = SKILL_DIR / "references" / "05_catalog.md"
REPO_URL = "https://github.com/koedame/fdm-minimal-design-skill"
THUMB_SIZE = (480, 384)        # 2x the widest list cell on a desktop, same 5:4 as preview.png
ZIP_DATE = (1980, 1, 1, 0, 0, 0)
MARK = "<!-- Written by tools/build_site.py"   # in every index.html it writes; --out is emptied only then
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(ROOT / "tools"))
import fdm_samples      # noqa: E402
import models           # noqa: E402
import viewer           # noqa: E402
from PIL import Image   # noqa: E402

SAMPLE_IDS = list(fdm_samples.SAMPLES)   # before any design.py from models/ adds itself
CATALOG_HEADING = re.compile(r"^## (\d\d) (\S+) — (.+)$", re.M)


def sample_entries():
    """The 12 samples, titled from the headings of references/05_catalog.md ("## 01 clock — arched body ...")."""
    by_number = {sid[:2]: sid for sid in SAMPLE_IDS}
    found = {}
    for number, word, summary in CATALOG_HEADING.findall(CATALOG.read_text(encoding="utf-8")):
        sid = by_number.get(number)
        if sid:
            found[sid] = {"title": word.replace("_", " ").capitalize(), "summary": summary[0].upper() + summary[1:]}
    missing = [s for s in SAMPLE_IDS if s not in found]
    if missing:
        raise SystemExit(f"{CATALOG.name} has no heading for {', '.join(missing)}")
    return [{"id": sid, "group": "samples", "number": sid[:2], **found[sid], "based_on": [], "mechanisms": [],
             "printed": False, "preview": SKILL_DIR / "assets" / "samples" / sid / "preview.png", "design": None,
             "meta": None, "safety": []}
            for sid in SAMPLE_IDS]


def model_entries(models_dir):
    entries = []
    for d in models.model_dirs(models_dir):
        meta = json.loads((d / "model.json").read_text(encoding="utf-8"))   # checked by tools/models.py check
        entries.append({"id": d.name, "group": "models", "number": d.name[:3], "title": meta["title"],
                        "summary": meta["summary"], "based_on": meta["based_on"], "mechanisms": meta["mechanisms"],
                        "printed": meta["printed"], "preview": d / "preview.png", "design": d / "design.py",
                        "meta": meta, "safety": safety_notes(d / "rationale.md")})
    return entries


SAFETY = re.compile(r"^Safety \(.*?(?=\n\s*\n|\Z)", re.M | re.S)


def safety_notes(rationale):
    """The "Safety (...): ..." paragraphs of a model's rationale.md (batteries, heat, food, magnets, mounting), one
    string each, so the page shows them next to the downloads."""
    if not rationale.is_file():
        return []
    return [" ".join(p.split()) for p in SAFETY.findall(rationale.read_text(encoding="utf-8"))]


def thumbnail(png, out):
    with Image.open(png) as im:
        im.convert("RGB").resize(THUMB_SIZE, Image.LANCZOS).save(out, "WEBP", quality=82, method=6)


def stl_zip(export_dir, out):
    """The print-oriented STLs of one design (print_<part>[_x<qty>].stl) in one zip."""
    files = sorted(p for p in Path(export_dir).iterdir() if p.name.startswith("print_") and p.suffix == ".stl")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in files:
            info = zipfile.ZipInfo(p.name, ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, p.read_bytes())
    return [p.name for p in files]


def build_model(job):
    """Write the files of one design into out/models/<id>/ and return what the page needs to know about it.

    Runs in a worker process, so a design from models/ is loaded here when the worker does not have it yet.
    """
    entry, out = job
    if entry["id"] not in fdm_samples.SAMPLES:
        models.load_design(Path(entry["design"]).parent)
    mid = entry["id"]
    d = Path(out) / "models" / mid
    d.mkdir(parents=True, exist_ok=True)
    data, glb = viewer.model(mid, entry["meta"])
    (d / "model.glb").write_bytes(glb)
    (d / f"{mid}_viewer.html").write_text(viewer.page(data, glb), encoding="utf-8")
    with tempfile.TemporaryDirectory() as work:
        fdm_samples.export(work, [mid])
        shutil.copyfile(Path(work) / mid / f"{mid}_assembly.step", d / f"{mid}_assembly.step")
        stls = stl_zip(Path(work) / mid, d / f"{mid}_print_stl.zip")
    thumbnail(entry["preview"], d / "thumb.webp")
    files = {
        "step": f"{mid}_assembly.step",
        "stl": f"{mid}_print_stl.zip",
        "viewer": f"{mid}_viewer.html",
    }
    return {
        "size": data["size"], "view": data["view"], "zoom": data["zoom"], "parts": data["parts"],
        "stl_files": stls,
        "downloads": {k: {"file": f, "bytes": (d / f).stat().st_size} for k, f in files.items()},
        "glb_bytes": len(glb),
    }


def mm(v):
    return f"{v:g}"


def card(e):
    w, h = THUMB_SIZE
    eager = "eager" if e["index"] < 8 else "lazy"   # the first two rows on a desktop
    size = " × ".join(mm(v) for v in e["size"])
    return (f'<li><a class="card" href="#{escape(e["id"])}" data-id="{escape(e["id"])}">'
            f'<img src="models/{escape(e["id"])}/thumb.webp" width="{w // 2}" height="{h // 2}" alt="" '
            f'loading="{eager}" decoding="async">'
            f'<span class="num">{escape(e["number"])}</span>'
            f'<span class="title">{escape(e["title"])}</span>'
            f'<span class="meta">{size} mm</span></a></li>')


def section(group, entries, heading, lead, empty):
    cards = "\n".join(card(e) for e in entries) if entries else f'<li class="empty">{empty}</li>'
    return (f'<section class="list" id="{group}" aria-labelledby="{group}-h">\n'
            f'<div class="list-head"><h2 id="{group}-h">{heading}</h2><span class="count">{len(entries)}</span></div>\n'
            f'<p class="lead2">{lead}</p>\n<ul class="grid">\n{cards}\n</ul>\n</section>')


def page_data(entries):
    keep = ("id", "group", "number", "title", "summary", "based_on", "mechanisms", "printed", "size", "view", "zoom",
            "parts", "downloads", "safety")
    titles = {e["id"]: e["title"] for e in entries if e["group"] == "samples"}
    return {"models": [{k: e[k] for k in keep} for e in entries], "sample_titles": titles}


def page(entries):
    html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
    samples = [e for e in entries if e["group"] == "samples"]
    made = [e for e in entries if e["group"] == "models"]
    fill = {
        "<!--MODELS-->": section("models", made, "Models", "Designed with the skill. Select one to turn it in 3D.",
                                 "None yet. The samples below show what the skill makes."),
        "<!--SAMPLES-->": section("samples", samples, "Samples",
                                  "The objects that come with the skill, as starting points for new designs.",
                                  "None in this build."),
        '"__DATA__"': json.dumps(page_data(entries), separators=(",", ":")).replace("<", "\\u003c"),
        "__REPO__": REPO_URL,
    }
    missing = [k for k in fill if k not in html]
    if missing:
        raise SystemExit(f"site/index.html has no {missing}")
    return re.sub("|".join(map(re.escape, fill)), lambda m: fill[m.group(0)], html)


INLINE = re.compile(r"<(script|style)>(.*?)</\1>", re.S)


def headers(html):
    """site/_headers with the hashes of the inline <style> and <script> blocks of the page, so that the CSP allows
    them and nothing else inline."""
    hashes = {"script": [], "style": []}
    for tag, body in INLINE.findall(html):
        digest = base64.b64encode(hashlib.sha256(body.encode("utf-8")).digest()).decode("ascii")
        hashes[tag].append(f"'sha256-{digest}'")
    text = (SITE_DIR / "_headers").read_text(encoding="utf-8")
    return text.replace("__SCRIPT_HASHES__", " ".join(hashes["script"])).replace(
        "__STYLE_HASHES__", " ".join(hashes["style"]))


def build(out, models_dir=models.MODELS_DIR, ids=None, workers=None):
    """Write the site into out (emptied first). Returns the entries in page order."""
    entries = model_entries(models_dir) + sample_entries()
    if ids:
        unknown = sorted(set(ids) - {e["id"] for e in entries})
        if unknown:
            raise SystemExit(f"no such model or sample: {', '.join(unknown)}")
        entries = [e for e in entries if e["id"] in ids]
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        index = out / "index.html"
        if not (index.is_file() and MARK in index.read_text(encoding="utf-8")):
            raise SystemExit(f"{out} is not empty and is not a site written by this tool; give another --out")
        shutil.rmtree(out)
    (out / "viewer").mkdir(parents=True)
    # spawn, not fork: forking a process that already runs threads (OCC, VTK, pytest plugins) can hang
    with ProcessPoolExecutor(max_workers=workers, mp_context=multiprocessing.get_context("spawn")) as pool:
        built = list(pool.map(build_model, [(e, str(out)) for e in entries]))
    for i, (e, b) in enumerate(zip(entries, built)):
        e.update(b, index=i)
    for name in ("three.min.js", "fdm-viewer.js", "three-LICENSE.txt"):
        shutil.copyfile(os.path.join(viewer.VIEWER_DIR, name), out / "viewer" / name)
    shutil.copyfile(SITE_DIR / "site.js", out / "site.js")
    html = page(entries)
    (out / "index.html").write_text(html, encoding="utf-8")
    (out / "_headers").write_text(headers(html), encoding="utf-8")
    (out / ".well-known").mkdir()
    shutil.copyfile(SITE_DIR / ".well-known" / "security.txt", out / ".well-known" / "security.txt")
    return entries


def sizes(out, entries):
    """Bytes the browser reads before any model is opened, and the size of the whole site."""
    out = Path(out)
    first = (out / "index.html").stat().st_size + (out / "site.js").stat().st_size
    thumbs = sum((out / "models" / e["id"] / "thumb.webp").stat().st_size for e in entries)
    eager = sum((out / "models" / e["id"] / "thumb.webp").stat().st_size for e in entries if e["index"] < 8)
    viewer_js = sum((out / "viewer" / n).stat().st_size for n in ("three.min.js", "fdm-viewer.js"))
    total = sum(p.stat().st_size for p in out.rglob("*") if p.is_file())
    return {"page": first, "thumbs_first_rows": eager, "thumbs_all": thumbs, "viewer_js": viewer_js,
            "glb_max": max(e["glb_bytes"] for e in entries), "total": total, "models": len(entries)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument("ids", nargs="*", help="only these models or samples (default: all)")
    ap.add_argument("--out", default=str(ROOT / "build" / "site"))
    ap.add_argument("--models-dir", default=str(models.MODELS_DIR), help=argparse.SUPPRESS)
    ap.add_argument("--workers", type=int, default=None, help="processes (default: one per CPU)")
    a = ap.parse_args(argv)
    entries = build(a.out, a.models_dir, a.ids, a.workers)
    s = sizes(a.out, entries)
    mb = lambda n: f"{n / 1e6:.2f} MB"   # noqa: E731
    print(f"wrote {a.out}: {s['models']} models, {mb(s['total'])} in all")
    print(f"  first load: page {mb(s['page'])} + thumbnails of the first rows {mb(s['thumbs_first_rows'])}"
          f" (all thumbnails {mb(s['thumbs_all'])}, read as they scroll into view)")
    print(f"  on first open: 3D viewer {mb(s['viewer_js'])} once, then one GLB per model (largest {mb(s['glb_max'])})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
