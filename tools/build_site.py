"""
Build the website: a home page that introduces the skill and lists every model, and a page for each model with
its 3D view, parts and downloads.

  python tools/build_site.py --out build/site                      # the 12 samples and every model in models/
  python tools/build_site.py --out build/site 06_radio 001_pen_cup # only these (quick checks)

The list is built from models/ (model.json, preview.png, design.py) and from the samples of the skill, so a
new model needs no change here. The output is plain files for any static host:

  index.html                 the home page; the list links to the page of each model
  index.md                   the home page in Markdown, for agents (<link rel="alternate" type="text/markdown">)
  llms.txt                   what the site is and the Markdown version of every model page, for agents
  models/<id>/index.html     the page of one model (/models/<id>/): its name, parts and downloads are in the HTML,
                             so it reads without JavaScript; site.js adds the 3D view
  models/<id>/index.md       the same page in Markdown (site/model.md)
  models/<id>/thumb.webp     list image
  models/<id>/preview.png    the still shown until the 3D view is ready, and the image of a shared link (og:image)
  models/<id>/model.glb      meshes for the 3D view
  downloads/<id>/<id>_assembly.step, <id>_print_stl.zip, <id>_viewer.html
                             downloads; _headers sends everything under /downloads/ as an attachment, so the viewer
                             HTML is saved and never runs on this site. They are kept out of /models/ so that the
                             rule cannot reach a page.
  site.js                    the 3D view, the parts switches and the keys of a model page
  viewer/                    three.min.js, fdm-viewer.js (the 3D view of scripts/viewer.py), part-menu.js, dimensions.js,
                             three.js licence
  404.html                   sent with status 404 for any other address (wrangler.jsonc: not_found_handling)
  sitemap.xml, robots.txt    the home page and every model page, for search engines; robots.txt also says what the
                             pages may be used for (Content-Signal)
  _headers                   response headers for Cloudflare (CSP with the hash of the inline style, UTF-8 for
                             llms.txt and the Markdown files)
  .well-known/security.txt   where to report a vulnerability

Every page has the same inline style (site/style.css) and no inline script that runs: a model's data for the 3D view
and the structured data of each page (schema.org, JSON-LD) are data blocks, which the browser does not run and the CSP
does not apply to. So the CSP allows one style hash and scripts from this site only. Nothing on the
pages is read from another server: no fonts, scripts or analytics from outside.
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
SITE_URL = "https://fdm-minimal-design.koeda.me"   # the custom domain of wrangler.jsonc; canonical and shared links
SITE_NAME = "fdm-minimal-design"
THUMB_SIZE = (480, 384)        # 2x the widest list cell on a desktop, same 5:4 as preview.png
ZIP_DATE = (1980, 1, 1, 0, 0, 0)
MARK = "<!-- Written by tools/build_site.py"   # in every page it writes; --out is emptied only when index.html has it
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


SAFETY = re.compile(r"^Safety(?: \([^)\n]*\))?:.*?(?=\n\s*\n|\Z)", re.M | re.S)
LIST_ITEM = re.compile(r"^\s*- ", re.M)


def safety_notes(rationale):
    """The "Safety: ..." and "Safety (...): ..." paragraphs of a model's rationale.md (batteries, heat, food, magnets,
    mounting), one plain-text string each (bold marks and list bullets dropped), so the page shows them next to the
    downloads."""
    if not rationale.is_file():
        return []
    return [" ".join(LIST_ITEM.sub("", p).replace("**", "").split())
            for p in SAFETY.findall(rationale.read_text(encoding="utf-8"))]


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
    """Write the files of one design into out/models/<id>/ (what its page shows) and out/downloads/<id>/, and return
    what the pages need to know about it.

    Runs in a worker process, so a design from models/ is loaded here when the worker does not have it yet.
    """
    entry, out = job
    if entry["id"] not in fdm_samples.SAMPLES:
        models.load_design(Path(entry["design"]).parent)
    mid = entry["id"]
    page_dir = Path(out) / "models" / mid
    d = Path(out) / "downloads" / mid
    page_dir.mkdir(parents=True, exist_ok=True)
    d.mkdir(parents=True, exist_ok=True)
    data, glb = viewer.model(mid, entry["meta"])
    (page_dir / "model.glb").write_bytes(glb)
    (d / f"{mid}_viewer.html").write_text(viewer.page(data, glb), encoding="utf-8")
    with tempfile.TemporaryDirectory() as work:
        fdm_samples.export(work, [mid])
        shutil.copyfile(Path(work) / mid / f"{mid}_assembly.step", d / f"{mid}_assembly.step")
        stls = stl_zip(Path(work) / mid, d / f"{mid}_print_stl.zip")
    thumbnail(entry["preview"], page_dir / "thumb.webp")
    shutil.copyfile(entry["preview"], page_dir / "preview.png")
    with Image.open(entry["preview"]) as im:
        preview_size = im.size
    files = {
        "step": f"{mid}_assembly.step",
        "stl": f"{mid}_print_stl.zip",
        "viewer": f"{mid}_viewer.html",
    }
    return {
        "size": data["size"], "view": data["view"], "zoom": data["zoom"], "parts": data["parts"],
        "stl_files": stls,
        "downloads": {k: {"file": f, "bytes": (d / f).stat().st_size} for k, f in files.items()},
        "glb_bytes": len(glb), "preview_size": preview_size,
    }


def mm(v):
    return f"{v:g}"


def mm1(v):
    """A length to 0.1 mm with thousands separators: 1,234.5 / 72."""
    return f"{round(v, 1):,.1f}".removesuffix(".0")


def dims(size):
    return " × ".join(mm1(v) for v in size)


def nbytes(n):
    return f"{n / 1e6:.1f} MB" if n >= 1e6 else f"{max(1, round(n / 1e3))} kB"


def words(s):
    return s.replace("_", " ")


def page_path(mid):
    return f"/models/{mid}/"


def card(e):
    w, h = THUMB_SIZE
    eager = "eager" if e["index"] < 8 else "lazy"   # the first two rows on a desktop
    size = " × ".join(mm(v) for v in e["size"])
    return (f'<li><a class="card" href="{escape(page_path(e["id"]))}">'
            f'<img src="/models/{escape(e["id"])}/thumb.webp" width="{w // 2}" height="{h // 2}" alt="" '
            f'loading="{eager}" decoding="async">'
            f'<span class="num">{escape(e["number"])}</span>'
            f'<span class="title">{escape(e["title"])}</span>'
            f'<span class="meta">{size} mm</span></a></li>')


def section(group, entries, heading, lead, empty):
    cards = "\n".join(card(e) for e in entries) if entries else f'<li class="empty">{empty}</li>'
    return (f'<section class="list" id="{group}" aria-labelledby="{group}-h">\n'
            f'<div class="list-head"><h2 id="{group}-h">{heading}</h2><span class="count">{len(entries)}</span></div>\n'
            f'<p class="lead2">{lead}</p>\n<ul class="grid">\n{cards}\n</ul>\n</section>')


def head(title, description, path, ld, image=None):
    """<title>, description, canonical address, the Markdown version, the tags of a shared link (Open Graph, X) and
    the structured data (ld, JSON-LD) of one page."""
    url = SITE_URL + path
    tags = [f"<title>{escape(title)}</title>",
            f'<meta name="description" content="{escape(description)}">',
            f'<link rel="canonical" href="{escape(url)}">',
            f'<link rel="alternate" type="text/markdown" href="{escape(markdown_path(path))}">',
            f'<meta property="og:site_name" content="{SITE_NAME}">',
            f'<meta property="og:type" content="website">',
            f'<meta property="og:title" content="{escape(title)}">',
            f'<meta property="og:description" content="{escape(description)}">',
            f'<meta property="og:url" content="{escape(url)}">']
    if image:
        src, (w, h), alt = image
        tags += [f'<meta property="og:image" content="{escape(SITE_URL + src)}">',
                 f'<meta property="og:image:width" content="{w}">', f'<meta property="og:image:height" content="{h}">',
                 f'<meta property="og:image:alt" content="{escape(alt)}">',
                 '<meta name="twitter:card" content="summary_large_image">']
    tags.append(f'<script type="application/ld+json">{data_block(ld)}</script>')
    return "\n".join(tags)


def data_block(value):
    """JSON for the inside of a <script> data block: no "<", so no text can end the block or open a comment."""
    return json.dumps(value, separators=(",", ":")).replace("<", "\\u003c")


def markdown_path(path):
    """The Markdown version of the page at path ("/" -> "/index.md", "/models/<id>/" -> "/models/<id>/index.md")."""
    return path + "index.md"


WEBSITE_ID = SITE_URL + "/#website"
CREATOR = {"@type": "Organization", "name": "koedame"}
LICENCE_MODELS = "https://creativecommons.org/licenses/by/4.0/"
INTRO = "An agent skill that designs minimalist objects for FDM 3D printing"


def home_ld(entries, description):
    """The site, the skill and the list of the model pages."""
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": WEBSITE_ID, "name": SITE_NAME, "url": SITE_URL + "/", "description": description,
         "inLanguage": "en", "creator": CREATOR},
        {"@type": "SoftwareSourceCode", "name": SITE_NAME, "description": INTRO + ".", "codeRepository": REPO_URL,
         "programmingLanguage": "Python", "license": REPO_URL + "/blob/main/LICENSE", "creator": CREATOR},
        {"@type": "ItemList", "name": "Models and samples", "numberOfItems": len(entries),
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": e["title"],
                              "url": SITE_URL + page_path(e["id"])} for i, e in enumerate(entries)]},
    ]}


ENCODING_FORMATS = {"step": "model/step", "stl": "application/zip", "viewer": "text/html"}


def model_ld(e, built_ids, description):
    """One model as a schema.org 3DModel, with its downloads as its encodings."""
    mid = e["id"]
    ld = {"@context": "https://schema.org", "@type": "3DModel", "name": e["title"], "description": description,
          "url": SITE_URL + page_path(mid), "image": f"{SITE_URL}/models/{mid}/preview.png",
          "license": LICENCE_MODELS, "creator": CREATOR, "isPartOf": {"@id": WEBSITE_ID},
          "encoding": [{"@type": "MediaObject", "name": DOWNLOAD_LABELS[k], "encodingFormat": ENCODING_FORMATS[k],
                        "contentUrl": f"{SITE_URL}/downloads/{mid}/{d['file']}", "contentSize": f"{d['bytes']} B"}
                       for k in DOWNLOAD_LABELS for d in [e["downloads"][k]]]}
    based = [SITE_URL + page_path(s) for s in e["based_on"] if s in built_ids]
    if based:
        ld["isBasedOn"] = based
    return ld


def fill(template, values):
    """The template of site/ with each placeholder replaced; stops when the template lacks one."""
    text = (SITE_DIR / template).read_text(encoding="utf-8")
    common = {"__REPO__": REPO_URL}
    if template.endswith(".html"):
        common["<!--STYLE-->"] = f"<style>\n{(SITE_DIR / 'style.css').read_text(encoding='utf-8')}</style>"
    values = {**common, **values}
    missing = [k for k in values if k not in text]
    if missing:
        raise SystemExit(f"site/{template} has no {missing}")
    return re.sub("|".join(map(re.escape, values)), lambda m: values[m.group(0)], text)


def no_warranty():
    return (SITE_DIR / "no-warranty.html").read_text(encoding="utf-8").strip()


HOME_DESCRIPTION = (INTRO + ", and the models designed with it, in 3D, with STEP and print-ready STL files to "
                    "download.")


def page(entries):
    samples = [e for e in entries if e["group"] == "samples"]
    made = [e for e in entries if e["group"] == "models"]
    return fill("index.html", {
        "<!--HEAD-->": head(f"{SITE_NAME} — an agent skill for minimal objects printed in FDM", HOME_DESCRIPTION, "/",
                            home_ld(entries, HOME_DESCRIPTION)),
        "<!--MODELS-->": section("models", made, "Models", "Designed with the skill. Select one to turn it in 3D.",
                                 "None yet. The samples below show what the skill makes."),
        "<!--SAMPLES-->": section("samples", samples, "Samples",
                                  "The objects that come with the skill, as starting points for new designs.",
                                  "None in this build."),
        "<!--NO_WARRANTY-->": no_warranty(),
    })


DOWNLOAD_LABELS = {"step": "STEP assembly", "stl": "STL for printing (zip)", "viewer": "3D viewer (HTML, works offline)"}


def html_link(text, path):
    return f'<a href="{escape(path)}">{escape(text)}</a>'


def md_link(text, path):
    return f"[{md(text)}]({SITE_URL + path})"


def facts(e, built_titles, sample_titles, esc=escape, link=html_link):
    """The line under the summary: size, parts, the samples it is based on (linked when built), mechanisms, printed.
    esc and link write it as HTML (the page) or as Markdown (md, md_link)."""
    n = len(e["parts"])
    out = [esc(f"{dims(e['size'])} mm"), f"{n} part{'s' if n > 1 else ''}"]
    if e["based_on"]:
        names = [link(built_titles[s], page_path(s)) if s in built_titles
                 else esc(sample_titles.get(s, words(s))) for s in e["based_on"]]
        out.append("based on " + ", ".join(names))
    if e["mechanisms"]:
        out.append(esc(", ".join(e["mechanisms"]).lower()))
    out.append("printed and checked" if e["printed"] else "not printed yet")
    return " · ".join(out)


# two squares, the front one see-through: the button that makes a part transparent
SEE_ICON = ('<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><rect x="1.5" y="1.5" width="9" '
            'height="9" rx="1.5" fill="none" stroke="currentColor"/><rect x="5.5" y="5.5" width="9" height="9" rx="1.5" '
            'fill="currentColor" fill-opacity="0.25" stroke="currentColor"/></svg>')


def how_printed(p):
    return f"{p['orientation']}, printed with {words(p['anchor'])}" if p["anchor"] else p["orientation"]


def part_row(p):
    """One row of the parts table. Its checkbox shows or hides the part in the 3D view, its button makes it
    transparent (site.js); both are hidden while the page has no script."""
    how = how_printed(p)
    size = dims(p["print_size"]) if p["print_size"] else "—"   # a bought part is not printed
    name = escape(words(p["name"]))
    return (f'          <tr data-part="{escape(p["name"])}"><td><span class="part"><label>'
            f'<input type="checkbox" checked aria-label="Show {name}">'
            f'<svg class="sw" viewBox="0 0 1 1" aria-hidden="true"><rect width="1" height="1" fill="{escape(p["color"])}"/></svg>'
            f'<span><b>{name}</b><br><span class="muted">{escape(how)}</span></span></label>'
            f'<button type="button" class="see" aria-pressed="false" title="Transparent" aria-label="Transparent {name}">'
            f'{SEE_ICON}</button></span></td>'
            f'<td class="n">{p["qty"]}</td><td class="n">{escape(size)}</td></tr>')


def description(e):
    n = len(e["parts"])
    return (f"{e['summary'].rstrip('.')}. A minimalist object for FDM 3D printing, {dims(e['size'])} mm in "
            f"{n} part{'s' if n > 1 else ''}: view it in 3D and download the STEP assembly and print-ready STL files "
            f"(CC BY 4.0).")


def model_page(entries, i, sample_titles):
    """The page of entries[i] (/models/<id>/)."""
    e = entries[i]
    mid = e["id"]
    prev, nxt = entries[i - 1], entries[(i + 1) % len(entries)]
    built_titles = {x["id"]: x["title"] for x in entries}
    still = (f"/models/{mid}/preview.png", e["preview_size"], f"{e['title']}: a rendering of the assembled model")
    downloads = "\n".join(
        f'        <li><a href="/downloads/{escape(mid)}/{escape(d["file"])}" download="{escape(d["file"])}">{label}</a>'
        f'<span class="muted">{nbytes(d["bytes"])}</span></li>'
        for k, label in DOWNLOAD_LABELS.items() for d in [e["downloads"][k]])
    safety = ""
    if e["safety"]:
        notes = "".join(f"<p>{escape(s)}</p>" for s in e["safety"])
        safety = f'    <section class="notes" id="safety">\n      <h2>Safety</h2>\n      {notes}\n    </section>\n'
    data = {"id": mid, "view": e["view"], "zoom": e["zoom"], "parts": e["parts"]}
    return fill("model.html", {
        "<!--HEAD-->": head(f"{e['title']} — 3D printable model, STEP and STL | {SITE_NAME}", description(e),
                            page_path(mid), model_ld(e, built_titles, description(e)), still),
        "__STILL__": still[0], "__STILL_W__": str(still[1][0]), "__STILL_H__": str(still[1][1]),
        "__STILL_ALT__": escape(still[2]),
        "__PREV__": page_path(prev["id"]), "__PREV_TITLE__": escape(prev["title"]),
        "__NEXT__": page_path(nxt["id"]), "__NEXT_TITLE__": escape(nxt["title"]),
        "__GROUP__": "Models" if e["group"] == "models" else "Samples",
        "__NUMBER__": escape(e["number"]), "__TITLE__": escape(e["title"]), "__SUMMARY__": escape(e["summary"]),
        "__FACTS__": facts(e, built_titles, sample_titles),
        "__PARTS__": "\n".join(part_row(p) for p in e["parts"]),
        "__DOWNLOADS__": downloads,
        "<!--SAFETY-->\n": safety,
        "__CREDIT__": escape(f"{e['title']} from fdm-minimal-design by koedame, CC BY 4.0"),
        "<!--NO_WARRANTY-->": no_warranty(),
        '"__DATA__"': data_block(data),
    })


MD_SPECIAL = re.compile(r"([\\`*_\[\]<>|#])")


def md(text):
    """Text from model.json or rationale.md as one line of Markdown that shows as written: no markup, link or HTML."""
    return MD_SPECIAL.sub(r"\\\1", " ".join(str(text).split()))


def md_no_warranty():
    return "\n\n".join(" ".join(p.split()) for p in re.findall(r"<p>(.*?)</p>", no_warranty(), re.S))


def md_list(entries):
    return "\n".join(f"- {md_link(e['number'] + ' ' + e['title'], page_path(e['id']))}: {md(e['summary'].rstrip('.'))}."
                     f" {md(dims(e['size']))} mm. Markdown: {SITE_URL + markdown_path(page_path(e['id']))}"
                     for e in entries) or "None yet."


def home_markdown(entries):
    """site/index.md: the home page in Markdown."""
    return fill("index.md", {
        "__PAGE__": SITE_URL + "/",
        "__MODELS__": md_list([e for e in entries if e["group"] == "models"]),
        "__SAMPLES__": md_list([e for e in entries if e["group"] == "samples"]),
        "<!--NO_WARRANTY-->": md_no_warranty(),
    })


def model_markdown(entries, i, sample_titles):
    """site/model.md: the page of entries[i] in Markdown, with what the HTML page holds but the 3D view."""
    e = entries[i]
    mid = e["id"]
    built_titles = {x["id"]: x["title"] for x in entries}
    parts = "\n".join(f"| {md(words(p['name']))} | {md(how_printed(p))} | {p['qty']} | "
                      f"{md(dims(p['print_size'])) if p['print_size'] else '—'} |" for p in e["parts"])
    downloads = "\n".join(f"- [{label}]({SITE_URL}/downloads/{mid}/{d['file']}): {nbytes(d['bytes'])}"
                          for k, label in DOWNLOAD_LABELS.items() for d in [e["downloads"][k]])
    safety = ""
    if e["safety"]:
        safety = "## Safety\n\n" + "\n\n".join(md(s) for s in e["safety"]) + "\n\n"
    return fill("model.md", {
        "__NUMBER__": md(e["number"]), "__TITLE__": md(e["title"]), "__SUMMARY__": md(e["summary"]),
        "__FACTS__": facts(e, built_titles, sample_titles, esc=md, link=md_link),
        "__PAGE__": SITE_URL + page_path(mid),
        "__STILL_ALT__": md(f"{e['title']}: a rendering of the assembled model"),
        "__STILL__": f"{SITE_URL}/models/{mid}/preview.png",
        "__PARTS__": parts, "__DOWNLOADS__": downloads, "<!--SAFETY-->\n": safety,
        "__CREDIT__": md(f"{e['title']} from fdm-minimal-design by koedame, CC BY 4.0"),
        "<!--NO_WARRANTY-->": md_no_warranty(),
    })


def llms_txt(entries):
    """/llms.txt (llmstxt.org): what the site is, and the Markdown version of every page."""
    def section(heading, group):
        found = [e for e in entries if e["group"] == group]
        lines = [f"- [{md(e['title'])}]({SITE_URL + markdown_path(page_path(e['id']))}): {md(e['summary'].rstrip('.'))}"
                 for e in found]
        return f"## {heading}\n\n" + ("\n".join(lines) if lines else "None yet.") + "\n"
    return (f"# {SITE_NAME}\n\n> {HOME_DESCRIPTION}\n\n"
            "Each model has a page with a 3D view and a Markdown version, linked below, that lists its size, parts "
            "(print orientation, quantity, print size), safety notes and downloads: a STEP assembly, a zip of "
            "print-ready STL files and a 3D viewer that works offline. Models and images are CC BY 4.0; the code and "
            "the skill documents are MIT. The files under /downloads/ are downloads, not pages.\n\n"
            f"- [Home page]({SITE_URL}/index.md): the skill, how to install it, and every model\n\n"
            + section("Models", "models") + "\n" + section("Samples", "samples") + "\n"
            f"## Optional\n\n- [Source]({REPO_URL}): the skill, its scripts, and the design script of every model\n")


def sitemap(entries):
    urls = "".join(f"<url><loc>{escape(SITE_URL + p)}</loc></url>\n"
                   for p in ["/"] + [page_path(e["id"]) for e in entries])
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'


CONTENT_SIGNAL = "search=yes, ai-input=yes, ai-train=no"   # contentsignals.org: searched and quoted, not trained on


def robots():
    """Every page may be crawled; the downloads are large and are not pages. Content-Signal says what the pages may be
    used for."""
    return f"User-agent: *\nContent-Signal: {CONTENT_SIGNAL}\nDisallow: /downloads/\n\nSitemap: {SITE_URL}/sitemap.xml\n"


INLINE_STYLE = re.compile(r"<style>(.*?)</style>", re.S)


def headers(pages):
    """site/_headers with the hashes of the inline <style> blocks of the pages, so that the CSP allows them and no
    other inline style. The pages share one style, so this is one hash however many models there are."""
    hashes = []
    for html in pages:
        for body in INLINE_STYLE.findall(html):
            digest = f"'sha256-{base64.b64encode(hashlib.sha256(body.encode('utf-8')).digest()).decode('ascii')}'"
            if digest not in hashes:
                hashes.append(digest)
    return (SITE_DIR / "_headers").read_text(encoding="utf-8").replace("__STYLE_HASHES__", " ".join(hashes))


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
    for name in ("three.min.js", "fdm-viewer.js", "part-menu.js", "dimensions.js", "three-LICENSE.txt"):
        shutil.copyfile(os.path.join(viewer.VIEWER_DIR, name), out / "viewer" / name)
    shutil.copyfile(SITE_DIR / "site.js", out / "site.js")
    sample_titles = {e["id"]: e["title"] for e in sample_entries()}
    pages = {"index.html": page(entries), "404.html": fill("404.html", {})}
    for i, e in enumerate(entries):
        pages[f"models/{e['id']}/index.html"] = model_page(entries, i, sample_titles)
    texts = {"index.md": home_markdown(entries), "llms.txt": llms_txt(entries)}
    for i, e in enumerate(entries):
        texts[f"models/{e['id']}/index.md"] = model_markdown(entries, i, sample_titles)
    for name, text in {**pages, **texts}.items():
        (out / name).write_text(text, encoding="utf-8")
    (out / "sitemap.xml").write_text(sitemap(entries), encoding="utf-8")
    (out / "robots.txt").write_text(robots(), encoding="utf-8")
    (out / "_headers").write_text(headers(pages.values()), encoding="utf-8")
    (out / ".well-known").mkdir()
    shutil.copyfile(SITE_DIR / ".well-known" / "security.txt", out / ".well-known" / "security.txt")
    return entries


def sizes(out, entries):
    """Bytes the browser reads for the home page, and the size of the whole site."""
    out = Path(out)
    first = (out / "index.html").stat().st_size
    thumbs = sum((out / "models" / e["id"] / "thumb.webp").stat().st_size for e in entries)
    eager = sum((out / "models" / e["id"] / "thumb.webp").stat().st_size for e in entries if e["index"] < 8)
    viewer_js = sum((out / "viewer" / n).stat().st_size for n in ("three.min.js", "fdm-viewer.js", "part-menu.js", "dimensions.js"))
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
    print(f"  on a model page: 3D viewer {mb(s['viewer_js'])} (cached after the first), and its GLB"
          f" (largest {mb(s['glb_max'])})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
