from lib import *

UB, GV, ITTI, VIN, RSA, RPRO = "org:ueno-bank", "org:grupo-vazquez", "org:itti", "org:vinanzas", "org:redisa", "org:redipro"

# ---------------------------------------------------------------- UH 4 Nov 2026 (ruta de los préstamos)
s = src("src:ultimahora-2026-11-04-ruta-de-los-prestamos", "press", "Última Hora",
        "La ruta de los préstamos de ueno a sus firmas vinculadas, que derivó en su colapso y en 27 imputados", "2026-11-04",
        "https://www.ultimahora.com/la-ruta-de-los-prestamos-de-ueno-a-sus-firmas-vinculadas-que-derivo-en-su-colapso-y-en-27-imputados")
R = lambda loc, q="", conf="medium", note="": P("regulator", s, loc, q, conf, note)
hq = "fueron transferidos mayormente a itti, Redipro y Redisa"
loan(UB, "org:grupo-hendy", R("Hendy loans", hq), date="2025-09-26", currency="PYG", principal=91334400000,
     note_en="Proceeds mostly transferred to ITTI, Redipro and Redisa; part used to amortise ITTI overdrafts.", note_es="Fondos transferidos mayormente a itti, Redipro y Redisa; parte para amortizar sobregiros de itti.")
loan(UB, "org:grupo-hendy", R("Hendy loans", hq), date="2025-10-30", currency="USD", principal=5075250, term_years=10, collateral="none",
     note_en="Terms 'up to ten years' and no sufficient real collateral apply to the three 2025 Hendy credits as a group.", note_es="Plazos de hasta diez años y sin garantías reales suficientes (para los tres créditos de 2025).")
L_H3 = loan(UB, "org:grupo-hendy", R("Hendy loans", hq), date="2025-12-29", currency="USD", principal=5527500, term_years=10, collateral="none",
            note_en="Passed to ITTI the next day.", note_es="Transferido a itti al día siguiente.")
flow("org:grupo-hendy", ITTI, 5527500, "USD", "2025-12-30", "transfer", "Hendy loan passed to ITTI the day after disbursement", "Crédito de Hendy transferido a itti al día siguiente", R("Hendy loans"), L_H3)
gq = "fueron transferidos en su totalidad a empresas vinculadas"
for d_, amt in (("2025-09-26", 13567500), ("2025-10-31", 4321500), ("2025-12-29", 5326500)):
    ln = loan(UB, "org:grupo-m", R("Grupo M loans", gq, "medium",
                                    "UH 10 Nov prints USD 14,3 millones for 26 Sep 2025; ABC 27 Oct prints US$ 4 millones for 31 Oct 2025." if amt != 5326500 else ""),
              date=d_, currency="USD", principal=amt, note_en="Transferred in full to ITTI, Red Digital and Kaitel.", note_es="Transferido en su totalidad a itti Saeca, Red Digital SA y Kaitel SA.")
    for to in (ITTI, RSA, "org:kaitel"):
        flow("org:grupo-m", to, None, "USD", d_[:7], "transfer", "Grupo M credit transferred in full to ITTI, Red Digital and Kaitel (split not given)",
             "Crédito de Grupo M transferido en su totalidad a itti, Red Digital y Kaitel (sin desglose)", R("Grupo M loans", gq), ln)
flow(ITTI, "org:grupo-m", None, "USD", "2026-04-29", "repayment", "First instalment of a Grupo M credit paid with ITTI funds", "Primera cuota de un crédito de Grupo M pagada con fondos de itti",
     R("Grupo M repayment", "", "medium", "UH 10 Nov gives the instalment as USD 4,32 millones."))
L_S = loan(UB, "org:satec", R("Satec", "transfirió el importe íntegro a Vinanzas SA"), date="2026-06-15", currency="USD", principal=20 * M)
flow("org:satec", VIN, 20 * M, "USD", "2026-06-15", "transfer", "Whole amount transferred to Vinanzas' account at Ueno", "Importe íntegro transferido a la cuenta de Vinanzas en ueno",
     R("Satec", "transfirió el importe íntegro a Vinanzas SA"), L_S)
for to in (ITTI, RSA, RPRO):
    flow("org:tuiu", to, None, None, "2025", "transfer", "TUIU credit proceeds passed at once or shortly to cover overdrafts, invoices and commitments of related companies (2025-2026)",
         "Fondos de créditos de TUIU transferidos de inmediato o en plazo próximo para cubrir sobregiros, facturas y compromisos de relacionadas (2025-2026)",
         R("TUIU", "sin vinculación con el desarrollo autónomo de la actividad"))
fact("org:grupo-hendy", "average_monthly_income", 73 * M, "PYG", "average monthly income during 2025 (BCP)", "2025", R("Hendy finances"))
fact("org:grupo-hendy", "equity_sign", -1, None, "net equity negative at end-2024 (no figure published); value -1 is a sign flag only", "2024-12-31", R("Hendy finances"))

# ---------------------------------------------------------------- UH 5 Nov 2026 (27 charged: corporate roles only)
u = src("src:ultimahora-2026-11-05-27-imputados", "press", "Última Hora", "¿Quiénes son y qué rol tuvieron los 27 imputados en el caso ueno bank?", "2026-11-05",
        "https://www.ultimahora.com/quienes-son-y-que-rol-tuvieron-los-27-imputados-en-el-caso-ueno-bank")
C = lambda q="", note="": P("prosecution", u, "list of 27", q, "medium", ("Role as described in the indictment per Última Hora. " + note).strip())
rr = [
    ("person:miguel-vazquez", UB, "vice_president", "vicepresidente 1° de ueno bank", "First vice-president.", None),
    ("person:miguel-vazquez", GV, "controlling_group", "", "Controlling shareholder ('controlante') until 2025 per the indictment; rating report still shows him president and 75.92% holder at Dec 2025.", None),
    ("person:miguel-vazquez", "org:grupo-m", "beneficial_owner", "", "Final beneficiary of 60%.", 60),
    ("person:miguel-vazquez", ITTI, "beneficial_owner", "", "Final beneficiary of 99%.", 99),
    ("person:juan-manuel-gustale", UB, "president", "presidente ueno bank", "", None),
    ("person:julio-rey", UB, "vice_president", "ex vicepresidente 2° de ueno bank", "Former second vice-president.", None),
    ("person:diana-mongelos", UB, "director", "directora titular de ueno bank", "", None),
    ("person:mariana-torres", UB, "director", "ex directora titular de ueno bank", "Former director.", None),
    ("person:alejandro-gomez-abente", UB, "director", "director titular de ueno bank", "", None),
    ("person:diego-duarte", UB, "director", "director titular de ueno bank", "", None),
    ("person:miguel-angel-almada", UB, "statutory_auditor", "síndico titular de ueno bank", "", None),
    ("person:jose-augusto-sala-cardozo", "org:mowi", "president", "accionista, presidente y representante legal de la empresa Mowi SA", "Also shareholder and legal representative.", None),
    ("person:sergio-pizurno", "org:mowi", "vice_president", "accionista y vicepresidente de la empresa Mowi SA", "Also shareholder.", None),
    ("person:sergio-pizurno", "org:grupo-m", "director", "", "Titular director.", None),
    ("person:vanessa-godoy", "org:grupo-hendy", "president", "vicepresidenta y luego presidenta de la empresa Grupo Hendy SA", "Shareholder; vice-president, later president.", None),
    ("person:oscar-urdapilleta", "org:grupo-hendy", "vice_president", "presidente y luego vicepresidente de la empresa Grupo Hendy SA", "Shareholder; president, later vice-president.", None),
    ("person:oscar-urdapilleta", "org:grupo-m", "vice_president", "", "", None),
    ("person:cesar-mengual", "org:grupo-hendy", "president", "presidente del Grupo Hendy SA", "", None),
    ("person:miguel-angel-garay", "org:grupo-hendy", "director", "director titular de Grupo Hendy SA", "", None),
    ("person:cesar-astigarraga", "org:grupo-m", "president", "presidente del Grupo M SA", "", None),
    ("person:luis-ernesto-angulo", "org:grupo-m", "vice_president", "vicepresidente Grupo M SA", "", None),
    ("person:guillermo-vazquez", "org:grupo-m", "director", "director titular del Grupo M SA", "", None),
    ("person:diego-gomez", "org:grupo-m", "president", "accionista y presidente del Grupo M SA", "Also shareholder.", None),
    ("person:luis-fernando-rios", "org:tuiu", "vice_president", "accionista y vicepresidente de TUIU SA", "Also shareholder.", None),
    ("person:andre-gayol-pires", "org:tuiu", "shareholder", "accionista de TUIU SA", "", None),
    ("person:nicolas-di-iorio", "org:tuiu", "shareholder", "accionista de TUIU SA", "", None),
    ("person:rodrigo-franco", "org:tuiu", "president", "presidente y representante legal de TUIU SA", "Also legal representative.", None),
    ("person:mauro-vargas", "org:franede", "president", "accionista presidente de Franede SA", "Shareholder and president.", None),
    ("person:mauro-vargas", "org:aime", "shareholder", "", "", None),
    ("person:cecilia-dominguez", "org:franede", "vice_president", "vicepresidenta de Franede SA", "", None),
    ("person:martin-vargas", "org:aime", "shareholder", "accionista de Aime SA Corredores de Seguros", "", None),
    ("person:gloria-villasanti", "org:aime", "president", "presidenta de Aime SA Corredores de Seguros", "", None),
    ("person:raul-sanchez", "org:aime", "director", "director titular de Aime SA Corredores de Seguros", "", None),
]
for h, o, r, q, ne, pct in rr:
    role(h, o, r, C(q), pct=pct, note_en=ne, note_es="")
fact("org:mowi", "share_count", 8000, None, "total shares in 2021; the group's principal held 1 share (G. 1,000,000) while vice-president", "2021", C())
for o in ("org:grupo-hendy", "org:tuiu", "org:franede", "org:office-design", "org:nubicom"):
    role(ITTI, o, "controlling_group", C("propiedad de itti y Grupo Vázquez antes", "Prosecution statement covers 'itti y Grupo Vázquez' jointly; no dates or percentages."),
         note_en="Owned by ITTI and Grupo Vázquez before receiving the loans (prosecution view as reported).", note_es="Propiedad de itti y Grupo Vázquez antes de recibir los créditos (según Fiscalía).")

# ---------------------------------------------------------------- UH 17 Nov 2026 (Galadriel)
g = src("src:ultimahora-2026-11-17-galadriel", "press", "Última Hora",
        "Vaciamiento: ueno prestó USD 15 millones sin proyecto de inversión, flujo de caja ni análisis de riesgo", "2026-11-17",
        "https://www.ultimahora.com/vaciamiento-ueno-presto-usd-15-millones-sin-proyecto-de-inversion-flujo-de-caja-ni-analisis-de-riesgo")
G = lambda loc, q="", conf="medium", note="": P("regulator", g, loc, q, conf, note)
L_G = loan(UB, "org:galadriel", G("loan", "identificada con el número 612661005074", "medium", "ABC 14 Nov rounds to US$ 15 millones."), op_number="612661005074", date="2026-07-31",
           term_days=720, currency="USD", principal=15_070_000, collateral="none", amortisation="bullet (capital at maturity)",
           note_en="No investment project, projected cash flow or risk analysis in the file per SIB; rate not reported.", note_es="Sin proyecto de inversión, flujo de caja ni análisis de riesgo según la SIB; tasa no informada.")
flow("org:galadriel", ITTI, None, "USD", "2026-07-31", "transfer", "Loan proceeds transferred from Galadriel to ITTI", "Fondos del préstamo transferidos de Galadriel a itti",
     G("flow", "transferencias desde la empresa hacia itti", "medium", "No amounts or dates of transfers given; date is disbursement date."), L_G, precision="month")
flow(ITTI, "org:nubicom", None, "USD", "2026-07-31", "transfer", "Funds passed on to Nubicom Paraguay, which used them to cancel loans at Ueno", "Fondos transferidos a Nubicom Paraguay, que canceló préstamos con ueno",
     G("flow", "para cancelar préstamos que mantenían con ueno bank"), L_G, precision="month")
fact("org:galadriel", "capital_owed_to_ueno_bank", 87941 * M, "PYG", "principal owed at end of September 2026", "2026-09-30",
     G("balance", "capital adeudado por la firma alcanzaba G. 87.941 millones", "medium", "UH debtor list (7 Nov) prints G. 88.623 millones."))
for d_, h, pct in (("2026-07-30", "person:bruno-vaccotti-ramos", 90), ("2026-07-31", "person:ramon-hernandez-sanabria", 10)):
    role(h, "org:galadriel", "shareholder", G("p. 164 of file", "", "medium", "Board minutes of 30 and 31 Jul 2026; which minute covers which transfer is not specified."), pct=pct, start="2026-07",
         note_en="Acquired via transfers recorded the day before and the day of the disbursement.", note_es="Adquirido mediante transferencias asentadas el día anterior y el día del desembolso.")
for h in ("person:antonio-villa-berkemeyer", "person:jorge-peralta-sosa"):
    role(h, "org:galadriel", "founder", G("profile", "creada en 2025 por Antonio Villa Berkemeyer"), start="2025")
event("2026-07-31", "credit", "Ueno lends USD 15.07m to Galadriel; shares change hands the same days", "ueno presta USD 15,07 millones a Galadriel; las acciones cambian de manos esos días",
      "Unsecured 720-day bullet loan (op. 612661005074); board minutes of 30-31 Jul 2026 record transfer of 90% and 10% of shares. SIB later ordered reclassification to risk category 3.",
      "Préstamo bullet a 720 días sin garantía real (op. 612661005074); actas del 30 y 31/07/2026 registran transferencia del 90% y 10% de acciones. La SIB ordenó reclasificar a categoría 3.",
      [UB, "org:galadriel", ITTI, "org:nubicom"], G("loan", "fue concedida el 31 de julio de 2026"), 15_070_000, "USD")

# ---------------------------------------------------------------- ABC 8 Oct 2026
a = src("src:abc-2026-10-08-maniobras-ocultar-nexos", "press", "ABC Color", "BCP detectó maniobras de Ueno Bank para ocultar nexos con empresas", "2026-10-08",
        "https://www.abc.com.py/economia/2026/10/08/bcp-detecto-maniobras-de-ueno-bank-para-ocultar-nexos-con-empresas/")
A = lambda loc, q="", conf="medium", note="": P("regulator", a, loc, q, conf, note)
event("2013", "corporate", "Grupo Hendy founded", "Fundación de Grupo Hendy", "Founded in 2013 by four individuals (company behind Hendyla.com).", "Fundada en 2013 por cuatro personas (empresa detrás de Hendyla.com).",
      ["org:grupo-hendy"], A("Hendy history", "firma fundada en 2013"))
event("2023-10", "corporate", "ITTI takes majority control of Grupo Hendy", "Itti pasa a tener el control mayoritario de Grupo Hendy", "Percentage not stated.", "Porcentaje no indicado.",
      [ITTI, "org:grupo-hendy"], A("Hendy history", "control mayoritario de Itti Saeca"))
event("2025-09-30", "corporate", "ITTI sells 90% of Grupo Hendy; remaining 10% also transferred", "Itti vende el 90% de Grupo Hendy; el 10% restante también se transfiere",
      "90% sold to Vanessa Godoy; remaining 10% (held by ITTI and Grupo Vázquez) transferred to Óscar Urdapilleta, who appeared in Bankitti as an ITTI employee.",
      "90% vendido a Vanessa Godoy; el 10% restante (de Itti y Grupo Vázquez) transferido a Óscar Urdapilleta, que figuraba en Bankitti como funcionario de Itti.",
      [ITTI, GV, "org:grupo-hendy", "person:vanessa-godoy", "person:oscar-urdapilleta"], A("Hendy history", "vendió el 90% de sus acciones"))
role("person:vanessa-godoy", "org:grupo-hendy", "shareholder", A("Hendy history", "vendió el 90% de sus acciones"), pct=90, start="2025-09-30")
role("person:oscar-urdapilleta", "org:grupo-hendy", "shareholder", A("Hendy history", "fue transferido a Óscar Urdapilleta"), pct=10, start="2025-09-30")
role("person:oscar-urdapilleta", ITTI, "employee", A("Hendy history", "", "medium", "Per Bankitti records cited in the BCP report."))
role("person:oscar-urdapilleta", RSA, "director", A("Hendy history"), note_en="Titular director of Red Digital SA.", note_es="Director titular de Red Digital SA.")
role("person:oscar-urdapilleta", "org:ueno-casa-de-bolsa", "director", A("Hendy history"), note_en="Titular director of Ueno Casa de Bolsa SA.", note_es="Director titular de Ueno Casa de Bolsa SA.")
role("person:vanessa-godoy", "org:mowi", "alternate_statutory_auditor", A("Mowi", "síndico suplente en Mowi SA"))
fact("org:grupo-hendy", "debt_to_ueno_bank", 252521 * M, "PYG", "accumulated balance up to April 2026 (about USD 42 million)", "2026-04", A("Hendy credit", "G. 252.521 millones"))
fact("org:grupo-hendy", "average_monthly_income", 73 * M, "PYG", "average monthly income in 2025", "2025", A("Hendy finances", "apenas G. 73 millones mensuales"))
fact(UB, "public_and_ips_funds_in_custody", 850 * M, "USD", "approximate public and IPS funds in custody", "2026", P("press", a, "context", "US$ 850 millones de fondos públicos"))

# ---------------------------------------------------------------- ABC 11 Oct 2026 (Grupo M)
m = src("src:abc-2026-10-11-itti-cedio-otra-empresa", "press", "ABC Color", "Itti \"cedió\" otra empresa a empleado y Ueno le prestó US$ 62 millones", "2026-10-11",
        "https://www.abc.com.py/politica/2026/10/11/itti-cedio-otra-empresa-a-empleado-y-ueno-le-presto-us-62-millones/")
Mp = lambda loc, q="", conf="medium", note="": P("regulator", m, loc, q, conf, note)
GM = "org:grupo-m"
event("2014", "corporate", "Grupo M constituted with capital of G. 100 million", "Constitución de Grupo M con capital de G. 100 millones", "Company behind Pagopar.", "Sociedad detrás de Pagopar.", [GM],
      Mp("profile", "fue constituida con un capital de G. 100 millones"), 100 * M, "PYG")
role("person:miguel-vazquez", GM, "beneficial_owner", Mp("ownership history", "dos nuevos beneficiarios finales"), pct=60, start="2024-01-17")
role("person:jack-fleischman", GM, "beneficial_owner", Mp("ownership history", "dos nuevos beneficiarios finales"), pct=26.83, start="2024-01-17")
role(ITTI, GM, "shareholder", Mp("ownership history", "Itti pasó a tener el 60,82%", "medium", "ABC 8 Sep: ITTI notified Conacom of acquiring 50% (Res. 69/2024, 30 Aug 2024)."), pct=60.82, start="2024-07-13")
role(ITTI, GM, "shareholder", Mp("ownership history", "Itti pasó a controlar el 99,02%"), pct=99.02, start="2025-07-30", end="2025-09-30")
role(GV, GM, "shareholder", Mp("ownership history"), pct=0.98, start="2025-07-30", end="2025-09-30")
role("person:oscar-urdapilleta", GM, "shareholder", Mp("ownership history", "", "medium", "90% stake valued at G. 1.476 millones."), pct=90, start="2025-09-30")
role("person:diego-gomez", GM, "shareholder", Mp("ownership history"), pct=10, start="2025-09-30", note_en="Described as CEO of Hanoi SA (Monchis), a Grupo Vázquez company.", note_es="Descrito como CEO de Hanoi SA (Monchis), empresa del Grupo Vázquez.")
event("2025-09-30", "corporate", "ITTI transfers Grupo M to an ITTI employee (90%) and the Hanoi SA CEO (10%)", "Itti transfiere Grupo M a un empleado de Itti (90%) y al CEO de Hanoi SA (10%)",
      "The 90% stake is valued at G. 1,476 million.", "El 90% está valuado en G. 1.476 millones.", [ITTI, GM, "person:oscar-urdapilleta", "person:diego-gomez"], Mp("ownership history", "Itti transfirió 1.476 acciones"), 1476 * M, "PYG")
fact(GM, "credit_granted_by_ueno_total", 62023077, "USD", "total of three credit operations (Phase 1 USD 23,100,000; Phase 2 USD 38,923,077), 7-8 years, 7.5%-8%, sole signature", "2025-09/2026-04",
     Mp("loans", "suman US$ 62.023.077"))
loan(UB, GM, Mp("loans", "préstamo de US$ 23.100.000"), date="2025", currency="USD", principal=23_100_000, collateral="none",
     note_en="'Phase 1'; terms 7 and 8 years and rates 7.5%-8% are given for the credits as a group.", note_es="'Fase 1'; plazos de 7 y 8 años y tasas de 7,5%-8% para el conjunto.")
loan(UB, GM, Mp("loans", "en la Fase 2, US$ 38.923.077"), date="2026", currency="USD", principal=38923077, collateral="none",
     note_en="'Phase 2'; date range Sept 2025-Apr 2026 for all operations; year here is indicative.", note_es="'Fase 2'; operaciones entre setiembre de 2025 y abril de 2026.")
fact(GM, "debt_to_ueno_bank", 237105 * M, "PYG", "outstanding balance (about USD 39 million)", "2026-04", Mp("balance", "saldo pendiente era de G. 237.105 millones"))
fact(GM, "long_term_debt_to_income_ratio", 11.85, None, "long-term debt as multiple of income of the analysed period", "2025", Mp("indicators", "supera aproximadamente 11,85 veces los ingresos"))
role("person:sergio-pizurno", GM, "director", Mp("context", "director titular en Grupo M SA"), note_en="Previously general manager of Itti (2021) and Wepa (2021-2024) per ABC.", note_es="Antes gerente general de Itti (2021) y Wepa (2021-2024) según ABC.")

# ---------------------------------------------------------------- ABC 12 Oct 2026 (USD 146m)
o = src("src:abc-2026-10-12-ueno-movio-146-millones", "press", "ABC Color", "Ueno movió US$ 146 millones hacia tres empresas vinculadas", "2026-10-12",
        "https://www.abc.com.py/politica/2026/10/12/ueno-movio-us-146-millones-hacia-tres-empresas-vinculadas/")
O = lambda loc, q="", conf="medium", note="": P("regulator", o, loc, q, conf, note)
fact(UB, "credit_moved_to_mowi_hendy_grupo_m", 146 * M, "USD", "total moved to the three firms Sep 2025-May 2026 (about G. 880,000 million); 35% of effective equity", "2025-09/2026-05",
     O("totals", "Ueno movió US$ 146 millones", "medium", "Article body also prints US$ 145 millones; ABC 10 Oct gives balance G. 743.784 millones (30%) at 30 Apr 2026."))
fact(UB, "effective_equity", 410 * M, "USD", "effective equity in USD as printed", "2026-04", O("totals", "35% del patrimonio efectivo"))
fact(UB, "loans_to_mowi_hendy_grupo_m_sep_dec_2025", 69_700_000, "USD", "loans Sep-Dec 2025 per Informe SBGS.ISEFS.SEFS. 4 Nº 006/2026 (8 Jun 2026)", "2025-09/2025-12", O("source documents"))
fact("org:mowi", "credit_granted_by_ueno_total", 42_500_000, "USD", "total credit Sep 2025-May 2026", "2025-09/2026-05", O("Mowi"))
fact("org:grupo-hendy", "credit_granted_by_ueno_total", 42 * M, "USD", "total credit Sep 2025-May 2026", "2025-09/2026-05", O("Hendy"))
fact("org:grupo-m", "credit_granted_by_ueno_total", 62 * M, "USD", "total credit Sep 2025-May 2026", "2025-09/2026-05", O("Grupo M"))
BR = "ABC writes 'Redisa (Upay)' and 'Redipro (Wepa)' here; Solventa pairs Red Digital = Wepa and Red Digital de Procesamiento = Upay."
L_MW2 = loan(UB, "org:mowi", O("Mowi", "préstamo de Ueno Bank (US$ 5,4 millones)"), date="2025-10-30", currency="USD", principal=5_400_000, collateral="none")
flow("org:mowi", RSA, 5_400_000, "USD", "2025-10-30", "transfer", "Mowi loan sent to Redisa to partly cover overdrafts", "Préstamo de Mowi girado a Redisa para cubrir sobregiros de forma parcial",
     O("transfers", "para cubrir sobregiros de forma parcial", "medium", BR), L_MW2, approx=True)
flow("org:grupo-hendy", ITTI, 5_100_000, "USD", "2025-10-30", "transfer", "Hendy transferred funds to Itti to cover part of an overdraft", "Hendy giró fondos a Itti para cubrir parte de un sobregiro",
     O("transfers", "giró US$ 5,1 millones a Itti"), approx=True)
flow("org:mowi", RPRO, 33500 * M, "PYG", "2025-12-30", "transfer", "Mowi funds sent to Redipro; debits labelled 'Acreditación Upay'", "Fondos de Mowi enviados a Redipro; débitos rotulados 'Acreditación Upay'",
     O("transfers", "Acreditación Upay", "medium", BR))
flow("org:grupo-hendy", ITTI, 5_500_000, "USD", "2025-12-30", "transfer", "Hendy loan sent to Itti, concept 'Pago Itti'", "Préstamo de Hendy enviado a Itti, concepto 'Pago Itti'", O("transfers", "Pago Itti"), approx=True)
flow("org:grupo-m", ITTI, 5_300_000, "USD", "2025-12-30", "transfer", "Grupo M loan sent to Itti", "Préstamo de Grupo M enviado a Itti", O("transfers", "US$ 5,3 millones a la misma empresa"), approx=True)
for f_ in ("org:mowi", "org:grupo-hendy"):
    for t_ in (ITTI, RPRO):
        flow(f_, t_, None, None, "2025-09-30", "transfer", "Loan proceeds moved to cover Itti overdrafts (amount not stated)", "Fondos de préstamos para cubrir sobregiros de Itti (sin monto)",
             O("transfers", "con el fin de cubrir sobregiros de Itti"))
role("person:jose-augusto-sala-cardozo", "org:mowi", "shareholder", O("ownership changes", "exsubgerente de Ueno Bank"), start="2025-09-30")
role("person:sergio-pizurno", "org:mowi", "shareholder", O("ownership changes"), start="2025-09-30",
     note_en="Described as former general manager of Grupo Vázquez, now commercial director of Technoma SA.", note_es="Descrito como exgerente general del Grupo Vázquez, ahora director comercial de Technoma SA.")
role("person:sergio-pizurno", "org:technoma", "officer", O("ownership changes"), note_en="Commercial director.", note_es="Director comercial.")
role("person:vanessa-godoy", ITTI, "employee", O("ownership changes", "encargada de Talento Humano de Itti"), note_en="Head of human talent at Itti.", note_es="Encargada de Talento Humano de Itti.")
event("2026-06-08", "supervisory", "Informe SBGS.ISEFS.SEFS. 4 Nº 006/2026 (ABC citation)", "Informe SBGS.ISEFS.SEFS. 4 Nº 006/2026 (cita de ABC)",
      "Report of the BCP's systemic-entities supervision office; reports USD 69.7 million of loans to the three firms Sep-Dec 2025 on sole signature.",
      "Informe de la Intendencia de Supervisión de EFS del BCP; reporta USD 69,7 millones en préstamos a las tres firmas entre set. y dic. de 2025, a sola firma.",
      ["auth:bcp", UB, "org:mowi", "org:grupo-hendy", "org:grupo-m"], O("source documents", "a sola firma", "medium", "Same report number as UH 10 Nov ('Informe SEFS 4 Nº 006/2026 sobre el grupo GPV 1535')."))

# ---------------------------------------------------------------- ABC 15 Oct 2026 (Redisa/Redipro stakes)
k = src("src:abc-2026-10-15-acciones-conacom", "press", "ABC Color", "Ueno Bank modifica sus acciones para evitar deducciones, pero contradice a Conacom", "2026-10-15",
        "https://www.abc.com.py/abc-color/2026/10/15/ueno-bank-modifica-sus-acciones-para-evitar-deducciones-pero-contradice-a-conacom/")
K = lambda by, loc, q="", conf="medium", note="": P(by, k, loc, q, conf, note)
for org, rows in ((RSA, [(72.12, "2026-03", "company", "US offering memorandum (projection), pp. 20-21"), (77.12, "2026-08-28", "company", "ITTI communication to Conacom"),
                         (53.27, "2026-09-11", "company", "ITTI report to Conacom"), (49.0, "2026-10-04", "company", "Ueno Bank statement of 15 Oct 2026")]),
                  (RPRO, [(86.02, "2026-03", "company", "US offering memorandum (projection), pp. 20-21"), (83.54, "2026-08-28", "company", "ITTI communication to Conacom"),
                          (59.98, "2026-09-11", "company", "ITTI report to Conacom"), (49.06, "2026-10-04", "company", "Ueno Bank statement of 15 Oct 2026")])):
    for pct, d_, by, doc in rows:
        role(UB, org, "shareholder", K(by, doc, "", "medium", "ABC notes the September ITTI filing contradicts Ueno's claim of holding under 50%." if d_ >= "2026-09" else ""), pct=pct, start=d_,
             note_en=f"Stake as of {d_} per {doc}.", note_es=f"Participación al {d_} según: {doc}.")
fact(RPRO, "funds_placed_by_ueno_bank", 640409 * M, "PYG", "Ueno's fund participation in Redipro at 2025 balance close (BCP memo)", "2025-12-31",
     K("regulator", "BCP memo of 29 Jun 2026", "", "medium", "US memorandum (Mar 2026) prints G. 640.469 millones (USD 106 million)."))
fact(RPRO, "funds_placed_by_ueno_bank", 640469 * M, "PYG", "placements in Redipro per US investor memorandum (about USD 106 million)", "2025-12-31", K("company", "US memorandum, March 2026"))
fact(RSA, "funds_placed_by_ueno_bank", 236231 * M, "PYG", "Ueno's fund participation in Redisa at 2025 balance close (about USD 40 million)", "2025-12-31", K("regulator", "BCP memo of 29 Jun 2026"))
fact(UB, "funds_placed_in_redisa_and_redipro", 876640 * M, "PYG", "participation of funds in Redipro and Redisa (about USD 146 million), said not to comply with solvency-calculation rule", "2025-12-31",
     K("regulator", "BCP memo of 29 Jun 2026", "", "medium", "ABC 27 Oct prints G. 876.300 millones for the same item."))
event("2026-06-29", "supervisory", "BCP director's memo questions Redisa/Redipro holdings in solvency calculation", "Memorando de directora del BCP cuestiona participaciones en Redisa/Redipro para la solvencia",
      "Memo by BCP board member Carmen Marín, from an intervention recorded in the minutes of 19 Jun 2026; asked the SIB for an exhaustive review of the G. 876,640 million participation.",
      "Memorando de la directora Carmen Marín, a partir de intervención en el acta del 19/06/2026; pidió a la SIB una revisión exhaustiva de la participación de G. 876.640 millones.",
      ["auth:bcp", "auth:superintendencia-de-bancos", UB, RSA, RPRO], K("regulator", "BCP memo of 29 Jun 2026"), 876640 * M, "PYG")
event("2026-09-15", "supervisory", "Conacom opinion PARECER/DI No 15/2026", "PARECER/DI No 15/2026 de la Conacom", "Issued on the basis of ITTI's August data on Ueno's stakes in Redisa and Redipro.",
      "Emitido a partir de los datos de agosto de Itti sobre las participaciones de Ueno en Redisa y Redipro.", [ITTI, UB, RSA, RPRO], K("regulator", "Conacom", "", "medium", "Asserted by the competition authority (Conacom)."))
event("2026-10-15", "statement", "Ueno says it has held under 50% of Redisa and Redipro since 4 Oct 2026", "Ueno afirma tener menos del 50% de Redisa y Redipro desde el 4/10/2026",
      "Bank statement: 49% and 49.06%. ABC notes ITTI's 11 Sep filing showed 53.27% and 59.98%.", "Comunicado del banco: 49% y 49,06%. ABC señala que el informe de Itti del 11/9 mostraba 53,27% y 59,98%.",
      [UB, RSA, RPRO], K("company", "Ueno statement", "mantiene una participación inferior al 50 %"))

# ---------------------------------------------------------------- El Observador 4 Nov 2026 (Mowi)
ob = src("src:elobservador-2026-11-04-empresas-vinculadas", "press", "El Observador", "Empresas vinculadas de UENO extrajeron cifras millonarias a sola firma y sin garantías", "2026-11-04",
         "https://observador.com.py/ueno-dilapido-dinero-del-publico-en-prestamos-sin-garantias-a-sus-empresas-vinculadas/")
B = lambda loc, q="", conf="medium", note="": P("regulator", ob, loc, q, conf, note)
MW = "org:mowi"
event("2021-01-12", "corporate", "Mowi S.A. incorporated", "Constitución de Mowi S.A.", "7,999 shares held by Grupo Vázquez and 1 by its principal.", "7.999 acciones del Grupo Vázquez y 1 de Miguel Vázquez.",
      [MW, GV, "person:miguel-vazquez"], B("Mowi history", "fue constituida el 12 de enero del 2021"))
role(GV, MW, "shareholder", B("Mowi history", "7999 acciones del Grupo Vázquez y 1 de Miguel Vázquez"), start="2021-01-12", note_en="7,999 of 8,000 shares at incorporation.", note_es="7.999 de 8.000 acciones en la constitución.")
role("person:miguel-vazquez", MW, "shareholder", B("Mowi history", "7999 acciones del Grupo Vázquez y 1 de Miguel Vázquez"), start="2021-01-12", end="2025-09-09", note_en="1 share; sold 9 Sep 2025.", note_es="1 acción; vendida el 9/9/2025.")
event("2025-09-09", "corporate", "Mowi shares transferred to a former Ueno sub-manager and another executive", "Acciones de Mowi transferidas a un exsubgerente de Ueno y a otro ejecutivo",
      "Miguel Vázquez sold his share to José Sala; ITTI SAECA sold Sala 7,199 shares and Sergio Pizurno its remaining 800 (dates of the ITTI sales not stated).",
      "Miguel Vázquez vendió su acción a José Sala; ITTI SAECA vendió a Sala 7.199 acciones y a Sergio Pizurno sus 800 restantes (fechas de las ventas de ITTI no indicadas).",
      [MW, ITTI, "person:miguel-vazquez", "person:jose-augusto-sala-cardozo", "person:sergio-pizurno"],
      B("Mowi history", "Miguel Vázquez vendió su acción a José Sala", "medium", "Article says the 7,999 shares were Grupo Vázquez's at incorporation but that ITTI sold them in 2025; intermediate transfer not explained. ABC 12 Oct dates the change 'by 30 Sep 2025'."))
role("person:jose-augusto-sala-cardozo", MW, "shareholder", B("Mowi history", "ITTI SAECA le vendió al mismo Sala 7.199 acciones"), start="2025-09-09", note_en="7,199 shares from ITTI plus 1 from the group's principal (of 8,000).", note_es="7.199 acciones de ITTI más 1 de Miguel Vázquez (de 8.000).")
role("person:sergio-pizurno", MW, "shareholder", B("Mowi history", "a Sergio Pizurno sus 800 acciones restantes"), start="2025-09", note_en="800 shares from ITTI (of 8,000).", note_es="800 acciones de ITTI (de 8.000).")
role("person:cesar-astigarraga", MW, "statutory_auditor", B("Mowi officers", "era al mismo tiempo síndico titular de Ueno Bank"), start="2024-04-30", note_en="Titular syndic at assembly of 30 Apr 2024.", note_es="Síndico titular en la asamblea del 30/04/2024.")
role("person:cesar-astigarraga", UB, "statutory_auditor", B("Mowi officers", "era al mismo tiempo síndico titular de Ueno Bank"), end="2026-03-27", note_en="Titular syndic of Ueno Bank until 27 Mar 2026.", note_es="Síndico titular de Ueno Bank hasta el 27/03/2026.")
role("person:vanessa-godoy", MW, "alternate_statutory_auditor", B("Mowi officers", "fue Síndico Suplente en la asamblea del 9 de mayo"), start="2025-05-09")
event("2025-10", "supervisory", "Ueno asks to de-link Mowi, Grupo Hendy and Grupo M without supporting documents", "Ueno solicita desvincular a Mowi, Grupo Hendy y Grupo M sin documentación",
      "Documents were only sent in May 2026 at the supervisor's request; the SIB concluded the firms remained related.", "La documentación recién se remitió en mayo de 2026 a pedido del supervisor; la SIB concluyó que seguían vinculadas.",
      [UB, MW, "org:grupo-hendy", "org:grupo-m", "auth:superintendencia-de-bancos"], B("de-linking", "solicitó su desvinculación"))
