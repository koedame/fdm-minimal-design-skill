# 009 Key rail

A plain bar on the wall by the door that holds keys by their steel rings. Five magnets sit in blind holes from the back,
0.84 behind the front face, so the front is one unbroken face. Two keyholes for countersunk screws are pocketed in the back.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Bar | 160 × 32 × 12 | 5:1 face; 12 deep takes the magnets and the keyhole pockets |
| Face radius | R4 | 12.5% of 32 |
| Magnets | 5 × Ø10 × 3 in Ø10.2 blind holes, pitch 32, 16 from the ends | Larger than the rule's 6 × 3 (same +0.2 hole) to pull through the skin; one key ring per magnet |
| Skin in front of the magnets | 0.84 | Thin for the pull; 4 layers at 0.2 still print a closed face on the bed |
| Keyholes | x ±48 (96 apart), entry Ø8.4 at 12 up, slot 4.2 wide rising 8 | The wall mounting rule's sizes; the bar is hung on two screws and dropped 8 onto them |
| Keyhole pocket | Ø8.4 head pocket 3 deep, 45° seat to the 4.2 slot, 2.0 ledge at the back | Departs from the rule (head relief on the wall-side face): the front must stay unbroken over the magnets, and in a 12 deep bar the head can sit inside. The countersunk head seats on the 45° cone, and face-down printing needs no support |
| Chamfers | 0.6 on the front (bed side), 0.5 on the back | As every part |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| rail | Front face down (the magnet holes and keyholes open upward) | Off-white |
| magnets_ref × 5 | Bought: Ø10 × 3 disc magnets | — |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| rail | Keyhole slot 4.4 wide, wider than the wall mounting rule's 4.2 | Rule violation | 4.2 |

Use cases:
- **Mount:** drive two countersunk screws (head up to Ø8) 96 apart, level, leaving about 2.5 mm of the head standing off the wall;
  put the bar over the heads at the entry holes and let it drop 8 mm.
- **Use:** touch a key ring to the face over a magnet; pull the key down and away to take it.
- **Assemble:** glue a Ø10 × 3 magnet to the bottom of each blind hole from the back, before mounting.
- **Print:** front face down, so the front is the smooth bed face and the 45° keyhole seats need no support.

verify.py: valid and watertight, fits a 256 bed. (The ground-contact line is not meaningful: the bar hangs on the wall.)

Compared with well-known products in this style: none of them is a wall rail; a plain bar with hidden magnets
is not taken from any product. No product was used as a model.

Safety (magnets, wall mounting): neodymium magnets are dangerous if swallowed, above all two or more. Glue them in fully, mount the
bar out of reach of small children, and do not use it if a magnet comes loose. Keep the bar away from cards with magnetic stripes and
from pacemakers. Hang it on screws in a stud, or in plugs or plasterboard anchors made for your wall; the hold of the printed keyholes
has not been tested, so before use pull the bar down by hand, harder than your keys weigh.

Not verified:
- Not printed on a real printer.
- How strongly a key ring holds through 0.84 of plastic (depends on the magnet grade and the ring).
- Whether a light-coloured 0.84 skin shows the magnets through it.
