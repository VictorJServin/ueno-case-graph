#!/usr/bin/env python3
"""Rows researched directly on the web by this project (tag: web), 23 Nov 2026: the 'did the bank have enough assets?' question.
Four of the five pages were opened and read on 23 Nov 2026; the Última Hora page was seen as a search result only.
  python3 data/build_web.py     # rewrites data/raw/web.*.jsonl
"""
import json, os
RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
UB, BCP, FGD = "org:ueno-bank", "auth:bcp", "auth:fgd"
S = [
 ("src:ultimahora-2026-11-18-latorre-activos", "Última Hora", "Afirman que existen activos para cubrir todos los depósitos de ahorristas, jubilatorios y públicos en ueno", "2026-11-18", "https://www.ultimahora.com/afirman-que-existen-activos-para-cubrir-todos-los-depositos-de-ahorristas-jubilatorios-y-publicos-en-ueno"),
 ("src:extra-2026-11-19-bcp-devolveran", "Extra", "BCP informó que devolverán plata a todos los depositantes de ueno", "2026-11-19", "https://www.extra.com.py/actualidad/bcp-informo-que-devolveran-plata-a-todos-los-depositantes-de-ueno"),
 ("src:economia-2026-11-19-activos-1500", "Economía.com.py", "El BCP identifica activos por USD 1.500 millones en ueno bank, pero advierte que no alcanzan para cubrir todas las deudas", "2026-11-19", "https://economia.com.py/el-bcp-identifica-activos-por-usd-1-500-millones-en-ueno-bank-pero-advierte-que-no-alcanzan-para-cubrir-todas-las-deudas/"),
 ("src:lanacion-2026-11-19-activos-verificados", "La Nación", "BCP: activos verificados de Ueno Bank alcanzan unos G. 9 billones", "2026-11-19", "https://www.lanacion.com.py/negocios_edicion_impresa/2026/11/19/bcp-activos-verificados-de-ueno-bank-alcanzan-unos-g-9-billones/"),
 ("src:rdn-2026-11-23-cramer-vaciamiento", "RDN", "Liz Cramer atribuye la caída de ueno bank a un vaciamiento", "2026-11-23", "https://www.rdn.com.py/2026/11/23/liz-cramer-atribuye-la-caida-de-ueno-bank-a-un-vaciamiento/"),
]
READ = "Page opened and read by this project on 23 Nov 2026."
def P(who, i, quote="", conf="high", note=READ): return {"asserted_by": who, "source": S[i][0], "locator": "article", "quote": quote, "confidence": conf, "note": note}
E = [
 ("2026-11-18", "statement", "Deputies' president Latorre says the BCP told legislators assets exist to cover all deposits, pension funds and public money",
  "El presidente de Diputados Latorre afirma que el BCP informó que hay activos para cubrir todos los depósitos, fondos jubilatorios y dinero público",
  "After a meeting with the BCP president, Raúl Latorre told the press that the central bank had identified assets sufficient to cover every depositor as well as pension and public funds. This is a legislator relaying the meeting, not a BCP statement; the BCP president qualified it the same day.",
  "Tras una reunión con el presidente del BCP, Raúl Latorre dijo a la prensa que la banca matriz identificó activos suficientes para cubrir a todos los depositantes y también los fondos jubilatorios y públicos. Es un legislador que relata la reunión, no un comunicado del BCP; el presidente del BCP lo matizó el mismo día.",
  ["person:raul-latorre", BCP, UB], None, None, P("press", 0, "", "medium", "Seen as a search result on 23 Nov 2026; page not opened. The same relay is reported by 5Días, El Nacional and Hoy.")),
 ("2026-11-18", "statement", "BCP president Schreiner: it is not accurate that assets cover everything; depositors yes, bonds no; the bank had a USD 1,500 million deficit",
  "Presidente del BCP Schreiner: no es exacto que los activos cubran todo; depositantes sí, bonos no; el banco tenía un déficit de USD 1.500 millones",
  "Extra reports the BCP president's clarification the same evening: the assets will show the bank had a deficit of USD 1,500 million; depositors would be covered but not international and local bonds; loan portfolios are to be sold to banks in stages of USD 60 to 80 million and reviewed item by item.",
  "Extra informa la aclaración del presidente del BCP esa misma noche: los activos demostrarán que el banco tenía un déficit de USD 1.500 millones; se cubriría a los depositantes pero no los bonos internacionales y locales; las carteras se venderán a bancos por etapas de USD 60 a 80 millones y se revisarán una por una.",
  ["person:jorge-schreiner", BCP, UB], 1500000000, "USD", P("regulator", 1, "Cubriríamos a los depositantes, pero no a los bonos internacionales y locales")),
 ("2026-11-18", "depositor", "BCP: verified assets of about G. 9.25 trillion are loans and property, not cash, and full repayment depends on banks buying them",
  "BCP: los activos verificados por unos G. 9,25 billones son carteras y bienes, no efectivo, y la devolución total depende de que los bancos los compren",
  "Economía.com.py reports director Pedro Acosta saying the verified assets would let the bank meet its obligations to depositors, and Schreiner adding that they are loan portfolios, certificates and property whose final value depends on their quality and on bids; figures are preliminary. The assets would not cover bondholders or repay the guarantee fund's advance; the BCP puts the shortfall at USD 1,000 to 1,500 million including that advance. Lots of USD 60 to 80 million go to a competitive tender after the balance is closed.",
  "Economía.com.py informa que el director Pedro Acosta dijo que los activos verificados permitirían cubrir las obligaciones con los depositantes, y que Schreiner agregó que son carteras, certificados y bienes cuyo valor final depende de su calidad y de las ofertas; las cifras son preliminares. Los activos no cubrirían a los bonistas ni repondrían el adelanto del fondo de garantía; el BCP estima el faltante en USD 1.000 a 1.500 millones, incluido ese adelanto. Lotes de USD 60 a 80 millones irán a licitación competitiva tras el cierre del balance.",
  ["person:pedro-acosta", "person:jorge-schreiner", BCP, FGD, UB], 9251891000000, "PYG", P("regulator", 2)),
 ("2026-11-23", "statement", "Banking association president Cramer: of about USD 4,400 million of declared assets, some USD 1,500 million would be recoverable",
  "Presidenta de Asoban Cramer: de unos USD 4.400 millones de activos declarados, unos USD 1.500 millones serían recuperables",
  "RDN, citing her remarks to ABC Color: Liz Cramer, executive president of the banking association, says the bank booked loans to related parties as assets although she considers them uncollectable, that losses may exceed USD 1,000 million, and that a forensic accounting review is needed to fix the final figure. Her estimates, not verified figures.",
  "RDN, citando sus declaraciones a ABC Color: Liz Cramer, presidenta ejecutiva de Asoban, afirma que el banco registró préstamos a vinculadas como activos aunque los considera incobrables, que las pérdidas superarían USD 1.000 millones y que hace falta un análisis contable forense para fijar la cifra final. Son estimaciones suyas, no cifras verificadas.",
  ["person:liz-cramer", "org:asoban", UB], 4400000000, "USD", P("press", 4)),
]
F = [
 (UB, "verified_assets_bcp", 9251891000000, "PYG", "about USD 1,450-1,500 million; preliminary; could rise as cash counts and file checks finish; book amounts, not sale prices", "2026-11-18", P("regulator", 2)),
 (UB, "deficit_bcp_president", 1500000000, "USD", "also given as a range of USD 1,000-1,500 million including the guarantee fund's advance", "2026-11-18", P("regulator", 1, "los activos van a permitirnos demostrar que el banco tenía un déficit")),
 (UB, "declared_assets", 4400000000, "USD", "about; as cited by the banking association's president", "2026-11", P("press", 4)),
 (UB, "recoverable_assets_asoban_estimate", 1500000000, "USD", "about; her estimate", "2026-11-23", P("press", 4)),
 (UB, "bonds_not_covered", 350000000, "USD", "foreign bond; local bonds in addition; bonds are outside the guarantee by law", "2026-11-18", P("regulator", 2)),
 (UB, "verified_assets_bcp_director", 9000000000000, "PYG", "about USD 1,450 million 'verified so far'; excludes category-1 loans until their files are checked", "2026-11-18", P("regulator", 3)),
]
ENT = [("person:raul-latorre", "Person", "Raúl Latorre", "President of the Chamber of Deputies.", "Presidente de la Cámara de Diputados.", 0),
       ("person:liz-cramer", "Person", "Liz Cramer", "Executive president of the banking association Asoban.", "Presidenta ejecutiva de la Asociación de Bancos del Paraguay (Asoban).", 4),
       ("org:asoban", "Company", "Asociación de Bancos del Paraguay (Asoban)", "Banking industry association.", "Gremio de bancos.", 4)]
def dump(kind, rows):
    with open(os.path.join(RAW, "web.%s.jsonl" % kind), "w", encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
dump("sources", [{"id": a, "kind": "press", "outlet": b, "title": c, "date": d, "url": e} for a, b, c, d, e in S])
dump("events", [{"id": "web:event:%04d" % i, "date": a[0], "date_precision": "day", "category": a[1], "title_en": a[2], "title_es": a[3], "detail_en": a[4], "detail_es": a[5], "parties": a[6], "amount": a[7], "currency": a[8], "prov": a[9]} for i, a in enumerate(E, 1)])
dump("facts", [{"id": "web:fact:%04d" % i, "entity": a[0], "metric": a[1], "value": a[2], "currency": a[3], "unit_note": a[4], "period": a[5], "prov": a[6]} for i, a in enumerate(F, 1)])
dump("entities", [{"id": a[0], "type": a[1], "label": a[2], "aliases": [], "desc_en": a[3], "desc_es": a[4], "prov": {"asserted_by": "press", "source": S[a[5]][0], "locator": "article", "quote": "", "confidence": "medium", "note": ""}} for a in ENT])
print(len(S), "sources,", len(E), "events,", len(F), "facts,", len(ENT), "entities")
