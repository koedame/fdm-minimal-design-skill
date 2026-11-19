# 010 Letter rack

Three upright dividers, 48, 72 and 96 high, doweled and glued into a low base. The rack rises toward the back, so every
compartment shows what is in it. The dividers are printed flat on their sides, which gives smooth faces and layers that run
along their length.

## Dimensions

| Dimension | Value | Reason |
|---|---|---|
| Base | 160 × 96 × 8 | 5:3 plan |
| Base radius | R12 | 12.5% of 96 |
| Dividers | 144 long (8 in from each end), 6 thick | 6 leaves 1.4 of wall on each side of a Ø3.2 hole |
| Divider heights | 48, 72, 96, front to back | Steps of 24; the tallest equals the base depth |
| Divider pitch | 30 (24 compartments) | A stack of letters or a slim notebook per compartment |
| Divider edges | full round top and ends (R3), C0.5 at the joint | Free ends get full rounds; the joint is half of a V line |
| Dowels | 2 per divider at x ±48, Ø3 × 16 steel, holes Ø3.2 | The split joint rule (hole +0.2, glued) with a 3 mm pin, since the divider is 6 thick |
| Hole depths | 6.5 in the base, 10 in the divider | 16.5 for a 16 pin; 1.5 of base under each hole |
| Rubber feet | 4 × Ø10.2 at x ±64, y ±36 | Inside the base outline |

## Parts

| Part | Orientation | Colour |
|---|---|---|
| base | Bottom down, as used | Off-white |
| divider_48, divider_72, divider_96 | On their side, the front face down; the dowel holes are horizontal teardrops with the 45° roof up | Off-white |
| dowels_steel_ref (× 6) | Reference only, do not print (Ø3 × 16 steel dowel pins) | Dark grey |

## Review

| Target | Problem | Kind | Fix |
|---|---|---|---|
| base, dividers | Dowel holes were Ø3.1, tighter than the split joint rule (hole = pin + 0.2, glued) | Rule violation | Ø3.2 |

Use cases:
- **Use:** letters, envelopes and slim notebooks stand in the three compartments; a 120 × 235 envelope stands on its long edge
  and overhangs the dividers at the ends.
- **Assemble:** glue the dowels into the base, put glue on the divider's bottom edge and push it onto the dowels.
- **Clean:** nothing to catch dust except the base between the dividers, 24 wide.
- **Print:** base bottom down; dividers on their sides with the teardrop holes roof up; no supports.

verify.py: all parts valid and watertight, no interference, fit a 256 bed, ground contact 14628 mm² over 158.9 × 94.9 mm.

Compared with well-known products in this style: none of them is a letter rack; stepped upright dividers on a
base are a generic office form, and no product was used as a model.

Not verified:
- Not printed on a real printer.
- How stiff the 96 divider is against a sideways push on a glued joint 6 wide.
