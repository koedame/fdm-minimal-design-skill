// The page written by tools/build_site.py: opens a model from the list in a dialog with its 3D view.
// SITE (models in page order, sample titles) is defined inline by the page. The 3D view is the one of
// scripts/viewer.py (viewer/fdm-viewer.js on viewer/three.min.js); both are loaded the first time a model
// is opened, and each model's meshes (models/<id>/model.glb) when it is opened. Everything is read from
// this site. The model shown follows the address (#<id>), so a model can be linked to and Back closes it.
(() => {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const byId = new Map(SITE.models.map((m, i) => [m.id, i]));
  const dialog = $("model");
  const mm = (v) => (Math.round(v * 10) / 10).toLocaleString("en-US");
  const dims = (s) => s.map(mm).join(" × ");
  const bytes = (n) => (n >= 1e6 ? `${(n / 1e6).toFixed(1)} MB` : `${Math.max(1, Math.round(n / 1e3))} kB`);
  const words = (s) => s.replace(/_/g, " ");
  // two squares, the front one see-through: the button that makes a part transparent
  const SEE_ICON = '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><rect x="1.5" y="1.5" width="9" height="9" rx="1.5" fill="none" stroke="currentColor"/><rect x="5.5" y="5.5" width="9" height="9" rx="1.5" fill="currentColor" fill-opacity="0.25" stroke="currentColor"/></svg>';

  let viewerLoaded = null; // the promise of the two scripts, made once
  const loadScript = (src) => new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = src;
    s.onload = resolve;
    s.onerror = () => reject(new Error(`could not load ${src}`));
    document.head.append(s);
  });
  const loadViewer = () => (viewerLoaded ||= loadScript("viewer/three.min.js")
    .then(() => loadScript("viewer/fdm-viewer.js"))
    .catch((e) => {
      viewerLoaded = null; // try again on the next opening
      throw e;
    }));

  let viewer = null; // the 3D view of the open model; one at a time, so only one WebGL context exists
  let shown = null; // id of the open model
  let opening = 0; // counts openings, so a slow load that was overtaken does not show up
  let pushed = false; // the dialog was opened from the list in this visit (then Close goes Back)
  let partRows = []; // the rows of the parts table of the open model: { name, show (checkbox), see (button), tr }

  function fill(m) {
    $("m-num").textContent = m.number;
    $("m-title").textContent = m.title;
    $("m-summary").textContent = m.summary;
    const meta = [`${dims(m.size)} mm`, `${m.parts.length} part${m.parts.length > 1 ? "s" : ""}`];
    if (m.based_on.length) meta.push(`based on ${m.based_on.map((s) => SITE.sample_titles[s] || words(s)).join(", ")}`);
    if (m.mechanisms.length) meta.push(m.mechanisms.join(", ").toLowerCase());
    meta.push(m.printed ? "printed and checked" : "not printed yet");
    $("m-meta").textContent = meta.join(" · ");

    // each row shows or hides its part (the checkbox) and makes it transparent (the button); a new model starts
    // with every part shown and opaque, as the rows are made again
    partRows = m.parts.map((p) => {
      const tr = document.createElement("tr");
      tr.innerHTML = '<td><span class="part"><label><input type="checkbox" checked><span class="sw"></span><span><b></b><br><span class="muted"></span></span></label>'
        + `<button type="button" class="see" aria-pressed="false" title="Transparent">${SEE_ICON}</button></span></td><td class="n"></td><td class="n"></td>`;
      tr.querySelector(".sw").style.background = p.color;
      tr.querySelector("b").textContent = words(p.name);
      tr.querySelector(".muted").textContent = p.anchor ? `${p.orientation}, printed with ${words(p.anchor)}` : p.orientation;
      tr.cells[1].textContent = String(p.qty);
      tr.cells[2].textContent = p.print_size ? dims(p.print_size) : "—"; // a bought part is not printed
      const row = { name: p.name, show: tr.querySelector("input"), see: tr.querySelector(".see"), tr };
      row.show.setAttribute("aria-label", `Show ${words(p.name)}`);
      row.see.setAttribute("aria-label", `Transparent ${words(p.name)}`);
      row.show.addEventListener("change", () => applyPart(row));
      row.see.addEventListener("click", () => {
        row.see.setAttribute("aria-pressed", String(row.see.getAttribute("aria-pressed") !== "true"));
        applyPart(row);
      });
      return row;
    });
    $("m-parts").replaceChildren(...partRows.map((r) => r.tr));

    const labels = { step: "STEP assembly", stl: "STL for printing (zip)", viewer: "3D viewer (HTML, works offline)" };
    const items = Object.entries(labels).map(([k, label]) => {
      const d = m.downloads[k];
      const li = document.createElement("li");
      li.innerHTML = '<a download></a><span class="muted"></span>';
      li.firstChild.href = `models/${m.id}/${d.file}`;
      li.firstChild.textContent = label;
      li.lastChild.textContent = bytes(d.bytes);
      return li;
    });
    $("m-downloads").replaceChildren(...items);
    $("m-safety").hidden = !m.safety.length;
    $("m-safety-notes").replaceChildren(...m.safety.map((text) => {
      const p = document.createElement("p");
      p.textContent = text;
      return p;
    }));
    $("m-credit").textContent = `${m.title} from fdm-minimal-design by koedame, CC BY 4.0`;
  }

  // the row's state is the state of the part: drawn on the row, and given to the 3D view once it is there
  function applyPart(row) {
    const see = row.see.getAttribute("aria-pressed") === "true";
    row.tr.classList.toggle("off", !row.show.checked);
    row.tr.classList.toggle("clear", see);
    if (!viewer) return;
    viewer.setVisible(row.name, row.show.checked);
    viewer.setTransparent(row.name, see);
  }

  function setControls(arrangement) {
    document.querySelectorAll("#arrangement button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.v === arrangement)));
    $("explode").disabled = arrangement === "print";
    $("explode-row").classList.toggle("off", arrangement === "print");
  }

  async function show(id) {
    const m = SITE.models[byId.get(id)];
    const n = ++opening;
    shown = id;
    if (viewer) viewer.dispose();
    viewer = null;
    fill(m);
    setControls("assembled");
    $("explode").value = "0";
    const stage = $("stage");
    stage.style.backgroundImage = `url("models/${m.id}/thumb.webp")`; // until the 3D view is ready
    $("status").textContent = "Loading…";
    if (!dialog.open) dialog.showModal();
    try {
      const [glb] = await Promise.all([
        fetch(`models/${m.id}/model.glb`).then((r) => {
          if (!r.ok) throw new Error(`model.glb: HTTP ${r.status}`);
          return r.arrayBuffer();
        }),
        loadViewer(),
      ]);
      if (n !== opening) return;
      const v = await FDMViewer.create(stage, {
        glb, view: m.view, zoom: m.zoom, background: "#f6f6f4",
        anchors: Object.fromEntries(m.parts.filter((p) => p.anchor).map((p) => [p.name, p.anchor])),
      });
      if (n !== opening) return v.dispose();
      viewer = v;
      partRows.forEach(applyPart); // what was changed while the model was loading
      stage.style.backgroundImage = "";
      $("status").textContent = "";
    } catch (e) {
      if (n === opening) $("status").textContent = `The 3D view could not start (${e.message}).`;
    }
  }

  function hide() {
    opening++;
    shown = null;
    if (viewer) viewer.dispose();
    viewer = null;
    if (dialog.open) dialog.close();
  }

  // the address decides what is shown
  const route = () => {
    let id = "";
    try {
      id = decodeURIComponent(location.hash.slice(1));
    } catch { /* not an id */ }
    if (byId.has(id)) {
      if (id !== shown) show(id);
    } else if (shown) {
      hide();
    }
  };
  window.addEventListener("hashchange", route);

  document.addEventListener("click", (e) => {
    const a = e.target.closest("a.card");
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
    pushed = true; // the link itself changes the address
  });
  const close = () => {
    if (pushed) {
      pushed = false;
      history.back();
    } else {
      history.replaceState(null, "", location.pathname + location.search);
      route();
    }
  };
  $("close").addEventListener("click", close);
  dialog.addEventListener("cancel", (e) => { // Esc
    e.preventDefault();
    close();
  });
  const step = (d) => {
    const i = (byId.get(shown) + d + SITE.models.length) % SITE.models.length;
    history.replaceState(null, "", `#${SITE.models[i].id}`);
    route();
  };
  $("prev").addEventListener("click", () => step(-1));
  $("next").addEventListener("click", () => step(1));
  dialog.addEventListener("keydown", (e) => {
    // Alt+Left is Back; on the parts table the arrows would leave the model being taken apart
    if (e.target.closest("input, #m-parts") || e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return;
    if (e.key === "ArrowLeft") step(-1);
    if (e.key === "ArrowRight") step(1);
  });

  document.querySelectorAll("#arrangement button").forEach((b) => b.addEventListener("click", () => {
    if (!viewer) return;
    viewer.setArrangement(b.dataset.v);
    setControls(b.dataset.v);
  }));
  $("explode").addEventListener("input", (e) => viewer && viewer.setExplode(Number(e.target.value)));
  $("reset").addEventListener("click", () => viewer && viewer.resetView());
  $("parts-all").addEventListener("click", () => partRows.forEach((row) => {
    row.show.checked = true;
    row.see.setAttribute("aria-pressed", "false");
    applyPart(row);
  }));

  route();
})();
