"""100 Bookend pair: two identical L-shaped bookends (120 wide, 144 high, 96 deep).

The books stand on the base, and their weight keeps the upright from tipping and the base from sliding. The upright is 5.04 thick;
the base tapers from 5.04 at the corner to 1.68 at its front edge, so a book standing across that edge steps down only 1.68, and the
books on the base lean 2 deg towards the upright. The corner is rounded R12 outside and R6.96 inside, concentric. Each bookend prints
on its side, so the lines run round the corner without a layer seam where the upright bends against the base.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, DIV, CH, CH_BED, OFF, box, copies, plane_yz  # noqa: E402

W, H, D = 120.0, 144.0, 96.0    # 30 x 36 x 24 modules
TK = 2 * T                      # 5.04: two outer walls
RO = 12.0                       # outer corner; 8.3 % of the height
RI = RO - TK                    # 6.96, concentric
SPAN = 240.0                    # between the two uprights in the preview: the bases leave 48 between them


def bookend():
    base = plane_yz(-W / 2).polyline([(0, 0), (D, 0), (D, DIV), (TK, TK), (0, TK)]).close().extrude(W)
    e = box(-W / 2, W / 2, 0, TK, 0, H).union(base)
    e = e.edges(cq.selectors.BoxSelector((-W, -0.1, -0.1), (W, 0.1, 0.1))).fillet(RO)
    e = e.edges(cq.selectors.BoxSelector((-W, TK - 0.1, TK - 0.1), (W, TK + 0.1, TK + 0.1))).fillet(RI)
    ends = cq.selectors.BoxSelector((-W, -0.1, H - 0.1), (W, TK + 0.1, H + 0.1))
    front = cq.selectors.BoxSelector((-W, D - 0.1, -0.1), (W, D + 0.1, DIV + 0.1))
    e = e.edges(ends).edges("|X").chamfer(CH)
    e = e.edges(front).edges("|X").chamfer(CH)
    return e.faces("<X").chamfer(CH_BED).faces(">X").chamfer(CH)


def bookend_pair():
    e = bookend()
    pair = copies([e.translate((0, -SPAN / 2 - TK, 0)), e.rotate((0, 0, 0), (0, 0, 1), 180).translate((0, SPAN / 2 + TK, 0))])
    prn = e.rotate((0, 0, 0), (0, 1, 0), 90)       # on its side, the <X face on the bed
    return {"bookend": Part(pair, prn, OFF, qty=2)}


SAMPLES["100_bookend_pair"] = bookend_pair
