/* people.js - directory of people, companies and authorities, with a profile card built only from
   assertions (roles, loans, flows, figures, charges), and the table of people charged. */
(function () {
  "use strict";
  var UC = window.UC, h = UC.h, L = UC.L, prov = UC.prov, ui = UC.ui;
  var OWN = /shareholder|beneficial|controlling|founder/;

  function shape(t) {
    var d = t === "Person" ? "<circle cx='8' cy='8' r='5.5'/>" : t === "Authority" ? "<path d='M8 1.5L14.5 8L8 14.5L1.5 8z'/>" : "<rect x='2.5' y='2.5' width='11' height='11' rx='2.5'/>";
    return "<svg width='16' height='16' viewBox='0 0 16 16' aria-hidden='true' fill='none' stroke='currentColor' stroke-width='1.6'>" + d + "</svg>";
  }
  function norm(x) { return String(x).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function section(title, n, body, note) {
    return h("section", { class: "card stack" }, h("h3", null, title + (n != null ? " (" + n + ")" : "")), note ? h("p", { class: "small muted", style: "margin:0;max-width:none" }, note) : null, body);
  }
  function rolesTable(list, who) {
    return ui.table([
      { label: who === "holder" ? L("Holder", "Titular") : L("In", "En"), render: function (r) { return ui.party(who === "holder" ? r.holder : r.organisation); }, sort: function (r) { return UC.short(who === "holder" ? r.holder : r.organisation); } },
      { label: L("Role", "Cargo o vínculo"), render: function (r) { return UC.enumLabel(r.roleType); }, sort: function (r) { return r.roleType; } },
      { label: "%", cls: "r", render: function (r) { return r.percentage ? UC.fmt.pct(r.percentage) : ""; }, sort: function (r) { return r.percentage ? Number(r.percentage) : null; } },
      { label: L("Dates stated", "Fechas indicadas"), render: function (r) { return UC.roleDates(r) || h("span", { class: "muted" }, L("not stated", "no indicadas")); }, sort: function (r) { return r.sortDate || null; } },
      { label: L("Note", "Nota"), render: function (r) { var t = UC.tx(r.note); return h("span", { class: "small" }, t.length > 160 ? t.slice(0, 157) + "…" : t); } },
      { label: L("Who says so", "Quién lo afirma"), render: function (r) { return prov.src(r); }, sort: function (r) { return r.assertedBy; } }
    ], list, { pageSize: 25, minWidth: 760, sortCol: 3 });
  }
  function chargeCard(c) {
    var off = (c.allegedOffence && (c.allegedOffence.es || c.allegedOffence.en)) || [], add = (c.allegedOffenceAdded && (c.allegedOffenceAdded.es || c.allegedOffenceAdded.en)) || [];
    var box = h("div", { class: "pv " + prov.vclass(c) });
    box.appendChild(h("div", { class: "row between" }, h("b", null, L("Case ", "Causa ") + (c.caseReference || "?")), prov.src(c)));
    if (c.roleReported) box.appendChild(h("div", { class: "small" }, h("span", { class: "muted" }, L("Role as reported: ", "Rol según la fuente: ")), UC.tx(c.roleReported)));
    box.appendChild(h("div", { class: "small" }, h("span", { class: "muted" }, L("Offences alleged (original wording): ", "Hechos punibles atribuidos: ")), h("span", { lang: "es" }, off.join("; ") || "—")));
    if (add.length) box.appendChild(h("div", { class: "small" }, h("span", { class: "muted" }, L("Reported as added later: ", "Informados como agregados después: ")), h("span", { lang: "es" }, add.join("; "))));
    box.appendChild(h("div", { class: "small" }, h("span", { class: "muted" }, L("Procedural measure: ", "Medida procesal: ")), UC.enumLabel(UC.tx(c.proceduralMeasure) || "none_reported") + (c.sortDate ? " (" + UC.fmt.date(c) + ")" : ""),
      c.measureSource ? h("span", null, " ", prov.chip(c.measureSource, L("source of the measure", "fuente de la medida"))) : null));
    if (c.nextHearing) box.appendChild(h("div", { class: "small" }, h("span", { class: "muted" }, L("Next hearing: ", "Próxima audiencia: ")), c.nextHearing));
    box.appendChild(h("div", { class: "small" }, h("span", { class: "muted" }, L("Defence position as reported: ", "Posición de la defensa según la fuente: ")), UC.tx(c.defenceStatement) || "—"));
    box.appendChild(h("div", { class: "note small" }, L("A charge is an allegation. No one here has been convicted.", "Una imputación es una atribución de hechos. Nadie aquí ha sido condenado.")));
    return box;
  }

  function profile(id, s) {
    var db = UC.db, p = db.byId[id], t = p["@type"][0], isP = t === "Person";
    var all = (db.byParty[id] || []).filter(function (n) { return UC.pass(n, s); });
    var of = function (type) { return all.filter(function (n) { return n["@type"][0] === type; }); };
    var box = h("div", { class: "pcard" });
    var head = h("div", { class: "card stack" });
    head.appendChild(h("div", { class: "eyebrow" }, UC.enumLabel(t) + (p["@type"].length > 1 ? " · " + p["@type"].slice(1).join(", ") : "") + (db.borrowers[id] ? " · " + L("borrower of Ueno Bank", "prestataria de Ueno Bank") : "")));
    head.appendChild(h("h2", null, UC.label(id)));
    if (p.altLabel && p.altLabel.length) head.appendChild(h("div", { class: "small muted" }, L("Also written: ", "También: ") + p.altLabel.join("; ")));
    if (p.isStub) head.appendChild(h("div", { class: "note small" }, L("Named by assertions but not yet described by any contributor.", "Nombrado en afirmaciones pero aún sin descripción.")));
    if (p.business) head.appendChild(h("p", { style: "margin:0" }, h("b", null, L("What it does: ", "A qué se dedica: ")), UC.tx(p.business)));
    if (p.description) head.appendChild(h("p", { style: "margin:0" }, UC.tx(p.description)));
    var ds = db.descOf[id] || [];
    if (ds.length) { var sb = h("div", { class: "row small muted" }, L("Description from:", "Descripción según:")); ds.forEach(function (d) { sb.appendChild(prov.src(d)); }); head.appendChild(sb); }
    if (isP) head.appendChild(h("div", { class: "note small", style: "background:var(--soft);padding:6px 8px;border-radius:6px" }, L("Only roles and case status stated by a source are shown. Being named, or listed as an officer or shareholder, is not an accusation.", "Solo se muestran cargos y situación procesal indicados por una fuente. Ser nombrado, o figurar como directivo o accionista, no es una acusación.")));
    head.appendChild(h("div", { class: "row" }, ui.voiceCount(all), h("button", { type: "button", class: "btn sm", onclick: function () { UC.go("network", { focus: id, preset: null, sel: { type: "node", id: id }, kinds: null, pos: {} }); } }, L("Show in network", "Ver en la red")),
      h("button", { type: "button", class: "btn sm", onclick: function () { UC.go("timeline", { party: id, mode: "events", domain: null }, "events"); } }, L("Its events on the timeline", "Sus hechos en la cronología"))));
    box.appendChild(head);

    var charges = of("Charge").filter(function (c) { return c.chargedPerson === id; });
    if (charges.length) { var cb = h("div", { class: "stack" }); charges.forEach(function (c) { cb.appendChild(chargeCard(c)); }); box.appendChild(section(L("Charges reported", "Imputaciones informadas"), charges.length, cb)); }

    var roles = of("RoleHolding"), inOrg = roles.filter(function (r) { return r.organisation === id && r.roleType !== "role_relative_of"; }), held = roles.filter(function (r) { return r.holder === id && r.roleType !== "role_relative_of"; }), kin = roles.filter(function (r) { return r.roleType === "role_relative_of"; });
    if (!isP) {
      var own = inOrg.filter(function (r) { return OWN.test(r.roleType); }), off = inOrg.filter(function (r) { return !OWN.test(r.roleType); });
      if (own.length) box.appendChild(section(L("Ownership and control, as stated over time", "Propiedad y control, según se afirma en el tiempo"), own.length, rolesTable(own, "holder"), L("Different sources and dates can give different owners; rows are not reconciled.", "Fuentes y fechas distintas pueden dar dueños distintos; las filas no se concilian.")));
      if (off.length) box.appendChild(section(L("Officers, staff and group ties", "Directivos, personal y vínculos de grupo"), off.length, rolesTable(off, "holder")));
    }
    if (held.length) box.appendChild(section(isP ? L("Roles and stakes", "Cargos y participaciones") : L("Stakes and roles it holds in others", "Participaciones y funciones en otras"), held.length, rolesTable(held, "org")));
    if (kin.length) box.appendChild(section(L("Kinship as stated by a source", "Parentesco según lo afirma una fuente"), kin.length, ui.alist(kin, { noGroup: true }), L("Recorded only because the source uses it to argue that parties are related.", "Se registra solo porque la fuente lo usa para sostener que las partes son vinculadas.")));

    var loans = all.filter(UC.isLoan), asB = loans.filter(function (l) { return l.nominalBorrower === id; }).sort(UC.byDate), asL = loans.filter(function (l) { return l.lender === id; });
    if (asB.length) box.appendChild(section(L("Loans received (as each source records them)", "Préstamos recibidos (según cada fuente)"), UC.groupAlts(asB).length, h("div", { class: "stack" }, ui.paged(asB, 20, function (part) { return ui.alist(part); }), h("div", null, h("button", { type: "button", class: "btn sm", onclick: function () { UC.go("flows", { borrower: id }, "borrowers"); } }, L("Open the borrower panel", "Abrir el panel de la prestataria")))), L("Repeated reports of one operation are folded together; nothing is added.", "Los informes repetidos de una operación se pliegan; nada se suma.")));
    if (asL.length && id !== "ucr:org/ueno-bank") box.appendChild(section(L("Loans granted", "Préstamos otorgados"), asL.length, ui.paged(asL.sort(UC.byDate), 15, function (part) { return ui.alist(part); })));
    else if (asL.length) box.appendChild(section(L("Loans granted", "Préstamos otorgados"), null, h("div", { class: "row" }, h("span", null, asL.length + L(" loan records name the bank as lender.", " registros de préstamo nombran al banco como acreedor.")), h("a", { class: "btn sm", href: "#flows-borrowers" }, L("See them by borrower", "Verlos por prestataria")))));

    var flows = of("Flow"), fin = flows.filter(function (f) { return f.toParty === id; }), fout = flows.filter(function (f) { return f.fromParty === id; });
    if (flows.length) {
      var fb = h("div", { class: "stack" });
      fb.appendChild(h("div", { class: "row" },
        h("button", { type: "button", class: "btn sm", disabled: !fin.length, data: fin.length ? { prov: fin.slice(0, 80).map(function (f) { return f["@id"]; }).join(" ") } : null }, L("Received: ", "Recibidos: ") + UC.groupAlts(fin).length + L(" items", " ítems")),
        h("button", { type: "button", class: "btn sm", disabled: !fout.length, data: fout.length ? { prov: fout.slice(0, 80).map(function (f) { return f["@id"]; }).join(" ") } : null }, L("Paid out: ", "Pagados: ") + UC.groupAlts(fout).length + L(" items", " ítems"))));
      fb.appendChild(ui.paged(flows.sort(UC.byDate), 15, function (part) { return ui.alist(part); }));
      box.appendChild(section(L("Money flows that name it", "Flujos de dinero que lo nombran"), UC.groupAlts(flows).length, fb, L("Counts are distinct items after folding repeated reports. Amounts are not totalled.", "Los conteos son ítems distintos tras plegar informes repetidos. Los montos no se totalizan.")));
    }
    var facts = of("FinancialFact").filter(function (f) { return f.aboutParty === id; });
    if (facts.length) box.appendChild(section(L("Reported figures", "Cifras informadas"), facts.length, ui.table([
      { label: L("Figure", "Cifra"), render: function (f) { return h("span", null, UC.metricLabel(f.metric), f.unitNote ? h("div", { class: "small muted" }, f.unitNote) : null); }, sort: function (f) { return f.metric; } },
      { label: L("Value", "Valor"), cls: "r", render: function (f) { return f.amount != null ? (f.currency ? UC.fmt.money(f.amount, f.currency) : UC.fmt.num(f.amount)) : (f.textValue || ""); }, sort: function (f) { return f.amount != null ? Number(f.amount) : null; } },
      { label: L("Period", "Período"), render: function (f) { return UC.fmt.date(f); }, sort: function (f) { return f.sortDate || null; } },
      { label: L("Who says so", "Quién lo afirma"), render: function (f) { return prov.src(f); }, sort: function (f) { return f.assertedBy; } }
    ], facts, { pageSize: 15, minWidth: 620, sortCol: 2 }), L("Each figure is one source's number for one period. Figures from different sources are not comparable without reading both.", "Cada cifra es el número de una fuente para un período. Las cifras de fuentes distintas no son comparables sin leer ambas.")));
    var ev = of("CaseEvent").sort(UC.byDate);
    if (ev.length) box.appendChild(section(L("Events that name it", "Hechos que lo nombran"), ev.length, ui.paged(ev, 12, function (part) { return ui.alist(part, { noGroup: true }); })));
    var otherCharges = of("Charge").filter(function (c) { return c.chargedPerson !== id; });
    if (otherCharges.length) box.appendChild(section(L("Charges against people linked to it, as reported", "Imputaciones a personas vinculadas, según se informa"), otherCharges.length, ui.paged(otherCharges, 12, function (part) { return ui.alist(part, { noGroup: true, compact: true }); })));
    if (!all.length) box.appendChild(h("div", { class: "empty" }, L("No assertion passes the current voice and source filters.", "Ninguna afirmación pasa los filtros actuales de voz y fuente.")));
    return box;
  }

  function charged(root, s) {
    var list = (UC.db.byType.Charge || []).filter(function (c) { return UC.pass(c, s); });
    var groups = {};
    list.forEach(function (c) { var k = String(c.caseReference || "?").match(/^\S+/)[0]; (groups[k] = groups[k] || []).push(c); });
    root.appendChild(h("div", { class: "disclaimer" }, h("p", null, L("These tables list people reported as charged. A charge is the prosecution's allegation at an early stage of the process; nobody listed has been tried or convicted, and every one of them is presumed innocent. The two cases are separate proceedings and are kept apart.", "Estas tablas listan a las personas informadas como imputadas. La imputación es la atribución de hechos por la Fiscalía en una etapa temprana del proceso; nadie de la lista ha sido juzgado ni condenado, y todos gozan de presunción de inocencia. Las dos causas son procesos distintos y se muestran por separado."))));
    Object.keys(groups).sort().forEach(function (k) {
      var rows = groups[k];
      root.appendChild(h("section", { class: "sec" }, h("h3", { style: "font-size:18px;font-family:var(--display)" }, L("Case ", "Causa ") + k + " (" + rows.length + ")"),
        h("p", { class: "small muted", style: "margin:0" }, k.indexOf("89") === 0 ? L("The Ueno Bank case: the proceeding this site is about.", "La causa Ueno Bank: el proceso del que trata este sitio.") : L("A related but separate proceeding. Its defendants are not defendants in Case 89/2026 unless listed there too.", "Un proceso relacionado pero distinto. Sus imputados no lo son en la Causa 89/2026 salvo que figuren también allí.")),
        ui.table([
          { label: L("Person", "Persona"), render: function (c) { return h("span", null, ui.party(c.chargedPerson, UC.label(c.chargedPerson)), c.caseReference && c.caseReference !== k ? h("div", { class: "small muted" }, c.caseReference) : null); }, sort: function (c) { return UC.label(c.chargedPerson); } },
          { label: L("Role as reported", "Rol según la fuente"), render: function (c) { return h("span", { class: "small" }, UC.tx(c.roleReported)); } },
          { label: L("Offences alleged (original wording)", "Hechos punibles atribuidos"), render: function (c) { var o = (c.allegedOffence && (c.allegedOffence.es || c.allegedOffence.en)) || [], a = (c.allegedOffenceAdded && (c.allegedOffenceAdded.es || c.allegedOffenceAdded.en)) || []; return h("span", { class: "small", lang: "es" }, o.join("; "), a.length ? h("div", { class: "muted" }, L("Reported as added later: ", "Agregados después, según se informa: ") + a.join("; ")) : null); } },
          { label: L("Measure", "Medida"), render: function (c) { return h("span", { class: "small" }, UC.enumLabel(UC.tx(c.proceduralMeasure) || "none_reported"), c.sortDate ? h("div", { class: "muted" }, UC.fmt.date(c)) : null); }, sort: function (c) { return UC.tx(c.proceduralMeasure); } },
          { label: L("Defence position as reported", "Posición de la defensa según la fuente"), render: function (c) { var t = UC.tx(c.defenceStatement); return h("span", { class: "small" }, t.length > 220 ? t.slice(0, 217) + "…" : t); } },
          { label: L("Who says so", "Quién lo afirma"), render: function (c) { return prov.src(c); } }
        ], rows, { pageSize: 40, minWidth: 1100 })));
    });
    if (!list.length) root.appendChild(h("div", { class: "empty" }, L("No charge rows pass the current filters.", "Ninguna imputación pasa los filtros actuales.")));
  }

  UC.views.people = {
    render: function (root, sub, s) {
      UC.filterDefaults(s);
      var db = UC.db;
      if (sub === "charged" || sub === "directory") s.tab = sub;
      if (!s.tab) s.tab = "directory";
      if (s.q == null) { s.q = ""; s.type = "all"; s.sort = "count"; }
      root.appendChild(h("div", { class: "view-head" }, h("h2", null, L("People and companies", "Personas y empresas")),
        h("p", null, L("Every party named in the graph, with what each source says about it. Profiles show roles and case status only; no identity numbers, addresses or dates of birth are in the data.", "Cada parte nombrada en el grafo, con lo que dice cada fuente. Las fichas muestran solo cargos y situación procesal; los datos no contienen números de documento, domicilios ni fechas de nacimiento."))));
      root.appendChild(ui.tabs([{ id: "directory", label: L("Directory", "Directorio") }, { id: "charged", label: L("People charged", "Personas imputadas") }], s.tab, function (t) { s.tab = t; UC.go("people", null, t); }));
      var ctl = h("div", { class: "controls" });
      ui.sourceFilters(s, UC.rerender, null, false).forEach(function (c) { ctl.appendChild(c); });
      if (s.tab === "charged") { root.appendChild(ctl); charged(root, s); return; }

      var listEl = h("div", { class: "dir-list", role: "group", "aria-label": L("Directory", "Directorio") }), detail = h("div"), countEl = h("span", { class: "small muted" });
      var search = h("input", { type: "search", value: s.q, placeholder: L("Search by name", "Buscar por nombre"), "aria-label": L("Search by name", "Buscar por nombre"), style: "width:240px" });
      search.addEventListener("input", function () { s.q = search.value; drawList(); });
      ctl.insertBefore(ui.ctl(L("Sort", "Orden"), ui.seg([{ v: "count", l: L("Most assertions", "Más afirmaciones") }, { v: "name", l: L("Name", "Nombre") }], s.sort, function (v) { s.sort = v; UC.rerender(); })), ctl.firstChild);
      ctl.insertBefore(ui.ctl(L("Kind", "Tipo"), ui.seg([{ v: "all", l: L("All", "Todos") }, { v: "Person", l: L("People", "Personas") }, { v: "Organisation", l: L("Companies", "Empresas") }, { v: "Authority", l: L("Authorities", "Autoridades") }], s.type, function (v) { s.type = v; UC.rerender(); })), ctl.firstChild);
      ctl.insertBefore(ui.ctl(L("Search", "Buscar"), search), ctl.firstChild);
      root.appendChild(ctl);
      var cnt = {};
      db.parties.forEach(function (p) { cnt[p["@id"]] = (db.byParty[p["@id"]] || []).filter(function (n) { return n["@type"][0] !== "PartyDescription"; }).length; });
      function drawList() {
        var q = norm(s.q.trim());
        var list = db.parties.filter(function (p) {
          var t = p["@type"][0] === "Party" ? "Organisation" : p["@type"][0];
          if (s.type !== "all" && t !== s.type) return false;
          return !q || norm(UC.label(p["@id"]) + " " + (p.altLabel || []).join(" ")).indexOf(q) >= 0;
        });
        list.sort(function (a, b) { return s.sort === "name" ? UC.label(a["@id"]).localeCompare(UC.label(b["@id"]), UC.lang) : cnt[b["@id"]] - cnt[a["@id"]] || UC.label(a["@id"]).localeCompare(UC.label(b["@id"])); });
        listEl.innerHTML = "";
        countEl.textContent = list.length + L(" of ", " de ") + db.parties.length;
        list.forEach(function (p) {
          var b = h("button", { type: "button", "aria-current": String(p["@id"] === s.sel), onclick: function () { s.sel = p["@id"]; drawList(); drawDetail(true); } });
          b.innerHTML = shape(p["@type"][0]) + "<span class='nm'>" + UC.esc(UC.label(p["@id"])) + "</span><span class='ct'>" + cnt[p["@id"]] + "</span>";
          listEl.appendChild(b);
        });
        if (!list.length) listEl.appendChild(h("div", { class: "empty" }, L("No match.", "Sin coincidencias.")));
      }
      function drawDetail(scroll) {
        detail.innerHTML = "";
        if (!s.sel || !db.byId[s.sel]) s.sel = "ucr:org/ueno-bank";
        detail.appendChild(profile(s.sel, s));
        if (scroll && window.innerWidth <= 980) detail.scrollIntoView({ block: "start" });
      }
      root.appendChild(h("div", { class: "dir" }, h("div", { class: "stack" }, countEl, listEl), detail));
      drawList(); drawDetail(false);
      var cur = listEl.querySelector("[aria-current='true']");
      if (cur) listEl.scrollTop = Math.max(0, cur.offsetTop - 80);
    }
  };
})();
