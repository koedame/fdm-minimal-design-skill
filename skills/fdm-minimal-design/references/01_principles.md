# 01 Principles: why the form looks like this language, and looks refined

The thinking behind the rules (02) and the Dos and Don'ts (03). When a rule leaves you unsure, come back here.

The subject is the design language this skill is inspired by (see the introduction of `SKILL.md`): one shared across a family of household appliances, audio equipment, clocks and calculators from the 1950s to the 1970s.
It is not for reproducing any particular product; it is for applying the **thinking** to your own designs.

---

## 1. The four elements of the language

In order of impact. The first two alone get the impression a long way.

1. **Form: large radii in plan, sharp edges**
   - Round the corners of the outline seen from above (the plan) with a generous, constant radius.
   - Leave the edges along the thickness almost unrounded, standing crisp.
   - The core is the combination of a "soft outline" and a "thickness with crisp edges". Put a large fillet on every edge and you get the shape of a generic appliance.
2. **Layout: a grid**
   - Make the outline, hole pitch and button positions multiples of one module (4 mm, for example).
   - Viewers do not measure, but they sense unconsciously that things line up.
3. **Colour: nearly achromatic, plus one accent**
   - The body is off-white or light grey, secondary parts dark grey.
   - Use only one chromatic colour, in only one place that carries a functional meaning (power, second hand and so on).
4. **Controls: repetition of one shape**
   - Line up buttons of the same shape and the same size. Show differences with colour.
   - A dial gets one step and one indicator line, nothing more.

On top of these, some **details** strongly shape the finished impression.

- Small holes in a dense array (a few large holes look like a toy)
- Seams between parts as intended reveal lines
- Labels tiny, light grey, sans-serif
- Material changes switched by face (an aluminium-look front plate on a matte plastic housing, for example)

---

## 2. Does simple look "lazy" or "refined"?

The difference is **whether the viewer can tell why the form is the way it is**.
With the same small number of elements, refined simplicity looks like "the result of choices", and lazy simplicity looks like "the result of doing nothing". The gap comes from these six points.

| Aspect | Looks lazy | Looks refined |
|---|---|---|
| 1. Precision | Gap widths vary, faces warp, edge treatment differs from place to place | Gaps constant all round, faces flat, treatment consistent |
| 2. System of dimensions | CAD defaults, round numbers, "just centre it" | Every dimension derived from the grid, ratios and line width |
| 3. Density of detail | Uniformly shallow everywhere | Mostly plain, with a few spots worked out to an unusual degree |
| 4. Edge treatment | Left sharp (chips on FDM), or a large radius all round (a bar of soap) | A small chamfer: "crisp, but treated" |
| 5. Margins | Whatever is left after placing elements | Margins of equal width, or aligned to clear reference lines |
| 6. Surface and colour | Layer lines, seams, stringing, uneven gloss, pure white or primary colours | An even surface, slightly muted colours |

**The fewer the elements, the higher the precision required.** Errors that would hide in a busy design become the main subject in a simple form.

Density of detail (3) has the strongest effect. A few precise details make the plain areas read as "deliberately left alone". When everything is shallow, everything looks lazy.

### How to judge your own form

- **Can you give a reason for every dimension?** Wherever "left at the default" or "felt right" remains is where it will look lazy.
- **Do not judge on the CAD screen.** Simple forms almost always look clean on screen. Judge the gaps and edges on a full-size print.

---

## 3. How to think when fitting it to FDM (fused deposition modelling)

- **"Large radii in plan, sharp edges" suits the nature of FDM well.** Curves in the XY plane (the layer plane) come out cleanly, while small radii in Z turn into steps. Put the plan on the build plate and you get the rounded outline and the crisp edges for free.
- **Put the visible face on the build plate.** It comes out smoothest, and holes and lettering are more accurate there. The exception is a part whose visible face has steps or recesses (the ceiling of a recess becomes a bridge).
- **Design on the assumption that parts are split.** Splitting lets you choose the best print orientation per part, gives you colour separation, and gives you reveal lines at the same time.
- **Do not make closed boxes.** A box printed bottom down turns its whole top into a ceiling. Put a separate lid on a sleeve-shaped body.

---

## 4. Do not apply the rules mechanically

Learn each rule together with "why". Applied without its reason, a rule creates defects.

Things that actually happened:
- **Full-round ends:** the rule "plate ends are nearly full round" was applied to the bottom end of a leg that stands on the ground, and the contact width became 1.9 mm. Full rounds are for ends that float in the air; ends that touch the ground stay flat.
- **Label colour:** the person who wrote the rule "labels are light grey" made their own model with black labels. Without checking against the checklist, even the author misses it.

Judge with the Dos and Don'ts (03) and the review procedure (04).
