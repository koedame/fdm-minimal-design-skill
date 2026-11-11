import sys

import pytest
from PIL import Image, ImageChops

from conftest import FIXTURE, ROOT

sys.path.insert(0, str(ROOT / "skills" / "fdm-minimal-design" / "scripts"))
import fdm_samples   # noqa: E402
import render        # noqa: E402

BACKGROUND = (247, 247, 245)


def drawn_box(png):
    """The box of the pixels that are not background, and the image size."""
    im = Image.open(png).convert("RGB")
    diff = ImageChops.difference(im, Image.new("RGB", im.size, BACKGROUND)).convert("L").point(lambda v: 255 * (v > 3))
    return diff.getbbox(), im.size


@pytest.mark.parametrize("w, d, h", [(20, 20, 200), (200, 40, 20)])
def test_when_no_zoom_is_given_the_design_fills_the_image_without_touching_its_edges(tmp_path, w, d, h):
    tall = fdm_samples.box(0, w, 0, d, 0, h)
    fdm_samples.SAMPLES["_test_frame"] = lambda: {"block": fdm_samples.Part(tall, tall, fdm_samples.OFF)}
    try:
        png = render.render("_test_frame", str(tmp_path / "f.png"), size=(500, 400))
    finally:
        del fdm_samples.SAMPLES["_test_frame"]
    (x0, y0, x1, y1), (iw, ih) = drawn_box(png)
    assert x0 > 0 and y0 > 0 and x1 < iw and y1 < ih             # nothing is cut off
    assert max((x1 - x0) / iw, (y1 - y0) / ih) > 0.8             # and it is not lost in the frame


def test_when_view_starts_with_a_negative_number_the_cli_takes_it_as_the_direction(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["render.py", "001_pen_cup", "--module", str(FIXTURE / "design.py"),
                                      "--out", str(tmp_path), "--view", "-0.6", "-1", "0.4"])
    render.main()
    assert (tmp_path / "001_pen_cup.png").is_file()


def test_when_model_json_has_a_view_it_gives_the_direction_and_the_zoom():
    assert render.meta_view({"view": {"direction": [-1, -1, 0.5], "zoom": 1.3}}) == ((-1, -1, 0.5), 1.3)
    assert render.meta_view({"view": {"direction": [-1, -1, 0.5]}}) == ((-1, -1, 0.5), None)
    assert render.meta_view({}) is None
