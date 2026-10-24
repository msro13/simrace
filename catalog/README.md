# Step 1: Mundo Perfil parts catalog

Collected from mundoperfil.com on 23 Oct 2026. All prices are in euros without VAT (IVA no incluido), as the site lists them.

## Files

| File | What it holds |
|---|---|
| `mundoperfil-catalog.json` | 3 profiles and 27 fittings (brackets, connectors, T-nuts, bolts, caps and feet), each with its name, link, price, specs and its job in a cockpit. The configurator reads this file. |
| `hexrig-frame-cutlist.csv` | Every profile in your HexRig cockpit frame matched to a Mundo Perfil profile, with its cut length, position in the model and how its ends connect. |
| `hexrig-frame-estimate.json` | What the HexRig cockpit frame would cost and weigh if it were built from Mundo Perfil parts. |

## What I found

**Profiles.** The grey line is compatible with Bosch Rexroth and has a 10 mm slot (they call it CS10). Both sizes a cockpit needs are available in natural aluminium:

| Profile | kg/m | Ix / Iy (cm⁴) |
|---|---|---|
| 40x40 CS10 | 1.5 | 9.1 / 9.1 |
| 40x80 CS10 | 2.7 | 63.4 / 17.3 |

Both can be ordered cut to length. Two machining options are available: holes for hidden quick connectors, and a core thread for feet.

**Black is limited.** The only black profile is a 40x40 with a 6 mm slot, which belongs to a different system, so CS10 brackets and nuts don't fit it. There is no black 40x80. End caps and 40x80 brackets do come in black, though. For the colour option, I suggest a natural aluminium frame with grey or black accents. Asking whether they could anodise CS10 profiles black is a good question for the pitch.

**Profile prices are hidden.** The site only shows a profile's price in the cart, after you enter a length. For a 1000 mm piece the cart shows 13 € for 40x40 and 27 € for 40x80 (checked on 23 Oct 2026), so the catalog uses 13 €/m and 27 €/m. Brackets, nuts, caps and feet have real listed prices.

**Your HexRig cockpit frame.** This is the 40x40 and 40x80 frame that sits on the motion base. It has:
- 18 pieces of 40x40, totalling 8.23 m
- 8 pieces of 40x80, totalling 5.50 m
- 12 butt joints and 23 places where profiles are bolted side by side
- 40 open ends that need caps

Built from Mundo Perfil parts, it would cost about **578 €**. That is 322 € of fittings plus 256 € of profile. It would weigh about 33 kg. The fitting count assumes 2 brackets per joint. Step 2 will place each bracket individually.

**3D models we can reuse in the demo.** Your assembly already contains the SPARCO seat, the MOZA F1 wheel and R9 base, the MOZA shifter, the rally handbrake, the load-cell pedals and the monitor.

## Still open
- The prices of the black end caps. They're listed on the profile pages without a price.
