"""
Preview images of assembled designs (references/04_review.md, Step 5). Uses VTK off-screen.

  python render.py 06_radio --out previews
  python render.py --all --out previews --sheet overview.png
  python render.py my_lamp --module template_new_object.py --view -0.6 -1 0.5
  python render.py my_lamp --module template_new_object.py --view -0.6 -1 0.5 1.1

The camera looks at the design from the direction given (x, y, z from the object), from VIEWS for the
samples, or from "view" in a model.json next to the --module file ({"direction": [x, y, z], "zoom": z}).
Without a zoom the design is framed so that it fills 90 % of the image in its tighter direction,
whatever its proportions.

The images are for checking proportions, alignment lines, the single accent and seam lines.
They are not proof of quality; judge gaps and edges on a real print.
"""
import argparse
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadquery as cq                      # noqa: E402
import fdm_samples as fs                  # noqa: E402

VIEWS = {  # camera direction from the object, zoom
    "01_clock": ((-0.45, -1.0, 0.3), 1.1), "02_remote": ((-0.6, -0.9, 1.1), 1.3),
    "03_tray": ((-0.6, -1.0, 0.9), 1.25), "04_cylinder_speaker": ((-0.7, -1.0, 0.45), 0.95),
    "05_stand": ((-1.0, -0.85, 0.5), 1.1), "06_radio": ((-0.45, -1.0, 0.45), 1.15),
    "07_hinged_case": ((-0.6, -1.0, 0.8), 1.2), "08_power_bank": ((-0.9, -1.0, 0.9), 1.25),
    "09_wall_unit": ((-0.45, -1.0, 0.35), 1.15), "10_lantern": ((0.75, -1.0, 0.45), 1.05),
    "11_split_riser": ((-0.7, -1.0, 0.55), 1.2), "12_threaded_jar": ((-0.6, -1.0, 0.55), 1.15),
}
DEFAULT_VIEW = ((-0.6, -1.0, 0.6), None)   # None: frame the design (fit)
FILL = 0.9


def meta_view(meta):
    """(direction, zoom) from the "view" of a model.json, or None."""
    v = meta.get("view")
    return (tuple(v["direction"]), v.get("zoom")) if v else None


def fit(ren, points, aspect, fill=FILL):
    """Zoom the camera so the points fill `fill` of the image in its tighter direction."""
    import numpy as np
    cam = ren.GetActiveCamera()
    for _ in range(3):                         # perspective: the zoom is not exactly linear, settle it
        m = cam.GetCompositeProjectionTransformMatrix(aspect, -1, 1)
        mat = np.array([[m.GetElement(i, j) for j in range(4)] for i in range(4)])
        q = points @ mat[:, :3].T + mat[:, 3]
        reach = np.abs(q[:, :2] / q[:, 3:4]).max()
        cam.Zoom(fill / reach)


def render(name, out_png, view=None, size=(1000, 800)):
    import numpy as np
    import vtk
    from vtk.util.numpy_support import vtk_to_numpy
    parts = fs.SAMPLES[name]()
    d, zoom = view or VIEWS.get(name, DEFAULT_VIEW)
    ren = vtk.vtkRenderer()
    ren.SetBackground(0.97, 0.97, 0.96)
    points = []
    with tempfile.TemporaryDirectory() as tmp:
        for n, p in parts.items():
            f = os.path.join(tmp, f"{n}.stl")
            cq.exporters.export(p.asm, f, tolerance=0.02, angularTolerance=0.1)
            r = vtk.vtkSTLReader()
            r.SetFileName(f)
            r.Update()
            points.append(vtk_to_numpy(r.GetOutput().GetPoints().GetData()))
            nm = vtk.vtkPolyDataNormals()
            nm.SetInputConnection(r.GetOutputPort())
            nm.SetFeatureAngle(35)
            m = vtk.vtkPolyDataMapper()
            m.SetInputConnection(nm.GetOutputPort())
            a = vtk.vtkActor()
            a.SetMapper(m)
            pr = a.GetProperty()
            pr.SetColor(*p.color)
            pr.SetAmbient(0.25)
            pr.SetDiffuse(0.75)
            pr.SetSpecular(0.08)
            pr.SetSpecularPower(20)
            ren.AddActor(a)
        ren.ResetCamera()
        cam = ren.GetActiveCamera()
        fp = cam.GetFocalPoint()
        cam.SetPosition(fp[0] + d[0] * 500, fp[1] + d[1] * 500, fp[2] + d[2] * 500)
        cam.SetViewUp(0, 0, 1)
        cam.SetViewAngle(25)
        ren.ResetCamera()
        if zoom:
            cam.Zoom(zoom)
        else:
            fit(ren, np.concatenate(points).astype(float), size[0] / size[1])
        for pos, inten in (((-300, -500, 600), 0.9), ((400, -200, 200), 0.35)):
            l = vtk.vtkLight()
            l.SetPosition(*pos)
            l.SetFocalPoint(0, 0, 0)
            l.SetIntensity(inten)
            ren.AddLight(l)
        w = vtk.vtkRenderWindow()
        w.SetOffScreenRendering(1)
        w.AddRenderer(ren)
        w.SetSize(*size)
        w.SetMultiSamples(8)
        w.Render()
        g = vtk.vtkWindowToImageFilter()
        g.SetInput(w)
        g.Update()
        png = vtk.vtkPNGWriter()
        png.SetFileName(out_png)
        png.SetInputConnection(g.GetOutputPort())
        png.Write()
    return out_png


def contact_sheet(pngs, names, out, cols=4):
    cols = max(1, min(cols, len(pngs)))
    from PIL import Image, ImageDraw, ImageFont
    ims = [Image.open(p) for p in pngs]
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (w * cols, h * rows), (247, 247, 245))
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 36)
    except OSError:
        font = ImageFont.load_default()
    dr = ImageDraw.Draw(sheet)
    for i, (im, n) in enumerate(zip(ims, names)):
        x, y = (i % cols) * w, (i // cols) * h
        sheet.paste(im, (x, y))
        dr.text((x + 30, y + 24), n.replace("_", " "), fill=(110, 110, 105), font=font)
    sheet.resize((w * cols // 2, h * rows // 2)).save(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--module", help="python file that registers extra designs in fdm_samples.SAMPLES "
                    "(the view of a model.json next to it is used)")
    ap.add_argument("--out", default="previews")
    ap.add_argument("--view", nargs="+", type=float, metavar="V",
                    help="camera direction x y z from the object, and optionally a zoom (default: fit)")
    ap.add_argument("--sheet", help="also write a contact sheet PNG")
    a = ap.parse_args()
    meta = fs.load_module(a.module) if a.module else {}
    names = list(fs.SAMPLES) if a.all else a.names
    if not names:
        ap.error("give sample names or --all")
    if a.view and len(a.view) not in (3, 4):
        ap.error("--view takes x y z and an optional zoom")
    view = (tuple(a.view[:3]), a.view[3] if len(a.view) > 3 else None) if a.view else None
    os.makedirs(a.out, exist_ok=True)
    pngs = [render(n, os.path.join(a.out, f"{n}.png"), view or (meta_view(meta) if n == meta.get("id") else None))
            for n in names]
    for p in pngs:
        print("wrote", p)
    if a.sheet:
        contact_sheet(pngs, names, a.sheet)
        print("wrote", a.sheet)


if __name__ == "__main__":
    main()
