# 009 Key rail

A plain bar on the wall by the door that holds keys by their steel rings. Five magnets sit in blind holes from the back,
0.84 behind the front face, so the front is one unbroken face. Two keyholes for countersunk screws are pocketed in the back.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Bar | 160 × 32 × 12 | 5:1 face; 12 deep takes the magnets and the keyhole pockets |
| Face radius | R4 | 12.5% of 32 |
| Magnets | 5 × Ø10 × 3 in Ø10.2 blind holes, pitch 32, 16 from the ends | One key ring per magnet with room between |
| Skin in front of the magnets | 0.84 | Thin for the pull; 4 layers at 0.2 still print a closed face on the bed |
| Keyholes | x ±48 (96 apart), entry Ø8.4 at 12 up, slot 4.4 wide rising 8 | The bar is hung on two screws and dropped 8 onto them |
| Keyhole pocket | Ø8.4 head pocket 3 deep, 45° seat to the 4.4 slot, 2.0 ledge at the back | The countersunk head seats on the 45° cone; face-down printing needs no support |
| Chamfers | 0.6 on the front (bed side), 0.5 on the back | As every part |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| rail | Front face down (the magnet holes and keyholes open upward) | Off-white |

## Review

No defects or rule violations found.

Use cases:
- **Mount:** drive two countersunk screws (head up to Ø8) 96 apart, level, leaving about 2.5 mm of the head standing off the wall;
  put the bar over the heads at the entry holes and let it drop 8 mm.
- **Use:** touch a key ring to the face over a magnet; pull the key down and away to take it.
- **Assemble:** glue a Ø10 × 3 magnet to the bottom of each blind hole from the back, before mounting.
- **Print:** front face down, so the front is the smooth bed face and the 45° keyhole seats need no support.

verify.py: valid and watertight, fits a 256 bed. (The ground-contact line is not meaningful: the bar hangs on the wall.)

Compared with well-known products (SK 4, T 3, ET 66, SK 61, L 2): none of them is a wall rail; a plain bar with hidden magnets
is not taken from any product. No product was used as a model.

Safety (magnets): neodymium magnets are dangerous if swallowed, above all two or more. Glue them in fully, mount the bar out of
reach of small children, and do not use it if a magnet comes loose. Keep the bar away from cards with magnetic stripes and from
pacemakers.

Not verified:
- Not printed on a real printer.
- How strongly a key ring holds through 0.84 of plastic (depends on the magnet grade and the ring).
- Whether a light-coloured 0.84 skin shows the magnets through it.
