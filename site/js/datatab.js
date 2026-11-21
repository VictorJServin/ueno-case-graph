/* datatab.js - what the graph is, the provenance model, the FIBO alignment, SPARQL examples,
   links to the RDF files, and a table browser over every class (including rows hidden elsewhere). */
(function () {
  "use strict";
  var UC = window.UC, h = UC.h, L = UC.L, prov = UC.prov, ui = UC.ui;

  function mdInline(t) { return UC.esc(t).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>"); }
  function countTable(title, obj, labelFn) {
    var tb = h("tbody");
    Object.keys(obj || {}).sort(function (a, b) { return obj[b] - obj[a]; }).forEach(function (k) { tb.appendChild(h("tr", null, h("td", null, labelFn ? labelFn(k) : k), h("td", { class: "r" }, UC.fmt.num(obj[k])))); });
    return h("div", { class: "card stack" }, h("h3", null, title), h("table", null, tb));
  }

  function browser(host, s) {
    var db = UC.db, classes = ["Loan", "Flow", "RoleHolding", "CaseEvent", "FinancialFact", "Charge", "Issue", "PartyDescription", "AnalystOpinion", "Source", "Person", "Organisation", "Authority", "Correction", "hidden"];
    if (!s.cls) { s.cls = "Loan"; s.q = ""; }
    UC.filterDefaults(s);
    function rowsOf(c) {
      if (c === "hidden") return db.hidden;
      if (c === "Loan") return (db.allByType.Loan || []).concat(db.allByType.Overdraft || []);
      return db.allByType[c] || [];
    }
    function clsLabel(c) { return c === "hidden" ? L("Rows hidden by the editor", "Filas ocultadas por el editor") : c === "Loan" ? L("Loans and overdrafts", "Préstamos y sobregiros") : UC.enumLabel(c); }
    var sel = h("select", { "aria-label": L("Class", "Clase") });
    classes.forEach(function (c) { var n = rowsOf(c).length; if (!n) return; var o = h("option", { value: c }, clsLabel(c) + " (" + n + ")"); if (c === s.cls) o.selected = true; sel.appendChild(o); });
    sel.addEventListener("change", function () { s.cls = sel.value; draw(); });
    var q = h("input", { type: "search", value: s.q, placeholder: L("Filter text", "Filtrar texto"), "aria-label": L("Filter text", "Filtrar texto"), style: "width:240px" });
    q.addEventListener("input", UC.debounce(function () { s.q = q.value; draw(); }, 150));
    var ctl = h("div", { class: "controls" }, ui.ctl(L("Class", "Clase"), sel), ui.ctl(L("Filter", "Filtro"), q)), out = h("div");
    ui.sourceFilters(s, function () { draw(); }, null, true).forEach(function (c) { ctl.appendChild(c); });
    host.appendChild(ctl); host.appendChild(out);
    function norm(x) { return String(x).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
    function draw() {
      var rows = rowsOf(s.cls), needle = norm(s.q.trim()), isA = rows.length && !!rows[0].graph;
      rows = rows.filter(function (n) {
        if (n.graph && n.graph !== "analysis" && !UC.pass(n, s)) return false;
        if (!needle) return true;
        var d = n.graph ? UC.describe(n) : { title: UC.label(n["@id"]), sub: UC.tx(n.description) + " " + (n.outlet || "") + " " + (n.name || "") };
        return norm((n.identifier || "") + " " + d.title + " " + d.sub + " " + (n.provenanceNote || "")).indexOf(needle) >= 0;
      });
      var cols;
      if (isA) cols = [
        { label: L("Row id", "Id de fila"), render: function (n) { return prov.chip(n); }, sort: function (n) { return n.identifier; } },
        { label: L("Date", "Fecha"), render: function (n) { return UC.kind(n) === "RoleHolding" ? UC.roleDates(n) : (n.sortDate || n.dateText ? UC.fmt.date(n) : ""); }, sort: function (n) { return n.sortDate || null; } },
        { label: L("What is claimed", "Qué se afirma"), render: function (n) { var d = UC.describe(n); return h("span", null, d.title, d.sub ? h("div", { class: "small muted" }, d.sub.length > 200 ? d.sub.slice(0, 197) + "…" : d.sub) : null, n.hidden ? h("div", { class: "small" }, h("span", { class: "tag warn" }, L("hidden", "oculta")), " " + UC.tx(n.hiddenReason)) : null); } },
        { label: L("Voice", "Voz"), render: function (n) { return prov.badge(n); }, sort: function (n) { return n.graph + n.assertedBy; } },
        { label: L("Tier", "Nivel"), render: function (n) { return h("span", { class: "small" }, UC.enumLabel(UC.tierOf(n))); }, sort: function (n) { return UC.tierOf(n); } },
        { label: L("Conf.", "Conf."), render: function (n) { return prov.conf(n.confidence); }, sort: function (n) { return { high: 0, medium: 1, low: 2 }[n.confidence]; } },
        { label: L("Source", "Fuente"), render: function (n) { return prov.src(n); }, sort: function (n) { return prov.sourceShort(n); } }
      ];
      else if (s.cls === "Source") cols = [
        { label: L("Source id", "Id de fuente"), render: function (n) { return prov.chip(n); }, sort: function (n) { return n.identifier; } },
        { label: L("Kind", "Tipo"), render: function (n) { return UC.enumLabel(n.sourceKind); }, sort: function (n) { return n.sourceKind; } },
        { label: L("Outlet", "Medio"), render: function (n) { return n.outlet || ""; }, sort: function (n) { return n.outlet || ""; } },
        { label: L("Title", "Título"), render: function (n) { return h("span", null, n.name || "", n.page != null ? " · p. " + n.page : ""); } },
        { label: L("Date", "Fecha"), render: function (n) { return UC.fmt.dateStr(n.sortDate, n.datePrecision); }, sort: function (n) { return n.sortDate; } },
        { label: L("Link", "Enlace"), render: function (n) { return n.url && /^https?:/.test(n.url) ? h("a", { href: n.url, target: "_blank", rel: "noopener" }, L("open", "abrir")) : h("span", { class: "muted" }, n.sourceKind === "record" ? L("record page", "página del acta") : L("no link", "sin enlace")); } }
      ];
      else if (s.cls === "Correction") cols = [
        { label: L("Id", "Id"), render: function (n) { return h("button", { type: "button", class: "chip", data: { prov: n["@id"] } }, n.identifier); }, sort: function (n) { return n.identifier; } },
        { label: L("Row corrected", "Fila corregida"), render: function (n) { return n.correctsRow ? prov.chip(n.correctsRow) : ""; } },
        { label: L("Field", "Campo"), render: function (n) { return (n.correctedField || []).join(", "); } },
        { label: L("Before → after", "Antes → después"), render: function (n) { var t = (n.originalValue || []).join("; ") + " → " + (n.newValue == null ? "" : n.newValue); return h("span", { class: "small" }, t.length > 160 ? t.slice(0, 157) + "…" : t); } }
      ];
      else cols = [
        { label: L("Name", "Nombre"), render: function (n) { return ui.party(n["@id"], UC.label(n["@id"])); }, sort: function (n) { return UC.label(n["@id"]); } },
        { label: L("Description", "Descripción"), render: function (n) { return h("span", { class: "small" }, UC.tx(n.description), n.business ? h("div", { class: "muted" }, UC.tx(n.business)) : null); } },
        { label: L("Assertions", "Afirmaciones"), cls: "r", render: function (n) { return (db.byParty[n["@id"]] || []).length; }, sort: function (n) { return (db.byParty[n["@id"]] || []).length; } },
        { label: L("Described by", "Descrito por"), render: function (n) { var b = h("span"); (db.descOf[n["@id"]] || []).forEach(function (d) { b.appendChild(prov.src(d)); b.appendChild(document.createTextNode(" ")); }); return b; } }
      ];
      out.innerHTML = "";
      out.appendChild(h("p", { class: "small muted" }, rows.length + L(" rows", " filas")));
      out.appendChild(ui.table(cols, rows, { pageSize: 30, minWidth: 900 }));
    }
    draw();
  }

  UC.views.data = {
    render: function (root, sub, s) {
      var db = UC.db, st = db.stats, fibo = db.extra.fibo;
      root.appendChild(h("div", { class: "view-head" }, h("h2", null, L("Data and ontology", "Datos y ontología")),
        h("p", null, L("The site is a view over one RDF graph. Everything shown elsewhere can be found here as rows, and the same data can be taken away as Turtle, TriG or JSON-LD.", "El sitio es una vista sobre un grafo RDF. Todo lo que se muestra en otras secciones está aquí como filas, y los mismos datos pueden obtenerse en Turtle, TriG o JSON-LD."))));
      var tr = st.triples || {};
      root.appendChild(h("section", { class: "sec" }, h("h2", null, L("What the graph is", "Qué es el grafo")),
        h("p", { style: "max-width:110ch" }, UC.fmt.num(st.nodes_total) + L(" nodes: ", " nodos: ") + UC.fmt.num(db.assertions.length + db.hidden.filter(function (n) { return n.graph && n.graph !== "analysis"; }).length) + L(" sourced assertions (claims with provenance), ", " afirmaciones con fuente (con procedencia), ") + (db.opinions.length ? db.opinions.length + L(" AI analyst estimates kept in a separate graph, ", " estimaciones de analistas de IA en un grafo aparte, ") : "") + UC.fmt.num(db.parties.length) + L(" parties and ", " partes y ") + UC.fmt.num(db.sources.length) + L(" sources. An assertion is a node of its own, so two sources that say the same thing are two nodes and nothing is merged or averaged. The vocabulary (prefix uc:) extends FIBO, PROV-O and schema.org.", " fuentes. Cada afirmación es un nodo propio: dos fuentes que dicen lo mismo son dos nodos y nada se fusiona ni se promedia. El vocabulario (prefijo uc:) extiende FIBO, PROV-O y schema.org.")),
        h("div", { class: "grid g4" },
          countTable(L("Nodes by class", "Nodos por clase"), st.nodes_by_type, UC.enumLabel),
          countTable(L("Nodes by named graph", "Nodos por grafo nombrado"), st.assertions_by_graph, function (k) { return h("span", { class: "v-" + k, html: "<span style='color:var(--vc)'>" + (k === "analysis" ? UC.glyph("Analyst") : UC.voiceGlyph(k)) + "</span> " + UC.esc(UC.enumLabel(k)) + " <code>graph/" + UC.esc(k) + "</code>" }); }),
          countTable(L("Assertions by source tier", "Afirmaciones por nivel de fuente"), st.assertions_by_source_tier, UC.enumLabel),
          countTable(L("Triples per graph", "Triples por grafo"), tr))));
      root.appendChild(h("section", { class: "sec" }, h("h2", null, L("The provenance model", "El modelo de procedencia")),
        h("div", { class: "grid g2" },
          h("div", { class: "card stack" },
            h("p", { style: "max-width:none" }, L("Provenance sits on the assertion itself. Every loan, flow, role, event, figure, charge and data issue carries:", "La procedencia está en la propia afirmación. Cada préstamo, flujo, cargo, hecho, cifra, imputación e inconsistencia lleva:")),
            h("ul", null,
              h("li", { html: "<code>assertedBy</code>: " + UC.esc(L("whose voice it is (prosecution, Rey, press, regulator, rating agency, company, defence).", "de quién es la voz (Fiscalía, Rey, prensa, regulador, calificadora, empresa, defensa).")) }),
              h("li", { html: "<code>graph</code>: " + UC.esc(L("the layer: prosecution and rey hold only what was read in the record itself; press holds everything else, including prosecution claims relayed by the press.", "la capa: prosecution y rey contienen solo lo leído en el acta; press contiene todo lo demás, incluidas las afirmaciones de la Fiscalía transmitidas por la prensa.")) }),
              h("li", { html: "<code>graph/analysis</code>: " + UC.esc(L("a fourth named graph that holds only AnalystOpinion nodes: estimates by the project's AI analysts, each pointing with basedOn at the sourced rows it rests on. It is not a voice of the case and is never counted with the other three.", "un cuarto grafo nombrado que contiene solo nodos AnalystOpinion: estimaciones de los analistas de IA del proyecto, cada una con basedOn hacia las filas con fuente en que se apoya. No es una voz del caso y nunca se cuenta junto con las otras tres.")) }),
              h("li", { html: "<code>source</code>, <code>locator</code>, <code>quote</code>: " + UC.esc(L("the document, the place in it, and up to twelve words in the original language.", "el documento, el lugar dentro de él y hasta doce palabras en el idioma original.")) }),
              h("li", { html: "<code>confidence</code>: " + UC.esc(L("how clearly the source could be read (not how likely the claim is).", "qué tan clara fue la lectura de la fuente (no la probabilidad de la afirmación).")) }),
              h("li", { html: "<code>sourceTier</code>, <code>verified</code>, <code>correctedField</code>, <code>sameOperationKey</code>, <code>hidden</code>: " + UC.esc(L("the editor's layer: where it was read, whether it was checked, what was corrected, which rows are the same operation, and which rows stay out of charts.", "la capa del editor: dónde se leyó, si fue cotejado, qué se corrigió, qué filas son la misma operación y cuáles quedan fuera de los gráficos.")) }))),
          (function () {
            var ex = db.byRaw["rec:flow:0061"] || db.flows[0], keep = {};
            ["@id", "@type", "graph", "assertedBy", "source", "sourceTier", "locator", "quote", "confidence", "verified", "verifiedMethod", "fromParty", "toParty", "amount", "currency", "sortDate", "sameOperationKey"].forEach(function (k) { if (ex && ex[k] != null) keep[k] = ex[k]; });
            return h("div", { class: "card stack" }, h("h3", null, L("One row as stored", "Una fila tal como está guardada")), h("pre", null, JSON.stringify(keep, null, 1)), ex ? h("div", null, prov.chip(ex, L("Open its provenance panel", "Abrir su panel de procedencia"))) : null);
          })())));

      root.appendChild(h("section", { class: "sec" }, h("h2", null, L("Take the data", "Obtener los datos")),
        h("div", { class: "card row" },
          h("a", { href: "data/graph.ttl" }, "data/graph.ttl"), h("span", { class: "muted small" }, L("Turtle, union of all graphs", "Turtle, unión de los grafos")),
          h("a", { href: "data/graph.trig" }, "data/graph.trig"), h("span", { class: "muted small" }, L("TriG, named graphs", "TriG, grafos nombrados")),
          h("a", { href: "data/graph.jsonld" }, "data/graph.jsonld"), h("span", { class: "muted small" }, L("JSON-LD, what this page loads", "JSON-LD, lo que carga esta página")),
          h("a", { href: "data/ontology.ttl" }, "data/ontology.ttl"), h("span", { class: "muted small" }, L("the vocabulary", "el vocabulario")))));

      if (fibo) {
        root.appendChild(h("section", { class: "sec" }, h("h2", null, L("Alignment with FIBO", "Alineación con FIBO")),
          h("p", { style: "max-width:110ch" }, L("Each concept the case needs, the FIBO or OMG Commons term it maps to, and where FIBO has no term. IRIs were checked against the FIBO source files. ", "Cada concepto que el caso necesita, el término de FIBO u OMG Commons al que corresponde, y dónde FIBO no tiene término. Los IRI se cotejaron con los archivos fuente de FIBO. ") + (fibo.result || "")),
          ui.table([
            { label: "#", cls: "r", render: function (m) { return m.n; }, sort: function (m) { return m.n; } },
            { label: L("Concept", "Concepto"), render: function (m) { return h("b", null, m.concept); }, sort: function (m) { return m.concept; } },
            { label: L("Status", "Estado"), render: function (m) { return h("span", { class: "tag " + (m.status === "VERIFIED" ? "strong" : "warn") }, m.status); }, sort: function (m) { return m.status; } },
            { label: L("FIBO / Commons terms", "Términos FIBO / Commons"), render: function (m) { var b = h("div", { class: "small" }); m.terms.forEach(function (t) { b.appendChild(h("div", null, h("code", null, t.iri), t.kind ? h("span", { class: "muted" }, " " + t.kind) : null)); }); return b; } },
            { label: L("How the case graph uses it", "Cómo lo usa el grafo"), render: function (m) { return h("span", { class: "small", html: mdInline(m.use) }); } },
            { label: L("Notes", "Notas"), render: function (m) { return h("span", { class: "small", html: mdInline(m.notes) }); } }
          ], fibo.mapping, { pageSize: 12, minWidth: 1250 }),
          h("div", { class: "grid g2" },
            h("details", { class: "card" }, h("summary", null, h("b", null, L("What FIBO lacks for this case", "Qué le falta a FIBO para este caso") + " (" + fibo.lacks.length + ")")), h("ul", { class: "small", html: fibo.lacks.map(function (t) { return "<li>" + mdInline(t) + "</li>"; }).join("") })),
            h("details", { class: "card" }, h("summary", null, h("b", null, L("Where FIBO differs from common assumptions", "Dónde FIBO difiere de lo que suele suponerse") + " (" + fibo.differs.length + ")")), h("ul", { class: "small", html: fibo.differs.map(function (t) { return "<li>" + mdInline(t) + "</li>"; }).join("") })))));
        if ((fibo.queries || []).length) {
          var qs = h("div", { class: "grid g2" });
          fibo.queries.forEach(function (q) {
            var full = fibo.query_prefixes + "\n\n" + q.sparql;
            qs.appendChild(h("div", { class: "card stack" }, h("div", { class: "row between" }, h("h3", null, q.title), ui.copyBtn(function () { return full; }, L("Copy query", "Copiar consulta"))), h("pre", { tabindex: "0", "aria-label": q.title }, q.sparql), q.note ? h("p", { class: "small muted", style: "margin:0;max-width:none", html: mdInline(q.note) }) : null));
          });
          root.appendChild(h("section", { class: "sec" }, h("h2", null, L("Example SPARQL queries", "Consultas SPARQL de ejemplo")),
            h("p", { style: "max-width:110ch" }, L("Run them on graph.trig or graph.ttl with any SPARQL 1.1 engine. Copy includes the prefix block.", "Ejecútelas sobre graph.trig o graph.ttl con cualquier motor SPARQL 1.1. Copiar incluye el bloque de prefijos.")),
            h("details", { class: "card" }, h("summary", null, L("Prefixes", "Prefijos")), h("pre", null, fibo.query_prefixes)), qs));
        }
      } else root.appendChild(h("div", { class: "empty" }, L("The FIBO alignment file (data/fibo_mapping.json) is not available.", "El archivo de alineación con FIBO (data/fibo_mapping.json) no está disponible.")));

      var bh = h("section", { class: "sec" }, h("h2", null, L("Browse the rows", "Explorar las filas")), h("p", null, L("Pick a class, filter, and open any row's provenance. Rows the editor keeps out of charts are listed here with the reason.", "Elija una clase, filtre y abra la procedencia de cualquier fila. Las filas que el editor excluye de los gráficos se listan aquí con el motivo.")));
      root.appendChild(bh);
      browser(bh, s);
    }
  };
})();
