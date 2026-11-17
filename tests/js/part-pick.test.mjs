// Picking a part by clicking it in the 3D view: which presses are clicks, which part a click picks, and where the
// part's menu goes. The pure functions of fdm-viewer.js and part-menu.js, run without a browser.
//   node --test tests/js/*.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const ctx = {};
for (const name of ["fdm-viewer.js", "part-menu.js"]) {
  vm.runInNewContext(readFileSync(new URL(`../../skills/fdm-minimal-design/scripts/viewer/${name}`, import.meta.url), "utf8"), ctx);
}
const { isTap, choose } = ctx.FDMViewer.input;
const { place } = ctx.FDMPartMenu;
const press = (p) => ({ button: 0, pointerType: "mouse", moved: 0, multi: false, ...p });

test("when the mouse is pressed and released without moving, it is a click", () => {
  assert.equal(isTap(press({ moved: 0 })), true);
  assert.equal(isTap(press({ moved: 3 })), true);
});
test("when the mouse moves more than a few pixels while pressed, it is a drag and not a click", () => {
  assert.equal(isTap(press({ moved: 8 })), false);
});
test("when a finger wobbles a little on a tap, it is still a tap", () => {
  assert.equal(isTap(press({ pointerType: "touch", moved: 8 })), true);
  assert.equal(isTap(press({ pointerType: "touch", moved: 20 })), false);
});
test("when a second finger goes down (a pinch), it is not a tap", () => {
  assert.equal(isTap(press({ pointerType: "touch", multi: true })), false);
});
test("when the press is of the middle or right button, it is not a click (the right button opens the menu by itself)", () => {
  assert.equal(isTap(press({ button: 1 })), false);
  assert.equal(isTap(press({ button: 2 })), false);
});

test("when nothing is under the pointer, no part is picked", () => {
  assert.equal(choose([]), null);
});
test("when an opaque part is nearest, it is picked", () => {
  assert.equal(choose([{ part: "lid", transparent: false }, { part: "body", transparent: false }]), "lid");
});
test("when a transparent part is in front of an opaque one, the opaque part behind it is picked", () => {
  assert.equal(choose([{ part: "lid", transparent: true }, { part: "body", transparent: true }, { part: "board", transparent: false }]), "board");
});
test("when only transparent parts are under the pointer, the nearest of them is picked", () => {
  assert.equal(choose([{ part: "lid", transparent: true }, { part: "body", transparent: true }]), "lid");
});

test("when there is room, the menu goes below and right of the click", () => {
  assert.deepEqual({ ...place(100, 100, 160, 120, 800, 600) }, { left: 108, top: 108 });
});
test("when the click is near the right and bottom edges, the menu goes left of and above it", () => {
  assert.deepEqual({ ...place(750, 560, 160, 120, 800, 600) }, { left: 582, top: 432 });
});
test("when the view is smaller than the menu, the menu stays at the top left corner of the view", () => {
  assert.deepEqual({ ...place(50, 40, 160, 120, 120, 100) }, { left: 0, top: 0 });
});
