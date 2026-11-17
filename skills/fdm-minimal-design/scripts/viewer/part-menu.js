// FDMPartMenu: the menu of a part, opened by clicking, tapping or right-clicking the part in the 3D view.
//
//   FDMPartMenu.attach(viewer, { container, rows, showAll });
//
// container is the element the viewer's canvas is in (the menu is placed in it, next to the click). rows has one entry
// per part of the parts table: { name, label, color, show, see, tr } with show the checkbox that shows the part,
// see the button that makes it transparent (aria-pressed) and tr the row, which is marked while the menu is open.
// showAll is the table's button that shows every part opaque. The menu works these controls (it clicks them), so the
// table holds the only state of the parts and the page reacts to the menu as to the table.
//
// The menu holds the part's name, Hide, Transparent (on and off), Show only this and Show all. Opened, it has the
// focus: the arrows, Home and End move in it, Enter and Space choose, Esc and Tab close it, and the focus goes back
// where it was. A click outside it, on nothing in the view, or a drag, wheel or pinch on the view closes it.
// Picking a part is for the mouse and touch; with the keyboard the parts table does the same.
(function (root) {
  "use strict";

  // Where a menu of size w x h goes in a container of size W x H for a click at x, y: below and right of the point,
  // flipped to the other side where it would overflow, and kept inside.
  function place(x, y, w, h, W, H, gap = 8) {
    let left = x + gap, top = y + gap;
    if (left + w > W) left = x - gap - w;
    if (top + h > H) top = y - gap - h;
    return { left: Math.max(0, Math.min(left, W - w)), top: Math.max(0, Math.min(top, H - h)) };
  }

  // the nearest ancestor that scrolls (the side panel), or null where the page itself scrolls
  function scroller(el) {
    for (let e = el.parentElement; e && e !== document.body; e = e.parentElement) {
      const o = getComputedStyle(e).overflowY;
      if ((o === "auto" || o === "scroll") && e.scrollHeight > e.clientHeight) return e;
    }
    return null;
  }

  function attach(viewer, { container, rows, showAll }) {
    const pressed = (b) => b.getAttribute("aria-pressed") === "true";
    const byName = new Map(rows.map((r) => [r.name, r]));
    const ITEMS = [
      { text: "Hide", run: (r) => r.show.checked && r.show.click() },
      { text: "Transparent", checked: (r) => pressed(r.see), run: (r) => r.see.click() },
      {
        text: "Show only this",
        enabled: (r) => rows.some((o) => o !== r && o.show.checked),
        run: (r) => rows.forEach((o) => o !== r && o.show.checked && o.show.click()),
      },
      { text: "Show all", enabled: () => rows.some((o) => !o.show.checked || pressed(o.see)), run: () => showAll.click() },
    ];

    const box = document.createElement("div");
    box.className = "part-menu";
    box.hidden = true;
    box.innerHTML = '<div class="pm-title" id="part-menu-title"><span class="pm-sw"></span><span class="pm-name"></span></div>'
      + '<div role="menu" aria-labelledby="part-menu-title"></div>';
    const list = box.querySelector('[role="menu"]');
    container.append(box);

    let current = null; // the row the menu is open for
    let back = null; // what had the focus before the menu opened
    const buttons = () => [...list.querySelectorAll("button")];

    function open(name, at) {
      const row = byName.get(name);
      if (!row) return close(false);
      if (current) current.tr.classList.remove("picked");
      else back = document.activeElement;
      current = row;
      box.querySelector(".pm-name").textContent = row.label;
      box.querySelector(".pm-sw").style.background = row.color;
      list.replaceChildren(...ITEMS.map((item) => {
        const b = document.createElement("button");
        b.type = "button";
        b.textContent = item.text;
        b.setAttribute("role", item.checked ? "menuitemcheckbox" : "menuitem");
        if (item.checked) b.setAttribute("aria-checked", String(item.checked(row)));
        // an item that would change nothing stays in the arrows' path and is read as unavailable
        const off = item.enabled ? !item.enabled(row) : false;
        if (off) b.setAttribute("aria-disabled", "true");
        b.addEventListener("click", () => {
          if (off) return;
          item.run(row);
          close(true);
        });
        return b;
      }));
      box.hidden = false;
      const p = place(at.x, at.y, box.offsetWidth, box.offsetHeight, container.clientWidth, container.clientHeight);
      box.style.left = `${p.left}px`;
      box.style.top = `${p.top}px`;
      row.tr.classList.add("picked");
      const s = scroller(row.tr); // bring the row into the side panel; a page that scrolls itself is left where it is
      if (s) {
        const r = row.tr.getBoundingClientRect(), v = s.getBoundingClientRect();
        if (r.top < v.top) s.scrollTop -= v.top - r.top + 8;
        else if (r.bottom > v.bottom) s.scrollTop += r.bottom - v.bottom + 8;
      }
      viewer.setHighlight(name);
      buttons()[0].focus({ preventScroll: true });
    }

    // restore: give the focus back (closed from the menu); a click elsewhere keeps the focus it gives
    function close(restore) {
      if (!current) return;
      current.tr.classList.remove("picked");
      current = null;
      viewer.setHighlight(null);
      const had = box.contains(document.activeElement);
      box.hidden = true;
      if (restore && had && back && back.isConnected && back.focus) back.focus({ preventScroll: true });
    }

    viewer.onPick((name, at) => open(name, at));
    // a press on the view does not take the focus from where it is, so closing the menu can give it back there
    viewer.canvas.addEventListener("mousedown", (e) => e.preventDefault());
    // a press anywhere but on the menu closes it (a click on a part then opens the part's menu)
    document.addEventListener("pointerdown", (e) => current && !box.contains(e.target) && close(false), true);
    // (on the container, in the capture phase: the view stops a two-finger scroll that pans from going further)
    for (const type of ["wheel", "gesturestart"]) container.addEventListener(type, () => close(false), { capture: true, passive: true });
    box.addEventListener("mousedown", (e) => e.target.closest("button") || e.preventDefault()); // the name keeps the focus in the menu
    // the menu's keys, before the page's own (Esc closes the model page there, the arrows go to the next model)
    window.addEventListener("keydown", (e) => {
      if (!current) return;
      if (e.key === "Escape") {
        e.preventDefault();
        e.stopPropagation();
        close(true);
        return;
      }
      if (!box.contains(document.activeElement)) return;
      e.stopPropagation();
      const bs = buttons(), i = bs.indexOf(document.activeElement);
      const to = { ArrowDown: i + 1, ArrowUp: i - 1, Home: 0, End: bs.length - 1 }[e.key];
      if (to !== undefined) {
        e.preventDefault();
        bs[(to + bs.length) % bs.length].focus();
      } else if (e.key === "Tab") {
        e.preventDefault();
        close(true);
      }
    }, true);
  }

  root.FDMPartMenu = { attach, place };
})(typeof window !== "undefined" ? window : globalThis);
