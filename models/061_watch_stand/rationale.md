# 061 Watch stand

A stand for one wristwatch, 80 × 64 × 52. The watch is buckled as it is worn and dropped over a dark upright post, 56 × 32 in plan;
the strap wraps the post and the case stands on the base in front of it, dial facing forward. The post sits 6 deep in a pocket in the
base with 0.25 clearance all round: it stands square, lifts out with the watch on it, and can be swapped for a post cut to another
wrist size. The base is an off-white plate on a floating plinth.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Post plan | 56 × 32, R12 | Perimeter 155, about the smallest wrist: a buckled strap or bracelet slides over it; R12 bends a bracelet gently |
| Post height above the base | 40 | The height of a common 40 case standing on the base: the case's top and the post's top line up |
| Base | 80 × 64 × 12, R12 | The post plus a 12 margin at the sides and back and 20 at the front (5 : 4); one radius for both parts |
| Front margin | 20 | The side margin plus 8: a case up to about 16 thick stands on the base in front of the post |
| Pocket | Post outline + 0.25 per side, 6 deep | Location clearance; half the base height, so the post tilts at most 5° when pushed |
| Plinth | 2.4 high, set in 1.2 with a 45° face | Floating base, the same plinth as the trays |
| Rubber feet | 4 × Ø10.2 × 1 recesses at x ±28, y ±20 | Inside the plinth, under the corners of the post |
| Edges | C0.5; C0.6 on the bed faces | One visible chamfer value; the pocket's rim takes C0.5 so the seam at the post's foot is one line |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| base | Bottom down | Off-white |
| post | Bottom down | Dark grey |
| (4 × Ø10 stick-on rubber feet) | Bought | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| base / post | The pocket was 4 deep: with 0.25 per side the post could lean 7° when the watch was pushed on | Defect | Pocket 6 deep (half the base): at most 5°, and the post's flat foot keeps it upright under its own weight |
| post | The post stood 48 above the base, a height with no relation to anything (it came from 1.5 × its depth) | Violation | 40, the height of a common case standing on the base, so the case's top lines up with the post's top |

Dos and Don'ts: one visible chamfer value (C0.5) plus C0.6 at the bed and the plinth's 1.2; one radius (R12) for the base and the
post; the margins round the post are 12 on three sides and 20 at the front, where the case stands; no fasteners; no accent (nothing has
a function to point at); the post is the secondary dark grey, the base off-white.

Use cases:
- **Put the watch on:** buckle it and slide it down over the post; the case comes to stand on the base in front of the post. A watch
  envelope (40 × 12 case, 2.4 strap round the post) sits there with no overlap with either part.
- **Take it off:** lift the watch up over the top of the post, or lift the post out of the pocket with the watch on it (swept: the post
  is free upward from 0 to 30; it stops at 0.3 downward and at 0.4 sideways, free at 0.2).
- **Place:** the base stands on 4205 mm² inside the plinth (76.5 × 60.5); the watch's weight is on the base, in front of the post, well
  inside it.
- **Hold:** carry it by the base. Lifted by the post, only the post comes up.
- **Another wrist size:** a strap that does not close round 155 needs a larger post; change `PW` and `PD` and the base follows.
- **Print:** both parts bottom down, no supports, no bridges. The post is a plain prism; its plan radii lie in the layer plane.

verify.py: both parts valid, watertight, one solid each; no interference; contact area 4205 mm²; motions as above.

Compared with well-known products in this style: none of them is a stand; they are housings with controls, a grille or
perforation, and this has none of those. Posts and cushions for watches are a common kind of object; no product was used as a model.

Safety: the stand has no batteries, LEDs, magnets or heat of its own.

Not verified:
- Not printed on a real printer.
- The post size suits one range of wrists; a very small or very large strap needs another post.
- How the 0.25 clearance of the pocket fits on your printer (settle it with a test piece of the post's foot and the pocket).
