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


def site_data(html):
    return json.loads(re.search(r"const SITE = (.*);</script>", html).group(1))


def test_when_a_model_is_in_models_it_is_listed_before_the_samples_with_its_title_and_size(built):
    _, _, html = built
    cards = [(a["href"], a["data-id"]) for t, a in tags(html) if t == "a" and a.get("class") == "card"]
    assert cards == [("#001_pen_cup", "001_pen_cup"), ("#03_tray", "03_tray")]
    assert 'Pen cup</span><span class="meta">72 × 72 × 108 mm' in html
    data = site_data(html)
    assert [m["id"] for m in data["models"]] == ["001_pen_cup", "03_tray"]
    assert data["models"][0]["group"] == "models" and data["models"][1]["group"] == "samples"


def test_when_a_model_is_built_its_step_print_stls_viewer_and_meshes_are_ready_to_download(built):
    out, _, html = built
    m = site_data(html)["models"][0]
    d = out / "models" / "001_pen_cup"
    assert (d / m["downloads"]["step"]["file"]).read_bytes().startswith(b"ISO-10303-21")
    with zipfile.ZipFile(d / m["downloads"]["stl"]["file"]) as z:
        assert z.namelist() == ["print_cup.stl"]
        assert len(z.read("print_cup.stl")) > 84   # more than an empty STL
    viewer_html = (d / m["downloads"]["viewer"]["file"]).read_text(encoding="utf-8")
    assert "const DATA = {" in viewer_html and "const GLB = \"" in viewer_html
    assert (d / "model.glb").read_bytes()[:4] == b"glTF"
    for k in ("step", "stl", "viewer"):
        assert m["downloads"][k]["bytes"] == (d / m["downloads"][k]["file"]).stat().st_size


def test_when_a_model_has_several_parts_the_page_data_holds_each_with_colour_qty_and_print_size(built):
    _, _, html = built
    tray = site_data(html)["models"][1]
    assert tray["title"] == "Tray" and tray["summary"] == "A container with no extra parts"
    assert all(set(p) >= {"name", "color", "qty", "orientation", "print_size"} for p in tray["parts"])
    assert len(tray["size"]) == 3


def test_when_the_page_is_opened_it_reads_only_the_page_its_script_and_list_images_from_this_site(built):
    out, _, html = built
    loads = []
    for tag, a in tags(html):
        for k in ("src", "srcset", "data", "poster", "action", "background"):
            if k in a:
                loads.append((tag, a[k]))
        if tag == "link":
            loads.append((tag, a.get("href")))
    assert sorted(loads) == [("img", "models/001_pen_cup/thumb.webp"), ("img", "models/03_tray/thumb.webp"),
                             ("script", "site.js")]
    for _, path in loads:
        assert (out / path).is_file()
    assert not re.search(r"url\(|@import|@font-face", html)


def test_when_the_page_links_outside_it_is_only_to_the_repository_and_the_licence(built):
    _, _, html = built
    outside = {a["href"] for t, a in tags(html) if t == "a" and a.get("href", "").startswith(("http:", "https:", "//"))}
    allowed = lambda h: any(h == b or h.startswith(b.rstrip("/") + "/") for b in LINKS_OUT)   # noqa: E731
    assert outside and all(allowed(h) for h in outside), outside
    assert not allowed(LINKS_OUT[0] + "-lookalike")


def test_when_a_model_is_opened_the_script_reads_only_files_of_this_site():
    code = (ROOT / "site" / "site.js").read_text(encoding="utf-8")
    assert not re.search(r"https?://|//[a-z0-9.-]+\.[a-z]{2,}/|XMLHttpRequest|import\(|sendBeacon|document\.cookie", code)
    assert re.findall(r"\bfetch\(([^)]*)\)", code) == ["`models/${m.id}/model.glb`"]
    assert sorted(re.findall(r'loadScript\("([^"]+)"\)', code)) == ["viewer/fdm-viewer.js", "viewer/three.min.js"]


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
    assert [m["id"] for m in site_data(html)["models"]] == ["03_tray"]


def test_when_a_title_holds_html_it_is_shown_as_text_and_does_not_end_the_inline_script(tmp_path, models_dir):
    meta_path = models_dir / "001_pen_cup" / "model.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["title"] = '</script><b class="x">Cup & "co"</b>'
    meta_path.write_text(json.dumps(meta), encoding="utf-8")
    site_tool.build(tmp_path / "site", models_dir, ids=["001_pen_cup"], workers=1)
    html = (tmp_path / "site" / "index.html").read_text(encoding="utf-8")
    assert "<b class" not in html and html.count("</script>") == 2
    assert "&lt;/script&gt;&lt;b class=&quot;x&quot;&gt;Cup &amp; &quot;co&quot;&lt;/b&gt;" in html
    assert site_data(html)["models"][0]["title"] == meta["title"]


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
