# Ueno Bank S.A. (Case 89/2026): flow-of-funds analysis

**Status of this document.** Analysis by an AI forensic-accounting and flow-of-funds analyst, not a licensed professional. It reorganises figures alleged in the prosecution record and reported by press. It is not an audit and does not find that any offence occurred. Everyone named is presumed innocent. Statements by Julio Rey are his own claims. Arithmetic and opinions are mine and are labelled.

**Sources.** `rec.*` is the 24-page prosecution record (prosecution voice pp. 1-19, Rey pp. 19-24), treated as authoritative for what is alleged. `press.*` is press and rating data, mostly relaying the supervisor. `dos.*` (a third-party dossier) holds no flow rows and was used only to note a conflict. Row ids are given in brackets without the `flow:` word where obvious, for example `rec:flow:0041`.

## 0. Coverage

| | Rows | With amount | Null amount |
|---|---|---|---|
| Record flows | 78 | 32 | 46 |
| Press flows | 146 | 81 | 65 |
| All | 224 | 113 | 111 |

- All 40 record rows on forwarding and repayment for the six borrowers (`rec:flow:0001`-`0040`) have no amount. The record's amounts are the June 2026 diagram (many read from small print, confidence low), the nine portfolio items and Rey's figures.
- 128 of 224 rows have a day-precision date.
- Press repeats legs across articles. After merging repeats I work with **69 unique money legs**. Excluded from totals: the ten non-cash portfolio-assignment rows, Rey's USD 900 million aggregate (`rec:flow:0075`), the property row of uncertain direction (`rec:flow:0076`), and three alternate attributions (`press:flow:0005`, `0006`, `0007`).

## 1. Chains

### 1a. Vinanzas circuit, 11-15 June 2026 (23 legs, loop closes in 0 to 4 days)

| # | Date | From → To | USD | Instrument | Rows |
|---|---|---|---|---|---|
| 1 | 11 Jun | Ueno → Technoma | 10,000,000 | loan | rec:flow:0043 |
| 2 | 11 Jun | Ueno → La Tropa Fletes | 10,000,000 | loan | rec:flow:0044 |
| 3 | 11 Jun | Technoma → ITTI | 4,230,383.21 | bonds | press:flow:0049, rec:flow:0048 |
| 4 | 11 Jun | Technoma → Grupo Vázquez | 5,769,861 | bonds | press:flow:0050, rec:flow:0049 |
| 5 | 11 Jun | Grupo Vázquez → ITTI | 5,769,861 | transfer | press:flow:0051, rec:flow:0054 |
| 6 | 11 or 15 Jun | ITTI → Grupo M (overdraft cancelled) | 6,321,574 | repayment | press:flow:0052, 0037; rec:flow:0055 |
| 7-9 | 15 Jun | Ueno → Satec / HD Invest / Factopar | 20,000,000 / 35,000,000 / 6,841,000 | loans | rec:flow:0041, 0042, 0045 |
| 10 | 15 Jun | La Tropa Fletes → Ueno Casa de Bolsa | 10,000,000 | transfer | press:flow:0068 |
| 11-14 | 15 Jun | Casa de Bolsa → Grupo Vázquez / Model / Kasas / ITTI | 4,215,767.91 / 2,117,596.26 / n.a. / n.a. | bonds | press:flow:0069-0072; rec:flow:0050, 0051, 0053 |
| 15 | 15 Jun | Factopar → Kasas | n.a. | bonds | rec:flow:0052, press:flow:0008 |
| 16-21 | 15 Jun | Satec, HD Invest, Kasas, ITTI, Grupo Vázquez, Model → Vinanzas | see table below | | |
| 22 | 15 Jun | Ueno → Vinanzas (nine loans, non-cash) | 74,418,418.12 | assignment | rec:flow:0060, 0062-0070 |
| 23 | 15 Jun | Vinanzas → Ueno | 74,418,418.12 | cash price | rec:flow:0061, press:flow:0064 |

**Vinanzas, 15 June 2026, sources and uses (USD)**

| Source | Record diagram | Press | Difference |
|---|---|---|---|
| Opening balance 14 Jun (`rec:event:0064`, `press:fact:0036`) | 93,628 | 93,828 | 200 |
| Satec (`rec:flow:0046`) | 20,000,000.00 | 20,000,000.00 | 0 |
| HD Invest (`rec:flow:0047`) | 35,000,000.00 | 35,000,000.00 | 0 |
| Kasas, contract (`rec:flow:0058`, `press:flow:0061`) | 10,049,628.97 | 10,049,628.97 | 0 |
| ITTI, loan (`rec:flow:0056`, `press:flow:0053`) | 4,474,670.00 | 4,678,670.99 | 204,000.99 |
| Grupo Vázquez, loan (`rec:flow:0057`, `press:flow:0062`) | 4,215,767.91 | 4,215,707.91* | -60.00 |
| Model, contract (`rec:flow:0059`, `press:flow:0063`) | 2,100,000.00 | 2,117,596.26 | 17,596.26 |
| **Sum of legs** | **75,840,066.88** | **76,061,604.13** | **221,537.25** |
| Stated total received (`press:fact:0045`) | 76,061,604.13 | 76,061,604.13 | |
| Use: price to Ueno (`rec:flow:0061`) | 74,418,418.12 | 74,418,418.12 | |
| **Residual of the day's receipts** | | **1,643,186.01** | |

\* Press prints 4,215,707 without cents; 4,215,707.91 is the value that makes the total exact.

What adds up:
- The press components equal the USD 76,061,604.13 total to the cent. The record diagram is USD 221,537.25 short, and that gap is fully explained by three small-print readings (ITTI, Model, Grupo Vázquez). I read this as transcription noise in the diagram, not a real difference.
- The nine portfolio items sum to 74,418,417 against a price of 74,418,418.12 (`rec:issue:0004`), a rounding matter.
- The price equals principal plus accrued interest. Principal of the nine loans is USD 71,712,884.46; price is 103.77% of that. Recomputing principal plus interest at the contract rate on a 365-day basis lands within 0.1% for seven items. No discount was applied.

What does not add up:
- **USD 1,643,186.01** received by Vinanzas that day has no reported use.
- Technoma's two bond purchases total USD 10,000,244.21, which is USD 244.21 more than its loan.
- ITTI received USD 10,000,244.21 from that operation and paid out 6,321,574 + 4,678,670.99 = 11,000,244.99. The **USD 1,000,000.78** difference has no identified source. Bond sales by ITTI to La Tropa Fletes or Factopar cannot cover it: the press figures cap those at USD 381,966.85.
- Total USD uses (76,061,604.13 + 6,321,574) exceed the five loans (81,841,000) by **USD 542,178.13**.
- The split of La Tropa Fletes' USD 9,923,899.99 and Factopar's USD 6,841,000 between Kasas, Grupo Vázquez, Model and ITTI is not given. Kasas received at least USD 3,208,628.97 from La Tropa Fletes.
- Date of the Grupo M overdraft cancellation: 11 June (`press:flow:0037`) or 15 June (record diagram).
- One article says Technoma, not ITTI, sent the USD 4,678,670.99 and G. 31,200 million (`press:flow:0006`, `0007`).

**Guaraní legs, 15 June 2026 (press only, 16 legs, same day)**

| Leg | G. million | Rows |
|---|---|---|
| Ueno → Sagas / HD Invest / Factopar (two loans) | 86,100 / 36,900 / 93,000 + 64,500 | press:loan:0002, 0004, 0007, 0008 |
| Sagas, HD Invest → Vinanzas | 86,100 / 36,900 | press:flow:0001, 0003 |
| Factopar → Vinanzas (derived: 218,700 less the two above) | 95,700 | press:fact:0038 |
| ITTI → Vinanzas (loan) | 31,200 | press:flow:0054 |
| Vinanzas → Redisa / Redipro | 110,940 / 18,770 | press:flow:0040, 0041 |
| Redisa → Hendy / Mowi | 110,940 / 98,202 | press:flow:0055, 0057 |
| Redipro → Hendy / Mowi | 7,304 / 11,466 | press:flow:0056, 0058 |
| Hendy, Mowi overdrafts cancelled at Ueno | 118,244 / 109,668 | press:loan:0029, 0030 |

Redipro balances exactly (18,770 in and out) and both overdraft totals tie to the payments. Gaps: Vinanzas took in G. 249,900 million and G. 120,190 million of it is not located; Redisa paid G. 98,202 million more than it is reported to have received; G. 61,800 million of Factopar's guaraní loans is not located. New guaraní lending that day was G. 280,500 million against G. 227,912 million of overdrafts cancelled.

### 1b. The six record borrowers

| Borrower | Record principal | First hop (named) | Amount-traced first hop | Repayment source alleged | Legs |
|---|---|---|---|---|---|
| Mowi | USD 23.27 M; G. 239,090 M | ITTI, Redisa, Redipro (`rec:flow:0001`-`0003`) | USD 5.4 M → Redisa 30 Oct 2025; G. 33,500 M → Redipro 30 Dec 2025 (`press:flow:0121`, `0123`) | ITTI, Redisa, Vinanzas; La Tropa SAE via Grupo Vázquez and ITTI (`press:flow:0024`, `0067`) | 14 |
| Grupo Hendy | USD 25.23 M; G. 190,922 M | ITTI, Redisa, Redipro (`rec:flow:0004`-`0007`) | USD 5.1 M and 5,527,500 → ITTI (`press:flow:0122`, `0104`) | Redipro with ITTI money; Vinanzas, Redisa, ITTI via SIPAP (`rec:flow:0008`-`0013`) | 16 |
| Grupo M | USD 29.52 M; G. 55,970 M | ITTI, Redisa, Kaitel, Redipro (`rec:flow:0014`-`0019`) | USD 5.3 M → ITTI 30 Dec 2025 (`press:flow:0125`) | ITTI (`rec:flow:0020`, `press:flow:0052`) | 12 |
| TUIU | USD 30.65 M; G. 144,600 M | ITTI, Redisa, Redipro (`rec:flow:0021`-`0023`) | none | Redipro with Vinanzas money fed by 72-hour cheques (`rec:flow:0024`-`0028`) | 11 |
| Franede | USD 60.83 M; G. 160,000 M | Vinanzas, Grupo Vázquez (`rec:flow:0029`, `0030`) | G. 65,000 M and USD 10,593,000 → Vinanzas same day (`press:flow:0018`, `0074`) | Vinanzas, Grupo Vázquez (`rec:flow:0031`, `0032`) | 12 |
| AIME | USD 25.05 M; G. 250,952 M | ITTI, Grupo Vázquez, Redisa, Redipro (`rec:flow:0033`-`0040`) | none | ITTI, Grupo Vázquez, Redisa (`rec:flow:0034`, `0036`, `0038`) | 12 |

Across the six, record principal is USD 194,545,732 and G. 1,041,534 million. Forwarding amounts exist for USD 31,920,500 (16.4%) and G. 98,500 million (9.5%), all from press. Neither source shows a repayment from a borrower's own revenue. The use side is stated only in general terms (overdrafts, invoices, cheques of related companies).

Arithmetic observations on the record's loan table (mine, to be tested):
- Twelve loans equal a round amount plus exactly 0.5% (for example 10,050,000; 13,567,500; G. 133,665 M). Three Franede balances exceed principal by exactly 0.5% (`rec:loan:0025`, `0027`, `0028`), which would explain `rec:issue:0007`.
- Mowi's USD 5,366,645.18 loan of 24 Apr 2026 equals its cancelled G. 33,500 M loan at 6,242.26 per USD. Hendy's USD 14,627,989.28 loan of 27 Apr equals its cancelled G. 91,334.4 M loan at 6,243.81. Franede's USD 10,593,000 loan of 27 Mar equals its cancelled USD 10 M loan plus 5.93% (270 days at 8% is 5.92%).

### 1c. Second ring (press only)

| Chain | Legs | Sequence | Gaps |
|---|---|---|---|
| Nubicom / Galadriel / Infocenter | 12 | Ueno → Nubicom G. 417,075 M (1 Jul 2026) → ITTI G. 415,000 M (contract dated 30 Jun) → Redisa G. 329,500 M; Ueno → Galadriel USD 15.07 M and Infocenter USD 18 M (31 Jul) → ITTI → Nubicom G. 285,600 M → Ueno (`press:flow:0091`-`0095`, `0119`, `0120`) | G. 285,600 M over USD 33 M implies 8,654 per USD against about 6,100 to 6,240 elsewhere; about G. 84,000 M unexplained. Infocenter leg is low confidence. |
| Sagas / Kasas, 29 Apr 2026 | 6 | Sagas credit → Kasas → Vinanzas → ITTI → Grupo M → Ueno, same day (`press:flow:0084`-`0087`, `rec:flow:0020`) | No amounts except the instalment (about USD 4.32 M). |
| Grupo Berilo | 6 | USD 30.15 M (23 Dec 2025) → Vinanzas 30 M same day → Redisa 30 M on 30 Dec; USD 26.4 M (1 Jun 2026) → Vinanzas 26.3 M → Grupo Vázquez (`press:flow:0097`, `0098`, `0031`, `0032`) | Return to Ueno not shown. Total loans given as USD 69 M elsewhere. |
| Office Design / Nuevo Mundo / Match | 11 | 26 May 2026: Nuevo Mundo → Vinanzas → ITTI → Office Design overdraft; Office Design USD 15.6 M → G. 96,767 M → ITTI → Match G. 74,071 M (`press:flow:0099`-`0103`) | One amount only. Nuevo Mundo loan figures overlap between articles. |
| GSR | 7 | USD 7 M and 8.5 M (late 2025) → Vinanzas by fixed-income contract → ITTI; G. 132,660 M (1 Jun 2026) → Vinanzas and ITTI (`press:flow:0022`, `0023`, `0033`, `0034`) | USD 15.5 M of about USD 72.8 M traced. |
| Henrici | 2 | USD 10,593,000 (27 Mar 2026) → ITTI (`press:flow:0005`) | Same loan is Franede's in the record (`rec:loan:0027`). |
| La Tropa SAE, 23-24 Apr 2026 | 5 | USD 5,936,654.88 → Grupo Vázquez same day → ITTI next day → Mowi → part-cancels G. 33,500 M loan (`press:flow:0065`-`0067`, `0088`) | Lender not named in the sentence; year assumed. |

### 1d. Cash and certificates of deposit (Rey's claim, 4 legs)

Rey says a liquidity officer told him that about USD 17 million and G. 17,000 million in cash were brought to the bank at night, took a day for Treasury to count, were booked in a Grupo Vázquez company as collections of unpaid loans, and were justified with receipts of three "dead portfolio" firms bearing consecutive numbers; that the money bought certificates of deposit in 2025; and that in 2026 the certificates were to capitalise the bank (`rec:flow:0071`-`0073`, `rec:event:0047`). The defence filed certificate schedules and three receipts (`rec:event:0068`). The date he gives conflicts with its context (`rec:issue:0009`). No press row corroborates amounts.

Documents that would test it: the certificate-of-deposit register (issue date, holder, amount, funding entry, endorsements); the cash-count sheets, vault log and CCTV for the night; the receipt book of the collecting company; the written-off loan ledger for the three firms and confirmation from those firms; the cash transaction report filed with the financial intelligence unit; and capital account entries and shareholder minutes for 2026.

## 2. Network metrics

Totals are from the 69 unique legs. They show what the data can count, not the true volumes.

| Entity | In USD | Out USD | In G. M | Out G. M | Counterparties | Rows with / without amount | Role |
|---|---|---|---|---|---|---|---|
| Vinanzas | 158,454,601 | 115,011,418 | 219,200 | 187,210 | 17 | 53 / 19 | collector and redistributor |
| ITTI | 69,520,744 | 15,320,244 | 511,767 | 720,371 | 21 | 26 / 42 | main destination and repayment payer |
| Ueno Bank | 91,418,418 | 81,841,000 | 17,000 | 4,767 | 10 | 31 / 3 | origin and end point |
| Grupo Vázquez | 15,922,284 | 10,719,568 | 4,767 | 1,687 | 13 | 20 / 12 | pass-through, bond seller |
| Redisa | 35,400,000 | 0 | 440,440 | 209,142 | 8 | 6 / 18 | receiver, overdraft payer |
| Redipro | 0 | 0 | 52,270 | 18,770 | 7 | 4 / 18 | receiver, repayment conduit |
| Kasas | 10,049,629 | 10,049,628 | 0 | 0 | 5 | 4 / 5 | same-day pass-through |
| Model | 2,117,596 | 2,117,596 | 0 | 0 | 3 | 5 / 1 | same-day pass-through |
| Satec / HD Invest | 20 M / 35 M | 20 M / 35 M | 0 | 0 / 36,900 | 2 / 2 | 6 / 0 each | pure pass-through |

ITTI's USD inflow includes USD 33 million from Galadriel and Infocenter that is low confidence. Ueno's figures include Rey's claimed cash (USD 17 M, G. 17,000 M) and exclude all disbursements that exist only as loan rows.

**Pass-through timing** (in and out within 0 to 4 days, day-dated rows): ITTI on seven dates (27 Mar, 24 Apr, 29 Apr, 26 May, 11 Jun, 15 Jun, 31 Jul 2026); Vinanzas on six (30 Sep 2025; 27 Mar, 29 Apr, 26 May, 1 Jun, 15 Jun 2026); Grupo Vázquez on three; Kasas on two.

**Cycles starting and ending at Ueno Bank.** Ignoring dates, the graph has 87 simple cycles of up to seven nodes through the bank; most are not possible in time order. Loops that are consistent with the dates:

| Loop | Elapsed | Closing leg |
|---|---|---|
| Ueno → Satec → Vinanzas → Ueno; same via HD Invest | 0 days | rec:flow:0061 |
| Ueno → Factopar → Kasas → Vinanzas → Ueno | 0 days | rec:flow:0061 |
| Ueno → Technoma → (Grupo Vázquez →) ITTI → Vinanzas → Ueno | 4 days | rec:flow:0061 |
| Ueno → La Tropa Fletes → Casa de Bolsa → Grupo Vázquez / Kasas / Model → Vinanzas → Ueno | 4 days | rec:flow:0061 |
| Ueno → Technoma → ITTI → Grupo M → Ueno (overdraft) | 0 or 4 days | press:loan:0034 |
| Ueno → Sagas / HD Invest → Vinanzas → Redisa / Redipro → Hendy / Mowi → Ueno (G.) | 0 days | press:loan:0029, 0030 |
| Ueno → Franede → Vinanzas → Ueno (30 Sep 2025) | 0 days | press:flow:0019 |
| Ueno → Sagas → Kasas → Vinanzas → ITTI → Grupo M → Ueno (29 Apr 2026) | 0 days | rec:loan:0013 |
| Ueno → La Tropa SAE → Grupo Vázquez → ITTI → Mowi → Ueno | 1 day | rec:loan:0003 |
| Ueno → Nuevo Mundo → Vinanzas → ITTI → Office Design → Ueno (overdraft) | 0 days | press:flow:0101 |
| Ueno → Galadriel / Infocenter → ITTI → Nubicom → Ueno | 0 days (30 from the Nubicom loan) | press:flow:0093 |
| TUIU overdraft of 2 Jan 2026 repaid via cheques → Vinanzas → Redipro → TUIU | 28 days | rec:flow:0024 |

**Share reaching ITTI, Redisa, Redipro, Vinanzas and Grupo Vázquez.** Of first-hop forwardings by borrowers that carry an amount, USD 211,873,167 of USD 229,840,392 (92.2%) and G. 733,267 million of G. 733,267 million (100%) went to those five. A further USD 12,167,225 went to Kasas and Model and reached Vinanzas the same day, lifting the USD share to 97.5%. The rest (USD 5.8 M) went to Nubicom SRL and Nokia. By row count, 94 of 110 forwarding rows, and 38 of 47 distinct sender-receiver pairs, point to the five. This describes the traced subset only: for the six record borrowers it is 16.4% of USD principal and 9.5% of guaraní principal.

## 3. Typology read

| Pattern | Indicators present | Not shown |
|---|---|---|
| Round-tripping | Five loans and the price paid linked in 0 to 4 days; buyer balance about USD 93,628 the day before; components sum to the cent; same-day guaraní loop (`rec:flow:0041`-`0047`, `0061`; `rec:event:0064`) | Time-stamped statements; who instructed the borrowers' transfers; use of USD 1,643,186.01; repayment capacity of the new borrowers |
| Loan-back / related-party funding via intermediaries | Record says all six borrowers forwarded at once (`rec:flow:0001`-`0040`); 92 to 100% of amount-traced first hops reach the five; exposure above cap (`press:fact:0081`-`0085`) | Amounts in the record; contracts or invoices that might justify payments as ordinary trade; approval minutes |
| Evergreening | Overdrafts paid down 30 Jan and redrawn 2-3 Feb 2026 (`rec:loan:0005`, `0006`, `0021`, `0022`); April and March amount equivalences; instalments paid by group firms (`rec:flow:0009`, `0020`, `0024`); 31 of 40 record operations dated within the last six or first four days of a month; portfolio sold at par plus interest | Cancellation dates and entries; the bank's exchange rates; classification and provisioning history |
| Nominee borrowers | Share transfers 0 to 7 days around first loans (`rec:event:0050`, `0052`, `0053`, `0054`, `0060`); 12 shared home-banking operators (`rec:role:0115`-`0120`); new owners with bank or group roles; very low paid-in capital at GSR and Nubicom (`press:fact:0047`, `0097`) | Share purchase contracts and payment; any account by the new owners; ownership of Satec, HD Invest, Factopar and Sagas |
| Kiting through 72-hour cheques | Cheques of Redisa, Redipro and ITTI funded Vinanzas in Jan 2026 (`rec:flow:0026`-`0028`); Franede repayments traced to such cheques; AIME money ended in cheques at Zeta Banco (`press:flow:0029`); ITTI → Redisa G. 329,500 M to cover them (`press:flow:0092`) | Cheque numbers, banks, amounts, dates; drawings against uncollected funds, which is what defines kiting; returned cheques |
| Circular capital via certificates of deposit | Rey's account only (`rec:flow:0071`-`0073`); a central bank minute on an undeducted contribution (`press:event:0026`) with no stated link | Any corroboration; certificate details; origin of the cash; whether capital was ever booked |

None of these readings establishes an offence. Each pattern also has lawful look-alikes (group treasury management, refinancing at arm's length, genuine asset sales) that the missing documents would distinguish.

## 4. Red-flag timing

| Date | Event | Rows |
|---|---|---|
| 30 Jun 2025 | Franede shares to an individual (99.62%) and two loans the same day | rec:event:0050; rec:loan:0023, 0024 |
| 28-29 Aug 2025 | ITTI sells 50% of TUIU; first loan next day | rec:event:0052; rec:loan:0017 |
| 19-26 Sep 2025 | Mowi shares (press: 9 Sep), officers 25 Sep, account and first loan 26 Sep | rec:event:0053; press:event:0003, 0045 |
| 26-30 Sep 2025 | Hendy and Grupo M borrow while owned by ITTI and Grupo Vázquez; shares pass four days later | rec:event:0054; rec:loan:0007, 0012 |
| 30 Sep 2025 | Franede G. 65,000 M → Vinanzas → Ueno portfolio purchase, same day | press:flow:0018, 0019 |
| 27-31 Oct 2025 | De-listing request without documents; four loans follow | rec:event:0055; press:event:0004 |
| 31 Oct 2025 | ITTI-Vinanzas framework loan contract signed | press:event:0015 |
| 29 Dec 2025 | Four borrowers funded the same day; three forwarded next day | rec:loan:0003, 0009, 0014, 0019 |
| 2 Jan 2026 | Five overdrafts opened the same day | rec:loan:0005, 0015, 0016, 0020, 0021 |
| 27-30 Jan 2026 | AIME share change, then loans on the day Mowi and TUIU overdrafts are paid down (coincidence noted by me) | rec:event:0060; rec:loan:0030, 0031; press:flow:0024 |
| 2-3 Feb 2026 | Overdrafts redrawn | rec:loan:0006, 0010, 0022 |
| 27 Mar 2026 | Franede USD 10,593,000 in and out the same day | press:flow:0074, 0075 |
| 24-27 Apr 2026 | Mowi loan part-cancelled and new loan the same day; Hendy loan three days later | press:flow:0067; rec:loan:0004, 0011 |
| 29 Apr 2026 | Sagas credit and five-entity chain, same day | press:flow:0084-0087 |
| 5-15 Jun 2026 | Supervisor confirms related status; ten days later the loans are sold | press:event:0005, 0006; rec:event:0065 |
| 15 Jun 2026 | Contract, funding and cash payment on one day | rec:flow:0060, 0061 |
| 30 Jun-1 Jul 2026 | Nubicom contract, loan and payment within two days | press:flow:0091; press:loan:0045 |
| 30-31 Jul 2026 | Galadriel share transfers and loan | press:event:0034; press:role:0083, 0084 |

**Shared operators.** The same 12 home-banking users, described as ITTI employees, on all six borrowers (`rec:role:0115`-`0120`, `press:event:0016`).

**Officers in common** (stated roles only): Urdapilleta, owner in Hendy and Grupo M, director of Redisa and of Ueno Casa de Bolsa, ITTI employee (`rec:role:0052`-`0057`, `0074`); Pizurno in Mowi, Grupo M and Technoma (`rec:role:0036`, `0038`, `press:role:0103`); Ríos in TUIU, Technoma and AIME (`rec:role:0078`, `0080`, `0082`); Almada, statutory auditor of the bank, TUIU and AIME (`rec:role:0015`, `0090`, `0091`); Astigarraga in Mowi, Grupo M, TUIU, Nubicom and formerly the bank (`rec:role:0042`, `0068`, `0069`, `0092`, `press:role:0034`); Sala Cardozo, former bank manager, in Mowi and GSR (`rec:role:0033`, `0035`, `press:role:0007`); Vera Moreira in Office Design and Technoma (`press:role:0004`, `0005`).

**Shared addresses.** The data hold no address or registered-office fields, so this cannot be tested here.

## 5. Conflicts to resolve

| # | Conflict | Rows | Document that settles it |
|---|---|---|---|
| 1 | ITTI → Vinanzas: 4,474,670 (record) or 4,678,670.99 (press); sender ITTI or Technoma | rec:flow:0056; press:flow:0053, 0006 | Vinanzas USD savings statement; framework contract drawdown notice |
| 2 | Grupo Vázquez leg 4,215,767.91 or 4,215,707.91; Model 2,100,000 or 2,117,596.26 | rec:flow:0057, 0059; press:flow:0062, 0063 | Original diagram; broker trade tickets |
| 3 | Vinanzas opening balance 93,628 or 93,828 | rec:event:0064; press:fact:0036 | Statements of its eight accounts |
| 4 | Source of USD 1,000,000.78 at ITTI and USD 542,178.13 overall; use of USD 1,643,186.01 | chain 1a | ITTI and Vinanzas statements; SIPAP log |
| 5 | Bonds bought by Technoma: Grupo Vázquez paper or "ueno" paper; primary or secondary | press:flow:0050 | Trade tickets; depository records |
| 6 | Grupo M overdraft cancelled 11 or 15 June | press:flow:0037; rec:flow:0055 | Grupo M overdraft ledger |
| 7 | Redisa G. 98,202 M; Factopar G. 61,800 M; Vinanzas G. 120,190 M | press:flow:0040, 0057; press:loan:0007, 0008 | Guaraní statements; SIPAP log |
| 8 | USD 10,593,000 of 27 Mar 2026: Franede or Henrici | rec:loan:0027; press:loan:0010, 0038 | Loan file 612661003607 |
| 9 | Mowi share transfer 19 or 9 Sep 2025 | rec:event:0053; press:event:0045 | Share register; transfer contracts |
| 10 | TUIU overdraft payer: Redipro (record) or Vinanzas (press) | rec:flow:0024; press:flow:0025 | TUIU account 614194019 statement |
| 11 | Grupo M loans: 13,567,500 and 4,321,500 or USD 14.3 M and 4 M | rec:loan:0012, 0013; press:loan:0013, 0040 | Loan ledger |
| 12 | Nubicom repayment and the USD 33 M exchange operation | press:flow:0093-0095 | FX deal tickets; ITTI statement |
| 13 | Rey's cash date; record dated 4 Nov, press dates the statement 17-18 Nov | rec:issue:0009, 0011 | Signed record; vault and treasury logs |
| 14 | Portfolio called impaired by press but listed as category 1a in the record | rec:flow:0062; press:flow:0038 | Classification reports; board minutes approving the sale |
| 15 | Dossier range of USD 41 to 74.4 M for the portfolio | dos:issue:0004 | Sale contract (record figure stands) |

## Opinions

1. **Opinion.** The June USD figures reconcile to the cent on the press numbers, so both sources probably derive from one supervisory work paper; three record-diagram legs should be re-read before being quoted. Basis: `rec:flow:0056`, `0057`, `0059`; `press:flow:0053`, `0062`, `0063`; `press:fact:0045`.
2. **Opinion.** The five June loans do not fully explain the day. At least USD 542,178.13 of uses and USD 1,000,000.78 of ITTI's payments came from unidentified sources, and USD 1,643,186.01 stayed in Vinanzas. These are gaps to close, not signs by themselves. Basis: `rec:flow:0041`-`0045`, `0061`; `press:flow:0049`-`0053`.
3. **Opinion.** Pricing the portfolio at principal plus accrued interest would have let the bank show full recovery of USD 71.7 million of principal and about USD 2.7 million of interest while its exposure moved to new borrowers for USD 81.8 million plus G. 280,500 million. Purpose is for the court. Basis: `rec:flow:0060`, `0062`-`0070`; `press:loan:0002`, `0007`, `0008`.
4. **Opinion.** The strongest pattern is repetition: ITTI on seven dates and Vinanzas on six received and paid out within 0 to 4 days, and every repayment with a named source was paid by a group company or passed through one. Basis: `press:flow:0075`, `0086`, `0100`, `0051`, `0093`; `rec:flow:0009`, `0020`, `0024`, `0031`, `0034`.
5. **Opinion.** The March and April 2026 amount coincidences look like roll-overs or currency conversions of earlier loans. This rests on my arithmetic alone. Basis: `rec:loan:0003`, `0004`, `0007`, `0011`, `0023`, `0027`.
6. **Opinion.** A financed 0.5% charge would explain twelve loan amounts and the three Franede balances above principal. I cannot say what the charge is. Basis: `rec:loan:0008`, `0012`, `0017`, `0025`, `0027`, `0028`; `rec:issue:0007`.
7. **Opinion.** The second-ring chains are press-only leads and several figures do not close. They are weaker than the record. Basis: `press:flow:0093`-`0095`, `0057`, `0040`, `0005`, `0074`.
8. **Opinion.** Rey's cash and certificate account is single-source and second-hand, from a charged person seeking a cooperation agreement. It is specific enough to test quickly and should be treated as untested until then. Basis: `rec:flow:0071`-`0073`; `rec:issue:0009`; `rec:event:0068`; `chrono:event:0223`.

## Tests I would run next

1. Rebuild the 10-16 June 2026 sources-and-uses table to the cent from time-stamped statements of Vinanzas (eight accounts), ITTI, Grupo Vázquez, Redisa, Redipro, Kasas and Model.
2. Pull SIPAP logs for those days to order credits and debits and identify the unexplained USD 542,178.13 and USD 1,000,000.78.
3. Obtain the broker-dealer's trade tickets and settlements for 11 and 15 June: buyer, seller, security, nominal, price, primary or secondary.
4. Recompute the nine portfolio prices from the loan ledgers and check the accounting entry and provisions released on 15 June.
5. Trace the guaraní gaps (Factopar, Vinanzas, Redisa).
6. For each of the 40 record operations, match disbursement to first outward transfer by date, amount and home-banking user; tabulate the lag in hours.
7. Extract home-banking access logs (user, IP, device) for the 12 shared operators, including on the five June borrowers.
8. Get cancellation entries for Franede 612561001554, Hendy 612561002345 and Mowi 612561002893, and the bank's exchange rates for 27 Mar and 24-28 Apr 2026.
9. Identify the 0.5% item on loan settlement sheets.
10. List every 72-hour cheque deposited to Vinanzas, Redisa, Redipro and ITTI from December 2025 to July 2026 with drawee bank and clearing result; test for drawings against uncollected funds.
11. From the certificate-of-deposit register, list 2025 certificates of Grupo Vázquez companies with funding entries, endorsements and any 2026 capital use; compare with the defence's schedules.
12. Contact the three firms on the consecutive receipts; examine the receipt book, cash-count records and vault logs.
13. Collect board and credit-committee minutes for each approval date and share-transfer contracts with proof of payment.
14. Obtain registry extracts (owners, officers, registered office) for Satec, HD Invest, Factopar, Sagas, Infocenter and Match.
