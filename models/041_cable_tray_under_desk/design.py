"""041 Under-desk cable tray: a 200 long hopper that hangs from two C rails screwed under the desk top.

The tray's section is the design: a 64 high back, a 48 floor and a front leaning out at 45 deg, so a
cable dropped from above or pushed in from the front stays in. It prints lying on its back, so every
wall stands up or leans at 45 deg. Each end wall carries a hook arm along its top. The arm slides into
a C rail screwed to the desk and sits on the rail's ledge; a V rib under the arm drops into a V notch in
the ledge, so the tray has to be lifted 1.5 before it can slide out. The rail screws sit above the arm,
hidden from below, and are driven before the tray goes on, where the ledge is cut away.
"""
import os
import sys

import cadquery as cq

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import Part, SAMPLES, T, CH, CH_BED, GAP, OFF, box, rx, plane_yz, plane_xz  # noqa: E402

L = 200.0                     # tray length (X)
H, FL, RISE = 64.0, 48.0, 32.0  # back height, floor depth, front rise at 45 deg -> 80 deep
R = 12.0                      # section corners (15 % of the 80 depth); inside R - T
AW, AT = 8.0, 4.0             # hook arm: reach out from the end wall, thickness
AL = FL                       # arm length along Y: the flat top of the end wall
PT = 4.0                      # rail flange, web and ledge thickness (= the arm)
LIFT = 2.0                    # headroom over the arm in the rail: the rib lifts out, the tray cannot tip far
SIDE = 0.5                    # side play between the arm and the rail
RIB = 1.5                     # V rib under the arm; V notch in the ledge 1.75 deep
RL, RY0 = 48.0, 0.0           # rail length and back end: as long as the arm, so the arm hides it from below
LEDGE = (-10.0, -40.0)        # ledge only under the middle 30: the screws beyond its ends stay drivable
SCREW_Y = (-5.0, -43.0)       # 4 mm countersunk wood screws, heads flush with the flange's underside
NOTCH_Y = -24.0
K2 = 2 ** 0.5


def cut_corners(pts):
    """Closed polygon of (x, y, c): a 45-deg cut of c along both edges at each corner (c = 0: left sharp)."""
    out = []
    n = len(pts)
    for i, (x, y, c) in enumerate(pts):
        if not c:
            out.append((x, y))
            continue
        for (px, py, _) in (pts[i - 1], pts[(i + 1) % n]):
            d = ((px - x) ** 2 + (py - y) ** 2) ** 0.5
            out.append((x + (px - x) * c / d, y + (py - y) * c / d))
    return out


def section(pts, length, x0):
    return plane_yz(x0).polyline(pts).close().extrude(length)


def cable_tray_under_desk():
    t = T / K2                                               # the front wall ends square to itself, in the front plane
    yi = -FL + T * (K2 - 1)                                  # inner floor-front corner: z = T on the inner front face
    sec = [(0, H, CH_BED), (0, 0, 0), (-FL, 0, 0), (-FL - RISE, RISE, CH), (-FL - RISE + t, RISE + t, CH),
           (yi, T, 0), (-T, T, 0), (-T, H, CH)]
    shell = plane_yz(-L / 2 + CH).polyline(cut_corners(sec)).close().extrude(L - 2 * CH)
    for (y, z, r) in ((0, 0, R), (-FL, 0, R), (-T, T, R - T), (yi, T, R - T)):
        shell = shell.edges("|X").edges(cq.selectors.BoxSelector((-L, y - 0.1, z - 0.1), (L, y + 0.1, z + 0.1))).fillet(r)
    hull = [(0, H), (0, 0), (-FL, 0), (-FL - RISE, RISE), (-FL - RISE + (H - RISE), H)]   # the end walls: front edge in the front plane
    body = shell
    for s in (-1, 1):
        end = section(hull, T, L / 2 - T if s > 0 else -L / 2)
        for (y, z) in ((0, 0), (-FL, 0)):
            end = end.edges("|X").edges(cq.selectors.BoxSelector((-L, y - 0.1, z - 0.1), (L, y + 0.1, z + 0.1))).fillet(R)
        body = body.union(end.edges().chamfer(CH))

    rail_l = rail_r = None
    for s in (-1, 1):
        xe = s * L / 2                                       # outer face of the end wall
        span = lambda a, b: (min(xe + s * a, xe + s * b), max(xe + s * a, xe + s * b))   # noqa: E731
        ax = span(0, AW)
        arm = box(*ax, -AL, 0, H - AT, H)
        rib = plane_yz(ax[0]).polyline([(NOTCH_Y - RIB, H - AT), (NOTCH_Y, H - AT - RIB),
                                         (NOTCH_Y + RIB, H - AT)]).close().extrude(AW)
        arm = arm.edges("|Y").chamfer(CH).union(rib)
        body = body.union(arm.translate((-s * 0.01, 0, 0)))

        z_led = H - AT                                       # ledge top: the arm rests on it
        z_fl = H + LIFT                                      # flange bottom
        xo, xw, xt = xe + s * (AW + SIDE + PT), xe + s * (AW + SIDE), xe + s * SIDE   # outer face, web inside, flange tip
        prof = [(xo, z_led - PT, CH_BED), (xw, z_led - PT, CH), (xw, z_fl, 0), (xt, z_fl, CH),
                (xt, z_fl + PT, CH), (xo, z_fl + PT, CH_BED)]
        rail = plane_xz(RY0).polyline(cut_corners(prof)).close().extrude(RL)
        rail = rail.faces("<Y or >Y").edges().chamfer(CH)
        ledge = box(*sorted((xw + s * 0.6, xt)), LEDGE[1], LEDGE[0], z_led - PT, z_led).edges().chamfer(CH)
        notch = plane_yz(-L).polyline([(NOTCH_Y - RIB - GAP * K2, z_led + 0.01), (NOTCH_Y, z_led - RIB - GAP * K2),
                                       (NOTCH_Y + RIB + GAP * K2, z_led + 0.01)]).close().extrude(2 * L)
        rail = rail.union(ledge.cut(notch))
        for y in SCREW_Y:
            x = xe + s * (AW / 2 + SIDE)
            tri = [(x - s * 2.25 * K2 / 2, y - 2.25 * K2 / 2), (x - s * 2.25 * K2, y), (x - s * 2.25 * K2 / 2, y + 2.25 * K2 / 2), (x, y)]
            hole = cq.Workplane("XY").workplane(offset=z_fl - 1)       # teardrop: its roof points up in the print
            hole = hole.center(x, y).circle(2.25).extrude(PT + 2).union(
                cq.Workplane("XY").workplane(offset=z_fl - 1).polyline(tri).close().extrude(PT + 2))
            sink = cq.Solid.makeCone(4.5 + 0.01, 2.25, 2.26, cq.Vector(x, y, z_fl - 0.01), cq.Vector(0, 0, 1))
            rail = rail.cut(hole).cut(cq.Workplane("XY").add(sink))
        if s < 0:
            rail_l = rail
        else:
            rail_r = rail

    # print: the tray on its back (y = 0 on the bed), the rails on their webs
    tray_prn = rx(body, -90)
    prn_l = rail_l.rotate((0, 0, 0), (0, 1, 0), -90)
    prn_r = rail_r.rotate((0, 0, 0), (0, 1, 0), 90)
    return {
        "tray": Part(body, tray_prn, OFF),
        "rail_left": Part(rail_l, prn_l, OFF),
        "rail_right": Part(rail_r, prn_r, OFF),
    }


SAMPLES["041_cable_tray_under_desk"] = cable_tray_under_desk
