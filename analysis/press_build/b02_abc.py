from lib import *

UB, GV, ITTI, VIN, RSA, RPRO = "org:ueno-bank", "org:grupo-vazquez", "org:itti", "org:vinanzas", "org:redisa", "org:redipro"

# ---------------------------------------------------------------- ABC 19 Nov 2026 (real estate)
a = src("src:abc-2026-11-19-costosos-inmuebles", "press", "ABC Color", "Costosos inmuebles, parte del esquema de triangulación de Ueno",
        "2026-11-19", "https://www.abc.com.py/politica/2026/11/19/costosos-inmuebles-parte-del-esquema-de-triangulacion-de-ueno/")
A = lambda by, loc, q="", conf="medium", note="": P(by, a, loc, q, conf, note)
DOCS = "From internal Grupo Vázquez spreadsheets/invoices supplied to ABC by group staff; not independently verified by ABC."
fact("org:franede", "loans_from_ueno_bank_total", 314001 * M, "PYG", "total Ueno lent to Franede for two real-estate projects (BCP report as reported)", "2025-2026",
     A("regulator", "Franede section"))
L_F3 = loan(UB, "org:franede", A("regulator", "Franede section", "", "medium",
                                   "Última Hora (7 Nov 2026) attributes a USD 10,593 millones loan of 27 Mar 2026 to Henrici S.A.; outlets conflict on the borrower."),
            date="2026-03-27", currency="USD", principal=10_593_000, note_en="For 'Proyecto Hotel Chaco' (hotel refurbishment, opening planned Dec 2026).",
            note_es="Para el 'Proyecto Hotel Chaco' (refacción, apertura prevista dic. 2026).")
flow("org:franede", VIN, 10_593_000, "USD", "2026-03-27", "transfer", "Same day as disbursement the money passed to Vinanzas",
     "El mismo día del desembolso el dinero pasó a Vinanzas SA", A("regulator", "Franede section"), L_F3)
flow(VIN, ITTI, 10_593_000, "USD", "2026-03-27", "transfer", "From Vinanzas on to Itti SAECA to cover 'various debits'",
     "De Vinanzas a Itti SAECA para cubrir 'varios débitos'", A("regulator", "Franede section", "", "medium", "Amount passed on to Itti is implied to be the same; article does not restate it."), L_F3, approx=True)
loan(UB, "org:franede", A("regulator", "Franede section", "", "medium", "Date not reported."), currency="PYG", principal=95000 * M,
     note_en="For construction/infrastructure of Alula hotel and another hotel on calle Palma, Asunción.",
     note_es="Para construcción e infraestructura del Alula y de otro hotel sobre la calle Palma, Asunción.")
event("2025-06-30", "corporate", "Franede shares pass from Grupo Vázquez to Mauro Vargas", "Las acciones de Franede pasan del Grupo Vázquez a Mauro Vargas",
      "ABC: Franede belonged to Grupo Vázquez until this date. The next sentence says the BCP identifies 'him' as a group employee and relative of the group's principal (referent not fully explicit).",
      "ABC: Franede perteneció al Grupo Vázquez hasta esta fecha. La oración siguiente dice que el BCP 'lo identifica' como funcionario del grupo y familiar (referente no del todo explícito).",
      ["org:franede", GV, "person:mauro-vargas"], A("press", "Franede section", "cuando sus acciones pasaron a Mauro Vargas"))
role(GV, "org:franede", "shareholder", A("press", "Franede section"), end="2025-06-30", note_en="Owner until 30 Jun 2025.", note_es="Propietario hasta el 30/06/2025.")
role("person:mauro-vargas", "org:franede", "shareholder", A("press", "Franede section", "cuando sus acciones pasaron a Mauro Vargas"), start="2025-06-30")
role("person:mauro-vargas", GV, "group_role", A("regulator", "Franede section", "El BCP lo identifica como funcionario del grupo", "low",
                                                 "Referent of 'lo' is inferred to be Mauro Vargas from sentence position."),
     note_en="Described (per BCP, as relayed) as a group employee.", note_es="Descrito (según el BCP) como funcionario del grupo.")
fact(GV, "payment_hotel_chaco", 1_000_000, "USD", "payment labelled 'Hotel Chaco' (G. 7,550 million) to unnamed seller; two lots deeded to Grupo Vázquez in Dec 2025", "2025-09-09",
     A("press", "Hotel Chaco", "", "medium", DOCS))
fact("org:nuevo-mundo-entertainment", "risk_balance_at_ueno_bank", 198962 * M, "PYG", "balance for 'Puerto Madero de Asunción' project", "2026-07", A("regulator", "Puerto Madero"))
fact("org:nuevo-mundo-entertainment", "project_budget", 5160508, "USD", "initial cost of Puerto Madero de Asunción project", "2025", A("regulator", "Puerto Madero"))
fact("org:nuevo-mundo-entertainment", "project_budget", 33 * M, "USD", "budget after February 2026 enlargement (no supporting quantities/quotes per BCP)", "2026-02", A("regulator", "Puerto Madero"))
fact("org:nuevo-mundo-entertainment", "disbursements_received", 7_800_000, "USD", "disbursements already reached in 2025", "2025", A("press", "Puerto Madero"))
for to in (ITTI, GV, VIN):
    flow("org:nuevo-mundo-entertainment", to, None, None, "2026", "transfer", "Puerto Madero loan disbursements passed at once or very shortly to cover debits, overdrafts and cheques",
         "Desembolsos de Puerto Madero pasaron de inmediato o a muy corto plazo para cubrir débitos, sobregiros y cheques", A("regulator", "Puerto Madero"))
fact(GV, "real_estate_payments_pyg", 61140 * M, "PYG", "71 payments Apr 2024-Aug 2026 per internal documents", "2024-04/2026-08", A("press", "payments summary", "", "medium", DOCS))
fact(GV, "real_estate_payments_usd", 6233023, "USD", "15 dollar payments Apr 2024-Aug 2026 per internal documents", "2024-04/2026-08", A("press", "payments summary", "", "medium", DOCS))
fact(GV, "land_purchase_nemby_for_nubicom_antenna", 450000, "USD", "9,956 m2 plot in Ñemby bought from private sellers; internal label refers to a NUBICOM antenna; signed 27 Feb 2026",
     "2026-02-27", A("press", "Ñemby plot", "", "medium", DOCS))
flow(GV, "org:criscatt", 500000, "USD", "2025-01-31", "transfer", "Initial payment for Jade Park apartment (contract price USD 1,460,000 plus 6% a year)",
     "Entrega inicial por departamento en Jade Park (precio USD 1.460.000 más 6% anual)", A("press", "Jade Park", "", "medium", DOCS))
flow(GV, "org:criscatt", 234000, "USD", "2026-02-28", "transfer", "First instalment with interest, Jade Park apartment", "Primera cuota con intereses, departamento Jade Park",
     A("press", "Jade Park", "", "medium", DOCS))
flow(GV, "org:bau-sa", 1687 * M, "PYG", "2025", "transfer", "Two payments invoiced by builder BAU S.A. for country house at Aqua Village", "Dos pagos facturados por BAU SA por casa quinta en Aqua Village",
     A("press", "Aqua Village", "", "medium", DOCS))
fact(GV, "payment_aqua_village_land", 468551, "USD", "payment labelled 'terreno Aqua Village' to unnamed seller", "2024-12-10", A("press", "Aqua Village", "", "medium", DOCS))
role("org:terravaz", "org:shopping-costanera", "controlling_group", A("press", "Terravaz"), note_en="Terravaz controls Shopping Costanera and Executive Center, Encarnación.",
     note_es="Terravaz controla el Shopping Costanera y el Executive Center, Encarnación.")
fact(GV, "inhibited_assets_identified_real_estate", 2331, None, "properties in the names of inhibited persons and companies identified by RUN (160 vehicles also)", "2026-11", A("regulator", "RUN statement", "", "medium", "Asserted by the registry directorate (RUN), not the bank regulator."))

# ---------------------------------------------------------------- ABC 10 Oct 2026 (Rivarola report)
b = src("src:abc-2026-10-10-tres-empresas-tope-legal", "press", "ABC Color",
        "Solo tres empresas vinculadas a Ueno tenían US$ 41,5 millones por encima del tope legal", "2026-10-10",
        "https://www.abc.com.py/politica/2026/10/10/solo-tres-empresas-vinculadas-a-ueno-tenian-us-415-millones-por-encima-del-tope-legal/")
B = lambda loc, q="", conf="medium", note="": P("regulator", b, loc, q, conf, note)
fact(UB, "related_exposure_mowi_hendy_grupo_m", 743784 * M, "PYG", "combined exposure to Mowi, Grupo Hendy and Grupo M (about USD 123 million)", "2026-04-30",
     B("report figures", "al 30 de abril de este año", "medium", "ABC 15 Oct 2026 cites about USD 146 million / 35% for the same three firms over seven months; different basis."))
fact(UB, "related_exposure_pct_of_effective_equity", 30, None, "percent of effective equity", "2026-04-30", B("report figures", "La cifra equivale al 30% del patrimonio efectivo"))
fact(UB, "related_party_cap", 493447 * M, "PYG", "regulatory cap = 20% of effective equity", "2026-04-30", B("report figures", "el tope regulatorio del 20%"))
fact(UB, "effective_equity", 2_460_000 * M, "PYG", "estimated effective equity ('G. 2,46 billones')", "2026-04", B("report figures", "patrimonio efectivo a ese mes del banco"))
fact(UB, "related_exposure_excess_over_cap", 250337 * M, "PYG", "excess over cap (about USD 41.5 million), exceeded for more than 10 consecutive days", "2026-04-30",
     B("report figures", "el exceso era de G. 250.337 millones"))
event("2026-07-10", "supervisory", "BCP supervision manager's 25-page report to the SIB", "Informe de 25 páginas del gerente de Supervisión del BCP a la SIB",
      "Fernando Rivarola's report describes 'accounting engineering' to evade related-party limits and poor credit conditions; recommends rejecting the portfolio sale to Vinanzas, applying art. 6 of Ley 2334/03 and requiring an immediate regularisation plan. Also flags loans to Tuiu, Franede and Aime.",
      "El informe de Fernando Rivarola describe 'ingeniería contable' para evadir límites con vinculadas y paupérrimas condiciones crediticias; recomienda rechazar la venta de cartera a Vinanzas, aplicar el art. 6 de la Ley 2334/03 y exigir un Plan de Regularización. Señala préstamos a Tuiu, Franede y Aime.",
      ["auth:bcp", "auth:superintendencia-de-bancos", UB, VIN, "org:mowi", "org:grupo-hendy", "org:grupo-m", "org:tuiu", "org:franede", "org:aime"],
      B("report description", "exigir de inmediato un Plan de Regularización", "medium", "UH 10 Nov identifies a report of the same date as Informe SEFS 4 Nº 007/2026; ABC gives no number."))

# ---------------------------------------------------------------- ABC 27 Oct 2026 ("salvadoras")
d = src("src:abc-2026-10-27-empresas-salvadoras", "press", "ABC Color", "Empresas \"salvadoras\" le deben 153 millones de dólares a Ueno Bank",
        "2026-10-27", "https://www.abc.com.py/politica/2026/10/27/empresas-salvadoras-le-deben-153-millones-de-dolares-a-ueno-bank/")
D = lambda loc, q="", conf="medium", note="", by="regulator": P(by, d, loc, q, conf, note)
fact("org:sagas", "debt_to_ueno_bank", 268363 * M, "PYG", "debt to Ueno (about USD 45 million)", "2026 (undated)", D("Sagas", "alcanzaban G. 268.363 millones", "medium", "UH debtor list prints G. 267.787 millones."))
fact("org:sagas", "debt_to_rest_of_financial_system", 84319401, "PYG", "debt with two other entities (USD 14,283)", "2026 (undated)", D("Sagas"))
fact("org:kasas-propiedades", "debt_to_ueno_bank", 426480 * M, "PYG", "commitments with Ueno (about USD 72 million), '800 times' its debt elsewhere", "2026 (undated)",
     D("Kasas", "Kasas arrastraba compromisos por G. 426.480 millones", "medium", "UH debtor list prints G. 425.957 millones."))
fact(VIN, "debt_to_ueno_bank", 10 * M, "PYG", "approximate debt to Ueno ('unos G. 10 millones')", "2026 (undated)", D("Vinanzas", "Vinanzas SA debía unos G. 10 millones"))
fact("org:la-tropa-sae", "debt_to_ueno_bank", 210971 * M, "PYG", "accumulated debt (about USD 35 million)", "2026-08", D("La Tropa", "La deuda acumulada de La Tropa SAE"))
fact("org:aime", "debt_to_ueno_bank", 77516 * M, "PYG", "liability to Ueno (about USD 12 million)", "2026-06", D("Aime", "pasivo de G. 77.516 millones"))
fact(UB, "debt_of_rescuer_firms", 905825 * M, "PYG", "combined debt of four of the five 'rescuer' firms (Vinanzas, La Tropa, Aime, Kasas, Sagas) as printed by ABC; about USD 153 million; 35% of effective equity",
     "2026-08", D("headline figure", "G. 905.825 millones (unos US$ 153 millones)", "medium", "Total as printed by ABC; which four firms are included is not explicit.", by="press"))
fact(UB, "public_sector_and_ips_funds_captured", 4_900_000 * M, "PYG", "funds captured from public sector and IPS over three years ('G. 4,9 billones', USD 855 million)", "2023-2026",
     D("context", "captó G. 4,9 billones (US$ 855 millones)", by="press"))
fact(UB, "effective_equity", 2_500_000 * M, "PYG", "effective equity ('G. 2,5 billones')", "2026", D("context", "35% del patrimonio efectivo", by="press"))
L_GM2 = loan(UB, "org:grupo-m", D("Grupo M", "préstamo de US$ 4 millones que Ueno Bank concedió", "medium", "UH 4 Nov 2026 gives USD 4,321,500 for the 31 Oct 2025 loan."),
             date="2025-10-31", currency="USD", principal=4 * M)
L_MW = loan(UB, "org:mowi", D("Mowi", "préstamo de G. 33.500 millones que Mowi SA obtuvo"), date="2025-12-29", currency="PYG", principal=33500 * M,
            note_en="Partly paid in April 2026 with funds contributed by La Tropa SAE.", note_es="Pagado parcialmente en abril de 2026 con fondos aportados por La Tropa SAE.")
L_HOD = loan(UB, "org:grupo-hendy", D("Hendy", "amortización de sobregiros por G. 253.699 millones"), kind="overdraft", date="2026-03-31", currency="PYG",
             principal=253699 * M, note_en="Overdrafts amortised 31 Mar 2026 with funds from ITTI and Redipro (ITTI fed by Vinanzas and Redisa; Redipro by ITTI).",
             note_es="Sobregiros amortizados el 31/03/2026 con fondos de Itti y Redipro (Itti recibió de Vinanzas y Redisa; Redipro de Itti).")
for frm in (ITTI, RPRO):
    flow(frm, "org:grupo-hendy", None, "PYG", "2026-03-31", "repayment", "Funds used to amortise Hendy overdrafts of G. 253,699 million (per-sender split not given)",
         "Fondos para amortizar sobregiros de Hendy por G. 253.699 millones (sin desglose)", D("Hendy", "recibió fondos de Itti y Redipro"), L_HOD)
chain = [("org:sagas", "org:kasas-propiedades"), ("org:kasas-propiedades", VIN), (VIN, ITTI), (ITTI, "org:grupo-m")]
for f_, t_ in chain:
    flow(f_, t_, None, None, "2026-04-29", "transfer", "Link in chain Sagas -> Kasas -> Vinanzas -> Itti -> Grupo M used to pay Grupo M's first instalment to Ueno; Sagas obtained a credit the same day",
         "Eslabón de la cadena Sagas -> Kasas -> Vinanzas -> Itti -> Grupo M para pagar la primera cuota de Grupo M a Ueno; Sagas obtuvo un crédito ese mismo día",
         D("Grupo M instalment", "para que cancelara su cuota con Ueno"), L_GM2)
flow("org:la-tropa-sae", "org:mowi", None, "PYG", "2026-04", "repayment", "La Tropa SAE contributed funds for a partial payment of Mowi's G. 33,500 million loan",
     "La Tropa SAE aportó fondos para el pago parcial del préstamo de G. 33.500 millones de Mowi", D("Mowi", "aportar en abril pasado los fondos"), L_MW)
flow(RPRO, "org:grupo-hendy", None, "PYG", "2026-04-30", "repayment", "Redipro (with Vinanzas funds) covered another Hendy overdraft",
     "Redipro (con fondos de Vinanzas) cubrió otro sobregiro de Hendy", D("Hendy", "Grupo Hendy canceló otro sobregiro"))
fact("org:aime", "overdraft_settled_with_vinanzas", 105090 * M, "PYG", "overdraft settled with Aime and Vinanzas as original contributors (debtor of the overdraft not identified in extraction)", "2026 (undated)",
     D("Aime", "sobregiro de G. 105.090 millones", "low"))
event("2026-06-08", "supervisory", "BCP supervision report on sole-signature lending to related firms", "Informe de supervisión del BCP sobre concesiones a sola firma",
      "Report of the BCP supervision area cited by ABC; confirms transfer of Mowi, Grupo Hendy and Grupo M to former managers and employees of Grupo Vázquez.",
      "Informe del área de supervisión del BCP citado por ABC; confirma el traspaso de Mowi, Grupo Hendy y Grupo M a exgerentes y empleados del Grupo Vázquez.",
      ["auth:bcp", UB, "org:mowi", "org:grupo-hendy", "org:grupo-m"], D("sources", "entre ellos una jefa de Recursos Humanos", "medium", "Likely the same document UH calls Informe SEFS 4 Nº 006/2026 (8 Jun 2026)."))
event("2026-06-19", "supervisory", "BCP board minutes record observations on Ueno", "Acta del Directorio del BCP registra observaciones sobre Ueno",
      "Per ABC: omission to deduct a G. 876,300 million contribution; 'non-enabled expenses' in the G. 2.5 trillion Visión merger trust; mis-classification of a G. 2.6 trillion past-due portfolio.",
      "Según ABC: omisión de descuento de un aporte de G. 876.300 millones; 'gastos no habilitados' en el fideicomiso de fusión de G. 2,5 billones; clasificación errónea de cartera morosa de G. 2,6 billones.",
      ["auth:bcp", UB], D("BCP board minutes", "gastos no habilitados"))

# ---------------------------------------------------------------- ABC 14 Nov 2026 (Nubicom)
n = src("src:abc-2026-11-14-nubicom", "press", "ABC Color", "Nubicom, en la mira del BCP y la CGR por irregularidades y pagos de Ueno", "2026-11-14",
        "https://www.abc.com.py/politica/2026/11/14/nubicom-en-la-mira-del-bcp-y-la-cgr-por-irregularidades-y-pagos-de-ueno/")
N = lambda loc, q="", conf="medium", note="", by="regulator": P(by, n, loc, q, conf, note)
NB = "org:nubicom"
event("2025-09-24", "corporate", "Biopulp S.A. renamed Nubicom Paraguay S.A.; 99% assigned to Nubicom SRL", "Biopulp SA pasa a llamarse Nubicom Paraguay SA; 99% a Nubicom SRL",
      "Deed of 24 Sep 2025 changed the name, raised capital to G. 162,800 million and assigned 99% of shares to Nubicom SRL (Argentina); only G. 200,000 paid in.",
      "Escritura del 24/09/2025: cambio de nombre, capital elevado a G. 162.800 millones y 99% de acciones a Nubicom SRL (Argentina); solo G. 200.000 integrados.",
      [NB, "org:nubicom-srl"], N("corporate history", by="press"))
fact(NB, "authorised_capital", 162800 * M, "PYG", "capital after deed of 24 Sep 2025", "2025-09-24", N("corporate history", by="press"))
fact(NB, "paid_in_capital", 200000, "PYG", "capital actually integrated; still so in June 2026 balance", "2026-06", N("corporate history", by="press"))
role("org:nubicom-srl", NB, "shareholder", N("corporate history", "", "medium", "Nubicom SRL says it sold all shares months earlier; BCP records still show it as majority holder."), pct=99, start="2025-09-24")
for h, r, st, ne in [("person:guillermo-vazquez", "president", "2025-10-03", "Acta N° 3 of 3 Oct 2025."), ("person:cesar-astigarraga", "vice_president", "2025-10-03", "Acta N° 3 of 3 Oct 2025."),
                     ("person:bernardo-algorta", "director", "2025-10-03", "Acta N° 3 of 3 Oct 2025."),
                     ("person:marco-galanti", "president", "2026-06", "Acta de asamblea N° 4 (June 2026)."),
                     ("person:gilberto-ramos", "director", "2026-06", "Acta N° 4 (June 2026), Acta de Directorio N° 12 (27 Jul 2026); he says he was added without consent."),
                     ("person:paul-gaston", "vice_president", "2026-07-27", "Acta de Directorio N° 12 of 27 Jul 2026.")]:
    role(h, NB, r, N("officers by acta", by="press"), start=st, note_en=ne, note_es=ne)
role("person:gilberto-ramos", ITTI, "officer", N("statements", by="press"), note_en="Described as former operations manager of Itti.", note_es="Descrito como exgerente de operaciones de Itti.")
loan(UB, NB, N("loans", "", "medium", "UH 7 Nov: 'líneas aprobadas de hasta USD 85 millones' (Caso VIII)."), date="2026-05", currency="USD", principal=85 * M, collateral="none",
     note_en="Credit line (limit, not a disbursement).", note_es="Línea de crédito (límite, no desembolso).")
L_N1 = loan(UB, NB, N("loans"), date="2026-06-09", currency="USD", principal=7_500_000)
L_N2 = loan(UB, NB, N("loans"), date="2026-07-01", currency="PYG", principal=417075 * M, term_days=180, collateral="none", note_en="Sole signature.", note_es="A sola firma.")
L_GAL = loan(UB, "org:galadriel", N("loans", "no se cuenta información referente al destino", "medium", "UH 17 Nov gives USD 15.07 million, op. 612661005074."), date="2026-07-31", currency="USD", principal=15 * M)
L_INF = loan(UB, "org:infocenter", N("loans", "no se cuenta información referente al destino", "medium", "Lender not restated in the sentence; context is Ueno loans per BCP. Date not given."),
             currency="USD", principal=18 * M)
flow(NB, "org:nubicom-srl", 4_600_000, "USD", "2026-06", "transfer", "Sent abroad (Jun-Jul 2026) to Nubicom SRL's account at Banco Macro, Argentina, out of the USD 7.5m loan",
     "Enviado al exterior (jun-jul 2026) a cuenta de Nubicom SRL en Banco Macro, Argentina, del préstamo de USD 7,5 millones", N("transfers"), L_N1)
flow(NB, ITTI, 415000 * M, "PYG", "2026-07-01", "contract", "Paid to Itti under a professional-services contract dated 30 Jun 2026",
     "Pagado a Itti bajo contrato de servicios profesionales del 30/06/2026", N("transfers", "servicios profesionales de asesoría, implementación y desarrollo"), L_N2, approx=True)
flow(ITTI, RSA, 329500 * M, "PYG", "2026-07", "transfer", "Itti passed funds to Red Digital to cover '72-hour cheques'", "Itti pasó fondos a Red Digital para cubrir 'cheques 72hs'", N("transfers"), L_N2)
flow(ITTI, NB, 285600 * M, "PYG", "2026-07-31", "repayment", "Partial payment of Nubicom's debt at Ueno, made by Itti out of a USD 33 million FX operation funded by the Infocenter and Galadriel loans",
     "Pago parcial de la deuda de Nubicom con Ueno, hecho por Itti con una operación de cambio de USD 33 millones fondeada con préstamos a Infocenter y Galadriel", N("transfers"), L_N2)
flow("org:infocenter", ITTI, 18 * M, "USD", "2026-07-31", "transfer", "Infocenter loan funded Itti's USD 33 million FX operation (per BCP)", "Préstamo de Infocenter fondeó la operación de cambio de Itti por USD 33 millones (según BCP)",
     N("transfers", "", "low", "Route inferred from 'funding of the Itti operation'; BCP says destination information unavailable."), L_INF)
flow("org:galadriel", ITTI, 15 * M, "USD", "2026-07-31", "transfer", "Galadriel loan funded Itti's USD 33 million FX operation (per BCP)", "Préstamo de Galadriel fondeó la operación de cambio de Itti por USD 33 millones (según BCP)",
     N("transfers", "", "low", "Route inferred from 'funding of the Itti operation'; UH 17 Nov describes flow Ueno -> Galadriel -> ITTI -> Nubicom -> Ueno."), L_GAL)
flow("org:nubicom-srl", NB, 14812 * M, "PYG", None, "cash_delivery", "Capitalisation contribution paid in cash by Nubicom SRL to the subsidiary, according to Ueno",
     "Aporte de capitalización pagado en efectivo por Nubicom SRL a la filial, según Ueno", N("transfers", "", "medium", "Asserted by Ueno Bank; conflicts with paid-in capital of G. 200,000.", by="company"))
fact(NB, "debt_to_ueno_bank", 37 * M, "USD", "debt to Ueno", "2026-08", N("balances"))
event("2025-10-13", "corporate", "Conatel awards 5G licence to Nubicom Paraguay", "Conatel adjudica licencia 5G a Nubicom Paraguay", "Ueno Bank issued the bid guarantee.",
      "Ueno Bank emitió la garantía de oferta.", [NB, UB], N("Conatel", by="press"))
event("2026-11-09", "supervisory", "Comptroller's final audit report on Nubicom licence", "Informe final de la Contraloría sobre la licencia de Nubicom",
      "CGR ratified five observations and recommended Conatel determine whether the licence should be extinguished; Conatel opened a sumario over unauthorised share transfers.",
      "La CGR ratificó cinco observaciones y recomendó a Conatel determinar si corresponde extinguir la licencia; Conatel abrió sumario por transferencias de acciones no autorizadas.",
      [NB], N("CGR", "", "medium", "Asserted by the Comptroller (CGR)."))
event("2026-11-05", "statement", "Nubicom SRL (Argentina) says it sold its shares months ago", "Nubicom SRL (Argentina) afirma que vendió sus acciones hace meses",
      "Communiqué: never administered or disposed of the Paraguayan company's funds.", "Comunicado: nunca ejerció la administración ni disposición de los fondos de la sociedad paraguaya.",
      ["org:nubicom-srl", NB], N("statements", "nunca ejerció la administración, gestión, custodia ni disposición de los fondos", by="company"))

# ---------------------------------------------------------------- ABC 8 Sep 2026
e = src("src:abc-2026-09-08-misteriosas-empresas", "press", "ABC Color",
        "Ueno Bank: misteriosas empresas citadas en proyecto de pedido de informe están ligadas al grupo Vázquez", "2026-09-08",
        "https://www.abc.com.py/politica/2026/09/08/ueno-bank-misteriosas-empresas-citadas-en-proyecto-de-pedido-de-informe-estan-ligadas-al-grupo-vazquez/")
EP = lambda loc, q="", conf="medium", note="": P("press", e, loc, q, conf, note)
event("2024-08-30", "corporate", "Conacom Res. 69/2024: ITTI notifies acquisition of 50% of Grupo M and 55% of Grupo Hendy", "Resolución Conacom 69/2024: ITTI notifica adquisición del 50% de Grupo M y 55% de Grupo Hendy",
      "Competition authority resolution authorising the operation.", "Resolución de la autoridad de competencia que autoriza la operación.", [ITTI, "org:grupo-m", "org:grupo-hendy"],
      EP("Conacom", "el 50% del paquete accionario del Grupo M S.A."))
role(ITTI, "org:grupo-m", "shareholder", EP("Conacom", "el 50% del paquete accionario del Grupo M S.A."), pct=50, start="2024-08-30", note_en="Acquisition notified to Conacom.", note_es="Adquisición notificada a Conacom.")
role(ITTI, "org:grupo-hendy", "shareholder", EP("Conacom", "el 55% del capital accionario del Grupo Hendy S.A."), pct=55, start="2024-08-30", note_en="Acquisition notified to Conacom.", note_es="Adquisición notificada a Conacom.")
event("2024-07-29", "corporate", "TUIU trademark registered with ITTI as applicant", "Marca Tuiu registrada con ITTI como solicitante", "Per official trademark records.", "Según registros oficiales de marcas.",
      ["org:tuiu", ITTI], EP("Tuiu", "fue registrada el 29 de Julio de 2024"))
role("person:bernardo-algorta", "org:mowi", "vice_president", EP("Mowi", "", "medium", "'Director vicepresidente' per the group's related-party declaration at 31 Dec 2025."), start="2025-12-31")
role("person:miguel-angel-almada", "org:aime", "alternate_director", EP("Aime", "director suplente de la aseguradora", "medium", "Per the group's related-party report."))
role("person:miguel-angel-almada", GV, "statutory_auditor", EP("Aime"), note_en="Síndico of Grupo Vázquez.", note_es="Síndico del Grupo Vázquez.")
event("2026-09-08", "political", "Senate draft information request names six borrower firms", "Proyecto de pedido de informe del Senado cita seis empresas",
      "31 questions to the BCP on prudential limits with related parties; lists Mowi, Grupo M, Grupo Hendy, Tuiu, Franede and Aime under 'excesses'. Date is publication date.",
      "31 preguntas al BCP sobre límites prudenciales con vinculadas; cita a Mowi, Grupo M, Grupo Hendy, Tuiu, Franede y Aime. Fecha = publicación.",
      ["auth:senado", "auth:bcp", UB, "org:mowi", "org:grupo-m", "org:grupo-hendy", "org:tuiu", "org:franede", "org:aime"], EP("draft request"))

# ---------------------------------------------------------------- El Parámetro 4 Nov 2026
p = src("src:elparametro-2026-11-04-ruta-del-dinero", "press", "El Parámetro",
        "La ruta del dinero de Ueno: préstamos a empresas, transferencias entre cuentas y millones que terminaban en su propio grupo", "2026-11-04",
        "https://elparametro.com/la-ruta-del-dinero-de-ueno-prestamos-a-empresas-transferencias-entre-cuentas-y-millones-que-terminaban-en-su")
PP = lambda loc, q="", conf="medium", note="": P("regulator", p, loc, q, conf, note)
L_B0 = loan(UB, "org:grupo-berilo", PP("Berilo", "terreno, proyecto ejecutivo, licencias e inicio de una obra civil"), date="2025-12-23", currency="USD", principal=30_150_000,
            note_en="Stated purpose: land, executive project, licences and start of civil works.", note_es="Destino declarado: terreno, proyecto ejecutivo, licencias e inicio de obra civil.")
flow("org:grupo-berilo", VIN, 30 * M, "USD", "2025-12-23", "transfer", "Works funds sent to Vinanzas the same day", "Fondos de la obra enviados a Vinanzas el mismo día", PP("Berilo"), L_B0)
flow(VIN, RSA, 30 * M, "USD", "2025-12-30", "transfer", "Three transfers of USD 10 million each to Redisa's savings account, used to cover a Redisa current-account overdraft",
     "Tres transferencias de USD 10 millones a la caja de ahorro de Redisa, para cubrir un sobregiro en cuenta corriente", PP("Berilo"), L_B0)
L_NM2 = loan(UB, "org:nuevo-mundo-entertainment", PP("Nuevo Mundo", "Ueno desembolsó G. 100.500 millones a Nuevo Mundo."), date="2026-05-26", currency="PYG", principal=100500 * M,
             note_en="Puerto Madero de Asunción project.", note_es="Proyecto Puerto Madero de Asunción.")
for f_, t_ in (("org:nuevo-mundo-entertainment", VIN), (VIN, ITTI), (ITTI, "org:office-design")):
    flow(f_, t_, None, "PYG", "2026-05-26", "transfer", "Link in route Nuevo Mundo -> Vinanzas -> ITTI -> Office Design, where funds covered an overdraft",
         "Eslabón de la ruta Nuevo Mundo -> Vinanzas -> ITTI -> Office Design, donde cubrieron un sobregiro", PP("Nuevo Mundo", "cubrieron un sobregiro"), L_NM2)
L_OD2 = loan(UB, "org:office-design", PP("Office Design", "El destino asentado para el préstamo era inversión."), date="2026-05-26", currency="USD", principal=15766440,
             note_en="Recorded purpose: investment.", note_es="Destino asentado: inversión.")
flow("org:office-design", ITTI, 96767 * M, "PYG", "2026-05-26", "transfer", "Office Design exchanged USD 15.6 million for guaraníes and sent them to ITTI",
     "Office Design cambió USD 15,6 millones por G. 96.767 millones y los envió a ITTI", PP("Office Design"), L_OD2)
flow(ITTI, "org:match-sa", 74071 * M, "PYG", "2026-05", "transfer", "After receiving Office Design funds ITTI transferred mainly to Match S.A.",
     "Tras recibir los fondos de Office Design, ITTI transfirió principalmente a Match S.A.", PP("Office Design"), L_OD2)
fact(VIN, "bank_accounts_at_ueno", 8, None, "number of accounts at Ueno", "2026-06", PP("Vinanzas"))
fact(VIN, "bank_account_balance", 93828, "USD", "available across its Ueno accounts the day before the purchase", "2026-06-14", PP("Vinanzas"))
fact(VIN, "credits_purchased_15_jun_2026", 9, None, "number of credits (Mowi, Grupo Hendy, Grupo M) bought for USD 74,418,418.12", "2026-06-15", PP("Vinanzas"))
fact(VIN, "funds_received_15_jun_2026", 76_060_000, "USD", "received from identified sources ('US$ 76,06 millones')", "2026-06-15", PP("Vinanzas"))
fact(UB, "outstanding_capital_six_related_companies_usd", 166_980_000, "USD", "outstanding capital in six related companies (USD part); includes credits sold to Vinanzas", "2026",
     PP("aggregates", "US$ 166,98 millones y G. 343.157 millones de capital pendiente"))
fact(UB, "outstanding_capital_six_related_companies_pyg", 343157 * M, "PYG", "outstanding capital in six related companies (PYG part)", "2026",
     PP("aggregates", "US$ 166,98 millones y G. 343.157 millones de capital pendiente"))
fact(UB, "provisions_deficit", 1_620_000 * M, "PYG", "provisions deficit ('G. 1,62 billones') per supervision report", "2026-11", PP("aggregates"))
fact("org:ips", "placements_at_ueno_bank_total", 2_030_000 * M, "PYG", "IPS funds at Ueno ('G. 2,03 billones', about USD 348.5 million)", "2026-09-30",
     PP("aggregates", "", "medium", "UH 7 Nov gives about USD 355 million for the same month."))
