# Cockpit Configurator

A sim racing cockpit configurator, in Spanish, built on Mundo Perfil (mundoperfil.com) aluminium profiles. You pick the options, see the cockpit in 3D and get the priced parts list.

- **Website:** https://msro13.github.io/simrace/ (published by GitHub Pages from `main`, see .github/workflows/pages.yml)
- **Spec:** "Floor cockpit spec" doc, https://claude.ai/artifact/QUJdCovTLyD9eT3aiGWmGJ
- **catalog/**: Mundo Perfil parts and prices (mundoperfil-catalog.json), plus the HexRig frame cut list and estimate.
- **src/rig.js**: the rule engine. It turns a set of options into profile pieces, joints, fittings, a priced parts list and where each 3D model goes. The 3D demo uses the same file.
- **tools/bom.mjs**: prints the parts list for any options from the command line, for example
  `node tools/bom.mjs length=1600 pedalHeight=high`
- **Demo link (private):** https://claude.ai/artifact/VW1A4K7bKGWcNWpkUj9GNF
- **Proposal for Mundo Perfil (private):** "Propuesta para Mundo Perfil" doc, in Spanish, https://claude.ai/artifact/LHsoZrJRHzicsn1VKgSyK2. Its annex is the example quote for the GT build. Export it to PDF or Word from the doc.
- **demo/index.html**: the 3D configurator. Double-click it to open it in a browser (it needs internet for three.js and the fonts).
- **demo/page.html**: the source of the demo page. Edit this one, not index.html.
- **tools/build-demo.mjs**: rebuilds the demo after a change to page.html, rig.js, the catalog or the models:
  `node tools/build-demo.mjs`
  It writes demo/index.html and demo/artifact.html (the same page without the document wrapper, for publishing as a Claude Artifact).
- **models/web/**: the slimmed HexRig models (seat, wheel, pedals, shifter, handbrake, screen) that the demo shows.

Run the tools from this folder; they need Node.js 18 or newer. No npm install is needed.

Units are millimetres. X runs forward from the rear end of the frame, Y up from the floor, Z to the driver's right.
Catalogue prices exclude VAT. Profiles cost 13 €/m (40x40) and 27 €/m (40x80), the Mundo Perfil cart price for a 1000 mm piece.
The demo's total is a proposed kit price, not a Mundo Perfil price: the catalogue total less 41 %, plus 21 % VAT (`kit` in the catalog). With it the Esencial preset, the default cockpit without a monitor stand, costs 349,84 € with VAT, about the 350 € that comparable commercial rigs cost (Homes, 24 October). The parts list keeps catalogue prices. If the 350 € target should be without VAT, the discount is 29 % instead.
Profiles can be natural or black. Mundo Perfil lists no black CS10 profile yet, so black is priced like natural (`black` in the catalog).

## Where things stand (24 October 2026)

1. Parts catalog: done.
2. Rig design, rules and prices: done. The default build (GT) is 21 cuts and 262 fittings: 591,94 € at catalogue price without VAT, 422,58 € with the kit discount and VAT.
3. Clickable 3D demo: built and working, with the whole page in Spanish from Spain (Homes asked for this on 23 October). It has the options panel, five presets (Esencial, GT, Fórmula, Rally, Triple pantalla), the live price with VAT and the kit discount, the cut list and accessories with links, camera views (Órbita, Lateral, Superior, Piloto), tap a profile to see its cut length, natural or black profiles, and LED and colour options.
   Checked in headless Chromium (desktop light, desktop dark, phone dark): it loads with no console errors, the totals match tools/bom.mjs for all five presets (Esencial 349,84 €, GT 422,58 €, Fórmula 412,15 €, Rally 429,44 €, Triple pantalla 514,79 €, with VAT), the black finish works, and the Piloto view and tap-a-profile work. Not yet tried on a real phone or in Safari or Firefox.
4. Pitch package: in progress. The proposal doc is written in Spanish: the idea, what the demo does, what Mundo Perfil gains, seven points for them to confirm (the kit price and cutting, shipping, catalogue data, how orders arrive, black profiles, the three plates, the business model) and next steps. Its annex is the printable quote for the Esencial build: cut list, fittings, 490,04 € at catalogue price, the 41 % kit discount and VAT, 349,84 € in total.
   Still to do: try the demo on a real phone and in Safari or Firefox, then review the proposal and send it. Both links are private, so share them before sending.

## How the demo is put together

- page.html holds the layout, styles and code. The build drops rig.js, the catalog and the models (as base64) into it, so index.html works as a single file.
- All text is Spanish from Spain, written straight into page.html. Part names are the Mundo Perfil catalogue names. rig.js still writes its notes in English, so the names of the profile pieces and the "También necesitas" notes are translated near the top of the script (PIECE_NAMES and NOTES). Prices use the Spanish format, 591,94 €.
- The 3D view uses three.js 0.170.0 from cdn.jsdelivr.net. If the 3D view cannot start, the options, price and parts list still work.
- Each profile is a real 40x40 or 40x80 T-slot section drawn from code (sectionOutline in page.html), stretched to its cut length. Brackets and end caps are placed from the joints that rig.js returns.
- The HexRig models are moved into place with the `placements` from rig.js: a shift from their HexRig position, then a turn about a pivot (seat recline, wheel tilt, pedal angle).
