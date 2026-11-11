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

  function fill(m) {
    $("m-num").textContent = m.number;
    $("m-title").textContent = m.title;
    $("m-summary").textContent = m.summary;
    const meta = [`${dims(m.size)} mm`, `${m.parts.length} part${m.parts.length > 1 ? "s" : ""}`];
    if (m.based_on.length) meta.push(`based on ${m.based_on.map((s) => SITE.sample_titles[s] || words(s)).join(", ")}`);
    if (m.mechanisms.length) meta.push(m.mechanisms.join(", ").toLowerCase());
    meta.push(m.printed ? "printed and checked" : "not printed yet");
    $("m-meta").textContent = meta.join(" · ");

    const rows = m.parts.map((p) => {
      const tr = document.createElement("tr");
      tr.innerHTML = '<td><span class="part"><span class="sw"></span><span><b></b><br><span class="muted"></span></span></span></td><td class="n"></td><td class="n"></td>';
      tr.querySelector(".sw").style.background = p.color;
      tr.querySelector("b").textContent = words(p.name);
      tr.querySelector(".muted").textContent = p.anchor ? `${p.orientation}, printed with ${words(p.anchor)}` : p.orientation;
      tr.cells[1].textContent = String(p.qty);
      tr.cells[2].textContent = p.print_size ? dims(p.print_size) : "—"; // a bought part is not printed
      return tr;
    });
    $("m-parts").replaceChildren(...rows);

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
    $("m-credit").textContent = `${m.title} from fdm-minimal-design by koedame, CC BY 4.0`;
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
    if (e.target.matches("input") || e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return; // Alt+Left is Back
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

  route();
})();
