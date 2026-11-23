/* payouts.js - "Depositor payouts": what savers are covered for, the schedule, the conditions, who is still
   waiting and whether the plan can cover it. Reads data/payouts.json (optional). Every item carries chips to
   the graph rows it rests on; the page adds no figures of its own. */
(function () {
  "use strict";
  var UC = window.UC, h = UC.h, L = UC.L, prov = UC.prov;
  function t(o) { return o == null ? "" : typeof o === "string" ? o : (o[UC.lang] != null ? o[UC.lang] : o.en); }
  function day(d) { if (!d) return L("no date", "sin fecha"); return UC.fmt.dateStr(d, d.length === 4 ? "year" : d.length === 7 ? "month" : "day"); }
  function chips(refs) { return refs && refs.length ? h("div", { class: "small pay-refs" }, h("span", { class: "muted" }, L("Rests on: ", "Se apoya en: ")), prov.chips(refs, 4)) : null; }
  function sec(title, note) {
    var e = h("section", { class: "sec" }, h("h2", null, title));
    if (note) e.appendChild(h("p", { class: "muted", style: "max-width:110ch;margin:0" }, note));
    for (var i = 2; i < arguments.length; i++) if (arguments[i]) e.appendChild(arguments[i]);
    return e;
  }
  var ST = {
    done: ["Paid", "Pagado", "pay-done"], pending: ["Pending", "Pendiente", "pay-pend"], unknown: ["Uncertain", "Incierto", "pay-unk"],
    next: ["Next", "Próximo", "pay-pend"]
  };
  function state(s, alt) { var x = ST[s] || ST.unknown; return h("span", { class: "pay-state " + x[2] }, alt || L(x[0], x[1])); }

  UC.views.payouts = {
    render: function (root) {
      var d = UC.db.extra.payouts;
      root.appendChild(h("div", { class: "view-head" }, h("h2", null, L("Depositor payouts", "Pagos a ahorristas")),
        h("p", null, L("What savers are covered for, when it is paid, on what conditions, who is still waiting and whether the plan can cover it.", "Qué tienen cubierto los ahorristas, cuándo se paga, con qué condiciones, quién sigue esperando y si el plan alcanza."))));
      if (!d) { root.appendChild(h("div", { class: "empty" }, L("The payouts file (data/payouts.json) is not available in this build.", "El archivo de pagos (data/payouts.json) no está disponible en esta versión."))); return; }
      root.appendChild(h("div", { class: "disclaimer" }, h("p", null, h("b", null, L("State of play at ", "Situación al ") + day(d.as_of) + ". "), t(d.disclaimer))));

      /* current state */
      var kp = h("div", { class: "pay-kpis" });
      (d.status || []).forEach(function (k) {
        kp.appendChild(h("div", { class: "card stack pay-kpi" }, h("span", { class: "small muted" }, t(k.k)), h("b", { class: "pay-v num" }, t(k.v)),
          h("span", { class: "small" }, t(k.n)), h("span", { class: "small muted" }, L("as of ", "al ") + day(k.d)), chips(k.refs)));
      });
      root.appendChild(sec(L("Where things stand", "Cómo está la situación"), null, kp));

      /* coverage ladder */
      var bar = h("div", { class: "pay-ladder", role: "img", "aria-label": L("Coverage by size of deposit", "Cobertura según el tamaño del depósito") });
      var cards = h("div", { class: "grid g3 pay-tiers" });
      (d.tiers || []).forEach(function (x) {
        var w = x.wages || [], span = w[1] == null ? 30 : (w[1] - w[0]);
        var lab = w[1] == null ? L("above 75 wages", "más de 75 salarios") : w[0] + "–" + w[1] + " " + L("minimum wages", "salarios mínimos");
        bar.appendChild(h("div", { class: "pay-seg " + (ST[x.state] || ST.unknown)[2], style: "flex:" + span + " 1 0" }, h("b", null, lab), h("span", null, L((ST[x.state] || ST.unknown)[0], (ST[x.state] || ST.unknown)[1]))));
        cards.appendChild(h("div", { class: "card stack" }, h("div", { class: "pay-row" }, h("h3", null, t(x.name)), state(x.state)),
          h("p", { class: "pay-amt" }, t(x.amount)), h("p", { class: "small" }, t(x.rule)), h("p", { class: "small" }, h("b", null, L("Now: ", "Ahora: ")), t(x.state_t)), chips(x.refs)));
      });
      root.appendChild(sec(L("What a depositor is covered for", "Qué tiene cubierto un depositante"),
        L("The guarantee is counted in monthly minimum wages, per person and per institution. ", "La garantía se cuenta en salarios mínimos mensuales, por persona y por entidad. ") + t(d.wage && d.wage.note), bar, cards));

      var out = h("div", { class: "grid g3" });
      (d.outside || []).forEach(function (x) { out.appendChild(h("div", { class: "card stack" }, h("h3", null, t(x.k)), h("p", { class: "small" }, t(x.t)), chips(x.refs))); });
      root.appendChild(sec(L("Money that is not a deposit", "Dinero que no es un depósito"), L("These are outside the deposit guarantee altogether.", "Estos casos quedan totalmente fuera de la garantía de depósitos."), out));

      /* schedule */
      var ol = h("ol", { class: "pay-sched" });
      (d.schedule || []).forEach(function (x) {
        ol.appendChild(h("li", { class: "pay-step " + (ST[x.s] || ST.unknown)[2] }, h("span", { class: "pay-date num" }, day(x.d)),
          h("div", { class: "stack", style: "gap:4px" }, h("div", { class: "pay-row" }, h("span", null, t(x.t)), x.s === "done" ? null : state(x.s, x.s === "unknown" ? L("No date announced", "Sin fecha anunciada") : null)), chips(x.refs))));
      });
      root.appendChild(sec(L("Schedule", "Calendario"), L("Done, next, and what has no date yet.", "Lo hecho, lo próximo y lo que aún no tiene fecha."), ol));

      /* conditions */
      var ul = h("ul", { class: "pay-list" });
      (d.conditions || []).forEach(function (x) { ul.appendChild(h("li", null, h("span", null, t(x.t)), chips(x.refs))); });
      root.appendChild(sec(L("Conditions and causes of delay", "Condiciones y causas de demora"), null, h("div", { class: "card" }, ul)));

      /* who is waiting */
      var tb = h("tbody");
      (d.waiting || []).forEach(function (x) { tb.appendChild(h("tr", null, h("th", { scope: "row" }, t(x.who)), h("td", { class: "num" }, t(x.amt)), h("td", null, h("span", { class: "small" }, t(x.n)), chips(x.refs)))); });
      root.appendChild(sec(L("Who is still waiting", "Quién sigue esperando"), L("Amounts as each source gave them; they overlap and are not added up.", "Montos tal como los dio cada fuente; se superponen y no se suman."),
        h("div", { class: "card", style: "overflow-x:auto" }, h("table", { class: "tbl pay-tbl" }, h("thead", null, h("tr", null, h("th", { scope: "col" }, L("Group", "Grupo")), h("th", { scope: "col" }, L("Amount reported", "Monto informado")), h("th", { scope: "col" }, L("Notes and source", "Notas y fuente")))), tb))));

      /* can the plan cover it */
      var cv = d.coverage || {}, have = h("div", { class: "card stack" }, h("h3", null, L("What there is to pay with", "Con qué se cuenta para pagar"))), owe = h("div", { class: "card stack" }, h("h3", null, L("What is missing or owed", "Qué falta o se debe")));
      (cv.rows || []).forEach(function (x) {
        (x.side === "have" ? have : owe).appendChild(h("div", { class: "pay-cov" }, h("div", { class: "pay-row" }, h("span", null, t(x.k)), h("b", { class: "num" }, t(x.v))), h("span", { class: "small muted" }, L("as of ", "al ") + day(x.d)), chips(x.refs)));
      });
      var unk = h("ul", { class: "small" });
      (d.unknown || []).forEach(function (x) { unk.appendChild(h("li", null, t(x))); });
      var ex = cv.explainer, exBox = null;
      if (ex) {
        var pts = h("ul", { class: "pay-list" });
        (ex.points || []).forEach(function (x) { pts.appendChild(h("li", null, h("span", null, t(x.t)), chips(x.refs))); });
        var mt = h("div", null);
        (ex.math || []).forEach(function (x) { mt.appendChild(h("div", { class: "pay-cov" }, h("div", { class: "pay-row" }, h("span", null, t(x.k)), h("b", { class: "num" }, t(x.v))), chips(x.refs))); });
        exBox = h("div", { class: "card stack pay-explain", id: "enough-assets" }, h("h3", null, t(ex.title)), h("p", { class: "pay-amt" }, t(ex.answer)), pts,
          h("h4", null, t(ex.math_title)), mt, h("p", { class: "small" }, t(ex.math_note)));
      }
      root.appendChild(sec(L("Can the plan cover it?", "¿Alcanza el plan?"), t(cv.intro), exBox, h("div", { class: "grid g2" }, have, owe),
        h("div", { class: "card stack", style: "border-top:4px solid var(--warn)" }, h("h3", null, L("Not known yet", "Aún no se sabe")), unk)));
    }
  };
})();
