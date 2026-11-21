/* flows.js - money flows: the June 2026 circuit (Sankey), reconstructed chains, the general matrix + table,
   and the per-borrower pass-through panel. Amounts are never added across sources or currencies. */
(function () {
  "use strict";
  var UC = window.UC, h = UC.h, s$ = UC.s, L = UC.L, prov = UC.prov, ui = UC.ui;
  var BANK = "ucr:org/ueno-bank";

  function isoDate(str) { if (!str) return ""; return UC.fmt.dateStr(str, str.length === 4 ? "year" : str.length === 7 ? "month" : "day"); }
  function head(title, text) { return h("div", { class: "sec" }, h("h2", null, title), text ? h("p", { class: "muted", style: "max-width:110ch" }, text) : null); }

  /* ================= (b) June 2026 circuit ================= */
  function circuit(root, s) {
    s.ccur = s.ccur || "USD";
    var db = UC.db, from = "2026-06-11", to = "2026-06-15";
    root.appendChild(head(L("The 11 to 15 June 2026 circuit", "El circuito del 11 al 15 de junio de 2026"),
      L("What the record and the supervisor (as relayed by the press) say happened in five days: Ueno Bank lends to new borrowers, the money moves through bond issuers and group companies to Vinanzas, and Vinanzas pays Ueno Bank for a loan portfolio. Built from the flow and loan rows dated in that window. Each band is one leg; where several rows report the same leg they are folded into it and counted, not added.", "Lo que el acta y el supervisor (según la prensa) dicen que ocurrió en cinco días: Ueno Bank presta a nuevas prestatarias, el dinero pasa por emisores de bonos y sociedades del grupo hasta Vinanzas, y Vinanzas paga a Ueno Bank por una cartera de créditos. Construido con las filas de flujos y préstamos fechadas en esa ventana. Cada banda es un tramo; cuando varias filas informan el mismo tramo se pliegan en él y se cuentan, no se suman.")));
    var ctl = h("div", { class: "controls" });
    ctl.appendChild(ui.ctl(L("Currency (never mixed)", "Moneda (nunca se mezclan)"), ui.seg([{ v: "USD", l: "USD" }, { v: "PYG", l: "PYG" }], s.ccur, function (v) { s.ccur = v; UC.rerender(); })));
    ui.sourceFilters(s, UC.rerender, null, false).forEach(function (c) { ctl.appendChild(c); });
    root.appendChild(ctl);

    var inWin = function (n) { return n.sortDate && n.sortDate >= from && n.sortDate <= to && (n.datePrecision || "day") === "day"; };
    var flows = db.flows.filter(function (f) { return inWin(f) && UC.pass(f, s) && f.instrument !== "instr_portfolio_assignment" && (f.currency === s.ccur || (!f.currency && f.amount == null)); });
    var loans = db.loans.filter(function (l) { return inWin(l) && UC.pass(l, s) && l.currency === s.ccur && l.lender === BANK && l.loanStatus !== "cancelled" && !UC.isOverdraft(l); });
    var legs = {};
    function add(a, b, n, isLoan) { var k = a + "|" + b, g = legs[k] = legs[k] || { from: a, to: b, flows: [], loans: [] }; (isLoan ? g.loans : g.flows).push(n); }
    flows.forEach(function (f) { add(f.fromParty, f.toParty, f, false); });
    loans.forEach(function (l) { add(l.lender, l.nominalBorrower, l, true); });
    var list = Object.keys(legs).map(function (k) {
      var g = legs[k], items = g.flows.length ? g.flows : g.loans, withAmt = items.filter(function (n) { return UC.amountOf(n) != null; }).sort(UC.repOrder);
      g.items = g.flows.concat(g.loans).sort(UC.repOrder); g.rep = withAmt[0] || items.slice().sort(UC.repOrder)[0];
      g.value = withAmt.length ? UC.amountOf(withAmt[0]) : null; g.approx = !!g.rep.amountIsApproximate;
      var seen = {}; withAmt.forEach(function (n) { seen[UC.amountOf(n)] = 1; }); g.distinct = Object.keys(seen).length;
      return g;
    });
    // forward-reachable from the bank; legs back into the bank end at a separate "receives" node so the diagram has no cycle
    var SINK = BANK + "#in", used = [], dropped = [], outOf = {}, state = {}, reach = {};
    list.forEach(function (g) { (outOf[g.from] = outOf[g.from] || []).push(g); });
    Object.keys(outOf).forEach(function (k) { outOf[k].sort(function (x, y) { return (y.value || 0) - (x.value || 0); }); });
    // depth-first walk from the bank: a leg that points back at a party still on the current path would close a
    // loop inside the diagram, so it is kept for the table only
    (function walk(id, depth) {
      state[id] = 1; if (reach[id] == null) reach[id] = depth;
      (outOf[id] || []).forEach(function (g) {
        if (g.to === BANK) { if (id !== BANK) used.push({ g: g, source: id, target: SINK }); return; }
        if (state[g.to] === 1) { dropped.push(g); return; }
        used.push({ g: g, source: id, target: g.to });
        if (!state[g.to]) walk(g.to, depth + 1);
      });
      state[id] = 2;
    })(BANK, 0);
    var fig = h("figure", { class: "fig" });
    root.appendChild(fig);
    if (!used.length) { fig.appendChild(h("div", { class: "empty" }, L("No dated legs in this currency pass the current filters.", "Ningún tramo fechado en esta moneda pasa los filtros actuales."))); return; }
    var maxV = Math.max.apply(null, used.map(function (u) { return u.g.value || 0; })), thin = maxV * 0.012 || 1;
    var ids = {}; used.forEach(function (u) { ids[u.source] = 1; ids[u.target] = 1; });
    var nodes = Object.keys(ids).map(function (id) { return { id: id }; });
    var links = used.map(function (u) { return { source: u.source, target: u.target, value: u.g.value || thin, g: u.g }; });
    var W = 1180, H = Math.max(440, nodes.length * 34), mL = 8, mR = 150;
    var sk = d3.sankey().nodeId(function (d) { return d.id; }).nodeWidth(14).nodePadding(20).nodeAlign(d3.sankeyJustify).extent([[mL, 26], [W - mR, H - 12]]);
    var graph;
    try { graph = sk({ nodes: nodes, links: links }); } catch (e) { fig.appendChild(h("div", { class: "empty" }, L("The legs in view form a loop that cannot be drawn as a flow diagram. Use the table below.", "Los tramos en vista forman un ciclo que no puede dibujarse como diagrama de flujo. Use la tabla."))); graph = null; }
    if (graph) {
      var svg = s$("svg", { viewBox: "0 0 " + W + " " + H, width: W, height: H, role: "img", "aria-label": L("Flow diagram of the June 2026 circuit in ", "Diagrama de flujo del circuito de junio de 2026 en ") + s.ccur, style: "min-width:" + W + "px" });
      var gl = s$("g", { fill: "none" }), gn = s$("g"), path = d3.sankeyLinkHorizontal();
      graph.links.forEach(function (l) {
        var g = l.g, none = g.value == null, lab = UC.short(g.from) + " → " + UC.short(g.to);
        var tipHtml = "<b>" + UC.esc(lab) + "</b><span class='t2'>" + UC.esc(none ? L("amount not stated", "monto no indicado") : UC.fmt.money(g.value, s.ccur, { approx: g.approx })) + " · " + g.items.length + UC.esc(L(" report(s)", " informe(s)")) + (g.distinct > 1 ? UC.esc(L(" with ", " con ") + g.distinct + L(" different figures", " cifras distintas")) : "") + " · " + UC.esc(prov.asserterText(g.rep)) + " · " + UC.esc(prov.sourceShort(g.rep)) + "</span>";
        var p = s$("path", { d: path(l), class: "mark-v-" + g.rep.graph, "stroke-width": none ? 1.5 : Math.max(1.5, l.width), "stroke-opacity": none ? 0.9 : 0.42, "stroke-dasharray": none ? "5 4" : null, fill: "none", "data-tip": tipHtml });
        p.style.fill = "none";
        prov.attach(p, g.items.map(function (n) { return n["@id"]; }), lab);
        gl.appendChild(p);
        var mx = (l.source.x1 + l.target.x0) / 2, my = (l.y0 + l.y1) / 2;
        if (l.width >= 11 || none) {
          var t = (none ? L("amount not stated", "sin monto") : (g.approx ? "≈ " : "") + UC.fmt.compact(g.value)) + (g.items.length > 1 ? "  ×" + g.items.length : "");
          gl.appendChild(s$("text", { x: mx, y: my + 4, "text-anchor": "middle", "font-size": 11.5, "pointer-events": "none", "paint-order": "stroke", stroke: "var(--card)", "stroke-width": 3, text: t }));
        }
      });
      graph.nodes.forEach(function (n) {
        var real = n.id.replace("#in", ""), isBank = real === BANK;
        var r = s$("rect", { x: n.x0, y: n.y0, width: n.x1 - n.x0, height: Math.max(3, n.y1 - n.y0), rx: 2, fill: isBank ? "var(--ink)" : "var(--own)", "data-party": real, tabindex: 0, role: "button", "aria-label": UC.label(real) });
        gn.appendChild(r);
        var name = UC.short(real) + (n.id === SINK ? L(" (receives)", " (recibe)") : isBank ? L(" (lends)", " (presta)") : "");
        gn.appendChild(s$("text", { x: isBank && n.id !== SINK ? n.x0 : n.x1 + 6, y: isBank && n.id !== SINK ? n.y0 - 7 : (n.y0 + n.y1) / 2 + 4, "font-size": 12.5, "font-weight": isBank ? 600 : 500, "paint-order": "stroke", stroke: "var(--card)", "stroke-width": 3, text: name }));
      });
      svg.appendChild(gl); svg.appendChild(gn);
      fig.appendChild(h("div", { class: "hint" }, L("Swipe sideways to see the whole figure.", "Deslice hacia los lados para ver toda la figura.")));
      fig.appendChild(h("div", { class: "scroll" }, svg));
    }
    var lg = h("div", { class: "legend", style: "margin-top:8px" });
    UC.VOICES.forEach(function (v) { lg.appendChild(h("span", { html: "<svg width='26' height='10' aria-hidden='true'><line x1='0' y1='5' x2='26' y2='5' stroke='var(--v-" + (v === "prosecution" ? "pros" : v) + ")' stroke-width='6' stroke-opacity='.5'/></svg>" + UC.esc(L("leg as given by: ", "tramo según: ") + UC.enumLabel(v)) })); });
    lg.appendChild(h("span", { html: "<svg width='26' height='10' aria-hidden='true'><line x1='0' y1='5' x2='26' y2='5' stroke='currentColor' stroke-width='1.5' stroke-dasharray='5 4'/></svg>" + UC.esc(L("named, no amount stated (width not meaningful)", "nombrado, sin monto (ancho sin significado)")) }));
    lg.appendChild(h("span", null, "≈ " + L("approximate figure", "cifra aproximada")));
    lg.appendChild(h("span", null, "×n " + L("number of rows reporting the same leg", "número de filas que informan el mismo tramo")));
    fig.appendChild(lg);
    var noAmt = used.filter(function (u) { return u.g.value == null; }).length;
    fig.appendChild(h("figcaption", null, L("Band width is the amount of the leg's representative row in ", "El ancho de la banda es el monto de la fila representativa del tramo en ") + s.ccur + L(" (record first, exact before approximate). The bank appears twice, once lending and once receiving, so the loop reads left to right. The non-cash assignment of the loans themselves is left out. ", " (primero el acta, exacto antes que aproximado). El banco aparece dos veces, prestando y recibiendo, para leer el circuito de izquierda a derecha. Se omite la cesión no dineraria de los créditos. ") + used.length + L(" legs drawn, ", " tramos dibujados, ") + noAmt + L(" of them without a stated amount", " de ellos sin monto indicado") + (dropped.length ? L("; ", "; ") + dropped.length + L(" legs that would close a loop inside the diagram are listed in the table only.", " tramos que cerrarían un ciclo dentro del diagrama figuran solo en la tabla.") : ".")));
    var rows = used.map(function (u) { return u.g; }).concat(dropped).sort(function (a, b) { return ((reach[a.from] || 0) - (reach[b.from] || 0)) || (b.value || 0) - (a.value || 0); });
    root.appendChild(ui.table([
      { label: L("From", "De"), render: function (g) { return ui.party(g.from); }, sort: function (g) { return UC.short(g.from); } },
      { label: L("To", "A"), render: function (g) { return ui.party(g.to); }, sort: function (g) { return UC.short(g.to); } },
      { label: L("Amount (representative row)", "Monto (fila representativa)"), cls: "r", render: function (g) { return g.value == null ? h("span", { class: "muted" }, L("not stated", "no indicado")) : UC.fmt.money(g.value, s.ccur, { approx: g.approx }); }, sort: function (g) { return g.value; } },
      { label: L("Reports", "Informes"), cls: "r", render: function (g) { return g.items.length + (g.distinct > 1 ? " · " + g.distinct + L(" figures", " cifras") : ""); }, sort: function (g) { return g.items.length; } },
      { label: L("Date", "Fecha"), render: function (g) { return UC.fmt.date(g.rep); }, sort: function (g) { return g.rep.sortDate; } },
      { label: L("How", "Cómo"), render: function (g) { return UC.isLoan(g.rep) ? L("loan", "préstamo") : UC.enumLabel(g.rep.instrument); } },
      { label: L("Who says so", "Quién lo afirma"), render: function (g) { return prov.src(g.rep, g.items.filter(function (n) { return n !== g.rep; }).map(function (n) { return n["@id"]; })); } }
    ], rows, { pageSize: 60, minWidth: 820, caption: L("Legs of the June 2026 circuit", "Tramos del circuito de junio de 2026") }));
  }

  /* ================= (a) reconstructed chains ================= */
  function chains(root, s) {
    var ff = UC.db.extra.finFlows;
    root.appendChild(head(L("Reconstructed chains", "Cadenas reconstruidas"), L("Step-by-step reconstructions by the flow-of-funds analyst. Each leg cites the graph rows it was built from; select a reference for its source.", "Reconstrucciones paso a paso del analista de flujo de fondos. Cada tramo cita las filas del grafo con que se armó; seleccione una referencia para ver su fuente.")));
    if (!ff || !Array.isArray(ff.chains) || !ff.chains.length) { root.appendChild(h("div", { class: "empty" }, L("The flow-of-funds analysis file is not available, so no reconstructed chains are shown. The circuit and the full flow table are built directly from the graph.", "El archivo de análisis de flujo de fondos no está disponible; no se muestran cadenas reconstruidas. El circuito y la tabla completa se arman directamente del grafo."))); return; }
    if (UC.px(ff, "disclaimer")) root.appendChild(h("div", { class: "disclaimer" }, h("p", null, UC.px(ff, "disclaimer"))));
    var cur = ff.chains.filter(function (c) { return c.id === s.chain; })[0] || ff.chains[0];
    var listEl = h("div", { class: "chainlist card", role: "group", "aria-label": L("Chains", "Cadenas") });
    ff.chains.forEach(function (c) {
      listEl.appendChild(h("button", { type: "button", "aria-pressed": String(c === cur), onclick: function () { s.chain = c.id; UC.rerender(); } }, UC.px(c, "title"),
        h("span", null, (c.legs || []).length + L(" legs", " tramos") + (c.closes_loop ? L(" · returns to its origin", " · vuelve al origen") : "") + (c.elapsed_days != null ? " · " + c.elapsed_days + L(" days", " días") : ""))));
    });
    var det = h("div", { class: "card stack" });
    det.appendChild(h("h3", { style: "font-size:18px;font-family:var(--display)" }, UC.px(cur, "title")));
    det.appendChild(h("div", { class: "row" }, h("span", { class: "tag strong" }, L("AI analyst's reconstruction", "Reconstrucción del analista de IA")),
      cur.closes_loop ? h("span", { class: "tag warn" }, L("money returns to its origin (as reconstructed)", "el dinero vuelve al origen (según la reconstrucción)")) : h("span", { class: "tag" }, L("does not close a loop", "no cierra un circuito")),
      cur.elapsed_days != null ? h("span", { class: "tag" }, L("elapsed: ", "transcurrido: ") + cur.elapsed_days + L(" days", " días")) : null));
    if (UC.px(cur, "summary")) det.appendChild(h("p", { style: "max-width:none" }, UC.px(cur, "summary")));
    var legs = h("div", { class: "legs" });
    (cur.legs || []).forEach(function (l) {
      var amt = l.amount == null ? h("span", { class: "muted" }, L("amount not stated", "monto no indicado")) : h("span", { class: "amt" }, UC.fmt.money(l.amount, l.currency));
      legs.appendChild(h("div", { class: "leg" },
        h("div", { class: "no", "aria-label": L("Step ", "Paso ") + l.step }, String(l.step)),
        h("div", { class: "stack" }, h("div", { class: "ft" }, UC.resolve(l.from) ? ui.party(UC.resolve(l.from)["@id"]) : h("span", null, String(l.from)), h("span", { class: "arrow", "aria-hidden": "true" }, "→"), h("span", { class: "sr" }, L(" to ", " a ")), UC.resolve(l.to) ? ui.party(UC.resolve(l.to)["@id"]) : h("span", null, String(l.to))),
          UC.px(l, "note") ? h("div", { class: "nt" }, UC.px(l, "note")) : null),
        h("div", null, amt, h("div", { class: "meta" }, (l.date ? isoDate(String(l.date)) : L("undated", "sin fecha")) + " · " + UC.enumLabel(l.instrument))),
        h("div", null, h("div", { class: "meta" }, L("Built from", "Armado con")), prov.chips(l.refs || [], 5))));
    });
    det.appendChild(legs);
    if (UC.px(cur, "reconciliation")) det.appendChild(h("div", { class: "note", style: "background:var(--soft);border-radius:8px;padding:10px 12px" }, h("h4", null, L("Reconciliation (analyst)", "Conciliación (analista)")), h("p", { style: "margin:4px 0 0;max-width:none" }, UC.px(cur, "reconciliation"))));
    root.appendChild(h("div", { class: "split l" }, listEl, det));
  }

  /* ================= (c) all flows: matrix + table ================= */
  function allFlows(root, s) {
    var db = UC.db;
    if (s.cur == null) { s.cur = "all"; s.instr = "all"; s.d0 = ""; s.d1 = ""; s.min = ""; }
    root.appendChild(head(L("All reported flows", "Todos los flujos informados"), L("Every movement of money or assets in the graph. The matrix reads from the row (payer) to the column (recipient).", "Todos los movimientos de dinero o activos del grafo. La matriz se lee de la fila (pagador) a la columna (receptor).")));
    var ctl = h("div", { class: "controls" });
    var d0 = h("input", { type: "date", value: s.d0, min: "2019-01-01", max: "2026-11-20" }), d1 = h("input", { type: "date", value: s.d1, min: "2019-01-01", max: "2026-11-20" });
    d0.addEventListener("change", function () { s.d0 = d0.value; UC.rerender(); }); d1.addEventListener("change", function () { s.d1 = d1.value; UC.rerender(); });
    var instr = h("select", { "aria-label": L("Instrument", "Instrumento") }, h("option", { value: "all" }, L("All instruments", "Todos los instrumentos")));
    var ic = {}; db.flows.forEach(function (f) { ic[f.instrument] = (ic[f.instrument] || 0) + 1; });
    Object.keys(ic).sort(function (a, b) { return ic[b] - ic[a]; }).forEach(function (k) { var o = h("option", { value: k }, UC.enumLabel(k) + " (" + ic[k] + ")"); if (k === s.instr) o.selected = true; instr.appendChild(o); });
    instr.addEventListener("change", function () { s.instr = instr.value; UC.rerender(); });
    var min = h("input", { type: "number", min: "0", step: "any", value: s.min, placeholder: "0", style: "width:140px", "aria-label": L("Minimum amount", "Monto mínimo") });
    min.addEventListener("change", function () { s.min = min.value; UC.rerender(); });
    ctl.appendChild(ui.ctl(L("Currency", "Moneda"), ui.seg([{ v: "all", l: L("All", "Todas") }, { v: "USD", l: "USD" }, { v: "PYG", l: "PYG" }, { v: "none", l: L("No amount", "Sin monto") }], s.cur, function (v) { s.cur = v; UC.rerender(); })));
    ctl.appendChild(ui.ctl(L("From date", "Desde"), d0)); ctl.appendChild(ui.ctl(L("To date", "Hasta"), d1));
    ctl.appendChild(ui.ctl(L("Instrument", "Instrumento"), instr));
    ctl.appendChild(ui.ctl(L("Minimum amount (in the chosen currency)", "Monto mínimo (en la moneda elegida)"), min));
    ui.sourceFilters(s, UC.rerender, null, true).forEach(function (c) { ctl.appendChild(c); });
    root.appendChild(ctl);
    var minV = s.min !== "" && isFinite(Number(s.min)) ? Number(s.min) : null;
    var list = db.flows.filter(function (f) {
      if (!UC.pass(f, s)) return false;
      if (s.cur === "none" ? f.amount != null : (s.cur !== "all" && f.currency !== s.cur)) return false;
      if (s.cur !== "none" && s.cur !== "all" && f.amount == null) return false;
      if (s.instr !== "all" && f.instrument !== s.instr) return false;
      if (s.d0 && (!f.sortDate || (f.sortDateEnd || f.sortDate) < s.d0)) return false;
      if (s.d1 && (!f.sortDate || f.sortDate > s.d1)) return false;
      if (minV != null && minV > 0 && (f.amount == null || Number(f.amount) < minV)) return false;
      return true;
    });
    var groups = UC.groupAlts(list), withAmt = groups.filter(function (g) { return g.rep.amount != null; }).length;
    root.appendChild(h("div", { class: "kpis card" },
      h("span", null, h("b", null, list.length), L("rows", "filas")), h("span", null, h("b", null, groups.length), L("distinct items after folding repeated reports", "ítems distintos tras plegar informes repetidos")),
      h("span", null, h("b", null, withAmt), L("with a stated amount", "con monto indicado")), h("span", null, h("b", null, groups.length - withAmt), L("named without an amount (dashed in the matrix)", "nombrados sin monto (punteados en la matriz)"))));

    /* matrix */
    var cnt = {}, cell = {};
    groups.forEach(function (g) {
      var f = g.rep; cnt[f.fromParty] = (cnt[f.fromParty] || 0) + 1; cnt[f.toParty] = (cnt[f.toParty] || 0) + 1;
      var k = f.fromParty + "|" + f.toParty; (cell[k] = cell[k] || []).push(g);
    });
    var parties = Object.keys(cnt).sort(function (a, b) { return cnt[b] - cnt[a]; }), cap = 26, top = parties.slice(0, cap);
    var fig = h("figure", { class: "fig" });
    if (!top.length) fig.appendChild(h("div", { class: "empty" }, L("No flows match the filters.", "Ningún flujo coincide con los filtros.")));
    else {
      var c = 24, left = 170, topM = 128, W = left + top.length * c + 10, H = topM + top.length * c + 10, maxN = 1;
      top.forEach(function (a) { top.forEach(function (b) { var g = cell[a + "|" + b]; if (g) maxN = Math.max(maxN, g.length); }); });
      var svg = s$("svg", { viewBox: "0 0 " + W + " " + H, width: W, height: H, role: "img", "aria-label": L("Matrix of flows between the most active parties", "Matriz de flujos entre las partes más activas"), style: "min-width:" + W + "px" });
      top.forEach(function (p, i) {
        var nm = UC.short(p); if (nm.length > 22) nm = nm.slice(0, 21) + "…";
        svg.appendChild(s$("text", { x: left - 8, y: topM + i * c + c / 2 + 4, "text-anchor": "end", "font-size": 12, text: nm, "data-party": p }));
        svg.appendChild(s$("text", { transform: "translate(" + (left + i * c + c / 2 + 4) + "," + (topM - 8) + ") rotate(-55)", "font-size": 12, text: nm, "data-party": p }));
        svg.appendChild(s$("line", { class: "gridl", x1: left, x2: left + top.length * c, y1: topM + i * c, y2: topM + i * c }));
        svg.appendChild(s$("line", { class: "gridl", y1: topM, y2: topM + top.length * c, x1: left + i * c, x2: left + i * c }));
      });
      svg.appendChild(s$("rect", { x: left, y: topM, width: top.length * c, height: top.length * c, fill: "none", stroke: "var(--rule-strong)" }));
      top.forEach(function (a, i) {
        top.forEach(function (b, j) {
          var gs = cell[a + "|" + b]; if (!gs) return;
          var amt = gs.filter(function (g) { return g.rep.amount != null; }), ids = [];
          gs.forEach(function (g) { g.items.forEach(function (n) { ids.push(n["@id"]); }); });
          var lines = amt.slice(0, 4).map(function (g) { return UC.esc(UC.moneyOf(g.rep) + " · " + UC.fmt.date(g.rep)); }).join("<br>") + (amt.length > 4 ? "<br>…" : "");
          var r = s$("rect", { x: left + j * c + 2, y: topM + i * c + 2, width: c - 4, height: c - 4, rx: 3,
            fill: amt.length ? "var(--own)" : "none", "fill-opacity": amt.length ? 0.25 + 0.75 * Math.sqrt(gs.length / maxN) : null,
            stroke: amt.length ? "none" : "var(--muted)", "stroke-width": 1.2, "stroke-dasharray": amt.length ? null : "3 2",
            "data-tip": "<b>" + UC.esc(UC.short(a) + " → " + UC.short(b)) + "</b><span class='t2'>" + gs.length + UC.esc(L(" item(s), ", " ítem(s), ")) + (gs.length - amt.length) + UC.esc(L(" without amount", " sin monto")) + (lines ? "<br>" + lines : "") + "</span>" });
          prov.attach(r, ids, UC.short(a) + " → " + UC.short(b) + ": " + gs.length);
          svg.appendChild(r);
          if (gs.length > 1) svg.appendChild(s$("text", { x: left + j * c + c / 2, y: topM + i * c + c / 2 + 4, "text-anchor": "middle", "font-size": 10.5, "pointer-events": "none", fill: "var(--paper)", style: amt.length ? "fill:var(--card)" : "fill:var(--ink)", text: gs.length }));
        });
      });
      fig.appendChild(h("div", { class: "hint" }, L("Swipe sideways to see the whole matrix.", "Deslice hacia los lados para ver toda la matriz.")));
      fig.appendChild(h("div", { class: "matrix-wrap" }, svg));
      fig.appendChild(h("figcaption", null, L("Rows pay, columns receive. Darker cells hold more distinct items (the number is shown when above one). Dashed empty cells are flows the source names without an amount. ", "Las filas pagan, las columnas reciben. Las celdas más oscuras contienen más ítems distintos (se muestra el número si es mayor que uno). Las celdas vacías punteadas son flujos que la fuente nombra sin monto. ") + (parties.length > cap ? L("Showing the ", "Se muestran las ") + cap + L(" most active of ", " partes más activas de ") + parties.length + L(" parties; the table below has everything.", "; la tabla inferior contiene todo.") : "")));
    }
    root.appendChild(fig);
    root.appendChild(ui.table([
      { label: L("Date", "Fecha"), render: function (g) { return UC.fmt.date(g.rep); }, sort: function (g) { return g.rep.sortDate || null; } },
      { label: L("From", "De"), render: function (g) { return ui.party(g.rep.fromParty); }, sort: function (g) { return UC.short(g.rep.fromParty); } },
      { label: L("To", "A"), render: function (g) { return ui.party(g.rep.toParty); }, sort: function (g) { return UC.short(g.rep.toParty); } },
      { label: "USD", cls: "r", render: function (g) { return g.rep.currency === "USD" && g.rep.amount != null ? (g.rep.amountIsApproximate ? "≈ " : "") + UC.fmt.num(g.rep.amount) : ""; }, sort: function (g) { return g.rep.currency === "USD" && g.rep.amount != null ? Number(g.rep.amount) : null; } },
      { label: "PYG", cls: "r", render: function (g) { return g.rep.currency === "PYG" && g.rep.amount != null ? (g.rep.amountIsApproximate ? "≈ " : "") + UC.fmt.num(g.rep.amount) : ""; }, sort: function (g) { return g.rep.currency === "PYG" && g.rep.amount != null ? Number(g.rep.amount) : null; } },
      { label: L("Instrument and purpose", "Instrumento y destino"), render: function (g) { var p = UC.tx(g.rep.purpose); return h("span", null, (g.rep.alleged ? (g.rep.assertedBy === "Rey" ? L("Rey states: ", "Rey declara: ") : L("The prosecution alleges: ", "La Fiscalía sostiene: ")) : "") + UC.enumLabel(g.rep.instrument), g.rep.amount == null ? h("span", { class: "tag", style: "margin-left:6px" }, L("no amount", "sin monto")) : null, p ? h("div", { class: "small muted" }, p.length > 150 ? p.slice(0, 147) + "…" : p) : null); } },
      { label: L("Reports", "Informes"), cls: "r", render: function (g) { return g.items.length > 1 ? h("span", { class: "tag warn" }, g.items.length) : "1"; }, sort: function (g) { return g.items.length; } },
      { label: L("Who says so", "Quién lo afirma"), render: function (g) { return prov.src(g.rep, g.items.slice(1).map(function (n) { return n["@id"]; })); }, sort: function (g) { return g.rep.assertedBy; } }
    ], groups, { pageSize: 40, sortCol: 0, minWidth: 980, caption: L("Flow legs", "Tramos de flujo") }));
  }

  /* ================= (d) per-borrower pass-through ================= */
  function borrowers(root, s) {
    var db = UC.db, ids = Object.keys(db.borrowers);
    function recCount(id) { return db.borrowers[id].filter(UC.fromRecord).length; }
    ids.sort(function (a, b) { return recCount(b) - recCount(a) || db.borrowers[b].length - db.borrowers[a].length; });
    if (!s.borrower || !db.borrowers[s.borrower]) s.borrower = ids[0];
    var id = s.borrower, p = db.byId[id];
    root.appendChild(head(L("Borrower pass-through", "Paso de fondos por prestataria"), L("For one borrower: the loans as each voice records them, where the sources say the money went, where they say repayments came from, and the borrower's own reported size.", "Para una prestataria: los préstamos según cada voz, a dónde dicen las fuentes que fue el dinero, de dónde dicen que salieron los pagos, y el tamaño informado de la propia empresa.")));
    var sel = h("select", { "aria-label": L("Borrower", "Prestataria") });
    ids.forEach(function (b) { var o = h("option", { value: b }, UC.label(b) + " (" + db.borrowers[b].length + ")"); if (b === id) o.selected = true; sel.appendChild(o); });
    sel.addEventListener("change", function () { s.borrower = sel.value; UC.rerender(); });
    var ctl = h("div", { class: "controls" }, ui.ctl(L("Borrower (loan records)", "Prestataria (registros de préstamo)"), sel));
    ui.sourceFilters(s, UC.rerender, null, false).forEach(function (c) { ctl.appendChild(c); });
    root.appendChild(ctl);
    root.appendChild(h("div", { class: "card stack" }, h("div", { class: "row between" }, h("h3", { style: "font-size:18px;font-family:var(--display)" }, UC.label(id)), h("div", { class: "row" }, ui.party(id, L("Profile and sources", "Ficha y fuentes")))),
      p.business ? h("div", { class: "small" }, UC.tx(p.business)) : null, p.description ? h("div", { class: "small muted" }, UC.tx(p.description)) : null));

    var loans = db.borrowers[id].filter(function (l) { return UC.pass(l, s); });
    var rec = loans.filter(function (l) { return l.graph === "prosecution"; }).sort(UC.byDate), other = loans.filter(function (l) { return l.graph !== "prosecution"; }).sort(UC.byDate);
    function loanCols(full) {
      var cols = [
        { label: L("Op. number", "N.º op."), render: function (l) { return l.operationNumber || ""; }, sort: function (l) { return l.operationNumber || null; } },
        { label: L("Date", "Fecha"), render: function (l) { return UC.fmt.date(l); }, sort: function (l) { return l.sortDate || null; } },
        { label: L("Type", "Tipo"), render: function (l) { return UC.isOverdraft(l) ? L("overdraft", "sobregiro") : L("loan", "préstamo"); } },
        { label: L("Term", "Plazo"), render: function (l) { return l.termYears ? UC.fmt.num(l.termYears) + L(" yr", " años") : l.termDays ? l.termDays + L(" d", " d") : ""; } },
        { label: L("Rate", "Tasa"), cls: "r", render: function (l) { return l.ratePct ? UC.fmt.pct(l.ratePct) : ""; }, sort: function (l) { return l.ratePct ? Number(l.ratePct) : null; } },
        { label: L("Cur.", "Mon."), render: function (l) { return l.currency || ""; }, sort: function (l) { return l.currency || null; } },
        { label: L("Principal", "Capital"), cls: "r", render: function (l) { return l.principal != null ? UC.fmt.num(l.principal) : ""; }, sort: function (l) { return l.principal != null ? Number(l.principal) : null; } },
        { label: L("Outstanding", "Saldo"), cls: "r", render: function (l) { return l.outstanding != null ? UC.fmt.num(l.outstanding) : ""; }, sort: function (l) { return l.outstanding != null ? Number(l.outstanding) : null; } },
        { label: L("Collateral", "Garantía"), render: function (l) { return l.collateral ? UC.enumLabel(l.collateral) : ""; } },
        { label: L("Status", "Estado"), render: function (l) { return l.loanStatus ? UC.enumLabel(l.loanStatus) : ""; } }
      ];
      if (!full) cols = cols.filter(function (c, i) { return [1, 2, 5, 6, 9].indexOf(i) >= 0; });
      if (!full) cols.push({ label: L("Note", "Nota"), render: function (l) { var t = UC.tx(l.note); return h("span", { class: "small" }, t.length > 140 ? t.slice(0, 137) + "…" : t); } });
      cols.push({ label: L("Who says so", "Quién lo afirma"), render: function (l) { var alts = (db.altOf[l["@id"]] || []).filter(function (x) { return x !== l; }); return h("span", null, prov.src(l), alts.length ? h("span", { class: "tag warn", style: "margin-left:4px", title: L("Also reported by other rows: one operation, not additive", "También informado por otras filas: una operación, no se suma") }, "+" + alts.length) : null); } });
      return cols;
    }
    root.appendChild(h("section", { class: "sec v-prosecution" }, h("h3", { html: "<span style='color:var(--vc)'>" + UC.voiceGlyph("prosecution") + "</span> " + UC.esc(L("Loans as listed in the prosecution record", "Préstamos según el acta fiscal")) + " (" + rec.length + ")" }),
      rec.length ? ui.table(loanCols(true), rec, { pageSize: 30, minWidth: 1040 }) : h("div", { class: "empty" }, L("The record's tables list no loan to this borrower (or the voice is filtered out).", "Las tablas del acta no listan préstamos a esta prestataria (o la voz está filtrada)."))));
    if (other.length) root.appendChild(h("section", { class: "sec v-press" }, h("h3", { html: "<span style='color:var(--vc)'>" + UC.voiceGlyph("press") + "</span> " + UC.esc(L("Loans as reported outside the record", "Préstamos según fuentes externas al acta")) + " (" + other.length + ")" }),
      h("p", { class: "small muted", style: "margin:0" }, L("These rows may describe the same operations as the record's table. They are shown side by side and never added to it.", "Estas filas pueden describir las mismas operaciones que la tabla del acta. Se muestran en paralelo y nunca se suman.")),
      ui.table(loanCols(false), other, { pageSize: 20, minWidth: 820 })));

    var fl = db.flows.filter(function (f) { return UC.pass(f, s) && (f.fromParty === id || f.toParty === id); });
    var out = fl.filter(function (f) { return f.fromParty === id && f.toParty !== BANK && f.instrument !== "instr_repayment"; }).sort(UC.byDate);
    var back = fl.filter(function (f) { return (f.toParty === id && f.fromParty !== BANK) || (f.fromParty === id && (f.toParty === BANK || f.instrument === "instr_repayment")); }).sort(UC.byDate);
    var disb = fl.filter(function (f) { return f.fromParty === BANK && f.toParty === id; }).sort(UC.byDate);
    function fsec(title, note, list) { return h("div", { class: "card stack" }, h("h3", null, title + " (" + UC.groupAlts(list).length + ")"), h("p", { class: "small muted", style: "margin:0" }, note), list.length ? ui.paged(list, 25, function (part) { return ui.alist(part); }) : h("div", { class: "empty" }, L("No row in the graph.", "Ninguna fila en el grafo."))); }
    root.appendChild(h("div", { class: "grid g2" },
      fsec(L("Where the sources say the money went", "A dónde dicen las fuentes que fue el dinero"), L("Flows out of the borrower to parties other than the bank.", "Flujos desde la prestataria hacia partes distintas del banco."), out),
      fsec(L("Where the sources say repayments came from", "De dónde dicen las fuentes que salieron los pagos"), L("Money received by the borrower from third parties, and its payments to the bank.", "Dinero recibido por la prestataria de terceros, y sus pagos al banco."), back)));
    if (disb.length) root.appendChild(fsec(L("Disbursements from the bank reported as flows", "Desembolsos del banco informados como flujos"), L("The same operations as the loan rows above, seen as movements.", "Las mismas operaciones que las filas de préstamos, vistas como movimientos."), disb));

    /* income versus credit */
    var facts = (db.byParty[id] || []).filter(function (n) { return n["@type"][0] === "FinancialFact" && UC.pass(n, s); }).sort(UC.byDate);
    var sec = h("section", { class: "sec" }, h("h3", null, L("The borrower's own size against its credit", "Tamaño de la prestataria frente a su crédito")));
    var srows = ((db.stats.loan_principal_by_borrower_currency || {}).rows || []).filter(function (r) { return UC.toId(r.borrower) === id && r.currency; });
    if (srows.length) {
      sec.appendChild(h("p", { class: "small muted", style: "margin:0" }, L("Principal recorded per source document. Each line is one source's own list; lines can cover the same loans and must not be added together.", "Capital registrado por documento fuente. Cada línea es la lista de una fuente; las líneas pueden cubrir los mismos préstamos y no deben sumarse.")));
      sec.appendChild(ui.table([
        { label: L("Asserted by", "Lo afirma"), render: function (r) { return UC.enumLabel({ prosecution: "Prosecution", regulator: "Regulator", press: "Press", rey: "Rey", rating_agency: "RatingAgency", company: "Company", defence: "Defence" }[r.asserted_by] || r.asserted_by); } },
        { label: L("Source document", "Documento fuente"), render: function (r) { var src = UC.resolve(r.source_group); return src ? prov.chip(src, (src.outlet || "") + ", " + UC.fmt.dateStr(src.sortDate, src.datePrecision)) : r.source_group; } },
        { label: L("Cur.", "Mon."), render: function (r) { return r.currency; } },
        { label: L("Records", "Registros"), cls: "r", render: function (r) { return r.loan_records + (r.of_which_overdrafts ? " (" + r.of_which_overdrafts + L(" overdraft)", " sobregiro)") : ""); } },
        { label: L("Principal in that document", "Capital en ese documento"), cls: "r", render: function (r) { return h("button", { type: "button", class: "linklike num", style: "color:var(--ink)", data: { prov: r.loan_ids.map(UC.toId).join(" ") } }, UC.fmt.num(r.principal_total)); } },
        { label: L("Outstanding", "Saldo"), cls: "r", render: function (r) { return r.outstanding_total != null && r.records_with_outstanding ? UC.fmt.num(r.outstanding_total) : ""; } }
      ], srows, { pageSize: 30, minWidth: 760 }));
    }
    if (facts.length) {
      var fb = h("div", { class: "facts" });
      facts.forEach(function (f) {
        var val = f.amount != null ? (f.currency ? UC.fmt.money(f.amount, f.currency) : UC.fmt.num(f.amount)) : (f.textValue || "");
        var b = h("button", { type: "button", class: "fact " + prov.vclass(f), data: { prov: f["@id"] } }, h("b", null, val), h("span", null, UC.metricLabel(f.metric) + " · " + UC.fmt.date(f)), h("span", { html: "<span style='color:var(--vc)'>" + UC.glyph(f.assertedBy) + "</span> " + UC.esc(prov.sourceShort(f)) }));
        fb.appendChild(b);
      });
      sec.appendChild(h("h4", null, L("Reported figures about the company", "Cifras informadas sobre la empresa") + " (" + facts.length + ")")); sec.appendChild(fb);
    } else sec.appendChild(h("div", { class: "empty" }, L("No financial figure about this company in the graph. The record gives income and equity in running text; see the case events.", "No hay cifras financieras de esta empresa en el grafo. El acta da ingresos y patrimonio en el texto; véanse los hechos del caso.")));
    var fc = db.extra.finCredit, raw = p.identifier;
    var ms = fc && Array.isArray(fc.metrics) ? fc.metrics.filter(function (m) { return m.entity === raw; }) : [];
    if (ms.length) {
      sec.appendChild(h("h4", null, L("Ratios computed by the AI credit analyst (not source figures)", "Ratios calculados por el analista de crédito de IA (no son cifras de la fuente)")));
      sec.appendChild(UC.metricTable(ms));
    }
    root.appendChild(sec);
  }

  /** Table of analyst metrics with inputs and refs; shared with the Analysis view. */
  UC.metricTable = function (ms) {
    return ui.table([
      { label: L("Entity", "Entidad"), render: function (m) { return UC.resolve(m.entity) ? ui.party(UC.resolve(m.entity)["@id"]) : m.entity; }, sort: function (m) { return m.entity; } },
      { label: L("Metric", "Métrica"), render: function (m) { return h("span", null, UC.px(m, "label"), UC.px(m, "note") ? h("div", { class: "small muted" }, UC.px(m, "note")) : null); } },
      { label: L("Value", "Valor"), cls: "r", render: function (m) { return h("b", null, UC.fmt.num(m.value, 2) + " " + (m.unit || "")); }, sort: function (m) { return m.value; } },
      { label: L("Inputs (each with its source)", "Insumos (cada uno con su fuente)"), render: function (m) {
        var box = h("div", { class: "small" });
        (m.inputs || []).forEach(function (i) { box.appendChild(h("div", null, i.what + ": ", h("span", { class: "num" }, (i.currency ? i.currency + " " : "") + UC.fmt.num(i.value)), " ", i.ref ? prov.chip(i.ref) : null)); });
        return box;
      } }
    ], ms, { pageSize: 40, minWidth: 900 });
  };

  UC.views.flows = {
    render: function (root, sub, s) {
      UC.filterDefaults(s);
      var tabs = [{ id: "circuit", label: L("June 2026 circuit", "Circuito de junio de 2026") }, { id: "chains", label: L("Reconstructed chains", "Cadenas reconstruidas") }, { id: "all", label: L("All flows", "Todos los flujos") }, { id: "borrowers", label: L("By borrower", "Por prestataria") }];
      if (sub && tabs.some(function (t) { return t.id === sub; })) s.tab = sub;
      if (!s.tab) s.tab = "circuit";
      root.appendChild(h("div", { class: "view-head" }, h("h2", null, L("Money flows", "Flujos de dinero")),
        h("p", null, L("Who is said to have paid whom. Every band, cell and row is a claim by a named voice and opens its source. Guaraníes and dollars are kept apart and nothing is converted or added across sources.", "Quién habría pagado a quién. Cada banda, celda y fila es una afirmación de una voz identificada y abre su fuente. Guaraníes y dólares van separados; nada se convierte ni se suma entre fuentes."))));
      root.appendChild(ui.tabs(tabs, s.tab, function (t) { s.tab = t; UC.go("flows", null, t); }, L("Flow views", "Vistas de flujos")));
      var body = h("div", { class: "stack", style: "gap:16px" });
      root.appendChild(body);
      ({ circuit: circuit, chains: chains, all: allFlows, borrowers: borrowers })[s.tab](body, s);
    }
  };
})();
