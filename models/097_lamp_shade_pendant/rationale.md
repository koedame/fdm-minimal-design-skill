# 097 Pendant lamp shade

A drum shade Ø160 × 160 for a ceiling pendant: a translucent PETG tube whose top narrows at 45° to a Ø80 opening with a short
collar. It hangs from an E26 lamp socket on a cap: the socket's shade ring clamps the cap, the cap's 45° rim carries the shade on the
inside of its shoulder, and a DIV lip on the cap rises through the opening, 0.25 inside the collar, so the shade is centred and the
top shows one even ring round the socket. Two printed parts; the socket, cord and bulb are bought.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Outline | Ø160 × 160 | 40 modules; height = diameter; holds a Ø60 × 100 LED bulb with 18 of air all round |
| Shoulder | 45° from R80 at z 116 to R40 at z 156; collar R40, 4 high | Prints upright without supports; the opening is half the diameter |
| Shade wall | DIV (1.68) everywhere, one turned profile | Thin enough to diffuse in white PETG (as 10_lantern's diffuser), four lines thick |
| Cap | Ø86.8 plate 2.4, top at z 152; rim 45°, bearing on the shoulder's inner cone | The rim and the shoulder share one angle, so the shade sits on the cap along a whole cone and centres itself under its own weight |
| Lip | DIV, from the cap's top up to the shade's top (8 high), 0.25 inside the collar | Location as in the rules; flush with the collar's top, so the collar and the lip read as one ring with a 0.25 reveal |
| Socket hole | Ø40.5 | For a socket whose threaded shell is about Ø40 and whose shade ring clamps a plate (check yours) |
| Edges | C0.5 on the collar's and lip's top edges; C0.6 on the outside of the shade's bed edge and on the cap's bed edges | One visible chamfer value; the shade's bed chamfer is outside only (see review) |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| shade | Bottom down (upright) | White translucent PETG |
| cap | Bottom down | Off-white, opaque |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| shade | C0.6 on both sides of a 1.68 wall left a 0.48 ring on the bed: a 1.2 m-long first layer of one line, easily knocked loose on a 160-high print | Defect | The bed chamfer is on the outside only (1.08 on the bed); the elephant's foot inside is not seen. Written into the rules |
| bulb envelope | The first envelope put the socket body under the cap; an E26 socket hangs above its shade ring, so the bulb sat 15 too high in the check | Defect (in the check) | Socket body above the cap, ring and shell 15 below it; the bulb (Ø60 × 100) clears the shade and the cap with the cap in place |

Dos and Don'ts: one wall thickness, one angle (45°) for the shoulder and the cap's rim, one visible chamfer value; one seam (the
reveal round the socket); plain drum, the collar and lip as the one worked-out spot; white, no accent.

Use cases:
- **Fit:** take the shade ring off the socket, pass the cap over the cord and the socket from below, put the ring back and tighten it.
  Pass the cord down through the shade's opening and let the shade drop over the cap: it lands on the 45° rim and the lip finds the
  opening. Then fit the bulb from below.
- **Change the bulb:** reach in from below; the bulb is 34 above the shade's lower edge, so the shade stays on.
- **Clean:** lift the shade off upwards over the cap (it only rests on it) and wipe it; rinse it if it is dusty, dry it before it goes back.
- **Print:** shade upright, bottom down, 45° shoulder; cap bottom down. No supports. White PETG for the shade.

verify.py: shade and cap valid, watertight, fit a 256 bed; the shade lifts free off the cap, rests on it (stop at 0.3 down) and stops
sideways at 0.4. The bulb envelope overlaps neither part.

Safety:
- **LED bulbs only, up to about 7 W (60 W-equivalent).** An incandescent or halogen bulb heats PETG past its softening point (about 80 °C);
  PLA softens at about 60 °C and is not suitable for the shade or the cap. No heat calculation was made.
- Use a certified socket, cord and ceiling fitting, wired by a qualified person where your local rules require it. The printed parts carry
  only their own weight; the cord and the socket carry the lamp.
- Check that the bulb's base and the socket's shell stay below about 50 °C after an hour on; if the cap is soft or discoloured, stop using it.

Compared with well-known products in this style: radios, a pocket radio, a calculator and a loudspeaker; none is a lamp.
A drum shade with a sloped shoulder is a common pendant form; no product was used as a model.

Not verified:
- Not printed on a real printer.
- How evenly a 1.68 white PETG wall diffuses the bulb, and whether a hot spot shows on the shoulder.
- Whether your socket's shade ring clamps a 2.4 plate with a Ø40.5 hole; socket sizes vary.
- The temperature of the cap and shade after hours on with a 7 W LED bulb.
