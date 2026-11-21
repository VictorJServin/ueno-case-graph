#!/usr/bin/env python3
"""Validate the source rows in data/raw/*.jsonl before they enter the graph.

Usage:  python3 tools/validate_rows.py [--strict TAG ...]
Exit code 1 if any ERROR is found. --strict applies the rules for automated
writers (every non-record source must carry a full http(s) link) to the given
contributor tags, e.g. --strict bot.
"""
import glob, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.environ.get("UENO_RAW") or os.path.join(ROOT, "data", "raw")
ASSERTERS = {"prosecution", "rey", "defence", "regulator", "rating_agency", "company", "press", "analyst"}
CONF = {"high", "medium", "low"}
CUR = {"PYG", "USD", "", None}
PROV_KEYS = ["asserted_by", "source", "locator", "quote", "confidence"]
REQUIRED = {
    "sources": ["id", "kind", "outlet", "title", "date"],
    "entities": ["id", "type", "label"],
    "roles": ["id", "holder", "org", "role"],
    "loans": ["id", "lender", "borrower", "kind"],
    "flows": ["id", "from", "to", "instrument"],
    "events": ["id", "date", "category", "title_en", "title_es"],
    "facts": ["id", "entity", "metric", "value"],
    "issues": ["id", "where", "issue_en", "issue_es"],
    "accused": ["id", "person", "label"],
    "opinions": ["id", "kind", "title_en", "title_es"],
}
NO_PROV = {"sources", "verified", "entity_merges"}
ENTITY_FIELDS = {"roles": ["holder", "org"], "loans": ["lender", "borrower"], "flows": ["from", "to"],
                 "facts": ["entity"], "accused": ["person"]}
_onto = open(os.path.join(ROOT, "data", "ontology.ttl"), encoding="utf-8").read()
VOCAB = {("events", "category"): set(re.findall(r"^uc:cat_([a-z0-9_]+)", _onto, re.M)),
         ("flows", "instrument"): set(re.findall(r"^uc:instr_([a-z0-9_]+)", _onto, re.M)),
         ("roles", "role"): set(re.findall(r"^uc:role_([a-z0-9_]+)", _onto, re.M))}
DATE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")
ID = re.compile(r"^(org|person|auth):[a-z0-9]+(-[a-z0-9]+)*$")
# things that must never be stored about a person
PII = [(re.compile(r"(?i)\b(c\.\s?i\.|cédula|cedula|c\.i\.c\.)\s*(n[°ºo.]*)?\s*:?\s*\d[\d.]{5,}"), "ID-card number"),
       (re.compile(r"(?i)\b(domicilio|domiciliad[oa]|home address)\b"), "home-address wording"),
       (re.compile(r"(?i)\b(fecha de nacimiento|date of birth|nacid[oa] el)\b"), "date-of-birth wording")]

def main():
    strict = set()
    a = sys.argv[1:]
    while a:
        if a[0] == "--strict": strict.update(a[1:]); break
        a = a[1:]
    rows = collections.defaultdict(list); errors = []; warns = []
    for path in sorted(glob.glob(os.path.join(RAW, "*.jsonl"))):
        name = os.path.basename(path); tag, kind = name.split(".")[0], name.split(".")[1]
        for n, line in enumerate(open(path, encoding="utf-8"), 1):
            if not line.strip(): continue
            try: r = json.loads(line)
            except Exception as e: errors.append(f"{name}:{n} not valid JSON ({e})"); continue
            rows[kind].append((tag, name, n, r))
    sources = {r["id"]: (tag, r) for tag, _, _, r in rows["sources"] if "id" in r}
    entities = {r["id"] for _, _, _, r in rows["entities"] if "id" in r}
    seen = {}
    for kind, items in rows.items():
        for tag, name, n, r in items:
            where = f"{name}:{n}"
            for k in REQUIRED.get(kind, []):
                if k not in r or r[k] in ("", None) and k not in ("value",):
                    errors.append(f"{where} missing required field '{k}'")
            rid = r.get("id")
            if rid:
                if rid in seen and kind not in ("sources", "entities"): errors.append(f"{where} duplicate id {rid} (also {seen[rid]})")
                seen.setdefault(rid, where)
            if kind not in NO_PROV and kind != "corrections" or kind == "corrections":
                p = r.get("prov")
                if kind in NO_PROV: p = True
                if p is None: errors.append(f"{where} has no prov block")
                elif isinstance(p, dict):
                    for k in PROV_KEYS:
                        if k not in p: errors.append(f"{where} prov lacks '{k}'")
                    if p.get("asserted_by") not in ASSERTERS: errors.append(f"{where} prov.asserted_by '{p.get('asserted_by')}' not allowed")
                    if p.get("confidence") not in CONF: errors.append(f"{where} prov.confidence '{p.get('confidence')}' not allowed")
                    if p.get("source") not in sources: errors.append(f"{where} prov.source '{p.get('source')}' is not in any sources file")
                    if len((p.get("quote") or "").split()) > 12: errors.append(f"{where} quote longer than 12 words")
            for f in ENTITY_FIELDS.get(kind, []):
                v = r.get(f)
                if v and not ID.match(str(v)): errors.append(f"{where} {f} '{v}' is not a valid entity id")
                elif v and v not in entities: warns.append(f"{where} {f} '{v}' has no entity row (a stub will be created)")
            for (k2, f), allowed in VOCAB.items():
                if kind == k2 and r.get(f) and r[f] not in allowed:
                    errors.append(f"{where} {f} '{r[f]}' is not in the ontology; allowed: {', '.join(sorted(allowed))}")
            if kind == "events":
                if not DATE.match(str(r.get("date", ""))): warns.append(f"{where} date '{r.get('date')}' is not ISO (YYYY, YYYY-MM or YYYY-MM-DD)")
            if "currency" in r and r["currency"] not in CUR: errors.append(f"{where} currency '{r['currency']}' must be PYG or USD")
            for k in ("amount", "principal", "outstanding"):
                if r.get(k) is not None and not isinstance(r[k], (int, float)): errors.append(f"{where} {k} must be a number or null")
            if kind == "sources":
                if r.get("kind") in ("press", "official", "rating") and not str(r.get("url", "")).startswith("http"):
                    (errors if tag in strict else warns).append(f"{where} source '{rid}' of kind {r.get('kind')} has no http(s) link")
                if tag in strict and re.search(r"(\.\.\.|…|-)$", str(r.get("url", ""))): errors.append(f"{where} link is truncated")
            text = json.dumps(r, ensure_ascii=False)
            if kind not in ("loans",):
                for rx, what in PII:
                    if rx.search(text) and "op_number" not in r: warns.append(f"{where} {what}: check that no personal identifier is stored")
    for e in errors: print("ERROR", e)
    by = collections.Counter(w.split(" ", 1)[1].split("'")[0].strip() if "'" in w else w for w in warns)
    print(f"\nrows: {sum(len(v) for v in rows.values())} in {len(set(x[1] for v in rows.values() for x in v))} files | errors: {len(errors)} | warnings: {len(warns)}")
    if "-v" in sys.argv:
        for w in warns: print("WARN ", w)
    else:
        kinds = collections.Counter(re.sub(r"'[^']*'", "'…'", w.split(" ", 1)[1]) for w in warns)
        for k, c in kinds.most_common(8): print(f"  warn x{c}: {k}")
        if warns: print("  (run with -v to list every warning)")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
