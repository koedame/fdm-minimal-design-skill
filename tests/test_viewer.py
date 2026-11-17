import base64
import html
import json
import re
import struct
import sys
from html.parser import HTMLParser

import pytest

from conftest import FIXTURE, ROOT

sys.path.insert(0, str(ROOT / "skills" / "fdm-minimal-design" / "scripts"))
import cadquery as cq    # noqa: E402
import fdm_samples       # noqa: E402
import viewer            # noqa: E402


@pytest.fixture(scope="module")
def remote_page(tmp_path_factory):
    """The viewer of 02_remote: parts with qty > 1, an inlay (anchor) and several print orientations."""
    with open(viewer.write("02_remote", tmp_path_factory.mktemp("viewers")), encoding="utf-8") as f:
        return f.read()


def embedded(html):
    data = json.loads(re.search(r"const DATA = (.*);\n", html).group(1))
    glb = base64.b64decode(json.loads(re.search(r'const GLB = (".*");\n', html).group(1)))
    return data, glb


def gltf_json(glb):
    magic, version, length = struct.unpack("<III", glb[:12])
    assert (magic, version, length) == (0x46546C67, 2, len(glb))
    size, kind = struct.unpack("<II", glb[12:20])
    assert kind == 0x4E4F534A
    return json.loads(glb[20:20 + size])


class References(HTMLParser):
    """Collects every tag and every attribute that could make a browser load something."""

    def __init__(self):
        super().__init__()
        self.tags, self.loads, self.css = set(), [], []
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        self.tags.add(tag)
        self._in_style = tag == "style"
        for name, value in attrs:
            if name in ("src", "href", "srcset", "data", "poster", "action", "background") or name.startswith("on"):
                self.loads.append((tag, name, value))

    def handle_endtag(self, tag):
        self._in_style = False

    def handle_data(self, data):
        if self._in_style:
            self.css.append(data)


def test_when_a_design_is_written_the_page_holds_every_part_with_its_colour_and_orientation(remote_page):
    data, _ = embedded(remote_page)
    parts = fdm_samples.SAMPLES["02_remote"]()
    assert [p["name"] for p in data["parts"]] == list(parts)
    by_name = {p["name"]: p for p in data["parts"]}
    assert by_name["key"]["qty"] == 12
    assert by_name["ir_window_inlay"]["anchor"] == "face_plate"
    assert by_name["face_plate"]["orientation"] == "Upside down, top on the bed"
    assert by_name["key_power"]["color"] == viewer.hex_color(fdm_samples.ACC)
    assert data["size"] == [52.0, 152.0, 15.2]


def test_when_a_design_is_written_the_glb_has_an_assembled_and_a_print_node_for_every_part(remote_page):
    data, glb = embedded(remote_page)
    doc = gltf_json(glb)
    roots = {doc["nodes"][i]["name"]: doc["nodes"][i] for i in doc["scenes"][0]["nodes"]}
    assert set(roots) == {"assembled", "print"}
    for group in roots.values():
        assert [doc["nodes"][c]["extras"]["part"] for c in group["children"]] == [p["name"] for p in data["parts"]]


def test_when_a_page_is_written_it_loads_no_other_file_and_nothing_from_the_network(remote_page):
    _, glb = embedded(remote_page)
    refs = References()
    refs.feed(remote_page)
    assert refs.loads == []
    assert not refs.tags & {"link", "img", "iframe", "object", "embed", "video", "audio", "source", "base"}
    assert not re.search(r"url\(|@import", "".join(refs.css))
    doc = gltf_json(glb)
    assert all("uri" not in b for b in doc["buffers"])
    assert "images" not in doc and "textures" not in doc
    assert "/*THREE*/" not in remote_page and "/*MENU*/" not in remote_page and "/*DIMS*/" not in remote_page and "__DATA__" not in remote_page and "__GLB__" not in remote_page


def test_when_a_page_is_written_the_viewer_scripts_do_not_fetch_anything():
    for name in ("fdm-viewer.js", "part-menu.js", "dimensions.js", "page.js"):
        code = viewer.asset(name)
        assert not re.search(r"\bfetch\(|XMLHttpRequest|import\(|https?://(?!www\.w3\.org/2000/svg)", code), name


def test_when_the_page_is_written_the_three_js_licence_is_inside_it(remote_page):
    licence = viewer.asset("three-LICENSE.txt")
    assert licence.startswith("The MIT License")
    assert html.escape(licence) in remote_page


def test_when_a_design_from_a_module_is_written_with_the_cli_it_produces_one_html_file(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["viewer.py", "001_pen_cup", "--module", str(FIXTURE / "design.py"),
                                      "--out", str(tmp_path)])
    viewer.main()
    assert (tmp_path / "001_pen_cup.html").is_file()
    assert "wrote" in capsys.readouterr().out
    data, _ = embedded((tmp_path / "001_pen_cup.html").read_text(encoding="utf-8"))
    assert [p["orientation"] for p in data["parts"]] == ["Bottom down"]     # as written in its model.json


def test_when_a_design_has_no_model_json_the_orientation_is_worked_out_from_the_shapes(tmp_path, monkeypatch):
    design = tmp_path / "design.py"
    design.write_text((FIXTURE / "design.py").read_text().replace('"..", "..", "..", "skills"', '"skills"'))
    monkeypatch.setenv("FDM_SCRIPTS", str(ROOT / "skills" / "fdm-minimal-design" / "scripts"))
    monkeypatch.setattr(sys, "argv", ["viewer.py", "001_pen_cup", "--module", str(design), "--out", str(tmp_path)])
    viewer.main()
    data, _ = embedded((tmp_path / "001_pen_cup.html").read_text(encoding="utf-8"))
    assert [p["orientation"] for p in data["parts"]] == ["As used, base on the bed"]


def test_when_a_part_is_bought_it_is_in_the_assembly_but_not_in_the_print_layout():
    base = fdm_samples.box(-20, 20, -20, 20, 0, 10)
    pin = fdm_samples.cyl(1.5, 2, 16)
    fdm_samples.SAMPLES["_test_bought"] = lambda: {
        "base": fdm_samples.Part(base, base, fdm_samples.OFF),
        "pin_ref": fdm_samples.Part(pin, None, fdm_samples.DARK, ref=True)}
    try:
        data, glb = viewer.model("_test_bought", {"parts": [{"name": "pin_ref", "orientation": "Steel pin, bought"}]})
    finally:
        del fdm_samples.SAMPLES["_test_bought"]
    pin_row = next(p for p in data["parts"] if p["name"] == "pin_ref")
    assert (pin_row["ref"], pin_row["orientation"], pin_row["print_size"]) == (True, "Steel pin, bought", None)
    doc = gltf_json(glb)
    groups = {n["name"]: [doc["nodes"][c]["extras"]["part"] for c in n["children"]] for n in doc["nodes"] if "children" in n}
    assert groups == {"assembled": ["base", "pin_ref"], "print": ["base"]}


@pytest.mark.parametrize("turn, expected", [
    (lambda wp: wp, "As used, base on the bed"),
    (lambda wp: fdm_samples.rx(wp, 180), "Upside down, top on the bed"),
    (lambda wp: fdm_samples.rx(wp, 90), "Front face on the bed"),     # (x, y, z) -> (x, -z, y)
    (lambda wp: fdm_samples.rx(wp, -90), "Back face on the bed"),
    (lambda wp: wp.rotate((0, 0, 0), (0, 1, 0), 90), "Right side on the bed"),   # (x, y, z) -> (z, y, -x)
    (lambda wp: wp.rotate((0, 0, 0), (0, 1, 0), -90), "Left side on the bed"),
    (lambda wp: fdm_samples.rz(fdm_samples.rx(wp, 180), 30), "Upside down, top on the bed"),
])
def test_when_a_part_is_turned_for_printing_the_face_on_the_bed_is_named(turn, expected):
    # a wedge-like part with no symmetry: a box with a block on its top front left corner
    wp = fdm_samples.box(0, 40, 0, 30, 0, 10).union(fdm_samples.box(0, 10, 0, 8, 10, 25))
    part = fdm_samples.Part(wp, turn(wp), fdm_samples.OFF)
    assert viewer.orientation(part) == expected


def test_when_a_part_is_printed_at_an_angle_that_is_not_a_quarter_turn_it_is_called_tilted():
    wp = fdm_samples.box(0, 40, 0, 30, 0, 10).union(fdm_samples.box(0, 10, 0, 8, 10, 25))
    part = fdm_samples.Part(wp, fdm_samples.rx(wp, 30), fdm_samples.OFF)
    assert viewer.orientation(part) == "Tilted for printing"


def test_when_parts_are_laid_out_for_printing_no_two_overlap_and_the_tallest_is_at_the_back():
    slots = [(20, 20, 5), (144, 72, 88), (123.5, 75.9, 2.4), (144, 72, 11), (13, 13, 12)]
    at = viewer.layout(slots)
    rects = [(x, y, x + w, y + d) for (x, y), (w, d, _) in zip(at, slots)]
    for i, a in enumerate(rects):
        for b in rects[i + 1:]:
            assert a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1], (a, b)
    assert max(r[3] for r in rects) == rects[1][3]


def test_when_a_model_is_meshed_the_triangles_cover_the_shape(tmp_path):
    shape = viewer.shape_of(cq.Workplane("XY").box(10, 20, 30))
    pos, idx = viewer.tessellate(shape, viewer.TOLERANCE, viewer.ANGULAR_TOLERANCE)
    xs, ys, zs = pos[0::3], pos[1::3], pos[2::3]
    assert (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)) == pytest.approx((10, 20, 30))
    assert len(idx) == 12 * 3 and max(idx) < len(pos) // 3
