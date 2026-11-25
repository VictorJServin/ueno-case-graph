/* app.js - shell: hash router, navigation, language and theme switches, persistent notice, load/error states. */
(function () {
  "use strict";
  var UC = window.UC, h = UC.h, L = UC.L;
  UC.views = UC.views || {};
  UC.state = UC.state || {};

  var ORDER = ["overview", "payouts", "missing", "network", "flows", "timeline", "people", "analysis", "data"];
  var NAV = {
    overview: ["Overview", "Resumen"], payouts: ["Depositor payouts", "Pagos a ahorristas"], missing: ["Missing money", "El dinero faltante"], network: ["Network", "Red"], flows: ["Money flows", "Flujos de dinero"], timeline: ["Timelines", "Cronologías"],
    people: ["People and companies", "Personas y empresas"], analysis: ["Analysis", "Análisis"], data: ["Data and ontology", "Datos y ontología"]
  };
  var loaded = false, cur = { view: null, sub: null };

  function parseHash() {
    var raw = (location.hash || "").replace(/^#/, "").toLowerCase().replace(/[^a-z0-9-]/g, "");
    var i = raw.indexOf("-"), view = i < 0 ? raw : raw.slice(0, i), sub = i < 0 ? null : raw.slice(i + 1);
    if (ORDER.indexOf(view) < 0) { view = "overview"; sub = null; }
    return { view: view, sub: sub };
  }
  /** Navigate to a view, optionally patching its remembered state first. */
  UC.go = function (view, patch, sub) {
    UC.state[view] = UC.state[view] || {};
    if (patch) for (var k in patch) UC.state[view][k] = patch[k];
    var target = "#" + view + (sub ? "-" + sub : "");
    if (location.hash === target) render(true); else location.hash = target;
  };
  /** Change only the sub-route of the current view without re-rendering (keeps links shareable). */
  UC.setSub = function (view, sub) {
    var target = "#" + view + (sub ? "-" + sub : "");
    if (location.hash !== target) { cur.sub = sub; try { history.replaceState(null, "", target); } catch (e) { /* sandboxed */ } }
  };
  UC.rerender = function () { render(true); };

  function chrome() {
    document.documentElement.lang = UC.lang;
    var nav = document.getElementById("nav");
    nav.innerHTML = "";
    nav.setAttribute("aria-label", L("Views", "Vistas"));
    ORDER.forEach(function (v) {
      if (v === "missing" && loaded && !(UC.db && UC.db.extra.missing)) return;
      if (v === "payouts" && loaded && !(UC.db && UC.db.extra.payouts)) return; // optional view: no data, no nav entry
      nav.appendChild(h("a", { href: "#" + v, "aria-current": cur.view === v ? "page" : null }, L(NAV[v][0], NAV[v][1])));
    });
    Array.prototype.forEach.call(document.querySelectorAll("#lang button"), function (b) { b.setAttribute("aria-pressed", String(b.dataset.lang === UC.lang)); });
    document.querySelector("[data-i='brand.eyebrow']").textContent = L("Case 89/2026 · Paraguay", "Causa 89/2026 · Paraguay");
    document.querySelector("[data-i='brand.title']").textContent = L("Ueno Bank case file", "Expediente Ueno Bank");
    document.querySelector(".skip").textContent = L("Skip to content", "Saltar al contenido");
    var th = UC.store.get("theme", "auto");
    document.getElementById("theme-l").textContent = th === "auto" ? L("Auto", "Auto") : th === "dark" ? L("Dark", "Oscuro") : L("Light", "Claro");
    document.getElementById("theme").setAttribute("aria-label", L("Colour theme: ", "Tema de color: ") + th);
    document.getElementById("notice-short").innerHTML = L(
      "<b>Allegations and statements, not findings.</b> <span class='notice-rest'>Nobody named here has been convicted; everyone is presumed innocent. Being listed as an officer or shareholder is not an accusation. Analysis sections are by AI analysts, not advice.</span><span class='notice-min'>No one is convicted; all presumed innocent.</span>",
      "<b>Imputaciones y declaraciones, no hechos probados.</b> <span class='notice-rest'>Nadie de los nombrados ha sido condenado; rige la presunción de inocencia. Figurar como directivo o accionista no es una acusación. Los análisis son de analistas de IA y no constituyen asesoramiento.</span><span class='notice-min'>Nadie está condenado; rige la presunción de inocencia.</span>");
    var more = document.getElementById("notice-more"), full = document.getElementById("notice-full");
    more.textContent = full.hidden ? L("How to read this", "Cómo leer esto") : L("Hide", "Ocultar");
    full.innerHTML = "";
    [
      L("Every figure, link, event and claim on this site is one of three things: an allegation in the prosecution record of Case 89/2026 (pages 1 to 19, which summarise the bank supervisor), a statement made by the suspect Julio Rey in that same record (pages 19 to 24), or a report by the press, the regulator, a rating agency, a company or the defence. The three are never merged, and each item is one click from its source.",
        "Cada cifra, vínculo, hecho y afirmación de este sitio es una de tres cosas: una imputación del acta fiscal de la Causa 89/2026 (páginas 1 a 19, que resumen al supervisor bancario), una declaración del imputado Julio Rey en esa misma acta (páginas 19 a 24), o un informe de prensa, del regulador, de una calificadora, de una empresa o de la defensa. Las tres voces nunca se mezclan y cada dato está a un clic de su fuente."),
      L("The record is an authentic primary document that the press has not seen in full. Where the press does not repeat something from the record, that is not a reason to doubt it; where the two differ, both are shown.",
        "El acta es un documento primario auténtico que la prensa no ha visto completo. Que la prensa no repita algo del acta no es motivo para dudarlo; cuando difieren, se muestran ambas versiones."),
      L("Amounts are shown as each source gives them, in guaraníes (PYG) or US dollars (USD), never converted and never added across sources. Several rows that describe the same operation are shown as alternative reports of one item.",
        "Los montos se muestran como los da cada fuente, en guaraníes (PYG) o dólares (USD), sin convertir y sin sumar entre fuentes. Varias filas que describen la misma operación se muestran como informes alternativos de un solo ítem."),
      L("The Analysis section is written by AI analysts, not by licensed lawyers or accountants. It is not legal or financial advice.",
        "La sección Análisis fue escrita por analistas de IA, no por abogados ni contadores matriculados. No constituye asesoramiento jurídico ni financiero.")
    ].forEach(function (t) { full.appendChild(h("p", null, t)); });
    document.getElementById("foot").innerHTML = "";
    document.getElementById("foot").appendChild(h("p", null, L(
      "Sources: Acta de Declaración Indagatoria of Julio Daniel Rey Fernández, Case 89/2026 (24 pages, 4 November 2026), and public reporting up to 25 November 2026, each cited on the item it supports. Personal identifiers that appear in the original record (ID numbers, addresses, dates of birth) are not part of the data. The scanned pages are not published.",
      "Fuentes: Acta de Declaración Indagatoria de Julio Daniel Rey Fernández, Causa 89/2026 (24 páginas, 4 de noviembre de 2026), e información pública hasta el 25 de noviembre de 2026, citada en cada dato. Los datos personales del acta original (cédulas, domicilios, fechas de nacimiento) no forman parte de los datos. Las páginas escaneadas no se publican.")));
  }

  function render(force) {
    var r = parseHash();
    if (!loaded) { cur = r; chrome(); return; }
    var same = r.view === cur.view && r.sub === cur.sub;
    if (same && !force) return;
    var switching = r.view !== cur.view;
    cur = r;
    chrome();
    var host = document.getElementById("view"), v = UC.views[r.view];
    if (UC.onLeave) { try { UC.onLeave(); } catch (e) { /* ignore */ } UC.onLeave = null; }
    host.innerHTML = "";
    host.hidden = false;
    document.title = L(NAV[r.view][0], NAV[r.view][1]) + " · " + L("Ueno Bank case file", "Expediente Ueno Bank");
    UC.state[r.view] = UC.state[r.view] || {};
    var root = h("div", { class: "view view-" + r.view });
    host.appendChild(root);
    try { v.render(root, r.sub, UC.state[r.view]); }
    catch (e) {
      root.appendChild(h("div", { class: "state err" }, h("h2", null, L("This view could not be drawn", "No se pudo dibujar esta vista")), h("pre", null, String(e && e.stack || e))));
      if (window.console) console.error(e);
    }
    if (switching) { window.scrollTo(0, 0); }
  }

  function applyTheme() {
    var th = UC.store.get("theme", "auto");
    if (th === "auto") document.documentElement.removeAttribute("data-theme"); else document.documentElement.setAttribute("data-theme", th);
  }

  function boot() {
    applyTheme();
    chrome();
    document.getElementById("lang").addEventListener("click", function (e) {
      var b = e.target.closest("button[data-lang]");
      if (!b || b.dataset.lang === UC.lang) return;
      UC.lang = b.dataset.lang; UC.store.set("lang", UC.lang);
      if (loaded) { render(true); UC.prov.refresh(); } else { chrome(); document.getElementById("state-msg").textContent = L("Loading the case graph…", "Cargando el grafo del caso…"); }
    });
    document.getElementById("theme").addEventListener("click", function () {
      var th = UC.store.get("theme", "auto"), next = th === "auto" ? "dark" : th === "dark" ? "light" : "auto";
      UC.store.set("theme", next); applyTheme();
      if (loaded) render(true); else chrome();
    });
    document.getElementById("notice-more").addEventListener("click", function () {
      var full = document.getElementById("notice-full");
      full.hidden = !full.hidden;
      this.setAttribute("aria-expanded", String(!full.hidden));
      this.textContent = full.hidden ? L("How to read this", "Cómo leer esto") : L("Hide", "Ocultar");
    });
    if (window.matchMedia) {
      var mq = window.matchMedia("(prefers-color-scheme: dark)"), onMq = function () { if (loaded && UC.store.get("theme", "auto") === "auto") render(true); };
      if (mq.addEventListener) mq.addEventListener("change", onMq); else if (mq.addListener) mq.addListener(onMq);
    }
    window.addEventListener("hashchange", function () { render(false); });
    document.getElementById("state-msg").textContent = L("Loading the case graph…", "Cargando el grafo del caso…");
    UC.load().then(function () {
      loaded = true;
      document.getElementById("state").hidden = true;
      cur = { view: null, sub: null };
      render(true);
    }).catch(function (e) {
      var st = document.getElementById("state");
      st.className = "state err";
      st.innerHTML = "";
      st.appendChild(h("h2", null, L("The data could not be loaded", "No se pudieron cargar los datos")));
      st.appendChild(h("p", null, L("The page needs data/graph.jsonld and data/stats.json next to index.html. Nothing is shown rather than showing partial data.", "La página necesita data/graph.jsonld y data/stats.json junto a index.html. No se muestra nada antes que mostrar datos parciales.")));
      st.appendChild(h("pre", null, String(e && e.message || e)));
      if (window.console) console.error(e);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
