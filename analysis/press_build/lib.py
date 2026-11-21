"""Row builders for the `press` contributor. Each batch module calls these; build.py writes JSONL."""
TAG = "press"
ROWS = {"sources": [], "entities": [], "facts": [], "roles": [], "loans": [], "flows": [], "events": []}
_SRC = {}
_cnt = {}


def _id(kind):
    _cnt[kind] = _cnt.get(kind, 0) + 1
    return f"{TAG}:{kind}:{_cnt[kind]:04d}"


def src(id, kind, outlet, title, date, url, page=None):
    assert id.startswith("src:"), id
    assert kind in ("record", "press", "rating", "official", "company"), kind
    if id in _SRC:
        raise ValueError("duplicate source " + id)
    _SRC[id] = 1
    ROWS["sources"].append({"id": id, "kind": kind, "outlet": outlet, "title": title, "date": date, "url": url, "page": page})
    return id


def P(by, source, loc, quote="", conf="medium", note=""):
    assert by in ("prosecution", "rey", "defence", "regulator", "rating_agency", "company", "press"), by
    assert conf in ("high", "medium", "low"), conf
    assert len(quote.split()) <= 12, quote
    return {"asserted_by": by, "source": source, "locator": loc, "quote": quote, "confidence": conf, "note": note}


def ent(id, type, label, prov, aliases=(), desc_en="", desc_es="", bus_en="", bus_es=""):
    assert type in ("Person", "Company", "Authority")
    ROWS["entities"].append({"id": id, "type": type, "label": label, "aliases": list(aliases), "desc_en": desc_en,
                             "desc_es": desc_es, "business_en": bus_en, "business_es": bus_es, "prov": prov})


def fact(entity, metric, value, currency, unit_note, period, prov):
    ROWS["facts"].append({"id": _id("fact"), "entity": entity, "metric": metric, "value": value, "currency": currency,
                          "unit_note": unit_note, "period": period, "prov": prov})


ROLES = set("shareholder beneficial_owner president vice_president director alternate_director statutory_auditor "
            "alternate_statutory_auditor officer employee founder legal_representative registry_agent group_role "
            "related_group_member relative_of controlling_group charged_person".split())


def role(holder, org, role, prov, pct=None, start=None, end=None, note_en="", note_es=""):
    assert role in ROLES, role
    ROWS["roles"].append({"id": _id("role"), "holder": holder, "org": org, "role": role, "pct": pct, "start": start,
                          "end": end, "note_en": note_en, "note_es": note_es, "prov": prov})


def loan(lender, borrower, prov, op_number=None, kind="loan", date=None, term_years=None, term_days=None,
         rate_pct=None, currency=None, principal=None, outstanding=None, collateral=None, amortisation=None,
         status=None, note_en="", note_es=""):
    assert kind in ("loan", "overdraft")
    rid = _id("loan")
    ROWS["loans"].append({"id": rid, "lender": lender, "borrower": borrower, "op_number": op_number, "kind": kind,
                          "date": date, "term_years": term_years, "term_days": term_days, "rate_pct": rate_pct,
                          "currency": currency, "principal": principal, "outstanding": outstanding,
                          "collateral": collateral, "amortisation": amortisation, "status": status,
                          "note_en": note_en, "note_es": note_es, "prov": prov})
    return rid


INSTR = set("loan_disbursement transfer bond_purchase loan contract repayment portfolio_sale_price "
            "portfolio_assignment cash_delivery cheque other".split())


def _prec(d):
    if d is None:
        return None
    return {4: "year", 7: "month", 10: "day"}[len(d)]


def flow(frm, to, amount, currency, date, instrument, purpose_en, purpose_es, prov, linked_loan=None, approx=False,
         precision=None):
    assert instrument in INSTR, instrument
    assert frm and to, (frm, to)
    ROWS["flows"].append({"id": _id("flow"), "from": frm, "to": to, "amount": amount, "currency": currency,
                          "date": date, "date_precision": precision or _prec(date), "instrument": instrument,
                          "purpose_en": purpose_en, "purpose_es": purpose_es, "linked_loan": linked_loan,
                          "amount_is_approx": approx, "prov": prov})


CATS = set("corporate credit supervisory criminal political market statement depositor".split())


def event(date, category, title_en, title_es, detail_en, detail_es, parties, prov, amount=None, currency=None,
          precision=None):
    assert category in CATS, category
    ROWS["events"].append({"id": _id("event"), "date": date, "date_precision": precision or _prec(date),
                           "category": category, "title_en": title_en, "title_es": title_es, "detail_en": detail_en,
                           "detail_es": detail_es, "parties": list(parties), "amount": amount, "currency": currency,
                           "prov": prov})


M = 1_000_000  # "millones"
