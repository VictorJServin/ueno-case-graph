# Generates rec.*.jsonl (record-only dataset). Run: python3 build_rec.py
import json, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
os.makedirs(OUT, exist_ok=True)
rows = {k: [] for k in ("sources", "entities", "roles", "loans", "flows", "events", "issues")}
cnt = {}

def nid(t):
    cnt[t] = cnt.get(t, 0) + 1
    return "rec:%s:%04d" % (t, cnt[t])

def P(page, loc, by=None, quote="", conf="high", note=""):
    if by is None:
        by = "rey" if page >= 20 else "prosecution"
    return {"asserted_by": by, "source": "src:acta-p%02d" % page, "locator": loc, "quote": quote,
            "confidence": conf, "note": note}

# ---------------- sources
for i in range(1, 25):
    rows["sources"].append({"id": "src:acta-p%02d" % i, "kind": "record", "outlet": "Ministerio Público del Paraguay",
        "title": "Acta de Declaración Indagatoria, Julio Daniel Rey Fernández, Causa 89/2026", "date": "2026-11-04",
        "url": "", "page": i})

# ---------------- entities
def ent(id, type, label, de, ds, prov, aliases=None, be="", bs=""):
    rows["entities"].append({"id": id, "type": type, "label": label, "aliases": aliases or [], "desc_en": de,
        "desc_es": ds, "business_en": be, "business_es": bs, "prov": prov})

C, A, PE = "Company", "Authority", "Person"
ent("org:ueno-bank", C, "Ueno Bank S.A.", "Bank placed in resolution on 2 Nov 2026; lender in all operations described.",
    "Banco sometido a resolución el 02/11/2026; prestamista en todas las operaciones descritas.", P(1, "para. 3-5"),
    ["UENO BANK", "Banco Ueno", "Financiera Ueno"], "Financial intermediation: takes deposits from the public and lends.",
    "Intermediación financiera: captación de recursos del público y otorgamiento de préstamos.")
ent("org:grupo-vazquez", C, "Grupo Vázquez S.A.E.", "Controlling group; former shareholder of borrowers; recipient of forwarded funds; bond issuer.",
    "Grupo controlante; ex accionista de prestatarias; receptor de fondos; emisor de bonos.", P(6, "Hendy table row 1"),
    ["Grupo Vázquez", "GPV-1535"], "Holding of about 33 business units, per Rey.", "Holding de unas 33 unidades de negocio, según Rey.")
ent("org:itti", C, "ITTI S.A.E.C.A.", "Group technology company; main recipient of forwarded loan money; former shareholder of borrowers.",
    "Empresa tecnológica del grupo; principal receptora de fondos; ex accionista de prestatarias.", P(3, "last para."),
    ["ITTI", "Itti", "ITTI S.A.E."], "Technology and product development for the bank (per Rey).",
    "Desarrollos tecnológicos y de productos para el banco (según Rey).")
ent("org:redisa", C, "Red Digital S.A. (REDISA)", "Group company; recipient of forwarded loan money.",
    "Sociedad del grupo; receptora de fondos.", P(11, "para. after table"), ["REDISA", "Red Digital S.A."],
    "Part of the 'financial ecosystem' per Rey.", "Parte del 'ecosistema financiero' según Rey.")
ent("org:redipro", C, "Red Digital de Procesamiento S.A. (REDIPRO)", "Group company; recipient of forwarded loan money and source of repayments.",
    "Sociedad del grupo; receptora de fondos y origen de repagos.", P(11, "para. after table"), ["REDIPRO", "UPAY"],
    "Card acquiring / POS payments (per Rey: 'UPAY o REDIPRO').", "Adquirencia, pagos por POS (según Rey: 'UPAY o REDIPRO').")
ent("org:vinanzas", C, "Vinanzas S.A.", "Related company (GPV-1535) that bought the USD 74.4 million loan portfolio; recipient and source of funds.",
    "Empresa vinculada (GPV-1535) que compró la cartera de USD 74,4 millones; receptora y origen de fondos.", P(17, "section D"), ["VINANZAS"])
ent("org:kaitel", C, "Kaitel", "Group-related company; recipient of Grupo M loan money.", "Sociedad vinculada al grupo; receptora de fondos de Grupo M.",
    P(7, "para. 'Los créditos desembolsados'"), ["KAITEL S.A.", "Kaitel S.R.L."])
ent("org:ueno-casa-de-bolsa", C, "Ueno Casa de Bolsa S.A.", "Group brokerage; channel for the June 2026 group-bond purchases.",
    "Casa de bolsa del grupo; canal de las compras de bonos de junio de 2026.", P(17, "diagram header col. 3", conf="low", note="diagram small print"))
ent("org:ueno-seguros", C, "Ueno Seguros", "Listed by Rey as part of the financial ecosystem.", "Citada por Rey como parte del ecosistema financiero.", P(23, "para. 2"))
ent("org:ueno-afpisa", C, "AFIPSA", "Listed by Rey as part of the financial ecosystem (spelled AFIPSA in the record).",
    "Citada por Rey como parte del ecosistema financiero (escrita AFIPSA en el acta).", P(23, "para. 2"), ["AFIPSA"])
ent("org:technoma", C, "Technoma S.A.E.C.A.", "Borrower of USD 10 million on 11 Jun 2026; bought ITTI and Grupo Vázquez bonds.",
    "Prestataria de USD 10 millones el 11/06/2026; compró bonos de ITTI y Grupo Vázquez.", P(17, "diagram col. 2", conf="medium"))
ent("org:terravaz", C, "Terravaz S.A.E.", "Related company; Cecilia Domínguez is alternate director.", "Sociedad vinculada; Cecilia Domínguez es directora suplente.", P(14, "Franede table row 2"))
ent("org:kasas-propiedades", C, "Kasas Propiedades S.A.E.", "Bond issuer in the Vinanzas funding circuit.", "Emisor de bonos en el circuito de fondeo de Vinanzas.", P(17, "diagram col. 3", conf="medium"))
ent("org:model", C, "Model S.A.", "Bond issuer in the Vinanzas funding circuit; also named by Rey among firms that received deferred-expense loans.",
    "Emisor de bonos en el circuito de Vinanzas; también citada por Rey.", P(17, "diagram col. 3", conf="medium"))
ent("org:discover-paraguay", C, "Discover Paraguay S.A.", "Related company; employer of André Gayol Pires.", "Sociedad vinculada; empleadora de André Gayol Pires.", P(12, "TUIU table row 2"))
ent("org:mulair", C, "Mulair S.A.", "Company where Rodrigo Franco is vice-president and signatory.", "Sociedad donde Rodrigo Franco es VP y firmante.", P(12, "TUIU table row 4"))
ent("org:bankitti", C, "Bankitti", "Entity where L. F. Ríos is described as 'employee'.", "Entidad donde L. F. Ríos figura como 'funcionario'.", P(12, "TUIU table row 1"))
ent("org:u-holdings", C, "U Luxemburgo (as named by Rey)", "Vehicle of OTP's investment, per Rey.", "Vehículo de la inversión de OTP, según Rey.", P(23, "para. 2"), ["U Luxemburgo"])
ent("org:u-paraguay", C, "U Paraguay", "Subsidiary of 'U Luxemburgo', per Rey.", "Filial de 'U Luxemburgo', según Rey.", P(23, "para. 2"))
ent("org:otp-bank", C, "OTP Bank", "Shareholder said by Rey to be negotiating a larger stake.", "Accionista que, según Rey, negociaba aumentar su participación.", P(23, "para. 2"))
ent("org:mowi", C, "MOWI S.A.", "Group A borrower: declared related, de-listing requested Oct 2025.", "Prestataria grupo A: declarada vinculada; baja solicitada en oct. 2025.",
    P(2, "para. 1; diagram"), ["Mowi"], "Digital wallet; incorporated 12/01/2021 (diagram).", "Billetera digital; constituida el 12/01/2021 (diagrama).")
ent("org:grupo-hendy", C, "Grupo Hendy S.A.", "Group A borrower.", "Prestataria grupo A.", P(2, "para. 1; diagram"), ["Hendy S.A."],
    "E-commerce; incorporated 15/11/2013 (diagram).", "E-commerce; constituida el 15/11/2013 (diagrama).")
ent("org:grupo-m", C, "Grupo M S.A.", "Group A borrower.", "Prestataria grupo A.", P(2, "para. 1; diagram"), ["Pagopar"],
    "Payment gateway (Pagopar) (diagram).", "Pasarela de pagos (Pagopar) (diagrama).")
ent("org:tuiu", C, "TUIU S.A.", "Group B borrower: never declared related.", "Prestataria grupo B: nunca declarada vinculada.", P(10, "para. 'La empresa TUIU'"), [],
    "Digital remittances; project for own remittance platform and e-wallet; incorporated 28/11/2024 (diagram).",
    "Remesadora digital; proyecto de plataforma propia de remesas y billetera; constituida el 28/11/2024 (diagrama).")
ent("org:franede", C, "FRANEDE S.A.", "Group B borrower.", "Prestataria grupo B.", P(12, "last para."), [],
    "Hotels and projects in Asunción (diagram).", "Hotelería y proyectos en Asunción (diagrama).")
ent("org:aime", C, "AIME S.A. Corredores de Seguros", "Group B borrower.", "Prestataria grupo B.", P(15, "para. 1"), ["AIME"],
    "Insurance broking; incorporated 20/10/2018 (diagram).", "Corretaje de seguros; constituida el 20/10/2018 (diagrama).")
for i, n in (("org:satec", "SATEC S.A."), ("org:hd-invest", "HD Invest E.A.S."), ("org:la-tropa-fletes", "La Tropa Fletes E.A.S."), ("org:factopar", "Factopar S.A.")):
    ent(i, C, n, "Borrower in June 2026 whose loan funded the Vinanzas portfolio purchase.",
        "Prestataria de junio de 2026 cuyo préstamo fondeó la compra de cartera de Vinanzas.", P(17, "diagram col. 2", conf="medium"))
for i, n in (("org:nuevo-mundo-entertainment", "Nuevo Mundo Entertainment S.A."), ("org:nubicom", "Nubicom S.A."), ("org:gsr", "GSR E.A.S."),
             ("org:office-design", "Office Design S.R.L."), ("org:grupo-berilo", "Grupo Berilo S.A."), ("org:galadriel", "Galadriel S.A.")):
    ent(i, C, n, "Group C: no sign of relatedness found, same lending pattern alleged.",
        "Grupo C: sin indicios de vinculación, mismo patrón de actuación atribuido.", P(16, "section C"))
ent("org:henrici", C, "Henrichi (as spelled in the record)", "Named by Rey among firms that received deferred-expense loans.", "Citada por Rey entre las firmas con créditos para diferir gastos.", P(22, "para. 1"), ["Henrichi"])
ent("org:dataforge", C, "Data Force (as spelled in the record)", "Named by Rey: deferred-expense loans; lottery (quiniela) business said to be linked to the group.",
    "Citada por Rey: créditos; la quiniela, que estaría vinculada al grupo.", P(22, "para. 1"), ["DATA FORCE"])
ent("org:kesingtong", C, "Kesingtong (as spelled in the record)", "Loan to a related party in which Rey says he took no part.", "Crédito a vinculada en el que Rey dice no haber participado.", P(23, "para. 1"))
ent("org:pear-srl", C, "PEARL S.R.L. (as spelled in the record)", "Client to whom a property was sold, per Rey.", "Cliente al que se vendió un inmueble, según Rey.", P(23, "para. 4"), ["PEARL S.R.L."])
ent("org:comitia", C, "COMITIA", "Company said by Rey to pay ITTI over voting machines.", "Empresa que, según Rey, paga a ITTI por las máquinas de votación.", P(23, "para. 5"))
ent("org:vision-banco", C, "Visión Banco", "Bank bought and absorbed by Ueno in 2024, per Rey.", "Banco comprado y absorbido por Ueno en 2024, según Rey.", P(20, "para. 1"))
ent("org:financiera-el-comercio", C, "Financiera El Comercio", "Finance company bought to obtain a licence, per Rey.", "Financiera comprada para acceder a licencia, según Rey.", P(20, "para. 1"))
ent("org:credicentro", C, "Credicentro", "Group company Rey joined in April 2019.", "Empresa del grupo a la que Rey ingresó en abril de 2019.", P(19, "last para.", by="rey"))
ent("org:wepa", C, "WEPA", "Managed former Visión Banco branches, per Rey.", "Administraba las sucursales de Visión Banco, según Rey.", P(20, "para. 2"))
ent("org:muv", C, "MUV", "Group company Rey proposed closing or selling.", "Empresa del grupo que Rey propuso cerrar o vender.", P(21, "para. 1"))
ent("org:zeta-banco", C, "Zeta Banco", "Bank where 72-hour cheques linked to AIME overdraft money ended.", "Banco donde terminaron cheques 72 hs ligados a sobregiros de AIME.", P(16, "para. 1"))
ent("org:mckinsey", C, "McKinsey (spelled 'Mckenize' in the record)", "Consultancy Rey says was hired to strengthen Ueno.", "Consultora que Rey dice se contrató para robustecer a Ueno.", P(21, "para. 2"), ["Mckenize"])
ent("org:estancia-don-miguel", C, "Estancia Don Miguel (Ganadera del Grupo Vázquez)", "Group ranch said to buy fodder from Peña Palacios, per Rey.", "Estancia del grupo que compraría forraje a Peña Palacios, según Rey.", P(23, "para. 4"))
ent("auth:bcp", A, "Banco Central del Paraguay", "Central bank; ordered resolution on 2 Nov 2026.", "Banco central; dispuso la resolución el 02/11/2026.", P(1, "para. 5"), ["BCP"])
ent("auth:superintendencia-de-bancos", A, "Superintendencia de Bancos", "Bank supervisor whose analysis underlies the charges.", "Supervisor bancario cuyo análisis sustenta la imputación.", P(2, "para. 3"))
ent("auth:ministerio-publico", A, "Ministerio Público, Unidad Especializada de Delitos Económicos y Anticorrupción", "Prosecuting authority.", "Autoridad que investiga.", P(1, "header"))

def per(id, label, de, ds, page, loc, by=None, conf="high", note="", aliases=None):
    ent(id, PE, label, de, ds, P(page, loc, by=by, conf=conf, note=note), aliases)

per("person:miguel-vazquez", "Federico Miguel Vázquez Villasanti", "Bank director; ultimate beneficial owner of Ueno; head of Grupo Vázquez per Rey.",
    "Director del banco; beneficiario final de Ueno; cabeza del Grupo Vázquez según Rey.", 1, "para. 4",
    note="Caption on every page reads 'Vazquez Velazquez'.", aliases=["Miguel Vázquez", "MV", "Federico Miguel Vazquez Velazquez"])
per("person:juan-manuel-gustale", "Juan Manuel Gustale", "Bank director named in the charges.", "Director del banco nombrado en la imputación.", 1, "para. 4", aliases=["Juan Gustale"])
per("person:julio-rey", "Julio Daniel Rey Fernández", "Bank director until July 2026; gives this statement.", "Director del banco hasta julio de 2026; presta esta declaración.", 1, "para. 1")
per("person:diana-mongelos", "Diana Leticia Mongelos González", "Bank director named in the charges.", "Directora del banco nombrada en la imputación.", 1, "para. 4")
per("person:mariana-torres", "Mariana Torres Rubiani", "Bank director named in the charges.", "Directora del banco nombrada en la imputación.", 1, "para. 4")
per("person:alejandro-gomez-abente", "Alejandro Gómez Abente", "Bank director named in the charges.", "Director del banco nombrado en la imputación.", 1, "para. 4")
per("person:diego-duarte", "Diego Fernando Duarte Schussmuller", "Bank director named in the charges.", "Director del banco nombrado en la imputación.", 1, "para. 4")
per("person:miguel-angel-almada", "Miguel Ángel Almada Frutos", "Statutory auditor (síndico) of the bank, named in the charges.", "Síndico del banco, nombrado en la imputación.", 1, "para. 4")
ppl = [("jose-augusto-sala-cardozo", "José Augusto Sala Cardozo", 4, "MOWI table row 1"), ("sergio-pizurno", "Sergio Pizurno", 4, "MOWI table row 2"),
       ("vanessa-godoy", "Vanessa Godoy", 6, "Hendy table row 2"), ("oscar-urdapilleta", "Oscar Urdapilleta", 6, "Hendy table row 3"),
       ("cesar-mengual", "César Javier Mengual Mazacotte", 6, "Hendy table row 4"), ("miguel-angel-garay", "Miguel Ángel Garay", 7, "Hendy table last row"),
       ("cesar-astigarraga", "César Astigarraga", 9, "Grupo M table"), ("luis-ernesto-angulo", "Luis Ernesto Angulo", 9, "Grupo M table"),
       ("guillermo-vazquez", "Guillermo Vázquez", 9, "Grupo M table"), ("paola-meza", "Paola Meza", 9, "Grupo M table"),
       ("diego-gomez", "Diego Gómez", 9, "Grupo M table"), ("luis-fernando-rios", "Luis Fernando Ríos", 12, "TUIU table row 1"),
       ("andre-gayol-pires", "André Gayol Pires", 12, "TUIU table row 2"), ("nicolas-di-iorio", "Nicolás S. Di Iorio Olivares", 12, "TUIU table row 3"),
       ("rodrigo-franco", "Rodrigo Franco", 12, "TUIU table row 4"), ("mauro-vargas", "Mauro Vargas Wildberger", 14, "Franede table row 1"),
       ("cecilia-dominguez", "Cecilia Domínguez", 14, "Franede table row 2"), ("martin-vargas", "Martín Vargas Wildberger", 16, "AIME table row 1"),
       ("gloria-villasanti", "Gloria Villasanti", 16, "AIME table row 3"), ("raul-sanchez", "Raúl Sánchez", 16, "AIME table row 4")]
for s, n, pg, loc in ppl:
    per("person:" + s, n, "Listed in the record among persons in charge of a borrower company.",
        "Figura en el acta entre las personas a cargo de una empresa prestataria.", pg, loc)
per("person:marcelo-gimenez-recalde", "Marcelo Giménez Recalde", "Appears in the page 2 diagram (Hendy / Grupo M).", "Figura en el diagrama de la página 2 (Hendy / Grupo M).", 2, "diagram", conf="low", note="diagram small print")
per("person:rudolph-goetz", "Rudolph F. Goetz González", "Appears in the page 2 diagram (Hendy / Grupo M).", "Figura en el diagrama de la página 2 (Hendy / Grupo M).", 2, "diagram", conf="low", note="diagram small print")
per("person:lucca-de-barba", "Lucca de Barba", "Bank liquidity-area staff member who sent the 'Delirio Colectivo' email, per Rey.",
    "Colaborador del área de Liquidez que envió el correo 'Delirio Colectivo', según Rey.", 21, "para. 2")
per("person:ruben-gonzalez", "Rubén González", "Security director of the bank, per Rey.", "Director de Seguridad del banco, según Rey.", 22, "para. 2")
per("person:diana-jara", "Diana Jara", "Person who handled tenders in which Grupo Vázquez took part, per Rey.", "Persona que se encargaba de las licitaciones del Grupo Vázquez, según Rey.", 23, "last para.")
per("person:francisco-pena-palacios", "Francisco Peña Palacios", "Person to whom PEARL S.R.L. 'corresponds', per Rey.", "Persona a quien 'corresponde' PEARL S.R.L., según Rey.", 23, "para. 4")
per("person:guillermo-ferreiro", "Guillermo Ferreiro", "Defence lawyer of Julio Rey.", "Abogado defensor de Julio Rey.", 1, "para. 1")
per("person:luis-esteban-palau", "Luis Esteban Palau", "Defence lawyer of Julio Rey.", "Abogado defensor de Julio Rey.", 1, "para. 1")
for s, n in (("yeimy-adle", "Yeimy Adle"), ("luz-guerrero", "Luz Guerrero"), ("luis-lionel-pinanez", "Luis Lionel Piñanez")):
    per("person:" + s, n, "Prosecutor, Economic Crimes and Anti-Corruption Unit.", "Agente fiscal, Unidad de Delitos Económicos y Anticorrupción.", 1, "para. 1")

# ---------------- roles
def role(holder, org, r, page, loc, pct=None, start="", end="", ne="", ns="", by=None, conf="high", note="", quote=""):
    rows["roles"].append({"id": nid("role"), "holder": holder, "org": org, "role": r, "pct": pct, "start": start, "end": end,
        "note_en": ne, "note_es": ns, "prov": P(page, loc, by=by, quote=quote, conf=conf, note=note)})

UB, GV, MV = "org:ueno-bank", "org:grupo-vazquez", "person:miguel-vazquez"
for p_ in ("juan-manuel-gustale", "miguel-vazquez", "julio-rey", "diana-mongelos", "mariana-torres", "alejandro-gomez-abente", "diego-duarte"):
    role("person:" + p_, UB, "director", 1, "para. 4 (board list)", ne="Board member 2025-2026 said to have authorised the operations.",
         ns="Miembro del directorio 2025-2026 que habría autorizado las operaciones.")
    role("person:" + p_, UB, "charged_person", 1, "para. 4", ne="Named among those to whom the facts are attributed.", ns="Nombrado entre aquellos a quienes se atribuyen los hechos.")
role("person:miguel-angel-almada", UB, "statutory_auditor", 1, "para. 4", ne="Síndico.", ns="Síndico.")
role("person:miguel-angel-almada", UB, "charged_person", 1, "para. 4")
role(MV, UB, "beneficial_owner", 14, "Franede table row 1", ne="'BF de UENO'.", ns="'BF de UENO'.", quote="familiar de Miguel Vázquez (BF de UENO)")
# Rey's account of group roles
role("person:diana-mongelos", GV, "group_role", 21, "para. 1", ne="Corporate Human Talent director of the whole group.", ns="Directora de Talento Humano corporativa de todo el grupo.")
role("person:diana-mongelos", "org:itti", "director", 23, "para. 3", end="2026-07", ne="Stopped being ITTI director; stayed bank director.", ns="Deja de ser directora de ITTI; queda en el banco.")
role("person:diego-duarte", GV, "group_role", 21, "para. 1", ne="Director of Integral Risks and Fraud of the whole group; responsible for the 20-year feasibility plan.", ns="Director de Riesgos Integrales y Fraude de todo el grupo; responsable del plan de factibilidad.")
role("person:juan-manuel-gustale", GV, "group_role", 21, "para. 1", end="2026-07", ne="Legal Director of the whole group; later bank President, leaving the group.", ns="Director Jurídico de todo el grupo; luego Presidente del banco.")
role("person:juan-manuel-gustale", UB, "president", 23, "para. 3", start="2026-07", ne="Stays as President of the bank.", ns="Queda como Presidente del banco.")
role("person:mariana-torres", GV, "group_role", 21, "para. 1", ne="Finance Director of the whole group; left the bank board in the July 2026 separation.", ns="Directora Financiera de todo el grupo; deja el directorio del banco.")
role("person:alejandro-gomez-abente", GV, "group_role", 21, "para. 1", ne="In charge of international funding and shareholders.", ns="Encargado de obtención de fondos internacionales y accionistas.")
role("person:julio-rey", GV, "group_role", 21, "para. 1", ne="Operations Director of the Group (33 business units); says he was not the bank's operations director.", ns="Director Operativo del Grupo (33 unidades); dice que no lo era del banco.")
role("person:julio-rey", UB, "director", 23, "para. 1", start="2021", end="2026-07", ne="Financiera Ueno board 2021 to Jan 2024; Visión Banco board Jan-Jul 2024; Ueno Bank board Jul 2024 to Jul 2026.", ns="Directorio de Financiera Ueno 2021 a ene. 2024; Visión Banco ene.-jul. 2024; Ueno Bank jul. 2024 a jul. 2026.")
role(MV, GV, "controlling_group", 21, "para. 1", ne="'Main head and top decision-maker' of the bank board and the group.", ns="'Cabeza principal y máximo decisor' del directorio y del grupo.", quote="la cabeza principal y el máximo decisor")
role(MV, UB, "director", 23, "para. 3", ne="Only person remaining director of both bank and group after July 2026.", ns="Único director de banco y grupo tras julio de 2026.")
role("org:otp-bank", UB, "shareholder", 23, "para. 2", ne="Shareholder via 'U Luxemburgo' and its subsidiary 'U Paraguay'; negotiating an increase.", ns="Accionista vía 'U Luxemburgo' y su filial 'U Paraguay'; negociaba un aumento.")
role("person:lucca-de-barba", UB, "employee", 21, "para. 2", ne="Liquidity area.", ns="Área de Liquidez.")
role("person:ruben-gonzalez", UB, "officer", 22, "para. 2", ne="Security director.", ns="Director de Seguridad.")
role("person:diana-jara", GV, "employee", 23, "last para.", ne="Handled tenders.", ns="Se encargaba de las licitaciones.", conf="medium")
# MOWI
role("person:jose-augusto-sala-cardozo", "org:mowi", "beneficial_owner", 4, "MOWI table row 1", 90.0, "2025-09-19", ne="Shareholder / ultimate beneficial owner.", ns="Accionista / beneficiario final.")
role("person:jose-augusto-sala-cardozo", "org:mowi", "president", 4, "MOWI table row 1", start="2025-09-25", ne="President and legal representative.", ns="Presidente y representante legal.")
role("person:jose-augusto-sala-cardozo", UB, "officer", 4, "MOWI table row 1", end="2024-12-09", ne="Former deputy general manager and interim general manager.", ns="Ex subgerente general y gerente general interino.")
role("person:sergio-pizurno", "org:mowi", "beneficial_owner", 4, "MOWI table row 2", 10.0, "2025-09-19")
role("person:sergio-pizurno", "org:mowi", "vice_president", 4, "MOWI table row 2", start="2025-09-25")
role("person:sergio-pizurno", "org:grupo-m", "director", 9, "Grupo M table last row", start="2025-11-03")
role("person:vanessa-godoy", "org:mowi", "alternate_statutory_auditor", 6, "Hendy table row 2")
role("person:luis-ernesto-angulo", "org:mowi", "president", 9, "Grupo M table (link column)", ne="Former president of MOWI.", ns="Ex presidente de MOWI.")
role("person:luis-ernesto-angulo", "org:tuiu", "vice_president", 9, "Grupo M table (link column)", ne="Former VP of TUIU.", ns="Ex VP de TUIU.")
role("person:cesar-astigarraga", "org:mowi", "statutory_auditor", 2, "diagram", conf="low", note="diagram small print")
role(MV, "org:mowi", "vice_president", 2, "diagram", conf="low", note="diagram small print; period illegible")
role(MV, "org:grupo-m", "beneficial_owner", 2, "diagram", conf="low", note="diagram small print; reads as BF and president 2023-24")
role("org:itti", "org:mowi", "shareholder", 2, "diagram top box", end="2025-09", conf="medium", ne="Shareholder with Grupo Vázquez until Sep 2025; shares passed 19/09/2025.", ns="Accionista junto a Grupo Vázquez hasta sep. 2025.")
role(GV, "org:mowi", "shareholder", 2, "diagram top box", end="2025-09", conf="medium")
# HENDY
role("org:itti", "org:grupo-hendy", "shareholder", 6, "Hendy table row 1", end="2025-09-30", ne="Includes the loan of 26/09/2025.", ns="Incluye crédito del 26/09/2025.")
role(GV, "org:grupo-hendy", "shareholder", 6, "Hendy table row 1", end="2025-09-30")
role("person:vanessa-godoy", "org:grupo-hendy", "beneficial_owner", 6, "Hendy table row 2", 90.0, "2025-09-30")
role("person:vanessa-godoy", "org:grupo-hendy", "vice_president", 6, "Hendy table row 2", start="2025-11-04", end="2025-11-28")
role("person:vanessa-godoy", "org:grupo-hendy", "president", 6, "Hendy table row 2", start="2025-11-28")
role("person:oscar-urdapilleta", "org:grupo-hendy", "beneficial_owner", 6, "Hendy table row 3", 10.0, "2025-09-30")
role("person:oscar-urdapilleta", "org:grupo-hendy", "president", 6, "Hendy table row 3", start="2025-11-04", end="2025-11-28")
role("person:oscar-urdapilleta", "org:grupo-hendy", "vice_president", 6, "Hendy table row 3", start="2025-11-28")
role("person:oscar-urdapilleta", "org:redisa", "director", 6, "Hendy table row 3")
role("person:oscar-urdapilleta", "org:ueno-casa-de-bolsa", "director", 6, "Hendy table row 3")
role("person:oscar-urdapilleta", "org:itti", "employee", 6, "Hendy table row 3", quote="funcionario de ITTI")
role("person:cesar-mengual", "org:grupo-hendy", "president", 6, "Hendy table row 4", end="2025-11-04", ne="Minutes No. 1 of 26/04/2022.", ns="Acta N.º 1 del 26/04/2022.")
role("person:cesar-mengual", "org:grupo-m", "founder", 6, "Hendy table row 4")
role("person:miguel-angel-garay", "org:grupo-hendy", "director", 7, "table continuation", end="2025-11-04")
role("person:miguel-angel-garay", "org:grupo-m", "shareholder", 7, "table continuation", 4.51, ne="4.51% in 2024.", ns="4,51% en 2024.")
role("person:marcelo-gimenez-recalde", "org:grupo-hendy", "vice_president", 2, "diagram", conf="low", note="diagram small print")
role("person:marcelo-gimenez-recalde", "org:grupo-m", "statutory_auditor", 2, "diagram", conf="low", note="diagram small print; also shown as shareholder")
role("person:rudolph-goetz", "org:grupo-hendy", "alternate_director", 2, "diagram", conf="low", note="diagram small print")
role("person:rudolph-goetz", "org:grupo-m", "vice_president", 2, "diagram", conf="low", note="diagram small print; year reads 2024")
# GRUPO M
role("org:itti", "org:grupo-m", "shareholder", 8, "Grupo M table", end="2025-09-30", ne="Includes the loan of 26/09/2025.", ns="Incluye crédito del 26/09/2025.", note="Row sits in a table that also repeats MOWI and Hendy rows.")
role(GV, "org:grupo-m", "shareholder", 8, "Grupo M table", end="2025-09-30", note="Row sits in a table that also repeats MOWI and Hendy rows.")
role("person:cesar-astigarraga", "org:grupo-m", "president", 9, "Grupo M table", start="2025-07-30", end="2025-11-03")
role("person:cesar-astigarraga", UB, "alternate_statutory_auditor", 9, "Grupo M table", end="2026-03-27")
role("person:luis-ernesto-angulo", "org:grupo-m", "vice_president", 9, "Grupo M table", start="2025-07-30", end="2025-11-03")
role("person:guillermo-vazquez", "org:grupo-m", "director", 9, "Grupo M table", start="2025-07-30", end="2025-11-03")
role("person:guillermo-vazquez", GV, "related_group_member", 9, "Grupo M table", quote="Vinculado al GPV-1535")
role("person:paola-meza", "org:grupo-m", "alternate_director", 9, "Grupo M table", start="2025-07-30", end="2025-11-03")
role("person:oscar-urdapilleta", "org:grupo-m", "beneficial_owner", 9, "Grupo M table", 90.0, "2025-09-30")
role("person:oscar-urdapilleta", "org:grupo-m", "vice_president", 9, "Grupo M table", start="2025-11-03")
role("person:diego-gomez", "org:grupo-m", "beneficial_owner", 9, "Grupo M table", 10.0, "2025-09-30")
role("person:diego-gomez", "org:grupo-m", "president", 9, "Grupo M table", start="2025-11-03")
# TUIU
role("person:luis-fernando-rios", "org:tuiu", "beneficial_owner", 12, "TUIU table row 1", 50.0, "2025-08-28")
role("person:luis-fernando-rios", "org:tuiu", "vice_president", 12, "TUIU table row 1", start="2025-08-28")
role("person:luis-fernando-rios", "org:technoma", "director", 12, "TUIU table row 1", ne="Director and signatory.", ns="Director titular y firmante.")
role("person:luis-fernando-rios", "org:bankitti", "employee", 12, "TUIU table row 1", quote="\"funcionario\" en Bankitti")
role("person:luis-fernando-rios", "org:aime", "director", 12, "TUIU table row 1", ne="Former director.", ns="Ex director.")
role("person:andre-gayol-pires", "org:tuiu", "beneficial_owner", 12, "TUIU table row 2", 40.0, "2024-11-28")
role("person:andre-gayol-pires", "org:discover-paraguay", "employee", 12, "TUIU table row 2")
role("person:nicolas-di-iorio", "org:tuiu", "beneficial_owner", 12, "TUIU table row 3", 10.0, "2024-11-28")
role("person:rodrigo-franco", "org:tuiu", "president", 12, "TUIU table row 4", start="2025-08-28", ne="President and legal representative (Minutes No. 6).", ns="Presidente y representante legal (Acta N.º 6).")
role("person:rodrigo-franco", "org:kaitel", "employee", 12, "TUIU table row 4")
role("person:rodrigo-franco", "org:mulair", "vice_president", 12, "TUIU table row 4", ne="VP and signatory.", ns="VP y firmante.")
role("org:itti", "org:tuiu", "shareholder", 10, "diagram arrow note", 50.0, end="2025-08-28", conf="low", note="diagram small print: ITTI sells its 50% to L. F. Ríos on 28/08/2025")
role("person:miguel-angel-almada", "org:tuiu", "statutory_auditor", 10, "diagram", conf="low", note="diagram small print; year reads 2024")
role("person:miguel-angel-almada", "org:aime", "statutory_auditor", 10, "diagram", conf="low", note="diagram small print; year reads 2025")
role("person:cesar-astigarraga", "org:tuiu", "president", 10, "diagram", conf="low", note="diagram small print; 2024-25, shown jointly with L. E. Angulo")
# FRANEDE
role("person:mauro-vargas", "org:franede", "beneficial_owner", 14, "Franede table row 1", 99.62, "2025-06-30")
role("person:mauro-vargas", "org:franede", "president", 14, "Franede table row 1", start="2025-06-04")
role("person:mauro-vargas", GV, "employee", 14, "Franede table row 1", quote="Funcionario del grupo")
role("person:mauro-vargas", MV, "relative_of", 14, "Franede table row 1", quote="familiar de Miguel Vázquez (BF de UENO)")
role("person:mauro-vargas", MV, "relative_of", 16, "AIME table row 2", ne="Second degree of affinity.", ns="2.º grado de afinidad.", quote="Pariente en 2° grado de afinidad del BF de UENO")
role("person:cecilia-dominguez", "org:franede", "vice_president", 14, "Franede table row 2", start="2025-06-04", ne="Minutes No. 77.", ns="Acta N.º 77.")
role("person:cecilia-dominguez", "org:terravaz", "alternate_director", 14, "Franede table row 2")
role(GV, "org:franede", "shareholder", 10, "diagram arrow note", 99.6, end="2025-06-30", conf="low", note="diagram small print: Grupo Vázquez sells 99.6% to M. Vargas; same day loans USD 10 M and Gs. 95,000 M")
# AIME
role("person:martin-vargas", "org:aime", "shareholder", 16, "AIME table row 1", 95.65, "2026-01-27")
role("person:martin-vargas", MV, "relative_of", 16, "AIME table row 1", ne="Second degree of affinity.", ns="2.º grado de afinidad.", quote="Pariente en 2° grado de afinidad del BF de UENO")
role("person:mauro-vargas", "org:aime", "shareholder", 16, "AIME table row 2", 4.35, "2026-01-27", ne="Previously 98.91%.", ns="Antes 98,91%.")
role("person:gloria-villasanti", "org:aime", "president", 16, "AIME table row 3", start="2025-05-09")
role("person:gloria-villasanti", GV, "related_group_member", 16, "AIME table row 3", quote="Incluida en el GPV-1535")
role("person:gloria-villasanti", MV, "relative_of", 16, "AIME table row 3", ne="'Would be' a first-degree blood relative (conditional in the record).", ns="'Sería' pariente en 1.er grado de consanguinidad.", conf="medium", quote="sería pariente en 1° grado de consanguinidad")
role("person:raul-sanchez", "org:aime", "director", 16, "AIME table row 4", start="2025-12-29", ne="Minutes No. 22.", ns="Acta N.º 22.")
# related group membership of companies
for o, pg, loc in (("org:itti", 6, "Hendy table row 1"), ("org:vinanzas", 17, "diagram col. 4"), ("org:redisa", 7, "para. on overdrafts"), ("org:redipro", 7, "para. on overdrafts"), ("org:kaitel", 7, "para. 'Los créditos desembolsados'")):
    role(o, GV, "related_group_member", pg, loc, ne="Related group GPV-1535.", ns="Grupo vinculado GPV-1535.", conf="medium" if pg == 17 else "high")
for o in ("org:terravaz", "org:discover-paraguay"):
    role(o, GV, "related_group_member", 14 if o == "org:terravaz" else 12, "link column", quote="(vinculada)")
# shared infrastructure (diagram)
for o in ("org:mowi", "org:grupo-hendy", "org:grupo-m", "org:tuiu", "org:franede", "org:aime"):
    role("org:itti", o, "officer", 2 if o in ("org:mowi", "org:grupo-hendy", "org:grupo-m") else 10, "diagram centre box", conf="low",
         ne="12 identical home-banking operators on the account, described as ITTI employees.", ns="12 operadores de home banking idénticos, funcionarios de ITTI.", note="diagram small print")

# ---------------- loans
def loan(borrower, op, kind, date, cur, principal, outstanding, status, page, loc, ty=None, td=None, rate=None, coll="none", amort="", ne="", ns="", conf="high", note=""):
    i = nid("loan")
    rows["loans"].append({"id": i, "lender": UB, "borrower": borrower, "op_number": op, "kind": kind, "date": date, "term_years": ty,
        "term_days": td, "rate_pct": rate, "currency": cur, "principal": principal, "outstanding": outstanding, "collateral": coll,
        "amortisation": amort, "status": status, "note_en": ne, "note_es": ns, "prov": P(page, loc, conf=conf, note=note, quote="ASF" if coll == "none" and kind == "loan" else "")})
    return i
O, X = "outstanding", "cancelled"
L = {}
L["m1"] = loan("org:mowi", "612561002344", "loan", "2025-09-26", "USD", 12500000, 12500000, O, 3, "MOWI table row 1", 10, rate=8.0, amort="annual k+i")
L["m2"] = loan("org:mowi", "612561002656", "loan", "2025-10-30", "USD", 5400000, 5400000, O, 3, "MOWI table row 2", 7, rate=8.0, amort="annual k+i")
loan("org:mowi", "612561002893", "loan", "2025-12-29", "PYG", 33500000000, 0, X, 3, "MOWI table row 3", 7, rate=12.5, amort="annual k+i")
L["m4"] = loan("org:mowi", "612661003859", "loan", "2026-04-24", "USD", 5366645.18, 5366645.18, O, 3, "MOWI table row 4", 7, rate=8.0, amort="annual k+i")
loan("org:mowi", "614261687", "overdraft", "2026-01-02", "PYG", 105090000000, 0, X, 3, "MOWI table row 5", amort="revolving")
loan("org:mowi", "614261687", "overdraft", "2026-02-02", "PYG", 100500000000, 100500000000, O, 3, "MOWI table row 6", rate=24.15, amort="revolving")
loan("org:grupo-hendy", "612561002345", "loan", "2025-09-26", "PYG", 91334400000, 0, X, 4, "Hendy table row 1", 8, rate=12.5, amort="annual", ne="Only loan with a recorded amortisation; repaid with REDIPRO funds originating at ITTI.", ns="Única operación con amortización; pagada con fondos de REDIPRO originados en ITTI.")
L["h2"] = loan("org:grupo-hendy", "612561002654", "loan", "2025-10-30", "USD", 5075250, 5075250, O, 4, "Hendy table row 2", 10, rate=8.0, amort="annual")
L["h3"] = loan("org:grupo-hendy", "612561002900", "loan", "2025-12-29", "USD", 5527500, 5527500, O, 4, "Hendy table row 3 (continues p5)", 10, rate=7.5, amort="annual")
loan("org:grupo-hendy", "614275822", "overdraft", "2026-02-02", "PYG", 99587231967, 99587231967, O, 5, "Hendy table row 4", rate=24.15, coll="not stated", amort="revolving")
L["h5"] = loan("org:grupo-hendy", "612661003878", "loan", "2026-04-27", "USD", 14627989.28, 14627989.28, O, 5, "Hendy table row 5", 8, rate=8.0, amort="annual")
L["g1"] = loan("org:grupo-m", "612561002346", "loan", "2025-09-26", "USD", 13567500, 13567500, O, 7, "Grupo M table row 1", 7, rate=8.0, amort="annual")
L["g2"] = loan("org:grupo-m", "612561002664", "loan", "2025-10-31", "USD", 4321500, 4321500, O, 7, "Grupo M table row 2", 8, rate=8.0, amort="annual", ne="First instalment paid 29/04/2026 with ITTI funds.", ns="Primera cuota pagada el 29/04/2026 con fondos de ITTI.")
L["g3"] = loan("org:grupo-m", "612561002897", "loan", "2025-12-29", "USD", 5326500, 5326500, O, 7, "Grupo M table row 3", 8, rate=7.5, amort="annual")
loan("org:grupo-m", "614261689", "overdraft", "2026-01-02", "PYG", 55970014590, 55970014590, O, 7, "Grupo M table row 4", coll="not stated", amort="revolving")
loan("org:grupo-m", "614261690", "overdraft", "2026-01-02", "USD", 6305659.87, 6305659.87, O, 7, "Grupo M table row 5", coll="not stated", amort="revolving")
loan("org:tuiu", "612561002080", "loan", "2025-08-29", "USD", 10050000, 10050000, O, 11, "TUIU table row 1", 10, rate=8.0, amort="annual k+i")
loan("org:tuiu", "612561002665", "loan", "2025-10-31", "USD", 5376750, 5376750, O, 11, "TUIU table row 2", 7, rate=8.0, amort="annual k+i")
loan("org:tuiu", "612561002892", "loan", "2025-12-29", "USD", 5226000, 5226000, O, 11, "TUIU table row 3", 7, rate=7.5, amort="annual k+i")
loan("org:tuiu", "614261691", "overdraft", "2026-01-02", "USD", 10000000, 10000000, O, 11, "TUIU table row 4", rate=10.51, amort="annual k+i (as printed)")
loan("org:tuiu", "614194019", "overdraft", "2026-01-02", "PYG", 57500000000, 0, X, 11, "TUIU table row 5", amort="revolving", ne="Repaid 30/01/2026 with REDIPRO funds from Vinanzas.", ns="Amortizado el 30/01/2026 con fondos de REDIPRO provenientes de Vinanzas.")
loan("org:tuiu", "614261792", "overdraft", "2026-02-03", "PYG", 87100000000, 87100000000, O, 11, "TUIU table row 6", rate=24.15, amort="revolving")
MC = "mortgage_claimed"
fn = "Bank reported mortgage collateral; the commitment letter was not valid and was later excluded."
fs = "El banco reportó garantía hipotecaria; la carta de compromiso no era válida y luego se excluyó."
loan("org:franede", "612561001554", "loan", "2025-06-30", "USD", 10000000, 0, X, 13, "Franede table row 1", 10, rate=8.0, coll=MC, amort="annual k+i", ne=fn, ns=fs)
loan("org:franede", "612561001555", "loan", "2025-06-30", "PYG", 95000000000, 0, X, 13, "Franede table row 2", 8, rate=12.0, coll=MC, amort="annual k+i", ne=fn, ns=fs)
loan("org:franede", "612561002073", "loan", "2025-08-28", "USD", 24900000, 25024500, O, 13, "Franede table row 3", 10, rate=8.0, coll=MC, amort="annual k+i", ne=fn, ns=fs, note="Outstanding printed above principal (25.024.500 vs 24.900.000).")
loan("org:franede", "612561002362", "loan", "2025-09-30", "PYG", 65000000000, 0, X, 13, "Franede table row 4", 10, rate=12.5, coll=MC, amort="annual k+i", ne=fn, ns=fs)
loan("org:franede", "612661003607", "loan", "2026-03-27", "USD", 10593000, 10645965, O, 13, "Franede table row 5", 10, rate=8.5, coll=MC, amort="annual k+i", ne=fn, ns=fs)
loan("org:franede", "612661003890", "loan", "2026-04-28", "USD", 15336437.83, 15413120, O, 13, "Franede table row 6", 7, rate=8.0, coll=MC, amort="annual k+i", ne=fn, ns=fs)
loan("org:franede", "614210810", "overdraft", "2025-07-21", "PYG", None, None, O, 13, "Franede table row 7", coll="not stated", amort="revolving", note="No amounts printed.")
loan("org:aime", "612661003123", "loan", "2026-01-30", "USD", 6815000, 0, X, 15, "AIME table row 1", td=30, rate=7.0, amort="principal + interest at maturity", note="Term printed as '30', presumably days.")
loan("org:aime", "612661003124", "loan", "2026-01-30", "PYG", 133665000000, 0, X, 15, "AIME table row 2", td=30, rate=12.5, amort="principal + interest at maturity")
loan("org:aime", "612661003412", "loan", "2026-03-04", "PYG", 64923000000, 0, X, 15, "AIME table row 3", td=90, rate=12.5, amort="principal + interest at maturity")
loan("org:aime", "614296500", "overdraft", "2026-04-10", "USD", 11000000, 0, X, 15, "AIME table row 4", coll="not stated", amort="revolving")
loan("org:aime", "614296500", "overdraft", "2026-05-19", "USD", 7230000, 7230000, O, 15, "AIME table row 5", coll="not stated", amort="revolving")
loan("org:aime", "614296528", "overdraft", "2026-05-04", "PYG", 52364312369, 52364312369, O, 15, "AIME table row 6", coll="not stated", amort="revolving")
dg = "diagram small print"
J = {}
J["satec"] = loan("org:satec", "", "loan", "2026-06-15", "USD", 20000000, None, O, 17, "diagram col. 2", conf="medium", note="diagram; no terms given")
J["hd"] = loan("org:hd-invest", "", "loan", "2026-06-15", "USD", 35000000, None, O, 17, "diagram col. 2", conf="medium", note="diagram; no terms given")
J["tech"] = loan("org:technoma", "", "loan", "2026-06-11", "USD", 10000000, None, O, 17, "diagram col. 2", conf="medium", note="diagram; no terms given")
J["tropa"] = loan("org:la-tropa-fletes", "", "loan", "2026-06-11", "USD", 10000000, None, O, 17, "diagram col. 2", conf="low", note=dg + "; loan number partly legible (61266100440x)")
J["fact"] = loan("org:factopar", "", "loan", "2026-06-15", "USD", 6841000, None, O, 17, "diagram col. 2", conf="low", note=dg + "; loan number partly legible (61266100441x)")

# ---------------- flows
def flow(fr, to, amount, cur, date, instr, pe, ps, page, loc, prec="day", linked="", approx=False, by=None, conf="high", note="", quote=""):
    rows["flows"].append({"id": nid("flow"), "from": fr, "to": to, "amount": amount, "currency": cur, "date": date, "date_precision": prec,
        "instrument": instr, "purpose_en": pe, "purpose_es": ps, "linked_loan": linked, "amount_is_approx": approx,
        "prov": P(page, loc, by=by, quote=quote, conf=conf, note=note)})
fw_e, fw_s = "Loan or overdraft money forwarded almost immediately; applied to overdrafts, invoices, cheques.", "Fondos del crédito o sobregiro transferidos casi de inmediato; aplicados a sobregiros, facturas, cheques."
for to in ("org:itti", "org:redisa", "org:redipro"):
    flow("org:mowi", to, None, "", "2025/2026", "transfer", fw_e, fw_s, 3, "last para.", prec="year", quote="transferidos en forma casi inmediata")
for to in ("org:redipro", "org:itti"):
    flow("org:grupo-hendy", to, None, "", "2026", "transfer", "Overdraft-line money forwarded; then channelled to REDIPRO and REDISA accounts at other banks via SIPAP.", "Fondos de sobregiro transferidos; luego canalizados a cuentas de REDIPRO y REDISA en otras entidades vía SIPAP.", 5, "para. 'En cuanto al destino'", prec="year")
for to in ("org:itti", "org:redisa"):
    flow("org:grupo-hendy", to, None, "", "2025/2026", "transfer", "Loan disbursements forwarded immediately; used to cover ITTI overdrafts and other Hendy obligations.", "Desembolsos transferidos de inmediato; cobertura de sobregiros de ITTI y otras obligaciones de Hendy.", 5, "para. 'Asimismo, los desembolsos'", prec="year")
flow("org:itti", "org:redipro", None, "", "", "transfer", "Funds later used to repay Hendy loan 612561002345; originated in SIPAP transfers from other banks and an overdraft line.", "Fondos luego usados para pagar el préstamo 612561002345 de Hendy; originados en SIPAP de otras entidades y un sobregiro.", 5, "para. 'Por otra parte'", prec="year")
flow("org:redipro", "org:grupo-hendy", None, "", "", "repayment", "Source of repayment of loan 612561002345.", "Origen del repago del préstamo 612561002345.", 5, "para. 'Por otra parte'", prec="year")
for fr in ("org:vinanzas", "org:redipro", "org:redisa", "org:itti"):
    flow(fr, "org:grupo-hendy", None, "", "2026", "repayment", "Funds for repayment of Hendy overdrafts, via SIPAP.", "Fondos para repago de sobregiros de Hendy, vía SIPAP.", 5, "last para.", prec="year")
for to in ("org:itti", "org:redisa", "org:kaitel"):
    flow("org:grupo-m", to, None, "USD", "2025", "transfer", "Loans of 26/09, 31/10 and 29/12/2025 forwarded in full.", "Créditos del 26/09, 31/10 y 29/12/2025 transferidos en su totalidad.", 7, "para. 'Los créditos desembolsados'", prec="year", quote="transferidos en su totalidad")
for to in ("org:itti", "org:redipro", "org:redisa"):
    flow("org:grupo-m", to, None, "", "2026", "transfer", "Overdrafts of Jan-May 2026 forwarded in full.", "Sobregiros de enero a mayo de 2026 transferidos en su totalidad.", 7, "last para.", prec="year")
flow("org:itti", "org:grupo-m", None, "", "2026-04-29", "repayment", "Source of first instalment of loan 612561002664 and amortisation of overdrafts 614261689 / 614261690.", "Origen de la primera cuota del crédito 612561002664 y de la amortización de los sobregiros.", 8, "para. 1", linked=L["g2"])
for to in ("org:itti", "org:redisa", "org:redipro"):
    flow("org:tuiu", to, None, "", "2025/2026", "transfer", fw_e, fw_s, 11, "para. after table", prec="year")
flow("org:redipro", "org:tuiu", None, "PYG", "2026-01-30", "repayment", "Repayment of overdraft on account 614194019 (dated 02/01/2026).", "Amortización del sobregiro de la cuenta 614194019 (del 02/01/2026).", 11, "last para.")
flow("org:vinanzas", "org:redipro", None, "", "2026-01", "transfer", "Funds that REDIPRO used to repay TUIU's overdraft.", "Fondos que REDIPRO usó para amortizar el sobregiro de TUIU.", 11, "last para.", prec="month")
for fr in ("org:redisa", "org:redipro", "org:itti"):
    flow(fr, "org:vinanzas", None, "", "2026-01", "cheque", "72-hour cheques on other banks deposited to fund Vinanzas's account.", "Cheques 72 hs cargo otros bancos depositados para fondear la cuenta de Vinanzas.", 11, "last para.", prec="month")
for to in ("org:vinanzas", "org:grupo-vazquez"):
    flow("org:franede", to, None, "", "2025/2026", "transfer", "Loan disbursements forwarded; used for invoices and to cancel or reduce overdrafts of related companies.", "Desembolsos transferidos; pago de facturas y cancelación o reducción de sobregiros de vinculadas.", 13, "last para. (continues p14)", prec="year")
for fr in ("org:vinanzas", "org:grupo-vazquez"):
    flow(fr, "org:franede", None, "", "2025/2026", "repayment", "Funds for amortisations and cancellations; originated mainly in overdrafts and 72-hour cheques of group companies.", "Fondos para amortizaciones y cancelaciones; originados en sobregiros y cheques a 72 horas de sociedades del grupo.", 14, "para. 3", prec="year")
for to in ("org:itti", "org:grupo-vazquez", "org:redisa"):
    flow("org:aime", to, None, "", "2026", "transfer", "Loan disbursements forwarded immediately or almost; applied to sundry debits, funding other accounts, cheques.", "Desembolsos transferidos en forma inmediata o casi; débitos varios, fondeo de otras cuentas, cheques.", 15, "para. 'Con relación al destino'", prec="year")
    flow(to, "org:aime", None, "", "2026", "repayment", "Loans later cancelled through transfers by the same companies.", "Créditos cancelados mediante transferencias de las mismas empresas.", 15, "para. 'Con relación al destino'", prec="year")
for to in ("org:itti", "org:redipro"):
    flow("org:aime", to, None, "", "2026", "transfer", "Overdrafts of 10/04, 04/05 and 19/05/2026 forwarded in full; part ended in bond purchases and 72-hour cheques at Zeta Banco.", "Sobregiros del 10/04, 04/05 y 19/05/2026 transferidos íntegramente; parte terminó en compras de bonos y cheques 72 hs en Zeta Banco.", 15, "last para. (continues p16)", prec="year")
# June 2026 circuit (p17 diagram)
D17 = "p17 diagram"
for k, b, amt, d in (("satec", "org:satec", 20000000, "2026-06-15"), ("hd", "org:hd-invest", 35000000, "2026-06-15"), ("tech", "org:technoma", 10000000, "2026-06-11"),
                     ("tropa", "org:la-tropa-fletes", 10000000, "2026-06-11"), ("fact", "org:factopar", 6841000, "2026-06-15")):
    flow(UB, b, amt, "USD", d, "loan_disbursement", "New Ueno loan (total of the five: USD 81,841,000).", "Nuevo préstamo de Ueno (total de los cinco: USD 81.841.000).", 17, D17, linked=J[k], conf="medium")
flow("org:satec", "org:vinanzas", 20000000, "USD", "2026-06-15", "transfer", "Labelled 'purchase of Vinanzas portfolio'.", "Rotulado 'compra de cartera de Vinanzas'.", 17, D17, linked=J["satec"], conf="medium")
flow("org:hd-invest", "org:vinanzas", 35000000, "USD", "2026-06-15", "transfer", "Labelled 'purchase of Vinanzas portfolio'.", "Rotulado 'compra de cartera de Vinanzas'.", 17, D17, linked=J["hd"], conf="medium")
lo = dict(conf="low", note=dg)
flow("org:technoma", "org:itti", 4230000, "USD", "2026-06", "bond_purchase", "Purchase of ITTI bonds.", "Compra de bonos de ITTI.", 17, D17, prec="month", linked=J["tech"], approx=True, **lo)
flow("org:technoma", "org:grupo-vazquez", 5770000, "USD", "2026-06", "bond_purchase", "Purchase of Grupo Vázquez bonds.", "Compra de bonos de Grupo Vázquez.", 17, D17, prec="month", linked=J["tech"], approx=True, **lo)
flow("org:la-tropa-fletes", "org:grupo-vazquez", 4215767.91, "USD", "2026-06", "bond_purchase", "Purchase of Grupo Vázquez bonds.", "Compra de bonos de Grupo Vázquez.", 17, D17, prec="month", linked=J["tropa"], conf="low", note=dg + "; digits read with moderate certainty")
flow("org:la-tropa-fletes", "org:kasas-propiedades", None, "USD", "2026-06", "bond_purchase", "Purchase of bonds (label partly illegible).", "Compra de bonos (rótulo parcialmente ilegible).", 17, D17, prec="month", linked=J["tropa"], **lo)
flow("org:factopar", "org:kasas-propiedades", None, "USD", "2026-06", "bond_purchase", "Purchase of Kasas bonds. Kasas box: bonds sold USD 10,049,628.97 in total.", "Compra de bonos Kasas. Recuadro Kasas: bonos vendidos por USD 10.049.628,97 en total.", 17, D17, prec="month", linked=J["fact"], **lo)
flow("org:la-tropa-fletes", "org:model", 2100000, "USD", "2026-06", "bond_purchase", "Purchase of Model bonds.", "Compra de bonos Model.", 17, D17, prec="month", linked=J["tropa"], approx=True, **lo)
flow("org:grupo-vazquez", "org:itti", 5770000, "USD", "2026-06", "transfer", "Transfer; ITTI box reads 'receives' about USD 10.0 million.", "Transferencia; el recuadro de ITTI dice 'recibe' unos USD 10,0 millones.", 17, D17, prec="month", approx=True, **lo)
flow("org:itti", "org:grupo-m", 6321524.00, "USD", "2026-06-15", "transfer", "Sent to Grupo M, which cancels an overdraft of about USD 6.3 million.", "Enviado a Grupo M, que cancela un sobregiro de unos USD 6,3 millones.", 17, D17, approx=True, **lo)
flow("org:itti", "org:vinanzas", 4474670.00, "USD", "2026-06-15", "loan", "Loan to Vinanzas.", "Préstamo a Vinanzas.", 17, D17, approx=True, **lo)
flow("org:grupo-vazquez", "org:vinanzas", 4215767.91, "USD", "2026-06-15", "loan", "Loan to Vinanzas.", "Préstamo a Vinanzas.", 17, D17, conf="low", note=dg + "; digits read with moderate certainty")
flow("org:kasas-propiedades", "org:vinanzas", 10049628.97, "USD", "2026-06-15", "contract", "Contract (label partly illegible).", "Contrato (rótulo parcialmente ilegible).", 17, D17, conf="low", note=dg + "; digits read with moderate certainty")
flow("org:model", "org:vinanzas", 2100000, "USD", "2026-06-15", "contract", "Contract.", "Contrato.", 17, D17, approx=True, **lo)
flow(UB, "org:vinanzas", 74418418.12, "USD", "2026-06-15", "portfolio_assignment", "Assignment without recourse of nine loans of MOWI, Grupo Hendy and Grupo M; contract of 15/06/2026.", "Cesión de cartera sin recurso de nueve créditos de MOWI, Grupo Hendy y Grupo M; contrato del 15/06/2026.", 17, D17 + "; text p17-18", quote="CESIÓN DE CARTERA sin recurso")
flow("org:vinanzas", UB, 74418418.12, "USD", "2026-06-15", "portfolio_sale_price", "Cash price of the portfolio. Vinanzas received about USD 76,061,604.13 that day; balance on 14/06/2026 read from the scan as about USD 93,628.", "Precio al contado de la cartera. Vinanzas recibió unos USD 76.061.604,13 ese día; saldo al 14/06/2026 leído del escaneo como unos USD 93.628.", 18, "para. 1 and total row", note="Balance figure is diagram small print; Última Hora (10 Nov 2026) prints USD 93,828.", quote="USD 74.418.418,12")
port = [("org:grupo-hendy", "612561002654", 5325536, "h2"), ("org:grupo-hendy", "612561002900", 5714905, "h3"), ("org:grupo-hendy", "612661003878", 14775471, "h5"),
        ("org:grupo-m", "612561002346", 14337688, "g1"), ("org:grupo-m", "612561002664", 4363176, "g2"), ("org:grupo-m", "612561002897", 5507090, "g3"),
        ("org:mowi", "612561002344", 13275637, "m1"), ("org:mowi", "612561002656", 5694633, "m2"), ("org:mowi", "612661003859", 5424281, "m4")]
for n, (b, op, amt, k) in enumerate(port, 1):
    flow(UB, "org:vinanzas", amt, "USD", "2026-06-15", "portfolio_assignment", "Portfolio item %d: loan %s of %s, promissory-note loan on signature alone, client category 1a." % (n, op, b.split(":")[1]),
         "Ítem %d de la cartera: crédito %s, préstamo c/ pagaré a sola firma, categoría 1a." % (n, op), 18, "portfolio table row %d" % n, linked=L[k])
# Rey's claims
R = dict(by="rey")
flow(MV, UB, 17000000, "USD", "2025-05", "cash_delivery", "Cash said to be brought at night in Vázquez's vehicle and counted by Treasury; booked in a Grupo Vázquez company as collections of unpaid loans.", "Efectivo que habría llegado de noche en el vehículo de Vázquez y contado por Tesorería; contabilizado en empresa del Grupo Vázquez como cobro de créditos impagos.", 22, "para. 2", prec="month", approx=True, conf="medium", note="Amount is hearsay: Rey says Lucca de Barba told him. Date 'approximately May 2025' sits oddly in a passage about Oct 2025-Mar 2026.", quote="unos diecisiete millones de dólares", **R)
flow(MV, UB, 17000000000, "PYG", "2025-05", "cash_delivery", "Guaraní part of the same cash delivery.", "Parte en guaraníes de la misma entrega de efectivo.", 22, "para. 2", prec="month", approx=True, conf="medium", note="Hearsay via Lucca de Barba.", quote="diecisiete mil millones de guaraníes", **R)
flow(GV, UB, None, "", "2025", "other", "Purchase of certificates of deposit (CDAs) by Grupo Vázquez, justified with the 'dead portfolio' receipts; several endorsed to Miguel Vázquez; intended in 2026 to capitalise the bank.", "Compra de CDA por el Grupo Vázquez, justificada con recibos de 'cartera muerta'; varios endosados a Miguel Vázquez; en 2026 se pretendía capitalizar el banco.", 22, "para. 2 (continues p23)", prec="year", conf="medium", **R)
flow(UB, "org:itti", None, "", "", "other", "Bank paid human-talent and technology expenses at ITTI, funded by related companies selling real estate and software (digital signature, Vitaldoc) to the bank.", "El banco pagaba gastos de talento humano y tecnología en ITTI, fondeado con ventas de inmuebles y software de las vinculadas al banco.", 22, "para. 1", prec="year", conf="medium", **R)
flow(UB, GV, 900000000, "USD", "", "other", "Aggregate of related and non-related loans used to defer expenses: about USD 300 M cashback and USD 300 M technology and other; remainder not broken down.", "Total de créditos vinculados y no vinculados para diferir gastos: unos USD 300 M reintegros y USD 300 M tecnología y otros; el resto sin desglose.", 22, "para. 1", prec="year", approx=True, conf="medium", note="Recipient is a set of firms (Grupo Hendy, Mowi, Grupo M, TUIU, Franede, Office Design, Henrichi, Model, Data Force, among others); Grupo Vázquez used as stand-in.", quote="unos novecientos millones de dólares", **R)
flow("org:pear-srl", UB, 2700000, "USD", "", "other", "Property sold to PEARL S.R.L. for USD 2.7-3.0 million (seller not stated; counterparty assumed).", "Inmueble vendido a PEARL S.R.L. por USD 2,7 a 3,0 millones (vendedor no indicado).", 23, "para. 4", prec="year", approx=True, conf="low", note="Range 2,700,000-3,000,000; lower bound recorded. The record does not say who sold; treat direction as uncertain.", **R)
flow(GV, "org:pear-srl", None, "USD", "", "other", "Instalments assumed by Grupo Vázquez through a supposed fodder payment to Estancia Don Miguel.", "Cuotas asumidas por el Grupo Vázquez mediante un supuesto pago de forraje a la Estancia Don Miguel.", 23, "para. 4", prec="year", conf="medium", quote="mediante un supuesto pago de forraje", **R)
flow("org:comitia", "org:itti", None, "", "", "other", "Payments to ITTI for the award of voting machines.", "Pagos a ITTI por la adjudicación de las máquinas de votación.", 23, "para. 5", prec="year", conf="medium", **R)

# ---------------- events
def ev(date, cat, te, ts, de, ds, parties, page, loc, prec="day", amount=None, cur="", by=None, conf="high", note="", quote=""):
    rows["events"].append({"id": nid("event"), "date": date, "date_precision": prec, "category": cat, "title_en": te, "title_es": ts,
        "detail_en": de, "detail_es": ds, "parties": parties, "amount": amount, "currency": cur, "prov": P(page, loc, by=by, quote=quote, conf=conf, note=note)})
# loans as credit events
names = {"org:mowi": "MOWI", "org:grupo-hendy": "Grupo Hendy", "org:grupo-m": "Grupo M", "org:tuiu": "TUIU", "org:franede": "FRANEDE", "org:aime": "AIME",
         "org:satec": "SATEC", "org:hd-invest": "HD Invest", "org:technoma": "Technoma", "org:la-tropa-fletes": "La Tropa Fletes", "org:factopar": "Factopar"}
for l in rows["loans"]:
    if l["principal"] is None:
        continue
    k = "Loan" if l["kind"] == "loan" else "Overdraft"; ks = "Préstamo" if l["kind"] == "loan" else "Sobregiro"
    rows["events"].append({"id": nid("event"), "date": l["date"], "date_precision": "day", "category": "credit",
        "title_en": "%s to %s" % (k, names[l["borrower"]]), "title_es": "%s a %s" % (ks, names[l["borrower"]]),
        "detail_en": "Operation %s; %s; %s." % (l["op_number"] or "n/a", "no collateral (signature only)" if l["collateral"] == "none" else l["collateral"], l["status"]),
        "detail_es": "Operación %s; %s; %s." % (l["op_number"] or "s/d", "a sola firma" if l["collateral"] == "none" else l["collateral"], "vigente" if l["status"] == O else "cancelada"),
        "parties": [UB, l["borrower"]], "amount": l["principal"], "currency": l["currency"], "prov": dict(l["prov"])})
Y = dict(by="rey")
ev("2019-04", "corporate", "Rey joins the group (Credicentro)", "Rey ingresa al grupo (Credicentro)", "Two-year contract to build the risk structure for the bank project.", "Contrato de dos años para armar la estructura de riesgos.", ["person:julio-rey", "org:credicentro"], 19, "last para.", prec="month", **Y)
ev("2020-01", "corporate", "Application to become a bank", "Solicitud para convertirse en banco", "Filed in January 2020; merger with credit houses during the pandemic.", "Presentada en enero de 2020; fusión con casas de crédito en la pandemia.", [GV, "auth:bcp"], 20, "para. 1", prec="month")
ev("2021", "corporate", "Purchase of Financiera El Comercio; Ueno model installed", "Compra de Financiera El Comercio; se instala el modelo Ueno", "Miguel Vázquez closes the purchase to obtain a licence; Rey joins the board of Financiera Ueno.", "Miguel Vázquez cierra la compra para acceder a licencia; Rey integra el directorio de Financiera Ueno.", [MV, "org:financiera-el-comercio", "person:julio-rey"], 20, "para. 1", prec="year")
ev("2024-01", "corporate", "Purchase of Visión Banco; Rey moves to its board", "Compra de Visión Banco; Rey pasa a su directorio", "Rey leaves the Ueno board for Visión Banco's, around January 2024.", "Rey sale del directorio de Ueno y pasa al de Visión Banco, aprox. enero de 2024.", ["org:vision-banco", "person:julio-rey", MV], 20, "para. 1", prec="month")
ev("2024-06", "supervisory", "20-year feasibility plan approved by the BCP", "Plan de factibilidad a 20 años aprobado por el BCP", "Prepared under Diego Duarte; dates from May or June 2024; contained the 'facilities' now questioned, including constant transactions among related companies.", "A cargo de Diego Duarte; de mayo o junio de 2024; contenía las 'facilidades' hoy cuestionadas.", ["person:diego-duarte", "auth:bcp", UB], 20, "para. 2", prec="month", quote="fue aprobado por el BCP")
ev("2024-07", "corporate", "Absorption of Visión Banco completed; Rey returns to Ueno board", "Se concreta la absorción de Visión Banco; Rey retoma el directorio de Ueno", "", "", ["org:vision-banco", UB, "person:julio-rey"], 20, "para. 1", prec="month")
ev("2024-12-09", "corporate", "Sala Cardozo ceases as Ueno deputy / interim general manager", "Sala Cardozo cesa como subgerente / gerente general interino de Ueno", "", "", ["person:jose-augusto-sala-cardozo", UB], 4, "MOWI table row 1", by="prosecution")
ev("2025-05", "statement", "Alleged night-time cash delivery to the bank", "Supuesto ingreso nocturno de efectivo al banco", "About USD 17 million and Gs. 17,000 million, per what Lucca de Barba told Rey; a day to count.", "Unos USD 17 millones y Gs. 17.000 millones, según lo que Lucca de Barba dijo a Rey; un día para contar.", [MV, UB, "person:ruben-gonzalez", "person:lucca-de-barba"], 22, "para. 2", prec="month", amount=17000000, cur="USD", conf="medium", note="Hearsay; date given as 'approximately May 2025'.")
ev("2025-05-09", "corporate", "Gloria Villasanti president of AIME", "Gloria Villasanti presidenta de AIME", "", "", ["person:gloria-villasanti", "org:aime"], 16, "AIME table row 3", by="prosecution")
ev("2025-06-04", "corporate", "Mauro Vargas president and Cecilia Domínguez VP of FRANEDE", "Mauro Vargas presidente y Cecilia Domínguez VP de FRANEDE", "Minutes No. 77.", "Acta N.º 77.", ["person:mauro-vargas", "person:cecilia-dominguez", "org:franede"], 14, "Franede table", by="prosecution")
ev("2025-06-30", "corporate", "FRANEDE shares pass to Mauro Vargas (99.62%)", "Las acciones de FRANEDE pasan a Mauro Vargas (99,62%)", "Diagram note: Grupo Vázquez sells 99.6%; same day loans of USD 10 M and Gs. 95,000 M.", "Nota de diagrama: Grupo Vázquez vende el 99,6%; el mismo día préstamos de USD 10 M y Gs. 95.000 M.", ["person:mauro-vargas", "org:franede", GV], 14, "Franede table row 1; p10 diagram", by="prosecution", note="Seller identified only in diagram small print.")
ev("2025-07-30", "corporate", "Astigarraga, Angulo, G. Vázquez, P. Meza take office at Grupo M", "Astigarraga, Angulo, G. Vázquez y P. Meza asumen en Grupo M", "In office until 03/11/2025.", "En funciones hasta el 03/11/2025.", ["person:cesar-astigarraga", "person:luis-ernesto-angulo", "person:guillermo-vazquez", "person:paola-meza", "org:grupo-m"], 9, "Grupo M table", by="prosecution")
ev("2025-08-28", "corporate", "L. F. Ríos takes 50% of TUIU; Rodrigo Franco president", "L. F. Ríos toma el 50% de TUIU; Rodrigo Franco presidente", "Diagram note: ITTI sells its 50%; TUIU's first loan follows on 29/08/2025.", "Nota de diagrama: ITTI vende su 50%; el primer crédito de TUIU es del 29/08/2025.", ["person:luis-fernando-rios", "person:rodrigo-franco", "org:tuiu", "org:itti"], 12, "TUIU table; p10 diagram", by="prosecution", note="Seller identified only in diagram small print.")
ev("2025-09-19", "corporate", "MOWI shares pass to Sala Cardozo (90%) and Pizurno (10%)", "Las acciones de MOWI pasan a Sala Cardozo (90%) y Pizurno (10%)", "Officers from 25/09/2025; first loan 26/09/2025.", "Cargos desde el 25/09/2025; primer crédito el 26/09/2025.", ["person:jose-augusto-sala-cardozo", "person:sergio-pizurno", "org:mowi"], 4, "MOWI table", by="prosecution")
ev("2025-09-30", "corporate", "Hendy and Grupo M shares pass from ITTI and Grupo Vázquez to individuals", "Las acciones de Hendy y Grupo M pasan de ITTI y Grupo Vázquez a personas físicas", "Hendy: Godoy 90%, Urdapilleta 10%. Grupo M: Urdapilleta 90%, Diego Gómez 10%. Four days after the loans of 26/09/2025.", "Hendy: Godoy 90%, Urdapilleta 10%. Grupo M: Urdapilleta 90%, Diego Gómez 10%. Cuatro días después de los créditos del 26/09/2025.", ["org:grupo-hendy", "org:grupo-m", "org:itti", GV, "person:vanessa-godoy", "person:oscar-urdapilleta", "person:diego-gomez"], 6, "Hendy table rows 1-3; p9 Grupo M table", by="prosecution")
ev("2025-10", "supervisory", "Bank asks to de-list MOWI, Hendy and Grupo M as related parties", "El banco solicita dar de baja a MOWI, Hendy y Grupo M como vinculadas", "No supporting documentation sent; no formal reply from the supervisor; lending continued.", "Sin documentación de respaldo; sin respuesta formal del supervisor; los créditos continuaron.", [UB, "auth:superintendencia-de-bancos", "org:mowi", "org:grupo-hendy", "org:grupo-m"], 2, "para. 2-4", prec="month", by="prosecution", quote="desvinculación sería meramente documental")
ev("2025-10-13", "statement", "'Delirio Colectivo' email", "Correo 'Delirio Colectivo'", "From Lucca de Barba to Mariana Torres and Rey, with a 20-page attachment on the bank's real liquidity channels; says it was discussed with Miguel Vázquez.", "De Lucca de Barba a Mariana Torres y Rey, con adjunto de 20 páginas sobre los canales reales de liquidez; dice que fue conversado con Miguel Vázquez.", ["person:lucca-de-barba", "person:mariana-torres", "person:julio-rey", MV], 21, "para. 2", quote="Delirio colectivo")
ev("2025-11-03", "corporate", "New officers at Grupo M (Gómez president, Urdapilleta VP, Pizurno director)", "Nuevas autoridades en Grupo M (Gómez presidente, Urdapilleta VP, Pizurno director)", "", "", ["org:grupo-m", "person:diego-gomez", "person:oscar-urdapilleta", "person:sergio-pizurno"], 9, "Grupo M table", by="prosecution")
ev("2025-11-04", "corporate", "Mengual and Garay leave Hendy; Urdapilleta president, Godoy VP", "Mengual y Garay dejan Hendy; Urdapilleta presidente, Godoy VP", "Positions swap on 28/11/2025.", "Los cargos se invierten el 28/11/2025.", ["org:grupo-hendy", "person:cesar-mengual", "person:miguel-angel-garay", "person:oscar-urdapilleta", "person:vanessa-godoy"], 6, "Hendy table", by="prosecution")
ev("2025-12-29", "corporate", "Raúl Sánchez director of AIME", "Raúl Sánchez director titular de AIME", "Minutes No. 22.", "Acta N.º 22.", ["person:raul-sanchez", "org:aime"], 16, "AIME table row 4", by="prosecution")
ev("2026-01-27", "corporate", "AIME shares: Martín Vargas 95.65%, Mauro Vargas 4.35%", "Acciones de AIME: Martín Vargas 95,65%, Mauro Vargas 4,35%", "Mauro Vargas previously 98.91%. First AIME loans on 30/01/2026.", "Mauro Vargas antes 98,91%. Primeros créditos de AIME el 30/01/2026.", ["person:martin-vargas", "person:mauro-vargas", "org:aime"], 16, "AIME table rows 1-2", by="prosecution")
ev("2026-01-30", "credit", "TUIU overdraft repaid with REDIPRO money that came from Vinanzas", "Sobregiro de TUIU amortizado con fondos de REDIPRO provenientes de Vinanzas", "Vinanzas account funded with 72-hour cheques of REDISA, REDIPRO and ITTI.", "Cuenta de Vinanzas fondeada con cheques 72 hs de REDISA, REDIPRO e ITTI.", ["org:tuiu", "org:redipro", "org:vinanzas"], 11, "last para.", by="prosecution")
ev("2026-03-27", "corporate", "Astigarraga ceases as alternate statutory auditor of Ueno Bank", "Astigarraga cesa como síndico suplente de Ueno Bank", "", "", ["person:cesar-astigarraga", UB], 9, "Grupo M table", by="prosecution")
ev("2026-04-29", "credit", "First instalment of Grupo M loan 612561002664 paid with ITTI money", "Primera cuota del crédito 612561002664 de Grupo M pagada con fondos de ITTI", "", "", ["org:grupo-m", "org:itti"], 8, "para. 1", by="prosecution")
ev("2026-06-14", "credit", "Vinanzas lacks own funds the day before the purchase", "Vinanzas no contaba con recursos propios el día previo a la compra", "Superintendency finding; diagram balance read as about USD 93,628.", "Hallazgo de la Superintendencia; saldo en el diagrama leído como unos USD 93.628.", ["org:vinanzas", "auth:superintendencia-de-bancos"], 18, "last para.", by="prosecution", amount=93628, cur="USD", note="Balance from p17 diagram small print; Última Hora (10 Nov 2026) prints USD 93,828.")
ev("2026-06-15", "credit", "Ueno sells USD 74.4 million loan portfolio to Vinanzas", "Ueno vende a Vinanzas cartera por USD 74,4 millones", "Nine loans of MOWI, Hendy and Grupo M; documented as a cash sale; funds traced to Ueno loans of 11 and 15 June (USD 81,841,000).", "Nueve créditos de MOWI, Hendy y Grupo M; instrumentada como venta al contado; fondos rastreados a préstamos de Ueno del 11 y 15 de junio (USD 81.841.000).", [UB, "org:vinanzas", "org:mowi", "org:grupo-hendy", "org:grupo-m"], 17, "section D; p18 table", by="prosecution", amount=74418418.12, cur="USD", quote="operación prohibida")
ev("2026-07", "corporate", "Rey leaves the bank's board", "Rey sale del directorio del banco", "By extraordinary shareholders' meeting; he attributes it to OTP requiring separation of group and financial-ecosystem directorships. Mongelos leaves ITTI, Gustale becomes President, Torres leaves the bank board.", "Por asamblea extraordinaria; lo atribuye a que OTP exigía separar direcciones del grupo y del ecosistema financiero.", ["person:julio-rey", UB, "org:otp-bank", "person:diana-mongelos", "person:juan-manuel-gustale", "person:mariana-torres"], 23, "para. 1-3", prec="month", **Y)
ev("2026-11-02", "supervisory", "BCP orders resolution of Ueno Bank", "El BCP dispone la resolución de Ueno Bank", "Resolution No. 1; solvency ratio below 50% of the legal minimum (Law 2.334/03 art. 13 b).", "Resolución N.º 1; índice de solvencia por debajo del 50% del mínimo (Ley 2.334/03 art. 13 inc. b).", ["auth:bcp", UB], 1, "para. 5", by="prosecution", quote="por debajo del cincuenta por ciento (50%)")
ev("2026-11-04", "criminal", "Record of Rey's investigative statement", "Acta de declaración indagatoria de Rey", "Dated 4 Nov 2026, 11:00, Asunción. Offences cited: arts. 179, 192, 187, 181 of the Penal Code. Defence files CDA schedules, three receipts, the email and its attachment, and offers unrestricted cooperation.", "Fechada el 04/11/2026, 11:00, Asunción. Hechos punibles: arts. 179, 192, 187 y 181 del Código Penal. La defensa agrega planillas de CDA, tres boletas, el correo y su adjunto, y ofrece colaborar sin restricciones.", ["person:julio-rey", "auth:ministerio-publico", "person:guillermo-ferreiro", "person:luis-esteban-palau"], 1, "para. 1; p19 legal classification; p24", by="prosecution", note="Press (El Nacional, 19 Nov 2026) dates Rey's statement to 18 Nov 2026.")

# ---------------- issues
def iss(where, e, s, page, loc, by="prosecution"):
    rows["issues"].append({"id": nid("issue"), "where": where, "issue_en": e, "issue_es": s, "prov": P(page, loc, by=by, conf="high")})
iss("Caption, every page", "Lead suspect named 'Vazquez Velazquez' in the caption and 'Vázquez Villasanti' in the body.", "El principal investigado figura como 'Vazquez Velazquez' en la carátula y 'Vázquez Villasanti' en el cuerpo.", 1, "caption vs para. 4")
iss("Page 1", "Announces '3 groups' of irregular operations; four sections (A-D) follow.", "Anuncia '3 grupos' de operaciones; siguen cuatro apartados (A-D).", 1, "last para.")
iss("Page 17", "Refers to the 'superintendencia de seguros'; context indicates the Superintendency of Banks.", "Menciona la 'superintendencia de seguros'; el contexto indica la de Bancos.", 17, "section D para. 1")
iss("Pages 17-18", "Sale price in words 74,418,418; the nine listed loans sum to 74,418,417 before cents.", "Precio en letras 74.418.418; los nueve créditos suman 74.418.417 antes de centavos.", 18, "portfolio table total")
iss("Pages 8-9", "Grupo M officer table repeats rows belonging to MOWI and Hendy.", "La tabla de Grupo M repite filas de MOWI y Hendy.", 8, "Grupo M table")
iss("Page 13", "FRANEDE capital printed as Gs. 2.628.000.000.000, implausible beside monthly income of Gs. 872 million.", "Capital de FRANEDE impreso como Gs. 2.628.000.000.000, inverosímil frente a ingresos de Gs. 872 millones al mes.", 13, "para. after table")
iss("Page 13", "Outstanding balances of three FRANEDE USD loans exceed their principal.", "Los saldos de tres préstamos en USD de FRANEDE superan el capital.", 13, "Franede table rows 3, 5, 6")
iss("Page 15", "Opening sentence on AIME is garbled (debts 'cancelled only at Ueno' at April 2026 and outstanding at March 2026).", "La frase inicial sobre AIME está mal construida.", 15, "para. 1")
iss("Page 22", "Rey dates the cash delivery to about May 2025 within a passage on enquiries made from October 2025.", "Rey fecha el efectivo hacia mayo de 2025 dentro de un pasaje sobre averiguaciones desde octubre de 2025.", 22, "para. 2", by="rey")
iss("Loan tables", "Stated totals per borrower track outstanding balances, at exchange rates that differ between tables.", "Los totales por prestataria siguen los saldos vigentes, con tipos de cambio distintos entre tablas.", 3, "tables pp 3-15")
iss("Record date", "Record dated 4 Nov 2026; press reports place Rey's statement on 18 Nov 2026.", "Acta fechada el 04/11/2026; la prensa ubica la declaración de Rey el 18/11/2026.", 1, "para. 1")

# ---------------- write + validate
ids = {e["id"] for e in rows["entities"]}
srcs = {s["id"] for s in rows["sources"]}
bad = []
def chk(x, where):
    if x and (x.startswith("org:") or x.startswith("person:") or x.startswith("auth:")) and x not in ids:
        bad.append((where, x))
for r in rows["roles"]: chk(r["holder"], r["id"]); chk(r["org"], r["id"])
for r in rows["loans"]: chk(r["lender"], r["id"]); chk(r["borrower"], r["id"])
for r in rows["flows"]: chk(r["from"], r["id"]); chk(r["to"], r["id"])
for r in rows["events"]:
    for p_ in r["parties"]: chk(p_, r["id"])
for k, v in rows.items():
    with open(os.path.join(OUT, "rec.%s.jsonl" % k), "w", encoding="utf-8") as f:
        for r in v:
            if k != "sources":
                pr = r["prov"]
                assert set(pr) == {"asserted_by", "source", "locator", "quote", "confidence", "note"}, r["id"]
                assert pr["source"] in srcs and pr["asserted_by"] and pr["confidence"] in ("high", "medium", "low"), r["id"]
                assert len(pr["quote"].split()) <= 12, (r["id"], pr["quote"])
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    # re-parse
    n = sum(1 for line in open(os.path.join(OUT, "rec.%s.jsonl" % k), encoding="utf-8") if json.loads(line))
    print(k, n)
print("unknown entity refs:", bad)
