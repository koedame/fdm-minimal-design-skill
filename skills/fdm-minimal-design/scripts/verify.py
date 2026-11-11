"""
Numeric checks for a design (references/04_review.md, Step 4).

  python verify.py 06_radio
  python verify.py --all
  python verify.py my_lamp --module template_new_object.py --bed 220
  python verify.py 07_hinged_case --hinge "lid:base:0,32,24:1,32,24:-30,-60,-90,-110"
  python verify.py my_case --module my_case.py --slide "lid:body:1,0,0:0,20,40"

Checks
  * solid validity of every part
  * interference between parts in the assembled state (should be 0)
  * print-oriented mesh is closed (watertight) and sits on z=0
  * part fits the bed (X/Y/Z extents)
  * a part with qty > 1 holds qty separate solids (copies that touch must not fuse)
  * ground contact in the assembled state: width and area of the slice at z=0
  * motions: a hinge (rotation) or a slide (translation) of one part against another, overlap at
    each position. --hinge and --slide expect no overlap anywhere; the motions in a model.json next to
    the --module file also say where a stop or a snap must touch (see motion_check)

Bought parts (Part(ref=True)) are checked for validity and interference, not as prints.
"""
import argparse
import itertools
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadquery as cq                      # noqa: E402
import fdm_samples as fs                  # noqa: E402


def mesh_check(wp):
    try:
        import trimesh
    except ImportError:
        return None, None
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "p.stl")
        bb = wp.val().BoundingBox()
        cq.exporters.export(wp.translate((-bb.xmin, -bb.ymin, -bb.zmin)), f, tolerance=0.05, angularTolerance=0.2)
        m = trimesh.load(f)
        return m.is_watertight, m.extents


def ground_contact(parts, thickness=0.05):
    slab = cq.Workplane("XY").box(5000, 5000, thickness, centered=(True, True, False)).val()
    zmin = min(p.asm.val().BoundingBox().zmin for p in parts.values())
    slab = slab.translate(cq.Vector(0, 0, zmin))
    area, boxes, narrow = 0.0, [], float("inf")
    for p in parts.values():
        s = p.asm.val().intersect(slab)
        if s.Volume() <= 1e-6:
            continue
        area += s.Volume() / thickness
        boxes.append(s.BoundingBox())
        for sol in s.Solids():                 # each separate contact patch
            b = sol.BoundingBox()
            narrow = min(narrow, min(b.xlen, b.ylen))
    if not boxes:
        return 0.0, 0.0, 0.0, 0.0
    w = max(b.xmax for b in boxes) - min(b.xmin for b in boxes)
    d = max(b.ymax for b in boxes) - min(b.ymin for b in boxes)
    return area, w, d, narrow


CLASH = 1e-3   # mm3: more overlap than this is a collision


def parse_motion(kind, spec):
    """--hinge "moving:fixed:x1,y1,z1:x2,y2,z2:ang,..." / --slide "moving:fixed:dx,dy,dz:mm,..." as a motion."""
    f = spec.split(":")
    vec = lambda t: [float(v) for v in t.split(",")]                 # noqa: E731
    if kind == "hinge":
        return {"part": f[0], "against": f[1], "hinge": [vec(f[2]), vec(f[3])], "free": vec(f[4])}
    return {"part": f[0], "against": f[1], "slide": vec(f[2]), "free": vec(f[3])}


def moved(wp, motion, pos):
    if "hinge" in motion:
        p1, p2 = motion["hinge"]
        return wp.rotate(tuple(p1), tuple(p2), pos)
    d = motion["slide"]
    n = sum(c * c for c in d) ** 0.5
    return wp.translate(tuple(c / n * pos for c in d))


def motion_check(parts, motion):
    """Overlap of motion["part"] moved against motion["against"], with what each position expects.

    motion: {"part", "against", and "hinge": [[x1, y1, z1], [x2, y2, z2]] (two points on the axis,
    positions in degrees) or "slide": [dx, dy, dz] (positions in mm along it), from the assembled pose}
    with the positions to try:
      "free": [...]   no overlap: the part moves freely there
      "stop": [...]   overlap: a stop or end wall catches the part there (proves the limit exists)
      "snap": {"at": [...], "max_mm3": v}   a small overlap up to v: a snap or detent being pushed over
    Returns [(position, overlap, expected, ok)].
    """
    a, b = parts[motion["part"]].asm, parts[motion["against"]].asm.val()
    snap = motion.get("snap", {})
    steps = ([(p, "free") for p in motion.get("free", [])] + [(p, "stop") for p in motion.get("stop", [])]
             + [(p, "snap") for p in snap.get("at", [])])
    out = []
    for pos, want in sorted(steps):
        vol = moved(a, motion, pos).val().intersect(b).Volume()
        ok = {"free": vol <= CLASH, "stop": vol > CLASH,
              "snap": CLASH < vol <= snap.get("max_mm3", 0)}[want]
        out.append((pos, vol, want, ok))
    return out


def check(name, bed, motions=()):
    parts = fs.SAMPLES[name]()
    print(f"== {name}")
    ok = True
    for n, p in parts.items():
        v = p.asm.val()
        valid = v.isValid()
        if p.ref:
            flag = "" if valid else "  <-- CHECK"
            ok &= flag == ""
            print(f"  {n:22s} valid={valid} bought part, not printed{flag}")
            continue
        wt, ext = mesh_check(p.prn)
        fits = ext is None or all(e <= bed + 1e-6 for e in ext)
        # copies that touch fuse in a union: then the tools cannot tell them apart
        fused = p.qty > 1 and len(v.Solids()) != p.qty * len(p.prn.val().Solids())
        flag = "" if (valid and wt in (True, None) and fits and not fused) else "  <-- CHECK"
        ok &= flag == ""
        ext_s = "x".join(f"{e:.1f}" for e in ext) if ext is not None else "n/a"
        print(f"  {n:22s} valid={valid} watertight={wt} print_extent={ext_s} fits_bed({bed})={fits}{flag}")
        if fused:
            print(f"    qty {p.qty} but the assembled shape has {len(v.Solids())} solid(s): copies fused in a union;"
                  " build them with fdm_samples.copies()")
    clash = []
    for a, b in itertools.combinations(parts, 2):
        if parts[a].anchor == b or parts[b].anchor == a:
            continue                       # inlay touches its parent by design
        vol = parts[a].asm.val().intersect(parts[b].asm.val()).Volume()
        if vol > CLASH:
            clash.append(f"{a} x {b}: {vol:.3f} mm3")
    print("  interference:", "none" if not clash else "")
    for c in clash:
        print("    " + c)
    ok &= not clash
    area, w, d, narrow = ground_contact(parts)
    print(f"  ground contact (assembled, lowest z): area {area:.0f} mm2, span {w:.1f} x {d:.1f} mm, "
          f"narrowest patch {narrow:.1f} mm" + ("  <-- line contact? (ignore for wall-mounted parts)" if narrow < 5 else ""))
    for m in motions:
        if not (m["part"] in parts and m["against"] in parts):
            print(f"  motion {m['part']} against {m['against']} skipped: the parts are not in this design")
            continue
        what, unit = ("hinge", "deg") if "hinge" in m else ("slide along ({:g}, {:g}, {:g})".format(*m["slide"]), "mm")
        for pos, vol, want, good in motion_check(parts, m):
            print(f"  {what} {m['part']} against {m['against']} {pos:+g} {unit}: overlap {vol:.3f} mm3, "
                  f"expected {want}" + ("" if good else "  <-- CHECK"))
            ok &= good
    print("  RESULT:", "OK" if ok else "NEEDS ATTENTION")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--module", help="python file that registers extra designs in fdm_samples.SAMPLES "
                    "(the motions of a model.json next to it are checked too)")
    ap.add_argument("--bed", type=float, default=256.0, help="bed size in mm (cube)")
    ap.add_argument("--hinge", help='"moving:fixed:x1,y1,z1:x2,y2,z2:ang1,ang2,..." (assembly frame)')
    ap.add_argument("--slide", help='"moving:fixed:dx,dy,dz:mm1,mm2,..." (assembly frame)')
    a = ap.parse_args()
    meta = fs.load_module(a.module) if a.module else {}
    names = list(fs.SAMPLES) if a.all else a.names
    if not names:
        ap.error("give sample names or --all")
    extra = [parse_motion(k, v) for k, v in (("hinge", a.hinge), ("slide", a.slide)) if v]
    results = [check(n, a.bed, (meta.get("motions", []) if n == meta.get("id") else []) + extra) for n in names]
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
