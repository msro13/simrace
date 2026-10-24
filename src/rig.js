// Rule engine for the floor cockpit configurator.
// Turns a configuration into profile pieces, joints, fittings, a priced parts list and accessory placements.
// Units are millimetres. X runs forward from the rear end of the frame, Y up from the floor, Z to the driver's right.

export const DEFAULTS = {
  length: 1500,        // side rail length
  width: 640,          // outer width of the base frame (gives the seat the same side clearance as the HexRig)
  seatOffset: 0,       // seat brackets along the seat rails, + is forward
  seatRecline: 0,      // degrees
  wheelHeight: 710,    // top of the wheel deck above the floor
  wheelX: 650,         // centre of the uprights from the rear end
  wheelTilt: 0,        // degrees
  pedalX: 1300,        // centre of the pedal deck from the rear end
  pedalHeight: 'low',  // 'low' | 'medium' | 'high'
  pedalAngle: 0,       // 0 | 10 | 20 (nominal degrees)
  sideArm: 'right',    // 'none' | 'right' | 'left'
  monitorStand: 'rig', // 'none' | 'rig' | 'floor1' | 'floor3'
  monitorSize: '34uw',
  monitorHeight: 1070, // centre of the screen above the floor
  finish: 'natural',  // profiles: 'natural' | 'black'
  accent: 'grey',      // end caps and brackets: 'grey' | 'black', always follows finish
  led: false,
  ledColor: '#33ccff',
};

export const LIMITS = {
  length: [1300, 1800], width: [620, 720], seatOffset: [-90, 90], seatRecline: [0, 20],
  wheelHeight: [600, 850], wheelX: [550, 900], wheelTilt: [0, 20],
  pedalX: [800, 1600], monitorHeight: [950, 1200],
};

export const MONITORS = {
  '27': { label: '27"', w: 615, h: 365, triple: true },
  '32': { label: '32"', w: 730, h: 430, triple: true },
  '34uw': { label: '34" ultrawide', w: 829, h: 366, triple: false },
  '49suw': { label: '49" super ultrawide', w: 1200, h: 365, triple: false },
};

// Fixed layout constants
export const FOOT_H = 30;              // floor to the underside of the base frame
export const RAIL_TOP = FOOT_H + 80;   // 110
export const SEAT_RAIL_LEN = 600;
export const SEAT_X0 = 300;            // seat rails are centred here
export const SEAT_Y = RAIL_TOP + 40;   // top of the seat rails, where the seat brackets sit
export const PEDAL_SPAN = 240;         // centre distance between the two pedal bars
const PEDAL_RAISE = { low: 0, medium: 40, high: 120 };
const PEDAL_DELTA = { 0: 0, 10: 40, 20: 90 };
const ARM_LEN = 400, ARM_BRACKET_LEN = 180;

// Where each accessory model sits in the HexRig file, as the point the configurator places it by.
export const HEX_ANCHORS = {
  seat: [2127.5, 618, -260.3],      // underside centre of the seat brackets
  wheelDeck: [2480, 1176, -260.5],  // top centre of the wheel deck bar (wheel and wheel base hang off it)
  pedals: [3231.5, 778, -260.3],    // underside centre of the pedal base
  arm: [2114, 948, 102],            // rear, top, outer corner of the side arm (shifter and handbrake)
  monitor: [2610.2, 1537.9, -259.6],// centre of the screen
};

export const clamp = (v, [lo, hi]) => Math.min(hi, Math.max(lo, v));

export function normalize(input) {
  const c = { ...DEFAULTS, ...input };
  for (const k of Object.keys(LIMITS)) c[k] = clamp(Number(c[k]), LIMITS[k]);
  c.pedalX = clamp(c.pedalX, [Math.max(LIMITS.pedalX[0], c.wheelX + (c.monitorStand === 'rig' ? 360 : 180)), c.length - 200]);
  c.accent = c.finish === 'black' ? 'black' : 'grey';
  if (!MONITORS[c.monitorSize]) c.monitorSize = DEFAULTS.monitorSize;
  if (c.monitorStand === 'floor3' && !MONITORS[c.monitorSize].triple) c.monitorSize = '27';
  return c;
}

export function build(input, catalog) {
  const c = normalize(input);
  const pieces = [], joints = [], notes = [];
  const W = c.width, L = c.length, half = W / 2, inner = W - 80;
  const railZ = half - 20;

  // size = [x, y, z] extent of the piece's bounding box; profile is '4040' or '4080'
  const piece = (id, module, profile, size, center, extra = {}) => {
    const len = Math.max(...size);
    const p = { id, module, profile, len: Math.round(len), size, center, ...extra };
    pieces.push(p); return p;
  };
  const butt = (a, b) => joints.push({ type: 'butt', a: a.id, b: b.id, profile: a.profile }); // end of a meets a face of b
  const cross = (a, b) => joints.push({ type: 'cross', a: a.id, b: b.id, profile: a.profile === '4080' && b.profile === '4080' ? '4080' : '4040' });

  // Base frame
  const railL = piece('rail-left', 'base', '4080', [L, 80, 40], [L / 2, FOOT_H + 40, -railZ]);
  const railR = piece('rail-right', 'base', '4080', [L, 80, 40], [L / 2, FOOT_H + 40, railZ]);
  for (const [id, x] of [['cross-rear', 20], ['cross-front', L - 20]]) {
    const p = piece(id, 'base', '4080', [40, 80, inner], [x, FOOT_H + 40, 0]);
    butt(p, railL); butt(p, railR); p.closedEnds = 2;
  }

  // Seat mount
  const seatCross = [SEAT_X0 - 200, SEAT_X0 + 200].map((x, i) => {
    const p = piece(`seat-cross-${i + 1}`, 'seat', '4040', [40, 40, inner], [x, RAIL_TOP - 20, 0]);
    butt(p, railL); butt(p, railR); p.closedEnds = 2; return p;
  });
  for (const [id, z] of [['seat-rail-left', -183], ['seat-rail-right', 183]]) {
    const p = piece(id, 'seat', '4040', [SEAT_RAIL_LEN, 40, 40], [SEAT_X0, RAIL_TOP + 20, z]);
    for (const sc of seatCross) cross(p, sc);
  }

  // Wheel deck
  const upLen = c.wheelHeight - RAIL_TOP;
  const ups = [[-railZ, 'left'], [railZ, 'right']].map(([z, side]) => {
    const p = piece(`upright-${side}`, 'wheel', '4080', [80, upLen, 40], [c.wheelX, RAIL_TOP + upLen / 2, z]);
    butt(p, side === 'left' ? railL : railR); return p;
  });
  for (const u of ups) { u.closedEnds = 1; u.openEnd = 'max'; }
  const deck = piece('deck-bar', 'wheel', '4080', [80, 40, inner], [c.wheelX, c.wheelHeight - 20, 0]);
  butt(deck, ups[0]); butt(deck, ups[1]); deck.closedEnds = 2;
  notes.push('Wheel base plate on the deck bar (not from Mundo Perfil)');

  // Pedal deck: the rear bar sets the height, the front bar sits higher for an angle
  const rearRaise = PEDAL_RAISE[c.pedalHeight] ?? 0;
  const delta = PEDAL_DELTA[c.pedalAngle] ?? 0;
  const pedalBars = [['rear', c.pedalX - PEDAL_SPAN / 2, rearRaise], ['front', c.pedalX + PEDAL_SPAN / 2, rearRaise + delta]];
  for (const [name, x, raise] of pedalBars) {
    if (raise === 0) {
      const p = piece(`pedal-bar-${name}`, 'pedals', '4040', [40, 40, inner], [x, RAIL_TOP - 20, 0]);
      butt(p, railL); butt(p, railR); p.closedEnds = 2;
    } else {
      const p = piece(`pedal-bar-${name}`, 'pedals', '4040', [40, 40, W], [x, RAIL_TOP + raise - 20, 0]);
      const riser = raise - 40;
      if (riser <= 0) { cross(p, railL); cross(p, railR); }
      else for (const [rail, z, side] of [[railL, -railZ, 'left'], [railR, railZ, 'right']]) {
        const r = piece(`pedal-riser-${name}-${side}`, 'pedals', '4040', [40, riser, 40], [x, RAIL_TOP + riser / 2, z]);
        butt(r, rail); butt(r, p); r.closedEnds = 2;
      }
    }
  }

  // Shifter and handbrake arm, bolted to the outside of one upright
  if (c.sideArm !== 'none') {
    const s = c.sideArm === 'left' ? -1 : 1;
    const up = s < 0 ? ups[0] : ups[1];
    const x0 = c.wheelX + 40 - ARM_LEN;
    const arm = piece(`arm-${c.sideArm}`, 'arm', '4080', [ARM_LEN, 80, 40], [x0 + ARM_LEN / 2, SEAT_Y + 290, s * (half + 20)]);
    cross(arm, up);
    for (const [i, dx] of [[1, 20], [2, 180]]) {
      const b = piece(`arm-bracket-${i}`, 'arm', '4040', [40, 40, ARM_BRACKET_LEN], [x0 + dx, SEAT_Y + 310, s * (half + 40 + ARM_BRACKET_LEN / 2)]);
      butt(b, arm); b.closedEnds = 1; b.openEnd = s > 0 ? 'max' : 'min';
    }
    notes.push('Plate for the shifter and handbrake (not from Mundo Perfil)');
  }

  // Monitor stand. The screen hangs on the driver's side of its cross bar, just in front of the wheel base.
  const mon = MONITORS[c.monitorSize];
  const monitors = [];
  if (c.monitorStand === 'rig') {
    const px = c.wheelX + 200, postLen = c.monitorHeight + 20 - RAIL_TOP;
    const posts = [[-railZ, 'left', railL, ups[0]], [railZ, 'right', railR, ups[1]]].map(([z, side, rail, up]) => {
      const p = piece(`monitor-post-${side}`, 'monitor', '4040', [40, postLen, 40], [px, RAIL_TOP + postLen / 2, z]);
      butt(p, rail); p.closedEnds = 1; p.openEnd = 'max';
      // a short link to the upright at deck height keeps the post from rocking
      const link = piece(`monitor-link-${side}`, 'monitor', '4040', [140, 40, 40], [c.wheelX + 110, c.wheelHeight - 20, z]);
      butt(link, up); butt(link, p); link.closedEnds = 2;
      return p;
    });
    const bar = piece('monitor-bar', 'monitor', '4040', [40, 40, inner], [px, c.monitorHeight, 0]);
    butt(bar, posts[0]); butt(bar, posts[1]); bar.closedEnds = 2;
    monitors.push({ center: [px - 68, c.monitorHeight, 0], yaw: 0 });
    notes.push('VESA plate for the monitor (not from Mundo Perfil)');
  } else if (c.monitorStand === 'floor1' || c.monitorStand === 'floor3') {
    const sx = c.wheelX + 200, sz = half + 80;
    const feet = [[-sz, 'left'], [sz, 'right']].map(([z, side]) =>
      piece(`stand-foot-${side}`, 'monitor', '4080', [600, 40, 80], [sx, FOOT_H + 20, z]));
    const upLenS = c.monitorHeight + 40 - (FOOT_H + 40);
    const sups = feet.map((f, i) => {
      const p = piece(`stand-upright-${i ? 'right' : 'left'}`, 'monitor', '4080', [40, upLenS, 80], [sx, FOOT_H + 40 + upLenS / 2, f.center[2]]);
      butt(p, f); p.closedEnds = 1; p.openEnd = 'max'; return p;
    });
    const bar = piece('stand-bar', 'monitor', '4080', [40, 80, 2 * sz - 80], [sx, c.monitorHeight, 0]);
    butt(bar, sups[0]); butt(bar, sups[1]); bar.closedEnds = 2;
    monitors.push({ center: [sx - 68, c.monitorHeight, 0], yaw: 0 });
    if (c.monitorStand === 'floor3') {
      // side arms swing back towards the driver; screens face the seat
      const th = 50 * Math.PI / 180, armLen = Math.round(mon.w * 0.9);
      for (const [s, side, up] of [[-1, 'left', sups[0]], [1, 'right', sups[1]]]) {
        const start = [sx, c.monitorHeight, s * (sz + 40)];
        const dir = [-Math.sin(th), 0, s * Math.cos(th)];
        const mid = start.map((v, i) => v + dir[i] * armLen / 2);
        const arm = piece(`stand-arm-${side}`, 'monitor', '4040', [armLen, 40, 40], mid, { yaw: -s * (90 + 50) });
        joints.push({ type: 'angle', a: arm.id, b: up.id, profile: '4040' });
        arm.closedEnds = 1; arm.openEnd = 'max';
        const n = [-Math.cos(th), 0, -s * Math.sin(th)];
        monitors.push({ center: mid.map((v, i) => v + n[i] * 68), yaw: -s * 50 });
      }
    }
    notes.push(`VESA plate${monitors.length > 1 ? 's' : ''} for the monitor${monitors.length > 1 ? 's' : ''} (not from Mundo Perfil)`);
  }

  // Where the HexRig models go: a translation from their HexRig position, then a turn of `pitch` degrees
  // about the Z axis through `pivot` (right-handed, so a positive pitch lifts the front).
  // The seat reclines about the lowest point of its shell, the wheel plate hinges on the front edge of the deck bar,
  // and the pedal base rests on the rear bar.
  const s = c.sideArm === 'left' ? -1 : 1;
  const seatPos = [SEAT_X0 + c.seatOffset, SEAT_Y, 0];
  const deckPos = [c.wheelX, c.wheelHeight, 0];
  const pedalPos = [c.pedalX, RAIL_TOP + rearRaise, 0];
  const armPos = [c.wheelX + 40 - ARM_LEN, SEAT_Y + 330, s * (half + 40)];
  const move = (to, from) => to.map((v, i) => v - from[i]);
  const placements = {
    seat: { offset: move(seatPos, HEX_ANCHORS.seat), pivot: [seatPos[0] - 143, SEAT_Y + 40, 0], pitch: c.seatRecline },
    seatBrackets: { offset: move(seatPos, HEX_ANCHORS.seat) },
    wheel: { offset: move(deckPos, HEX_ANCHORS.wheelDeck), pivot: [c.wheelX + 40, c.wheelHeight, 0], pitch: -c.wheelTilt },
    wheelbase: { offset: move(deckPos, HEX_ANCHORS.wheelDeck), pivot: [c.wheelX + 40, c.wheelHeight, 0], pitch: -c.wheelTilt },
    pedals: { offset: move(pedalPos, HEX_ANCHORS.pedals), pivot: [c.pedalX - PEDAL_SPAN / 2, RAIL_TOP + rearRaise, 0], pitch: Math.atan2(delta, PEDAL_SPAN) * 180 / Math.PI },
    sideArm: c.sideArm === 'none' ? null : { offset: move(armPos, [HEX_ANCHORS.arm[0], HEX_ANCHORS.arm[1], s * HEX_ANCHORS.arm[2]]), mirrorZ: s < 0 },
    // the HexRig screen is 829 x 366 mm; other sizes stretch it across (Z) and up (Y)
    monitors: monitors.map(m => ({ center: m.center, yaw: m.yaw, width: mon.w / 829, height: mon.h / 366 })),
  };

  return { config: c, pieces, joints, notes, placements, pedalAngleReal: Math.atan2(delta, PEDAL_SPAN) * 180 / Math.PI, ...priceList(c, pieces, joints, monitors, catalog) };
}

// Fittings, caps, feet and prices
export function priceList(c, pieces, joints, monitors, catalog) {
  const parts = Object.fromEntries(catalog.parts.map(p => [p.id, p]));
  const prof = Object.fromEntries(catalog.profiles.map(p => [p.id, p]));
  const lines = new Map();
  const add = (id, qty, why) => {
    if (!qty) return;
    const l = lines.get(id) || { id, qty: 0, why: new Set() };
    l.qty += qty; l.why.add(why); lines.set(id, l);
  };
  for (const j of joints) {
    if (j.type === 'angle') { add('QC45', 2, 'angled monitor arms'); continue; }
    if (j.profile === '4080') { add('BR4080', 2, 'joints between 40x80 profiles'); add('HB-M8x20', 8, 'bolts for 40x80 brackets'); add('FN-M8', 8, 'bolts for 40x80 brackets'); }
    else add('BR4040-SET', 2, j.type === 'butt' ? 'butt joints with 40x40' : 'profiles bolted across each other');
  }
  let caps40 = 0, caps80 = 0;
  for (const p of pieces) {
    const open = 2 - (p.closedEnds || 0);
    if (p.profile === '4080') caps80 += open; else caps40 += open;
  }
  const capSuffix = c.accent === 'black' ? ' (black)' : '';
  add('CAP4040', caps40, 'open 40x40 ends' + capSuffix);
  add('CAP4080', caps80, 'open 40x80 ends' + capSuffix);
  const feetPerRail = Math.ceil(c.length / 750) + 1;
  const standFeet = c.monitorStand.startsWith('floor') ? 4 : 0;
  add('FOOT-M8-40', 2 * feetPerRail + standFeet, 'levelling feet in the bottom slot');
  add('TN-M8', 2 * feetPerRail + standFeet, 'nuts for the feet');
  add('TN-M8', 4, 'wheel base plate');
  add('TN-M6', 8, 'seat brackets');
  add('TN-M6', 4, 'pedals');
  if (c.sideArm !== 'none') add('TN-M6', 8, 'shifter and handbrake');
  add('TN-M6', 4 * monitors.length, 'monitor mounts');
  if (c.led) add('SLOT-LED', 2 * Math.ceil(c.length / 2000), 'clear slot cover for LED strips, 2 m pieces');

  const fittings = [...lines.values()].map(l => {
    const p = parts[l.id];
    return { id: l.id, name: p.name, url: p.url, qty: l.qty, unit: p.price, total: round2(l.qty * p.price), why: [...l.why].join(', ') };
  });
  const cut = {};
  for (const p of pieces) (cut[p.profile] ||= []).push(p.len);
  const finishFactor = c.finish === 'black' ? (catalog.black?.price_factor ?? 1) : 1; // no black CS10 profile is listed yet
  const profiles = Object.entries(cut).map(([k, lens]) => {
    const pr = prof[k === '4040' ? 'P4040-CS10' : 'P4080-CS10'];
    const m = lens.reduce((a, b) => a + b, 0) / 1000;
    const perMetre = round2((pr.price_per_m ?? pr.placeholder_price_per_m) * finishFactor);
    return { id: pr.id, name: pr.name, url: pr.url, finish: c.finish, pieces: lens.length, metres: round2(m), perMetre,
             placeholder: pr.price_per_m == null, total: round2(m * perMetre), kg: round2(m * pr.kg_per_m),
             cuts: lens.slice().sort((a, b) => b - a) };
  }).sort((a, b) => a.id.localeCompare(b.id));
  const fittingsTotal = round2(fittings.reduce((a, f) => a + f.total, 0));
  const profilesTotal = round2(profiles.reduce((a, p) => a + p.total, 0));
  const kg = round2(profiles.reduce((a, p) => a + p.kg, 0));
  // Proposed kit price: the catalogue total less the kit discount, then VAT (see "kit" in the catalog)
  const catalogue = round2(profilesTotal + fittingsTotal);
  const kit = catalog.kit ?? { discount: 0, vat: 0.21 };
  const discount = round2(catalogue * kit.discount);
  const net = round2(catalogue - discount);
  const vat = round2(net * kit.vat);
  return { profiles, fittings, totals: { profiles: profilesTotal, fittings: fittingsTotal, catalogue, discountRate: kit.discount, discount, net, vatRate: kit.vat, vat, gross: round2(net + vat), kg } };
}

const round2 = v => Math.round(v * 100) / 100;
