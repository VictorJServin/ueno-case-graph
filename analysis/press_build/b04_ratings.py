from lib import *

UB, GV, ITTI, VIN, RSA, RPRO = "org:ueno-bank", "org:grupo-vazquez", "org:itti", "org:vinanzas", "org:redisa", "org:redipro"
SR = "Solventa&Riskmétrica"

# ---------------------------------------------------------------- Solventa&Riskmétrica: Grupo Vázquez (27 May 2026)
s = src("src:solventa-2026-05-27-grupo-vazquez-peg-g1-usd1", "rating", SR, "Informe de calificación Grupo Vázquez S.A.E., PEG G1 y PEG USD1 (corte 31/12/2025)",
        "2026-05-27", "https://www.bolsadevalores.com.py/uploads/2026/05/GRUPO-VAZQUEZ-PEG-G1-y-USD1-Mayo26.pdf")
R = lambda loc, note="", conf="medium": P("rating_agency", s, loc, "", conf, note)
MG = "Gs. millones as printed in the rating report, converted to full guaraníes"
ind = {"revenue": (2454213, 769073), "ebitda": (1663004, 410095), "net_result": (1496578, 644790), "total_assets": (3322740, 4579376),
       "total_liabilities": (1352413, 2476137), "equity": (1970327, 2103239), "financial_debt": (932721, 1067176)}
for k, (a, b) in ind.items():
    fact(GV, k, a * M, "PYG", MG + "; individual statements", "2024-12-31", R("individual statements table"))
    fact(GV, k, b * M, "PYG", MG + "; individual statements", "2025-12-31", R("individual statements table"))
con = {"revenue": (6980682, 2191141), "ebitda": (4760394, 576534), "net_result": (1352328, 644790), "total_assets": (17190382, 6972561),
       "total_liabilities": (14592262, 4471380), "equity": (2598121, 2501181)}
for k, (a, b) in con.items():
    fact(GV, k + "_consolidated", a * M, "PYG", MG + "; consolidated (Ueno Bank consolidated in 2024, not in 2025)", "2024-12-31", R("consolidated statements table, pp. 15-17"))
    fact(GV, k + "_consolidated", b * M, "PYG", MG + "; consolidated (Ueno Bank no longer consolidated)", "2025-12-31", R("consolidated statements table, pp. 15-17"))
fact(GV, "financial_debt_consolidated", 1613206 * M, "PYG", MG + "; consolidated", "2025-12-31", R("p. 16"))
fact(GV, "debt_to_ebitda", 6.04, None, "times; individual (0.81 at Dec-2024)", "2025-12-31", R("p. 14"))
fact(GV, "investments_in_associates", 3670282 * M, "PYG", MG + "; individual", "2025-12-31", R("p. 6"))
fact(GV, "investment_in_u_holdings_carrying_value", 3083405 * M, "PYG", MG + "; 84.01% of investments in associates", "2025-12-31", R("p. 6"))
fact(GV, "income_from_valuation_of_investments", 379256 * M, "PYG", MG + "; individual (1,708,614 in 2024)", "2025", R("p. 8"))
fact(GV, "dividends_received", 12116 * M, "PYG", MG + " (5,908 in 2024)", "2025", R("p. 8"))
fact(GV, "staff", 6000, None, "'more than 6,000' direct employees", "2025-12-31", R("p. 3"))
fact(GV, "group_companies", 28, None, "companies in six business units", "2025-12-31", R("p. 3"))
fact(GV, "biological_assets", 20128 * M, "PYG", MG, "2025-12-31", R("pp. 3, 6"))
fact(GV, "bonds_outstanding_total", 828672560400, "PYG", "capital outstanding across six programmes (USD programmes expressed in guaraníes)", "2025-12-31", R("p. 12 programme table"))
for nm, yr, issued, outst in [("PEG USD1", 2021, 164638750000, 151467650000), ("PEG G1", 2021, 50000000000, 50000000000), ("PEG G2", 2023, 150000000000, 137000000000),
                              ("PEG G3", 2024, 105000000000, 105000000000), ("PEG G4", 2024, 336946000000, 336946000000), ("PEG USD3", 2025, 133574710650, 48258910400)]:
    fact(GV, "bond_programme_outstanding", outst, "PYG", f"{nm} ({yr}): issued Gs. {issued:,}; outstanding as printed", "2025-12-31",
         R("p. 12 programme table", "Report prints PEG G2 outstanding 137,000 million on p. 12 but placed 74,000 million on p. 11." if nm == "PEG G2" else ""))
for yr, v in ((2026, 74357), (2027, 28342), (2028, 65255), (2030, 87747), (2031, 76099), (2033, 5927), (2034, 391946), (2035, 25000), (2041, 74000)):
    fact(GV, "bond_capital_maturing", v * M, "PYG", "capital maturity profile read from chart, Gs. millones", str(yr), R("p. 12 chart", "Read from a chart by an automated tool.", "low"))
for h, sh, pct, ne in [("person:miguel-vazquez", 2018, 75.92, "2,000 multiple-vote ordinary shares (75.24%) plus 18 single-vote (0.68%) of 2,658."),
                       ("person:guillermo-vazquez", 160, 6.02, "160 single-vote shares."), ("person:adriana-vazquez", 160, 6.02, "160 single-vote shares."),
                       ("person:rebeca-villasanti", 160, 6.02, "160 single-vote shares."), ("person:veronica-vazquez", 160, 6.02, "160 single-vote shares.")]:
    role(h, GV, "shareholder", R("p. 4 shareholder table", "75.92% is the sum of two printed lines (75.24% + 0.68%) for the same holder." if sh == 2018 else ""), pct=pct, start="2025-12-31", note_en=ne, note_es="")
for o, cap, votes in [(ITTI, 88.80, 95.72), ("org:u-holdings", 90.19, 99.16), ("org:oniria", 60, 60), ("org:sports-lab", 60, 60), ("org:23-sports-marketing", 60, 60),
                      ("org:v-media", 99.95, 99.95), ("org:terravaz", 98.36, 97.33)]:
    nt = ""
    if o == ITTI:
        nt = "Same report prints 80.80% on p. 16; the ITTI rating report prints 94.41% capital / 97.75% votes."
    if o == "org:u-holdings":
        nt = "Última Hora (6 Nov 2026) gives 86.73% / 98.82% for 2026; the bank's own rating report prints 90.01%."
    if o == "org:terravaz":
        nt = "Terravaz rating report prints 97.33% of capital and 98.36% of votes (columns reversed relative to this table)."
    role(GV, o, "shareholder", R("p. 6 investee table", nt), pct=cap, start="2025-12-31", note_en=f"{cap}% of capital, {votes}% of votes.", note_es=f"{cap}% del capital, {votes}% de los votos.")
event("2026-05-27", "market", "Solventa&Riskmétrica rates Grupo Vázquez pyA+ (up from pyA)", "Solventa&Riskmétrica califica a Grupo Vázquez pyA+ (antes pyA)",
      "PEG G1 and PEG USD1; trend 'Fuerte (+)'; cut-off 31 Dec 2025; published 29 May 2026; auditor Grant Thornton Paraguay.",
      "PEG G1 y PEG USD1; tendencia 'Fuerte (+)'; corte 31/12/2025; publicado el 29/05/2026; auditor Grant Thornton Paraguay.", [GV], R("pp. 1, 19", "", "high"))

# ---------------------------------------------------------------- Solventa&Riskmétrica: ITTI (12 May 2026)
i = src("src:solventa-2026-05-12-itti-peg-g1", "rating", SR, "Informe de calificación ITTI S.A.E.C.A., PEG G1 (corte 31/12/2025)", "2026-05-12",
        "https://syr.com.py/wp-content/uploads/2025/09/Informe-de-Calificacion-PEG-G1-ITTI-Dic25.pdf")
RI = lambda loc, note="", conf="medium": P("rating_agency", i, loc, "", conf, note)
it = {"revenue": (1012487, 1825988), "gross_profit": (556490, 1292673), "ebitda": (339616, 418812), "net_result": (114270, 169979), "total_assets": (1578442, 2253647),
      "total_liabilities": (1323774, 1793370), "equity": (254669, 460276), "financial_debt": (394970, 346316), "bank_debt": (218548, 78185), "bond_debt": (176422, 268131),
      "sundry_debtors_intercompany": (163103, 341330), "trade_receivables": (25486, 62681), "long_term_investments_other_companies": (400009, 241933)}
for k, (a, b) in it.items():
    fact(ITTI, k, a * M, "PYG", MG + "; standalone", "2024-12-31", RI("financial tables, pp. 6-12"))
    fact(ITTI, k, b * M, "PYG", MG + "; standalone", "2025-12-31", RI("financial tables, pp. 6-12", "Report says sundry debtors are mainly inter-company operations." if k.startswith("sundry") else ""))
for k, (a, b) in {"revenue_consolidated": (1072011, 2157093), "ebitda_consolidated": (230249, 306481), "net_result_consolidated": (112914, 171561),
                  "total_assets_consolidated": (1594485, 2310386), "equity_consolidated": (247745, 448699), "financial_debt_consolidated": (395849, 347703)}.items():
    fact(ITTI, k, a * M, "PYG", MG + "; consolidated", "2024-12-31", RI("pp. 14, 16"))
    fact(ITTI, k, b * M, "PYG", MG + "; consolidated", "2025-12-31", RI("pp. 14, 16"))
fact(ITTI, "staff", 3184, None, "employees of 16 nationalities", "2025-12-31", RI("p. 4"))
fact(ITTI, "corporate_clients", 1100, None, "'more than 1,100' local and multinational companies", "2025-12-31", RI("p. 3"))
fact(ITTI, "bankitti_share_of_regulated_entities_pct", 45, None, "percent of regulated financial entities using the Bankitti core", "2025-12-31", RI("p. 3"))
fact(ITTI, "bonds_outstanding_total", 261886121850, "PYG", "capital outstanding across five programmes at Gs. 6,585.55 per USD", "2025-12-31", RI("p. 11"))
for nm, outst, nt in [("PEG G1 (2021), issued Gs. 105,000 million", 95000000000, ""), ("PEG G2 (2023), issued Gs. 60,000 million, placed Gs. 36,051 million", 36051000000, ""),
                      ("PEG USD1 (2023), USD 7,493,000 placed of USD 8,000,000", 49345526150, ""), ("PEG USD2 (2025), USD 3,000,000", 19756650000, ""),
                      ("PEG USD3 (2025), USD 9,374,000 placed of USD 9,389,000", 61732945700, "")]:
    fact(ITTI, "bond_programme_outstanding", outst, "PYG", nm + "; outstanding expressed in guaraníes", "2025-12-31", RI("p. 11"))
fact("org:discover-paraguay", "revenue_contribution_to_itti_consolidated", 191306 * M, "PYG", MG + "; Discover PY revenue in ITTI consolidated 2025", "2025", RI("p. 16"))
for h, sh, cap, votes in [(GV, 236018, 94.41, 97.75), ("org:ueno-seguros", 7577, 3.03, 1.22), ("org:business-financial-group", 6405, 2.56, 1.03)]:
    role(h, ITTI, "shareholder", RI("p. 4 shareholder table", "Grupo Vázquez rating report (same agency, 27 May 2026) prints 88.80% capital / 95.72% votes." if h == GV else ""),
         pct=cap, start="2025-12-31", note_en=f"{sh:,} of 250,000 shares; {cap}% of capital, {votes}% of votes.", note_es=f"{sh} de 250.000 acciones; {cap}% del capital, {votes}% de los votos.")
for o, pct in [("org:idl", 99.23), (VIN, 49.73), ("org:ioio", 49.24), ("org:red-uts-paraguay", 60.06), ("org:place-analyzer", 60.0), ("org:click-sa-muv", 60.0),
               ("org:hanoi-sa-monchis", 72.76), ("org:discover-paraguay", 94.63), ("org:wom-77", 60.0), ("org:fintux-mas-money", 69.79), ("org:tiva", 60.0),
               ("org:kostas-viajes-y-turismo", 98.94), ("org:comdetur", 99.0), ("org:inter-express", 0.10), ("org:consolid", 80.0), ("org:intertours", 45.0)]:
    role(ITTI, o, "shareholder", RI("investee table, pp. 4, 14"), pct=pct, start="2025-12-31")
role(VIN, ITTI, "group_role", RI("p. 5"), note_en="Outsourced same-group company that manages ITTI's collections.", note_es="Empresa tercerizada del mismo grupo que gestiona las cobranzas de ITTI.")
event("2026-05-12", "market", "Solventa&Riskmétrica rates ITTI pyA+ (up from pyA), stable", "Solventa&Riskmétrica califica a ITTI pyA+ (antes pyA), estable",
      "PEG G1 (max Gs. 105,000 million); cut-off 31 Dec 2025; rating incorporates risk of dependence on related entities and on sales to group-associated companies.",
      "PEG G1 (máx. Gs. 105.000 millones); corte 31/12/2025; la calificación incorpora el riesgo de dependencia de entidades vinculadas y de ventas a empresas asociadas al grupo.",
      [ITTI], P("rating_agency", i, "pp. 1, 18", "incorpora el riesgo derivado de la dependencia con entidades vinculadas", "medium"))
event("2004", "corporate", "ITTI starts as IT Consultores", "ITTI inicia como IT Consultores", "Merged with J. Fleischman in 2022 per the rating report.", "Se fusionó con J. Fleischman en 2022 según el informe de calificación.",
      [ITTI], RI("p. 3", "Earlier notes citing the group's website date the J. Fleischman merger to 2021."))

# ---------------------------------------------------------------- Solventa&Riskmétrica: Terravaz (17 Jun 2026)
t = src("src:solventa-2026-06-17-terravaz-peg-usd3", "rating", SR, "Informe de calificación Terravaz S.A.E., PEG USD3 (corte 31/12/2025)", "2026-06-17",
        "https://syr.com.py/wp-content/uploads/2025/08/Informe-de-Calificacion-TERRAVAZ-PEG-USD3-Dic2025.pdf")
RT = lambda loc, note="", conf="medium": P("rating_agency", t, loc, "", conf, note)
TV = "org:terravaz"
for k, (a, b) in {"revenue": (10462, 14361), "net_result": (2031, 2049), "total_assets": (258617, 283362), "total_liabilities": (182645, 205340), "equity": (75972, 78022),
                  "financial_debt": (167666, 195509), "long_term_debt_to_third_parties_mainly_shareholders": (46448, 94125)}.items():
    fact(TV, k, a * M, "PYG", MG, "2024-12-31", RT("pp. 6-13"))
    fact(TV, k, b * M, "PYG", MG, "2025-12-31", RT("pp. 6-13"))
fact(TV, "staff", 48, None, "employees", "2025-12-31", RT("p. 4"))
fact(TV, "paid_in_capital", 30000 * M, "PYG", "300 shares (Gs. 2,300 million until 2024)", "2025-12-31", RT("p. 4"))
fact(TV, "bonds_outstanding_total", 16476000, "USD", "PEG USD2 USD 14,836,000 + PEG USD3 USD 1,640,000 (total as printed)", "2025-12-31", RT("pp. 11-12", "PEG USD3 series 2 (USD 400,000) was issued 8 Jan 2026, after the cut-off, but is included."))
fact(TV, "main_asset_appraisal_market_value", 498050 * M, "PYG", "Fideicomiso Shopping Costanera appraisal (quick-sale value Gs. 398,440 million)", "2026-02", RT("p. 3"))
fact(TV, "shopping_occupancy_pct", 93, None, "percent of leasable area occupied; 54 active tenants; about 10,000 m2 GLA", "2025-12-31", RT("pp. 3-6"))
role(GV, TV, "shareholder", RT("p. 4", "Table gives 97.33% (292 of 300 shares); report text says 96.00%; votes 98.36%."), pct=97.33, start="2025-12-31",
     note_en="97.33% of capital per table, 98.36% of votes.", note_es="97,33% del capital según tabla, 98,36% de los votos.")
event("2018-08-28", "corporate", "Terravaz incorporated (as Radice SAECA)", "Constitución de Terravaz (como Radice SAECA)", "Renamed Terravaz in 2025.", "Cambió su denominación a Terravaz en 2025.", [TV], RT("p. 3", "", "high"))
event("2026-06-17", "market", "Solventa&Riskmétrica rates Terravaz pyBBB (up from pyBBB-), stable", "Solventa&Riskmétrica califica a Terravaz pyBBB (antes pyBBB-), estable",
      "PEG USD3; cut-off 31 Dec 2025; published 19 Jun 2026; auditor Baker Tilly Paraguay.", "PEG USD3; corte 31/12/2025; publicado el 19/06/2026; auditor Baker Tilly Paraguay.", [TV], RT("pp. 1, 16", "", "high"))

# ---------------------------------------------------------------- Solventa&Riskmétrica: Ueno Bank (16 Mar 2026)
b = src("src:solventa-2026-03-16-ueno-bank", "rating", SR, "Informe de calificación Ueno Bank S.A. (corte 31/12/2025)", "2026-03-16",
        "https://www.ueno.com.py/wp-content/uploads/2026/04/Informe-de-Calificacion-UENO-BANK-Dic25-firmado_Solventa.pdf")
RB = lambda loc, note="", conf="medium": P("rating_agency", b, loc, "", conf, note)
for k, (a_, b_), nt in [("total_assets", (13981751, 21095542), ""), ("net_loans", (6847709, 11111835), "Report text (p. 6); the table on p. 9 prints 6,665,790 and 10,882,577."),
                        ("deposits", (10261065, 15830815), ""), ("total_liabilities", (12543715, 18977877), ""), ("equity", (1438037, 2117665), ""),
                        ("share_capital", (820423, 1401619), ""), ("net_result", (294025, 313857), "'Utilidad a distribuir'; page 1 of the report labels 313,857 as pre-tax profit, the table gives pre-tax 344,163."),
                        ("bonds_issued", (572801, 668512), "'Otros valores emitidos'; includes subordinated programme placed Dec 2025.")]:
    fact(UB, k, a_ * M, "PYG", MG, "2024-12-31", RB("p. 9 table", nt))
    fact(UB, k, b_ * M, "PYG", MG, "2025-12-31", RB("p. 9 table", nt))
fact(UB, "roe_pct", 19.08, None, "percent (28.39 at Dec-2024)", "2025-12-31", RB("p. 10"))
fact(UB, "npl_ratio_pct", 0.44, None, "morosidad, percent (system 2.10)", "2025-12-31", RB("p. 10"))
fact(UB, "tier1_plus_tier2_pct", 15.84, None, "capital adequacy, percent (minimum 12; 21.05 at Dec-2024)", "2025-12-31", RB("p. 10", "5Días (per notes) later reported 13.85% before and 5.56% after supervisory adjustments at resolution."))
fact(UB, "other_investments", 3188417 * M, "PYG", MG + "; increase driven by larger investments in Red Digital S.A. and Redipro S.A. (no per-company amount)", "2025-12-31",
     RB("p. 6", "Table on p. 9 prints 3,015,231."))
fact(UB, "merger_expenses_trust", 2105744 * M, "PYG", MG + "; trust for merger-related expenses managed by Zeta Banco, 66.04% of other investments, to be amortised by 2035", "2025-12-31", RB("p. 6"))
fact(UB, "other_assets_incl_deferred_losses", 2514476 * M, "PYG", MG + "; includes deferred accumulated losses of the absorbed entity (amount not disclosed)", "2025-12-31", RB("p. 6"))
fact(UB, "clients", 2700000, None, "'more than 2.7 million' clients", "2025-12-31", RB("p. 3"))
fact(UB, "non_bank_correspondents", 25000, None, "'more than 25,000'", "2025-12-31", RB("p. 3"))
role("org:u-paraguay", UB, "shareholder", RB("p. 4", "Última Hora (6 Nov 2026) prints 93.05% for 2026."), pct=91.21, start="2025-12-31", note_en="1,082,682 of 1,187,065 shares.", note_es="1.082.682 de 1.187.065 acciones.")
role("org:oikocredit", UB, "shareholder", RB("p. 4"), pct=2.87, start="2025-12-31", note_en="Preferred class A shares.", note_es="Acciones preferidas clase A.")
role("org:triodos-sicav-ii", UB, "shareholder", RB("p. 4"), pct=1.37, start="2025-12-31")
role(GV, "org:u-holdings", "shareholder", RB("p. 4", "Grupo Vázquez's own rating report prints 90.19%."), pct=90.01, start="2025-12-31")
role("org:otp-bank", "org:u-holdings", "shareholder", RB("pp. 2, 4", "Última Hora (6 Nov 2026) prints 9.99% for 2026."), pct=6.4, start="2025-12", note_en="Entered late 2025.", note_es="Ingresó a fines de 2025.")
role(VIN, UB, "group_role", RB("p. 5"), note_en="Collections outsourced to Vinanzas S.A.", note_es="Cobranzas tercerizadas a Vinanzas S.A.")
role("org:zeta-banco", UB, "group_role", RB("p. 6"), note_en="Manages (as trustee) the merger-expenses trust of Gs. 2,105,744 million.", note_es="Administra el fideicomiso de gastos de fusión de Gs. 2.105.744 millones.")
event("2026-03-16", "market", "Solventa&Riskmétrica keeps Ueno Bank at AA-py, trend raised to 'Fuerte (+)'", "Solventa&Riskmétrica mantiene a Ueno Bank en AA-py, tendencia sube a 'Fuerte (+)'",
      "Cut-off 31 Dec 2025; published 17 Mar 2026.", "Corte 31/12/2025; publicado el 17/03/2026.", [UB], RB("pp. 1, 11", "", "high"))
event("2024-06", "corporate", "Ueno Bank absorbs Visión Banco", "Ueno Bank absorbe a Visión Banco", "Merger by absorption; absorbed impaired loans and foreclosed assets placed under BCP regulatory facilities.",
      "Fusión por absorción; cartera deteriorada y bienes adjudicados absorbidos bajo facilidades regulatorias del BCP.", [UB, "org:vision-banco", "auth:bcp"], RB("pp. 3, 5-6"))
