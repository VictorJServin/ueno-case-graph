#!/usr/bin/env python3
"""Writes site/data/payouts.json: the curated content of the 'Depositor payouts' view.
Every item points at rows that are already in data/raw (refs); the script fails if a ref does not exist,
so nothing on that view can be shown without provenance. No figure is computed here except the three
guaranteed-amount steps, which follow from the cap stated in the cited rows (75, 40 and 35 minimum wages).
"""
import glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ids = set()
for f in glob.glob(os.path.join(HERE, "raw", "*.jsonl")):
    for l in open(f, encoding="utf-8"):
        if l.strip(): ids.add(json.loads(l).get("id"))
def T(en, es): return {"en": en, "es": es}
C = "chrono:event:%04d"; D4 = "dos4:event:%04d"; D5 = "dos5:event:%04d"
P = {
 "as_of": "2026-11-25",
 "disclaimer": T("This view explains what has been reported about repayments. It is not advice and it is not an official notice: confirm your own case with the BCP or the deposit guarantee fund. Figures come from officials' statements as reported by the press and are shown as each source gave them.",
                 "Esta vista explica lo que se ha informado sobre los pagos. No es asesoramiento ni un aviso oficial: confirme su caso con el BCP o el Fondo de Garantía de Depósitos. Las cifras provienen de declaraciones de autoridades según la prensa y se muestran tal como las dio cada fuente."),
 "status": [
  {"k": T("Depositors covered", "Depositantes cubiertos"), "v": "97%", "d": "2026-11-22", "n": T("per BCP director Rivarola; the other 3% are above the cap or institutional", "según el director del BCP Rivarola; el 3% restante supera el tope o es institucional"), "refs": [D5 % 19]},
  {"k": T("People paid by the legal deadline", "Personas pagadas al vencimiento legal"), "v": "1,812,348", "d": "2026-11-11", "n": T("G. 3.9 trillion, about USD 644 million", "G. 3,9 billones, unos USD 644 millones"), "refs": [C % 179]},
  {"k": T("Guarantee fund used", "Fondo de garantía utilizado"), "v": T("about USD 644M of 1,663M", "unos USD 644M de 1.663M"), "d": "2026-11-20", "n": T("more than USD 1,000 million left, per the fund's director", "quedan más de USD 1.000 millones, según el director del fondo"), "refs": ["dos4:fact:0007", D4 % 9]},
  {"k": T("Certificates of deposit pending", "CDA pendientes"), "v": "3,975", "d": "2026-11-20", "n": T("about G. 221,000 million awaiting validation", "unos G. 221.000 millones a la espera de validación"), "refs": ["dos4:fact:0006", D4 % 9]},
  {"k": T("Next date", "Próxima fecha"), "v": T("2 Dec 2026", "2 dic 2026"), "d": "2026-11-21", "n": T("end of the 15-day extension to close the exclusion balance and tender the asset lots", "fin de la prórroga de 15 días para cerrar el balance de exclusión y licitar los lotes de activos"), "refs": [D5 % 13, C % 226]},
 ],
 "wage": {"monthly": 3044000, "note": T("One monthly minimum wage is about G. 3,044,000, which follows from the cap of 75 wages = G. 228.3 million in the cited rows.", "Un salario mínimo mensual equivale a unos G. 3.044.000, lo que se deduce del tope de 75 salarios = G. 228,3 millones en las filas citadas.")},
 "tiers": [
  {"id": "advance", "wages": [0, 40], "amount": T("up to G. 121.76 million", "hasta G. 121,76 millones"), "name": T("Advance under emergency Law 7745", "Adelanto por la Ley de emergencia 7745"),
   "rule": T("Paid by the deposit guarantee fund, starting within 24 hours of the law and taking up to five business days. An initial payment of up to G. 10 million, net of debts, came first.", "Pagado por el Fondo de Garantía, desde las 24 horas de la ley y en hasta cinco días hábiles. Antes hubo un primer pago de hasta G. 10 millones, neto de deudas."),
   "state": "done", "state_t": T("Complete, per the BCP (22 Nov). Some certificates of deposit are still being validated.", "Completado, según el BCP (22 nov). Algunos CDA siguen en validación."), "refs": [C % 100, C % 112, C % 73, D5 % 19]},
  {"id": "rest", "wages": [40, 75], "amount": T("the next G. 106.5 million, up to the cap of G. 228.3 million", "los siguientes G. 106,5 millones, hasta el tope de G. 228,3 millones"), "name": T("Rest of the guarantee (35 more wages)", "Resto de la garantía (35 salarios más)"),
   "rule": T("Two routes, per the BCP as reported by Hoy: if the asset lots are sold to other banks, the deposit moves in full to the buyer; if the sale fails, the guarantee fund pays the remaining 35 wages up to the cap.", "Dos caminos, según el BCP citado por Hoy: si los lotes de activos se venden a otros bancos, el depósito se traslada íntegro al comprador; si la venta fracasa, el Fondo de Garantía paga los 35 salarios restantes hasta el tope."),
   "state": "pending", "state_t": T("Pending the tender. No payment date has been reported.", "Pendiente de la licitación. No se informó fecha de pago."), "refs": [D5 % 13, C % 232]},
  {"id": "above", "wages": [75, None], "amount": T("anything above G. 228.3 million per person and institution", "todo lo que supere G. 228,3 millones por persona y entidad"), "name": T("Above the cap (not guaranteed)", "Por encima del tope (sin garantía)"),
   "rule": T("Not covered by the guarantee. Recovery depends on the exclusion balance: if the lots sell, deposits transfer in full, including public and pension funds; otherwise the amount above the cap becomes a claim on what the bank's assets yield.", "No está cubierto por la garantía. La recuperación depende del balance de exclusión: si los lotes se venden, los depósitos se trasladan íntegros, incluidos fondos públicos y jubilatorios; si no, lo que excede el tope queda como crédito sobre lo que rindan los activos del banco."),
   "state": "unknown", "state_t": T("Uncertain. About 3% of depositors, including institutions.", "Incierto. Cerca del 3% de los depositantes, incluidas instituciones."), "refs": [D5 % 13, D5 % 19, D5 % 52]},
 ],
 "outside": [
  {"k": T("Mutual funds (Ueno AFPISA)", "Fondos mutuos (Ueno AFPISA)"), "t": T("Not deposits, so not guaranteed. Each fund's assets are separate from the bank. Authorisation suspended for 180 days; about 30,000 investors and USD 46 million; the regulator is seeking a new manager. Each fund's securities remain in custody at the securities depository, and on 24 Nov the manager began asking unitholders whether they want to redeem once a procedure exists. On 25 Nov the central bank said, per 5Días, that Ueno AFPISA itself must set the redemption mechanism using the funds' own assets; investors' spokespeople said they were told the funds would be liquidated because no manager would take them, while the depository's manager spoke of a transfer of management and expected a definition within two weeks. These accounts conflict. Later on 25 Nov the securities regulator temporarily lifted the suspension, per 1000 Noticias: unit-holders of Ueno Cash Guaraníes and Ueno Cash Dólares may redeem up to G. 30 million per investor per week, with Investor Casa de Bolsa selling the funds' securities and acting as paying agent; payments are expected to start the following week, with no need to open an account at the broker. The regulator also called an assembly of unit-holders to decide whether the funds are liquidated.", "No son depósitos, por lo que no tienen garantía. El patrimonio de cada fondo está separado del banco. Autorización suspendida por 180 días; unos 30.000 inversores y USD 46 millones; el regulador busca un nuevo administrador. Los títulos de cada fondo siguen en custodia en la Caja de Valores, y el 24 nov la administradora empezó a consultar a los cuotapartistas si quieren rescatar cuando exista un procedimiento. El 25 nov el BCP señaló, según 5Días, que la propia Ueno AFPISA debe fijar el mecanismo de rescate con los activos de los fondos; voceros de los inversionistas dijeron que se les informó que los fondos serían liquidados porque ninguna administradora los asumió, mientras el gerente de la Caja de Valores habló de un traspaso de la administración y espera una definición en dos semanas. Estas versiones no coinciden. Más tarde el 25 nov la Superintendencia de Valores levantó temporalmente la suspensión, según 1000 Noticias: los cuotapartistas de Ueno Cash Guaraníes y Ueno Cash Dólares podrán rescatar hasta G. 30 millones por inversor por semana, con Investor Casa de Bolsa a cargo de vender los títulos de los fondos y actuar como agente de pago; los pagos comenzarían la semana siguiente, sin necesidad de abrir cuenta en la casa de bolsa. La Superintendencia también convocó una asamblea de cuotapartistas para decidir si los fondos se liquidan."), "refs": ["dos6:event:0019", "dos6:event:0025", C % 167, C % 141, "bot:event:0020", "bot:event:0021", "bot:event:0022", "bot:event:0024"]},
  {"k": T("Brokerage accounts (Ueno Casa de Bolsa)", "Cuentas bursátiles (Ueno Casa de Bolsa)"), "t": T("Suspended but not in resolution; since 24 Nov the depository must transfer a client's account to another depositary on the client's request, without the suspended broker.", "Suspendida pero no en resolución; desde el 24 nov la Caja de Valores debe traspasar la cuenta de un cliente a otro depositario a su pedido, sin la casa de bolsa suspendida."), "refs": ["dos6:event:0025", D4 % 10, C % 176]},
  {"k": T("Bonds issued by the bank or the group", "Bonos emitidos por el banco o el grupo"), "t": T("Not guaranteed. Bondholders are last in the order of payment; the guarantee fund recovers first, per BCP director Rivarola.", "Sin garantía. Los bonistas son los últimos en el orden de pago; el Fondo de Garantía recupera primero, según el director del BCP Rivarola."), "refs": [D5 % 51, D5 % 20, "dos6:event:0026"]},
 ],
 "schedule": [
  {"d": "2026-11-03", "s": "done", "t": T("Resolution announced; operations suspended; first payment of up to G. 10 million announced", "Se anuncia la resolución; operaciones suspendidas; se anuncia un primer pago de hasta G. 10 millones"), "refs": [C % 72, C % 73]},
  {"d": "2026-11-04", "s": "done", "t": T("Law 7745 promulgated: advance of up to 40 minimum wages", "Se promulga la Ley 7745: adelanto de hasta 40 salarios mínimos"), "refs": [C % 100]},
  {"d": "2026-11-05", "s": "done", "t": T("Advances begin", "Comienzan los adelantos"), "refs": [C % 112]},
  {"d": "2026-11-09", "s": "done", "t": T("About 1.7 million people reached, USD 340 million", "Cerca de 1,7 millones de personas alcanzadas, USD 340 millones"), "refs": [C % 153]},
  {"d": "2026-11-11", "s": "done", "t": T("Legal deadline for the advance: 1,812,348 people paid G. 3.9 trillion", "Vence el plazo legal del adelanto: 1.812.348 personas cobraron G. 3,9 billones"), "refs": [C % 179]},
  {"d": "2026-11-18", "s": "done", "t": T("Exclusion balance postponed 15 days", "Se posterga 15 días el balance de exclusión"), "refs": [C % 226]},
  {"d": "2026-11-19", "s": "done", "t": T("BCP assembling lots of assets and deposits for tender; no transfer yet", "El BCP arma lotes de activos y depósitos para licitar; aún sin traspasos"), "refs": [C % 232]},
  {"d": "2026-11-20", "s": "done", "t": T("88% of earmarked funds disbursed; 3,975 certificates pending", "88% de los fondos previstos desembolsados; 3.975 CDA pendientes"), "refs": [D4 % 9]},
  {"d": "2026-11-22", "s": "done", "t": T("BCP: the advance is complete; 97% of depositors covered", "BCP: el adelanto está completo; 97% de los depositantes cubiertos"), "refs": [D5 % 19]},
  {"d": "2026-12-02", "s": "next", "t": T("Extension ends: exclusion balance and tender of lots to other banks", "Vence la prórroga: balance de exclusión y licitación de lotes a otros bancos"), "refs": [D5 % 13]},
  {"d": None, "s": "unknown", "t": T("Payment of the remaining 35 wages, or transfer of deposits to a buying bank", "Pago de los 35 salarios restantes, o traspaso de los depósitos a un banco comprador"), "refs": [D5 % 13]},
  {"d": None, "s": "unknown", "t": T("Any recovery above the cap, for institutions and for bondholders", "Cualquier recuperación por encima del tope, para instituciones y para bonistas"), "refs": [D5 % 51]},
 ],
 "conditions": [
  {"t": T("The cap applies per person (natural or legal) and per institution, not per account.", "El tope se aplica por persona (física o jurídica) y por entidad, no por cuenta."), "refs": [C % 73]},
  {"t": T("The first payment was announced net of debts owed to the bank.", "El primer pago se anunció neto de deudas con el banco."), "refs": [C % 73]},
  {"t": T("Certificates of deposit are paid only after validation. Reported causes of delay: data that do not match, holders who have not registered, and joint certificates where not every holder registered.", "Los CDA se pagan solo tras su validación. Causas de demora informadas: datos que no coinciden, titulares sin registrarse y certificados conjuntos en los que no todos los titulares se registraron."), "refs": [D4 % 9]},
  {"t": T("The BCP director blamed 'much disorder' in the bank's records for slower payment of certificates.", "El director del BCP atribuyó a 'mucho desorden' en los registros del banco la demora en el pago de los CDA."), "refs": [D5 % 19]},
  {"t": T("If you owe the bank: the interveners say no payment channel exists yet, and default and penalty interest is waived until 30 Nov 2026.", "Si usted le debe al banco: los interventores informan que aún no hay canal de pago y que los intereses moratorios y punitorios no se cobran hasta el 30 nov 2026."), "refs": ["dos6:event:0025"]},
  {"t": T("Small firms with money trapped above the cap: the BCP allows bridge loans and refinancing without a rating penalty, and the public lender AFD announced a G. 50,000 million programme, still pending.", "Mipymes con dinero atrapado por encima del tope: el BCP permite créditos puente y refinanciación sin castigo de calificación, y la AFD anunció un programa de G. 50.000 millones, aún pendiente."), "refs": [D5 % 53, C % 214, D4 % 13]},
 ],
 "waiting": [
  {"who": T("Depositors above the cap", "Depositantes por encima del tope"), "amt": T("not published", "no publicado"), "n": T("no official figure; a savers' lawyer estimates 80,000 to 90,000 depositors and about USD 1,200 million above the cover, and has asked the central bank for a dated timetable", "sin cifra oficial; un abogado de ahorristas estima entre 80.000 y 90.000 depositantes y unos USD 1.200 millones por encima de la cobertura, y pidió al BCP un cronograma con fechas"), "refs": ["bot:event:0008", "bot:fact:0003", "bot:fact:0004", D5 % 52, D5 % 19]},
  {"who": T("Holders of unvalidated certificates of deposit", "Titulares de CDA sin validar"), "amt": T("about G. 221,000 million", "unos G. 221.000 millones"), "n": T("3,975 certificates at 20 Nov", "3.975 certificados al 20 nov"), "refs": ["dos4:fact:0006"]},
  {"who": T("Social security institute (IPS)", "Instituto de Previsión Social (IPS)"), "amt": T("more than USD 516 million", "más de USD 516 millones"), "n": T("about USD 350 million of pension-fund investments; the 32,000 pensioners paid through Ueno were moved to other banks", "unos USD 350 millones de inversiones del fondo jubilatorio; los 32.000 jubilados que cobraban por Ueno pasaron a otros bancos"), "refs": ["dos4:fact:0003", "dos5:fact:0005", D5 % 33]},
  {"who": T("Itaipú", "Itaipú"), "amt": T("USD 163.8 million plus G. 115,200 million", "USD 163,8 millones más G. 115.200 millones"), "n": T("an earlier report gave USD 182 million; on 24 Nov a board member said 'above USD 200 million'", "un informe previo daba USD 182 millones; el 24 nov un consejero dijo 'más de USD 200 millones'"), "refs": ["dos5:fact:0006", "dos4:fact:0004", "dos6:fact:0003"]},
  {"who": T("City of Asunción", "Municipalidad de Asunción"), "amt": T("G. 1,792.6 million", "G. 1.792,6 millones"), "n": T("three accounts in the official balance at 31 Oct", "tres cuentas en el balance oficial al 31 oct"), "refs": ["dos5:fact:0007"]},
  {"who": T("Mutual-fund investors (Ueno AFPISA)", "Inversores de fondos mutuos (Ueno AFPISA)"), "amt": T("about USD 46 million", "unos USD 46 millones"), "n": T("about 30,000 investors; outside the guarantee; they ask for the funds to move to another manager", "unos 30.000 inversores; fuera de la garantía; piden pasar los fondos a otra administradora"), "refs": ["bot:event:0009", "bot:fact:0005", "bot:fact:0006", C % 167]},
 ],
 "coverage": {
  "explainer": {
   "title": T("Did the bank have enough assets?", "¿Tenía el banco activos suficientes?"),
   "answer": T("Enough for depositors, by the central bank's account, if other banks buy them. Not enough for all of the bank's debts.", "Suficientes para los depositantes, según el BCP, si otros bancos los compran. No alcanzan para todas las deudas del banco."),
   "points": [
    {"t": T("The '100% covered' headlines of 18 Nov come from a legislator describing a meeting with the central bank, not from a central bank statement.", "Los titulares de 'cobertura del 100%' del 18 nov provienen de un legislador que relató una reunión con el BCP, no de un comunicado del BCP."), "refs": ["web:event:0001"]},
    {"t": T("The central bank president qualified it the same day: depositors would be covered, international and local bonds would not, and the assets show a deficit of USD 1,500 million.", "El presidente del BCP lo matizó el mismo día: se cubriría a los depositantes, no los bonos internacionales y locales, y los activos muestran un déficit de USD 1.500 millones."), "refs": ["web:event:0002", "web:fact:0002"]},
    {"t": T("The verified assets, about G. 9.25 trillion, are loans, certificates and property, not cash. What they are worth is what banks bid in the tender, and the figure is preliminary.", "Los activos verificados, unos G. 9,25 billones, son carteras, certificados y bienes, no efectivo. Valen lo que los bancos ofrezcan en la licitación, y la cifra es preliminar."), "refs": ["web:event:0003", "web:fact:0001"]},
    {"t": T("They would not repay the guarantee fund's advance either. The central bank puts the shortfall at USD 1,000 to 1,500 million including that advance.", "Tampoco alcanzarían para reponer el adelanto del fondo de garantía. El BCP estima el faltante en USD 1.000 a 1.500 millones, incluido ese adelanto."), "refs": ["web:event:0003"]},
   ],
   "math_title": T("Why both statements can be true (our reading, not a source's)", "Por qué ambas afirmaciones pueden ser ciertas (lectura nuestra, no de una fuente)"),
   "math": [
    {"k": T("Assets the bank declared", "Activos que declaraba el banco"), "v": T("about USD 4,400 million", "unos USD 4.400 millones"), "refs": ["web:fact:0003"]},
    {"k": T("Assets verified so far", "Activos verificados hasta ahora"), "v": T("about USD 1,450 to 1,500 million", "unos USD 1.450 a 1.500 millones"), "refs": ["web:fact:0001", "web:fact:0006"]},
    {"k": T("Deposits", "Depósitos"), "v": T("about USD 2,800 million", "unos USD 2.800 millones"), "refs": [C % 166]},
    {"k": T("Already paid to depositors by the guarantee fund", "Ya pagado a depositantes por el fondo de garantía"), "v": T("about USD 644 million", "unos USD 644 millones"), "refs": ["dos4:fact:0007"]},
   ],
   "math_note": T("About USD 1,500 million of assets can cover what depositors are still owed only if the guarantee fund absorbs what it has already paid and bondholders and other creditors take the loss. That is a loss being shared out, not a bank that had enough. These figures come from different sources and dates and are indicative only.", "Unos USD 1.500 millones de activos pueden cubrir lo que aún se debe a los depositantes solo si el fondo de garantía absorbe lo que ya pagó y los bonistas y demás acreedores asumen la pérdida. Eso es repartir una pérdida, no un banco al que le alcanzaba. Las cifras provienen de fuentes y fechas distintas y son solo indicativas.")},
  "intro": T("Whether the plan can pay everyone turns on two numbers that officials have not reconciled: what the sound assets are worth, and how much is owed above the guarantee. The figures below were given on different dates and measure different things; they are not added up.", "Que el plan alcance para todos depende de dos números que las autoridades no han conciliado: cuánto valen los activos sanos y cuánto se debe por encima de la garantía. Las cifras de abajo se dieron en fechas distintas y miden cosas distintas; no se suman."),
  "rows": [
   {"k": T("Guarantee fund still available", "Fondo de garantía aún disponible"), "v": T("more than USD 1,000 million", "más de USD 1.000 millones"), "d": "2026-11-20", "side": "have", "refs": ["dos4:fact:0007"]},
   {"k": T("Sound assets of the bank, BCP president", "Activos sanos del banco, presidente del BCP"), "v": T("about USD 600 million", "unos USD 600 millones"), "d": "2026-11-12", "side": "have", "refs": [C % 187]},
   {"k": T("Sound assets of the bank, BCP director", "Activos sanos del banco, director del BCP"), "v": T("USD 1,400 to 1,500 million", "USD 1.400 a 1.500 millones"), "d": "2026-11-22", "side": "have", "refs": ["dos5:fact:0002"]},
   {"k": T("Assets verified by the interveners, BCP", "Activos verificados por los interventores, BCP"), "v": T("about G. 9.25 trillion", "unos G. 9,25 billones"), "d": "2026-11-18", "side": "have", "refs": ["web:fact:0001", C % 226]},
   {"k": T("Deficit, BCP president", "Déficit, presidente del BCP"), "v": T("USD 1,500 million", "USD 1.500 millones"), "d": "2026-11-18", "side": "owe", "refs": ["web:fact:0002"]},
   {"k": T("Bonds outside the guarantee", "Bonos fuera de la garantía"), "v": T("USD 350 million abroad, plus local bonds", "USD 350 millones en el exterior, más bonos locales"), "d": "2026-11-18", "side": "owe", "refs": ["web:fact:0005"]},
   {"k": T("Hole in the balance sheet, BCP director", "Agujero en el balance, director del BCP"), "v": T("more than USD 1,500 million", "más de USD 1.500 millones"), "d": "2026-11-22", "side": "owe", "refs": ["dos5:fact:0001"]},
   {"k": T("Losses to the guarantee fund and securities holders, La Nación's count", "Pérdidas para el fondo de garantía y tenedores de títulos, cálculo de La Nación"), "v": T("USD 1,362 million", "USD 1.362 millones"), "d": "2026-11-22", "side": "owe", "refs": ["dos5:fact:0003"]},
   {"k": T("Total deposits at the bank, AFP", "Depósitos totales del banco, AFP"), "v": T("about USD 2,800 million", "unos USD 2.800 millones"), "d": "2026-11-10", "side": "owe", "refs": [C % 166]},
  ]},
 "unknown": [
  T("The total owed above the cap, and how many depositors that is.", "El total adeudado por encima del tope y cuántos depositantes son."),
  T("The date and method for paying the remaining 35 wages if the tender fails.", "La fecha y el modo de pago de los 35 salarios restantes si la licitación fracasa."),
  T("Which banks will bid for the lots and on what terms.", "Qué bancos ofertarán por los lotes y en qué condiciones."),
  T("An official list of affected public bodies and amounts; none has been published.", "Una lista oficial de entidades públicas afectadas y montos; no se publicó ninguna."),
  T("What happens to the mutual funds: transfer to a new manager or liquidation.", "Qué pasará con los fondos mutuos: traspaso a un nuevo administrador o liquidación."),
 ],
}
def refs(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "refs": yield from v
            else: yield from refs(v)
    elif isinstance(o, list):
        for v in o: yield from refs(v)
missing = sorted({r for r in refs(P) if r not in ids})
if missing: sys.exit("payouts.json: refs not found in data/raw: %s" % missing)
out = os.path.join(os.path.dirname(HERE), "site", "data", "payouts.json")
json.dump(P, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("payouts.json:", len(set(refs(P))), "distinct rows cited, all present")
