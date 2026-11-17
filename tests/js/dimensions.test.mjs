// Where the labels of the print layout go (dimensions.js): a label that would overlap one already drawn moves down.
//   node --test tests/js/*.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const ctx = {};
vm.runInNewContext(readFileSync(new URL("../../skills/fdm-minimal-design/scripts/viewer/dimensions.js", import.meta.url), "utf8"), ctx);
const { stack } = ctx.FDMDimensions;

test("when no label is drawn yet, a label stays where it is wanted", () => {
  assert.equal(stack([], 100, 50, 60), 50);
});
test("when a label would cover one already drawn, it moves down below it", () => {
  assert.equal(stack([{ x: 110, y: 50, w: 60 }], 100, 50, 60), 80);
});
test("when the label below is taken too, it moves down past both", () => {
  assert.equal(stack([{ x: 100, y: 50, w: 60 }, { x: 100, y: 80, w: 60 }], 100, 60, 60), 120);
});
test("when the labels are side by side and do not touch, neither moves", () => {
  assert.equal(stack([{ x: 0, y: 50, w: 60 }], 61, 50, 60), 50);
});

// What attach draws, on a stand-in for the viewer and the SVG (the drawing itself is checked in a browser)
function stage({ arrangement = "assembled", explode = 0, hidden = [] } = {}) {
  const el = (tag) => ({ tag, attrs: {}, textContent: "", setAttribute(k, v) { this.attrs[k] = v; }, getBBox: () => ({ width: 40 }) });
  const svg = { kids: [], append(e) { this.kids.push(e); }, replaceChildren() { this.kids = []; } };
  const listeners = [];
  const viewer = {
    arrangement, explode, parts: ["body", "inlay", "board", "lid"],
    visible: (n) => !hidden.includes(n),
    box: (n) => (n ? { min: [0, 0, 0], max: [10, 10, 10] } : { min: [0, 0, 0], max: [96, 40.04, 82.4] }),
    toScreen: (v) => ({ x: v[0] * 10, y: v[1] * 10 + v[2], behind: false }),
    onRender: (f) => listeners.push(f),
  };
  const parts = [
    { name: "body", qty: 1, print_size: [96, 40, 80] },
    { name: "inlay", qty: 1, anchor: "body", print_size: [40, 30, 0.4] },
    { name: "board", qty: 1, ref: true, print_size: null },
    { name: "lid", qty: 2, print_size: [96, 40, 6.4] },
  ];
  const c = { document: { createElementNS: (_, tag) => el(tag) } };
  vm.runInNewContext(readFileSync(new URL("../../skills/fdm-minimal-design/scripts/viewer/dimensions.js", import.meta.url), "utf8"), c);
  const dims = c.FDMDimensions.attach(viewer, { svg, parts });
  const texts = () => svg.kids.filter((k) => k.tag === "text").map((k) => k.textContent);
  return { svg, viewer, dims, texts, redraw: () => listeners.forEach((f) => f()) };
}

test("when assembled, the width, depth and height of the box of the parts shown are drawn to 0.1 mm", () => {
  const s = stage();
  assert.deepEqual(s.texts(), ["96", "40", "82.4"]);
  assert.equal(s.svg.kids.filter((k) => k.tag === "line").length, 9);
});
test("when exploded, the overall dimensions are not drawn", () => {
  assert.deepEqual(stage({ explode: 0.3 }).texts(), []);
});
test("when every part is hidden, nothing is drawn", () => {
  assert.deepEqual(stage({ hidden: ["body", "inlay", "board", "lid"] }).texts(), []);
});
test("when in the print layout, each printed part shown gets its name and print size, but not inlays, bought parts or hidden parts", () => {
  assert.deepEqual(stage({ arrangement: "print" }).texts(), ["body", "96 × 40 × 80", "lid ×2", "96 × 40 × 6.4"]);
  assert.deepEqual(stage({ arrangement: "print", hidden: ["lid"] }).texts(), ["body", "96 × 40 × 80"]);
});
test("when the switch is turned off, nothing is drawn, also after the view is drawn again, and on brings them back", () => {
  const s = stage();
  s.dims.setOn(false);
  s.redraw();
  assert.deepEqual(s.texts(), []);
  s.dims.setOn(true);
  assert.deepEqual(s.texts(), ["96", "40", "82.4"]);
});
test("when the view changes (a part hidden), the next frame draws the dimensions again from it", () => {
  const s = stage();
  s.viewer.visible = () => false;
  s.redraw();
  assert.deepEqual(s.texts(), []);
});
