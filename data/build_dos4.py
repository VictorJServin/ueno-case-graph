#!/usr/bin/env python3
"""Rows from the user's dossier of 21 Nov 2026 06:10 PT (v1.2): the 17 new claims and the changed claims that add facts
the graph did not have. Claims the graph already holds (Peña's transfer to Viñas Cué, the phone-data order, the night
cash delivery from the record) are not repeated.

Each row cites ONE article or official page whose full link the dossier lists as checked. Individual social-media posts
are not used as sources. The links were not opened by this project, so confidence is 'medium' at most.

  python3 data/build_dos4.py /path/to/dossier.parsed.json    # private input; rewrites data/raw/dos4.*.jsonl
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, "raw")
D = json.load(open(sys.argv[1], encoding="utf-8"))["sources"]
NOTE = "Link from the 21 Nov 2026 dossier, which lists it as checked (HTTP 200). Not opened by this project. Dossier claim %s."
SRC = {  # dossier ref -> (source id, kind)
 6: ("src:diputados-2026-11-20-comision-especial", "official"), 26: ("src:asuncion-gov-2026-11-20-situacion-financiera", "official"),
 27: ("src:asuncion-gov-2026-11-18-demanda-nulidad", "official"), 36: ("src:5dias-2026-11-20-25-emisores", "press"),
 40: ("src:abc-2026-11-19-jefe-cibercrimen", "press"), 52: ("src:abc-2026-11-20-conmebol", "press"),
 66: ("src:abc-2026-11-20-pear-forraje", "press"), 73: ("src:abc-2026-10-15-balance-vinculadas", "press"),
 75: ("src:abc-2026-11-20-noche-efectivo", "press"), 77: ("src:abc-2026-11-20-tsje-niega", "press"),
 50: ("src:abc-2026-11-20-rey-comitia", "press"), 99: ("src:hoy-2026-11-21-fiscales-rolon", "press"),
 122: ("src:faro-2026-11-21-fgd-88", "press"), 123: ("src:faro-2026-11-21-rolon-onu", "press"),
 141: ("src:lanacion-2026-11-21-afd-ips", "press"), 143: ("src:lanacion-2026-11-21-itaipu-bancos", "press"),
 147: ("src:lanacion-2026-11-21-schreiner", "press"), 153: ("src:latribuna-2026-11-21-marcha-extrabajadores", "press"),
 190: ("src:ultimahora-2026-11-20-delirio-colectivo", "press"), 195: ("src:ultimahora-2026-11-20-terreno-municipal", "press"),
 12: ("src:ministerio-publico-2026-11-20-comunicado-corbeta", "official"),
}
def src(n): return SRC[n][0]
def P(who, n, claim, quote="", conf="medium", loc="article as cited in the dossier"):
    return {"asserted_by": who, "source": src(n), "locator": loc, "quote": quote, "confidence": conf, "note": NOTE % claim}
UB, GV = "org:ueno-bank", "org:grupo-vazquez"
E = []  # (date, precision, category, title_en, title_es, detail_en, detail_es, parties, amount, currency, prov)
def ev(*a): E.append(a)
ev("2025-10", "month", "statement", "Press: Rey says an employee's 'Delirio colectivo' report warned of the bank's real liquidity",
   "Prensa: Rey afirma que el informe 'Delirio colectivo' de un empleado advirtió sobre la liquidez real del banco",
   "Última Hora reports that Rey told prosecutors a liquidity-area employee warned him in October 2025 how little money remained; the employee testified as a witness on 19 Nov 2026 and Rey handed over the report. Per the outlet's reading, Rey alleges about USD 900 million of real expenses were carried as assets or loans. Co-defendant's account, not a finding.",
   "Última Hora informa que Rey declaró ante la Fiscalía que un empleado del área de liquidez le advirtió en octubre de 2025 cuán poco dinero quedaba; el empleado declaró como testigo el 19 nov 2026 y Rey entregó el informe. Según la lectura del medio, Rey alega que unos USD 900 millones de gastos reales figuraban como activos o préstamos. Es la versión de un coprocesado, no un hecho probado.",
   ["person:julio-rey", UB], 900000000, "USD", P("rey", 190, "C-DIR-10"))
ev("2023-09-07", "day", "corporate", "ABC: Financiera Ueno sold a 1,184 ha property to Pear S.R.L.; Rey attributes the company to Francisco Peña",
   "ABC: Financiera Ueno vendió un inmueble de 1.184 ha a Pear S.R.L.; Rey atribuye la empresa a Francisco Peña",
   "ABC reports the sale of 7 Sep 2023 and a Pear invoice of 3 Jun 2026 for USD 739,000 to Grupo Vázquez for forage. Rey told prosecutors the instalments (price USD 2.7-3 million) were in fact paid by Grupo Vázquez through such invoices. Outlets disagree on the property's location. Francisco Peña has not been charged in this matter; presumption of innocence.",
   "ABC informa la venta del 7 sep 2023 y una factura de Pear del 3 jun 2026 por USD 739.000 a Grupo Vázquez por forraje. Rey declaró que las cuotas (precio USD 2,7-3 millones) eran pagadas en realidad por Grupo Vázquez mediante esas facturas. Los medios difieren sobre la ubicación del inmueble. Francisco Peña no ha sido imputado por este hecho; rige la presunción de inocencia.",
   ["org:pear-srl", "person:francisco-pena-palacios", GV, "person:julio-rey"], 739000, "USD", P("rey", 66, "C-PEN-20", "Pearl S.R.L. corresponde al señor Francisco Peña Palacios"))
ev("2026-11-20", "day", "statement", "Press: Rey says Comitia pays ITTI over the voting-machine award",
   "Prensa: Rey afirma que Comitia paga a ITTI por la adjudicación de las máquinas de votación",
   "ABC reports Rey's statement that Comitia makes payments to ITTI for the award of the electoral voting-machine lease, and that the quiniela business ran through Data Force. Contested: see the TSJE and Comitia denial of the same day.",
   "ABC informa la declaración de Rey de que Comitia realiza pagos a ITTI por la adjudicación del alquiler de máquinas de votación, y que el negocio de la quiniela operaba vía Data Force. Controvertido: ver la negativa del TSJE y de Comitia del mismo día.",
   ["person:julio-rey", "org:comitia", "org:itti"], None, None, P("rey", 50, "C-OTH-04", "la empresa COMITIA realiza pagos a ITTI"))
ev("2026-11-20", "day", "statement", "TSJE denies any contract with ITTI; Comitia denies ties to Grupo Vázquez",
   "El TSJE niega todo contrato con ITTI; Comitia niega vínculos con Grupo Vázquez",
   "ABC reports the electoral court's reply that it never had a contractual link with ITTI, and Comitia's statement to the court that it holds no stake in Grupo Vázquez and only hired Ueno Seguros for transport insurance.",
   "ABC informa la respuesta de la Justicia Electoral de que nunca tuvo vínculo contractual con ITTI, y la nota de Comitia al tribunal de que no tiene participación en Grupo Vázquez y solo contrató a Ueno Seguros para un seguro de transporte.",
   ["auth:tsje", "org:comitia", "org:itti"], None, None, P("company", 77, "C-OTH-04"))
ev("2026-11-20", "day", "criminal", "Attorney General orders protection for prosecutor Corbeta after reported threats",
   "La Fiscal General dispone protección para el fiscal Corbeta tras amenazas denunciadas",
   "Communiqué of Attorney General Alba Cantero rejecting the intimidation reported by prosecutor Silvio Corbeta, adopting security measures and asking the National Police for protection. Corbeta says the representative of GSR Security threatened him during a raid; that person is charged and presumed innocent, and outlets give two different first names.",
   "Comunicado de la Fiscal General Alba Cantero que rechaza la intimidación denunciada por el fiscal Silvio Corbeta, adopta medidas de seguridad y pide protección a la Policía Nacional. Corbeta afirma que el representante de GSR Security lo amenazó durante un allanamiento; esa persona está imputada y se presume inocente, y los medios dan dos nombres de pila distintos.",
   ["person:alba-rocio-cantero", "person:silvio-corbeta", "org:gsr-security", "auth:ministerio-publico"], None, None,
   P("prosecution", 12, "C-LEG-19 / C-LEG-16", "ningún acto de intimidación o presión detendrá la labor del Ministerio Público", loc="official post of the Ministerio Público"))
ev("2026-11-20", "day", "criminal", "Prosecutors assigned to investigate former Attorney General Rolón (Res. F.G.E. 4695)",
   "Designan fiscales para investigar al ex Fiscal General Rolón (Res. F.G.E. 4695)",
   "Hoy reports the team formed by Alba Cantero to investigate Emiliano Rolón for alleged obstruction of prosecution, after a complaint by two legislators alleging inaction on Ueno. Rolón is presumed innocent.",
   "Hoy informa el equipo conformado por Alba Cantero para investigar a Emiliano Rolón por supuesta frustración de la persecución penal, tras una denuncia de dos legisladores que alegan inacción sobre Ueno. Rolón se presume inocente.",
   ["person:alba-rocio-cantero", "person:emiliano-rolon", "auth:ministerio-publico"], None, None, P("prosecution", 99, "C-LEG-14"))
ev("2026-11-20", "day", "statement", "Rolón alleges reprisals to a UN rapporteur and asks for the complaint to be archived",
   "Rolón alega represalias ante un relator de la ONU y pide archivar la denuncia",
   "Faro reports that Rolón wrote to the UN Special Rapporteur on the Independence of Judges and Lawyers alleging 'lawfare', and asked the Ministerio Público to reject the complaint against him. The original communication was not located by the dossier.",
   "Faro informa que Rolón escribió al Relator Especial de la ONU sobre la independencia de magistrados y abogados alegando 'lawfare', y pidió al Ministerio Público desestimar la denuncia en su contra. El dossier no localizó la comunicación original.",
   ["person:emiliano-rolon"], None, None, P("defence", 123, "C-LEG-15"))
ev("2026-11-17", "day", "political", "Chamber of Deputies creates a special commission to follow the Ueno resolution",
   "Diputados crea una comisión especial de seguimiento de la resolución de Ueno",
   "Resolution approved unanimously (session of 17 Nov; release of 20 Nov) creating a commission to monitor deposit-guarantee repayments, balances and the deposits of IPS and Caja Fiscal. It is separate from the bicameral inquiry commission.",
   "Resolución aprobada por unanimidad (sesión del 17 nov; comunicado del 20 nov) que crea una comisión para controlar los pagos del fondo de garantía, los balances y los depósitos del IPS y la Caja Fiscal. Es distinta de la comisión bicameral de investigación.",
   ["auth:camara-de-diputados", UB], None, None, P("regulator", 6, "C-LEG-20", loc="official release"))
ev("2026-11-20", "day", "depositor", "Deposit guarantee fund: 88% paid; 3,975 certificates of deposit pending validation",
   "Fondo de garantía: 88% pagado; 3.975 CDA pendientes de validación",
   "Faro, citing a TV interview with FGD director José Maciel: 88% of the funds earmarked for Ueno depositors disbursed; 3,975 CDAs (about G. 221,000 million) pending. The interview itself was not located by the dossier.",
   "Faro, citando una entrevista televisiva al director del FGD José Maciel: 88% de los fondos destinados a depositantes de Ueno desembolsados; 3.975 CDA (unos G. 221.000 millones) pendientes. El dossier no localizó la entrevista original.",
   ["auth:fgd", "person:jose-maciel", UB], 221000000000, "PYG", P("regulator", 122, "C-COL-16"))
ev("2026-11-20", "day", "market", "Stock exchange suspends new placements by 25 issuers without September statements",
   "La Bolsa suspende nuevas colocaciones de 25 emisores sin balances de setiembre",
   "5Días reports the preventive suspension (Circular 15/26), reportedly including Ueno Bank and several Grupo Vázquez companies. The securities superintendent said Ueno Casa de Bolsa is suspended but not in resolution and clients can move their investments.",
   "5Días informa la suspensión preventiva (Circular 15/26), que incluiría a Ueno Bank y varias empresas del Grupo Vázquez. El superintendente de valores dijo que Ueno Casa de Bolsa está suspendida pero no en resolución y que los clientes pueden trasladar sus inversiones.",
   ["org:bva", "org:ueno-casa-de-bolsa", UB, GV], None, None, P("press", 36, "C-COL-17"))
ev("2026-11-20", "day", "statement", "Central bank president: the failure involved 'connections of power and friends'",
   "Presidente del BCP: la falla involucró 'conexiones de poder y amigos'",
   "La Nación, citing a Bloomberg interview with Jorge Schreiner: the failure went beyond the banking superintendency and the central bank must be rebuilt with people able to refuse politicians. Original interview paywalled.",
   "La Nación, citando una entrevista de Bloomberg a Jorge Schreiner: la falla fue más allá de la Superintendencia de Bancos y el BCP debe reconstruirse con personas capaces de decir no a los políticos. Entrevista original de pago.",
   ["person:jorge-schreiner", "auth:bcp", UB], None, None, P("regulator", 147, "C-CB-05", "una falla que involucró conexiones de poder y amigos"))
ev("2026-11-20", "day", "depositor", "IPS draws on retirement reserves; more than USD 516 million stuck at Ueno",
   "El IPS recurre a reservas jubilatorias; más de USD 516 millones atrapados en Ueno",
   "La Nación reports the IPS legal director's statement that operating funds are trapped: USD 356 million in investments and the rest in operating accounts, plus more than USD 40 million in bonds.",
   "La Nación informa la declaración del director jurídico del IPS de que los fondos operativos están atrapados: USD 356 millones en inversiones y el resto en cuentas operativas, más de USD 40 millones en bonos aparte.",
   ["org:ips", UB], 516000000, "USD", P("company", 141, "C-IPS-05"))
ev("2026-11-21", "day", "depositor", "AFD announces a G. 50,000 million programme for small firms with frozen Ueno deposits",
   "La AFD anuncia un programa de G. 50.000 millones para mipymes con depósitos congelados en Ueno",
   "La Nación reports loans of up to G. 350 million with guarantees from Fogapy. The AFD communiqué itself was not located by the dossier.",
   "La Nación informa créditos de hasta G. 350 millones con garantías del Fogapy. El dossier no localizó el comunicado de la AFD.",
   ["org:afd", UB], 50000000000, "PYG", P("press", 141, "C-PUB-06"))
ev("2026-11-20", "day", "depositor", "Itaipú's Brazilian side asks to review the banks holding the plant's funds in Paraguay",
   "El lado brasileño de Itaipú pide revisar los bancos que manejan fondos de la entidad en Paraguay",
   "La Nación, citing Valor Econômico: the request follows USD 182 million of Itaipú deposits trapped at Ueno.",
   "La Nación, citando a Valor Econômico: el pedido sigue a USD 182 millones de depósitos de Itaipú atrapados en Ueno.",
   ["org:itaipu", UB], 182000000, "USD", P("press", 143, "C-PUB-07"))
ev("2026-11-20", "day", "depositor", "Former employees of Grupo Vázquez companies march in Asunción",
   "Extrabajadores de empresas del Grupo Vázquez marchan en Asunción",
   "La Tribuna reports about 500 marchers demanding talks on unpaid wages, severance and medical cover; organisers speak of about 6,000 people affected.",
   "La Tribuna informa unos 500 manifestantes que piden una mesa de diálogo por salarios impagos, indemnizaciones y cobertura médica; los organizadores hablan de unos 6.000 afectados.",
   [GV], None, None, P("press", 153, "C-PUB-08"))
ev("2026-11-19", "day", "criminal", "Police cybercrime chief removed from the Ueno investigation over payments from Grupo Vázquez",
   "Apartan de la investigación de Ueno al jefe de Cibercrimen de la Policía por pagos del Grupo Vázquez",
   "ABC reports that Diosnel Alarcón received G. 10 million a month paid through Vinanzas and invoiced as training; he acknowledged the payments and was removed from the case but kept his post. No charge reported; presumption of innocence.",
   "ABC informa que Diosnel Alarcón recibía G. 10 millones mensuales pagados vía Vinanzas y facturados como capacitación; reconoció los pagos y fue apartado del caso pero conserva el cargo. No se informa imputación; rige la presunción de inocencia.",
   ["person:diosnel-alarcon", GV, "org:vinanzas"], 10000000, "PYG", P("press", 40, "C-OTH-05"))
ev("2026-11-20", "day", "depositor", "Asunción reports liabilities of about G. 2.3 trillion and a liquidity squeeze worsened by Ueno",
   "Asunción informa pasivos de unos G. 2,3 billones y problemas de liquidez agravados por Ueno",
   "Municipal release: liabilities at 31 Oct, about G. 30,000 million in cash, and an invitation to banks for a short-term line of up to G. 50,000 million.",
   "Comunicado municipal: pasivos al 31 oct, unos G. 30.000 millones en caja, e invitación a bancos para una línea de corto plazo de hasta G. 50.000 millones.",
   ["auth:municipalidad-de-asuncion", UB], 2300000000000, "PYG", P("regulator", 26, "C-MUN-11", "agravadas por la situación relacionada con Ueno Bank", loc="official release"))
ev("2026-11-18", "day", "depositor", "Asunción announces a nullity suit to recover three La Piedad properties",
   "Asunción anuncia una demanda de nulidad para recuperar tres inmuebles de La Piedad",
   "Municipal release: three properties identified among 26 under review; audit requested from the Comptroller; files sent to prosecutors.",
   "Comunicado municipal: tres inmuebles identificados entre 26 en revisión; se pide auditoría a la Contraloría; antecedentes remitidos a la Fiscalía.",
   ["auth:municipalidad-de-asuncion", "person:soledad-nunez", GV], None, None, P("regulator", 27, "C-MUN-08", "vamos a presentar una demanda de nulidad para recuperar esos inmuebles", loc="official release"))
ev("2026-11-20", "day", "depositor", "Asunción: a 900 m² municipal plot was ceded to Rebeca Villasanti for under G. 200 million",
   "Asunción: un terreno municipal de 900 m² fue cedido a Rebeca Villasanti por menos de G. 200 millones",
   "Última Hora reports the municipal lawyer's account of a file processed in the name of Federico Miguel Vázquez Villasanti. Allegation by the municipality; no ruling.",
   "Última Hora informa lo expuesto por la abogada municipal sobre un expediente tramitado a nombre de Federico Miguel Vázquez Villasanti. Es una afirmación de la Municipalidad; no hay resolución judicial.",
   ["auth:municipalidad-de-asuncion", "person:rebeca-villasanti", GV], 200000000, "PYG", P("regulator", 195, "C-MUN-09"))
ev("2026-11-20", "day", "statement", "CONMEBOL discloses USD 15 million placed at Ueno; ABC reports USD 3.5 million paid to its president by Grupo Vázquez",
   "La CONMEBOL informa USD 15 millones colocados en Ueno; ABC reporta USD 3,5 millones pagados a su presidente por Grupo Vázquez",
   "ABC reports CONMEBOL's disclosure to its Council and, separately, payments to Alejandro Domínguez under a contract of 28 Oct 2025 as an advance on future commissions; CONMEBOL says that was his personal business. Contested; earlier reports gave about USD 14 million. No charge reported.",
   "ABC informa lo comunicado por la CONMEBOL a su Consejo y, por separado, pagos a Alejandro Domínguez bajo un contrato del 28 oct 2025 como anticipo de comisiones futuras; la CONMEBOL dice que era un negocio personal. Controvertido; informes previos daban unos USD 14 millones. No se informa imputación.",
   ["org:conmebol", "person:alejandro-dominguez", GV, UB], 15000000, "USD", P("press", 52, "C-OTH-01"))
ev("2026-11-20", "day", "statement", "ABC reports the alleged night cash delivery of USD 17 million and G. 17,000 million",
   "ABC informa la supuesta entrega nocturna de USD 17 millones y G. 17.000 millones en efectivo",
   "Press account of Rey's statement (already in this graph from the record): cash brought one night in May 2025 and booked as recoveries of written-off loans, backed by three receipts with consecutive numbers from three companies.",
   "Versión de prensa de la declaración de Rey (ya incluida en este grafo desde el acta): efectivo llevado una noche de mayo de 2025 y registrado como recupero de cartera castigada, con tres recibos de numeración consecutiva de tres empresas distintas.",
   ["person:julio-rey", UB, GV], 17000000, "USD", P("rey", 75, "C-DIR-09", "son con numeración consecutiva y de tres empresas diferentes"))
F = [  # entity, metric, value, currency, unit_note, period, prov
 (UB, "related_party_asset_accounts", 2400000000000, "PYG", "four asset accounts tied to related parties; exceeds effective equity (G. 2.2 trillion) by G. 197,984 million; ABC analysis", "2025-12-31", {**P("press", 73, "C-COL-05", conf="low"), "note": NOTE % "C-COL-05" + " The dossier cites several ABC articles for this claim; which one carries the figure was not confirmed."}),
 (UB, "hidden_losses_alleged", 900000000, "USD", "about; one outlet's reading of Rey's statement", "2026-11", P("rey", 190, "C-DIR-10")),
 ("org:ips", "frozen_at_ueno", 516000000, "USD", "more than; USD 356M investments, rest operating accounts; bonds of >USD 40M not included", "2026-11", P("company", 141, "C-IPS-05")),
 ("org:itaipu", "frozen_at_ueno", 182000000, "USD", "deposits", "2026-11", P("press", 143, "C-PUB-07")),
 ("org:conmebol", "frozen_at_ueno", 15000000, "USD", "1.8% of its assets per its own disclosure; earlier reports ~USD 14M", "2026-11", P("company", 52, "C-OTH-01")),
 ("auth:fgd", "cda_pending_validation", 221000000000, "PYG", "about; 3,975 certificates", "2026-11-20", P("regulator", 122, "C-COL-16")),
 ("auth:fgd", "fund_used", 644000000, "USD", "about; of USD 1,663M available", "2026-11-20", P("regulator", 122, "C-COL-16")),
 ("auth:municipalidad-de-asuncion", "total_liabilities", 2300000000000, "PYG", "about; at 31 Oct 2026", "2026-10-31", P("regulator", 26, "C-MUN-11", loc="official release")),
]
ENT = [
 ("auth:tsje", "Authority", "Tribunal Superior de Justicia Electoral (TSJE)", "Electoral court; denies any contract with ITTI.", "Justicia Electoral; niega todo contrato con ITTI.", 77),
 ("auth:fgd", "Authority", "Fondo de Garantía de Depósitos (FGD)", "Deposit guarantee fund paying Ueno depositors.", "Fondo de garantía que paga a los depositantes de Ueno.", 122),
 ("org:afd", "Company", "Agencia Financiera de Desarrollo (AFD)", "Public development lender.", "Banca pública de desarrollo.", 141),
 ("org:itaipu", "Company", "Itaipú Binacional", "Binational hydroelectric entity with deposits at Ueno.", "Entidad hidroeléctrica binacional con depósitos en Ueno.", 143),
 ("org:conmebol", "Company", "CONMEBOL", "South American football confederation; discloses funds placed at Ueno.", "Confederación Sudamericana de Fútbol; informa fondos colocados en Ueno.", 52),
 ("org:gsr-security", "Company", "GSR Security", "Security firm reported as linked to Grupo Vázquez; raided. Distinct from the borrower GSR E.A.S.", "Empresa de seguridad reportada como vinculada al Grupo Vázquez; allanada. Distinta de la prestataria GSR E.A.S.", 12),
 ("person:diosnel-alarcon", "Person", "Diosnel Alarcón González", "Head of the National Police cybercrime department; removed from the Ueno investigation. Not charged.", "Jefe de Cibercrimen de la Policía Nacional; apartado de la investigación de Ueno. No imputado.", 40),
 ("person:alejandro-dominguez", "Person", "Alejandro Domínguez", "President of CONMEBOL. Not charged.", "Presidente de la CONMEBOL. No imputado.", 52),
]
def dump(kind, rows):
    with open(os.path.join(RAW, "dos4.%s.jsonl" % kind), "w", encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
dump("sources", [{"id": sid, "kind": kind, "outlet": re.sub(r"\s*\(PY\)|\s*\(@\w+\) on X", "", D[str(n)]["outlet"]), "title": re.split(r"\s+\S+-\S+-\S+-", D[str(n)]["title"])[0] or "(title not captured)",
                  "date": D[str(n)]["date"], "url": D[str(n)]["url"], "page": "link listed in the dossier of 21 Nov 2026, ref [%d]" % n} for n, (sid, kind) in sorted(SRC.items())])
dump("events", [{"id": "dos4:event:%04d" % i, "date": a[0], "date_precision": a[1], "category": a[2], "title_en": a[3], "title_es": a[4], "detail_en": a[5],
                 "detail_es": a[6], "parties": a[7], "amount": a[8], "currency": a[9], "prov": a[10]} for i, a in enumerate(E, 1)])
dump("facts", [{"id": "dos4:fact:%04d" % i, "entity": a[0], "metric": a[1], "value": a[2], "currency": a[3], "unit_note": a[4], "period": a[5], "prov": a[6]} for i, a in enumerate(F, 1)])
dump("entities", [{"id": a[0], "type": a[1], "label": a[2], "aliases": [], "desc_en": a[3], "desc_es": a[4],
                   "prov": {"asserted_by": "press", "source": src(a[5]), "locator": "article as cited in the dossier", "quote": "", "confidence": "medium", "note": ""}} for a in ENT])
print(len(SRC), "sources,", len(E), "events,", len(F), "facts,", len(ENT), "entities")
