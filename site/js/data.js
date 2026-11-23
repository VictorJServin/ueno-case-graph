/* data.js - load the JSON-LD graph and the optional analysis files, index them once, and expose
   helpers shared by every view (DOM builders, labels, one-line descriptions, alternative-report groups). */
(function () {
  "use strict";
  var UC = window.UC;

  /* ---------- tiny DOM helpers ---------- */
  UC.esc = function (s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  };
  function append(el, c) {
    if (c == null || c === false) return;
    if (Array.isArray(c)) { c.forEach(function (x) { append(el, x); }); return; }
    el.appendChild(c.nodeType ? c : document.createTextNode(String(c)));
  }
  /** h("div", {class:"x", onclick:fn, html:"..."}, child, [children]) */
  UC.h = function (tag, attrs) {
    var el = document.createElement(tag), k;
    if (attrs) for (k in attrs) {
      var v = attrs[k];
      if (v == null || v === false) continue;
      if (k === "class") el.className = v;
      else if (k === "html") el.innerHTML = v;
      else if (k === "text") el.textContent = v;
      else if (k.slice(0, 2) === "on") el.addEventListener(k.slice(2), v);
      else if (k === "data") { for (var d in v) if (v[d] != null) el.dataset[d] = v[d]; }
      else el.setAttribute(k, v === true ? "" : v);
    }
    for (var i = 2; i < arguments.length; i++) append(el, arguments[i]);
    return el;
  };
  var NS = "http://www.w3.org/2000/svg";
  UC.s = function (tag, attrs) {
    var el = document.createElementNS(NS, tag), k;
    if (attrs) for (k in attrs) {
      if (attrs[k] == null || attrs[k] === false) continue;
      if (k === "text") el.textContent = attrs[k];
      else if (k.slice(0, 2) === "on") el.addEventListener(k.slice(2), attrs[k]);
      else el.setAttribute(k, attrs[k]);
    }
    for (var i = 2; i < arguments.length; i++) append(el, arguments[i]);
    return el;
  };

  /* ---------- asserter glyphs: shape carries the voice, colour only reinforces it ---------- */
  var SHAPES = {
    Prosecution: function (r) { return "M" + (-r) + "," + (-r) + "h" + 2 * r + "v" + 2 * r + "h" + (-2 * r) + "z"; },
    Rey: function (r) { return "M0," + (-r * 1.15) + "L" + r * 1.1 + "," + r * 0.9 + "L" + (-r * 1.1) + "," + r * 0.9 + "z"; },
    Press: function (r) { return "M" + r + ",0A" + r + "," + r + " 0 1 1 " + (-r) + ",0A" + r + "," + r + " 0 1 1 " + r + ",0z"; },
    Regulator: function (r) { var q = r * 1.2; return "M0," + (-q) + "L" + q + ",0L0," + q + "L" + (-q) + ",0z"; },
    RatingAgency: function (r) { var a = r * 1.1, b = a * 0.5, c = a * 0.87; return "M" + a + ",0L" + b + "," + c + "L" + (-b) + "," + c + "L" + (-a) + ",0L" + (-b) + "," + (-c) + "L" + b + "," + (-c) + "z"; },
    Company: function (r) { var t = r * 0.42; return "M" + (-t) + "," + (-r) + "h" + 2 * t + "v" + (r - t) + "h" + (r - t) + "v" + 2 * t + "h" + (-(r - t)) + "v" + (r - t) + "h" + (-2 * t) + "v" + (-(r - t)) + "h" + (-(r - t)) + "v" + (-2 * t) + "h" + (r - t) + "z"; },
    Defence: function (r) { return "M0," + (r * 1.15) + "L" + r * 1.1 + "," + (-r * 0.9) + "L" + (-r * 1.1) + "," + (-r * 0.9) + "z"; },
    Analyst: function (r) { var i = r * 0.5; return "M" + r + ",0A" + r + "," + r + " 0 1 1 " + (-r) + ",0A" + r + "," + r + " 0 1 1 " + r + ",0zM" + i + ",0A" + i + "," + i + " 0 1 0 " + (-i) + ",0A" + i + "," + i + " 0 1 0 " + i + ",0z"; }
  };
  UC.ASSERTERS = ["Prosecution", "Rey", "Press", "Regulator", "RatingAgency", "Company", "Defence", "Analyst"];
  UC.VOICES = ["prosecution", "rey", "press"];
  UC.glyphPath = function (asserter, r) { return (SHAPES[asserter] || SHAPES.Press)(r); };
  UC.glyph = function (asserter, cls) {
    return '<svg class="glyph ' + (cls || "") + '" viewBox="-7 -7 14 14" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" d="' + UC.glyphPath(asserter, 5) + '"/></svg>';
  };
  UC.voiceGlyph = function (voice, cls) { return UC.glyph(voice === "prosecution" ? "Prosecution" : voice === "rey" ? "Rey" : "Press", cls); };

  /* ---------- loading ---------- */
  function getJSON(url) {
    return fetch(url).then(function (r) { if (!r.ok) throw new Error(url + ": HTTP " + r.status); return r.json(); });
  }
  function optional(url, text) {
    return fetch(url).then(function (r) { if (!r.ok) return null; return text ? r.text() : r.json(); }).catch(function () { return null; });
  }
  function isObj(x) { return x && typeof x === "object" && !Array.isArray(x); }

  UC.load = function () {
    return Promise.all([
      getJSON("data/graph.jsonld"), getJSON("data/stats.json"),
      optional("data/legal_prosecution.json"), optional("data/legal_defence.json"),
      optional("data/fin_credit.json"), optional("data/fin_flows.json"),
      optional("data/fibo_mapping.json"), optional("data/verified.json"),
      optional("data/editor_report.md", true), optional("data/missing_money.json"), optional("data/payouts.json")
    ]).then(function (r) {
      if (!r[0] || !Array.isArray(r[0]["@graph"])) throw new Error("data/graph.jsonld: no @graph array");
      index(r[0], r[1]);
      var x = UC.db.extra;
      x.legalP = isObj(r[2]) && Array.isArray(r[2].offences) ? r[2] : null;
      x.legalD = isObj(r[3]) && Array.isArray(r[3].offences) ? r[3] : null;
      x.finCredit = isObj(r[4]) && (Array.isArray(r[4].sections) || Array.isArray(r[4].metrics)) ? r[4] : null;
      x.finFlows = isObj(r[5]) && (Array.isArray(r[5].chains) || Array.isArray(r[5].hubs)) ? r[5] : null;
      x.fibo = isObj(r[6]) && Array.isArray(r[6].mapping) ? r[6] : null;
      x.verified = {};
      if (Array.isArray(r[7])) r[7].forEach(function (id) { if (typeof id === "string") x.verified[id] = true; });
      x.editorMd = typeof r[8] === "string" && r[8].trim() && !/^\s*<!doctype/i.test(r[8]) ? r[8] : null;
      x.missing = isObj(r[9]) && isObj(r[9].headline) && r[9].headline.central != null ? r[9] : null;
      x.payouts = isObj(r[10]) && Array.isArray(r[10].tiers) ? r[10] : null;
      return UC.db;
    });
  };

  var ASSERTION_TYPES = ["RoleHolding", "Loan", "Overdraft", "Flow", "CaseEvent", "FinancialFact", "Charge", "Issue", "PartyDescription"];
  UC.ASSERTION_TYPES = ASSERTION_TYPES;

  function index(doc, stats) {
    var nodes = doc["@graph"], db = UC.db = {
      nodes: nodes, stats: stats || {}, byId: {}, byRaw: {}, byType: {}, byParty: {},
      parties: [], sources: [], assertions: [], extra: {}, descOf: {}, altOf: {}, hidden: [], allByType: {}, opinions: [], opinionAt: {}
    };
    nodes.forEach(function (n) {
      db.byId[n["@id"]] = n;
      if (n.identifier) db.byRaw[n.identifier] = n;
      var t = n["@type"][0];
      (db.allByType[t] = db.allByType[t] || []).push(n);
      // rows the editor marked hidden stay resolvable (and listed in the Data tab) but leave every list and figure
      if (n.hidden) { db.hidden.push(n); return; }
      // analyst estimates live in graph "analysis": resolvable and listed apart, never counted or drawn as sourced claims
      if (n.graph === "analysis") { db.opinions.push(n); var loc = String(n.locator || "").split("#")[1]; if (loc) db.opinionAt[loc] = n; return; }
      (db.byType[t] = db.byType[t] || []).push(n);
      if (n.graph) db.assertions.push(n);
      else if (t === "Source") db.sources.push(n);
      else if (t === "Person" || t === "Organisation" || t === "Authority" || t === "Party") db.parties.push(n);
    });
    db.assertions.forEach(function (n) {
      (n.involvesParty || []).forEach(function (p) { (db.byParty[p] = db.byParty[p] || []).push(n); });
      if (n["@type"][0] === "PartyDescription") (n.involvesParty || []).forEach(function (p) { (db.descOf[p] = db.descOf[p] || []).push(n); });
    });
    db.loans = db.assertions.filter(UC.isLoan);
    db.flows = db.byType.Flow || [];
    db.roles = db.byType.RoleHolding || [];
    db.borrowers = {};
    db.loans.forEach(function (l) { (db.borrowers[l.nominalBorrower] = db.borrowers[l.nominalBorrower] || []).push(l); });
    buildAlts(db);
  }

  /* ---------- basic accessors ---------- */
  UC.isLoan = function (n) { return n["@type"].indexOf("Loan") >= 0; };
  UC.isOverdraft = function (n) { return n["@type"].indexOf("Overdraft") >= 0; };
  UC.kind = function (n) { return UC.isLoan(n) ? "Loan" : n["@type"][0]; };
  UC.toId = function (raw) { return "ucr:" + String(raw).replace(/:/g, "/"); };
  /** Resolve a raw project id (rec:loan:0003, org:ueno-bank, src:acta-p17) or a graph id to a node. */
  UC.resolve = function (ref) {
    if (!ref) return null;
    var db = UC.db;
    return db.byId[ref] || db.byRaw[ref] || db.byId[UC.toId(ref)] || null;
  };
  UC.isParty = function (n) { return !!n && !n.graph && /^(Person|Organisation|Authority|Party)$/.test(n["@type"][0]); };
  UC.label = function (id) {
    var n = UC.resolve(id);
    if (!n) return String(id || "").replace(/^ucr:/, "");
    if (n.label) return n.isStub ? prettyStub(n) : n.label;
    return n.name || n.identifier || n["@id"];
  };
  var STUB_LABELS = {
    "ucr:auth/juzgado-penal-garantias-de-turno": "Juzgado Penal de Garantías (de turno)",
    "ucr:auth/juzgado-penal-garantias-crimen-organizado": "Juzgado Penal de Garantías (crimen organizado)"
  };
  function prettyStub(n) {
    if (STUB_LABELS[n["@id"]]) return STUB_LABELS[n["@id"]];
    var s = (n.identifier || n["@id"]).split(/[:\/]/).pop().replace(/-/g, " ");
    return s.replace(/\b[a-z]/g, function (c) { return c.toUpperCase(); });
  }
  /** Short label for tight spaces (drops legal-form suffixes). */
  UC.short = function (id) {
    return UC.label(id).replace(/\s*\((as [^)]*|[A-Z]{3,})\)$/, "").replace(/,? (S\.A\.E\.C\.A\.|S\.A\.E\.|S\.A\.|S\.R\.L\.|E\.A\.S\.|S\.à r\.l\.)( .*)?$/, "").trim();
  };
  UC.fromRecord = function (n) { var s = UC.db.byId[n.source]; return !!s && s.sourceKind === "record"; };
  UC.isConflict = function (n) { return !!n.graph && !!n.provenanceNote && /conflict|contradict|differs?\b|disagree|discrepan|inconsisten|\bvs\.?\s/i.test(n.provenanceNote); };
  UC.precision = function (n, end) {
    if (n.datePrecision) return n.datePrecision;
    var lit = end ? n.endDate : (n.startDate || n.onDate);
    var v = lit && lit["@value"] ? lit["@value"] : "";
    return v.length === 4 ? "year" : v.length === 7 ? "month" : "day";
  };
  UC.roleDates = function (n) {
    if (!n.sortDate && !n.sortDateEnd) return "";
    var a = n.sortDate ? UC.fmt.dateStr(n.sortDate, UC.precision(n)) : "?";
    var b = n.sortDateEnd ? UC.fmt.dateStr(n.sortDateEnd, UC.precision(n, true)) : "";
    return b ? a + " – " + b : UC.L("from ", "desde ") + a;
  };
  UC.amountOf = function (n) { var v = n.amount != null ? n.amount : n.principal; return v == null ? null : Number(v); };
  UC.moneyOf = function (n, o) {
    var v = n.amount != null ? n.amount : n.principal;
    o = o || {};
    if (n.amountIsApproximate) o.approx = true;
    return UC.fmt.money(v, n.currency, o);
  };

  /** One-line description of an assertion: {title, sub}. Always phrased as a claim's content, never as fact. */
  UC.describe = function (n) {
    var t = n["@type"][0], L = UC.L, lab = UC.label, title = "", sub = "";
    if (UC.isLoan(n)) {
      title = (UC.isOverdraft(n) ? L("Overdraft", "Sobregiro") : L("Loan", "Préstamo")) + ": " + UC.short(n.lender) + " → " + UC.short(n.nominalBorrower) + ", " + UC.moneyOf(n);
      var bits = [];
      if (n.operationNumber) bits.push(L("op. ", "op. ") + n.operationNumber);
      if (n.ratePct) bits.push(UC.fmt.pct(n.ratePct));
      if (n.termYears) bits.push(UC.fmt.num(n.termYears) + L(" yr", " años"));
      if (n.termDays) bits.push(n.termDays + L(" days", " días"));
      if (n.collateral) bits.push(L("collateral: ", "garantía: ") + UC.enumLabel(n.collateral));
      if (n.loanStatus) bits.push(UC.enumLabel(n.loanStatus));
      sub = bits.join(" · ") || UC.tx(n.note);
    } else if (t === "Flow") {
      title = UC.short(n.fromParty) + " → " + UC.short(n.toParty) + ": " + UC.moneyOf(n);
      sub = UC.enumLabel(n.instrument) + (n.purpose ? " · " + UC.tx(n.purpose) : "");
    } else if (t === "RoleHolding") {
      title = lab(n.holder) + " · " + UC.enumLabel(n.roleType) + (n.percentage ? " " + UC.fmt.pct(n.percentage) : "") + " · " + lab(n.organisation);
      sub = UC.tx(n.note);
    } else if (t === "CaseEvent") {
      title = UC.tx(n.title);
      sub = UC.tx(n.description);
      if (n.amount) sub = UC.fmt.money(n.amount, n.currency) + (sub ? " · " + sub : "");
    } else if (t === "FinancialFact") {
      var val = n.amount != null ? (n.currency ? UC.fmt.money(n.amount, n.currency) : UC.fmt.num(n.amount)) : (n.textValue || "");
      title = UC.short(n.aboutParty) + ": " + UC.metricLabel(n.metric) + " = " + val;
      sub = n.unitNote || "";
    } else if (t === "Charge") {
      title = lab(n.chargedPerson) + ": " + L("charge reported", "imputación reportada") + " (" + UC.enumLabel(UC.tx(n.proceduralMeasure) || "none_reported") + ")";
      sub = ((n.allegedOffence && (n.allegedOffence.es || n.allegedOffence.en)) || []).join("; ");
    } else if (t === "Issue") {
      title = L("Data issue: ", "Inconsistencia: ") + (n.issueLocation || "");
      sub = UC.tx(n.description);
    } else if (t === "AnalystOpinion") {
      var eb = [];
      if (n.estimateCentral != null) eb.push(UC.fmt.money(n.estimateCentral, n.currency, { compact: true }));
      if (n.estimateLow != null && n.estimateHigh != null) eb.push("(" + UC.fmt.money(n.estimateLow, n.currency, { compact: true }) + " – " + UC.fmt.money(n.estimateHigh, n.currency, { compact: true }) + ")");
      title = L("AI analyst estimate: ", "Estimación de analista de IA: ") + UC.tx(n.title) + (eb.length ? " · " + eb.join(" ") : "");
      sub = UC.tx(n.description);
    } else if (t === "PartyDescription") {
      title = L("Description of ", "Descripción de ") + (n.label || lab((n.involvesParty || [])[0]));
      sub = UC.tx(n.description) + (n.business ? " · " + UC.tx(n.business) : "");
    } else {
      title = n.label || n.name || n["@id"];
    }
    // rows flagged `alleged` state conduct: say whose claim it is in the text itself
    if (n.alleged) title = (n.assertedBy === "Rey" ? L("Rey states: ", "Rey declara: ") : L("The prosecution alleges: ", "La Fiscalía sostiene: ")) + title;
    return { title: title, sub: sub };
  };
  /** Same, without the "alleges" prefix (for tight labels that already sit under a voice heading). */
  UC.describeBare = function (n) { var a = n.alleged; n.alleged = false; var d = UC.describe(n); if (a) n.alleged = a; return d; };

  /* ---------- source tiers and the shared voice / tier / confidence filter ---------- */
  UC.TIERS = ["record", "press_linked", "rating_or_official", "dossier", "editorial", "unlinked"];
  UC.tierOf = function (n) { return n.sourceTier || "unlinked"; };
  UC.filterDefaults = function (s) {
    if (!s.voices) s.voices = { prosecution: true, rey: true, press: true };
    if (!s.tiers) { s.tiers = {}; UC.TIERS.forEach(function (t) { s.tiers[t] = true; }); }
    if (!s.conf) s.conf = { high: true, medium: true, low: true };
    return s;
  };
  UC.pass = function (n, s) { return !!s.voices[n.graph] && !!s.tiers[UC.tierOf(n)] && (!s.conf || !!s.conf[n.confidence]); };
  /** Editor check of a row: {verified, method, note} or null. */
  UC.checkOf = function (n) {
    if (!n) return null;
    if (n.verified != null) return { verified: !!n.verified, method: n.verifiedMethod || "", note: n.verifiedNote || "" };
    var v = UC.db.extra.verified;
    return v && (v[n["@id"]] || v[n.identifier]) ? { verified: true, method: "", note: "" } : null;
  };

  /* ---------- alternative reports of one item ----------
     Several rows often describe the same transfer or loan (same parties, currency, date and amount).
     They are grouped so views can show one item with a counter; amounts are never added. */
  function buildAlts(db) {
    var parent = {};
    function find(x) { while (parent[x] && parent[x] !== x) x = parent[x]; return x; }
    function union(a, b) { a = find(a); b = find(b); if (a !== b) parent[b] = a; }
    db.assertions.forEach(function (n) { parent[n["@id"]] = n["@id"]; });
    var buckets = {}, opKey = {};
    // the editor's explicit grouping comes first; the heuristics below only add exact repeats it did not cover
    db.assertions.forEach(function (n) {
      if (!n.sameOperationKey) return;
      if (opKey[n.sameOperationKey]) union(opKey[n.sameOperationKey], n["@id"]); else opKey[n.sameOperationKey] = n["@id"];
    });
    db.flows.forEach(function (f) {
      var k = "F|" + f.fromParty + "|" + f.toParty + "|" + (f.currency || "") + "|" + (f.sortDate || f.dateText || "") + "|" + (f.amount == null ? "na|" + f.instrument : "");
      (buckets[k] = buckets[k] || []).push(f);
    });
    db.loans.forEach(function (l) {
      if (l.principal == null) return;
      var k = "L|" + l.nominalBorrower + "|" + (l.currency || "") + "|" + (l.sortDate || "") + "|" + (UC.isOverdraft(l) ? "od" : "ln");
      (buckets[k] = buckets[k] || []).push(l);
      (l.sameSubjectAs || []).forEach(function (o) { if (parent[o]) union(l["@id"], o); });
    });
    Object.keys(buckets).forEach(function (k) {
      var b = buckets[k];
      if (b.length < 2) return;
      if (b[0].amount == null && b[0].principal == null) { b.forEach(function (x) { union(b[0]["@id"], x["@id"]); }); return; }
      b.sort(function (x, y) { return UC.amountOf(x) - UC.amountOf(y); });
      for (var i = 1; i < b.length; i++) {
        var a0 = UC.amountOf(b[i - 1]), a1 = UC.amountOf(b[i]);
        if (a1 === a0 || (a0 > 0 && (a1 - a0) / a0 <= 0.006)) union(b[i - 1]["@id"], b[i]["@id"]);
      }
    });
    var groups = {};
    db.assertions.forEach(function (n) { var r = find(n["@id"]); (groups[r] = groups[r] || []).push(n); });
    Object.keys(groups).forEach(function (r) {
      var g = groups[r];
      if (g.length < 2) return;
      g.sort(UC.repOrder);
      g.forEach(function (n) { db.altOf[n["@id"]] = g; });
    });
  }
  var CONF = { high: 0, medium: 1, low: 2 };
  /** Order used to choose the row that represents a group: record first, exact before approximate, clearer reading first. */
  UC.repOrder = function (a, b) {
    var ra = UC.fromRecord(a) ? 0 : 1, rb = UC.fromRecord(b) ? 0 : 1;
    if (ra !== rb) return ra - rb;
    var xa = a.amountIsApproximate ? 1 : 0, xb = b.amountIsApproximate ? 1 : 0;
    if (xa !== xb) return xa - xb;
    if (CONF[a.confidence] !== CONF[b.confidence]) return CONF[a.confidence] - CONF[b.confidence];
    return a["@id"] < b["@id"] ? -1 : 1;
  };
  /** Collapse a list of assertions into [{rep, items}] using the alternative-report groups. */
  UC.groupAlts = function (list) {
    var seen = {}, out = [], inList = {};
    list.forEach(function (n) { inList[n["@id"]] = 1; });
    list.forEach(function (n) {
      if (seen[n["@id"]]) return;
      var g = (UC.db.altOf[n["@id"]] || [n]).filter(function (x) { return inList[x["@id"]]; });
      g.forEach(function (x) { seen[x["@id"]] = 1; });
      out.push({ rep: g[0], items: g });
    });
    return out;
  };

  UC.byDate = function (a, b) {
    var x = a.sortDate || "9999", y = b.sortDate || "9999";
    return x < y ? -1 : x > y ? 1 : (a["@id"] < b["@id"] ? -1 : 1);
  };
  UC.debounce = function (fn, ms) { var t; return function () { var a = arguments, s = this; clearTimeout(t); t = setTimeout(function () { fn.apply(s, a); }, ms); }; };
  /** Read a CSS token (for canvas drawing). */
  UC.token = function (name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); };
})();
