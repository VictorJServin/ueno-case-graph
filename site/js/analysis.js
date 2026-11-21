/* analysis.js - AI analysts' sections: legal (prosecution and defence side by side), financial
   (credit, flow of funds) and editorial (data editor's report and corrections). Each file is optional. */
(function () {
  "use strict";
  var UC = window.UC, h = UC.h, s$ = UC.s, L = UC.L, prov = UC.prov, ui = UC.ui;

  function disclaimer(o) { var t = UC.px(o, "disclaimer"); return t ? h("div", { class: "disclaimer" }, h("p", null, t)) : null; }
  function refs(list, max) { return list && list.length ? h("div", { class: "small", style: "margin-top:2px" }, h("span", { class: "muted" }, L("Rests on: ", "Se apoya en: ")), prov.chips(list, max || 6)) : null; }
  function missing(what) { return h("div", { class: "empty" }, what + L(" is not available in this build, so this part is not shown.", " no está disponible en esta versión; esta parte no se muestra.")); }
  function meter(level, of, label) {
    var m = h("span", { class: "meter", role: "img", "aria-label": label });
    for (var i = 0; i < of; i++) m.appendChild(h("i", { class: i < level ? "on" : "" }));
    return h("span", { class: "row", style: "gap:6px;display:inline-flex" }, m, h("b", { class: "small" }, label));
  }
  var STRENGTH = { well_supported_in_record: 4, partly_supported: 3, legally_uncertain: 2, thin: 1 }, WEIGHT = { strong: 3, arguable: 2, weak: 1 };
  function textList(items) { var ul = h("ul"); (items || []).forEach(function (t) { ul.appendChild(h("li", null, t)); }); return ul; }
  function pointList(items) {
    var box = h("div", { class: "stack" });
    (items || []).forEach(function (p) { box.appendChild(h("div", { class: "el" }, h("p", null, UC.px(p, "text")), refs(p.refs || p.basis_refs))); });
    return box;
  }
  function fold(title, n, body, open) {
    var d = h("details", { class: "agroup" }, h("summary", null, h("span", { class: "t" }, title), n != null ? h("span", { class: "n" }, n) : null));
    if (open) d.open = true;
    d.appendChild(h("div", { style: "padding:10px 0" }, body));
    return d;
  }

  /* ================= legal ================= */
  function legal(root, s) {
    var P = UC.db.extra.legalP, D = UC.db.extra.legalD;
    if (!P && !D) { root.appendChild(missing(L("The legal analysis", "El análisis jurídico"))); return; }
    root.appendChild(h("div", { class: "grid g2" },
      h("div", { class: "stack v-prosecution" }, h("h4", null, L("Prosecution-side analyst", "Analista del lado acusador")), P ? disclaimer(P) : missing(L("The prosecution-side file", "El archivo del lado acusador"))),
      h("div", { class: "stack" }, h("h4", null, L("Defence-side analyst", "Analista del lado de la defensa")), D ? disclaimer(D) : missing(L("The defence-side file", "El archivo de la defensa")))));
    var ids = [], byP = {}, byD = {};
    ((P && P.offences) || []).forEach(function (o) { byP[o.id] = o; if (ids.indexOf(o.id) < 0) ids.push(o.id); });
    ((D && D.offences) || []).forEach(function (o) { byD[o.id] = o; if (ids.indexOf(o.id) < 0) ids.push(o.id); });
    if (!s.offence || ids.indexOf(s.offence) < 0) s.offence = ids[0];
    root.appendChild(h("div", { class: "sec" }, h("h3", null, L("Offence by offence", "Hecho punible por hecho punible")),
      ui.seg(ids.map(function (id) { var o = byP[id] || byD[id]; return { v: id, l: (o.article || id) + " · " + UC.px(o, "name").replace(/\s*\(.*\)$/, "") }; }), s.offence, function (v) { s.offence = v; UC.rerender(); }, L("Offence", "Hecho punible"))));
    var p = byP[s.offence], d = byD[s.offence], cols = h("div", { class: "offence-cols" });
    var pc = h("div", { class: "stack v-prosecution" }), dc = h("div", { class: "stack v-press" });
    pc.appendChild(h("div", { class: "colhead" }, h("span", { html: "<span style='color:var(--vc);display:inline-flex'>" + UC.glyph("Prosecution", "lg") + "</span>" }), h("h3", null, L("The case for the prosecution", "La tesis acusatoria"))));
    if (p) {
      pc.appendChild(h("p", { class: "small", style: "max-width:none" }, h("b", null, (p.article || "") + " · " + UC.px(p, "name") + ". "), h("span", { class: "muted" }, UC.px(p, "penalty"))));
      (p.elements || []).forEach(function (e, i) {
        var el = h("div", { class: "el" }, h("div", { class: "row between" }, h("h3", null, (i + 1) + ". " + UC.px(e, "element")), meter(STRENGTH[e.strength] || 0, 4, UC.enumLabel(e.strength))));
        if (UC.px(e, "strength_reason")) el.appendChild(h("p", { class: "muted" }, UC.px(e, "strength_reason")));
        el.appendChild(h("div", { class: "lab" }, L("Facts alleged", "Hechos alegados")));
        (e.alleged_facts || []).forEach(function (f) { el.appendChild(h("div", null, h("p", null, UC.px(f, "text")), refs(f.refs))); });
        if (UC.px(e, "evidence_needed")) { el.appendChild(h("div", { class: "lab" }, L("Evidence still needed", "Prueba aún necesaria"))); el.appendChild(h("p", null, UC.px(e, "evidence_needed"))); }
        pc.appendChild(el);
      });
      if ((p.role_notes || []).length) pc.appendChild(fold(L("By role", "Por rol"), p.role_notes.length, (function () { var b = h("div", { class: "stack" }); p.role_notes.forEach(function (r) { b.appendChild(h("div", { class: "el" }, h("h3", null, UC.px(r, "role")), h("p", null, UC.px(r, "note")))); }); return b; })()));
      if ((UC.px(p, "open_questions") || []).length) pc.appendChild(fold(L("Open questions", "Preguntas abiertas"), UC.px(p, "open_questions").length, textList(UC.px(p, "open_questions")), true));
    } else pc.appendChild(missing(L("The prosecution-side analysis of this offence", "El análisis acusatorio de este hecho")));
    dc.appendChild(h("div", { class: "colhead" }, h("span", { html: "<span style='color:var(--vc);display:inline-flex'>" + UC.glyph("Defence", "lg") + "</span>" }), h("h3", null, L("The case for the defence", "La tesis de la defensa"))));
    if (d) {
      dc.appendChild(h("p", { class: "small muted", style: "max-width:none" }, (d.arguments || []).length + L(" arguments, each tagged by kind (law, fact, evidence, procedure) and by how much weight the analyst gives it.", " argumentos, cada uno rotulado por tipo (derecho, hecho, prueba, procedimiento) y por el peso que le asigna el analista.")));
      (d.arguments || []).forEach(function (a) {
        var el = h("div", { class: "el" }, h("div", { class: "row between" }, h("h3", null, UC.px(a, "title")), h("span", { class: "row", style: "gap:8px" }, h("span", { class: "tag" }, UC.enumLabel(a.kind)), meter(WEIGHT[a.weight] || 0, 3, UC.enumLabel(a.weight)))));
        el.appendChild(h("p", null, UC.px(a, "text")));
        if (UC.px(a, "weight_reason")) el.appendChild(h("p", { class: "muted" }, UC.px(a, "weight_reason")));
        var r = refs(a.refs); if (r) el.appendChild(r);
        dc.appendChild(el);
      });
    } else dc.appendChild(missing(L("The defence-side analysis of this offence", "El análisis de la defensa de este hecho")));
    cols.appendChild(pc); cols.appendChild(dc);
    root.appendChild(cols);

    var across = h("div", { class: "offence-cols" }), pa = h("div", { class: "stack" }), da = h("div", { class: "stack" });
    if (P) {
      if (P.rey_statement && (P.rey_statement.points || []).length) pa.appendChild(fold(L("How the prosecution side reads Rey's statement", "Cómo lee el lado acusador la declaración de Rey"), P.rey_statement.points.length, pointList(P.rey_statement.points)));
      if ((P.supervisor_questions || []).length) pa.appendChild(fold(L("Questions for the supervisor", "Preguntas para el supervisor"), P.supervisor_questions.length, pointList(P.supervisor_questions)));
    }
    if (D) {
      if ((D.role_positions || []).length) da.appendChild(fold(L("Defence position by role", "Posición de la defensa por rol"), D.role_positions.length, (function () { var b = h("div", { class: "stack" }); D.role_positions.forEach(function (r) { b.appendChild(h("div", { class: "el" }, h("h3", null, UC.px(r, "role")), h("p", null, UC.px(r, "text")), refs(r.refs))); }); return b; })()));
      if ((D.data_weaknesses || []).length) da.appendChild(fold(L("Weaknesses in the record's data", "Debilidades en los datos del acta"), D.data_weaknesses.length, pointList(D.data_weaknesses)));
      if ((UC.px(D, "weakest_arguments") || []).length) da.appendChild(fold(L("The defence's weakest arguments (analyst's own view)", "Los argumentos más débiles de la defensa (opinión del analista)"), UC.px(D, "weakest_arguments").length, textList(UC.px(D, "weakest_arguments"))));
    }
    across.appendChild(pa); across.appendChild(da);
    root.appendChild(h("div", { class: "sec" }, h("h3", null, L("Across all offences", "Para todos los hechos punibles")), across));
  }

  /* ================= financial ================= */
  function kindTag(k) { return h("span", { class: "tag " + (k === "opinion" ? "k-opinion" : "") }, UC.enumLabel(k)); }
  function financial(root, s) {
    var C = UC.db.extra.finCredit, F = UC.db.extra.finFlows;
    if (!C && !F) { root.appendChild(missing(L("The financial analysis", "El análisis financiero"))); return; }
    s.fin = s.fin || (C ? "credit" : "flows");
    root.appendChild(ui.seg([{ v: "credit", l: L("Credit and prudential", "Crédito y regulación prudencial") }, { v: "flows", l: L("Flow of funds", "Flujo de fondos") }], s.fin, function (v) { s.fin = v; UC.rerender(); }));
    if (s.fin === "credit") {
      if (!C) { root.appendChild(missing(L("The credit analysis file", "El archivo de análisis de crédito"))); return; }
      root.appendChild(disclaimer(C));
      root.appendChild(h("p", { class: "small muted", style: "max-width:110ch" }, L("Findings are tagged as fact (read in a source), computation (arithmetic by the analyst on cited inputs) or opinion. Where the analyst adds amounts or converts currency, that is the analyst's working, shown with its inputs, and is not a figure from any source.", "Los hallazgos se rotulan como hecho (leído en una fuente), cálculo (aritmética del analista sobre insumos citados) u opinión. Cuando el analista suma montos o convierte moneda, es trabajo del analista, mostrado con sus insumos, y no una cifra de ninguna fuente.")));
      (C.sections || []).forEach(function (sec, i) {
        var body = h("div", { class: "stack" });
        if (UC.px(sec, "summary")) body.appendChild(h("p", { style: "max-width:none" }, h("span", { class: "tag strong", style: "margin-right:6px" }, L("analyst's summary", "resumen del analista")), UC.px(sec, "summary")));
        (sec.findings || []).forEach(function (f) { body.appendChild(h("div", { class: "el" + (f.kind === "opinion" ? " opinion" : "") }, h("div", null, kindTag(f.kind)), h("p", null, UC.px(f, "text")), refs(f.refs))); });
        root.appendChild(fold(UC.px(sec, "title"), (sec.findings || []).length, body, i === 0));
      });
      if ((C.metrics || []).length) root.appendChild(h("section", { class: "sec" }, h("h3", null, L("Computed metrics, with their inputs", "Métricas calculadas, con sus insumos") + " (" + C.metrics.length + ")"),
        h("p", { class: "small muted", style: "margin:0" }, L("Each ratio is the analyst's arithmetic. The inputs column gives every number used and the row it was read from.", "Cada ratio es aritmética del analista. La columna de insumos da cada número utilizado y la fila de donde se leyó.")), UC.metricTable(C.metrics)));
      if ((C.opinions || []).length) { var ob = h("div", { class: "stack" }); C.opinions.forEach(function (o) { ob.appendChild(h("div", { class: "opinion" }, h("div", null, kindTag("opinion")), h("p", { style: "margin:4px 0;max-width:none" }, UC.px(o, "text")), refs(o.basis_refs))); }); root.appendChild(h("section", { class: "sec" }, h("h3", null, L("Opinions (clearly not facts)", "Opiniones (no son hechos)")), ob)); }
      if ((UC.px(C, "missing_data") || []).length) root.appendChild(fold(L("Data the analyst would need", "Datos que el analista necesitaría"), UC.px(C, "missing_data").length, textList(UC.px(C, "missing_data"))));
      return;
    }
    if (!F) { root.appendChild(missing(L("The flow-of-funds analysis file", "El archivo de análisis de flujo de fondos"))); return; }
    root.appendChild(disclaimer(F));
    var cv = F.coverage || {};
    root.appendChild(h("section", { class: "sec" }, h("h3", null, L("Coverage of the flow data", "Cobertura de los datos de flujos")),
      h("div", { class: "kpis card" }, h("span", null, h("b", null, UC.fmt.num(cv.flow_rows)), L("flow rows", "filas de flujo")), h("span", null, h("b", null, UC.fmt.num(cv.with_amount)), L("with an amount", "con monto")), h("span", null, h("b", null, UC.fmt.num(cv.without_amount)), L("without", "sin monto")), h("span", null, h("b", null, UC.fmt.num(cv.unique_money_legs_after_dedup)), L("distinct money legs after merging repeats (analyst's count)", "tramos distintos tras unir repeticiones (conteo del analista)")), h("span", null, h("b", null, UC.fmt.num(cv.rows_with_day_date)), L("dated to the day", "con fecha exacta"))),
      UC.px(cv, "note") ? h("p", { class: "small muted", style: "max-width:none;margin:0" }, UC.px(cv, "note")) : null,
      h("div", null, h("a", { class: "btn sm", href: "#flows-chains" }, L("Open the reconstructed chains", "Abrir las cadenas reconstruidas")))));
    if ((F.hubs || []).length) root.appendChild(h("section", { class: "sec" }, h("h3", null, L("Hubs: who receives and passes on", "Nodos centrales: quién recibe y traspasa")),
      h("p", { class: "small muted", style: "margin:0;max-width:110ch" }, L("Totals per party are the analyst's sums over one representative row per leg, in each currency separately. They are working figures for comparison between parties, not amounts stated by any source.", "Los totales por parte son sumas del analista sobre una fila representativa por tramo, en cada moneda por separado. Son cifras de trabajo para comparar partes, no montos afirmados por ninguna fuente.")),
      ui.table([
        { label: L("Party", "Parte"), render: function (x) { return UC.resolve(x.entity) ? ui.party(UC.resolve(x.entity)["@id"]) : x.entity; }, sort: function (x) { return x.entity; } },
        { label: L("In, USD", "Entra, USD"), cls: "r", render: function (x) { return x.in_usd ? UC.fmt.num(x.in_usd) : ""; }, sort: function (x) { return x.in_usd || 0; } },
        { label: L("Out, USD", "Sale, USD"), cls: "r", render: function (x) { return x.out_usd ? UC.fmt.num(x.out_usd) : ""; }, sort: function (x) { return x.out_usd || 0; } },
        { label: L("In, PYG", "Entra, PYG"), cls: "r", render: function (x) { return x.in_pyg ? UC.fmt.num(x.in_pyg) : ""; }, sort: function (x) { return x.in_pyg || 0; } },
        { label: L("Out, PYG", "Sale, PYG"), cls: "r", render: function (x) { return x.out_pyg ? UC.fmt.num(x.out_pyg) : ""; }, sort: function (x) { return x.out_pyg || 0; } },
        { label: L("Counterparties", "Contrapartes"), cls: "r", render: function (x) { return x.counterparties; }, sort: function (x) { return x.counterparties; } },
        { label: L("Rows with / without amount", "Filas con / sin monto"), cls: "r", render: function (x) { return (x.rows_with_amount || 0) + " / " + (x.rows_without_amount || 0); } },
        { label: L("Role in the flows (analyst)", "Papel en los flujos (analista)"), render: function (x) { return h("span", { class: "small" }, UC.px(x, "role")); } }
      ], F.hubs, { pageSize: 20, minWidth: 1180 })));
    if ((F.typologies || []).length) {
      var tb = h("div", { class: "grid g2" });
      F.typologies.forEach(function (t) {
        var c = h("div", { class: "card stack" }, h("h3", null, UC.px(t, "name")));
        c.appendChild(h("div", { class: "lab el", style: "border:0;padding:0;background:none" }, h("span", { class: "lab" }, L("Indicators present in the sources", "Indicadores presentes en las fuentes") + " (" + (t.indicators_present || []).length + ")")));
        (t.indicators_present || []).forEach(function (i) { c.appendChild(h("div", { class: "el" }, h("p", null, UC.px(i, "text")), refs(i.refs, 4))); });
        var abs = UC.px(t, "indicators_absent") || [];
        if (abs.length) { c.appendChild(h("span", { class: "lab", style: "font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)" }, L("Not in the sources (would be needed to confirm)", "Ausentes en las fuentes (necesarios para confirmar)") + " (" + abs.length + ")")); c.appendChild(textList(abs)); }
        tb.appendChild(c);
      });
      root.appendChild(h("section", { class: "sec" }, h("h3", null, L("Typologies: indicators present and absent", "Tipologías: indicadores presentes y ausentes")),
        h("p", { class: "small muted", style: "margin:0;max-width:110ch" }, L("A typology is a pattern analysts look for. Indicators being present is not proof that the pattern occurred.", "Una tipología es un patrón que buscan los analistas. Que haya indicadores no prueba que el patrón haya ocurrido.")), tb));
    }
    if ((F.red_flags || []).length) root.appendChild(h("section", { class: "sec" }, h("h3", null, L("Red flags in time order", "Señales de alerta en orden temporal") + " (" + F.red_flags.length + ")"), redFlags(F.red_flags)));
    if ((F.opinions || []).length) { var ob2 = h("div", { class: "stack" }); F.opinions.forEach(function (o) { ob2.appendChild(h("div", { class: "opinion" }, h("div", null, kindTag("opinion")), h("p", { style: "margin:4px 0;max-width:none" }, UC.px(o, "text")), refs(o.basis_refs))); }); root.appendChild(h("section", { class: "sec" }, h("h3", null, L("Opinions (clearly not facts)", "Opiniones (no son hechos)")), ob2)); }
    if ((UC.px(F, "next_tests") || []).length) root.appendChild(fold(L("Tests the analyst would run next", "Pruebas que el analista haría a continuación"), UC.px(F, "next_tests").length, textList(UC.px(F, "next_tests"))));
  }
  function redFlags(flags) {
    var list = flags.slice().sort(function (a, b) { return String(a.date) < String(b.date) ? -1 : 1; });
    var dated = list.filter(function (f) { return /^\d{4}/.test(String(f.date || "")); });
    var box = h("div", { class: "stack" });
    if (dated.length > 1) {
      var W = 1100, H = 74, mL = 20, mR = 20, t = function (d) { d = String(d); return Date.UTC(+d.slice(0, 4), (+d.slice(5, 7) || 1) - 1, +d.slice(8, 10) || 1); };
      var x = d3.scaleUtc().domain([t(dated[0].date) - 20 * 864e5, t(dated[dated.length - 1].date) + 20 * 864e5]).range([mL, W - mR]);
      var svg = s$("svg", { viewBox: "0 0 " + W + " " + H, width: W, height: H, role: "img", "aria-label": L("Red flags on a time axis", "Señales de alerta en un eje temporal"), style: "min-width:" + W + "px" });
      svg.appendChild(s$("line", { x1: mL, x2: W - mR, y1: 40, y2: 40, stroke: "var(--rule-strong)" }));
      x.ticks(8).forEach(function (d) { svg.appendChild(s$("line", { class: "gridl", x1: x(d), x2: x(d), y1: 34, y2: 46 })); svg.appendChild(s$("text", { x: x(d), y: 64, "text-anchor": "middle", "font-size": 11, class: "sub", text: UC.fmt.dateStr(new Date(+d).toISOString().slice(0, 10), "month") })); });
      var last = -99, row = 0;
      dated.forEach(function (f, i) {
        var xx = x(t(f.date)); row = xx - last < 13 ? row + 1 : 0; last = xx;
        var c = s$("circle", { cx: xx, cy: 40 - (row % 3) * 11, r: 5.5, fill: "var(--warn)", stroke: "var(--card)", "stroke-width": 1.5, tabindex: 0, role: "button", "aria-label": f.date + ": " + UC.px(f, "text").slice(0, 80), "data-tip": "<b>" + UC.esc(String(f.date)) + "</b><span class='t2'>" + UC.esc(UC.px(f, "text").slice(0, 220)) + "</span>", style: "cursor:pointer" });
        c.addEventListener("click", function () { var el = document.getElementById("rf-" + i); if (el) { el.scrollIntoView({ block: "center" }); el.focus(); } });
        c.addEventListener("keydown", function (e) { if (e.key === "Enter") c.dispatchEvent(new Event("click")); });
        f._i = i; svg.appendChild(c);
      });
      box.appendChild(h("figure", { class: "fig" }, h("div", { class: "scroll" }, svg), h("figcaption", null, L("Each dot is one red flag named by the analyst; select it to jump to its text and sources below.", "Cada punto es una señal de alerta indicada por el analista; selecciónela para ir a su texto y fuentes."))));
    }
    var rows = h("div", { class: "card alist" });
    list.forEach(function (f) {
      var d = String(f.date || ""), ds = /^\d{4}/.test(d) ? UC.fmt.dateStr(d, d.length === 4 ? "year" : d.length === 7 ? "month" : "day") : d;
      rows.appendChild(h("div", { class: "arow", id: f._i != null ? "rf-" + f._i : null, tabindex: "-1" }, h("span", { class: "d" }, ds), h("div", { class: "x" }, UC.px(f, "text"), refs(f.refs, 5)), h("span", { class: "tag warn" }, L("analyst's flag", "alerta del analista"))));
    });
    box.appendChild(rows);
    return box;
  }

  /* ================= editorial ================= */
  function md(text) {
    var out = [], lines = text.replace(/\r/g, "").split("\n"), i = 0, esc = UC.esc;
    function inline(t) {
      return esc(t).replace(/`([^`]+)`/g, function (m, c) { return /^(rec|press|chrono|dos|edit|src):[a-z0-9:_.-]+$/i.test(c) ? "<span data-ref='" + c + "'></span>" : "<code>" + c + "</code>"; })
        .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>").replace(/\b((?:rec|press|chrono|dos):[a-z]+:\d{3,4})\b/g, "<span data-ref='$1'></span>");
    }
    while (i < lines.length) {
      var l = lines[i];
      if (/^\s*$/.test(l)) { i++; continue; }
      var m = l.match(/^(#{1,4})\s+(.*)$/);
      if (m) { var lv = Math.min(4, m[1].length + 1); out.push("<h" + lv + ">" + inline(m[2]) + "</h" + lv + ">"); i++; continue; }
      if (/^\s*\|/.test(l)) {
        var rows = [];
        while (i < lines.length && /^\s*\|/.test(lines[i])) { rows.push(lines[i].trim().replace(/^\||\|$/g, "").split(/(?<!\\)\|/).map(function (c) { return c.trim(); })); i++; }
        var body = rows.filter(function (r, k) { return k !== 1 || !/^[\s:|-]+$/.test(r.join("")); });
        out.push("<div class='tbl'><table><thead><tr>" + body[0].map(function (c) { return "<th>" + inline(c) + "</th>"; }).join("") + "</tr></thead><tbody>" + body.slice(1).map(function (r) { return "<tr>" + r.map(function (c) { return "<td>" + inline(c) + "</td>"; }).join("") + "</tr>"; }).join("") + "</tbody></table></div>");
        continue;
      }
      if (/^\s*([-*]|\d+\.)\s+/.test(l)) {
        var ord = /^\s*\d+\./.test(l), items = [];
        while (i < lines.length && (/^\s*([-*]|\d+\.)\s+/.test(lines[i]) || (/^\s{2,}\S/.test(lines[i]) && items.length))) {
          if (/^\s*([-*]|\d+\.)\s+/.test(lines[i])) items.push(lines[i].replace(/^\s*([-*]|\d+\.)\s+/, "")); else items[items.length - 1] += " " + lines[i].trim();
          i++;
        }
        out.push((ord ? "<ol>" : "<ul>") + items.map(function (t) { return "<li>" + inline(t) + "</li>"; }).join("") + (ord ? "</ol>" : "</ul>"));
        continue;
      }
      var para = [];
      while (i < lines.length && !/^\s*$/.test(lines[i]) && !/^(#{1,4})\s/.test(lines[i]) && !/^\s*\|/.test(lines[i]) && !/^\s*([-*]|\d+\.)\s+/.test(lines[i])) { para.push(lines[i].trim()); i++; }
      out.push("<p>" + inline(para.join(" ")) + "</p>");
    }
    var box = h("div", { class: "md", html: out.join("\n") });
    Array.prototype.forEach.call(box.querySelectorAll("[data-ref]"), function (sp) { sp.parentNode.replaceChild(prov.chip(sp.getAttribute("data-ref")), sp); });
    return box;
  }
  function editorial(root) {
    var x = UC.db.extra, corr = UC.db.byType.Correction || [];
    if (!x.editorMd && !corr.length) { root.appendChild(missing(L("The data editor's report", "El informe del editor de datos"))); return; }
    root.appendChild(h("div", { class: "disclaimer" }, h("p", null, L("Written by an AI data editor who re-read the sources to check the extracted rows. It is about the quality of the data, not about anyone's guilt or innocence, and it is not legal or financial advice. The report is in English only.", "Escrito por un editor de datos de IA que releyó las fuentes para cotejar las filas extraídas. Trata de la calidad de los datos, no de la culpabilidad o inocencia de nadie, y no constituye asesoramiento jurídico ni financiero. El informe está solo en inglés."))));
    var ver = UC.db.assertions.filter(function (n) { return n.verified === true; }).length, fail = UC.db.assertions.filter(function (n) { return n.verified === false; }), hidden = UC.db.hidden;
    root.appendChild(h("div", { class: "kpis card" }, h("span", null, h("b", null, ver), L("rows checked against their source and confirmed", "filas cotejadas con su fuente y confirmadas")),
      h("span", null, h("b", null, fail.length), L("checked and not confirmed", "cotejadas y no confirmadas"), fail.length ? h("button", { type: "button", class: "more", data: { prov: fail.map(function (n) { return n["@id"]; }).join(" ") } }, L("list", "listar")) : null),
      h("span", null, h("b", null, corr.length), L("corrections applied to the graph", "correcciones aplicadas al grafo")),
      h("span", null, h("b", null, hidden.length), L("rows kept out of charts", "filas excluidas de los gráficos"), hidden.length ? h("button", { type: "button", class: "more", data: { prov: hidden.map(function (n) { return n["@id"]; }).join(" ") } }, L("list", "listar")) : null)));
    if (corr.length) root.appendChild(fold(L("Corrections applied by the editor", "Correcciones aplicadas por el editor"), corr.length, ui.table([
      { label: L("Row", "Fila"), render: function (c) { return c.correctsRow ? prov.chip(c.correctsRow) : h("span", { class: "muted" }, "—"); }, sort: function (c) { return c.correctsRow || ""; } },
      { label: L("Action", "Acción"), render: function (c) { return c.correctionAction || ""; }, sort: function (c) { return c.correctionAction || ""; } },
      { label: L("Field", "Campo"), render: function (c) { return (c.correctedField || []).join(", "); }, sort: function (c) { return (c.correctedField || []).join(","); } },
      { label: L("Before", "Antes"), render: function (c) { var t = (c.originalValue || []).join("; "); return h("span", { class: "small" }, t.length > 90 ? t.slice(0, 87) + "…" : t); } },
      { label: L("After", "Después"), render: function (c) { var t = String(c.newValue == null ? "" : c.newValue); return h("span", { class: "small" }, t.length > 90 ? t.slice(0, 87) + "…" : t); } },
      { label: L("Reason", "Motivo"), render: function (c) { var n = c.editorNote ? (c.editorNote[UC.lang] || c.editorNote.en || []) : []; var t = n.join(" "); return h("span", { class: "small" }, t.length > 240 ? t.slice(0, 237) + "…" : t); } },
      { label: "", render: function (c) { return h("button", { type: "button", class: "btn sm", data: { prov: c["@id"] } }, L("Detail", "Detalle")); } }
    ], corr, { pageSize: 25, minWidth: 1100 })));
    if (x.editorMd) root.appendChild(h("div", { class: "card" }, md(x.editorMd)));
  }

  UC.views.analysis = {
    render: function (root, sub, s) {
      var tabs = [{ id: "legal", label: L("Legal", "Jurídico") }, { id: "financial", label: L("Financial", "Financiero") }, { id: "editorial", label: L("Editorial", "Editorial") }];
      if (sub && tabs.some(function (t) { return t.id === sub; })) s.tab = sub;
      if (!s.tab) s.tab = "legal";
      root.appendChild(h("div", { class: "view-head" }, h("h2", null, L("Analysis", "Análisis")),
        h("p", null, L("Written by AI analysts, not by licensed lawyers or accountants. Not legal or financial advice. The analysts argue from the data in the graph; each reference chip opens the row it relies on.", "Escrito por analistas de IA, no por abogados ni contadores matriculados. No constituye asesoramiento jurídico ni financiero. Los analistas argumentan a partir de los datos del grafo; cada referencia abre la fila en que se apoya."))));
      root.appendChild(ui.tabs(tabs, s.tab, function (t) { s.tab = t; UC.go("analysis", null, t); }));
      var body = h("div", { class: "stack", style: "gap:16px" });
      root.appendChild(body);
      ({ legal: legal, financial: financial, editorial: editorial })[s.tab](body, s);
    }
  };
})();
