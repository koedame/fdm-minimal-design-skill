"""Test fixture: the pen cup from template_new_object.py, laid out as a model directory."""
import os
import sys

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, CH, CH_BED, OFF, rrect, feet  # noqa: E402


def pen_cup():
    S, H, R = 72.0, 108.0, 12.0
    PL, INSET = 2.4, 1.2
    FLOOR = 2.4
    body = rrect(S - 2 * INSET, S - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    body = body.union(rrect(S, S, R, PL, H - PL).faces("<Z").chamfer(INSET))
    body = body.cut(rrect(S - 2 * T, S - 2 * T, R - T, FLOOR, H))
    body = body.faces(">Z").chamfer(CH)
    body = feet(body, [(sx * 24, sy * 24) for sx in (-1, 1) for sy in (-1, 1)])
    return {"cup": Part(body, body, OFF)}


SAMPLES["001_pen_cup"] = pen_cup
