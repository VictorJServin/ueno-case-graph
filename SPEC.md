# Ueno Bank case knowledge graph: shared spec for all contributors

Everyone working on this project reads this file first and follows it exactly.

## What we are building

A provenance-first knowledge graph of the Ueno Bank S.A. case (Paraguay, Case 89/2026), published as real RDF
(Turtle + JSON-LD) and explored through an interactive HTML report (companies, people, money flows, timelines).

## Ground rules

1. Every data point carries provenance. No row without a `source` block. If you cannot source it, leave it out.
2. Everything about wrongdoing is ALLEGATION. Record who asserts it (`asserted_by`). Presumption of innocence
   applies to every person. Never write that someone "did" something unlawful; write that X alleges it.
3. Two primary voices in the prosecution record must never be merged: `prosecution` (pages 1-19, summarising the
   bank supervisor) and `rey` (pages 19-24, the suspect's own statement).
4. People appear only in publicly reported or record-stated roles relevant to the case. Do NOT collect or record
   home addresses, ID numbers, dates of birth, photos, personal social accounts, or family details beyond what
   the record or an outlet states as relevant to the case (for example a stated kinship used to argue related-party status).
5. Quotes: at most 12 words, in the original language, in `quote`. Paraphrase everything else.
6. Dates ISO (`2026-06-15`). If only month or year is known, give `2026-06` or `2026` and set `date_precision`
   to `month` or `year`.
7. Amounts: plain numbers, no separators; `currency` is `PYG` or `USD`. Guaraní figures: beware "millones" vs
   "mil millones"; write the full number (Gs. 314.001 millones = 314001000000).
8. Labels and descriptions in both English (`_en`) and Spanish (`_es`). Keep them short and factual.
9. Cutoff: information up to 20 November 2026.
10. `confidence`: `high` (read directly and clearly from the source), `medium` (source is clear but second-hand,
    or summarised), `low` (hard-to-read diagram small print, single uncorroborated outlet, or inferred mapping).

## Source files already on disk

- `source/acta_ocr_es.txt`: OCR of the 24-page prosecution record (Spanish, imperfect; page 12 is garbled because
  it was scanned upside down). `source/v-01.jpg` ... `v-24.jpg` are page images (`v-12r.jpg` is page 12 rotated).
- `source/map_v3_index.html`: the previous interactive page; its JS arrays `N` (nodes) and `E` (edges) hold the
  roles and flows already extracted from the record.
- `research_notes/*/*.md` and `reports/*.md`: press research already done (8 notes files, 2 reports), with URLs.

## Entity IDs (use these exactly; mint new ones with the same pattern: `org:` / `person:` / `auth:` + lowercase-hyphen slug)

Organisations: org:ueno-bank, org:grupo-vazquez, org:itti, org:redisa, org:redipro, org:vinanzas, org:kaitel,
org:ueno-casa-de-bolsa, org:ueno-seguros, org:ueno-afpisa, org:technoma, org:terravaz, org:kasas-propiedades,
org:model, org:discover-paraguay, org:mulair, org:u-holdings, org:u-paraguay, org:otp-bank,
org:mowi, org:grupo-hendy, org:grupo-m, org:tuiu, org:franede, org:aime,
org:satec, org:hd-invest, org:la-tropa-fletes, org:factopar,
org:nuevo-mundo-entertainment, org:nubicom, org:gsr, org:office-design, org:grupo-berilo, org:galadriel,
org:henrici, org:dataforge, org:pear-srl, org:comitia, org:cadiem, org:vision-banco, org:financiera-el-comercio,
org:ips, org:zeta-banco, org:mckinsey

Authorities: auth:bcp, auth:superintendencia-de-bancos, auth:superintendencia-de-valores, auth:ministerio-publico,
auth:senado, auth:fgd

People (bank board): person:miguel-vazquez, person:juan-manuel-gustale, person:julio-rey, person:diana-mongelos,
person:mariana-torres, person:alejandro-gomez-abente, person:diego-duarte, person:miguel-angel-almada
People (companies): person:jose-augusto-sala-cardozo, person:sergio-pizurno, person:vanessa-godoy,
person:oscar-urdapilleta, person:diego-gomez, person:cesar-mengual, person:miguel-angel-garay,
person:cesar-astigarraga, person:luis-ernesto-angulo, person:guillermo-vazquez, person:paola-meza,
person:marcelo-gimenez-recalde, person:rudolph-goetz, person:luis-fernando-rios, person:andre-gayol-pires,
person:nicolas-di-iorio, person:rodrigo-franco, person:mauro-vargas, person:martin-vargas,
person:cecilia-dominguez, person:gloria-villasanti, person:raul-sanchez, person:lucca-de-barba
People (public office): person:santiago-pena, person:carlos-carvallo, person:holger-insfran

## Source IDs

- Record pages: `src:acta-p01` ... `src:acta-p24`.
- Anything else: mint `src:<outlet>-<yyyy-mm-dd>-<short-slug>` and add a row to your `sources` file.

## Output files (JSON Lines, one object per line, UTF-8) in `data/raw/`, prefixed with your contributor tag

`<tag>.sources.jsonl`
  {"id","kind":"record|press|rating|official|company","outlet","title","date","url","page"}

`<tag>.entities.jsonl`
  {"id","type":"Person|Company|Authority","label","aliases":[],"desc_en","desc_es","business_en","business_es", "prov":{...}}

`<tag>.roles.jsonl`   (a person or company holding a position or stake in an organisation)
  {"id","holder","org","role":"shareholder|beneficial_owner|president|vice_president|director|alternate_director|
   statutory_auditor|alternate_statutory_auditor|officer|employee|founder|legal_representative|registry_agent|
   group_role|related_group_member|relative_of|controlling_group|charged_person","pct","start","end",
   "note_en","note_es","prov":{...}}

`<tag>.loans.jsonl`
  {"id","lender","borrower","op_number","kind":"loan|overdraft","date","term_years","term_days","rate_pct",
   "currency","principal","outstanding","collateral":"none|mortgage_claimed|...","amortisation","status":"outstanding|cancelled",
   "note_en","note_es","prov":{...}}

`<tag>.flows.jsonl`   (a movement of money or assets between two parties)
  {"id","from","to","amount","currency","date","date_precision","instrument":"loan_disbursement|transfer|
   bond_purchase|loan|contract|repayment|portfolio_sale_price|portfolio_assignment|cash_delivery|cheque|other",
   "purpose_en","purpose_es","linked_loan","amount_is_approx":true|false,"prov":{...}}
  If the source names sender and receiver but no amount, set "amount": null.

`<tag>.events.jsonl`  (anything with a date, for the timelines)
  {"id","date","date_precision":"day|month|year","category":"corporate|credit|supervisory|criminal|political|
   market|statement|depositor","title_en","title_es","detail_en","detail_es","parties":[entity ids],
   "amount","currency","prov":{...}}

`prov` block (required on every row):
  {"asserted_by":"prosecution|rey|defence|regulator|rating_agency|company|press","source":"src:...",
   "locator":"page / table row / paragraph hint","quote":"<=12 words original language or empty",
   "confidence":"high|medium|low","note":"optional caveat, conflict with another source, etc."}

IDs for rows: `<tag>:<type>:<n>` (for example `rec:loan:0007`).
