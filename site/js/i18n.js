/* i18n.js - language state, enumeration labels and number/date formatting. One IIFE, no dependencies. */
(function () {
  "use strict";
  var UC = window.UC = window.UC || {};
  UC.views = {}; UC.state = {};

  UC.store = {
    get: function (k, d) { try { var v = window.localStorage.getItem("ueno." + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { window.localStorage.setItem("ueno." + k, JSON.stringify(v)); } catch (e) { /* storage not available */ } }
  };

  UC.lang = UC.store.get("lang", "en") === "es" ? "es" : "en";
  /** Pick the string for the current language. */
  UC.L = function (en, es) { return UC.lang === "es" && es != null ? es : en; };
  /** Text from a JSON-LD language map {en, es}; falls back to the other language. */
  UC.tx = function (m) {
    if (m == null) return "";
    if (typeof m === "string") return m;
    var v = m[UC.lang];
    if (v == null) v = UC.lang === "es" ? m.en : m.es;
    if (Array.isArray(v)) return v.join("; ");
    return v == null ? "" : String(v);
  };
  /** Text from analysis JSON, where fields are named base_en / base_es. */
  UC.px = function (o, base) {
    if (!o) return "";
    var v = o[base + "_" + UC.lang];
    if (v == null) v = o[base + "_en"] != null ? o[base + "_en"] : o[base + "_es"];
    return v == null ? "" : v;
  };

  var E = {
    // voices (named graphs)
    prosecution: ["Prosecution record", "Acta fiscal"],
    rey: ["Rey's statement", "Declaración de Rey"],
    press: ["Press and others", "Prensa y otros"],
    analysis: ["AI analysis (estimate)", "Análisis de IA (estimación)"], AnalystOpinion: ["AI analyst estimates", "Estimaciones de analistas de IA"],
    // asserters
    Prosecution: ["Prosecution", "Fiscalía"],
    Rey: ["Rey (suspect's statement)", "Rey (declaración del imputado)"],
    Press: ["Press", "Prensa"],
    Regulator: ["Regulator", "Regulador"],
    RatingAgency: ["Rating agency", "Calificadora"],
    Company: ["Company", "Empresa"],
    Defence: ["Defence", "Defensa"],
    Analyst: ["AI analyst", "Analista de IA"],
    // confidence
    high: ["high", "alta"], medium: ["medium", "media"], low: ["low", "baja"],
    // node types
    Person: ["Person", "Persona"], Organisation: ["Company", "Empresa"], Authority: ["Authority", "Autoridad"], Party: ["Party", "Parte"],
    RoleHolding: ["Roles and stakes", "Cargos y participaciones"], Loan: ["Loans", "Préstamos"], Overdraft: ["Overdrafts", "Sobregiros"],
    Flow: ["Money flows", "Flujos de dinero"], CaseEvent: ["Case events", "Hechos del caso"], FinancialFact: ["Financial figures", "Cifras financieras"],
    Charge: ["Charges", "Imputaciones"], Issue: ["Data issues", "Inconsistencias"], PartyDescription: ["Descriptions", "Descripciones"], Source: ["Sources", "Fuentes"],
    // roles
    role_shareholder: ["shareholder", "accionista"], role_beneficial_owner: ["beneficial owner", "beneficiario final"],
    role_president: ["president", "presidente"], role_vice_president: ["vice-president", "vicepresidente"],
    role_director: ["director", "director"], role_alternate_director: ["alternate director", "director suplente"],
    role_statutory_auditor: ["statutory auditor (síndico)", "síndico"], role_alternate_statutory_auditor: ["alternate statutory auditor", "síndico suplente"],
    role_officer: ["officer", "directivo / funcionario"], role_employee: ["employee", "empleado"], role_founder: ["founder", "fundador"],
    role_legal_representative: ["legal representative", "representante legal"], role_registry_agent: ["agent", "gestor / agente"],
    role_group_role: ["group role", "función en el grupo"], role_related_group_member: ["member of related group", "integrante de grupo vinculado"],
    role_relative_of: ["relative of", "pariente de"], role_controlling_group: ["controlling party", "controlante"], role_charged_person: ["charged in connection with", "imputado en relación con"],
    // instruments
    instr_transfer: ["transfer", "transferencia"], instr_repayment: ["repayment", "pago de préstamo"], instr_bond_purchase: ["bond purchase", "compra de bonos"],
    instr_portfolio_assignment: ["portfolio assignment (non-cash)", "cesión de cartera (no dineraria)"], instr_cash_delivery: ["cash delivery", "entrega de efectivo"],
    instr_other: ["other", "otro"], instr_portfolio_sale_price: ["portfolio sale price", "precio de venta de cartera"], instr_contract: ["contract", "contrato"],
    instr_loan_disbursement: ["loan disbursement", "desembolso de préstamo"], instr_cheque: ["cheque", "cheque"], instr_loan: ["loan between companies", "préstamo entre empresas"],
    // analysis JSON uses the bare codes
    transfer: ["transfer", "transferencia"], repayment: ["repayment", "pago de préstamo"], bond_purchase: ["bond purchase", "compra de bonos"],
    portfolio_assignment: ["portfolio assignment (non-cash)", "cesión de cartera (no dineraria)"], cash_delivery: ["cash delivery", "entrega de efectivo"],
    other: ["other", "otro"], portfolio_sale_price: ["portfolio sale price", "precio de venta de cartera"], contract: ["contract", "contrato"],
    loan_disbursement: ["loan disbursement", "desembolso de préstamo"], cheque: ["cheque", "cheque"], loan: ["loan", "préstamo"], overdraft: ["overdraft", "sobregiro"],
    // event categories
    cat_corporate: ["Corporate", "Societario"], cat_credit: ["Credit", "Crédito"], cat_supervisory: ["Supervisory", "Supervisión"], cat_criminal: ["Criminal", "Penal"],
    cat_political: ["Political", "Político"], cat_market: ["Market", "Mercado"], cat_depositor: ["Depositors", "Depositantes"], cat_statement: ["Statements", "Declaraciones"],
    // source kinds
    record: ["prosecution record", "acta fiscal"], rating: ["rating report", "informe de calificación"], official: ["official document", "documento oficial"], company: ["company document", "documento de la empresa"],
    dossier: ["third-party dossier (no links)", "dossier de terceros (sin enlaces)"], project: ["project label", "rótulo del proyecto"],
    // source tiers
    press_linked: ["linked press or document", "prensa o documento con enlace"], rating_or_official: ["rating report or official", "calificadora u oficial"],
    editorial: ["project label", "rótulo del proyecto"], unlinked: ["no link available", "sin enlace"],
    Correction: ["Editor corrections", "Correcciones del editor"],
    // loan fields
    outstanding: ["outstanding", "vigente"], cancelled: ["cancelled", "cancelado"], none: ["none (signature only)", "ninguna (a sola firma)"],
    mortgage_claimed: ["mortgage claimed", "hipoteca alegada"], "not stated": ["not stated", "no indicada"],
    // procedural measures
    pretrial_prison: ["pre-trial detention", "prisión preventiva"], house_arrest: ["house arrest", "arresto domiciliario"], none_reported: ["none reported", "ninguna reportada"],
    // analysis codes
    well_supported_in_record: ["well supported in the record", "bien respaldado en el acta"], partly_supported: ["partly supported", "parcialmente respaldado"],
    legally_uncertain: ["legally uncertain", "jurídicamente incierto"], thin: ["thin", "débil"],
    strong: ["strong", "fuerte"], arguable: ["arguable", "discutible"], weak: ["weak", "débil"],
    law: ["law", "derecho"], fact: ["fact", "hecho"], evidence: ["evidence", "prueba"], procedure: ["procedure", "procedimiento"],
    computation: ["computation", "cálculo"], opinion: ["opinion", "opinión"]
  };
  var METRICS = {
    debt_to_ueno_bank: ["Debt to Ueno Bank", "Deuda con Ueno Bank"], debt_to_ueno_bank_debtor_list: ["Debt to Ueno Bank (debtor list)", "Deuda con Ueno Bank (lista de deudores)"],
    total_liabilities: ["Total liabilities", "Pasivo total"], equity: ["Equity", "Patrimonio neto"], net_result: ["Net result", "Resultado neto"],
    total_assets: ["Total assets", "Activo total"], revenue: ["Revenue", "Ingresos"], financial_debt: ["Financial debt", "Deuda financiera"], staff: ["Staff", "Personal"],
    share_capital: ["Share capital", "Capital social"], ebitda: ["EBITDA", "EBITDA"], paid_in_capital: ["Paid-in capital", "Capital integrado"],
    average_monthly_income: ["Average monthly income", "Ingreso mensual promedio"], bond_programme_outstanding: ["Bond programme outstanding", "Programa de bonos vigente"],
    bond_capital_maturing: ["Bond capital maturing", "Capital de bonos a vencer"], effective_equity: ["Effective equity", "Patrimonio efectivo"],
    bank_account_balance: ["Bank account balance", "Saldo en cuenta bancaria"], deposits: ["Deposits", "Depósitos"], net_loans: ["Net loans", "Cartera neta"],
    long_term_debt: ["Long-term debt", "Deuda de largo plazo"], customers: ["Customers", "Clientes"]
  };
  /* labels used by the "Missing money" view (codes from missing_money.json) */
  var MM = {
    reported: ["reported", "informado"], computed: ["computed", "calculado"], estimate: ["estimate", "estimación"], assumption: ["assumption", "supuesto"],
    spent: ["spent", "gastado"], circulated: ["circulated back", "recirculado"], held_as_assets: ["held as assets", "convertido en activos"], extracted: ["extracted", "extraído"], unknown: ["fate unknown", "destino desconocido"],
    regulator: ["Regulator", "Regulador"], prosecution: ["Prosecution", "Fiscalía"], rey: ["Rey (his statement)", "Rey (su declaración)"], press: ["Press", "Prensa"], analyst: ["AI analyst", "Analista de IA"],
    rating_agency: ["Rating agency", "Calificadora"], company: ["Company", "Empresa"], defence: ["Defence", "Defensa"],
    low: ["low", "bajo"], central: ["central", "central"], high: ["high", "alto"], medium: ["medium", "media"],
    low_shortfall: ["low shortfall", "faltante bajo"], high_shortfall: ["high shortfall", "faltante alto"],
    start: ["start", "inicio"], deduction: ["deduction", "deducción"], subtotal: ["subtotal", "subtotal"], end: ["result", "resultado"]
  };
  UC.mmLabel = function (code) { var m = MM[code]; return m ? (UC.lang === "es" ? m[1] : m[0]) : String(code == null ? "" : code).replace(/_/g, " "); };
  UC.enumLabel = function (code) {
    if (code == null) return "";
    var e = E[code];
    if (e) return UC.lang === "es" ? e[1] : e[0];
    return String(code).replace(/^(role|instr|cat)_/, "").replace(/_/g, " ");
  };
  UC.metricLabel = function (code) {
    var m = METRICS[code];
    if (m) return UC.lang === "es" ? m[1] : m[0];
    var s = String(code || "").replace(/_/g, " ");
    return s.charAt(0).toUpperCase() + s.slice(1);
  };

  /* ---------- numbers, money, dates: the only place formatting happens ---------- */
  function loc() { return UC.lang === "es" ? "es-PY" : "en-US"; }
  var nfCache = {};
  function nf(min, max) {
    var k = loc() + min + "/" + max;
    if (!nfCache[k]) {
      try { nfCache[k] = new Intl.NumberFormat(loc(), { minimumFractionDigits: min, maximumFractionDigits: max }); }
      catch (e) { nfCache[k] = new Intl.NumberFormat(UC.lang === "es" ? "es" : "en", { minimumFractionDigits: min, maximumFractionDigits: max }); }
    }
    return nfCache[k];
  }
  var MON = { en: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], es: ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"] };
  UC.fmt = {
    /** Plain number. Decimals are kept as given (up to `max`). */
    num: function (v, max, min) {
      if (v == null || v === "") return "";
      var x = Number(v);
      if (!isFinite(x)) return String(v);
      if (max == null) { var s = String(v); var i = s.indexOf("."); max = i < 0 ? 0 : Math.min(4, s.length - i - 1); if (typeof v === "number") max = Math.min(max, 4); }
      return nf(min == null ? 0 : min, max).format(x);
    },
    /** Money with the currency code always shown. Never converts. */
    money: function (v, cur, o) {
      if (v == null || v === "") return UC.L("amount not stated", "monto no indicado");
      var c = cur || UC.L("(currency not stated)", "(moneda no indicada)");
      var s = o && o.compact ? UC.fmt.compact(v) : UC.fmt.num(v);
      return (o && o.approx ? "≈ " : "") + c + " " + s;
    },
    compact: function (v) {
      var x = Number(v), a = Math.abs(x), es = UC.lang === "es";
      if (a >= 1e12) return nf(0, 2).format(x / 1e12) + (es ? " B" : " tn");
      if (a >= 1e9) return nf(0, 2).format(x / 1e9) + (es ? " mil M" : " bn");
      if (a >= 1e6) return nf(0, 1).format(x / 1e6) + " M";
      if (a >= 1e4) return nf(0, 0).format(x / 1e3) + (es ? " mil" : " k");
      return nf(0, 2).format(x);
    },
    pct: function (v) { return UC.fmt.num(v) + "%"; },
    /** ISO date string at a stated precision ('day' | 'month' | 'year'). */
    dateStr: function (iso, precision) {
      if (!iso) return "";
      var y = iso.slice(0, 4), m = +iso.slice(5, 7), d = +iso.slice(8, 10), mon = MON[UC.lang][m - 1] || "";
      if (precision === "year") return y;
      if (precision === "month") return mon + " " + y;
      return d + " " + mon + " " + y;
    },
    /** Date of a graph node, honouring datePrecision; periods and undated rows are spelled out. */
    date: function (n) {
      if (!n) return "";
      if (!n.sortDate) return n.dateText ? n.dateText : UC.L("undated", "sin fecha");
      var p = n.datePrecision || "day";
      var s = UC.fmt.dateStr(n.sortDate, p);
      if (n.sortDateEnd && n.sortDateEnd !== n.sortDate && UC.fmt.dateStr(n.sortDateEnd, p) !== s) s += " – " + UC.fmt.dateStr(n.sortDateEnd, p);
      return s;
    }
  };
})();
