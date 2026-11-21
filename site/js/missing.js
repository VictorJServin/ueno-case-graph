/* missing.js - "Missing money": how much is missing, where it is thought to have gone, what might be
   recovered, and how to find out. Reads data/missing_money.json (optional). Nothing here is added by the
   page: every figure is shown as the file gives it, nulls are "not known", and meanings are never summed. */
(function () {
  "use strict";
  var UC = window.UC, h = UC.h, s$ = UC.s, L = UC.L, prov = UC.prov, ui = UC.ui, M = UC.mmLabel;

  var NK = function () { return L("not known", "no se sabe"); };
  function num(v) { return typeof v === "number" && isFinite(v) ? v : null; }
  /** Money, compact, null-safe; the exact figure is in the title. */
  function usd(v, cur, exact) {
    if (num(v) == null) return h("span", { class: "muted" }, NK());
    return h("span", { class: "num", title: UC.fmt.money(v, cur || "USD") }, UC.fmt.money(v, cur || "USD", { compact: !exact }));
  }
  function usdT(v, cur) { return num(v) == null ? NK() : UC.fmt.money(v, cur || "USD", { compact: true }); }
  function pct(v) { return num(v) == null ? NK() : UC.fmt.num(v, 1) + "%"; }
  function asOf(d) { if (!d) return ""; d = String(d); return UC.fmt.dateStr(d, d.length === 4 ? "year" : d.length === 7 ? "month" : "day"); }
  var ASSERT = { regulator: ["Regulator", "v-press"], prosecution: ["Prosecution", "v-prosecution"], rey: ["Rey", "v-rey"], press: ["Press", "v-press"], rating_agency: ["RatingAgency", "v-press"], company: ["Company", "v-press"], defence: ["Defence", "v-press"], analyst: ["Analyst", "v-analyst"] };
  function who(code) {
    if (!code) return null;
    var a = ASSERT[code] || ["Press", "v-press"];
    return h("span", { class: "badge " + a[1], html: UC.glyph(a[0]) + UC.esc(M(code)) });
  }
  function vcls(code) { return (ASSERT[code] || ["", ""])[1]; }
  function kmark(kind) { return kind ? h("span", { class: "kmark k-" + kind, title: L("Kind of figure", "Tipo de cifra") }, h("i"), M(kind)) : null; }
  function conf(c) { return c ? h("span", { class: "small muted" }, prov.conf(c), " " + L("confidence ", "confianza ") + UC.enumLabel(c)) : null; }
  function link(url, label) { return url && /^https?:\/\//.test(url) ? h("a", { href: url, target: "_blank", rel: "noopener", class: "small" }, label || L("source", "fuente")) : null; }
  function refs(list, url, max) {
    var has = (list && list.length) || (url && /^https?:/.test(url));
    if (!has) return null;
    var box = h("div", { class: "small" }, h("span", { class: "muted" }, L("Rests on: ", "Se apoya en: ")));
    if (list && list.length) box.appendChild(chips(list, max || 5));
    var a = link(url, L("open source", "abrir fuente")); if (a) { box.appendChild(document.createTextNode(" ")); box.appendChild(a); }
    return box;
  }
  /** Like prov.chips, but the analysts' own computation id gets a readable plain label. */
  /** Chip to the AnalystOpinion node stored for a JSON path (e.g. "/meanings/2"); its drawer lists the basedOn rows. */
  function opinion(path) {
    var o = UC.db.opinionAt[path];
    if (!o) return null;
    return h("div", { class: "small" }, h("span", { class: "muted" }, L("In the graph as: ", "En el grafo como: ")), prov.chip(o), (o.basedOn || []).length ? h("button", { type: "button", class: "more", data: { prov: o.basedOn.join(" ") } }, L("the ", "las ") + o.basedOn.length + L(" sourced rows it rests on", " filas con fuente en que se apoya")) : null);
  }
  function chips(list, max) {
    var own = list.filter(function (r) { return /^src:analysis-/.test(r); }), rest = list.filter(function (r) { return own.indexOf(r) < 0; });
    var box = rest.length ? prov.chips(rest, max) : h("span", { class: "refs" }), lab = L("analysts' own computation", "cálculo de los analistas");
    if (own.length) box.appendChild(UC.resolve(own[0]) ? prov.chip(own[0], lab) : h("span", { class: "chip plain", title: own[0] }, lab));
    return box;
  }
  /** Range bar on a shared scale [0, max]; any of low / central / high may be null. */
  function rangeBar(lo, mid, hi, max, cls, line) {
    var w = h("div", { class: "rbw" }), b = h("div", { class: "rb " + (cls || "") });
    lo = num(lo); mid = num(mid); hi = num(hi);
    if (lo == null && mid == null && hi == null) { w.appendChild(h("span", { class: "small muted" }, NK())); return w; }
    var p = function (v) { return Math.max(0, Math.min(100, v / max * 100)); };
    b.appendChild(h("div", { class: "track" }));
    if (lo != null && hi != null) b.appendChild(h("div", { class: "rng", style: "left:" + p(lo) + "%;width:" + Math.max(0.4, p(hi) - p(lo)) + "%" }));
    if (mid != null) b.appendChild(h("div", { class: "mid" + (lo == null || hi == null ? " only" : ""), style: "left:" + p(mid) + "%" }));
    if (line != null) b.appendChild(h("div", { class: "line", style: "left:" + p(line) + "%" }));
    b.setAttribute("role", "img");
    b.setAttribute("aria-label", (lo != null && hi != null ? usdT(lo) + " – " + usdT(hi) : L("single figure", "cifra única")) + (mid != null ? ", " + M("central") + " " + usdT(mid) : ""));
    w.appendChild(b);
    return w;
  }
  function axis(max, cur) {
    var a = h("div", { class: "axis-row", "aria-hidden": "true" }), step = niceStep(max);
    for (var v = 0; v <= max + 1; v += step) a.appendChild(h("span", { style: "left:" + (v / max * 100) + "%" }, v === 0 ? (cur || "USD") + " 0" : UC.fmt.compact(v)));
    return a;
  }
  function niceStep(max) { var raw = max / 5, p = Math.pow(10, Math.floor(Math.log10(raw))), f = raw / p; return (f < 1.5 ? 1 : f < 3.5 ? 2 : f < 7.5 ? 5 : 10) * p; }
  function niceMax(v) { var s = niceStep(v); return Math.ceil(v / s) * s; }
  function sec(title, note) { var e = h("section", { class: "sec" }, h("h2", null, title)); if (note) e.appendChild(h("p", { class: "muted", style: "max-width:110ch;margin:0" }, note)); for (var i = 2; i < arguments.length; i++) if (arguments[i]) e.appendChild(arguments[i]); return e; }
  function noAdd(text) {
    return h("div", { class: "noadd", role: "note" }, h("span", { html: "<svg width='34' height='20' viewBox='0 0 34 20' aria-hidden='true'><circle cx='11' cy='10' r='8' fill='none' stroke='currentColor' stroke-width='1.6'/><circle cx='23' cy='10' r='8' fill='none' stroke='currentColor' stroke-width='1.6'/><path d='M17 4.7a8 8 0 0 1 0 10.6a8 8 0 0 1 0-10.6z' fill='currentColor' opacity='.45'/></svg>", style: "display:inline-flex" }), h("span", null, text));
  }
  function list(items, cls) { var ul = h("ul", { class: cls || "" }); (items || []).forEach(function (t) { ul.appendChild(h("li", null, t)); }); return ul; }
  /** Row button + collapsible detail, used by meanings, waterfall and stakeholders. */
  function expander(btn, makeDetail, open) {
    var det = null, wrap = h("div");
    btn.setAttribute("aria-expanded", String(!!open));
    function set(on) { btn.setAttribute("aria-expanded", String(on)); if (on && !det) { det = makeDetail(); wrap.appendChild(det); } if (det) det.hidden = !on; }
    btn.addEventListener("click", function () { set(btn.getAttribute("aria-expanded") !== "true"); });
    wrap.appendChild(btn); if (open) set(true);
    return wrap;
  }

  /* ================= 1. how much is missing ================= */
  function size(root, d, s) {
    var hl = d.headline, cur = hl.currency || "USD", fx = d.fx || {};
    var hmax = niceMax(Math.max(num(hl.high) || 0, num(hl.central) || 0) * 1.05);
    var left = h("div", { class: "stack" },
      h("div", { class: "row" }, h("span", { class: "tag k-opinion" }, L("AI analysts' estimate, reviewed by an AI reviewer. Not a finding.", "Estimación de analistas de IA, revisada por un revisor de IA. No es un hecho probado.")), kmark(hl.kind), conf(hl.confidence)),
      h("div", { class: "eyebrow" }, L("How much is missing? Central estimate", "¿Cuánto falta? Estimación central") + (hl.as_of ? " · " + L("as of ", "al ") + asOf(hl.as_of) : "")),
      h("div", { class: "mm-big" }, UC.fmt.money(hl.central, cur, { compact: true })),
      h("div", { class: "small" }, L("Plausible range: ", "Rango verosímil: "), h("b", null, usdT(hl.low, cur) + " – " + usdT(hl.high, cur))),
      h("div", { class: "v-analyst" }, rangeBar(hl.low, hl.central, hl.high, hmax, "k-estimate"), axis(hmax, cur)),
      h("p", { class: "lead", style: "margin:6px 0 0" }, UC.px(hl, "plain")),
      refs(hl.refs, null, 6), opinion("/headline"));
    var sens = [];
    (fx.sensitivity || []).forEach(function (x) { sens.push({ rate: x.rate, v: x.headline_central, cur: x.currency }); });
    sens.push({ rate: fx.rate || hl.fx_rate, v: hl.central, cur: cur, base: true });
    sens.sort(function (a, b) { return a.rate - b.rate; });
    var stats = h("div", { class: "mm-stats" });
    sens.forEach(function (x) { stats.appendChild(h("div", { class: "mm-stat" }, h("b", null, usdT(x.v, x.cur)), h("span", null, L("at Gs. ", "a Gs. ") + UC.fmt.num(x.rate) + L(" per USD", " por USD") + (x.base ? L(" (rate used)", " (tipo usado)") : "")))); });
    var wo = hl.without_unofficial_list;
    if (wo) stats.appendChild(h("div", { class: "mm-stat", title: UC.px(wo, "note") }, h("b", null, usdT(wo.headline_central, wo.currency)), h("span", null, L("without the unofficial debtor list (questioned book ", "sin la lista oficiosa de deudores (cartera cuestionada ") + usdT(wo.questioned_book, wo.currency) + ")")));
    var right = h("div", { class: "stack" },
      h("div", null, h("h4", null, L("What this number measures", "Qué mide esta cifra")), h("p", { style: "margin:4px 0 0;max-width:none" }, UC.px(hl, "measure"))),
      h("div", null, h("h4", null, L("What it is not", "Qué no es")), list([
        L("Not a finding by a court, the prosecution or the supervisor. It is arithmetic by AI analysts on published numbers and stated assumptions.", "No es una conclusión de un tribunal, de la Fiscalía ni del supervisor. Es aritmética de analistas de IA sobre cifras publicadas y supuestos declarados."),
        L("Not an amount said to have been stolen or diverted by anyone. A shortfall of assets says nothing by itself about who is responsible.", "No es un monto que se diga robado o desviado por alguien. Un faltante de activos no dice por sí solo quién es responsable."),
        L("Not the sum of the seven figures below. They answer different questions and overlap.", "No es la suma de las siete cifras de abajo. Responden a preguntas distintas y se superponen."),
        L("Not the loss of any one group. Who bears it depends on the order of payment (see What can be recovered).", "No es la pérdida de un grupo en particular. Quién la soporta depende del orden de pago (véase Qué puede recuperarse).")], "small")),
      h("div", null, h("h4", null, L("Sensitivity", "Sensibilidad")), stats, wo && UC.px(wo, "note") ? h("p", { class: "small muted", style: "margin:6px 0 0;max-width:none" }, UC.px(wo, "note")) : null, UC.px(fx, "basis") ? h("details", { class: "small" }, h("summary", { class: "muted" }, L("Why Gs. ", "Por qué Gs. ") + UC.fmt.num(fx.rate) + L(" per USD", " por USD")), h("p", { style: "margin:4px 0;max-width:none" }, UC.px(fx, "basis")), refs(fx.refs)) : null));
    root.appendChild(h("div", { class: "card mm-hero" }, left, right));
    if ((UC.px(hl, "drivers") || []).length) root.appendChild(h("details", { class: "card" }, h("summary", null, h("b", null, L("What moves the number most", "Qué mueve más la cifra") + " (" + UC.px(hl, "drivers").length + ")")), list(UC.px(hl, "drivers"), "small biglist")));

    /* seven meanings */
    var ms = d.meanings || [];
    if (ms.length) {
      var mmax = niceMax(Math.max.apply(null, ms.map(function (m) { return Math.max(num(m.high) || 0, num(m.central) || 0); })) * 1.03);
      var rows = h("div", { class: "mrows card", style: "padding:0" }), byId = {};
      rows.appendChild(h("div", { class: "mrow", style: "cursor:default;border-top:0", "aria-hidden": "true" }, h("span", { class: "small muted" }, L("Meaning, who says it, kind of figure", "Significado, quién lo afirma, tipo de cifra")), h("div", { class: "rbw" }, axis(mmax, "USD")), h("span", { class: "v small muted" }, L("central (low – high)", "central (bajo – alto)"))));
      ms.forEach(function (m, mi) {
        var btn = h("button", { type: "button", class: "mrow " + vcls(m.asserted_by) },
          h("span", null, h("span", { class: "t" }, UC.px(m, "title")), h("span", { class: "m" }, who(m.asserted_by), kmark(m.kind), m.as_of ? h("span", { class: "tiny muted" }, asOf(m.as_of)) : null)),
          rangeBar(m.low, m.central, m.high, mmax, "k-" + m.kind),
          h("span", { class: "v" }, h("b", null, usdT(m.central, m.currency)), num(m.low) != null || num(m.high) != null ? "(" + usdT(m.low, m.currency) + " – " + usdT(m.high, m.currency) + ")" : h("span", { class: "muted" }, L("single figure, no range given", "cifra única, sin rango"))));
        byId[m.id] = btn;
        function hi(on) {
          rows.classList.toggle("hovering", on);
          Object.keys(byId).forEach(function (k) { byId[k].classList.remove("me", "ov"); });
          if (on) { btn.classList.add("me"); (m.overlaps || []).forEach(function (o) { if (byId[o]) byId[o].classList.add("ov"); }); }
        }
        btn.addEventListener("mouseenter", function () { hi(true); }); btn.addEventListener("mouseleave", function () { hi(false); });
        btn.addEventListener("focus", function () { hi(true); }); btn.addEventListener("blur", function () { hi(false); });
        rows.appendChild(expander(btn, function () {
          var det = h("div", { class: "mdetail" }, h("p", { style: "margin:0;max-width:110ch" }, UC.px(m, "explain")), h("div", { class: "row" }, conf(m.confidence)));
          var ov = (m.overlaps || []).map(function (o) { var x = ms.filter(function (y) { return y.id === o; })[0]; return x ? UC.px(x, "title") : o; });
          det.appendChild(h("div", { class: "small" }, h("b", null, ov.length ? L("Overlaps with (do not add): ", "Se superpone con (no sumar): ") : L("Does not overlap the other six, but is far too small to add meaningfully.", "No se superpone con las otras seis, pero es demasiado pequeña para sumarse con sentido.")), ov.join(" · ")));
          var op = opinion("/meanings/" + mi); if (op) det.appendChild(op);
          if ((m.inputs || []).length) det.appendChild(inputsTable(m.inputs));
          return det;
        }, s.meaning === m.id));
      });
      root.appendChild(sec(ms.length + L(" things “missing” can mean", " cosas que «faltante» puede significar"), L("Each row is a different question, answered by a different voice. All on one USD axis so they can be compared. Hover or focus a row to see which others it overlaps; select it for the explanation and inputs.", "Cada fila es una pregunta distinta, respondida por una voz distinta. Todas en un mismo eje en USD para poder compararlas. Pase el cursor o enfoque una fila para ver con cuáles se superpone; selecciónela para ver la explicación y los insumos."),
        noAdd(UC.px(d, "meanings_note") || L("These figures overlap and must not be added together.", "Estas cifras se superponen y no deben sumarse.")), rows,
        h("div", { class: "legend" }, kmark("reported"), kmark("computed"), kmark("estimate"), h("span", { html: "<svg width='22' height='14' aria-hidden='true'><rect x='9.5' y='0' width='3' height='14' rx='1' fill='currentColor'/></svg>" + UC.esc(L("central value", "valor central")) }), h("span", { html: "<svg width='14' height='14' aria-hidden='true'><circle cx='7' cy='7' r='5' fill='currentColor'/></svg>" + UC.esc(L("single figure (no range given)", "cifra única (sin rango)")) }), h("span", { html: "<svg width='14' height='14' aria-hidden='true'><rect x='0' y='0' width='4' height='14' fill='var(--warn)'/></svg>" + UC.esc(L("overlaps the row in focus", "se superpone con la fila en foco")) }))));
    }
    if (d.waterfall && (d.waterfall.steps || []).length) root.appendChild(waterfall(d.waterfall, s));
    if ((d.stakeholders || []).length) root.appendChild(stakeholders(d));
    var two = h("div", { class: "grid g2" });
    if ((d.does_not_reconcile || []).length) {
      var ul = h("ul", { class: "biglist" });
      d.does_not_reconcile.forEach(function (x) { ul.appendChild(h("li", null, UC.px(x, "text"), refs(x.refs, x.url, 4))); });
      two.appendChild(h("div", { class: "card stack", style: "border-top:4px solid var(--bad)" }, h("h2", null, L("Does not reconcile", "No concilia") + " (" + d.does_not_reconcile.length + ")"), h("p", { class: "small muted", style: "margin:0" }, L("Published figures that contradict each other or the model. Left open, not smoothed over.", "Cifras publicadas que se contradicen entre sí o con el modelo. Quedan abiertas; no se disimulan.")), ul));
    }
    if ((UC.px(d, "cannot_determine") || []).length) two.appendChild(h("div", { class: "card stack", style: "border-top:4px solid var(--ink)" }, h("h2", null, L("Cannot be determined from public sources", "No puede determinarse con fuentes públicas") + " (" + UC.px(d, "cannot_determine").length + ")"), h("p", { class: "small muted", style: "margin:0" }, L("What nobody outside the bank, the supervisor and the prosecution can know today.", "Lo que nadie fuera del banco, el supervisor y la Fiscalía puede saber hoy.")), list(UC.px(d, "cannot_determine"), "biglist")));
    if (two.children.length) root.appendChild(two);
  }
  function inputsTable(inputs) {
    return ui.table([
      { label: L("Input", "Insumo"), render: function (i) { return UC.px(i, "label"); } },
      { label: L("Value", "Valor"), cls: "r", render: function (i) { return num(i.value) == null ? h("span", { class: "muted" }, NK()) : UC.fmt.money(i.value, i.currency || ""); } },
      { label: L("Kind", "Tipo"), render: function (i) { return kmark(i.kind); } },
      { label: L("As of", "Al"), render: function (i) { return asOf(i.as_of); } },
      { label: L("Provenance", "Procedencia"), render: function (i) { var b = h("span"); if ((i.refs || []).length) b.appendChild(chips(i.refs, 4)); var a = link(i.url, L("open source", "abrir fuente")); if (a) b.appendChild(a); if (!b.childNodes.length) b.appendChild(h("span", { class: "muted small" }, "—")); return b; } }
    ], inputs, { pageSize: 20, minWidth: 720 });
  }

  function waterfall(w, s) {
    var scs = (w.scenarios || ["central"]).slice(), cur = w.currency || "USD";
    if (scs.indexOf(s.wf) < 0) s.wf = scs.indexOf("central") >= 0 ? "central" : scs[0];
    var host = h("div"), box = sec(UC.px(w, "title") || L("From book assets to the shortfall", "Del activo contable al faltante"), L("Read down: what the balance sheet says the bank owns, less what the analysts think is not really there, less what it owes. Solid bars are reported figures; hatched bars are the analysts' assumptions. Select a step for its note and sources.", "Lea hacia abajo: lo que el balance dice que el banco tiene, menos lo que los analistas creen que en realidad no está, menos lo que debe. Las barras llenas son cifras informadas; las rayadas, supuestos de los analistas. Seleccione un paso para ver su nota y fuentes."));
    box.appendChild(h("div", { class: "row" }, ui.seg(scs.map(function (k) { return { v: k, l: M(k) + (k === "low" ? L(" shortfall", " (faltante menor)") : k === "high" ? L(" shortfall", " (faltante mayor)") : "") }; }), s.wf, function (v) { s.wf = v; draw(); }, L("Scenario", "Escenario")), h("span", { class: "tag k-opinion" }, L("analysts' model", "modelo de los analistas"))));
    box.appendChild(host);
    function draw() {
      host.innerHTML = "";
      Array.prototype.forEach.call(box.querySelectorAll(".seg button"), function (b, i) { b.setAttribute("aria-pressed", String(scs[i] === s.wf)); });
      var steps = w.steps, run = 0, lo = 0, hi = 0, endV = null, foot = true, subBad = [];
      // extent over every scenario so the scale does not jump when switching
      scs.forEach(function (k) { var r = 0; steps.forEach(function (st) { var v = num(st.values && st.values[k]); if (v == null) return; if (st.type === "start" || st.type === "deduction" || st.type === "delta" || st.type === "addition") { r += v; } hi = Math.max(hi, r, st.type === "subtotal" || st.type === "end" ? v : 0); lo = Math.min(lo, r, st.type === "end" ? v : 0); }); });
      var span = hi - lo || 1, P = function (v) { return (v - lo) / span * 100; };
      var wf = h("div", { class: "wf card", style: "padding:0" });
      steps.forEach(function (st) {
        var v = num(st.values && st.values[s.wf]), t = st.type, bar = h("div", { class: "wbar" }), a, b, cls;
        if (t === "subtotal" || t === "end") {
          if (v != null && Math.abs(v - run) > 150000) { if (t === "end") foot = false; else subBad.push(UC.px(st, "label")); }
          if (t === "end") endV = v;
          a = Math.min(0, v == null ? run : v); b = Math.max(0, v == null ? run : v); cls = t === "end" ? "end" + ((v == null ? run : v) >= 0 ? " pos" : "") : "sub";
        } else if (t === "start") { run = v || 0; a = 0; b = run; cls = "start"; }
        else { var before = run; run += v || 0; a = Math.min(before, run); b = Math.max(before, run); cls = "ded k-" + st.kind; }
        if (v != null || t === "subtotal" || t === "end") bar.appendChild(h("div", { class: "b " + cls, style: "left:" + P(a) + "%;width:" + Math.max(0.3, P(b) - P(a)) + "%" }));
        bar.appendChild(h("div", { class: "zero", style: "left:" + P(0) + "%" }));
        var btn = h("button", { type: "button", class: "wrow " + (t === "subtotal" ? "sub" : t === "end" ? "end" : t === "start" ? "start" : "") },
          h("span", null, UC.px(st, "label"), h("span", { class: "m", style: "display:flex;gap:8px;margin-top:2px;font-weight:400" }, kmark(st.kind), t === "subtotal" ? h("span", { class: "tag" }, L("running total, not added", "suma acumulada, no se suma")) : null)),
          bar, h("span", { class: "v" }, v == null ? h("span", { class: "muted" }, NK()) : (v < 0 ? "− " : "") + UC.fmt.money(Math.abs(v), cur, { compact: true })));
        wf.appendChild(expander(btn, function () {
          return h("div", { class: "mdetail" }, UC.px(st, "note") ? h("p", { style: "margin:0;max-width:110ch" }, UC.px(st, "note")) : null,
            h("div", { class: "row small" }, kmark(st.kind), st.as_of ? h("span", { class: "muted" }, L("as of ", "al ") + asOf(st.as_of)) : null, v != null ? h("span", { class: "num muted" }, UC.fmt.money(v, cur)) : null), refs(st.refs, st.url, 6));
        }));
      });
      host.appendChild(wf);
      var okSub = !subBad.length;
      host.appendChild(h("div", { class: "row", style: "margin-top:8px" },
        endV == null ? h("span", { class: "foots bad" }, L("No end value given for this scenario; nothing to check.", "No hay valor final para este escenario; nada que verificar."))
          : foot && okSub ? h("span", { class: "foots" }, "✓ " + L("Foots: start plus deductions equals the result (", "Cuadra: el inicio más las deducciones da el resultado (") + UC.fmt.money(run, cur, { compact: true }) + L("), checked in the page.", "), verificado en la página."))
            : h("span", { class: "foots bad" }, "✕ " + L("Does not foot: the steps give ", "No cuadra: los pasos dan ") + UC.fmt.money(run, cur) + L(" but the file states ", " pero el archivo indica ") + UC.fmt.money(endV, cur) + (subBad.length ? " · " + subBad.join("; ") : "")),
        h("span", { class: "small muted" }, UC.px(w, "sign_note"))));
    }
    draw();
    return box;
  }

  function stakeholders(d) {
    var st = d.stakeholders, max = niceMax(Math.max.apply(null, st.map(function (x) { return Math.max(num(x.exposure_high) || 0, num(x.expected_loss_high) || 0); })) * 1.03);
    var rows = h("div", { class: "card", style: "padding:0" });
    rows.appendChild(h("div", { class: "mrow", style: "cursor:default;border-top:0", "aria-hidden": "true" }, h("span", { class: "small muted" }, L("Who", "Quién")), h("div", { class: "rbw" }, axis(max, "USD")), h("span", { class: "v small muted" }, L("exposure / expected loss", "exposición / pérdida esperada"))));
    st.forEach(function (x) {
      var rng = function (a, b) { return num(a) == null && num(b) == null ? NK() : a === b ? usdT(a, x.currency) : usdT(a, x.currency) + " – " + usdT(b, x.currency); };
      var one = function (a, b) { return num(a) != null && a === b; };
      var bars = h("div", { class: "rbw stack", style: "gap:3px" },
        one(x.exposure_low, x.exposure_high) ? rangeBar(null, x.exposure_low, null, max, "k-" + x.exposure_kind) : rangeBar(x.exposure_low, null, x.exposure_high, max, "k-" + x.exposure_kind),
        one(x.expected_loss_low, x.expected_loss_high) ? rangeBar(0, null, x.expected_loss_low, max, "loss") : rangeBar(x.expected_loss_low, null, x.expected_loss_high, max, "loss"));
      var btn = h("button", { type: "button", class: "mrow" }, h("span", null, h("span", { class: "t" }, UC.px(x, "who"))), bars,
        h("span", { class: "v" }, h("span", { style: "display:block" }, rng(x.exposure_low, x.exposure_high)), h("b", { style: "color:var(--out)" }, rng(x.expected_loss_low, x.expected_loss_high))));
      rows.appendChild(expander(btn, function () {
        return h("div", { class: "mdetail" }, h("div", { class: "row small" }, h("span", null, L("Exposure: ", "Exposición: ")), kmark(x.exposure_kind), h("span", null, L("Expected loss: ", "Pérdida esperada: ")), kmark(x.loss_kind), x.as_of ? h("span", { class: "muted" }, asOf(x.as_of)) : null),
          h("p", { style: "margin:0;max-width:110ch" }, h("b", null, L("Recovery assumption. ", "Supuesto de recuperación. ")), UC.px(x, "assumption")), refs(x.refs, x.url, 6));
      }));
    });
    return sec(L("Who is exposed, and what each might lose", "Quién está expuesto y cuánto podría perder cada uno"), L("Upper bar: what each party has at stake. Lower bar: the range of loss the analysts expect. Select a row for the assumption behind it.", "Barra superior: lo que cada parte tiene en juego. Barra inferior: el rango de pérdida que esperan los analistas. Seleccione una fila para ver el supuesto."),
      noAdd(UC.px(d, "stakeholders_note") || L("Rows overlap and must not be added.", "Las filas se superponen y no deben sumarse.")), rows,
      h("div", { class: "legend" }, h("span", { html: "<svg width='24' height='10' aria-hidden='true'><rect width='24' height='10' rx='3' fill='var(--own)' opacity='.8'/></svg>" + UC.esc(L("exposure", "exposición")) }), h("span", { html: "<svg width='24' height='10' aria-hidden='true'><rect width='24' height='10' rx='3' fill='var(--out)' opacity='.8'/></svg>" + UC.esc(L("expected loss (estimate)", "pérdida esperada (estimación)")) }), kmark("reported"), kmark("computed")));
  }

  /* ================= 2. where did it go ================= */
  function uses(root, d, s) {
    (d.uses && d.uses.hypotheses || []).forEach(function (x, i) { x._path = "/uses/hypotheses/" + i; });
    var u = d.uses || {}, t = u.total || {}, hy = (u.hypotheses || []).slice().sort(function (a, b) { return (a.rank || 99) - (b.rank || 99); }), un = u.unexplained, cur = t.currency || "USD";
    if (!u.total && !hy.length) { root.appendChild(h("div", { class: "empty" }, L("The file has no section on uses.", "El archivo no tiene sección de usos."))); return; }
    s.umode = s.umode || "central";
    var tmax = niceMax((num(t.high) || num(t.value) || 1) * 1.03);
    root.appendChild(sec(L("Where did it go? The questioned book", "¿A dónde fue? La cartera cuestionada"), null,
      h("div", { class: "card stack v-analyst" }, h("div", { class: "row" }, h("span", { class: "mm-big", style: "font-size:clamp(26px,3vw,40px)" }, usdT(t.value, cur)), kmark(t.kind), t.as_of ? h("span", { class: "small muted" }, L("as of ", "al ") + asOf(t.as_of)) : null, h("span", { class: "small" }, L("range ", "rango ") + usdT(t.low, cur) + " – " + usdT(t.high, cur))),
        rangeBar(t.low, t.value, t.high, tmax, "k-" + t.kind), axis(tmax, cur), h("p", { style: "margin:0;max-width:110ch" }, UC.px(t, "scope")),
        h("div", { class: "grid g2" }, h("div", null, h("h4", null, L("Counted", "Se cuenta") + " (" + (UC.px(t, "in_scope") || []).length + ")"), list(UC.px(t, "in_scope"), "small")), h("div", null, h("h4", null, L("Left out", "Queda fuera") + " (" + (UC.px(t, "out_of_scope") || []).length + ")"), list(UC.px(t, "out_of_scope"), "small"))),
        refs(t.refs, null, 6))));

    var total = num(t.value), sumC = 0, sumH = 0, cards = {};
    hy.forEach(function (x) { sumC += num(x.central) || 0; sumH += num(x.high) || 0; });
    var foots = total != null && un && num(un.central) != null && Math.abs(sumC + un.central - total) < 150000;
    var fig = h("div", { class: "card stack" });
    fig.appendChild(h("div", { class: "row between" }, h("h3", null, L("Hypotheses, ranked by central estimate", "Hipótesis, ordenadas por estimación central")), ui.seg([{ v: "central", l: L("Central", "Central") }, { v: "range", l: L("Low / high", "Bajo / alto") }], s.umode, function (v) { s.umode = v; UC.rerender(); }, L("Show", "Mostrar"))));
    function openCard(id) { var c = cards[id]; if (c) { c.open = true; c.scrollIntoView({ block: "center" }); c.querySelector("summary").focus(); } }
    if (s.umode === "central" && total) {
      var bar = h("div", { class: "stack-bar", role: "group", "aria-label": L("Central estimates as shares of the questioned book", "Estimaciones centrales como partes de la cartera cuestionada") });
      hy.forEach(function (x) {
        if (!num(x.central)) return;
        var b = h("button", { type: "button", style: "flex:" + x.central + " 0 0", "data-tip": "<b>" + UC.esc(x.rank + ". " + UC.px(x, "title")) + "</b><span class='t2'>" + UC.esc(usdT(x.central, cur) + (x.share_central_pct != null ? " · " + pct(x.share_central_pct) : "")) + "</span>", "aria-label": x.rank + ". " + UC.px(x, "title") + ": " + usdT(x.central, cur), onclick: function () { openCard(x.id); } }, x.central / total > 0.035 ? String(x.rank) : "");
        bar.appendChild(b);
      });
      if (un && num(un.central)) bar.appendChild(h("button", { type: "button", class: "unx", style: "flex:" + un.central + " 0 0", "data-tip": "<b>" + UC.esc(L("Unexplained", "Sin explicar")) + "</b><span class='t2'>" + UC.esc(usdT(un.central, cur) + " · " + pct(un.share_central_pct)) + "</span>", "aria-label": L("Unexplained: ", "Sin explicar: ") + usdT(un.central, cur), onclick: function () { openCard("_unx"); } }, h("span", null, L("Unexplained ", "Sin explicar ") + pct(un.share_central_pct))));
      fig.appendChild(bar);
      fig.appendChild(h("p", { class: "small muted", style: "margin:0;max-width:none" }, L("Numbers are ranks; widths are central estimates as shares of ", "Los números son el orden; los anchos, las estimaciones centrales como parte de ") + usdT(total, cur) + ". " + (foots ? "✓ " + L("The central estimates and the unexplained remainder foot to the questioned book (checked in the page).", "Las estimaciones centrales y el remanente sin explicar cuadran con la cartera cuestionada (verificado en la página).") : L("The central estimates do not foot to the questioned book in this file.", "Las estimaciones centrales no cuadran con la cartera cuestionada en este archivo."))));
    } else {
      fig.appendChild(noAdd(L("The high bounds cannot all hold at once: taken together they come to ", "Los máximos no pueden darse todos a la vez: en conjunto llegan a ") + usdT(sumH, cur) + L(", more than the whole questioned book of ", ", más que toda la cartera cuestionada de ") + usdT(total, cur) + L(" (red dashed line). Each range is what one hypothesis alone could reach.", " (línea roja punteada). Cada rango es lo que una hipótesis podría alcanzar por sí sola.")));
    }
    var rmax = niceMax(Math.max(total || 0, Math.max.apply(null, hy.map(function (x) { return num(x.high) || num(x.central) || 0; }).concat([un ? num(un.high) || 0 : 0]))) * 1.03);
    var rws = h("div");
    rws.appendChild(h("div", { class: "mrow", style: "cursor:default;border-top:0", "aria-hidden": "true" }, h("span"), h("div", { class: "rbw" }, axis(rmax, cur)), h("span", { class: "v small muted" }, s.umode === "central" ? L("central · share", "central · parte") : L("low – high", "bajo – alto"))));
    function row(x, id, isUn) {
      var b = h("button", { type: "button", class: "mrow", onclick: function () { openCard(id); } },
        h("span", null, h("span", { class: "t" }, (isUn ? "" : x.rank + ". ") + (isUn ? L("Unexplained (no evidenced destination)", "Sin explicar (sin destino acreditado)") : UC.px(x, "title"))), h("span", { class: "m" }, isUn ? null : h("span", { class: "tag strong" }, M(x.fate)), kmark(x.kind))),
        s.umode === "central" ? rangeBar(0, null, x.central, rmax, isUn ? "hatch" : "", total) : rangeBar(x.low, x.central, x.high, rmax, isUn ? "hatch" : "k-estimate", total),
        h("span", { class: "v" }, s.umode === "central" ? h("b", null, usdT(x.central, cur)) : h("b", null, usdT(x.low, cur) + " – " + usdT(x.high, cur)), s.umode === "central" ? pct(x.share_central_pct) : L("central ", "central ") + usdT(x.central, cur)));
      return b;
    }
    hy.forEach(function (x) { rws.appendChild(row(x, x.id, false)); });
    if (un) rws.appendChild(row(un, "_unx", true));
    fig.appendChild(rws);
    fig.appendChild(h("div", { class: "legend" }, h("span", { html: "<svg width='2' height='14' aria-hidden='true'><line x1='1' y1='0' x2='1' y2='14' stroke='var(--bad)' stroke-width='2' stroke-dasharray='3 2'/></svg>" + UC.esc(L("size of the whole questioned book", "tamaño de toda la cartera cuestionada")) }), h("span", { html: "<svg width='24' height='10' aria-hidden='true'><rect x='1' y='1' width='22' height='8' fill='none' stroke='var(--muted)' stroke-width='1.5'/><path d='M4 9L10 1M10 9L16 1M16 9L22 1' stroke='var(--muted)'/></svg>" + UC.esc(L("unexplained", "sin explicar")) })));
    root.appendChild(fig);

    var cl = h("div", { class: "stack" });
    hy.forEach(function (x, i) {
      var det = h("details", { class: "hyp", id: "hyp-" + x.id }, h("summary", null, h("span", { class: "rank" }, String(x.rank)), h("span", null, h("b", null, UC.px(x, "title")), h("span", { class: "m", style: "display:flex;gap:6px;flex-wrap:wrap;margin-top:3px" }, h("span", { class: "tag strong" }, M(x.fate)), conf(x.confidence))), rangeBar(x.low, x.central, x.high, rmax, "k-estimate", total), h("span", { class: "v num", style: "text-align:right" }, h("b", null, usdT(x.central, cur)), h("span", { class: "small muted", style: "display:block" }, usdT(x.low, cur) + " – " + usdT(x.high, cur)))));
      if (i === 0 && !s.hypOpened) det.open = true;
      var body = h("div", { class: "hyp-body" }, h("p", { style: "margin:0;max-width:110ch" }, UC.px(x, "summary")));
      function evcol(title, items, cls) {
        var c = h("div", { class: "evcol " + cls }, h("h4", null, title + " (" + (items || []).length + ")"));
        var st = h("div", { class: "stack" });
        (items || []).forEach(function (e) { st.appendChild(h("div", { class: "ev" }, e.asserted_by ? h("div", null, who(e.asserted_by)) : null, h("div", null, UC.px(e, "text")), refs(e.refs, e.url, 4))); });
        if (!(items || []).length) st.appendChild(h("div", { class: "empty" }, L("None listed.", "Ninguna indicada.")));
        c.appendChild(st); return c;
      }
      body.appendChild(h("div", { class: "grid g2" }, evcol(L("Evidence for", "Indicios a favor"), x.evidence_for, "for"), evcol(L("Evidence against", "Indicios en contra"), x.evidence_against, "against")));
      if (UC.px(x, "would_confirm")) body.appendChild(h("div", { class: "note", style: "background:var(--soft);border-radius:8px;padding:8px 10px" }, h("b", null, L("What would confirm it. ", "Qué lo confirmaría. ")), UC.px(x, "would_confirm")));
      var op = opinion(x._path); if (op) body.appendChild(op);
      if (UC.px(x, "reviewer_note")) body.appendChild(h("div", { class: "opinion small" }, h("b", null, L("Reviewer's note. ", "Nota del revisor. ")), UC.px(x, "reviewer_note")));
      det.appendChild(body); cards[x.id] = det; cl.appendChild(det);
    });
    if (un) {
      var du = h("details", { class: "hyp unx", id: "hyp-unx" }, h("summary", null, h("span", { class: "rank" }, "?"), h("span", null, h("b", null, L("Unexplained", "Sin explicar")), h("span", { class: "m", style: "display:flex;gap:6px;margin-top:3px" }, kmark(un.kind))), rangeBar(un.low, un.central, un.high, rmax, "hatch", total), h("span", { class: "v num", style: "text-align:right" }, h("b", null, usdT(un.central, cur)), h("span", { class: "small muted", style: "display:block" }, usdT(un.low, cur) + " – " + usdT(un.high, cur)))));
      du.appendChild(h("div", { class: "hyp-body" }, h("p", { style: "margin:0;max-width:110ch" }, UC.px(un, "note")), refs(un.refs, un.url)));
      cards._unx = du; cl.appendChild(du);
    }
    root.appendChild(sec(L("Each hypothesis, with the evidence both ways", "Cada hipótesis, con los indicios en ambos sentidos"), L("These are hypotheses by AI analysts about the use of borrowed money. None is a finding about any person; evidence items carry the voice that asserts them.", "Son hipótesis de analistas de IA sobre el uso del dinero prestado. Ninguna es una conclusión sobre persona alguna; cada indicio lleva la voz que lo afirma."), cl));

    var c = u.circulation;
    if (c && num(c.disbursed_with_amount)) {
      var share = num(c.share_pct) != null ? c.share_pct : (num(c.returned_to_bank) != null ? c.returned_to_bank / c.disbursed_with_amount * 100 : null);
      root.appendChild(sec(L("Circulation: money that came back to the bank", "Circulación: dinero que volvió al banco"), null,
        h("div", { class: "card stack" }, h("div", { class: "twobar", role: "img", "aria-label": L("Returned to the bank: ", "Volvió al banco: ") + pct(share) }, share != null ? h("div", { class: "ret", style: "width:" + Math.max(8, share) + "%" }, pct(share)) : null, h("div", { class: "rest" }, L("disbursed with an amount in the sources: ", "desembolsado con monto en las fuentes: ") + usdT(c.disbursed_with_amount, c.currency))),
          h("div", { class: "row small" }, h("span", null, h("b", null, usdT(c.returned_to_bank, c.currency)), L(" returned to the bank", " volvió al banco")), h("span", { class: "muted" }, L("of ", "de ") + usdT(c.disbursed_with_amount, c.currency) + L(" disbursed", " desembolsados")), kmark(c.kind)),
          h("p", { style: "margin:0;max-width:110ch" }, UC.px(c, "note")), refs(c.refs, c.url, 6), h("div", null, h("a", { class: "btn sm", href: "#flows-chains" }, L("See the reconstructed chains in Money flows", "Ver las cadenas reconstruidas en Flujos de dinero"))))));
    }
  }

  /* ================= 3. what can be recovered ================= */
  function recovery(root, d) {
    var r = d.recovery;
    if (!r) { root.appendChild(h("div", { class: "empty" }, L("The file has no recovery section.", "El archivo no tiene sección de recuperación."))); return; }
    var hl = d.headline, sc = h("div", { class: "grid g3" });
    (r.scenarios || []).forEach(function (x, xi) {
      var pair = x.pairs_with_headline, hv = pair && hl ? hl[pair] : null;
      sc.appendChild(h("div", { class: "card stack" }, h("div", { class: "row between" }, h("h3", null, L("Recovery: ", "Recuperación: ") + M(x.name)), kmark(x.kind)),
        h("div", { class: "mm-big", style: "font-size:28px" }, usdT(x.assets_realised, x.currency)), h("div", { class: "small muted" }, L("assets realised", "activo realizado")),
        pair ? h("div", { class: "note", style: "background:var(--warn-soft);border:1px solid var(--warn);border-radius:8px;padding:6px 10px;font-size:13.5px" }, h("b", null, L("Pairs with the “", "Corresponde al faltante «") + M(pair) + L("” shortfall", "»")), hv != null ? L(" in the headline: ", " de la cifra principal: ") + usdT(hv, hl.currency) : "") : null,
        h("p", { class: "small", style: "margin:0;max-width:none" }, UC.px(x, "assumptions")), opinion("/recovery/scenarios/" + xi)));
    });
    root.appendChild(sec(L("What can be recovered?", "¿Qué puede recuperarse?"), UC.px(r, "note"), sc));
    var ac = r.asset_classes || [];
    if (ac.length) root.appendChild(sec(L("Asset by asset", "Activo por activo"), L("Book value and the share the analysts think can be turned into money. The bar runs from the low to the high recovery rate; the tick is the central rate.", "Valor contable y la parte que los analistas creen convertible en dinero. La barra va de la tasa de recuperación baja a la alta; la marca es la central."),
      ui.table([
        { label: L("Asset class", "Clase de activo"), render: function (a) { return h("span", null, h("b", null, UC.px(a, "title")), h("div", { class: "small muted" }, UC.px(a, "reason")), refs(a.refs, a.url, 3)); } },
        { label: L("Book value", "Valor contable"), cls: "r", render: function (a) { return h("span", null, usd(a.book_value, a.currency), h("div", { class: "tiny muted" }, asOf(a.as_of))); }, sort: function (a) { return num(a.book_value); } },
        { label: L("Kind", "Tipo"), render: function (a) { return kmark(a.kind); } },
        { label: L("Recovery, low – central – high", "Recuperación, baja – central – alta"), render: function (a) { return h("div", { style: "min-width:170px" }, rangeBar(a.recovery_low_pct, a.recovery_central_pct, a.recovery_high_pct, 100, "k-estimate"), h("div", { class: "small num" }, pct(a.recovery_low_pct) + " – " + pct(a.recovery_central_pct) + " – " + pct(a.recovery_high_pct))); }, sort: function (a) { return num(a.recovery_central_pct); } }
      ], ac, { pageSize: 30, minWidth: 860 })));
    var f = r.fund_rank_fork;
    if (f) {
      var keys = f.by_scenario ? Object.keys(f.by_scenario) : [], col = function (which, title, sub) {
        var tb = h("tbody");
        function tr(label, o) { tb.appendChild(h("tr", null, h("th", { scope: "row", style: "position:static" }, label), h("td", { class: "r" }, o ? usd(o.fund_cost, f.currency) : NK()), h("td", { class: "r" }, o ? pct(o.uninsured_recovery_pct) : NK()), h("td", { class: "r" }, o ? pct(o.bondholder_recovery_pct) : NK()))); }
        if (keys.length) keys.forEach(function (k) { tr(M(k), f.by_scenario[k] && f.by_scenario[k][which]); }); else tr(M("central"), f[which]);
        return h("div", { class: "card stack" }, h("h3", null, title), h("p", { class: "small muted", style: "margin:0" }, sub),
          h("div", { class: "tbl" }, h("table", { style: "min-width:420px" }, h("thead", null, h("tr", null, h("th", null, L("Headline scenario", "Escenario de la cifra principal")), h("th", { class: "r" }, L("Cost to the fund", "Costo para el fondo")), h("th", { class: "r" }, L("Uninsured depositors recover", "Recuperan los depositantes no garantizados")), h("th", { class: "r" }, L("Bondholders recover", "Recuperan los bonistas")))), tb)));
      };
      root.appendChild(sec(L("The fork: where the guarantee fund stands in the queue", "La bifurcación: qué lugar ocupa el fondo de garantía en la fila"), UC.px(f, "explain"),
        h("div", { class: "row" }, kmark(f.kind), f.as_of ? h("span", { class: "small muted" }, L("as of ", "al ") + asOf(f.as_of)) : null),
        h("div", { class: "fork" }, col("if_fund_absorbs", L("If the fund absorbs the gap", "Si el fondo absorbe la diferencia"), L("The fund tops up and does not rank ahead of other depositors.", "El fondo completa y no cobra antes que los demás depositantes.")), col("if_fund_first", L("If the fund is repaid first", "Si el fondo cobra primero"), L("The fund recovers its payout ahead of uninsured depositors.", "El fondo recupera su desembolso antes que los depositantes no garantizados."))),
        refs(f.refs, f.url, 6)));
    }
  }

  /* ================= 4. how to find it ================= */
  function tracing(root, d) {
    var tp = (d.tracing_plan || []).slice().sort(function (a, b) { return (a.priority || 99) - (b.priority || 99); });
    if (tp.length) root.appendChild(sec(L("How to find it: the records that would settle it", "Cómo encontrarlo: los registros que lo resolverían"), L("In order of priority. None of these is public today.", "En orden de prioridad. Ninguno es público hoy."),
      ui.table([
        { label: "#", render: function (x) { return h("span", { class: "prio" }, String(x.priority == null ? "" : x.priority)); }, sort: function (x) { return x.priority; } },
        { label: L("Record", "Registro"), render: function (x) { return h("b", null, UC.px(x, "record")); } },
        { label: L("Who holds it", "Quién lo tiene"), render: function (x) { return UC.px(x, "held_by"); } },
        { label: L("What it would show", "Qué mostraría"), render: function (x) { return h("span", null, UC.px(x, "would_show"), refs(x.refs, x.url, 3)); } }
      ], tp, { pageSize: 30, minWidth: 900 })));
    var wl = (d.watch_list || []).filter(function (x) { return x.date; });
    if (wl.length) {
      var t0 = function (x) { var s = String(x); return Date.UTC(+s.slice(0, 4), (+s.slice(5, 7) || 1) - 1, +s.slice(8, 10) || 1); };
      var t1 = function (x) { var s = String(x); return s.length >= 10 ? t0(s) : s.length === 7 ? Date.UTC(+s.slice(0, 4), +s.slice(5, 7), 0) : Date.UTC(+s.slice(0, 4), 11, 31); };
      var a = Math.min.apply(null, wl.map(function (x) { return t0(x.date); })) - 6 * 864e5, b = Math.max.apply(null, wl.map(function (x) { return t1(x.date); })) + 10 * 864e5;
      var W = 1100, H = 96, x = d3.scaleUtc().domain([a, b]).range([24, W - 24]);
      var svg = s$("svg", { viewBox: "0 0 " + W + " " + H, width: W, height: H, role: "img", "aria-label": L("Dates to watch", "Fechas a seguir"), style: "min-width:" + W + "px" });
      svg.appendChild(s$("line", { x1: 24, x2: W - 24, y1: 60, y2: 60, stroke: "var(--rule-strong)" }));
      x.ticks(d3.utcMonth.every(1)).forEach(function (t) { svg.appendChild(s$("line", { class: "gridl", x1: x(t), x2: x(t), y1: 52, y2: 68 })); svg.appendChild(s$("text", { x: x(t) + 3, y: 84, "font-size": 11, class: "sub", text: UC.fmt.dateStr(new Date(+t).toISOString().slice(0, 10), "month") })); });
      var cut = d.as_of ? x(t0(d.as_of)) : null;
      if (cut != null) { svg.appendChild(s$("line", { x1: cut, x2: cut, y1: 8, y2: 68, stroke: "var(--ink)", "stroke-dasharray": "2 3" })); svg.appendChild(s$("text", { x: cut + 4, y: 14, "font-size": 10.5, class: "sub", text: L("data as of ", "datos al ") + asOf(d.as_of) })); }
      var rowsUsed = [];
      wl.forEach(function (w, i) {
        var xa = x(t0(w.date)), xb = x(t1(w.date)), range = String(w.date).length < 10, row = 0;
        while (rowsUsed[row] != null && rowsUsed[row] > xa - 9) row++;
        rowsUsed[row] = Math.max(xb, xa) + 9;
        var cy = 46 - row * 10, g = s$("g", { tabindex: 0, role: "button", style: "cursor:pointer", "aria-label": asOf(w.date) + ": " + UC.px(w, "text").slice(0, 90), "data-tip": "<b>" + UC.esc(asOf(w.date)) + "</b><span class='t2'>" + UC.esc(UC.px(w, "text").slice(0, 240)) + "</span>" });
        if (range) g.appendChild(s$("rect", { x: xa, y: cy - 2.5, width: Math.max(6, xb - xa), height: 5, rx: 2.5, fill: "var(--warn)", "fill-opacity": 0.45 }));
        g.appendChild(s$("circle", { cx: xa, cy: cy, r: 5, fill: "var(--warn)", stroke: "var(--card)", "stroke-width": 1.5 }));
        var go = function () { var el = document.getElementById("watch-" + i); if (el) { el.scrollIntoView({ block: "center" }); el.focus(); } };
        g.addEventListener("click", go); g.addEventListener("keydown", function (e) { if (e.key === "Enter") go(); });
        svg.appendChild(g);
      });
      var lst = h("div", { class: "card alist" });
      wl.forEach(function (w, i) { lst.appendChild(h("div", { class: "arow", id: "watch-" + i, tabindex: "-1" }, h("span", { class: "d" }, asOf(w.date)), h("div", { class: "x" }, UC.px(w, "text"), refs(w.refs, w.url, 4)), h("span"))); });
      root.appendChild(sec(L("Dates to watch", "Fechas a seguir"), L("Events ahead that would move the estimate. A bar is a date known only to the month.", "Hechos próximos que moverían la estimación. Una barra es una fecha conocida solo por mes."), h("figure", { class: "fig" }, h("div", { class: "hint" }, L("Swipe sideways to see the whole figure.", "Deslice hacia los lados para ver toda la figura.")), h("div", { class: "scroll" }, svg)), lst));
    }
    var rv = d.review;
    if (rv) root.appendChild(sec(L("The review", "La revisión"), L("An AI reviewer re-derived the key numbers and re-opened sources before this view was written.", "Un revisor de IA volvió a derivar las cifras clave y reabrió fuentes antes de redactar esta vista."),
      h("div", { class: "grid g2" }, h("div", { class: "card stack" }, h("h3", null, L("What the review changed", "Qué cambió la revisión") + " (" + (UC.px(rv, "changed") || []).length + ")"), list(UC.px(rv, "changed"), "small biglist")),
        h("div", { class: "card stack", style: "border-top:4px solid var(--warn)" }, h("h3", null, L("Disagreements that remain", "Desacuerdos que persisten") + " (" + (UC.px(rv, "residual_disagreements") || []).length + ")"), list(UC.px(rv, "residual_disagreements"), "small biglist")))));
    var sa = d.sources_added || [];
    if (sa.length) {
      var ul = h("ul", { class: "small" });
      sa.forEach(function (x) { ul.appendChild(h("li", null, (x.outlet || "") + " · " + (x.title || "") + (x.date ? " · " + asOf(x.date) : "") + " ", link(x.url, L("open", "abrir")))); });
      root.appendChild(h("details", { class: "card" }, h("summary", null, h("b", null, L("Sources opened for this analysis that are not in the graph", "Fuentes abiertas para este análisis que no están en el grafo") + " (" + sa.length + ")")), ul));
    }
  }

  UC.views.missing = {
    render: function (root, sub, s) {
      var d = UC.db.extra.missing;
      root.appendChild(h("div", { class: "view-head" }, h("h2", null, L("Missing money", "El dinero faltante")),
        h("p", null, L("Two questions, in order: how much is missing, and where did it go. Then what might be recovered and which records would settle it.", "Dos preguntas, en orden: cuánto falta y a dónde fue. Después, qué podría recuperarse y qué registros lo resolverían."))));
      if (!d) { root.appendChild(h("div", { class: "empty" }, L("The missing-money analysis (data/missing_money.json) is not available in this build, so this view has nothing to show.", "El análisis del dinero faltante (data/missing_money.json) no está disponible en esta versión; esta vista no tiene nada que mostrar."))); return; }
      var tabs = [{ id: "size", label: L("1. How much is missing?", "1. ¿Cuánto falta?") }, { id: "uses", label: L("2. Where did it go?", "2. ¿A dónde fue?") }, { id: "recovery", label: L("3. What can be recovered?", "3. ¿Qué puede recuperarse?") }, { id: "tracing", label: L("4. How to find it", "4. Cómo encontrarlo") }];
      s.tab = sub && tabs.some(function (t) { return t.id === sub; }) ? sub : (sub ? s.tab || "size" : "size");
      if (UC.px(d, "disclaimer")) root.appendChild(h("div", { class: "disclaimer" }, h("p", null, h("b", null, L("About this view. ", "Sobre esta vista. ")), UC.px(d, "disclaimer"))));
      root.appendChild(ui.tabs(tabs, s.tab, function (t) { s.tab = t; UC.go("missing", null, t); }, L("Questions", "Preguntas")));
      var body = h("div", { class: "stack", style: "gap:22px" });
      root.appendChild(body);
      ({ size: size, uses: uses, recovery: recovery, tracing: tracing })[s.tab](body, d, s);
    }
  };
})();
