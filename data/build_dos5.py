#!/usr/bin/env python3
"""Rows from the user's dossier JSON of 23 Nov 2026 (v1.6): claims first seen after the 21 Nov dossier.

  python3 data/build_dos5.py /path/to/Ueno_Dossier_2026-11-23_0619.json    # private input; rewrites data/raw/dos5.*.jsonl

Rules applied here, on top of SPEC.md:
- one source per row: the claim's first article or official page whose link the dossier marks ok; never a social post;
- claims the dossier labels Low, or that have no article or official page, are not imported;
- detail_en is the dossier's own statement (cut at 700 characters) unless overridden below to drop relatives,
  health details or third parties' unrelated criminal history;
- links were checked by the dossier's bot, not opened by this project, so confidence is 'medium' at most.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, "raw")
D = json.load(open(sys.argv[1], encoding="utf-8")); CL = {c["id"]: c for c in D["claims"]}
UB, GV, BCP, MUNI = "org:ueno-bank", "org:grupo-vazquez", "auth:bcp", "auth:municipalidad-de-asuncion"
PENA, REY, IPS, ITAIPU = "person:santiago-pena", "person:julio-rey", "org:ips", "org:itaipu"
SKIP = {"C-MED-01": "Instagram profile note, no claim", "C-LEG-23": "health details of a third party, not about the case",
        "C-IPS-06": "Low: unsubstantiated accusations against named people", "C-CB-11": "Low: outlet's own presumption",
        "C-MUN-18": "Low: social posts only", "C-COL-20": "social posts only", "C-COL-21": "social posts only",
        "C-MUN-15": "social posts only", "C-MUN-17": "conflict over a signing date; no new fact", "C-LEG-29": "photo report; no new fact"}
# claim -> (category, asserted_by, title_en, title_es, parties, amount, currency, detail_override)
M = {
"C-PEN-21": ("criminal", "prosecution", "Prosecutors search the registered address of Pear S.R.L.", "La Fiscalía allana el domicilio fiscal de Pear S.R.L.", ["org:pear-srl", "person:francisco-pena-palacios", "auth:ministerio-publico"], None, None, None),
"C-PEN-22": ("criminal", "defence", "Peña's defence complains about his detention regime at Viñas Cué", "La defensa de Peña reclama por su régimen de reclusión en Viñas Cué", [PENA, "person:ricardo-preda", "person:osmar-legal"], None, None, None),
"C-PEN-26": ("criminal", "press", "Judge orders Peña be held on the same terms as other inmates", "El juez ordena que Peña esté en igualdad de condiciones con los demás internos", [PENA, "person:osmar-legal"], None, None, None),
"C-LEG-21": ("criminal", "press", "Judge Legal rejects a challenge to his taking case 92/2026 (A.I. 420)", "El juez Legal rechaza la reposición contra su competencia en la causa 92/2026 (A.I. 420)", ["person:osmar-legal", "person:miguel-angel-mora", "person:rodrigo-estigarribia"], None, None, None),
"C-PEN-23": ("statement", "press", "Banking association head: Peña defended Ueno at a tense meeting with banks on 10 Sep", "Titular de Asoban: Peña defendió a Ueno en una tensa reunión con bancos el 10 de setiembre", [PENA, UB, "person:horacio-cartes"], None, None, None),
"C-OTH-06": ("political", "press", "Senator Villalba announces a criminal complaint over the alleged Comitia-ITTI link", "El senador Villalba anuncia denuncia penal por el supuesto vínculo Comitia-ITTI", ["org:comitia", "org:itti", "auth:tsje"], None, None, None),
"C-OTH-07": ("political", "press", "ABC: the Army took part in a 2024 'strategic alliance' launch with ITTI; the general denies any agreement", "ABC: el Ejército participó en 2024 del lanzamiento de una 'alianza estratégica' con ITTI; el general niega convenio", ["org:itti", "person:guillermo-vazquez"], None, None, None),
"C-OWN-04": ("political", "regulator", "Executive bill would put Ueno-linked companies under temporary administration for 8 months", "Proyecto del Ejecutivo pondría a las empresas vinculadas a Ueno bajo administración temporal por 8 meses", [GV, "person:pedro-alliana", "auth:senado"], None, None, None),
"C-PUB-09": ("depositor", "press", "Former workers demand wages and severance now and reject State administration of the group", "Extrabajadores exigen salarios e indemnizaciones ya y rechazan la administración estatal del grupo", [GV, UB], None, None, None),
"C-LEG-22": ("criminal", "press", "ABC: a G. 3,090.6 million shortfall was found in the vault of GSR Security", "ABC: se detectó un faltante de G. 3.090,6 millones en la bóveda de GSR Security", ["org:gsr-security", "org:redisa", UB], 3090600000, "PYG",
   "ABC, citing investigators: the vault should have held G. 18,102 million plus USD 189,396 at the 3 Nov count (part belonging to Ueno Bank, part to Red Digital/REDISA); after the 17-18 Nov count a shortfall of G. 3,090.6 million was found in the REDISA package. The firm's representative is charged and presumed innocent."),
"C-LEG-24": ("statement", "company", "GSR Security (Dobrestec) says it is not part of Grupo Vázquez", "GSR Security (Dobrestec) afirma que no forma parte del Grupo Vázquez", ["org:gsr-security", GV], None, None, None),
"C-PUB-11": ("corporate", "press", "ABC: Itaipú awarded GSR Security's legal entity two surveillance contracts worth G. 32,746 million", "ABC: Itaipú adjudicó a la razón social de GSR Security dos contratos de vigilancia por G. 32.746 millones", [ITAIPU, "org:gsr-security"], 32745781980, "PYG", None),
"C-COL-19": ("depositor", "regulator", "BCP: deposits above the guarantee cap depend on the sale of asset lots to other banks", "BCP: los depósitos por encima del tope de garantía dependen de la venta de lotes de activos a otros bancos", [BCP, "auth:fgd", UB], None, None, None),
"C-CB-06": ("supervisory", "regulator", "Central bank keeps its policy rate at 5.50%, sees no reason to change it over Ueno", "El BCP mantiene la tasa en 5,50% y no ve motivos para cambiarla por el caso Ueno", [BCP], None, None, None),
"C-OTH-08": ("credit", "press", "BID Invest confirms it disbursed only USD 10 million of a planned USD 20 million to Ueno", "BID Invest confirma que desembolsó solo USD 10 millones de los USD 20 millones previstos para Ueno", [UB], 10000000, "USD", None),
"C-PUB-10": ("depositor", "press", "Business guilds warn of a slowdown; small-business federation reports revenue falls of up to 35%", "Gremios advierten una desaceleración; la federación de mipymes reporta caídas de ingresos de hasta 35%", [UB], None, None, None),
"C-OTH-09": ("credit", "press", "ABC: Ueno told the electoral court in 2025 that Comitia had a USD 14.1 million credit line for the voting-machine tender", "ABC: Ueno comunicó al TSJE en 2025 que Comitia tenía una línea de crédito de USD 14,1 millones para la licitación de máquinas de votación", ["org:comitia", UB, "auth:tsje"], 14100000, "USD", None),
"C-CB-07": ("supervisory", "rey", "La Nación, from Rey's statement: resident BCP supervisors had full access, yet the formal observation came months later", "La Nación, según la declaración de Rey: supervisores del BCP con acceso total, pero la observación formal llegó meses después", [BCP, REY, UB, "person:miguel-vazquez"], None, None, None),
"C-COL-22": ("depositor", "regulator", "BCP director Rivarola: 97% of depositors covered; a hole of more than USD 1,500 million", "Director del BCP Rivarola: 97% de los depositantes cubiertos; un agujero de más de USD 1.500 millones", ["person:fernando-rivarola", BCP, "auth:fgd", UB], 1500000000, "USD", None),
"C-COL-23": ("market", "press", "La Nación computes a preliminary USD 1,362 million of losses to the guarantee fund and securities holders", "La Nación calcula de forma preliminar USD 1.362 millones de pérdidas para el fondo de garantía y los tenedores de títulos", [UB, GV, "org:itti", "auth:fgd"], 1362339250, "USD", None),
"C-PUB-12": ("market", "press", "Última Hora: Ueno's share of State-entity deposits rose from about 3% to about 18-23% between 2024 and Sept 2026", "Última Hora: la participación de Ueno en depósitos de entidades del Estado subió de cerca de 3% a 18-23% entre 2024 y setiembre de 2026", [UB, IPS], None, None, None),
"C-OTH-10": ("market", "press", "Última Hora: the rating agency kept Ueno at AApy while its own reports recorded repeated sales of past-due loans to Vinanzas", "Última Hora: la calificadora mantuvo a Ueno en AApy pese a que sus informes registraban ventas recurrentes de cartera vencida a Vinanzas", [UB, "org:vinanzas"], None, None,
   "Última Hora reports that Solventa & Riskmétrica kept Ueno at AApy until November 2026 even though its own reports recorded recurring sales of past-due portfolio to Vinanzas to hold down delinquency. The article's material on the agency's shareholders is not imported here."),
"C-PUB-13": ("corporate", "press", "El Observador: the Supreme Court signed at least seven contracts with Grupo Vázquez firms since 2023", "El Observador: la Corte Suprema firmó al menos siete contratos con empresas del Grupo Vázquez desde 2023", ["org:itti", "org:technoma", GV], 12346350503, "PYG", None),
"C-MUN-12": ("depositor", "regulator", "Asunción intervenes in municipal properties in La Piedad and halts unauthorised works", "Asunción interviene inmuebles municipales en La Piedad y frena obras no autorizadas", [MUNI, "person:soledad-nunez", GV], None, None, None),
"C-PEN-24": ("political", "regulator", "Congress elects Antonio 'Tony' Barrios Vice-President", "El Congreso elige a Antonio 'Tony' Barrios como Vicepresidente", ["person:pedro-alliana", "auth:camara-de-diputados"], None, None, None),
"C-OTH-11": ("political", "press", "Opposition senator says sectors of the State want to confine the inquiry to those already charged", "Senador opositor afirma que sectores del Estado buscan limitar la investigación a los ya imputados", ["person:pedro-alliana", "auth:seprelad"], None, None, None),
"C-PUB-14": ("political", "press", "Deputy asks to replace Itaipú's new director, who sat on the board that approved Ueno as an eligible bank", "Diputado pide reemplazar al nuevo director de Itaipú, que integró el consejo que habilitó a Ueno", [ITAIPU, "person:pedro-alliana", UB], None, None, None),
"C-MUN-13": ("depositor", "regulator", "Asunción's official balance at 31 Oct lists three Ueno accounts totalling G. 1,792.6 million", "El balance oficial de Asunción al 31 de octubre lista tres cuentas en Ueno por G. 1.792,6 millones", [MUNI, UB], 1792556937, "PYG",
   "The city's official balance sheet at 31 Oct 2026, published on 22 Nov, lists two savings accounts and one current account at Ueno Bank which the dossier sums to G. 1,792,556,937. Account numbers are in the source and are not repeated here."),
"C-MUN-14": ("depositor", "regulator", "Asunción's finance adviser: November tax collection about 20% below last year, partly because of Ueno", "Asesor financiero de Asunción: la recaudación de noviembre está cerca de 20% por debajo del año pasado, en parte por Ueno", [MUNI, UB], None, None, None),
"C-MUN-16": ("statement", "regulator", "Asunción's finance adviser: a 2020 file shows Miguel Vázquez applying for a municipal plot as a social occupant", "Asesor financiero de Asunción: un expediente de 2020 muestra a Miguel Vázquez solicitando un lote municipal como poblador social", [MUNI, "person:miguel-vazquez", GV], None, None, None),
"C-CB-09": ("supervisory", "regulator", "BCP director Rivarola: the technical alerts on Ueno went off and many people ignored them", "Director del BCP Rivarola: las alertas técnicas sobre Ueno saltaron y mucha gente las desoyó", ["person:fernando-rivarola", BCP, UB], None, None, None),
"C-CB-10": ("supervisory", "press", "Última Hora: the Ueno-Visión merger plan asked the BCP for about G. 5.2 trillion of deferrals and a trust", "Última Hora: el plan de fusión Ueno-Visión pidió al BCP diferimientos y un fideicomiso por unos G. 5,2 billones", [UB, "org:vision-banco", BCP], 5200000000000, "PYG", None),
"C-IPS-07": ("depositor", "company", "IPS legal director: about USD 350 million of the pension fund and USD 150 million of operating money are at Ueno", "Director jurídico del IPS: unos USD 350 millones del fondo de jubilaciones y USD 150 millones operativos están en Ueno", [IPS, UB, BCP], 516000000, "USD", None),
"C-IPS-08": ("statement", "press", "El Independiente: the 'Delirio colectivo' report planned to capture more IPS pensioners' money", "El Independiente: el informe 'Delirio colectivo' planeaba captar más dinero de jubilados del IPS", [IPS, UB, REY], None, None, None),
"C-LEG-25": ("criminal", "press", "Creditors ask a civil court to declare Grupo Vázquez S.A.E. bankrupt over an unpaid debt of about G. 5,570 million", "Acreedores piden a un juzgado civil declarar la quiebra de Grupo Vázquez S.A.E. por una deuda impaga de unos G. 5.570 millones", [GV], 5570000000, "PYG", None),
"C-LEG-26": ("political", "press", "The legitimacy of interim Attorney General Cantero's appointment is contested", "Se cuestiona la legitimidad de la designación de la Fiscal General interina Cantero", ["person:alba-rocio-cantero", "auth:senado"], None, None, None),
"C-LEG-27": ("political", "press", "Opposition pushes to impeach the Comptroller General over his review of Peña's assets", "La oposición impulsa el juicio político al Contralor por su examen de los bienes de Peña", ["auth:contraloria", PENA], None, None, None),
"C-LEG-28": ("criminal", "press", "Former statutory auditor Almada's defence withdraws its appeal; his charge stands", "La defensa del exsíndico Almada desiste de su apelación; la imputación queda firme", ["person:miguel-angel-almada", "person:rodrigo-estigarribia", "auth:tribunal-apelacion-delitos-economicos"], None, None, None),
"C-OTH-12": ("political", "press", "Lawyers and a senator question the silence of the anti-laundering and tax agencies over the cash delivery", "Abogados y una senadora cuestionan el silencio de Seprelad y la DNIT ante la entrega de efectivo", ["auth:seprelad", UB], None, None, None),
"C-PEN-25": ("political", "regulator", "Deputies ask the Foreign Ministry for a report on all of Peña's official trips", "Diputados pide a Cancillería un informe sobre todos los viajes oficiales de Peña", [PENA, "auth:camara-de-diputados"], None, None, None),
"C-COL-24": ("market", "press", "Only about 550,000 of Ueno's 1.9 million clients have moved to other institutions", "Solo unos 550.000 de los 1,9 millones de clientes de Ueno migraron a otras entidades", [UB, BCP], None, None, None),
"C-PUB-15": ("depositor", "press", "Contractors' guild says USD 68 million of the power utility ANDE is trapped at Ueno; earlier itemisation gave about USD 27 million", "Gremio de contratistas dice que USD 68 millones de la ANDE están atrapados en Ueno; un desglose previo daba unos USD 27 millones", [UB], 68000000, "USD", None),
"C-OTH-13": ("statement", "press", "The archbishop of Asunción says he briefed the Pope on the Ueno collapse and urges a change of ministers", "El arzobispo de Asunción dice que informó al Papa sobre la caída de Ueno y pide cambio de ministros", ["person:pedro-alliana"], None, None, None),
"C-OTH-14": ("credit", "press", "ABC: a deputy received a Ueno loan a week after voting for the payments law, and monthly payments from the bank; he says they were sponsorships", "ABC: un diputado recibió un préstamo de Ueno una semana después de votar la ley de pagos, y pagos mensuales del banco; él dice que eran auspicios", [UB, PENA], 216200000, "PYG", None),
"C-DIR-11": ("corporate", "press", "ABC: Dataforge, part-owned by a charged former Ueno manager, is in a consortium awarded a quiniela concession in April 2026", "ABC: Dataforge, con un exgerente imputado de Ueno entre sus accionistas, integra un consorcio adjudicado con una concesión de quiniela en abril de 2026", ["org:dataforge", "person:jose-augusto-sala-cardozo", GV], None, None, None),
"C-DIR-12": ("criminal", "press", "Última Hora: one of the firms whose receipts backed the night cash entry has a suspended tax registration", "Última Hora: una de las firmas cuyos recibos respaldaron el ingreso nocturno de efectivo tiene el RUC suspendido", [UB, GV], None, None,
   "Última Hora reports that the firms whose receipts were used to justify the cash Rey says was brought in one night include Racole S.A., whose tax registration is suspended by the DNIT. The article's material on the criminal history of a company officer is not imported here."),
"C-PUB-16": ("depositor", "regulator", "Labour minister: 22 group companies shut since 3 Nov; 3,610 workers in Paraguay without work or severance", "Ministra de Trabajo: 22 empresas del grupo cerradas desde el 3 de noviembre; 3.610 trabajadores en Paraguay sin empleo ni indemnización", [GV, UB], None, None, None),
"C-PUB-17": ("political", "press", "Former senator asks the President to remove Itaipú's legal director over the Ueno deposits", "Exsenador pide al Presidente remover a la directora jurídica de Itaipú por los depósitos en Ueno", [ITAIPU, "person:pedro-alliana"], None, None, None),
"C-OTH-15": ("political", "regulator", "Senate urges agencies to establish where the personal and biometric data of over 3 million Ueno clients are", "El Senado insta a establecer dónde están los datos personales y biométricos de más de 3 millones de clientes de Ueno", ["auth:senado", BCP, UB], None, None, None),
"C-OTH-16": ("depositor", "press", "Volunteer firefighters' rescue unit appeals for funds because its savings are stuck at Ueno", "Unidad de rescate de bomberos voluntarios pide fondos porque sus ahorros están atrapados en Ueno", [UB], 20000000, "PYG", None),
}
FACTS = [  # claim, entity, metric, value, currency, unit_note, period
 ("C-COL-22", UB, "balance_sheet_hole_bcp_director", 1500000000, "USD", "more than; 'plata que desapareció' per BCP director Rivarola, radio interview", "2026-11-22"),
 ("C-COL-22", UB, "healthy_assets_bcp_director", 1450000000, "USD", "range USD 1.4-1.5 billion; another official cited about USD 900 million", "2026-11-22"),
 ("C-COL-23", UB, "losses_fgd_and_securities_holders", 1362339250, "USD", "La Nación's preliminary sum: guarantee-fund payouts + USD 350M New York bond + USD 368.3M of local securities; a different construct from the BCP's deficit estimate", "2026-11-22"),
 ("C-CB-10", UB, "merger_plan_deferrals_requested", 5200000000000, "PYG", "about; G. 2.68 trillion deferred portfolio + G. 2.52 trillion trust; what the BCP granted is not itemised", "2024-06"),
 ("C-IPS-07", IPS, "pension_fund_investments_at_ueno", 350000000, "USD", "about", "2026-11"),
 ("C-PUB-14", ITAIPU, "frozen_at_ueno", 163800000, "USD", "plus G. 115,200 million, at the resolution date; an earlier report gave USD 182 million", "2026-11-03"),
 ("C-MUN-13", MUNI, "frozen_at_ueno", 1792556937, "PYG", "three accounts in the official balance at 31 Oct 2026; dossier's sum", "2026-10-31"),
 ("C-PUB-16", GV, "workers_without_severance", 3610, "", "workers in Paraguay; about 1,000 more in Argentina", "2026-11-23"),
 ("C-LEG-22", "org:gsr-security", "vault_shortfall", 3090600000, "PYG", "found after the 17-18 Nov count, per investigators cited by ABC", "2026-11-18"),
]
def pick(c):
    for s in c["sources"]:
        if s["kind"] not in ("x-post", "instagram") and s["tier"] in ("T1", "T2", "T3") and s["link_status"] == "ok" and s["url"].startswith("http"): return s
def sid(s):
    a, _, b = s["id"].partition("_"); outlet = {"uh": "ultimahora", "ln": "lanacion", "elnac": "elnacional", "5d": "5dias", "obs": "elobservador", "muni": "asuncion-gov", "dip3245": "diputados", "cp": "cp", "ind": "elindependiente", "mil": "radio1000"}.get(a, a)
    return "src:%s-%s-%s" % (outlet, s["pub_date"], re.sub(r"[^a-z0-9]+", "-", (b or a).lower()).strip("-"))
def cut(t, n=700):
    if len(t) <= n: return t
    t = t[:n]; i = max(t.rfind(". "), t.rfind("; "))
    return (t[:i + 1] if i > 300 else t.rstrip() + " [...]")
def quote(q):
    q = re.sub(r"\s*\(.*?\)\s*$", "", q).strip("«»“”\"' "); w = q.split()
    return " ".join(w[:12]) if q else ""
def prov(cid, who, s, q=""):
    return {"asserted_by": who, "source": sid(s), "locator": "official page" if s["kind"].startswith("official") else "article",
            "quote": q, "confidence": "medium", "note": "Link from the 23 Nov 2026 dossier (v1.6), marked ok by its checker on %s. Not opened by this project. Dossier claim %s, labelled %s / %s." % (s.get("retrieved", "?"), cid, CL[cid]["label"], CL[cid]["status"])}
srcs, events, facts, skipped = {}, [], [], dict(SKIP)
for cid, (cat, who, ten, tes, parties, amt, cur, over) in M.items():
    c = CL[cid]; s = pick(c)
    assert s, cid
    srcs[sid(s)] = {"id": sid(s), "kind": "official" if s["kind"].startswith("official") else "press", "outlet": re.sub(r"\s*\(PY\)", "", s["outlet"]), "title": s["title"], "date": s["pub_date"], "url": s["url"], "page": "dossier v1.6 source id %s" % s["id"]}
    events.append({"id": "dos5:event:%04d" % (len(events) + 1), "date": c["event_date"], "date_precision": {4: "year", 7: "month"}.get(len(c["event_date"]), "day"), "category": cat,
                   "title_en": ten, "title_es": tes, "detail_en": over or cut(c["statement"]), "detail_es": tes + ". (Detalle completo solo en inglés.)", "parties": parties, "amount": amt, "currency": cur,
                   "prov": prov(cid, who, s, "" if over else quote(c.get("quote", "")))})
for i, (cid, ent, metric, val, cur, note, period) in enumerate(FACTS, 1):
    s = pick(CL[cid]); who = M[cid][1]
    facts.append({"id": "dos5:fact:%04d" % i, "entity": ent, "metric": metric, "value": val, "currency": cur, "unit_note": note, "period": period, "prov": prov(cid, who, s)})
def dump(kind, rows):
    with open(os.path.join(RAW, "dos5.%s.jsonl" % kind), "w", encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
dump("sources", sorted(srcs.values(), key=lambda r: r["id"])); dump("events", events); dump("facts", facts)
seen = open("/dev/null"); new_ids = [c["id"] for c in D["claims"] if c["id"] not in M and c["id"] not in SKIP]
print(len(srcs), "sources,", len(events), "events,", len(facts), "facts; skipped on purpose:", len(SKIP))
