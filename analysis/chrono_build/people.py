# New entities, reported roles and the table of people charged (chrono contributor).
from lib import ENT, R, A, P

LN13 = "src:lanacion-2026-11-13-27-imputados"
UH5 = "src:ultimahora-2026-11-05-27-imputados-rol"
ABC16 = "src:abc-2026-11-16-uno-a-uno"
ABC5 = "src:abc-2026-11-05-juez-envia-prision"
ABC13 = "src:abc-2026-11-13-amplian-imputacion-pena"

# ---------------------------------------------------------------- entities
def person(id_, label, en, es, src, loc="", conf="high", aliases=None):
    ENT(id_, "Person", label, en, es, P("press", src, loc, "", conf), aliases)

# judges
person("person:rodrigo-estigarribia", "Rodrigo Estigarribia", "Criminal guarantees judge specialised in economic crimes (second shift); judge of Case 89/2026.", "Juez penal de Garantías Especializado en Delitos Económicos (segundo turno); juez de la Causa 89/2026.", "src:abc-2026-11-19-astigarraga-recurso", "body", aliases=["Rodrigo Enmanuel Estigarribia"])
person("person:humberto-otazu", "Humberto Otazú", "Guarantees judge specialised in economic crimes; admitted the charges in Case 89/2026 as duty judge and ordered detention in Case 92/2026.", "Juez de Garantías Especializado en Delitos Económicos; admitió la imputación en la Causa 89/2026 como juez de turno y dictó prisión en la Causa 92/2026.", "src:lanacion-2026-11-04-juez-admite", "body")
person("person:osmar-legal", "Osmar Legal", "Guarantees judge specialised in organised crime; reported in decisions concerning Santiago Peña (transfer, phone extraction).", "Juez de Garantías Especializado en Crimen Organizado; interviene en decisiones sobre Santiago Peña (traslado, extracción de celulares).", "src:ultimahora-2026-11-20-celulares", "body")
person("person:clara-ruiz-diaz", "Clara Ruiz Díaz", "Judge of Criminal Guarantees Court No. 1; rejected the habeas corpus filed for Julio Rey.", "Jueza del Juzgado Penal de Garantías N.º 1; rechazó el habeas corpus planteado a favor de Julio Rey.", "src:abc-2026-11-05-habeas-corpus", "body")
person("person:marcelo-saldivar", "Marcelo Saldívar", "Judge reported as ordering pre-trial detention of the Ueno Casa de Bolsa operations chief.", "Juez que, según se informó, dictó prisión preventiva a la jefa de operaciones de Ueno Casa de Bolsa.", "src:riotimes-2026-11-11-benitez", "body", "medium")
person("person:walter-mendoza", "Walter Mendoza", "First-instance civil and commercial judge (8th shift); ordered the preventive embargo requested by the BCP.", "Juez de Primera Instancia en lo Civil y Comercial del Octavo Turno; dictó el embargo preventivo pedido por el BCP.", "src:ultimahora-2026-11-03-embargo", "body")
for pid, label in (("person:silvana-luraghi", "Silvana Luraghi"), ("person:paublino-escobar", "Paublino Escobar"), ("person:claudia-criscioni", "Claudia Criscioni")):
    person(pid, label, "Member of the Appeals Tribunal specialised in economic crimes, organised crime and anti-corruption (panel named in the ruling that upheld detention and added offences).", "Camarista del Tribunal de Apelaciones Especializado en Delitos Económicos, Crimen Organizado y Anticorrupción (integró la sala que confirmó la prisión y amplió los hechos punibles).", "src:elnacional-2026-11-10-agravan-cargos", "body")
person("person:arnaldo-fleitas", "Arnaldo Fleitas", "Member of the specialised Appeals Tribunal panel that declared César Astigarraga's appeal inadmissible.", "Camarista del Tribunal de Apelación Especializado que declaró inadmisible el recurso de César Astigarraga.", "src:abc-2026-11-19-astigarraga-recurso", "body")

# prosecutors
person("person:jorge-arce", "Jorge Arce Rolandi", "Prosecutor (economic crimes and anti-corruption unit); signed the charges in Case 89/2026.", "Agente fiscal (Delitos Económicos y Anticorrupción); firmó la imputación en la Causa 89/2026.", "src:abc-2026-11-19-astigarraga-recurso", "body", aliases=["Jorge Arce", "Jorge Luis Arce Rolandi"])
person("person:silvio-corbeta", "Silvio Corbeta Dinamarca", "Prosecutor; signed the charges in Case 89/2026.", "Agente fiscal; firmó la imputación en la Causa 89/2026.", "src:abc-2026-11-19-astigarraga-recurso", "body", aliases=["Silvio Corbeta", "Silvio Corbetta"])
person("person:yeimy-adle", "Yeimy Adle Monges", "Prosecutor; signed the charges in Case 89/2026.", "Agente fiscal; firmó la imputación en la Causa 89/2026.", "src:abc-2026-11-19-astigarraga-recurso", "body", aliases=["Yeimy Adle", "Yeimy Rossana Adle Monges", "Yeimi Adle", "Yeimy Addle"])
person("person:francisco-cabrera", "Francisco Cabrera Sanabria", "Prosecutor; signed the charges in Case 89/2026; spoke on asset tracing abroad.", "Agente fiscal; firmó la imputación en la Causa 89/2026; informó sobre el rastreo de activos en el exterior.", "src:abc-2026-11-19-astigarraga-recurso", "body", aliases=["Francisco Cabrera", "Francisco Manuel Cabrera Sanabria"])
person("person:ruth-benitez", "Ruth Karina Benítez", "Prosecutor; named in the enlarged Case 89/2026 team and in the Case 92/2026 team.", "Agente fiscal; nombrada en el equipo ampliado de la Causa 89/2026 y en el equipo de la Causa 92/2026.", "src:lanacion-2026-11-13-pena-carvallo-bcp", "body", aliases=["Ruth Benítez"])
person("person:luz-guerrero", "Luz Guerrero", "Prosecutor named in the enlarged Case 89/2026 team.", "Agente fiscal nombrada en el equipo ampliado de la Causa 89/2026.", LN13, "body")
person("person:luis-pinanez", "Luis Piñánez", "Prosecutor named in the enlarged Case 89/2026 team.", "Agente fiscal nombrado en el equipo ampliado de la Causa 89/2026.", LN13, "body")
person("person:belinda-bobadilla", "Belinda Bobadilla Biscouto", "Prosecutor named in the enlarged Case 89/2026 team.", "Agente fiscal nombrada en el equipo ampliado de la Causa 89/2026.", LN13, "body")
person("person:nancy-salomon", "Nancy Salomón Marín", "Deputy attorney general (fiscal adjunta) coordinating the prosecution teams.", "Fiscal adjunta que coordina los equipos fiscales.", LN13, "body", aliases=["Nancy Salomón"])
person("person:manuel-doldan", "Manuel Doldán", "Deputy attorney general heading the International Affairs prosecution unit.", "Fiscal adjunto a cargo de la Fiscalía de Asuntos Internacionales.", "src:telefuturo-2026-11-03-directivos", "body")
person("person:federico-leguizamon", "Federico Leguizamón", "Prosecutor assigned to the case against the Ueno Casa de Bolsa employee.", "Agente fiscal asignado a la causa contra la funcionaria de Ueno Casa de Bolsa.", "src:abc-2026-11-10-benitez", "body")
for pid, label, al in (("person:silvia-gonzalez-vester", "Silvia González Vester", ["Silvia González"]), ("person:christian-benitez-caceres", "Christian Manuel Benítez Cáceres", ["Christian Benítez"]), ("person:elena-fiore", "Elena Fiore Franco", ["Elena Fiore"]), ("person:laura-giacummo", "Laura Mercedes Giacummo", ["Laura Giacummo"]), ("person:veronica-valdez", "María Verónica Valdez", ["Verónica Valdez"]), ("person:marlene-gonzalez", "Marlene González", [])):
    person(pid, label, "Prosecutor named in the team of the related case against Santiago Peña and former Central Bank officials.", "Agente fiscal nombrado/a en el equipo de la causa conexa contra Santiago Peña y exautoridades del BCP.", "src:lanacion-2026-11-13-pena-carvallo-bcp", "body", aliases=al)
person("person:emiliano-rolon", "Emiliano Rolón Fernández", "Attorney General from March 2023; resigned on 17 November 2026 amid an impeachment motion.", "Fiscal general del Estado desde marzo de 2023; renunció el 17 de noviembre de 2026 en medio de un pedido de juicio político.", "src:dw-2026-11-17-rolon", "body", aliases=["Emiliano Rolón"])
person("person:alba-rocio-cantero", "Alba Rocío Cantero Vera", "Interim Attorney General after Emiliano Rolón's resignation.", "Fiscal general interina tras la renuncia de Emiliano Rolón.", "src:abc-2026-11-19-denuncia-rolon", "body", aliases=["Alba Rocío Cantero"])

# officials / politicians
person("person:pedro-alliana", "Pedro Alliana", "Vice-president sworn in as President of Paraguay on 6 November 2026.", "Vicepresidente que juró como presidente de la República el 6 de noviembre de 2026.", "src:abc-2026-11-06-en-vivo-juicio-politico", "19:45")
person("person:antonio-barrios", "Antonio Barrios", "Senator elected and sworn in as vice-president on 6 November 2026.", "Senador electo y juramentado como vicepresidente el 6 de noviembre de 2026.", "src:abc-2026-11-06-en-vivo-juicio-politico", "20:10-20:18")
person("person:horacio-cartes", "Horacio Cartes", "Former president; president of the Colorado Party (ANR).", "Expresidente; titular del Partido Colorado (ANR).", "src:infobae-2026-11-05-cartes", "body")
person("person:rafael-filizzola", "Rafael Filizzola", "Senator (PDP); requested BCP reports and co-signed the criminal complaint against Peña.", "Senador (PDP); pidió informes al BCP y firmó la denuncia penal contra Peña.", "src:abc-2026-10-19-filizzola", "body")
person("person:rocio-vallejo", "Rocío Vallejo", "Deputy (Patria Querida); one of the deputies prosecuting the impeachment.", "Diputada (Patria Querida); una de las fiscales acusadoras del juicio político.", "src:abc-2026-11-19-denuncia-rolon", "body")
person("person:yolanda-paredes", "Yolanda Paredes", "Senator (Cruzada Nacional).", "Senadora (Cruzada Nacional).", "src:abc-2026-11-19-denuncia-rolon", "body")
person("person:jorge-schreiner", "Jorge Schreiner", "President of the Central Bank of Paraguay approved by the Senate on 9 November 2026.", "Presidente del BCP con acuerdo del Senado del 9 de noviembre de 2026.", "src:5dias-2026-11-18-especial-ueno", "9 Nov entry")
person("person:pedro-acosta", "Pedro de Jesús Acosta Bernal", "BCP board member; reported as interim president from 4 November 2026.", "Miembro del directorio del BCP; reportado como presidente interino desde el 4 de noviembre de 2026.", "src:5dias-2026-11-18-especial-ueno", "4 Nov entry", aliases=["Pedro Acosta", "Pedro Acosta Bernal"])
person("person:jose-maciel", "José Maciel", "Director of the Deposit Guarantee Fund (FGD).", "Director del Fondo de Garantía de Depósitos (FGD).", "src:afp-2026-11-10-retornos", "body")
person("person:raul-vera-bogado", "Raúl Vera Bogado", "Economist nominated by Peña to head the BCP in early November 2026 (Senate approval pending at the time).", "Economista propuesto por Peña para presidir el BCP a inicios de noviembre de 2026 (pendiente de acuerdo del Senado en ese momento).", "src:infobae-2026-11-05-cartes", "body")
person("person:carmen-marin", "Carmen Marín", "BCP board member who signed the 29 June 2026 memo to the Superintendency of Banks; resigned 29 October 2026.", "Directora del BCP que firmó el memorando del 29 de junio de 2026 a la Superintendencia de Bancos; renunció el 29 de octubre de 2026.", "src:abc-2026-10-16-gastos", "body")
person("person:fernando-rivarola", "Fernando Rivarola", "Author of the 10 July 2026 warning memo; approved by the Senate for the BCP board on 9 November 2026.", "Autor del dictamen de alerta del 10 de julio de 2026; con acuerdo del Senado para el directorio del BCP el 9 de noviembre de 2026.", ABC13, "chronology")
person("person:liana-caballero", "Liana Emilce Caballero Krauze", "Former BCP board member; charged in the related case.", "Exmiembro del directorio del BCP; imputada en la causa conexa.", ABC13, "body", aliases=["Liana Caballero", "Liana Caballero Krause"])
person("person:miguel-angel-mora", "Miguel Ángel Mora", "Former BCP board member; charged in the related case.", "Exmiembro del directorio del BCP; imputado en la causa conexa.", ABC13, "body", aliases=["Miguel Mora"])
person("person:marco-aurelio-gonzalez", "Marco Aurelio González Maldonado", "Former BCP board member and former Procurador General; charged in the related case.", "Exmiembro del directorio del BCP y exprocurador general; imputado en la causa conexa.", ABC13, "body", aliases=["Marco Aurelio González"])
person("person:aldo-rodriguez", "Aldo Javier Rodríguez González", "BCP legal director until his detention; listed among those deprived of liberty in Case 92/2026.", "Director jurídico del BCP hasta su detención; figura entre los privados de libertad en la Causa 92/2026.", ABC16, "item 17", aliases=["Aldo Rodríguez"])
person("person:andrea-benitez-garcia", "Andrea María José Benítez García", "Head of operations at Ueno Casa de Bolsa S.A.; charged with frustration of criminal prosecution.", "Jefa de operaciones de Ueno Casa de Bolsa S.A.; imputada por frustración de la persecución y ejecución penal.", ABC16, "item 10", aliases=["Andrea Benítez"])
person("person:carlos-fernandez-valdovinos", "Carlos Fernández Valdovinos", "Former Minister of Economy and Finance; reported as investigated but not charged.", "Exministro de Economía y Finanzas; reportado como investigado pero no imputado.", ABC16, "Otros")
person("person:lucca-de-barba", "Lucca de Barba", "Reported as former manager of Financial and Commercial Integration at Grupo Vázquez.", "Reportado como exgerente de Integración Financiera y Comercial del Grupo Vázquez.", "src:abc-2026-11-13-bolsones", "body", "medium") if False else None

# defence lawyers (professional role only)
for pid, label, en, es, src in (
    ("person:ricardo-preda", "Ricardo Preda", "Defence lawyer of Santiago Peña.", "Abogado defensor de Santiago Peña.", "src:ultimahora-2026-11-06-preda"),
    ("person:adolfo-ferreiro", "Adolfo Ferreiro", "Defence lawyer of Santiago Peña in the impeachment trial.", "Abogado defensor de Santiago Peña en el juicio político.", "src:abc-2026-11-06-en-vivo-juicio-politico"),
    ("person:guillermo-ferreiro", "Guillermo Ferreiro", "Defence lawyer of Julio Rey.", "Abogado defensor de Julio Rey.", ABC5),
    ("person:jose-miguel-fernandez-zacur", "José Miguel Fernández Zacur", "Defence lawyer of Juan Manuel Gustale, Alejandro Gómez Abente and Diego Duarte Schussmuller.", "Abogado defensor de Juan Manuel Gustale, Alejandro Gómez Abente y Diego Duarte Schussmuller.", ABC5),
    ("person:marcio-battilana", "Marcio Battilana", "Defence lawyer of Juan Manuel Gustale.", "Abogado defensor de Juan Manuel Gustale.", "src:ultimahora-2026-11-11-gustale-corte"),
    ("person:victor-dante-gulino", "Víctor Dante Gulino", "Defence lawyer of Miguel Vázquez until 9 November 2026.", "Abogado defensor de Miguel Vázquez hasta el 9 de noviembre de 2026.", "src:lanacion-2026-11-09-abogados-renuncian"),
    ("person:cristobal-caceres", "Cristóbal Cáceres", "Defence lawyer of Miguel Vázquez until 9 November 2026.", "Abogado defensor de Miguel Vázquez hasta el 9 de noviembre de 2026.", "src:lanacion-2026-11-09-abogados-renuncian"),
    ("person:alvaro-caceres", "Álvaro Cáceres Alsina", "Defence lawyer of Miguel Vázquez until 9 November 2026.", "Abogado defensor de Miguel Vázquez hasta el 9 de noviembre de 2026.", "src:lanacion-2026-11-09-abogados-renuncian"),
    ("person:christian-bernal", "Christian Bernal", "Defence lawyer of César Astigarraga.", "Abogado defensor de César Astigarraga.", "src:abc-2026-11-19-astigarraga-recurso"),
    ("person:andres-alvarez", "Andrés Álvarez", "Defence lawyer of Andrea Benítez García.", "Abogado defensor de Andrea Benítez García.", "src:riotimes-2026-11-11-benitez"),
    ("person:william-justiniano", "William Dante Justiniano", "Lawyer representing Grupo Vázquez S.A.E. in its third-party filing.", "Abogado que representa a Grupo Vázquez S.A.E. en su presentación como tercero.", "src:abc-2026-11-17-clan-vazquez"),
    ("person:laszlo-bencsik", "László Bencsik", "Deputy CEO of OTP Bank.", "Director general adjunto de OTP Bank.", "src:vg-2026-11-11-otp"),
    ("person:cesar-paredes", "César Paredes", "President of Cadiem Administradora de Fondos.", "Presidente de Cadiem Administradora de Fondos.", "src:5dias-2026-11-10-cadiem"),
):
    person(pid, label, en, es, src, "body")

def org(id_, type_, label, en, es, src, loc="body", aliases=None, bus_en="", bus_es=""):
    ENT(id_, type_, label, en, es, P("press", src, loc), aliases, bus_en, bus_es)

org("auth:juzgado-garantias-delitos-economicos-2", "Authority", "Juzgado Penal de Garantías Especializado en Delitos Económicos N.º 2", "Criminal guarantees court specialised in economic crimes (second shift), handling Case 89/2026.", "Juzgado penal de garantías especializado en delitos económicos (segundo turno), a cargo de la Causa 89/2026.", "src:abc-2026-11-17-clan-vazquez")
org("auth:tribunal-apelacion-delitos-economicos", "Authority", "Tribunal de Apelaciones Especializado en Delitos Económicos, Crimen Organizado y Anticorrupción", "Specialised appeals tribunal that reviewed detention in Case 89/2026.", "Tribunal de apelaciones especializado que revisó las medidas en la Causa 89/2026.", "src:elnacional-2026-11-10-agravan-cargos")
org("auth:corte-suprema-sala-penal", "Authority", "Sala Penal de la Corte Suprema de Justicia", "Criminal chamber of the Supreme Court, to which Gustale's defence appealed.", "Sala Penal de la Corte Suprema, ante la cual recurrió la defensa de Gustale.", "src:ultimahora-2026-11-11-gustale-corte")
org("auth:camara-de-diputados", "Authority", "Cámara de Diputados", "Lower house of Congress; brought the impeachment accusation.", "Cámara baja del Congreso; formuló la acusación en el juicio político.", "src:infobae-2026-11-05-cartes")
org("auth:seprelad", "Authority", "Secretaría de Prevención de Lavado de Dinero o Bienes (Seprelad)", "Anti-money-laundering secretariat.", "Secretaría de prevención de lavado de dinero o bienes.", "src:ultimahora-2026-11-05-seprelad")
org("auth:senabico", "Authority", "Secretaría Nacional de Administración de Bienes Incautados y Comisados (Senabico)", "Agency administering seized assets.", "Secretaría que administra los bienes incautados y comisados.", "src:efe-2026-11-08-incautaciones")
org("auth:mef", "Authority", "Ministerio de Economía y Finanzas (MEF)", "Ministry of Economy and Finance.", "Ministerio de Economía y Finanzas.", "src:ultimahora-2026-11-05-oposicion-denuncia")
org("auth:contraloria", "Authority", "Contraloría General de la República", "Comptroller General's office.", "Contraloría General de la República.", "src:5dias-2026-11-18-especial-ueno", "16 Nov entry")
org("auth:juzgado-civil-comercial-8", "Authority", "Juzgado de Primera Instancia en lo Civil y Comercial del Octavo Turno", "Civil and commercial court that ordered the preventive embargo requested by the BCP.", "Juzgado civil y comercial que dictó el embargo preventivo pedido por el BCP.", "src:ultimahora-2026-11-03-embargo")
org("org:bva", "Company", "Bolsa de Valores y Productos de Asunción (BVA)", "Asunción stock exchange.", "Bolsa de valores de Asunción.", "src:abc-2026-11-06-bva-suspende", aliases=["Bolsa de Valores de Asunción"], bus_en="Stock exchange", bus_es="Bolsa de valores")
org("org:ueno-holding", "Company", "Ueno Holding S.A.E.C.A.", "Group holding company, formerly Credicentro (founded 1984, renamed 2022).", "Holding del grupo, antes Credicentro (fundada en 1984, renombrada en 2022).", "src:forbesar-2026-11-03-financiera-a-banco", aliases=["Credicentro", "ueno Holding"], bus_en="Consumer credit / holding", bus_es="Crédito de consumo / holding")
org("org:valores-casa-de-bolsa", "Company", "Valores Casa de Bolsa S.A.", "Brokerage suspended by the BVA on 5 November 2026 for failed repo settlements.", "Casa de bolsa suspendida por la BVA el 5 de noviembre de 2026 por incumplir recompras de reporto.", "src:abc-2026-11-06-bva-suspende", bus_en="Brokerage", bus_es="Casa de bolsa")
org("org:puente-afpisa", "Company", "Puente AFPISA", "Fund administrator whose fund suspension was lifted on 6 November 2026.", "Administradora de fondos cuya suspensión fue levantada el 6 de noviembre de 2026.", "src:revistaplus-2026-11-06-levanta-restricciones", bus_en="Fund administration", bus_es="Administración de fondos")
org("org:balanz", "Company", "Balanz Capital", "Argentine financial group that signed a memorandum to acquire a majority of Cadiem.", "Grupo financiero argentino que firmó un acuerdo de entendimiento para adquirir la mayoría de Cadiem.", "src:lanacion-2026-11-17-balanz-cadiem", bus_en="Financial services", bus_es="Servicios financieros")
org("org:fitch", "Company", "Fitch Ratings", "International rating agency.", "Calificadora internacional.", "src:ultimahora-2026-10-16-fitch", bus_en="Credit ratings", bus_es="Calificación de riesgo")
org("org:moodys", "Company", "Moody's", "International rating agency.", "Calificadora internacional.", "src:expansion-2026-11-06-moodys", bus_en="Credit ratings", bus_es="Calificación de riesgo")
org("org:fix-scr", "Company", "FIX SCR", "Local rating agency.", "Calificadora local.", "src:lanacion-2026-11-06-fix-grupo-vazquez", bus_en="Credit ratings", bus_es="Calificación de riesgo")
org("org:idb-invest", "Company", "IDB Invest", "Private-sector arm of the Inter-American Development Bank group.", "Brazo del sector privado del Grupo BID.", "src:idbinvest-2024-11-18-loan", bus_en="Development finance", bus_es="Financiamiento para el desarrollo")
org("org:triodos-bank", "Company", "Triodos Bank", "Dutch bank that lent to ueno bank in August 2026.", "Banco neerlandés que financió a ueno bank en agosto de 2026.", "src:ueno-2026-08-06-triodos-gawa", bus_en="Banking", bus_es="Banca")
org("org:gawa-capital", "Company", "GAWA Capital", "Spanish impact investor that lent to ueno bank in August 2026.", "Gestora española de inversión de impacto que financió a ueno bank en agosto de 2026.", "src:ueno-2026-08-06-triodos-gawa", bus_en="Impact investment", bus_es="Inversión de impacto")
org("org:anr", "Company", "Asociación Nacional Republicana (Partido Colorado)", "Governing party.", "Partido de gobierno.", "src:infobae-2026-11-05-cartes", aliases=["ANR", "Partido Colorado"], bus_en="Political party", bus_es="Partido político")

# ---------------------------------------------------------------- roles: officials
def off(holder, org_, en, es, src, loc="body", conf="high", note="", start=None, end=None):
    R(holder, org_, "officer", en, es, P("press", src, loc, "", conf, note), start=start, end=end)

J2 = "auth:juzgado-garantias-delitos-economicos-2"
off("person:rodrigo-estigarribia", J2, "Judge of Case 89/2026 (criminal guarantees, economic crimes, second shift).", "Juez de la Causa 89/2026 (penal de garantías, delitos económicos, segundo turno).", "src:abc-2026-11-19-astigarraga-recurso")
off("person:humberto-otazu", "auth:ministerio-publico", "Duty guarantees judge who admitted the charges in Case 89/2026 on 4 Nov 2026; also judge in Case 92/2026 (org field is a placeholder: no court entity minted).", "Juez de garantías de turno que admitió la imputación en la Causa 89/2026 el 4/11/2026; también juez en la Causa 92/2026 (el campo org es un marcador: no se creó entidad para su juzgado).", "src:lanacion-2026-11-04-juez-admite", note="org is a placeholder; court of judge Otazú not minted as an entity")
off("person:osmar-legal", "auth:ministerio-publico", "Organised-crime guarantees judge reported in decisions on Peña (16 and 20 Nov 2026) (org field is a placeholder).", "Juez de garantías de crimen organizado reportado en decisiones sobre Peña (16 y 20/11/2026) (campo org es un marcador).", "src:ultimahora-2026-11-20-celulares", note="org is a placeholder. Conflict: Prensa Mercosur/ABC (12 Nov) names Legal, not Estigarribia, as the judge who ordered Astigarraga's detention")
off("person:walter-mendoza", "auth:juzgado-civil-comercial-8", "Civil and commercial judge who ordered the preventive embargo on 3 Nov 2026.", "Juez civil y comercial que dictó el embargo preventivo el 3/11/2026.", "src:ultimahora-2026-11-03-embargo")
for j in ("person:silvana-luraghi", "person:paublino-escobar", "person:claudia-criscioni"):
    off(j, "auth:tribunal-apelacion-delitos-economicos", "Appeals judge on the panel that upheld detention and added offences (ruling reported 10 Nov 2026).", "Camarista de la sala que confirmó la prisión y amplió los hechos punibles (fallo informado el 10/11/2026).", "src:elnacional-2026-11-10-agravan-cargos")
for j in ("person:claudia-criscioni", "person:silvana-luraghi", "person:arnaldo-fleitas"):
    off(j, "auth:tribunal-apelacion-delitos-economicos", "Appeals judge (first chamber) on the panel that declared Astigarraga's appeal inadmissible on 19 Nov 2026.", "Camarista (primera sala) de la sala que declaró inadmisible el recurso de Astigarraga el 19/11/2026.", "src:abc-2026-11-19-astigarraga-recurso")
MP = "auth:ministerio-publico"
for pr in ("person:jorge-arce", "person:silvio-corbeta", "person:yeimy-adle", "person:francisco-cabrera"):
    off(pr, MP, "Prosecutor who signed the charges of 4 Nov 2026 in Case 89/2026.", "Agente fiscal que firmó la imputación del 4/11/2026 en la Causa 89/2026.", "src:lanacion-2026-11-04-imputan-27", start="2026-11-03")
for pr in ("person:francisco-cabrera", "person:silvio-corbeta", "person:jorge-arce", "person:yeimy-adle", "person:ruth-benitez", "person:luz-guerrero", "person:luis-pinanez", "person:belinda-bobadilla"):
    off(pr, MP, "Member of the Case 89/2026 prosecution team as listed on 13 Nov 2026.", "Integrante del equipo fiscal de la Causa 89/2026 según la lista del 13/11/2026.", LN13, note="Date on which the additional prosecutors joined is not reported")
off("person:nancy-salomon", MP, "Deputy attorney general coordinating the Case 89/2026 team and the related-case team.", "Fiscal adjunta coordinadora del equipo de la Causa 89/2026 y del equipo de la causa conexa.", LN13)
off("person:manuel-doldan", MP, "Deputy attorney general, International Affairs; involved because of bonds and investments placed abroad.", "Fiscal adjunto de Asuntos Internacionales; interviene por bonos e inversiones colocados en el exterior.", "src:telefuturo-2026-11-03-directivos")
off("person:federico-leguizamon", MP, "Prosecutor assigned to the case against Andrea Benítez García.", "Agente fiscal de la causa contra Andrea Benítez García.", "src:abc-2026-11-10-benitez")
for pr in ("person:silvia-gonzalez-vester", "person:christian-benitez-caceres", "person:elena-fiore", "person:ruth-benitez", "person:laura-giacummo", "person:veronica-valdez", "person:marlene-gonzalez"):
    off(pr, MP, "Member of the prosecution team in the related case (Case 92/2026) against Santiago Peña and former BCP officials.", "Integrante del equipo fiscal de la causa conexa (Causa 92/2026) contra Santiago Peña y exautoridades del BCP.", "src:lanacion-2026-11-13-pena-carvallo-bcp")
off("person:emiliano-rolon", MP, "Attorney General; designated the first prosecution team on 3 Nov 2026; resigned 17 Nov 2026.", "Fiscal general del Estado; designó el primer equipo fiscal el 3/11/2026; renunció el 17/11/2026.", "src:dw-2026-11-17-rolon", start="2023-03", end="2026-11-17")
off("person:alba-rocio-cantero", MP, "Interim Attorney General; formalised by Resolution N.º 4665 on 18 Nov 2026 per 5Días.", "Fiscal general interina; formalizada por Resolución N.º 4665 el 18/11/2026 según 5Días.", "src:5dias-2026-11-18-especial-ueno", "18 Nov entry", start="2026-11-17")
R("person:jorge-schreiner", "auth:bcp", "president", "President of the BCP; Senate approval 9 Nov 2026.", "Presidente del BCP; acuerdo del Senado el 9/11/2026.", P("press", "src:5dias-2026-11-18-especial-ueno", "9 Nov entry"), start="2026-11-09")
R("person:pedro-acosta", "auth:bcp", "director", "BCP board member; interim president from 4 Nov 2026 per 5Días.", "Miembro del directorio del BCP; presidente interino desde el 4/11/2026 según 5Días.", P("press", "src:5dias-2026-11-18-especial-ueno", "4 Nov entry", "", "medium", "Conflict: La Política Online (13 Nov) and ABC (14, 16 Nov) describe Liana Caballero (and ABC also Mora) as interim BCP president after Carvallo's resignation"), start="2026-11-04")
R("person:jose-maciel", "auth:fgd", "officer", "Director of the Deposit Guarantee Fund.", "Director del Fondo de Garantía de Depósitos.", P("press", "src:afp-2026-11-10-retornos", "body"))
R("person:carlos-carvallo", "auth:bcp", "president", "BCP president appointed by Decree N.º 214 of 7 Sep 2023 (prosecution chronology); signed his resignation on 3 Nov 2026 (AP).", "Presidente del BCP designado por Decreto N.º 214 del 7/9/2023 (cronología fiscal); firmó su renuncia el 3/11/2026 (AP).", P("prosecution", ABC13, "chronology", "", "high", "5Días says he led the regulator 'from August' 2023"), start="2023-09-07", end="2026-11-03")
R("person:carlos-carvallo", "org:financiera-el-comercio", "president", "President of Financiera Ueno until 14 Aug 2023 according to the prosecution chronology.", "Presidente de Financiera Ueno hasta el 14/8/2023 según la cronología fiscal.", P("prosecution", ABC13, "chronology", "", "medium", "Conflict: 5Días and Infobae say until July 2023; Paperjam says August 2023. org id used for the finance company later converted into ueno bank"), end="2023-08-14")
R("person:holger-insfran", "auth:superintendencia-de-bancos", "officer", "Superintendent of Banks until his detention on 12 Nov 2026.", "Superintendente de Bancos hasta su detención el 12/11/2026.", P("press", ABC16, "item 13"), end="2026-11-12")
for h in ("person:liana-caballero", "person:miguel-angel-mora", "person:marco-aurelio-gonzalez"):
    R(h, "auth:bcp", "director", "Former member of the BCP board.", "Exmiembro del directorio del BCP.", P("press", ABC16, "items 14-16"))
R("person:aldo-rodriguez", "auth:bcp", "officer", "Legal director of the BCP until his detention.", "Director jurídico del BCP hasta su detención.", P("press", ABC16, "item 17"))
R("person:carmen-marin", "auth:bcp", "director", "BCP board member; resigned 29 Oct 2026.", "Directora del BCP; renunció el 29/10/2026.", P("press", "src:5dias-2026-11-18-especial-ueno", "29 Oct entry"), end="2026-10-29")
R("person:andrea-benitez-garcia", "org:ueno-casa-de-bolsa", "employee", "Head of operations at Ueno Casa de Bolsa S.A.", "Jefa de operaciones de Ueno Casa de Bolsa S.A.", P("press", ABC16, "item 10"))
R("person:juan-manuel-gustale", "org:u-holdings", "director", "Appointed category B manager of U Holdings on 1 Jul 2026.", "Designado gerente de categoría B de U Holdings el 1/7/2026.", P("press", "src:ultimahora-2026-11-12-luxemburgo-salida", "body"), start="2026-07-01")
R("person:alejandro-gomez-abente", "org:u-holdings", "director", "Appointed category B manager of U Holdings on 1 Jul 2026.", "Designado gerente de categoría B de U Holdings el 1/7/2026.", P("press", "src:ultimahora-2026-11-12-luxemburgo-salida", "body"), start="2026-07-01")
R("org:otp-bank", "org:u-holdings", "shareholder", "9.99% of U Holdings for a total of USD 47 million; less than 1% of voting rights per Paperjam.", "9,99 % de U Holdings por un total de USD 47 millones; menos del 1 % de los votos según Paperjam.", P("press", "src:paperjam-2026-11-luxembourg", "body", "", "medium", "ueno's own 3 Jun 2026 release called OTP the company's 'main shareholder'; Paperjam/EFE/Forbes give Grupo Vázquez 86.73%"), pct=9.99)
R("org:grupo-vazquez", "org:u-holdings", "shareholder", "86.73% of U Holdings as published at 20 Oct 2026.", "86,73 % de U Holdings según lo publicado al 20/10/2026.", P("press", "src:forbesar-2026-11-03-financiera-a-banco", "ownership paragraph"), pct=86.73)
R("org:u-holdings", "org:u-paraguay", "shareholder", "U Holdings holds 100% of U Paraguay.", "U Holdings posee el 100 % de U Paraguay.", P("press", "src:ultimahora-2026-11-12-luxemburgo-salida", "body"), pct=100)
R("org:u-paraguay", "org:ueno-bank", "shareholder", "U Paraguay holds 93.17% of ueno bank.", "U Paraguay posee el 93,17 % de ueno bank.", P("press", "src:ultimahora-2026-11-12-luxemburgo-salida", "body"), pct=93.17)

# ---------------------------------------------------------------- roles: accused, as reported per outlet
ROLE_ROWS = [
 # holder, org, role, es wording, source, note
 ("person:miguel-vazquez", "org:ueno-bank", "vice_president", "vicepresidente primero de Ueno Bank", LN13, "Conflict: ABC 5 Nov 'ex-CEO y ex vicepresidente 1.º'; El Nacional 10 Nov 'exdirector ejecutivo'; AP 3 Nov 'CEO'; Independiente 'beneficiario final y vicepresidente primero'"),
 ("person:miguel-vazquez", "org:grupo-vazquez", "president", "presidente de Grupo Vázquez", LN13, ""),
 ("person:miguel-vazquez", "org:ueno-bank", "beneficial_owner", "beneficiario final (según la imputación)", "src:independiente-2026-11-04-imputacion", ""),
 ("person:juan-manuel-gustale", "org:ueno-bank", "president", "presidente de Ueno Bank", LN13, ""),
 ("person:julio-rey", "org:ueno-bank", "vice_president", "exvicepresidente segundo de Ueno Bank", LN13, "Extra (20 Nov): removed from the board four months before the intervention"),
 ("person:diana-mongelos", "org:ueno-bank", "vice_president", "vicepresidenta segunda de Ueno Bank", LN13, "Conflict: Última Hora 5 Nov and ABC 5 Nov say 'directora titular'; Telefuturo 3 Nov and ABC 16 Nov say 'vicepresidenta segunda'"),
 ("person:diana-mongelos", "org:ueno-bank", "director", "directora titular", UH5, "Conflict with La Nación 13 Nov ('vicepresidenta segunda')"),
 ("person:mariana-torres", "org:ueno-bank", "director", "exdirectora titular de Ueno Bank", LN13, ""),
 ("person:alejandro-gomez-abente", "org:ueno-bank", "director", "director titular de Ueno Bank", LN13, ""),
 ("person:diego-duarte", "org:ueno-bank", "director", "director titular de Ueno Bank", LN13, ""),
 ("person:diego-duarte", "org:ueno-seguros", "vice_president", "vicepresidente primero de Ueno Seguros", LN13, ""),
 ("person:miguel-angel-almada", "org:ueno-bank", "statutory_auditor", "exsíndico titular de Ueno Bank", LN13, "Última Hora 5 Nov and ABC 5 Nov: 'síndico titular' (not 'ex')"),
 ("person:jose-augusto-sala-cardozo", "org:mowi", "president", "presidente y representante legal de MOWI S.A.", LN13, "Última Hora 5 Nov adds 'accionista'"),
 ("person:jose-augusto-sala-cardozo", "org:mowi", "legal_representative", "representante legal de MOWI S.A.", LN13, ""),
 ("person:sergio-pizurno", "org:mowi", "vice_president", "vicepresidente de MOWI S.A.", LN13, "Última Hora 5 Nov adds 'accionista'"),
 ("person:sergio-pizurno", "org:grupo-m", "director", "director titular de Grupo M S.A.", LN13, ""),
 ("person:vanessa-godoy", "org:grupo-hendy", "president", "presidenta de Grupo Hendy S.A.", LN13, "Última Hora 5 Nov: 'accionista; vicepresidenta, luego presidenta'"),
 ("person:cesar-mengual", "org:grupo-hendy", "president", "presidente de Grupo Hendy S.A.", LN13, "La Nación lists both Godoy and Mengual as president of Grupo Hendy; periods not given"),
 ("person:miguel-angel-garay", "org:grupo-hendy", "director", "director titular de Grupo Hendy S.A.", LN13, ""),
 ("person:oscar-urdapilleta", "org:grupo-m", "vice_president", "vicepresidente de Grupo M S.A.", LN13, ""),
 ("person:oscar-urdapilleta", "org:grupo-hendy", "vice_president", "accionista; presidente, luego vicepresidente de Grupo Hendy S.A.", UH5, "Only Última Hora 5 Nov links Urdapilleta to Grupo Hendy"),
 ("person:luis-ernesto-angulo", "org:grupo-m", "group_role", "vinculado a Grupo M S.A.", LN13, "Conflict: Última Hora 5 Nov says 'vicepresidente' of Grupo M"),
 ("person:luis-ernesto-angulo", "org:grupo-m", "vice_president", "vicepresidente de Grupo M S.A.", UH5, "Conflict with La Nación 13 Nov ('vinculado')"),
 ("person:guillermo-vazquez", "org:grupo-m", "director", "director titular de Grupo M S.A.", LN13, "Telefuturo 3 Nov lists a 'Guillermo Vázquez' as alternate director of the bank; no source read states it is the same person"),
 ("person:diego-gomez", "org:grupo-m", "president", "presidente de Grupo M S.A.", LN13, "Última Hora 5 Nov adds 'accionista'"),
 ("person:cesar-astigarraga", "org:itti", "president", "presidente y CEO de ITTI S.A.E.C.A.", LN13, "Conflict: Última Hora 5 Nov lists him as 'presidente' of Grupo M S.A.; ABC 19 Nov says president of Itti and of Grupo M and 'síndico suplente' of Ueno Bank"),
 ("person:cesar-astigarraga", "org:grupo-m", "president", "presidente de Grupo M S.A.", UH5, "Conflict with La Nación 13 Nov, which gives Diego Gómez Arce as president of Grupo M"),
 ("person:cesar-astigarraga", "org:ueno-bank", "alternate_statutory_auditor", "síndico suplente de Ueno Bank", "src:abc-2026-11-19-astigarraga-recurso", "Only ABC reports this role"),
 ("person:luis-fernando-rios", "org:tuiu", "vice_president", "vicepresidente de TUIU S.A.", LN13, "Última Hora 5 Nov adds 'accionista'"),
 ("person:andre-gayol-pires", "org:tuiu", "beneficial_owner", "accionista y beneficiario final de TUIU S.A.", LN13, "Última Hora 4 Nov spells 'Andrés Gayol Pires'"),
 ("person:nicolas-di-iorio", "org:tuiu", "beneficial_owner", "accionista y beneficiario final de TUIU S.A.", LN13, ""),
 ("person:rodrigo-franco", "org:tuiu", "president", "presidente y representante legal de TUIU S.A.", LN13, ""),
 ("person:mauro-vargas", "org:franede", "president", "presidente y accionista de FRANDEDE S.A.", LN13, "Company spelled 'Frandede' and 'Franede' interchangeably across outlets"),
 ("person:mauro-vargas", "org:aime", "shareholder", "accionista de AIME S.A. Corredores de Seguros", LN13, ""),
 ("person:cecilia-dominguez", "org:franede", "vice_president", "vicepresidenta de FRANDEDE S.A.", LN13, ""),
 ("person:martin-vargas", "org:aime", "shareholder", "accionista de AIME S.A. Corredores de Seguros", LN13, ""),
 ("person:gloria-villasanti", "org:aime", "president", "presidenta de AIME S.A. Corredores de Seguros", LN13, "Última Hora 5 Nov adds 'directora suplente de Mowi'"),
 ("person:raul-sanchez", "org:aime", "director", "director titular de AIME S.A. Corredores de Seguros", LN13, ""),
]
for holder, org_, role, es, src, note in ROLE_ROWS:
    R(holder, org_, role, "Role as reported by the outlet (Spanish wording kept in note_es).", es, P("press", src, "list of the 27", "", "high" if not note.startswith("Conflict") else "medium", note))

# ---------------------------------------------------------------- accused table
O4 = ["lesión de confianza", "conducta indebida en situaciones de crisis", "tentativa de estafa", "violación de la obligación de llevar libros de comercio"]
OADD = ["estafa agravada (en lugar de tentativa de estafa)", "lavado de activos", "asociación criminal"]
NOTE_OFF = ("Original four offences per La Nación (4 and 13 Nov). 'offences_added' = offences added of its own motion by the Appeals Tribunal (ruling reported 10 Nov), "
            "listed for all eight bank defendants by ABC on 16 Nov. Conflict: El Nacional frames the expansion around the four appellants; La Nación (13 Nov) still lists only the original four; "
            "Gustale's defence has challenged the expansion before the Supreme Court. All charges are allegations; presumption of innocence applies.")
NOHEAR = "none reported"
bank = [
 ("person:miguel-vazquez", "Federico Miguel Vázquez Villasanti", "First vice-president of Ueno Bank; president of Grupo Vázquez", "vicepresidente primero de Ueno Bank y presidente de Grupo Vázquez", "pretrial_prison",
  "No statement on the merits reported. On 3 Nov his then lawyer said he surrendered voluntarily on learning of the order; on 6 Nov the defence appealed, citing family and work ties and offering real-estate surety, and asked for house arrest with electronic monitoring; his three lawyers resigned on 9 Nov (reasons not given).",
  "No se reportó declaración sobre el fondo. El 3/11 su entonces abogado dijo que se presentó voluntariamente al conocer la orden; el 6/11 la defensa apeló invocando arraigo familiar y laboral y ofreciendo caución real, y pidió arresto domiciliario con monitoreo electrónico; sus tres abogados renunciaron el 9/11 (sin motivo informado).",
  {"offences_added": OADD + ["conducta conducente a la quiebra"], "place_reported": "Centro Nacional de Prevenidos (ex-Tacumbú)"}),
 ("person:juan-manuel-gustale", "Juan Manuel Gustale Cardoni", "President of Ueno Bank", "presidente de Ueno Bank", "pretrial_prison",
  "At the 5 Nov hearing his lawyer accepted the alternative measures requested by the prosecution and offered real-estate surety. On 11 Nov the defence was reported to have gone to the Supreme Court's criminal chamber against the appeals ruling that added offences, arguing the tribunal acted as an original decision-maker, not a reviewer. Before the collapse (reported 21 Oct) he denied indirect financing of the portfolio sale.",
  "En la audiencia del 5/11 su abogado se allanó a las medidas alternativas pedidas por la Fiscalía y ofreció caución real. El 11/11 se informó que la defensa recurrió a la Sala Penal de la Corte contra el fallo de apelación que amplió los hechos punibles, alegando que el tribunal actuó como órgano de decisión originaria y no revisor. Antes de la caída (publicado el 21/10) negó la financiación indirecta de la venta de cartera.",
  {"offences_added": OADD, "place_reported": "Centro Nacional de Prevenidos (ex-Tacumbú)"}),
 ("person:julio-rey", "Julio Daniel Rey Fernández", "Former second vice-president of Ueno Bank", "exvicepresidente segundo de Ueno Bank", "pretrial_prison",
  "His lawyer filed a habeas corpus (rejected) and offered personal and real surety on 5 Nov. He gave a voluntary statement to prosecutors in mid-November (18 Nov per El Nacional; 'last Tuesday' per Extra) and handed over documents; the lawyer says he will answer for what he did but not for acts outside his functions, that he had been removed from the board before the resolution, and that he wants to cooperate.",
  "Su abogado planteó un habeas corpus (rechazado) y ofreció caución personal y real el 5/11. Declaró voluntariamente ante la Fiscalía a mediados de noviembre (18/11 según El Nacional; 'el pasado martes' según Extra) y entregó documentos; el abogado dice que responderá por lo que hizo pero no por actos ajenos a sus funciones, que fue apartado del directorio antes de la resolución y que quiere colaborar.",
  {"offences_added": OADD, "place_reported": "Centro Nacional de Prevenidos (ex-Tacumbú)"}),
 ("person:diana-mongelos", "Diana Leticia Mongelós González", "Second vice-president of Ueno Bank", "vicepresidenta segunda de Ueno Bank", "house_arrest",
  "No defence submissions or statements reported.", "No se reportaron planteos ni declaraciones de la defensa.",
  {"offences_added": OADD, "place_reported": "arresto domiciliario con tobillera electrónica"}),
 ("person:mariana-torres", "Mariana Torres Rubiani", "Former titular director of Ueno Bank", "exdirectora titular de Ueno Bank", "house_arrest",
  "No defence submissions or statements reported.", "No se reportaron planteos ni declaraciones de la defensa.",
  {"offences_added": OADD, "place_reported": "arresto domiciliario con tobillera electrónica"}),
 ("person:alejandro-gomez-abente", "Alejandro Gómez Abente", "Titular director of Ueno Bank", "director titular de Ueno Bank", "pretrial_prison",
  "At the 5 Nov hearing his lawyer accepted the alternative measures requested by the prosecution and offered real-estate surety. No statement on the merits reported.",
  "En la audiencia del 5/11 su abogado se allanó a las medidas alternativas pedidas por la Fiscalía y ofreció caución real. Sin declaración sobre el fondo.",
  {"offences_added": OADD, "place_reported": "Centro Nacional de Prevenidos (ex-Tacumbú)"}),
 ("person:diego-duarte", "Diego Fernando Duarte Schussmuller", "Titular director of Ueno Bank; first vice-president of Ueno Seguros", "director titular de Ueno Bank y vicepresidente primero de Ueno Seguros", "pretrial_prison",
  "At the 5 Nov hearing his lawyer accepted the alternative measures requested by the prosecution and offered real-estate surety; the judge gave the defence 15 days to file appraisals of two properties. No statement on the merits reported.",
  "En la audiencia del 5/11 su abogado se allanó a las medidas alternativas pedidas por la Fiscalía y ofreció caución real; el juez dio 15 días a la defensa para presentar tasaciones de dos inmuebles. Sin declaración sobre el fondo.",
  {"offences_added": OADD, "place_reported": "Conflict: Penitenciaría Padre Juan de la Vega, Emboscada (ABC 5 Nov) vs Centro Nacional de Prevenidos (ABC 16 Nov)"}),
 ("person:miguel-angel-almada", "Miguel Ángel Almada Frutos", "Former titular statutory auditor (síndico) of Ueno Bank", "exsíndico titular de Ueno Bank", "pretrial_prison",
  "At the 5 Nov hearing his lawyers offered personal sureties. No statement on the merits reported.",
  "En la audiencia del 5/11 sus abogados ofrecieron fiadores personales. Sin declaración sobre el fondo.",
  {"offences_added": OADD, "place_reported": "Penitenciaría de Emboscada (ABC 5 and 16 Nov)"}),
]
for pid, label, ren, res, measure, den, des, extra in bank:
    nh = "none reported; defence given 15 days from 5 Nov 2026 to file property appraisals" if pid == "person:diego-duarte" else NOHEAR
    A(pid, label, ren, res, "org:ueno-bank", O4, measure, "2026-11-05", nh, den, des,
      P("press", LN13, "list of the 27; measures from ABC 5 Nov (A.I. N.º 359) and ABC 16 Nov", "", "high", NOTE_OFF),
      case="89/2026", measure_source="src:abc-2026-11-05-juez-envia-prision", status_source=ABC16, **extra)

N18 = ("Charged with the same four offences as the rest of the 27 (not broken down per person in any article read). Prosecution requested travel ban and surety (Independiente) / 'libertad ambulatoria' (Última Hora 5 Nov); "
       "to be summoned to a measures hearing whose date is not reported; subject to the general inhibition and account freeze reported on 5 Nov; ABC (16 Nov) says the other 18 company-linked defendants remain at liberty. "
       "No per-person measure ruling found. Presumption of innocence applies.")
others = [
 ("person:jose-augusto-sala-cardozo", "José Augusto Sala Cardozo", "President and legal representative of MOWI S.A.", "presidente y representante legal de MOWI S.A.", "org:mowi", ""),
 ("person:sergio-pizurno", "Sergio Amado Pizurno Zsarán", "Vice-president of MOWI S.A.; titular director of Grupo M S.A.", "vicepresidente de MOWI S.A. y director titular de Grupo M S.A.", "org:mowi", "Surname spelled 'Zsarán' (La Nación) and 'Szarán' (Última Hora 4 Nov)."),
 ("person:vanessa-godoy", "Vanessa Esther Godoy Ayala", "President of Grupo Hendy S.A.", "presidenta de Grupo Hendy S.A.", "org:grupo-hendy", ""),
 ("person:oscar-urdapilleta", "Óscar Urdapilleta", "Vice-president of Grupo M S.A.", "vicepresidente de Grupo M S.A.", "org:grupo-m", "Última Hora (5 Nov) also lists him under Grupo Hendy (shareholder; president, later vice-president)."),
 ("person:cesar-mengual", "César Javier Mengual Mazacotte", "President of Grupo Hendy S.A.", "presidente de Grupo Hendy S.A.", "org:grupo-hendy", ""),
 ("person:miguel-angel-garay", "Miguel Ángel Garay", "Titular director of Grupo Hendy S.A.", "director titular de Grupo Hendy S.A.", "org:grupo-hendy", ""),
 ("person:luis-ernesto-angulo", "Luis Ernesto Angulo Rivera", "Linked to Grupo M S.A.", "vinculado a Grupo M S.A.", "org:grupo-m", "Conflict: Última Hora (5 Nov) says vice-president of Grupo M. Omitted from Última Hora's 4 Nov list."),
 ("person:guillermo-vazquez", "Guillermo Vázquez Muniagurria", "Titular director of Grupo M S.A.", "director titular de Grupo M S.A.", "org:grupo-m", ""),
 ("person:diego-gomez", "Diego Sebastián Gómez Arce", "President of Grupo M S.A.", "presidente de Grupo M S.A.", "org:grupo-m", ""),
 ("person:luis-fernando-rios", "Luis Fernando Ríos Espínola", "Vice-president of TUIU S.A.", "vicepresidente de TUIU S.A.", "org:tuiu", ""),
 ("person:andre-gayol-pires", "André Gayol Pires", "Shareholder and beneficial owner of TUIU S.A.", "accionista y beneficiario final de TUIU S.A.", "org:tuiu", ""),
 ("person:nicolas-di-iorio", "Nicolás S. Di Iorio Olivares", "Shareholder and beneficial owner of TUIU S.A.", "accionista y beneficiario final de TUIU S.A.", "org:tuiu", ""),
 ("person:rodrigo-franco", "Rodrigo Ramón Franco Ortiz", "President and legal representative of TUIU S.A.", "presidente y representante legal de TUIU S.A.", "org:tuiu", ""),
 ("person:mauro-vargas", "Mauro Vargas Wildberger", "President and shareholder of FRANDEDE S.A.; shareholder of AIME S.A.", "presidente y accionista de FRANDEDE S.A. y accionista de AIME S.A.", "org:franede", "Company spelled 'Frandede'/'Franede'."),
 ("person:cecilia-dominguez", "Cecilia Domínguez Elizeche", "Vice-president of FRANDEDE S.A.", "vicepresidenta de FRANDEDE S.A.", "org:franede", ""),
 ("person:martin-vargas", "Martín Vargas Wildberger", "Shareholder of AIME S.A. Corredores de Seguros", "accionista de AIME S.A. Corredores de Seguros", "org:aime", ""),
 ("person:gloria-villasanti", "Gloria Villasanti Farinha", "President of AIME S.A. Corredores de Seguros", "presidenta de AIME S.A. Corredores de Seguros", "org:aime", ""),
 ("person:raul-sanchez", "Raúl Fernando Sánchez Gómez", "Titular director of AIME S.A. Corredores de Seguros", "director titular de AIME S.A. Corredores de Seguros", "org:aime", ""),
]
for pid, label, ren, res, comp, extra_note in others:
    A(pid, label, ren, res, comp, O4, "none_reported", None, "measures hearing to be scheduled; date not reported",
      "No public statement found.", "No se encontró declaración pública.",
      P("press", LN13, "list of the 27", "", "medium", (extra_note + " " + N18).strip()), case="89/2026")

A("person:cesar-astigarraga", "César Manuel Astigarraga Lambaré", "President and CEO of ITTI S.A.E.C.A.", "presidente y CEO de ITTI S.A.E.C.A.", "org:itti", O4, "pretrial_prison", "2026-11-12", NOHEAR,
  "His lawyer argued that voluntary surrender disproves flight risk and that there are no valid grounds for detention; the Appeals Tribunal declared the appeal inadmissible on 19 Nov.",
  "Su abogado sostuvo que la presentación voluntaria desvirtúa el peligro de fuga y que no hay fundamentos valederos para la prisión; el Tribunal de Apelación declaró inadmisible el recurso el 19/11.",
  P("press", "src:abc-2026-11-19-astigarraga-recurso", "body", "", "medium",
    "Conflicts: (1) role: La Nación 'presidente y CEO de ITTI'; Última Hora 5 Nov 'presidente de Grupo M'; ABC 'presidente de Itti y de Grupo M, síndico suplente de Ueno Bank'. (2) offences: ABC 19 Nov lists the original four; ABC 12/16 Nov list lavado de activos, estafa agravada, conducta indebida, lesión de confianza, asociación criminal. "
    "(3) judge: Estigarribia (ABC 19 Nov) vs Osmar Legal (ABC via Prensa Mercosur 12 Nov). (4) place: ex-Tacumbú (12 and 16 Nov) vs Martín Mendoza, Emboscada (19 Nov). (5) detention order: in force since 5 Nov (ABC) vs requested by prosecutor Corbeta on 10 Nov (Última Hora). Presumption of innocence applies."),
  case="89/2026", offences_added=["lavado de activos", "estafa agravada", "asociación criminal"], place_reported="Conflict: Centro Nacional de Prevenidos (ex-Tacumbú) vs cárcel de máxima seguridad Martín Mendoza, Emboscada")

A("person:andrea-benitez-garcia", "Andrea María José Benítez García", "Head of operations at Ueno Casa de Bolsa S.A. (not one of the 27)", "jefa de operaciones de Ueno Casa de Bolsa S.A. (no integra los 27)", "org:ueno-casa-de-bolsa",
  ["frustración de la persecución y ejecución penal"], "house_arrest", "2026-11-19", NOHEAR,
  "Her lawyer said she had already cooperated and handed over documents and called the prosecution's account fanciful; ABC reports she told prosecutors the torn papers were unsigned draft resolutions and contracts.",
  "Su abogado dijo que ya había colaborado y entregado documentos y calificó de fantasiosa la versión fiscal; ABC informa que ella dijo a la Fiscalía que los papeles rotos eran proyectos de resoluciones y contratos sin firmar.",
  P("press", ABC16, "item 10", "", "medium", "Detained 9 Nov; pre-trial detention ordered 11 Nov (judge Marcelo Saldívar per Rio Times); house arrest with ankle monitor reported 19 Nov (Última Hora 20 Nov). ABC lists her under Causa 89/2026; headline of ABC 10 Nov says she 'abstained' while its body says she declared briefly. Presumption of innocence applies."),
  case="89/2026 (separate charge, as listed by ABC)", previous_measure="pretrial_prison (2026-11-11)")

REL = "92/2026"
A("person:santiago-pena", "Santiago Peña Palacios", "Former President of the Republic (removed by the Senate on 6 Nov 2026)", "expresidente de la República (destituido por el Senado el 6/11/2026)", None,
  ["lesión de confianza (instigador)", "administración en provecho propio (autor)", "asociación criminal (autor; ampliación del 13/11/2026)"], "pretrial_prison", "2026-11-07",
  "2026-11-27 09:30: swearing-in of the expert for extraction of data from three phones (not a hearing on the merits)",
  "Declares himself innocent; abstained from testifying on 7 Nov. Lawyer Ricardo Preda: Peña held no direct shares in the bank, only a stake in Ueno Holding sold by buyout (dated variously April 2025 or late 2024/early 2025) and audited by the Comptroller; the president does not tell agencies where to deposit; no act or file signed by Peña favouring the bank is identified; expects dismissal. No lawyer's response to the 13 Nov criminal-association charge was found.",
  "Se declara inocente; se abstuvo de declarar el 7/11. El abogado Ricardo Preda: Peña no tenía acciones directas del banco sino una participación en Ueno Holding vendida mediante rescate (fechada en abril de 2025 o fines de 2024/inicios de 2025) y auditada por la Contraloría; el presidente no indica a los entes dónde depositar; no se identifica acto ni expediente firmado por Peña a favor del banco; espera el sobreseimiento. No se halló respuesta de sus abogados a la imputación por asociación criminal del 13/11.",
  P("press", ABC13, "Acta de imputación N.º 9", "", "high", "Related case (Causa 92/2026 per ABC 6 and 16 Nov). Held at Regimiento Escolta Presidencial, then moved to Viñas Cué military prison by order of 16 Nov. Presumption of innocence applies."), case=REL, place_reported="Regimiento Escolta Presidencial; traslado a Viñas Cué ordenado el 16/11/2026")
A("person:carlos-carvallo", "Carlos Dagoberto Carvallo Spalding", "Former president of the BCP; former president of Financiera Ueno", "expresidente del BCP; expresidente de Financiera Ueno", "auth:bcp",
  ["lesión de confianza", "producción inmediata de documentos públicos de contenido falso", "administración en provecho propio", "asociación criminal (ampliación del 13/11/2026)"], "pretrial_prison", "2026-11-07", NOHEAR,
  "Abstained from testifying on 7 Nov; told prosecutors he fears for his life without giving details. No statement on the merits from his lawyers was reported.",
  "Se abstuvo de declarar el 7/11; dijo a los fiscales que teme por su vida, sin dar detalles. No se reportó declaración de sus abogados sobre el fondo.",
  P("press", "src:abc-2026-11-08-carvallo", "body", "", "high", "Conflict on surrender date: Friday 6 Nov (Infobae, Rio Times, ABC 16 Nov 'desde la noche del viernes') vs 7 Nov (La Política Online). ABC 16 Nov omits 'administración en provecho propio' from his list. Presumption of innocence applies."), case=REL, place_reported="Agrupación Especializada")
A("person:holger-insfran", "Holger Aníbal Insfrán Ibarrola", "Superintendent of Banks of the BCP (until his detention)", "superintendente de Bancos del BCP (hasta su detención)", "auth:superintendencia-de-bancos",
  ["lesión de confianza grave", "asociación criminal (ampliación del 13/11/2026)"], "pretrial_prison", None, NOHEAR,
  "No statement from him or his defence was found.", "No se halló declaración suya ni de su defensa.",
  P("press", ABC16, "item 13", "", "medium", "Detained 12 Nov 2026; prosecution requested pre-trial detention; ABC (16 Nov) lists him in pre-trial detention at the Agrupación Especializada; date of the ruling not stated. Presumption of innocence applies."), case=REL, detained="2026-11-12", place_reported="Agrupación Especializada")
A("person:marco-aurelio-gonzalez", "Marco Aurelio González Maldonado", "Former member of the BCP board", "exmiembro del directorio del BCP", "auth:bcp",
  ["lesión de confianza grave", "producción inmediata de documentos públicos de contenido falso", "uso de documentos públicos de contenido falso", "asociación criminal"], "pretrial_prison", None, NOHEAR,
  "No statement from him or his defence was found.", "No se halló declaración suya ni de su defensa.",
  P("press", ABC13, "body", "", "medium", "Detained 13 Nov 2026 after presenting himself (Comisaría 1.ª, Sajonia per La Nación; Dirección de Crimen Organizado per La Política Online). Prosecution requested pre-trial detention; ABC (16 Nov) lists him in pre-trial detention; ruling date not stated. Presumption of innocence applies."), case=REL, detained="2026-11-13", place_reported="Agrupación Especializada")
A("person:liana-caballero", "Liana Emilce Caballero Krauze", "Former BCP board member; reported as interim BCP president after Carvallo's resignation", "exmiembro del directorio del BCP; reportada como presidenta interina tras la renuncia de Carvallo", "auth:bcp",
  ["lesión de confianza grave", "asociación criminal"], "pretrial_prison", None, NOHEAR,
  "No statement from her or her defence was found.", "No se halló declaración suya ni de su defensa.",
  P("press", ABC13, "body", "", "medium", "Detained 13 Nov 2026. Conflict: prosecution requested house arrest with ankle monitor (ABC 13 Nov) but ABC (16 Nov) lists her in pre-trial detention (Departamento Judicial Femenino); ruling date not stated. Surname spelled Krauze/Krause. Presumption of innocence applies."), case=REL, detained="2026-11-13", measure_requested="house_arrest", place_reported="Departamento Judicial Femenino")
A("person:miguel-angel-mora", "Miguel Ángel Mora", "Former member of the BCP board", "exmiembro del directorio del BCP", "auth:bcp",
  ["lesión de confianza grave", "asociación criminal"], "pretrial_prison", None, NOHEAR,
  "No statement from him or his defence was found.", "No se halló declaración suya ni de su defensa.",
  P("press", ABC13, "body", "", "medium", "Detained 13 Nov 2026. Conflict: prosecution requested house arrest with ankle monitor (ABC 13 Nov) but ABC (16 Nov) lists him in pre-trial detention at the Agrupación Especializada; ruling date not stated. Presumption of innocence applies."), case=REL, detained="2026-11-13", measure_requested="house_arrest", place_reported="Agrupación Especializada")
A("person:aldo-rodriguez", "Aldo Javier Rodríguez González", "Legal director of the BCP (until his detention)", "director jurídico del BCP (hasta su detención)", "auth:bcp",
  ["lesión de confianza", "producción inmediata de documentos públicos de contenido falso", "uso de documentos públicos de contenido falso", "asociación criminal"], "pretrial_prison", None, NOHEAR,
  "No statement from him or his defence was found.", "No se halló declaración suya ni de su defensa.",
  P("press", ABC16, "item 17", "", "medium", "Only ABC (16 Nov) reports his detention and charges; date of detention and of the ruling not stated. On 13 Nov ABC named him as not charged at that time. Presumption of innocence applies."), case=REL, place_reported="Agrupación Especializada (pendiente de traslado)")
