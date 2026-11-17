// FDMDimensions: the dimensions drawn over the 3D view, on an <svg> that covers the view's container.
//
//   const dims = FDMDimensions.attach(viewer, { svg, parts, on: true });
//   dims.setOn(false);   // the page's switch
//
// parts is the parts list of the page data (scripts/viewer.py): { name, qty, anchor, ref, print_size }.
// Assembled, the overall box of the parts shown gets its width, depth and height, with extension lines; it is not
// drawn while exploded, since that is not the size of the object. In the print layout each printed part shown gets its
// name and print size under it; inlays (anchor) are printed with their parent and bought parts (ref) are not printed,
// so they get none. A label that would overlap one already drawn moves down.
// The overlay follows the view: it is drawn again after every frame the viewer draws, so hiding a part, exploding or
// turning the view updates it. The page styles it (lines; text, and text.sub for the print size).
(function (root) {
  "use strict";

  const SVG = "http://www.w3.org/2000/svg";
  const mm = (v) => (Math.round(v * 10) / 10).toLocaleString("en-US");
  const dims = (s) => s.map(mm).join(" × ");

  // The y of a label of width w centred at x, wanted at y: moved down past the labels already placed (taken, each
  // { x, y, w }) that it would overlap. Labels are `step` high.
  function stack(taken, x, y, w, step = 30) {
    while (taken.some((r) => Math.abs(r.x - x) < (r.w + w) / 2 && Math.abs(r.y - y) < step)) y += step;
    return y;
  }

  function attach(viewer, { svg, parts, on = true }) {
    const add = (tag, attrs, text) => {
      const e = document.createElementNS(SVG, tag);
      for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
      if (text !== undefined) e.textContent = text;
      svg.append(e);
      return e;
    };
    const line = (a, b) => add("line", { x1: a.x, y1: a.y, x2: b.x, y2: b.y });
    const label = (p, text, cls) => add("text", { x: p.x, y: p.y, "text-anchor": "middle", "dominant-baseline": "middle", class: cls || "" }, text);

    // one dimension: the edge a-b moved outward by `off`, with extension lines and the length in the middle
    function dimension(a, b, off) {
      const pa = a.map((v, i) => v + off[i]), pb = b.map((v, i) => v + off[i]);
      const [sa, sb, ea, eb] = [pa, pb, a, b].map((v) => viewer.toScreen(v));
      if ([sa, sb].some((s) => s.behind)) return;
      line(ea, sa);
      line(eb, sb);
      line(sa, sb);
      const len = Math.hypot(...a.map((v, i) => b[i] - v));
      label({ x: (sa.x + sb.x) / 2, y: (sa.y + sb.y) / 2 }, mm(len));
    }

    function draw() {
      svg.replaceChildren();
      if (!on) return;
      if (viewer.arrangement === "assembled") {
        if (viewer.explode > 0 || !viewer.parts.some((n) => viewer.visible(n))) return;
        const { min: [x0, y0, z0], max: [x1, y1, z1] } = viewer.box();
        const o = Math.max(x1 - x0, y1 - y0, z1 - z0) * 0.06;
        dimension([x0, y0, z0], [x1, y0, z0], [0, -o, 0]); // width along the front
        dimension([x1, y0, z0], [x1, y1, z0], [o, 0, 0]); // depth along the right side
        dimension([x0, y0, z0], [x0, y0, z1], [-o, -o, 0]); // height at the front left corner
      } else {
        const taken = [];
        for (const p of parts) {
          if (!viewer.visible(p.name) || p.anchor || p.ref) continue;
          const { min: [x0, y0, z0], max: [x1] } = viewer.box(p.name);
          const s = viewer.toScreen([(x0 + x1) / 2, y0, z0]);
          if (s.behind) continue;
          const name = label({ x: s.x, y: s.y + 12 }, p.name.replace(/_/g, " ") + (p.qty > 1 ? ` ×${p.qty}` : ""));
          const size = label({ x: s.x, y: s.y + 26 }, dims(p.print_size), "sub");
          const w = Math.max(name.getBBox().width, size.getBBox().width) + 8;
          const y = stack(taken, s.x, s.y + 4, w);
          taken.push({ x: s.x, y, w });
          name.setAttribute("y", y + 8);
          size.setAttribute("y", y + 22);
        }
      }
    }
    viewer.onRender(draw);
    draw();
    return {
      setOn(v) {
        on = Boolean(v);
        draw();
      },
    };
  }

  root.FDMDimensions = { attach, stack };
})(typeof window !== "undefined" ? window : globalThis);
