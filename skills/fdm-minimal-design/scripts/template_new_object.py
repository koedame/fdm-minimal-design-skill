"""
Template for a new design. Copy this file, rename the function, and replace the body.

  python template_new_object.py --out out          # export STL (print orientation) + STEP
  python verify.py pen_cup --module template_new_object.py
  python render.py pen_cup --module template_new_object.py --out previews

Steps (references/04_review.md):
  1. Fill in the dimension rationale table below BEFORE modelling. A number you cannot justify
     is a number that will look unfinished.
  2. Pick the nearest sample(s) in references/05_catalog.md and reuse their helpers.
  3. Model in the assembly frame (Z up in use). Give each part its print orientation in Part.prn.
  4. Run verify.py and render.py, then walk references/03_dos_donts.md top to bottom.

Dimension rationale (example below: a square pen cup)
  | dimension     | value | why                                             |
  | plan          | 72x72 | grid 4                                          |
  | height        | 108   | 3:2 to the plan                                 |
  | plan radius   | 12    | same as the other samples of this size          |
  | wall          | 2.52  | 6 lines                                         |
  | plinth        | 2.4 / inset 1.2 | floating base (one precise detail)     |
  | accent        | none  | nothing on a pen cup has a function to point at |
"""
import os
import sys

# fdm_samples.py must be importable: keep this file next to it, or set FDM_SCRIPTS to its folder
sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.dirname(os.path.abspath(__file__))))
from fdm_samples import (Part, SAMPLES, T, CH, CH_BED, OFF, rrect, feet, export)  # noqa: E402


def pen_cup():
    S, H, R = 72.0, 108.0, 12.0
    PL, INSET = 2.4, 1.2
    FLOOR = 2.4
    body = rrect(S - 2 * INSET, S - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    body = body.union(rrect(S, S, R, PL, H - PL).faces("<Z").chamfer(INSET))
    body = body.cut(rrect(S - 2 * T, S - 2 * T, R - T, FLOOR, H))
    body = body.faces(">Z").chamfer(CH)                     # inner and outer rim, same value
    body = feet(body, [(sx * 24, sy * 24) for sx in (-1, 1) for sy in (-1, 1)])
    # Part(assembly shape, print-oriented shape, colour)
    return {"cup": Part(body, body, OFF)}


SAMPLES["pen_cup"] = pen_cup                                  # register so verify/render can find it


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="my_designs_out")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    export(a.out, ["pen_cup"])
