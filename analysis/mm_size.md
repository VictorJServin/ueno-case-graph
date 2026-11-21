# Ueno Bank S.A.: how much money is missing

**Status.** Analysis by an AI bank-resolution and financial-loss analyst, not a licensed professional. Figures are reported facts, computations from reported facts, or estimates with stated assumptions. Nothing here is a finding. Conduct is described as alleged; everyone named is presumed innocent. The prosecution record (Case 89/2026) states what the prosecution alleges and what Julio Rey told prosecutors; Rey's statements are his own claims. Cut-off: 20 November 2026.

**Kinds.** R = reported fact, C = computation from reported facts, E = estimate with assumptions. Confidence: H, M, L.

**Exchange rate.** Gs. 6,500 per USD, the rate the record itself uses on page 7 (Gs. 253,000,000,000 given as about USD 38,923,077; `src:acta-p07`, `press:fact:0114`). Sensitivity uses two other printed rates: Gs. 6,358.5 (wholesale, 5 November 2026; `chrono:event:0122`) and Gs. 6,585.55 (December 2025; `press:fact:0219`). "Gs. bn" means thousand million guaraníes.

## 1. Answer

On published numbers, the bank's realisable assets fall short of its liabilities by about **USD 740 million**, in a range of **USD 390 million to USD 1.26 billion**. That is what creditors as a group stand to lose after shareholders lose their USD 375 million of book equity. It is an estimate built on the June 2026 balance sheet, the last one published.

"Missing" has at least three other meanings, and they must not be added to the figure above or to each other:

| Meaning | Low | Central | High | Conf. |
|---|---|---|---|---|
| A1. Capital hole, supervisor-stated | USD 167 M | USD 250 M | USD 320 M | M |
| A2. Capital hole plus questioned assets | USD 384 M | USD 708 M | USD 847 M | M |
| A3. Capital hole on Rey's account | USD 600 M | USD 900 M | USD 1,224 M | L |
| B. Questioned credit outstanding (exposure) | USD 594 M | USD 879 M | USD 946 M | M |
| E. Cash outside the system | 0 | USD 19.6 M | USD 20.8 M | L |
| F. Shortfall of assets against all liabilities | USD 393 M | USD 738 M | USD 1,263 M | L |

A1 sits inside A2. B is the loan book behind most of A1 and A3. F is B after a loss rate, plus the non-credit items in A2, less equity. The prosecution's own damage figure, USD 809.5 million (`chrono:event:0148`, R, M), falls between the central values of A2 and A3.

## 2. A. The capital hole

| Figure | Value | As of | Asserted by | Ref | Kind | Conf. |
|---|---|---|---|---|---|---|
| Solvency reported / minimum / adjusted | 13.85% / 12% / 5.56% | 2 Nov 2026 | Regulator via 5Días | `chrono:event:0070` | R | M |
| Provisions deficit | Gs. 1,621.9 bn (USD 249.5 M) | Nov 2026 | Regulator via press | `chrono:event:0070`, `press:fact:0105` | R | M |
| Civil embargo sought by the BCP | USD 70 M + Gs. 1.6 trillion | 3 Nov 2026 | BCP via court | `chrono:event:0084` | R | M |
| Placements in REDISA and REDIPRO | Gs. 876.6 bn (USD 134.9 M) | Dec 2025 | BCP director's memo via ABC | `press:fact:0126`, `press:event:0041` | R | M |
| Merger-expenses trust | Gs. 2,105.7 bn (USD 324.0 M) | Dec 2025 | Rating agency | `press:fact:0265` | R | M |
| Other intangible assets | Gs. 901.0 bn (USD 138.6 M) | Dec 2025 | FIX SCR | new source 2 | R | M |
| Deferred charges and intangibles | Gs. 825.2 bn (USD 126.9 M) | Jun 2026 | Bank | new source 1 | R | M |
| Book equity | Gs. 2,117.7 bn; Gs. 2,436.5 bn | Dec 2025; Jun 2026 | Rating agency; bank | `press:fact:0254`; new source 1 | R | M |
| Effective equity before adjustment | about Gs. 2,559 bn | Nov 2026 | This analysis | from `chrono:event:0070` | C | M |
| Risk-weighted assets before adjustment | about Gs. 18,476 bn | Nov 2026 | This analysis | from `chrono:event:0070` | C | M |

**Arithmetic.** Two equations, two unknowns: equity ÷ RWA = 13.85%, and (equity − 1,621.9) ÷ (RWA − 1,621.9) = 5.56%. The solution is equity of about Gs. 2,559 bn and RWA of about Gs. 18,476 bn (72% of June 2026 assets, a plausible density). If the deficit is taken only from the numerator the values are Gs. 2,710 bn and Gs. 19,564 bn. Either way, **the provisions deficit alone reproduces 5.56%**. My inference is that the adjusted ratio does not deduct the trust, the REDISA and REDIPRO placements or intangibles.

**Three definitions.**

| Definition | Deduction (Gs. bn) | Capital after (Gs. bn) | Ratio | Needed to reach 12% |
|---|---|---|---|---|
| A1. Supervisor-stated: provisions deficit | 1,621.9 | 937 | 5.56% | Gs. 1,085 bn (USD 167 M) |
| A2-low. Plus REDISA and REDIPRO placements | 2,498.5 | 60 | 0.4% | Gs. 1,857 bn (USD 286 M) |
| A2-central. Plus merger-expenses trust | 4,604.2 | −2,045 | negative | Gs. 3,710 bn (USD 571 M) |
| A2-high. Plus intangibles | 5,505.2 | −2,946 | negative | Gs. 4,503 bn (USD 693 M) |
| A3. Rey: loans standing in for expenses | 5,850 (USD 900 M) | −3,291 | negative | not computed |

All rows are C from the inputs above; A2 and A3 are scenarios. A1's range runs from the capital needed to regain 12% (USD 167 M), through the deficit itself (USD 250 M), to the deficit plus the USD 70 million in the embargo (USD 320 M).

Caveats. The trust and the placements are December 2025 values; the bank's "investments" line fell only from Gs. 3,188 bn to Gs. 3,067 bn by June 2026, so neither was unwound in the first half (`press:fact:0264`; new source 1). The trust was authorised by BCP Resolution 32 of 27 May 2024 (`chrono:event:0017`); authorisation makes it lawful to carry, not able to absorb losses. A financial executive's "USD 1,600 million capital deficit" quoted by ABC is almost certainly a confusion with Gs. 1.6 trillion and is not used.

## 3. B. Questioned credit

**De-duplication.** The dataset has 109 loan rows (40 record, 69 press). The sameOperation rule (same operation number, or same borrower, date and amount within 0.6%) reduces them to 73 operations. The editor's manual matches take it to about 60: the USD 10,593,000 loan of 27 March 2026 is FRANEDE's, not Henrici's (`rec:loan:0027`, `press:loan:0010`), and "USD 14.3 M" for Grupo M is the sale value of `rec:loan:0012`. Technoma and La Tropa Fletes each borrowed USD 10 million on 11 June; those are two loans. Editor corrections are applied throughout.

| Block | USD part | PYG part | Combined at 6,500 | Asserted by | Ref | Kind | Conf. |
|---|---|---|---|---|---|---|---|
| (i) Six record borrowers, record balances | USD 166.98 M | Gs. 395.5 bn | Gs. 1,480.9 bn (USD 227.8 M) | Prosecution | `rec:loan:0001`-`0035`; `press:fact:0103` | C | H |
| (i) Same six, after 15 June 2026 | USD 88.97 M | Gs. 195.4 bn | Gs. 773.7 bn (USD 119.0 M) | This analysis | plus `rec:flow:0060`, `press:loan:0029`, `0030`, `0034` | C | M |
| (ii) Five June borrowers, June loans | USD 81.84 M | Gs. 194.4 bn | Gs. 726.4 bn (USD 111.7 M) | Prosecution; regulator via press | `rec:loan:0036`-`0040`; `press:loan:0004`, `0007`, `0008` | C | M |
| (ii) Same five, debtor-list balance | not split | Gs. 1,337.5 bn | USD 205.8 M | Press (unofficial list) | `press:fact:0007`, `0012`-`0015` | R | M |
| (iii) Second ring, eight shell-type borrowers | not split | Gs. 2,358.5 bn | USD 362.8 M | Press (unofficial list) | `press:fact:0001`-`0006`, `0011`, `0016` | C | M |
| (iii) Second ring, all 15 listed incl. group companies | not split | Gs. 3,601.4 bn | USD 554.1 M | Press (unofficial list) | `press:fact:0001`-`0021` | C | M |
| (iii) Others outside the list | USD 18 M | Gs. 321.0 bn | Gs. 438.0 bn (USD 67.4 M) | Regulator via press | `press:fact:0090`, `0050`, `0052`; `press:loan:0047` | C | L |

The eight are GSR, Grupo Berilo, Nubicom, Galadriel, Office Design, Nuevo Mundo, Sagas and Henrici. The 15 add Kasas, Model, Grupo Vázquez, ITTI, Redipro, Discover and Muar. "Others" are La Tropa SAE, Dobrestec, TSV and Infocenter. Match appears only as a recipient of money, with no loan figure. IPS and Valores Casa de Bolsa are on the list but are left out.

**Overlap between (i) and (ii).** The June loans funded, as alleged, the purchase of nine of the six's loans (USD 71.7 million of principal) and the pay-down of three overdrafts. Counting the six at record balances plus the June loans counts the same money twice. The totals below use the six after 15 June.

| Questioned book | Gs. bn | USD M at 6,500 | at 6,358.5 | at 6,585.55 |
|---|---|---|---|---|
| Low: six net + five June loans + eight | 3,858.6 | 594 | 607 | 586 |
| Central: six net + five on list basis + 15 listed | 5,712.6 | 879 | 898 | 867 |
| High: central + others | 6,150.6 | 946 | 967 | 934 |

The list prints guaraní figures only, so the currency split of the second ring is not known. The regulator as relayed puts related exposure at "more than USD 300 million" (`press:fact:0321`), which is roughly the six plus the five June borrowers; it leaves most of the second ring outside the official count.

**Unsecured share.** 80% of the six's balance is printed "ASF" (sole signature); the other 20% is overdrafts whose guarantee cell is blank (C, H). FRANEDE's claimed mortgages rested on a letter the bank itself later excluded (`rec:loan:0023`-`0028`). In the second ring, sole signature is reported for GSR, Nubicom and Galadriel, 21% of the listed ring (`press:loan:0032`, `0045`, `0058`). So at least 24% of the central book is expressly unsecured, and no source reports real collateral on any of it. The BCP complaint describes the pattern as signature-only (`chrono:event:0077`).

**Repaid only with group money.** The bank granted the six USD 194.5 million plus Gs. 1,041.5 bn (Gs. 2,306 bn). Of that, 66.5% (Gs. 1,534 bn, USD 236 million) shows as repaid or sold. The record alleges every one of those repayments came from ITTI, REDISA, REDIPRO, Vinanzas or Grupo Vázquez, or from the bank's own June loans (`rec:flow:0009`, `0020`, `0024`, `0031`, `0034`, `0061`). No source shows a repayment from a borrower's own income. On the allegations, the share repaid with independent money is nil.

## 4. C. Rey's USD 900 million

Rey says expenses on technology, products and cashback were deferred first through asset sales between the bank and related companies, then moved into loans to related and unrelated firms "por valor de unos novecientos millones de dólares": about 300 cashback, about 300 technology and other, the rest not explained (`rec:flow:0075`, `src:acta-p22`; R as his claim, L as fact).

| Test | Result | Kind | Conf. |
|---|---|---|---|
| Against B, firms he names (the six, Office Design, Henrici, Model) | Gs. 2,483 bn = USD 382 M, **42%** of 900. Data Force has no figure. | C | M |
| Against B, whole questioned book | USD 879 to 946 M, **98% to 105%** of 900 | C | M |
| Against money traced by amount to ITTI, REDISA, REDIPRO, Vinanzas, Grupo Vázquez | about USD 325 M, 36% of 900 (`analysis/fin_flows.md` §2) | C | M |
| Technology: ITTI billed related parties USD 168 M in 2025 (`press:fact:0299`) | USD 300 M is 1.8 years of that billing | C | M |
| Cashback: 1,824,994 funded accounts (`chrono:event:0165`) | USD 300 M is USD 164 per funded account; spread over the 2.5 years since the bank opened (my assumption), USD 120 M a year, 54% of the bank's 2025 revenue of USD 221 M (`press:fact:0293`) | C | L |
| Against the trust (`press:fact:0265`) | USD 324 M, the size of one of his components | C | M |
| Against loan growth | The central book is 39% of June 2026 performing loans to non-financial borrowers (Gs. 14,568 bn; new source 1) | C | M |

Reading. The figure is plausible in scale: an independently assembled list of questioned borrowers adds up to almost exactly his number. Scale is not proof of purpose. Only 42% can be matched to companies he names, and only about a third to money traced by amount into the group. Cashback of USD 120 million a year would have turned the reported 2025 profit of Gs. 313.9 bn (`press:fact:0258`) into a loss, which is a motive for deferral, but no published total for the programme was found. Rey himself leaves about USD 300 million unexplained. The trust was still on the balance sheet in mid-2026, so if he is right the USD 900 million sits largely on top of it.

## 5. D. Stakeholders: exposure and expected loss

Recovery assumptions come from section 7. Payment order under Ley 2334/03 art. 20, as summarised in `analysis/legal_framework.md`: guaranteed private deposits and public social-security deposits first; other creditors after. Rows overlap and must not be summed.

| Stakeholder | Exposure (USD M) | Expected loss (USD M) | Assumption | Ref |
|---|---|---|---|---|
| Deposit Guarantee Fund | 740 to 928 | 0 to 845 | Zero if it recovers by subrogation (low and central cases). 845 if only the BCP's USD 600 M of healthy assets exists and pension deposits of 517 are paid first. | `chrono:event:0166`, `0181`, `0138` |
| Uninsured private depositors | 1,060 to 1,248 | 0 to 387 | 71% of USD 2.8 bn less the guaranteed part. Nil in low and central; 31% in high. | `chrono:event:0166`; new source 6 |
| IPS | 345 to 517 | 17 to 87 | Pension deposits first-order. Loss on Gs. 250 bn of bonds (43% to 100%) and, in the high case, 31% on USD 157.7 M of operating funds. | `chrono:event:0091`, `0163`, `0198`; `press:fact:0033`; new source 8 |
| All public entities, IPS included | 787 to 888 (press: 800 to 900) | 17 to 255 | Gs. 3.6 trillion plus USD 233.4 M at 30 Sept 2026. Non-pension public deposits treated like uninsured private ones. | `chrono:event:0052`, `0035`; `dos:fact:0002`, `0003` |
| International senior noteholders | 350 | 150 to 350 (market: about 332) | Recovery for non-deposit creditors 57% low, 20% central, nil high. Price about 5 cents. | `chrono:event:0032`, `0200` |
| Local bonds of the bank | 103 | 44 to 103 | Gs. 668.5 bn at Dec 2025, incl. USD 25 M subordinated. Funds told to value at zero. | `press:fact:0260`, `chrono:event:0114` |
| IDB Invest, Triodos, GAWA | about 41 (original) | 17 to 41 | Balances not published. | `chrono:event:0020`, `0048` |
| OTP Bank | 47 | 32 to 47 | Charge booked; remainder at risk. | `chrono:event:0036`, `0177` |
| Bank shareholders | 375 | 375 | June 2026 book equity. OTP is inside this. | new source 1 |
| Grupo Vázquez bondholders | 204 | 122 to 184 | Recovery 10% to 40%: cash 71 against debt 341. | `press:fact:0302`-`0304` |
| ITTI bondholders | 40 | 16 to 32 | Recovery 20% to 60%: cash 35 against debt 66. | `press:fact:0309`-`0311` |
| Local funds (Cadiem and others); Kasas, Model, La Tropa SAE paper | not published; at most about 47 at Cadiem | 0 to 47 | Upper bound applies one fund's 11.73% to all USD 400 M managed. Ueno AFPISA: USD 46 M blocked. | `chrono:event:0114`, `0142`, `0167` |

All expected-loss figures are E, confidence L. Exposure figures are R, confidence M, except where marked.

## 6. E. Cash outside the system

| Item | Value | As of | Asserted by | Ref | Kind | Conf. |
|---|---|---|---|---|---|---|
| Night cash delivery | USD 17 M + Gs. 17,000 M = USD 19.6 M | about May 2025 | Rey, repeating a colleague | `rec:flow:0071`, `0072`; `rec:issue:0009` | R | L |
| Cash orders in internal messages | Gs. 4,537 M (USD 0.7 M) | Jan and Oct 2026 | ABC, leaked documents | `chrono:event:0031`, `0053`, `0058`, `0064` | C | L |
| GSR Security shortfall | Gs. 3,090 M (USD 0.5 M) | 17 Nov 2026 | Press | `chrono:event:0216` | R | L |
| Reserve requirement not replenished | USD 70 M | 29 Oct 2026 | Perfil | `chrono:event:0067` | R | L |

Rey's cash is under 3% of the central shortfall. It did not leave the bank; on his account it came in, was booked as collections of written-off loans and bought certificates of deposit meant to capitalise the bank in 2026 (`rec:flow:0073`). If true, it bears on the origin of about USD 20 million of intended capital, not on the size of the hole. The USD 70 million is a liquidity gap, not cash outside the system, and is already in liabilities.

## 7. F. Reconciliation

Base: balance sheet at 30 June 2026 (new source 1): assets Gs. 25,641.8 bn, liabilities Gs. 23,205.2 bn, equity Gs. 2,436.5 bn. Deposits at end-June are computed as Gs. 17,241 bn from government deposits of Gs. 5 trillion being 29% (`chrono:event:0035`).

| Step (Gs. bn) | Low | Central | High | Kind |
|---|---|---|---|---|
| Assets at book, June 2026 | 25,641.8 | 25,641.8 | 25,641.8 | R |
| Less merger-expenses trust | −2,105.7 | −2,105.7 | −2,105.7 | R |
| Less deferred charges and intangibles | −825.2 | −825.2 | −825.2 | R |
| Less REDISA and REDIPRO placements (50% / 100% / 100%) | −438.3 | −876.6 | −876.6 | E |
| Less loss on questioned book | −1,621.9 | −3,427.6 | −5,535.5 | E |
| Less Visión past-due facility (0 / 0 / 50% of Gs. 2.6 trillion) | 0 | 0 | −1,300.0 | E |
| **Assets left for deposits and creditors** | **20,650.7** | **18,406.7** | **14,998.7** | C |
| Less deposits | −17,241.4 | −17,241.4 | −17,241.4 | C |
| Left for other creditors | 3,409.3 | 1,165.3 | −2,242.7 | C |
| Less other liabilities | −5,963.8 | −5,963.8 | −5,963.8 | C |
| **Shortfall against all liabilities** | **−2,554.5** | **−4,798.5** | **−8,206.5** | C |
| In USD at 6,500 (6,358.5; 6,585.55) | 393 (402; 388) | 738 (755; 729) | 1,263 (1,291; 1,246) | C |
| Assets left ÷ deposits | 120% | 107% | 87% | C |
| Recovery for non-deposit creditors | 57% | 20% | nil | C |

**Assumptions.**
1. The trust and intangibles have no sale value: they are spent money and software.
2. Loss on the questioned book: low takes the supervisor's own deficit (28% of the central book); central 60% of Gs. 5,712.6 bn; high 90% of Gs. 6,150.6 bn. The loans are unsecured and the borrowers' repayment source was the group, whose main asset was the bank. Three seized ranches are valued at USD 15.95 million (`press:fact:0063`-`0065`).
3. The rest of the book, liquid assets and fixed assets are taken at book. That is generous: a tender will discount them.
4. Deposits that left between June and November reduce assets and liabilities equally, so the shortfall in money terms is unaffected.
5. No resolution costs, no accrued interest, no recoveries abroad.

**Against the Central Bank's statements.**

- *"Assets suffice to cover deposits"* (18 November; `chrono:event:0226`). **Reconciles in the low and central cases** (120% and 107% of deposits) and fails in the high case (87%). It is compatible with heavy losses for bondholders: in the central case non-deposit creditors recover about 20 cents, and the international notes trade near 5.
- *"About USD 600 million of healthy assets"* (12 November; `chrono:event:0187`). **Does not reconcile.** USD 600 million is Gs. 3,900 bn, 15% of June book assets. Even my high case leaves USD 2.3 billion. The president of the BCP said the figure came from reviewing client portfolios, excludes real estate and exceeds the bank's debt to the pension system (new source 4). Two foreign outlets reported it as assets exceeding liabilities by USD 600 million (new sources 3 and 5), which cannot be squared with solvency below 6%. The most likely reading is a first pool of performing loans identified by that date, not the total. If it were the total, the guarantee fund would bear most of its USD 740 to 928 million.
- *Provisions deficit of Gs. 1.62 trillion.* Equals my low-case credit loss by construction. It is 28% of the questioned book. Whether it also covers the Visión facility is not stated.
- *Prosecution damage of USD 809.5 million and embargo of about USD 316 million.* The first is close to my central shortfall and to A2; the second is A1 plus USD 70 million.

## 8. Biggest uncertainties

1. **The loss rate on the questioned book.** Each 10 points is about Gs. 571 bn (USD 88 million).
2. **The balance sheet at resolution.** June 2026 is five months stale; the exclusion balance was postponed on 18 November.
3. **What the Gs. 1.62 trillion covers** and which items sit behind 5.56%.
4. **The debtor list.** It is unofficial and undated, and may print cumulative lending.
5. **The Visión past-due facility.** Up to Gs. 2.6 trillion with no published balance; it appears only in the high case.

## 9. What cannot be determined

- Whether Rey's USD 900 million overlaps the trust, and what the unexplained USD 300 million was.
- The total cashback paid.
- Fund-by-fund holdings of bank and group paper; bonds outstanding of Kasas, Model and La Tropa SAE.
- The split of public deposits between pension funds and other entities.
- The value of 2,331 properties and of assets abroad identified by authorities (`press:fact:0080`, `chrono:event:0196`).
- The origin of the cash Rey describes.

## 10. New sources opened

| # | Outlet | Title | Date | URL |
|---|---|---|---|---|
| 1 | ueno bank S.A. | Aviso de balance al 30 de junio de 2026 | Jul 2026 | https://www.ueno.com.py/wp-content/uploads/2026/07/Aviso-Balance-255x35cm_jun2026-1.pdf |
| 2 | FIX SCR | UENO Bank S.A., informe de revisión integral | 31 Mar 2026 | https://www.ueno.com.py/wp-content/uploads/2026/04/UENO-Bank-S.A.-_FIX.pdf |
| 3 | Perfil | El Banco Central de Paraguay informó que encontró activos de Ueno Bank | 13 Nov 2026 | https://www.perfil.com/noticias/amp/internacional/el-banco-central-de-paraguay-informo-que-encontro-activos-de-ueno-bank-y-detallo-a-quienes-se-le-devolvera-ese-dinero-aYk6R4M1Ioff.phtml |
| 4 | InfoNegocios Paraguay | Jorge Schreiner: analizando las carteras de clientes... | 13 Nov 2026 | https://infonegocios.com.py/nota-principal/jorge-schreiner-analizando-las-carteras-de-clientes-y-sin-incluir-activos-el-monto-supera-el-conjunto-de-la-deuda-de-ueno-con-el-sistema-previsional |
| 5 | Diario El Sol | Nota sobre los activos de Ueno Bank informados por el BCP | 13 Nov 2026 | https://www.elsol.com.ar/?p=2281912 |
| 6 | AFP via CR Hoy | ¿Qué pasó con el dinero de Ueno Bank en Paraguay y cuánto falta recuperar? | 10 Nov 2026 | https://crhoy.com/mundo/que-paso-con-el-dinero-de-ueno-bank-en-paraguay-y-cuanto-falta-recuperar/ |
| 7 | EFE via La Prensa | Fondos públicos: el gran desafío tras la intervención del Ueno bank | 9 Nov 2026 | https://www.laprensa.hn/mundo/ueno-bank-paraguay-fondos-publicos-gran-desafio-intervencion-GM32584570 |
| 8 | Forbes Argentina | El escándalo Ueno Bank sacude Paraguay | 10 Nov 2026 | https://www.forbesargentina.com/today/el-escandalo-ueno-bank-sacude-paraguay-fondos-publicos-juego-una-crisis-amenaza-su-reputacion-n102136 |

Notes on new sources. Source 1 was read through an automated text extraction of a scanned notice; the totals reconcile (liabilities plus equity equal assets), but individual lines carry medium confidence. Source 2's intangibles figure equals book equity less the "adjusted capital" it prints (Gs. 2,117.7 bn − Gs. 1,216.7 bn). Source 7 was consulted for public-entity detail but its per-entity conversions are inconsistent and are not used. Searches for a published cashback total and for the exclusion balance returned nothing usable.

Machine-readable version: `analysis/mm_size.json`. Computation scripts: `analysis/mm_build/`.
