#!/usr/bin/env python3
"""Prepare the extra JSON files the interactive site loads next to graph.jsonld.

Run from anywhere:  python3 data/build_site_data.py
- data/fibo_mapping.md            -> site/data/fibo_mapping.json
- analysis/{legal_*,fin_*}.json   -> site/data/ (copied only if present and valid JSON)
- analysis/editor_report.md       -> site/data/editor_report.md (if present)
(verified.json and the editor corrections are produced by data/build_graph.py, not here.)
Safe to re-run; missing optional inputs are skipped (the page hides those sections).
"""
import json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "data"


def md_cells(line):
    cells = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    return [c.strip().replace("\\|", "|") for c in cells]


def parse_fibo(md):
    out = {"intro": [], "result": "", "prefixes": [], "mapping": [], "differs": [], "lacks": [],
           "query_prefixes": "", "query_note": "", "queries": []}
    sections, cur = {}, None
    for line in md.splitlines():
        m = re.match(r"^## (.+)$", line)
        if m:
            cur = m.group(1).strip()
            sections[cur] = []
        elif cur is not None:
            sections[cur].append(line)
        elif line.strip() and not line.startswith("# "):
            out["intro"].append(line.strip())

    def table(lines):
        rows = [md_cells(l) for l in lines if l.strip().startswith("|")]
        return [r for r in rows[2:]] if len(rows) > 2 else []

    for l in sections.get("How the IRIs were verified", []):
        if l.startswith("**Result"):
            out["result"] = l.strip().strip("*")
    for r in table(sections.get("Prefixes", [])):
        if len(r) >= 2:
            out["prefixes"].append({"prefix": r[0].strip("`"), "namespace": r[1].strip("`")})
    for r in table(sections.get("Mapping table", [])):
        if len(r) < 7:
            continue
        terms = []
        for t in r[3].split("<br>"):
            m = re.match(r'`([^`]+)`\s*\("([^"]*)",\s*([^)]+)\)', t.strip())
            if m:
                terms.append({"iri": m.group(1), "label": None if m.group(2) == "None" else m.group(2), "kind": m.group(3)})
            elif t.strip():
                terms.append({"iri": t.strip().strip("`"), "label": None, "kind": ""})
        out["mapping"].append({
            "n": int(r[0]) if r[0].isdigit() else r[0], "concept": r[1], "status": r[2], "terms": terms,
            "files": [f.strip().strip("`") for f in r[4].split("<br>") if f.strip()],
            "use": r[5], "notes": r[6]})
    for key, sec in (("differs", "FIBO terms that differ from common assumptions"), ("lacks", "What FIBO lacks for this use case")):
        for l in sections.get(sec, []):
            m = re.match(r"^(?:\d+\.|-)\s+(.*)$", l.strip())
            if m:
                out[key].append(m.group(1))
    q = "\n".join(sections.get("Example SPARQL queries", []))
    parts = re.split(r"^### ", q, flags=re.M)
    head = parts[0]
    m = re.search(r"```sparql\n(.*?)```", head, flags=re.S)
    out["query_prefixes"] = m.group(1).strip() if m else ""
    out["query_note"] = re.sub(r"```sparql.*?```", "", head, flags=re.S).strip()
    for p in parts[1:]:
        title, _, body = p.partition("\n")
        m = re.search(r"```sparql\n(.*?)```", body, flags=re.S)
        if not m:
            continue
        note = re.sub(r"```sparql.*?```", "", body, flags=re.S).strip()
        out["queries"].append({"title": title.strip(), "sparql": m.group(1).strip(), "note": note})
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = []
    src = ROOT / "data" / "fibo_mapping.md"
    if src.exists():
        d = parse_fibo(src.read_text(encoding="utf-8"))
        (OUT / "fibo_mapping.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        report.append("fibo_mapping.json: %d concepts, %d queries, %d prefixes" % (len(d["mapping"]), len(d["queries"]), len(d["prefixes"])))
    for name in ("legal_prosecution", "legal_defence", "fin_credit", "fin_flows"):
        p = ROOT / "analysis" / (name + ".json")
        if not p.exists():
            report.append(name + ".json: not present, skipped")
            continue
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except ValueError as e:
            report.append(name + ".json: INVALID JSON, skipped (%s)" % e)
            continue
        shutil.copyfile(p, OUT / (name + ".json"))
        report.append(name + ".json: copied")
    ed = ROOT / "analysis" / "editor_report.md"
    if ed.exists():
        shutil.copyfile(ed, OUT / "editor_report.md")
        report.append("editor_report.md: copied")
    print("\n".join(report))


if __name__ == "__main__":
    sys.exit(main())
