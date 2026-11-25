/* overview.js - the case on one screen. Captions are editorial; every number is read from a graph row
   or from stats.json and opens its provenance. */
(function () {
  "use strict";
  var UC = window.UC, h = UC.h, L = UC.L, prov = UC.prov, ui = UC.ui;

  // Key figures: a graph row plus an editorial caption. Rows that are missing from the graph are skipped.
  var FIGURES = [
    { id: "rec:flow:0061", en: "paid to Ueno Bank by Vinanzas, a related company, for a loan portfolio on 15 June 2026", es: "pagados a Ueno Bank por Vinanzas, sociedad vinculada, por una cartera de créditos el 15 de junio de 2026" },
    { id: "press:fact:0036", en: "balance of Vinanzas's account the day before that purchase, as the supervisor is reported to have found", es: "saldo de la cuenta de Vinanzas el día anterior a esa compra, según habría constatado el supervisor" },
    { id: "rec:loan:0037", en: "largest of the five new loans of 11 and 15 June 2026 that the record traces to Vinanzas", es: "el mayor de los cinco préstamos nuevos del 11 y 15 de junio de 2026 que el acta rastrea hasta Vinanzas" },
    { id: "press:fact:0335", en: "average monthly income of borrower Grupo Hendy in 2025, as the prosecution is reported to state", es: "ingreso mensual promedio de la prestataria Grupo Hendy en 2025, según se informa que sostiene la Fiscalía" },
    { id: "rec:flow:0071", en: "in cash that Rey says was brought to the bank at night (his statement only)", es: "en efectivo que, según Rey, fue llevado de noche al banco (solo su declaración)" },
    { id: "chrono:event:0068", event: true, en: "the central bank orders the resolution of the bank", es: "el banco central dispone la resolución del banco" }
  ];

  function figureTiles() {
    var box = h("div", { class: "tiles" });
    FIGURES.forEach(function (f) {
      var n = UC.resolve(f.id);
      if (!n) return;
      var big = f.event ? UC.fmt.date(n) : (n.amount != null || n.principal != null ? UC.moneyOf(n) : UC.fmt.date(n));
      var t = h("button", { type: "button", class: "tile " + prov.vclass(n), data: { prov: n["@id"] } },
        h("span", { class: "n" }, big),
        h("span", { class: "l" }, L(f.en, f.es)),
        h("span", { class: "s", html: "<span style='color:var(--vc);display:inline-flex'>" + UC.glyph(n.assertedBy) + "</span>" + UC.esc(prov.asserterText(n)) + " · " + UC.esc(prov.sourceShort(n)) + " · " + UC.esc(L("confidence ", "confianza ") + UC.enumLabel(n.confidence)) }));
      box.appendChild(t);
    });
    return box;
  }

  function rowsBtn(nodes, label) {
    if (!nodes.length) return null;
    var ids = nodes.slice(0, 80).map(function (n) { return n["@id"]; });
    return h("button", { type: "button", class: "btn sm", data: { prov: ids.join(" ") } }, (label || L("Rows behind this", "Filas que lo sustentan")) + " (" + nodes.length + ")");
  }

  function mechanism() {
    var db = UC.db, rec = function (n) { return n.graph === "prosecution" && UC.fromRecord(n); };
    var unsecured = db.loans.filter(function (l) { return rec(l) && l.collateral === "none"; });
    var passed = db.flows.filter(function (f) { return rec(f) && db.borrowers[f.fromParty] && !/disbursement|repayment|portfolio/.test(f.instrument) && f.fromParty !== "ucr:org/ueno-bank"; });
    var repaid = db.flows.filter(function (f) { return rec(f) && (f.instrument === "instr_repayment" || (db.borrowers[f.toParty] && f.fromParty !== "ucr:org/ueno-bank")); });
    var sale = db.flows.filter(function (f) { return rec(f) && f.sortDate >= "2026-06-11" && f.sortDate <= "2026-06-15"; });
    var steps = [
      [L("Lend without security", "Prestar sin garantía"), L("The record alleges long-term loans and overdrafts on signature alone to companies with little income of their own.", "El acta sostiene que se otorgaron préstamos a largo plazo y sobregiros a sola firma a empresas con escasos ingresos propios."), unsecured],
      [L("Pass it through", "Hacerlo pasar"), L("It alleges that each borrower forwarded the money within hours or days to companies of the bank's own group.", "Sostiene que cada prestataria transfirió los fondos en horas o días a sociedades del propio grupo del banco."), passed],
      [L("Repay in a circle", "Repagar en círculo"), L("It alleges that instalments were paid with money sent back by those same companies, often funded by overdrafts and short-dated cheques.", "Sostiene que las cuotas se pagaron con fondos devueltos por esas mismas sociedades, a menudo originados en sobregiros y cheques de corto plazo."), repaid],
      [L("Sell the loans to a related company", "Vender la cartera a una vinculada"), L("It alleges that when the supervisor insisted the borrowers were related, the bank sold the loans to Vinanzas, which paid with money from new Ueno loans.", "Sostiene que, cuando el supervisor insistió en la vinculación, el banco vendió los créditos a Vinanzas, que pagó con dinero de nuevos préstamos de Ueno."), sale]
    ];
    var box = h("div", { class: "steps" });
    steps.forEach(function (s) {
      box.appendChild(h("div", { class: "step v-prosecution" }, h("h3", null, s[0]), h("p", null, s[1]), rowsBtn(s[2], L("Record rows", "Filas del acta"))));
    });
    return box;
  }

  function borrowerTable() {
    var rows = ((UC.db.stats.loan_principal_by_borrower_currency || {}).rows || []).filter(function (r) { return r.asserted_by === "prosecution" && /^prosecution record/.test(r.source_group); });
    var by = {}, max = { PYG: 0, USD: 0 };
    rows.forEach(function (r) {
      if (!r.currency) return;
      (by[r.borrower] = by[r.borrower] || {})[r.currency] = r;
      max[r.currency] = Math.max(max[r.currency] || 0, Number(r.principal_total));
    });
    var list = Object.keys(by).sort(function (a, b) { return Number((by[b].PYG || {}).principal_total || 0) - Number((by[a].PYG || {}).principal_total || 0) || Number((by[b].USD || {}).principal_total || 0) - Number((by[a].USD || {}).principal_total || 0); });
    function cell(r, cur) {
      if (!r) return h("td", { class: "r muted" }, "—");
      var ids = r.loan_ids.map(UC.toId);
      var b = h("button", { type: "button", class: "linklike num", style: "color:var(--ink);font-size:13.5px", data: { prov: ids.join(" ") } }, UC.fmt.num(r.principal_total));
      return h("td", { class: "r" }, b, h("span", { class: "tiny muted" }, " · " + r.loan_records + L(" rec.", " reg.")), h("span", { class: "mini", style: "width:" + Math.max(1, Number(r.principal_total) / max[cur] * 100).toFixed(1) + "%" }));
    }
    var tb = h("tbody");
    list.forEach(function (b) {
      tb.appendChild(h("tr", null, h("td", null, ui.party(UC.toId(b))), cell(by[b].PYG, "PYG"), cell(by[b].USD, "USD")));
    });
    return h("div", { class: "tbl btot" }, h("table", { style: "min-width:520px" },
      h("thead", null, h("tr", null, h("th", null, L("Borrower", "Prestataria")), h("th", { class: "r" }, L("Principal in PYG", "Capital en PYG")), h("th", { class: "r" }, L("Principal in USD", "Capital en USD")))), tb));
  }

  function bars(title, obj, order, opt) {
    opt = opt || {};
    var keys = (order || Object.keys(obj)).filter(function (k) { return obj[k] != null; });
    if (!order) keys.sort(function (a, b) { return obj[b] - obj[a]; });
    var max = Math.max.apply(null, keys.map(function (k) { return obj[k]; }).concat([1]));
    var box = h("div", { class: "card stack" }, h("h3", null, title));
    var bs = h("div", { class: "bars" });
    keys.forEach(function (k) {
      var lab = opt.label ? opt.label(k) : UC.enumLabel(k), cls = opt.cls ? opt.cls(k) : "";
      var kEl = h("span", { class: "k " + cls });
      kEl.innerHTML = (opt.glyph ? "<span style='color:var(--vc);display:inline-flex'>" + opt.glyph(k) + "</span>" : "") + "<span>" + UC.esc(lab) + "</span>";
      bs.appendChild(h("div", { class: "bar " + cls }, kEl, h("div", { class: "track" }, h("div", { class: "fill", style: "width:" + (obj[k] / max * 100).toFixed(1) + "%" })), h("span", { class: "v" }, UC.fmt.num(obj[k]))));
    });
    box.appendChild(bs);
    if (opt.note) box.appendChild(h("p", { class: "small muted", style: "margin:0" }, opt.note));
    return box;
  }


  /** "What's new": the latest entry of data/updates.json, with when the update ran; earlier runs fold away. */
  function when(iso) {
    var d = new Date(iso);
    if (isNaN(d)) return iso;
    try { return d.toLocaleString(UC.lang === "es" ? "es" : "en-GB", { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit", timeZoneName: "short" }); } catch (e) { return iso; }
  }
  function updItems(u) {
    var ul = h("ul", { class: "upd-list" });
    (u.items || []).forEach(function (it) {
      var li = h("li", null, h("span", null, it[UC.lang] || it.en));
      if (it.go) li.appendChild(h("a", { href: "#" + it.go, class: "small" }, " " + L("Open", "Abrir")));
      if (it.refs && it.refs.length) li.appendChild(h("span", { class: "small upd-refs" }, UC.prov.chips(it.refs, 3)));
      ul.appendChild(li);
    });
    return ul;
  }
  function updMeta(u) {
    var c = u.counts || {};
    return h("p", { class: "small muted", style: "margin:0" }, (u.input ? (u.input[UC.lang] || u.input.en) + " · " : "") +
      L("added ", "se agregaron ") + (c.events || 0) + L(" events, ", " hechos, ") + (c.figures || 0) + L(" figures, ", " cifras, ") + (c.sources || 0) + L(" sources", " fuentes"));
  }
  function whatsNew(list) {
    var u = list[0], box = h("section", { class: "card stack upd", "aria-label": L("What's new", "Novedades") },
      h("div", { class: "upd-head" }, h("h2", null, L("What's new since the last update", "Novedades desde la última actualización")),
        h("span", { class: "upd-when" }, L("Updated ", "Actualizado ") + when(u.executed_at))),
      updMeta(u), updItems(u));
    if (u.not_done) box.appendChild(h("p", { class: "small muted", style: "margin:0" }, u.not_done[UC.lang] || u.not_done.en));
    if (list.length > 1) {
      var d = h("details", { class: "small" }, h("summary", null, L("Earlier updates", "Actualizaciones anteriores") + " (" + (list.length - 1) + ")"));
      list.slice(1).forEach(function (p) { d.appendChild(h("div", { class: "stack upd-old" }, h("b", null, when(p.executed_at)), updMeta(p), updItems(p))); });
      box.appendChild(d);
    }
    return box;
  }

  UC.views.overview = {
    render: function (root) {
      var db = UC.db, st = db.stats;
      var hero = h("div", { class: "hero" },
        h("div", { class: "stack" },
          h("div", { class: "eyebrow" }, L("Case 89/2026 · Public Prosecutor's Office of Paraguay · data to 25 November 2026", "Causa 89/2026 · Ministerio Público del Paraguay · datos al 25 de noviembre de 2026")),
          h("h1", null, L("Ueno Bank: what the record alleges, what the suspect says, what the press adds", "Ueno Bank: qué sostiene el acta, qué dice el imputado, qué agrega la prensa")),
          h("p", { class: "lead" }, L("A provenance-first map of the loans, companies, people and money movements described in the investigative statement of former director Julio Rey and in public reporting on the bank's resolution.", "Un mapa, con procedencia en cada dato, de los créditos, empresas, personas y movimientos de dinero descritos en la declaración indagatoria del exdirector Julio Rey y en la información pública sobre la resolución del banco."))),
        h("div", { class: "card stack v-prosecution" },
          h("h3", null, L("What the record alleges", "Qué sostiene el acta")),
          h("ul", null,
            h("li", null, L("That between 2025 and 2026 the bank's board authorised credit to companies related to its own group without treating them as related parties. ", "Que entre 2025 y 2026 el directorio del banco autorizó créditos a sociedades vinculadas a su propio grupo sin tratarlas como vinculadas. "), prov.chip("src:acta-p01", L("Record p. 1", "Acta p. 1"))),
            h("li", null, L("That six borrowers passed the money on to group companies and repaid with money from those same companies. ", "Que seis prestatarias traspasaron los fondos a sociedades del grupo y repagaron con dinero de esas mismas sociedades. "), prov.chip("src:acta-p02", L("Record p. 2", "Acta p. 2")), prov.chip("src:acta-p10", L("Record p. 10", "Acta p. 10"))),
            h("li", null, L("That in June 2026 the bank sold part of those loans to a related company which paid with money the bank itself had just lent. ", "Que en junio de 2026 el banco vendió parte de esos créditos a una vinculada que pagó con dinero que el propio banco acababa de prestar. "), prov.chip("src:acta-p17", L("Record p. 17", "Acta p. 17")))),
          h("p", { class: "small muted", style: "margin:0" }, L("These are allegations put to a suspect. The record also contains his reply (pages 19 to 24), shown separately throughout.", "Son imputaciones formuladas a un imputado. El acta contiene también su respuesta (páginas 19 a 24), que se muestra siempre por separado."))));
      var up = db.extra.updates;
      if (up) root.appendChild(whatsNew(up));
      root.appendChild(hero);

      root.appendChild(h("section", { class: "sec" }, h("h2", null, L("Key figures", "Cifras clave")),
        h("p", null, L("Each figure is one claim by one voice. Select a tile for its source, locator, quote and confidence.", "Cada cifra es una afirmación de una voz. Seleccione una tarjeta para ver fuente, ubicación, cita y confianza.")),
        figureTiles()));

      var mm = db.extra.missing;
      if (mm) {
        var hl = mm.headline, cur = hl.currency || "USD";
        root.appendChild(h("a", { class: "card mm-link v-analyst", href: "#missing" },
          h("span", { class: "eyebrow" }, L("AI analysts' estimate, not a finding", "Estimación de analistas de IA, no un hecho probado")),
          h("span", { class: "mm-link-n" }, L("How much is missing? About ", "¿Cuánto falta? Unos ") + UC.fmt.money(hl.central, cur, { compact: true }) + (hl.low != null && hl.high != null ? L(", plausibly between ", ", verosímilmente entre ") + UC.fmt.money(hl.low, cur, { compact: true }) + L(" and ", " y ") + UC.fmt.money(hl.high, cur, { compact: true }) : "")),
          h("span", { class: "small muted" }, L("Estimated shortfall of the bank's assets against everything it owes. What that number measures, what it does not, where the money is thought to have gone and what might be recovered: open the Missing money view.", "Faltante estimado del activo del banco frente a todo lo que debe. Qué mide esa cifra, qué no mide, a dónde se cree que fue el dinero y qué podría recuperarse: abra la vista El dinero faltante."))));
      }
      root.appendChild(h("section", { class: "sec" }, h("h2", null, L("The alleged mechanism in four moves", "El mecanismo atribuido, en cuatro movimientos")),
        h("p", null, L("As described by the prosecution record. The buttons list the record rows each step rests on.", "Tal como lo describe el acta fiscal. Los botones listan las filas del acta en que se apoya cada paso.")), mechanism(),
        h("div", { class: "row" }, h("a", { class: "btn", href: "#flows-circuit" }, L("See the June 2026 circuit", "Ver el circuito de junio de 2026")), h("a", { class: "btn", href: "#network" }, L("Explore the network", "Explorar la red")), h("a", { class: "btn", href: "#timeline" }, L("Open the timelines", "Abrir las cronologías")))));

      root.appendChild(h("section", { class: "sec" }, h("h2", null, L("Credit recorded per borrower in the prosecution record", "Crédito registrado por prestataria en el acta fiscal")),
        h("p", null, L("Principal of the loan and overdraft records read in the record's tables, per borrower. Guaraníes and dollars are separate columns and are not converted. Totals include cancelled operations and renewed overdraft lines, so they overstate what was owed at any one time. Select a number for the loan rows.", "Capital de los registros de préstamos y sobregiros leídos en las tablas del acta, por prestataria. Guaraníes y dólares van en columnas separadas, sin convertir. Los totales incluyen operaciones canceladas y sobregiros renovados, por lo que exceden lo adeudado en un momento dado. Seleccione una cifra para ver las filas.")),
        borrowerTable()));

      var voices = h("div", { class: "voicecards" });
      [["prosecution", L("Pages 1 to 19 of the record, read on the page itself: the facts put to the suspect, summarising the bank supervisor's findings. Primary source. An allegation, not a judgment.", "Páginas 1 a 19 del acta: los hechos atribuidos al imputado, que resumen las constataciones del supervisor bancario. Fuente primaria. Es una imputación, no una sentencia.")],
        ["rey", L("Pages 19 to 24: what Julio Rey told prosecutors in his own defence. Unverified, and often about other people.", "Páginas 19 a 24: lo que Julio Rey declaró ante la Fiscalía en su defensa. Sin verificar, y a menudo sobre terceros.")],
        ["press", L("Everything not read in the record itself: press, the regulator, rating agencies, company filings, defence statements, a third-party dossier, and prosecution or Rey claims as relayed by the press. The exact asserter is always labelled.", "Todo lo externo al acta: prensa, regulador, calificadoras, documentos de empresas, declaraciones de la defensa y un dossier de terceros. Siempre se indica quién lo afirma.")]
      ].forEach(function (v) {
        var c = h("div", { class: "voicecard v-" + v[0] });
        c.appendChild(h("h3", { html: "<span style='color:var(--vc);display:inline-flex'>" + UC.voiceGlyph(v[0], "lg") + "</span>" + UC.esc(UC.enumLabel(v[0])) + " <span class='muted num' style='font-weight:400'>" + UC.fmt.num((st.assertions_by_graph || {})[v[0]] || 0) + "</span>" }));
        c.appendChild(h("p", null, v[1]));
        voices.appendChild(c);
      });
      var conf = h("div", { class: "card stack" }, h("h3", null, L("Confidence is about reading, not truth", "La confianza mide la lectura, no la verdad")),
        h("div", { class: "row small" }, prov.conf("high"), L("high: read directly and clearly in the source", "alta: leído directa y claramente en la fuente")),
        h("div", { class: "row small" }, prov.conf("medium"), L("medium: clear but second-hand or summarised", "media: claro, pero de segunda mano o resumido")),
        h("div", { class: "row small" }, prov.conf("low"), L("low: hard-to-read diagram, single outlet, or inferred", "baja: diagrama poco legible, un solo medio, o inferido")),
        h("div", null, h("h4", null, L("Who asserts: shape and colour", "Quién afirma: forma y color")), ui.legendVoices()),
        h("p", { class: "small muted", style: "margin:0" }, "✓ " + L("marks rows the data editor checked against the source; \"corr.\" marks rows the editor corrected (the original value is kept in the provenance panel).", "marca las filas que el editor de datos cotejó con la fuente; \"corr.\" marca las filas corregidas por el editor (el valor original se conserva en el panel de procedencia).")));
      var tb = st.assertions_by_source_tier || {};
      var tiers = h("div", { class: "card stack" }, h("h3", null, L("Source tiers: where each claim was read", "Niveles de fuente: dónde se leyó cada afirmación")),
        h("p", { class: "small", style: "margin:0;max-width:none" }, h("b", null, L("The prosecution record is the primary source. ", "El acta fiscal es la fuente primaria. ")), L("It is an authentic document that the press has not seen in full, so the absence of press coverage for something in the record is never treated as doubt.", "Es un documento auténtico que la prensa no ha visto completo, por lo que la falta de cobertura de algo que consta en el acta nunca se trata como duda.")),
        h("ul", { class: "small" },
          h("li", null, h("b", null, UC.enumLabel("record") + " (" + UC.fmt.num(tb.record || 0) + "): "), L("read on a page of the record, cited by page number.", "leído en una página del acta, citada por número de página.")),
          h("li", null, h("b", null, UC.enumLabel("press_linked") + " (" + UC.fmt.num(tb.press_linked || 0) + "): "), L("an article or document with a link you can open.", "un artículo o documento con enlace que puede abrirse.")),
          h("li", null, h("b", null, UC.enumLabel("rating_or_official") + " (" + UC.fmt.num(tb.rating_or_official || 0) + "): "), L("rating-agency reports and official publications.", "informes de calificadoras y publicaciones oficiales.")),
          h("li", null, h("b", null, UC.enumLabel("dossier") + " (" + UC.fmt.num(tb.dossier || 0) + "): "), L("an unlinked third-party dossier. It names outlets but gives no article, date or page, so nothing in this tier can be traced to its origin. Treat it as the weakest tier; it can be switched off in every view.", "un dossier de terceros sin enlaces. Nombra medios pero no artículo, fecha ni página, de modo que nada en este nivel puede rastrearse hasta su origen. Es el nivel más débil y puede desactivarse en todas las vistas.")),
          tb.editorial ? h("li", null, h("b", null, UC.enumLabel("editorial") + " (" + UC.fmt.num(tb.editorial) + "): "), L("names supplied by the project for parties nobody described; not claims about the case.", "nombres puestos por el proyecto a partes que nadie describió; no son afirmaciones sobre el caso.")) : null));
      root.appendChild(h("section", { class: "sec" }, h("h2", null, L("How to read this", "Cómo leer esto")), voices, h("div", { class: "grid g2" }, tiers, conf)));

      var byClass = {}, byConf = {};
      Object.keys(st.assertions_by_class || {}).forEach(function (k) { if (k !== "AnalystOpinion") byClass[k] = st.assertions_by_class[k]; });
      db.assertions.concat(db.hidden.filter(function (n) { return n.graph && n.graph !== "analysis"; })).forEach(function (n) { byConf[n.confidence] = (byConf[n.confidence] || 0) + 1; });
      var sourcedTotal = (st.assertions_total || 0) - ((st.assertions_by_graph || {}).analysis || 0);
      var issues = (db.byType.Issue || []).length, conflicts = db.assertions.filter(UC.isConflict).length;
      var asserter = {};
      Object.keys(st.assertions_by_asserter || {}).forEach(function (k) { if (k === "analyst") return; var m = { prosecution: "Prosecution", rey: "Rey", press: "Press", regulator: "Regulator", rating_agency: "RatingAgency", company: "Company", defence: "Defence", analyst: "Analyst" }[k] || k; asserter[m] = st.assertions_by_asserter[k]; });
      var vOf = function (a) { return a === "Prosecution" ? "v-prosecution" : a === "Rey" ? "v-rey" : "v-press"; };
      root.appendChild(h("section", { class: "sec" }, h("h2", null, L("What the graph holds", "Qué contiene el grafo")),
        h("p", null, UC.fmt.num(sourcedTotal) + L(" sourced assertions about ", " afirmaciones con fuente sobre ") + UC.fmt.num((st.parties || {}).described + (st.parties || {}).stubs) + L(" people, companies and authorities, drawn from ", " personas, empresas y autoridades, tomadas de ") + UC.fmt.num((st.sources || {}).total) + L(" sources. Counts are claims, not established facts.", " fuentes. Los conteos son afirmaciones, no hechos establecidos.")),
        h("div", { class: "grid g4" },
          bars(L("By voice", "Por voz"), st.assertions_by_graph || {}, UC.VOICES, { cls: function (k) { return "v-" + k; }, glyph: function (k) { return UC.voiceGlyph(k); } }),
          bars(L("By who asserts", "Por quién afirma"), asserter, null, { cls: vOf, glyph: function (k) { return UC.glyph(k); } }),
          bars(L("By kind of claim", "Por tipo de afirmación"), byClass, null),
          bars(L("By reading confidence", "Por confianza de lectura"), byConf, ["high", "medium", "low"])),
        db.opinions.length ? h("div", { class: "card row between v-analysis" }, h("div", null, h("h3", null, L("Kept apart: ", "Aparte: ") + db.opinions.length + L(" AI analyst estimates", " estimaciones de analistas de IA")),
          h("p", { class: "small muted", style: "margin:4px 0 0" }, L("Estimates and hypotheses by the project's AI analysts sit in their own graph (analysis). They are not in any count above, not in the network, flows or timelines, and are never added to sourced amounts.", "Las estimaciones e hipótesis de los analistas de IA del proyecto están en su propio grafo (analysis). No figuran en ningún conteo anterior, ni en la red, los flujos o las cronologías, y nunca se suman a montos con fuente."))),
          db.extra.missing ? h("a", { class: "btn", href: "#missing" }, L("See them in Missing money", "Verlas en El dinero faltante")) : null) : null,
        h("div", { class: "card row between" },
          h("div", null, h("h3", null, issues + L(" recorded data issues and ", " inconsistencias registradas y ") + conflicts + L(" rows flagged as conflicting between sources", " filas marcadas con conflicto entre fuentes")),
            h("p", { class: "small muted", style: "margin:4px 0 0" }, L("Misprints in the record, figures that differ between outlets, dates that disagree. They are listed, not resolved by guesswork.", "Erratas del acta, cifras que difieren entre medios, fechas que no coinciden. Se listan; no se resuelven por conjetura."))),
          h("button", { type: "button", class: "btn", onclick: function () { UC.go("timeline", { mode: "issues" }, "issues"); } }, L("Open the list", "Abrir la lista")))));
    }
  };
})();
