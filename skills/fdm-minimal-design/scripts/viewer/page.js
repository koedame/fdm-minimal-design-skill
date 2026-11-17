// The page around FDMViewer (page.html): the panel and the parts table, with the part menu (part-menu.js) and the
// dimensions (dimensions.js) on the view.
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
  $("explode").addEventListener("input", (e) => viewer.setExplode(Number(e.target.value)));
  $("edges").addEventListener("change", (e) => viewer.setEdges(e.target.checked));
  $("reset").addEventListener("click", () => viewer.resetView());

  // ---- parts table: each row shows or hides its part (the checkbox) and makes it transparent (the button) ----
  // two squares, the front one see-through
  const SEE_ICON = '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><rect x="1.5" y="1.5" width="9" height="9" rx="1.5" fill="none" stroke="currentColor"/><rect x="5.5" y="5.5" width="9" height="9" rx="1.5" fill="currentColor" fill-opacity="0.25" stroke="currentColor"/></svg>';
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
    const row = { name: p.name, label: words, color: p.color, show: tr.querySelector("input"), see: tr.querySelector(".see"), tr };
    row.show.setAttribute("aria-label", `Show ${words}`);
    row.see.setAttribute("aria-label", `Transparent ${words}`);
    row.show.addEventListener("change", () => applyPart(row));
    row.see.addEventListener("click", () => {
      row.see.setAttribute("aria-pressed", String(row.see.getAttribute("aria-pressed") !== "true"));
      applyPart(row);
    });
    rows.push(row);
    $("parts").append(tr);
  }
  $("all").addEventListener("click", () => {
    for (const row of rows) {
      row.show.checked = true;
      row.see.setAttribute("aria-pressed", "false");
      applyPart(row);
    }
  });
  // clicking a part in the view opens its menu, which works the controls of its row
  FDMPartMenu.attach(viewer, { container: $("view"), rows, showAll: $("all") });
  // the dimensions follow the view and the parts shown (they are drawn again after every frame)
  const dimensions = FDMDimensions.attach(viewer, { svg: $("overlay"), parts: DATA.parts, on: $("dims").checked });
  $("dims").addEventListener("change", (e) => dimensions.setOn(e.target.checked));

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

})();
