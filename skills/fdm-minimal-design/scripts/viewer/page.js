// The page around FDMViewer (page.html): the panel, the parts table and the dimension overlay.
// DATA (from scripts/viewer.py) and GLB (base64) are defined by the page before this script.
(async () => {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const mm = (v) => (Math.round(v * 10) / 10).toLocaleString("en-US");
  const dims = (s) => s.map(mm).join(" × ");
  const store = {
    get: (k) => { try { return localStorage.getItem(k); } catch { return null; } },
    set: (k, v) => { try { localStorage.setItem(k, v); } catch { /* storage off (file:// in some browsers) */ } },
  };

  $("size").textContent = `${dims(DATA.size)} mm · ${DATA.parts.length} part${DATA.parts.length > 1 ? "s" : ""}`;
  $("tol").textContent = String(DATA.tolerance);

  let viewer;
  try {
    viewer = await FDMViewer.create($("view"), {
      glb: FDMViewer.decode(GLB), view: DATA.view, zoom: DATA.zoom,
      anchors: Object.fromEntries(DATA.parts.filter((p) => p.anchor).map((p) => [p.name, p.anchor])),
    });
    $("status").textContent = "";
  } catch (e) {
    $("status").textContent = `The 3D view could not start (${e.message}). WebGL may be turned off in this browser.`;
    return;
  }

  // ---- arrangement, explode, edges ----
  const pressed = (group, v) => document.querySelectorAll(`#${group} button`).forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.v === v)));
  document.querySelectorAll("#arrangement button").forEach((b) => b.addEventListener("click", () => {
    viewer.setArrangement(b.dataset.v);
    pressed("arrangement", b.dataset.v);
    const print = b.dataset.v === "print";
    $("explode").disabled = print;
    $("explode-row").classList.toggle("off", print);
  }));
  $("explode").addEventListener("input", (e) => viewer.setExplode(Number(e.target.value))); // redraws the overlay
  $("edges").addEventListener("change", (e) => viewer.setEdges(e.target.checked));
  $("dims").addEventListener("change", () => drawOverlay());
  $("reset").addEventListener("click", () => viewer.resetView());

  // ---- parts table: each row shows or hides its part (the checkbox) and makes it transparent (the button) ----
  // two squares, the front one see-through
  const SEE_ICON = '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><rect x="1.5" y="1.5" width="9" height="9" rx="1.5" fill="none" stroke="currentColor"/><rect x="5.5" y="5.5" width="9" height="9" rx="1.5" fill="currentColor" fill-opacity="0.25" stroke="currentColor"/></svg>';
  const boxes = {};
  const rows = [];
  const applyPart = (row) => {
    const see = row.see.getAttribute("aria-pressed") === "true";
    row.tr.classList.toggle("off", !row.show.checked);
    row.tr.classList.toggle("clear", see);
    viewer.setVisible(row.name, row.show.checked);
    viewer.setTransparent(row.name, see);
  };
  for (const p of DATA.parts) {
    const words = p.name.replace(/_/g, " ");
    const tr = document.createElement("tr");
    tr.className = "part";
    tr.innerHTML = `<td><span class="pick"><label><input type="checkbox" checked><span class="sw"></span><span><span class="name"></span><br><span class="orient"></span></span></label>`
      + `<button type="button" class="see" aria-pressed="false" title="Transparent">${SEE_ICON}</button></span></td><td class="num"></td><td class="num"></td>`;
    tr.querySelector(".sw").style.background = p.color;
    tr.querySelector(".name").textContent = words;
    tr.querySelector(".orient").textContent = p.anchor ? `${p.orientation}, printed with ${p.anchor.replace(/_/g, " ")}` : p.orientation;
    tr.cells[1].textContent = `${p.qty}`;
    tr.cells[2].textContent = p.print_size ? dims(p.print_size) : "—"; // a bought part is not printed
    const row = { name: p.name, show: tr.querySelector("input"), see: tr.querySelector(".see"), tr };
    row.show.setAttribute("aria-label", `Show ${words}`);
    row.see.setAttribute("aria-label", `Transparent ${words}`);
    row.show.addEventListener("change", () => {
      applyPart(row);
      drawOverlay();
    });
    row.see.addEventListener("click", () => {
      row.see.setAttribute("aria-pressed", String(row.see.getAttribute("aria-pressed") !== "true"));
      applyPart(row);
    });
    boxes[p.name] = row.show;
    rows.push(row);
    $("parts").append(tr);
  }
  $("all").addEventListener("click", () => {
    for (const row of rows) {
      row.show.checked = true;
      row.see.setAttribute("aria-pressed", "false");
      applyPart(row);
    }
    drawOverlay();
  });

  // ---- controls help and the two-finger scroll setting (remembered on this device) ----
  const SCROLL_KEY = "fdm-viewer.scroll";
  const TRACKPAD = {
    zoom: { rotate: "click-drag", pan: "Shift + click-drag", zoom: "pinch, two-finger scroll" },
    pan: { rotate: "click-drag, Shift + two-finger scroll", pan: "two-finger scroll", zoom: "pinch" },
  };
  const setScroll = (v) => {
    viewer.setScroll(v);
    pressed("scroll", v);
    for (const [k, text] of Object.entries(TRACKPAD[v])) $(`tp-${k}`).textContent = text;
  };
  setScroll(store.get(SCROLL_KEY) === "pan" ? "pan" : "zoom");
  document.querySelectorAll("#scroll button").forEach((b) => b.addEventListener("click", () => {
    store.set(SCROLL_KEY, b.dataset.v);
    setScroll(b.dataset.v);
  }));

  // ---- dimension overlay: overall box when assembled, name and size of each part in the print layout ----
  const SVG = "http://www.w3.org/2000/svg";
  const overlay = $("overlay");
  const add = (tag, attrs, text) => {
    const e = document.createElementNS(SVG, tag);
    for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
    if (text !== undefined) e.textContent = text;
    overlay.append(e);
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

  function drawOverlay() {
    overlay.replaceChildren();
    if (!$("dims").checked) return;
    if (viewer.arrangement === "assembled") {
      // the overall size is the size of the assembled object, so it is not drawn while exploded
      if (Number($("explode").value) > 0 || !Object.values(boxes).some((b) => b.checked)) return;
      const { min: [x0, y0, z0], max: [x1, y1, z1] } = viewer.box();
      const o = Math.max(x1 - x0, y1 - y0, z1 - z0) * 0.06;
      dimension([x0, y0, z0], [x1, y0, z0], [0, -o, 0]); // width along the front
      dimension([x1, y0, z0], [x1, y1, z0], [o, 0, 0]); // depth along the right side
      dimension([x0, y0, z0], [x0, y0, z1], [-o, -o, 0]); // height at the front left corner
    } else {
      const taken = []; // label boxes already drawn; a label that would overlap one moves down
      for (const p of DATA.parts) {
        if (!boxes[p.name].checked || p.anchor || p.ref) continue;
        const { min: [x0, y0, z0], max: [x1] } = viewer.box(p.name);
        const s = viewer.toScreen([(x0 + x1) / 2, y0, z0]);
        if (s.behind) continue;
        const name = label({ x: s.x, y: s.y + 12 }, p.name.replace(/_/g, " ") + (p.qty > 1 ? ` ×${p.qty}` : ""));
        const size = label({ x: s.x, y: s.y + 26 }, dims(p.print_size), "sub");
        const w = Math.max(name.getBBox().width, size.getBBox().width) + 8;
        let y = s.y + 4;
        while (taken.some((r) => Math.abs(r.x - s.x) < (r.w + w) / 2 && Math.abs(r.y - y) < 30)) y += 30;
        taken.push({ x: s.x, y, w });
        name.setAttribute("y", y + 8);
        size.setAttribute("y", y + 22);
      }
    }
  }
  viewer.onRender(drawOverlay);
})();
