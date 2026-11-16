import base64
import copy
import datetime
import hashlib
import json
import re
import shutil
import zipfile
from html.parser import HTMLParser

import pytest

from conftest import FIXTURE, ROOT
import build_site as site_tool   # tools/build_site.py

LINKS_OUT = ("https://github.com/koedame/fdm-minimal-design-skill", "https://creativecommons.org/licenses/by/4.0/")


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    """The site built from a models/ holding 001_pen_cup, with one sample (03_tray)."""
    models_dir = tmp_path_factory.mktemp("repo") / "models"
    shutil.copytree(FIXTURE, models_dir / "001_pen_cup")
    out = tmp_path_factory.mktemp("site")
    entries = site_tool.build(out, models_dir, ids=["001_pen_cup", "03_tray"], workers=2)
    return out, entries, (out / "index.html").read_text(encoding="utf-8")


def model_html(out, mid):
    return (out / "models" / mid / "index.html").read_text(encoding="utf-8")


def all_pages(out):
    return {p.relative_to(out).as_posix(): p.read_text(encoding="utf-8") for p in sorted(out.rglob("*.html"))
            if not p.is_relative_to(out / "downloads")}


class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def tags(html):
    p = Tags()
    p.feed(html)
    return p.tags


def model_data(html):
    return json.loads(re.search(r'<script type="application/json" id="model-data">(.*?)</script>', html).group(1))


def head_tags(html):
    """{name or property: content} of the <meta> tags, and the canonical address, of a page."""
    found = {}
    for t, a in tags(html):
        if t == "meta" and ("name" in a or "property" in a):
            found[a.get("name") or a["property"]] = a["content"]
        if t == "link" and a.get("rel") == "canonical":
            found["canonical"] = a["href"]
    return found


def test_when_a_model_is_in_models_it_is_listed_before_the_samples_as_a_link_to_its_own_page(built):
    out, _, html = built
    cards = [a["href"] for t, a in tags(html) if t == "a" and a.get("class") == "card"]
    assert cards == ["/models/001_pen_cup/", "/models/03_tray/"]
    assert 'Pen cup</span><span class="meta">72 × 72 × 108 mm' in html
    for href in cards:
        assert (out / href.strip("/") / "index.html").is_file()


def test_when_a_model_page_is_read_without_javascript_it_holds_the_name_summary_parts_and_downloads(built):
    out, _, _ = built
    html = model_html(out, "03_tray")
    assert '<h1 class="mhead"><span class="num">03</span> Tray</h1>' in html
    assert '<p class="summary">A container with no extra parts</p>' in html
    assert html.count("<tr data-part=") == len(model_data(html)["parts"]) >= 1
    downloads = [a["href"] for t, a in tags(html) if t == "a" and "download" in a]
    assert downloads == [f"/downloads/03_tray/03_tray_{f}" for f in ("assembly.step", "print_stl.zip", "viewer.html")]
    for t, a in tags(html):
        if t == "a" and "download" in a:
            assert a["download"] == a["href"].rsplit("/", 1)[1]   # saved under its own name, not the served one
    assert "not printed yet" in html


def test_when_a_model_page_is_shared_or_found_it_has_its_own_title_description_canonical_and_image(built):
    out, _, _ = built
    html = model_html(out, "001_pen_cup")
    meta = head_tags(html)
    page = f"{site_tool.SITE_URL}/models/001_pen_cup/"
    assert re.search(r"<title>Pen cup — [^<]*fdm-minimal-design</title>", html)
    assert meta["canonical"] == meta["og:url"] == page
    assert meta["description"].startswith("A square cup for pens on a floating plinth. ") and meta["og:description"] == meta["description"]
    assert meta["og:title"].startswith("Pen cup")
    assert meta["og:image"] == page + "preview.png" and (out / "models" / "001_pen_cup" / "preview.png").is_file()
    assert meta["twitter:card"] == "summary_large_image"
    home = head_tags(built[2])
    assert home["canonical"] == site_tool.SITE_URL + "/" and home["description"] != meta["description"]


def test_when_the_site_is_built_the_sitemap_lists_the_home_page_and_every_model_page_and_robots_points_to_it(built):
    out, entries, _ = built
    locs = re.findall(r"<loc>(.*?)</loc>", (out / "sitemap.xml").read_text(encoding="utf-8"))
    assert locs == [site_tool.SITE_URL + "/"] + [f"{site_tool.SITE_URL}/models/{e['id']}/" for e in entries]
    robots = (out / "robots.txt").read_text(encoding="utf-8")
    assert f"Sitemap: {site_tool.SITE_URL}/sitemap.xml" in robots.splitlines()
    assert "Disallow: /downloads/" in robots.splitlines() and "Disallow: /\n" not in robots


def test_when_the_site_is_built_it_has_a_not_found_page_and_the_host_is_set_to_send_it_with_404(built):
    # the answer itself (404, not the home page) is checked against wrangler dev and the live site
    out, _, _ = built
    assert "There is no page at this address" in (out / "404.html").read_text(encoding="utf-8")
    wrangler = (ROOT / "wrangler.jsonc").read_text(encoding="utf-8")
    assert '"not_found_handling": "404-page"' in wrangler and '"html_handling": "auto-trailing-slash"' in wrangler


def three_models(built):
    """The built entries as three models a, b, c (page order), for writing pages without building again."""
    _, entries, _ = built
    return [{**copy.deepcopy(entries[0]), "id": mid, "title": mid.upper()} for mid in ("a", "b", "c")]


def test_when_models_are_paged_through_previous_and_next_go_to_the_neighbours_and_round_the_ends(built):
    entries = three_models(built)
    links = [{a["id"]: a["href"] for t, a in tags(site_tool.model_page(entries, i, {}))
              if t == "a" and a.get("id") in ("prev", "next")} for i in range(3)]
    assert links == [{"prev": "/models/c/", "next": "/models/b/"},
                     {"prev": "/models/a/", "next": "/models/c/"},
                     {"prev": "/models/b/", "next": "/models/a/"}]


def test_when_a_part_name_holds_html_it_is_text_in_the_table_and_does_not_end_the_data_block(built):
    entries = three_models(built)
    entries[0]["parts"][0]["name"] = '</script><img src=x onerror=alert(1)>'
    html = site_tool.model_page(entries, 0, {})
    assert "<img src=x" not in html and html.count("</script>") == 2
    assert model_data(html)["parts"][0]["name"] == '</script><img src=x onerror=alert(1)>'
    assert "&lt;/script&gt;&lt;img src=x onerror=alert(1)&gt;" in html


def test_when_a_model_page_has_parts_each_row_has_a_switch_to_show_it_and_a_button_to_see_through_it(built):
    out, _, _ = built
    html = model_html(out, "03_tray")
    names = [p["name"] for p in model_data(html)["parts"]]
    assert [a["data-part"] for t, a in tags(html) if t == "tr" and "data-part" in a] == names
    boxes = [a for t, a in tags(html) if t == "input" and a.get("type") == "checkbox"]
    sees = [a for t, a in tags(html) if t == "button" and a.get("class") == "see"]
    assert [a["aria-label"] for a in boxes] == [f"Show {n.replace('_', ' ')}" for n in names]
    assert all("checked" in a for a in boxes) and all(a["aria-pressed"] == "false" for a in sees)
    assert 'id="parts-all"' in html
    css = (ROOT / "site" / "style.css").read_text(encoding="utf-8")
    assert ".model:not(.js) :is(.part input, .see, #parts-all) { display: none; }" in css   # inert without the script


def test_when_a_model_is_built_its_step_print_stls_viewer_and_meshes_are_ready_to_download(built):
    out, entries, _ = built
    m = entries[0]
    d = out / "downloads" / "001_pen_cup"
    assert (d / m["downloads"]["step"]["file"]).read_bytes().startswith(b"ISO-10303-21")
    with zipfile.ZipFile(d / m["downloads"]["stl"]["file"]) as z:
        assert z.namelist() == ["print_cup.stl"]
        assert len(z.read("print_cup.stl")) > 84   # more than an empty STL
    viewer_html = (d / m["downloads"]["viewer"]["file"]).read_text(encoding="utf-8")
    assert "const DATA = {" in viewer_html and "const GLB = \"" in viewer_html
    assert (out / "models" / "001_pen_cup" / "model.glb").read_bytes()[:4] == b"glTF"
    for k in ("step", "stl", "viewer"):
        assert m["downloads"][k]["bytes"] == (d / m["downloads"][k]["file"]).stat().st_size
    assert sorted(p.name for p in d.iterdir()) == sorted(f["file"] for f in m["downloads"].values())


def test_when_a_model_has_several_parts_its_page_data_holds_each_with_colour_qty_and_print_size(built):
    out, _, _ = built
    tray = model_data(model_html(out, "03_tray"))
    assert tray["id"] == "03_tray" and len(tray["view"]) == 3
    assert all(set(p) >= {"name", "color", "qty", "orientation", "print_size", "anchor"} for p in tray["parts"])


def loads(html):
    """What a page makes the browser read: (tag, address) of every src, and of every <link> but the canonical."""
    found = []
    for tag, a in tags(html):
        for k in ("src", "srcset", "data", "poster", "action", "background"):
            if k in a:
                found.append((tag, a[k]))
        if tag == "link" and a.get("rel") != "canonical":
            found.append((tag, a.get("href")))
    return sorted(found)


def test_when_a_page_is_opened_it_reads_only_its_images_and_script_from_this_site(built):
    out, _, html = built
    assert loads(html) == [("img", "/models/001_pen_cup/thumb.webp"), ("img", "/models/03_tray/thumb.webp")]
    assert loads(model_html(out, "03_tray")) == [("img", "/models/03_tray/preview.png"), ("script", "/site.js")]
    for name, page in all_pages(out).items():
        for _, path in loads(page):
            assert (out / path.lstrip("/")).is_file(), (name, path)
        assert not re.search(r"url\(|@import|@font-face", page), name


def test_when_a_page_links_outside_it_is_only_to_the_repository_and_the_licence(built):
    out, _, _ = built
    allowed = lambda h: any(h == b or h.startswith(b.rstrip("/") + "/") for b in LINKS_OUT)   # noqa: E731
    for name, html in all_pages(out).items():
        outside = {a["href"] for t, a in tags(html) if t == "a" and a.get("href", "").startswith(("http:", "https:", "//"))}
        assert outside and all(allowed(h) for h in outside), (name, outside)
    assert not allowed(LINKS_OUT[0] + "-lookalike")


def test_when_a_model_page_starts_its_3d_view_the_script_reads_only_files_of_this_site():
    code = (ROOT / "site" / "site.js").read_text(encoding="utf-8")
    assert not re.search(r"https?://|//[a-z0-9.-]+\.[a-z]{2,}/|XMLHttpRequest|import\(|sendBeacon|document\.cookie", code)
    assert not re.search(r"localStorage|sessionStorage|indexedDB", code)
    assert re.findall(r"\bfetch\(([^)]*)\)", code) == ["`/models/${m.id}/model.glb`"]
    assert sorted(re.findall(r'loadScript\("([^"]+)"\)', code)) == ["/viewer/fdm-viewer.js", "/viewer/three.min.js"]


def test_when_the_site_is_built_the_3d_view_and_the_three_js_licence_are_copied_from_the_skill(built):
    out, _, _ = built
    for name in ("three.min.js", "fdm-viewer.js", "three-LICENSE.txt"):
        assert (out / "viewer" / name).read_bytes() == (ROOT / "skills" / "fdm-minimal-design" / "scripts" / "viewer" / name).read_bytes()


def test_when_list_images_are_made_they_are_small_webp_at_twice_the_cell_size(built):
    out, _, _ = built
    for mid in ("001_pen_cup", "03_tray"):
        thumb = (out / "models" / mid / "thumb.webp").read_bytes()
        assert thumb[:4] == b"RIFF" and thumb[8:12] == b"WEBP"
        assert len(thumb) < 30_000
    from PIL import Image
    with Image.open(out / "models" / "03_tray" / "thumb.webp") as im:
        assert im.size == site_tool.THUMB_SIZE


def test_when_the_samples_are_listed_each_takes_its_title_and_summary_from_the_catalogue():
    entries = site_tool.sample_entries()
    assert [e["id"] for e in entries] == site_tool.SAMPLE_IDS and len(entries) == 12
    titles = {e["id"]: (e["title"], e["summary"]) for e in entries}
    assert titles["07_hinged_case"] == ("Hinged case", "A box with an opening lid")
    assert titles["01_clock"] == ("Clock", "Arched body + round dial")
    assert all(e["preview"].is_file() for e in entries)


def test_when_an_unknown_id_is_asked_for_the_build_stops_without_writing(tmp_path, models_dir):
    with pytest.raises(SystemExit, match="no such model or sample: 999_nothing"):
        site_tool.build(tmp_path / "site", models_dir, ids=["999_nothing"])
    assert not (tmp_path / "site").exists()


def test_when_models_has_no_model_yet_the_models_section_stays_with_a_note_and_the_samples_are_listed(tmp_path):
    empty = tmp_path / "models"
    empty.mkdir()
    site_tool.build(tmp_path / "site", empty, ids=["03_tray"], workers=1)
    html = (tmp_path / "site" / "index.html").read_text(encoding="utf-8")
    assert 'id="models"' in html and "None yet." in html     # the "Models" link of the header has a target
    assert [a["href"] for t, a in tags(html) if t == "a" and a.get("class") == "card"] == ["/models/03_tray/"]


@pytest.fixture(scope="module")
def odd(tmp_path_factory):
    """The site of 001_pen_cup with HTML in its title and in a safety note of its rationale.md."""
    models_dir = tmp_path_factory.mktemp("repo") / "models"
    shutil.copytree(FIXTURE, models_dir / "001_pen_cup")
    meta_path = models_dir / "001_pen_cup" / "model.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["title"] = '</script><b class="x">Cup & "co"</b>'
    meta_path.write_text(json.dumps(meta), encoding="utf-8")
    (models_dir / "001_pen_cup" / "rationale.md").write_text(
        "# Cup\n\nSafety (heat): keep it <b>below</b> 50 °C & dry.\n", encoding="utf-8")
    out = tmp_path_factory.mktemp("site")
    site_tool.build(out, models_dir, ids=["001_pen_cup"], workers=1)
    return out


def test_when_a_title_holds_html_it_is_shown_as_text_on_the_list_and_on_the_model_page(odd):
    shown = "&lt;/script&gt;&lt;b class=&quot;x&quot;&gt;Cup &amp; &quot;co&quot;&lt;/b&gt;"
    for html in ((odd / "index.html").read_text(encoding="utf-8"), model_html(odd, "001_pen_cup")):
        assert "<b class" not in html and shown in html
    page = model_html(odd, "001_pen_cup")
    assert f"<title>{shown} — " in page and f'<h1 class="mhead"><span class="num">001</span> {shown}</h1>' in page
    assert page.count("</script>") == 2   # the data block and site.js, nothing ended early
    assert head_tags(page)["og:title"].startswith('</script><b class="x">Cup & "co"</b>')


def test_when_a_rationale_has_safety_notes_the_model_page_shows_them_as_text_and_omits_the_section_without(odd, built):
    page = model_html(odd, "001_pen_cup")
    assert '<section class="notes" id="safety">' in page
    assert "<p>Safety (heat): keep it &lt;b&gt;below&lt;/b&gt; 50 °C &amp; dry.</p>" in page
    out, _, _ = built
    assert 'id="safety"' not in model_html(out, "001_pen_cup")


def test_when_out_is_a_folder_with_other_files_the_build_stops_without_deleting_them(tmp_path, models_dir):
    out = tmp_path / "somewhere"
    out.mkdir()
    (out / "notes.txt").write_text("keep me", encoding="utf-8")
    with pytest.raises(SystemExit, match="not a site written by this tool"):
        site_tool.build(out, models_dir, ids=["001_pen_cup"], workers=1)
    assert (out / "notes.txt").read_text(encoding="utf-8") == "keep me"


def test_when_the_site_is_built_again_into_the_same_folder_the_old_files_are_replaced(tmp_path, models_dir):
    out = tmp_path / "site"
    site_tool.build(out, models_dir, ids=["001_pen_cup"], workers=1)
    (out / "models" / "stale.txt").write_text("old", encoding="utf-8")
    site_tool.build(out, models_dir, ids=["001_pen_cup"], workers=1)
    assert not (out / "models" / "stale.txt").exists() and (out / "index.html").is_file()


def response_headers(out):
    """_headers as {path pattern: {header: value}}."""
    rules, path = {}, None
    for line in (out / "_headers").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        if not line[0].isspace():
            path = line.strip()
            rules[path] = {}
        else:
            name, value = line.strip().split(":", 1)
            rules[path][name] = value.strip()
    return rules


def csp(value):
    return {d.split()[0]: d.split()[1:] for d in (p.strip() for p in value.split(";")) if d}


def test_when_a_page_is_served_its_csp_allows_only_files_of_this_site_and_the_one_inline_style_of_the_pages(built):
    out, _, html = built
    policy = csp(response_headers(out)["/*"]["Content-Security-Policy"])
    styles = set()
    for name, page in all_pages(out).items():
        styles |= {f"'sha256-{base64.b64encode(hashlib.sha256(body.encode()).digest()).decode()}'"
                   for body in re.findall(r"<style>(.*?)</style>", page, re.S)}
        scripts = [a for t, a in tags(page) if t == "script"]
        # a script is a file of this site or a JSON data block, which the browser does not run
        assert all(a.get("src") or a.get("type") == "application/json" for a in scripts), name
        assert not re.search(r"<[^>]+\s(on[a-z]+|style)=", page), name   # no event handler or style attribute
    assert len(styles) == 1   # the same for every page, so the header stays one hash for any number of models
    assert policy["default-src"] == ["'none'"]
    assert policy["script-src"] == ["'self'"]
    assert policy["style-src"] == ["'self'"] + sorted(styles)
    for d in ("img-src", "connect-src"):
        assert policy[d] == ["'self'"]
    assert policy["base-uri"] == policy["form-action"] == policy["frame-ancestors"] == ["'none'"]
    assert "__" not in (out / "_headers").read_text(encoding="utf-8")


def test_when_the_page_is_served_it_asks_for_https_no_sniffing_no_referrer_and_no_device_access(built):
    out, _, _ = built
    h = response_headers(out)["/*"]
    assert h["Strict-Transport-Security"] == "max-age=15552000"   # the same as the zone, which overrides it
    assert h["X-Content-Type-Options"] == "nosniff" and h["Referrer-Policy"] == "no-referrer"
    assert all(p.endswith("=()") for p in h["Permissions-Policy"].split(", "))


def test_when_a_download_is_opened_it_is_saved_and_not_run_on_the_site_while_the_pages_are_shown(built):
    out, entries, _ = built
    rules = response_headers(out)
    assert rules["/downloads/*"] == {"Content-Disposition": "attachment"}
    assert [p for p, h in rules.items() if "Content-Disposition" in h] == ["/downloads/*"]
    downloads = {p.relative_to(out).as_posix() for p in (out / "downloads").rglob("*") if p.is_file()}
    assert downloads == {f"downloads/{e['id']}/{f['file']}" for e in entries for f in e["downloads"].values()}
    assert not any(p.suffix in (".step", ".zip") or p.name.endswith("_viewer.html") for p in (out / "models").rglob("*"))


def test_when_the_site_is_built_security_txt_points_to_private_reporting_and_has_not_expired(built):
    out, _, _ = built
    fields = dict(line.split(": ", 1) for line in
                  (out / ".well-known" / "security.txt").read_text(encoding="utf-8").splitlines())
    assert fields["Contact"] == LINKS_OUT[0] + "/security/advisories/new"
    expires = datetime.datetime.fromisoformat(fields["Expires"].replace("Z", "+00:00"))
    now = datetime.datetime.now(datetime.timezone.utc)
    assert now < expires < now + datetime.timedelta(days=366)
    wrangler = (ROOT / "wrangler.jsonc").read_text(encoding="utf-8")
    host = re.search(r'"pattern": "([^"]+)", "custom_domain": true', wrangler).group(1)
    assert fields["Canonical"] == f"https://{host}/.well-known/security.txt"
    assert site_tool.SITE_URL == f"https://{host}"   # the canonical addresses and the sitemap name the served host
    assert '"directory": "./build/site"' in wrangler and '"workers_dev": false' in wrangler


def test_when_a_rationale_has_safety_paragraphs_each_is_shown_with_the_model_as_one_line(tmp_path):
    rationale = tmp_path / "rationale.md"
    rationale.write_text("# Cup\n\nWhy the walls are 2 mm.\n\nSafety (food): not a food-safe container.\nKeep food in a bag.\n\n"
                         "More reasoning.\n\nSafety (magnets): keep away from children.\n", encoding="utf-8")
    assert site_tool.safety_notes(rationale) == ["Safety (food): not a food-safe container. Keep food in a bag.",
                                                 "Safety (magnets): keep away from children."]
    assert site_tool.safety_notes(tmp_path / "missing.md") == []
