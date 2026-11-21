# Ueno Bank S.A.: credit and prudential assessment

**Analyst role:** AI bank-credit and prudential-regulation analyst. Not a licensed professional; this is analysis and labelled opinion, not advice. **Cut-off:** 20 November 2026.

**Ground rules.** Everything about wrongdoing is alleged. Presumption of innocence applies to every person and company named. The prosecution record (Case 89/2026, 24 pages) is treated as the authoritative statement of what the prosecution alleges (pp. 1-19, summarising the bank supervisor) and of what Julio Rey told prosecutors (pp. 19-24); Rey's statements are his own claims. Press rows carry the reliability of their outlet; the dossier (`dos.*`) is used only for context.

**Currency.** Figures are given in the currency of the source. Where a single total is needed I convert at **Gs. 6,500 per USD**, the rate implied by the record itself (p. 7: Gs. 253,000,000,000 ≈ USD 38,923,077; `src:acta-p07`, `press:fact:0114`). The record's own borrower totals imply different rates per table (6,061 to 6,604; `rec:issue:0010`), so converted totals are indicative to about ±5%.

---

## 1. Underwriting quality

### 1.1 The six borrowers in the record

| Borrower | Granted (record tables) | Outstanding (record tables) | At Gs. 6,500 | Overdraft share of outstanding | Financial capacity stated | Ratio |
|---|---|---|---|---|---|---|
| MOWI | USD 23.27 M + Gs. 239.09 bn | USD 23.27 M + Gs. 100.50 bn | Gs. 251.7 bn | 40% | "No capacity to generate ordinary income" (record p. 4); press relays debt/equity 12.5x, long-term debt 154x 2025 revenue | n/a (inputs not printed) |
| Grupo Hendy | USD 25.23 M + Gs. 190.92 bn | USD 25.23 M + Gs. 99.59 bn | Gs. 263.6 bn | 38% | Average monthly income Gs. 73 M (2025); negative equity at end-2024 | **288.3x annual income** (record total Gs. 252.52 bn / Gs. 876 M) |
| Grupo M | USD 29.52 M + Gs. 55.97 bn | same | Gs. 247.9 bn | 39% | Income Gs. 10.576 bn; equity Gs. 5.327 bn; liabilities 96% of assets | **22.4x income; 44.5x equity** (record total Gs. 237.11 bn) |
| TUIU | USD 30.65 M + Gs. 144.60 bn | USD 30.65 M + Gs. 87.10 bn | Gs. 286.3 bn | 53% | None printed; incorporated 28 Nov 2024 | n/a |
| FRANEDE | USD 60.83 M + Gs. 160.00 bn | USD 51.08 M | Gs. 332.0 bn (record: Gs. 314.0 bn) | 0% (one overdraft, no amount) | Average monthly income Gs. 872 M (2025); loss in 2024 | **30.0x annualised income** (Gs. 314.0 bn / Gs. 10.46 bn) |
| AIME | USD 25.05 M + Gs. 250.95 bn | USD 7.23 M + Gs. 52.36 bn | Gs. 99.4 bn | 100% | None printed; debts only at Ueno | n/a |
| **Six** | | **USD 166.98 M + Gs. 395.52 bn** | **Gs. 1,480.9 bn (≈ USD 227.8 M)** | **37%** | | |

Sources: `rec:loan:0001`-`0035`; `src:acta-p03`, `p04`, `p05`, `p07`, `p08`, `p12`, `p13`, `p15`; `press:fact:0322`, `0323`. The six-borrower USD total reconciles to the supervisor figure relayed by the press (USD 166.98 M, `press:fact:0103`); the guaraní figure there (Gs. 343.157 bn, `press:fact:0104`) equals my total less AIME's guaraní overdraft of Gs. 52.364 bn (`rec:loan:0035`), so the press figure probably predates 4 May 2026.

**Readings.**

- **Size versus capacity.** Hendy's debt was 288 times its annual income; interest alone, at the printed rates and Gs. 6,500 per USD, is about Gs. 37.0 bn a year, or **42x annual income** (`rec:loan:0008`-`0011`). For Grupo M, interest on the three USD term loans alone (USD 1.83 M a year, about Gs. 11.9 bn) is 113% of total income (`rec:loan:0012`-`0014`, `src:acta-p08`). Neither borrower could service interest from operations, let alone principal. The record's own Grupo M ratios (long-term debt 23.5x equity, 11.85x income) rest on statements carrying Gs. 125.4 bn of long-term debt; the bank's exposure by April 2026 was 1.9 times that, so they understate the final position.
- **Tenor and structure.** Term loans run 7 to 10 years with annual amortisation, so the first test of repayment capacity arrives 12 months after disbursement. Only one term loan shows a recorded amortisation (Hendy, `rec:loan:0007`) and the record says it was paid with REDIPRO funds that originated at ITTI (`rec:flow:0008`, `0009`).
- **Pricing.** USD term loans carry 7.5% to 8.5%, guaraní term loans 12% to 12.5%, guaraní overdrafts 24.15% and one USD overdraft 10.51%. The only benchmarks inside the sources: the bank's own five-year senior notes at 6.70% (March 2026, `chrono:event:0032`) and an ITTI-to-Vinanzas intragroup framework loan at 13% (`press:flow:0053`). An 8% ten-year unsecured loan to a borrower with negative equity therefore earned about 130 basis points over the bank's own five-year wholesale cost and 500 basis points less than the group charged itself. In my opinion that margin does not price the risk described; it is consistent with the record's phrase "condiciones preferenciales".
- **Collateral.** All on sole signature. For FRANEDE the bank reported mortgages, but the supporting paper was a commitment letter that the record says was not enforceable; the bank later excluded it (`src:acta-p14`, `rec:loan:0023`-`0028`).
- **Revolving overdrafts.** 37% of the outstanding balance of the six is overdraft, and every guaraní balance still outstanding is an overdraft. Overdrafts have no amortisation schedule, so they do not age into arrears.
- **Evergreening.** For each of the six the record alleges the same two-way pattern: proceeds forwarded almost immediately to ITTI, REDISA, REDIPRO, Vinanzas or Grupo Vázquez, and repayments funded by those same companies (`rec:flow:0001`-`0040`). Dated examples: TUIU's Gs. 57.5 bn overdraft of 2 Jan 2026 was repaid on 30 Jan with REDIPRO money that came from Vinanzas, itself funded with 72-hour cheques (`rec:event:0061`); Grupo M's first instalment on 29 Apr 2026 came from ITTI (`rec:event:0063`); AIME's 30-day and 90-day bullet loans (Gs. 133.7 bn, USD 6.8 M, Gs. 64.9 bn) were all cancelled, the record says with transfers from the same group companies, and overdrafts followed in April and May (`rec:loan:0030`-`0035`, `rec:flow:0033`-`0040`).
- **Timing against ownership changes.** First loans follow or straddle the share transfers by days: FRANEDE same day (30 Jun 2025), TUIU one day after, AIME three days after, MOWI seven days after; Hendy and Grupo M were lent to four days *before* ITTI and Grupo Vázquez left the share register (`rec:event:0050`, `0052`, `0053`, `0054`, `0060`).
- **A pattern in the amounts (inference).** In 12 of the 39 record operations with amounts, the booked principal is a round sum plus exactly 0.5% (for example USD 5,075,250 = 5,050,000 × 1.005; Gs. 100.5 bn = 100 bn × 1.005), and three FRANEDE balances equal principal plus exactly 0.5% (`rec:issue:0007`). The press shows the same arithmetic: Nubicom's Gs. 417.075 bn loan against Gs. 415 bn paid on to ITTI (`press:loan:0045`, `press:flow:0091`). The simplest reading is that a 0.5% up-front charge was financed inside the loan, so the borrower did not fund even its origination cost. This is my inference, not a statement in any source.

### 1.2 Second ring (press and rating data; regulator as relayed)

| Borrower | Exposure reported | Capacity datum | Ratio | Terms / use |
|---|---|---|---|---|
| GSR | Gs. 453.8 bn (list); Gs. 439.1 bn at Aug 2026 | Paid-in capital Gs. 100 M; 2025 revenue projection Gs. 10.7 bn | **4,538x paid-in capital**; 41x projected 2025 revenue | 10 years, sole signature; project financed 100% by Ueno; routed to Vinanzas and ITTI |
| Nubicom | Gs. 228.4 bn (list); lines up to USD 85 M | Paid-in capital Gs. 200,000 | **1,142,155x paid-in capital** | Gs. 417.1 bn, 180 days, sole signature; Gs. 415 bn paid to ITTI next day |
| Grupo Berilo | USD 30.15 M + USD 26.4 M + Gs. 82.4 bn | Shareholder commitment USD 3.8 M, off balance sheet | Commitment = 5.5% of USD 69 M of loans | Proceeds to Vinanzas the same day |
| Nuevo Mundo | Gs. 199.0 bn (≈ USD 30.6 M) | Budget raised from USD 5.16 M to USD 33 M without support | 5.9x original budget | Routed to Vinanzas and ITTI |
| Office Design | Gs. 359.7 bn + Gs. 67.2 bn overdraft | n/a | n/a | 8 years; FX operations to cover ITTI overdrafts |
| Galadriel | USD 15.07 M | No project, cash flow or risk analysis in file | n/a | 720 days, sole signature; funded ITTI FX operation |
| Sagas | Gs. 268.4 bn | Debt elsewhere Gs. 84.3 M | **3,183x** its other bank debt | Gs. 86.1 bn passed to Vinanzas on 15 Jun 2026 |
| La Tropa Fletes | USD 10 M (list: Gs. 246.5 bn) | Capital Gs. 250 M; system deposits Gs. 2.24 bn | List debt 986x capital | Whole loan to Ueno Casa de Bolsa for group bonds |
| SATEC / HD Invest / Technoma / Factopar | USD 20 M / 35 M / 10 M / 6.84 M (11-15 Jun 2026) | No terms in record | n/a | See section 4 |

Sources: `press:fact:0001`-`0016`, `0026`-`0030`, `0039`-`0043`, `0047`, `0060`, `0061`, `0073`, `0074`, `0086`, `0087`, `0096`, `0097`, `0110`, `0326`, `0327`; `press:loan:0045`, `0048`, `0058`; `rec:loan:0036`-`0040`. The debtor list is unofficial and undated; treat it as medium reliability.

---

## 2. Related-party and single-risk-unit exposure

**What the sources say.** At 30 April 2026 the three declared-related borrowers owed Gs. 743.784 bn, 30% of effective equity (31.9% in the charges against the Superintendent), against a cap of Gs. 493.447 bn (20%): an excess of Gs. 250.337 bn sustained for more than ten consecutive days (`press:fact:0081`-`0085`, `chrono:event:0034`). The supervisor as relayed puts total related exposure above USD 300 M (`press:fact:0321`), which is 73% of the USD 410 M effective equity printed in the same coverage (`press:fact:0118`). My own sum of record balances for the six (Gs. 1,480.9 bn) is **3.0x the cap and 60% of effective equity**. Caveat: the 20% figure is a BCP regulatory limit as reported; the statutory 20% of Ley 861/96 art. 59 was repealed in 2016 and the current BCP resolution was not retrieved (`analysis/legal_framework.md` §3, §6).

**"One unit of risk".** Under arts. 46-47 of Ley 861/96, debtors are aggregated as a single exposure when one controls or decisively influences another, when credit to one is presumed to benefit another, or when one's repayment capacity depends on another. The record alleges exactly those facts: proceeds passed in full to group companies and repayments came from them (`src:acta-p07`, `p08`). If so, the economically relevant debtor of all these loans is the ITTI / Grupo Vázquez complex, and the exposure to measure against capital is the sum, not each shell.

**Effect of the October 2025 de-listing request.** As related parties, the three share one 20% bucket. As unrelated clients each would be tested alone: Gs. 254.2 bn, 252.5 bn and 237.1 bn are each about 10% of effective equity, inside any plausible single-borrower limit. De-listing would therefore have turned one 30% breach into three compliant 10% exposures without moving a guaraní. The record says the request came without documentation and lending continued without a formal reply (`rec:event:0055`); the press says documents arrived only in May 2026 (`press:event:0046`).

**Effect of the 15 June 2026 sale.** The nine term loans (USD 74.4 M) left the balance sheet; the same day REDISA and REDIPRO paid off the Hendy and MOWI overdrafts (Gs. 118.2 bn and Gs. 109.7 bn) with money remitted by Vinanzas, and ITTI cleared Grupo M's USD overdraft (`press:loan:0029`, `0030`; `press:flow:0040`, `0055`-`0058`; `rec:flow:0055`). Reported exposure to the three fell by about Gs. 752.7 bn (the fate of Grupo M's Gs. 56.0 bn guaraní overdraft is not stated); the BCP later said the excess was "corrected" on 15 June (`chrono:event:0038`). New loans of 11-15 June to the funding companies total USD 81.841 M plus Gs. 280.5 bn, about Gs. 812.5 bn. **Net, the bank's credit exposure rose by about Gs. 59.7 bn (≈ USD 9.2 M) while its reported related-party exposure fell by about Gs. 753 bn.** On provisioning: the loans were sold as category 1a (`rec:flow:0062`-`0070`) at 103.8% of original principal, which matches principal plus accrued contractual interest for most of the nine. No loss was recognised and about USD 2.7 M of accrued interest was collected with the bank's own money.

---

## 3. Capital and solvency

**Reported versus adjusted.** 13.85% reported, 12% minimum, 5.56% after supervisory adjustments, with a provisions shortfall of Gs. 1,621.9 bn (`chrono:event:0070`). Resolution requires a ratio below half the minimum, i.e. below 6% if the 12% ratio is the reference (`rec:event:0067`).

**Arithmetic (assumptions stated).** Take effective equity of Gs. 2,467 bn (cap ÷ 20%, April 2026). Reported 13.85% implies risk-weighted assets of about Gs. 17,814 bn. Deducting the provisions shortfall from both numerator and denominator gives (2,467 − 1,622) ÷ (17,814 − 1,622) = **5.2%**; with equity of Gs. 2,500 bn, 5.3%. The published 5.56% is therefore roughly what the provisions shortfall alone produces. Inference: the 5.56% does not appear to include two other items the BCP board discussed on 19 June 2026 (`press:event:0026`):

| Step | Capital (Gs. bn) | Ratio on unchanged RWA |
|---|---|---|
| Effective equity, April 2026 | 2,467 | 13.85% |
| Less provisions shortfall 1,622 | 845 | 4.7% (5.2% if RWA also falls) |
| Less placements in REDISA and REDIPRO, 877 | −31 | −0.2% |
| Less merger-expenses trust, 2,106 | −2,137 | −12.0% |

The last two rows are scenarios, not findings; the supervisor may have treated part of those items differently, and the dates differ (equity April 2026; trust and placements December 2025; shortfall November 2026).

**Quality of equity at December 2025.** Book equity Gs. 2,117.7 bn. The merger-expenses trust (deferred charges to be amortised to 2035) stood at Gs. 2,105.7 bn, **99.4% of equity**; excluding it leaves Gs. 11.9 bn, 0.06% of assets. "Other assets", which include an undisclosed amount of deferred losses of the absorbed bank, add Gs. 2,514.5 bn; together the two are 2.2x equity (`press:fact:0254`, `0265`, `0266`). The two facilities approved on 27 May 2024 totalled Gs. 5.1 trillion, 3.5x end-2024 equity (`chrono:event:0017`). The provisions shortfall equals 5.2 years of 2025 profit and 14.6% of net loans (`press:fact:0248`, `0258`). Reported non-performing loans were 0.44% against 2.10% for the system (`press:fact:0262`); that figure is what evergreening would produce.

**Rey's description.** Rey says expenses on technology, products and cashback were first deferred through asset sales between the bank and related companies (real estate, software) and then moved into loans to related and unrelated firms "por valor de unos novecientos millones de dólares": about USD 300 M cashback, USD 300 M technology and other, remainder not broken down (`rec:flow:0074`, `0075`; `src:acta-p22`). He also says the 2024 feasibility plan with its facilities was approved by the BCP and visible to it (`rec:event:0044`). These are his claims.

If accurate: USD 900 M is Gs. 5,850 bn, **2.8x book equity** and 53% of end-2025 net loans. A loan that financed an expense already consumed has no asset behind it; its only repayment source is the group. Capital would fall below the 6% trigger with a loss rate of **25%** on that book, and effective equity would be exhausted at **42%**. The supervisor's Gs. 1,622 bn shortfall is 28% of Rey's figure. As a cross-check on order of magnitude: the unofficial debtor list (excluding IPS and Valores Casa de Bolsa) sums to Gs. 4,939 bn, about USD 760 M; adding the six record borrowers gives about USD 988 M, with some double counting (`press:fact:0001`-`0021`). Rey's number is at least not out of scale with independently reported exposures.

Rey also describes cash of about USD 17 M and Gs. 17 bn (hearsay via a colleague) later documented as collections of dead loans and used to buy certificates of deposit meant to capitalise the bank in 2026 (`rec:flow:0071`-`0073`). At Gs. 6,500 that is Gs. 127.5 bn, about 5% of effective equity: small for solvency, serious for the integrity of capital if true.

---

## 4. The Vinanzas transaction as a prudential matter

**Before and after.** Before: nine category-1a loans to three related shells, USD 71.7 M of original principal. After: USD 74,418,418.12 of "cash" received and USD 81.841 M of new sole-signature loans to SATEC, HD Invest, Technoma, La Tropa Fletes and Factopar, made on 11 and 15 June (`rec:loan:0036`-`0040`, `rec:flow:0060`, `0061`). Vinanzas held about USD 93,628 the day before (0.13% of the price) and received USD 76.06 M on the day (`rec:event:0064`, `press:fact:0037`). The bank lent 110% of the price it then received; USD 55 M went straight from SATEC and HD Invest to Vinanzas, and the rest travelled through purchases of group bonds (`rec:flow:0046`-`0059`).

**Why derecognition fails in substance.** A sale removes an asset only if the seller stops bearing its risk. Here (alleged) the buyer is a related party with no resources; the price was funded by the seller; the buyer's ability to repay its funders depends on the same shells whose loans were sold. The bank's risk moved from "MOWI, Hendy, Grupo M" to "five companies whose repayment depends on Vinanzas collecting from MOWI, Hendy, Grupo M". That is the same risk plus intermediaries, at a higher amount. The record adds that the applicable rule prohibits financed portfolio sales to related parties (`src:acta-p17`, `p19`); the regulation is reported as BCP Resolution 15/24 but its text was not retrieved.

**What an examiner needed to see.** (1) Vinanzas account statements for 1-15 June; (2) the bank's disbursements of the preceding week matched against credits to the buyer; (3) proof of the buyer's own or third-party funds; (4) credit files of the five new borrowers, stated purpose against use; (5) Ueno Casa de Bolsa trades of 11-15 June; (6) a valuation supporting par plus interest for unsecured loans to a borrower with negative equity. Items 1 and 2 sit in the bank's own systems, and the supervisor did obtain them (reports of 10 July, 28 July and 5 August 2026; `press:event:0008`-`0010`).

---

## 5. Group dependence

**ITTI.** 2025 standalone revenue Gs. 1,826 bn (+80%), EBITDA Gs. 418.8 bn, equity Gs. 460.3 bn, liabilities 3.9x equity (`press:fact:0178`-`0191`). About 59% of revenue (USD 168 M) came from related parties (`press:fact:0299`). Intercompany "sundry debtors" doubled to Gs. 341.3 bn, 74% of equity (`press:fact:0198`, `0199`). ITTI is also the main alleged recipient of forwarded loan proceeds. If the bank's loans to shells financed payments to ITTI, part of ITTI's revenue was the bank's own money, and both ITTI's earnings and the bank's interest income were supported by the same circuit. A single Nubicom payment of Gs. 415 bn (July 2026) equals 23% of ITTI's whole 2025 revenue (`press:flow:0091`).

**Grupo Vázquez (holding).** 2025 individual revenue Gs. 769.1 bn, of which Gs. 379.3 bn (49%) is valuation of investments; 70% in 2024. Dividends received were Gs. 12.1 bn: 1.6% of revenue and 1.1% of financial debt of Gs. 1,067 bn (`press:fact:0128`, `0140`, `0157`, `0158`). The stake in U Holdings (the bank's parent) is carried at Gs. 3,083 bn, 67% of assets and **147% of equity** (`press:fact:0134`, `0138`, `0156`). Writing it to zero leaves equity of about −Gs. 980 bn. FIX put individual leverage at 9.5x EBITDA (`press:fact:0289`).

**Implications.** Recoverability of the bank's loans depends on ITTI and Grupo Vázquez; their solvency depends on the bank's value and on fees from the bank. With the bank in resolution the loop is broken on both sides. For holders of group paper: at June 2026 Grupo Vázquez had USD 204 M of bonds, USD 54 M of short-term maturities and USD 71 M of cash; ITTI USD 40 M of bonds, USD 22 M short-term, USD 35 M cash (`press:fact:0302`-`0312`); both were cut to Cpy on 3 November. About USD 26.8 M of June 2026 bank loans funded purchases of group bonds through the group broker (`rec:loan:0038`-`0040`), so part of recent "market" demand for that paper was bank-financed. Mutual funds holding bank instruments were told to value them at zero (`chrono:event:0114`).

---

## 6. Supervisory red flags and when they were visible

| Date | Event | Days before resolution |
|---|---|---|
| 27 May 2024 | BCP authorises merger facilities of Gs. 5.1 trillion (`chrono:event:0017`) | 889 |
| 29 Aug 2025 | SIB report: past-due portfolio under the facility not separated in the accounts (`chrono:event:0026`) | 430 |
| Oct 2025 | De-listing request without documents; lending continues (`rec:event:0055`) | ~370 |
| 29-30 Apr 2026 | Related exposure 30-32% versus 20%; Superintendent allegedly informed (`chrono:event:0034`) | 187 |
| 5-8 Jun 2026 | SIB confirms relatedness, orders recalculation; report 006/2026 (`press:event:0005`, `0006`) | 150 |
| 15 Jun 2026 | Vinanzas sale; excess "corrected" | 140 |
| 19-29 Jun 2026 | BCP board minute 27 and director's memo: REDISA/REDIPRO placements not deducted, trust expenses, portfolio classification (`press:event:0026`, `0041`) | 136 |
| 10 Jul 2026 | Report 007/2026 and supervision manager's memo recommending rejection of the sale and a regularisation plan; he is reassigned the same day (`press:event:0008`, `0024`) | 115 |
| 5 Aug 2026 | Findings report 011/2026: prohibited indirect financing (`press:event:0010`) | 89 |
| 24 Sep 2026 | BCP Resolution 42 opens administrative proceedings (`press:event:0011`) | 39 |
| 2 Nov 2026 | Resolution | 0 |

**Even-handed reading.** In the supervisor's favour: the breach could be measured only once relatedness was settled, and the bank's de-listing request and late documents delayed that; tracing the June circuit took account-level work, completed in 51 days; rating agencies (AA-py in March, A+py for the holding in July), an international bond placement and a foreign bank investor all passed the same balance sheet; the merger facilities were a formal regulatory decision. Against: the ten-day limit breach is itself a statutory regularisation trigger (Ley 2334/03 art. 6) and was known by late April; the capital-quality issues were minuted on 19 June; loans of the same pattern were still granted on 1 and 31 July 2026 (Nubicom Gs. 417 bn, Galadriel USD 15.07 M; `press:loan:0045`, `0058`), after reports 006 and 007; and the conflict on whether the regulator replied to the de-listing request (the record says no formal reply; one outlet says it refused for MOWI, `press:event:0004`) is unresolved. The officials charged have not been tried and their defence is not in the sources I read.

---

## 7. Recovery outlook: scenarios, not predictions

**Fixed points.** Deposits about USD 2.8 bn; guarantee expected to absorb USD 740 M to 928 M (26% to 33% of deposits; 46% to 58% of a fund of USD 1.6 bn); Gs. 3.9 trillion already paid to 1.81 million people (`chrono:event:0138`, `0166`, `0179`, `0181`). Public funds at 30 Sept 2026: Gs. 3.6 trillion plus USD 233.4 M, about USD 787 M at Gs. 6,500; IPS between USD 348.5 M and USD 517 M depending on source (`chrono:event:0052`, `0198`; `press:fact:0106`). The BCP said on 12 Nov that healthy assets were about USD 600 M and on 18 Nov that assets suffice to cover deposits (`chrono:event:0187`, `0226`); the two statements are not reconciled in the sources.

**Illustrative coverage test** (December 2025 balance sheet, the latest available; stale by ten months). "Hard" assets = total assets Gs. 21,095.5 bn, less trust, other assets and REDISA/REDIPRO placements (Gs. 5,496.9 bn, 26% of assets), less a credit loss:

| Scenario | Credit loss assumed | Hard assets / deposits (Gs. 15,830.8 bn) |
|---|---|---|
| A. Supervisor's shortfall only | Gs. 1,622 bn | 88% |
| B. Rey's USD 900 M, half lost | Gs. 2,925 bn | 80% |
| C. Rey's USD 900 M, all lost | Gs. 5,850 bn | 62% |

For deposits to be covered in full, as the BCP stated, scenario A needs material value from the "soft" assets or a 2026 balance sheet better than end-2025. I cannot test that without the exclusion balance.

**Loss drivers.** (1) The loan book to group-dependent borrowers is unsecured; the only recovery route is the group's assets. Three seized ranches are valued at USD 15.95 M, 7% of the six-borrower exposure; 2,331 properties are identified without values (`press:fact:0063`-`0065`, `0080`). (2) Deferred charges in the trust are spent money with no liquidation value. (3) The value of REDISA/REDIPRO placements depends on businesses that lived off the bank. (4) Time: a slow tender erodes the performing retail book. (5) Ranking: guaranteed private deposits and public social-security deposits come first (Ley 2334/03 art. 20 as summarised in the framework file); bonds do not. IPS reportedly holds Gs. 250 bn of bonds, issuer split not given (`press:fact:0033`). The international notes (USD 350 M) trade near 5 cents (`chrono:event:0200`). (6) Deposits of related persons are excluded from the guarantee (art. 1 f).

**By class.** Small depositors: largely paid. Large private and public depositors: scenarios A to C span roughly 60% to 90% asset coverage before costs and before the guarantee fund's own claim. Bondholders of the bank: little or nothing in B and C. Holders of Grupo Vázquez and ITTI bonds: dependent on non-bank assets and on litigation over seized property.

---

## Opinions

1. **Opinion: these were not credit decisions in the ordinary sense.** Debt of 288x income (Hendy), 22x income and 45x equity (Grupo M), 4,538x paid-in capital (GSR) and 1.1 million times paid-in capital (Nubicom), on sole signature for up to ten years, cannot be explained by optimistic underwriting. Basis: `src:acta-p05`, `p07`, `p08`; `press:fact:0047`, `0097`.
2. **Opinion: the loans functioned as group funding booked through shells, and performing status was manufactured by circular repayment.** Basis: the alleged forwarding and repayment flows in `rec:flow:0001`-`0040`, the 37% overdraft share, and the 0.44% NPL ratio.
3. **Opinion: the six borrowers, and probably much of the second ring, were one unit of risk whose true obligor was ITTI / Grupo Vázquez; on that basis the exposure was about three times the related-party cap before the June sale.** Basis: `rec:loan:0001`-`0035`, `press:fact:0083`.
4. **Opinion: the 15 June sale changed labels, not risk, and should not have been derecognised.** The bank lent 110% of the price it received and its total exposure rose. Basis: `rec:flow:0041`-`0061`, `rec:event:0064`.
5. **Opinion: reported capital was overstated well before November 2026.** With a deferred-expense trust equal to 99.4% of book equity, loss-absorbing capital at December 2025 was close to nil on any conservative reading, whether or not the facility was lawfully authorised. The authorisation is a regulatory fact; it does not create loss absorption. Basis: `press:fact:0254`, `0265`; `chrono:event:0017`.
6. **Opinion: Rey's USD 900 M is plausible in scale but unverified, and if even a quarter of it is unrecoverable the bank was below the resolution trigger.** Basis: `rec:flow:0075`; computation in section 3.
7. **Opinion: the supervisor had enough by late April 2026 (limit breach) and certainly by 19 June 2026 (board minute) to impose a regularisation plan and stop new lending to the pattern; whether the delay to November was justified is for the proceedings to decide.** Basis: `chrono:event:0034`, `press:event:0026`, `press:loan:0045`, `0058`.
8. **Opinion: full recovery for uninsured depositors is possible but is not the central case on the published numbers; bondholders of the bank should expect heavy losses.** Basis: section 7 scenarios; `chrono:event:0187`, `0200`.

## What would change my view

- The bank's monthly balance sheets and solvency worksheets for 2026, and the BCP's adjustment schedule behind 5.56% (which items were deducted).
- The exclusion balance and the definition of the USD 600 M "healthy assets".
- Text of the BCP resolutions on related-party limits, single-borrower limits and portfolio sales (Res. 15/24), and of Resolution 32 of 27 May 2024 with the feasibility plan: if the plan expressly allowed the transactions Rey describes, opinions 5 and 7 soften.
- Credit files and audited statements of the borrowers (TUIU, AIME and MOWI have no income or equity figures in the record), and any collateral or guarantees not mentioned.
- Evidence of real project spending by borrowers (works, licences, equipment) that would show economic use of proceeds.
- A loan-by-loan schedule supporting or refuting Rey's USD 900 M, and the trust's expense ledger.
- Audited 2025 statements of REDISA, REDIPRO and Vinanzas.
- Independent valuations of group assets under seizure, and whether Grupo Vázquez and ITTI met the bond payments due from 19 November 2026.
- The defence's account for each director and official; none of it is tested here.
