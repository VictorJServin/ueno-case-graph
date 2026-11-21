# Data editor report: Ueno Bank knowledge graph

Editor pass of 20 November 2026 over `data/raw/` (1,795 data rows in 21 files, plus 4 sources files).
No file in `data/raw/` was edited. Output: `edit.corrections.jsonl` (126 corrections on 99 rows),
`edit.verified.jsonl` (360 rows), `edit.entity_merges.jsonl` (6 merges).

## 1. Bottom line

- The record tables were extracted accurately. All 35 table loans, all 9 portfolio items and every table-derived
  role, percentage and date match the page images cell for cell.
- The page 17 diagram was not. Nine flow amounts were wrong or rounded. They are now fixed to the cent, and the
  fix is proven by arithmetic: the six legs into Vinanzas sum exactly to the printed USD 76,061,604.13.
- The Vinanzas balance on 14 June 2026 cannot be settled from this scan. I recommend showing USD 93,828 at low
  confidence (reasoning in section 4).
- The press layer is faithful to its sources: 22 of 25 spot-checked rows pass, and the 3 failures are a missing
  date, an unsupported borrower and an amount taken from a different article.
- Privacy is clean: no ID numbers, birth dates, addresses or phone numbers anywhere in the data, although page 19
  of the record contains all of them for Rey.

## 2. What was checked

| Check | Scope | Method |
|---|---|---|
| Record tables | pp. 3-9, 11-16, 18 | Native-resolution page images extracted from the PDF (about 2,100 px wide), read cell by cell |
| Record diagrams | pp. 2, 10, 17 | Crops at 300-700%; glyph-level comparison for the disputed digit; arithmetic closure; press figures quoting the BCP file |
| Record text | pp. 1, 19-24 | OCR text; pages 21 and 24 (absent from OCR) and the page 11/12 and 15/16 breaks read on images |
| Consistency | all contributors | Scripts: provenance, dates, currencies, entity ids, duplicates, quote-versus-value, record-versus-press loans |
| Press spot-check | 25 rows (plus 29 others on the same pages) | Cited URLs re-opened (16 articles) |
| Privacy and fairness | all text fields | Pattern scan plus reading of every hit |

## 3. Pass rates by file

| File | Rows | Checked | Pass | Notes |
|---|---|---|---|---|
| rec.loans | 40 | 40 | 40 | 6 FRANEDE rows need a collateral note; 5 diagram loans confirmed |
| rec.roles | 120 | 120 | 120 | 1 percentage added (80%); 1 duplicate; 6 rows are a modelling problem |
| rec.flows | 78 | 78 | 67 | 9 diagram amounts corrected; 2 rows are not real flows; 12 malformed dates |
| rec.events | 68 | 68 | 67 | Events 1-39 mirror the loan table exactly; 1 amount unsettled; 3 titles reworded |
| press (facts, flows, loans) | 551 | 41 | 38 | Core sample: 17 of 19 pass |
| chrono (events, roles) | 323 | 13 | 12 | Core sample: 5 of 6 pass |
| dos.* | 50 | script only | n/a | Untraceable by design; 2 rows down-weighted |

Not individually verified: `rec.entities`, `press.entities`, `chrono.entities`, `press.roles`, `press.events`,
`chrono.accused` (script checks only) and the roughly 500 press and chrono rows outside the sample.

### Press spot-check, 25 core rows

| Row | Claim | Result |
|---|---|---|
| press:fact:0036 | Vinanzas balance USD 93,828 on 14 June | pass |
| press:fact:0037 | USD 76,061,604.13 received 15 June | pass |
| press:flow:0038 | Portfolio USD 74,418,418.12, 15 June 2026 | pass |
| press:loan:0013 | Grupo M USD 14.3 M on 26/09/2025 | fail: amount printed, date not stated |
| press:loan:0025 | GSR G. 132,660 M, 1 June 2026 | pass |
| press:loan:0032 | GSR terms 3,600 days / ten years | pass |
| press:flow:0049 | Technoma to ITTI bonds USD 4,230,383.21 | pass |
| press:flow:0050 | USD 5,769,861 bond leg | pass (article says ueno bank bonds sold by Grupo Vázquez) |
| press:flow:0053 | ITTI to Vinanzas USD 4,678,670 | pass |
| press:flow:0062 | Grupo Vázquez to Vinanzas USD 4,215,707 | pass |
| press:loan:0034 | Grupo M overdraft USD 6,321,573.22 | pass |
| press:loan:0035 | Borrower of op. 612561002345 is Redipro | fail: article names no borrower; record says Grupo Hendy |
| press:loan:0010 | Henrici USD 10.593 M, 27 March 2026 | pass as printed (conflicts with record) |
| press:fact:0024 | GSR financing USD 72.8 M | pass |
| press:flow:0091 | Nubicom to ITTI G. 415,000 M | pass |
| press:flow:0093 | G. 285,600 M repaid 31 July via ITTI | pass |
| press:loan:0045 | Nubicom G. 417,075 M, 1 July 2026 | pass |
| press:fact:0097 | Nubicom paid-in capital G. 200,000 | pass |
| chrono:event:0160 | Appeals tribunal adds laundering and criminal association | pass |
| chrono:event:0106 | A.I. 359: six detained, two under house arrest | pass |
| chrono:event:0096 | 27 charged on 4 November | pass |
| chrono:event:0070 | Solvency 13.85% / 12% / 5.56%; G. 1,621,853,458,972 | fail on amount: source prints only "G. 1,62 billones" |
| chrono:event:0036 | OTP USD 47 M for 9.99% of U Holdings | pass |
| chrono:role:0052 | U Paraguay holds 93.17% of the bank | pass |
| press:fact:0081 | Related exposure G. 743,784 M at 30 April (30%) | pass |

## 4. Record check: findings

### Tables (pp. 3-18)

- **Loans.** Operation number, date, term, rate, currency, principal, outstanding and status are correct in all
  35 table rows.
- **FRANEDE outstanding above principal.** Confirmed as printed for the three USD loans. In each case outstanding
  equals principal times 1.005 exactly (25,024,500 / 24,900,000; 10,645,965 / 10,593,000; 15,413,120 /
  15,336,437.83). It is a uniform 0.5% uplift, not a typo.
- **FRANEDE collateral.** The table's guarantee column prints "ASF" (signature only) for all six loans. The
  dataset's `mortgage_claimed` comes from the page 14 narrative. Both are true to the record; a note is added.
- **Roles.** Every percentage, start and end date in the MOWI, Hendy, Grupo M, TUIU, FRANEDE and AIME tables is
  correct.
- **Portfolio.** All nine amounts are correct and sum to 74,418,417 before cents, as the dataset already notes.

### Page 17 diagram

The scan is a halftone at about 12 px glyph height; 0, 6 and 8 are routinely indistinguishable. Última Hora
(5 and 7 November) prints the same legs from the BCP file, and with those values the diagram closes exactly.

| Row | Leg | Raw value | Corrected | Basis |
|---|---|---|---|---|
| rec:flow:0048 | Technoma to ITTI (bonds) | 4,230,000 | 4,230,383.21 | Label cents ",21"; ITTI box "recibe USD 10.000.244,21" |
| rec:flow:0049 | Technoma to Grupo Vázquez (bonds) | 5,770,000 | 5,769,861.00 | Closes the ITTI box total |
| rec:flow:0054 | Grupo Vázquez to ITTI | 5,770,000 | 5,769,861.00 | Same money passed on |
| rec:flow:0055 | ITTI to Grupo M | 6,321,524 | 6,321,574.00 | Scan "6.321.5x4,00" |
| rec:flow:0056 | ITTI to Vinanzas (loan) | 4,474,670 | 4,678,670.99 | Sum to funding total |
| rec:flow:0057 | Grupo Vázquez to Vinanzas (loan) | 4,215,767.91 | 4,215,707.91 | Sum to funding total (off by exactly 60) |
| rec:flow:0050 | La Tropa Fletes to Grupo Vázquez (bonds) | 4,215,767.91 | 4,215,707.91 | Same figure |
| rec:flow:0053 | La Tropa Fletes to Model (bonds) | 2,100,000 | 2,117,596.26 | Scan "2.1x7.59x,2x" |
| rec:flow:0059 | Model to Vinanzas (contract) | 2,100,000 | 2,117,596.26 | Sum to funding total |

Check: 20,000,000 + 35,000,000 + 4,678,670.99 + 4,215,707.91 + 10,049,628.97 + 2,117,596.26 = 76,061,604.13.

- **Funding received:** USD 76,061,604.13, confirmed.
- **Kasas leg:** USD 10,049,628.97, confirmed. The split between Factopar and La Tropa Fletes is not printed.
- **Five new loans:** 20 + 35 + 10 + 10 + 6.841 = USD 81,841,000, as printed in the Ueno box.
- **Column 3 heading** reads "BONOS DEL GRUPO (vía Ueno Casa de Bolsa S.A.)". The dataset omitted the intermediary.
- **Bottom payment line** (not in the dataset): "PAGO en efectivo USD 74.418.418,12 (USD 50.0xx.x80,77 + USD
  24.3xx.5xx,35) · 15/06/2026". The cents add to ,12. One consistent candidate is 50,023,880.77 + 24,394,537.35;
  this is a low-confidence reading with no second source.
- **Balance on 14 June 2026:** not settled by the scan. At 600% the disputed glyph is a 6/8 blur, and matching it
  against known 6s and 8s in the same box was inconclusive. El Parámetro (4 November) and Última Hora
  (10 November) both print 93,828. Since the scan reading lost to the press on three other figures of the same
  diagram, I recommend 93,828 at low confidence with 93,628 kept as the alternative reading. This is a judgement
  call: the owner's rule says the record wins on what the record says, but here the record's digit is not legible.

### Diagrams on pages 2 and 10

All person chips match entities already in the dataset, and their roles agree with the tables.

- **Page 2 chips:** Sergio Pizurno; Luis Ernesto Angulo; César Astigarraga; Federico Miguel Vázquez; Vanessa
  Godoy; Oscar Urdapilleta; "Familia Mengual" (two people: César J. Mengual M. and an "Augusto C. Mengual");
  Marcelo Giménez Recalde; Miguel Ángel Garay; Rudolph F. Goetz González.
- **Page 10 chips:** Luis Fernando Ríos; Miguel A. Almada Frutos; "C. Astigarraga · L. E. Angulo"; Rodrigo Franco;
  André Gayol Pires; Mauro Vargas Wildberger; Cecilia Domínguez; Martín Vargas Wildberger; Gloria Villasanti;
  Miguel Vázquez.
- **Chips with no entity in the dataset:** "Mónica Cadea" (surname uncertain; statutory auditor at TUIU and
  FRANEDE), "Sandra N. Caballero Almada / Laura Pane" (registry agents) and "Alan D. Campos Pardo" (AIME registry
  agent, said to be the same agent as for MOWI, Hendy and Grupo M). I did not add them; that would be new
  extraction. If added, they need low confidence.
- **Vázquez chip:** reads "Grupo M: BF 80% (presidente 2023-24)"; 80% is added to rec:role:0044 at low confidence.
- **Arrow notes** confirm the dataset: 19/09/2025 MOWI shares to Sala (90%) and Pizurno (10%); 30/09/2025 Hendy to
  Godoy (90%) and Urdapilleta (10%); 28/08/2025 ITTI sells its 50% of TUIU to L. F. Ríos; 30/06/2025 Grupo Vázquez
  sells 99.6% of FRANEDE to M. Vargas.

## 5. The ten corrections that matter most

1. **rec:flow:0056** ITTI to Vinanzas: 4,474,670 to 4,678,670.99 (USD 204,000 understated).
2. **rec:flow:0057 and 0050** Grupo Vázquez legs: 4,215,767.91 to 4,215,707.91.
3. **rec:flow:0053 and 0059** Model legs: 2,100,000 to 2,117,596.26.
4. **rec:flow:0048, 0049, 0054** Technoma bond split: 4,230,383.21 and 5,769,861.00 instead of rounded 4.23 M and
   5.77 M.
5. **rec:flow:0055** ITTI to Grupo M: 6,321,524 to 6,321,574.
6. **rec:event:0064** Vinanzas balance: confidence high to low; display value 93,628 to 93,828 (recommended, not
   proven).
7. **press:loan:0035** borrower org:redipro to org:grupo-hendy. Operation 612561002345 is Hendy's loan; Redipro
   only supplied the repayment money.
8. **press:loan:0010 and press:flow:0005** down-weighted: the USD 10,593,000 loan of 27 March 2026 is FRANEDE's
   in the record and in ABC, Henrici's only in Última Hora.
9. **press:flow:0006 and 0007** sender org:technoma to org:itti. These duplicate press:flow:0053 and 0054 and
   contradicted the record diagram.
10. **chrono:role:0002 and 0003** placeholder `auth:ministerio-publico` replaced by proposed court entities
    `auth:juzgado-penal-garantias-de-turno` (Otazú; La Nación: "juez de Garantías de turno") and
    `auth:juzgado-penal-garantias-crimen-organizado` (Legal; court number to confirm).

Also worth knowing: press:loan:0013's "USD 14.3 M" for Grupo M is the price at which that loan was sold to
Vinanzas (14,337,688), not its principal (13,567,500).

## 6. Consistency checks

- **Provenance.** Every row has a `prov` block, and every `prov.source` exists in a sources file.
- **Dates.** 1,051 values checked, none outside 1976 to 2026-11-20. Twelve `rec.flows` rows carry "2025/2026",
  which is not ISO; corrected to "2025" with year precision.
- **Thousand-fold errors.** None found. Every guaraní amount with a quote matches it; the few very small or very
  large values are genuine (Nubicom paid-in capital G. 200,000 confirmed at source; bank total assets).
- **Currency.** No mismatches. Ten rows quote a sentence that names the other currency of a two-currency pair;
  this is harmless but makes the quote weak evidence for that row.
- **Duplicate facts with different values.**
  - press:fact:0123 and 0124: 640,409 against 640,469 (the first fits the stated total).
  - U Paraguay's stake: 91%, 93.05% and 93.17%.
  - Sale date: 15 June against 16 June.
  - Vinanzas funding: 76,061,604.13 against a rounded 76.06 M.
  - Grupo M loans: 13,567,500 against 14.3 M, and 4,321,500 against 4 M (rounding).
- **Same party under two ids** (see `edit.entity_merges.jsonl`):
  - auth:diputados to auth:camara-de-diputados
  - person:luis-pinanez to person:luis-lionel-pinanez
  - org:credicentro to org:ueno-holding
  - org:muv to org:click-sa-muv
  - org:wepa to org:redisa (medium)
  - org:bankitti to org:itti (medium)
- **Look-alikes that must not be merged:** org:gsr and org:dobrestec; org:la-tropa-fletes and org:la-tropa-sae;
  org:nubicom and org:nubicom-srl.
- **Ids used without an entity row:** auth:fgd, auth:superintendencia-de-valores, org:cadiem,
  person:carlos-carvallo, person:holger-insfran.
- **Same fact under two orgs.** Carvallo's pre-2023 presidency sits under org:financiera-el-comercio in chrono and
  org:ueno-bank in the dossier.
- **Accents.** Eighteen press person labels lack accents. Eleven are fixed from the record's spelling; seven are
  flagged only, because no second source in the dataset prints the name. "FRANDEDE" in two `chrono.accused` rows
  is an outlet typo.
- **Id spelling.** `org:pear-srl` is the SPEC id but the record prints "PEARL S.R.L."; the label is right, the
  slug is not.

## 7. Privacy and fairness

- **Personal details.** None of the excluded categories appears. The record's page 19 identity paragraph was
  correctly left out.
- **Private individuals.** press:role:0024 to 0026 name three small private holders of U Holdings who have no
  stated relevance to the case; I recommend hiding them.
- **Family.** Kinship rows (rec:role:0096, 0097, 0102, 0106) are record-stated grounds for related-party status
  and are allowed. chrono:event:0015 and 0023 mention an unnamed brother of the then president, as the outlet
  does; acceptable.
- **Allegation stated as fact.** The press and chrono layers attribute carefully. The record layer does not:
  `rec.flows` purposes and several `rec.events` titles use the indicative ("forwarded", "repaid with") where the
  record uses the conditional. Three titles are reworded. For the 40 text-derived flows, the display should prefix
  "the prosecution alleges" from `asserted_by` rather than rely on the purpose text.
- **Missing responses.** Gustale's denial of indirect financing (chrono:event:0063, 21 October) is now referenced
  from four Vinanzas rows. Rey's hearsay account of a cash delivery by Miguel Vázquez (rec:flow:0071 and 0072) has
  no reported response anywhere in the data; that absence is now stated on the row.

## 8. Unresolved conflicts

| Conflict | Values | What would settle it |
|---|---|---|
| Vinanzas balance, 14 June 2026 | 93,628 (scan reading) / 93,828 (two outlets) | A clean copy of page 17, or the Superintendency report behind the diagram |
| Date of Rey's statement | 4 November (header) / 17 or 18 November (press; PDF scanned 18 November) | The prosecution case file entry or the filing stamp |
| Date of the Vinanzas sale | 15 June (record, most press) / 16 June (charges against Peña, per ABC) | The assignment contract and the bank's accounting entry |
| Borrower of USD 10,593,000 on 27 March 2026 | FRANEDE (record, ABC) / Henrici (Última Hora) | Loan file for op. 612661003607 |
| Issuer of the USD 5.77 M bonds | Grupo Vázquez paper (diagram label) / ueno bank paper sold by Grupo Vázquez (Última Hora) | Ueno Casa de Bolsa trade tickets |
| ITTI to Grupo M: overdraft cancelled | "6.29x.732,30" (scan) / 6,321,573.22 (Última Hora) / 6,305,659.87 (p7 table) | Grupo M account statement, 15 June 2026 |
| Bottom payment line, page 17 | 50.0xx.x80,77 + 24.3xx.5xx,35 | Clean copy of page 17 |
| MOWI overdraft, January 2026 | 105,090 M (record) / 114,000 M accumulated (Última Hora) | MOWI account statement |
| MOWI and Hendy overdraft status | Outstanding (record tables) / cancelled 15 June (Última Hora) | Cut-off date of the record tables |
| U Paraguay's stake in the bank | 91% / 93.05% / 93.17% | Shareholder register filed with the BCP |
| Rey's title and tenure | Director, left July 2026 (record) / former second vice-president (press) / 2023-2025 (dossier) | Minutes of the extraordinary meeting |
| Astigarraga's company | President of Grupo M (record) / of ITTI (La Nación) | Company registry minutes |
| Brand mapping | Wepa is Redisa and UPay is Redipro (Rey, Solventa) / reversed (ABC) | Trademark or company filings |
| FRANEDE capital | Gs. 2,628,000,000,000 as printed (rec:issue:0006) | FRANEDE 2024 balance sheet |

## 9. Rows to hide or down-weight

- **Hide from the money-flow graph:** rec:flow:0075 (USD 900 M aggregate with a stand-in recipient) and
  rec:flow:0076 (property sale with assumed direction).
- **Render as an annotation, not an office:** rec:role:0115 to 0120 (the "12 home-banking operators").
- **Hide by default:** press:role:0024 to 0026 (private small holders).
- **Down-weight:** press:loan:0010, press:flow:0005, press:fact:0095 (probable wrong entity), dos:role:0007,
  dos:role:0011.
- **De-duplicate:** press:flow:0006 and 0007 against 0053 and 0054; rec:role:0096 against 0097; rec:events 1-39
  against rec:loans (the same 39 facts twice in one contributor).
- **Low by construction:** all `dos.*` rows (no links, dates or page references).

## 10. How far the dataset can be relied on

| Tier | Reliability | Comment |
|---|---|---|
| Record tables and running text (prosecution voice) | High as a transcription | 100% of checked cells correct. What it proves is what the prosecution alleges, in the conditional mood. |
| Record, Rey's statement | High as a transcription | Content is one suspect's account, partly hearsay (the cash figures come from a third person). |
| Record diagrams | Medium after corrections | Before this pass 9 of the 17 diagram flow amounts were wrong. The corrected set closes arithmetically. Loan numbers, chip percentages and the 14 June balance remain low. |
| Press quoting the BCP or prosecution file | Medium-high for figures | 88% pass on the core sample. Outlets disagree with each other on attribution in a few places; use for amounts, be careful with who-paid-whom. |
| Press, other (politics, measures, rulings) | Medium-high | All sampled rulings and dates confirmed. Role titles vary by outlet. |
| Rating-agency figures | Not sampled | Internally consistent by script only. |
| Third-party dossier | Low | Untraceable. Use only as a pointer. |

Systematic problems, in order of importance: small print on the page 17 diagram read with too much confidence;
record-layer wording in the indicative; entity ids minted independently by contributors; missing accents in the
press entity file.
