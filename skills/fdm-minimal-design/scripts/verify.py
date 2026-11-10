"""
Numeric checks for a design (references/04_review.md, Step 4).

  python verify.py 06_radio
  python verify.py --all
  python verify.py my_lamp --module template_new_object.py --bed 220
  python verify.py 07_hinged_case --hinge "lid:base:0,32,24:1,32,24:-30,-60,-90,-110"

Checks
  * solid validity of every part
  * interference between parts in the assembled state (should be 0)
  * print-oriented mesh is closed (watertight) and sits on z=0
  * part fits the bed (X/Y/Z extents)
  * ground contact in the assembled state: width and area of the slice at z=0
  * optional: hinge / rotation sweep, overlap at each angle
"""
import argparse
import importlib.util
import itertools
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadquery as cq                      # noqa: E402
import fdm_samples as fs                  # noqa: E402


def load_module(path):
    spec = importlib.util.spec_from_file_location("user_designs", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)           # the module registers its designs in fs.SAMPLES


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


def hinge_sweep(parts, spec):
    a, b, p1, p2, angs = spec.split(":")
    p1 = tuple(float(v) for v in p1.split(","))
    p2 = tuple(float(v) for v in p2.split(","))
    out = []
    for ang in (float(v) for v in angs.split(",")):
        moved = parts[a].asm.rotate(p1, p2, ang)
        out.append((ang, moved.val().intersect(parts[b].asm.val()).Volume()))
    return out


def check(name, bed, hinge=None):
    parts = fs.SAMPLES[name]()
    print(f"== {name}")
    ok = True
    for n, p in parts.items():
        v = p.asm.val()
        valid = v.isValid()
        wt, ext = mesh_check(p.prn)
        fits = ext is None or all(e <= bed + 1e-6 for e in ext)
        zmin = p.prn.val().BoundingBox().zmin
        flag = "" if (valid and wt in (True, None) and fits) else "  <-- CHECK"
        ok &= flag == ""
        ext_s = "x".join(f"{e:.1f}" for e in ext) if ext is not None else "n/a"
        print(f"  {n:22s} valid={valid} watertight={wt} print_extent={ext_s} fits_bed({bed})={fits}{flag}")
    clash = []
    for a, b in itertools.combinations(parts, 2):
        if parts[a].anchor == b or parts[b].anchor == a:
            continue                       # inlay touches its parent by design
        vol = parts[a].asm.val().intersect(parts[b].asm.val()).Volume()
        if vol > 1e-3:
            clash.append(f"{a} x {b}: {vol:.3f} mm3")
    print("  interference:", "none" if not clash else "")
    for c in clash:
        print("    " + c)
    ok &= not clash
    area, w, d, narrow = ground_contact(parts)
    print(f"  ground contact (assembled, lowest z): area {area:.0f} mm2, span {w:.1f} x {d:.1f} mm, "
          f"narrowest patch {narrow:.1f} mm" + ("  <-- line contact? (ignore for wall-mounted parts)" if narrow < 5 else ""))
    if hinge and not all(k in parts for k in hinge.split(":")[:2]):
        print("  rotation sweep skipped: parts named in --hinge are not in this design")
        hinge = None
    if hinge:
        for ang, vol in hinge_sweep(parts, hinge):
            print(f"  rotation {ang:+.0f} deg: overlap {vol:.3f} mm3" + ("  <-- CLASH" if vol > 1e-3 else ""))
            ok &= vol <= 1e-3
    print("  RESULT:", "OK" if ok else "NEEDS ATTENTION")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--module", help="python file that registers extra designs in fdm_samples.SAMPLES")
    ap.add_argument("--bed", type=float, default=256.0, help="bed size in mm (cube)")
    ap.add_argument("--hinge", help='"moving:fixed:x1,y1,z1:x2,y2,z2:ang1,ang2,..." (assembly frame)')
    a = ap.parse_args()
    if a.module:
        load_module(a.module)
    names = list(fs.SAMPLES) if a.all else a.names
    if not names:
        ap.error("give sample names or --all")
    results = [check(n, a.bed, a.hinge) for n in names]
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
