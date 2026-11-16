"""097 Pendant lamp shade: a Ø160 x 160 translucent shade with a 45-deg shoulder, hung from a lamp socket by a cap that
locates in its top opening.

The shade is one turned profile with a 1.68 wall (the diffuser rule of 10_lantern): a cylinder 116 high, a 45-deg shoulder
narrowing to Ø80, and a collar 4 high round the opening; it prints upright without supports. The cap is a disc that the lamp
socket clamps with its shade ring. The shade rests on the cap's 45-deg rim, which bears on the inside of the shoulder; a lip on
the cap rises to the top of the collar, 0.25 inside it, so the cap is centred and shows as one ring round the socket.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, DIV, CH, CH_BED, GAP, OFF  # noqa: E402

TRANSLUCENT = (0.93, 0.92, 0.88)          # white translucent PETG
RO, H = 80.0, 160.0                       # Ø160 x 160: height = diameter
RT = RO / 2                               # opening: half the diameter
COLLAR = 4.0
ZC = H - COLLAR - (RO - RT)               # top of the cylinder: 116
K = 1.41421356
TOP = 152.0                               # cap's top face, 8 under the shade's top
PLATE = 2.4                               # cap plate
SOCKET = 40.5                             # hole for the socket's threaded shell (check yours)
BULB = (60.0, 100.0)                      # LED bulb Ø and length below the socket (check yours)
SOCKET_LEN = 45.0                         # socket body above the cap (check yours)
RING = 15.0                               # shade ring and threaded shell below the cap (check yours)


def revolve(pts):
    return cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0))


def lamp_shade_pendant():
    ri = RO - DIV                                     # the bed chamfer is outside only: both would leave 0.48 on the bed
    k_out = RO + ZC                                   # outer cone: r + z = k_out
    k_in = k_out - DIV * K                            # inner cone, 1.68 inside it
    rti = RT - DIV
    shade = revolve([(ri, 0), (RO - CH_BED, 0), (RO, CH_BED), (RO, ZC), (RT, H - COLLAR), (RT, H - CH),
                     (RT - CH, H), (rti + CH, H), (rti, H - CH), (rti, k_in - rti), (ri, k_in - ri)])

    r2 = k_in - TOP                                   # cap's rim on the inner cone, 0.6 vertical below it
    rc = r2 + PLATE - 0.6
    zb = TOP - PLATE
    lo, li = rti - GAP, rti - GAP - DIV               # lip, 0.25 inside the collar
    cap = revolve([(SOCKET / 2 + CH_BED, zb), (rc, zb), (rc, zb + 0.6), (r2, TOP), (lo, TOP), (lo, H - CH),
                   (lo - CH, H), (li + CH, H), (li, H - CH), (li, TOP), (SOCKET / 2, TOP), (SOCKET / 2, zb + CH_BED)])
    cap_print = cap.translate((0, 0, -zb))
    return {
        "shade": Part(shade, shade, TRANSLUCENT),
        "cap": Part(cap, cap_print, OFF),
    }


def bulb():
    """Socket and LED bulb as an envelope under the cap; checked against the shade in the review."""
    zb = TOP - PLATE
    s = cq.Workplane("XY").workplane(offset=zb - RING).circle(SOCKET / 2 - 0.25).extrude(RING + SOCKET_LEN)
    b = cq.Workplane("XY").workplane(offset=zb - RING - BULB[1]).circle(BULB[0] / 2).extrude(BULB[1])
    return s.union(b)


SAMPLES["097_lamp_shade_pendant"] = lamp_shade_pendant
