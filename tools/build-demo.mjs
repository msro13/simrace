// Builds the demo page from demo/page.html: node tools/build-demo.mjs
// Writes demo/index.html, which opens on its own in a browser, and demo/artifact.html, the same page without the
// document wrapper, for publishing. Both carry rig.js, the catalog and the 3D models inline; three.js comes from jsDelivr.
// --local loads three.js from /node_modules/three instead, for testing with a local web server (--out=FILE sets where it goes).
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';

const root = new URL('../', import.meta.url);
const read = p => readFileSync(new URL(p, root), 'utf8');
const local = process.argv.includes('--local');
const out = process.argv.find(a => a.startsWith('--out='))?.slice(6);

const rig = read('src/rig.js').replace(/^export /gm, '');
const catalog = JSON.parse(read('catalog/mundoperfil-catalog.json'));
const models = Object.fromEntries(readdirSync(new URL('models/web/', root)).filter(f => f.endsWith('.glb')).sort()
  .map(f => [f.slice(0, -4), readFileSync(new URL(`models/web/${f}`, root)).toString('base64')]));
const three = local ? '/node_modules/three/' : 'https://cdn.jsdelivr.net/npm/three@0.170.0/';
const importmap = { imports: { three: `${three}build/three.module.min.js`, 'three/addons/': `${three}examples/jsm/` } };

// function replacements, so the $ signs in the code stay as they are
const page = read('demo/page.html')
  .replace('/*@IMPORTMAP@*/', () => JSON.stringify(importmap))
  .replace('/*@MODELS@*/', () => JSON.stringify(models))
  .replace('/*@RIG@*/', () => rig)
  .replace('/*@CATALOG@*/', () => JSON.stringify(catalog));

// The publishing skeleton adds the doctype, charset, viewport and these basics; the standalone page needs them itself
const standalone = `<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
${page}
</body>
</html>
`;

if (out) writeFileSync(out, standalone);
else {
  writeFileSync(new URL('demo/index.html', root), standalone);
  writeFileSync(new URL('demo/artifact.html', root), page);
}
console.log(`Built ${out ?? 'demo/index.html and demo/artifact.html'}: ${(standalone.length / 1e6).toFixed(2)} MB, ${Object.keys(models).length} models, three.js from ${three}`);
