#!/usr/bin/env python3
"""Load site/data/graph.trig into a local Oxigraph store (store/db) and run the saved queries.

  python3 store/load.py            # rebuild the store from the TriG file
  python3 store/load.py q3         # run store/queries/q3.rq and print rows
  python3 store/load.py --all      # run every saved query, print row counts
  python3 store/load.py --serve    # print the command for a SPARQL endpoint on :7878
"""
import glob, os, shutil, sys
import pyoxigraph as ox
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
DB = os.path.join(HERE, "db"); TRIG = os.path.join(ROOT, "site", "data", "graph.trig")

def build():
    shutil.rmtree(DB, ignore_errors=True)
    s = ox.Store(DB)
    s.bulk_load(path=TRIG, format=ox.RdfFormat.TRIG)
    # the ontology (class hierarchy) goes in its own named graph so queries can use rdfs:subClassOf
    s.bulk_load(path=os.path.join(ROOT, "site", "data", "ontology.ttl"), format=ox.RdfFormat.TURTLE,
                to_graph=ox.NamedNode("https://w3id.org/ueno-case/graph/ontology"))
    s.flush()
    print(f"loaded {len(s)} quads, {len(list(s.named_graphs()))} named graphs -> {DB}")
    return s

def run(s, path, show=True):
    q = open(path, encoding="utf-8").read()
    res = s.query(q, use_default_graph_as_union=True)
    rows = list(res); vars_ = [v.value for v in res.variables]
    if show:
        print("\t".join(vars_))
        for r in rows[:50]:
            print("\t".join("" if r[v] is None else str(r[v].value) for v in vars_))
        if len(rows) > 50: print(f"... {len(rows)} rows")
    return len(rows)

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: build(); sys.exit()
    if a[0] == "--serve":
        print(f"oxigraph serve --location {DB} --bind 0.0.0.0:7878   # needs the oxigraph CLI (cargo install oxigraph-cli or the ghcr.io/oxigraph/oxigraph image)"); sys.exit()
    s = ox.Store(DB) if os.path.isdir(DB) else build()
    if a[0] == "--all":
        bad = 0
        for p in sorted(glob.glob(os.path.join(HERE, "queries", "*.rq"))):
            n = run(s, p, show=False); print(f"{os.path.basename(p)}: {n} rows  {open(p).readline().strip()[2:]}")
            bad += n == 0
        sys.exit(1 if bad else 0)
    run(s, os.path.join(HERE, "queries", a[0] + ".rq"))
