from lib import *

UB, GV, ITTI, VIN, RSA, RPRO = "org:ueno-bank", "org:grupo-vazquez", "org:itti", "org:vinanzas", "org:redisa", "org:redipro"

# ---------------------------------------------------------------- UH 7 Nov 2026 (debtor list)
s = src("src:ultimahora-2026-11-07-grandes-deudores", "press", "Última Hora",
        "Grandes deudores de ueno aparecen en la investigación del BCP sobre desvío de fondos", "2026-11-07",
        "https://www.ultimahora.com/grandes-deudores-de-ueno-aparecen-en-la-investigacion-del-bcp-sobre-desvio-de-fondos")
NOTE_LIST = ("Unofficial ('oficioso') debtor list as printed by Última Hora; article gives no cut-off date and does "
             "not say whether figure is balance or cumulative.")
for org, val, q in [
    ("org:nubicom", 228431, "con un saldo de G. 228.431 millones"),
    ("org:gsr", 453828, "registra G. 453.828 millones en la nómina"),
    ("org:office-design", 357057, "Office Design SRL, con G. 357.057 millones"),
    ("org:grupo-berilo", 419231, "Grupo Berilo SA, con G. 419.231 millones"),
    ("org:galadriel", 88623, "con G. 88.623 millones"),
    ("org:nuevo-mundo-entertainment", 198205, "registra G. 198.205 millones"),
    ("org:technoma", 476783, "registra G. 476.783 millones"),
    ("org:kasas-propiedades", 425957, "con G. 425.957 millones"),
    ("org:model", 299993, "con G. 299.993 millones"),
    ("org:grupo-vazquez", 295381, "con G. 295.381 millones"),
    ("org:sagas", 267787, "registra G. 267.787 millones"),
    ("org:hd-invest", 267247, "con G. 267.247 millones"),
    ("org:la-tropa-fletes", 246498, "con G. 246.498 millones"),
    ("org:factopar", 199159, "registra G. 199.159 millones"),
    ("org:satec", 147777, "con G. 147.777 millones"),
    ("org:henrici", 345372, "con G. 345.372 millones"),
    ("org:itti", 86845, "figura en la nómina con G. 86.845 millones"),
    ("org:redipro", 115707, "con G. 115.707 millones"),
    ("org:valores-casa-de-bolsa", 405456, "con G. 405.456 millones"),
    ("org:discover-paraguay", 10147, "con G. 10.147 millones"),
    ("org:muar-srl", 8819, "registra G. 8.819 millones"),
    ("org:ips", 88702, "una obligación registrada de G. 88.702 millones"),
]:
    fact(org, "debt_to_ueno_bank_debtor_list", val * M, "PYG", "obligation at Ueno Bank per unofficial debtor list",
         "undated (list published 2026-11-07)", P("press", s, "debtor list", q, "medium", NOTE_LIST))

fact("org:nubicom", "credit_lines_approved", 85 * M, "USD", "approved lines 'up to' (Caso VIII of BCP file)", "2026",
     P("regulator", s, "Caso VIII", "líneas aprobadas de hasta USD 85 millones"))
fact("org:gsr", "financing_received_usd", 72_800_000, "USD", "financings, Caso IX; plus G. 30.150 millones (separate row)",
     "2025-2026", P("regulator", s, "Caso IX", "financiamientos de USD 72,8 millones"))
fact("org:gsr", "financing_received_pyg", 30150 * M, "PYG", "financings, Caso IX (guaraní part)", "2025-2026",
     P("regulator", s, "Caso IX", "financiamientos de USD 72,8 millones"))
fact("org:office-design", "capital_owed_to_ueno_bank", 359722 * M, "PYG", "capital owed, Caso X; article equates to USD 60 millones",
     "undated", P("regulator", s, "Caso X", "capital adeudado por G. 359.722 millones", "medium",
                  "Same article's debtor list prints G. 357.057 millones for Office Design; two different figures in one source."))
fact("org:office-design", "overdrafts_at_ueno_bank", 67194 * M, "PYG", "overdrafts, Caso X", "undated",
     P("regulator", s, "Caso X", "capital adeudado por G. 359.722 millones"))
fact("org:grupo-berilo", "loans_and_overdrafts_usd", 26_400_000, "USD", "loans and overdrafts, Caso XI (USD part)", "2026",
     P("regulator", s, "Caso XI", "préstamos y sobregiros de USD 26,4 millones"))
fact("org:grupo-berilo", "loans_and_overdrafts_pyg", 82410 * M, "PYG", "loans and overdrafts, Caso XI (PYG part)", "2026",
     P("regulator", s, "Caso XI", "préstamos y sobregiros de USD 26,4 millones"))
fact("org:nuevo-mundo-entertainment", "risk_balance_at_ueno_bank", 198962 * M, "PYG", "saldo de riesgo, Caso VII", "undated",
     P("regulator", s, "Caso VII, pp. 85-87", "destinados a la ampliación de galpones y estacionamientos"))
fact("org:valores-casa-de-bolsa", "bond_trade_transfers", 2400137.25, "USD", "transfers traced in bond trades ('giros')", "2026",
     P("regulator", s, "Valores Casa de Bolsa paragraph", "", "low", "No counterparty or date given in the article."))
# IPS placements (Sept 2026 bulletin)
fact("org:ips", "placements_at_ueno_bank_total", 355 * M, "USD", "approximate total of IPS placements at Ueno Bank", "2026-09",
     P("press", s, "IPS paragraph", "alcanzaban aproximadamente USD 355 millones", "medium",
       "Other outlets give USD 345-380 million (CDs/bonds) and USD 516-517 million 'committed'; see collapse notes."))
fact("org:ips", "ueno_bank_bonds_held", 250000 * M, "PYG", "bonds held by IPS (issuer split not given)", "2026-09",
     P("press", s, "IPS paragraph", "El boletín de inversiones de setiembre de 2026"))
fact("org:ips", "ueno_bank_cda_foreign_currency", 27_400_000, "USD", "CDs in foreign currency at Ueno Bank", "2026-09",
     P("press", s, "IPS paragraph", "El boletín de inversiones de setiembre de 2026"))

L_TECH = loan(UB, "org:technoma", P("regulator", s, "Technoma paragraph", "préstamo de USD 10 millones el 11 de junio de 2026"),
              date="2026-06-11", currency="USD", principal=10 * M,
              note_en="Used to buy bonds of ITTI and 'ueno bank' per this article.",
              note_es="Usado para comprar bonos de Itti y 'ueno bank' según este artículo.")
L_SAGAS = loan(UB, "org:sagas", P("regulator", s, "Sagas paragraph", "un crédito de G. 86.100 millones"),
               date="2026-06-15", currency="PYG", principal=86100 * M,
               note_en="Transferred in full to Vinanzas.", note_es="Transferido íntegramente a Vinanzas.")
L_HD_USD = loan(UB, "org:hd-invest", P("regulator", s, "HD Invest paragraph", "préstamos por USD 35 millones"),
                date="2026-06-15", currency="USD", principal=35 * M, note_en="Passed directly to Vinanzas.",
                note_es="Transferido directamente a Vinanzas.")
L_HD_PYG = loan(UB, "org:hd-invest", P("regulator", s, "HD Invest paragraph", "préstamos por USD 35 millones"),
                date="2026-06-15", currency="PYG", principal=36900 * M, note_en="Guaraní loan, passed to Vinanzas.",
                note_es="Préstamo en guaraníes, transferido a Vinanzas.")
L_LTF = loan(UB, "org:la-tropa-fletes", P("regulator", s, "La Tropa Fletes paragraph", "obtuvo un préstamo de USD 10 millones"),
             date="2026-06-11", currency="USD", principal=10 * M,
             note_en="Used to buy Kasas, Model and ITTI bonds to fund Vinanzas.",
             note_es="Usado para comprar bonos de Kasas, Model e ITTI para fondear a Vinanzas.")
pf = P("regulator", s, "Factopar paragraph", "créditos por USD 6,841 millones", "medium",
       "Printed 'USD 6,841 millones' (decimal comma) = USD 6,841,000.")
L_FAC_USD = loan(UB, "org:factopar", pf, date="2026-06-15", currency="USD", principal=6_841_000,
                 note_en="For bond purchases and transfer to Vinanzas.", note_es="Para compra de bonos y transferencia a Vinanzas.")
L_FAC_P1 = loan(UB, "org:factopar", pf, date="2026-06-15", currency="PYG", principal=93000 * M,
                note_en="Guaraní loan, same day.", note_es="Préstamo en guaraníes, mismo día.")
L_FAC_P2 = loan(UB, "org:factopar", pf, date="2026-06-15", currency="PYG", principal=64500 * M,
                note_en="Guaraní loan, same day.", note_es="Préstamo en guaraníes, mismo día.")
L_SATEC = loan(UB, "org:satec", P("regulator", s, "Satec paragraph", "un crédito de USD 20 millones"),
               date="2026-06-15", currency="USD", principal=20 * M, note_en="Passed in full to Vinanzas.",
               note_es="Derivado íntegramente a Vinanzas.")
L_HENR = loan(UB, "org:henrici", P("regulator", s, "Henrici paragraph", "un préstamo de USD 10,593 millones", "medium",
                                     "ABC Color (19 Nov 2026) attributes a USD 10,593,000 loan of the same date to Franede "
                                     "('Proyecto Hotel Chaco'); outlets conflict on the borrower."),
              date="2026-03-27", currency="USD", principal=10_593_000, note_en="Transferred to ITTI.",
              note_es="Transferido a Itti Saeca.")

flow("org:sagas", VIN, 86100 * M, "PYG", "2026-06-15", "transfer", "Loan proceeds passed in full to Vinanzas",
     "Crédito transferido íntegramente a Vinanzas", P("regulator", s, "Sagas paragraph", "un crédito de G. 86.100 millones"), L_SAGAS)
flow("org:hd-invest", VIN, 35 * M, "USD", "2026-06-15", "transfer", "Loan proceeds passed directly to Vinanzas",
     "Préstamo transferido directamente a Vinanzas", P("regulator", s, "HD Invest paragraph", "préstamos por USD 35 millones"), L_HD_USD)
flow("org:hd-invest", VIN, 36900 * M, "PYG", "2026-06-15", "transfer", "Guaraní loan proceeds passed to Vinanzas",
     "Préstamo en guaraníes transferido a Vinanzas", P("regulator", s, "HD Invest paragraph", "préstamos por USD 35 millones"), L_HD_PYG)
flow("org:satec", VIN, 20 * M, "USD", "2026-06-15", "transfer", "Loan proceeds passed in full to Vinanzas",
     "Crédito derivado íntegramente a Vinanzas", P("regulator", s, "Satec paragraph", "un crédito de USD 20 millones"), L_SATEC)
flow("org:henrici", ITTI, 10_593_000, "USD", "2026-03-27", "transfer", "Loan proceeds transferred to ITTI",
     "Préstamo transferido a Itti Saeca", P("regulator", s, "Henrici paragraph", "un préstamo de USD 10,593 millones", "medium",
                                           "ABC (19 Nov) describes the same amount/date as Franede -> Vinanzas -> Itti."), L_HENR)
flow("org:technoma", VIN, 4678670.99, "USD", "2026-06", "transfer", "Funds channelled to Vinanzas out of the Technoma operation",
     "Fondos canalizados a Vinanzas desde la operación de Technoma",
     P("regulator", s, "Technoma paragraph", "", "low",
       "UH 5 Nov 2026 describes the same USD 4,678,670 as ITTI -> Vinanzas (15 Jun 2026) 'via Technoma'. Kept as printed here."), L_TECH)
flow("org:technoma", VIN, 31200 * M, "PYG", "2026-06", "transfer", "Guaraní funds channelled to Vinanzas",
     "Fondos en guaraníes canalizados a Vinanzas",
     P("regulator", s, "Technoma paragraph", "", "low", "UH 5 Nov 2026 gives G. 31.200 millones as ITTI -> Vinanzas loan on 15 Jun 2026."), L_TECH)
flow("org:factopar", "org:kasas-propiedades", 10049628.97, "USD", "2026-06", "bond_purchase",
     "Kasas Propiedades sold bonds to Factopar and La Tropa Fletes (single figure for both buyers); proceeds ended at Vinanzas",
     "Kasas Propiedades vendió bonos a Factopar y La Tropa Fletes (cifra única para ambos compradores); fondos terminaron en Vinanzas",
     P("regulator", s, "Kasas paragraph", "", "medium", "Buyer side is two firms (Factopar and La Tropa Fletes); split not given. 'from' set to Factopar only for schema reasons."))
flow("org:la-tropa-fletes", "org:model", 2117596.26, "USD", "2026-06", "bond_purchase", "Model S.A. sold bonds to La Tropa Fletes",
     "Model SA vendió bonos a La Tropa Fletes", P("regulator", s, "Model paragraph", ""))
fact("org:grupo-vazquez", "bonds_sold_june_2026", 4215707.91, "USD", "bonds issued/sold by Grupo Vázquez in the June 2026 circuit", "2026-06",
     P("regulator", s, "Grupo Vázquez paragraph", ""))

pe = lambda loc, q="": P("regulator", s, loc, q, "medium", "Role as identified in the BCP/SIB file per Última Hora.")
role("person:rodrigo-nogues-bazan", "org:nuevo-mundo-entertainment", "founder", pe("pp. 85-87 of file", "con una participación original de 33,33%"), pct=33.33,
     note_en="Founding partner, shareholder and director; original stake.", note_es="Socio fundador, accionista y directivo; participación original.")
role("person:santiago-sosa-fracchia", "org:nuevo-mundo-entertainment", "founder", pe("pp. 85-87 of file", "con una participación original de 33,33%"), pct=33.33,
     note_en="Founding partner, shareholder and director; original stake.", note_es="Socio fundador, accionista y directivo; participación original.")
role("person:enrique-vera-moreira", UB, "alternate_statutory_auditor", pe("pp. 8, 144, 152 of file", "síndico suplente de Ueno Bank"))
role("person:enrique-vera-moreira", "org:office-design", "officer", pe("pp. 8, 144, 152 of file"),
     note_en="Alternate managing partner (socio gerente suplente).", note_es="Socio gerente suplente.")
role("person:enrique-vera-moreira", "org:technoma", "beneficial_owner", pe("pp. 8, 144, 152 of file"))
role("person:andre-gayol-pires", "org:discover-paraguay", "shareholder", pe("pp. 45, 55 of file", "por la vinculación de su accionista André Gayol Pires"))

# ---------------------------------------------------------------- UH 10 Nov 2026 (chronology)
c = src("src:ultimahora-2026-11-10-cronologia", "press", "Última Hora",
        "Cronología de la caída de ueno: El BCP dejó operar 10 meses al banco con créditos a empresas vinculadas",
        "2026-11-10", "https://www.ultimahora.com/cronologia-de-la-caida-de-ueno-el-bcp-dejo-operar-10-meses-al-banco-con-creditos-a-vinculadas")
R = lambda loc, q="", conf="medium", note="": P("regulator", c, loc, q, conf, note)

L_FR1 = loan(UB, "org:franede", R("28 Aug 2025", "obtuvo un préstamo de USD 24,9 millones a diez años"), date="2025-08-28",
             term_years=10, currency="USD", principal=24_900_000, collateral="none",
             note_en="Funds transferred at once to Vinanzas, Redisa and Grupo Vázquez.",
             note_es="Fondos transferidos de inmediato a Vinanzas, Redisa y Grupo Vázquez.")
for to in (VIN, RSA, GV):
    flow("org:franede", to, None, "USD", "2025-08-28", "transfer", "Share of Franede USD 24.9m loan passed on (split not given)",
         "Parte del préstamo de USD 24,9 millones a Franede (sin desglose)", R("28 Aug 2025", "obtuvo un préstamo de USD 24,9 millones a diez años"), L_FR1)
L_HEN1 = loan(UB, "org:grupo-hendy", R("26 Sep 2025"), date="2025-09-26", currency="PYG", principal=91334 * M,
              note_en="Funds went to ITTI and Redisa to cover ITTI overdrafts. UH 4 Nov prints G. 91.334.400.000.",
              note_es="Fondos a itti y Redisa para cubrir sobregiros de itti.")
for to in (ITTI, RSA):
    flow("org:grupo-hendy", to, None, "PYG", "2025-09-26", "transfer", "Hendy loan proceeds used to cover ITTI overdrafts (split not given)",
         "Fondos del préstamo de Hendy para cubrir sobregiros de itti (sin desglose)", R("26 Sep 2025"), L_HEN1)
L_GM1 = loan(UB, "org:grupo-m", R("26 Sep 2025", "un préstamo de USD 14,3 millones", "medium",
                                    "UH 4 Nov 2026 gives USD 13,567,500 for the 26 Sep 2025 Grupo M loan; this article prints USD 14,3 millones."),
             date="2025-09-26", currency="USD", principal=14_300_000,
             note_en="Passed in full to ITTI, Red Digital and Kaitel.", note_es="Derivado íntegramente a itti, Red Digital y Kaitel.")
for to in (ITTI, RSA, "org:kaitel"):
    flow("org:grupo-m", to, None, "USD", "2025-09-26", "transfer", "Grupo M loan passed in full to ITTI, Red Digital and Kaitel (split not given)",
         "Préstamo de Grupo M derivado íntegramente a itti, Red Digital y Kaitel (sin desglose)", R("26 Sep 2025", "un préstamo de USD 14,3 millones"), L_GM1)
L_FR2 = loan(UB, "org:franede", R("30 Sep 2025", "otro préstamo de G. 65.000 millones"), date="2025-09-30", currency="PYG",
             principal=65000 * M, note_en="Sent to Vinanzas; part passed to Ueno (alleged portfolio purchase) and part to ITTI.",
             note_es="Enviado a Vinanzas; parte a ueno bank por supuesta compra de cartera y parte a itti.")
flow("org:franede", VIN, 65000 * M, "PYG", "2025-09-30", "transfer", "Franede loan proceeds sent to Vinanzas",
     "Fondos del préstamo de Franede enviados a Vinanzas", R("30 Sep 2025", "otro préstamo de G. 65.000 millones"), L_FR2)
flow(VIN, UB, None, "PYG", "2025-09-30", "portfolio_sale_price", "Part of Franede funds paid by Vinanzas to Ueno for an alleged portfolio purchase",
     "Parte de los fondos de Franede pagada por Vinanzas a ueno por supuesta compra de cartera", R("30 Sep 2025"), L_FR2, precision="month")
flow(VIN, ITTI, None, "PYG", "2025-09-30", "transfer", "Part of Franede funds passed by Vinanzas to ITTI",
     "Parte de los fondos de Franede derivada por Vinanzas a itti", R("30 Sep 2025"), L_FR2, precision="month")
L_OD1 = loan(UB, "org:office-design", R("30 Sep 2025", "un crédito de USD 13,7 millones a ocho años"), date="2025-09-30",
             term_years=8, currency="USD", principal=13_700_000,
             note_en="Applied to FX operations to cover ITTI overdrafts.", note_es="Aplicado a operaciones de cambio para cubrir sobregiros de itti.")
flow("org:office-design", ITTI, None, "USD", "2025-09-30", "transfer", "Office Design loan applied via FX operations to cover ITTI overdrafts",
     "Crédito de Office Design aplicado vía operaciones de cambio a sobregiros de itti", R("30 Sep 2025", "un crédito de USD 13,7 millones a ocho años"), L_OD1)
gq = "transferidos a Vinanzas mediante contratos de instrumentos de renta fija"
L_GSR1 = loan(UB, "org:gsr", R("Oct-Dec 2025", gq), date="2025", currency="USD", principal=7 * M, collateral="none",
              note_en="Oct-Dec 2025; placed with Vinanzas via fixed-income contracts, then re-routed to ITTI.",
              note_es="Oct-dic 2025; transferido a Vinanzas mediante contratos de renta fija y rederivado a itti.")
L_GSR2 = loan(UB, "org:gsr", R("Oct-Dec 2025", gq), date="2025", currency="USD", principal=8_500_000, collateral="none",
              note_en="Oct-Dec 2025; placed with Vinanzas via fixed-income contracts, then re-routed to ITTI.",
              note_es="Oct-dic 2025; transferido a Vinanzas mediante contratos de renta fija y rederivado a itti.")
flow("org:gsr", VIN, 7 * M, "USD", "2025", "contract", "GSR loan placed with Vinanzas via fixed-income instrument contract (Oct-Dec 2025), then re-routed to ITTI",
     "Préstamo de GSR transferido a Vinanzas por contrato de renta fija (oct-dic 2025), luego a itti", R("Oct-Dec 2025", gq), L_GSR1)
flow("org:gsr", VIN, 8_500_000, "USD", "2025", "contract", "GSR loan placed with Vinanzas via fixed-income instrument contract (Oct-Dec 2025), then re-routed to ITTI",
     "Préstamo de GSR transferido a Vinanzas por contrato de renta fija (oct-dic 2025), luego a itti", R("Oct-Dec 2025", gq), L_GSR2)
L_MOWI_OD = loan(UB, "org:mowi", R("30 Jan 2026", "amortizado el 30 de enero mediante G. 105.000 millones"), kind="overdraft",
                 date="2026-01-30", currency="PYG", principal=114000 * M,
                 note_en="Accumulated overdraft; paid down on 30 Jan 2026 with G. 105,000 million from ITTI, Redisa and Vinanzas.",
                 note_es="Sobregiro acumulado; amortizado el 30/01/2026 con G. 105.000 millones de Itti, Redisa y Vinanzas.")
flow(ITTI, "org:mowi", 105000 * M, "PYG", "2026-01-30", "repayment",
     "Mowi overdraft paid down with funds from ITTI, Redisa and Vinanzas (single figure for the three senders)",
     "Sobregiro de Mowi amortizado con fondos de Itti, Redisa y Vinanzas (cifra única para los tres)",
     R("30 Jan 2026", "amortizado el 30 de enero mediante G. 105.000 millones", "medium",
       "Senders are ITTI, Redisa and Vinanzas jointly; 'from' set to ITTI for schema reasons; split not given."), L_MOWI_OD)
L_TUIU_OD = loan(UB, "org:tuiu", R("30 Jan 2026", "canceló un sobregiro de G. 57.500 millones"), kind="overdraft", date="2026-01-30",
                 currency="PYG", principal=57500 * M, status="cancelled",
                 note_en="Cancelled with Vinanzas funds, Vinanzas having been fed by Redisa, Redipro and ITTI.",
                 note_es="Cancelado con fondos de Vinanzas, alimentada previamente por Redisa, Redipro e itti.")
flow(VIN, "org:tuiu", 57500 * M, "PYG", "2026-01-30", "repayment", "Vinanzas funds used to cancel TUIU overdraft at Ueno",
     "Fondos de Vinanzas para cancelar sobregiro de Tuiu en ueno", R("30 Jan 2026", "canceló un sobregiro de G. 57.500 millones"), L_TUIU_OD)
L_AIME1 = loan(UB, "org:aime", R("Jan 2026", "recibió préstamos por G. 133.000 millones"), date="2026-01", currency="PYG",
               principal=133000 * M, note_en="Disbursements financed ITTI, Grupo Vázquez and Redisa.",
               note_es="Desembolsos financiaron a itti, Grupo Vázquez y Redisa.")
L_AIME2 = loan(UB, "org:aime", R("Jan 2026", "recibió préstamos por G. 133.000 millones"), date="2026-01", currency="USD",
               principal=6_800_000, note_en="Disbursements financed ITTI, Grupo Vázquez and Redisa.",
               note_es="Desembolsos financiaron a itti, Grupo Vázquez y Redisa.")
for to in (ITTI, GV, RSA):
    flow("org:aime", to, None, None, "2026-01", "transfer", "Aime loan disbursements financed this company (split not given)",
         "Desembolsos de Aime financiaron a esta empresa (sin desglose)", R("Jan 2026", "recibió préstamos por G. 133.000 millones"), L_AIME1)
flow("org:aime", "org:zeta-banco", None, "PYG", "2026-05", "cheque",
     "Aime overdraft funds circulated to ITTI, Grupo Vázquez and Redipro and ended in cheques deposited at Zeta Banco (Apr-May 2026)",
     "Sobregiros de Aime circularon hacia itti, Grupo Vázquez y Redipro y terminaron en cheques depositados en Zeta Banco (abr-may 2026)",
     R("Apr-May 2026", "terminando en el libramiento de cheques depositados en Zeta Banco"))
g2 = "los préstamos de G. 30.150 millones y USD 16,9 millones"
L_GSR3 = loan(UB, "org:gsr", R("Mar-May 2026", g2), date="2026", currency="PYG", principal=30150 * M, collateral="none",
              note_en="Mar-May 2026; routed to Vinanzas and ITTI.", note_es="Mar-may 2026; derivado a Vinanzas e itti.")
L_GSR4 = loan(UB, "org:gsr", R("Mar-May 2026", g2), date="2026", currency="USD", principal=16_900_000, collateral="none",
              note_en="Mar-May 2026; routed to Vinanzas and ITTI.", note_es="Mar-may 2026; derivado a Vinanzas e itti.")
flow(ITTI, "org:grupo-m", 4_320_000, "USD", "2026-04", "repayment", "Grupo M loan instalment paid with ITTI transfers, not own revenue",
     "Cuota de Grupo M pagada con transferencias de itti y no con recursos propios", R("Apr 2026", "con transferencias de itti y no con recursos", "medium", "Notes file gives 29 Apr 2026."), approx=True)
L_BER = loan(UB, "org:grupo-berilo", R("1 Jun 2026", "recibió un préstamo de USD 26,4 millones"), date="2026-06-01", currency="USD",
             principal=26_400_000, note_en="USD 26.3m sent to Vinanzas, which passed funds to Grupo Vázquez to finance ITTI, Redisa and Redipro.",
             note_es="USD 26,3 millones a Vinanzas, que derivó a Grupo Vázquez para financiar a itti, Redisa y Redipro.")
flow("org:grupo-berilo", VIN, 26_300_000, "USD", "2026-06-01", "transfer", "Berilo loan proceeds transferred to Vinanzas",
     "Fondos del préstamo de Berilo transferidos a Vinanzas", R("1 Jun 2026", "recibió un préstamo de USD 26,4 millones"), L_BER, approx=True)
flow(VIN, GV, None, "USD", "2026-06-01", "transfer", "Vinanzas passed Berilo funds to Grupo Vázquez to finance ITTI, Redisa and Redipro",
     "Vinanzas derivó fondos de Berilo a Grupo Vázquez para financiar a itti, Redisa y Redipro", R("1 Jun 2026"), L_BER, precision="month")
L_GSR5 = loan(UB, "org:gsr", R("1 Jun 2026", "obtuvo un préstamo de G. 132.660 millones"), date="2026-06-01", currency="PYG",
              principal=132660 * M, collateral="none", note_en="Routed to Vinanzas and ITTI.", note_es="Derivado a Vinanzas e itti.")
L_NM = loan(UB, "org:nuevo-mundo-entertainment", R("1 Jun 2026", "recibió G. 198.205 millones"), date="2026-06-01", currency="PYG",
            principal=198205 * M, collateral="none", note_en="Routed to Vinanzas and ITTI.", note_es="Derivado a Vinanzas e itti.")
for b, ln in (("org:gsr", L_GSR5), ("org:nuevo-mundo-entertainment", L_NM)):
    for to in (VIN, ITTI):
        flow(b, to, None, "PYG", "2026-06-01", "transfer", "Loan proceeds routed to Vinanzas and ITTI (split not given)",
             "Préstamo derivado a Vinanzas e itti (sin desglose)", R("1 Jun 2026"), ln)
loan(UB, "org:technoma", R("11 Jun 2026", "préstamos de USD 10 millones a Technoma Saeca", "medium",
                            "This article says Technoma bought bonds of 'itti y Grupo Vázquez'; UH 5 Nov says ITTI bonds and 'ueno' bonds sold by Grupo Vázquez; UH 7 Nov says 'Itti y ueno bank'."),
     date="2026-06-11", currency="USD", principal=10 * M, note_en="For securities operations through Ueno Casa de Bolsa.",
     note_es="Para operaciones bursátiles a través de ueno Casa de Bolsa.")
loan(UB, "org:la-tropa-fletes", R("11 Jun 2026", "préstamos de USD 10 millones a Technoma Saeca"), date="2026-06-11", currency="USD",
     principal=10 * M, note_en="For securities operations via Ueno Casa de Bolsa; bought Kasas, Model, Grupo Vázquez and ITTI paper.",
     note_es="Para operaciones bursátiles vía ueno Casa de Bolsa; compró títulos de Kasas, Model, Grupo Vázquez e itti.")
flow(ITTI, "org:grupo-m", 6_320_000, "USD", "2026-06-11", "repayment", "ITTI funds used to cancel Grupo M overdraft",
     "itti usó USD 6,32 millones para cancelar el sobregiro de Grupo M", R("11 Jun 2026"), approx=True)
fact(VIN, "bank_account_balance", 93828, "USD", "balance in its bank account the day before the portfolio purchase", "2026-06-14",
     R("14 Jun 2026", "apenas USD 93.828 en su cuenta bancaria"))
fact(VIN, "funds_received_15_jun_2026", 76061604.13, "USD", "received through loans and transfers from related companies on one day", "2026-06-15",
     R("15 Jun 2026", "recibió USD 76.061.604,13 mediante préstamos y transferencias"))
flow(UB, VIN, 74418418.12, "USD", "2026-06-15", "portfolio_assignment",
     "Ueno sold impaired past-due portfolio (credits of Mowi, Grupo Hendy, Grupo M) to Vinanzas",
     "ueno vendió a Vinanzas cartera morosa deteriorada (créditos de Mowi, Grupo Hendy y Grupo M)", R("15 Jun 2026", "cartera morosa deteriorada por USD 74.418.418,12"))
flow(VIN, UB, 74418418.12, "USD", "2026-06-15", "portfolio_sale_price", "Vinanzas paid cash for the impaired portfolio",
     "Vinanzas pagó al contado la cartera morosa", R("15 Jun 2026", "pagó al contado USD 74,4 millones", "medium", "Sentence prints the rounded 'USD 74,4 millones'; exact price from same article."))
flow(VIN, RSA, 110940 * M, "PYG", "2026-06-15", "transfer", "Vinanzas remitted funds to Redisa", "Vinanzas giró fondos a Redisa",
     R("15 Jun 2026", "giró G. 110.940 millones a Redisa"))
flow(VIN, RPRO, 18770 * M, "PYG", "2026-06-15", "transfer", "Vinanzas remitted funds to Redipro", "Vinanzas giró fondos a Redipro",
     R("15 Jun 2026", "giró G. 110.940 millones a Redisa"))
L_HEN_OD = loan(UB, "org:grupo-hendy", R("15 Jun 2026", "cancelaron los sobregiros de Grupo Hendy y MOWI"), kind="overdraft",
                date="2026-06-15", currency="PYG", principal=118244 * M, status="cancelled",
                note_en="Overdraft cancelled at the bank by Redisa and Redipro.", note_es="Sobregiro cancelado en el banco por Redisa y Redipro.")
L_MOWI_OD2 = loan(UB, "org:mowi", R("15 Jun 2026", "cancelaron los sobregiros de Grupo Hendy y MOWI"), kind="overdraft",
                  date="2026-06-15", currency="PYG", principal=109668 * M, status="cancelled",
                  note_en="Overdraft cancelled at the bank by Redisa and Redipro.", note_es="Sobregiro cancelado en el banco por Redisa y Redipro.")
# Vinanzas funding table per UH 10 Nov
VN = "Funding breakdown as printed by UH 10 Nov; the article does not reconcile components with the USD 76,061,604.13 total. Do not sum."
for frm, amt, cur, pe_, ps_, ln in [
    ("org:satec", 20 * M, "USD", "Ueno loan passed directly to Vinanzas", "Préstamo de ueno transferido directamente a Vinanzas", None),
    ("org:hd-invest", 35 * M, "USD", "Ueno credit passed in full to the buyer (Vinanzas)", "Crédito de ueno derivado íntegramente a la compradora", None),
    ("org:kasas-propiedades", 10_040_000, "USD", "Transferred via fixed-income instrument contract", "Transferido mediante contrato de instrumento de renta fija", None),
    (ITTI, 4_670_000, "USD", "Transferred to Vinanzas", "Transferido a Vinanzas", None),
    (GV, 4_210_000, "USD", "Transferred to Vinanzas", "Transferido a Vinanzas", None),
    ("org:model", 2_110_000, "USD", "Transferred to Vinanzas", "Transferido a Vinanzas", None),
    ("org:sagas", 86100 * M, "PYG", "Loan passed to Vinanzas labelled as 'property purchase'", "Préstamo derivado a Vinanzas bajo la figura de 'compra de inmueble'", None),
]:
    flow(frm, VIN, amt, cur, "2026-06-15", "transfer", pe_, ps_, R("15 Jun 2026 funding list", "", "medium", VN), ln, approx=(cur == "USD" and amt not in (20 * M, 35 * M)))
loan(UB, "org:factopar", R("15 Jun 2026 funding list", "", "medium", "UH 7 Nov prints USD 6,841 millones; here USD 6,84 millones."),
     date="2026-06-15", currency="USD", principal=6_840_000,
     note_en="Factopar bought bonds of Kasas Propiedades, Grupo Vázquez and ITTI for USD 6.8 million.",
     note_es="Factopar adquirió bonos de Kasas Propiedades, Grupo Vázquez e itti por USD 6,8 millones.")
fact(VIN, "guarani_lines_gathered_15_jun_2026", 218700 * M, "PYG", "guaraní funds gathered from lines of Factopar, HD Invest and Sagas", "2026-06-15",
     R("15 Jun 2026", "", "medium", "Component split not given by the article."))
fact("org:gsr", "debt_to_ueno_bank", 439134 * M, "PYG", "debt exclusively with Ueno Bank; article equates to about USD 75 million", "2026-08",
     R("Aug 2026", "una deuda de G. 439.134 millones exclusivamente con ueno bank"))
fact("org:gsr", "overdraft_outstanding", 97800 * M, "PYG", "overdraft in force at end of September 2026", "2026-09", R("Sep 2026"))
fact("org:gsr", "investment_project_financed_by_ueno", 72 * M, "USD", "investment project financed entirely by Ueno (Caso IX)", "2025-2026",
     R("Caso IX", "proyecto de inversión de USD 72 millones"))
fact("org:gsr", "projected_revenue", 10685 * M, "PYG", "revenue projection in credit file (no supporting contracts per SIB)", "2025",
     R("Caso IX", "de G. 10.685 millones en 2025 a G. 124.448 millones"))
fact("org:gsr", "projected_revenue", 124448 * M, "PYG", "revenue projection in credit file (no supporting contracts per SIB)", "2026",
     R("Caso IX", "de G. 10.685 millones en 2025 a G. 124.448 millones"))
loan(UB, "org:gsr", R("Caso IX", "Los plazos alcanzaban 3.600 días, equivalentes a diez años"), date="2025", term_days=3600, term_years=10,
     collateral="none", amortisation="annual instalments, 360-day grace period",
     note_en="General terms of GSR loans 2025-2026 (Caso IX): sole signature, investment-project and working-capital modalities; rate not reported. Not a single operation.",
     note_es="Condiciones generales de los préstamos a GSR 2025-2026 (Caso IX): a sola firma; tasa no informada. No es una operación única.")
role("person:jose-augusto-sala-cardozo", "org:gsr", "legal_representative",
     R("Caso IX", "Acta de Directorio N.º 1254 del 9 de diciembre de ese año", "medium", "Article prints 'José Salas'; partner and legal representative of GSR."),
     note_en="Partner and legal representative.", note_es="Socio y representante legal.")
role("person:jose-augusto-sala-cardozo", UB, "officer", R("Caso IX", "Acta de Directorio N.º 1254 del 9 de diciembre de ese año"), end="2024-12",
     note_en="Interim general manager of Ueno until December 2024 (Board Minutes No. 1254 of 9 Dec 2024).",
     note_es="Gerente general interino de ueno hasta diciembre de 2024 (Acta de Directorio N.º 1254).")

E = lambda d, cat, te, ts, de, ds, parties, loc, q="", amount=None, currency=None, by="regulator", conf="medium", note="", precision=None: \
    event(d, cat, te, ts, de, ds, parties, P(by, c, loc, q, conf, note), amount, currency, precision)
E("2025-08", "credit", "Related-company credit operations begin", "Comienzan las operaciones de crédito entre vinculadas",
  "Per the BCP file, sole-signature loans of up to ten years begin; disbursements end at ITTI, Vinanzas, Redisa and Grupo Vázquez.",
  "Según el expediente del BCP, comienzan préstamos a sola firma de hasta diez años; los desembolsos terminan en itti, Vinanzas, Redisa y Grupo Vázquez.",
  [UB, ITTI, VIN, RSA, GV], "Aug 2025", "comenzaron en agosto de 2025")
E("2025-08", "credit", "TUIU receives long-term sole-signature credits", "Tuiu recibe créditos de largo plazo a sola firma",
  "Operations began the day after a share transfer to executives linked to the group; amounts not published.",
  "Las operaciones comenzaron al día siguiente de una transferencia accionaria a ejecutivos vinculados al grupo; sin montos.",
  [UB, "org:tuiu"], "Aug 2025", "cuyas operaciones comenzaron al día siguiente")
E("2025-09-26", "credit", "Ueno opens Mowi account and disburses without fund blocking", "ueno abre cuenta de Mowi y desembolsa sin bloqueo de fondos",
  "Account opening and disbursements approved without blocking of funds or legal backing documents, per the file.",
  "Apertura de cuenta y desembolsos aprobados sin bloqueo de fondos y sin documentación legal de respaldo, según el expediente.",
  [UB, "org:mowi"], "26 Sep 2025", "sin bloqueo de fondos y sin contar con documentación legal")
E("2025-10-27", "supervisory", "Ueno asks to de-link Mowi; regulator refuses", "ueno pide desvincular a Mowi; el regulador rechaza",
  "By Nota SG Nº 298/2025 Ueno asked to de-link Mowi S.A.; the regulator refused citing shared administration and operational interconnection (art. 47, Ley 861/96).",
  "Por Nota SG Nº 298/2025 ueno pidió la desvinculación de Mowi SA; el regulador la rechazó por administración compartida e interconexión operativa (art. 47, Ley 861/96).",
  [UB, "org:mowi", "auth:superintendencia-de-bancos"], "27 Oct 2025", "rechazó el pedido al constatar criterios objetivos")
E("2026-06-05", "supervisory", "SIB confirms Mowi and Grupo Hendy remain related parties", "La SIB ratifica que Mowi y Grupo Hendy siguen vinculadas",
  "The Superintendency ordered recalculation of global exposure limits.", "La Superintendencia exigió recalcular los límites globales de exposición.",
  ["auth:superintendencia-de-bancos", UB, "org:mowi", "org:grupo-hendy"], "5 Jun 2026", "debían permanecer como empresas vinculadas")
E("2026-06-08", "supervisory", "SIB report SEFS 4 Nº 006/2026 on group GPV 1535", "Informe SEFS 4 Nº 006/2026 sobre el grupo GPV 1535",
  "Supervisor report on the related group coded GPV 1535.", "Informe de supervisión sobre el grupo vinculado GPV 1535.",
  ["auth:superintendencia-de-bancos", UB], "8 Jun 2026", "Informe SEFS 4 Nº 006/2026 sobre el grupo GPV 1535")
E("2026-06-15", "credit", "Ueno sells USD 74.4m impaired portfolio to Vinanzas", "ueno vende cartera morosa por USD 74,4 millones a Vinanzas",
  "Portfolio of Mowi, Grupo Hendy and Grupo M credits; the same day Vinanzas received USD 76,061,604.13 from related companies and paid cash.",
  "Cartera de Mowi, Grupo Hendy y Grupo M; el mismo día Vinanzas recibió USD 76.061.604,13 de sociedades relacionadas y pagó al contado.",
  [UB, VIN, "org:mowi", "org:grupo-hendy", "org:grupo-m"], "15 Jun 2026", "cartera morosa deteriorada por USD 74.418.418,12", 74418418.12, "USD")
E("2026-07-10", "supervisory", "SIB report SEFS 4 Nº 007/2026: first signs of triangulated funding", "Informe SEFS 4 Nº 007/2026: primeros indicios de financiación triangulada",
  "First document identifying signs of triangulated financing. The same day supervision manager Fernando Rivarola was reassigned to the AFD; in an e-mail he asked that the 15 June operation not be accepted.",
  "Primer documento que identifica indicios de financiación triangulada. Ese día el gerente Fernando Rivarola fue designado en la AFD; en un correo pidió no aceptar la operación del 15 de junio.",
  ["auth:superintendencia-de-bancos", UB, VIN], "10 Jul 2026", "no se aceptara la operación del 15 de junio")
E("2026-07-28", "supervisory", "SIB report SEFS 4 Nº 010/2026 confirms buyer lacked own funds", "Informe SEFS 4 Nº 010/2026 confirma insuficiencia de recursos de la compradora",
  "Confirms the operation and Vinanzas' lack of own resources.", "Confirma la operación y la insuficiencia de recursos propios de Vinanzas.",
  ["auth:superintendencia-de-bancos", UB, VIN], "28 Jul 2026", "confirmó la operación y la insuficiencia de recursos propios")
E("2026-08-05", "supervisory", "SIB findings report Nº 011/2026: prohibited indirect financing", "Informe de Hallazgos Nº 011/2026: financiación indirecta prohibida",
  "Informe de Hallazgos SB.GS.ISEFS.SEFS 4 Nº 011/2026: the SIB determines Ueno indirectly financed the purchase of its own past-due portfolio through SATEC, HD Invest, Technoma, Factopar and La Tropa Fletes.",
  "Informe de Hallazgos SB.GS.ISEFS.SEFS 4 Nº 011/2026: la SIB determina que ueno financió indirectamente la compra de su propia cartera morosa vía SATEC, HD Invest, Technoma, Factopar y La Tropa Fletes.",
  ["auth:superintendencia-de-bancos", UB, VIN, "org:satec", "org:hd-invest", "org:technoma", "org:factopar", "org:la-tropa-fletes"], "5 Aug 2026",
  "financiación indirecta prohibida para adquirir su propia cartera morosa")
E("2026-09-24", "supervisory", "BCP board Resolution No. 42 opens sumario against Ueno and directors", "Directorio del BCP aprueba Resolución N.º 42: sumario a Ueno y directores",
  "Orders an administrative proceeding (sumario) against Ueno Bank and its directors for alleged serious faults.",
  "Ordena instruir sumario contra Ueno Bank y sus directores por presuntas faltas graves.", ["auth:bcp", UB], "24 Sep 2026", "aprobó la Resolución N.º 42")
E("2026-10", "supervisory", "SIB note SB.SG Nº 00307/2026 orders reclassification to risk category 3", "Nota SB.SG Nº 00307/2026 exige reclasificar a categoría 3",
  "New SIB reports on related exposure; note requires reclassification (GSR among those ordered to category 3).",
  "Nuevos informes sobre exposición con vinculados; la nota exige reclasificar en categoría de riesgo 3 (GSR entre ellas).",
  ["auth:superintendencia-de-bancos", UB, "org:gsr"], "Oct 2026", "Nota SB.SG Nº 00307/2026")
E("2026-10-22", "credit", "Ueno reports reclassifying Nuevo Mundo and Nubicom", "ueno informa reclasificación de Nuevo Mundo y Nubicom",
  "Bank informs it reclassified the two borrowers.", "El banco informa que reclasificó a ambas prestatarias.",
  [UB, "org:nuevo-mundo-entertainment", "org:nubicom"], "22 Oct 2026", "reclasificado a Nuevo Mundo Entertainment SA y Nubicom Paraguay SA", by="company")
E("2026-11-03", "criminal", "BCP sends 199-page file to Attorney General (Nota BCP/P Nº 019)", "El BCP remite expediente de 199 páginas al fiscal general (Nota BCP/P Nº 019)",
  "Requests an ex officio criminal investigation for alleged breach of trust and patrimonial damage.",
  "Pide investigación penal de oficio por presunta lesión de confianza y daño patrimonial.", ["auth:bcp", "auth:ministerio-publico", UB], "3 Nov 2026",
  "lesión de confianza y daño patrimonial")

# ---------------------------------------------------------------- UH 5 Nov 2026 (ITTI hub)
i = src("src:ultimahora-2026-11-05-itti-centro-operativo", "press", "Última Hora",
        "itti, el centro operativo por donde triangulaban todos los recursos de ueno a empresas de fachada", "2026-11-05",
        "https://www.ultimahora.com/itti-el-centro-operativo-por-donde-triangulaban-todos-los-recursos-de-ueno-a-empresas-de-fachada")
RI = lambda loc, q="", conf="medium", note="": P("regulator", i, loc, q, conf, note)
L_TECH_I = loan(UB, "org:technoma", RI("bond operation of 11 Jun 2026", "préstamo de USD 10 millones"), date="2026-06-11", currency="USD",
                principal=10 * M, note_en="Financed purchase of ITTI bonds and 'ueno' bonds.", note_es="Financió compra de bonos de itti y de bonos 'ueno'.")
flow("org:technoma", ITTI, 4230383.21, "USD", "2026-06-11", "bond_purchase", "Technoma bought ITTI bonds, nominal USD 4,199,000",
     "Technoma compró bonos de itti, valor nominal USD 4.199.000", RI("bond operation of 11 Jun 2026"), L_TECH_I)
flow("org:technoma", GV, 5769861, "USD", "2026-06-11", "bond_purchase", "Technoma bought 'ueno' bonds sold by Grupo Vázquez, nominal USD 5,722,000",
     "Technoma compró bonos 'ueno' vendidos por Grupo Vázquez, valor nominal USD 5.722.000",
     RI("bond operation of 11 Jun 2026", "", "medium", "Issuer described as 'ueno'; unclear whether Ueno Bank or Ueno Holding paper. UH 10 Nov calls them Grupo Vázquez bonds."), L_TECH_I)
flow(GV, ITTI, 5769861, "USD", "2026-06-11", "transfer", "Grupo Vázquez passed the full bond-sale proceeds to ITTI",
     "Grupo Vázquez transfirió íntegramente a itti el producto de la venta de bonos", RI("bond operation of 11 Jun 2026", "transfirió íntegramente a itti"), L_TECH_I)
fact(ITTI, "received_from_technoma_bond_operation", 10000244, "USD", "total ITTI received from the two bond operations of 11 Jun 2026 (as printed)", "2026-06-11",
     RI("bond operation of 11 Jun 2026"))
L_GM_OD = loan(UB, "org:grupo-m", RI("Grupo M overdraft"), kind="overdraft", currency="USD", outstanding=6321573.22, status="cancelled",
               note_en="Negative balance cancelled with ITTI transfer.", note_es="Saldo negativo cancelado con transferencia de itti.")
flow(ITTI, "org:grupo-m", 6321574, "USD", "2026-06", "repayment", "ITTI transfer to cancel Grupo M overdraft of USD 6,321,573.22 at Ueno",
     "Transferencia de itti para cancelar sobregiro de Grupo M de USD 6.321.573,22 en ueno",
     RI("Grupo M overdraft", "", "medium", "Date not in this article; UH 10 Nov dates it 11 Jun 2026."), L_GM_OD)
flow(ITTI, VIN, 4678670, "USD", "2026-06-15", "loan", "ITTI loan to Vinanzas under framework contract of 31 Oct 2025 (13% a year), credited to Vinanzas USD savings account at Ueno",
     "Préstamo de itti a Vinanzas bajo contrato marco del 31/10/2025 (13% anual), acreditado en caja de ahorro en dólares de Vinanzas en ueno",
     RI("15 Jun 2026", "itti Saeca transfirió USD 4.678.670", "medium", "UH 7 Nov prints USD 4.678.670,99 and attributes the channeling to Technoma."))
flow(ITTI, VIN, 31200 * M, "PYG", "2026-06-15", "loan", "ITTI loan to Vinanzas under the framework contract",
     "Préstamo de itti a Vinanzas bajo el contrato marco", RI("15 Jun 2026"))
sv = "devoluciones por servicios"
flow(RSA, "org:grupo-hendy", 110940 * M, "PYG", "2026-06-15", "transfer", "Booked as service refunds; used to cover Hendy overdraft at Ueno",
     "Registrado como devolución de servicios; cubrió sobregiro de Hendy en ueno", RI("15 Jun 2026", sv), L_HEN_OD)
flow(RPRO, "org:grupo-hendy", 7304 * M, "PYG", "2026-06-15", "transfer", "Booked as service refunds; used to cover Hendy overdraft at Ueno",
     "Registrado como devolución de servicios; cubrió sobregiro de Hendy en ueno", RI("15 Jun 2026", sv), L_HEN_OD)
flow(RSA, "org:mowi", 98202 * M, "PYG", "2026-06-15", "transfer", "Booked as service refunds; used to cover Mowi overdraft at Ueno",
     "Registrado como devolución de servicios; cubrió sobregiro de Mowi en ueno",
     RI("15 Jun 2026", sv, "medium", "UH 10 Nov says Vinanzas sent Redisa only G. 110.940 millones that day, while Redisa paid out G. 110.940 + 98.202 millones here; unreconciled."), L_MOWI_OD2)
flow(RPRO, "org:mowi", 11466 * M, "PYG", "2026-06-15", "transfer", "Booked as service refunds; used to cover Mowi overdraft at Ueno",
     "Registrado como devolución de servicios; cubrió sobregiro de Mowi en ueno", RI("15 Jun 2026", sv), L_MOWI_OD2)
VI = "Contributor list as printed by UH 5 Nov (exact figures truncated to whole dollars in the article)."
for frm, amt, pe_, ps_ in [
    ("org:satec", 20 * M, "Direct contribution to Vinanzas", "Aporte directo a Vinanzas"),
    ("org:hd-invest", 35 * M, "Direct contribution to Vinanzas", "Aporte directo a Vinanzas"),
    ("org:kasas-propiedades", 10049628, "Via Factopar and La Tropa Fletes (bond sale proceeds)", "Vía Factopar y La Tropa Fletes (venta de bonos)"),
    (GV, 4215707, "Via La Tropa Fletes (bond sale proceeds)", "Vía La Tropa Fletes (venta de bonos)"),
    ("org:model", 2117596, "Bond sale proceeds", "Producto de venta de bonos"),
]:
    flow(frm, VIN, amt, "USD", "2026-06-15", "transfer", pe_, ps_, RI("Vinanzas contributors, 15 Jun 2026", "Vinanzas utilizó los fondos acreditados", "medium", VI))
fact(VIN, "funds_received_15_jun_2026", 76061604.13, "USD", "funds credited to Vinanzas on the day of the portfolio purchase", "2026-06-15", RI("Vinanzas contributors"))
flow(VIN, UB, 74418418, "USD", "2026-06-15", "portfolio_sale_price", "Vinanzas paid Ueno for the assigned portfolio the same day",
     "Vinanzas pagó a ueno la cartera cedida el mismo día", RI("Vinanzas contributors", "Vinanzas utilizó los fondos acreditados"))
loan(UB, RPRO, RI("loan Nº 612561002345", "Nº 612561002345", "low", "Borrower of this operation is not clearly identified in the extraction; repaid with funds Redipro had received from ITTI."),
     op_number="612561002345", note_en="Ueno loan repaid with funds Redipro received from ITTI; borrower identity uncertain.",
     note_es="Préstamo de ueno repagado con fondos que Redipro recibió de itti; prestataria incierta.")
event("2025-10-31", "corporate", "ITTI-Vinanzas framework loan contract", "Contrato marco de préstamos itti-Vinanzas",
      "Framework contract for ITTI to finance Vinanzas' commercial operations and projects at 13% a year.",
      "Contrato marco para que itti financie operaciones comerciales y proyectos de Vinanzas, tasa anual 13%.", [ITTI, VIN], RI("contracts"))
fact(ITTI, "home_banking_operators_of_borrowers_who_were_itti_staff", 12, None, "home-banking operators of Mowi and other borrowers who were active ITTI employees (Bankitti system review)",
     "2025-2026", RI("home banking finding", "indicio de unidad de decisión y control"))
event("2026-11-05", "statement", "SIB: 12 borrower home-banking operators were ITTI staff", "SIB: 12 operadores de home banking de prestatarias eran funcionarios de itti",
      "Reported finding that home-banking operators of Mowi, Grupo Hendy, Grupo M, TUIU, Franede and Aime were active ITTI employees; SIB treats it as an indication of unity of decision and control. Date is publication date.",
      "Hallazgo reportado: operadores de home banking de Mowi, Grupo Hendy, Grupo M, TUIU, Franede y Aime eran funcionarios activos de itti; la SIB lo considera indicio de unidad de decisión y control. Fecha = publicación.",
      [ITTI, "org:mowi", "org:grupo-hendy", "org:grupo-m", "org:tuiu", "org:franede", "org:aime"], RI("home banking finding", "funcionarios activos de itti Saeca"))

# ---------------------------------------------------------------- UH 11 Nov 2026 (GSR)
g = src("src:ultimahora-2026-11-11-gsr-usd-78-millones", "press", "Última Hora",
        "Ueno prestó USD 78 millones a GSR, firma con capital de G. 100 millones representada por su ex gerente", "2026-11-11",
        "https://www.ultimahora.com/ueno-presto-usd-78-millones-a-gsr-firma-con-capital-de-g-100-millones-representada-por-su-exgerente")
PG = lambda loc, q="", conf="medium", note="", by="press": P(by, g, loc, q, conf, note)
fact("org:gsr", "paid_in_capital", 100 * M, "PYG", "paid-in capital (about USD 17,300 per article); MIC registry data", "2026", PG("GSR profile"))
fact("org:gsr", "debt_to_ueno_bank", 453828 * M, "PYG", "debt to Ueno; article equates to about USD 78 million", "undated (2026)",
     PG("lead", "", "medium", "UH 10 Nov gives G. 439.134 millones at Aug 2026; this is the debtor-list figure."))
fact("org:mowi", "debt_to_ueno_bank", 254157 * M, "PYG", "debt to Ueno Bank", "undated (2026)", PG("Mowi paragraph"))
fact("org:dobrestec", "debt_to_ueno_bank", 17737 * M, "PYG", "debt to Ueno Bank", "undated (2026)", PG("Dobrestec paragraph"))
fact("org:dobrestec", "state_contracts_awarded", 77906099420, "PYG", "awards from the State incl. share in Consorcio Track", "undated", PG("Dobrestec paragraph"))
fact("org:tsv-del-paraguay", "debt_to_ueno_bank", 92307 * M, "PYG", "debt to Ueno Bank", "undated (2026)", PG("TSV paragraph"))
fact("org:tsv-del-paraguay", "state_contract_value", 81332 * M, "PYG", "contract ID 451113 (Consorcio Track, electronic ankle monitors)", "undated", PG("TSV paragraph"))
role("person:jose-augusto-sala-cardozo", "org:gsr", "legal_representative", PG("GSR profile", "", "medium", "Per Ministry of Industry and Commerce (MIC) data cited by UH."))
role("person:jose-augusto-sala-cardozo", "org:mowi", "shareholder", PG("Mowi paragraph"), pct=90)
role("person:jose-augusto-sala-cardozo", UB, "officer", PG("Sala paragraph", "ex gerente general interino"), end="2024-12",
     note_en="Sub-general manager, then interim general manager until December 2024.", note_es="Subgerente general y luego gerente general interino hasta diciembre de 2024.")
event("2023-02-23", "corporate", "GSR E.A.S. incorporated", "Constitución de GSR EAS", "Incorporated as a simplified stock company; declared activity investigation and security.",
      "Constituida como empresa por acciones simplificadas; actividad declarada investigación y seguridad.", ["org:gsr"], PG("GSR profile"))
event("2026-11-04", "criminal", "Indictment places GSR and five others in 'Bloque C'", "La imputación ubica a GSR y otras cinco en el 'Bloque C'",
      "Acta de imputación Nº 1 (Causa Nº 89/2026): Bloque C = firms 'without indications of linkage' but with the same pattern of credits and overdrafts: Nuevo Mundo Entertainment, Nubicom, GSR, Office Design, Grupo Berilo, Galadriel. UH notes GSR's legal representative is a former senior Ueno executive.",
      "Acta de imputación Nº 1 (Causa Nº 89/2026): Bloque C = firmas 'sin indicios de vinculación' pero con el mismo patrón de créditos y sobregiros: Nuevo Mundo Entertainment, Nubicom, GSR, Office Design, Grupo Berilo, Galadriel.",
      ["auth:ministerio-publico", "org:gsr", "org:nuevo-mundo-entertainment", "org:nubicom", "org:office-design", "org:grupo-berilo", "org:galadriel"],
      PG("Bloque C paragraph", "sin indicios de vinculación", "medium", "Date is that of the indictment (4 Nov 2026) per other outlets; article published 11 Nov.", by="prosecution"))

# ---------------------------------------------------------------- UH 16 Nov 2026 (La Tropa)
t = src("src:ultimahora-2026-11-16-la-tropa", "press", "Última Hora",
        "Ganadera La Tropa trianguló préstamos del Grupo Vázquez y movió animales en plena intervención", "2026-11-16",
        "https://www.ultimahora.com/ganadera-la-tropa-triangulo-prestamos-del-grupo-vazquez-y-movio-animales-en-plena-intervencion")
PT = lambda loc, q="", conf="medium", note="", by="press": P(by, t, loc, q, conf, note)
YR = "Article gives day and month only; year 2026 assumed from context."
L_LT = loan(UB, "org:la-tropa-sae", PT("23 April loan", "un préstamo de USD 5.936.654,88", "low",
                                         YR + " Lender not named in the sentence; article frames it as Ueno/Grupo Vázquez loan triangulation and names Ueno as La Tropa's main creditor."),
            date="2026-04-23", currency="USD", principal=5936654.88, note_en="Equivalent G. 36,172,717,196; transferred the same day to Grupo Vázquez.",
            note_es="Equivalente a G. 36.172.717.196; transferido el mismo día a Grupo Vázquez.")
flow("org:la-tropa-sae", GV, 5936654.88, "USD", "2026-04-23", "transfer", "La Tropa SAE passed the loan to Grupo Vázquez the same day",
     "La Tropa SAE transfirió los fondos a Grupo Vázquez ese mismo día", PT("23 April loan", "transfirió los fondos ese mismo día", "medium", YR), L_LT)
flow(GV, ITTI, None, "PYG", "2026-04-24", "transfer", "Next day funds passed from Grupo Vázquez to ITTI", "Al día siguiente los fondos pasaron de Grupo Vázquez a itti",
     PT("23 April loan", "", "medium", YR + " Date inferred from 'al día siguiente'."), L_LT)
flow(ITTI, "org:mowi", None, "PYG", "2026-04-24", "transfer", "ITTI passed funds to Mowi, which partly cancelled a G. 33,500 million debt at Ueno",
     "itti pasó fondos a Mowi, que canceló parcialmente una deuda de G. 33.500 millones con ueno",
     PT("23 April loan", "cancelar parcialmente una deuda de G. 33.500 millones", "medium", YR), L_LT)
fact("org:mowi", "debt_partly_cancelled_apr_2026", 33500 * M, "PYG", "Mowi debt at Ueno partly cancelled with funds routed from La Tropa SAE", "2026-04", PT("23 April loan", "cancelar parcialmente una deuda de G. 33.500 millones"))
fact("org:la-tropa-sae", "debt_to_ueno_bank_capital", 33_920_000, "USD", "capital owed to Ueno Bank (plus interest and guaraní debts), bond prospectus data", "2026-06-30",
     PT("prospectus data", "principal acreedor con obligaciones de corto y largo plazo", by="company"))
fact("org:la-tropa-sae", "temporary_investments_in_ueno_holding", 89321 * M, "PYG", "temporary investments in 'ueno holding'", "2026-06-30", PT("prospectus data", "inversiones temporales en ueno holding", by="company"))
fact("org:la-tropa-sae", "temporary_investments_in_ueno_holding", 40113 * M, "PYG", "temporary investments in 'ueno holding'", "2025-12-31", PT("prospectus data", "inversiones temporales en ueno holding", by="company"))
fact("org:la-tropa-sae", "bond_programme_limit", 20 * M, "USD", "bond programme organised and placed by Ueno Casa de Bolsa (up to)", "2026", PT("bond programme", "de hasta USD 20 millones", by="company"))
fact("org:la-tropa-sae", "bond_proceeds_for_ueno_bank_obligations", 13_590_000, "USD", "part of the USD 14 million refinancing use of proceeds corresponding to Ueno Bank obligations", "2026",
     PT("bond programme", "USD 13,59 millones correspondían a obligaciones", by="company"))
fact("org:la-tropa-fletes", "capital", 250 * M, "PYG", "capital at creation (2021)", "2021", PT("La Tropa Fletes profile", "creada en el 2021 con un capital"))
fact("org:la-tropa-fletes", "deposits_whole_financial_system", 2238 * M, "PYG", "deposits across the whole financial system (BCP)", "2026-05-31",
     PT("La Tropa Fletes profile", "depósitos por G. 2.238 millones", by="regulator"))
role("person:carlos-gauto-paredes", "org:la-tropa-sae", "president", PT("La Tropa SAE profile", "presidente del Directorio y accionista mayoritario"))
role("person:carlos-gauto-paredes", "org:la-tropa-sae", "shareholder", PT("La Tropa SAE profile", "presidente del Directorio y accionista mayoritario"), pct=65,
     note_en="Also co-debtor of all La Tropa SAE bank loans with Ueno.", note_es="También codeudor de todos los préstamos de La Tropa SAE con ueno.")
role("org:ueno-casa-de-bolsa", "org:la-tropa-sae", "registry_agent", PT("bond programme", "organizados por ueno Casa de Bolsa"),
     note_en="Organising and placement agent of La Tropa SAE's bond programme (closest schema role).", note_es="Agente organizador y colocador del programa de bonos de La Tropa SAE.")
L_LTF2 = loan(UB, "org:la-tropa-fletes", PT("11 June loan", "un préstamo de USD 10 millones", "medium", YR, by="regulator"), date="2026-06-11", currency="USD", principal=10 * M)
flow("org:la-tropa-fletes", "org:ueno-casa-de-bolsa", 10 * M, "USD", "2026-06-15", "transfer", "Whole loan passed to Ueno Casa de Bolsa four days later",
     "Totalidad del préstamo transferida a ueno Casa de Bolsa cuatro días después",
     PT("11 June loan", "transfirió íntegramente a ueno Casa de Bolsa", "medium", "Date computed from 'cuatro días después'.", by="regulator"), L_LTF2)
for to in (GV, "org:kasas-propiedades", "org:model", ITTI):
    flow("org:ueno-casa-de-bolsa", to, None, "USD", "2026-06-15", "bond_purchase",
         "Ueno Casa de Bolsa bought bonds for a combined USD 9,923,899.99 from Grupo Vázquez, Kasas, Model and ITTI; issuers channelled funds to Vinanzas (per-seller split not given)",
         "ueno Casa de Bolsa compró bonos por un total de USD 9.923.899,99 a Grupo Vázquez, Kasas, Model e itti; fondos canalizados a Vinanzas (sin desglose)",
         PT("11 June loan", "", "medium", "Combined amount USD 9,923,899.99 for four sellers.", by="regulator"), L_LTF2)
fact("org:ueno-casa-de-bolsa", "bonds_bought_with_la_tropa_fletes_funds", 9923899.99, "USD", "bonds bought from Grupo Vázquez, Kasas, Model and ITTI with La Tropa Fletes' USD 10 million", "2026-06-15", PT("11 June loan", by="regulator"))
for nm, ha, val in (("Don Miguel", "about 16,000 productive ha plus reserve (17,000 ha also printed)", 14_400_000), ("Doña Brígida", "500 ha, San Pedro", 1_300_000), ("Costa Flor", "100 ha, San Pedro", 250_000)):
    fact(GV, "seized_rural_property_value", val, "USD", f"Estancia {nm}: {ha}; valuation as reported", "2026-11", PT("properties", "", by="prosecution"))
fact(GV, "cattle_head_don_miguel", 6148, None, "head of cattle on Don Miguel balance", "2026-11-05", PT("cattle", "registraba 6.148 cabezas de ganado", by="prosecution"))
event("2026-11-05", "corporate", "La Tropa SAE removes 523 cattle from Estancia Don Miguel", "La Tropa SAE retira 523 animales de la estancia Don Miguel",
      "Reported removal during the intervention; a further 150 animals were sent to auction between 2 and 13 Nov; 5,475 to be located, 1,219 identified by 13 Nov (Senabico).",
      "Retiro reportado en plena intervención; otros 150 animales enviados a feria entre el 2 y el 13 de nov.; 5.475 a localizar, 1.219 identificados al 13 de nov. (Senabico).",
      ["org:la-tropa-sae", GV], PT("cattle", "retiró 523 animales del establecimiento", by="prosecution"))

# ---------------------------------------------------------------- UH 6 Nov 2026 (Luxembourg)
x = src("src:ultimahora-2026-11-06-conexion-luxemburgo", "press", "Última Hora", "La conexión Luxemburgo dentro del entramado del caso ueno bank",
        "2026-11-06", "https://www.ultimahora.com/la-conexion-luxemburgo-dentro-del-entramado-del-caso-ueno-bank")
PX = lambda loc, q="", conf="medium", note="": P("press", x, loc, q, conf, note)
UH_, UP_ = "org:u-holdings", "org:u-paraguay"
event("2023-09-29", "corporate", "U Holdings S.à r.l. incorporated in Luxembourg", "Constitución de U Holdings S.à r.l. en Luxemburgo",
      "Initial capital USD 40,704,152; registered 5 Oct 2023 in the RCS under B280698.", "Capital inicial USD 40.704.152; matriculada el 5/10/2023 en el RCS bajo N° B280698.",
      [UH_, GV], PX("incorporation", "con un capital inicial de USD 40.704.152"), 40704152, "USD")
event("2023-10-05", "corporate", "U Holdings registered in Luxembourg trade register (B280698)", "U Holdings matriculada en el RCS de Luxemburgo (B280698)",
      "Registration in the Registre de Commerce et des Sociétés.", "Inscripción en el Registro Mercantil y de Sociedades.", [UH_], PX("incorporation", "matriculada bajo el N° B280698"))
event("2024-03-20", "corporate", "U Holdings restructured through 22 share-transfer contracts", "Reestructuración de U Holdings mediante 22 contratos de transmisión",
      "22 shareholders incorporated; 19 of the 2024 holders no longer appear in the March 2026 report. Article prints both 22 and 23 as the 2024 total.",
      "Se incorporaron 22 accionistas; 19 de los de 2024 ya no figuran en el reporte de marzo de 2026. El artículo imprime 22 y 23.",
      [UH_], PX("2024 restructuring", "22 contratos de transmisión de acciones"))
fact(UH_, "share_capital", 40704152, "USD", "initial capital at incorporation", "2023", PX("incorporation", "con un capital inicial de USD 40.704.152"))
fact(UH_, "share_capital", 221866000, "USD", "reported capital 2024-2025", "2024-2025", PX("capital"))
fact(UP_, "ueno_bank_stake_value", 1522707 * M, "PYG", "value of U Paraguay's 93.05% holding in Ueno Bank", "2026", PX("ownership chain", "principal accionista con el 93,05% de participación"))
role(UP_, UB, "shareholder", PX("ownership chain", "principal accionista con el 93,05% de participación", "medium",
                               "FIX SCR (Jul 2026) gives 91.21% for U Paraguay's stake; sources differ."), pct=93.05, note_en="Main shareholder.", note_es="Principal accionista.")
role(UH_, UP_, "shareholder", PX("ownership chain"), pct=100, note_en="Sole shareholder.", note_es="Único accionista.")
role(GV, UH_, "shareholder", PX("ownership chain", "con 86,73% de participación y 98,82% de votos", "medium",
                                "Solventa (cut-off Dec 2025) gives 90.19% capital / 99.16% votes."), pct=86.73, start="2026",
     note_en="86.73% of shares, 98.82% of votes (2026).", note_es="86,73% de participación y 98,82% de votos (2026).")
role("org:otp-bank", UH_, "shareholder", PX("ownership chain", "con 9,99% de participación y 0,89% de votos", "medium", "Solventa (Dec 2025) gives 6.40%."), pct=9.99, start="2025-12",
     note_en="9.99% of shares, 0.89% of votes; entry formalised end-December 2025, consolidated mid-2026.", note_es="9,99% de participación y 0,89% de votos; ingreso formalizado a fines de diciembre de 2025.")
flow("org:otp-bank", UH_, 30 * M, "USD", "2025-12", "other", "OTP Bank equity investment in U Holdings", "Inversión de capital de OTP Bank en U Holdings",
     PX("OTP", "con una inversión de USD 30 millones"))
for h, pct in (("person:miguel-vazquez", 75.94), ("person:guillermo-vazquez", 8.02), ("person:adriana-vazquez", 8.02), ("person:rebeca-villasanti", 8.02)):
    role(h, UH_, "shareholder", PX("2023 holders", "Miguel tenía el 75,94% de participación" if pct > 70 else "", "medium",
                                    "Article also says Grupo Vázquez held 100% of the holding at constitution; the personal percentages are printed for the same year (possibly look-through)."),
         pct=pct, start="2023", note_en="Holder at constitution (2023) as printed.", note_es="Participación en la constitución (2023) según el artículo.")
for h, units in (("person:francisco-pena-palacios", 58), ("person:juan-carlos-lopez-moreira", 222), ("person:graciela-celia-de-lopez-moreira", 159), ("person:maria-del-mar-lopez-moreira", 50)):
    role(h, UH_, "shareholder", PX("2024 holders", "", "medium", "Listed in 2024; absent from the March 2026 report."), start="2024-03-20", end="2026-03",
         note_en=f"{units} units (USD {units},000) in the 2024 list.", note_es=f"{units} unidades (USD {units}.000) en la nómina de 2024.")
role("person:santiago-pena", "org:ueno-holding", "shareholder", PX("sworn declaration of 1 Sep 2023", "6.144 acciones ordinarias en Ueno Holding Saeca"), start="2023-09-01",
     note_en="6,144 ordinary shares of Ueno Holding Saeca (G. 6,144,000,000) per sworn asset declaration filed 1 Sep 2023.",
     note_es="6.144 acciones ordinarias de Ueno Holding Saeca (G. 6.144.000.000) según declaración jurada del 1/9/2023.")
