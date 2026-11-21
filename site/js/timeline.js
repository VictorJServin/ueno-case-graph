/* timeline.js - one shared, zoomable, brushable time axis with four lane sets:
   transactions, case events, role holdings (Gantt) and issues/conflicts. Marks open provenance. */
(function () {
  "use strict";
  var UC = window.UC, h = UC.h, s$ = UC.s, L = UC.L, prov = UC.prov, ui = UC.ui;
  var DAY = 864e5, T0 = Date.UTC(2019, 0, 1), T1 = Date.UTC(2026, 10, 20), PAD = 25 * DAY;
  var CATS = ["cat_corporate", "cat_credit", "cat_supervisory", "cat_criminal", "cat_political", "cat_market", "cat_depositor", "cat_statement"];
  function ms(iso) { return Date.UTC(+iso.slice(0, 4), (+iso.slice(5, 7) || 1) - 1, +iso.slice(8, 10) || 1); }
  /** [start, end, isRange] of a node, widening month/year precision to the whole period. */
  function span(n, end) {
    if (!n.sortDate) return null;
    var a = ms(n.sortDate), b = a, p = UC.precision(n), range = false;
    if (n.sortDateEnd && n.sortDateEnd > n.sortDate) { b = ms(n.sortDateEnd); range = true; }
    else if (p === "month") { b = Date.UTC(+n.sortDate.slice(0, 4), +n.sortDate.slice(5, 7), 0); range = true; }
    else if (p === "year") { b = Date.UTC(+n.sortDate.slice(0, 4), 11, 31); range = true; }
    return [a, b, range];
  }
  function vcol(g) { return "var(--v-" + (g === "prosecution" ? "pros" : g) + ")"; }

  function defaults(s) {
    UC.filterDefaults(s);
    if (!s.mode) s.mode = "events";
    if (!s.lanesBy) s.lanesBy = "borrower";
    if (!s.cats) { s.cats = {}; CATS.forEach(function (c) { s.cats[c] = true; }); }
    if (!s.domain) s.domain = [Date.UTC(2025, 5, 1), T1 + PAD];
  }

  /* ---------- items per mode ---------- */
  function build(s) {
    var db = UC.db, items = [], lanes = [], laneOf, undated = 0, note = "";
    var ok = function (n) { return UC.pass(n, s) && (!s.party || (n.involvesParty || []).indexOf(s.party) >= 0); };
    if (s.mode === "tx") {
      var list = db.loans.concat(db.flows).filter(ok), maxA = { USD: 0, PYG: 0 };
      list.forEach(function (n) { var a = UC.amountOf(n); if (a != null && n.currency) maxA[n.currency] = Math.max(maxA[n.currency] || 0, a); });
      if (s.lanesBy === "currency") {
        lanes = [{ id: "USD", label: "USD" }, { id: "PYG", label: "PYG" }, { id: "none", label: L("No amount stated", "Sin monto indicado") }];
        laneOf = function (n) { return UC.amountOf(n) == null || !n.currency ? "none" : n.currency; };
      } else {
        var cnt = {}, bOf = function (n) {
          if (UC.isLoan(n)) return n.nominalBorrower;
          var ll = n.linkedLoan && db.byId[n.linkedLoan];
          if (ll) return ll.nominalBorrower;
          return db.borrowers[n.fromParty] ? n.fromParty : db.borrowers[n.toParty] ? n.toParty : "other";
        };
        list.forEach(function (n) { if (n.sortDate) { var b = bOf(n); cnt[b] = (cnt[b] || 0) + 1; } });
        var top = Object.keys(cnt).filter(function (k) { return k !== "other"; }).sort(function (a, b) { return cnt[b] - cnt[a]; }).slice(0, 14), inTop = {};
        top.forEach(function (b) { inTop[b] = 1; lanes.push({ id: b, label: UC.short(b), party: b }); });
        lanes.push({ id: "other", label: L("Other parties", "Otras partes") });
        laneOf = function (n) { var b = bOf(n); return inTop[b] ? b : "other"; };
      }
      list.forEach(function (n) {
        var sp = span(n); if (!sp) { undated++; return; }
        var a = UC.amountOf(n);
        items.push({ n: n, lane: laneOf(n), t0: sp[0], t1: sp[1], range: sp[2], r: a != null && n.currency && maxA[n.currency] ? 3.5 + 10 * Math.sqrt(a / maxA[n.currency]) : 3.5, hollow: UC.isLoan(n), noAmt: a == null });
      });
      note = L("Loans are outlined marks, flows are filled. Mark size grows with the amount within its own currency (USD and PYG are scaled separately). The smallest marks have no stated amount.", "Los préstamos son marcas huecas y los flujos, llenas. El tamaño crece con el monto dentro de su propia moneda (USD y PYG se escalan por separado). Las marcas más pequeñas no tienen monto indicado.");
    } else if (s.mode === "events") {
      CATS.forEach(function (c) { if (s.cats[c]) lanes.push({ id: c, label: UC.enumLabel(c) }); });
      (db.byType.CaseEvent || []).filter(ok).forEach(function (n) {
        if (!s.cats[n.eventCategory]) return;
        var sp = span(n); if (!sp) { undated++; return; }
        items.push({ n: n, lane: n.eventCategory, t0: sp[0], t1: sp[1], range: sp[2], r: 5 });
      });
      note = L("One mark per reported event, in the lane of its category.", "Una marca por hecho informado, en el carril de su categoría.");
    } else if (s.mode === "parties") {
      var roles = db.roles.filter(function (r) { return ok(r) && (r.sortDate || r.sortDateEnd) && r.roleType !== "role_relative_of"; }), per = {};
      roles.forEach(function (r) { (per[r.organisation] = per[r.organisation] || []).push(r); });
      var orgs = Object.keys(per).sort(function (a, b) { return (db.borrowers[b] ? 1 : 0) - (db.borrowers[a] ? 1 : 0) || per[b].length - per[a].length; });
      if (!s.party && !s.allOrgs) orgs = orgs.filter(function (o) { return db.borrowers[o] || o === "ucr:org/ueno-bank"; }).slice(0, 14);
      orgs.forEach(function (o) {
        lanes.push({ id: o, label: UC.short(o), party: o, gantt: true });
        per[o].forEach(function (r) {
          var a = r.sortDate ? ms(r.sortDate) : null, b = r.sortDateEnd ? ms(r.sortDateEnd) : null;
          items.push({ n: r, lane: o, t0: a == null ? T0 : a, t1: b == null ? T1 : b, bar: true, openStart: a == null, openEnd: b == null, own: /shareholder|beneficial|controlling|founder/.test(r.roleType) });
        });
        (db.borrowers[o] || []).filter(function (l) { return UC.pass(l, s) && l.sortDate; }).forEach(function (l) { var sp = span(l); items.push({ n: l, lane: o, t0: sp[0], t1: sp[1], tick: true }); });
      });
      undated = db.roles.filter(ok).length - roles.length;
      note = L("Bars are role holdings with a stated start or end: solid for ownership and control, outlined for offices. A faded end means the source gives no date on that side. Vertical ticks above the bars are the dates of Ueno Bank loans to that company, so changes of ownership can be read against disbursements.", "Las barras son cargos o participaciones con inicio o fin indicados: llenas para propiedad y control, huecas para cargos. Un extremo difuminado significa que la fuente no da fecha de ese lado. Las marcas verticales sobre las barras son las fechas de préstamos de Ueno Bank a esa empresa, para leer los cambios de propiedad frente a los desembolsos.");
    } else {
      var types = ["Loan", "Flow", "CaseEvent", "FinancialFact", "RoleHolding", "Charge"];
      types.forEach(function (t) { lanes.push({ id: t, label: UC.enumLabel(t) }); });
      db.assertions.filter(function (n) { return UC.isConflict(n) && ok(n); }).forEach(function (n) {
        var sp = span(n); if (!sp) { undated++; return; }
        var k = UC.kind(n); if (types.indexOf(k) < 0) return;
        items.push({ n: n, lane: k, t0: sp[0], t1: sp[1], range: sp[2], r: 5 });
      });
      note = L("Rows whose provenance note records a conflict between sources, by kind of claim and by the date of the thing claimed.", "Filas cuya nota de procedencia registra un conflicto entre fuentes, por tipo de afirmación y por la fecha de lo afirmado.");
    }
    return { items: items, lanes: lanes, undated: undated, note: note };
  }

  UC.views.timeline = {
    render: function (root, sub, s) {
      defaults(s);
      if (sub && ["tx", "events", "parties", "issues"].indexOf(sub) >= 0) s.mode = sub;
      var db = UC.db;
      root.appendChild(h("div", { class: "view-head" }, h("h2", null, L("Timelines", "Cronologías")),
        h("p", null, L("One time axis, four ways to fill it. Drag to pan, scroll or pinch to zoom, or drag the handles on the strip underneath. Dates given only to the month or year are drawn as bars covering the whole period, not as points. Select any mark for its source.", "Un eje temporal y cuatro formas de llenarlo. Arrastre para mover, use la rueda o pellizque para acercar, o arrastre los bordes de la franja inferior. Las fechas dadas solo por mes o año se dibujan como barras que cubren todo el período, no como puntos. Seleccione cualquier marca para ver su fuente."))));
      root.appendChild(ui.tabs([{ id: "events", label: L("Case events", "Hechos del caso") }, { id: "tx", label: L("Transactions", "Transacciones") }, { id: "parties", label: L("Owners and officers", "Dueños y directivos") }, { id: "issues", label: L("Issues and conflicts", "Inconsistencias y conflictos") }],
        s.mode, function (m) { s.mode = m; UC.go("timeline", null, m); }, L("Lanes", "Carriles")));

      var data = build(s);
      /* controls */
      var ctl = h("div", { class: "controls" });
      function zoomTo(a, b) { s.domain = [a, b]; applyDomain(); }
      ctl.appendChild(ui.ctl(L("Quick zoom", "Zoom rápido"), h("div", { class: "row" },
        h("button", { type: "button", class: "btn sm", onclick: function () { zoomTo(T0, T1 + PAD); } }, L("2019 to 20 Nov 2026", "2019 al 20 nov 2026")),
        h("button", { type: "button", class: "btn sm", onclick: function () { zoomTo(Date.UTC(2025, 5, 1), T1 + PAD); } }, L("Jun 2025 to Nov 2026", "Jun 2025 a nov 2026")),
        h("button", { type: "button", class: "btn sm", onclick: function () { zoomTo(Date.UTC(2026, 5, 8), Date.UTC(2026, 5, 19)); } }, L("11 to 15 June 2026", "11 al 15 de junio de 2026")),
        h("button", { type: "button", class: "btn sm", onclick: function () { zoomTo(Date.UTC(2026, 9, 25), T1 + 3 * DAY); } }, L("Nov 2026", "Nov 2026")))));
      if (s.mode === "tx") ctl.appendChild(ui.ctl(L("Lanes", "Carriles"), ui.seg([{ v: "borrower", l: L("Per borrower", "Por prestataria") }, { v: "currency", l: L("Per currency", "Por moneda") }], s.lanesBy, function (v) { s.lanesBy = v; UC.rerender(); })));
      if (s.mode === "parties") ctl.appendChild(ui.ctl(L("Companies", "Empresas"), ui.seg([{ v: false, l: L("Borrowers and the bank", "Prestatarias y el banco") }, { v: true, l: L("All with dated roles", "Todas con fechas") }], !!s.allOrgs, function (v) { s.allOrgs = v; UC.rerender(); })));
      var ac = ui.autocomplete({ placeholder: L("Filter by person or company", "Filtrar por persona o empresa"), items: function () { return ui.partyItems(); }, onPick: function (it) { s.party = it.id; UC.rerender(); } });
      ctl.appendChild(ui.ctl(L("Party", "Parte"), s.party ? h("div", { class: "row" }, ui.party(s.party), h("button", { type: "button", class: "btn sm", onclick: function () { s.party = null; UC.rerender(); } }, L("Clear", "Quitar"))) : ac));
      ui.sourceFilters(s, UC.rerender, null, false).forEach(function (c) { ctl.appendChild(c); });
      if (s.mode === "events") ctl.appendChild(ui.ctl(L("Category", "Categoría"), ui.pills(CATS.map(function (c) { return { v: c, l: UC.enumLabel(c) }; }), s.cats, UC.rerender, L("Category", "Categoría"))));
      root.appendChild(ctl);

      if (s.mode === "issues") {
        var issues = (db.byType.Issue || []).filter(function (n) { return UC.pass(n, s); });
        var ib = h("div", { class: "grid gauto" });
        issues.forEach(function (n) {
          ib.appendChild(h("div", { class: "card stack " + prov.vclass(n) }, h("div", { class: "row between" }, h("b", { class: "small" }, n.issueLocation || ""), prov.src(n)), h("div", { class: "small" }, UC.tx(n.description))));
        });
        root.appendChild(h("section", { class: "sec" }, h("h3", null, L("Recorded data issues (undated)", "Inconsistencias registradas (sin fecha)") + " (" + issues.length + ")"),
          h("p", { class: "small muted", style: "margin:0" }, L("Misprints, internal contradictions and differences between documents that contributors wrote down while reading. They describe the sources, not anyone's conduct.", "Erratas, contradicciones internas y diferencias entre documentos que los colaboradores anotaron al leer. Describen las fuentes, no la conducta de nadie.")), ib));
      }

      /* figure */
      var fig = h("figure", { class: "fig" }), host = h("div", { class: "scroll tl-stage" }), listHost = h("div", { class: "card tl-list" }), cap = h("figcaption");
      fig.appendChild(h("div", { class: "hint" }, L("Swipe sideways to see the whole figure.", "Deslice hacia los lados para ver toda la figura.")));
      fig.appendChild(legend(s)); fig.appendChild(host); fig.appendChild(cap);
      root.appendChild(fig);
      root.appendChild(h("section", { class: "sec" }, h("h3", { id: "tl-list-h" }, ""), listHost));

      var W, mL = 150, mR = 16, axisH = 26, ctxH = 46, x, x0, svg, gMarks, gAxis, brushG, brush, zoom, muteBrush = false, muteZoom = false, raf = 0;
      var early = data.items.filter(function (i) { return i.t1 < T0; }), late = data.items.filter(function (i) { return i.t0 > T1 + PAD; });

      function layout() {
        W = Math.max(880, host.clientWidth || 880);
        host.innerHTML = "";
        x0 = d3.scaleUtc().domain([T0, T1 + PAD]).range([mL, W - mR]);
        x = x0.copy().domain(s.domain);
        svg = s$("svg", { width: W, role: "img", "aria-label": L("Timeline: ", "Cronología: ") + data.items.length + L(" dated items in ", " ítems fechados en ") + data.lanes.length + L(" lanes", " carriles"), style: "min-width:" + W + "px;touch-action:pan-y" });
        svg.appendChild(s$("defs", null, s$("clipPath", { id: "tl-clip" }, s$("rect", { x: mL, y: 0, width: W - mL - mR, height: 4000 }))));
        gAxis = s$("g", { class: "axis" }); gMarks = s$("g"); brushG = s$("g", { class: "brush" });
        svg.appendChild(gAxis); svg.appendChild(gMarks); svg.appendChild(brushG);
        host.appendChild(svg);
        zoom = d3.zoom().scaleExtent([1, 900]).translateExtent([[mL, 0], [W - mR, 10]]).extent([[mL, 0], [W - mR, 10]])
          .filter(function (ev) { return (!ev.ctrlKey || ev.type === "wheel") && !ev.button && !(ev.target && ev.target.closest && ev.target.closest(".brush")); })
          .on("zoom", function (ev) { if (muteZoom) return; s.domain = ev.transform.rescaleX(x0).domain().map(Number); x.domain(s.domain); schedule(true); });
        d3.select(svg).call(zoom).on("dblclick.zoom", null);
        applyDomain();
      }
      function applyDomain() {
        var a = Math.max(T0, s.domain[0]), b = Math.min(T1 + PAD, s.domain[1]);
        if (b - a < DAY) b = a + DAY;
        s.domain = [a, b]; x.domain(s.domain);
        var k = (x0.range()[1] - x0.range()[0]) / (x0(b) - x0(a)), t = d3.zoomIdentity.translate(mL - x0(a) * k, 0).scale(k);
        muteZoom = true; d3.select(svg).call(zoom.transform, t); muteZoom = false;
        draw(true);
      }
      function schedule(moveBrush) { if (raf) return; raf = requestAnimationFrame(function () { raf = 0; draw(moveBrush); }); }
      var listLater = UC.debounce(drawList, 180);

      function draw(moveBrush) {
        gMarks.innerHTML = ""; gAxis.innerHTML = "";
        var y = axisH + 8, d0 = s.domain[0], d1 = s.domain[1], x1 = W - mR;
        data.lanes.forEach(function (lane, li) {
          var its = data.items.filter(function (i) { return i.lane === lane.id && i.t1 >= d0 - 40 * DAY && i.t0 <= d1 + 40 * DAY; }), g = s$("g", { "clip-path": "url(#tl-clip)" }), rows = [], laneH;
          if (lane.gantt) {
            var bars = its.filter(function (i) { return i.bar; }).sort(function (a, b) { return (b.own ? 1 : 0) - (a.own ? 1 : 0) || a.t0 - b.t0; }), ticks = its.filter(function (i) { return i.tick; });
            var bh = 13, top = y + 12;
            bars.forEach(function (it, bi) {
              var xa = Math.max(mL - 20, x(it.t0)), xb = Math.min(x1 + 20, x(it.t1)), yy = top + bi * (bh + 3), n = it.n, w = Math.max(4, xb - xa);
              var lab = UC.short(n.holder) + " · " + UC.enumLabel(n.roleType) + (n.percentage ? " " + UC.fmt.pct(n.percentage) : "");
              var r = s$("rect", { x: xa, y: yy, width: w, height: bh, rx: 3, fill: it.own ? vcol(n.graph) : "var(--card)", "fill-opacity": it.own ? 0.38 : 1, stroke: vcol(n.graph), "stroke-width": 1.4, "stroke-dasharray": it.openStart || it.openEnd ? "none" : null, "data-tip": prov.tip(n) });
              if (it.openEnd || it.openStart) { r.setAttribute("fill", "url(#tl-fade-" + n.graph + (it.own ? "-own" : "") + (it.openStart ? "-s" : "") + ")"); r.setAttribute("stroke-dasharray", "4 3"); }
              prov.attach(r, n["@id"], lab + ", " + UC.roleDates(n));
              g.appendChild(r);
              var tx = Math.max(mL + 4, xa + 5), fits = xb - tx > lab.length * 6.1;
              g.appendChild(s$("text", { x: fits ? tx : Math.min(x1 - 4, xb + 5), y: yy + bh - 3, "font-size": 11, "pointer-events": "none", "text-anchor": !fits && xb + 5 + lab.length * 6 > x1 ? "end" : "start", "paint-order": fits ? null : "stroke", stroke: fits ? null : "var(--card)", "stroke-width": fits ? null : 3, text: lab }));
            });
            ticks.forEach(function (it) {
              var xx = x(it.t0), tk = s$("path", { d: "M" + xx + "," + (y - 1) + "v9", stroke: "var(--out)", "stroke-width": 2.5, "stroke-linecap": "round", "data-tip": prov.tip(it.n) });
              prov.attach(tk, it.n["@id"], UC.describe(it.n).title); g.appendChild(tk);
              g.appendChild(s$("path", { d: "M" + xx + "," + (y + 9) + "V" + (top + bars.length * (bh + 3)), stroke: "var(--out)", "stroke-width": 1, "stroke-opacity": 0.35, "stroke-dasharray": "2 3", "pointer-events": "none" }));
            });
            laneH = 16 + Math.max(1, bars.length) * (bh + 3) + 6;
          } else {
            its.sort(function (a, b) { return a.t0 - b.t0 || (b.r || 0) - (a.r || 0); });
            var rowH = s.mode === "tx" ? 22 : 15, maxRows = s.mode === "tx" ? 5 : 7;
            its.forEach(function (it) {
              var xa = x(it.t0), xb = it.range ? Math.max(xa + 5, x(it.t1)) : xa, r = Math.min(it.r || 5, rowH / 2 + 3), lo = xa - r - 1, hi = Math.max(xb, xa + r) + 1, row = 0;
              while (row < maxRows - 1 && rows[row] != null && rows[row] > lo) row++;
              rows[row] = Math.max(rows[row] || -1e9, hi); it._row = row; it._xa = xa; it._xb = xb; it._r = r;
            });
            laneH = Math.max(1, rows.length) * rowH + 8;
            its.forEach(function (it) {
              var cy = y + 4 + it._row * rowH + rowH / 2, n = it.n, col = vcol(n.graph), d = UC.describe(n);
              var mark = s$("g", { "data-tip": prov.tip(n) });
              if (it.range) mark.appendChild(s$("rect", { x: it._xa, y: cy - 1.5, width: Math.max(4, it._xb - it._xa), height: 3, rx: 1.5, fill: col, "fill-opacity": 0.32 }));
              mark.appendChild(s$("path", { transform: "translate(" + it._xa + "," + cy + ")", d: UC.glyphPath(n.assertedBy, Math.max(3, it._r * 0.82)), "fill-rule": "evenodd", fill: it.hollow ? "var(--card)" : col, "fill-opacity": it.hollow ? 1 : (it.noAmt ? 0.45 : 0.88), stroke: it.hollow ? col : "var(--card)", "stroke-width": it.hollow ? 2 : 1 }));
              prov.attach(mark, n["@id"], UC.fmt.date(n) + ": " + d.title);
              g.appendChild(mark);
            });
          }
          gMarks.appendChild(s$("rect", { x: 0, y: y, width: W, height: laneH, fill: li % 2 ? "var(--soft)" : "none", "fill-opacity": 0.45 }));
          var ll = s$("text", { class: "tl-lane-label", x: mL - 10, y: y + 15, "text-anchor": "end", "font-size": 12, text: lane.label.length > 21 ? lane.label.slice(0, 20) + "…" : lane.label });
          if (lane.party) { ll.setAttribute("data-party", lane.party); ll.style.fill = "var(--ink)"; }
          gMarks.appendChild(ll); gMarks.appendChild(g);
          y += laneH;
        });
        if (!data.lanes.length) y += 30;
        /* axis + grid */
        var ticksT = x.ticks(Math.max(4, Math.floor((W - mL) / 110))), fmtT = x.tickFormat();
        ticksT.forEach(function (t) {
          var xx = x(t);
          gAxis.appendChild(s$("line", { class: "gridl", x1: xx, x2: xx, y1: axisH, y2: y }));
          gAxis.appendChild(s$("text", { x: xx, y: 16, "text-anchor": "middle", text: tickLabel(t, fmtT) }));
        });
        gAxis.appendChild(s$("line", { x1: mL, x2: x1, y1: axisH, y2: axisH, stroke: "var(--rule-strong)" }));
        var cut = x(T1);
        if (cut > mL && cut < x1) { gAxis.appendChild(s$("line", { x1: cut, x2: cut, y1: axisH - 6, y2: y, stroke: "var(--ink)", "stroke-dasharray": "2 3" })); gAxis.appendChild(s$("text", { x: cut - 4, y: axisH + 12, "text-anchor": "end", "font-size": 10.5, class: "sub", text: L("data cutoff 20 Nov 2026", "corte de datos 20 nov 2026") })); }
        /* context strip with brush */
        var cy0 = y + 14;
        if (moveBrush !== "skip") {
          brushG.innerHTML = "";
          var bins = d3.bin().domain([T0, T1 + PAD]).thresholds(120).value(function (i) { return i.t0; })(data.items.filter(function (i) { return !i.tick; }));
          var maxB = d3.max(bins, function (b) { return b.length; }) || 1;
          bins.forEach(function (b) { if (b.length) brushG.appendChild(s$("rect", { x: x0(b.x0), y: cy0 + ctxH - 14 - (ctxH - 16) * Math.sqrt(b.length / maxB), width: Math.max(1, x0(b.x1) - x0(b.x0) - 0.5), height: (ctxH - 16) * Math.sqrt(b.length / maxB), fill: "var(--muted)", "fill-opacity": 0.55 })); });
          d3.range(2019, 2027).forEach(function (yr) { brushG.appendChild(s$("text", { x: x0(Date.UTC(yr, 0, 1)) + 3, y: cy0 + ctxH - 2, "font-size": 10.5, class: "sub", text: yr })); brushG.appendChild(s$("line", { class: "gridl", x1: x0(Date.UTC(yr, 0, 1)), x2: x0(Date.UTC(yr, 0, 1)), y1: cy0, y2: cy0 + ctxH })); });
          brushG.appendChild(s$("text", { x: mL - 10, y: cy0 + 16, "text-anchor": "end", "font-size": 11, class: "sub", text: L("whole period", "período completo") }));
          brush = d3.brushX().extent([[mL, cy0], [x1, cy0 + ctxH - 13]]).on("brush end", function (ev) {
            if (muteBrush || !ev.sourceEvent || !ev.selection) return;
            s.domain = [Number(x0.invert(ev.selection[0])), Number(x0.invert(ev.selection[1]))]; x.domain(s.domain);
            var k = (x0.range()[1] - x0.range()[0]) / (ev.selection[1] - ev.selection[0]);
            muteZoom = true; d3.select(svg).call(zoom.transform, d3.zoomIdentity.translate(mL - ev.selection[0] * k, 0).scale(k)); muteZoom = false;
            draw("skip");
          });
          var bsel = d3.select(brushG).append("g").attr("class", "brush");
          bsel.call(brush);
          muteBrush = true; bsel.call(brush.move, [x0(s.domain[0]), x0(s.domain[1])]); muteBrush = false;
          bsel.select(".selection").attr("fill", "var(--grp)").attr("fill-opacity", 0.18).attr("stroke", "var(--grp)");
          bsel.selectAll(".handle").attr("fill", "var(--grp)").attr("fill-opacity", 0.7);
        }
        var total = cy0 + ctxH + 6;
        svg.setAttribute("height", total); svg.setAttribute("viewBox", "0 0 " + W + " " + total);
        listLater();
      }
      function tickLabel(t, f) {
        var spanD = (s.domain[1] - s.domain[0]) / DAY, iso = new Date(+t).toISOString().slice(0, 10);
        if (spanD > 1500) return iso.slice(0, 4);
        if (spanD > 150) return UC.fmt.dateStr(iso, "month");
        return UC.fmt.dateStr(iso, "day");
      }
      function drawList() {
        var d0 = s.domain[0], d1 = s.domain[1];
        var inView = data.items.filter(function (i) { return i.t1 >= d0 && i.t0 <= d1; }).map(function (i) { return i.n; }).sort(UC.byDate);
        var hd = document.getElementById("tl-list-h");
        if (hd) hd.textContent = L("In view: ", "En vista: ") + inView.length + L(" items, ", " ítems, ") + UC.fmt.dateStr(new Date(d0).toISOString().slice(0, 10), "day") + " – " + UC.fmt.dateStr(new Date(Math.min(d1, T1)).toISOString().slice(0, 10), "day");
        listHost.innerHTML = "";
        listHost.appendChild(ui.voiceCount(inView));
        listHost.appendChild(ui.paged(inView, 40, function (part) { return ui.alist(part, { noGroup: s.mode !== "tx" }); }));
      }
      cap.appendChild(document.createTextNode(data.note + " "));
      if (data.undated) cap.appendChild(document.createTextNode(data.undated + L(" matching rows have no usable date and are not drawn. ", " filas coincidentes no tienen fecha utilizable y no se dibujan. ")));
      if (early.length) cap.appendChild(h("button", { type: "button", class: "more", data: { prov: early.slice(0, 80).map(function (i) { return i.n["@id"]; }).join(" ") } }, early.length + L(" items before 2019", " ítems anteriores a 2019")));
      if (late.length) { cap.appendChild(document.createTextNode(" ")); cap.appendChild(h("button", { type: "button", class: "more", data: { prov: late.slice(0, 80).map(function (i) { return i.n["@id"]; }).join(" ") } }, late.length + L(" items dated after the cutoff (maturities, projections)", " ítems con fecha posterior al corte (vencimientos, proyecciones)"))); }

      /* gradient defs for open-ended bars are added once per layout */
      function fades() {
        var defs = svg.querySelector("defs");
        UC.VOICES.forEach(function (v) {
          [["", 0.75, false], ["-own", 0.75, false], ["-s", 0.75, true], ["-own-s", 0.75, true]].forEach(function (o) {
            var own = o[0].indexOf("own") >= 0, col = own ? vcol(v) : "var(--card)";
            var lg = s$("linearGradient", { id: "tl-fade-" + v + o[0], x1: o[2] ? 1 : 0, x2: o[2] ? 0 : 1, y1: 0, y2: 0 });
            lg.appendChild(s$("stop", { offset: "0%", "stop-color": col, "stop-opacity": own ? 0.38 : 1 }));
            lg.appendChild(s$("stop", { offset: "70%", "stop-color": col, "stop-opacity": own ? 0.3 : 1 }));
            lg.appendChild(s$("stop", { offset: "100%", "stop-color": col, "stop-opacity": own ? 0.04 : 0.2 }));
            defs.appendChild(lg);
          });
        });
      }
      function full() { layout(); fades(); draw(true); }
      full();
      var lastW = host.clientWidth, onResize = UC.debounce(function () { if (Math.abs(host.clientWidth - lastW) > 4) { lastW = host.clientWidth; full(); } }, 120);
      window.addEventListener("resize", onResize);
      UC.onLeave = function () { window.removeEventListener("resize", onResize); if (raf) cancelAnimationFrame(raf); UC.tip.hide(); };
    }
  };

  function legend(s) {
    var lg = ui.legendVoices();
    if (s.mode === "tx") {
      lg.appendChild(h("span", { html: "<svg width='14' height='14' viewBox='-7 -7 14 14' aria-hidden='true'><circle r='5' fill='none' stroke='currentColor' stroke-width='2'/></svg>" + UC.esc(L("loan record", "registro de préstamo")) }));
      lg.appendChild(h("span", { html: "<svg width='14' height='14' viewBox='-7 -7 14 14' aria-hidden='true'><circle r='5' fill='currentColor'/></svg>" + UC.esc(L("flow", "flujo")) }));
    }
    if (s.mode !== "parties") lg.appendChild(h("span", { html: "<svg width='30' height='10' aria-hidden='true'><rect x='0' y='2.5' width='30' height='5' rx='2.5' fill='currentColor' fill-opacity='.4'/><circle cx='4' cy='5' r='4' fill='currentColor'/></svg>" + UC.esc(L("date known only to the month or year (whole period shown)", "fecha conocida solo por mes o año (se muestra el período)")) }));
    else lg.appendChild(h("span", { html: "<svg width='10' height='12' aria-hidden='true'><path d='M5 1v10' stroke='var(--out)' stroke-width='2.5' stroke-linecap='round'/></svg>" + UC.esc(L("Ueno Bank loan to the company", "préstamo de Ueno Bank a la empresa")) }));
    return lg;
  }
})();
