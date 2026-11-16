// FDMViewer: the 3D view of a design, without any page around it.
//
//   const viewer = await FDMViewer.create(container, { glb, view: [-0.6, -1, 0.6], zoom: 1.15, anchors: { inlay: "plate" } });
//   viewer.setArrangement("print");   // "assembled" (default) or "print"
//   viewer.setVisible("lid", false);
//   viewer.setTransparent("lid", true); // see the parts inside it
//   viewer.setExplode(0.5);           // 0 = assembled, 1 = fully apart (assembled arrangement only)
//   viewer.setEdges(true);
//   viewer.setScroll("pan");          // what a trackpad two-finger scroll does: "zoom" (default) or "pan"
//   viewer.resetView();
//   viewer.dispose();
//
// glb is an ArrayBuffer of the binary glTF written by scripts/viewer.py: a root node "assembled" and a
// root node "print", each holding one node per part (the part name in the node extras as "part"),
// with the part colours as materials.
// window.THREE must be loaded first (three.min.js). FDMViewer.input holds the pure functions that read
// wheel events, so they can be tested without a browser.
//
// Input (the same on every platform):
//   mouse     wheel = zoom (a fixed step per notch), drag = rotate, Shift + drag or middle drag = pan
//   trackpad  pinch or two-finger scroll = zoom, click-drag = rotate, Shift + click-drag = pan;
//             with setScroll("pan"): two-finger scroll = pan, Shift + two-finger scroll = rotate
// The right button is not used (the browser menu opens there).
(function (root) {
  "use strict";

  const ZOOM_STEP = 0.88; // distance factor per wheel notch
  const EDGE_OPACITY = 0.35;
  const TRANSPARENT = 0.2; // opacity of the faces of a part made transparent; its edges are drawn at half their own

  // How many wheel notches an event stands for, whatever the browser and OS.
  function notches(e) {
    const d = Math.abs(e.deltaY), w = Math.abs(e.wheelDeltaY || 0);
    if (e.deltaMode === 1) return d / 3; // Firefox: 3 lines per notch
    if (e.deltaMode === 2) return d; // pages
    // Chrome: wheelDeltaY is 120 per notch (before acceleration). A trackpad (wheelDeltaY = 3 x deltaY)
    // that happens to send a multiple of 40 px is not a notch.
    if (w && w % 120 === 0 && w !== 3 * d) return w / 120;
    const k = d / 4.000244140625; // Safari on macOS: 0.1 line x 40 px per notch, multiples when accelerated
    if (k >= 1 && Math.abs(k - Math.round(k)) < 1e-6) return 1;
    return d / 100; // other pixel deltas (Windows sends 100 px per notch)
  }

  // Whether a wheel event is a trackpad two-finger scroll that should pan (only when the scroll setting
  // is "pan"). Pinch arrives as a wheel event with ctrlKey and always zooms. Chrome and Safari send
  // wheelDeltaY = -3 x deltaY for a trackpad; Firefox (no wheelDelta) sends pixels for a trackpad and
  // lines for a wheel. Some mice (Magic Mouse, smooth-scrolling drivers) look exactly like a trackpad,
  // which is why "zoom" is the default.
  function isTrackpadPan(e, scroll) {
    if (e.ctrlKey || scroll !== "pan") return false;
    const [w, d] = e.wheelDeltaY ? [e.wheelDeltaY, e.deltaY] : [e.wheelDeltaX, e.deltaX];
    return w ? w === -3 * d : e.deltaMode === 0;
  }

  // The wheel event OrbitControls should see: deltaY such that one notch zooms by ZOOM_STEP
  // (OrbitControls zooms by 0.95 ^ (|deltaY| / 100)). Pinch (ctrlKey) is passed through.
  function zoomDelta(e) {
    if (e.ctrlKey) return e.deltaY;
    return (Math.sign(e.deltaY) * notches(e) * 100 * Math.log(ZOOM_STEP)) / Math.log(0.95);
  }

  function decode(base64) {
    const s = atob(base64);
    const out = new Uint8Array(s.length);
    for (let i = 0; i < s.length; i++) out[i] = s.charCodeAt(i);
    return out.buffer;
  }

  async function create(container, options) {
    const T = root.THREE;
    const opts = Object.assign({ view: [-0.6, -1, 0.6], zoom: 1.15, background: "#f6f6f4", edges: true }, options);
    const gltf = await new Promise((resolve, reject) => new T.GLTFLoader().parse(opts.glb, "", resolve, reject));

    const renderer = new T.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(root.devicePixelRatio || 1, 2));
    renderer.outputColorSpace = T.SRGBColorSpace;
    renderer.domElement.style.display = "block";
    renderer.domElement.style.touchAction = "none";
    container.appendChild(renderer.domElement);

    const scene = new T.Scene();
    scene.background = new T.Color(opts.background);
    scene.add(new T.HemisphereLight(0xffffff, 0x8a8a86, 1.6));
    const camera = new T.PerspectiveCamera(25, 1, 1, 10000);
    camera.up.set(0, 0, 1);
    const key = new T.DirectionalLight(0xffffff, 1.6);
    key.position.set(-0.5, 0.8, 1); // upper left of the view, follows the camera
    camera.add(key);
    scene.add(camera);

    // one group per arrangement, one mesh per part; the edges are drawn at creases over 30 degrees
    const groups = {}, parts = {};
    for (const g of [...gltf.scene.children]) { // a copy: scene.add moves g out of gltf.scene
      groups[g.name] = g;
      for (const node of g.children) {
        const mesh = node.isMesh ? node : node.children.find((c) => c.isMesh);
        mesh.geometry.computeVertexNormals();
        mesh.material = new T.MeshStandardMaterial({ color: mesh.material.color, roughness: 0.75, metalness: 0 });
        mesh.material.polygonOffset = true; // lines in front of the faces they lie on
        mesh.material.polygonOffsetFactor = 1;
        mesh.material.polygonOffsetUnits = 1;
        const edgeMat = new T.LineBasicMaterial({ color: 0x3a3a38, transparent: true, opacity: EDGE_OPACITY }); // one per part, for setTransparent
        const edges = new T.LineSegments(new T.EdgesGeometry(mesh.geometry, 30), edgeMat);
        edges.visible = opts.edges;
        mesh.add(edges);
        (parts[node.userData.part] ||= {})[g.name] = { node, mesh, edges, home: node.position.clone() };
      }
      scene.add(g);
    }
    if (!groups.assembled || !groups.print) throw new Error("the GLB needs the root nodes 'assembled' and 'print'");

    const boxOf = (obj) => new T.Box3().setFromObject(obj, true);
    const assembledBox = boxOf(groups.assembled);
    const centre = assembledBox.getCenter(new T.Vector3());
    // a part moves away from the centre of the assembly along the line through its own centre;
    // an inlay (options.anchors: {inlay: parent}) moves with its parent
    const anchors = opts.anchors || {};
    const rootOf = (n) => (anchors[n] && parts[anchors[n]] ? rootOf(anchors[n]) : n);
    for (const [name, p] of Object.entries(parts)) {
      p.assembled.away = boxOf(parts[rootOf(name)].assembled.mesh).getCenter(new T.Vector3()).sub(centre);
    }

    // the ground grid: 10 mm cells, under whichever arrangement is shown
    const grid = new T.Group();
    scene.add(grid);
    const makeGrid = (box) => {
      grid.clear();
      const size = box.getSize(new T.Vector3());
      const span = Math.ceil((Math.max(size.x, size.y) * 1.6) / 20) * 20;
      const minor = new T.GridHelper(span, span / 10, 0xe2e2de, 0xe2e2de);
      const major = new T.GridHelper(span, span / 50, 0xd2d2ce, 0xd2d2ce);
      for (const g of [minor, major]) {
        g.rotation.x = Math.PI / 2;
        g.position.set(Math.round(box.getCenter(new T.Vector3()).x / 10) * 10,
          Math.round(box.getCenter(new T.Vector3()).y / 10) * 10, box.min.z - 0.05);
        grid.add(g);
      }
    };

    const controls = new T.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = false;
    controls.zoomToCursor = true;
    controls.mouseButtons = { LEFT: T.MOUSE.ROTATE, MIDDLE: T.MOUSE.PAN, RIGHT: null };
    // one wheel notch zooms by the same step on every platform (OrbitControls' own wheel zoom is
    // proportional to deltaY, which barely moves on a Mac). _customWheelEvent, _rotateLeft, _rotateUp,
    // _pan, _updateZoomParameters and _dollyIn are internals of OrbitControls in three.js 0.187.
    controls._customWheelEvent = (e) => ({ clientX: e.clientX, clientY: e.clientY, deltaY: zoomDelta(e) });

    let state = { arrangement: "assembled", explode: 0, scroll: "zoom" };
    let dirty = true;
    const render = () => (dirty = true);
    controls.addEventListener("change", render);

    const el = renderer.domElement;
    el.addEventListener("mousedown", (e) => e.button === 1 && e.preventDefault()); // no autoscroll
    el.addEventListener("contextmenu", (e) => e.preventDefault());
    el.addEventListener("wheel", (e) => {
      if (!isTrackpadPan(e, state.scroll)) return;
      e.preventDefault();
      e.stopImmediatePropagation();
      const h = el.clientHeight || 1;
      if (e.shiftKey) {
        controls._rotateLeft((2 * Math.PI * -e.deltaX) / h);
        controls._rotateUp((2 * Math.PI * -e.deltaY) / h);
      } else {
        controls._pan(-e.deltaX, -e.deltaY);
      }
      controls.update();
    }, { capture: true, passive: false });
    // Safari on macOS sends pinch as gesture events (without preventDefault the whole page zooms)
    let pinched = 1;
    el.addEventListener("gesturestart", (e) => {
      e.preventDefault();
      pinched = 1;
    });
    el.addEventListener("gesturechange", (e) => {
      e.preventDefault();
      controls._updateZoomParameters(e.clientX, e.clientY);
      controls._dollyIn(pinched / e.scale);
      pinched = e.scale;
      controls.update();
    });

    const visibleBox = () => {
      const box = new T.Box3();
      for (const p of Object.values(parts)) {
        const m = p[state.arrangement]; // a bought part has no node in the print layout
        if (m && m.node.visible) box.union(boxOf(m.mesh));
      }
      return box.isEmpty() ? boxOf(groups[state.arrangement]) : box;
    };

    function resetView() {
      const box = boxOf(groups[state.arrangement]);
      const sphere = box.getBoundingSphere(new T.Sphere());
      const dir = state.arrangement === "print" ? new T.Vector3(0.35, -0.9, 1.3) : new T.Vector3(...opts.view);
      dir.normalize();
      const fit = sphere.radius / Math.sin((camera.fov * Math.PI) / 360);
      const zoom = state.arrangement === "print" ? 0.85 : (opts.zoom || 1) * 0.9; // the print layout leaves room for labels
      const dist = (fit * Math.max(1, 1 / camera.aspect)) / zoom;
      controls.target.copy(sphere.center);
      camera.position.copy(sphere.center).addScaledVector(dir, dist);
      camera.near = dist / 100;
      camera.far = dist * 100;
      camera.updateProjectionMatrix();
      controls.minDistance = sphere.radius * 0.1;
      controls.maxDistance = dist * 10;
      controls.update();
      render();
    }

    function setArrangement(name) {
      if (!groups[name]) throw new Error(`no arrangement ${name}`);
      state.arrangement = name;
      groups.assembled.visible = name === "assembled";
      groups.print.visible = name === "print";
      makeGrid(boxOf(groups[name]));
      resetView();
    }

    function setExplode(t) {
      state.explode = Math.max(0, Math.min(1, t));
      for (const p of Object.values(parts)) {
        const a = p.assembled;
        a.node.position.copy(a.home).addScaledVector(a.away, state.explode * 1.2);
      }
      render();
    }

    function setVisible(name, on) {
      for (const m of Object.values(parts[name] || {})) m.node.visible = on;
      render();
    }

    // A transparent part does not hide what is behind it (it writes no depth), so the parts inside show through.
    // It is drawn after the edges of the other parts (renderOrder), so those are dimmed by it like their faces.
    function setTransparent(name, on) {
      for (const m of Object.values(parts[name] || {})) {
        m.mesh.renderOrder = m.edges.renderOrder = on ? 1 : 0;
        m.mesh.material.transparent = on;
        m.mesh.material.opacity = on ? TRANSPARENT : 1;
        m.mesh.material.depthWrite = !on;
        m.mesh.material.needsUpdate = true;
        m.edges.material.opacity = on ? EDGE_OPACITY / 2 : EDGE_OPACITY;
      }
      render();
    }

    function setEdges(on) {
      for (const p of Object.values(parts)) for (const m of Object.values(p)) m.edges.visible = on;
      render();
    }

    // Where a point of the scene is on the canvas, in CSS pixels (for labels drawn by the page)
    function toScreen(v) {
      const p = new T.Vector3(...v).project(camera);
      return { x: ((p.x + 1) / 2) * el.clientWidth, y: ((1 - p.y) / 2) * el.clientHeight, behind: p.z > 1 };
    }

    // The box of a part (or of every visible part) in the current arrangement, explode included
    function box(name) {
      const b = name ? boxOf(parts[name][state.arrangement].mesh) : visibleBox();
      return { min: b.min.toArray(), max: b.max.toArray() };
    }

    const listeners = [];
    const resize = () => {
      const w = container.clientWidth, h = container.clientHeight;
      renderer.setSize(w, h, true);
      camera.aspect = w / Math.max(h, 1);
      camera.updateProjectionMatrix();
      render();
    };
    const observer = new ResizeObserver(resize);
    observer.observe(container);
    let frame = 0;
    const loop = () => {
      frame = requestAnimationFrame(loop);
      if (!dirty) return;
      dirty = false;
      renderer.render(scene, camera);
      for (const f of listeners) f();
    };
    resize();
    setArrangement("assembled");
    loop();

    return {
      parts: Object.keys(parts),
      size: assembledBox.getSize(new T.Vector3()).toArray(),
      setArrangement,
      setExplode,
      setVisible,
      setTransparent,
      setEdges,
      setScroll: (mode) => (state.scroll = mode === "pan" ? "pan" : "zoom"),
      resetView,
      toScreen,
      box,
      get arrangement() {
        return state.arrangement;
      },
      onRender: (f) => listeners.push(f), // called after every frame that was drawn
      canvas: el,
      dispose() {
        cancelAnimationFrame(frame);
        observer.disconnect();
        controls.dispose();
        renderer.dispose();
        renderer.forceContextLoss(); // free the WebGL context now; browsers allow only a few at a time
        el.remove();
      },
    };
  }

  root.FDMViewer = { create, decode, input: { notches, isTrackpadPan, zoomDelta, ZOOM_STEP } };
})(typeof window !== "undefined" ? window : globalThis);
