// Prints the parts list for a configuration: node tools/bom.mjs length=1600 pedalHeight=high (a JSON object works too)
import { readFileSync } from 'node:fs';
import { build } from '../src/rig.js';

const catalog = JSON.parse(readFileSync(new URL('../catalog/mundoperfil-catalog.json', import.meta.url)));
const args = process.argv.slice(2).filter(a => a !== '--json');
const value = v => v === 'true' ? true : v === 'false' ? false : v !== '' && !isNaN(Number(v)) ? Number(v) : v;
const cfg = args[0]?.startsWith('{') ? JSON.parse(args[0]) : Object.fromEntries(args.map(a => a.split('=')).map(([k, v]) => [k, value(v)]));
const r = build(cfg, catalog);
if (process.argv.includes('--json')) { console.log(JSON.stringify(r, null, 1)); process.exit(0); }
console.log('Profiles');
for (const p of r.profiles) console.log(`  ${p.id}  ${p.pieces} pieces  ${p.metres} m  ${p.perMetre} €/m${p.placeholder ? ' (placeholder)' : ''}  = ${p.total} €   cuts: ${p.cuts.join(', ')}`);
console.log('Fittings');
for (const f of r.fittings) console.log(`  ${String(f.qty).padStart(3)} x ${f.id.padEnd(11)} ${f.unit.toFixed(2)} € = ${f.total.toFixed(2).padStart(7)} €  ${f.why}`);
console.log('Totals', r.totals);
console.log('Pieces');
for (const p of r.pieces) console.log(`  ${p.id.padEnd(24)} ${p.profile} ${String(p.len).padStart(5)} mm  centre ${p.center.map(v => Math.round(v)).join(', ')}`);
console.log('Notes', r.notes);
