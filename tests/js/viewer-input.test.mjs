// Wheel events as each browser and OS sends them, fed to the input functions of the HTML viewer.
//   node --test tests/js/*.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const src = readFileSync(new URL("../../skills/fdm-minimal-design/scripts/viewer/fdm-viewer.js", import.meta.url), "utf8");
const ctx = {};
vm.runInNewContext(src, ctx);
const { notches, isTrackpadPan, zoomDelta, ZOOM_STEP } = ctx.FDMViewer.input;
const wheel = (e) => ({ deltaMode: 0, deltaX: 0, wheelDeltaX: 0, ctrlKey: false, ...e });

// one notch of a mouse wheel, toward the screen
const MOUSE = {
  "Chrome, Windows": wheel({ deltaY: -100, wheelDeltaY: 120 }),
  "Chrome, macOS": wheel({ deltaY: -4, wheelDeltaY: 120 }),
  "Safari, macOS": wheel({ deltaY: -4.000244140625, wheelDeltaY: 12 }),
  "Firefox": wheel({ deltaY: -3, deltaMode: 1 }),
};

for (const [name, e] of Object.entries(MOUSE)) {
  test(`when a mouse wheel turns one notch in ${name}, it counts as one notch`, () => {
    assert.equal(notches(e), 1);
  });
  test(`when a mouse wheel turns one notch in ${name}, the view zooms by the fixed step`, () => {
    assert.ok(Math.abs(0.95 ** (Math.abs(zoomDelta(e)) / 100) - ZOOM_STEP) < 1e-9);
  });
}

test("when Chrome accelerates a mouse wheel to three notches, it counts as three", () => {
  assert.equal(notches(wheel({ deltaY: -12, wheelDeltaY: 360 })), 3);
});

test("when a trackpad scrolls a little in Chrome, it is a fraction of a notch", () => {
  assert.equal(notches(wheel({ deltaY: 7, wheelDeltaY: -21 })), 0.07);
});

test("when a trackpad sends a multiple of 40 px in Chrome, it is not taken for wheel notches", () => {
  assert.equal(notches(wheel({ deltaY: 40, wheelDeltaY: -120 })), 0.4);
});

test("when the two-finger scroll setting is zoom, a trackpad scroll does not pan", () => {
  assert.equal(isTrackpadPan(wheel({ deltaY: 7, wheelDeltaY: -21 }), "zoom"), false);
});

test("when the two-finger scroll setting is pan, a trackpad scroll in Chrome or Safari pans", () => {
  assert.equal(isTrackpadPan(wheel({ deltaY: 7, wheelDeltaY: -21 }), "pan"), true);
  assert.equal(isTrackpadPan(wheel({ deltaX: 5, wheelDeltaX: -15, deltaY: 0, wheelDeltaY: 0 }), "pan"), true);
});

test("when the two-finger scroll setting is pan, a trackpad scroll in Firefox (pixels) pans", () => {
  assert.equal(isTrackpadPan(wheel({ deltaY: 7 }), "pan"), true);
});

test("when the two-finger scroll setting is pan, a Windows mouse wheel still zooms", () => {
  assert.equal(isTrackpadPan(MOUSE["Chrome, Windows"], "pan"), false);
  assert.equal(isTrackpadPan(MOUSE.Firefox, "pan"), false);
});

test("when the trackpad pinches (ctrlKey), it zooms by the pinch and never pans", () => {
  const pinch = wheel({ deltaY: 3.5, wheelDeltaY: -10.5, ctrlKey: true });
  assert.equal(isTrackpadPan(pinch, "pan"), false);
  assert.equal(zoomDelta(pinch), 3.5);
});
