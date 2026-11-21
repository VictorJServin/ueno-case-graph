import json
N=json.load(open('/home/claude/ueno-kg/analysis/mm_build/numbers.json'))
FX=6500
def usd(gs): return round(gs/FX/1e5)*1e5
pd=1621853458972; plc=876640e6; trust=2105744e6; intD=900995e6; intJ=825160884847
A=25641756262733; Lb=23205211051347; Eq=2436545211386
res=N['res']
U={
 'aviso':'https://www.ueno.com.py/wp-content/uploads/2026/07/Aviso-Balance-255x35cm_jun2026-1.pdf',
 'fix':'https://www.ueno.com.py/wp-content/uploads/2026/04/UENO-Bank-S.A.-_FIX.pdf',
 'perfil':'https://www.perfil.com/noticias/amp/internacional/el-banco-central-de-paraguay-informo-que-encontro-activos-de-ueno-bank-y-detallo-a-quienes-se-le-devolvera-ese-dinero-aYk6R4M1Ioff.phtml',
 'infoneg':'https://infonegocios.com.py/nota-principal/jorge-schreiner-analizando-las-carteras-de-clientes-y-sin-incluir-activos-el-monto-supera-el-conjunto-de-la-deuda-de-ueno-con-el-sistema-previsional',
 'elsol':'https://www.elsol.com.ar/?p=2281912',
 'afp':'https://crhoy.com/mundo/que-paso-con-el-dinero-de-ueno-bank-en-paraguay-y-cuanto-falta-recuperar/',
 'efe':'https://www.laprensa.hn/mundo/ueno-bank-paraguay-fondos-publicos-gran-desafio-intervencion-GM32584570',
 'forbes':'https://www.forbesargentina.com/today/el-escandalo-ueno-bank-sacude-paraguay-fondos-publicos-juego-una-crisis-amenaza-su-reputacion-n102136'}
def I(le,ls,v,c,k,refs,url=''): return {"label_en":le,"label_es":ls,"value":v,"currency":c,"kind":k,"refs":refs,"url":url}
six_refs=["rec:loan:%04d"%i for i in range(1,36)]
list_refs=["press:fact:%04d"%i for i in range(1,22)]
D=[]
D.append({"id":"capital_hole_supervisor","title_en":"Capital hole as stated by the supervisor","title_es":"Faltante de capital según el supervisor",
"what_en":"The provisions shortfall the Central Bank found, and the capital needed to return to the 12% legal minimum. It measures regulatory capital, not cash that left the bank.",
"what_es":"El déficit de previsiones que constató el BCP y el capital necesario para volver al mínimo legal del 12%. Mide capital regulatorio, no dinero que haya salido del banco.",
"low":usd(1085.4e9),"central":usd(pd),"high":usd(pd)+70e6,"currency":"USD","as_of":"2026-11",
"method_en":"Central: provisions deficit of Gs. 1,621.9 billion at Gs. 6,500. Low: capital needed to reach 12% once the deficit is taken from capital and from risk-weighted assets (solving 13.85% and 5.56% gives effective equity of about Gs. 2,559 billion and risk-weighted assets of about Gs. 18,476 billion). High: deficit plus the USD 70 million also claimed in the Central Bank's civil embargo.",
"method_es":"Central: déficit de previsiones de Gs. 1,62 billones a Gs. 6.500. Bajo: capital necesario para llegar al 12% deduciendo el déficit del patrimonio y de los activos ponderados (al resolver 13,85% y 5,56% resultan un patrimonio efectivo de unos Gs. 2,56 billones y activos ponderados de unos Gs. 18,48 billones). Alto: déficit más los USD 70 millones que el BCP también reclamó en el embargo civil.",
"inputs":[I("Provisions deficit","Déficit de previsiones",pd,"PYG","reported",["chrono:event:0070","press:fact:0105"]),
 I("Solvency ratio reported / after adjustments / minimum (13.85 / 5.56 / 12)","Índice de solvencia informado / ajustado / mínimo (13,85 / 5,56 / 12)",5.56,"PCT","reported",["chrono:event:0070"]),
 I("Implied effective equity before adjustment","Patrimonio efectivo implícito antes del ajuste",round(N['pe2']),"PYG","computed",["chrono:event:0070"]),
 I("Capital needed to restore 12%","Capital necesario para restituir el 12%",1085.4e9,"PYG","computed",["chrono:event:0070"]),
 I("Civil embargo: USD 70 million plus Gs. 1.6 trillion","Embargo civil: USD 70 millones más Gs. 1,6 billones",70000000,"USD","reported",["chrono:event:0084","chrono:event:0085"])],
"overlaps_with":["capital_hole_questioned_assets","questioned_credit","rey_figure"],"confidence":"medium"})
D.append({"id":"capital_hole_questioned_assets","title_en":"Capital hole adding the assets analysts question","title_es":"Faltante de capital sumando los activos cuestionados",
"what_en":"The supervisor's shortfall plus balance-sheet items with little or no value in a wind-down: placements in REDISA and REDIPRO, the merger-expenses trust and intangible assets.",
"what_es":"El déficit del supervisor más partidas del balance con poco o ningún valor en una liquidación: colocaciones en REDISA y REDIPRO, el fideicomiso de gastos de fusión y los intangibles.",
"low":usd(pd+plc),"central":usd(pd+plc+trust),"high":usd(pd+plc+trust+intD),"currency":"USD","as_of":"2025-12 / 2026-11",
"method_en":"Low: provisions deficit plus placements in REDISA and REDIPRO. Central: plus the merger-expenses trust. High: plus intangible assets as measured by FIX at December 2025. The published 5.56% is reproduced by the provisions deficit alone, so these items do not appear to be in it. Against implied effective equity of about Gs. 2,559 billion the central case leaves capital of about minus Gs. 2,045 billion; restoring 12% would take about Gs. 3,710 billion (USD 571 million).",
"method_es":"Bajo: déficit de previsiones más colocaciones en REDISA y REDIPRO. Central: más el fideicomiso de gastos de fusión. Alto: más los intangibles medidos por FIX a diciembre de 2025. El 5,56% publicado se reproduce solo con el déficit de previsiones, por lo que estas partidas no parecen estar incluidas. Frente a un patrimonio efectivo implícito de unos Gs. 2,56 billones, el caso central deja un capital de unos Gs. 2,05 billones negativos; restituir el 12% exigiría unos Gs. 3,71 billones (USD 571 millones).",
"inputs":[I("Provisions deficit","Déficit de previsiones",pd,"PYG","reported",["chrono:event:0070"]),
 I("Placements in REDISA and REDIPRO, December 2025","Colocaciones en REDISA y REDIPRO, diciembre de 2025",plc,"PYG","reported",["press:fact:0126","press:event:0041","press:event:0026"]),
 I("Merger-expenses trust, December 2025","Fideicomiso de gastos de fusión, diciembre de 2025",trust,"PYG","reported",["press:fact:0265","chrono:event:0017"]),
 I("Other intangible assets, December 2025 (FIX SCR)","Otros activos intangibles, diciembre de 2025 (FIX SCR)",intD,"PYG","reported",[],U['fix']),
 I("Deferred charges and intangibles, June 2026 (published balance sheet)","Cargos diferidos e intangibles, junio de 2026 (balance publicado)",intJ,"PYG","reported",[],U['aviso']),
 I("Book equity, December 2025","Patrimonio neto contable, diciembre de 2025",2117665e6,"PYG","reported",["press:fact:0254"])],
"overlaps_with":["capital_hole_supervisor","rey_figure","reconciliation_shortfall"],"confidence":"medium"})
D.append({"id":"capital_hole_rey","title_en":"The hole on Julio Rey's account","title_es":"El faltante según el relato de Julio Rey",
"what_en":"Rey told prosecutors that expenses of about USD 900 million were deferred by moving them into loans to related and unrelated companies. This is his claim; no schedule supports it.",
"what_es":"Rey declaró ante la Fiscalía que gastos por unos USD 900 millones se difirieron pasándolos a créditos a empresas vinculadas y no vinculadas. Es su afirmación; no hay planilla que la respalde.",
"low":600e6,"central":900e6,"high":900e6+usd(trust),"currency":"USD","as_of":"2026-11",
"method_en":"Low: the two components he itemises (about 300 cashback and about 300 technology and other). Central: his total. High: his total plus the merger-expenses trust, on the reading that the trust authorised in 2024 is separate from the later transfer of expenses into loans; the overlap between the two is not known.",
"method_es":"Bajo: los dos componentes que detalla (unos 300 de reintegros y unos 300 de tecnología y otros). Central: su total. Alto: su total más el fideicomiso de gastos de fusión, bajo la lectura de que el fideicomiso autorizado en 2024 es distinto del posterior traspaso de gastos a créditos; no se conoce el solapamiento entre ambos.",
"inputs":[I("Rey: loans used to defer expenses","Rey: créditos usados para diferir gastos",900e6,"USD","reported",["rec:flow:0075","src:acta-p22"]),
 I("Rey: cashback component","Rey: componente de reintegros",300e6,"USD","reported",["rec:flow:0075"]),
 I("Rey: technology and other","Rey: tecnología y otros",300e6,"USD","reported",["rec:flow:0075","rec:flow:0074"]),
 I("Merger-expenses trust","Fideicomiso de gastos de fusión",trust,"PYG","reported",["press:fact:0265"])],
"overlaps_with":["questioned_credit","capital_hole_questioned_assets","capital_hole_supervisor"],"confidence":"low"})
D.append({"id":"questioned_credit","title_en":"Questioned credit outstanding","title_es":"Créditos cuestionados, saldo vigente",
"what_en":"Loans and overdrafts to the six record borrowers, the five June 2026 borrowers and the second ring of press-reported borrowers, counted once. It is exposure, not loss.",
"what_es":"Préstamos y sobregiros a las seis prestatarias del acta, las cinco de junio de 2026 y el segundo anillo de prestatarias según la prensa, contados una sola vez. Es exposición, no pérdida.",
"low":usd(N['book_low']),"central":usd(N['book_c']),"high":usd(N['book_h']),"currency":"USD","as_of":"2026-06 to 2026-11",
"method_en":"109 loan rows collapse to 73 operations by the sameOperation rule (same operation number, or same borrower, date and amount) and to about 60 after the editor's manual matches. Six record borrowers: record balances of USD 166.98 million plus Gs. 395.5 billion, less the nine loans sold on 15 June 2026 and the three overdrafts cancelled that day, leaving USD 88.97 million plus Gs. 195.4 billion. Low: that, plus the five June loans (USD 81.84 million plus Gs. 194.4 billion) and eight shell-type borrowers on the unofficial debtor list. Central: the debtor-list balance for the five June borrowers and 15 listed borrowers including overt group companies. High: plus La Tropa SAE, Dobrestec, TSV and Infocenter.",
"method_es":"Las 109 filas de préstamos se reducen a 73 operaciones con la regla sameOperation (mismo número de operación, o misma prestataria, fecha y monto) y a unas 60 con las coincidencias manuales del editor. Seis prestatarias del acta: saldos del acta de USD 166,98 millones más Gs. 395.500 millones, menos los nueve créditos vendidos el 15 de junio de 2026 y los tres sobregiros cancelados ese día, lo que deja USD 88,97 millones más Gs. 195.400 millones. Bajo: eso, más los cinco préstamos de junio (USD 81,84 millones más Gs. 194.400 millones) y ocho prestatarias tipo fachada de la nómina oficiosa. Central: el saldo de la nómina para las cinco de junio y 15 deudoras de la nómina, incluidas empresas abiertamente del grupo. Alto: más La Tropa SAE, Dobrestec, TSV e Infocenter.",
"inputs":[I("Six record borrowers, outstanding per record tables (USD part)","Seis prestatarias del acta, saldo según tablas (parte USD)",round(N['S']['out_USD'],2),"USD","computed",six_refs+["press:fact:0103"]),
 I("Six record borrowers, outstanding per record tables (PYG part)","Seis prestatarias del acta, saldo según tablas (parte Gs.)",round(N['S']['out_PYG']),"PYG","computed",six_refs),
 I("Six, still on the balance sheet after 15 June 2026 (USD part)","Seis, aún en balance tras el 15 de junio de 2026 (parte USD)",round(N['six_net_usd'],2),"USD","computed",six_refs+["rec:flow:0060","press:loan:0029","press:loan:0030","press:loan:0034"]),
 I("Six, still on the balance sheet after 15 June 2026 (PYG part)","Seis, aún en balance tras el 15 de junio de 2026 (parte Gs.)",round(N['six_net_pyg']),"PYG","computed",six_refs+["press:loan:0029","press:loan:0030"]),
 I("Five June 2026 loans (USD part)","Cinco préstamos de junio de 2026 (parte USD)",N['five_usd'],"USD","reported",["rec:loan:0036","rec:loan:0037","rec:loan:0038","rec:loan:0039","rec:loan:0040"]),
 I("Five June 2026 borrowers, guaraní loans the same day","Cinco prestatarias de junio de 2026, préstamos en guaraníes del mismo día",N['five_pyg'],"PYG","reported",["press:loan:0004","press:loan:0007","press:loan:0008"]),
 I("Five June 2026 borrowers, unofficial debtor-list balance","Cinco prestatarias de junio de 2026, saldo en la nómina oficiosa",N['five_list'],"PYG","reported",["press:fact:0007","press:fact:0012","press:fact:0013","press:fact:0014","press:fact:0015"]),
 I("Second ring, 15 borrowers on the unofficial debtor list","Segundo anillo, 15 deudoras de la nómina oficiosa",N['ring_list'],"PYG","reported",list_refs),
 I("Further borrowers outside the list (La Tropa SAE, Dobrestec, TSV, Infocenter)","Otras deudoras fuera de la nómina (La Tropa SAE, Dobrestec, TSV, Infocenter)",N['ring_extra'],"PYG","computed",["press:fact:0090","press:fact:0050","press:fact:0052","press:loan:0047"]),
 I("Share of the six's balance explicitly on sole signature","Parte del saldo de las seis expresamente a sola firma",round(N['asf_share']*100,1),"PCT","computed",six_refs),
 I("Share of everything granted to the six shown as repaid, all with group or bank-funded money as alleged","Parte de lo otorgado a las seis que figura como pagado, todo con dinero del grupo o fondeado por el banco según se alega",round(N['tot_rep']/ (N['S']['grant_USD']*FX+N['S']['grant_PYG'])*100,1),"PCT","computed",six_refs+["rec:flow:0009","rec:flow:0020","rec:flow:0024","rec:flow:0031","rec:flow:0034","rec:flow:0061"])],
"overlaps_with":["rey_figure","capital_hole_supervisor","reconciliation_shortfall"],"confidence":"medium"})
D.append({"id":"rey_figure","title_en":"Rey's USD 900 million tested","title_es":"Los USD 900 millones de Rey, puestos a prueba",
"what_en":"How much of Rey's figure can be tied to identified loans. The low value is what matches the companies he names; the central value is his figure; the high value is the whole questioned book.",
"what_es":"Qué parte de la cifra de Rey puede vincularse con créditos identificados. El valor bajo es lo que coincide con las empresas que él nombra; el central es su cifra; el alto es toda la cartera cuestionada.",
"low":usd(N['named']),"central":900e6,"high":usd(N['book_h']),"currency":"USD","as_of":"2026-11",
"method_en":"Named companies with a figure (the six, Office Design, Henrici, Model): Gs. 2,483 billion, 42% of USD 900 million; Data Force has no figure. The whole de-duplicated questioned book is USD 879 to 946 million, the same order as his total. Money traced by amount from borrowers to ITTI, REDISA, REDIPRO, Vinanzas and Grupo Vázquez is about USD 325 million (36%). ITTI billed related parties USD 168 million in 2025, so USD 300 million of technology spending is under two years of that billing. USD 300 million of cashback is about USD 164 per funded account. Rey leaves about USD 300 million unexplained.",
"method_es":"Empresas nombradas con cifra (las seis, Office Design, Henrici, Model): Gs. 2,48 billones, 42% de USD 900 millones; Data Force no tiene cifra. Toda la cartera cuestionada depurada suma entre USD 879 y 946 millones, del mismo orden que su total. El dinero rastreado con monto desde las prestatarias hacia ITTI, REDISA, REDIPRO, Vinanzas y Grupo Vázquez es de unos USD 325 millones (36%). ITTI facturó a vinculadas USD 168 millones en 2025, de modo que USD 300 millones de tecnología equivalen a menos de dos años de esa facturación. USD 300 millones de reintegros son unos USD 164 por cuenta con saldo. Rey deja unos USD 300 millones sin explicar.",
"inputs":[I("Rey's total","Total de Rey",900e6,"USD","reported",["rec:flow:0075"]),
 I("Exposure to companies Rey names","Exposición a las empresas que Rey nombra",N['named'],"PYG","computed",six_refs+["press:fact:0003","press:fact:0016","press:fact:0009"]),
 I("ITTI revenue from related parties, 2025","Ingresos de ITTI por servicios a vinculadas, 2025",168e6,"USD","reported",["press:fact:0299","press:fact:0308"]),
 I("Funded accounts","Cuentas con saldo",1824994,"COUNT","reported",["chrono:event:0165"]),
 I("Clients claimed, December 2025","Clientes declarados, diciembre de 2025",2700000,"COUNT","reported",["press:fact:0267"]),
 I("Bank revenue, 2025","Ingresos del banco, 2025",221e6,"USD","reported",["press:fact:0293"]),
 I("Cashback per funded account implied by USD 300 million","Reintegro por cuenta con saldo implícito en USD 300 millones",164,"USD","computed",["rec:flow:0075","chrono:event:0165"]),
 I("Merger-expenses trust","Fideicomiso de gastos de fusión",trust,"PYG","reported",["press:fact:0265"])],
"overlaps_with":["questioned_credit","capital_hole_rey","capital_hole_questioned_assets"],"confidence":"low"})
D.append({"id":"cash_outside_system","title_en":"Cash outside the banking system","title_es":"Efectivo fuera del sistema",
"what_en":"Cash that Rey says was brought to the bank at night and later used to buy certificates of deposit, plus other cash reported by the press. Small against the hole; relevant to the origin of capital.",
"what_es":"Efectivo que, según Rey, se llevó de noche al banco y luego se usó para comprar CDA, más otros movimientos de efectivo publicados. Es poco frente al faltante; importa para el origen del capital.",
"low":0,"central":round((17e6*FX+17e9)/FX,-5),"high":round((17e6*FX+17e9+4537e6+3090e6)/FX,-5),"currency":"USD","as_of":"2025 to 2026-11",
"method_en":"Central: USD 17 million plus Gs. 17,000 million at Gs. 6,500 (hearsay through a colleague, dated about May 2025). High: adds cash orders reported by ABC (Gs. 4,537 million) and the shortfall found at GSR Security (Gs. 3,090 million). Low: zero, because none of it is corroborated.",
"method_es":"Central: USD 17 millones más Gs. 17.000 millones a Gs. 6.500 (de oídas, por un colega, hacia mayo de 2025). Alto: suma los pedidos de efectivo publicados por ABC (Gs. 4.537 millones) y el faltante hallado en GSR Security (Gs. 3.090 millones). Bajo: cero, porque nada está corroborado.",
"inputs":[I("Rey: cash in dollars","Rey: efectivo en dólares",17e6,"USD","reported",["rec:flow:0071","rec:event:0047"]),
 I("Rey: cash in guaraníes","Rey: efectivo en guaraníes",17e9,"PYG","reported",["rec:flow:0072"]),
 I("ABC: internal cash orders, January and October 2026","ABC: pedidos internos de efectivo, enero y octubre de 2026",4537e6,"PYG","computed",["chrono:event:0031","chrono:event:0053","chrono:event:0058","chrono:event:0064"]),
 I("GSR Security: preliminary shortfall","GSR Security: faltante preliminar",3090e6,"PYG","reported",["chrono:event:0216"]),
 I("Reserve requirement the bank said it could not replenish","Encaje legal que el banco dijo no poder reponer",70e6,"USD","reported",["chrono:event:0067"])],
"overlaps_with":["capital_hole_rey"],"confidence":"low"})
D.append({"id":"reconciliation_shortfall","title_en":"Shortfall of assets against all liabilities","title_es":"Faltante de activos frente a todo el pasivo",
"what_en":"June 2026 book assets, less items with no realisable value and a loss on the questioned book, compared with book liabilities. This is the estimate of what creditors as a whole stand to lose after shareholders are wiped out.",
"what_es":"Activos contables a junio de 2026, menos las partidas sin valor realizable y una pérdida sobre la cartera cuestionada, comparados con el pasivo contable. Es la estimación de lo que el conjunto de acreedores puede perder una vez absorbido el patrimonio de los accionistas.",
"low":usd(res['low']['short']),"central":usd(res['central']['short']),"high":usd(res['high']['short']),"currency":"USD","as_of":"2026-06 balance, losses as known at 2026-11",
"method_en":"Low: trust and intangibles at zero, half the REDISA and REDIPRO placements, credit loss equal to the supervisor's provisions deficit (28% of the questioned book). Central: placements at zero and 60% loss on a questioned book of Gs. 5,713 billion. High: 90% loss on Gs. 6,151 billion and half of the Gs. 2.6 trillion past-due facility inherited from Visión.",
"method_es":"Bajo: fideicomiso e intangibles en cero, mitad de las colocaciones en REDISA y REDIPRO, pérdida crediticia igual al déficit de previsiones del supervisor (28% de la cartera cuestionada). Central: colocaciones en cero y pérdida del 60% sobre una cartera cuestionada de Gs. 5,71 billones. Alto: pérdida del 90% sobre Gs. 6,15 billones y la mitad de la facilidad de cartera vencida de Gs. 2,6 billones heredada de Visión.",
"inputs":[I("Total assets, 30 June 2026","Activo total, 30 de junio de 2026",A,"PYG","reported",[],U['aviso']),
 I("Total liabilities, 30 June 2026","Pasivo total, 30 de junio de 2026",Lb,"PYG","reported",[],U['aviso']),
 I("Equity, 30 June 2026","Patrimonio neto, 30 de junio de 2026",Eq,"PYG","reported",[],U['aviso']),
 I("Deposits at end-June 2026 (government deposits of Gs. 5 trillion were 29%)","Depósitos a fines de junio de 2026 (los depósitos públicos de Gs. 5 billones eran el 29%)",round(N['dep']),"PYG","computed",["chrono:event:0035"]),
 I("Loss given default on the questioned book: 28% / 60% / 90%","Pérdida en caso de incumplimiento sobre la cartera cuestionada: 28% / 60% / 90%",60,"PCT","assumption",[]),
 I("Past-due facility authorised for the Visión merger","Facilidad de cartera vencida autorizada para la fusión con Visión",2.6e12,"PYG","reported",["chrono:event:0017","press:event:0026"]),
 I("Central Bank: about USD 600 million of healthy assets","BCP: unos USD 600 millones de activos sanos",600e6,"USD","reported",["chrono:event:0187"],U['infoneg']),
 I("Prosecution: total damage","Fiscalía: perjuicio total",809.5e6,"USD","reported",["chrono:event:0148"])],
"overlaps_with":["capital_hole_supervisor","capital_hole_questioned_assets","questioned_credit","rey_figure"],"confidence":"low"})
W=[]
def w(se,ss,v,k,refs): W.append({"step_en":se,"step_es":ss,"value":v,"currency":"USD","kind":k,"refs":refs})
c=res['central']
w("Total assets at book, 30 June 2026 (Gs. 25,641.8 billion)","Activo total contable, 30 de junio de 2026 (Gs. 25,64 billones)",usd(A),"reported",[])
w("Less merger-expenses trust (Gs. 2,105.7 billion, December 2025 value)","Menos fideicomiso de gastos de fusión (Gs. 2,11 billones, valor a diciembre de 2025)",-usd(trust),"reported",["press:fact:0265"])
w("Less deferred charges and intangibles (Gs. 825.2 billion)","Menos cargos diferidos e intangibles (Gs. 825.200 millones)",-usd(intJ),"reported",[])
w("Less placements in REDISA and REDIPRO (Gs. 876.6 billion; low case takes half)","Menos colocaciones en REDISA y REDIPRO (Gs. 876.600 millones; el caso bajo toma la mitad)",-usd(plc),"assumption",["press:fact:0126"])
w("Less loss on the questioned book, central 60% of Gs. 5,712.6 billion (low: Gs. 1,621.9 billion; high: 90% of Gs. 6,150.6 billion)","Menos pérdida sobre la cartera cuestionada, central 60% de Gs. 5,71 billones (bajo: Gs. 1,62 billones; alto: 90% de Gs. 6,15 billones)",-usd(.6*N['book_c']),"assumption",["chrono:event:0070"]+list_refs[:3])
w("Less Visión past-due facility (central: nil; high: half of Gs. 2.6 trillion)","Menos facilidad de cartera vencida de Visión (central: cero; alto: mitad de Gs. 2,6 billones)",0,"assumption",["chrono:event:0017"])
w("Equals assets left to cover deposits and creditors (low USD 3,177 million; high USD 2,307 million)","Igual a activos que quedan para cubrir depósitos y acreedores (bajo USD 3.177 millones; alto USD 2.307 millones)",usd(c['left']),"computed",[])
w("Less deposits, end-June 2026 (Gs. 17,241 billion)","Menos depósitos, fines de junio de 2026 (Gs. 17,24 billones)",-usd(N['dep']),"computed",["chrono:event:0035"])
w("Equals what is left for other creditors (low USD 525 million; high: deposits short by USD 345 million)","Igual a lo que queda para los demás acreedores (bajo USD 525 millones; alto: faltan USD 345 millones para los depósitos)",usd(c['left']-N['dep']),"computed",[])
w("Less other liabilities (Gs. 5,963.8 billion)","Menos otros pasivos (Gs. 5,96 billones)",-usd(Lb-N['dep']),"computed",[])
w("Equals shortfall against all liabilities (low USD 393 million; high USD 1,263 million)","Igual a faltante frente a todo el pasivo (bajo USD 393 millones; alto USD 1.263 millones)",usd(c['left']-Lb),"computed",[])
def S(we,ws,el,eh,ll,lh,ae,as_,refs): return {"who_en":we,"who_es":ws,"exposure_low":el,"exposure_high":eh,"expected_loss_low":ll,"expected_loss_high":lh,"currency":"USD","assumption_en":ae,"assumption_es":as_,"refs":refs}
ST=[
S("Deposit Guarantee Fund","Fondo de Garantía de Depósitos",740e6,928e6,0,845e6,
 "Exposure is the expected payout. Low loss: the fund recovers in full through subrogation, as in the low and central cases where adjusted assets exceed deposits. High loss: only the Central Bank's USD 600 million of healthy assets exists and pension deposits of USD 517 million are paid first.",
 "La exposición es el desembolso previsto. Pérdida baja: el Fondo recupera todo por subrogación, como en los casos bajo y central, en los que el activo ajustado supera los depósitos. Pérdida alta: solo existen los USD 600 millones de activos sanos del BCP y antes se pagan depósitos previsionales por USD 517 millones.",
 ["chrono:event:0166","chrono:event:0181","chrono:event:0138","chrono:event:0179","chrono:event:0187"]),
S("Uninsured private depositors","Depositantes privados no cubiertos por la garantía",1060e6,1248e6,0,387e6,
 "Exposure: 71% of USD 2.8 billion of deposits less the guaranteed part. Loss nil in the low and central cases; 31% in the high case, where first-order claims are paid in full and the rest share what is left.",
 "Exposición: 71% de USD 2.800 millones de depósitos menos la parte garantizada. Pérdida nula en los casos bajo y central; 31% en el caso alto, en el que los créditos de primer orden se pagan íntegramente y el resto se reparte lo que queda.",
 ["chrono:event:0166","chrono:event:0181","chrono:event:0226"]),
S("IPS (social security institute)","IPS (Instituto de Previsión Social)",345e6,517e6,17e6,87e6,
 "Pension deposits rank in the first order of payment. Low loss: 43% on Gs. 250 billion of bonds, if they are the bank's paper. High loss: all of those bonds plus 31% of USD 157.7 million of operating funds if these are not given pension priority.",
 "Los depósitos previsionales están en el primer orden de pago. Pérdida baja: 43% sobre Gs. 250.000 millones en bonos, si son papeles del banco. Pérdida alta: la totalidad de esos bonos más el 31% de USD 157,7 millones de fondos operativos si no se les reconoce la prelación previsional.",
 ["chrono:event:0091","chrono:event:0163","chrono:event:0198","press:fact:0106","press:fact:0033"]),
S("All public entities, IPS included","Todas las entidades públicas, incluido el IPS",787e6,888e6,17e6,255e6,
 "Exposure: Gs. 3.6 trillion plus USD 233.4 million at 30 September 2026 (USD 787 million at Gs. 6,500) up to the Ministry of Economy's USD 888 million. Non-pension public deposits above the guarantee are treated like uninsured private deposits: nil to 31%.",
 "Exposición: Gs. 3,6 billones más USD 233,4 millones al 30 de setiembre de 2026 (USD 787 millones a Gs. 6.500) hasta los USD 888 millones del MEF. Los depósitos públicos no previsionales por encima de la garantía se tratan como los privados no cubiertos: de cero a 31%.",
 ["chrono:event:0052","chrono:event:0035","dos:fact:0002","dos:fact:0003","press:fact:0113"]),
S("Holders of the international senior notes","Tenedores de los bonos internacionales senior",350e6,350e6,150e6,350e6,
 "Low loss: 57% recovery for non-deposit creditors in the low case. High: nothing. The market price of about 5 cents implies a loss of about USD 332 million.",
 "Pérdida baja: recupero del 57% para los acreedores no depositantes en el caso bajo. Alta: nada. El precio de mercado de unos 5 centavos implica una pérdida de unos USD 332 millones.",
 ["chrono:event:0032","chrono:event:0200","press:fact:0298"]),
S("Holders of the bank's local bonds, subordinated included","Tenedores de bonos locales del banco, incluidos los subordinados",103e6,103e6,44e6,103e6,
 "Exposure: Gs. 668.5 billion of securities issued at December 2025. Same recovery range as other non-deposit creditors; subordinated paper (USD 25 million) nil. The regulator has ordered funds to value the bank's instruments at zero. Part is held by IPS.",
 "Exposición: Gs. 668.500 millones en valores emitidos a diciembre de 2025. Mismo rango de recupero que los demás acreedores no depositantes; los subordinados (USD 25 millones), cero. El regulador ordenó a los fondos valuar en cero los instrumentos del banco. Una parte está en poder del IPS.",
 ["press:fact:0260","chrono:event:0086","chrono:event:0114"]),
S("Development lenders (IDB Invest, Triodos, GAWA)","Financiadores de desarrollo (BID Invest, Triodos, GAWA)",41e6,41e6,17e6,41e6,
 "Original amounts; balances outstanding are not published. Ranked with other non-deposit creditors.",
 "Montos originales; no se publican los saldos vigentes. Se ubican con los demás acreedores no depositantes.",
 ["chrono:event:0020","chrono:event:0048"]),
S("OTP Bank","OTP Bank",47e6,47e6,32e6,47e6,
 "Low: the fair-value charge already booked. High: the whole investment, since the bank's equity is exhausted in every case.",
 "Bajo: el ajuste a valor razonable ya registrado. Alto: toda la inversión, porque el patrimonio del banco se agota en todos los casos.",
 ["chrono:event:0036","chrono:event:0177","chrono:event:0089"]),
S("Shareholders of the bank (book equity, June 2026)","Accionistas del banco (patrimonio contable, junio de 2026)",375e6,375e6,375e6,375e6,
 "Equity of Gs. 2,436.5 billion is lost in all three cases. OTP's stake is inside this figure through U Holdings.",
 "El patrimonio de Gs. 2,44 billones se pierde en los tres casos. La participación de OTP está dentro de esta cifra a través de U Holdings.",
 ["press:fact:0254","chrono:event:0037"]),
S("Bondholders of Grupo Vázquez S.A.E.","Tenedores de bonos de Grupo Vázquez S.A.E.",204e6,204e6,122e6,184e6,
 "Recovery of 10% to 40%: cash of about USD 71 million against debt of USD 341 million; the main asset was the stake in the bank's parent.",
 "Recupero de 10% a 40%: caja de unos USD 71 millones frente a deuda de USD 341 millones; el principal activo era la participación en la controlante del banco.",
 ["press:fact:0303","press:fact:0304","press:fact:0302","press:fact:0156","chrono:event:0087"]),
S("Bondholders of ITTI S.A.E.","Tenedores de bonos de ITTI S.A.E.",40e6,40e6,16e6,32e6,
 "Recovery of 20% to 60%: cash of about USD 35 million against debt of USD 66 million; 59% of revenue came from the bank, but the core-banking business serves other entities.",
 "Recupero de 20% a 60%: caja de unos USD 35 millones frente a deuda de USD 66 millones; el 59% de los ingresos venía del banco, pero el negocio de core bancario atiende a otras entidades.",
 ["press:fact:0310","press:fact:0311","press:fact:0309","press:fact:0308","chrono:event:0088"]),
S("Local mutual funds holding bank and group paper (Cadiem and others)","Fondos mutuos locales con papeles del banco y del grupo (Cadiem y otros)",0,47e6,0,47e6,
 "Not published. The upper bound applies the 11.73% reported for one Cadiem fund to all USD 400 million under management, which overstates it. Bondholders of Kasas, Model and La Tropa SAE cannot be sized. Ueno AFPISA investors have about USD 46 million blocked; that is access, not a measured loss.",
 "No publicado. El tope aplica el 11,73% informado para un fondo de Cadiem a los USD 400 millones administrados, lo que lo sobrestima. No es posible dimensionar a los tenedores de bonos de Kasas, Model y La Tropa SAE. Los inversores de Ueno AFPISA tienen bloqueados unos USD 46 millones; es un problema de acceso, no una pérdida medida.",
 ["chrono:event:0114","chrono:event:0142","chrono:event:0167","press:fact:0058"])]
out={"analyst":"hole_sizing",
"disclaimer_en":"Analysis by an AI bank-resolution and financial-loss analyst, not a licensed professional. Every figure is a reported fact, a computation from reported facts or an estimate with stated assumptions; none is a finding. Conduct is described as alleged and everyone named is presumed innocent. The prosecution record states what the prosecution alleges and what Julio Rey told prosecutors; Rey's statements are his own claims. Cut-off: 20 November 2026.",
"disclaimer_es":"Análisis de un analista de IA en resolución bancaria y pérdidas financieras, no de un profesional matriculado. Cada cifra es un dato publicado, un cálculo a partir de datos publicados o una estimación con supuestos explícitos; ninguna es una conclusión firme. Las conductas se describen como presuntas y toda persona nombrada goza de la presunción de inocencia. El acta fiscal expresa lo que sostiene la Fiscalía y lo que Julio Rey declaró ante ella; lo dicho por Rey son afirmaciones suyas. Fecha de corte: 20 de noviembre de 2026.",
"fx":{"rate":6500,
 "basis_en":"Rate printed in the prosecution record, page 7: Gs. 253,000,000,000 is given as about USD 38,923,077, which is exactly Gs. 6,500 per dollar. Sensitivity uses two other printed rates: Gs. 6,358.5 (wholesale, 5 November 2026) and Gs. 6,585.55 (rating report, December 2025). The central shortfall is USD 738 million at 6,500, USD 755 million at 6,358.5 and USD 729 million at 6,585.55.",
 "basis_es":"Tipo de cambio que surge del acta fiscal, página 7: Gs. 253.000.000.000 figuran como unos USD 38.923.077, exactamente Gs. 6.500 por dólar. La sensibilidad usa otros dos tipos publicados: Gs. 6.358,5 (mayorista, 5 de noviembre de 2026) y Gs. 6.585,55 (informe de calificación, diciembre de 2025). El faltante central es de USD 738 millones a 6.500, USD 755 millones a 6.358,5 y USD 729 millones a 6.585,55.",
 "refs":["src:acta-p07","press:fact:0114","chrono:event:0122","press:fact:0219"]},
"definitions":D,"waterfall":W,"stakeholders":ST,
"headline":{"low":usd(res['low']['short']),"central":usd(res['central']['short']),"high":usd(res['high']['short']),"currency":"USD",
 "statement_en":"On published numbers, the bank's realisable assets fall short of its liabilities by about USD 740 million, within a range of USD 390 million to USD 1.26 billion. That is after shareholders lose their USD 375 million of book equity. The range is driven by how much of a questioned loan book of about USD 880 million is recovered. This is an estimate, not a finding.",
 "statement_es":"Con las cifras publicadas, los activos realizables del banco no alcanzan a cubrir su pasivo por unos USD 740 millones, dentro de un rango de USD 390 millones a USD 1.260 millones. Eso es después de que los accionistas pierdan sus USD 375 millones de patrimonio contable. El rango depende de cuánto se recupere de una cartera cuestionada de unos USD 880 millones. Es una estimación, no una conclusión firme."},
"cannot_determine_en":[
 "Which items the Central Bank deducted to reach 5.56%, and whether the Gs. 1.62 trillion already covers the related-company loans, the Visión past-due facility or both.",
 "The bank's balance sheet at the resolution date and the exclusion balance; the latest published balance sheet is June 2026.",
 "What the Central Bank's 'about USD 600 million of healthy assets' covers; it is about 15% of June 2026 book assets.",
 "The balance of the merger-expenses trust after December 2025 and the unamortised balance of the Visión past-due facility.",
 "Whether Rey's USD 900 million overlaps the trust, and what the unexplained USD 300 million was.",
 "The cut-off date of the unofficial debtor list and whether it prints balances or cumulative disbursements.",
 "The total cashback paid; no published figure was found.",
 "Per-fund holdings of bank and group paper at Cadiem and other managers, and bonds outstanding of Kasas, Model and La Tropa SAE.",
 "The split of public deposits between pension funds and other entities, and whether IPS's Gs. 250 billion of bonds are the bank's own paper.",
 "The value of 2,331 properties and assets abroad identified by authorities.",
 "The origin of the cash Rey describes and whether the certificates of deposit were ever booked as capital."],
"cannot_determine_es":[
 "Qué partidas dedujo el BCP para llegar al 5,56%, y si los Gs. 1,62 billones ya cubren los créditos a vinculadas, la facilidad de cartera vencida de Visión o ambas cosas.",
 "El balance del banco a la fecha de la resolución y el balance de exclusión; el último balance publicado es el de junio de 2026.",
 "Qué abarcan los 'unos USD 600 millones de activos sanos' del BCP; equivalen a cerca del 15% del activo contable de junio de 2026.",
 "El saldo del fideicomiso de gastos de fusión después de diciembre de 2025 y el saldo sin amortizar de la facilidad de cartera vencida de Visión.",
 "Si los USD 900 millones de Rey se solapan con el fideicomiso, y a qué corresponden los USD 300 millones sin explicar.",
 "La fecha de corte de la nómina oficiosa de deudores y si refleja saldos o desembolsos acumulados.",
 "El total pagado en reintegros; no se halló cifra publicada.",
 "Las tenencias por fondo de papeles del banco y del grupo en Cadiem y otras administradoras, y los bonos en circulación de Kasas, Model y La Tropa SAE.",
 "La división de los depósitos públicos entre cajas previsionales y demás entidades, y si los Gs. 250.000 millones en bonos del IPS son papeles del propio banco.",
 "El valor de los 2.331 inmuebles y de los activos en el exterior identificados por las autoridades.",
 "El origen del efectivo que describe Rey y si los CDA llegaron a registrarse como capital."],
"new_sources":[
 {"outlet":"ueno bank S.A.","title":"Aviso de balance al 30 de junio de 2026 (estados financieros publicados)","date":"2026-07","url":U['aviso']},
 {"outlet":"FIX SCR","title":"UENO Bank S.A., informe de revisión integral (cifras a diciembre de 2025)","date":"2026-03-31","url":U['fix']},
 {"outlet":"Perfil (Argentina)","title":"El Banco Central de Paraguay informó que encontró activos de Ueno Bank y detalló a quiénes se les devolverá ese dinero","date":"2026-11-13","url":U['perfil']},
 {"outlet":"InfoNegocios Paraguay","title":"Jorge Schreiner: analizando las carteras de clientes y sin incluir activos, el monto supera el conjunto de la deuda de ueno con el sistema previsional","date":"2026-11-13","url":U['infoneg']},
 {"outlet":"Diario El Sol (Mendoza)","title":"Nota sobre los activos de Ueno Bank informados por el BCP","date":"2026-11-13","url":U['elsol']},
 {"outlet":"AFP (via CR Hoy)","title":"¿Qué pasó con el dinero de Ueno Bank en Paraguay y cuánto falta recuperar?","date":"2026-11-10","url":U['afp']},
 {"outlet":"EFE (via La Prensa, Honduras)","title":"Fondos públicos: el gran desafío tras la intervención del Ueno bank","date":"2026-11-09","url":U['efe']},
 {"outlet":"Forbes Argentina","title":"El escándalo Ueno Bank sacude Paraguay: fondos públicos en juego y una crisis que amenaza su reputación","date":"2026-11-10","url":U['forbes']}]}
json.dump(out,open('/home/claude/ueno-kg/analysis/mm_size.json','w'),ensure_ascii=False,indent=1)
# validate
import glob
ids=set()
for f in glob.glob('/home/claude/ueno-kg/data/raw/*.jsonl'):
    for l in open(f):
        r=json.loads(l); ids.add(r.get('id'))
bad=[]
def chk(refs,where):
    for x in refs:
        if x not in ids: bad.append((where,x))
d=json.load(open('/home/claude/ueno-kg/analysis/mm_size.json'))
chk(d['fx']['refs'],'fx')
for x in d['definitions']:
    assert x['low']<=x['central']<=x['high'],x['id']
    for i in x['inputs']:
        chk(i['refs'],x['id']); assert i['refs'] or i['url'] or i['kind']=='assumption',(x['id'],i['label_en'])
    for o in x['overlaps_with']: assert o in [y['id'] for y in d['definitions']],o
for x in d['waterfall']: chk(x['refs'],'wf')
for x in d['stakeholders']: chk(x['refs'],x['who_en']); assert x['exposure_low']<=x['exposure_high'] and x['expected_loss_low']<=x['expected_loss_high']
print('bad refs',bad)
for x in d['definitions']: print(x['id'],x['low']/1e6,x['central']/1e6,x['high']/1e6)
for x in d['waterfall']: print(round(x['value']/1e6,1),x['step_en'][:70])
print(d['headline'])
