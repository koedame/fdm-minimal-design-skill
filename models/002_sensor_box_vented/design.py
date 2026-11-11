"""002 Vented sensor box: a 48 x 48 x 72 sleeve printed top face down, closed by a bottom plate on two snaps.

Air comes in through slots in the bottom plate and leaves through slot fields on both sides, so a
temperature sensor inside sees room air rather than the warmth of its own board.
"""
import os
import sys

sys.path.insert(0, os.environ.get("FDM_SCRIPTS", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "fdm-minimal-design", "scripts")))
from fdm_samples import (Part, SAMPLES, T, DIV, CH, CH_BED, GAP, OFF,  # noqa: E402
                         box, rrect, rx, plane_yz, plane_xz)

S, H, R = 48.0, 72.0, 6.0          # 3:2 tall, R = 12.5 % of the plan
INSET = 1.2                         # the plate sits 1.2 up inside the rim: only the rim stands
PL = T                              # plate = wall thickness
SLOT_W, PITCH, N = 1.6, 4.0, 7
BAND = (12.0, 60.0)                 # side slots: 12 margin top and bottom
RIB_W, RIB_D = 8.0, T
TAB_W, TAB_L, BUMP = 6.0, 14.0, 0.8


def vslots(x_wall, inward):
    """Vertical round-ended slots through the wall normal to X at x_wall."""
    out = None
    z0, z1 = BAND
    for i in range(N):
        y = (i - (N - 1) / 2) * PITCH
        s = plane_yz(x_wall - inward * 1.0).center(y, (z0 + z1) / 2) \
            .slot2D(z1 - z0, SLOT_W, 90).extrude(inward * (T + 2.0))
        out = s if out is None else out.union(s)
    return out


def sensor_box_vented():
    zp0, zp1 = INSET, INSET + PL                       # plate bottom / top
    body = rrect(S, S, R, 0, H).faces(">Z").chamfer(CH_BED).faces("<Z").chamfer(CH)
    body = body.cut(rrect(S - 2 * T, S - 2 * T, R - T, -1, H - T + 1))

    # ribs on the front and back walls: stops for the plate and seats of the snap grooves.
    # They run full height to the top, so printed upside down they start on the top wall.
    yi = S / 2 - T
    zg = zp1 + TAB_L - 2.0                             # groove / bump centre
    for s in (-1, 1):
        rib = box(-RIB_W / 2, RIB_W / 2, min(s * yi, s * (yi - RIB_D)), max(s * yi, s * (yi - RIB_D)),
                  zp1, H - T + 0.01)
        body = body.union(rib)
        yf = s * (yi - RIB_D)                          # rib face
        g = BUMP + GAP
        groove = plane_yz(-RIB_W / 2 - 1).polyline(
            [(yf, zg - g - 0.2), (yf + s * g, zg), (yf, zg + g + 0.2)]).close().extrude(RIB_W + 2)
        body = body.cut(groove.intersect(box(-TAB_W / 2 - GAP, TAB_W / 2 + GAP, -S, S, 0, H)))
        lead = plane_yz(-RIB_W / 2 - 1).polyline(                 # 45-deg lead-in for the bump
            [(yf - s * 0.01, zp1 - 0.01), (yf + s * 1.0, zp1 - 0.01), (yf - s * 0.01, zp1 + 1.01)]).close()
        body = body.cut(lead.extrude(RIB_W + 2))

    for s in (-1, 1):                                  # side slot fields
        body = body.cut(vslots(s * S / 2, -s))
    led = plane_xz(-S / 2 - 1).center(0, BAND[1]).circle(0.8).extrude(-(T + 2))   # status LED, on the slot tops
    usb = plane_xz(S / 2 + 1).center(12.0, zp1 + 4.0 + 3.2).slot2D(12.0, 6.4, 0).extrude(T + 2)
    body = body.cut(led).cut(usb)

    # bottom plate: inside the rim with 0.25 all round, two cantilever tabs with 45-deg bumps
    plate = rrect(S - 2 * (T + GAP), S - 2 * (T + GAP), R - T - GAP, zp0, PL)
    plate = plate.faces("<Z").chamfer(CH)
    for i in range(N):                                 # intake slots, the same field as the sides
        x = (i - (N - 1) / 2) * PITCH
        plate = plate.cut(cq_slot_z(x, 0, 24.0, SLOT_W, zp0 - 1, PL + 2))
    plate = plate.cut(box(10.0, 16.0, S / 2 - T - GAP - 1.2, S, zp0 - 1, zp0 + PL + 1))   # pry notch, back right
    for s in (-1, 1):
        yt = s * (yi - RIB_D - GAP)                    # outer face of the tab
        tab = box(-TAB_W / 2, TAB_W / 2, min(yt, yt - s * DIV), max(yt, yt - s * DIV), zp1 - 0.01, zp1 + TAB_L)
        bump = plane_yz(-TAB_W / 2).polyline(
            [(yt, zg - BUMP), (yt + s * BUMP, zg), (yt, zg + BUMP)]).close().extrude(TAB_W)
        plate = plate.union(tab).union(bump)

    return {
        "body": Part(body, rx(body, 180), OFF),
        "bottom_plate": Part(plate, plate, OFF),
    }


def cq_slot_z(x, y, length, width, z0, h):
    """Round-ended slot along Y, through a plate normal to Z."""
    return rrect(width, length, width / 2 - 0.001, z0, h, x, y)


SAMPLES["002_sensor_box_vented"] = sensor_box_vented
