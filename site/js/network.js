/* network.js - force-directed graph of parties on canvas. Every edge is a bundle of assertions
   (roles, loans, flows, kinship); clicking a node or an edge lists them with provenance. */
(function () {
  "use strict";
  var UC = window.UC, h = UC.h, L = UC.L, prov = UC.prov, ui = UC.ui;

  var KINDS = ["own", "office", "group", "kin", "loan", "flow", "case"];
  var KIND_OF_ROLE = {
    role_shareholder: "own", role_beneficial_owner: "own", role_controlling_group: "own", role_founder: "own",
    role_president: "office", role_vice_president: "office", role_director: "office", role_alternate_director: "office", role_statutory_auditor: "office",
    role_alternate_statutory_auditor: "office", role_officer: "office", role_employee: "office", role_legal_representative: "office", role_registry_agent: "office",
    role_group_role: "group", role_related_group_member: "group", role_relative_of: "kin", role_charged_person: "case"
  };
  function kindLabel(k) {
    return { own: L("Ownership and control", "Propiedad y control"), office: L("Office or job", "Cargo o empleo"), group: L("Group tie", "Vínculo de grupo"), kin: L("Kinship (as stated)", "Parentesco (según se afirma)"),
      loan: L("Loan (lender to borrower)", "Préstamo (acreedor a deudor)"), flow: L("Money flow", "Flujo de dinero"), case: L("Charged in connection with", "Imputado en relación con") }[k];
  }
  var STYLE = { own: { tok: "--own", w: 1.4, dash: [] }, office: { tok: "--muted", w: 0.9, dash: [] }, group: { tok: "--grp", w: 1.3, dash: [2, 3] }, kin: { tok: "--kin", w: 1.6, dash: [6, 4] },
    loan: { tok: "--out", w: 2.2, dash: [], arrow: true }, flow: { tok: "--back", w: 1.5, dash: [], arrow: true }, case: { tok: "--bad", w: 1.1, dash: [8, 3, 2, 3] } };

  var G = null; // edges built once per data load

  function build() {
    if (G) return G;
    var db = UC.db, map = {}, edges = [];
    function add(a, b, kind, n) {
      if (!a || !b || a === b || !db.byId[a] || !db.byId[b]) return;
      var k = a + "|" + b + "|" + kind, e = map[k];
      if (!e) { e = map[k] = { id: k, source: a, target: b, kind: kind, items: [] }; edges.push(e); }
      e.items.push(n);
    }
    db.roles.forEach(function (r) { add(r.holder, r.organisation, KIND_OF_ROLE[r.roleType] || "office", r); });
    db.loans.forEach(function (l) { add(l.lender, l.nominalBorrower, "loan", l); });
    db.flows.forEach(function (f) { add(f.fromParty, f.toParty, "flow", f); });
    var borrowers = db.borrowers, multi = {}, seen = {};
    db.roles.forEach(function (r) {
      if (!borrowers[r.organisation] || r.roleType === "role_relative_of" || r.roleType === "role_charged_person") return;
      var p = db.byId[r.holder];
      if (!p || p["@type"][0] !== "Person") return;
      seen[r.holder] = seen[r.holder] || {};
      seen[r.holder][r.organisation] = 1;
    });
    Object.keys(seen).forEach(function (p) { if (Object.keys(seen[p]).length >= 2) multi[p] = Object.keys(seen[p]); });
    var groupOrgs = { "ucr:org/ueno-bank": 1, "ucr:org/grupo-vazquez": 1 };
    db.roles.forEach(function (r) { if (r.roleType === "role_related_group_member" && db.byId[r.holder] && db.byId[r.holder]["@type"][0] !== "Person") groupOrgs[r.holder] = 1; });
    G = { edges: edges, multi: multi, groupOrgs: groupOrgs };
    return G;
  }

  function defaults(s) {
    UC.filterDefaults(s);
    if (s.preset === undefined) s.preset = "borrowers";
    if (!s.kinds) { s.kinds = {}; var pk = s.preset ? PRESETS[s.preset].kinds : { own: true, office: true, group: true, kin: true, loan: true, flow: true }; KINDS.forEach(function (k) { s.kinds[k] = !!pk[k]; }); }
    if (!s.types) s.types = { Person: true, Organisation: true, Authority: true };
    if (!s.depth) s.depth = 1;
    if (s.preset === undefined) s.preset = "borrowers";
    if (!s.pos) s.pos = {};
    return s;
  }
  var PRESETS = {
    borrowers: { kinds: { own: true, loan: true }, test: function (e) { var b = UC.db.borrowers; return e.kind === "loan" ? !!b[e.target] : !!b[e.target]; } },
    board: { kinds: { office: true, group: true }, test: function (e) { return !!G.groupOrgs[e.target] || !!G.groupOrgs[e.source]; } },
    money: { kinds: { loan: true, flow: true }, test: function () { return true; } },
    multi: { kinds: { own: true, office: true, group: true }, test: function (e) { return !!G.multi[e.source] && !!UC.db.borrowers[e.target]; } }
  };
  function presetLabel(p) {
    return { borrowers: L("Borrowers and their owners", "Prestatarias y sus dueños"), board: L("Board and group roles", "Directorio y funciones de grupo"), money: L("Money recipients", "Receptores de dinero"), multi: L("People in two or more borrowers", "Personas en dos o más prestatarias") }[p];
  }
  function typeOf(id) { var t = UC.db.byId[id]["@type"][0]; return t === "Party" ? "Organisation" : t; }

  /** Apply filters, preset and focus. Returns {nodes:[{id,deg}], edges:[{..., shown:[assertions]}]} */
  function visible(s) {
    var g = build(), pr = s.preset ? PRESETS[s.preset] : null, out = [], deg = {};
    g.edges.forEach(function (e) {
      if (!s.kinds[e.kind]) return;
      if (pr && !pr.test(e)) return;
      if (!s.types[typeOf(e.source)] || !s.types[typeOf(e.target)]) return;
      var items = e.items.filter(function (n) { return UC.pass(n, s); });
      if (!items.length) return;
      out.push({ id: e.id, source: e.source, target: e.target, kind: e.kind, shown: items, noAmount: e.kind === "flow" && !items.some(function (n) { return n.amount != null; }) });
    });
    if (s.focus && UC.db.byId[s.focus]) {
      var dist = {}; dist[s.focus] = 0;
      for (var d = 0; d < s.depth; d++) {
        out.forEach(function (e) {
          if (dist[e.source] === d && dist[e.target] == null) dist[e.target] = d + 1;
          if (dist[e.target] === d && dist[e.source] == null) dist[e.source] = d + 1;
        });
      }
      out = out.filter(function (e) { return dist[e.source] != null && dist[e.target] != null && (dist[e.source] < s.depth || dist[e.target] < s.depth); });
    }
    out.forEach(function (e) { deg[e.source] = (deg[e.source] || 0) + 1; deg[e.target] = (deg[e.target] || 0) + 1; });
    if (s.focus && UC.db.byId[s.focus] && deg[s.focus] == null) deg[s.focus] = 0;
    var nodes = Object.keys(deg).map(function (id) { return { id: id, deg: deg[id], type: typeOf(id) }; });
    return { nodes: nodes, edges: out };
  }

  function layout(vis, s, w, hgt) {
    var nodes = vis.nodes.map(function (n, i) {
      var p = s.pos[n.id];
      // deterministic start: cached position, otherwise a sunflower spiral (no randomness)
      var a = i * 2.39996, r = 14 * Math.sqrt(i + 0.5);
      return { id: n.id, deg: n.deg, x: p ? p.x : Math.cos(a) * r, y: p ? p.y : Math.sin(a) * r };
    });
    var idx = {}; nodes.forEach(function (n) { idx[n.id] = n; });
    var pairs = {}, links = [];
    vis.edges.forEach(function (e) { var k = e.source < e.target ? e.source + "|" + e.target : e.target + "|" + e.source; if (!pairs[k]) { pairs[k] = 1; links.push({ source: idx[e.source], target: idx[e.target] }); } });
    var many = nodes.length > 120;
    var sim = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).distance(function (l) { return (many ? 46 : 60) + 9 * Math.sqrt(Math.max(l.source.deg, l.target.deg)); }))
      .force("charge", d3.forceManyBody().strength(function (n) { return -Math.min(2600, (many ? 150 : 260) + 55 * n.deg); }).distanceMax(700))
      .force("collide", d3.forceCollide(function (n) { return radius(n.deg) + (many ? 10 : 16); }))
      .force("x", d3.forceX(0).strength(many ? 0.045 : 0.06)).force("y", d3.forceY(0).strength((many ? 0.045 : 0.06) * Math.max(1, w / Math.max(1, hgt))))
      .stop();
    for (var i = 0; i < 300; i++) sim.tick();
    nodes.forEach(function (n) { s.pos[n.id] = { x: n.x, y: n.y }; });
  }
  function radius(deg) { return Math.min(17, 4.5 + Math.sqrt(deg) * 1.9); }

  UC.views.network = {
    render: function (root, sub, s) {
      defaults(s); build();
      var db = UC.db, vis, tr = d3.zoomIdentity, hover = null, W = 0, H = 0, dpr = Math.max(1, window.devicePixelRatio || 1), colors = {};
      root.appendChild(h("div", { class: "view-head" }, h("h2", null, L("Network of people, companies and authorities", "Red de personas, empresas y autoridades")),
        h("p", null, L("Each line bundles the assertions that connect two parties: who owns, who holds office, who lent, who paid. A line means that some source states the link, not that the link is proven or improper. Select a node or a line to read the assertions and their sources.", "Cada línea agrupa las afirmaciones que conectan a dos partes: quién es dueño, quién ocupa un cargo, quién prestó, quién pagó. Una línea significa que alguna fuente afirma el vínculo, no que esté probado ni que sea indebido. Seleccione un nodo o una línea para leer las afirmaciones y sus fuentes."))));

      var side = h("div", { class: "net-side" }), stage = h("div", { class: "net-stage" }), panel = h("div", { class: "card net-panel", "aria-live": "polite" });
      var canvas = h("canvas", { role: "img", tabindex: "0" }), count = h("div", { class: "net-count" });
      var fitBtn = h("button", { type: "button", class: "btn sm", onclick: function () { fit(true); } }, L("Fit to view", "Ajustar a la vista"));
      var zin = h("button", { type: "button", class: "btn sm icon", "aria-label": L("Zoom in", "Acercar"), onclick: function () { d3.select(canvas).call(zoom.scaleBy, 1.4); } }, "+");
      var zout = h("button", { type: "button", class: "btn sm icon", "aria-label": L("Zoom out", "Alejar"), onclick: function () { d3.select(canvas).call(zoom.scaleBy, 1 / 1.4); } }, "−");
      stage.appendChild(canvas); stage.appendChild(count); stage.appendChild(h("div", { class: "net-tools" }, zout, zin, fitBtn));
      var mid = h("div", { class: "stack" }, stage, legend());
      root.appendChild(h("div", { class: "net" }, side, mid, panel));

      /* ----- controls ----- */
      function refresh(relayout) { compute(relayout); controls(); drawPanel(); }
      function controls() {
        side.innerHTML = "";
        var ac = ui.autocomplete({ placeholder: L("Find a person or company", "Buscar persona o empresa"), items: function () { return ui.partyItems(); }, onPick: function (it) { s.sel = { type: "node", id: it.id }; s.focus = it.id; s.preset = null; KINDS.forEach(function (k) { s.kinds[k] = k !== "case"; }); refresh(true); } });
        side.appendChild(h("div", { class: "card stack" }, h("h3", null, L("Find and focus", "Buscar y enfocar")), ac,
          s.focus ? h("div", { class: "stack" }, h("div", { class: "small" }, L("Focused on ", "Enfocado en "), h("b", null, UC.short(s.focus))),
            h("div", { class: "row" }, ui.seg([{ v: 1, l: L("1 step", "1 paso") }, { v: 2, l: L("2 steps", "2 pasos") }], s.depth, function (v) { s.depth = v; refresh(true); }, L("Depth", "Profundidad")),
              h("button", { type: "button", class: "btn sm", onclick: function () { s.focus = null; refresh(true); } }, L("Clear focus", "Quitar enfoque")))) : h("p", { class: "small muted", style: "margin:0" }, L("Pick a party to see only its direct ties (one or two steps).", "Elija una parte para ver solo sus vínculos directos (uno o dos pasos)."))));
        var pbox = h("div", { class: "stack" });
        Object.keys(PRESETS).concat(["all"]).forEach(function (p) {
          var on = p === "all" ? !s.preset : s.preset === p;
          pbox.appendChild(h("button", { type: "button", class: "btn sm", "aria-pressed": String(on), style: "justify-content:flex-start;text-align:left", onclick: function () {
            s.preset = p === "all" ? null : p; s.focus = null; s.sel = null;
            var k = p === "all" ? { own: true, office: true, group: true, kin: true, loan: true, flow: true } : PRESETS[p].kinds;
            KINDS.forEach(function (x) { s.kinds[x] = !!k[x]; });
            s.pos = {}; refresh(true);
          } }, p === "all" ? L("Everything", "Todo") : presetLabel(p)));
        });
        side.appendChild(h("div", { class: "card stack" }, h("h3", null, L("Presets", "Vistas predefinidas")), pbox));
        var kinds = h("div", { class: "checks" });
        KINDS.forEach(function (k) {
          var n = G.edges.filter(function (e) { return e.kind === k; }).length;
          if (!n) return;
          var cb = h("input", { type: "checkbox" }); cb.checked = !!s.kinds[k];
          cb.addEventListener("change", function () { s.kinds[k] = cb.checked; refresh(true); });
          kinds.appendChild(h("label", null, cb, edgeSample(k), h("span", null, kindLabel(k)), h("span", { class: "n" }, n)));
        });
        var types = h("div", { class: "checks" });
        ["Person", "Organisation", "Authority"].forEach(function (t) {
          var cb = h("input", { type: "checkbox" }); cb.checked = !!s.types[t];
          cb.addEventListener("change", function () { s.types[t] = cb.checked; refresh(true); });
          types.appendChild(h("label", null, cb, nodeSample(t), h("span", null, UC.enumLabel(t))));
        });
        side.appendChild(h("div", { class: "card stack" }, h("h3", null, L("Filters", "Filtros")),
          h("fieldset", null, h("legend", null, L("Voice", "Voz")), ui.voicePills(s.voices, function () { refresh(true); })),
          h("fieldset", null, h("legend", null, L("Source tier", "Nivel de fuente")), ui.tierPills(s.tiers, function () { refresh(true); })),
          h("fieldset", null, h("legend", null, L("Reading confidence", "Confianza de lectura")), ui.confPills(s.conf, function () { refresh(true); })),
          h("fieldset", null, h("legend", null, L("Kind of link", "Tipo de vínculo")), kinds),
          h("fieldset", null, h("legend", null, L("Kind of party", "Tipo de parte")), types)));
      }
      function nodeSample(t) {
        var d = t === "Person" ? "<circle cx='8' cy='8' r='5.5'/>" : t === "Organisation" ? "<rect x='2.5' y='2.5' width='11' height='11' rx='2.5'/>" : "<path d='M8 1.5L14.5 8L8 14.5L1.5 8z'/>";
        return h("span", { html: "<svg width='16' height='16' viewBox='0 0 16 16' aria-hidden='true' fill='none' stroke='currentColor' stroke-width='1.6'>" + d + "</svg>", style: "display:inline-flex" });
      }
      function edgeSample(k) {
        var st = STYLE[k];
        return h("span", { html: "<svg width='26' height='10' viewBox='0 0 26 10' aria-hidden='true'><line x1='1' y1='5' x2='" + (st.arrow ? 19 : 25) + "' y2='5' stroke='var(" + st.tok + ")' stroke-width='" + Math.max(1.6, st.w) + "' stroke-dasharray='" + st.dash.join(" ") + "'/>" + (st.arrow ? "<path d='M18 1.5L25 5L18 8.5z' fill='var(" + st.tok + ")'/>" : "") + "</svg>", style: "display:inline-flex" });
      }
      function legend() {
        var lg = h("div", { class: "legend" });
        ["Person", "Organisation", "Authority"].forEach(function (t) { lg.appendChild(h("span", null, nodeSample(t), UC.enumLabel(t))); });
        lg.appendChild(h("span", null, h("span", { html: "<svg width='16' height='16' viewBox='0 0 16 16' aria-hidden='true'><rect x='2.5' y='2.5' width='11' height='11' rx='2.5' fill='var(--soft)' stroke='var(--out)' stroke-width='2'/></svg>", style: "display:inline-flex" }), L("Borrower of Ueno Bank", "Prestataria de Ueno Bank")));
        KINDS.forEach(function (k) { lg.appendChild(h("span", null, edgeSample(k), kindLabel(k))); });
        lg.appendChild(h("span", null, h("span", { html: "<svg width='26' height='10' viewBox='0 0 26 10' aria-hidden='true'><line x1='1' y1='5' x2='25' y2='5' stroke='var(--back)' stroke-width='1.2' stroke-dasharray='3 3'/></svg>", style: "display:inline-flex" }), L("Flow with no stated amount", "Flujo sin monto indicado")));
        return h("div", { class: "fig" }, lg, h("p", { class: "small muted", style: "margin:6px 0 0;max-width:none" }, L("Node size grows with the number of visible links. Drag to pan, scroll or pinch to zoom. The graph has no shared-address or shared-operator assertions; kinship appears only where the record states it.", "El tamaño del nodo crece con el número de vínculos visibles. Arrastre para mover; use la rueda o pellizque para acercar. El grafo no contiene afirmaciones de domicilio u operador compartido; el parentesco aparece solo donde el acta lo afirma.")));
      }

      /* ----- compute + draw ----- */
      var nodeById = {}, adj = {};
      function compute(relayout) {
        vis = visible(s);
        if (relayout || vis.nodes.some(function (n) { return !s.pos[n.id]; })) layout(vis, s, W || 900, H || 600);
        nodeById = {}; adj = {};
        vis.nodes.forEach(function (n) { n.x = s.pos[n.id].x; n.y = s.pos[n.id].y; n.r = radius(n.deg); nodeById[n.id] = n; });
        var pairCount = {};
        vis.edges.forEach(function (e) {
          e.s = nodeById[e.source]; e.t = nodeById[e.target];
          var k = e.source < e.target ? e.source + "|" + e.target : e.target + "|" + e.source;
          e.slot = pairCount[k] = (pairCount[k] || 0) + 1; e.pair = k;
          (adj[e.source] = adj[e.source] || {})[e.target] = 1; (adj[e.target] = adj[e.target] || {})[e.source] = 1;
        });
        vis.edges.forEach(function (e) { e.of = pairCount[e.pair]; });
        if (s.sel && s.sel.type === "node" && !nodeById[s.sel.id]) { /* keep panel, node hidden by filters */ }
        if (s.sel && s.sel.type === "edge" && !vis.edges.some(function (e) { return e.id === s.sel.id; })) s.sel = null;
        var asserts = 0; vis.edges.forEach(function (e) { asserts += e.shown.length; });
        count.textContent = vis.nodes.length + L(" parties · ", " partes · ") + vis.edges.length + L(" links · ", " vínculos · ") + asserts + L(" assertions", " afirmaciones");
        canvas.setAttribute("aria-label", L("Network graph: ", "Grafo de red: ") + count.textContent + L(". Use the search box and the side panel to explore it by keyboard.", ". Use el buscador y el panel lateral para explorarlo con teclado."));
        if (relayout) fit(false); else draw();
      }
      function size() {
        var r = stage.getBoundingClientRect();
        W = Math.max(200, r.width); H = Math.max(200, r.height);
        canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      }
      function fit(animate) {
        if (!vis || !vis.nodes.length) { draw(); return; }
        var x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
        vis.nodes.forEach(function (n) { x0 = Math.min(x0, n.x - 30); x1 = Math.max(x1, n.x + 30); y0 = Math.min(y0, n.y - 20); y1 = Math.max(y1, n.y + 34); });
        var k = Math.min(2.2, 0.94 * Math.min(W / Math.max(1, x1 - x0), H / Math.max(1, y1 - y0)));
        var t = d3.zoomIdentity.translate(W / 2 - k * (x0 + x1) / 2, H / 2 - k * (y0 + y1) / 2).scale(k);
        d3.select(canvas).call(zoom.transform, t);
      }
      function readColors() {
        ["--card", "--ink", "--muted", "--rule", "--soft", "--out", "--back", "--own", "--kin", "--grp", "--bad", "--paper", "--focus", "--rule-strong"].forEach(function (t) { colors[t] = UC.token(t); });
      }
      function ends(e) {
        var dx = e.t.x - e.s.x, dy = e.t.y - e.s.y, len = Math.sqrt(dx * dx + dy * dy) || 1, off = (e.slot - (e.of + 1) / 2) * 5 / Math.max(0.6, tr.k);
        var nx = -dy / len * off, ny = dx / len * off;
        return { x1: e.s.x + nx, y1: e.s.y + ny, x2: e.t.x + nx, y2: e.t.y + ny, ux: dx / len, uy: dy / len, len: len };
      }
      function draw() {
        if (!vis) return;
        var ctx = canvas.getContext("2d"), selNode = s.sel && s.sel.type === "node" ? s.sel.id : null, selEdge = s.sel && s.sel.type === "edge" ? s.sel.id : null;
        var hi = hover && hover.type === "node" ? hover.id : selNode;
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        ctx.clearRect(0, 0, W, H);
        ctx.save(); ctx.translate(tr.x, tr.y); ctx.scale(tr.k, tr.k);
        var ik = 1 / tr.k;
        vis.edges.forEach(function (e) {
          var st = STYLE[e.kind], p = ends(e), hot = e.id === selEdge || (hover && hover.type === "edge" && hover.id === e.id) || (hi && (e.source === hi || e.target === hi));
          ctx.globalAlpha = hi || selEdge ? (hot ? 1 : 0.12) : 0.62;
          ctx.strokeStyle = colors[st.tok]; ctx.fillStyle = colors[st.tok];
          ctx.lineWidth = (st.w + (hot ? 1.2 : 0)) * ik * Math.min(1.6, Math.max(1, Math.sqrt(tr.k)));
          ctx.setLineDash((e.noAmount ? [3, 3] : st.dash).map(function (d) { return d * ik; }));
          var ex = p.x2 - p.ux * (e.t.r + (st.arrow ? 5 * ik : 0)), ey = p.y2 - p.uy * (e.t.r + (st.arrow ? 5 * ik : 0));
          ctx.beginPath(); ctx.moveTo(p.x1 + p.ux * e.s.r, p.y1 + p.uy * e.s.r); ctx.lineTo(ex, ey); ctx.stroke();
          if (st.arrow && p.len > e.s.r + e.t.r + 8) {
            var a = 6.5 * ik, tx = p.x2 - p.ux * e.t.r, ty = p.y2 - p.uy * e.t.r;
            ctx.setLineDash([]); ctx.beginPath(); ctx.moveTo(tx, ty); ctx.lineTo(tx - p.ux * a * 1.5 - p.uy * a * 0.6, ty - p.uy * a * 1.5 + p.ux * a * 0.6); ctx.lineTo(tx - p.ux * a * 1.5 + p.uy * a * 0.6, ty - p.uy * a * 1.5 - p.ux * a * 0.6); ctx.closePath(); ctx.fill();
          }
        });
        ctx.setLineDash([]);
        vis.nodes.forEach(function (n) {
          var p = UC.db.byId[n.id], isB = !!UC.db.borrowers[n.id], sel = n.id === selNode, near = hi && (n.id === hi || (adj[hi] && adj[hi][n.id]));
          ctx.globalAlpha = hi && !near ? 0.25 : 1;
          ctx.fillStyle = isB ? colors["--soft"] : colors["--card"];
          ctx.strokeStyle = sel ? colors["--focus"] : isB ? colors["--out"] : n.id === "ucr:org/ueno-bank" ? colors["--ink"] : colors["--own"];
          ctx.lineWidth = (sel ? 3.2 : isB || n.id === "ucr:org/ueno-bank" ? 2.2 : 1.4) * Math.max(ik, 0.6);
          if (p.isStub) ctx.setLineDash([3 * ik, 2 * ik]);
          ctx.beginPath();
          if (n.type === "Person") ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
          else if (n.type === "Authority") { var q = n.r * 1.25; ctx.moveTo(n.x, n.y - q); ctx.lineTo(n.x + q, n.y); ctx.lineTo(n.x, n.y + q); ctx.lineTo(n.x - q, n.y); ctx.closePath(); }
          else { var r = n.r, c = Math.min(4, r / 2); roundRect(ctx, n.x - r, n.y - r, 2 * r, 2 * r, c); }
          ctx.fill(); ctx.stroke(); ctx.setLineDash([]);
        });
        ctx.restore();
        /* labels in screen space with greedy collision avoidance */
        ctx.globalAlpha = 1;
        var order = vis.nodes.slice().sort(function (a, b) { return pri(b) - pri(a); }), boxes = [], fs = 12;
        function pri(n) { return (n.id === selNode ? 1e6 : 0) + (hover && hover.id === n.id ? 5e5 : 0) + (hi && adj[hi] && adj[hi][n.id] ? 1e4 : 0) + n.deg; }
        ctx.font = "500 " + fs + "px " + (getComputedStyle(document.body).fontFamily || "sans-serif");
        ctx.textAlign = "center"; ctx.textBaseline = "top";
        var limit = tr.k < 0.5 ? 18 : tr.k < 0.8 ? 45 : 400;
        order.forEach(function (n, i) {
          var forced = pri(n) >= 1e4;
          if (!forced && (i > limit || (hi && true))) { if (!forced && hi) return; if (i > limit) return; }
          var sx = n.x * tr.k + tr.x, sy = n.y * tr.k + tr.y + n.r * tr.k + 3;
          if (sx < -60 || sx > W + 60 || sy < -20 || sy > H + 20) return;
          var text = UC.short(n.id); if (text.length > 28) text = text.slice(0, 26) + "…";
          var w = ctx.measureText(text).width + 6, b = { x: sx - w / 2, y: sy, w: w, h: fs + 3 };
          if (!forced) for (var j = 0; j < boxes.length; j++) { var o = boxes[j]; if (b.x < o.x + o.w && b.x + b.w > o.x && b.y < o.y + o.h && b.y + b.h > o.y) return; }
          boxes.push(b);
          ctx.fillStyle = colors["--card"]; ctx.globalAlpha = 0.82; ctx.fillRect(b.x, b.y, b.w, b.h);
          ctx.globalAlpha = 1; ctx.fillStyle = colors["--ink"]; ctx.fillText(text, sx, sy + 1);
        });
      }
      function roundRect(ctx, x, y, w, hh, r) { ctx.moveTo(x + r, y); ctx.lineTo(x + w - r, y); ctx.quadraticCurveTo(x + w, y, x + w, y + r); ctx.lineTo(x + w, y + hh - r); ctx.quadraticCurveTo(x + w, y + hh, x + w - r, y + hh); ctx.lineTo(x + r, y + hh); ctx.quadraticCurveTo(x, y + hh, x, y + hh - r); ctx.lineTo(x, y + r); ctx.quadraticCurveTo(x, y, x + r, y); ctx.closePath(); }

      function pick(ev) {
        var r = canvas.getBoundingClientRect(), x = (ev.clientX - r.left - tr.x) / tr.k, y = (ev.clientY - r.top - tr.y) / tr.k, best = null, bd = Infinity;
        vis.nodes.forEach(function (n) { var d = Math.hypot(n.x - x, n.y - y) - n.r; if (d < 6 / tr.k && d < bd) { bd = d; best = { type: "node", id: n.id }; } });
        if (best) return best;
        bd = 6 / tr.k;
        vis.edges.forEach(function (e) {
          var p = ends(e), t = Math.max(0, Math.min(1, ((x - p.x1) * (p.x2 - p.x1) + (y - p.y1) * (p.y2 - p.y1)) / (p.len * p.len)));
          var d = Math.hypot(x - (p.x1 + t * (p.x2 - p.x1)), y - (p.y1 + t * (p.y2 - p.y1)));
          if (d < bd) { bd = d; best = { type: "edge", id: e.id }; }
        });
        return best;
      }
      var zoom = d3.zoom().scaleExtent([0.15, 6]).on("zoom", function (ev) { tr = ev.transform; draw(); });
      d3.select(canvas).call(zoom).on("dblclick.zoom", null);
      canvas.addEventListener("mousemove", function (ev) {
        var p = pick(ev), changed = (p && p.id) !== (hover && hover.id);
        hover = p; canvas.style.cursor = p ? "pointer" : "grab";
        if (p) {
          var html;
          if (p.type === "node") html = "<b>" + UC.esc(UC.label(p.id)) + "</b><span class='t2'>" + UC.esc(UC.enumLabel(UC.db.byId[p.id]["@type"][0])) + " · " + nodeById[p.id].deg + UC.esc(L(" visible links", " vínculos visibles")) + "</span>";
          else { var e = vis.edges.filter(function (x) { return x.id === p.id; })[0]; html = "<b>" + UC.esc(UC.short(e.source) + (STYLE[e.kind].arrow ? " → " : " — ") + UC.short(e.target)) + "</b><span class='t2'>" + UC.esc(kindLabel(e.kind)) + " · " + e.shown.length + UC.esc(L(" assertions", " afirmaciones")) + "</span>"; }
          UC.tip.show(html, ev.clientX, ev.clientY);
        } else UC.tip.hide();
        if (changed) draw();
      });
      canvas.addEventListener("mouseleave", function () { hover = null; UC.tip.hide(); draw(); });
      canvas.addEventListener("click", function (ev) { var p = pick(ev); s.sel = p; drawPanel(); draw(); });

      /* ----- side panel ----- */
      function drawPanel() {
        panel.innerHTML = "";
        if (!s.sel) {
          panel.appendChild(h("h3", null, L("Nothing selected", "Nada seleccionado")));
          panel.appendChild(h("p", { class: "small muted" }, L("Select a node to read every assertion about that party, or a line to read the assertions behind the link. Each row opens its provenance.", "Seleccione un nodo para leer todas las afirmaciones sobre esa parte, o una línea para leer las afirmaciones detrás del vínculo. Cada fila abre su procedencia.")));
          var top = vis.nodes.slice().sort(function (a, b) { return b.deg - a.deg; }).slice(0, 14), tb = h("div", { class: "row" });
          top.forEach(function (n) { tb.appendChild(h("button", { type: "button", class: "chip party", onclick: function () { s.sel = { type: "node", id: n.id }; drawPanel(); draw(); } }, UC.short(n.id))); });
          panel.appendChild(h("h4", null, L("Most connected in this view", "Más conectados en esta vista"))); panel.appendChild(tb);
          return;
        }
        if (s.sel.type === "edge") {
          var e = vis.edges.filter(function (x) { return x.id === s.sel.id; })[0];
          if (!e) { s.sel = null; return drawPanel(); }
          panel.appendChild(h("div", { class: "eyebrow" }, kindLabel(e.kind)));
          panel.appendChild(h("h3", { style: "font-size:17px" }, UC.label(e.source) + (STYLE[e.kind].arrow ? " → " : " — ") + UC.label(e.target)));
          panel.appendChild(h("div", { class: "row", style: "margin:6px 0" }, ui.party(e.source), ui.party(e.target)));
          panel.appendChild(ui.voiceCount(e.shown));
          if (e.kind === "flow" || e.kind === "loan") panel.appendChild(h("p", { class: "small muted", style: "margin:6px 0 0" }, L("Rows that report the same operation are folded into one item. Amounts are not added.", "Las filas que informan la misma operación se pliegan en un ítem. Los montos no se suman.")));
          panel.appendChild(ui.paged(e.shown.slice().sort(UC.byDate), 30, function (part) { return ui.alist(part); }));
          return;
        }
        var id = s.sel.id, p = db.byId[id], claims = (db.byParty[id] || []).filter(function (n) { return n["@type"][0] !== "PartyDescription"; });
        panel.appendChild(h("div", { class: "eyebrow" }, UC.enumLabel(p["@type"][0]) + (db.borrowers[id] ? " · " + L("borrower of Ueno Bank", "prestataria de Ueno Bank") : "")));
        panel.appendChild(h("h3", { style: "font-size:18px;font-family:var(--display)" }, UC.label(id)));
        if (p.business) panel.appendChild(h("p", { class: "small", style: "margin:4px 0" }, UC.tx(p.business)));
        if (p.description) panel.appendChild(h("p", { class: "small", style: "margin:4px 0" }, UC.tx(p.description)));
        var ds = db.descOf[id] || [];
        if (ds.length) { var sb = h("div", { class: "row small muted" }, L("Described by:", "Descrito por:")); ds.forEach(function (d) { sb.appendChild(prov.src(d)); }); panel.appendChild(sb); }
        panel.appendChild(h("div", { class: "row", style: "margin:8px 0" },
          h("button", { type: "button", class: "btn sm", "aria-pressed": String(s.focus === id), onclick: function () { s.focus = s.focus === id ? null : id; if (s.focus) { s.preset = null; KINDS.forEach(function (k) { s.kinds[k] = k !== "case"; }); } refresh(true); } }, L("Focus on its ties", "Enfocar sus vínculos")),
          h("button", { type: "button", class: "btn sm", onclick: function () { UC.go("people", { sel: id }); } }, L("Full profile", "Ficha completa"))));
        var nb = Object.keys(adj[id] || {});
        if (nb.length) {
          var box = h("div", { class: "row" });
          nb.sort(function (a, b) { return UC.short(a).localeCompare(UC.short(b)); }).forEach(function (o) { box.appendChild(h("button", { type: "button", class: "chip party", onclick: function () { s.sel = { type: "node", id: o }; drawPanel(); draw(); } }, UC.short(o))); });
          panel.appendChild(h("h4", { style: "margin-top:6px" }, L("Linked in this view", "Vinculados en esta vista") + " (" + nb.length + ")")); panel.appendChild(box);
        }
        panel.appendChild(h("h4", { style: "margin-top:10px" }, L("Every assertion about this party", "Todas las afirmaciones sobre esta parte") + " (" + claims.length + ")"));
        panel.appendChild(ui.voiceCount(claims));
        panel.appendChild(ui.agroups(claims, { openFirst: false }));
      }

      readColors(); size(); controls(); compute(true); drawPanel();
      var ro = null, onResize = UC.debounce(function () { size(); draw(); }, 80);
      if (window.ResizeObserver) { ro = new ResizeObserver(onResize); ro.observe(stage); } else window.addEventListener("resize", onResize);
      UC.onLeave = function () { if (ro) ro.disconnect(); else window.removeEventListener("resize", onResize); UC.tip.hide(); };
    }
  };
})();
