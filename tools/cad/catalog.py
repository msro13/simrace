import json, csv, sys, math
S, OUT = sys.argv[1], sys.argv[2]
U = "https://mundoperfil.com/productos/"
# Profile prices only show in the cart. Homes read them for a 1000 mm piece on 2026-10-23.
CART_NOTE = "Cart price for a 1000 mm piece, read by Homes on 2026-10-23"
catalog = {
  "source": "mundoperfil.com",
  "retrieved": "2026-10-23",
  "currency": "EUR",
  "prices": "excluding VAT (IVA no incluido), as listed on the product pages",
  "profiles": [
    {"id": "P4040-CS10", "name": "Perfil de aluminio modular 40×40 CS10 ranura 10mm", "url": U+"perfil-aluminio-ranurado-40x40/",
     "section_mm": [40, 40], "slot_mm": 10, "open_slots": 4, "finish": "natural", "kg_per_m": 1.5, "area_cm2": 5.6,
     "Ix_cm4": 9.1, "Iy_cm4": 9.1, "It_cm4": 1.3, "Wx_cm3": 4.5, "Wy_cm3": 4.5, "Wt_cm3": 0.74,
     "machining_options": ["Quick-connector holes: no / 1 end / both ends", "M12 core thread for feet: no / yes"],
     "price_per_m": 13.00, "price_note": CART_NOTE},
    {"id": "P4080-CS10", "name": "Perfil aluminio ranurado 40×80 CS10 ranura 10mm", "url": U+"perfil-aluminio-ranurado-40x80/",
     "section_mm": [40, 80], "slot_mm": 10, "open_slots": 6, "finish": "natural", "kg_per_m": 2.7, "area_cm2": 9.9,
     "Ix_cm4": 63.4, "Iy_cm4": 17.3, "It_cm4": 8.02, "Wx_cm3": 15.9, "Wy_cm3": 8.7, "Wt_cm3": 4.8,
     "machining_options": ["Quick-connector holes: no / 1 end / both ends", "Core thread for feet: no / yes"],
     "shipping_note": "Bars over 2400 mm have a higher shipping rate",
     "price_per_m": 27.00, "price_note": CART_NOTE},
    {"id": "P4040-BLK-S6", "name": "Perfil extruido 40×40 negro", "url": U+"perfil-extruido-40x40-negro/",
     "section_mm": [40, 40], "slot_mm": 6, "finish": "black anodized", "bar_mm": 2000, "bar_kg": 2.6, "price_per_bar": 38.27,
     "cutting": "Up to 7 cuts per bar, 3-4 mm lost per cut, offcut shipped with the order",
     "note": "Different slot system (6 mm). CS10 brackets and nuts do not fit. No black 40x80 is listed."},
  ],
  "parts": [
    # role: what the configurator uses it for
    {"id": "BR4040", "group": "brackets", "name": "Escuadra de montaje de 40X40 CS10 ranura 10mm", "url": U+"escuadra-40x40-cs10/", "price": 1.66, "role": "40x40 butt joint (bracket only)"},
    {"id": "BR4040-SET", "group": "brackets", "name": "Set escuadra 40X40 con tornillos y tuercas", "url": U+"set-escuadra-40x40-con-tornillos-y-tuercas/", "price": 3.93, "role": "40x40 butt joint, with 2 M8x20 hammer bolts and 2 M8 flange nuts", "size_mm": [40, 40, 40], "kg": 0.08},
    {"id": "BR4080", "group": "brackets", "name": "Escuadra de montaje 40X80 CS10 ranura 10mm", "url": U+"escuadra-40x80-cs10/", "price": 5.10, "role": "40x80 butt joint", "size_mm": [76, 38, 76], "kg": 0.115, "colors": ["grey RAL 7004", "black RAL 9005"]},
    {"id": "BR40160", "group": "brackets", "name": "Escuadra de fijación 40X160 CS10 ranura 10mm", "url": U+"escuadra-de-fijacion-40x160-cs10/", "price": 9.10, "role": "Heavy joint (wheel deck, uprights)"},
    {"id": "PIV180", "group": "brackets", "name": "Fijación giratoria 180º ranura 8-10mm", "url": U+"fijacion-orientable-180-cs10-cs8/", "price": 13.80, "role": "Angle-adjustable joint (pedal plate, wheel deck tilt)"},
    {"id": "QC90", "group": "connectors", "name": "Unión de apriete rápido 90º ranura 10", "url": U+"union-de-apriete-rapido-90o-ranura-10/", "price": 2.10, "role": "Hidden 90° joint, needs drilled profile end"},
    {"id": "QC0", "group": "connectors", "name": "Unión de apriete rápido 0º ranura 10", "url": U+"union-de-apriete-papida-0-cs10/", "price": 2.10, "role": "Hidden joint for profiles bolted side by side, needs drilling"},
    {"id": "QC45", "group": "connectors", "name": "Unión de apriete 45-135º ranura 10", "url": U+"union-de-apriete-45-135o-ranura-10/", "price": 7.15, "role": "Angled joint (sloped pedal deck)"},
    {"id": "PLT4080", "group": "connectors", "name": "Pletina aluminio 40×80 set", "url": U+"pletina-aluminio-40x80-set/", "price": 5.99, "role": "Joining plate for 40x80"},
    {"id": "CUBE3", "group": "connectors", "name": "Conector en Cubo para Esquina CS10 Perfil 40/3 conexiones", "url": U+"conector-en-cubo-para-esquina-cs10-40-3/", "price": 6.00, "role": "3-way frame corner"},
    {"id": "CUBE2", "group": "connectors", "name": "Conector de cubos para esquinas CS10 Perfil 40/2 conexiones", "url": U+"conector-en-cubo-para-esquina-cs10-40-2/", "price": 5.40, "role": "2-way frame corner"},
    {"id": "SPLICE", "group": "connectors", "name": "Empalmador de Perfiles CS10 para ranura 10mm", "url": U+"conector-de-perfiles-180-10-m8/", "price": 11.70, "role": "Straight splice for long rails"},
    {"id": "TN-M6", "group": "fasteners", "name": "Tuerca martillo M6 ranura 10", "url": U+"tuerca-martillo-m6-ranura-10/", "price": 0.25, "role": "Mounting seat, wheel base and pedal plates"},
    {"id": "TN-M8", "group": "fasteners", "name": "Tuerca martillo M8 ranura 10", "url": U+"tuerca-martillo-m8-ranura-10/", "price": 0.25, "role": "Mounting heavy plates"},
    {"id": "TN-M6-SPR", "group": "fasteners", "name": "Tuerca deslizante giratoria con resorte ranura 10, M6", "url": U+"tuerca-deslizante-giratoria-con-resorte-ranura-10-m6/", "price": 0.83, "role": "Spring nut that stays put while you adjust positions"},
    {"id": "HB-M8x20", "group": "fasteners", "name": "Tornillo cabeza martillo M8x20 ranura 10", "url": U+"tornillo-cabeza-martillo-m8x20-ranura-10/", "price": 0.33, "role": "Bracket bolt"},
    {"id": "HB-M8x25", "group": "fasteners", "name": "Tornillo cabeza martillo M8x25 ranura 10", "url": U+"tornillo-cabeza-martillo-m8x25-ranura-10/", "price": 0.35, "role": "Bracket bolt"},
    {"id": "FN-M8", "group": "fasteners", "name": "Tuerca de brida M8", "url": U+"tuerca-de-brida-m8/", "price": 0.11, "role": "Nut for hammer bolts"},
    {"id": "CAP4040", "group": "caps", "name": "Tapa 40X40L color gris", "url": U+"tapa-40x40l-color-gris/", "price": 0.81, "role": "End cap 40x40 (black version listed on the profile page, price not shown)"},
    {"id": "CAP4080", "group": "caps", "name": "Tapa 40X80L color gris", "url": U+"tapa-40x80l-color-gris/", "price": 1.74, "role": "End cap 40x80 (black version listed on the profile page, price not shown)"},
    {"id": "CAPBR4040", "group": "caps", "name": "Tapa para escuadra 40X40", "url": U+"tapa-para-escuadra-40x40/", "price": 0.67, "role": "Bracket cover"},
    {"id": "SLOT-GREY", "group": "caps", "name": "Perfil de cubierta para ranura de 10 Gris", "url": U+"perfil-de-cubierta-para-ranura-de-10-gris/", "price": 2.05, "role": "Slot cover strip"},
    {"id": "SLOT-LED", "group": "caps", "name": "Perfil de cubierta para ranura de 10 Transparente (Led)", "url": U+"perfil-de-cubierta-cs10-transparente/", "price": 3.79, "role": "Clear slot cover for LED strips, 2 m piece (fun lighting option)", "piece_mm": 2000},
    {"id": "FOOT-M8-40", "group": "feet", "name": "Patas nivelación M8 Diámetro 40mm", "url": U+"patas-nivelacion-m8-diametro-40mm/", "price": 1.88, "role": "Levelling foot D40, M8, 0-60 kg per foot; screws into an M8 hammer nut in the bottom slot"},
    {"id": "FOOT-M12-44", "group": "feet", "name": "Pata ajustable M12 perfil ranura 10mm", "url": U+"pata-ajustable-para-perfil-con-ranura-de-10mm/", "price": 4.85, "role": "Levelling foot D44, 30 mm adjustment, 10,000 N"},
    {"id": "FOOT-M12-70", "group": "feet", "name": "Patas nivelación M12 Diámetro 70mm", "url": U+"patas-antivibracion-m12-d7/", "price": 7.55, "role": "Anti-vibration foot"},
    {"id": "FOOT-M12-90", "group": "feet", "name": "Patas nivelación M12 Diámetro 90mm", "url": U+"patas-antivibracion-m12-d9/", "price": 7.55, "role": "Anti-vibration foot"},
    {"id": "PLATE4080", "group": "feet", "name": "Placa de nivelación 40×80 M12", "url": U+"placa-de-nivelacion-40x80-m12/", "price": 12.70, "role": "Foot plate for 40x80 rails"},
  ],
  "profile_price_basis": "Profile prices only appear in the cart after entering a length. 40x40 CS10 is 13 EUR and 40x80 CS10 is 27 EUR for a 1000 mm piece (read by Homes on 2026-10-23). The configurator assumes the price scales with length; cutting and drilling charges are not confirmed yet.",
}
json.dump(catalog, open(f"{OUT}/mundoperfil-catalog.json", "w"), ensure_ascii=False, indent=2)

# HexRig upper frame cut list, mapped to Mundo Perfil profiles
j = json.load(open(f"{S}/out/joints.json"))
names = {"4524N12": "Cross member under the seat", "4524N32": "Base rail", "Component3": "Seat rail",
         "Component4": "Wheel upright", "Component5": "Wheel base cross bar", "Component6": "Wheel deck arm",
         "Component7": "Monitor upright", "Component8": "Monitor arm", "Component9": "Monitor cross bar",
         "Component10": "Front upright", "Component11": "Pedal deck rail (sloped 4°)", "Component12": "Pedal cross bar",
         "Component13": "Shifter and handbrake arm", "Component14": "Shifter and handbrake bracket"}
rows = []
for p in j["profiles"]:
    key = p["inst"].split("_T-Slotted")[0].split(":")[0]
    rows.append({"model_part": p["inst"], "role": names.get(key, key), "profile": "P4080-CS10" if p["kind"] == "40x80" else "P4040-CS10",
                 "length_mm": p["sizes"][2], "free_ends": sum(1 for e in p["ends"] if not e), "butt_ends": sum(1 for e in p["ends"] if e),
                 "axis": " ".join(map(str, p["axis"])), "center_mm": " ".join(map(str, p["center"]))})
rows.sort(key=lambda r: (r["profile"], -r["length_mm"]))
with open(f"{OUT}/hexrig-frame-cutlist.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

prof = {p["id"]: p for p in catalog["profiles"]}; part = {p["id"]: p for p in catalog["parts"]}
m40 = sum(r["length_mm"] for r in rows if r["profile"] == "P4040-CS10") / 1000
m80 = sum(r["length_mm"] for r in rows if r["profile"] == "P4080-CS10") / 1000
butt = sum(r["butt_ends"] for r in rows)
side = len([c for c in j["contacts"] if not any(c[1] in e for p in j["profiles"] if p["inst"] == c[0] for e in p["ends"]) and not any(c[0] in e for p in j["profiles"] if p["inst"] == c[1] for e in p["ends"])])
free80 = sum(r["free_ends"] for r in rows if r["profile"] == "P4080-CS10")
free40 = sum(r["free_ends"] for r in rows if r["profile"] == "P4040-CS10")
bom = [
  ("P4040-CS10", f"{m40:.2f} m", m40 * prof["P4040-CS10"]["price_per_m"], "cart price per metre"),
  ("P4080-CS10", f"{m80:.2f} m", m80 * prof["P4080-CS10"]["price_per_m"], "cart price per metre"),
  ("BR4040-SET", f"{2*butt}", 2*butt * part["BR4040-SET"]["price"], f"2 per butt joint, {butt} butt joints"),
  ("BR4040-SET", f"{2*side}", 2*side * part["BR4040-SET"]["price"], f"2 per bolted side contact, {side} contacts"),
  ("CAP4080", f"{free80}", free80 * part["CAP4080"]["price"], "free 40x80 ends"),
  ("CAP4040", f"{free40}", free40 * part["CAP4040"]["price"], "free 40x40 ends"),
]
summary = {"pieces_40x40": sum(1 for r in rows if r["profile"] == "P4040-CS10"), "pieces_40x80": sum(1 for r in rows if r["profile"] == "P4080-CS10"),
           "m_40x40": round(m40, 3), "m_40x80": round(m80, 3), "butt_joints": butt, "side_contacts": side, "free_ends_40x80": free80, "free_ends_40x40": free40,
           "frame_kg": round(m40 * 1.5 + m80 * 2.7 + 2*(butt+side) * 0.08, 1),
           "bom": [{"id": i, "qty": q, "eur": round(e, 2), "note": n} for i, q, e, n in bom],
           "total_eur_excl_vat": round(sum(b[2] for b in bom), 2),
           "hardware_eur_excl_vat": round(sum(b[2] for b in bom[2:]), 2)}
json.dump(summary, open(f"{OUT}/hexrig-frame-estimate.json", "w"), ensure_ascii=False, indent=2)
print(json.dumps(summary, indent=1, ensure_ascii=False))
