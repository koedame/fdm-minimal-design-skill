"""
Sample objects in a minimal product design language for FDM 3D printing, plus the helper library
they are built from.
Original designs (not reproductions of specific products). Units: mm. Requires CadQuery.

Usage
  python fdm_samples.py --list
  python fdm_samples.py                     # all samples -> ./fdm_samples_out
  python fdm_samples.py 06_radio --out out  # one sample

Design rules applied everywhere (see references/02_rules.md):
  * one visible chamfer value (CH 0.5); bed-side edges 0.6 only for elephant foot
  * every dimension derived from a stated rule (grid 4 mm, ratios, line width 0.42)
  * at most 2-3 radii per object, chosen by role; ground-contact ends stay flat
  * seams of parts are designed lines, not leftovers

To start a new object, copy template_new_object.py rather than editing this file.

  01_clock          round dial in an arched body        | through-bore, step instead of a ceiling
  02_remote         handheld slab, body + face plate    | face plate printed face-down, inset with reveal
  03_tray           open container                      | single part, 2:1 cells, wall hierarchy
  04_cylinder       vertical tube speaker               | 2:1 tube, round-ended vertical slots
  05_stand          angled device stand                 | printed on its side so the profile is crisp
  06_radio          box device, grille over controls    | sleeve body, slide-in plate, cover on magnets
  07_hinged_case    box with hinged lid                 | pin hinge, 45-deg knuckle webs, magnets
  08_power_bank     slab with battery door and port     | dovetail slide door, printed snap tab, USB-C window
  09_wall_unit      wall-mounted unit                   | keyhole bracket, removable snap hooks, clear window
  10_lantern        stacked light                       | translucent section, slide switch
  11_split_riser    object larger than the bed          | halves printed on side, dowels, joint as V line
  12_threaded_jar   screw-top container                 | 45-deg threads, flush lid
"""
import math
import os
from dataclasses import dataclass
import cadquery as cq
from cadquery.selectors import BoxSelector

T = 2.52        # wall: 6 lines @ 0.42
DIV = 1.68      # divider / lip: 4 lines @ 0.42
CH_BED = 0.6    # bed-side chamfer (elephant foot)
CH = 0.5        # the ONLY visible chamfer value
GAP = 0.25      # reveal / clearance per side
OFF = (0.925, 0.918, 0.894)
PLATE = (0.78, 0.78, 0.77)
DARK = (0.23, 0.23, 0.22)
ACC = (0.94, 0.62, 0.15)
LABEL_GRAY = (0.55, 0.55, 0.53)   # labels: close to the plate, not black


@dataclass
class Part:
    """One part: the assembled shape (in use, Z up), the print-oriented shape and the colour.

    qty > 1: asm holds every copy in place and prn one copy; build asm with copies() so that
    copies that touch stay separate solids. ref=True marks a bought part (a clock movement, a
    driver, steel dowels) that is shown in the assembly and checked for fit but not printed:
    prn may be None and no print STL is written for it.
    """
    asm: cq.Workplane
    prn: cq.Workplane
    color: tuple
    anchor: str = None
    qty: int = 1
    ref: bool = False


# ---------------- helpers ----------------
def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def rrect(w, h, r, z0, t, cx=0, cy=0):
    return (cq.Workplane("XY").workplane(offset=z0).center(cx, cy)
            .rect(w, h).extrude(t).edges("|Z").fillet(r))


def cyl(r, z0, h, x=0, y=0):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(r).extrude(h)


def copies(shapes):
    """Several copies of a part (qty > 1) as one shape that keeps every copy a separate solid.

    A union fuses copies that touch (stacked trays, a pin in a row of pins) into one solid, and
    then the tools cannot tell the copies apart (verify.py reports it)."""
    return cq.Workplane("XY").add(cq.Compound.makeCompound([s.val() for s in shapes]))


def on_slope(wp, tilt, origin=(0, 0, 0)):
    """Move a shape built in the XY frame onto a face that leans back `tilt` degrees from the desk.

    Local x stays +X, local y runs up the slope (and back), local +Z is the outward normal of the face
    (forward and up); the local origin goes to `origin`. tilt 90 is a vertical front face, 0 a top face.
    Build features with the usual helpers (rrect, cyl, box, slot2D on an XY workplane) and move them;
    on_slope(wp, -tilt) brings a shape back into the face frame when the origin is (0, 0, 0)."""
    return wp.rotate((0, 0, 0), (1, 0, 0), tilt).translate(origin)


def rx(wp, deg):
    return wp.rotate((0, 0, 0), (1, 0, 0), deg)


def rz(wp, deg):
    return wp.rotate((0, 0, 0), (0, 0, 1), deg)


def fillet_at(wp, xy, r, zmax=1000):
    """Fillet the vertical edge passing through (x, y)."""
    x, y = xy
    return wp.edges("|Z").edges(BoxSelector((x - .05, y - .05, -1), (x + .05, y + .05, zmax))).fillet(r)


def knob_local(R, H, inner_r, groove, rib_n, rib_z0, dshaft=True):
    """Axis +Z, front face at z=0. Concentric step + one indicator toward -Y:
    groove=(r0, r1) cuts a line from r0 to r1, groove=r cuts a dot (diameter 2.4) at radius r."""
    k = cyl(R, 0, H).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH)
    k = k.cut(cyl(inner_r, -0.01, 0.81))
    if isinstance(groove, tuple):
        k = k.cut(box(-0.6, 0.6, -groove[1], -groove[0], -0.01, 1.4))
    else:
        k = k.cut(cyl(1.2, -0.01, 1.41, 0, -groove))
    ribs = (cq.Workplane("XY").workplane(offset=rib_z0)
            .polarArray(R, 0, 360, rib_n).rect(1.0, 0.8).extrude(H))
    k = k.cut(ribs)
    if dshaft:
        k = k.cut(cyl(3.05, 2.5, H).intersect(box(-4, 1.55, -4, 4, 2.5, H + 1)))
    return k


def button_local(d, protrude, panel_t, flange_r, stem_r=1.5, stem_len=2.0):
    """Axis +Z, front face at z=0. 45 deg cone under the flange -> no overhang printed face down."""
    cap = protrude + panel_t
    b = cyl(d / 2, 0, cap).faces("<Z").chamfer(CH)
    cone_h = flange_r - d / 2
    b = b.union(cq.Workplane("XY").add(
        cq.Solid.makeCone(d / 2, flange_r, cone_h, pnt=cq.Vector(0, 0, cap))))
    b = b.union(cyl(flange_r, cap + cone_h, 1.0))
    return b.union(cyl(stem_r, cap + cone_h + 1.0, stem_len))


def chamfer_rim(wp, r, z_top):
    """45-deg chamfer CH on the rim of a circular pocket opening at z_top."""
    cone = cq.Solid.makeCone(r, r + CH + 0.01, CH + 0.01, pnt=cq.Vector(0, 0, z_top - CH))
    return wp.cut(cq.Workplane("XY").add(cone))


def feet(wp, pts, z_bottom=0.0):
    for (x, y) in pts:
        wp = wp.cut(cyl(5.1, z_bottom - 0.01, 1.01, x, y))
    return wp


# ---------------- 01 clock ----------------
CLOCK_SHAFT_HOLE = 7.6      # movement thread; check your movement
HAND_HOLES = {"hour": 5.2, "minute": 3.1}  # vary by movement; the sample has no second hand


def clock():
    # grid 4: W=104 (26), arch R=52 (13), DEP=36 (9), dial 88 (22), dot ring 72 (18)
    # The top of the body is a half circle concentric with the dial, so the frame around the
    # dial is one even band (52 - 44 = 8). Below the dial the frame doubles (16), which puts
    # the dial above the middle of the body. The bottom stands flat; its corners take R8,
    # the same width as the frame.
    W, DEP = 104.0, 36.0
    R_TOP = W / 2
    DIAL_R = 44.0
    FRAME = R_TOP - DIAL_R                    # 8
    LOW = -(DIAL_R + 2 * FRAME)               # bottom face, 60 below the dial centre
    RING, MAJ_D, MIN_D = 36.0, 4.8, 2.4       # dot diameters 2:1
    outline = (cq.Workplane("XY").moveTo(-R_TOP, LOW).lineTo(R_TOP, LOW).lineTo(R_TOP, 0)
               .threePointArc((0, R_TOP), (-R_TOP, 0)).close().extrude(DEP))
    for x in (-R_TOP, R_TOP):
        outline = fillet_at(outline, (x, LOW), FRAME)
    outer = outline.faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    housing = outer.cut(cyl(41.0, -1, DEP + 2)).cut(cyl(DIAL_R + GAP, DEP - 2.4, 3))
    housing = chamfer_rim(housing, DIAL_R + GAP, DEP)          # same edge as the outer rim

    dial = cyl(DIAL_R, DEP - 2.4, 2.4).faces(">Z").chamfer(CH)
    marks = top_mark = None
    for i in range(12):
        major = i % 3 == 0
        d = MAJ_D if major else MIN_D
        a = math.radians(30 * i)
        m = cyl(d / 2, DEP - 0.4, 0.4, RING * math.sin(a), RING * math.cos(a))
        if i == 0:
            top_mark = m                       # 12 o'clock: the one accent, marks which way is up
        else:
            marks = m if marks is None else marks.union(m)
    dial = dial.cut(marks).cut(top_mark).cut(cyl(CLOCK_SHAFT_HOLE / 2, DEP - 3, 4))

    def hand(w, tip, hub, hole, t):
        # round-ended bar: the same circle as the dots, drawn out
        h = box(-w / 2, w / 2, 0, tip - w / 2, 0, t).union(cyl(w / 2, 0, t, 0, tip - w / 2))
        return h.union(cyl(hub, 0, t)).cut(cyl(hole / 2, -1, t + 2))

    # hand widths are the two dot diameters. The minute hand stops 1.6 mm (4 lines) short
    # of the major dots; the hour hand is 3/4 of the minute hand. Hubs step down 1 mm.
    MIN_TIP = RING - MAJ_D / 2 - 1.6           # 32
    hands = {
        "hand_hour": (hand(MAJ_D, 0.75 * MIN_TIP, 5.0, HAND_HOLES["hour"], 1.0), DEP + 0.6, 60),
        "hand_minute": (hand(MIN_D, MIN_TIP, 4.0, HAND_HOLES["minute"], 1.0), DEP + 1.8, -48),
    }
    disp = lambda wp: rx(wp, 90)
    parts = {
        "housing": Part(disp(housing), housing, OFF),
        "dial": Part(disp(dial), rx(dial, 180), PLATE),
        "dial_marks_inlay": Part(disp(marks), rx(marks, 180), DARK, anchor="dial"),
        "dial_top_mark_inlay": Part(disp(top_mark), rx(top_mark, 180), ACC, anchor="dial"),
    }
    for n, (h, z0, ang) in hands.items():
        parts[n] = Part(disp(rz(h, ang).translate((0, 0, z0))), h, DARK)
    return parts


# ---------------- 02 remote ----------------
def remote():
    # grid 4: W=52 (13), L=152 (38), H=14; key pitch 12 (3 x grid)
    W, L, R, H = 52.0, 152.0, 14.0, 14.0
    PT, FLOOR, LEDGE = 2.4, 2.0, DIV
    PITCH = 12.0
    boss_xy = [(sx * 14, sy * 58) for sx in (-1, 1) for sy in (-1, 1)]
    BOSS_SPLIT = 7.0

    # one-piece body: the only line on the object is the reveal around the face plate
    body = rrect(W, L, R, 0, H).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    body = body.cut(rrect(W - 2 * T, L - 2 * T, R - T, H - PT, PT + 1))
    body = body.cut(rrect(W - 2 * (T + LEDGE), L - 2 * (T + LEDGE), R - T - LEDGE, FLOOR, H))
    for (x, y) in boss_xy:
        body = body.union(cyl(3.0, FLOOR - 0.1, BOSS_SPLIT - FLOOR + 0.1, x, y))
        body = body.cut(cyl(1.2, -1, H, x, y)).cut(cyl(2.2, -1, 2.6, x, y))

    plate = rrect(W - 2 * (T + GAP), L - 2 * (T + GAP), R - T - GAP, H - PT, PT).faces(">Z").chamfer(CH)
    for (x, y) in boss_xy:
        plate = plate.union(cyl(3.0, BOSS_SPLIT, H - PT - BOSS_SPLIT + 0.01, x, y))
        plate = plate.cut(cyl(0.9, BOSS_SPLIT - 1, H - PT - BOSS_SPLIT, x, y))

    KEY_D = 9.0
    pw, pl = W / 2 - T - GAP, L / 2 - T - GAP            # plate half sizes
    blk = PITCH + KEY_D / 2                              # key block half width
    m = pw - blk                                         # side margin, reused above the IR window
    IR_H = 3.0
    ir_y = pl - m - IR_H / 2
    power = (0.0, ir_y - 1.5 * PITCH)                    # IR window 1.5 pitches above power
    top_row = power[1] - 2 * PITCH                       # key block 2 pitches below power
    rows = [top_row - PITCH * i for i in range(4)]
    keys = [(x, y) for y in rows for x in (-PITCH, 0, PITCH)]
    for (x, y) in keys + [power]:
        plate = plate.cut(cyl(4.8, H - PT - 1, PT + 2, x, y))
    ir = box(-blk, blk, ir_y - IR_H / 2, ir_y + IR_H / 2, H - 0.4, H)   # same width as the key block
    plate = plate.cut(ir)

    key_l = button_local(9.0, 1.2, PT, 5.5, stem_r=1.5, stem_len=1.0)
    place = lambda x, y: rx(key_l, 180).translate((x, y, H + 1.2))
    key_asm = None
    for (x, y) in keys:
        key_asm = place(x, y) if key_asm is None else key_asm.union(place(x, y))

    return {
        "body": Part(body, body, OFF),
        "face_plate": Part(plate, rx(plate, 180), OFF),
        "ir_window_inlay": Part(ir, rx(ir, 180), DARK, anchor="face_plate"),
        "key": Part(key_asm, key_l, DARK, qty=12),
        "key_power": Part(place(*power), key_l, ACC),
    }


# ---------------- 03 tray ----------------
def tray():
    # outer 2:1 (200 x 100). Inner: trough : column = 2 : 1, column split into two equal cells.
    W, Dp, H, R = 200.0, 100.0, 28.0, 14.0
    FLOOR, DIV_H = 2.4, H - 4.0
    ri, r_in = R - T, 3.0                    # two radii only: outer-derived and inner
    xi, yi = W / 2 - T, Dp / 2 - T
    col_w = (2 * xi - DIV) / 3
    xd = xi - col_w - DIV / 2                # divider centre

    # one precise detail: a 45-deg undercut plinth so the tray floats on a shadow line
    PL, INSET = 2.4, 1.2
    body = rrect(W - 2 * INSET, Dp - 2 * INSET, R - INSET, 0, PL).faces("<Z").chamfer(CH_BED)
    body = body.union(rrect(W, Dp, R, PL, H - PL).faces("<Z").chamfer(INSET))

    def cell(x0, x1, y0, y1, radii):
        c = box(x0, x1, y0, y1, FLOOR, H + 1)
        for xy, r in radii.items():
            c = fillet_at(c, xy, r, H + 2)
        return c.faces("<Z").edges().fillet(r_in - 0.05)

    a, b = xd - DIV / 2, xd + DIV / 2
    left = cell(-xi, a, -yi, yi, {(-xi, -yi): ri, (-xi, yi): ri, (a, -yi): r_in, (a, yi): r_in})
    rt = cell(b, xi, DIV / 2, yi, {(xi, yi): ri, (b, yi): r_in, (b, DIV / 2): r_in, (xi, DIV / 2): r_in})
    rb = cell(b, xi, -yi, -DIV / 2, {(xi, -yi): ri, (b, -yi): r_in, (b, -DIV / 2): r_in, (xi, -DIV / 2): r_in})
    body = body.cut(left).cut(rt).cut(rb)
    body = body.cut(rrect(W - 2 * T, Dp - 2 * T, ri, DIV_H, H))
    body = body.faces(">Z").chamfer(CH)      # both rim edges, inner and outer, same value
    # divider tops get the same 45-deg edge, cut as small prisms along each top edge
    c = 0.4
    def edge_prism(plane, pts, length):
        return cq.Workplane(plane).polyline(pts).close().extrude(length)
    pxz = cq.Plane(origin=(0, yi, 0), xDir=(1, 0, 0), normal=(0, -1, 0))  # local y = +Z
    for xe, s_ in ((a, 1), (b, -1)):
        body = body.cut(edge_prism(pxz, [(xe - s_ * .01, DIV_H + .01), (xe + s_ * c, DIV_H + .01),
                                          (xe - s_ * .01, DIV_H - c)], 2 * yi))
    pyz = cq.Plane(origin=(b, 0, 0), xDir=(0, 1, 0), normal=(1, 0, 0))
    for ye, s_ in ((DIV / 2, -1), (-DIV / 2, 1)):
        body = body.cut(edge_prism(pyz, [(ye - s_ * .01, DIV_H + .01), (ye + s_ * c, DIV_H + .01),
                                          (ye - s_ * .01, DIV_H - c)], xi - b))
    body = feet(body, [(sx * 84, sy * 36) for sx in (-1, 1) for sy in (-1, 1)])
    return {"tray": Part(body, body, OFF)}


# ---------------- 04 cylinder speaker ----------------
def cylinder():
    # height : diameter = 2 : 1 (144 : 72). Slot field leaves equal plain bands top and bottom.
    R, HB, HC = 36.0, 134.0, 10.0
    BAND = 24.0                                   # visible plain area, bottom and top
    SW = 1.6
    body = cyl(R, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    body = body.cut(cyl(R - T, 2.4, HB))
    z0, z1 = BAND, HB - (BAND - HC)              # top band + cap = BAND
    slot = box(R - 4, R + 1, -SW / 2, SW / 2, z0 + SW / 2, z1 - SW / 2)
    for zc in (z0 + SW / 2, z1 - SW / 2):        # full-round slot ends
        slot = slot.union(cq.Workplane("YZ").workplane(offset=R - 4).center(0, zc).circle(SW / 2).extrude(5))
    for i in range(40):
        body = body.cut(rz(slot, i * 9.0 + 4.5))
    r = 4.0
    pl = cq.Plane(origin=(0, R, 12), xDir=(1, 0, 0), normal=(0, -1, 0))
    body = body.cut(cq.Workplane(pl).circle(r).extrude(5, both=True))
    body = body.cut(cq.Workplane(pl).polyline([(-r * .7071, r * .7071), (0, r * 1.4142), (r * .7071, r * .7071), (0, 0)])
                    .close().extrude(5, both=True))
    body = feet(body, [(sx * 20, sy * 20) for sx in (-1, 1) for sy in (-1, 1)])

    cap = cyl(R, HB, HC).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    cap = cap.cut(cyl(31.2, HB - 1, HC - 3 + 1))   # clears the button flange
    cap = cap.union(cyl(R - T - GAP, HB - 3, 3.01).cut(cyl(R - T - GAP - DIV, HB - 4, 5)))
    top_z = HB + HC
    KNOB_R = 15.0
    btn_xy = (0.0, -(KNOB_R + R) / 2)            # button sits midway between knob and rim
    cap = cap.cut(cyl(7.2 / 2, top_z - 4, 5)).cut(cyl(4.3, top_z - 4, 5, *btn_xy))

    knob_l = knob_local(KNOB_R, 10.0, 11.5, (4.0, 9.5), 36, 2.5)
    btn_l = button_local(8.0, 1.5, 3.0, 5.0, stem_len=2.0)
    knob_asm = rx(knob_l, 180).translate((0, 0, top_z + 0.5 + 10.0))
    btn_asm = rx(btn_l, 180).translate((btn_xy[0], btn_xy[1], top_z + 1.5))
    return {
        "body": Part(body, body, OFF),
        "top_cap": Part(cap, rx(cap, 180), OFF),
        "knob": Part(knob_asm, rx(knob_l, 180), OFF),
        "button_on": Part(btn_asm, btn_l, ACC),
    }


# ---------------- 05 angled stand ----------------
def stand():
    # one plate thickness t=8 everywhere (foot, back, lip). Grid 4: foot 96, height 80, width 80,
    # channel 12. Radii by role: free ends ~t/2 (near full round), the load-bearing inside
    # corner R10, the channel R2 so its floor stays flat for the pad.
    WID, t = 80.0, 8.0
    import math
    ang = math.radians(70)
    ch0, ch1 = t, t + 12.0                    # channel between lip and back
    top = 80.0
    run = (top - t) / math.tan(ang)
    dx = t / math.sin(ang)
    P = {
        "fb": (0, 0), "bb": (96, 0), "bt": (96, t), "kb": (ch1 + dx, t),
        "kt": (ch1 + dx + run, top), "ft": (ch1 + run, top), "cf": (ch1, t),
        "lc": (ch0, t), "lt": (ch0, 3 * t), "lf": (0, 3 * t),
    }
    order = ["fb", "bb", "bt", "kb", "kt", "ft", "cf", "lc", "lt", "lf"]
    body = cq.Workplane("XY").polyline([P[k] for k in order]).close().extrude(WID)
    END = t / 2 - 0.2
    radii = {"fb": END, "bb": END, "bt": END, "lt": END, "lf": END,
             "kt": END, "ft": END, "kb": 10.0, "cf": 2.0, "lc": 2.0}
    for k, r in radii.items():
        body = fillet_at(body, P[k], r, WID + 1)
    body = body.faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)

    x0, x1 = ch0 + 2.5, ch1 - 2.5                # flat part of the channel floor
    body = body.cut(box(x0, x1, 3.5, t + 0.5, 37, 43))
    gpl = cq.Plane(origin=(x0, 0, 0), xDir=(0, 1, 0), normal=(1, 0, 0))
    body = body.cut(cq.Workplane(gpl).polyline([(-0.1, 33), (4, 37), (4, 43), (-0.1, 47)]).close().extrude(100))
    body = body.cut(box(x0, x1, t - 1.0, t + 0.5, 4, WID - 4))
    pad = box(x0 + 0.1, x1 - 0.1, t - 1.0, t + 0.6, 4.1, WID - 4.1).cut(box(0, 30, 0, 20, 36, 44))

    disp = lambda wp: rx(wp, 90)
    return {
        "stand": Part(disp(body), body, OFF),
        "grip_pad_tpu": Part(disp(pad), pad.rotate((0, 0, 0), (1, 0, 0), -90), ACC),
    }


# ---------------- 06 radio ----------------
def _find_font():
    """A grotesk-like font for labels. Falls back to CadQuery's default font."""
    for p in ("/usr/share/fonts/opentype/inter/Inter-Regular.otf",
              "/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Helvetica.ttc",
              "C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return p
    return None


FONT = _find_font()


def radio():
    """Box device. Sleeve body (open top), plate slides down into grooves, top cover on magnets.
    Front 144 x 96 = 3:2. Front-plate layout uses alignment lines instead of loose placement:
      * the grille is a band across the top of the plate; its margin m is the same on the
        left, top and right, and again below the dial
      * dial left edge = grille left edge, right button edge = grille right edge
      * the dial and the buttons share one centre line; the labels sit under the buttons
    """
    W, D, H_BODY, H_COVER, R = 144.0, 72.0, 88.0, 8.0, 12.0
    T_FRONT, FLOOR = 4.8, 2.4
    WIN_X = 58.0
    WIN_Z0 = W / 2 - WIN_X                     # bottom frame = side frame (14)
    GROOVE_X, GY0, GY1 = 62.0, 1.15, 2.65
    GZ0 = WIN_Z0 - 2.25
    PT_FACE, PT = 1.2, 2.4
    PLATE_TOP = H_BODY - 0.1
    POST, MAG_D, MAG_H = 8.0, 6.2, 3.2
    cy = D / 2

    # ---- body ----
    outer = rrect(W, D, R, 0, H_BODY, cy=cy).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    cav = rrect(W - 2 * T, D - 2 * T, R - T, FLOOR, H_BODY + 1, cy=cy) \
        .intersect(box(-W, W, T_FRONT, D, FLOOR, H_BODY + 2))
    body = outer.cut(cav)
    px = W / 2 - T - POST / 2
    posts = [(sx * px, py) for sx in (-1, 1) for py in (T_FRONT + POST / 2, D - T - POST / 2)]
    for (x, y) in posts:
        body = body.union(box(x - POST / 2, x + POST / 2, y - POST / 2, y + POST / 2, FLOOR - 0.1, H_BODY))
    body = body.intersect(outer)
    for (x, y) in posts:
        body = body.cut(cyl(MAG_D / 2, H_BODY - MAG_H, MAG_H + 1, x, y))
    body = body.cut(box(-WIN_X, WIN_X, -1, T_FRONT + 0.01, WIN_Z0, H_BODY + 5).edges("|Y").fillet(1.0))
    body = body.cut(box(-GROOVE_X, GROOVE_X, GY0, GY1, GZ0, H_BODY + 1))
    r = 4.0
    pl = cq.Plane(origin=(50, D, 14), xDir=(1, 0, 0), normal=(0, -1, 0))
    body = body.cut(cq.Workplane(pl).circle(r).extrude(6, both=True))
    body = body.cut(cq.Workplane(pl).polyline([(-r * .7071, r * .7071), (0, r * 1.4142), (r * .7071, r * .7071), (0, 0)])
                    .close().extrude(6, both=True))
    body = feet(body, [(sx * 56, y) for sx in (-1, 1) for y in (10, D - 10)])

    # ---- front plate layout ----
    vx = WIN_X - GAP                         # visible half width 57.75
    vz0, vz1 = WIN_Z0 + GAP, H_BODY          # visible plate (cover sits on top)
    PD, PP = 2.4, 4.0
    NC, NR = 25, 4
    m = vx - PP * (NC - 1) / 2 - PD / 2      # grille margin 8.55, used left/top/right and below the dial
    cols = [PP * (i - (NC - 1) / 2) for i in range(NC)]
    rows = [vz1 - m - PD / 2 - PP * j for j in range(NR)]
    DIAL_R, DIAL_H = 16.0, 8.0               # dial diameter = outer button centre distance (2 x 16)
    dial_x = -vx + m + DIAL_R                # dial left edge = grille left edge
    dial_z = vz0 + m + DIAL_R                # margin below the dial = grille margin
    BTN_D, pitch = 10.0, 16.0
    btn_xs = [vx - m - BTN_D / 2 - pitch * k for k in (2, 1, 0)]   # right button edge = grille right edge
    btn_z = dial_z                           # one centre line for every control
    LABEL_H = 3.0
    label_z = btn_z - BTN_D / 2 - 3.0 - LABEL_H / 2

    face = box(-vx, vx, 0, PT_FACE, vz0, PLATE_TOP).edges("|Y").fillet(0.75).faces("<Y").chamfer(CH)
    tongue = box(-(GROOVE_X - GAP), GROOVE_X - GAP, PT_FACE, PT, GZ0 + GAP, PLATE_TOP)
    plate = face.union(tongue)
    fp = lambda o: cq.Workplane(cq.Plane(origin=o, xDir=(1, 0, 0), normal=(0, -1, 0)))
    plate = plate.cut(fp((0, PT + 1, 0)).pushPoints([(x, z) for x in cols for z in rows])
                      .circle(PD / 2).extrude(PT + 2))
    for (x, z, d) in [(dial_x, dial_z, 7.2)] + [(x, btn_z, BTN_D + 0.6) for x in btn_xs]:
        plate = plate.cut(fp((x, PT + 1, z)).circle(d / 2).extrude(PT + 2))
    inlay = None
    for x, txt in zip(btn_xs, ["on", "1", "2"]):
        kw = {"fontPath": FONT} if FONT else {}
        t = fp((x, 0.4, label_z)).text(txt, LABEL_H, 0.4, halign="center", valign="center", **kw)
        inlay = t if inlay is None else inlay.union(t)
    plate = plate.cut(inlay)

    # ---- top cover ----
    cover = rrect(W, D, R, H_BODY, H_COVER, cy=cy).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    c = 0.3
    yf = T_FRONT + c
    lip_o = rrect(W - 2 * (T + c), D - 2 * (T + c), R - T - c, H_BODY - 3, 3, cy=cy)
    lip_i = rrect(W - 2 * (T + c + DIV), D - 2 * (T + c + DIV), R - T - c - DIV, H_BODY - 4, 5, cy=cy)
    lip = lip_o.cut(lip_i).intersect(box(-W, W, yf, D, 0, H_BODY + 1)) \
        .union(box(-(W / 2 - T - c), W / 2 - T - c, yf, yf + DIV, H_BODY - 3, H_BODY + 0.01)).intersect(lip_o)
    for (x, y) in posts:
        lip = lip.cut(box(x - POST / 2 - c, x + POST / 2 + c, y - POST / 2 - c, y + POST / 2 + c, 0, H_BODY + 1))
        cover = cover.cut(cyl(MAG_D / 2, H_BODY - 0.01, MAG_H + 0.01, x, y))
    cover = cover.union(lip)

    # ---- dial and buttons ----
    dial_l = knob_local(DIAL_R, DIAL_H, DIAL_R - 3.5, DIAL_R - 7.0, 44, 4.0)   # low disc, dot indicator
    btn_l = button_local(BTN_D, 3.0, PT, 6.5, stem_r=2.0, stem_len=4.0)
    to_asm = lambda wp, x, y, z: wp.rotate((0, 0, 0), (1, 0, 0), -90).translate((x, y, z))
    parts = {
        "body": Part(body, body, OFF),
        "front_plate": Part(plate, rx(plate, 90), PLATE),
        "label_inlay": Part(inlay, rx(inlay, 90), LABEL_GRAY, anchor="front_plate"),
        "top_cover": Part(cover, rx(cover, 180), OFF),
        "dial": Part(to_asm(dial_l, dial_x, -(DIAL_H + 0.5), dial_z), rx(dial_l, 180), OFF),
        "button_on": Part(to_asm(btn_l, btn_xs[0], -3.0, btn_z), btn_l, ACC),
    }
    b12 = to_asm(btn_l, btn_xs[1], -3.0, btn_z).union(to_asm(btn_l, btn_xs[2], -3.0, btn_z))
    parts["button"] = Part(b12, btn_l, DARK, qty=2)
    return parts


# ---------------- shared: extra helpers ----------------
def plane_yz(x0):
    """Plane at x=x0: local x = +Y, local y = +Z, normal +X."""
    return cq.Workplane(cq.Plane(origin=(x0, 0, 0), xDir=(0, 1, 0), normal=(1, 0, 0)))


def plane_xz(y0):
    """Plane at y=y0: local x = +X, local y = +Z, normal -Y."""
    return cq.Workplane(cq.Plane(origin=(0, y0, 0), xDir=(1, 0, 0), normal=(0, -1, 0)))


def stadium_x(x0, length, yc, zc, w, h):
    """Horizontal stadium hole (USB-C style) through a wall normal to X."""
    return plane_yz(x0).center(yc, zc).slot2D(w, h, 0).extrude(length)


def teardrop_x(x0, length, yc, zc, r, apex=(0, 1)):
    """Horizontal round hole along X with a 45-deg roof toward `apex` (local y,z direction)."""
    k = 0.70710678
    ay, az = apex
    # roof triangle in local (y,z)
    def rot(u, v):
        return (yc + u * az + v * ay, zc + -u * ay + v * az)
    tri = [rot(-r * k, r * k), rot(0, r * 1.41421356), rot(r * k, r * k), rot(0, 0)]
    c = plane_yz(x0).center(yc, zc).circle(r).extrude(length)
    return c.union(plane_yz(x0).polyline(tri).close().extrude(length))


def keyhole_local(travel, ledge=2.0, pocket=3.0, head=8.4, shank=4.2):
    """Cutting tool for a keyhole in a wall-side face: the wall face at z=0, the part at z > 0, the entry
    centred on the origin and the slot rising `travel` toward +y (the part drops that far onto the screw).

    The slot (shank wide) runs through the `ledge`; behind it a head pocket (head wide, `pocket` deep) with a
    45-deg seat narrowing to the slot: a countersunk head seats on it, and the pocket prints without support
    with the wall face up (the part printed face down). The entry hole and the top ends have 45-deg roofs
    toward +y, so the tool also prints with the wall face vertical and +y up (the part printed bottom down).
    Move it onto the face with rx/rz/translate or on_slope (rx(tool, 90) puts a wall face at y=0 for a part
    in y < 0, +y up)."""
    k = 0.70710678

    def outline(w, z):                    # the slot or pocket in plan: a round bottom end, a 45-deg roof at the top
        h = w / 2
        return (cq.Workplane("XY").workplane(offset=z).moveTo(-h, 0).lineTo(-h, travel)
                .threePointArc((-h * 0.92388, travel + h * 0.38268), (-h * k, travel + h * k))
                .lineTo(0, travel + h * 1.41421356).lineTo(h * k, travel + h * k)
                .threePointArc((h * 0.92388, travel + h * 0.38268), (h, travel)).lineTo(h, 0)
                .threePointArc((0, -h), (-h, 0)).close())

    zs = ledge + (head - shank) / 2
    tool = outline(shank, -1).extrude(ledge + 1)
    seat = cq.Solid.makeLoft([outline(shank, ledge).wires().val(), outline(head, zs).wires().val()], True)
    tool = tool.union(cq.Workplane("XY").add(seat)).union(outline(head, zs).extrude(ledge + pocket - zs))
    r = head / 2                          # entry: the head passes the ledge and the seat here
    roof = [(-r * k, r * k), (0, r * 1.41421356), (r * k, r * k), (0, 0)]
    entry = cyl(r, -1, ledge + pocket + 1).union(
        cq.Workplane("XY").workplane(offset=-1).polyline(roof).close().extrude(ledge + pocket + 1))
    return tool.union(entry)


# ---------------- 07 hinged case ----------------
def hinged_case():
    """Box with a lid on a pin hinge (1.75 mm filament as the pin) and magnet closure."""
    W, Dp, R = 96.0, 64.0, 12.0
    HB, HL = 24.0, 8.0                      # 3 : 1, total 32
    FLOOR, TOP = 2.4, 2.4
    yb = Dp / 2                              # hinge axis on the back face, at the seam
    KR = 4.0                                 # knuckle radius
    KL, KG, NK = 12.0, 0.4, 5                # knuckle length, gap, count
    PIN = 1.9                                # 1.75 filament pin
    x0 = -(NK * KL + (NK - 1) * KG) / 2
    segs = [(x0 + i * (KL + KG), x0 + i * (KL + KG) + KL) for i in range(NK)]
    base_k, lid_k = segs[0::2], segs[1::2]
    MAG_X = 24.0
    POST = 8.0

    base = rrect(W, Dp, R, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    base = base.cut(rrect(W - 2 * T, Dp - 2 * T, R - T, FLOOR, HB))
    lid = rrect(W, Dp, R, HB, HL).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    lid = lid.cut(rrect(W - 2 * T, Dp - 2 * T, R - T, HB - 1, HL - TOP + 1))

    # magnet posts at the front (vertical, printable both ways)
    fy = -Dp / 2 + T + POST / 2
    for sx in (-1, 1):
        x = sx * MAG_X
        base = base.union(box(x - POST / 2, x + POST / 2, fy - POST / 2, fy + POST / 2, FLOOR - .1, HB))
        base = base.cut(cyl(3.1, HB - 3.2, 3.3, x, fy))
        lid = lid.union(box(x - POST / 2, x + POST / 2, fy - POST / 2, fy + POST / 2, HB + 0.0, HB + HL - TOP + .1))
        lid = lid.cut(cyl(3.1, HB - 0.1, 3.3, x, fy))

    # lid lip on front and sides only (the back must swing freely)
    c = GAP
    lip = rrect(W - 2 * (T + c), Dp - 2 * (T + c), R - T - c, HB - 3, 3.01) \
        .cut(rrect(W - 2 * (T + c + DIV), Dp - 2 * (T + c + DIV), R - T - c - DIV, HB - 4, 5)) \
        .cut(box(-W, W, 0, Dp, 0, 100))
    for sx in (-1, 1):
        x = sx * MAG_X
        lip = lip.cut(box(x - POST / 2 - c, x + POST / 2 + c, fy - POST / 2 - c, fy + POST / 2 + c, 0, 100))
    lid = lid.union(lip)

    # knuckles: circle + 45-deg web down to the wall (base) / up to the wall (lid)
    def knuckle(xa, xb, sign):
        k = 2.828427
        web = [(yb - 0.6, HB), (yb + k, HB + sign * k), (yb, HB + sign * 2 * k), (yb - 0.6, HB + sign * 2 * k)]
        s = plane_yz(xa).center(yb, HB).circle(KR).extrude(xb - xa)
        return s.union(plane_yz(xa).polyline(web).close().extrude(xb - xa))

    for (xa, xb) in base_k:
        base = base.union(knuckle(xa, xb, -1))
    for (xa, xb) in lid_k:
        lid = lid.union(knuckle(xa, xb, +1))
    for (xa, xb) in lid_k:                       # room in the base for the lid knuckles
        base = base.cut(plane_yz(xa - .2).center(yb, HB).circle(KR + 0.4).extrude(xb - xa + .4))
    for (xa, xb) in base_k:                      # room in the lid for the base knuckles
        lid = lid.cut(plane_yz(xa - .2).center(yb, HB).circle(KR + 0.4).extrude(xb - xa + .4))
    pin = plane_yz(-W).center(yb, HB).circle(PIN / 2).extrude(2 * W)
    base, lid = base.cut(pin), lid.cut(pin)

    # finger scoop across the front seam: one shallow disc, half in each part
    SCOOP_R = 0.75 * HL                       # stays below the lid's top edge
    scoop = plane_xz(-Dp / 2 + 1.2).center(0, HB).circle(SCOOP_R).extrude(3)
    base, lid = base.cut(scoop), lid.cut(scoop)
    base = feet(base, [(sx * 36, sy * 20) for sx in (-1, 1) for sy in (-1, 1)])

    return {
        "base": Part(base, base, OFF),
        "lid": Part(lid, rx(lid, 180), OFF),
    }


# ---------------- 08 power bank ----------------
def power_bank():
    """Slab printed top-face down. Bottom door slides in dovetail rails, held by a printed snap tab.
    USB-C port window, LED light-pipe holes, one accent button."""
    L, W, H, R = 120.0, 64.0, 24.0, 12.0
    TOP = 2.0
    DT = 2.4                                  # door thickness
    yr = W / 2 - T - DIV                      # rail inner face
    hw0, hw1 = yr - GAP, yr - GAP + 1.2       # door half width at z=0 / z=DT (dovetail)

    body = rrect(L, W, R, 0, H).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    body = body.cut(rrect(L - 2 * T, W - 2 * T, R - T, -1, H - TOP + 1))
    outline = rrect(L, W, R, -1, H + 2)
    for s in (-1, 1):
        rail = box(-L / 2, L / 2, min(s * yr, s * (W / 2 - T + .01)), max(s * yr, s * (W / 2 - T + .01)), 0, 2 * DT)
        body = body.union(rail.intersect(outline))

    # partition carrying the snap notch (full height: no bridge when printed upside down)
    xp0, xp1 = L / 2 - 16.2, L / 2 - 12.0
    xn = (xp0 + xp1) / 2
    cav = rrect(L - 2 * T, W - 2 * T, R - T, 0, H)
    body = body.union(box(xp0, xp1, -W, W, DT + GAP, H - TOP + .01).intersect(cav))
    body = body.cut(box(xn - 0.9, xn + 0.9, -yr, yr, DT, DT + GAP + 0.9))

    def trap(h0, h1, z1, x_a, x_b):
        return plane_yz(x_a).polyline([(-h0, -.01 if z1 > DT else 0), (h0, -.01 if z1 > DT else 0),
                                        (h1, z1), (-h1, z1)]).close().extrude(x_b - x_a)

    # envelope cut: door path, clipped to the cavity on the closed (-X) end
    env = trap(yr, yr + 1.2 * (DT + GAP) / DT, DT + GAP, -L / 2, L / 2 + 5)
    env = env.intersect(rrect(L - 2 * T, W - 2 * T, R - T, -1, 10).union(box(0, L, -W, W, -1, 10)))
    body = body.cut(env)

    door = trap(hw0, hw1, DT, -L / 2, L / 2 + 1)
    door = door.intersect(
        rrect(L - 2 * (T + GAP), W - 2 * (T + GAP), R - T - GAP, -1, 10).intersect(box(-L, 0, -W, W, -2, 10))
        .union(rrect(L, W, R, -1, 10).intersect(box(0, L, -W, W, -2, 10))))
    door = door.faces("<Z").chamfer(CH)
    # snap tab: U-slot frees a cantilever; 45-deg bump drops into the partition notch
    tx0, tx1, tw = xn - 12.0, xn + 1.5, 5.0
    door = door.cut(box(tx0, tx1 + 1.0, tw, tw + 1.0, -1, DT + 1)).cut(box(tx0, tx1 + 1.0, -tw - 1.0, -tw, -1, DT + 1)) \
        .cut(box(tx1, tx1 + 1.0, -tw - 1.0, tw + 1.0, -1, DT + 1))
    bump = plane_xz(-(tw - 0.5)).polyline([(xn - 0.8, DT), (xn + 0.8, DT), (xn, DT + 0.8)]).close().extrude(-(2 * tw - 1))
    door = door.union(bump)
    door = door.cut(box(tx1 - 6, tx1 - 3, -3, 3, -0.01, 0.6))          # thumb grip on the tab

    # top face: LED light pipes on the centre line, accent button on the same line
    BTN_X, BTN_D = L / 4, 10.0                           # quarter point of the length
    LED_P = 4.0                                          # grid pitch
    last = BTN_X - BTN_D / 2 - 2 * LED_P                 # LED row ends 2 pitches before the button
    LED = [last - LED_P * i for i in range(4)]
    for x in LED:
        body = body.cut(cyl(0.8, H - TOP - 1, TOP + 2, x, 0))   # Φ1.6: smallest hole that stays open in FDM
    body = body.cut(cyl(5.3, H - TOP - 1, TOP + 2, BTN_X, 0))
    # USB-C window on the closed end (-X), centred on the remaining wall height
    body = body.cut(stadium_x(-L / 2 - 1, T + 2, 0, (DT + H) / 2, 12.0, 6.4))
    btn_l = button_local(10.0, 1.2, TOP, 6.5, stem_len=2.0)
    btn = rx(btn_l, 180).translate((BTN_X, 0, H + 1.2))
    return {
        "body": Part(body, rx(body, 180), OFF),
        "door": Part(door, door, OFF),
        "button": Part(btn, btn_l, ACC),
    }


# ---------------- 09 wall unit ----------------
def wall_unit():
    """Wall-mounted unit (thermostat/sensor type). Bracket screws to the wall via keyholes,
    cover clicks on with two removable 45-deg snap hooks; clear window insert; plinth shadow gap."""
    S, R, DEP = 84.0, 12.0, 16.0
    FRONT = 2.4
    BR, BT = 76.0, 3.0                        # bracket
    XH = 36.5                                 # hook outer face
    HZ1 = 12.0
    PL, INSET = 2.4, 1.2

    # local frame: wall is z=0, front at z=DEP
    cov = rrect(S - 2 * INSET, S - 2 * INSET, R - INSET, 0, PL)
    cov = cov.union(rrect(S, S, R, PL, DEP - PL).faces("<Z").chamfer(INSET)).faces(">Z").chamfer(CH_BED)
    cov = cov.cut(rrect(S - 2 * T, S - 2 * T, R - T, -1, DEP - FRONT + 1))
    xp = XH + 0.2
    xw = S / 2 - T
    for s in (-1, 1):
        pad = box(min(s * xp, s * xw), max(s * xp, s * xw), -7, 7, 0, DEP - FRONT + .01)
        cov = cov.union(pad)
        groove = plane_xz(-8).polyline([(s * (xp - .01), 7.8), (s * (xp + 1.25), 9.05), (s * (xp + 1.25), 10.0),
                                         (s * (xp - .01), 11.25)]).close().extrude(-16)
        cov = cov.cut(groove)

    WIN_W, WIN_H = 40.0, 16.0
    m = (S - WIN_W) / 2                       # side margin = top margin = bottom margin
    win_y = S / 2 - m - WIN_H / 2
    BTN_D = 10.0
    btn_y = -S / 2 + m + BTN_D / 2
    cov = cov.cut(rrect(WIN_W, WIN_H, 2.0, DEP - FRONT - 1, FRONT + 2, 0, win_y))
    cov = cov.cut(cyl(BTN_D / 2 + 0.3, DEP - FRONT - 1, FRONT + 2, 0, btn_y))

    win = rrect(WIN_W - 2 * GAP, WIN_H - 2 * GAP, 2.0 - GAP, DEP - FRONT, FRONT) \
        .union(rrect(WIN_W + 6, WIN_H + 6, 3.0, DEP - FRONT - 1.2, 1.2)).translate((0, win_y, 0))
    win = win.faces(">Z").chamfer(CH)

    br = rrect(BR, BR, 8.0, 0, BT)
    for s in (-1, 1):                       # keyholes: head Φ8, slot 4 wide going up, head channel on the wall side
        yk = s * 20.0
        br = br.cut(cyl(4.2, -1, BT + 2, 0, yk)).cut(box(-2.1, 2.1, yk, yk + 8, -1, BT + 2))
        br = br.cut(box(-4.2, 4.2, yk, yk + 8, -1, 1.6)).cut(cyl(4.2, -1, 2.6, 0, yk + 8))
    for s in (-1, 1):                       # clear the cover's catch pads
        br = br.cut(box(min(s * (XH + .05), s * BR), max(s * (XH + .05), s * BR), -7.3, 7.3, -1, BT + 1))
    for s in (-1, 1):
        x_in, x_out = s * (XH - DIV), s * XH
        hook = box(min(x_in, x_out), max(x_in, x_out), -5, 5, BT - .01, HZ1)
        barb = plane_xz(-5).polyline([(x_out, 8.0), (x_out + s * 1.0, 9.0), (x_out + s * 1.0, 10.0),
                                       (x_out, 11.0)]).close().extrude(-10)
        br = br.union(hook).union(barb)

    btn_l = button_local(BTN_D, 1.2, FRONT, 6.5, stem_len=2.0)
    btn = rx(btn_l, 180).translate((0, btn_y, DEP + 1.2))
    disp = lambda wp: rx(wp, 90)
    return {
        "cover": Part(disp(cov), rx(cov, 180), OFF),
        "bracket": Part(disp(br), br, OFF),
        "window_smoke": Part(disp(win), rx(win, 180), DARK),
        "button": Part(disp(btn), btn_l, ACC),
    }


# ---------------- 10 lantern ----------------
def lantern():
    """Stacked sections: opaque base, translucent diffuser tube, cap. Slide switch on the side."""
    S, R = 64.0, 12.0
    HB, HD, HC = 48.0, 64.0, 16.0             # total 128 = 2 x 64
    WD = DIV                                  # diffuser wall 1.68 (even glow)
    base = rrect(S, S, R, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    base = base.cut(rrect(S - 2 * T, S - 2 * T, R - T, 2.4, HB))
    lo, li = WD + GAP, WD + GAP + DIV         # lip offsets
    lip_b = rrect(S - 2 * lo, S - 2 * lo, R - lo, HB - 1, 4.01).cut(rrect(S - 2 * li, S - 2 * li, R - li, HB - 2, 7))
    base = base.union(lip_b)
    dif = rrect(S, S, R, HB, HD).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH)
    dif = dif.cut(rrect(S - 2 * WD, S - 2 * WD, R - WD, HB - 1, HD + 2))
    cap = rrect(S, S, R, HB + HD, HC).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    cap = cap.cut(rrect(S - 2 * T, S - 2 * T, R - T, HB + HD - 1, HC - 2.4 + 1))
    lip_c = rrect(S - 2 * lo, S - 2 * lo, R - lo, HB + HD - 3, 3.01).cut(rrect(S - 2 * li, S - 2 * li, R - li, HB + HD - 4, 5))
    cap = cap.union(lip_c)

    # slide switch on the +X side: vertical slot (prints clean), travel 8
    TRAVEL, NECK = 8.0, 2.4
    SZ0 = HB / 2 - (1.5 + NECK / 2) - TRAVEL / 2   # mid-travel = base mid-height
    slot_z0, slot_z1 = SZ0, SZ0 + TRAVEL + NECK + 3.0     # +3: rounded slot ends
    xo = S / 2
    base = base.cut(box(xo - T - 1, xo + 1, -(NECK + 0.6) / 2, (NECK + 0.6) / 2, slot_z0, slot_z1)
                    .edges("|X").fillet(1.4))
    zs = slot_z0 + 1.5 + NECK / 2            # slider at the "off" end, clear of the end radius
    carrier = box(xo - T - 1.6 - 1.6, xo - T - 0.2, -6, 6, zs - 7, zs + 7) \
        .union(box(xo - T - 0.3, xo + 1.0, -NECK / 2, NECK / 2, zs - NECK / 2, zs + NECK / 2))
    knob = box(xo + 0.3, xo + 2.7, -5, 5, zs - 9, zs + 9)
    knob = knob.edges("|X").fillet(2.0).faces(">X").chamfer(CH)
    knob = knob.cut(box(xo + 0.29, xo + 1.31, -NECK / 2 - 0.1, NECK / 2 + 0.1, zs - NECK / 2 - .1, zs + NECK / 2 + .1))
    for k in range(-2, 3):                    # 3 grip grooves, pitch 4
        knob = knob.cut(box(xo + 2.2, xo + 3, -4, 4, zs + 4 * k - 0.4, zs + 4 * k + 0.4)) if k in (-1, 0, 1) else knob

    base = base.cut(teardrop_x(-S / 2 - 1, T + 2, 0, 10.0, 3.0, apex=(0, 1)))   # cable, back
    base = feet(base, [(sx * 20, sy * 20) for sx in (-1, 1) for sy in (-1, 1)])
    DIF = (0.99, 0.94, 0.80)                  # translucent white, shown lit
    return {
        "base": Part(base, base, OFF),
        "diffuser_translucent": Part(dif, dif.translate((0, 0, -HB)), DIF),
        "cap": Part(cap, rx(cap, 180), OFF),
        "slider_carrier": Part(carrier, carrier.rotate((0, 0, 0), (0, 1, 0), -90), DARK),
        "slider_knob": Part(knob, knob.rotate((0, 0, 0), (0, 1, 0), 90), ACC),
    }


# ---------------- 11 split riser ----------------
def split_riser():
    """400 mm monitor riser > any bed: two L-halves printed on their side (profile on the bed),
    joined at the centre with 4 mm steel dowels. The joint is a designed V line."""
    L, Dp, Hh, t = 400.0, 200.0, 80.0, 12.0
    PIN_D, PIN_L = 4.2, 14.0
    half = L / 2
    P = {"top_out": (-half, Hh), "foot_o": (-half, 0), "foot_i": (-half + t, 0), "ic": (-half + t, Hh - t),
         "j_bot": (0, Hh - t), "j_top": (0, Hh)}
    order = ["foot_o", "foot_i", "ic", "j_bot", "j_top", "top_out"]
    prof = plane_xz(Dp / 2).polyline([P[k] for k in order]).close()
    a = prof.extrude(Dp)                          # extrudes toward +Y? normal -Y -> toward -Y
    # ground-contact ends stay flat (only the bed chamfer); full rounds are for free ends only
    radii = {"top_out": 16.0, "ic": 12.0}
    for k, r in radii.items():
        x, z = P[k]
        a = a.edges("|Y").edges(BoxSelector((x - .05, -Dp, z - .05), (x + .05, Dp, z + .05))).fillet(r)
    a = a.faces("<Y").chamfer(CH_BED).faces(">Y").chamfer(CH)
    a = a.faces(">X").chamfer(CH)                 # joint face: half of the designed V line
    for y in (-60.0, 0.0, 60.0):
        a = a.cut(teardrop_x(-PIN_L, PIN_L + 1, y, Hh - t / 2, PIN_D / 2, apex=(1, 0)))
    a = a.edges("|Y").edges(BoxSelector((-half - .1, -Dp, -.1), (-half + t + .1, Dp, .1))).chamfer(CH)
    for y in (-60.0, 60.0):                       # round 10 mm feet under the leg
        a = a.cut(cyl(5.1, -0.01, 1.01, -half + t / 2, y))
    b = a.mirror("YZ")
    prn = a.rotate((0, 0, 0), (1, 0, 0), 90)      # profile face (y = -Dp/2) on the bed
    pins = None
    for y in (-60.0, 0.0, 60.0):
        p = plane_yz(-PIN_L + 1).center(y, Hh - t / 2).circle(2.0).extrude(2 * PIN_L - 2)
        pins = p if pins is None else pins.union(p)
    return {
        "half_left": Part(a, prn, OFF),
        "half_right": Part(b, b.rotate((0, 0, 0), (1, 0, 0), 90), OFF),
        "dowels_steel_ref": Part(pins, pins.rotate((0, 0, 0), (0, 1, 0), 90), DARK),
    }


# ---------------- 12 threaded jar ----------------
def thread_solid(r_root, z0, turns, pitch, depth, base, crest, external=True):
    h = pitch * turns
    helix = cq.Wire.makeHelix(pitch, h, r_root, center=cq.Vector(0, 0, z0))
    sgn = 1 if external else -1
    rb = r_root - sgn * 0.2
    rc = r_root + sgn * depth
    pts = [(rb, z0 - base / 2), (rc, z0 - crest / 2), (rc, z0 + crest / 2), (rb, z0 + base / 2)]
    prof = cq.Workplane(cq.Plane(origin=(0, 0, 0), xDir=(1, 0, 0), normal=(0, -1, 0))).polyline(pts).close()
    return prof.sweep(cq.Workplane(obj=helix), isFrenet=True)


def jar():
    """Screw-top jar. Lid is flush with the body; 45-deg thread flanks print upright and upside down."""
    RO, HB, HL = 40.0, 64.0, 16.0            # body : lid = 4 : 1, height = diameter (80)
    NECK_R = 36.0                             # thread root on the body
    PITCH, DEPTH = 4.0, 1.2
    body = cyl(RO, 0, HB).faces("<Z").chamfer(CH_BED).faces(">Z").chamfer(CH)
    body = body.union(cyl(NECK_R, HB - .01, 12.0))
    ri = RO - T
    rn = NECK_R - T
    inner = cyl(ri, 2.4, HB - 6.4).union(cq.Workplane("XY").add(
        cq.Solid.makeCone(ri, rn, ri - rn, pnt=cq.Vector(0, 0, HB - 4.0)))).union(cyl(rn, HB - 4.0 + (ri - rn) - .01, 20))
    body = body.cut(inner)
    body = body.faces(">Z").chamfer(CH)
    body = body.union(thread_solid(NECK_R, HB + 2.0, 2.0, PITCH, DEPTH, 2.8, 0.4, external=True))
    body = feet(body, [(sx * 22, sy * 22) for sx in (-1, 1) for sy in (-1, 1)])

    rl = RO - 2.4                             # lid wall 2.4 on the shoulder
    lid = cyl(RO, HB, HL).faces("<Z").chamfer(CH).faces(">Z").chamfer(CH_BED)
    lid = lid.cut(cyl(rl, HB - 1, HL - 2.4 + 1))
    lid = lid.union(thread_solid(rl, HB + 2.0 + PITCH / 2, 2.25, PITCH, DEPTH, 2.4, 0.4, external=False)
                    .intersect(cyl(RO - 0.5, HB + 0.5, HL - 3)))
    ribs = (cq.Workplane("XY").workplane(offset=HB + 7).polarArray(RO, 0, 360, 72).rect(1.0, 0.8).extrude(HL - 7.5))
    lid = lid.cut(ribs)                        # grip on the upper band only; seam band stays smooth
    return {
        "body": Part(body, body, OFF),
        "lid": Part(lid, rx(lid, 180), OFF),
    }


SAMPLES = {
    "01_clock": clock,
    "02_remote": remote,
    "03_tray": tray,
    "04_cylinder_speaker": cylinder,
    "05_stand": stand,
    "06_radio": radio,
    "07_hinged_case": hinged_case,
    "08_power_bank": power_bank,
    "09_wall_unit": wall_unit,
    "10_lantern": lantern,
    "11_split_riser": split_riser,
    "12_threaded_jar": jar,
}


def load_module(path):
    """Run a design file (it registers its designs in SAMPLES) and return the model.json next to it.

    model.json is optional ({} without it). The scripts read from it what a design file does not say:
    the print orientation of each part (parts[].orientation), the camera of render.py (view) and the
    motions verify.py sweeps (motions); the format is in models/README.md of the repository."""
    import importlib.util
    import json
    spec = importlib.util.spec_from_file_location("user_designs", path)
    spec.loader.exec_module(importlib.util.module_from_spec(spec))
    meta = os.path.join(os.path.dirname(os.path.abspath(path)), "model.json")
    if not os.path.isfile(meta):
        return {}
    with open(meta, encoding="utf-8") as f:
        return json.load(f)


def export(root, names=None):
    """Write print-oriented STLs, assembly STLs (for render.py), STEP and colours for each design."""
    import json
    report = {}
    cpath = os.path.join(root, "_colors.json")
    if os.path.exists(cpath):
        report = json.load(open(cpath))
    for sname, fn in SAMPLES.items():
        if names and sname not in names:
            continue
        out = os.path.join(root, sname)
        os.makedirs(out, exist_ok=True)
        for f in os.listdir(out):
            if f.endswith((".stl", ".step")):
                os.remove(os.path.join(out, f))
        parts = fn()
        shifts = {}
        asm = cq.Assembly(name=sname)
        for name, p in parts.items():
            if not p.ref:                      # a bought part is in the assembly, not on the bed
                bb = p.prn.val().BoundingBox()
                shift = shifts[p.anchor] if p.anchor else (-bb.xmin, -bb.ymin, -bb.zmin)
                shifts[name] = shift
                suffix = f"_x{p.qty}" if p.qty > 1 else ""
                cq.exporters.export(p.prn.translate(shift), os.path.join(out, f"print_{name}{suffix}.stl"),
                                    tolerance=0.02, angularTolerance=0.1)
            cq.exporters.export(p.asm, os.path.join(out, f"_asm_{name}.stl"),
                                tolerance=0.02, angularTolerance=0.1)
            asm.add(p.asm, name=name, color=cq.Color(*p.color))
        asm.export(os.path.join(out, f"{sname}_assembly.step"))
        report[sname] = {n: {"color": p.color} for n, p in parts.items()}
        print("exported", sname)
    with open(os.path.join(root, "_colors.json"), "w") as f:
        json.dump(report, f)


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Generate the FDM sample objects (STL in print orientation + STEP).")
    ap.add_argument("names", nargs="*", help="sample names, e.g. 06_radio (default: all)")
    ap.add_argument("--out", default="fdm_samples_out", help="output directory")
    ap.add_argument("--list", action="store_true", help="list available samples")
    a = ap.parse_args()
    if a.list:
        print("\n".join(SAMPLES))
        return
    os.makedirs(a.out, exist_ok=True)
    export(a.out, a.names or None)


if __name__ == "__main__":
    main()
