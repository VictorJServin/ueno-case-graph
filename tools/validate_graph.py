#!/usr/bin/env python3
"""Validate the built graph against shapes/ueno-shapes.ttl (SHACL). Exit 1 on any violation."""
import os, sys, collections
import rdflib
from pyshacl import validate
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = rdflib.Graph(); data.parse(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "site", "data", "graph.ttl"), format="turtle")
shapes = rdflib.Graph(); shapes.parse(os.path.join(ROOT, "shapes", "ueno-shapes.ttl"), format="turtle")
conforms, report, _ = validate(data, shacl_graph=shapes, inference="none", advanced=True)
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
viol = collections.Counter(); warn = collections.Counter(); examples = {}
for r in report.subjects(rdflib.RDF.type, SH.ValidationResult):
    sev = report.value(r, SH.resultSeverity); msg = str(report.value(r, SH.resultMessage) or report.value(r, SH.sourceConstraintComponent))
    (warn if sev == SH.Warning else viol)[msg] += 1
    examples.setdefault(msg, str(report.value(r, SH.focusNode)))
print(f"triples: {len(data)} | violations: {sum(viol.values())} | warnings: {sum(warn.values())}")
for label, c in (("VIOLATION", viol), ("WARNING", warn)):
    for m, n in c.most_common(): print(f"{label} x{n}: {m}\n    e.g. {examples[m]}")
sys.exit(1 if viol else 0)
