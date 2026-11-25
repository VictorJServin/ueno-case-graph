#!/usr/bin/env python3
"""End-to-end checks: good bot rows pass and reach the graph; bad rows and bad triples are rejected.
Run: python3 tests/test_pipeline.py   (takes about a minute)"""
import json, os, shutil, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
def sh(args, env=None):
    r = subprocess.run(args, cwd=ROOT, env={**os.environ, **(env or {})}, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
SRC = {"id": "src:test-2026-11-20-example", "kind": "press", "outlet": "Test outlet", "title": "Example headline",
       "date": "2026-11-20", "url": "https://example.org/news/2026/11/20/example-headline"}
EVT = {"id": "bot:event:900001", "date": "2026-11-20", "date_precision": "day", "category": "supervisory",
       "title_en": "Test event", "title_es": "Evento de prueba", "detail_en": "A test.", "detail_es": "Una prueba.",
       "parties": ["org:ueno-bank"], "amount": None, "currency": None,
       "prov": {"asserted_by": "press", "source": SRC["id"], "locator": "para. 2", "quote": "short quote here", "confidence": "medium", "note": ""}}
def raw_with(tmp, sources, events):
    """Copy of data/raw with the test's rows APPENDED to the bot's files, as a real delivery would be."""
    raw = os.path.join(tmp, "raw"); shutil.copytree(os.path.join(ROOT, "data", "raw"), raw)
    for name, rows in (("bot.sources.jsonl", sources), ("bot.events.jsonl", events)):
        with open(os.path.join(raw, name), "a", encoding="utf-8") as f:
            f.write("".join(json.dumps(x) + "\n" for x in rows))
    return raw
fails = []
def check(name, cond, out=""):
    print(("ok   " if cond else "FAIL ") + name); 
    if not cond: fails.append(name); print(out[-800:])

with tempfile.TemporaryDirectory() as t:
    raw = raw_with(t, [SRC], [EVT]); site = os.path.join(t, "site"); os.makedirs(site)
    c, o = sh([PY, "tools/validate_rows.py", "--strict", "bot"], {"UENO_RAW": raw}); check("good bot rows pass the row validator", c == 0, o)
    c, o = sh([PY, "data/build_graph.py", "--raw", raw, "--site", site, "--report", os.path.join(t, "merge_report.md"), "--quiet"]); check("graph builds with bot rows and passes its own checks", c == 0 and "all checks passed" in o, o)
    ttl = open(os.path.join(site, "graph.ttl"), encoding="utf-8").read()
    check("bot event is in the graph with its link", "Test event" in ttl and SRC["url"] in ttl)
    c, o = sh([PY, "tools/validate_graph.py", os.path.join(site, "graph.ttl")]); check("graph with bot rows passes SHACL", c == 0, o)
    bad = os.path.join(t, "bad.ttl")
    open(bad, "w", encoding="utf-8").write(ttl + '\n<https://w3id.org/ueno-case/id/flow/orphan> a <https://w3id.org/ueno-case/ont#Flow> ; <https://w3id.org/ueno-case/ont#confidence> "certain" .\n')
    c, o = sh([PY, "tools/validate_graph.py", bad]); check("SHACL rejects a flow with no source and a made-up confidence", c == 1 and "no source" in o, o)

def bad_case(name, src, evt, expect):
    with tempfile.TemporaryDirectory() as t:
        raw = raw_with(t, [src] if src else [], [evt])
        c, o = sh([PY, "tools/validate_rows.py", "--strict", "bot"], {"UENO_RAW": raw}); check(name, c == 1 and expect in o, o)
bad_case("rejects a press source without a link", {**SRC, "url": ""}, EVT, "no http(s) link")
bad_case("rejects a truncated link", {**SRC, "url": "https://example.org/news/..."}, EVT, "truncated")
bad_case("rejects a claim whose source is not defined", None, EVT, "is not in any sources file")
bad_case("rejects a quote over 12 words", SRC, {**EVT, "prov": {**EVT["prov"], "quote": " ".join(["w"] * 13)}}, "longer than 12 words")
bad_case("rejects an unknown confidence", SRC, {**EVT, "prov": {**EVT["prov"], "confidence": "certain"}}, "confidence")
bad_case("rejects an unknown asserter", SRC, {**EVT, "prov": {**EVT["prov"], "asserted_by": "twitter"}}, "asserted_by")
bad_case("rejects a category that is not in the ontology", SRC, {**EVT, "category": "regulatory"}, "not in the ontology")
bad_case("rejects a social-media link as a source", {**SRC, "url": "https://x.com/someone/status/123"}, EVT, "social-media link")
bad_case("rejects 'high' confidence without a note that the page was opened", SRC, {**EVT, "prov": {**EVT["prov"], "confidence": "high"}}, "needs a prov.note")
bad_case("rejects an id outside the bot's own series", SRC, {**EVT, "id": "chrono:event:9999"}, "must look like bot:event:0001")
bad_case("rejects a row with no provenance", SRC, {k: v for k, v in EVT.items() if k != "prov"}, "no prov block")
print("\n%d failed" % len(fails)); sys.exit(1 if fails else 0)
