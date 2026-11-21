# Ueno Bank S.A.: review of the three "missing money" reports

**Status.** Sceptic's and editor's review by an AI financial reviewer, not a licensed professional. The result is analysis and labelled estimate, not a finding. All conduct is alleged; everyone named is presumed innocent. The prosecution record (Case 89/2026) is authoritative for what the prosecution alleges; Julio Rey's statements are his own claims. Cut-off: 20 November 2026.

**Reviewed.** `mm_size` (how much), `mm_uses` (where it went), `mm_recovery` (what can be recovered), their scripts, and `data/raw/*.jsonl` with editor corrections applied. Key numbers were re-derived from the raw rows in `scratch/mm_review/model.py`. Three source documents were re-opened. Gs. bn means thousand million guaraníes; USD figures use Gs. 6,500.

**Outputs.** `site/data/missing_money.json` (the public tab), `data/raw/mm.opinions.jsonl` (19 rows), `data/raw/mm.sources.jsonl` (1 row).

## 1. Result

| Item | Low | Central | High |
|---|---|---|---|
| **Headline: shortfall of assets against all liabilities** | USD 393 M | **USD 956 M** | USD 1,374 M |
| Questioned credit still owed to the bank | USD 594 M | **USD 879 M** | USD 946 M |
| Unexplained share of the questioned credit | 0 | USD 303 M (34%) | USD 636 M |

The headline measures one thing: what the bank's assets are plausibly worth, less everything it owes, on the balance sheet of 30 June 2026. Shareholders' book equity of USD 375 M is already gone before that number starts. It is the loss creditors bear as a group before the Deposit Guarantee Fund pays anything. It is not the amount taken, not the amount lent to related companies, and not any one depositor's loss. Confidence is low.

## 2. The seven disagreements

### 2.1 Balance-sheet base

`mm_size` used the bank's notice for 30 June 2026. `mm_recovery` said nothing existed after December 2025 and rolled forward to Gs. 24.3 trillion.

I opened the notice. It prints assets of Gs. 25,641.8 bn, liabilities of Gs. 23,205.2 bn and equity of Gs. 2,436.5 bn. The nine asset lines add up to the total to the guaraní, which a mis-read scan would not do. **The June 2026 base stands; the roll-forward is dropped.** The December 2025 total in the rating report (Gs. 21,095.5 bn) also checks, so assets grew by Gs. 4,546 bn in six months, not the Gs. 3,200 bn `mm_recovery` assumed.

Both models now run on the June lines. The trust and the REDISA and REDIPRO placements are December 2025 values; together they are Gs. 2,982 bn of the Gs. 3,067 bn June investments line, which fits.

### 2.2 Size of the questioned book

`mm_size` had USD 879 M (594 to 946). `mm_uses` had USD 915 M (620 to 990).

Re-derived from the rows:

| Component | USD M |
|---|---|
| Six record borrowers, record balances (USD 166.98 M + Gs. 395.5 bn) | 227.8 |
| Less nine loans sold to Vinanzas (principal USD 71.7 M) and three overdrafts paid down on 15 June 2026 | −108.8 |
| Six record borrowers, still on the bank's books | 119.0 |
| Twenty group-linked names on the unofficial list (Gs. 4,938.8 bn) | 759.8 |
| **Central** | **878.9** |

The USD 36 M gap between the analysts has two causes. First, `mm_uses` subtracted the June loans *granted* (USD 125.0 M). The correct deduction is the loans those funds *retired* (USD 108.8 M); the other USD 16 M bought group bonds and is new exposure. Second, `mm_uses` added La Tropa SAE (USD 33.9 M) and Infocenter (USD 18 M). **`mm_size`'s figure stands; `mm_uses`'s does not.**

Scope. In: the six record borrowers net of the June retirement, and the 20 list names. Out, and in the high case only: La Tropa SAE (an operating cattle firm with a bond programme; only USD 5.9 M of its debt is described as passed to the group), Infocenter (one article, undated, off the list), Dobrestec and TSV. Out altogether: Valores Casa de Bolsa and the social-security institute, which are on the list but are not group borrowers; the trust and the placements; unpaid interest.

Infocenter is the closest call: its USD 18 M plus Galadriel's USD 15.07 M equals the "USD 33 million" operation the supervisor is said to describe. I left it out to keep one rule: central means record or list.

### 2.3 Recovery on the questioned book

`mm_size` assumed losses of 28%, 60% and 90%. `mm_recovery` assumed recoveries of 3%, 10% and 25%.

Two bottom-up checks. By composition: 5% on the record borrowers and June shells, 10% on other conduit-type firms, 30% on group companies with real assets gives 12%. By obligor: group cash of about USD 106 M at June 2026, three ranches at USD 16 M, a shopping-centre stake worth USD 30 to 45 M net and a sale of ITTI at USD 15 to 65 M come to USD 165 to 230 M. That is shared with USD 341 M of other group debt and with workers, so 14% to 19% of the claims.

**Central: 20% recovery, 80% loss.** `mm_size`'s 40% recovery has no identified asset behind it. `mm_recovery`'s 10% is defensible but sits at the bottom of the range, and it was applied to a book size taken from Rey.

`mm_size`'s low case is kept as an amount, the supervisor's provisions deficit of Gs. 1,621.9 bn. Calling it "28% of the book" does not survive: the complaint, as relayed, puts related exposure at "more than USD 300 million", so the deficit is roughly 80% of what the supervisor had reviewed. The low case really says the rest of the list is sound.

Effect on the headline, all else equal: 60% loss gives USD 780 M; 80% gives USD 956 M; 90% gives USD 1,044 M.

### 2.4 The Central Bank's statements

I re-opened the local report of the 12 November statement. The Central Bank president spoke of "aproximadamente US$ 600 millones en activos sanos" identified so far: performing loans, bonds and other instruments, buildings excluded, evaluation still under way, and more than the debt to the pension system.

What reconciles:
- USD 600 M exceeds the institute's reported USD 517 M.
- "Assets suffice to cover deposits" (18 November) holds approximately in the low and central cases: 120% and 99% of an estimated Gs. 17.2 trillion. Deposits are known only to about 5%, so 99% is level.
- The same official gave an example of 80 of assets against 100 of liabilities with the fund making up the 20, so the Central Bank itself expects a gap in some packages.

What does not:
- USD 600 M cannot be the whole stock of sound assets. The June balance sheet shows USD 544 M of cash alone.
- No published number bridges USD 600 M to full cover of deposits (about USD 2.7 bn).
- Two foreign outlets reported USD 600 M as assets *exceeding* liabilities. That contradicts a capital ratio of 5.56% and the local wording. Not used.
- In the high case assets are 83% of deposits and the 18 November statement fails.

The analysts disagreed because `mm_recovery` discounted cash to 62% and ordinary loans to 72%. No source supports that. Cash is cash, and a run reduces deposits and assets equally. On those discounts the June base gives a shortfall of USD 1.9 bn, which no reading of the regulator can accommodate. **Those discounts are not kept.** I replaced them with 0%, 5% and 15% on ordinary loans, for the unseparated past-due portfolio of the 2024 merger and a buyer's discount, and 50% on sundry receivables in the high case only.

### 2.5 The headline

| Step (USD M at 6,500) | Low | Central | High |
|---|---|---|---|
| Assets at book, 30 June 2026 | 3,944.9 | 3,944.9 | 3,944.9 |
| Merger-expenses trust | −324.0 | −324.0 | −324.0 |
| Deferred charges and intangibles | −126.9 | −126.9 | −126.9 |
| REDISA and REDIPRO placements (loss 50 / 80 / 95%) | −67.4 | −107.9 | −128.1 |
| Questioned book (supervisor's deficit / 80% / 95%) | −249.5 | −703.1 | −898.9 |
| Rest of the loan book (0 / 5 / 15%) | 0 | −68.6 | −195.7 |
| Sundry receivables (0 / 0 / 50%) | 0 | 0 | −75.5 |
| Assets left | 3,177.1 | 2,614.4 | 2,195.8 |
| Liabilities at book | −3,570.0 | −3,570.0 | −3,570.0 |
| **Shortfall** | **−392.9** | **−955.6** | **−1,374.2** |

Against `mm_size`'s USD 738 M: +176 from the loss rate, +69 from the discount on ordinary loans, −27 from a lower loss on the placements.

**The fund-rank fork.** `mm_recovery`'s USD 630 M swing does not survive on the reviewed base. The fork matters only when assets fall short of deposits. Central: the fund loses about USD 84 M if it absorbs the gap, nothing if it is repaid first, and deposits above the guarantee recover 100% or 94%. High: USD 503 M or nothing, and 100% or 66%. Low: no difference; non-deposit creditors recover about 52%. With `mm_recovery`'s own discounts the swing would be about USD 770 M. The fork is real, but its size depends on the asset view.

### 2.6 The 0.5% uplift loans

Settled from `rec.loans`. Twelve principals divide by 1.005 into a round amount: rows 0006, 0007, 0008, 0009, 0012, 0013, 0014, 0017, 0018, 0019, 0031 and 0032. Ten pass a strict test (at least USD 50,000 or Gs. 1,000 million). The eleventh is Gs. 64,923 million (64,600 × 1.005). The twelfth is Gs. 91,334.4 million (90,880 × 1.005). Separately, three FRANEDE balances equal principal × 1.005 (rows 0025, 0027, 0028). **Twelve principals plus three balances, fifteen operations.** Ten, eleven and twelve were each a fair reading of the same pattern. Observed uplifts total USD 0.82 M, not USD 0.70 M.

### 2.7 Unit risks

- **Rating agency's cash-flow annex for the group.** Header: "miles de Gs". Gross interest of 251,239,287 for 2025 is Gs. 251.2 bn, about USD 39 M, as `mm_uses` stated. Net new debt of Gs. 261.9 bn and Gs. 33.8 bn gives USD 45 M. **No error.** The 2024 debt line (Gs. 13.4 trillion) belongs to a year when the bank was consolidated and is not comparable. Unused by the analyst: a "Dividendos" line of about Gs. 111 bn, negative, in 2025. I could not establish what it is; see "does not reconcile".
- **Bank rating report, December 2025.** Tables in "Gs mill"; total assets 21,095,542.0. Consistent with the data rows.
- **June 2026 notice.** In guaraníes; foots.
- **Debtor list.** Three entries (Galadriel, GSR, Berilo) match supervisor-attributed dollar loans only at about Gs. 5,880 per dollar. The list appears to have been drawn up at a lower rate than the 6,500 used here, so its dollar value is probably understated by up to 10%. This is a conversion issue, not a "millones" error.

## 3. Other tests

**Double counting.** (a) Six borrowers and June loans: fixed in 2.2. (b) In `mm_uses`, ITTI's selling expenses supported "sponsorship" while already inside ITTI's cost base under "operating costs". Sponsorship is cut from USD 35 M to 15 M. (c) Capitalised software sat under both "assets" and "operating costs"; assets cut from 50 to 30. (d) The trust and Rey's 900 may overlap; this cannot be resolved and is flagged. (e) The meanings of "missing" overlap by construction; the JSON marks each overlap and nothing sums them.

**Single unofficial source.** The undated list is 86% of the central book. Without it, using only the record and loan rows attributed to the supervisor, the book is USD 461 M and the central headline USD 642 M. In the list's favour: for five borrowers its figures agree with supervisor-attributed data within about 2%. Against it: one borrower has two figures in the same article, the social-security institute appears as a debtor, and two record borrowers that still owed over USD 40 M each are absent.

**Exchange rate.** Central headline: USD 1,014 M at 6,100; USD 956 M at 6,500; USD 942 M at 6,600. Rates printed in the sources for 2026 run from about 5,750 to 6,590.

**Circular reasoning.** `mm_recovery` used Rey's USD 900 M as the size of the book. `mm_size` and `mm_uses` cited closeness to 900 as support. `mm_uses` also took Rey's 300 + 300 split as the basis of its largest hypothesis and then pointed to the total matching Rey. In the reviewed model Rey's figure is neither input nor validation. The book runs from 594 to 946 depending on scope, so a match at 879 is weak evidence.

**Overconfidence.**
- "Operating costs, USD 440 M, medium confidence": cut to USD 350 M, low. The loans reached ITTI, REDISA and REDIPRO. What those companies spent the money on is in no source. The bank's own promotion rules say the bank credits the cashback. ITTI's billing measures what it charged, not what the questioned loans paid for.
- "Circular support, USD 65 M": cut to 45. The USD 20 M of certificates bought with cash is removed; Rey describes cash coming *in*, of unknown origin.
- "USD 291 M (39%) circulated": USD 4.3 M was counted for an instalment the record gives no amount for. Now USD 287 M, 38%.
- `mm_size`'s "the provisions deficit alone reproduces 5.56%" checks: equity Gs. 2,559 bn and risk-weighted assets Gs. 18,476 bn solve both ratios. The inference that the trust and placements are not in the official figure is reasonable but remains an inference.

After these cuts USD 303 M is unexplained. That is close to the third Rey says he could not break down; I do not treat the coincidence as evidence.

## 4. What stands

- `mm_size`: the June 2026 base, the capital arithmetic, the waterfall structure and the de-duplicated book of USD 879 M.
- `mm_uses`: large-scale circulation of traced money, the June 2026 loop, the 0.5% pattern and the list of what the evidence does not show.
- `mm_recovery`: the claims stack, the two readings of the fund's rank, the group as the real obligor, the tracing plan and the watch list.
- All three: seizures (about USD 17 M of reported value) are small and are not recovery for depositors.

## 5. Residual disagreements

1. **Loss rate on the questioned book.** 60% and 90% are both defensible; 80% is a judgement. Range on the headline: USD 780 M to 1,044 M.
2. **Forced-sale discounts on ordinary assets.** Excluded from the central range for lack of a source. A disorderly tender could move the result towards `mm_recovery`'s view.
3. **La Tropa SAE and Infocenter.** Including both adds about USD 50 M to the book and USD 40 M to the headline.
4. **The list.** USD 642 M without it, USD 956 M with it.
5. **Uses.** A constrained guess. The three largest items are the least documented and a third is unexplained.
6. **Deposits.** The total and its split drive the cover ratio and the fork, not the headline.

The Central Bank's exclusion balance, expected about 2 December, supersedes most of this.

## 6. Checks run

- **Waterfall footing:** start plus deductions equals the end value in each scenario; the subtotal equals the running total; the headline equals the end value with the sign reversed. Passed.
- **Uses:** hypothesis centrals (USD 576.0 M) plus unexplained (USD 302.9 M) equals the total (USD 878.9 M); shares sum to 100%. Passed.
- **Asset classes:** book value × central recovery sums to the central "assets left". Passed.
- **Refs:** 559 references in the JSON and the opinion rows checked against 1,889 row and source ids in `data/raw`. None missing.
- **Bilingual:** every `_en` field has an `_es` twin. Passed.
- **Meanings:** seven, overlaps marked, none summed.
- **Balance sheet:** asset lines sum to total assets.

## 7. Limits

- The three PDFs were read through an automated fetch-and-summarise tool, not by eye. The balance-sheet totals are corroborated by footing; the dividend line in the rating annex is not.
- I did not re-open the article carrying the debtor list or re-verify press rows beyond the editor's earlier sample.
- I did not run `data/build_graph.py`. The new `mm.opinions.jsonl` has a row kind the graph builder may not yet map.

## 8. Sources re-opened

The bank's June 2026 balance-sheet notice; the FIX SCR reports on the bank (December 2025) and on Grupo Vázquez (cash-flow annex); the InfoNegocios and Perfil reports of the Central Bank president's 12 November statement. URLs are in `sources_added` in the JSON.

Model and builders: `scratch/mm_review/` (`model.py`, `build_a.py`, `build_b.py`, `build_c.py`).
