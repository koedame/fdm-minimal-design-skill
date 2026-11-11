"""
An interactive 3D viewer for a design, as one HTML file that opens offline in any browser.

  python viewer.py 06_radio --out viewers
  python viewer.py --all --out viewers
  python viewer.py pen_cup --module template_new_object.py --out viewers

The page shows the assembled design in its part colours and every part laid out in its print
orientation, with part visibility, an exploded view, the overall dimensions and a parts table
(colour, quantity, print orientation, print size). three.js, its licence and the meshes are embedded,
so the file reads nothing else: it can be sent as it is and opened with a double click.

The page is viewer/page.html around viewer/fdm-viewer.js (the 3D view on its own,
usable in other pages through FDMViewer.create) and viewer/three.min.js.
"""
import argparse
import base64
import importlib.util
import json
import os
import re
import struct
import sys
from array import array
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadquery as cq                      # noqa: E402
from OCP.Bnd import Bnd_Box               # noqa: E402
from OCP.BRepBndLib import BRepBndLib     # noqa: E402
from OCP.BRepGProp import BRepGProp       # noqa: E402
from OCP.GProp import GProp_GProps        # noqa: E402
import fdm_samples as fs                  # noqa: E402
from render import VIEWS, DEFAULT_VIEW    # noqa: E402

VIEWER_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "viewer")
TOLERANCE = 0.05        # mm, mesh deviation from the true surface
ANGULAR_TOLERANCE = 0.2  # rad
LAYOUT_GAP = 12.0       # mm between parts in the print layout (grid 4)

# The face of the assembled part (front is -Y, Z up in use) that lies on the bed.
DOWN = {
    (0, 0, -1): "As used, base on the bed",
    (0, 0, 1): "Upside down, top on the bed",
    (0, -1, 0): "Front face on the bed",
    (0, 1, 0): "Back face on the bed",
    (-1, 0, 0): "Left side on the bed",
    (1, 0, 0): "Right side on the bed",
}


def load_module(path):
    spec = importlib.util.spec_from_file_location("user_designs", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)           # the module registers its designs in fs.SAMPLES


def shape_of(wp):
    return cq.Compound.makeCompound(wp.vals()) if isinstance(wp, cq.Workplane) else wp


def bbox(shape):
    """Tight box from the exact geometry (Shape.BoundingBox grows once the shape has been meshed)."""
    b = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape.wrapped, b, False, False)
    x0, y0, z0, x1, y1, z1 = b.Get()
    return (x0, y0, z0), (x1, y1, z1)


def mass_props(shape):
    """Centre of mass and the inertia matrix about it (3x3), for matching orientations."""
    g = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape.wrapped, g)
    c = g.CentreOfMass()
    m = g.MatrixOfInertia()
    return (c.X(), c.Y(), c.Z()), [[m.Value(i, j) for j in (1, 2, 3)] for i in (1, 2, 3)]


def orientation(part):
    """Name the face of the assembled part that lies on the bed when it is printed.

    The face is the axis direction d of the assembly frame for which the print-oriented shape stands
    exactly as the assembled one would standing on d: the same height, the same height of the centre
    of mass and the same moment of inertia about the vertical. A turn about the vertical (a part laid
    at an angle on the bed) does not change these, so it does not matter. The first match in the
    order of DOWN wins, so a part symmetric about its middle reads "as used".
    """
    a, p = shape_of(part.asm), shape_of(part.prn)
    if part.qty > 1 and len(a.Solids()) == part.qty:
        a = a.Solids()[0]                    # the assembly holds every copy, the print shape one
    (amin, amax), (pmin, pmax) = bbox(a), bbox(p)
    ca, ia = mass_props(a)
    cp, ip = mass_props(p)
    height_p, com_p, izz_p = pmax[2] - pmin[2], cp[2] - pmin[2], ip[2][2]
    for d, label in DOWN.items():
        k = next(i for i in range(3) if d[i])
        height = amax[k] - amin[k]
        com = ca[k] - amin[k] if d[k] < 0 else amax[k] - ca[k]
        if (abs(height - height_p) < 0.01 and abs(com - com_p) < 0.01
                and abs(ia[k][k] - izz_p) <= 1e-6 * max(abs(izz_p), 1e-9)):
            return label
    return "Tilted for printing"


def tessellate(shape, tolerance, angular):
    """Positions (float32) and triangle indices of a shape's mesh. Vertices are per CAD face."""
    verts, tris = shape.tessellate(tolerance, angular)
    pos = array("f", (c for v in verts for c in (v.x, v.y, v.z)))
    idx = array("H" if len(verts) < 65536 else "I", (i for t in tris for i in t))
    return pos, idx


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_color(rgb):
    return "#" + "".join(f"{round(c * 255):02x}" for c in rgb)


def glb(groups, materials):
    """A binary glTF 2.0 file.

    groups: [(group_name, [(node_name, material_index, positions, indices, translation), ...]), ...]
    materials: [(name, srgb_rgb), ...]
    """
    blob = bytearray()
    views, accessors, meshes, nodes, roots = [], [], [], [], []

    def view(data, target):
        while len(blob) % 4:
            blob.append(0)
        views.append({"buffer": 0, "byteOffset": len(blob), "byteLength": len(data), "target": target})
        blob.extend(data)
        return len(views) - 1

    for gname, items in groups:
        children = []
        for name, mat, pos, idx, translation in items:
            n = len(pos) // 3
            lo = [min(pos[i::3]) for i in range(3)]
            hi = [max(pos[i::3]) for i in range(3)]
            accessors.append({"bufferView": view(pos.tobytes(), 34962), "componentType": 5126,
                              "count": n, "type": "VEC3", "min": lo, "max": hi})
            accessors.append({"bufferView": view(idx.tobytes(), 34963),
                              "componentType": 5123 if idx.typecode == "H" else 5125,
                              "count": len(idx), "type": "SCALAR"})
            meshes.append({"name": name, "primitives": [
                {"attributes": {"POSITION": len(accessors) - 2}, "indices": len(accessors) - 1, "material": mat}]})
            nodes.append({"name": name, "mesh": len(meshes) - 1, "translation": list(translation),
                          "extras": {"part": name}})   # three.js renames the second "body" to "body_1"
            children.append(len(nodes) - 1)
        nodes.append({"name": gname, "children": children})
        roots.append(len(nodes) - 1)

    doc = {
        "asset": {"version": "2.0", "generator": "fdm-minimal-design viewer.py"},
        "scene": 0, "scenes": [{"nodes": roots}], "nodes": nodes, "meshes": meshes,
        "materials": [{"name": n, "pbrMetallicRoughness": {
            "baseColorFactor": [srgb_to_linear(c) for c in rgb] + [1.0], "metallicFactor": 0.0,
            "roughnessFactor": 0.7}} for n, rgb in materials],
        "accessors": accessors, "bufferViews": views, "buffers": [{"byteLength": len(blob)}],
    }
    js = json.dumps(doc, separators=(",", ":")).encode()
    js += b" " * (-len(js) % 4)
    blob.extend(b"\0" * (-len(blob) % 4))
    return (struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(blob))
            + struct.pack("<II", len(js), 0x4E4F534A) + js
            + struct.pack("<II", len(blob), 0x004E4942) + bytes(blob))


def layout(slots):
    """Place boxes (w, d, h) in rows on the bed plane, centred on the origin; returns each box's (x, y).

    The tallest parts go first: to the back row and, within a row, to the left. Rows are aligned on
    their front edge, with room in front of each row for the labels of the page. Seen from the front
    right, nothing hides behind a taller part.
    """
    order = sorted(range(len(slots)), key=lambda i: -slots[i][2])
    area = sum((w + LAYOUT_GAP) * (d + LAYOUT_GAP) for w, d, _ in slots)
    row_w = max(max(w for w, _, _ in slots), (area ** 0.5) * 1.2)
    row_gap = max(LAYOUT_GAP, 0.15 * row_w)
    rows, x = [[]], 0.0
    for i in order:
        if rows[-1] and x + slots[i][0] > row_w:
            rows.append([])
            x = 0.0
        rows[-1].append((i, x))
        x += slots[i][0] + LAYOUT_GAP
    at, y = {}, 0.0
    for row in rows:                     # from the back (+Y) to the front
        y -= max(slots[i][1] for i, _ in row)
        for i, x in row:
            at[i] = (x, y)
        y -= row_gap
    x0 = min(at[i][0] for i in at)
    x1 = max(at[i][0] + slots[i][0] for i in at)
    y0 = min(at[i][1] for i in at)
    y1 = max(at[i][1] + slots[i][1] for i in at)
    return [(at[i][0] - (x0 + x1) / 2, at[i][1] - (y0 + y1) / 2) for i in range(len(slots))]


def model(name, tolerance=TOLERANCE, angular=ANGULAR_TOLERANCE):
    """The data and the GLB for one design: (data dict, glb bytes)."""
    parts = fs.SAMPLES[name]()
    # print-oriented shapes sit on z=0 from their own box, inlays (anchor) share their parent's shift,
    # as in fdm_samples.export
    shifts, prn = {}, {}
    for pname, p in parts.items():
        s = shape_of(p.prn)
        (x0, y0, z0), _ = bbox(s)
        shifts[pname] = shifts[p.anchor] if p.anchor else (-x0, -y0, -z0)
        prn[pname] = s.translate(cq.Vector(*shifts[pname]))
    roots = [n for n, p in parts.items() if not p.anchor]
    group_of = {n: (parts[n].anchor if parts[n].anchor else n) for n in parts}
    while any(g not in roots for g in group_of.values()):     # inlay of an inlay
        group_of = {n: group_of[g] if g not in roots else g for n, g in group_of.items()}
    extents = {}
    for r in roots:
        boxes = [bbox(prn[n]) for n in parts if group_of[n] == r]
        extents[r] = tuple(max(b[1][k] for b in boxes) for k in range(3))
    places = dict(zip(roots, layout([extents[r] for r in roots])))

    materials, assembled, printed, info = [], [], [], []
    lo, hi = [float("inf")] * 3, [float("-inf")] * 3
    for i, (pname, p) in enumerate(parts.items()):
        a = shape_of(p.asm)
        amin, amax = bbox(a)
        lo = [min(u, v) for u, v in zip(lo, amin)]
        hi = [max(u, v) for u, v in zip(hi, amax)]
        materials.append((pname, p.color))
        assembled.append((pname, i, *tessellate(a, tolerance, angular), (0.0, 0.0, 0.0)))
        x, y = places[group_of[pname]]
        printed.append((pname, i, *tessellate(prn[pname], tolerance, angular), (x, y, 0.0)))
        pmin, pmax = bbox(prn[pname])
        info.append({"name": pname, "color": hex_color(p.color), "qty": p.qty, "anchor": p.anchor,
                     "orientation": orientation(p),
                     "print_size": [round(h - l, 1) for l, h in zip(pmin, pmax)]})
    view, zoom = VIEWS.get(name, DEFAULT_VIEW)
    data = {"name": name, "size": [round(h - l, 1) for l, h in zip(lo, hi)], "tolerance": tolerance,
            "view": list(view), "zoom": zoom, "parts": info}
    return data, glb([("assembled", assembled), ("print", printed)], materials)


def asset(name):
    with open(os.path.join(VIEWER_DIR, name), encoding="utf-8") as f:
        return f.read()


def page(data, glb_bytes):
    """The HTML page: page.html with three.js, fdm-viewer.js, the data and the GLB filled in."""
    html = asset("page.html")
    script = lambda s: s.replace("</script", "<\\/script")            # noqa: E731
    fill = {
        "__TITLE__": escape(data["name"].replace("_", " ")),
        "/*THREE*/": script(asset("three.min.js")),
        "/*VIEWER*/": script(asset("fdm-viewer.js")),
        "/*PAGE*/": script(asset("page.js")),
        "__LICENSE__": escape(asset("three-LICENSE.txt")),
        '"__DATA__"': json.dumps(data, separators=(",", ":")).replace("<", "\\u003c"),
        '"__GLB__"': json.dumps(base64.b64encode(glb_bytes).decode()),
    }
    missing = [k for k in fill if k not in html]
    if missing:
        raise SystemExit(f"page.html has no {missing}")
    # one pass, so a marker inside the filled-in code is left alone
    return re.sub("|".join(map(re.escape, fill)), lambda m: fill[m.group(0)], html)


def write(name, out_dir, tolerance=TOLERANCE, angular=ANGULAR_TOLERANCE):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{name}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(page(*model(name, tolerance, angular)))
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument("names", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--module", help="python file that registers extra designs in fdm_samples.SAMPLES")
    ap.add_argument("--out", default="viewers", help="output directory, one <name>.html per design")
    ap.add_argument("--tolerance", type=float, default=TOLERANCE,
                    help=f"mesh deviation in mm (default {TOLERANCE}); larger gives a smaller file")
    a = ap.parse_args()
    if a.module:
        load_module(a.module)
    names = list(fs.SAMPLES) if a.all else a.names
    if not names:
        ap.error("give design names or --all")
    for n in names:
        p = write(n, a.out, a.tolerance)
        print(f"wrote {p} ({os.path.getsize(p) / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
