// The page of one model (/models/<id>/, written by tools/build_site.py). Its name, parts and downloads are in the
// HTML already; this script adds the 3D view of scripts/viewer.py (viewer/fdm-viewer.js on viewer/three.min.js) with
// the model's meshes (model.glb), the parts table's switches (show or hide a part, see through it), and the keys:
// Esc closes, ← and → go to the previous and next model. The model's data for the view (#model-data) is a JSON block
// of the page. Everything is read from this site.
(() => {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const m = JSON.parse($("model-data").textContent);
  const stage = $("stage");
  let viewer = null;
  document.querySelector("main.model").classList.add("js"); // shows the switches of the parts table

  const loadScript = (src) => new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = src;
    s.onload = resolve;
    s.onerror = () => reject(new Error(`could not load ${src}`));
    document.head.append(s);
  });

  async function start() {
    $("status").textContent = "Loading…";
    try {
      const [glb] = await Promise.all([
        fetch(`/models/${m.id}/model.glb`).then((r) => {
          if (!r.ok) throw new Error(`model.glb: HTTP ${r.status}`);
          return r.arrayBuffer();
        }),
        loadScript("/viewer/three.min.js").then(() => loadScript("/viewer/fdm-viewer.js")),
      ]);
      viewer = await FDMViewer.create(stage, {
        glb, view: m.view, zoom: m.zoom, background: "#f6f6f4",
        anchors: Object.fromEntries(m.parts.filter((p) => p.anchor).map((p) => [p.name, p.anchor])),
      });
      partRows.forEach(applyPart); // what was changed while the model was loading
      $("still").hidden = true; // the preview image stays until the 3D view is there
      $("status").textContent = "";
      $("help").hidden = false;
      $("controls").hidden = false;
    } catch (e) {
      $("status").textContent = `The 3D view could not start (${e.message}).`;
    }
  }

  // each row of the parts table shows or hides its part (the checkbox) and makes it transparent (the button); the
  // page starts with every part shown and opaque
  const partRows = [...document.querySelectorAll("tr[data-part]")].map((tr) => ({
    name: tr.dataset.part, show: tr.querySelector("input"), see: tr.querySelector(".see"), tr,
  }));
  // the row's state is the state of the part: drawn on the row, and given to the 3D view once it is there
  function applyPart(row) {
    const see = row.see.getAttribute("aria-pressed") === "true";
    row.tr.classList.toggle("off", !row.show.checked);
    row.tr.classList.toggle("clear", see);
    if (!viewer) return;
    viewer.setVisible(row.name, row.show.checked);
    viewer.setTransparent(row.name, see);
  }
  for (const row of partRows) {
    row.show.addEventListener("change", () => applyPart(row));
    row.see.addEventListener("click", () => {
      row.see.setAttribute("aria-pressed", String(row.see.getAttribute("aria-pressed") !== "true"));
      applyPart(row);
    });
  }
  $("parts-all").addEventListener("click", () => partRows.forEach((row) => {
    row.show.checked = true;
    row.see.setAttribute("aria-pressed", "false");
    applyPart(row);
  }));

  function setControls(arrangement) {
    document.querySelectorAll("#arrangement button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.v === arrangement)));
    $("explode").disabled = arrangement === "print";
    $("explode-row").classList.toggle("off", arrangement === "print");
  }
  document.querySelectorAll("#arrangement button").forEach((b) => b.addEventListener("click", () => {
    viewer.setArrangement(b.dataset.v);
    setControls(b.dataset.v);
  }));
  $("explode").addEventListener("input", (e) => viewer.setExplode(Number(e.target.value)));
  $("reset").addEventListener("click", () => viewer.resetView());

  // Close goes Back when the page before this one is on this site (the list, or the page the visitor came here
  // from), so it comes back where it was scrolled to. Opened from a search or a shared link, or without the
  // Navigation API, it is a plain link to the home page. The Navigation API lists only the entries of this site
  // before and after this one; it does not tell their addresses here (Referrer-Policy: no-referrer).
  const fromSite = () => {
    const nav = window.navigation;
    return Boolean(nav && nav.currentEntry && nav.currentEntry.index > 0);
  };
  const close = () => {
    if (fromSite()) history.back();
    else location.assign($("close").href);
  };
  // Previous and next replace this page in the history, so Back still goes to where the visitor came from.
  const step = (a) => location.replace(a.href);

  const plain = (e) => !(e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0); // not "open in a new tab"
  $("close").addEventListener("click", (e) => {
    if (!plain(e)) return;
    e.preventDefault();
    close();
  });
  for (const id of ["prev", "next"]) {
    $(id).addEventListener("click", (e) => {
      if (!plain(e)) return;
      e.preventDefault();
      step($(id));
    });
  }
  document.addEventListener("keydown", (e) => {
    // the slider uses the arrows, and on the parts table they would leave the model being taken apart
    if (e.target.closest("input, tbody") && e.key !== "Escape") return;
    if (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return; // Alt+Left is Back
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft") step($("prev"));
    if (e.key === "ArrowRight") step($("next"));
  });

  start();
})();
