"""038 Magnetic clip bowl: a Ø72 x 36 bowl for paper clips with a Ø20 x 3 magnet sealed in its floor.

The magnet sits in a pocket in the middle of the floor, under a dark cover disc glued flush over it, so
clips gather on the disc and stay in when the bowl is knocked over, and the magnet is never exposed. Both
the pocket and the cover's recess open upward, so the bowl prints bottom down with no bridge. The bottom
edge is cut back 45 deg by 6: the bowl stands on a smaller circle and its wall seems to float.
"""
import os
import sys

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, CH, CH_BED, GAP, OFF, DARK, cyl, feet, chamfer_rim  # noqa: E402

R_OUT, H = 36.0, 36.0               # Ø72 x 36: 2 : 1
BEVEL = 6.0                         # 45-deg cut on the bottom edge: stands on Ø60
BASE = 1.2                          # solid under the magnet
MAG_R, MAG_T = 10.0, 3.0            # Ø20 x 3 disc magnet
POCKET_R, POCKET_T = 10.1, 3.2
COVER_T = 1.2
COVER_R = 16.0                      # Ø32 (8 modules): reads as a disc, not as a lid over the magnet
FLOOR = BASE + POCKET_T + COVER_T   # 5.6
COVE = 16.0                         # floor to wall: the flat of the floor is Ø34.96, the cover fits inside it


def clip_bowl_magnetic():
    body = cyl(R_OUT, 0, H).faces("<Z").chamfer(BEVEL)
    body = body.faces("<Z").chamfer(CH_BED)
    body = body.cut(cyl(R_OUT - T, FLOOR, H).faces("<Z").edges().fillet(COVE))
    body = body.faces(">Z").chamfer(CH)                              # rim: inner and outer edge
    body = body.cut(cyl(COVER_R + GAP, FLOOR - COVER_T, COVER_T + 1))
    body = chamfer_rim(body, COVER_R + GAP, FLOOR)
    body = body.cut(cyl(POCKET_R, BASE, POCKET_T + 0.01))
    body = feet(body, [(sx * 17, sy * 17) for sx in (-1, 1) for sy in (-1, 1)])

    cover = cyl(COVER_R, FLOOR - COVER_T, COVER_T).faces(">Z").chamfer(CH)
    magnet = cyl(MAG_R, BASE, MAG_T)                                 # glued to the pocket floor
    return {
        "bowl": Part(body, body, OFF),
        "cover": Part(cover, cover, DARK),          # bottom down: the C0.5 edge is the top, not the bed side
        "magnet_ref": Part(magnet, None, (0.6, 0.6, 0.62), ref=True),
    }


SAMPLES["038_clip_bowl_magnetic"] = clip_bowl_magnetic
