from lib import *

UB, GV, ITTI, VIN, RSA, RPRO = "org:ueno-bank", "org:grupo-vazquez", "org:itti", "org:vinanzas", "org:redisa", "org:redipro"

# ---------------------------------------------------------------- FIX SCR: Grupo Vázquez (2 Jul 2026)
f = src("src:fixscr-2026-07-02-grupo-vazquez", "rating", "FIX SCR", "Grupo Vázquez S.A.E. - informe de calificación (asignación), estados al 31/03/2026", "2026-07-02",
        "https://www.grupovazquez.com/wp-content/uploads/sites/2/2026/08/Grupo-Vazquez-S.A.E._compressed.pdf")
F = lambda loc, note="", conf="medium": P("rating_agency", f, loc, "", conf, note)
K = 1000
AN = "Anexo I, printed in thousands of Gs. under the heading 'Cifras No Consolidadas' although 2025 values match the consolidated summary on p. 1."
for k, q1, y25 in [("revenue", 575687078, 2191140536), ("ebitda", 271884338, 1048822291), ("net_result", 161735602, 644790158), ("total_assets", 7975811330, 6972560881),
                   ("total_debt", 2238705835, 2115730530), ("equity", 2091415075, 2501181143), ("cash_and_current_investments", 538259861, 694342804)]:
    fact(GV, k + "_fix", q1 * K, "PYG", "FIX figure; three months to / at 31 Mar 2026", "2026-Q1", F("Anexo I, pp. 10-11", AN))
    fact(GV, k + "_fix", y25 * K, "PYG", "FIX figure; year 2025 / at 31 Dec 2025", "2025-12-31",
         F("Anexo I, pp. 10-11", AN + (" Solventa prints EBITDA 576,534 million (consolidated) for 2025; different adjustments." if k == "ebitda" else "")))
fact(GV, "adjusted_financial_debt_fix", 2226482033 * K, "PYG", "total adjusted debt incl. off-balance-sheet debt", "2025-12-31", F("p. 1, Anexo I"))
for k, v, un, per in [("group_revenue_incl_bank", 367, "consolidated revenue incl. Ueno Bank", "2025"), ("group_ebitda_incl_bank", 136, "consolidated EBITDA incl. Ueno Bank", "2025"),
                      ("group_debt_incl_deposits", 3161, "total group debt incl. depositor funds", "2025-12-31"), ("group_debt_excl_deposits", 778, "group debt excluding Ueno depositor funds", "2025-12-31"),
                      ("net_assets_excl_deposits", 1362, "total assets net of saver deposits", "2025-12-31"), ("individual_ebitda", 27, "Grupo Vázquez individual EBITDA (leverage 9.5x)", "2025"),
                      ("stake_in_u_holdings_value", 546.8, "value of holding in U Holdings (USD 202.1 M in 2024)", "2025-12-31"),
                      ("local_market_bonds_outstanding", 124, "Grupo Vázquez bonds in local market (69% of group total USD 181 M)", "2025-12-31")]:
    fact(GV, k, int(v * M) if v != 546.8 else 546_800_000, "USD", "USD millions as printed by FIX; " + un, per,
         F("pp. 1-9", "FIX's own figures do not reconcile (USD 3,161 M less deposits USD 2,844 M is not USD 778 M)." if "debt" in k else ""))
fact(GV, "staff", 5000, None, "'more than 5,000' people in the group", "2026", F("p. 5", "Solventa prints 'more than 6,000' at Dec 2025."))
fact(UB, "revenue_usd", 221 * M, "USD", "Ueno Bank revenue, 60% of group revenue", "2025", F("p. 1"))
fact(UB, "ebitda_usd", 80 * M, "USD", "Ueno Bank EBITDA, 59% of group EBITDA", "2025", F("p. 1"))
fact(UB, "deposits_usd", 2844 * M, "USD", "saver deposits", "2025-12-31", F("pp. 2, 9"))
fact(UB, "related_party_assistance_limit", 64 * M, "USD", "20% of effective equity (equity base USD 322 M)", "2025-12-31", F("pp. 1, 3, 9", "ABC (10 Oct 2026) reports the cap as G. 493.447 millones (about USD 82 million) at Apr 2026."))
fact(UB, "staff", 500, None, "'more than 500' employees", "2026", F("p. 3"))
fact(UB, "senior_unsecured_bond_2031", 350 * M, "USD", "international senior unsecured bond issued March 2026, due 2031", "2026-03", F("pp. 2, 3, 9"))
fact(ITTI, "revenue_from_related_parties", 168 * M, "USD", "revenue from services to related parties, about 59% of ITTI revenue", "2025",
     F("p. 4", "La Nación (6 Nov 2026) relays FIX's November update as 59% of ITTI revenue coming from services to Ueno Bank specifically."))
fact(ITTI, "share_of_paraguay_financial_transactions_pct", 40, None, "percent of Paraguay's financial transactions processed ('más del 40%'); Bankitti used by 9 BCP-regulated entities", "2026", F("pp. 1, 4"))
fact(ITTI, "local_market_bonds_outstanding", 41 * M, "USD", "ITTI bonds in local market (22% of group total)", "2025-12-31", F("pp. 1, 9"))
role("org:u-paraguay", UB, "shareholder", F("p. 3"), pct=91.21, start="2025-12-31")
role("org:otp-bank", "org:u-holdings", "shareholder", F("pp. 3, 9", "FIX prints 6.4% (p. 3) and 6.3% (p. 9); contribution USD 30 M; date not given."), pct=6.4)
flow("org:otp-bank", "org:u-holdings", 30 * M, "USD", None, "other", "OTP Bank Plc capital contribution", "Aporte de capital de OTP Bank Plc", F("pp. 3, 9", "Date not stated by FIX; other sources say December 2025."))
event("2026-07-02", "market", "FIX SCR assigns Grupo Vázquez A+py, trend 'Fuerte'", "FIX SCR asigna a Grupo Vázquez A+py, tendencia 'Fuerte'",
      "Seven global programmes (G1-G4, USD1-USD3) rated pyA+; Ueno Bank at AA-py (FIX) at that date.", "Siete programas globales (G1-G4, USD1-USD3) en pyA+; Ueno Bank en AA-py (FIX) a esa fecha.",
      [GV, UB], F("pp. 1, 15-16", "", "high"))
event("2026-03", "market", "Ueno Bank issues USD 350 million senior unsecured notes due 2031", "Ueno Bank emite bono senior sin garantía por USD 350 millones con vencimiento 2031",
      "USD 50 M earmarked for SME portfolio, USD 300 M for corporate portfolio; no cross-default clauses with controlling-group companies per FIX.",
      "USD 50 M para cartera Pyme y USD 300 M para cartera corporativa; sin cláusulas de incumplimiento cruzado con el grupo controlante según FIX.", [UB], F("pp. 2, 3, 8-9"), 350 * M, "USD")

# ---------------------------------------------------------------- La Nación 6 Nov 2026: FIX downgrades
l1 = src("src:lanacion-2026-11-06-fix-rebaja-grupo-vazquez", "press", "La Nación (Paraguay)",
         "Crisis de ueno bank golpea al Grupo Vázquez: calificadora rebaja su nota y advierte alto riesgo de incumplimiento", "2026-11-06",
         "https://www.lanacion.com.py/negocios/2026/11/06/crisis-de-ueno-bank-golpea-al-grupo-vazquez-calificadora-rebaja-su-nota-y-advierte-alto-riesgo-de-incumplimiento/")
L1 = lambda loc, q="", note="": P("rating_agency", l1, loc, q, "medium", ("FIX SCR update of 3 Nov 2026 as relayed by La Nación. " + note).strip())
event("2026-11-03", "market", "FIX SCR cuts Grupo Vázquez from A+py to Cpy", "FIX SCR rebaja a Grupo Vázquez de A+py a Cpy",
      "Seven bond programmes cut from pyA+ to pyC; Ueno Bank at Dpy. Could fall to Dpy/pyD if the next debt service is missed; report does not state a missed payment.",
      "Siete programas de bonos bajan de pyA+ a pyC; ueno bank en Dpy. Podría bajar a Dpy/pyD si incumple el próximo servicio de deuda; no declara incumplimiento.",
      [GV, UB], L1("rating action", "pasó de A+py a Cpy", "Solventa's May 2026 report lists six programmes; FIX counts seven."))
for k, v, un in [("group_debt_excl_ueno_bank", 341, "group debt excluding Ueno Bank"), ("bonds_outstanding_usd", 204, "of which obligaciones negociables"),
                 ("cash_and_current_investments_usd", 71, "cash and current investments (approx.)"), ("short_term_maturities_usd", 54, "short-term maturities")]:
    fact(GV, k, v * M, "USD", un, "2026-06", L1("figures"))
fact(GV, "bond_principal_due", 300000, "USD", "principal due", "2027-09", L1("upcoming payments"))
fact(GV, "bond_principal_due", 4 * M, "USD", "principal due", "2027-12", L1("upcoming payments"))
event("2026-11-19", "market", "Grupo Vázquez bond interest falls due from this date (per FIX)", "Vencen intereses de bonos del Grupo Vázquez desde esta fecha (según FIX)",
      "Amount not stated; whether paid is not reported in the sources opened.", "Monto no indicado; no se informa si se pagó en las fuentes abiertas.", [GV], L1("upcoming payments"))
l2 = src("src:lanacion-2026-11-06-fix-rebaja-itti", "press", "La Nación (Paraguay)",
         "Caso ueno: ITTI cae de A+ a C en calificación de riesgo y advierten posible incumplimiento de deudas", "2026-11-06",
         "https://www.lanacion.com.py/negocios/2026/11/06/caso-ueno-itti-cae-de-a-a-c-en-calificacion-de-riesgo-y-advierten-posible-incumplimiento-de-deudas/")
L2 = lambda loc, q="", note="": P("rating_agency", l2, loc, q, "medium", ("FIX SCR update of 3 Nov 2026 as relayed by La Nación. " + note).strip())
event("2026-11-03", "market", "FIX SCR cuts ITTI from A+py to Cpy", "FIX SCR rebaja a ITTI de A+py a Cpy",
      "Five programmes (G1, G2, USD1, USD2, USD3) cut from pyA+ to pyC; could fall to Dpy on a missed debt service; no default confirmed.",
      "Cinco programas (G1, G2, USD1, USD2, USD3) bajan de pyA+ a pyC; podría caer a Dpy si incumple; no se confirma impago.", [ITTI],
      L2("rating action", "Podría descender nuevamente, hasta la categoría Dpy"))
fact(ITTI, "revenue_share_from_ueno_bank_pct", 59, None, "percent of ITTI revenue from services to Ueno Bank", "2026",
     L2("figures", "", "FIX's July 2026 report words the 59% as revenue from related parties (USD 168 M), not Ueno Bank alone."))
for k, v, un, per in [("total_debt_usd", 66, "total debt, consolidated", "2026-06"), ("bonds_outstanding_usd", 40, "obligaciones negociables", "2026-06"),
                      ("cash_and_current_investments_usd", 35, "cash and current investments (approx.)", "2026-06"), ("short_term_maturities_usd", 22, "short-term consolidated maturities", "2026-06"),
                      ("bond_debt_service_due", 10, "capital and interest on bonds due in 2027 (approx.)", "2027")]:
    fact(ITTI, k, v * M, "USD", un, per, L2("figures"))

# ---------------------------------------------------------------- ABC 6 Nov 2026: asset freeze
z = src("src:abc-2026-11-06-juez-bloquea-bienes", "press", "ABC Color", "Caso Ueno: juez bloquea bienes de otras empresas vinculadas al Grupo Vázquez", "2026-11-06",
        "https://www.abc.com.py/nacionales/2026/11/06/caso-ueno-juez-bloquea-bienes-de-otras-empresas-vinculadas-al-grupo-vazquez/")
Z = lambda loc, q="": P("prosecution", z, loc, q, "medium", "Allegation in the prosecutors' request as reported by ABC.")
TEN = [ITTI, GV, RSA, RPRO, "org:satec", "org:hd-invest", "org:technoma", "org:la-tropa-fletes", "org:factopar", "org:kasas-propiedades"]
event("2026-11-06", "criminal", "Judge freezes assets and accounts of ten more Grupo Vázquez-linked companies", "Juez bloquea bienes y cuentas de otras diez empresas vinculadas al Grupo Vázquez",
      "General inhibition to sell or encumber and preventive immobilisation of accounts for ITTI, Grupo Vázquez, Redisa, Redipro, SATEC, HD Invest, Technoma, La Tropa Fletes, Factopar and Kasas Propiedades; seven firms (Mowi, Grupo Hendy, Grupo M, Tuiu, Franede, Aime, Vinanzas) had been frozen earlier. Date is publication date; resolution number not given.",
      "Inhibición general de vender y gravar e inmovilización preventiva de cuentas para ITTI, Grupo Vázquez, Redisa, Redipro, SATEC, HD Invest, Technoma, La Tropa Fletes, Factopar y Kasas Propiedades; siete firmas ya estaban bloqueadas. Fecha = publicación.",
      TEN + ["auth:ministerio-publico"], Z("measures"))
for bw, cur, amt in [("org:satec", "USD", 20_000_000), ("org:hd-invest", "USD", 35_000_000), ("org:hd-invest", "PYG", 36_900_000_000), ("org:technoma", "USD", 10_000_000),
                     ("org:la-tropa-fletes", "USD", 10_000_000), ("org:factopar", "USD", 6_841_000)]:
    loan(UB, bw, Z("loans listed by prosecutors"), currency=cur, principal=amt, note_en="Loan cited in the prosecutors' freeze request; date not given in the article.",
         note_es="Préstamo citado en el pedido fiscal de bloqueo; fecha no indicada en el artículo.")
flow(VIN, UB, 74418418.12, "USD", "2026", "portfolio_sale_price", "Cash purchase of a credit portfolio without sufficient own funds; price allegedly funded indirectly by the bank's credits to other firms",
     "Compra al contado de cartera sin fondos propios suficientes; precio integrado indirectamente con créditos del banco a otras empresas", Z("Vinanzas", "Parte de estos fondos habría transitado"))

# ---------------------------------------------------------------- Hoy 5 Nov 2026
h = src("src:hoy-2026-11-05-ruta-del-dinero", "press", "Hoy", "Ueno Bank: la ruta del dinero y dónde está la plata", "2026-11-05",
        "https://www.hoy.com.py/nacionales/2026/11/05/ueno-bank-las-cifras-reales-y-la-ruta-final-del-dinero")
H = lambda loc, note="": P("regulator", h, loc, "", "medium", ("BCP complaint figures as relayed by Hoy. " + note).strip())
fact("org:franede", "debt_to_ueno_bank", 314001127279, "PYG", "registered debt", "2026", H("exposure list", "ABC 19 Nov rounds to G. 314.001 millones and calls it the amount lent."))
fact("org:grupo-hendy", "debt_to_ueno_bank", 252521261384, "PYG", "direct debt", "2026", H("exposure list"))
fact("org:office-design", "debt_to_ueno_bank_usd", 60 * M, "USD", "accumulated debt", "2026", H("exposure list"))
fact("org:gsr", "financing_projected_and_granted", 72_800_000, "USD", "projected and granted", "2026", H("exposure list"))
fact("org:grupo-m", "accumulated_financing", 38923077, "USD", "accumulated financing (matches ABC's 'Phase 2' figure)", "2026", H("exposure list"))
fact("org:nuevo-mundo-entertainment", "credits_assigned", 33 * M, "USD", "assigned credits for 'Puerto Madero'", "2026", H("exposure list", "ABC 19 Nov gives USD 33 million as the enlarged project budget."))
fact(UB, "intermediary_loans_one_day", 76061604.13, "USD", "described by Hoy as loans granted in one day to Satec and HD Invest", "2026-06-15",
     H("portfolio hole", "Última Hora describes USD 76,061,604.13 as total funds Vinanzas received from several sources; Satec + HD Invest loans are USD 20 M and USD 35 M."))
fact(UB, "related_exposure_total", 300 * M, "USD", "'more than USD 300 million' exposure", "2026", H("aggregate"))

# ---------------------------------------------------------------- La Nación (AR) via Yahoo, 8 Nov 2026
y = src("src:lanacion-ar-2026-11-08-expediente-reservado", "press", "La Nación (Argentina) via Yahoo Noticias",
        "El expediente reservado del Banco Central: cómo Ueno se prestó plata a sí mismo y desató la crisis en Paraguay", "2026-11-08",
        "https://es-us.noticias.yahoo.com/expediente-reservado-banco-central-ueno-193740485.html")
Y = lambda loc, note="", q="": P("regulator", y, loc, q, "medium", ("BCP 199-page file as relayed by La Nación (AR); date shown is the page's update date. " + note).strip())
L_M = loan(UB, "org:mowi", Y("Mowi", "Article prints both '12 millones' and US$12,5 millones."), date="2025-09-26", currency="USD", principal=12_500_000, collateral="none",
           note_en="First loan, about a week after the change of owners.", note_es="Primer préstamo, cerca de una semana después del cambio de dueños.")
for to in (ITTI, RPRO):
    flow("org:mowi", to, None, "USD", "2025-09-30", "transfer", "Mowi's USD 12.5 M loan went four days later to Itti and Redipro (split not given)",
         "El préstamo de USD 12,5 millones de Mowi fue cuatro días después a Itti y Redipro (sin desglose)", Y("Mowi"), L_M)
fact("org:mowi", "intangibles_share_of_assets_pct", 84, None, "percent of assets that were intangible developments", "2025-12-31", Y("Mowi"))
fact("org:mowi", "debt_to_equity", 12.5, None, "times; long-term debt 154 times 2025 revenue; losses four years running", "2025-12-31", Y("Mowi"))
L_NB = loan(UB, "org:nubicom", Y("Nubicom", "ABC 14 Nov prints US$ 7,5 millones."), date="2026-06-09", currency="USD", principal=7_540_000)
flow("org:nubicom", "org:nubicom-srl", 4_600_000, "USD", "2026-06", "transfer", "International transfer to Nubicom SRL account at Banco Macro", "Transferencia internacional a cuenta de Nubicom SRL en Banco Macro", Y("Nubicom"), L_NB, approx=True)
flow("org:nubicom", "org:nokia", 1_200_000, "USD", "2026-06", "transfer", "Payment to Nokia (Finland)", "Pago a Nokia (Finlandia)", Y("Nubicom"), L_NB, approx=True)
fact("org:nubicom", "project_cost", 670 * M, "USD", "planned 5G project with no revenue", "2026", Y("Nubicom"))
fact("org:nubicom", "contribution_for_future_capitalisation", 2_400_000, "USD", "booked as 'aporte para futura capitalización', attributed to Nubicom SRL (approx.)", "2026-06",
     Y("Nubicom", "ABC 14 Nov: G. 14.812 millones in cash according to Ueno.", "aporte para futura capitalización"))
fact("org:grupo-berilo", "loans_from_ueno_bank_total", 69 * M, "USD", "loans, almost half of project cost", "2026", Y("Berilo", "UH/El Parámetro itemise USD 30.15 M (Dec 2025) and USD 26.4 M (Jun 2026)."))
fact("org:grupo-berilo", "shareholder_commitment_off_balance", 3_800_000, "USD", "shareholder commitment not shown on the balance sheet", "2026", Y("Berilo"))
fact(VIN, "funds_needed_for_portfolio_purchase", 76_100_000, "USD", "needed from other group companies before the 15 Jun 2026 purchase", "2026-06-15", Y("Vinanzas"))
fact(UB, "companies_financed_linked_to_owners", 12, None, "companies linked to its owners financed by the bank", "2025-2026", Y("aggregate"))
role("person:santiago-pena", "org:ueno-holding", "shareholder", Y("Peña", "Reported corporate holding only."), pct=1.58, end="2025-03",
     note_en="6,144 shares of Ueno Holding (1.58% of capital) until redemption in March 2025.", note_es="6.144 acciones de Ueno Holding (1,58% del capital) hasta su rescate en marzo de 2025.")
fact("org:ips", "ueno_bonds_purchase_approved", 32 * M, "USD", "approx. purchases of Ueno bonds approved by IPS", "2024-08", Y("IPS"))

# ---------------------------------------------------------------- Judiciales.net 4 Nov 2026
j = src("src:judiciales-2026-11-04-imputacion-prestamos", "press", "Judiciales.net", "Caso Ueno Bank: imputación describe préstamos millonarios sin garantías", "2026-11-04",
        "https://www.judiciales.net/caso-ueno-bank-imputacion-describe-prestamos-millonarios-sin-garantias/")
J = lambda loc, q="": P("prosecution", j, loc, q, "medium", "Figures from the indictment as reported by Judiciales.net.")
GM = "org:grupo-m"
fact(GM, "revenue", 10576 * M, "PYG", "income of the analysed period", "2025 (period analysed)", J("Grupo M"))
fact(GM, "equity", 5327 * M, "PYG", "net equity", "2025 (period analysed)", J("Grupo M"))
fact(GM, "total_liabilities", 126776 * M, "PYG", "96% of assets", "2025 (period analysed)", J("Grupo M"))
fact(GM, "long_term_debt", 125356 * M, "PYG", "98.9% of liabilities; about 23.5x equity and 11.85x income", "2025 (period analysed)", J("Grupo M"))
fact("org:grupo-hendy", "average_monthly_income", 73 * M, "PYG", "approximate monthly average 2025; equity negative at end-2024", "2025", J("Hendy"))
event("2026-11-02", "supervisory", "BCP Resolution No. 1 opens resolution of Ueno Bank", "Resolución N.º 1 del BCP inicia la resolución de Ueno Bank",
      "Solvency ratio below 50% of the legal minimum (art. 13(b), Ley 2.334/03), as cited in the indictment.", "Índice de solvencia por debajo del 50% del mínimo legal (art. 13 inc. b, Ley 2.334/03), según la imputación.",
      ["auth:bcp", UB], J("regulatory context"))
for frm in (VIN, RPRO, RSA, ITTI):
    flow(frm, "org:grupo-hendy", None, "PYG", "2026", "repayment", "Hendy overdrafts repaid with funds transferred via SIPAP by Vinanzas, Redipro, Redisa and Itti (2025-2026)",
         "Sobregiros de Hendy pagados con fondos transferidos vía SIPAP por Vinanzas, Redipro, Redisa e Itti (2025-2026)", J("Hendy"))
event("2026-11-04", "criminal", "Indictment: 'mortgages' behind some loans were only commitment letters", "Imputación: las 'hipotecas' de algunos préstamos eran solo cartas de compromiso",
      "Some loans appeared mortgage-backed but the documents were notes promising to constitute a mortgage, later excluded from the guarantee calculation.",
      "Algunos préstamos figuraban con hipoteca, pero eran cartas o notas de compromiso de constitución; el banco luego las excluyó del cómputo de garantías.",
      [UB, "auth:ministerio-publico"], J("guarantees"))

# ---------------------------------------------------------------- ABC 13 Nov 2026: cash
k = src("src:abc-2026-11-13-efectivo-bolsones", "press", "ABC Color", "Grupo Vázquez distribuía dinero efectivo en bolsones y sobres", "2026-11-13",
        "https://www.abc.com.py/politica/2026/11/13/grupo-vazquez-distribuia-dinero-efectivo-en-bolsones-y-sobres/")
KP = lambda loc, note="": P("press", k, loc, "", "medium", ("From internal e-mails, messages and spreadsheets supplied to ABC by Ueno Bank staff; no response from Grupo Vázquez reported. " + note).strip())
for d_, amt, ne in [("2026-10-02", 881, "Cash packaged in box, bag and envelope; components printed (753 + 99 + 28) do not add to 881."), ("2026-10-13", 500, "Cash requested in writing for the group's corporate-integration function."),
                    ("2026-10-19", 90, "Cash request."), ("2026-10-19", 140, "Cash request."), ("2026-10-22", 480, "Replacement request."), ("2026-10-22", 1500, "New request flagged 'pedido MV'."),
                    ("2026-01", 1176, "Cash from the bank's cash desk packaged in a bag; three directives.")]:
    flow(UB, GV, amt * M, "PYG", d_, "cash_delivery", "Cash prepared at Ueno Bank for delivery on Grupo Vázquez instructions. " + ne,
         "Efectivo preparado en Ueno Bank para entrega por instrucción del Grupo Vázquez.", KP("cash requests", "Final recipients are not companies; 'to' set to Grupo Vázquez as the requesting function."))
fact(GV, "advance_of_future_commissions_paid_to_sports_executive", 3_500_000, "USD", "'more than USD 3.5 million' from a Grupo Vázquez corporate account to an external sports executive's account, labelled advance of future commissions", "undated",
     KP("commission advance"))
