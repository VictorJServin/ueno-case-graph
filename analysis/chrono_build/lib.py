# Shared helpers for the `chrono` contributor build (sources, events, accused, entities, roles).
import json, os, re

OUT = "/home/claude/ueno-kg/data/raw"
SOURCES, EVENTS, ENTITIES, ROLES, ACCUSED = [], [], [], [], []
_src_ids = set()


def S(id_, kind, outlet, title, date, url, page=None):
    assert id_.startswith("src:") and id_ not in _src_ids, id_
    _src_ids.add(id_)
    SOURCES.append({"id": id_, "kind": kind, "outlet": outlet, "title": title,
                    "date": date, "url": url, "page": page})


def P(by, src, loc="", quote="", conf="high", note=""):
    assert by in ("prosecution", "rey", "defence", "regulator", "rating_agency", "company", "press"), by
    assert src in _src_ids, src
    assert conf in ("high", "medium", "low")
    assert len(quote.split()) <= 12, quote
    return {"asserted_by": by, "source": src, "locator": loc, "quote": quote,
            "confidence": conf, "note": note}


def precision(d):
    return {4: "year", 7: "month", 10: "day"}[len(d)]


def E(date, cat, t_en, t_es, d_en, d_es, parties, prov, amount=None, currency=None):
    assert cat in ("corporate", "credit", "supervisory", "criminal", "political",
                   "market", "statement", "depositor"), cat
    assert re.fullmatch(r"\d{4}(-\d{2}){0,2}", date), date
    assert date <= "2026-11-20", date
    EVENTS.append({"id": None, "date": date,
                   "date_precision": precision(date), "category": cat,
                   "title_en": t_en, "title_es": t_es, "detail_en": d_en, "detail_es": d_es,
                   "parties": parties, "amount": amount, "currency": currency, "prov": prov})


def ENT(id_, type_, label, desc_en, desc_es, prov, aliases=None, business_en="", business_es=""):
    assert type_ in ("Person", "Company", "Authority")
    ENTITIES.append({"id": id_, "type": type_, "label": label, "aliases": aliases or [],
                     "desc_en": desc_en, "desc_es": desc_es,
                     "business_en": business_en, "business_es": business_es, "prov": prov})


def R(holder, org, role, note_en, note_es, prov, pct=None, start=None, end=None):
    ROLES.append({"id": "chrono:role:%04d" % (len(ROLES) + 1), "holder": holder, "org": org,
                  "role": role, "pct": pct, "start": start, "end": end,
                  "note_en": note_en, "note_es": note_es, "prov": prov})


def A(person, label, role_en, role_es, company, offences, measure, measure_date, next_hearing,
      def_en, def_es, prov, **extra):
    row = {"id": "chrono:accused:%04d" % (len(ACCUSED) + 1), "person": person, "label": label,
           "role_reported_en": role_en, "role_reported_es": role_es, "company": company,
           "offences": offences, "measure": measure, "measure_date": measure_date,
           "next_hearing": next_hearing, "defence_statement_en": def_en,
           "defence_statement_es": def_es}
    row.update(extra)
    row["prov"] = prov
    ACCUSED.append(row)


def dump():
    os.makedirs(OUT, exist_ok=True)
    EVENTS.sort(key=lambda r: r["date"])
    for i, r in enumerate(EVENTS, 1):
        r["id"] = "chrono:event:%04d" % i
    for name, rows in (("sources", SOURCES), ("events", EVENTS),
                       ("entities", ENTITIES), ("roles", ROLES), ("accused", ACCUSED)):
        with open(os.path.join(OUT, "chrono.%s.jsonl" % name), "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(name, len(rows))
