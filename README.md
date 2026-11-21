# Ueno Bank case graph

Source of truth for the Ueno Bank S.A. (Paraguay) case file: claim-level rows with provenance, the script that turns them into an RDF graph, the checks that guard it, and the site that reads it.

**Keep this repository private.** It names people in connection with unproven allegations. Everything here is an allegation; everyone named is presumed innocent. The analysis memos were written by AI analysts, not licensed professionals.

## How it fits together

    data/raw/*.jsonl   --build_graph.py-->   site/data/graph.{trig,ttl,jsonld}   -->   site/ (static page)
       ^ edit here         ^ deterministic, ~8 s        ^ build output, not committed        store/ (Oxigraph, SPARQL)

- **The rows are the truth.** Change a claim by editing or adding a row; never edit the graph files. Every change is then a diff someone can review.
- **Corrections are rows too** (`edit.corrections.jsonl`): the original value stays visible in the graph.

## Commands

| Command | What it does | Time |
|---|---|---|
| `pip install -r requirements.txt` | rdflib, pyshacl, pyoxigraph | |
| `make hooks` | turn on the commit hook (once per clone) | |
| `make check` | validate rows, build graph, run SHACL shapes | ~35 s |
| `make queries` | load the graph into Oxigraph (`store/db`) and run the six saved queries | ~5 s |
| `python3 store/load.py q3` | print the rows of one query | |
| `make test` | end-to-end tests with good and deliberately bad rows | ~1 min |
| `make pub` | build `pub/`, the public copy of the site (three private individuals removed) | |

## Layout

| Path | Contents |
|---|---|
| `SPEC.md` | row schema and rules for every contributor |
| `data/raw/` | the rows, one file per contributor tag and kind |
| `data/build_graph.py` | rows -> graph, with its own consistency checks |
| `data/ontology.ttl`, `data/fibo_mapping.md` | the vocabulary and its FIBO alignment |
| `shapes/ueno-shapes.ttl` | SHACL: no assertion without source, asserter and confidence |
| `tools/` | `validate_rows.py`, `validate_graph.py` |
| `store/` | Oxigraph loader, `queries/q1..q6.rq`, optional Fuseki compose file |
| `docs/BOT_CONTRACT.md` | what the monitoring bot may write and how it is checked |
| `analysis/`, `reports/`, `research_notes/` | memos and reports built on the graph |
| `site/` | the interactive case file (static; open `site/index.html` through any web server) |

## Not in this repository, on purpose

The scanned prosecution record, its raw OCR text and the uploaded dossiers. The record's personal-details block holds an ID number and a home address; `.gitignore` blocks `source/` and `*.pdf`. Rows cite the record by page (`src:acta-pNN`).

## Known limits

- The Fuseki compose file is untested (no container runtime where this was built). The Oxigraph path is tested.
- SHACL and the row validator check shape, not truth: they cannot tell whether a quote is really in the linked page.
- The personal-data check is a pattern match and will miss things. A person reviews every bot pull request.
- `site/data/fibo_mapping.json` still shows the old text of query 5; `store/queries/q5.rq` is the corrected one.
