#!/usr/bin/env python3
"""Turns the bot's run manifests (inbox/runs/*.json) into entries of data/updates.json, the "What's new" log.
  python3 tools/apply_run.py [--at 2026-11-25T10:40:00-08:00]
Adds one entry per manifest not yet logged (matched on the 'run' key), newest first. Prints what it added.
The refresh that calls this still reviews the rows first; this script only does the bookkeeping."""
import datetime, glob, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data", "updates.json"); U = json.load(open(P, encoding="utf-8"))
at = sys.argv[sys.argv.index("--at") + 1] if "--at" in sys.argv else datetime.datetime.now(datetime.timezone.utc).astimezone().replace(microsecond=0).isoformat()
done = {u.get("run") for u in U}; added = []
for f in sorted(glob.glob(os.path.join(ROOT, "inbox", "runs", "*.json"))):
    run = os.path.basename(f)[:-5]
    if run in done: continue
    m = json.load(open(f, encoding="utf-8")); ra = m.get("rows_added", {}); g = m["generated_at"]
    when = datetime.datetime.fromisoformat(g).strftime("%-d %b %Y %H:%M PT")
    e = {"executed_at": at, "run": run, "data_to": g[:10],
         "input": {"en": "Monitoring dossier %s, generated %s" % (m.get("dossier_version", ""), when), "es": "Dossier de monitoreo %s, generado el %s" % (m.get("dossier_version", ""), when)},
         "counts": {"events": len(ra.get("events", [])), "figures": len(ra.get("facts", [])), "sources": len(ra.get("sources", []))},
         "items": [{k: v for k, v in it.items() if k in ("en", "es", "refs", "go")} for it in m.get("whats_new", [])[:6]]}
    nh = m.get("needs_human") or []
    e["not_done"] = {"en": "Automatic refresh from the monitoring bot's delivery. Not updated in this run: the missing-money estimate, the charges table and the written reports." + (" %d point(s) were flagged for a person to check." % len(nh) if nh else ""),
                     "es": "Actualización automática a partir de la entrega del bot de monitoreo. No actualizado en esta corrida: la estimación del dinero faltante, la tabla de imputaciones y los informes escritos." + (" Se marcaron %d punto(s) para revisión humana." % len(nh) if nh else "")}
    added.append(e)
for e in added: U.insert(0, e)
if added: json.dump(U, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("runs logged:", [e["run"] for e in added] or "none new")
