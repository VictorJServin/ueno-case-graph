/* prov.js - the single provenance component (drawer) used by every view, plus small shared UI pieces.
   Any element carrying data-prov="id id ..." opens the drawer on click / Enter. */
(function () {
  "use strict";
  var UC = window.UC, h = UC.h, L = UC.L, esc = UC.esc;
  var prov = UC.prov = {}, ui = UC.ui = {};
  var lastFocus = null, current = null;

  function vclass(n) { return n && n.graph ? "v-" + n.graph : ""; }
  prov.vclass = vclass;

  /* ---------- source wording ---------- */
  prov.sourceShort = function (n) {
    var s = UC.db.byId[n.source];
    if (!s) return "";
    if (s.sourceKind === "record") return L("Record p. ", "Acta p. ") + (s.page != null ? s.page : "?");
    return (s.outlet || UC.enumLabel(s.sourceKind)) + (s.sortDate ? ", " + UC.fmt.dateStr(s.sortDate, s.datePrecision) : "");
  };
  prov.asserterText = function (n) {
    var a = UC.enumLabel(n.assertedBy);
    if ((n.assertedBy === "Prosecution" || n.assertedBy === "Rey") && !UC.fromRecord(n)) a += L(", as reported by ", ", según ") + ((UC.db.byId[n.source] || {}).outlet || L("press", "prensa"));
    return a;
  };
  /** Plain-text provenance line (tooltips, copy). */
  prov.line = function (n) {
    var s = UC.db.byId[n.source] || {}, q = n.quote ? UC.tx(n.quote) : "";
    return prov.asserterText(n) + " · " + prov.sourceShort(n) + (n.locator ? " · " + n.locator : "") + (q ? " · “" + q + "”" : "") + " · " + L("confidence ", "confianza ") + UC.enumLabel(n.confidence) + (s.url ? " · " + s.url : "");
  };
  prov.tip = function (n) {
    var d = UC.describe(n);
    return "<b>" + esc(d.title) + "</b><span class='t2'>" + esc(UC.fmt.date(n)) + " · " + esc(prov.asserterText(n)) + " · " + esc(prov.sourceShort(n)) + " · " + esc(UC.enumLabel(n.confidence)) + "</span>";
  };

  /* ---------- small building blocks ---------- */
  prov.badge = function (n) {
    return h("span", { class: "badge " + vclass(n), html: UC.glyph(n.assertedBy) + esc(UC.enumLabel(n.assertedBy)) });
  };
  prov.conf = function (c) {
    return h("span", { class: "conf c-" + c, title: L("Reading confidence: ", "Confianza de lectura: ") + UC.enumLabel(c), role: "img", "aria-label": L("confidence ", "confianza ") + UC.enumLabel(c) }, h("i"), h("i"), h("i"));
  };
  function checked(n) { return UC.checkOf(n); }
  function okMark(ck) { return ck && ck.verified ? "<span class='ok' title='" + esc(L("Checked against the source by the editor", "Cotejado con la fuente por el editor")) + "'>✓</span>" : ""; }
  /** Chip that opens provenance for one node (assertion, source or party). */
  prov.chip = function (ref, label) {
    var n = typeof ref === "string" ? UC.resolve(ref) : ref;
    if (!n) return h("span", { class: "chip plain", title: L("Reference not in the graph", "Referencia fuera del grafo") }, String(ref));
    if (UC.isParty(n)) return ui.party(n["@id"]);
    var raw = n.identifier || n["@id"], ck = checked(n);
    var b = h("button", { type: "button", class: "chip " + vclass(n), data: { prov: n["@id"] }, "aria-label": L("Provenance of ", "Procedencia de ") + raw });
    b.innerHTML = (n.graph ? UC.glyph(n.assertedBy) : "") + esc(label || raw) + okMark(ck);
    b.dataset.tip = n.graph ? prov.tip(n) : esc((n.outlet || "") + " · " + (n.name || ""));
    return b;
  };
  /** List of raw refs as chips; long lists fold behind a "+n" button. */
  prov.chips = function (refs, max) {
    var box = h("span", { class: "refs" });
    refs = (refs || []).filter(function (r, i, a) { return r && a.indexOf(r) === i; });
    max = max || 6;
    refs.forEach(function (r, i) {
      var c = prov.chip(r);
      if (i >= max) c.hidden = true;
      box.appendChild(c);
    });
    if (refs.length > max) {
      var more = h("button", { type: "button", class: "more", "aria-expanded": "false" }, "+" + (refs.length - max));
      more.addEventListener("click", function () {
        Array.prototype.forEach.call(box.querySelectorAll(".chip"), function (c) { c.hidden = false; });
        more.remove();
      });
      box.appendChild(more);
    }
    if (refs.length > 1) {
      var all = refs.map(function (r) { var n = UC.resolve(r); return n && !UC.isParty(n) ? n["@id"] : null; }).filter(Boolean);
      if (all.length > 1) box.appendChild(h("button", { type: "button", class: "more", data: { prov: all.join(" ") } }, L("all", "todas")));
    }
    return box;
  };
  /** Compact "who + where" button shown beside any figure or row. */
  prov.src = function (n, extraIds) {
    var b = h("button", { type: "button", class: "src " + vclass(n), data: { prov: [n["@id"]].concat(extraIds || []).join(" ") } });
    var ck = checked(n);
    b.innerHTML = UC.glyph(n.assertedBy) + "<span>" + esc(prov.sourceShort(n)) + "</span>" + okMark(ck) + (n.correctedField ? "<span class='tag' title='" + esc(L("Corrected by the editor", "Corregido por el editor")) + "'>" + esc(L("corr.", "corr.")) + "</span>" : "") + (extraIds && extraIds.length ? " <span class='tag'>+" + extraIds.length + "</span>" : "");
    b.setAttribute("aria-label", L("Provenance: ", "Procedencia: ") + prov.asserterText(n) + ", " + prov.sourceShort(n));
    return b;
  };
  /** Make any element (HTML or SVG) open provenance. */
  prov.attach = function (el, ids, label) {
    ids = Array.isArray(ids) ? ids : [ids];
    el.setAttribute("data-prov", ids.join(" "));
    if (el.tagName.toLowerCase() !== "button") { el.setAttribute("tabindex", "0"); el.setAttribute("role", "button"); }
    if (label) el.setAttribute("aria-label", label);
    return el;
  };
  ui.party = function (id, label) {
    var n = UC.resolve(id);
    if (!n) return h("span", { class: "chip plain" }, String(id));
    return h("button", { type: "button", class: "chip party", data: { party: n["@id"] } }, label || UC.short(n["@id"]));
  };

  /* ---------- drawer ---------- */
  var drawer, body, head;
  function ensure() {
    if (drawer) return;
    drawer = document.getElementById("drawer"); body = document.getElementById("drawer-body"); head = document.getElementById("drawer-h");
    document.getElementById("drawer-x").addEventListener("click", prov.close);
  }
  prov.close = function () {
    ensure();
    if (drawer.hidden) return;
    drawer.hidden = true; current = null;
    if (lastFocus && document.contains(lastFocus)) { try { lastFocus.focus(); } catch (e) { /* ignore */ } }
  };
  prov.isOpen = function () { ensure(); return !drawer.hidden; };
  /** Open the drawer for one or more node ids. */
  prov.open = function (ids, opts) {
    ensure();
    ids = (Array.isArray(ids) ? ids : String(ids).split(/\s+/)).filter(Boolean);
    var nodes = ids.map(UC.resolve).filter(Boolean);
    if (!nodes.length) return;
    if (drawer.hidden) lastFocus = document.activeElement;
    current = { ids: ids, opts: opts || {} };
    body.innerHTML = "";
    document.getElementById("drawer-x").setAttribute("aria-label", L("Close", "Cerrar"));
    if (nodes.length === 1 && UC.isParty(nodes[0])) {
      head.textContent = UC.enumLabel(nodes[0]["@type"][0]);
      body.appendChild(partyBlock(nodes[0]));
    } else {
      head.textContent = (opts && opts.title) || (nodes.length === 1 ? L("Provenance", "Procedencia") : nodes.length + L(" reports", " informes"));
      if (nodes.length > 1) {
        body.appendChild(h("p", { class: "small muted" }, (opts && opts.note) || L("Each card is a separate claim with its own source. Where several cards describe the same operation they are alternative reports of it: amounts are not to be added.", "Cada tarjeta es una afirmación distinta con su propia fuente. Cuando varias describen la misma operación son informes alternativos: los montos no se suman.")));
        body.appendChild(ui.voiceCount(nodes));
      }
      nodes.sort(function (a, b) { return a.graph && b.graph ? UC.repOrder(a, b) : 0; });
      nodes.forEach(function (n, i) { body.appendChild(n.graph ? assertionBlock(n, nodes.length <= 3 || i === 0) : n["@type"][0] === "Correction" ? correctionBlock(n) : sourceBlock(n)); });
    }
    drawer.hidden = false;
    body.scrollTop = 0;
    body.focus();
  };
  prov.refresh = function () { if (current && !drawer.hidden) prov.open(current.ids, current.opts); };

  function dl(rows) {
    var d = h("dl");
    rows.forEach(function (r) { if (r && r[1] != null && r[1] !== "") { d.appendChild(h("dt", null, r[0])); d.appendChild(h("dd", null, r[1])); } });
    return d;
  }
  function sourceLine(s) {
    var box = h("span");
    if (s.sourceKind === "record") {
      box.appendChild(h("b", null, L("Prosecution record, page ", "Acta fiscal, página ") + (s.page != null ? s.page : "?")));
      box.appendChild(h("span", { class: "muted" }, " · " + (s.name || "") + " · " + UC.fmt.dateStr(s.sortDate, s.datePrecision)));
      box.appendChild(h("div", { class: "small muted" }, L("Primary document. The scanned pages are not published here.", "Documento primario. Las páginas escaneadas no se publican aquí.")));
    } else {
      box.appendChild(h("b", null, s.outlet || UC.enumLabel(s.sourceKind)));
      box.appendChild(h("span", null, " · " + (s.name || "")));
      box.appendChild(h("span", { class: "muted" }, " · " + UC.fmt.dateStr(s.sortDate, s.datePrecision) + " · " + UC.enumLabel(s.sourceKind)));
      if (s.url && /^https?:\/\//.test(s.url)) box.appendChild(h("div", null, h("a", { href: s.url, target: "_blank", rel: "noopener" }, L("Open the source in a new tab", "Abrir la fuente en una pestaña nueva"))));
    }
    if (s.provenanceNote) box.appendChild(h("div", { class: "small muted" }, s.provenanceNote));
    return box;
  }
  function sourceBlock(s) {
    var used = UC.db.assertions.filter(function (a) { return a.source === s["@id"]; });
    return h("div", { class: "pv" },
      h("div", { class: "pv-title" }, L("Source", "Fuente")),
      sourceLine(s),
      h("div", { class: "small muted" }, used.length + L(" assertions in the graph cite this source.", " afirmaciones del grafo citan esta fuente.")),
      used.length ? h("button", { type: "button", class: "btn sm", data: { prov: used.slice(0, 60).map(function (a) { return a["@id"]; }).join(" ") } }, L("Show them", "Mostrarlas") + (used.length > 60 ? " (60)" : "")) : null);
  }
  function correctionBlock(c) {
    var notes = c.editorNote ? (c.editorNote[UC.lang] || c.editorNote.en || []) : [];
    return h("div", { class: "pv" },
      h("div", { class: "row between" }, h("span", { class: "tag strong" }, L("Editor correction", "Corrección del editor")), h("span", { class: "tiny muted" }, c.identifier || "")),
      dl([[L("Row", "Fila"), c.correctsRow ? prov.chip(c.correctsRow) : null], [L("Action", "Acción"), c.correctionAction], [L("Field", "Campo"), (c.correctedField || []).join(", ")],
        [L("Before", "Antes"), (c.originalValue || []).join("; ")], [L("After", "Después"), c.newValue], [L("Reason", "Motivo"), notes.join(" ")],
        [L("Checked against", "Cotejado con"), c.checkedAgainst], [L("Status", "Estado"), c.correctionStatus], [L("Source", "Fuente"), c.source && UC.db.byId[c.source] ? prov.chip(c.source) : null]]));
  }
  var DENY = /c[eé]dula|^ci$|passport|pasaporte|address|domicilio|birth|nacimiento|^dob$|phone|tel[eé]fono|email|^ruc$|^x_|placeReported/i;
  var SKIP = { basedOn: 1, description: 1, title: 1, correction: 1, correctionSource: 1, editorNote: 1, originalValue: 1, hiddenReason: 1, "@id": 1, "@type": 1, graph: 1, onDate: 1, startDate: 1, endDate: 1, date: 1, involvesParty: 1, source: 1, quote: 1, provenanceNote: 1, locator: 1, confidence: 1, assertedBy: 1 };
  function fieldTable(n) {
    var kv = h("div", { class: "kv" });
    Object.keys(n).forEach(function (k) {
      if (SKIP[k] || DENY.test(k)) return;
      var v = n[k], out;
      if (v && typeof v === "object" && !Array.isArray(v)) out = UC.tx(v);
      else if (Array.isArray(v)) out = v.map(function (x) { return typeof x === "string" && x.indexOf("ucr:") === 0 ? UC.label(x) : x; }).join("; ");
      else if (typeof v === "string" && v.indexOf("ucr:") === 0) out = UC.label(v);
      else out = String(v);
      kv.appendChild(h("b", null, k)); kv.appendChild(h("span", null, out));
    });
    return kv;
  }
  function assertionBlock(n, open) {
    var d = UC.describe(n), s = UC.db.byId[n.source] || {}, raw = n.identifier || n["@id"];
    var box = h("div", { class: "pv " + vclass(n) });
    box.appendChild(h("div", { class: "row between" }, prov.badge(n), h("span", { class: "tiny muted" }, UC.enumLabel(UC.kind(n)) + " · " + raw)));
    box.appendChild(h("div", { class: "pv-title" }, d.title));
    if (d.sub) box.appendChild(h("div", { class: "pv-sub" }, d.sub));
    var voiceNote = n.graph === "prosecution" ? L("Read directly in the prosecution record (pages 1-19). An allegation, not a finding.", "Leído directamente en el acta fiscal (páginas 1 a 19). Es una imputación, no un hecho probado.")
      : n.graph === "analysis" ? L("An estimate or interpretation by the project's AI analysts. It is not a finding of the record and not a sourced figure; it must not be added to sourced amounts.", "Estimación o interpretación de los analistas de IA del proyecto. No es una conclusión del acta ni una cifra con fuente; no debe sumarse a montos con fuente.")
      : n.graph === "rey" ? L("Said by the suspect in his own statement (record pages 19-24). Unverified.", "Dicho por el imputado en su declaración (acta, páginas 19 a 24). Sin verificar.")
      : n.assertedBy === "Prosecution" ? L("A prosecution claim as reported by another source; not read in the record itself.", "Afirmación de la Fiscalía según otra fuente; no leída en el acta.")
      : n.assertedBy === "Rey" ? L("Attributed to Rey's statement by another source; not read in the record itself.", "Atribuido a la declaración de Rey por otra fuente; no leído en el acta.")
      : L("Outside the record: press, regulator, rating agency, company or defence, as labelled.", "Fuera del acta: prensa, regulador, calificadora, empresa o defensa, según se indica.");
    var tier = UC.tierOf(n), tierEl = h("span", null, UC.enumLabel(tier), tier === "dossier" ? h("span", { class: "muted" }, L(" · unlinked third-party material: it names outlets but gives no article, date or page, so it cannot be traced further", " · material de terceros sin enlaces: nombra medios pero no artículo, fecha ni página, por lo que no puede rastrearse más")) : tier === "record" ? h("span", { class: "muted" }, L(" · the primary source", " · la fuente primaria")) : null);
    var q = n.quote ? UC.tx(n.quote) : "";
    var qEl = q ? h("blockquote", { lang: n.quote.es ? "es" : "en" }, "“" + q + "”") : null;
    var confEl = h("span", null, prov.conf(n.confidence), " " + UC.enumLabel(n.confidence), h("span", { class: "muted" }, L(" (how clearly the source could be read, not how likely the claim is)", " (qué tan clara es la lectura de la fuente, no la probabilidad de la afirmación)")));
    var dateTxt = n.sortDate || n.dateText ? UC.fmt.date(n) + (n.dateText && n.datePrecision && n.datePrecision !== "day" ? " (" + L("stated as ", "indicado como ") + n.dateText + ")" : "") : (UC.kind(n) === "RoleHolding" ? UC.roleDates(n) : "");
    if (UC.kind(n) === "RoleHolding" && (n.sortDate || n.sortDateEnd)) dateTxt = UC.roleDates(n);
    box.appendChild(dl([
      [L("Asserted by", "Lo afirma"), h("span", null, h("b", null, prov.asserterText(n)), h("div", { class: "small muted" }, voiceNote))],
      [L("Source", "Fuente"), sourceLine(s)],
      [L("Source tier", "Nivel de fuente"), tierEl],
      [L("Where", "Ubicación"), n.locator],
      [L("Quote", "Cita"), qEl],
      [L("Confidence", "Confianza"), confEl],
      [L("Date", "Fecha"), dateTxt]
    ]));
    if (n.provenanceNote) {
      var conflict = UC.isConflict(n);
      box.appendChild(h("div", { class: "note" + (conflict ? " conflict" : "") }, conflict ? h("b", null, L("Conflict between sources. ", "Conflicto entre fuentes. ")) : h("b", null, L("Note. ", "Nota. ")), n.provenanceNote));
    }
    var ck = checked(n);
    if (ck) box.appendChild(h("div", { class: "checked" + (ck.verified ? "" : " fail") }, (ck.verified ? "✓ " + L("Checked against the source by the editor", "Cotejado con la fuente por el editor") : "✕ " + L("Editor check: not confirmed", "Control del editor: no confirmado")) + (ck.method ? " (" + ck.method + ")" : ""), ck.note ? h("span", { class: "muted", style: "font-weight:400" }, " " + ck.note) : null));
    if (n.hidden) box.appendChild(h("div", { class: "note conflict" }, h("b", null, L("Kept out of charts and lists by the editor. ", "Excluido de gráficos y listas por el editor. ")), UC.tx(n.hiddenReason)));
    if (n.correctedField && n.correctedField.length) {
      var cb = h("div", { class: "note" }, h("b", null, L("Corrected by the editor", "Corregido por el editor") + " (" + n.correctedField.join(", ") + "). "), L("The value shown is the corrected one.", "El valor mostrado es el corregido."));
      var notes = n.editorNote ? (n.editorNote[UC.lang] || n.editorNote.en || n.editorNote.es || []) : [];
      (n.originalValue || []).forEach(function (o, i) {
        cb.appendChild(h("div", { style: "margin-top:4px" }, h("span", { class: "muted" }, L("Before: ", "Antes: ")), h("code", null, o.length > 220 ? o.slice(0, 217) + "…" : o), notes[i] ? h("div", null, notes[i]) : null));
      });
      if (notes.length > (n.originalValue || []).length) notes.slice((n.originalValue || []).length).forEach(function (t) { cb.appendChild(h("div", null, t)); });
      var cs = (n.correctionSource || []).concat(n.correction || []);
      if (cs.length) { var cl = h("div", { class: "small", style: "margin-top:4px" }, L("Relies on: ", "Se apoya en: ")); cs.forEach(function (x) { cl.appendChild(prov.chip(x)); }); cb.appendChild(cl); }
      box.appendChild(cb);
    }
    var alts = (UC.db.altOf[n["@id"]] || []).filter(function (x) { return x !== n; });
    if (alts.length) {
      var ab = h("div", { class: "small" }, h("b", null, L("Other reports of the same item (not additive): ", "Otros informes del mismo ítem (no se suman): ")));
      alts.forEach(function (x) { ab.appendChild(prov.chip(x)); });
      box.appendChild(ab);
    }
    var links = [];
    if (n.basedOn && n.basedOn.length) {
      var bb = h("div", { class: "small" }, h("b", null, L("Rests on these sourced rows (", "Se apoya en estas filas con fuente (") + n.basedOn.length + "): "));
      n.basedOn.slice(0, 12).forEach(function (x) { bb.appendChild(prov.chip(x)); });
      bb.appendChild(h("button", { type: "button", class: "btn sm", data: { prov: n.basedOn.join(" ") } }, L("Open all with their sources", "Abrir todas con sus fuentes")));
      box.appendChild(bb);
    }
    if (n.linkedLoan) links.push(n.linkedLoan);
    if (n.restates) links.push(n.restates);
    if (n.measureSource) links.push(n.measureSource);
    if (n.statusSource) links.push(n.statusSource);
    (n.recipientDerivedFrom || []).forEach(function (x) { links.push(x); });
    (n.concerns || []).forEach(function (x) { links.push(x); });
    if (links.length) {
      var lb = h("div", { class: "small" }, h("b", null, L("Linked rows: ", "Filas relacionadas: ")));
      links.forEach(function (x) { lb.appendChild(prov.chip(x)); });
      box.appendChild(lb);
    }
    if (n.involvesParty && n.involvesParty.length) {
      var pb = h("div", { class: "small" }, h("b", null, L("Parties named: ", "Partes nombradas: ")));
      n.involvesParty.forEach(function (p) { pb.appendChild(ui.party(p)); });
      box.appendChild(pb);
    }
    var cite = d.title + " — " + prov.line(n) + " [" + raw + "]";
    box.appendChild(h("div", { class: "row" }, ui.copyBtn(function () { return cite; }, L("Copy citation", "Copiar cita")),
      h("details", null, h("summary", null, L("All fields of this row", "Todos los campos de la fila")), fieldTable(n))));
    if (!open) {
      var det = h("details", { class: "pv " + vclass(n) }, h("summary", { class: "row" }, prov.badge(n), h("span", { class: "pv-sub", style: "flex:1;min-width:0" }, d.title), h("span", { class: "tiny muted" }, prov.sourceShort(n))));
      box.className = "stack"; box.style.marginTop = "8px";
      det.appendChild(box);
      return det;
    }
    return box;
  }
  function partyBlock(p) {
    var id = p["@id"], claims = UC.db.byParty[id] || [], t = p["@type"][0];
    var box = h("div", { class: "stack" });
    box.appendChild(h("div", { class: "pv-title", style: "font-size:18px;font-family:var(--display)" }, UC.label(id)));
    if (p.altLabel) box.appendChild(h("div", { class: "small muted" }, L("Also written: ", "También: ") + p.altLabel.join("; ")));
    if (p.isStub) box.appendChild(h("div", { class: "note small" }, L("Named by assertions but not yet described by any contributor.", "Nombrado en afirmaciones pero aún sin descripción.")));
    if (p.business) box.appendChild(h("div", null, h("b", null, L("Business: ", "Actividad: ")), UC.tx(p.business)));
    if (p.description) box.appendChild(h("div", null, UC.tx(p.description)));
    var descs = UC.db.descOf[id] || [];
    if (descs.length) { var sb = h("div", { class: "small muted row" }, L("Description from: ", "Descripción según: ")); descs.forEach(function (d) { sb.appendChild(prov.src(d)); }); box.appendChild(sb); }
    if (t === "Person") box.appendChild(h("div", { class: "note small" }, L("Being named here, or listed as an officer or shareholder, is not an accusation. Presumption of innocence applies.", "Figurar aquí, o como directivo o accionista, no es una acusación. Rige la presunción de inocencia.")));
    box.appendChild(ui.voiceCount(claims));
    box.appendChild(h("div", { class: "row" },
      h("button", { type: "button", class: "btn sm", onclick: function () { prov.close(); UC.go("people", { sel: id }); } }, L("Open full profile", "Abrir ficha completa")),
      h("button", { type: "button", class: "btn sm", onclick: function () { prov.close(); UC.go("network", { focus: id, preset: null, kinds: null, sel: { type: "node", id: id } }); } }, L("Show in network", "Ver en la red"))));
    box.appendChild(ui.agroups(claims.filter(function (c) { return c["@type"][0] !== "PartyDescription"; }), { openFirst: false }));
    return box;
  }

  /* ---------- shared list components ---------- */
  ui.voiceCount = function (nodes) {
    var c = { prosecution: 0, rey: 0, press: 0 };
    nodes.forEach(function (n) { if (n.graph) c[n.graph]++; });
    var box = h("div", { class: "row small" });
    UC.VOICES.forEach(function (v) { if (c[v]) box.appendChild(h("span", { class: "badge v-" + v, html: UC.voiceGlyph(v) + esc(UC.enumLabel(v)) + " <b>" + c[v] + "</b>" })); });
    return box;
  };
  /** Rows of assertions: date | what is claimed | who and where (opens provenance). */
  ui.alist = function (nodes, opts) {
    opts = opts || {};
    var box = h("div", { class: "alist" });
    var groups = opts.noGroup ? nodes.map(function (n) { return { rep: n, items: [n] }; }) : UC.groupAlts(nodes);
    groups.forEach(function (g) {
      var n = g.rep, d = UC.describe(n);
      var x = h("div", { class: "x" }, d.title, d.sub && !opts.compact ? h("span", { class: "sub" }, d.sub.length > 260 ? d.sub.slice(0, 257) + "…" : d.sub) : null);
      if (g.items.length > 1) x.appendChild(h("span", { class: "tag warn", title: L("Reported several times; one item, not additive", "Reportado varias veces; un solo ítem, no se suma") }, g.items.length + L(" reports of one item", " informes de un ítem")));
      if (UC.isConflict(n)) x.appendChild(h("span", { class: "tag warn" }, L("sources conflict", "fuentes en conflicto")));
      var when = UC.kind(n) === "RoleHolding" ? UC.roleDates(n) : (n.sortDate || n.dateText ? UC.fmt.date(n) : "");
      box.appendChild(h("div", { class: "arow" }, h("span", { class: "d" }, when), x, prov.src(n, g.items.slice(1).map(function (i) { return i["@id"]; }))));
    });
    if (!groups.length) box.appendChild(h("div", { class: "empty" }, L("Nothing matches.", "Sin resultados.")));
    return box;
  };
  /** Assertions grouped by type in collapsible sections, each sorted by date. */
  ui.agroups = function (nodes, opts) {
    opts = opts || {};
    var by = {}, box = h("div", { class: "stack" });
    nodes.forEach(function (n) { var k = n["@type"][0] === "Overdraft" ? "Loan" : n["@type"][0]; (by[k] = by[k] || []).push(n); });
    ["Charge", "RoleHolding", "Loan", "Flow", "CaseEvent", "FinancialFact", "Issue", "PartyDescription"].forEach(function (t, i) {
      if (!by[t]) return;
      var list = by[t].slice().sort(UC.byDate);
      var det = h("details", { class: "agroup" }, h("summary", null, h("span", { class: "t" }, UC.enumLabel(t)), h("span", { class: "n" }, list.length)));
      if (opts.openFirst !== false && (opts.openAll || Object.keys(by).length === 1)) det.open = true;
      var filled = false;
      function fill() { if (filled) return; filled = true; det.appendChild(ui.paged(list, 40, function (part) { return ui.alist(part); })); }
      det.addEventListener("toggle", function () { if (det.open) fill(); });
      if (det.open) fill();
      box.appendChild(det);
    });
    if (!nodes.length) box.appendChild(h("div", { class: "empty" }, L("No assertions.", "Sin afirmaciones.")));
    return box;
  };
  /** Paginate any list: render(part) is called for the current page. */
  ui.paged = function (list, size, render) {
    var page = 0, box = h("div", { class: "stack" }), host = h("div"), nav = h("div", { class: "pager" });
    function draw() {
      host.innerHTML = "";
      host.appendChild(render(list.slice(page * size, (page + 1) * size), page * size));
      nav.innerHTML = "";
      var pages = Math.ceil(list.length / size);
      if (pages > 1) {
        nav.appendChild(h("span", null, (page * size + 1) + "–" + Math.min(list.length, (page + 1) * size) + L(" of ", " de ") + list.length));
        nav.appendChild(h("button", { type: "button", class: "btn sm", disabled: page === 0, onclick: function () { page--; draw(); } }, L("Previous", "Anterior")));
        nav.appendChild(h("button", { type: "button", class: "btn sm", disabled: page >= pages - 1, onclick: function () { page++; draw(); } }, L("Next", "Siguiente")));
      }
    }
    draw();
    box.appendChild(host); box.appendChild(nav);
    return box;
  };
  /** Sortable, paginated table. cols: [{label, cls, render(row) -> node|string, sort(row) -> value}] */
  ui.table = function (cols, rows, opts) {
    opts = opts || {};
    var sortCol = opts.sortCol == null ? -1 : opts.sortCol, dir = opts.dir || 1, wrap = h("div", { class: "stack" }), host = h("div");
    function draw() {
      var list = rows.slice();
      if (sortCol >= 0 && cols[sortCol].sort) {
        var f = cols[sortCol].sort;
        list.sort(function (a, b) { var x = f(a), y = f(b); if (x == null && y == null) return 0; if (x == null) return 1; if (y == null) return -1; return (x < y ? -1 : x > y ? 1 : 0) * dir; });
      }
      host.innerHTML = "";
      host.appendChild(ui.paged(list, opts.pageSize || 50, function (part) {
        var thead = h("tr");
        cols.forEach(function (c, i) {
          var th = h("th", { class: c.cls || "", scope: "col" });
          if (c.sort) {
            var b = h("button", { type: "button", "aria-sort": "none", onclick: function () { if (sortCol === i) dir = -dir; else { sortCol = i; dir = 1; } draw(); } }, c.label);
            if (sortCol === i) b.dataset.dir = dir > 0 ? "asc" : "desc";
            th.appendChild(b);
          } else th.textContent = c.label;
          thead.appendChild(th);
        });
        var tb = h("tbody");
        part.forEach(function (r) {
          var tr = h("tr");
          cols.forEach(function (c) { var v = c.render(r); tr.appendChild(h("td", { class: c.cls || "" }, v == null ? "" : v)); });
          tb.appendChild(tr);
        });
        if (!part.length) tb.appendChild(h("tr", null, h("td", { colspan: cols.length, class: "muted" }, L("Nothing matches.", "Sin resultados."))));
        return h("div", { class: "tbl" + (opts.tall ? " tall" : "") }, h("table", opts.minWidth ? { style: "min-width:" + opts.minWidth + "px" } : null, opts.caption ? h("caption", { class: "sr" }, opts.caption) : null, h("thead", null, thead), tb));
      }));
    }
    draw();
    wrap.appendChild(host);
    return wrap;
  };
  ui.copyBtn = function (getText, label) {
    var b = h("button", { type: "button", class: "btn sm" }, label || L("Copy", "Copiar"));
    b.addEventListener("click", function () {
      var text = getText(), orig = b.textContent;
      function done() { b.textContent = L("Copied", "Copiado"); setTimeout(function () { b.textContent = orig; }, 1400); }
      function fallback() {
        var ta = h("textarea", { readonly: true, "aria-label": L("Text to copy", "Texto para copiar") });
        ta.value = text;
        b.parentNode.insertBefore(ta, b.nextSibling);
        ta.focus(); ta.select();
        b.textContent = L("Select and copy", "Seleccione y copie");
        ta.addEventListener("blur", function () { ta.remove(); b.textContent = orig; });
      }
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, fallback);
        else fallback();
      } catch (e) { fallback(); }
    });
    return b;
  };
  ui.seg = function (options, value, onChange, label) {
    var box = h("div", { class: "seg wrap", role: "group", "aria-label": label || "" });
    options.forEach(function (o) {
      box.appendChild(h("button", { type: "button", "aria-pressed": String(o.v === value), onclick: function () { onChange(o.v); } }, o.l));
    });
    return box;
  };
  ui.tabs = function (tabs, cur, onPick, label) {
    var box = h("div", { class: "tabs", role: "tablist", "aria-label": label || "" });
    tabs.forEach(function (t) {
      box.appendChild(h("button", { type: "button", role: "tab", "aria-selected": String(t.id === cur), onclick: function () { onPick(t.id); } }, t.label));
    });
    return box;
  };
  /** Toggle pills over a set object {key: true}. options: [{v, l, html, n}] */
  ui.pills = function (options, set, onChange, label) {
    var box = h("div", { class: "pills", role: "group", "aria-label": label || "" });
    options.forEach(function (o) {
      var b = h("button", { type: "button", class: "pill " + (o.cls || ""), "aria-pressed": String(!!set[o.v]) });
      b.innerHTML = (o.html || "") + "<span>" + esc(o.l) + "</span>" + (o.n != null ? "<span class='n'>" + o.n + "</span>" : "");
      b.addEventListener("click", function () { set[o.v] = !set[o.v]; b.setAttribute("aria-pressed", String(!!set[o.v])); onChange(); });
      box.appendChild(b);
    });
    return box;
  };
  /** Standard three-voice filter, used in every view. */
  ui.voicePills = function (set, onChange, nodes) {
    var c = {};
    (nodes || []).forEach(function (n) { c[n.graph] = (c[n.graph] || 0) + 1; });
    return ui.pills(UC.VOICES.map(function (v) { return { v: v, l: UC.enumLabel(v), html: UC.voiceGlyph(v), cls: "v-" + v, n: nodes ? (c[v] || 0) : null }; }), set, onChange, L("Voices", "Voces"));
  };
  ui.tierPills = function (set, onChange, nodes) {
    var c = {};
    (nodes || UC.db.assertions).forEach(function (n) { var t = UC.tierOf(n); c[t] = (c[t] || 0) + 1; });
    return ui.pills(UC.TIERS.filter(function (t) { return c[t] || (!nodes && false); }).map(function (t) { return { v: t, l: UC.enumLabel(t), n: nodes ? c[t] : null }; }), set, onChange, L("Source tier", "Nivel de fuente"));
  };
  /** Voice + source-tier (+ confidence) filter block shared by all views. s is the view state. */
  ui.sourceFilters = function (s, onChange, nodes, withConf) {
    UC.filterDefaults(s);
    var out = [ui.ctl(L("Voice", "Voz"), ui.voicePills(s.voices, onChange, nodes)), ui.ctl(L("Source tier", "Nivel de fuente"), ui.tierPills(s.tiers, onChange, nodes))];
    if (withConf) out.push(ui.ctl(L("Reading confidence", "Confianza de lectura"), ui.confPills(s.conf, onChange)));
    return out;
  };
  ui.confPills = function (set, onChange) {
    return ui.pills(["high", "medium", "low"].map(function (c) { return { v: c, l: UC.enumLabel(c) }; }), set, onChange, L("Confidence", "Confianza"));
  };
  ui.ctl = function (label, el) { return h("div", { class: "ctl" }, h("span", { class: "lab" }, label), el); };
  /** Search box with a keyboard-navigable suggestion list. items() -> [{id, label, sub}] */
  ui.autocomplete = function (o) {
    var input = h("input", { type: "search", placeholder: o.placeholder || "", "aria-label": o.placeholder || "", autocomplete: "off", role: "combobox", "aria-expanded": "false", "aria-autocomplete": "list" });
    var list = h("ul", { class: "ac-list", role: "listbox", hidden: true }), box = h("div", { class: "ac" }, input, list), sel = -1, shown = [];
    function norm(s) { return String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
    function close() { list.hidden = true; input.setAttribute("aria-expanded", "false"); sel = -1; }
    function pick(it) { input.value = o.keepText ? it.label : ""; close(); o.onPick(it); }
    function draw() {
      var q = norm(input.value.trim());
      if (o.onInput) o.onInput(input.value);
      if (!q) { close(); return; }
      shown = o.items().filter(function (it) { return norm(it.label + " " + (it.alt || "")).indexOf(q) >= 0; }).slice(0, 12);
      list.innerHTML = "";
      shown.forEach(function (it, i) {
        var li = h("li", { role: "option", "aria-selected": String(i === sel) }, it.label, it.sub ? h("span", null, it.sub) : null);
        li.addEventListener("mousedown", function (e) { e.preventDefault(); pick(it); });
        list.appendChild(li);
      });
      if (!shown.length) list.appendChild(h("li", { class: "muted" }, L("No match", "Sin coincidencias")));
      list.hidden = false; input.setAttribute("aria-expanded", "true");
    }
    input.addEventListener("input", function () { sel = -1; draw(); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { sel = Math.min(shown.length - 1, sel + 1); draw(); e.preventDefault(); }
      else if (e.key === "ArrowUp") { sel = Math.max(0, sel - 1); draw(); e.preventDefault(); }
      else if (e.key === "Enter" && shown.length) { pick(shown[Math.max(0, sel)]); e.preventDefault(); }
      else if (e.key === "Escape") { close(); }
    });
    input.addEventListener("blur", function () { setTimeout(close, 120); });
    box.input = input;
    return box;
  };
  ui.partyItems = function (filter) {
    return UC.db.parties.filter(filter || function () { return true; }).map(function (p) {
      return { id: p["@id"], label: UC.label(p["@id"]), alt: (p.altLabel || []).join(" "), sub: UC.enumLabel(p["@type"][0]) };
    });
  };
  ui.legendVoices = function () {
    var box = h("div", { class: "legend", "aria-label": L("Who asserts", "Quién afirma") });
    UC.ASSERTERS.forEach(function (a) {
      if (a === "Analyst") return;
      var v = a === "Prosecution" ? "prosecution" : a === "Rey" ? "rey" : "press";
      box.appendChild(h("span", { class: "v-" + v, html: "<span style='color:var(--vc);display:inline-flex'>" + UC.glyph(a) + "</span>" + esc(UC.enumLabel(a)) }));
    });
    return box;
  };

  /* ---------- global delegation: clicks, keyboard, tooltips ---------- */
  var tipEl;
  function showTip(html, x, y) {
    tipEl = tipEl || document.getElementById("tip");
    tipEl.innerHTML = html; tipEl.hidden = false;
    var w = tipEl.offsetWidth, hh = tipEl.offsetHeight, vw = window.innerWidth, vh = window.innerHeight;
    tipEl.style.left = Math.max(6, Math.min(vw - w - 6, x + 14)) + "px";
    tipEl.style.top = (y + 18 + hh > vh ? Math.max(6, y - hh - 10) : y + 18) + "px";
  }
  function hideTip() { if (tipEl) tipEl.hidden = true; }
  UC.tip = { show: showTip, hide: hideTip };
  function closest(el, attr) { while (el && el.nodeType === 1) { if (el.hasAttribute(attr)) return el; el = el.parentNode; } return null; }
  document.addEventListener("click", function (e) {
    var p = closest(e.target, "data-prov");
    if (p) { e.preventDefault(); hideTip(); prov.open(p.getAttribute("data-prov")); return; }
    var q = closest(e.target, "data-party");
    if (q) { e.preventDefault(); hideTip(); prov.open(q.getAttribute("data-party")); }
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && prov.isOpen()) { prov.close(); return; }
    if ((e.key === "Enter" || e.key === " ") && e.target && e.target.tagName && e.target.tagName.toLowerCase() !== "button") {
      var p = closest(e.target, "data-prov") || closest(e.target, "data-party");
      if (p && p === e.target) { e.preventDefault(); prov.open(p.getAttribute("data-prov") || p.getAttribute("data-party")); }
    }
  });
  document.addEventListener("mouseover", function (e) {
    var t = closest(e.target, "data-tip");
    if (t) showTip(t.getAttribute("data-tip"), e.clientX, e.clientY); else hideTip();
  });
  document.addEventListener("mousemove", function (e) {
    if (tipEl && !tipEl.hidden && closest(e.target, "data-tip")) showTip(tipEl.innerHTML, e.clientX, e.clientY);
  });
  document.addEventListener("scroll", hideTip, true);
})();
