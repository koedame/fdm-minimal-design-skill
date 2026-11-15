"""061 Watch stand: a low base and a separate upright post that a buckled watch drops over, dial forward.

Two parts, both printed bottom down. The post is a 56 x 32 rounded rectangle, 46 tall, about the size of a
small wrist: a buckled strap or bracelet slides down over it and the case stands on the base in front of it,
dial facing forward. The post drops 6 into a pocket in the base with 0.25 clearance all round, so it stands
square and lifts out to take the watch off over its top or to swap for a post cut to another wrist size.
The base is the post plus a 12 margin at the sides and the back and 20 at the front, where the case stands;
it sits on a floating plinth.
"""
import os
import sys

from cadquery.selectors import BoxSelector

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, CH, CH_BED, GAP, OFF, DARK, box, cyl, rrect, feet)  # noqa: E402

PW, PD, R = 56.0, 32.0, 12.0      # post plan: perimeter 155, about a small wrist; R12 bends a bracelet gently
M_SIDE, M_FRONT = 12.0, 20.0      # side and back margin; front margin = side + 8 for the case to stand on
W, D = PW + 2 * M_SIDE, PD + M_SIDE + M_FRONT      # base 80 x 64 (5 : 4)
HB = 12.0                         # base height
PL, INSET = 2.4, 1.2              # floating plinth
SOCK = 6.0                        # pocket depth = half the base: the post tilts 5 deg at most when pushed
HP = 40.0                         # post above the base = a 40 case standing on the base: their tops line up
PY = (M_FRONT - M_SIDE) / 2       # post centre: 4 behind the base centre


def post_outline(z0, h, grow=0.0):
    return rrect(PW + 2 * grow, PD + 2 * grow, R + grow, z0, h, cy=PY)


def watch():
    """A buckled watch as an envelope: a 40 x 12 case standing on the base in front of the post (3 strap), and
    the strap as a 2.4 band round the post. Not a part: checked against the parts in the review."""
    case = (cyl(20, 0, 12).rotate((0, 0, 0), (1, 0, 0), 90)
            .translate((0, PY - PD / 2 - 3.25 - GAP, HB + 20 + 0.1)))
    band = post_outline(HB + 10, 20, 0.5 + 2.4).cut(post_outline(HB + 9, 22, 0.5))
    return case.union(band)


def watch_stand():
    base = rrect(W - 2 * INSET, D - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    base = base.union(rrect(W, D, R, PL, HB - PL).faces("<Z").chamfer(INSET))
    base = base.faces(">Z").chamfer(CH)
    pocket = post_outline(HB - SOCK, SOCK + 1, GAP)
    base = base.cut(pocket)
    base = base.edges(BoxSelector((-PW / 2 - 1, PY - PD / 2 - 1, HB - 0.1),       # the pocket's rim
                                  (PW / 2 + 1, PY + PD / 2 + 1, HB + 0.1))).chamfer(CH)
    base = feet(base, [(sx * 28, sy * 20) for sx in (-1, 1) for sy in (-1, 1)])

    post = post_outline(HB - SOCK, SOCK + HP).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    return {
        "base": Part(base, base, OFF),
        "post": Part(post, post.translate((0, -PY, -(HB - SOCK))), DARK),
    }


SAMPLES["061_watch_stand"] = watch_stand
