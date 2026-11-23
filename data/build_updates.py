#!/usr/bin/env python3
"""Checks data/updates.json (the log shown as "What's new" on the overview) and copies it to site/data/updates.json.
Add one entry at the TOP for every run that changes the published data. Fails if an entry cites a row that does not exist,
if entries are not newest-first, or if executed_at lacks a time zone."""
import datetime, glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ids = set()
for f in glob.glob(os.path.join(HERE, "raw", "*.jsonl")):
    for l in open(f, encoding="utf-8"):
        if l.strip(): ids.add(json.loads(l).get("id"))
U = json.load(open(os.path.join(HERE, "updates.json"), encoding="utf-8")); err = []
ts = []
for u in U:
    t = datetime.datetime.fromisoformat(u["executed_at"])
    if t.tzinfo is None: err.append("executed_at without time zone: " + u["executed_at"])
    ts.append(t)
    for it in u["items"]:
        if not (it.get("en") and it.get("es")): err.append("item without both languages")
        err += ["ref not in data/raw: " + r for r in it.get("refs", []) if r not in ids]
if ts != sorted(ts, reverse=True): err.append("entries must be newest first")
if err: sys.exit("updates.json: " + "; ".join(err))
json.dump(U, open(os.path.join(os.path.dirname(HERE), "site", "data", "updates.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("updates.json: %d entries, latest %s" % (len(U), U[0]["executed_at"]))
