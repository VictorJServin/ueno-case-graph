#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_graph.py - merge the raw contributor files of the Ueno Bank case project into one RDF graph
with claim-level provenance, and emit the files the interactive page loads.

    python3 data/build_graph.py            # reads data/raw/*.jsonl, writes site/data/* and data/merge_report.md
    python3 data/build_graph.py --raw DIR --site DIR --report FILE   # alternative locations (used for tests)

Safe to re-run at any time: every output is rebuilt from scratch, files in data/raw/ are only read,
missing or empty contributor files are tolerated, and the output is deterministic (sorted).

Outputs
    site/data/graph.trig     named graphs (default + prosecution / rey / press)
    site/data/graph.ttl      union of all graphs, Turtle
    site/data/graph.jsonld   flat JSON-LD for the browser (shape documented in site/data/README.md)
    site/data/ontology.ttl   copy of data/ontology.ttl
    site/data/stats.json     counts and loan-principal totals
    site/data/verified.json  ids of the nodes the editor verified
    site/data/README.md      description of the JSON-LD shape, generated with real examples
    data/merge_report.md     things a human should review (suspected duplicates, unknown references...)

Modelling choices (see also site/data/README.md)
  * Vocabulary: data/ontology.ttl (uc:, v0.2.0). Every statement about the case is an n-ary resource carrying
    prov:wasDerivedFrom, uc:assertedBy, uc:confidence, uc:locator, uc:quote, uc:provenanceNote, uc:sourceTier.
  * Named graphs: prosecution and rey hold only assertions of those voices whose source is a page of the
    prosecution record (src:acta-pNN). Everything else is in the press graph: press, regulator, rating agency,
    company, defence, and prosecution / Rey claims reported second-hand (SECOND_HAND_TO_PRESS). uc:assertedBy
    always keeps the exact voice. Parties, sources, correction records and the dataset node (owl:imports) are
    in the default graph.
  * Editor layer (edit.corrections / edit.verified / edit.entity_merges) is applied in memory after loading and
    before any RDF is made: corrected values replace the originals, which are kept as uc:originalValue with
    uc:correctedField, uc:editorNote, the correction's source and a uc:Correction record. Nothing is deleted:
    delete_row and HIDDEN_ROWS only set uc:hidden. Entity merges go through the alias map.
  * Entities with the same id are one entity. Entities with different ids are merged ONLY through ALIAS_MAP and
    edit.entity_merges.jsonl; other suspected duplicates go to data/merge_report.md.
  * Each entity row also yields one uc:PartyDescription assertion, so the provenance of labels and
    descriptions is not lost.
  * References to entities that no contributor has described become stub parties (uc:isStub true), unless
    EDITORIAL_ENTITIES gives them a label.
  * Derived links: uc:involvesParty (RDFS super-property of the participant properties), uc:ultimateRecipient +
    uc:recipientDerivedFrom on loans, uc:sameSubjectAs between loan records of different voices with the same
    operation number, lender and borrower, and uc:sameOperationKey on alternative reports of one operation.
  * Nothing is summed in the RDF. stats.json holds totals, grouped so that no two sources are added together.
"""
import argparse
import collections
import datetime
import difflib
import glob
import json
import os
import re
import shutil
import sys
import unicodedata
from decimal import Decimal, InvalidOperation

from rdflib import Dataset, Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, SKOS, XSD

# =============================================================================================
# Configuration a human may edit
# =============================================================================================

# Explicit alias map: {"id that should disappear": "canonical id"}. Applied to entity rows and to every
# reference before anything else. Add a pair only after checking the "Suspected duplicates" section of
# data/merge_report.md by hand. Nothing else ever merges two ids.
ALIAS_MAP = {
    # "org:ueno-holding": "org:u-holdings",
}

# Which named graph each asserter's rows go to. Voices other than the two primary voices of the
# prosecution record are kept together in the press graph and told apart by uc:assertedBy.
GRAPH_OF_ASSERTER = {
    "prosecution": "prosecution",
    "rey": "rey",
    "press": "press",
    "regulator": "press",
    "rating_agency": "press",
    "company": "press",
    "defence": "press",
    "analyst": "press",
}

# Policy (coordinator, 20 Nov 2026): the prosecution and rey graphs contain ONLY assertions whose source is a page
# of the prosecution record (src:acta-pNN). A prosecution or Rey claim that reaches us through the press, the
# dossier or any other document keeps its uc:assertedBy but lives in the press graph. Set to False to file rows
# by asserter alone.
SECOND_HAND_TO_PRESS = True

# Contributor whose label wins when several contributors describe the same entity (others become altLabels).
LABEL_PRIORITY = ["rec", "chrono", "press", "dos", "edit"]
# When two contributors spell the same label with and without accents, the accented spelling wins automatically.

# Editorial label decisions: id -> (label, altLabels to add, altLabels to drop from the party node).
LABEL_OVERRIDES = {
    "org:u-holdings": ("U Holdings S.à r.l.", ["U Luxemburgo (as named in the record)"], ["U Luxemburgo (as named by Rey)"]),
}

# Editorial entities: ids of the SPEC.md id list that assertions use but no contributor has described.
# Used only while no contributor describes the id. Provenance: asserted_by press, confidence high, EDITORIAL_SOURCE.
EDITORIAL_SOURCE = {"id": "src:spec-id-list", "kind": "project", "outlet": "Ueno case project",
                    "title": "SPEC.md, entity id list", "date": "2026-11-20", "url": "", "page": None}
EDITORIAL_ENTITIES = {
    "person:carlos-carvallo": ("Person", "Carlos Carvallo"),
    "auth:fgd": ("Authority", "Fondo de Garantía de Depósitos"),
    "person:holger-insfran": ("Person", "Holger Insfrán"),
    "auth:superintendencia-de-valores": ("Authority", "Superintendencia de Valores"),
    "org:cadiem": ("Company", "Cadiem"),
}

# Rows kept in the graph but marked uc:hidden true so the page leaves them out of its visualisations.
HIDDEN_ROWS = {
    "rec:flow:0075": ("Aggregate figure (about USD 900 million) with a stand-in recipient; not a single movement of money. "
                      "Shown as a statement by Rey instead (see the linked event).",
                      "Cifra agregada (unos USD 900 millones) con un destinatario supuesto; no es un movimiento de dinero único. "
                      "Se muestra como declaración de Rey (ver el evento vinculado)."),
    "rec:flow:0076": ("Property sale whose seller is not stated in the record; the direction of the flow is an assumption.",
                      "Venta de inmueble cuyo vendedor no consta en el acta; el sentido del flujo es una suposición."),
    "press:role:0024": ("Small private holder of U Holdings; not relevant to the case narrative.",
                        "Pequeño tenedor privado de U Holdings; sin relevancia para el caso."),
    "press:role:0025": ("Small private holder of U Holdings; not relevant to the case narrative.",
                        "Pequeño tenedor privado de U Holdings; sin relevancia para el caso."),
    "press:role:0026": ("Small private holder of U Holdings; not relevant to the case narrative.",
                        "Pequeño tenedor privado de U Holdings; sin relevancia para el caso."),
}

# Hidden flows that are restated as a uc:CaseEvent (a claim by the same voice, same provenance) so the statement
# stays visible on timelines: flow id -> (category, title_en, title_es, parties to keep).
CLAIM_EVENTS = {
    "rec:flow:0075": ("statement", "Rey: about USD 900 million of loans were used to defer expenses",
                      "Rey: unos USD 900 millones en créditos se usaron para diferir gastos", ["org:ueno-bank"]),
}

# Source kind overrides by id prefix (the dossier is a third-party compilation, not a company publication).
SOURCE_KIND_BY_PREFIX = {"src:dossier-": "dossier"}

# Extra FIBO / Commons classes for a few parties, exactly as listed in data/fibo_mapping.md (rows 1-4).
EXTRA_PARTY_TYPES = {
    "org:ueno-bank": "Bank", "org:vision-banco": "Bank", "org:zeta-banco": "Bank", "org:otp-bank": "Bank",
    "auth:bcp": "CentralBank",
    "auth:superintendencia-de-bancos": "RegulatoryAgency", "auth:superintendencia-de-valores": "RegulatoryAgency",
    "org:ueno-casa-de-bolsa": "BrokerDealer", "org:cadiem": "BrokerDealer",
}

CUTOFF = "2026-11-20"          # SPEC.md rule 9; later dates are reported, not dropped
MAX_QUOTE_WORDS = 12           # SPEC.md rule 5; longer quotes are reported, not dropped

# Flow instruments that are not a forwarding of loan proceeds (ignored when deriving uc:ultimateRecipient).
NON_PROCEEDS_INSTRUMENTS = {"loan_disbursement", "repayment", "portfolio_assignment", "portfolio_sale_price"}

# =============================================================================================
# Namespaces and vocabulary tables
# =============================================================================================

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

UC = Namespace("https://w3id.org/ueno-case/ont#")
ID = "https://w3id.org/ueno-case/id/"
ONT = URIRef("https://w3id.org/ueno-case/ont")
PROV = Namespace("http://www.w3.org/ns/prov#")
SCHEMA = Namespace("https://schema.org/")
CUR = Namespace("https://spec.edmcouncil.org/fibo/ontology/FND/Accounting/ISO4217-CurrencyCodes/")
FSE = Namespace("https://spec.edmcouncil.org/fibo/ontology/FBC/FunctionalEntities/FinancialServicesEntities/")
FPAS = Namespace("https://spec.edmcouncil.org/fibo/ontology/FBC/ProductsAndServices/FinancialProductsAndServices/")
LN = Namespace("https://spec.edmcouncil.org/fibo/ontology/LOAN/LoansGeneral/Loans/")
CMNS_RA = Namespace("https://www.omg.org/spec/Commons/RegulatoryAgencies/")
DATASET = URIRef(ID + "dataset")
GRAPH_NAMES = ["prosecution", "rey", "press", "analysis"]
ANALYSIS_GRAPH = "analysis"      # uc:AnalystOpinion rows only; never mixed with sourced assertions

PREFIXES = [
    ("uc", str(UC)), ("ucr", ID), ("rdf", str(RDF)), ("rdfs", str(RDFS)), ("owl", str(OWL)), ("xsd", str(XSD)),
    ("skos", str(SKOS)), ("dcterms", str(DCTERMS)), ("prov", str(PROV)), ("schema", str(SCHEMA)),
    ("fibo-fnd-acc-4217", str(CUR)), ("fibo-fbc-fct-fse", str(FSE)), ("fibo-fbc-pas-fpas", str(FPAS)),
    ("fibo-loan-ln-ln", str(LN)), ("cmns-ra", str(CMNS_RA)),
]

ASSERTER_CONCEPT = {"prosecution": "Prosecution", "rey": "Rey", "defence": "Defence", "regulator": "Regulator",
                    "press": "Press", "rating_agency": "RatingAgency", "company": "Company", "analyst": "Analyst"}
CONFIDENCES = ("high", "medium", "low")
ENTITY_CLASS = {"Person": "Person", "Company": "Organisation", "Organisation": "Organisation",
                "Organization": "Organisation", "Authority": "Authority"}
PREFIX_CLASS = {"person": "Person", "org": "Organisation", "auth": "Authority"}
EXTERNAL_CLASSES = {"Bank": FSE.Bank, "CentralBank": FSE.CentralBank, "BrokerDealer": FPAS.BrokerDealer,
                    "RegulatoryAgency": CMNS_RA.RegulatoryAgency, "UnsecuredLoan": LN.UnsecuredLoan}

# JSON-LD term table: term -> (predicate IRI, kind).
#   ref / refs   IRI reference, written as a compact id string (refs: always an array)
#   voc          reference to an enumeration concept or currency, written as a context term
#   lang / langs language map {"en": ..., "es": ...} (langs: each value is an array)
#   str / strs   plain string (strs: always an array)
#   dec          xsd:decimal written as a JSON string;  int / bool: native JSON
#   day          xsd:date written as a "YYYY-MM-DD" string
#   anydate      typed literal object {"@value": ..., "@type": "xsd:date|xsd:gYearMonth|xsd:gYear"}
#   url          xsd:anyURI written as a string
TERMS = {
    # provenance
    "source": (PROV.wasDerivedFrom, "ref"), "assertedBy": (UC.assertedBy, "voc"),
    "confidence": (UC.confidence, "str"), "locator": (UC.locator, "str"), "quote": (UC.quote, "lang"),
    "provenanceNote": (UC.provenanceNote, "str"), "sameSubjectAs": (UC.sameSubjectAs, "refs"),
    # generic
    "identifier": (DCTERMS.identifier, "str"), "label": (RDFS.label, "str"), "altLabel": (SKOS.altLabel, "strs"),
    "description": (DCTERMS.description, "lang"), "title": (DCTERMS.title, "lang"), "note": (SKOS.note, "lang"),
    "comment": (RDFS.comment, "lang"), "imports": (OWL.imports, "ref"), "subClassOf": (RDFS.subClassOf, "ref"),
    "isDefinedBy": (RDFS.isDefinedBy, "ref"),
    # sources
    "sourceKind": (UC.sourceKind, "str"), "outlet": (UC.outlet, "str"), "name": (SCHEMA.name, "str"),
    "date": (DCTERMS.date, "anydate"), "url": (SCHEMA.url, "url"), "page": (UC.page, "int"),
    # parties
    "business": (UC.business, "lang"), "isStub": (UC.isStub, "bool"),
    "involvesParty": (UC.involvesParty, "refs"),
    # roles
    "holder": (UC.holder, "ref"), "organisation": (UC.organisation, "ref"), "roleType": (UC.roleType, "voc"),
    "percentage": (UC.percentage, "dec"), "startDate": (UC.startDate, "anydate"), "endDate": (UC.endDate, "anydate"),
    "startDateText": (UC.startDateText, "str"), "endDateText": (UC.endDateText, "str"),
    # loans
    "lender": (UC.lender, "ref"), "nominalBorrower": (UC.nominalBorrower, "ref"),
    "ultimateRecipient": (UC.ultimateRecipient, "refs"), "recipientDerivedFrom": (UC.recipientDerivedFrom, "refs"),
    "operationNumber": (UC.operationNumber, "str"), "principal": (UC.principal, "dec"),
    "outstanding": (UC.outstanding, "dec"), "ratePct": (UC.ratePct, "dec"), "termYears": (UC.termYears, "dec"),
    "termDays": (UC.termDays, "int"), "collateral": (UC.collateral, "str"), "amortisation": (UC.amortisation, "str"),
    "loanStatus": (UC.loanStatus, "str"),
    # flows, events, facts
    "fromParty": (UC.fromParty, "ref"), "toParty": (UC.toParty, "ref"), "amount": (UC.amount, "dec"),
    "amountIsApproximate": (UC.amountIsApproximate, "bool"), "currency": (UC.currency, "voc"),
    "onDate": (UC.onDate, "anydate"), "datePrecision": (UC.datePrecision, "str"), "dateText": (UC.dateText, "str"),
    "sortDate": (UC.sortDate, "day"), "sortDateEnd": (UC.sortDateEnd, "day"),
    "instrument": (UC.instrument, "voc"), "purpose": (UC.purpose, "lang"), "linkedLoan": (UC.linkedLoan, "ref"),
    "eventCategory": (UC.eventCategory, "voc"), "aboutParty": (UC.aboutParty, "ref"), "metric": (UC.metric, "str"),
    "textValue": (UC.textValue, "str"), "unitNote": (UC.unitNote, "str"),
    # charges, issues
    "chargedPerson": (UC.chargedPerson, "ref"), "allegedOffence": (UC.allegedOffence, "langs"),
    "allegedOffenceAdded": (UC.allegedOffenceAdded, "langs"), "proceduralMeasure": (UC.proceduralMeasure, "lang"),
    "nameAsReported": (UC.nameAsReported, "str"), "roleReported": (UC.roleReported, "lang"),
    "defenceStatement": (UC.defenceStatement, "lang"),
    "concerns": (UC.concerns, "refs"), "issueKind": (UC.issueKind, "str"), "issueLocation": (UC.issueLocation, "str"),
    # ---- additions of the second pass (all optional) ----
    "correctionSource": (PROV.wasDerivedFrom, "refs"),      # second JSON key for the same predicate, see build_jsonld
    "correction": (UC.correction, "refs"), "correctedField": (UC.correctedField, "strs"),
    "originalValue": (UC.originalValue, "strs"), "editorNote": (UC.editorNote, "langs"),
    "hidden": (UC.hidden, "bool"), "hiddenReason": (UC.hiddenReason, "lang"),
    "verified": (UC.verified, "bool"), "verifiedMethod": (UC.verifiedMethod, "str"), "verifiedNote": (UC.verifiedNote, "str"),
    "alleged": (UC.alleged, "bool"), "sourceTier": (UC.sourceTier, "str"),
    "sameOperationKey": (UC.sameOperationKey, "str"), "restates": (UC.restates, "ref"),
    # uc:Correction nodes
    "correctsRow": (UC.correctsRow, "ref"), "correctionAction": (UC.correctionAction, "str"),
    "rawField": (UC.rawField, "str"), "newValue": (UC.newValue, "str"), "checkedAgainst": (UC.checkedAgainst, "str"),
    "correctionStatus": (UC.correctionStatus, "str"),
    # chrono.accused fields
    "caseReference": (UC.caseReference, "str"), "detainedOn": (UC.detainedOn, "day"),
    "measureRequested": (UC.measureRequested, "lang"), "measureSource": (UC.measureSource, "ref"),
    "statusSource": (UC.statusSource, "ref"), "nextHearing": (UC.nextHearing, "str"),
    "placeReported": (UC.placeReported, "str"), "previousMeasure": (UC.previousMeasure, "str"),
    # ---- additions of the third pass: analyst opinions (graph "analysis") ----
    "opinionKind": (UC.opinionKind, "str"), "estimateLow": (UC.estimateLow, "dec"),
    "estimateCentral": (UC.estimateCentral, "dec"), "estimateHigh": (UC.estimateHigh, "dec"),
    "basedOn": (UC.basedOn, "refs"),
}
DUAL_TERMS = {"correctionSource"}       # JSON keys that share their predicate with another key

# raw field -> JSON-LD key, for uc:correctedField
FIELD_KEY = {"amount": "amount", "amount_is_approx": "amountIsApproximate", "prov.confidence": "confidence",
             "prov.note": "provenanceNote", "prov.locator": "locator", "prov.quote": "quote", "prov.source": "source",
             "note_en": "note", "note_es": "note", "pct": "percentage", "date": "dateText", "date_precision": "datePrecision",
             "period": "dateText", "title_en": "title", "title_es": "title", "detail_en": "description",
             "detail_es": "description", "borrower": "nominalBorrower", "lender": "lender", "from": "fromParty",
             "to": "toParty", "org": "organisation", "holder": "holder", "label": "label", "role": "roleType",
             "role_reported_en": "roleReported", "role_reported_es": "roleReported", "principal": "principal",
             "outstanding": "outstanding", "currency": "currency", "value": "amount", "entity": "aboutParty",
             "id": "involvesParty", "instrument": "instrument", "category": "eventCategory", "start": "startDate",
             "end": "endDate", "op_number": "operationNumber", "desc_en": "description", "desc_es": "description"}
EDIT_KINDS = ("corrections", "verified", "entity_merges")

# All uc: terms used here are declared in data/ontology.ttl (v0.2.0). The only terms the builder still declares
# itself, in the default graph, are the fallback uc:x_<field> properties for raw fields nobody has mapped yet.
# raw fields handled explicitly per file kind (anything else non-empty becomes a uc:x_<field> literal)
HANDLED = {
    "roles": {"id", "holder", "org", "role", "pct", "start", "end", "note_en", "note_es", "prov"},
    "loans": {"id", "lender", "borrower", "op_number", "kind", "date", "date_precision", "term_years", "term_days",
              "rate_pct", "currency", "principal", "outstanding", "collateral", "amortisation", "status",
              "note_en", "note_es", "prov"},
    "flows": {"id", "from", "to", "amount", "currency", "date", "date_precision", "instrument", "purpose_en",
              "purpose_es", "linked_loan", "amount_is_approx", "prov"},
    "events": {"id", "date", "date_precision", "category", "title_en", "title_es", "detail_en", "detail_es",
               "parties", "amount", "currency", "prov"},
    "facts": {"id", "entity", "metric", "value", "currency", "unit_note", "period", "prov"},
    "issues": {"id", "where", "issue_en", "issue_es", "kind", "concerns", "prov"},
    "accused": {"id", "person", "label", "role_reported_en", "role_reported_es", "company", "offences",
                "offences_added", "measure", "measure_date", "defence_statement_en", "defence_statement_es", "prov",
                "case", "detained", "measure_requested", "measure_source", "status_source", "next_hearing",
                "place_reported", "previous_measure"},
    "entities": {"id", "type", "label", "aliases", "desc_en", "desc_es", "business_en", "business_es", "prov"},
    "opinions": {"id", "kind", "title_en", "title_es", "text_en", "text_es", "low", "central", "high", "currency",
                 "basis_refs", "prov"},
}
KIND_CLASS = {"roles": "RoleHolding", "loans": "Loan", "flows": "Flow", "events": "CaseEvent",
              "facts": "FinancialFact", "issues": "Issue", "accused": "Charge", "entities": "PartyDescription",
              "opinions": "AnalystOpinion"}
KIND_SLUG = {"roles": "role", "loans": "loan", "flows": "flow", "events": "event", "facts": "fact",
             "issues": "issue", "accused": "accused", "entities": "entity", "opinions": "opinion"}
TYPE_ORDER = ["Ontology", "Person", "Organisation", "Authority", "Party", "Source", "RoleHolding", "Loan",
              "Overdraft", "Flow", "CaseEvent", "FinancialFact", "Charge", "Issue", "PartyDescription", "AnalystOpinion", "Correction"]


# =============================================================================================
# Small helpers
# =============================================================================================

class Log:
    """Collects everything the report and merge_report.md need."""

    def __init__(self, quiet=False):
        self.quiet = quiet
        self.warnings = []
        self.dropped = []            # (file, line, row id, reason)
        self.notes = collections.defaultdict(list)

    def warn(self, msg):
        self.warnings.append(msg)
        if not self.quiet:
            print("WARNING: " + msg, file=sys.stderr)

    def drop(self, fname, line, rid, reason):
        self.dropped.append((fname, line, rid or "", reason))
        self.warn("dropped %s line %s (%s): %s" % (fname, line, rid or "no id", reason))

    def note(self, section, msg):
        self.notes[section].append(msg)


def blank(v):
    return v is None or (isinstance(v, str) and not v.strip()) or v == [] or v == {}


def iri_for(sid):
    """SPEC id -> instance IRI: 'org:ueno-bank' -> <.../id/org/ueno-bank>."""
    parts = [re.sub(r"[^A-Za-z0-9_.~\-]", lambda m: "%%%02X" % ord(m.group(0)) if ord(m.group(0)) < 128
                    else "".join("%%%02X" % b for b in m.group(0).encode("utf-8")), p)
             for p in str(sid).strip().split(":")]
    return URIRef(ID + "/".join(parts))


def sid_for(iri):
    s = str(iri)
    return s[len(ID):].replace("/", ":") if s.startswith(ID) else s


def dec_lex(v):
    """Plain decimal lexical form of a JSON number (no exponent, no trailing '.0'); None if not a number."""
    if isinstance(v, bool) or blank(v):
        return None
    try:
        d = Decimal(repr(v)) if isinstance(v, float) else Decimal(str(v).strip().replace(" ", ""))
    except (InvalidOperation, ValueError):
        return None
    if not d.is_finite():
        return None
    if d == d.to_integral_value():
        return str(int(d))
    return format(d.normalize(), "f")


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


_ES = set("de del la el los las en con por para que un una se su al y a o no fue según segun como entre "
          "más mas millones préstamo prestamo sin sobre ya sus es son lo le".split())
_EN = set("the of and with was were by for is are from to in on that this which loan not has had as at its "
          "be been it their they".split())


def guess_lang(text):
    """Language tag for an original-language snippet. Sources are overwhelmingly Spanish; 'en' only when
    English function words clearly dominate."""
    toks = re.findall(r"[a-záéíóúñü]+", text.lower())
    es = sum(t in _ES for t in toks) + (2 if re.search(r"[áéíóúñ¿¡]", text.lower()) else 0)
    en = sum(t in _EN for t in toks)
    return "en" if en > es and en >= 2 else "es"


# ---------------------------------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------------------------------

_PREC_RANK = {"day": 3, "month": 2, "year": 1}
_DT = {"day": XSD.date, "month": XSD.gYearMonth, "year": XSD.gYear}


def _valid(y, m=1, d=1):
    try:
        datetime.date(int(y), int(m), int(d))
        return 1000 <= int(y) <= 2999
    except ValueError:
        return False


def _single(s):
    """One date token -> (lexical, precision) or None."""
    s = s.strip()
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})(?:T[\d:.]+(?:Z|[+-]\d\d:?\d\d)?)?", s) or \
        re.fullmatch(r"(\d{4})/(\d{1,2})/(\d{1,2})", s)
    if m and _valid(*m.groups()):
        return "%04d-%02d-%02d" % tuple(int(x) for x in m.groups()), "day"
    m = re.fullmatch(r"(\d{1,2})[/.](\d{1,2})[/.](\d{4})", s)          # dd/mm/yyyy (Paraguayan usage)
    if m and _valid(m.group(3), m.group(2), m.group(1)):
        return "%04d-%02d-%02d" % (int(m.group(3)), int(m.group(2)), int(m.group(1))), "day"
    m = re.fullmatch(r"(\d{4})-(\d{1,2})", s)
    if m and _valid(m.group(1), m.group(2)) and len(m.group(2)) == 2:
        return "%04d-%02d" % (int(m.group(1)), int(m.group(2))), "month"
    m = re.fullmatch(r"(\d{4})", s)
    if m and _valid(m.group(1)):
        return m.group(1), "year"
    return None


def _quarter(s):
    """'2026-Q1' / '2026Q1' / 'Q1 2026' -> the three-month period as a pair of month tokens."""
    m = re.fullmatch(r"(\d{4})[-\s]?[QqTt]([1-4])", s.strip()) or re.fullmatch(r"[QqTt]([1-4])[-\s]?(\d{4})", s.strip())
    if not m:
        return None
    y, q = (m.group(1), int(m.group(2))) if len(m.group(1)) == 4 else (m.group(2), int(m.group(1)))
    if not _valid(y):
        return None
    return ("%s-%02d" % (y, 3 * q - 2), "month"), ("%s-%02d" % (y, 3 * q), "month")


def _range(s):
    """'2025/2026', '2023-2026', '2025-09/2026-05', '2025 to 2026' -> pair of tokens, else None."""
    for sep in (r"\s*/\s*", r"\s+to\s+", r"\s+a\s+", r"\s*\.\.\s*", r"\s*[–—]\s*", r"\s+-\s+", r"-"):
        bits = re.split(sep, s.strip())
        if len(bits) == 2 and _single(bits[0]) and _single(bits[1]):
            return _single(bits[0]), _single(bits[1])
    return None


def _first_day(lex):
    return (lex + "-01-01")[:10] if len(lex) == 4 else (lex + "-01" if len(lex) == 7 else lex)


def _last_day(lex):
    if len(lex) == 4:
        return lex + "-12-31"
    if len(lex) == 7:
        y, m = int(lex[:4]), int(lex[5:7])
        nxt = datetime.date(y + (m == 12), m % 12 + 1, 1)
        return (nxt - datetime.timedelta(days=1)).isoformat()
    return lex


def _coarsen(lex, prec):
    return lex[:{"day": 10, "month": 7, "year": 4}[prec]]


def norm_date(raw, stated_precision=None):
    """Normalise a date or period string.

    Returns a dict: original, kind ('none' | 'single' | 'range' | 'unparsed'), start, end (lexical forms),
    precision ('day' | 'month' | 'year' | None), sort, sort_end ('YYYY-MM-DD'), flags (list of remarks).
    Accepts 2026-06-15, 2026-06, 2026, 15/06/2026, ranges such as 2025/2026, 2023-2026 or 2025-09/2026-05,
    quarters such as 2026-Q1, and qualifiers such as '2026 (undated)', '2025 (period analysed)' or 'undated (2026)'. A date that is merely mentioned inside free
    text ('undated (list published 2026-11-07)') is NOT taken as the date of the claim.
    """
    out = {"original": None, "kind": "none", "start": None, "end": None, "precision": None,
           "sort": None, "sort_end": None, "flags": []}
    if blank(raw):
        return out
    s = str(raw).strip()
    out["original"] = s
    core = s
    m = re.fullmatch(r"(.*?)\s*\((.*?)\)\s*", s)
    if m:
        head, inner = m.group(1).strip(), m.group(2).strip()
        if head.lower() in ("undated", "n/d", "s/f", "sin fecha", ""):
            core = inner if _single(inner) else ""
            out["flags"].append("undated")
        elif _single(head) or _quarter(head) or _range(head):
            core = head                                   # '2026 (undated)', '2025 (period analysed)'
            if inner.lower() != "undated":
                out["flags"].append("qualifier '%s' kept in dateText" % inner)
    if core.lower() in ("undated", "n/d", "s/f", "sin fecha", "unknown", "none", "null", ""):
        if "undated" not in out["flags"]:
            out["flags"].append("undated")
        return out
    one = _single(core)
    pair = None if one else (_quarter(core) or _range(core))
    if one:
        lex, prec = one
        if stated_precision in _PREC_RANK and _PREC_RANK[stated_precision] < _PREC_RANK[prec]:
            out["flags"].append("stated precision '%s' is coarser than the date; coarsened" % stated_precision)
            prec = stated_precision
            lex = _coarsen(lex, prec)
        elif stated_precision in _PREC_RANK and stated_precision != prec:
            out["flags"].append("stated precision '%s' is finer than the date; '%s' used" % (stated_precision, prec))
        out.update(kind="single", start=lex, precision=prec, sort=_first_day(lex))
    elif pair:
        (a, pa), (b, pb) = pair
        prec = pa if _PREC_RANK[pa] <= _PREC_RANK[pb] else pb
        if _first_day(a) > _first_day(b):
            out["flags"].append("range end precedes start")
        out.update(kind="range", start=a, end=b, precision=prec, sort=_first_day(a), sort_end=_last_day(b))
        out["start_precision"], out["end_precision"] = pa, pb
    else:
        out["kind"] = "unparsed"
    return out


def date_literal(lex):
    return Literal(lex, datatype={10: XSD.date, 7: XSD.gYearMonth, 4: XSD.gYear}[len(lex)])


# ---------------------------------------------------------------------------------------------
# Name normalisation for duplicate detection
# ---------------------------------------------------------------------------------------------

_LEGAL = re.compile(r"\b(s\.?\s?a\.?\s?e\.?\s?c\.?\s?a\.?|s\.?\s?a\.?\s?e\.?|s\.?\s?r\.?\s?l\.?|e\.?\s?a\.?\s?s\.?|"
                    r"s\.?\s?a\.?|ltda\.?|inc\.?|corp\.?|sociedad an[oó]nima)(?=\W|$)", re.I)
_LEGAL_SLUG = {"sa", "saeca", "sae", "srl", "eas", "ltda"}


def norm_name(s):
    s = re.sub(r"\(.*?\)", " ", s)
    s = _LEGAL.sub(" ", s)
    s = strip_accents(s).lower()
    return " ".join(re.findall(r"[a-z0-9]+", s))


def slug_name(sid):
    toks = sid.split(":", 1)[-1].split("-")
    while len(toks) > 1 and toks[-1] in _LEGAL_SLUG:
        toks.pop()
    return " ".join(toks)


def placeholder_label(sid):
    """Display label for a party nobody has described yet; made from the id only."""
    toks = sid.split(":", 1)[-1].split("-")
    if len(toks) == 1 and len(toks[0]) <= 4:
        return toks[0].upper()
    return " ".join(t.capitalize() for t in toks)


# =============================================================================================
# 1. Load
# =============================================================================================

def load_raw(raw_dir, log):
    """Read every *.jsonl in raw_dir. Returns {kind: [(tag, file, line_no, row)]} and a file inventory."""
    rows = collections.defaultdict(list)
    inventory = []
    files = sorted(glob.glob(os.path.join(raw_dir, "*.jsonl")))
    if not files:
        log.warn("no *.jsonl files found in %s" % raw_dir)
    for path in files:
        fname = os.path.basename(path)
        bits = fname[:-len(".jsonl")].split(".")
        if len(bits) != 2:
            log.warn("%s: file name is not <tag>.<kind>.jsonl; skipped" % fname)
            continue
        tag, kind = bits
        if kind != "sources" and kind not in KIND_CLASS and kind not in EDIT_KINDS:
            log.warn("%s: unknown kind '%s'; file skipped" % (fname, kind))
            continue
        n_ok = n_bad = n_blank = 0
        try:
            with open(path, encoding="utf-8-sig", errors="replace") as f:
                lines = f.read().split("\n")
        except OSError as e:
            log.warn("%s: cannot read (%s); skipped" % (fname, e))
            continue
        for i, line in enumerate(lines, 1):
            if not line.strip():
                n_blank += bool(line) or i < len(lines)
                continue
            try:
                obj = json.loads(line)
            except ValueError as e:
                n_bad += 1
                log.drop(fname, i, None, "malformed JSON (%s)" % str(e)[:60])
                continue
            if not isinstance(obj, dict):
                n_bad += 1
                log.drop(fname, i, None, "line is not a JSON object")
                continue
            rows[kind].append((tag, fname, i, obj))
            n_ok += 1
        if n_ok == 0:
            log.note("empty_files", fname)
        inventory.append({"file": fname, "rows": n_ok, "malformed": n_bad})
    return rows, inventory


# =============================================================================================
# 1b. Editor layer: corrections, verification marks, entity merges (applied before any RDF is made)
# =============================================================================================

def _same_value(a, b):
    if blank(a) and blank(b):
        return True
    if isinstance(a, bool) or isinstance(b, bool):
        return a is b
    da, db = dec_lex(a) if not isinstance(a, str) else None, dec_lex(b) if not isinstance(b, str) else None
    if da is not None and db is not None:
        return Decimal(da) == Decimal(db)
    return str(a).strip() == str(b).strip()


def show_value(v):
    if blank(v):
        return "(empty)"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return dec_lex(v)
    if isinstance(v, (list, dict)):
        return json.dumps(v, ensure_ascii=False, sort_keys=True)
    return str(v).strip()


def apply_edits(rows, log):
    """Apply edit.corrections / edit.verified / edit.entity_merges to the loaded rows (in memory only).

    Each data row gets private keys: _edits (applied corrections), _verified, _hidden. Returns a dict with
    the alias map built from the merges and the full list of corrections with their status.
    """
    index = {}
    for kind in KIND_CLASS:
        for tag, fname, line, row in rows.get(kind, []):
            if blank(row.get("id")):
                continue
            if kind == "entities":
                index.setdefault("%s.entities:%s" % (tag, str(row["id"]).strip()), row)
            else:
                index.setdefault(str(row["id"]).strip(), row)
    alias = dict(ALIAS_MAP)
    out = {"alias": alias, "corrections": [], "merge_reasons": {}, "verified": 0, "verified_false": 0,
           "verified_unknown": [], "merge_notes": []}

    def add_alias(frm, to, why):
        frm, to = str(frm).strip(), str(to).strip()
        if frm == to:
            return "not applied: from and to are the same id"
        if alias.get(frm, to) != to:
            return "not applied: %s is already merged into %s" % (frm, alias[frm])
        known = frm in alias
        alias[frm] = to
        out["merge_reasons"].setdefault(frm, why)
        return "already applied" if known else "applied"

    for tag, fname, line, m in rows.get("entity_merges", []):
        if blank(m.get("from")) or blank(m.get("to")):
            log.drop(fname, line, None, "entity merge without from / to")
            continue
        st = add_alias(m["from"], m["to"], str(m.get("reason") or ""))
        out["merge_notes"].append("`%s` -> `%s` (%s): %s" % (m["from"], m["to"], st, str(m.get("reason") or "")))

    for tag, fname, line, c in rows.get("corrections", []):
        cid = str(c.get("id") or "%s:corr:line%04d" % (tag, line))
        action, field, target = str(c.get("action") or ""), str(c.get("field") or ""), str(c.get("target_row") or "")
        rec = {"id": cid, "c": c, "target": target, "status": None, "row": index.get(target)}
        out["corrections"].append(rec)
        row = rec["row"]
        prov = c.get("prov") if isinstance(c.get("prov"), dict) else {}
        if blank(prov.get("source")) or str(prov.get("asserted_by") or "").lower() not in ASSERTER_CONCEPT \
                or str(prov.get("confidence") or "").lower() not in CONFIDENCES:
            rec["status"] = "not applied: correction has no complete prov block"
            continue
        if row is None:
            rec["status"] = "not applied: target row %s not found" % (target or "(none)")
            continue
        if action == "merge_entity":
            st = add_alias(c.get("old") if not blank(c.get("old")) else row.get("id"), c.get("new"), str(c.get("reason_en") or ""))
            rec["status"] = "applied" if st in ("applied", "already applied") else st
            if rec["status"] == "applied":
                row.setdefault("_edits", []).append(rec)
            continue
        if action == "delete_row":
            row["_hidden"] = (str(c.get("reason_en") or "Marked for deletion by the editor."),
                              str(c.get("reason_es") or c.get("reason_en") or "Marcada para eliminación por el editor."))
            rec["status"] = "applied"
            row.setdefault("_edits", []).append(rec)
            continue
        if action not in ("set", "set_confidence", "add_note"):
            rec["status"] = "not applied: unknown action %r" % action
            continue
        if action == "set_confidence":
            field = field or "prov.confidence"
            if str(c.get("new") or "").lower() not in CONFIDENCES:
                rec["status"] = "not applied: new confidence %r is not high / medium / low" % c.get("new")
                continue
        if not field:
            rec["status"] = "not applied: no field given"
            continue
        holder, key = (row.get("prov"), field[5:]) if field.startswith("prov.") else (row, field)
        if not isinstance(holder, dict):
            rec["status"] = "not applied: target row has no prov block"
            continue
        cur = holder.get(key)
        if _same_value(cur, c.get("new")) and not _same_value(cur, c.get("old")):
            rec["status"] = "not applied: the row already has the new value"
            continue
        if "old" in c and not _same_value(cur, c.get("old")):
            rec["status"] = "not applied: current value %s differs from the correction's old value %s" % (
                show_value(cur)[:60], show_value(c.get("old"))[:60])
            continue
        rec["old_value"] = cur
        holder[key] = c.get("new")
        rec["status"] = "applied"
        row.setdefault("_edits", []).append(rec)

    for tag, fname, line, v in rows.get("verified", []):
        row = index.get(str(v.get("row") or "").strip())
        if row is None:
            out["verified_unknown"].append(str(v.get("row")))
            continue
        row["_verified"] = (v.get("verified") is True, str(v.get("method") or "").strip(), str(v.get("note") or "").strip())
        out["verified" if v.get("verified") is True else "verified_false"] += 1

    # resolve alias chains
    for k in list(alias):
        seen, t = {k}, alias[k]
        while t in alias and alias[t] not in seen:
            seen.add(t)
            t = alias[t]
        alias[k] = t
    for rid, reason in sorted(HIDDEN_ROWS.items()):
        if rid in index:
            index[rid].setdefault("_hidden", reason)
        else:
            log.note("oddities", "HIDDEN_ROWS names %s, which is not in the raw data" % rid)
    return out


# =============================================================================================
# 2. Build
# =============================================================================================

class Builder:
    def __init__(self, rows, log, edits=None):
        self.rows = rows
        self.log = log
        self.edits = edits or {"alias": dict(ALIAS_MAP), "corrections": [], "merge_reasons": {}, "verified": 0,
                               "verified_false": 0, "verified_unknown": [], "merge_notes": []}
        self.alias = self.edits["alias"]
        self.corr_sources = collections.defaultdict(set)     # node -> sources added by corrections
        self.primary_source = {}                             # node -> the row's own source
        self.verified_ids = []
        self.ds = Dataset()
        self.default = self.ds.default_graph if hasattr(self.ds, "default_graph") else self.ds.default_context
        self.graphs = {g: self.ds.graph(URIRef(ID + "graph/" + g)) for g in GRAPH_NAMES}
        self.sources = {}                 # sid -> row
        self.entities = {}                # sid -> merged entity
        self.stubs = collections.defaultdict(list)       # sid -> [row ids that reference it]
        self.stub_sources = collections.defaultdict(list)
        self.assertions = {}              # row id -> dict(kind, graph, asserter, iri, row)
        self.used_sources = collections.Counter()
        self.alias_applied = collections.Counter()
        self.unmapped = collections.Counter()
        self.x_terms = {}                 # extra term -> kind
        self.enum_unknown = collections.Counter()
        self.currencies = set()
        self.date_notes = []
        self.loans = {}                   # row id -> info for derivations
        self.flows = {}
        self.derived = collections.Counter()
        self.second_hand = collections.Counter()

    # ----- generic ---------------------------------------------------------------------------
    def canon(self, sid, ctx=None):
        sid = str(sid).strip()
        if sid in self.alias:
            self.alias_applied[(sid, self.alias[sid])] += 1
            return self.alias[sid]
        return sid

    def party(self, sid, used_by):
        """IRI of a party reference; registers a stub when no contributor has described the entity."""
        sid = self.canon(sid)
        if sid not in self.entities:
            self.stubs[sid].append(used_by)
        return iri_for(sid)

    def add(self, g, s, p, o):
        g.add((s, p, o))

    def lang_pair(self, g, s, p, row, base):
        for lg in ("en", "es"):
            v = row.get("%s_%s" % (base, lg))
            if not blank(v):
                g.add((s, p, Literal(str(v).strip(), lang=lg)))

    def add_date(self, g, s, raw, stated, rid, prop=None):
        """Attach a normalised date or period to an assertion; returns the normalised dict."""
        d = norm_date(raw, stated)
        if d["original"] is None:
            return d
        g.add((s, UC.dateText, Literal(d["original"])))
        if d["kind"] == "single":
            g.add((s, prop or UC.onDate, date_literal(d["start"])))
        elif d["kind"] == "range":
            g.add((s, UC.startDate, date_literal(d["start"])))
            g.add((s, UC.endDate, date_literal(d["end"])))
        if d["precision"]:
            g.add((s, UC.datePrecision, Literal(d["precision"])))
        if d["sort"]:
            g.add((s, UC.sortDate, Literal(d["sort"], datatype=XSD.date)))
        if d["sort_end"]:
            g.add((s, UC.sortDateEnd, Literal(d["sort_end"], datatype=XSD.date)))
        if d["kind"] == "unparsed":
            self.date_notes.append("%s: date string %r could not be normalised; kept as dateText only" % (rid, d["original"]))
        elif d["kind"] == "none":
            pass
        for fl in d["flags"]:
            if fl not in ("undated",):
                self.date_notes.append("%s: %r - %s" % (rid, d["original"], fl))
        if d["sort"] and d["sort"] > CUTOFF:
            self.log.note("oddities", "%s: date %s is after the %s cutoff (fine if it is a maturity or a projection)" % (rid, d["original"], CUTOFF))
        return d

    def add_money(self, g, s, prop, value, rid, field):
        if blank(value):
            return None
        lex = dec_lex(value)
        if lex is None:
            self.log.note("oddities", "%s: %s %r is not a number; kept as text in uc:x_%s" % (rid, field, value, field))
            self.extra(g, s, field, value)
            return None
        g.add((s, prop, Literal(lex, datatype=XSD.decimal)))
        return Decimal(lex)

    def add_currency(self, g, s, value, rid):
        if blank(value):
            return None
        code = str(value).strip().upper()
        if not re.fullmatch(r"[A-Z]{3}", code):
            self.log.note("oddities", "%s: currency %r is not an ISO 4217 code; kept as text" % (rid, value))
            self.extra(g, s, "currency", value)
            return None
        if code not in ("PYG", "USD"):
            self.log.note("oddities", "%s: currency %s is outside the SPEC enumeration (PYG, USD); kept" % (rid, code))
        self.currencies.add(code)
        g.add((s, UC.currency, CUR[code]))
        return code

    def enum(self, g, s, prop, prefix, value, rid, known):
        if blank(value):
            return
        v = re.sub(r"[^a-z0-9_]", "_", str(value).strip().lower())
        if known and (prefix + v) not in known:
            self.enum_unknown[(prefix + v, str(prop).split("#")[-1])] += 1
        g.add((s, prop, UC[prefix + v]))

    def extra(self, g, s, key, value):
        """Unmapped raw field -> literal(s) on uc:x_<key>, so nothing is silently lost."""
        term = "x_" + re.sub(r"[^A-Za-z0-9_]", "_", key)
        vals = value if isinstance(value, list) else [value]
        for v in vals:
            if blank(v):
                continue
            if isinstance(v, bool):
                v = "true" if v else "false"
            elif isinstance(v, (dict, list)):
                v = json.dumps(v, ensure_ascii=False, sort_keys=True)
            g.add((s, UC[term], Literal(str(v))))
            self.x_terms[term] = "strs"
            self.unmapped[key] += 1

    def extras(self, g, s, row, kind):
        handled = HANDLED[kind]
        keys = [k for k in sorted(row) if k not in handled and not k.startswith("_") and not blank(row[k])]
        done = set()
        for k in keys:
            if k in done:
                continue
            m = re.fullmatch(r"(.+)_(en|es)", k)
            if m and isinstance(row[k], str):
                base = m.group(1)
                term = "x_" + re.sub(r"[^A-Za-z0-9_]", "_", base)
                for lg in ("en", "es"):
                    kk = "%s_%s" % (base, lg)
                    if kk in row and kk not in handled and isinstance(row[kk], str) and not blank(row[kk]):
                        g.add((s, UC[term], Literal(row[kk].strip(), lang=lg)))
                        done.add(kk)
                        self.unmapped[kk] += 1
                self.x_terms[term] = "lang"
            else:
                self.extra(g, s, k, row[k])

    def references(self, sid):
        """True when some data row refers to the entity id (after aliasing)."""
        if not hasattr(self, "_refs"):
            refs = set()
            for kind, keys in (("roles", ("holder", "org")), ("loans", ("lender", "borrower")), ("flows", ("from", "to")),
                               ("facts", ("entity",)), ("accused", ("person", "company")), ("events", ("parties",))):
                for _, _, _, row in self.rows.get(kind, []):
                    for k in keys:
                        v = row.get(k)
                        for x in (v if isinstance(v, list) else [v]):
                            if isinstance(x, str) and x.strip():
                                refs.add(self.alias.get(x.strip(), x.strip()))
            self._refs = refs
        return sid in self._refs

    def tier(self, src):
        """uc:sourceTier of an assertion, from its own source."""
        row = self.sources.get(src, {}).get("row", {})
        kind = str(row.get("kind") or "")
        if src.startswith("src:acta-"):
            return "record"
        if src.startswith("src:dossier-") or kind == "dossier":
            return "dossier"
        if kind in ("rating", "official"):
            return "rating_or_official"
        if not blank(row.get("url")):
            return "press_linked"
        return "editorial" if src == EDITORIAL_SOURCE["id"] else "unlinked"

    # ----- sources ---------------------------------------------------------------------------
    def build_sources(self):
        for tag, fname, line, row in self.rows.get("sources", []):
            sid = row.get("id")
            if blank(sid):
                self.log.drop(fname, line, None, "source row without id")
                continue
            sid = str(sid).strip()
            if sid in self.sources:
                if self.sources[sid]["row"] != row:
                    self.log.note("source_conflicts", "%s is defined twice with different content (%s kept, %s line %d ignored)"
                                  % (sid, self.sources[sid]["file"], fname, line))
                continue
            for pre, kind in SOURCE_KIND_BY_PREFIX.items():
                if sid.startswith(pre) and row.get("kind") != kind:
                    self.log.note("source_kinds", "%s: kind %r replaced by %r" % (sid, row.get("kind"), kind))
                    row = dict(row, kind=kind)
            self.sources[sid] = {"row": row, "file": fname, "tag": tag}
        described = {self.canon(r[3].get("id")) for r in self.rows.get("entities", []) if not blank(r[3].get("id"))}
        self.editorial = sorted(e for e in EDITORIAL_ENTITIES if e not in described and self.references(e))
        if self.editorial and EDITORIAL_SOURCE["id"] not in self.sources:
            self.sources[EDITORIAL_SOURCE["id"]] = {"row": dict(EDITORIAL_SOURCE), "file": "(build_graph.py)", "tag": "edit"}
        g = self.default
        for sid in sorted(self.sources):
            row = self.sources[sid]["row"]
            s = iri_for(sid)
            g.add((s, RDF.type, UC.Source))
            g.add((s, DCTERMS.identifier, Literal(sid)))
            for key, prop in (("kind", UC.sourceKind), ("outlet", UC.outlet), ("title", SCHEMA.name)):
                if not blank(row.get(key)):
                    g.add((s, prop, Literal(str(row[key]).strip())))
            if not blank(row.get("url")):
                url = str(row["url"]).strip()
                if re.match(r"https?://\S+$", url) or re.fullmatch(r"[A-Za-z0-9_./\-]+\.[A-Za-z0-9]+", url):
                    g.add((s, SCHEMA.url, Literal(url, datatype=XSD.anyURI)))
                else:
                    self.log.note("oddities", "%s: url %r is not an http(s) URL; kept as provenanceNote" % (sid, url))
                    g.add((s, UC.provenanceNote, Literal("url as given: " + url)))
            page = row.get("page")
            if isinstance(page, int) and not isinstance(page, bool):
                g.add((s, UC.page, Literal(page)))
            elif isinstance(page, str) and page.strip().isdigit():
                g.add((s, UC.page, Literal(int(page.strip()))))
            elif not blank(page):
                g.add((s, UC.provenanceNote, Literal(str(page).strip())))
            d = norm_date(row.get("date"))
            if d["kind"] == "single":
                g.add((s, DCTERMS.date, date_literal(d["start"])))
                g.add((s, UC.sortDate, Literal(d["sort"], datatype=XSD.date)))
                g.add((s, UC.datePrecision, Literal(d["precision"])))
                if d["sort"] > CUTOFF:
                    self.log.note("oddities", "%s: source date %s is after the %s cutoff" % (sid, d["original"], CUTOFF))
            elif d["original"]:
                g.add((s, UC.dateText, Literal(d["original"])))
                self.date_notes.append("%s: source date %r could not be normalised to one date" % (sid, d["original"]))
            else:
                self.log.note("oddities", "%s: source has no date" % sid)
            if blank(row.get("url")) and blank(row.get("page")) and sid != EDITORIAL_SOURCE["id"]:
                self.log.note("oddities", "%s: source has neither a URL nor a record page" % sid)
            for k in sorted(row):
                if k not in ("id", "kind", "outlet", "title", "date", "url", "page") and not blank(row[k]):
                    self.extra(g, s, k, row[k])

    # ----- entities --------------------------------------------------------------------------
    def build_entities(self):
        per = collections.defaultdict(list)
        for tag, fname, line, row in self.rows.get("entities", []):
            sid = row.get("id")
            if blank(sid):
                self.log.drop(fname, line, None, "entity row without id")
                continue
            per[self.canon(sid)].append((tag, fname, line, row))
        for sid in self.editorial:
            cls, label = EDITORIAL_ENTITIES[sid]
            row = {"id": sid, "type": cls, "label": label, "aliases": [], "desc_en": "", "desc_es": "",
                   "prov": {"asserted_by": "press", "source": EDITORIAL_SOURCE["id"], "locator": "Entity IDs",
                            "quote": "", "confidence": "high",
                            "note": "Editorial label for an id of the SPEC.md id list that no contributor has described."}}
            per[sid].append(("edit", "(build_graph.py EDITORIAL_ENTITIES)", 0, row))

        def prio(item):
            tag = item[0]
            return (LABEL_PRIORITY.index(tag) if tag in LABEL_PRIORITY else len(LABEL_PRIORITY), tag, item[1], item[2])

        for sid in sorted(per):
            items = sorted(per[sid], key=prio)
            types = []
            for tag, fname, line, row in items:
                t = ENTITY_CLASS.get(str(row.get("type", "")).strip())
                if t is None:
                    t = PREFIX_CLASS.get(sid.split(":")[0], "Party")
                    self.log.note("entity_conflicts", "%s: type %r in %s is not Person / Company / Authority; %s used"
                                  % (sid, row.get("type"), fname, t))
                types.append(t)
            cls = types[0]
            if len(set(types)) > 1:
                self.log.note("entity_conflicts", "%s: contributors disagree on the type (%s); %s kept"
                              % (sid, ", ".join("%s=%s" % (i[0], t) for i, t in zip(items, types)), cls))
            expect = PREFIX_CLASS.get(sid.split(":")[0])
            if expect and expect != cls:
                self.log.note("entity_conflicts", "%s: id prefix suggests %s but the row says %s" % (sid, expect, cls))
            labels = []
            for tag, fname, line, row in items:
                for v in [row.get("label")] + (row.get("aliases") if isinstance(row.get("aliases"), list) else [row.get("aliases")]):
                    if not blank(v) and str(v).strip() not in labels:
                        labels.append(str(v).strip())
            label = labels[0] if labels else slug_name(sid)
            # same spelling with and without accents: the accented one is the label
            fold = lambda x: strip_accents(x).lower()
            accents = lambda x: sum(1 for ch in x if ord(ch) > 127)
            for cand in [str(i[3].get("label") or "").strip() for i in items]:
                if cand and fold(cand) == fold(label) and accents(cand) > accents(label):
                    label = cand
            if sid in LABEL_OVERRIDES:
                label, add_alt, drop_alt = LABEL_OVERRIDES[sid]
                labels = [x for x in labels if x not in drop_alt] + [x for x in add_alt if x not in labels]
            for i in items:                              # labels replaced by the editor stay as altLabels
                for e in i[3].get("_edits", []):
                    if e["c"].get("field") == "label" and not blank(e.get("old_value")) and str(e["old_value"]).strip() not in labels:
                        labels.append(str(e["old_value"]).strip())
            ent = {"id": sid, "class": cls, "label": label,
                   "alt": sorted(x for x in labels if x != label), "rows": items, "tags": sorted({i[0] for i in items})}
            if len(items) > 1:
                differ = len({str(i[3].get("label", "")).strip() for i in items if not blank(i[3].get("label"))}) > 1
                self.log.note("entity_merges", "`%s` (%s)%s" % (sid, ", ".join(i[0] for i in items),
                              ": labels differ - " + " / ".join("%s: \"%s\"" % (i[0], i[3].get("label")) for i in items)
                              + "; the first is the label, the others are altLabels" if differ else ""))
            self.entities[sid] = ent

        g = self.default
        for sid in sorted(self.entities):
            ent = self.entities[sid]
            s = iri_for(sid)
            g.add((s, RDF.type, UC[ent["class"]]))
            if sid in EXTRA_PARTY_TYPES:
                g.add((s, RDF.type, EXTERNAL_CLASSES[EXTRA_PARTY_TYPES[sid]]))
            g.add((s, DCTERMS.identifier, Literal(sid)))
            g.add((s, RDFS.label, Literal(ent["label"])))
            for a in ent["alt"]:
                g.add((s, SKOS.altLabel, Literal(a)))
            # description / business of the party node: first non-empty value in contributor priority order
            for base, prop in (("desc", DCTERMS.description), ("business", UC.business)):
                for lg in ("en", "es"):
                    for tag, fname, line, row in ent["rows"]:
                        v = row.get("%s_%s" % (base, lg))
                        if not blank(v):
                            g.add((s, prop, Literal(str(v).strip(), lang=lg)))
                            break

    def build_party_descriptions(self):
        """One uc:PartyDescription per entity row, in the asserter's graph, so entity provenance is kept."""
        seen = collections.Counter()
        for sid in sorted(self.entities):
            for tag, fname, line, row in self.entities[sid]["rows"]:
                base = "%s:entity:%s" % (tag, str(row.get("id") or sid).strip().replace(":", "-"))
                seen[base] += 1
                rid = base if seen[base] == 1 else "%s-%d" % (base, seen[base])
                reg = self.register(rid, "entities", tag, fname, line, row)
                if not reg:
                    continue
                g, s = reg
                g.add((s, UC.involvesParty, iri_for(sid)))
                if not blank(row.get("label")):
                    g.add((s, RDFS.label, Literal(str(row["label"]).strip())))
                for a in (row.get("aliases") or []) if isinstance(row.get("aliases"), list) else []:
                    if not blank(a):
                        g.add((s, SKOS.altLabel, Literal(str(a).strip())))
                self.lang_pair(g, s, DCTERMS.description, row, "desc")
                self.lang_pair(g, s, UC.business, row, "business")
                self.extras(g, s, row, "entities")

    # ----- provenance / registration ---------------------------------------------------------
    def register(self, rid, kind, tag, fname, line, row):
        """Validate id + prov, create the assertion node with its provenance. Returns (graph, iri) or None."""
        if blank(rid):
            rid = "%s:%s:line%04d" % (tag, KIND_SLUG[kind], line)
            self.log.note("oddities", "%s line %d: row has no id; %s minted" % (fname, line, rid))
        rid = str(rid).strip()
        prov = row.get("prov")
        if not isinstance(prov, dict):
            self.log.drop(fname, line, rid, "no prov block")
            return None
        by = str(prov.get("asserted_by") or "").strip().lower()
        if by not in ASSERTER_CONCEPT:
            self.log.drop(fname, line, rid, "prov.asserted_by missing or unknown (%r)" % prov.get("asserted_by"))
            return None
        if blank(prov.get("source")):
            self.log.drop(fname, line, rid, "prov.source missing")
            return None
        conf = str(prov.get("confidence") or "").strip().lower()
        if conf not in CONFIDENCES:
            self.log.drop(fname, line, rid, "prov.confidence missing or not high/medium/low (%r)" % prov.get("confidence"))
            return None
        if rid in self.assertions:
            if self.assertions[rid]["row"] == row:
                self.log.note("oddities", "%s line %d: exact duplicate of row %s; ignored" % (fname, line, rid))
            else:
                self.log.drop(fname, line, rid, "row id already used by a different row in %s" % self.assertions[rid]["file"])
            return None
        src = str(prov["source"]).strip()
        if src not in self.sources:
            self.stub_sources[src].append(rid)
        self.used_sources[src] += 1
        if kind == "opinions" and by != "analyst":
            self.log.note("oddities", "%s: analyst opinion with asserted_by %r; recorded as analyst" % (rid, by))
            by = "analyst"
        gname = ANALYSIS_GRAPH if kind == "opinions" else GRAPH_OF_ASSERTER[by]
        first_hand = src.startswith("src:acta-")
        if gname in ("prosecution", "rey") and not first_hand:
            self.second_hand[by] += 1
            if SECOND_HAND_TO_PRESS:
                gname = "press"
        g = self.graphs[gname]
        s = iri_for(rid)
        g.add((s, RDF.type, UC[KIND_CLASS[kind]]))
        g.add((s, DCTERMS.identifier, Literal(rid)))
        g.add((s, PROV.wasDerivedFrom, iri_for(src)))
        g.add((s, UC.assertedBy, UC[ASSERTER_CONCEPT[by]]))
        g.add((s, UC.confidence, Literal(conf)))
        if not blank(prov.get("locator")):
            g.add((s, UC.locator, Literal(str(prov["locator"]).strip())))
        if not blank(prov.get("quote")):
            q = str(prov["quote"]).strip()
            g.add((s, UC.quote, Literal(q, lang=guess_lang(q))))
            if len(q.split()) > MAX_QUOTE_WORDS:
                self.log.note("oddities", "%s: quote has %d words (SPEC limit %d)" % (rid, len(q.split()), MAX_QUOTE_WORDS))
        if not blank(prov.get("note")):
            g.add((s, UC.provenanceNote, Literal(str(prov["note"]).strip())))
        for k in sorted(prov):
            if k not in ("asserted_by", "source", "locator", "quote", "confidence", "note") and not blank(prov[k]):
                self.extra(g, s, "prov_" + k, prov[k])
        self.primary_source[s] = iri_for(src)
        tier = "analysis" if kind == "opinions" else self.tier(src)
        g.add((s, UC.sourceTier, Literal(tier)))
        if kind in ("flows", "events") and gname in ("prosecution", "rey"):
            g.add((s, UC.alleged, Literal(True)))
        hidden = row.get("_hidden")
        if hidden:
            g.add((s, UC.hidden, Literal(True)))
            g.add((s, UC.hiddenReason, Literal(hidden[0], lang="en")))
            g.add((s, UC.hiddenReason, Literal(hidden[1], lang="es")))
        if row.get("_verified"):
            ok, method, vnote = row["_verified"]
            g.add((s, UC.verified, Literal(ok)))
            if method:
                g.add((s, UC.verifiedMethod, Literal(method)))
            if vnote:
                g.add((s, UC.verifiedNote, Literal(vnote)))
            if ok:
                self.verified_ids.append(rid)
        for e in row.get("_edits", []):
            c = e["c"]
            e["node"] = s
            key = FIELD_KEY.get(str(c.get("field") or ""), str(c.get("field") or c.get("action")))
            if c.get("action") == "delete_row":
                key = "hidden"
            g.add((s, UC.correction, iri_for(e["id"])))
            g.add((s, UC.correctedField, Literal(key)))
            if c.get("action") != "delete_row":
                old = c.get("old") if c.get("action") == "merge_entity" else e.get("old_value")
                g.add((s, UC.originalValue, Literal("%s: %s" % (key, show_value(old)))))
            for lg in ("en", "es"):
                if not blank(c.get("reason_" + lg)):
                    g.add((s, UC.editorNote, Literal(str(c["reason_" + lg]).strip(), lang=lg)))
            csrc = str(c["prov"]["source"]).strip()
            if csrc not in self.sources:
                self.stub_sources[csrc].append(e["id"])
            g.add((s, PROV.wasDerivedFrom, iri_for(csrc)))
            self.corr_sources[s].add(iri_for(csrc))
        self.assertions[rid] = {"kind": kind, "graph": gname, "asserter": by, "iri": s, "row": row, "file": fname,
                                "tag": tag, "source": src, "confidence": conf, "tier": tier, "hidden": bool(hidden)}
        return g, s

    def need(self, row, keys, fname, line):
        missing = [k for k in keys if blank(row.get(k))]
        if missing:
            self.log.drop(fname, line, row.get("id"), "required field(s) missing: " + ", ".join(missing))
            return False
        return True

    # ----- assertion kinds -------------------------------------------------------------------
    def build_roles(self, known):
        for tag, fname, line, row in self.rows.get("roles", []):
            if not self.need(row, ("holder", "org", "role"), fname, line):
                continue
            reg = self.register(row.get("id"), "roles", tag, fname, line, row)
            if not reg:
                continue
            g, s = reg
            rid = sid_for(s)
            h, o = self.party(row["holder"], rid), self.party(row["org"], rid)
            g.add((s, UC.holder, h))
            g.add((s, UC.organisation, o))
            g.add((s, UC.involvesParty, h))
            g.add((s, UC.involvesParty, o))
            self.enum(g, s, UC.roleType, "role_", row["role"], rid, known)
            pct = self.add_money(g, s, UC.percentage, row.get("pct"), rid, "pct")
            if pct is not None and not (0 <= pct <= 100):
                self.log.note("oddities", "%s: percentage %s is outside 0-100" % (rid, pct))
            ds = norm_date(row.get("start"))
            de = norm_date(row.get("end"))
            for d, prop, textprop, nm in ((ds, UC.startDate, UC.startDateText, "start"), (de, UC.endDate, UC.endDateText, "end")):
                if d["kind"] == "single":
                    g.add((s, prop, date_literal(d["start"])))
                    if d["original"] != d["start"]:
                        g.add((s, textprop, Literal(d["original"])))
                elif d["original"]:
                    g.add((s, textprop, Literal(d["original"])))
                    self.date_notes.append("%s: role %s %r is not a single date; kept as text only" % (rid, nm, d["original"]))
            if ds["kind"] == "single":
                g.add((s, UC.sortDate, Literal(ds["sort"], datatype=XSD.date)))
            if de["kind"] == "single":
                g.add((s, UC.sortDateEnd, Literal(_last_day(de["start"]), datatype=XSD.date)))
            if ds["kind"] == "single" and de["kind"] == "single" and ds["sort"] > _last_day(de["start"]):
                self.log.note("oddities", "%s: role ends (%s) before it starts (%s)" % (rid, de["original"], ds["original"]))
            self.lang_pair(g, s, SKOS.note, row, "note")
            self.extras(g, s, row, "roles")

    def build_loans(self):
        for tag, fname, line, row in self.rows.get("loans", []):
            if not self.need(row, ("lender", "borrower"), fname, line):
                continue
            reg = self.register(row.get("id"), "loans", tag, fname, line, row)
            if not reg:
                continue
            g, s = reg
            rid = sid_for(s)
            kind = str(row.get("kind") or "loan").strip().lower()
            if kind == "overdraft":
                g.remove((s, RDF.type, UC.Loan))
                g.add((s, RDF.type, UC.Overdraft))
                g.add((s, RDF.type, UC.Loan))        # stated explicitly so plain SPARQL finds overdrafts as loans
            elif kind != "loan":
                self.log.note("oddities", "%s: loan kind %r is not loan/overdraft; typed uc:Loan" % (rid, row.get("kind")))
                self.extra(g, s, "kind", row.get("kind"))
            lender, borrower = self.party(row["lender"], rid), self.party(row["borrower"], rid)
            g.add((s, UC.lender, lender))
            g.add((s, UC.nominalBorrower, borrower))
            g.add((s, UC.involvesParty, lender))
            g.add((s, UC.involvesParty, borrower))
            if not blank(row.get("op_number")):
                g.add((s, UC.operationNumber, Literal(str(row["op_number"]).strip())))
            self.add_date(g, s, row.get("date"), row.get("date_precision"), rid)
            principal = self.add_money(g, s, UC.principal, row.get("principal"), rid, "principal")
            outstanding = self.add_money(g, s, UC.outstanding, row.get("outstanding"), rid, "outstanding")
            self.add_money(g, s, UC.ratePct, row.get("rate_pct"), rid, "rate_pct")
            self.add_money(g, s, UC.termYears, row.get("term_years"), rid, "term_years")
            td = row.get("term_days")
            if isinstance(td, int) and not isinstance(td, bool):
                g.add((s, UC.termDays, Literal(td)))
            elif not blank(td):
                self.extra(g, s, "term_days", td)
            cur = self.add_currency(g, s, row.get("currency"), rid)
            for key, prop in (("collateral", UC.collateral), ("amortisation", UC.amortisation), ("status", UC.loanStatus)):
                if not blank(row.get(key)):
                    g.add((s, prop, Literal(str(row[key]).strip())))
            if str(row.get("collateral") or "").strip().lower() == "none":
                g.add((s, RDF.type, LN.UnsecuredLoan))
            self.lang_pair(g, s, SKOS.note, row, "note")
            self.extras(g, s, row, "loans")
            if (principal is not None or outstanding is not None) and cur is None:
                self.log.note("oddities", "%s: amount without currency" % rid)
            if principal is not None and principal <= 0:
                self.log.note("oddities", "%s: principal %s is not positive" % (rid, principal))
            if principal is not None and outstanding is not None and outstanding > principal and kind == "loan":
                self.log.note("oddities", "%s: outstanding %s exceeds principal %s" % (rid, outstanding, principal))
            if str(row.get("status") or "").lower() == "cancelled" and outstanding not in (None, Decimal(0)):
                self.log.note("oddities", "%s: status 'cancelled' but outstanding is %s" % (rid, outstanding))
            if lender == borrower:
                self.log.note("oddities", "%s: lender and borrower are the same party" % rid)
            self.loans[rid] = {"iri": s, "g": g, "lender": lender, "borrower": borrower, "principal": principal,
                               "outstanding": outstanding, "currency": cur, "kind": kind,
                               "op": str(row.get("op_number") or "").strip(), "asserter": self.assertions[rid]["asserter"]}

    def build_flows(self, known):
        for tag, fname, line, row in self.rows.get("flows", []):
            if not self.need(row, ("from", "to"), fname, line):
                continue
            reg = self.register(row.get("id"), "flows", tag, fname, line, row)
            if not reg:
                continue
            g, s = reg
            rid = sid_for(s)
            a, b = self.party(row["from"], rid), self.party(row["to"], rid)
            g.add((s, UC.fromParty, a))
            g.add((s, UC.toParty, b))
            g.add((s, UC.involvesParty, a))
            g.add((s, UC.involvesParty, b))
            amount = self.add_money(g, s, UC.amount, row.get("amount"), rid, "amount")
            cur = self.add_currency(g, s, row.get("currency"), rid)
            d = self.add_date(g, s, row.get("date"), row.get("date_precision"), rid)
            self.enum(g, s, UC.instrument, "instr_", row.get("instrument"), rid, known)
            self.lang_pair(g, s, UC.purpose, row, "purpose")
            if isinstance(row.get("amount_is_approx"), bool):
                g.add((s, UC.amountIsApproximate, Literal(row["amount_is_approx"])))
            elif not blank(row.get("amount_is_approx")):
                self.extra(g, s, "amount_is_approx", row["amount_is_approx"])
            self.extras(g, s, row, "flows")
            if amount is not None and cur is None:
                self.log.note("oddities", "%s: amount without currency" % rid)
            if amount is not None and amount <= 0:
                self.log.note("oddities", "%s: amount %s is not positive" % (rid, amount))
            if a == b:
                self.log.note("oddities", "%s: flow from a party to itself (%s)" % (rid, sid_for(a)))
            self.flows[rid] = {"iri": s, "g": g, "from": a, "to": b, "amount": amount, "currency": cur,
                               "date": d["start"] if d["kind"] == "single" else d["original"],
                               "instrument": str(row.get("instrument") or ""),
                               "linked": None if blank(row.get("linked_loan")) else str(row["linked_loan"]).strip(),
                               "asserter": self.assertions[rid]["asserter"], "source": self.assertions[rid]["source"]}

    def link_flows_to_loans(self):
        for rid in sorted(self.flows):
            f = self.flows[rid]
            if not f["linked"]:
                continue
            if f["linked"] in self.loans:
                f["g"].add((f["iri"], UC.linkedLoan, self.loans[f["linked"]]["iri"]))
            else:
                self.log.note("unknown_refs", "%s: linked_loan %s is not a known loan row; kept as text in uc:x_linked_loan"
                              % (rid, f["linked"]))
                self.extra(f["g"], f["iri"], "linked_loan", f["linked"])
                f["linked"] = None

    def build_events(self, known):
        for tag, fname, line, row in self.rows.get("events", []):
            reg = self.register(row.get("id"), "events", tag, fname, line, row)
            if not reg:
                continue
            g, s = reg
            rid = sid_for(s)
            d = self.add_date(g, s, row.get("date"), row.get("date_precision"), rid)
            if d["kind"] in ("none", "unparsed"):
                self.log.note("oddities", "%s: event without a usable date" % rid)
            self.enum(g, s, UC.eventCategory, "cat_", row.get("category"), rid, known)
            self.lang_pair(g, s, DCTERMS.title, row, "title")
            self.lang_pair(g, s, DCTERMS.description, row, "detail")
            parties = row.get("parties") or []
            if not isinstance(parties, list):
                parties = [parties]
            for p in parties:
                if not blank(p):
                    g.add((s, UC.involvesParty, self.party(p, rid)))
            amount = self.add_money(g, s, UC.amount, row.get("amount"), rid, "amount")
            cur = self.add_currency(g, s, row.get("currency"), rid)
            if amount is not None and cur is None:
                self.log.note("oddities", "%s: amount without currency" % rid)
            if blank(row.get("title_en")) and blank(row.get("title_es")):
                self.log.note("oddities", "%s: event without a title" % rid)
            self.extras(g, s, row, "events")

    def build_facts(self):
        for tag, fname, line, row in self.rows.get("facts", []):
            if not self.need(row, ("entity", "metric"), fname, line):
                continue
            reg = self.register(row.get("id"), "facts", tag, fname, line, row)
            if not reg:
                continue
            g, s = reg
            rid = sid_for(s)
            p = self.party(row["entity"], rid)
            g.add((s, UC.aboutParty, p))
            g.add((s, UC.involvesParty, p))
            g.add((s, UC.metric, Literal(str(row["metric"]).strip())))
            v = row.get("value")
            if not blank(v) or v == 0:
                if dec_lex(v) is not None:
                    g.add((s, UC.amount, Literal(dec_lex(v), datatype=XSD.decimal)))
                else:
                    g.add((s, UC.textValue, Literal(str(v).strip())))
            else:
                self.log.note("oddities", "%s: fact without a value" % rid)
            self.add_currency(g, s, row.get("currency"), rid)
            if not blank(row.get("unit_note")):
                g.add((s, UC.unitNote, Literal(str(row["unit_note"]).strip())))
            self.add_date(g, s, row.get("period"), None, rid)
            self.extras(g, s, row, "facts")

    def build_issues(self):
        for tag, fname, line, row in self.rows.get("issues", []):
            reg = self.register(row.get("id"), "issues", tag, fname, line, row)
            if not reg:
                continue
            g, s = reg
            if not blank(row.get("where")):
                g.add((s, UC.issueLocation, Literal(str(row["where"]).strip())))
            if not blank(row.get("kind")):
                g.add((s, UC.issueKind, Literal(str(row["kind"]).strip())))
            self.lang_pair(g, s, DCTERMS.description, row, "issue")
            self.assertions[sid_for(s)]["concerns"] = row.get("concerns")
            self.extras(g, s, row, "issues")

    def link_issues(self):
        for rid in sorted(self.assertions):
            a = self.assertions[rid]
            if a["kind"] != "issues" or blank(a.get("concerns")):
                continue
            refs = a["concerns"] if isinstance(a["concerns"], list) else [a["concerns"]]
            g = self.graphs[a["graph"]]
            for r in refs:
                r = self.canon(r)
                if r in self.assertions or r in self.entities or r in self.sources:
                    g.add((a["iri"], UC.concerns, iri_for(r)))
                else:
                    self.log.note("unknown_refs", "%s: concerns %s, which is not a known row, party or source; kept as text" % (rid, r))
                    self.extra(g, a["iri"], "concerns", r)

    def build_charges(self):
        for tag, fname, line, row in self.rows.get("accused", []):
            if not self.need(row, ("person",), fname, line):
                continue
            reg = self.register(row.get("id"), "accused", tag, fname, line, row)
            if not reg:
                continue
            g, s = reg
            rid = sid_for(s)
            p = self.party(row["person"], rid)
            g.add((s, UC.chargedPerson, p))
            g.add((s, UC.involvesParty, p))
            comp = row.get("company")
            for c in (comp if isinstance(comp, list) else [comp]):
                if blank(c):
                    continue
                if re.fullmatch(r"(org|auth|person):[a-z0-9\-]+", str(c).strip()):
                    g.add((s, UC.involvesParty, self.party(c, rid)))
                else:
                    self.extra(g, s, "company", c)
            if not blank(row.get("label")):
                g.add((s, UC.nameAsReported, Literal(str(row["label"]).strip())))
            self.lang_pair(g, s, UC.roleReported, row, "role_reported")
            for key, prop in (("offences", UC.allegedOffence), ("offences_added", UC.allegedOffenceAdded)):
                vals = row.get(key) or []
                for o in (vals if isinstance(vals, list) else [vals]):
                    if not blank(o):
                        g.add((s, prop, Literal(str(o).strip(), lang=guess_lang(str(o)))))
            if not blank(row.get("measure")):
                g.add((s, UC.proceduralMeasure, Literal(str(row["measure"]).strip(), lang="en")))
            self.add_date(g, s, row.get("measure_date"), None, rid)
            self.lang_pair(g, s, UC.defenceStatement, row, "defence_statement")
            for key, prop in (("case", UC.caseReference), ("next_hearing", UC.nextHearing),
                              ("place_reported", UC.placeReported), ("previous_measure", UC.previousMeasure)):
                if isinstance(row.get(key), (str, int)) and not blank(row.get(key)):
                    g.add((s, prop, Literal(str(row[key]).strip())))
                elif not blank(row.get(key)):
                    self.extra(g, s, key, row[key])
            if not blank(row.get("measure_requested")):
                if isinstance(row["measure_requested"], str):
                    g.add((s, UC.measureRequested, Literal(row["measure_requested"].strip(), lang="en")))
                else:
                    self.extra(g, s, "measure_requested", row["measure_requested"])
            if not blank(row.get("detained")):
                dd = norm_date(row["detained"])
                if dd["kind"] == "single" and dd["precision"] == "day":
                    g.add((s, UC.detainedOn, Literal(dd["start"], datatype=XSD.date)))
                else:
                    self.extra(g, s, "detained", row["detained"])
            for key, prop in (("measure_source", UC.measureSource), ("status_source", UC.statusSource)):
                v = row.get(key)
                if isinstance(v, str) and v.strip() in self.sources:
                    g.add((s, prop, iri_for(v.strip())))
                    self.used_sources[v.strip()] += 1
                elif not blank(v):
                    self.extra(g, s, key, v)
            self.extras(g, s, row, "accused")

    # ----- analyst opinions -------------------------------------------------------------------
    def build_opinions(self):
        """mm.opinions and the like: uc:AnalystOpinion nodes in the analysis graph. Estimates, not sourced claims."""
        self.opinion_basis = {}
        for tag, fname, line, row in self.rows.get("opinions", []):
            reg = self.register(row.get("id"), "opinions", tag, fname, line, row)
            if not reg:
                continue
            g, s = reg
            rid = sid_for(s)
            if not blank(row.get("kind")):
                g.add((s, UC.opinionKind, Literal(str(row["kind"]).strip())))
            self.lang_pair(g, s, DCTERMS.title, row, "title")
            self.lang_pair(g, s, DCTERMS.description, row, "text")
            vals = {}
            for key, prop in (("low", UC.estimateLow), ("central", UC.estimateCentral), ("high", UC.estimateHigh)):
                vals[key] = self.add_money(g, s, prop, row.get(key), rid, key)
            cur = self.add_currency(g, s, row.get("currency"), rid)
            if any(v is not None for v in vals.values()) and cur is None:
                self.log.note("oddities", "%s: estimate without currency" % rid)
            seq = [vals[k] for k in ("low", "central", "high") if vals[k] is not None]
            if seq != sorted(seq):
                self.log.note("oddities", "%s: estimates are not in the order low <= central <= high" % rid)
            refs = row.get("basis_refs") or []
            self.opinion_basis[rid] = [str(r).strip() for r in (refs if isinstance(refs, list) else [refs]) if not blank(r)]
            self.extras(g, s, row, "opinions")

    def link_opinions(self):
        self.basis_resolved, self.basis_unresolved = 0, []
        for rid in sorted(getattr(self, "opinion_basis", {})):
            a = self.assertions[rid]
            g = self.graphs[a["graph"]]
            for r in self.opinion_basis[rid]:
                if r in self.assertions and r != rid:
                    g.add((a["iri"], UC.basedOn, self.assertions[r]["iri"]))
                    self.basis_resolved += 1
                else:
                    self.basis_unresolved.append((rid, r))
                    self.log.note("unknown_refs", "%s: basis_refs entry %s is not a known row; skipped" % (rid, r))

    # ----- editor layer nodes ----------------------------------------------------------------
    def build_corrections(self):
        g = self.default
        for e in self.edits["corrections"]:
            c = e["c"]
            s = iri_for(e["id"])
            prov = c.get("prov") if isinstance(c.get("prov"), dict) else {}
            g.add((s, RDF.type, UC.Correction))
            g.add((s, DCTERMS.identifier, Literal(e["id"])))
            g.add((s, UC.correctionStatus, Literal(e["status"] or "not applied")))
            if not blank(c.get("action")):
                g.add((s, UC.correctionAction, Literal(str(c["action"]))))
            if not blank(c.get("field")):
                g.add((s, UC.rawField, Literal(str(c["field"]))))
                g.add((s, UC.correctedField, Literal(FIELD_KEY.get(str(c["field"]), str(c["field"])))))
            if "old" in c:
                g.add((s, UC.originalValue, Literal(show_value(c.get("old")))))
            if "new" in c:
                g.add((s, UC.newValue, Literal(show_value(c.get("new")))))
            for lg in ("en", "es"):
                if not blank(c.get("reason_" + lg)):
                    g.add((s, UC.editorNote, Literal(str(c["reason_" + lg]).strip(), lang=lg)))
            if not blank(c.get("checked_against")):
                g.add((s, UC.checkedAgainst, Literal(str(c["checked_against"]).strip())))
            if e.get("node") is not None:
                g.add((s, UC.correctsRow, e["node"]))
            src = str(prov.get("source") or "").strip()
            if src:
                if src not in self.sources:
                    self.stub_sources[src].append(e["id"])
                g.add((s, PROV.wasDerivedFrom, iri_for(src)))
                self.primary_source[s] = iri_for(src)
                self.used_sources[src] += 1
            by = str(prov.get("asserted_by") or "").strip().lower()
            if by in ASSERTER_CONCEPT:
                g.add((s, UC.assertedBy, UC[ASSERTER_CONCEPT[by]]))
            if str(prov.get("confidence") or "").lower() in CONFIDENCES:
                g.add((s, UC.confidence, Literal(str(prov["confidence"]).lower())))
            if not blank(prov.get("locator")):
                g.add((s, UC.locator, Literal(str(prov["locator"]).strip())))
            if not blank(prov.get("quote")):
                q = str(prov["quote"]).strip()
                g.add((s, UC.quote, Literal(q, lang=guess_lang(q))))

    def build_claim_events(self):
        """Hidden flows restated as a CaseEvent by the same voice, with the flow row's own provenance."""
        for fid in sorted(CLAIM_EVENTS):
            if fid not in self.assertions or self.assertions[fid]["kind"] != "flows":
                continue
            cat, t_en, t_es, parties = CLAIM_EVENTS[fid]
            a = self.assertions[fid]
            src = a["row"]
            row = {"id": "edit:event:" + fid.replace(":", "-"), "date": src.get("date"), "date_precision": src.get("date_precision"),
                   "category": cat, "title_en": t_en, "title_es": t_es, "detail_en": src.get("purpose_en"),
                   "detail_es": src.get("purpose_es"), "parties": parties, "amount": src.get("amount"),
                   "currency": src.get("currency"), "prov": dict(src.get("prov") or {})}
            reg = self.register(row["id"], "events", "edit", "(build_graph.py CLAIM_EVENTS)", 0, row)
            if not reg:
                continue
            g, s = reg
            rid = sid_for(s)
            self.add_date(g, s, row["date"], row["date_precision"], rid)
            g.add((s, UC.eventCategory, UC["cat_" + cat]))
            self.lang_pair(g, s, DCTERMS.title, row, "title")
            self.lang_pair(g, s, DCTERMS.description, row, "detail")
            for p in parties:
                g.add((s, UC.involvesParty, self.party(p, rid)))
            self.add_money(g, s, UC.amount, row["amount"], rid, "amount")
            self.add_currency(g, s, row["currency"], rid)
            if isinstance(src.get("amount_is_approx"), bool):
                g.add((s, UC.amountIsApproximate, Literal(src["amount_is_approx"])))
            g.add((s, UC.restates, a["iri"]))

    def same_operation_keys(self):
        """uc:sameOperationKey: one shared key for loan / flow records that describe the same operation.

        Loans: same operation number (unless two rows of one source document carry different dates: those are
        successive drawings of one line), or same lender, borrower, currency, date and principal.
        Flows: same sender, receiver, currency, date and amount. Amounts match when equal, or when one is the
        other rounded (4,230,000 ~ 4,230,383.21). The key is the id of the first record of the group. Rows are
        never merged.
        """
        def close(a, b):
            if a is None or b is None:
                return False
            if a == b:
                return True
            lo, hi = sorted((a, b))
            if lo <= 0 or (hi - lo) / hi > Decimal("0.01"):
                return False
            for x, y in ((a, b), (b, a)):                       # is x the other figure rounded?
                if x != x.to_integral_value():
                    continue
                sig = len(str(int(x)).rstrip("0"))
                if sig >= 2:
                    q = Decimal(10) ** (len(str(int(x))) - sig)
                    if (y / q).quantize(Decimal(1)) * q == x or (y / q).to_integral_value(rounding="ROUND_DOWN") * q == x:
                        return True
            return False

        def work(rid):
            src = self.assertions[rid]["source"]
            return "acta" if src.startswith("src:acta-") else src

        def groups(ids, same):
            parent = {i: i for i in ids}

            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    if same(ids[i], ids[j]):
                        ra, rb = find(ids[i]), find(ids[j])
                        if ra != rb:
                            parent[max(ra, rb)] = min(ra, rb)
            out = collections.defaultdict(list)
            for i in ids:
                out[find(i)].append(i)
            return [sorted(v) for v in out.values() if len(v) > 1]

        L, F = self.loans, self.flows

        def date_of(rid):
            return str(self.assertions[rid]["row"].get("date") or "").strip()

        def same_loan(a, b):
            x, y = L[a], L[b]
            if x["lender"] != y["lender"] or x["borrower"] != y["borrower"]:
                return False
            if x["op"] and x["op"] == y["op"]:
                return not (work(a) == work(b) and date_of(a) != date_of(b))
            if x["op"] and y["op"]:
                return False
            return bool(date_of(a)) and date_of(a) == date_of(b) and x["currency"] == y["currency"] \
                and close(x["principal"], y["principal"])

        def same_flow(a, b):
            x, y = F[a], F[b]
            return x["from"] == y["from"] and x["to"] == y["to"] and x["currency"] == y["currency"] \
                and bool(x["date"]) and x["date"] == y["date"] and close(x["amount"], y["amount"])

        self.same_op_groups = []
        for table, same, label in ((L, same_loan, "loans"), (F, same_flow, "flows")):
            for grp in sorted(groups(sorted(table), same)):
                for rid in grp:
                    table[rid]["g"].add((table[rid]["iri"], UC.sameOperationKey, Literal(grp[0])))
                self.same_op_groups.append((label, grp))
                self.derived["uc:sameOperationKey groups (%s)" % label] += 1
                self.derived["uc:sameOperationKey records (%s)" % label] += len(grp)

    # ----- stubs -----------------------------------------------------------------------------
    def build_stubs(self):
        g = self.default
        for sid in sorted(self.stubs):
            if sid in self.entities:
                continue
            s = iri_for(sid)
            cls = PREFIX_CLASS.get(sid.split(":")[0], "Party")
            if cls == "Party":
                self.log.note("unknown_refs", "%s: reference has no org: / person: / auth: prefix; typed uc:Party" % sid)
            g.add((s, RDF.type, UC[cls]))
            if sid in EXTRA_PARTY_TYPES:
                g.add((s, RDF.type, EXTERNAL_CLASSES[EXTRA_PARTY_TYPES[sid]]))
            g.add((s, DCTERMS.identifier, Literal(sid)))
            g.add((s, RDFS.label, Literal(placeholder_label(sid))))
            g.add((s, UC.isStub, Literal(True)))
        for sid in sorted(self.stub_sources):
            s = iri_for(sid)
            g.add((s, RDF.type, UC.Source))
            g.add((s, DCTERMS.identifier, Literal(sid)))
            g.add((s, UC.isStub, Literal(True)))

    # ----- derived links ---------------------------------------------------------------------
    def derive(self):
        # (a) uc:ultimateRecipient: end points of the chain of flows linked to a loan, same voice as the loan
        by_loan = collections.defaultdict(list)
        for rid in sorted(self.flows):
            f = self.flows[rid]
            if f["linked"]:
                by_loan[f["linked"]].append(rid)
        for lid in sorted(by_loan):
            loan = self.loans[lid]
            usable = []
            for rid in by_loan[lid]:
                f = self.flows[rid]
                if f["asserter"] != loan["asserter"]:
                    self.derived["flows skipped: asserter differs from the loan's"] += 1
                    continue
                if f["instrument"] in NON_PROCEEDS_INSTRUMENTS:
                    self.derived["flows skipped: instrument is not a forwarding of proceeds"] += 1
                    continue
                if f["from"] == f["to"]:
                    continue
                usable.append(rid)
            if not usable:
                continue
            out_edges = collections.defaultdict(list)
            for rid in usable:
                out_edges[self.flows[rid]["from"]].append(rid)
            # walk from the nominal borrower
            reached, via, todo = set(), collections.defaultdict(set), [loan["borrower"]]
            visited = {loan["borrower"]}
            while todo:
                node = todo.pop()
                for rid in out_edges.get(node, []):
                    to = self.flows[rid]["to"]
                    via[to].add(rid)
                    reached.add(to)
                    if to not in visited:
                        visited.add(to)
                        todo.append(to)
            sinks = sorted(p for p in reached if p != loan["borrower"] and not out_edges.get(p))
            if not sinks:
                self.derived["loans with linked flows but no end recipient reachable from the borrower"] += 1
                continue
            for p in sinks:
                loan["g"].add((loan["iri"], UC.ultimateRecipient, p))
                loan["g"].add((loan["iri"], UC.involvesParty, p))
                for rid in sorted(via[p]):
                    loan["g"].add((loan["iri"], UC.recipientDerivedFrom, self.flows[rid]["iri"]))
                self.derived["uc:ultimateRecipient links"] += 1
            self.derived["loans with a derived ultimate recipient"] += 1
        # (b) uc:sameSubjectAs: same operation number + lender + borrower, different voice
        by_op = collections.defaultdict(list)
        for lid in sorted(self.loans):
            if self.loans[lid]["op"]:
                by_op[self.loans[lid]["op"]].append(lid)
        for op in sorted(by_op):
            ids = by_op[op]
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    a, b = self.loans[ids[i]], self.loans[ids[j]]
                    same_parties = a["lender"] == b["lender"] and a["borrower"] == b["borrower"]
                    if a["asserter"] != b["asserter"] and same_parties:
                        a["g"].add((a["iri"], UC.sameSubjectAs, b["iri"]))
                        b["g"].add((b["iri"], UC.sameSubjectAs, a["iri"]))
                        self.derived["uc:sameSubjectAs pairs (same operation number, lender, borrower; different voice)"] += 1
                        self.log.note("same_op", "%s and %s share operation number %s across voices (%s / %s): linked with uc:sameSubjectAs"
                                      % (ids[i], ids[j], op, a["asserter"], b["asserter"]))
                    elif not same_parties:
                        self.log.note("same_op", "%s and %s share operation number %s but lender or borrower differ: NOT linked, please check"
                                      % (ids[i], ids[j], op))
                    else:
                        self.log.note("same_op", "%s and %s share operation number %s within one voice (%s): possibly one operation recorded twice, or a renewal; NOT linked"
                                      % (ids[i], ids[j], op, a["asserter"]))

    # ----- dataset node and extension declarations -------------------------------------------
    def build_meta(self):
        g = self.default
        g.add((DATASET, RDF.type, OWL.Ontology))
        g.add((DATASET, OWL.imports, ONT))
        g.add((DATASET, DCTERMS.title, Literal("Ueno Bank case knowledge graph (instance data)", lang="en")))
        g.add((DATASET, DCTERMS.title, Literal("Grafo de conocimiento del caso Ueno Bank (datos de instancia)", lang="es")))
        g.add((DATASET, DCTERMS.description, Literal(
            "Provenance-first instance data. Every statement about the case is an allegation or report by a named "
            "asserter; presumption of innocence applies to every person.", lang="en")))
        g.add((DATASET, DCTERMS.description, Literal(
            "Datos de instancia centrados en la procedencia. Toda afirmación sobre el caso es una alegación o un informe "
            "de un declarante identificado; rige la presunción de inocencia para todas las personas.", lang="es")))
        for term in sorted(self.x_terms):
            g.add((UC[term], RDF.type, OWL.DatatypeProperty))
            g.add((UC[term], RDFS.comment, Literal(
                "Builder extension. Raw contributor field '%s' that has no mapping yet; value copied as text." % term[2:], lang="en")))
            g.add((UC[term], RDFS.isDefinedBy, DATASET))

    def run(self, ontology):
        known = {str(s).split("#")[-1] for s in ontology.subjects(RDF.type, SKOS.Concept)} if ontology else set()
        self.build_sources()
        self.build_entities()
        self.build_party_descriptions()
        self.build_roles(known)
        self.build_loans()
        self.build_flows(known)
        self.link_flows_to_loans()
        self.build_events(known)
        self.build_facts()
        self.build_issues()
        self.link_issues()
        self.build_charges()
        self.build_opinions()
        self.build_claim_events()
        self.link_opinions()
        self.build_corrections()
        self.build_stubs()
        self.derive()
        self.same_operation_keys()
        self.build_meta()
        return self


# =============================================================================================
# 3. Serialisers (own writers: sorted, stable output)
# =============================================================================================

_PN_LOCAL = re.compile(r"[A-Za-z0-9_](?:[A-Za-z0-9_\-]*[A-Za-z0-9_])?$")


class TurtleWriter:
    """Minimal deterministic Turtle / TriG writer for IRIs and literals (the graph has no blank nodes)."""

    def __init__(self, quads):
        self.ns = list(PREFIXES)
        seen = {n for _, n in self.ns}
        extra = set()
        for q in quads:
            for t in q[:3]:
                if isinstance(t, URIRef) and str(t).startswith(ID):
                    head = str(t).rsplit("/", 1)[0] + "/"
                    if head != ID and head not in seen and _PN_LOCAL.match(str(t)[len(head):]):
                        extra.add(head)
        for head in sorted(extra):
            name = head[len(ID):].strip("/").replace("/", "-")
            if re.fullmatch(r"[A-Za-z][A-Za-z0-9_\-]*", name) and name not in {p for p, _ in self.ns}:
                self.ns.append((name, head))
        self.by_len = sorted(self.ns, key=lambda x: -len(x[1]))
        self.used = set()

    def term(self, t):
        if isinstance(t, URIRef):
            if t == RDF.type:
                return "a"
            s = str(t)
            for p, n in self.by_len:
                if s.startswith(n) and _PN_LOCAL.match(s[len(n):]):
                    self.used.add(p)
                    return "%s:%s" % (p, s[len(n):])
            return "<%s>" % s
        s = str(t)
        esc = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
        if t.language:
            return '"%s"@%s' % (esc, t.language)
        dt = t.datatype
        if dt is None or dt == XSD.string:
            return '"%s"' % esc
        if dt == XSD.boolean and s in ("true", "false"):
            return s
        if dt == XSD.integer and re.fullmatch(r"[+-]?\d+", s):
            return s
        self.used.add("xsd")
        return '"%s"^^%s' % (esc, self.term(dt))

    @staticmethod
    def _okey(o):
        return (0, str(o), "", "") if isinstance(o, URIRef) else (1, str(o), o.language or "", str(o.datatype or ""))

    def block(self, triples, indent=""):
        by_s = collections.defaultdict(lambda: collections.defaultdict(set))
        for s, p, o in triples:
            by_s[s][p].add(o)
        out = []
        for s in sorted(by_s, key=str):
            lines = []
            preds = sorted(by_s[s], key=lambda p: (p != RDF.type, str(p)))
            for p in preds:
                objs = " , ".join(self.term(o) for o in sorted(by_s[s][p], key=self._okey))
                lines.append("%s %s" % (self.term(p), objs))
            out.append("%s%s %s .\n" % (indent, self.term(s), (" ;\n%s    " % indent).join(lines)))
        return "\n".join(out)

    def header(self):
        return "".join("@prefix %s: <%s> .\n" % (p, n) for p, n in self.ns if p in self.used) + "\n"


def write_trig(b, path):
    quads = list(b.ds.quads((None, None, None, None)))
    w = TurtleWriter(quads)
    body = ["# Ueno Bank case knowledge graph - named graphs. Generated by data/build_graph.py; do not edit.\n"
            "# Default graph: parties, sources, correction records, dataset node (owl:imports).\n",
            w.block(set(b.default))]
    for name in GRAPH_NAMES:
        g = b.graphs[name]
        body.append("\n%s {\n%s}\n" % (w.term(g.identifier), w.block(set(g), "    ")))
    text = "".join(body)
    with open(path, "w", encoding="utf-8") as f:
        f.write(w.header() + text)


def union_triples(b):
    return {(s, p, o) for s, p, o, _ in b.ds.quads((None, None, None, None))}


def write_ttl(b, path):
    triples = union_triples(b)
    w = TurtleWriter(triples)
    text = ("# Ueno Bank case knowledge graph - union of all graphs. Generated by data/build_graph.py; do not edit.\n"
            "# Voices are told apart by uc:assertedBy here; use graph.trig for the named graphs.\n" + w.block(triples))
    with open(path, "w", encoding="utf-8") as f:
        f.write(w.header() + text)


# ---------------------------------------------------------------------------------------------
# JSON-LD
# ---------------------------------------------------------------------------------------------

JSONLD_PREFIXES = [("uc", str(UC)), ("ucr", ID), ("rdfs", str(RDFS)), ("owl", str(OWL)), ("xsd", str(XSD)),
                   ("skos", str(SKOS)), ("dcterms", str(DCTERMS)), ("prov", str(PROV)), ("schema", str(SCHEMA))]


def build_jsonld(b):
    """Returns (context, nodes, type_of): a flat list of node objects with compact keys."""
    terms = dict(TERMS)
    for t, kind in b.x_terms.items():
        terms[t] = (UC[t], kind)
    pred_term = {}
    for t, (p, k) in terms.items():
        if t in DUAL_TERMS:
            continue
        if p in pred_term:
            raise RuntimeError("two JSON-LD terms for %s" % p)
        pred_term[p] = t

    # value terms: every IRI used as rdf:type or as the object of a 'voc' property gets a context term
    value_term = {}

    def vterm(iri):
        s = str(iri)
        if iri in value_term:
            return value_term[iri]
        if s.startswith(str(UC)):
            name = s[len(str(UC)):]
        elif s.startswith(str(CUR)):
            name = s[len(str(CUR)):]
        elif s.startswith(str(OWL)):
            name = s[len(str(OWL)):]
        else:
            name = next((k for k, v in EXTERNAL_CLASSES.items() if v == iri), None) or re.split(r"[/#]", s)[-1]
        if name in terms or name in value_term.values() or name in dict(JSONLD_PREFIXES) or name == "graph":
            raise RuntimeError("JSON-LD term clash for %s" % s)
        value_term[iri] = name
        return name

    def ref(iri):
        s = str(iri)
        if s.startswith(ID):
            return "ucr:" + s[len(ID):]
        if s.startswith(str(UC)):
            return "uc:" + s[len(str(UC)):]
        return s

    subj_graphs = collections.defaultdict(set)
    props = collections.defaultdict(lambda: collections.defaultdict(list))
    for s, p, o, g in b.ds.quads((None, None, None, None)):
        gid = g.identifier if isinstance(g, Graph) else g
        gname = str(gid)[len(ID + "graph/"):] if str(gid).startswith(ID + "graph/") else "default"
        subj_graphs[s].add(gname)
        props[s][p].append(o)

    def type_rank(t):
        return TYPE_ORDER.index(t) if t in TYPE_ORDER else len(TYPE_ORDER)

    nodes = []
    for s in props:
        if len(subj_graphs[s]) != 1:
            raise RuntimeError("%s has statements in several graphs: %s" % (s, sorted(subj_graphs[s])))
        gname = next(iter(subj_graphs[s]))
        types = sorted({vterm(o) for o in props[s].get(RDF.type, [])},
                       key=lambda t: (t in EXTERNAL_CLASSES or t == "Loan" and UC.Overdraft in props[s][RDF.type], type_rank(t), t))
        node = {"@id": ref(s), "@type": types}
        if gname != "default":
            node["graph"] = gname
        body = {}
        for p, objs in props[s].items():
            if p == RDF.type:
                continue
            if p not in pred_term:
                raise RuntimeError("no JSON-LD term for predicate %s" % p)
            t = pred_term[p]
            kind = terms[t][1]
            objs = sorted(set(objs), key=TurtleWriter._okey)
            if p == PROV.wasDerivedFrom and b.corr_sources.get(s):
                # the row's own source stays the single 'source'; sources added by corrections are listed under
                # 'correctionSource' (same predicate, so RDF sees every one of them as prov:wasDerivedFrom)
                extra_src = b.corr_sources[s]
                if set(objs) != extra_src | {b.primary_source[s]}:
                    raise RuntimeError("%s: unexpected prov:wasDerivedFrom values" % s)
                body["correctionSource"] = [ref(o) for o in sorted(extra_src, key=str)]
                objs = [b.primary_source[s]]
            single = kind in ("ref", "voc", "str", "dec", "int", "bool", "day", "anydate", "url")
            if single and len(objs) > 1:
                raise RuntimeError("%s has %d values for single-valued key %s" % (s, len(objs), t))
            if kind in ("ref", "refs"):
                vals = [ref(o) for o in objs]
            elif kind == "voc":
                vals = [vterm(o) for o in objs]
            elif kind in ("lang", "langs"):
                m = collections.defaultdict(list)
                for o in objs:
                    if not o.language:
                        raise RuntimeError("%s %s: literal without language tag" % (s, t))
                    m[o.language].append(str(o))
                if kind == "lang" and any(len(v) > 1 for v in m.values()):
                    raise RuntimeError("%s has several %s values in one language" % (s, t))
                body[t] = {lg: (m[lg] if kind == "langs" else m[lg][0]) for lg in sorted(m)}
                continue
            elif kind == "anydate":
                vals = [{"@value": str(o), "@type": "xsd:" + str(o.datatype)[len(str(XSD)):]} for o in objs]
            elif kind == "int":
                vals = [int(o) for o in objs]
            elif kind == "bool":
                vals = [str(o) == "true" for o in objs]
            else:
                vals = [str(o) for o in objs]
            body[t] = vals[0] if single else vals
        if "identifier" in body:
            node["identifier"] = body.pop("identifier")
        for k in sorted(body):
            node[k] = body[k]
        nodes.append(node)
    nodes.sort(key=lambda n: (type_rank(n["@type"][0]) if n["@type"] else 99, n["@id"]))

    ctx = collections.OrderedDict()
    ctx["@version"] = 1.1
    for p, n in JSONLD_PREFIXES:
        ctx[p] = n
    for iri in sorted(value_term, key=lambda i: value_term[i]):
        ctx[value_term[iri]] = str(iri)
    coercion = {"ref": {"@type": "@id"}, "refs": {"@type": "@id", "@container": "@set"},
                "voc": {"@type": "@vocab"}, "lang": {"@container": "@language"}, "langs": {"@container": "@language"},
                "str": {}, "strs": {"@container": "@set"}, "dec": {"@type": "xsd:decimal"},
                "int": {"@type": "xsd:integer"}, "bool": {"@type": "xsd:boolean"}, "day": {"@type": "xsd:date"},
                "anydate": {}, "url": {"@type": "xsd:anyURI"}}
    used_terms = {k for n in nodes for k in n}
    for t in sorted(terms):
        if t not in used_terms:
            continue
        p, kind = terms[t]
        d = {"@id": ref(p) if str(p).startswith(str(UC)) else compact_iri(p)}
        d.update(coercion[kind])
        ctx[t] = d
    return ctx, nodes


def compact_iri(iri):
    s = str(iri)
    for p, n in sorted(JSONLD_PREFIXES, key=lambda x: -len(x[1])):
        if s.startswith(n):
            return "%s:%s" % (p, s[len(n):])
    return s


def write_jsonld(ctx, nodes, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write('{\n"@context": ')
        f.write(json.dumps(ctx, ensure_ascii=False, indent=1))
        f.write(',\n"@graph": [\n')
        f.write(",\n".join(json.dumps(n, ensure_ascii=False, separators=(",", ":")) for n in nodes))
        f.write("\n]\n}\n")


# =============================================================================================
# 4. Review material: duplicates, oddities
# =============================================================================================

def suspected_duplicates(b):
    names = {}
    for sid, ent in b.entities.items():
        names[sid] = {norm_name(x) for x in [ent["label"]] + ent["alt"]} | {slug_name(sid)}
    for sid in b.stubs:
        if sid not in b.entities:
            names[sid] = {slug_name(sid)}
    names = {k: {n for n in v if n} for k, v in names.items()}
    ids = sorted(names)
    exact, similar = [], []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, c = ids[i], ids[j]
            fam = lambda x: "person" if x.startswith("person:") else "org"
            if fam(a) != fam(c):
                continue
            common = names[a] & names[c]
            if common:
                exact.append((a, c, sorted(common)[0]))
                continue
            best = None
            for x in names[a]:
                for y in names[c]:
                    tx, ty = set(x.split()), set(y.split())
                    small, big = (tx, ty) if len(tx) <= len(ty) else (ty, tx)
                    ratio = difflib.SequenceMatcher(None, x, y).ratio()
                    subset = len(small) >= 2 and small <= big
                    if fam(a) == "person":
                        # same first given name and a shared surname token, or token subset
                        hit = subset or ratio >= 0.88
                    else:
                        hit = subset or ratio >= 0.80
                    if hit and (best is None or ratio > best[0]):
                        best = (ratio, x, y, "one name contains the other" if subset else "similar spelling")
            if best:
                similar.append((a, c, best[1], best[2], best[3], best[0]))
    return exact, sorted(similar, key=lambda t: (-t[5], t[0], t[1]))


def extra_oddities(b):
    """Checks across rows; returns list of strings."""
    out = []
    # repeated flows (same parties, amount, currency, date, voice) - risk of double counting
    seen = collections.defaultdict(list)
    for rid, f in sorted(b.flows.items()):
        if f["amount"] is not None:
            seen[(f["from"], f["to"], f["amount"], f["currency"], f["date"], f["asserter"])].append(rid)
    for key, ids in sorted(seen.items(), key=lambda kv: kv[1]):
        if len(ids) > 1:
            out.append("flows %s describe the same movement (%s -> %s, %s %s, %s) in the %s voice: do not add them up"
                       % (", ".join(ids), sid_for(key[0]), sid_for(key[1]), key[3] or "", key[2], key[4] or "undated", key[5]))
    # repeated loans without operation number
    seenl = collections.defaultdict(list)
    for rid, l in sorted(b.loans.items()):
        row = b.assertions[rid]["row"]
        if l["principal"] is not None:
            seenl[(l["borrower"], l["principal"], l["currency"], str(row.get("date") or ""), l["asserter"])].append(rid)
    for key, ids in sorted(seenl.items(), key=lambda kv: kv[1]):
        if len(ids) > 1:
            out.append("loans %s look like the same operation (%s, %s %s, %s) reported in several rows of the %s voice: do not add them up"
                       % (", ".join(ids), sid_for(key[0]), key[2] or "", key[1], key[3] or "undated", key[4]))
    # shareholdings above 100 % for one organisation within one source
    sh = collections.defaultdict(lambda: Decimal(0))
    for rid, a in sorted(b.assertions.items()):
        row = a["row"]
        if a["kind"] == "roles" and row.get("role") == "shareholder" and dec_lex(row.get("pct")) and blank(row.get("end")):
            sh[(b.canon(row["org"]), a["source"], a["asserter"], str(row.get("start") or ""))] += Decimal(dec_lex(row["pct"]))
    for (org, src, by, start), tot in sorted(sh.items()):
        if tot > Decimal("100.5"):
            out.append("shareholder percentages for %s add up to %s%% within one source and start date (%s, voice %s, start %s)"
                       % (org, tot, src, by, start or "not stated"))
    # unused sources
    for sid in sorted(b.sources):
        if not b.used_sources.get(sid):
            out.append("source %s is not cited by any row" % sid)
    return out


# =============================================================================================
# 5. Checks, stats, reports
# =============================================================================================

def install_join_orderer():
    """Give rdflib a join order for basic graph patterns, so the queries of fibo_mapping.md finish.

    rdflib 7 starts a basic graph pattern with every triple pattern that has a single variable, so
    `?f1 a uc:Flow . ?f2 a uc:Flow . ?f3 a uc:Flow` is evaluated as a cross product before any join
    (Q2 and Q3 then run for many minutes on this data). This wrapper only changes WHICH triple pattern is
    tried next: the one expected to match the fewest triples given the variables already bound, using
    simple counts per predicate and per (predicate, object). The query results are unchanged.
    """
    try:
        import rdflib.plugins.sparql.evaluate as evaluate
    except Exception:  # noqa
        return False
    if getattr(evaluate.evalBGP, "_ueno_ordered", False):
        return True
    original = evaluate.evalBGP
    cache = {}

    def stats_for(graph):
        key = id(graph)
        if key not in cache:
            n_p, n_po, subj_p = collections.Counter(), collections.Counter(), collections.defaultdict(set)
            total = 0
            for s_, p_, o_ in graph.triples((None, None, None)):
                total += 1
                n_p[p_] += 1
                n_po[(p_, o_)] += 1
                subj_p[p_].add(s_)
            cache[key] = (total, n_p, n_po, {k: len(v) for k, v in subj_p.items()})
        return cache[key]

    def ordered(ctx, bgp):
        if len(bgp) > 1:
            total, n_p, n_po, n_subj = stats_for(ctx.graph)
            best, best_key = 0, None
            for i, t in enumerate(bgp):
                s_, p_, o_ = (ctx[c] for c in t)
                if not isinstance(p_, URIRef):                 # variable predicate or property path
                    est = 1.0 if (s_ is not None and o_ is not None) else (20.0 if (s_ is not None or o_ is not None) else float(total))
                elif s_ is not None and o_ is not None:
                    est = 0.5
                elif o_ is not None:
                    est = float(n_po.get((p_, o_), 0))
                elif s_ is not None:
                    est = n_p.get(p_, 0) / float(n_subj.get(p_, 1) or 1)
                else:
                    est = float(n_p.get(p_, 0))
                key = (est, i)
                if best_key is None or key < best_key:
                    best, best_key = i, key
            if best:
                bgp = [bgp[best]] + list(bgp[:best]) + list(bgp[best + 1:])
        return original(ctx, bgp)

    ordered._ueno_ordered = True
    evaluate.evalBGP = ordered
    return True


def read_queries(path):
    """SPARQL blocks of fibo_mapping.md: returns (prefix block, [(title, query)])."""
    if not os.path.exists(path):
        return "", []
    text = open(path, encoding="utf-8").read()
    blocks = re.findall(r"```sparql\n(.*?)```", text, re.S)
    prefix = next((b for b in blocks if "SELECT" not in b), "")
    out = []
    for m in re.finditer(r"^### (Q\d+\..*?)\n(.*?)(?=^### |\Z)", text, re.S | re.M):
        q = re.search(r"```sparql\n(.*?)```", m.group(2), re.S)
        if q:
            out.append((m.group(1).strip(), q.group(1)))
    return prefix, out


def short(term):
    """Compact display form for the printed report."""
    if term is None:
        return ""
    s = str(term)
    if " | " in s:
        return " | ".join(short(x) for x in s.split(" | "))
    if s.startswith(ID):
        return s[len(ID):].replace("/", ":")
    for p, n in PREFIXES:
        if s.startswith(n) and p != "ucr":
            return "%s:%s" % (p, s[len(n):])
    return s


def make_stats(b, inventory, nodes):
    by_type = collections.Counter()
    for n in nodes:
        by_type[n["@type"][0] if n["@type"] else "(untyped)"] += 1
    A = b.assertions
    stats = collections.OrderedDict()
    stats["note"] = ("Counts describe assertions (claims with provenance), not established facts. Figures are never "
                     "added across sources: loan totals are grouped by borrower, currency, asserter and source document. "
                     "Different groups may describe the same loans, so do not add groups together.")
    stats["inputs"] = inventory
    stats["nodes_total"] = len(nodes)
    stats["nodes_by_type"] = dict(sorted(by_type.items()))
    stats["assertions_total"] = len(A)
    stats["assertions_by_class"] = dict(sorted(collections.Counter(KIND_CLASS[a["kind"]] if not (a["kind"] == "loans" and str(a["row"].get("kind")).lower() == "overdraft") else "Overdraft" for a in A.values()).items()))
    stats["assertions_by_asserter"] = dict(sorted(collections.Counter(a["asserter"] for a in A.values()).items()))
    stats["assertions_by_graph"] = dict(sorted(collections.Counter(a["graph"] for a in A.values()).items()))
    stats["assertions_by_confidence"] = dict(sorted(collections.Counter(a["confidence"] for a in A.values()).items()))
    stats["assertions_second_hand_in_primary_graphs"] = {
        "note": "prosecution / rey assertions whose source is not the prosecution record (reported by press or others)",
        "counts": dict(sorted(b.second_hand.items())), "kept_in": "press graph" if SECOND_HAND_TO_PRESS else "asserter's graph"}
    C = b.edits["corrections"]
    stats["editor_layer"] = collections.OrderedDict([
        ("corrections_total", len(C)),
        ("corrections_applied", sum(1 for e in C if e["status"] == "applied")),
        ("corrections_not_applied", sum(1 for e in C if e["status"] != "applied")),
        ("corrections_by_action", dict(sorted(collections.Counter(str(e["c"].get("action")) for e in C).items()))),
        ("rows_corrected", len({e["target"] for e in C if e["status"] == "applied"})),
        ("entity_merges", dict(sorted(b.alias.items()))),
        ("verified_true", len(set(b.verified_ids))),
        ("verified_false", sum(1 for a in A.values() if a["row"].get("_verified") and not a["row"]["_verified"][0])),
        ("hidden", sorted(r for r, a in A.items() if a["hidden"])),
        ("alleged", sum(1 for a in A.values() if a["kind"] in ("flows", "events") and a["graph"] in ("prosecution", "rey"))),
        ("same_operation_groups", {"loans": sum(1 for k, g in b.same_op_groups if k == "loans"),
                                   "flows": sum(1 for k, g in b.same_op_groups if k == "flows"),
                                   "records": sum(len(g) for k, g in b.same_op_groups)})])
    ops = [a for a in A.values() if a["kind"] == "opinions"]
    stats["analyst_opinions"] = collections.OrderedDict([
        ("note", "Estimates by the project's analysts (graph 'analysis'). They are opinions resting on the cited assertions, "
                 "not sourced claims; never add them to sourced figures."),
        ("total", len(ops)),
        ("by_kind", dict(sorted(collections.Counter(str(a["row"].get("kind")) for a in ops).items()))),
        ("by_confidence", dict(sorted(collections.Counter(a["confidence"] for a in ops).items()))),
        ("basis_links_resolved", getattr(b, "basis_resolved", 0)),
        ("basis_links_unresolved", ["%s -> %s" % x for x in getattr(b, "basis_unresolved", [])])])
    stats["assertions_by_source_tier"] = dict(sorted(collections.Counter(a["tier"] for a in A.values()).items()))
    stats["assertions_by_contributor"] = dict(sorted(collections.Counter(a["tag"] for a in A.values()).items()))
    cross = collections.Counter("%s|%s" % (a["asserter"], KIND_CLASS[a["kind"]]) for a in A.values())
    stats["assertions_by_asserter_and_class"] = dict(sorted(cross.items()))
    stats["parties"] = {"described": len(b.entities), "stubs": len([s for s in b.stubs if s not in b.entities])}
    stats["sources"] = {"total": len(b.sources), "by_kind": dict(sorted(collections.Counter(
        str(v["row"].get("kind")) for v in b.sources.values()).items()))}
    # date range
    dr = {}
    for cls in ("CaseEvent", "Flow", "Loan", "FinancialFact", "RoleHolding", "Charge"):
        ds = sorted(n["sortDate"] for n in nodes if cls in n["@type"] and "sortDate" in n)
        if ds:
            dr[cls] = {"min": ds[0], "max": ds[-1], "dated": len(ds),
                       "undated": sum(1 for n in nodes if cls in n["@type"] and "sortDate" not in n)}
    alld = sorted(n["sortDate"] for n in nodes if "graph" in n and "sortDate" in n)
    stats["date_range"] = {"all_assertions": {"min": alld[0], "max": alld[-1]} if alld else None, "by_class": dr,
                           "note": "sortDate = first day of the stated date or period; see datePrecision"}
    # loan principal totals
    groups = collections.OrderedDict()
    for rid in sorted(b.loans):
        l = b.loans[rid]
        a = A[rid]
        skind = str(b.sources.get(a["source"], {}).get("row", {}).get("kind") or "")
        sgroup = "prosecution record (all pages)" if skind == "record" else a["source"]
        key = (sid_for(l["borrower"]), l["currency"] or "", a["asserter"], sgroup)
        gr = groups.setdefault(key, {"n": 0, "n_overdraft": 0, "n_no_principal": 0, "principal": Decimal(0),
                                     "principal_overdraft": Decimal(0),
                                     "outstanding": Decimal(0), "n_outstanding": 0, "ids": []})
        gr["n"] += 1
        gr["n_overdraft"] += l["kind"] == "overdraft"
        if l["principal"] is None:
            gr["n_no_principal"] += 1
        else:
            gr["principal"] += l["principal"]
            if l["kind"] == "overdraft":
                gr["principal_overdraft"] += l["principal"]
        if l["outstanding"] is not None:
            gr["outstanding"] += l["outstanding"]
            gr["n_outstanding"] += 1
        gr["ids"].append(rid)
    rows = []
    for (borrower, cur, by, sgroup), gr in sorted(groups.items()):
        ent = b.entities.get(borrower)
        rows.append(collections.OrderedDict([
            ("borrower", borrower), ("borrower_label", ent["label"] if ent else borrower.split(":", 1)[-1].replace("-", " ")),
            ("currency", cur or None), ("asserted_by", by), ("source_group", sgroup),
            ("loan_records", gr["n"]), ("of_which_overdrafts", gr["n_overdraft"]),
            ("records_without_principal", gr["n_no_principal"]),
            ("principal_total", dec_lex(gr["principal"])),
            ("principal_of_loans", dec_lex(gr["principal"] - gr["principal_overdraft"])),
            ("principal_of_overdrafts", dec_lex(gr["principal_overdraft"])),
            ("records_with_outstanding", gr["n_outstanding"]),
            ("outstanding_total", dec_lex(gr["outstanding"]) if gr["n_outstanding"] else None),
            ("loan_ids", gr["ids"])]))
    stats["loan_principal_by_borrower_currency"] = {
        "note": ("One row per borrower x currency x asserter x source document. Amounts are strings (exact decimals) in the "
                 "original currency; currencies are never converted or mixed. principal_total = principal_of_loans + "
                 "principal_of_overdrafts, includes cancelled operations, and counts an overdraft line once per record (a "
                 "renewed line can appear in several records). Rows from different asserters or source documents can cover "
                 "the same loans: compare them, do not add them."),
        "rows": rows}
    return stats


def run_checks(b, ontology, mapping_path, jsonld_path, ttl_path, trig_path, ctx, nodes, log):
    R = []
    P = R.append
    ok = True
    union = union_triples(b)
    P("=" * 78)
    P("BUILD REPORT")
    P("=" * 78)
    P("")
    P("Triples per graph")
    P("  %-14s %6d" % ("default", len(b.default)))
    for g in GRAPH_NAMES:
        P("  %-14s %6d" % (g, len(b.graphs[g])))
    P("  %-14s %6d   (distinct triples in the union)" % ("union", len(union)))
    P("")
    P("Instances per class (rdf:type, union graph)")
    cnt = collections.Counter(o for s, p, o in union if p == RDF.type)
    for o, n in sorted(cnt.items(), key=lambda kv: short(kv[0])):
        P("  %-58s %5d" % (short(o), n))
    P("")
    P("Assertions by asserter -> graph")
    for (by, g), n in sorted(collections.Counter((a["asserter"], a["graph"]) for a in b.assertions.values()).items()):
        P("  %-14s -> %-12s %5d" % (by, g, n))
    if b.second_hand:
        P("  of which reported second-hand (source is not the prosecution record): %s -> kept in the %s graph"
          % (", ".join("%s %d" % kv for kv in sorted(b.second_hand.items())),
             "press" if SECOND_HAND_TO_PRESS else "asserter's"))
    P("")
    P("Rows dropped: %d" % len(log.dropped))
    for (fname, line, rid, reason) in log.dropped:
        P("  %s line %s %s: %s" % (fname, line, rid, reason))
    reasons = collections.Counter(re.sub(r"\(.*", "", r[3]).strip() for r in log.dropped)
    for reason, n in sorted(reasons.items()):
        P("  by reason: %-50s %d" % (reason, n))
    P("")
    stubs = sorted(s for s in b.stubs if s not in b.entities)
    P("References to unknown entities: %d ids (stub parties created), %d references"
      % (len(stubs), sum(len(b.stubs[s]) for s in stubs)))
    for s in stubs:
        P("  %-45s %3d refs" % (s, len(b.stubs[s])))
    P("References to unknown sources: %d" % len(b.stub_sources))
    for s in sorted(b.stub_sources):
        P("  %-45s %3d refs" % (s, len(b.stub_sources[s])))
    P("")
    # provenance check on the graph itself
    missing = []
    for rid, a in sorted(b.assertions.items()):
        g = b.graphs[a["graph"]]
        for p in (PROV.wasDerivedFrom, UC.assertedBy, UC.confidence):
            if (a["iri"], p, None) not in g:
                missing.append((rid, short(p)))
    typed = {s for s, p, o in union if p == RDF.type and str(o).startswith(str(UC)) and
             str(o)[len(str(UC)):] in set(KIND_CLASS.values()) | {"Overdraft"}}
    not_registered = sorted(short(s) for s in typed if sid_for(s) not in b.assertions)
    P("Assertion nodes: %d; without full provenance (source, asserter, confidence): %d"
      % (len(b.assertions), len(missing) + len(not_registered)))
    if missing or not_registered:
        ok = False
        for m in missing[:20]:
            P("  MISSING %s %s" % m)
        for m in not_registered[:20]:
            P("  NOT REGISTERED %s" % m)
    # sources: outlet + (url or page)
    weak = [sid for sid, v in sorted(b.sources.items()) if blank(v["row"].get("url")) and blank(v["row"].get("page"))]
    P("Sources: %d; without URL and without record page: %d %s" % (len(b.sources), len(weak), weak if weak else ""))
    # dangling object references
    subjects = {s for s, p, o in union}
    dangling = sorted({short(o) for s, p, o in union if isinstance(o, URIRef) and str(o).startswith(ID)
                       and o not in subjects})
    P("Object references to instance IRIs that are not described: %d %s" % (len(dangling), dangling[:10] if dangling else ""))
    if dangling:
        ok = False
    # ontology coverage
    if ontology is not None:
        declared = set(ontology.subjects())
        ext = {UC[t] for t in b.x_terms}
        undeclared = sorted({short(t) for s, p, o in union for t in (p, o) if isinstance(t, URIRef)
                             and str(t).startswith(str(UC)) and t not in declared and t not in ext})
        P("uc: terms used but declared neither in ontology.ttl nor as builder extension: %d %s"
          % (len(undeclared), undeclared if undeclared else ""))
        ok &= not undeclared
        used_ext = sorted(short(t) for t in ext if any(t in (p, o) for s, p, o in union if p != RDFS.isDefinedBy and s != t))
        P("Unmapped raw fields declared by the builder as uc:x_ terms: %s" % (", ".join(used_ext) or "none"))
        # participant properties really are sub-properties of uc:involvesParty
        for name in ("holder", "organisation", "lender", "nominalBorrower", "ultimateRecipient", "fromParty", "toParty",
                     "aboutParty", "chargedPerson"):
            if (UC[name], RDFS.subPropertyOf, UC.involvesParty) not in ontology:
                P("  NOTE: uc:%s is not declared rdfs:subPropertyOf uc:involvesParty in ontology.ttl" % name)
    P("")
    C = b.edits["corrections"]
    P("Editor layer")
    P("  corrections: %d read, %d applied, %d not applied" % (len(C), sum(1 for e in C if e["status"] == "applied"),
                                                            sum(1 for e in C if e["status"] != "applied")))
    for (act, st), n in sorted(collections.Counter((str(e["c"].get("action")), "applied" if e["status"] == "applied" else "not applied")
                                                   for e in C).items()):
        P("    %-16s %-12s %4d" % (act, st, n))
    for e in C:
        if e["status"] != "applied":
            P("    %s on %s: %s" % (e["id"], e["target"], e["status"]))
    P("  entity merges through the alias map: %d %s" % (len(b.alias), dict(sorted(b.alias.items())) if b.alias else ""))
    P("  verified marks: %d true, %d false, %d on unknown rows" % (b.edits["verified"], b.edits["verified_false"], len(b.edits["verified_unknown"])))
    P("  hidden rows: %s" % ", ".join(sorted(r for r, a in b.assertions.items() if a["hidden"])))
    P("  source tiers: %s" % dict(sorted(collections.Counter(a["tier"] for a in b.assertions.values()).items())))
    leak = [r for r, a in b.assertions.items() if a["graph"] in ("prosecution", "rey") and not a["source"].startswith("src:acta-")]
    if SECOND_HAND_TO_PRESS:
        P("  assertions in the prosecution / rey graphs whose source is not a record page: %d" % len(leak))
        ok &= not leak
    P("")
    P("Analyst opinions (graph 'analysis'): %d; uc:basedOn links resolved: %d, not resolved: %d"
      % (sum(1 for a in b.assertions.values() if a["kind"] == "opinions"), getattr(b, "basis_resolved", 0),
         len(getattr(b, "basis_unresolved", []))))
    for rid, r in getattr(b, "basis_unresolved", []):
        P("    %s -> %s" % (rid, r))
    stray = [r for r, a in b.assertions.items() if (a["kind"] == "opinions") != (a["graph"] == ANALYSIS_GRAPH)]
    P("  sourced assertions in the analysis graph or opinions outside it: %d" % len(stray))
    ok &= not stray
    P("")
    P("Derived links")
    for k, n in sorted(b.derived.items()):
        P("  %-88s %4d" % (k, n))
    P("")
    # serialisation round trips
    P("Serialisation checks")
    try:
        t = Graph()
        t.parse(ttl_path, format="turtle")
        same = set(t) == union
        P("  graph.ttl    parses: %d triples; identical to the union graph: %s" % (len(t), same))
        ok &= same
        d = Dataset()
        d.parse(trig_path, format="trig")
        per = {}
        for g in d.graphs():
            if len(g):
                per[str(g.identifier)] = set(g)
        same = all(per.get(str(b.graphs[n].identifier), set()) == set(b.graphs[n]) for n in GRAPH_NAMES)
        tot = {(s, p, o) for s, p, o, _ in d.quads((None, None, None, None))}
        same &= tot == union
        P("  graph.trig   parses: %d quads in %d graphs; identical to the built dataset: %s"
          % (len(list(d.quads((None, None, None, None)))), len(per), same))
        ok &= same
        j = Graph()
        j.parse(jsonld_path, format="json-ld")
        jt = set(j)
        same = jt == union
        P("  graph.jsonld parses: %d triples vs %d in the union; identical triple set: %s  (the 'graph' key is not"
          % (len(jt), len(union), same))
        P("               mapped in the @context, so it adds no triple)")
        if not same:
            for tr in sorted(union - jt, key=str)[:5]:
                P("    only in union : %s" % (tr,))
            for tr in sorted(jt - union, key=str)[:5]:
                P("    only in jsonld: %s" % (tr,))
        ok &= same
        raw = json.load(open(jsonld_path, encoding="utf-8"))
        flat = isinstance(raw, dict) and set(raw) == {"@context", "@graph"} and all(
            isinstance(n, dict) and "@id" in n and isinstance(n.get("@type"), list) for n in raw["@graph"])
        ids = [n["@id"] for n in raw["@graph"]]
        P("  graph.jsonld shape: one object with @context and flat @graph: %s; nodes: %d; duplicate @id: %d"
          % (flat, len(ids), len(ids) - len(set(ids))))
        ag = [n for n in raw["@graph"] if "graph" in n]
        P("               nodes with 'graph': %d (= assertion nodes: %s); values: %s"
          % (len(ag), len(ag) == len(b.assertions), dict(sorted(collections.Counter(n["graph"] for n in ag).items()))))
        known_ids = set(ids)
        ref_terms = [t for t, v in ctx.items() if isinstance(v, dict) and v.get("@type") == "@id"]
        bad = sorted({v for n in raw["@graph"] for t in ref_terms if t in n
                      for v in (n[t] if isinstance(n[t], list) else [n[t]])
                      if v.startswith("ucr:") and v not in known_ids})
        P("               id references that do not resolve to a node in @graph: %d %s" % (len(bad), bad[:5] if bad else ""))
        ok &= flat and len(ids) == len(set(ids)) and len(ag) == len(b.assertions) and not bad
    except Exception as e:  # noqa
        ok = False
        P("  FAILED: %r" % e)
    P("")
    # SPARQL
    prefix, queries = read_queries(mapping_path)
    P("SPARQL queries from fibo_mapping.md, run on the real data (%d found)" % len(queries))
    q_results = {}
    if queries:
        install_join_orderer()
        qds = Dataset(default_union=True)
        for s, p, o, g in b.ds.quads((None, None, None, None)):
            gid = g.identifier if isinstance(g, Graph) else g
            qds.add((s, p, o, gid))
        if ontology is not None:
            og = qds.graph(URIRef("urn:x-ueno:ontology"))
            for tr in ontology:
                og.add(tr)
        for title, q in queries:
            try:
                res = qds.query(prefix + "\n" + q)
                rows = sorted(tuple(" | ".join(sorted(short(v).split(" | "))) for v in r) for r in res)
                heads = [str(v) for v in res.vars]
            except Exception as e:  # noqa
                P("  %s\n    FAILED: %s" % (title, str(e)[:200]))
                ok = False
                continue
            q_results[title] = len(rows)
            P("  %s" % title)
            P("    rows: %d%s" % (len(rows), " (first rows, sorted for a stable printout)" if rows else ""))
            if rows:
                P("    columns: " + " | ".join(heads))
                for r in rows[:6]:
                    P("      " + " | ".join(x if len(x) <= 46 else x[:43] + "..." for x in r))
                if len(rows) > 6:
                    P("      ... %d more" % (len(rows) - 6))
    P("")
    P("Warnings while loading: %d (see data/merge_report.md)" % len(log.warnings))
    P("OVERALL: %s" % ("all checks passed" if ok else "CHECKS FAILED - see above"))
    return "\n".join(R), ok, q_results


def write_merge_report(b, log, path, inventory, exact, similar, oddities):
    L = []
    A = L.append
    A("# Merge report (generated by data/build_graph.py - do not edit by hand)")
    A("")
    A("Things a human should review. The builder never merges two different ids on its own; to merge, add a pair "
      "to `ALIAS_MAP` at the top of `data/build_graph.py` and re-run.")
    A("")
    A("## Input files")
    A("")
    A("| file | rows read | malformed lines |")
    A("|---|---|---|")
    for f in inventory:
        A("| %s | %d | %d |" % (f["file"], f["rows"], f["malformed"]))
    if log.notes.get("empty_files"):
        A("")
        A("Empty (0 rows) at build time: " + ", ".join("`%s`" % x for x in log.notes["empty_files"]) + ".")
    for expected in ("chrono",):
        if not any(f["file"].startswith(expected + ".") for f in inventory):
            A("")
            A("No `%s.*` files were present at build time; re-run when they arrive." % expected)
    A("")
    A("## Editor corrections (edit.corrections.jsonl)")
    A("")
    C = b.edits["corrections"]
    A("%d corrections read, %d applied, %d not applied. Applied corrections change the value in the graph; the node keeps "
      "`originalValue`, `correctedField`, `editorNote` and a link to the `Correction` node." % (
          len(C), sum(1 for e in C if e["status"] == "applied"), sum(1 for e in C if e["status"] != "applied")))
    A("")
    bad = [e for e in C if e["status"] != "applied"]
    A("\n".join("- `%s` on `%s` (%s %s): %s" % (e["id"], e["target"], e["c"].get("action"), e["c"].get("field"), e["status"]) for e in bad)
      or "Every correction could be applied.")
    A("")
    A("## Entity merges applied through the alias map")
    A("")
    A("\n".join("- " + x for x in b.edits["merge_notes"]) or "None from edit.entity_merges.jsonl.")
    A("")
    A("\n".join("- alias in force: `%s` -> `%s` (%d references rewritten)" % (a_, c_, n) for (a_, c_), n in sorted(b.alias_applied.items())) or "")
    A("")
    A("## Verification marks, hidden rows, source kinds")
    A("")
    A("- verified: %d rows true, %d rows false, unknown rows: %s" % (b.edits["verified"], b.edits["verified_false"],
                                                                 ", ".join(b.edits["verified_unknown"]) or "none"))
    A("- hidden: " + (", ".join("`%s`" % r for r, a_ in sorted(b.assertions.items()) if a_["hidden"]) or "none"))
    for x in log.notes.get("source_kinds", []):
        A("- " + x)
    if b.editorial:
        A("- editorial labels (source `%s`) given to: %s" % (EDITORIAL_SOURCE["id"], ", ".join("`%s`" % e for e in b.editorial)))
    A("")
    A("## Same-operation groups (sameOperationKey)")
    A("")
    A("\n".join("- %s: %s" % (k, ", ".join(g_)) for k, g_ in b.same_op_groups) or "None.")
    A("")
    A("## Same id described by several contributors (merged, same id = same entity)")
    A("")
    A("\n".join("- " + x for x in log.notes.get("entity_merges", [])) or "None.")
    A("")
    A("## Entity conflicts")
    A("")
    A("\n".join("- " + x for x in log.notes.get("entity_conflicts", []) + log.notes.get("source_conflicts", [])) or "None.")
    A("")
    A("## Suspected duplicates with different ids (NOT merged)")
    A("")

    def lab(sid):
        e = b.entities.get(sid)
        return ("%s" % e["label"]) if e else "(stub, not described)"

    A("### Same normalised name")
    A("")
    if exact:
        A("| id A | label A | id B | label B | shared normalised name |")
        A("|---|---|---|---|---|")
        for a, c, n in exact:
            A("| `%s` | %s | `%s` | %s | %s |" % (a, lab(a), c, lab(c), n))
    else:
        A("None.")
    A("")
    A("### Similar names (weaker signal: one name contains the other, or close spelling)")
    A("")
    if similar:
        A("| id A | label A | id B | label B | why | similarity |")
        A("|---|---|---|---|---|---|")
        for a, c, x, y, why, r in similar:
            A("| `%s` | %s | `%s` | %s | %s (\"%s\" / \"%s\") | %.2f |" % (a, lab(a), c, lab(c), why, x, y, r))
    else:
        A("None.")
    A("")
    A("## References to entities that no contributor has described (stub parties)")
    A("")
    stubs = sorted(s for s in b.stubs if s not in b.entities)
    if stubs:
        A("Each id below is used by assertions but has no row in any `*.entities.jsonl`. The graph contains a stub "
          "(`uc:isStub true`, placeholder label made from the id) so no assertion is lost.")
        A("")
        A("| id | references | by contributor | first rows |")
        A("|---|---|---|---|")
        for s in stubs:
            refs = b.stubs[s]
            tags = collections.Counter(r.split(":")[0] for r in refs)
            A("| `%s` | %d | %s | %s |" % (s, len(refs), ", ".join("%s %d" % kv for kv in sorted(tags.items())),
                                         ", ".join(sorted(set(refs))[:4])))
    else:
        A("None.")
    A("")
    A("## Unknown sources and other unresolved references")
    A("")
    items = ["source `%s` is cited by %d rows but defined in no `*.sources.jsonl` (stub source created)" % (s, len(v))
             for s, v in sorted(b.stub_sources.items())] + log.notes.get("unknown_refs", [])
    A("\n".join("- " + x for x in items) or "None.")
    A("")
    A("## Rows dropped")
    A("")
    if log.dropped:
        A("| file | line | row id | reason |")
        A("|---|---|---|---|")
        for d in log.dropped:
            A("| %s | %s | %s | %s |" % d)
    else:
        A("None.")
    A("")
    A("## Loan records sharing an operation number")
    A("")
    A("\n".join("- " + x for x in log.notes.get("same_op", [])) or "None.")
    A("")
    A("## Dates that needed normalisation")
    A("")
    A("\n".join("- " + x for x in b.date_notes) or "None.")
    A("")
    A("## Enumeration values not in ontology.ttl")
    A("")
    A("\n".join("- `uc:%s` used %d times as %s" % (k[0], n, k[1]) for k, n in sorted(b.enum_unknown.items())) or "None.")
    A("")
    A("## Raw fields without a mapping (copied as `uc:x_<field>` text)")
    A("")
    A("\n".join("- `%s`: %d values" % kv for kv in sorted(b.unmapped.items())) or "None.")
    A("")
    A("## Things in the raw data that look wrong or need a second look")
    A("")
    allodd = log.notes.get("oddities", []) + oddities
    A("\n".join("- " + x for x in allodd) or "None.")
    A("")
    A("## Loader warnings")
    A("")
    A("\n".join("- " + x for x in log.warnings) or "None.")
    A("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))


# ---------------------------------------------------------------------------------------------
# README for the front-end developer
# ---------------------------------------------------------------------------------------------

def write_readme(b, ctx, nodes, stats, path, ontology):
    by_id = {n["@id"]: n for n in nodes}

    def pick(pred):
        return next((n for n in nodes if pred(n)), None)

    def show(n):
        return "```json\n%s\n```" % json.dumps(n, ensure_ascii=False, indent=2) if n else "_(no such node in the current data)_"

    loan = pick(lambda n: "Loan" in n["@type"] and "ultimateRecipient" in n and n.get("graph") == "prosecution") or \
        pick(lambda n: "Loan" in n["@type"] and "ultimateRecipient" in n) or pick(lambda n: "Loan" in n["@type"])
    flow = None
    if loan and loan.get("recipientDerivedFrom"):
        flow = by_id.get(loan["recipientDerivedFrom"][0])
    flow = flow or pick(lambda n: "Flow" in n["@type"] and "amount" in n and "linkedLoan" in n) or pick(lambda n: "Flow" in n["@type"])
    event = pick(lambda n: "CaseEvent" in n["@type"] and "amount" in n and n.get("datePrecision") == "day") or \
        pick(lambda n: "CaseEvent" in n["@type"])

    def enum_vals(prefix):
        vals = sorted(k for k in ctx if k.startswith(prefix))
        onto = sorted(str(s).split("#")[-1] for s in ontology.subjects(RDF.type, SKOS.Concept)
                      if str(s).split("#")[-1].startswith(prefix)) if ontology is not None else []
        return ", ".join("`%s`" % v for v in (onto or vals))

    asserters = ", ".join("`%s`" % v for v in ["Prosecution", "Rey", "Defence", "Regulator", "Press", "RatingAgency", "Company", "Analyst"])
    used_asserters = ", ".join("`%s` %d" % (ASSERTER_CONCEPT[k], v) for k, v in stats["assertions_by_asserter"].items())
    x_terms = sorted(b.x_terms)
    cur = ", ".join("`%s`" % c for c in sorted(b.currencies)) or "`PYG`, `USD`"
    T = []
    A = T.append
    A("# site/data - files for the interactive page")
    A("")
    A("Generated by `python3 data/build_graph.py`. Do not edit these files by hand: re-run the script. "
      "Output is deterministic, so a re-run with unchanged inputs gives byte-identical files.")
    A("")
    A("| file | what it is |")
    A("|---|---|")
    A("| `graph.jsonld` | The whole graph as one flat JSON-LD document. **This is the file the page loads.** |")
    A("| `stats.json` | Pre-computed counts and loan-principal totals. |")
    A("| `graph.trig` | Same data as RDF named graphs (default, prosecution, rey, press). |")
    A("| `graph.ttl` | Same data as one Turtle graph (union of the named graphs). |")
    A("| `ontology.ttl` | Copy of `data/ontology.ttl`, the vocabulary (`uc:`). |")
    A("")
    A("Current size: %d nodes, of which %d assertion nodes, %d parties (%d of them stubs) and %d sources."
      % (len(nodes), len(b.assertions), len(b.entities) + stats["parties"]["stubs"], stats["parties"]["stubs"], len(b.sources)))
    A("")
    A("## Rules that matter for the page")
    A("")
    A("1. **Everything about the case is a claim.** A loan, flow, role, event, figure, charge or data issue is a node that says "
      "who asserts it (`assertedBy`), where it was read (`source`, `locator`, `quote`) and how well it could be read (`confidence`). "
      "Show it as \"X alleges / reports ...\", never as fact. Presumption of innocence applies to every person.")
    A("2. **Never merge voices.** `graph` is `prosecution`, `rey` or `press`. Two nodes that describe the same loan from two voices "
      "stay two nodes (linked by `sameSubjectAs` when the builder can prove it).")
    A("3. **Do not add amounts across sources or voices.** The same loan or transfer is often reported by several sources. "
      "Use `stats.json` for totals, and keep its groups apart.")
    A("4. **`confidence`** is how well the contributor could read the source (`high`, `medium`, `low`), not how likely the claim is to be true.")
    A("")
    A("## Document shape")
    A("")
    A("```json\n{\n  \"@context\": { ...terms... },\n  \"@graph\": [ { \"@id\": \"...\", \"@type\": [\"...\"], ... }, ... ]\n}\n```")
    A("")
    A("- One top-level object with exactly two keys. `@graph` is a **flat array**: no nesting, no blank nodes. "
      "You can use it with `JSON.parse` only; no JSON-LD library is needed.")
    A("- Every node has `@id` (string) and `@type` (**always an array**; the first element is the main type).")
    A("- **Ids** are compact: `ucr:` + the project id with `:` turned into `/`. `org:ueno-bank` is `ucr:org/ueno-bank`, "
      "`rec:loan:0007` is `ucr:rec/loan/0007`, `src:acta-p05` is `ucr:src/acta-p05`. Every party, source and assertion node "
      "also has `identifier`, the original project id (`org:ueno-bank`).")
    A("- **References are plain id strings** (never `{\"@id\": ...}` objects), for example `\"lender\": \"ucr:org/ueno-bank\"`. "
      "Build an index once: `const byId = Object.fromEntries(doc['@graph'].map(n => [n['@id'], n]))`. "
      "Every `ucr:` reference resolves to a node in `@graph` (the build checks this).")
    A("- **Enumerations** are short strings that are terms of the context: `\"roleType\": \"role_director\"`, "
      "`\"instrument\": \"instr_transfer\"`, `\"eventCategory\": \"cat_credit\"`, `\"assertedBy\": \"Prosecution\"`, `\"currency\": \"USD\"`.")
    A("- **Bilingual text** is an object `{\"en\": \"...\", \"es\": \"...\"}`; either language can be missing. "
      "`quote` uses the same shape with the single language of the original (almost always `es`).")
    A("- **Amounts and percentages are strings holding exact decimals** (`\"principal\": \"12500000\"`, `\"amount\": \"5936654.88\"`). "
      "Convert with `Number(x)` for display or charts. (JSON-LD turns JSON numbers with decimals into floating-point literals, "
      "so strings are the only safe form.) `termDays` and `page` are JSON integers; `amountIsApproximate` and `isStub` are JSON booleans.")
    A("- **Keys that are always arrays** (even with one value): `@type`, `involvesParty`, `altLabel`, `ultimateRecipient`, "
      "`recipientDerivedFrom`, `sameSubjectAs`, `concerns`%s. Inside `allegedOffence` / `allegedOffenceAdded` each language holds an array. "
      "Every other key holds a single value. A key is absent when there is no value (no `null`, no empty strings)."
      % ("".join(", `%s`" % t for t in x_terms if b.x_terms[t] == "strs")))
    A("- **`graph`** is present on assertion nodes only. It is not part of the RDF (it is deliberately not defined in `@context`, "
      "so JSON-LD processors ignore it and the document converts to exactly the triples of `graph.ttl`).")
    A("")
    A("### Dates")
    A("")
    A("Contributors write dates as `2026-06-15`, `2026-06`, `2026`, or periods such as `2025/2026` or `2025-09/2026-05`. Use these keys:")
    A("")
    A("| key | format | meaning |")
    A("|---|---|---|")
    A("| `sortDate` | `\"YYYY-MM-DD\"` | First day of the date or period. For sorting and timelines only; read `datePrecision` before displaying it. |")
    A("| `sortDateEnd` | `\"YYYY-MM-DD\"` | Last day of a period or of a role's end. Only when there is an end. |")
    A("| `datePrecision` | `day`, `month`, `year` | How precise the stated date is. Display `sortDate.slice(0, 10)`, `.slice(0, 7)` or `.slice(0, 4)` accordingly. Not set on roles. |")
    A("| `dateText` | string | The date or period exactly as written by the contributor (`\"2025/2026\"`, `\"undated (list published 2026-11-07)\"`). |")
    A("| `onDate`, `startDate`, `endDate`, `date` | `{\"@value\": \"2026-06\", \"@type\": \"xsd:gYearMonth\"}` | The RDF literal (`xsd:date`, `xsd:gYearMonth` or `xsd:gYear`). `onDate` for a single date, `startDate` + `endDate` for a period or role, `date` on sources. The page can ignore these. |")
    A("")
    A("A node with `dateText` but no `sortDate` is undated (or its date could not be read). When the contributor gave a full date "
      "but marked it as month precision, the builder keeps the month only and `dateText` keeps the original.")
    A("")
    A("## Node types")
    A("")
    A("### Provenance keys (on every assertion node)")
    A("")
    A("Assertion nodes are those with a `graph` key: `RoleHolding`, `Loan`, `Overdraft`, `Flow`, `CaseEvent`, `FinancialFact`, `Charge`, `Issue`, `PartyDescription`.")
    A("")
    A("| key | format | notes |")
    A("|---|---|---|")
    A("| `graph` | `prosecution`, `rey`, `press` | Named graph. `prosecution` and `rey` hold those two voices; `press` holds every other voice (see `assertedBy`). |")
    A("| `assertedBy` | %s | The exact voice. In the current data: %s. |" % (asserters, used_asserters))
    A("| `source` | id of a `Source` node | Always present. |")
    A("| `confidence` | `high`, `medium`, `low` | Always present. |")
    A("| `locator` | string | Page, table row or paragraph hint. |")
    A("| `quote` | `{\"es\": \"...\"}` | At most 12 words in the original language. |")
    A("| `provenanceNote` | string (English) | Caveat, or conflict with another source. |")
    A("| `involvesParty` | array of party ids | **Every party the assertion mentions**, whatever its part. Always present except on `Issue` and on events without parties. |")
    A("| `identifier` | string | Project id of the row, e.g. `rec:loan:0007`. |")
    A("")
    n2 = sum(b.second_hand.values())
    if SECOND_HAND_TO_PRESS:
        A("Note: `prosecution` and `rey` hold only what was read in the prosecution record itself. The %d claims of those two voices "
          "that reach us through the press or another document are in `press`, with `assertedBy` still `Prosecution` or `Rey`." % n2)
    else:
        A("Note: `graph` follows the voice, not the document. A prosecution claim reported by a newspaper has `graph: prosecution`, "
          "`assertedBy: Prosecution` and a press `source` (%d such nodes in the current data, for both voices). To tell what was read in "
          "the prosecution record itself from what was reported, test `byId[n.source].sourceKind === 'record'`." % n2)
    A("")
    A("### Party: `Person`, `Organisation`, `Authority` (no `graph`)")
    A("")
    A("| key | format | notes |")
    A("|---|---|---|")
    A("| `@type` | `[\"Person\"]`, `[\"Organisation\"]`, `[\"Authority\"]` | Companies are `Organisation`. A few carry a second type: `Bank`, `CentralBank`, `BrokerDealer`, `RegulatoryAgency`. A stub with an unusual id is `Party`. |")
    A("| `label` | string | Display name. |")
    A("| `altLabel` | array of strings | Other names and spellings. |")
    A("| `description` | `{en, es}` | Short description. Its provenance is in the party's `PartyDescription` nodes. |")
    A("| `business` | `{en, es}` | What the company does, when known. |")
    A("| `isStub` | `true` | Only on parties that assertions mention but no contributor has described yet. `label` is then a placeholder made from the id. |")
    A("")
    A("### `Source` (no `graph`)")
    A("")
    A("| key | format | notes |")
    A("|---|---|---|")
    A("| `sourceKind` | `record`, `press`, `rating`, `official`, `company` | |")
    A("| `outlet` | string | Publisher. |")
    A("| `name` | string | Title of the document or article. |")
    A("| `url` | string | Absent for pages of the prosecution record. |")
    A("| `page` | integer | Page of the prosecution record. |")
    A("| `date`, `sortDate`, `datePrecision` | see Dates | Publication date. |")
    A("| `provenanceNote` | string | Free-text remark about the source (for example a page description that is not a number). |")
    A("")
    A("### `RoleHolding` - a person or company holds a position or stake")
    A("")
    A("| key | format | notes |")
    A("|---|---|---|")
    A("| `holder` | party id | |")
    A("| `organisation` | party id | For `role_relative_of` this is the other person. |")
    A("| `roleType` | %s | |" % enum_vals("role_"))
    A("| `percentage` | decimal string | Stake in percent, when stated. |")
    A("| `startDate`, `endDate`, `sortDate`, `sortDateEnd` | see Dates | `startDateText` / `endDateText` appear only when the original string was not a plain date. |")
    A("| `note` | `{en, es}` | |")
    A("")
    A("### `Loan` and `Overdraft` - a credit operation as described by one voice")
    A("")
    A("| key | format | notes |")
    A("|---|---|---|")
    A("| `@type` | `[\"Loan\"]`, `[\"Loan\", \"UnsecuredLoan\"]`, `[\"Overdraft\", \"Loan\"]`, ... | Test with `n['@type'].includes('Loan')`; overdrafts are also loans. `UnsecuredLoan` is added when `collateral` is `none`. |")
    A("| `lender`, `nominalBorrower` | party id | The borrower named on the operation. |")
    A("| `operationNumber` | string | |")
    A("| `principal`, `outstanding` | decimal string | In `currency`. |")
    A("| `currency` | %s | |" % cur)
    A("| `ratePct` | decimal string | Annual rate in percent. |")
    A("| `termYears` | decimal string | |")
    A("| `termDays` | integer | |")
    A("| `collateral` | string | Short code as stated: `none`, `mortgage_claimed`, `not stated`, ... |")
    A("| `amortisation` | string | Free text. |")
    A("| `loanStatus` | `outstanding`, `cancelled` | |")
    A("| `onDate`, `sortDate`, `datePrecision`, `dateText` | see Dates | Date of the operation. |")
    A("| `note` | `{en, es}` | |")
    A("| `ultimateRecipient` | array of party ids | **Derived by the builder.** See below. |")
    A("| `recipientDerivedFrom` | array of `Flow` ids | **Derived.** The flows that justify each `ultimateRecipient`. |")
    A("| `sameSubjectAs` | array of `Loan` ids | **Derived.** Loan records by another voice with the same operation number, lender and borrower. |")
    A("")
    A("### `Flow` - a movement of money or assets")
    A("")
    A("| key | format | notes |")
    A("|---|---|---|")
    A("| `fromParty`, `toParty` | party id | |")
    A("| `amount` | decimal string | Absent when the source names the parties but no amount. |")
    A("| `currency` | %s | |" % cur)
    A("| `amountIsApproximate` | boolean | |")
    A("| `instrument` | %s | |" % enum_vals("instr_"))
    A("| `purpose` | `{en, es}` | |")
    A("| `linkedLoan` | `Loan` id | The loan record this flow relates to. |")
    A("| `onDate` or `startDate` + `endDate`, `sortDate`, `sortDateEnd`, `datePrecision`, `dateText` | see Dates | |")
    A("")
    A("### `CaseEvent` - a dated item for the timelines")
    A("")
    A("| key | format | notes |")
    A("|---|---|---|")
    A("| `eventCategory` | %s | |" % enum_vals("cat_"))
    A("| `title` | `{en, es}` | |")
    A("| `description` | `{en, es}` | Detail text. |")
    A("| `involvesParty` | array of party ids | The parties of the event. |")
    A("| `amount`, `currency` | decimal string, currency | When the event has a figure. |")
    A("| `onDate`, `sortDate`, `datePrecision`, `dateText` | see Dates | |")
    A("")
    A("### `FinancialFact` - a reported figure about one party")
    A("")
    A("| key | format | notes |")
    A("|---|---|---|")
    A("| `aboutParty` | party id | |")
    A("| `metric` | string | Contributor's metric code, e.g. `debt_to_ueno_bank`. Not a closed list. |")
    A("| `amount` | decimal string | The value. A money amount when `currency` is present; otherwise a count, ratio or percentage explained by `unitNote`. |")
    A("| `textValue` | string | Used instead of `amount` when the value is not a number. |")
    A("| `currency` | %s | Absent for non-monetary values. |" % cur)
    A("| `unitNote` | string (English) | What the value measures. |")
    A("| `onDate` or `startDate` + `endDate`, `sortDate`, `sortDateEnd`, `datePrecision`, `dateText` | see Dates | The period the figure refers to. |")
    A("")
    A("### `Charge` - an offence alleged against a person (from `chrono.accused.jsonl`, when present)")
    A("")
    A("| key | format | notes |")
    A("|---|---|---|")
    A("| `chargedPerson` | party id | An allegation only. |")
    A("| `nameAsReported` | string | Name as printed by the source. |")
    A("| `roleReported` | `{en, es}` | |")
    A("| `allegedOffence` | `{\"es\": [\"...\", ...]}` | One string per offence, original language. |")
    A("| `allegedOffenceAdded` | `{\"es\": [...]}` | Offences reported as added later. |")
    A("| `proceduralMeasure` | `{\"en\": \"pretrial_prison\"}` | Contributor's code for the measure. |")
    A("| `defenceStatement` | `{en, es}` | Position of the defence as reported. |")
    A("| `onDate`, `sortDate`, `datePrecision`, `dateText` | see Dates | Date of the measure. |")
    A("")
    A("### `Issue` - a recorded inconsistency in the data")
    A("")
    A("| key | format | notes |")
    A("|---|---|---|")
    A("| `issueLocation` | string | Where it was found (\"Page 17\", \"Loan tables\"). |")
    A("| `description` | `{en, es}` | The issue. |")
    A("| `issueKind` | string | Only if the contributor gave one. |")
    A("| `concerns` | array of ids | Only if the contributor linked the issue to rows or parties. |")
    A("")
    A("### `PartyDescription` - where a party's name and description come from")
    A("")
    A("One per contributor row describing a party: `involvesParty` (one id: the party), `label`, `altLabel`, `description`, `business`, "
      "plus the provenance keys. Use it to show the source of a party's description; a party described by several contributors has several.")
    A("")
    A("### Other nodes")
    A("")
    A("- `ucr:dataset` (`@type` `[\"Ontology\"]`): the dataset itself, with `imports` pointing at the ontology.")
    A("- Nodes with `@type` `[\"DatatypeProperty\"]` (only when a contributor adds a field nobody has mapped yet): declarations of "
      "`x_` keys. The page can skip them: `n['@id'].startsWith('uc:')`.")
    if x_terms:
        A("- Keys starting with `x_` (%s) are raw contributor fields that have no mapping yet, copied as text." % ", ".join("`%s`" % t for t in x_terms))
    A("")
    A("## Derived keys")
    A("")
    A("Only these are computed by the builder; everything else is copied from a contributor row.")
    A("")
    A("| key | rule |")
    A("|---|---|")
    A("| `involvesParty` | Union of the node's own party references (`holder`, `organisation`, `lender`, `nominalBorrower`, `ultimateRecipient`, `fromParty`, `toParty`, `aboutParty`, `chargedPerson`, event parties). |")
    A("| `ultimateRecipient`, `recipientDerivedFrom` | Take the flows whose `linkedLoan` is this loan, asserted by the **same voice** as the loan, leaving out `instr_loan_disbursement`, `instr_repayment`, `instr_portfolio_assignment` and `instr_portfolio_sale_price`. Follow them from the nominal borrower. The parties where the chain ends (they receive and do not pass on) are the ultimate recipients. It means \"this voice says the proceeds ended up with R\", nothing more. |")
    A("| `sameSubjectAs` | Two loan records by different voices with the same `operationNumber`, lender and borrower. |")
    A("| `sortDate`, `sortDateEnd`, `datePrecision` | From the date string, see Dates. |")
    A("| stub parties, `isStub` | Created for ids that are referenced but not described. |")
    A("")
    A("## How to find all assertions about an entity")
    A("")
    A("```js\nconst doc = await (await fetch('data/graph.jsonld')).json();\nconst nodes = doc['@graph'];\nconst byId = Object.fromEntries(nodes.map(n => [n['@id'], n]));\n"
      "\n// every claim that mentions a party, whatever its part in it\nconst about = id => nodes.filter(n => n.graph && (n.involvesParty || []).includes(id));\n"
      "\nconst claims = about('ucr:org/ueno-bank');\nconst loansAsBorrower = claims.filter(n => n['@type'].includes('Loan') && n.nominalBorrower === 'ucr:org/ueno-bank');\n"
      "const rolesHeld  = claims.filter(n => n['@type'][0] === 'RoleHolding' && n.holder === 'ucr:org/ueno-bank');\n"
      "const byVoice    = Object.groupBy(claims, n => n.graph);   // prosecution / rey / press\n```")
    A("")
    A("`involvesParty` is the single place to look: it already includes every specific party key of the node. "
      "To find the part the party plays, compare the id with the specific keys (`holder`, `fromParty`, ...).")
    A("")
    A("## How provenance is attached")
    A("")
    A("Provenance is on the assertion node itself, not on a separate statement:")
    A("")
    A("```js\nconst n = byId['%s'];\nconst src = byId[n.source];            // Source node\n"
      "const where = src.url || ('record page ' + src.page);\n"
      "// \"<assertedBy> - <outlet>, <name>, <date> - <locator> - '<quote>' (confidence)\"\n"
      "const line = `${n.assertedBy} - ${src.outlet}, ${src.name}, ${src.sortDate} - ${n.locator || ''} - ${n.quote ? Object.values(n.quote)[0] : ''} (${n.confidence})`;\n```"
      % (loan["@id"] if loan else "ucr:rec/loan/0001"))
    A("")
    A("- One assertion has exactly one `source`, one `assertedBy`, one `confidence`.")
    A("- When two sources report the same thing there are two assertion nodes. Nothing is averaged or summed.")
    A("- Party nodes carry no provenance of their own; their `PartyDescription` nodes do.")
    A("")
    A("## Three real examples (copied from the current output)")
    A("")
    A("A loan:")
    A("")
    A(show(loan))
    A("")
    A("A flow%s:" % (" (one of the flows the loan above derives its ultimate recipient from)" if loan and flow and flow["@id"] in loan.get("recipientDerivedFrom", []) else ""))
    A("")
    A(show(flow))
    A("")
    A("An event:")
    A("")
    A(show(event))
    A("")
    A("And the source of the loan above:")
    A("")
    A(show(by_id.get(loan["source"]) if loan else None))
    A("")
    A("## `@context`")
    A("")
    A("The context defines one term per key and per enumeration value. Kinds of term:")
    A("")
    A("| kind | context entry | keys |")
    A("|---|---|---|")
    kinds = collections.defaultdict(list)
    allterms = dict(TERMS)
    allterms.update({t: (UC[t], k) for t, k in b.x_terms.items()})
    for t in sorted(allterms):
        if t in ctx:
            kinds[allterms[t][1]].append(t)
    desc = [("ref", "`{\"@type\": \"@id\"}`: one id string"), ("refs", "`{\"@type\": \"@id\", \"@container\": \"@set\"}`: array of id strings"),
            ("voc", "`{\"@type\": \"@vocab\"}`: one enumeration term"), ("lang", "`{\"@container\": \"@language\"}`: `{en, es}`"),
            ("langs", "`{\"@container\": \"@language\"}`: `{es: [...]}`"), ("str", "plain string"),
            ("strs", "`{\"@container\": \"@set\"}`: array of strings"), ("dec", "`{\"@type\": \"xsd:decimal\"}`: decimal as string"),
            ("int", "`{\"@type\": \"xsd:integer\"}`: JSON integer"), ("bool", "`{\"@type\": \"xsd:boolean\"}`: JSON boolean"),
            ("day", "`{\"@type\": \"xsd:date\"}`: `YYYY-MM-DD`"), ("anydate", "no coercion: `{\"@value\", \"@type\"}` object"),
            ("url", "`{\"@type\": \"xsd:anyURI\"}`: string")]
    for k, d in desc:
        if kinds.get(k):
            A("| %s | %s | %s |" % (k, d, ", ".join("`%s`" % t for t in kinds[k])))
    A("")
    A("## stats.json")
    A("")
    A("New blocks: `editor_layer` (corrections applied / not applied, merges, verified, hidden, alleged, same-operation groups) "
      "and `assertions_by_source_tier`.")
    A("")
    A("`nodes_by_type`, `assertions_by_class`, `assertions_by_asserter`, `assertions_by_graph`, `assertions_by_confidence`, "
      "`assertions_by_contributor`, `assertions_by_asserter_and_class`, `parties`, `sources`, `date_range` (min and max `sortDate`, overall and per class) "
      "and `loan_principal_by_borrower_currency.rows`: one row per borrower, currency, asserter and source document, with "
      "`principal_total` (= `principal_of_loans` + `principal_of_overdrafts`) and `outstanding_total` as decimal strings in the original currency. Currencies are never converted. "
      "Rows of different asserters or source documents can describe the same loans: show them side by side, do not add them.")
    A("")
    additions(A, b, nodes, by_id)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(T))


def additions(A, b, nodes, by_id):
    """README section 'Additions': everything added after the first release of the shape."""
    def show(n):
        return "```json\n%s\n```" % json.dumps(n, ensure_ascii=False, indent=2) if n else "_(no such node in the current data)_"

    def n(key):
        return sum(1 for x in nodes if key in x)
    A("## Additions")
    A("")
    A("Added on 20 November 2026 (second pass). The shape described above is unchanged: same node types, same keys, same value "
      "formats. Every key below is **optional**: it is simply absent when it does not apply. Counts are for the current data.")
    A("")
    A("### New keys on assertion nodes")
    A("")
    A("| key | format | on | meaning |")
    A("|---|---|---|---|")
    A("| `sourceTier` | `record`, `press_linked`, `rating_or_official`, `dossier`, `editorial`, `unlinked` | every assertion (%d) | Where the claim was read. `record`: a page of the prosecution record. `press_linked`: a document with a URL. `rating_or_official`: a rating report or official publication. `dossier`: the third-party dossier, which gives no links. `editorial`: a label supplied by the project from the SPEC id list. `unlinked`: any other source without a URL. |" % n("sourceTier"))
    A("| `alleged` | `true` | `Flow` and `CaseEvent` in the `prosecution` and `rey` graphs (%d) | The text states conduct. Prefix it: \"the prosecution alleges ...\" (`graph: prosecution`) or \"Rey states ...\" (`graph: rey`). Never present as `false`. |" % n("alleged"))
    A("| `hidden` | `true` | %d nodes | Keep the node out of visualisations (flow diagrams, ownership charts). It stays in the graph and can still be listed. |" % n("hidden"))
    A("| `hiddenReason` | `{en, es}` | with `hidden` | Why. |")
    A("| `verified` | boolean | %d nodes | `true`: the editor checked the row against its source. `false`: checked and not confirmed (see `verifiedNote`). Absent: not checked. |" % n("verified"))
    A("| `verifiedMethod` | string | with `verified` | How it was checked: `page image`, `ocr text`, `url`, `script + page image`, ... |")
    A("| `verifiedNote` | string (English) | with `verified` | The editor's remark. |")
    A("| `correctedField` | array of strings | %d assertion nodes | JSON keys of this node that an editor correction changed (`amount`, `confidence`, `provenanceNote`, `dateText`, `title`, `label`, ...). The node already shows the corrected value. |" % sum(1 for x in nodes if "correctedField" in x and "graph" in x))
    A("| `originalValue` | array of strings | with `correctedField` | One entry per correction, written `\"<key>: <value before the correction>\"`, e.g. `\"amount: 4230000\"`. `(empty)` means there was no value. |")
    A("| `editorNote` | `{en: [...], es: [...]}` | with `correctedField` | The editor's reason for each correction. Each language holds an **array**. |")
    A("| `correction` | array of `Correction` ids | with `correctedField` | The correction records, for the exact pairing of field, old value, new value and reason. |")
    A("| `correctionSource` | array of `Source` ids | with `correctedField` | Sources the corrections rely on. `source` is unchanged and still holds the single source of the row itself. (In RDF both keys are `prov:wasDerivedFrom`.) |")
    A("| `sameOperationKey` | string | `Loan`, `Overdraft`, `Flow` (%d nodes) | Nodes with the same key are alternative reports of one operation. Collapse them in the page: show one, list the others, never add their amounts. The key is the `identifier` of the first node of the group. |" % n("sameOperationKey"))
    A("| `restates` | `Flow` id | `CaseEvent` (%d) | The event restates a hidden flow as a statement by the same voice, with the same provenance. |" % n("restates"))
    A("")
    A("### New keys on `Charge` (they replace the provisional `x_` keys)")
    A("")
    A("| key | format | was |")
    A("|---|---|---|")
    A("| `caseReference` | string, e.g. `89/2026` | `x_case` |")
    A("| `detainedOn` | `\"YYYY-MM-DD\"` | `x_detained` |")
    A("| `measureRequested` | `{\"en\": \"house_arrest\"}` | `x_measure_requested` |")
    A("| `measureSource` | `Source` id: the source of the procedural measure | `x_measure_source` |")
    A("| `statusSource` | `Source` id: the source of the current status | `x_status_source` |")
    A("| `nextHearing` | string (English) | `x_next_hearing` |")
    A("| `placeReported` | string | `x_place_reported` |")
    A("| `previousMeasure` | string | `x_previous_measure` |")
    A("")
    A("The old `x_` keys were arrays of strings; the new keys hold a single value.")
    A("")
    A("### New node type: `Correction` (no `graph` key)")
    A("")
    A("One node per row of `edit.corrections.jsonl` (%d). It records an editorial change; it is not a claim about the case." % sum(1 for x in nodes if x["@type"] == ["Correction"]))
    A("")
    A("| key | format | notes |")
    A("|---|---|---|")
    A("| `correctsRow` | id of the corrected node | Absent when the target row was not found. For a corrected entity row this is its `PartyDescription`. |")
    A("| `correctionAction` | `set`, `set_confidence`, `add_note`, `merge_entity`, `delete_row` | `delete_row` never deletes: the row gets `hidden: true`. |")
    A("| `correctionStatus` | `applied` or `not applied: <reason>` | |")
    A("| `correctedField` | array with one JSON key | |")
    A("| `rawField` | string | Field name in the contributor file (`amount_is_approx`, `prov.note`). |")
    A("| `originalValue` | array with one string | Value before. |")
    A("| `newValue` | string | Value after. |")
    A("| `editorNote` | `{en: [...], es: [...]}` | Reason. |")
    A("| `checkedAgainst` | string | What the editor compared the row with. |")
    A("| `source`, `assertedBy`, `confidence`, `locator`, `quote`, `identifier` | as on assertions | Provenance of the correction. |")
    A("")
    A("### Changed values (same keys as before)")
    A("")
    A("- **`graph`**: `prosecution` and `rey` now contain only assertions read in the prosecution record itself (`sourceTier: record`). "
      "The %d prosecution or Rey claims reported by the press or the dossier are in `press`; their `assertedBy` is unchanged. "
      "So `graph` answers \"which layer\" and `assertedBy` answers \"whose voice\"." % sum(b.second_hand.values()))
    A("- **`sourceKind`** has two new values: `dossier` (the user-supplied dossier) and `project` (the SPEC id list used for editorial labels).")
    A("- **Merged parties**: %s. References were rewritten to the surviving id; the old name is an `altLabel`." % (
        ", ".join("`%s` into `%s`" % kv for kv in sorted(b.alias.items())) or "none"))
    stubs = sorted(x for x in b.stubs if x not in b.entities)
    A("- **Labels**: when contributors spell a name with and without accents, the accented form is the `label`. "
      "`ucr:org/u-holdings` is now \"U Holdings S.à r.l.\". The five parties that were stubs have editorial labels and no longer carry `isStub`. "
      "Stubs in the current data: %s." % (", ".join("`%s`" % x for x in stubs) or "none"))
    A("- **Corrected values**: %d editor corrections are applied to the values themselves (amounts, dates, titles, confidence, notes, parties)."
      % sum(1 for e in b.edits["corrections"] if e["status"] == "applied"))
    A("- The declaration nodes for builder terms (`@type` `Class` / `DatatypeProperty` / `ObjectProperty`, ids starting `uc:`) are gone: "
      "the terms are now defined in `ontology.ttl`.")
    A("- New file `verified.json`: a JSON array of the `@id`s of all nodes with `verified: true`.")
    A("")
    A("### Examples")
    A("")
    ex = next((x for x in nodes if "graph" in x and len(x.get("correctedField", [])) >= 2 and "sameOperationKey" in x), None) or \
        next((x for x in nodes if "graph" in x and "correctedField" in x), None)
    A("A corrected flow:")
    A("")
    A(show(ex))
    A("")
    A("One of its correction records:")
    A("")
    A(show(by_id.get(ex["correction"][0]) if ex else None))
    A("")
    A("A hidden flow and the event that restates it:")
    A("")
    ev = next((x for x in nodes if "restates" in x), None)
    A(show(by_id.get(ev["restates"]) if ev else None))
    A("")
    A(show(ev))
    A("")
    A("### Typical page code")
    A("")
    A("```js\nconst visible = nodes.filter(n => n.graph && !n.hidden);\n"
      "const prefix = n => n.alleged ? (n.graph === 'rey' ? 'Rey states: ' : 'The prosecution alleges: ') : '';\n"
      "// collapse alternative reports of one operation\n"
      "const groups = Object.groupBy(visible.filter(n => n.sameOperationKey), n => n.sameOperationKey);\n"
      "const verified = new Set(await (await fetch('data/verified.json')).json());   // or n.verified === true\n```")
    A("")
    third_pass(A, b, nodes, by_id, show)


def third_pass(A, b, nodes, by_id, show):
    ops = [x for x in nodes if x["@type"] == ["AnalystOpinion"]]
    A("### Third pass: analyst opinions (new node type, new graph)")
    A("")
    A("Added on 20 November 2026 (third pass). Nothing in the `prosecution`, `rey` and `press` graphs changed. "
      "There are %d new nodes of a new type, in a new graph." % len(ops))
    A("")
    A("- **`graph` has a fourth value, `analysis`.** It holds only `AnalystOpinion` nodes. Code that lists claims with "
      "`nodes.filter(n => n.graph)` now also gets these nodes: filter with `n.graph !== 'analysis'` (or by `@type`) wherever "
      "only sourced claims are wanted.")
    A("- **`sourceTier` has a new value, `analysis`**, on exactly these nodes.")
    A("- **`assertedBy` is `Analyst`** on these nodes. An analyst opinion is an estimate or interpretation by the project's "
      "analysts. It is never a finding of the record and never a sourced figure; present it as \"analyst estimate\" and do not add "
      "it to sourced amounts.")
    A("- These nodes have **no `involvesParty`**: `about(id)` does not return them. Reach the parties through `basedOn`.")
    A("")
    A("#### `AnalystOpinion`")
    A("")
    A("| key | format | notes |")
    A("|---|---|---|")
    A("| `opinionKind` | %s | Kind of opinion. |" % ", ".join("`%s`" % k for k in sorted({x.get("opinionKind", "") for x in ops} | {"headline", "meaning", "hypothesis", "recovery_scenario"}) if k))
    A("| `title` | `{en, es}` | Short title. |")
    A("| `description` | `{en, es}` | The full text of the opinion. |")
    A("| `estimateLow`, `estimateCentral`, `estimateHigh` | decimal string | The estimate, in `currency`. Any of the three can be absent (%d nodes have no figure at all). |" % sum(1 for x in ops if not any(k in x for k in ("estimateLow", "estimateCentral", "estimateHigh"))))
    A("| `currency` | `USD`, `PYG` | Currency of the estimates. |")
    A("| `basedOn` | array of assertion ids | The sourced assertions the opinion rests on. Each resolves to a node in `@graph` with its own `source`, `assertedBy` and `confidence`. Absent when the row gave no basis. |")
    A("| `graph`, `sourceTier`, `assertedBy`, `source`, `confidence`, `locator`, `provenanceNote`, `identifier` | as on assertions | `graph: \"analysis\"`, `sourceTier: \"analysis\"`, `assertedBy: \"Analyst\"`. `source` is the analysis document itself. `confidence` is the analysts' own grading. |")
    A("")
    A("Example:")
    A("")
    ex = next((x for x in ops if "estimateCentral" in x and 0 < len(x.get("basedOn", [])) <= 6), None) or (ops[0] if ops else None)
    A(show(ex))
    A("")
    A("```js\nconst opinions = nodes.filter(n => n.graph === 'analysis');\n"
      "const sourced  = nodes.filter(n => n.graph && n.graph !== 'analysis');\n"
      "const basis = o => (o.basedOn || []).map(id => byId[id]);          // the claims an estimate rests on\n```")
    A("")
    A("`stats.json` has a new block `analyst_opinions`, and `assertions_by_graph` now has an `analysis` entry.")
    A("")


# =============================================================================================
# main
# =============================================================================================

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--raw", default=os.path.join(HERE, "raw"), help="directory with <tag>.<kind>.jsonl files")
    ap.add_argument("--site", default=os.path.join(ROOT, "site", "data"), help="output directory")
    ap.add_argument("--report", default=os.path.join(HERE, "merge_report.md"), help="path of the merge report")
    ap.add_argument("--ontology", default=os.path.join(HERE, "ontology.ttl"))
    ap.add_argument("--mapping", default=os.path.join(HERE, "fibo_mapping.md"))
    ap.add_argument("--quiet", action="store_true", help="do not echo warnings to stderr")
    args = ap.parse_args(argv)

    log = Log(args.quiet)
    os.makedirs(args.site, exist_ok=True)
    ontology = None
    if os.path.exists(args.ontology):
        ontology = Graph()
        try:
            ontology.parse(args.ontology, format="turtle")
            if os.path.abspath(args.ontology) != os.path.abspath(os.path.join(args.site, "ontology.ttl")):
                shutil.copyfile(args.ontology, os.path.join(args.site, "ontology.ttl"))
        except Exception as e:  # noqa
            log.warn("ontology.ttl could not be parsed (%s); enumeration checks and Q5 are limited" % str(e)[:80])
            ontology = None
    else:
        log.warn("ontology file %s not found; not copied" % args.ontology)

    rows, inventory = load_raw(args.raw, log)
    edits = apply_edits(rows, log)
    b = Builder(rows, log, edits).run(ontology)

    trig, ttl, jsonld = (os.path.join(args.site, n) for n in ("graph.trig", "graph.ttl", "graph.jsonld"))
    write_trig(b, trig)
    write_ttl(b, ttl)
    ctx, nodes = build_jsonld(b)
    write_jsonld(ctx, nodes, jsonld)

    stats = make_stats(b, inventory, nodes)
    exact, similar = suspected_duplicates(b)
    oddities = extra_oddities(b)
    report, ok, q_results = run_checks(b, ontology, args.mapping, jsonld, ttl, trig, ctx, nodes, log)
    stats["triples"] = collections.OrderedDict(
        [("default", len(b.default))] + [(g, len(b.graphs[g])) for g in GRAPH_NAMES] + [("union", len(union_triples(b)))])
    stats["review"] = {"rows_dropped": len(log.dropped), "suspected_duplicates_same_name": len(exact),
                       "suspected_duplicates_similar_name": len(similar),
                       "stub_parties": stats["parties"]["stubs"], "unknown_sources": len(b.stub_sources)}
    with open(os.path.join(args.site, "stats.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=1)
        f.write("\n")
    with open(os.path.join(args.site, "verified.json"), "w", encoding="utf-8") as f:
        json.dump(["ucr:" + r.replace(":", "/") for r in sorted(set(b.verified_ids))], f, ensure_ascii=False, indent=0)
        f.write("\n")
    write_merge_report(b, log, args.report, inventory, exact, similar, oddities)
    write_readme(b, ctx, nodes, stats, os.path.join(args.site, "README.md"), ontology)

    print(report)
    print("")
    print("Review items written to %s: %d suspected duplicates with the same name, %d with similar names, %d stub parties, "
          "%d other oddities" % (os.path.relpath(args.report, ROOT), len(exact), len(similar), stats["parties"]["stubs"],
                                 len(log.notes.get("oddities", [])) + len(oddities)))
    print("")
    print("Output files")
    for n in ("graph.trig", "graph.ttl", "graph.jsonld", "ontology.ttl", "stats.json", "verified.json", "README.md"):
        p = os.path.join(args.site, n)
        if os.path.exists(p):
            print("  %-14s %9d bytes" % (n, os.path.getsize(p)))
    print("  %-14s %9d bytes" % (os.path.basename(args.report), os.path.getsize(args.report)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
