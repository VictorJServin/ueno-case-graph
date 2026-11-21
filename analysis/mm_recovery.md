# Ueno Bank S.A.: what can be recovered, and how the money could be traced

**Role and status.** Analysis by an AI insolvency, asset-recovery and bank-resolution analyst, not a licensed professional. The figures are labelled estimates and scenarios, not predictions, valuations or legal advice. **Cut-off:** 20 November 2026. The exclusion balance had not been published.

**Ground rules.** Everything about wrongdoing is alleged; everyone named is presumed innocent. The prosecution record (Case 89/2026) is authoritative for what the prosecution alleges (pp. 1-19) and for what Julio Rey told prosecutors (pp. 19-24); Rey's statements are his own claims. Ids in backticks refer to `data/raw`.

**Currency.** Arithmetic is in guaraníes (Gs. bn = thousand million). USD equivalents use **Gs. 6,500 per USD**, the rate implied by the record (p. 7: Gs. 253,000,000,000 against USD 38,923,077; `src:acta-p07`). Press figures printed in USD use rates between about 5,570 and 6,360, so USD totals are indicative to roughly ±10%.

**Bottom line.** On published numbers, assets alone do not cover all deposits in any of my three scenarios; assets plus the guarantee fund do so only in the high one, and only in aggregate (my waterfall still gives uninsured depositors 94% there, because late recoveries go back to the fund). The central case realises about Gs. 10.1 trillion (USD 1.5 bn), 41% of book assets. Who bears the gap is a legal and policy choice that matters more than the asset uncertainty: if the fund absorbs it, uninsured depositors recover about 71% and the fund loses about USD 630 M; if the fund is repaid first, the fund loses nothing and uninsured depositors recover about 20%. Bondholders recover little or nothing either way.

---

## 1. The claims stack

Order as I read Ley 2334/03 arts. 16-20 and 26 (BACN text). The law ranks the "exclusion balance" (what is transferred to other banks) and sends everything else to a "residual balance" liquidated by a court under bankruptcy rules.

| Rank | Creditor | Amount known | Basis and caveats |
|---|---|---|---|
| 1 | Guaranteed private deposits (up to 75 minimum wages, Gs. 228.3 M each); now largely the **guarantee fund's subrogated claim** | USD 740 M to 928 M as printed; Gs. 3.9 trillion already advanced to 1,812,348 people | Art. 20, first sub-order; art. 18 c gives the fund first rank in liquidation when it pays directly. Related parties' deposits are excluded (art. 1 f). `chrono:event:0166`, `0179`, `0181` |
| 1 | **Public social-security deposits** (IPS, Caja Fiscal, other funds) | IPS USD 348.5 M (30 Sep) to USD 517 M (IPS, Nov; includes Gs. 250 bn of bonds); Caja Fiscal Gs. 250 bn | Same sub-order. That the full balance ranks here is my reading. `press:fact:0106`, `chrono:event:0198`, `0119` |
| 2 | Cash mandates, tax collections, withholdings | Not published | First order, second sub-order |
| 3 | Guaranteed slice of other public entities | Negligible (Gs. 228.3 M per entity) | First order, third sub-order |
| 4 | BCP: credit claims, then non-credit claims and taxes | About USD 70 M of reserve requirement, if it qualifies | Second and third orders; enter the exclusion balance only with securitisation. `chrono:event:0067`, `0084` |
| 5 | Employees not transferred | About 490 to 500 staff; amount unknown | First on the residual balance (art. 26); directors and senior managers excluded (art. 17) |
| 6 | **Private deposits above the guarantee** | About USD 1.0 bn to 1.25 bn (computed) | Rank not stated expressly. Art. 20 lets the BCP raise the transferred amount per depositor in equal steps if assets allow; the rest is an ordinary claim on the residual |
| 6 | **Other public entities above the guarantee** (Itaipú, ANDE, Petropar, Conatel, municipalities) | About USD 330 M to 500 M (computed from the Ministry of Economy's USD 888 M total) | Same rank on my reading. Itaipú reported at USD 182 M. `chrono:event:0052` |
| 7 | Senior noteholders (USD 350 M, 6.70%, 2031, New York law) | USD 350 M; quoted near 5 cents | Unsecured, residual balance only. `press:fact:0298`, `chrono:event:0200` |
| 7 | Local financial and subordinated bonds | Gs. 668.5 bn (about USD 103 M) | Subordinated part ranks lower; split not published. `press:fact:0260` |
| 7 | IDB Invest, Triodos, GAWA; other liabilities | About USD 40 M known; up to Gs. 2,479 bn of other liabilities of unknown rank | `chrono:event:0020`, `0048` |
| 8 | Shareholders | Book equity Gs. 2,117.7 bn | Rights suspended; nil |

Two officials have described the fund's position differently. Its director said it ranks first and hoped acquirers would pay it something (InfoNegocios, 11 Nov). The BCP president said the fund can complete the gap between healthy assets and liabilities in the packages, and that healthy assets exceed the debt to the pension system (InfoNegocios, 13 Nov). Both readings have a footing in art. 18; section 4 runs both.

---

## 2. The asset side by recoverability

Book values are from the December 2025 balance sheet in the rating report (`press:fact:0246`-`0266`), the latest available. I roll it forward by assuming about Gs. 3,200 bn of 2026 growth (the USD 350 M notes plus deposit and equity growth) went into loans, which gives a book of about Gs. 24.3 trillion against liabilities of about Gs. 22.2 trillion. Note on classification: the merger trust is 66.04% of "other investments" (`press:fact:0265`), so the trust and the REDISA/REDIPRO placements sit inside that line.

| Class | Book (Gs. bn) | USD M | Low / central / high | Reasoning |
|---|---|---|---|---|
| Cash, BCP reserves, securities, premises, unallocated (computed residual) | 4,487 | 690 | 40 / 62 / 85% | Composition unpublished. Liquidity drained before the resolution: about USD 70 M of reserve requirement not replenished, repo failures at the group broker (`chrono:event:0067`, `0113`). Securities may include group paper |
| Unquestioned loan book (assumption) | 8,462 | 1,302 | 55 / 72 / 85% | Transfers go at book net of provisions; acquirers pick first. Past-due loans under the 2024 merger facility were not separated in the accounts (`chrono:event:0026`); the reported 0.44% non-performing ratio is no guide. The BCP's first-pass USD 600 M of "healthy assets" is about 46% of this class: my floor |
| **Questioned book** (loans to group-dependent borrowers) | 5,850 | 900 | 3 / 10 / 25% | Size is Rey's claim (`rec:flow:0075`); cross-checks in §3. All sole signature; recoverable only from the group |
| Merger-expenses trust | 2,106 | 324 | 0 / 0 / 2% | Spent money booked as an asset, 99.4% of book equity. Only clawback of non-permitted invoices (about USD 20 M per a BCP memo, `press:event:0026`) |
| Other assets incl. deferred losses, intangibles | 2,514 | 387 | 5 / 15 / 30% | Deferred losses are worth nothing; the rest includes software and property that, per Rey, related companies sold to the bank (`rec:flow:0074`) |
| Placements in REDISA and REDIPRO; REDISA stake | 877 | 135 | 5 / 20 / 45% | Real payment businesses, but bank-funded, frozen and named as conduits in the record; value only in a quick going-concern sale |
| Claims on directors, shareholders, beneficial owner | 2,055 claimed | 316 | 0 / 1 / 5% | The embargo figure is the claim, not assets found (`chrono:event:0084`). The holding companies' main asset is the bank |
| Seized and frozen assets | 113 reported | 17 | 0 / 25 / 60% | Three ranches USD 15.95 M, nine vehicles USD 1.4 M; aircraft, yacht, 2,331 properties and frozen accounts unvalued (`press:fact:0063`-`0065`, `0080`). Managed by Senabico; passes to the State only on forfeiture |
| Real estate in the bank's name | n/a | n/a | 50 / 70 / 90% of appraisal | 47 properties identified (`chrono:event:0085`); already inside the first row, not added |
| Group-owned businesses; insurers (D&O), auditors | n/a | n/a | not added | Group units are reachable only through the questioned book; no D&O policy reported; audit opinion of February 2026 was clean |
| Assets abroad | n/a | n/a | not estimated | "Several countries" confirmed assets per prosecutors; no asset, value or freeze confirmed (`chrono:event:0196`) |

**Totals realised:** low Gs. 6,794 bn (USD 1,045 M, 28% of book); central Gs. 10,061 bn (USD 1,548 M, 41%); high Gs. 13,830 bn (USD 2,128 M, 57%).

**How this squares with the BCP.** The BCP put healthy assets at about USD 600 M on 12 November and said on 18 November that assets suffice for 100% of deposits (`chrono:event:0187`, `0226`). Paying all deposits plus costs needs about Gs. 16.8 trillion, 69% of book. I reach about Gs. 16.2 trillion (98% of deposits) only if the bad book is limited to the supervisor's provisions deficit of Gs. 1,622 bn and everything else realises at 85 to 90%. The exclusion balance will settle it: is the hole Gs. 1.6 trillion or closer to Rey's Gs. 5.9 trillion?

---

## 3. The group as the real obligor

The record alleges that loan proceeds went at once to ITTI, REDISA, REDIPRO, Vinanzas and Grupo Vázquez and that repayments came from them (`rec:flow:0001`-`0040`). If so, the debtor that matters is the group.

| Entity | Reported position | What it can pay (opinion) |
|---|---|---|
| **ITTI** | 2025: revenue Gs. 1,826 bn, EBITDA Gs. 419 bn, equity Gs. 460 bn; 59% of revenue from the bank and related parties; Gs. 341 bn of intercompany receivables. June 2026: debt USD 66 M (USD 40 M bonds), cash about USD 35 M. Cut to Cpy; frozen since 6 Nov; Argentine arm suspended about 900 staff without pay (`press:fact:0179`-`0199`, `0308`-`0312`, `chrono:event:0123`) | Illustration: non-related revenue at the 2025 margin gives EBITDA near Gs. 170 bn; at 3 to 5 times, Gs. 0.5 to 0.9 trillion before its own debt and labour claims. A small fraction of what is traced to it, and only if the core-banking unit keeps its clients |
| **Grupo Vázquez (holding)** | Assets Gs. 4,579 bn, of which the stake in the bank's parent is Gs. 3,083 bn; equity about minus Gs. 980 bn once that is written off. Group debt outside the bank USD 341 M (USD 204 M bonds), cash about USD 71 M, USD 54 M short term; interest due from 19 Nov; Cpy (`press:fact:0134`-`0158`, `0302`-`0305`) | Sale value of non-bank units, shared with its own bondholders. I do not expect the holding to survive as a going concern |
| **REDISA / REDIPRO** | Bank placements Gs. 236 bn and Gs. 640 bn; no public accounts; frozen | Only through a going-concern sale |
| **Vinanzas** | USD 93,828 the day before buying USD 74.4 M of loans (`rec:event:0064`); assets are those loans | Nil. A simulation ruling returns the loans to the bank; it creates no value |
| **Terravaz** | Shopping-centre trust appraised at Gs. 498 bn (quick sale Gs. 398 bn); liabilities Gs. 205 bn (`press:fact:0233`, `0243`) | About USD 30 to 45 M net, after its own creditors |

Kasas, Model, Technoma and the Luxembourg holding are covered in the JSON.

**Survival.** The bank funded the group and the group's value was the bank; that loop is broken on both sides. With accounts frozen, ratings at Cpy and coupons falling due, the realistic question is which units can be sold whole. The Executive's bill for a temporary administrator of up to eight months, deciding company by company between sale and bankruptcy (ABC, 19 Nov), frames it that way. Whether the 19 November coupons were paid is not reported.

**Ranking against the bank.** The bank's loans to group companies are unsecured, so the estate ranks with the group's bondholders (about USD 244 M across the holding and ITTI), banks and suppliers, and behind roughly 6,000 to 7,000 workers. Two things can change that: a finding of simulation (Civil Code arts. 305-310), which lets earlier creditors of the simulating seller rank ahead of the apparent buyer's unsecured creditors, and criminal forfeiture, which takes assets for the State ahead of all. About USD 26.8 M of June 2026 bank loans financed purchases of group bonds (`rec:loan:0038`-`0040`), a point both sets of creditors will argue.

**Why 10% on the questioned book.** Hard assets with a published value total under USD 65 M; a saleable ITTI might add USD 15 to 65 M net of its debt. Against USD 900 M of questioned loans and USD 341 M of competing group debt, a central USD 90 M already assumes the payment companies and ITTI are sold in working order.

---

## 4. Recovery scenarios (not predictions)

**Liabilities assumed (Gs. bn).** Deposits 16,500 (between the December 2025 book of 15,831 and the mid-2026 level implied by Bloomberg's "Gs. 5 trillion public = 29%"): guaranteed private 5,000 (30% of value, Moody's; `chrono:event:0138`), social security 2,600, uninsured private 6,500, other public 2,400. Other unsecured 5,686 (notes 2,275; local bonds 669; lenders 264; other 2,479). Costs and labour: 300.

**Waterfall.** Transferable assets (first two classes) pay deposits; residual assets (everything else, net of costs) go to the court liquidation.
- **Fund absorbs** (the BCP president's description): transferable assets go to pension deposits, then to other deposits; the fund recovers only from the residual.
- **Fund first** (the fund director's reading): the fund shares the transferable assets with pension deposits; other deposits get what is left; unpaid deposits and bondholders share the residual equally.

| | Low | Central | High |
|---|---|---|---|
| Transferable assets realised | 6,449 | 8,875 | 11,007 |
| Residual assets realised (gross) | 345 | 1,186 | 2,824 |
| **Total realised** | **6,794 (USD 1,045 M)** | **10,061 (USD 1,548 M)** | **13,830 (USD 2,128 M)** |
| *Fund absorbs:* cost to the fund | 4,955 (USD 762 M) | 4,114 (USD 633 M) | 2,476 (USD 381 M) |
| Pension deposits | 100% | 100% | 100% |
| Uninsured private and other public deposits | 43% | 71% | 94% |
| Bank bondholders | 0% | 0% | 0% |
| *Fund first:* cost to the fund | 728 (USD 112 M) | 0 | 0 |
| Pension deposits | 85% | 100% | 100% |
| Uninsured private and other public deposits | 0% | 20% | 52% |
| Bank bondholders | 0% | 7% | 23% |

Central arithmetic, fund absorbs: 8,875 less 2,600 for pension deposits leaves 6,275 for 8,900 of other deposits (71%); residual 1,186 less 300 of costs gives 886 to the fund against its 5,000 outlay, a net cost of 4,114. Fund first: 8,875 less 7,600 leaves 1,275 for other deposits; the residual 886 is shared over 7,625 of unpaid deposits and 5,686 of other creditors (6.7% each), so other deposits get (1,275 + 508) / 8,900 = 20%.

**Reading.** (1) Small savers are paid in every case. (2) Pension deposits are covered in five of six cells. (3) The press range for the fund (USD 740 M to 928 M) is its gross outlay; the net cost depends on which reading prevails, and the fund holds about USD 1.6 bn (`chrono:event:0138`). (4) Other public entities, companies and holders of large certificates are the swing creditors: 20% or 71% in the central case. (5) The notes' price near 5 cents matches the fund-first central case. (6) Amounts are nominal and undiscounted; transfers take weeks, the residual takes years.

**What drives the range.** The size of the questioned book (each Gs. 1 trillion moved to the unquestioned book adds about Gs. 620 bn), the realisation rate on unquestioned loans (each 10 points is Gs. 846 bn) and the true liquidity at 2 November.

---

## 5. Tracing plan

Rey's account, if accurate, is that most of the money was spent earlier on technology, cashback and operating costs and then carried as loans (`rec:flow:0074`, `0075`). Tracing has two aims: to size the part that was consumed, and to find the part that still sits in assets, accounts or third parties.

| # | Record | Held by | Would show | Tool | Time |
|---|---|---|---|---|---|
| 1 | Loan-by-loan schedule of the questioned book, with first outward transfer | Bank core system (intervention team); ITTI as operator | True size of the hole and each first recipient | Intervention powers, arts. 15 and 17 | Weeks |
| 2 | Account statements by entity: ITTI, Grupo Vázquez, REDISA, REDIPRO, Vinanzas (eight accounts), Kasas, Model, borrowers | The bank; other banks for outside accounts | Where the money stopped: costs, bond service, property, cash, abroad; the USD 1.64 M and USD 1.0 M gaps of 15 June 2026 | No bank secrecy against prosecutors or BCP (Ley 861/96 art. 86) | 1 to 6 months |
| 3 | SIPAP transfer logs with time stamps | BCP | Order of same-day credits and debits; destination banks | Prosecutor's request | Days to weeks |
| 4 | Broker trade tickets and depository records for group bonds | Ueno Casa de Bolsa (raided), exchange, Cavapy | New issue or resale, price, final holder; bank-financed demand | Securities regulator; seizure made | Weeks |
| 5 | Board and credit-committee minutes; de-listing correspondence | Bank; Superintendency | Who voted and who dissented: basis of each director's joint liability | Liquidator's action (art. 138 a) | Weeks; judgment 3 to 8 years |
| 6 | Certificate-of-deposit register and endorsements | Bank treasury; schedules filed by Rey's defence | Funding of group-held certificates; related holders claiming the guarantee | Exclusion under art. 1 f; simulation | Weeks |
| 7 | Vault logs, count sheets, video; cash-carrier records | Bank treasury; cash-handling firm raided 17 Nov | Whether about USD 17 M and Gs. 17 bn in cash came in, and how it was booked | Seizure; cash-transaction reports | Weeks |
| 8 | The three consecutive receipts Rey filed; the issuer's receipt book | Prosecution file; the issuing company; the three firms named | Whether written-off debtors really paid | Witness statements; laundering forfeiture (art. 196) | 1 to 2 months to test |
| 9 | "Delirio Colectivo" email and 20-page attachment (13 Oct 2025) | Prosecution file; mail server | Insider map of real liquidity channels, and who knew | Forensic authentication | Weeks |
| 10 | Intercompany ledgers of ITTI and Grupo Vázquez | Seized servers; auditors; rating agencies | How inflows were booked and spent; collectability of ITTI's Gs. 341 bn receivables | Seizure; temporary administrator | 2 to 6 months |
| 11 | Trust ledger and supplier invoices | Trustee bank; BCP file | Payments to group suppliers outside the authorised facility | Nullity, unjust enrichment | 1 to 3 months |
| 12 | Property, vehicle, aircraft, vessel and livestock registries | Registries; Senabico | Values and liens; transfers after June 2026 | Inhibition in force; simulation; early sale (Law 5876/17) | Appraisal 1 to 3 months; sales 1 to 3 years |
| 13 | Foreign bank and registry records; crypto wallets | Luxembourg, Argentina, United States, others | Whether and how much left the country | Mutual legal assistance; informal freezes | Freeze weeks to months; evidence 6 to 18 months; return after final judgment |

**Legal tools and their limits.** *Embargo and inhibition* are in place against 17 companies and the charged persons (`chrono:event:0110`, `0135`); Grupo Vázquez S.A.E. has asked for them to be lifted (`chrono:event:0211`). *Simulation actions* have free proof for third parties (art. 310) and fit the June 2026 portfolio sale and the share transfers that preceded first loans. *Forfeiture* needs a conviction; laundering was added on appeal and is under challenge (`chrono:event:0160`, `0170`). *Director liability* is joint and unlimited in principle (Civil Code arts. 1111-1115, commentary only). Senabico can sell depreciating assets early but must return asset or price with interest on acquittal, so seizure is not recovery.

**Time frames from precedent** (details and links in the JSON).

| Case | Outcome |
|---|---|
| Ára S.A. de Finanzas, 2015 | About 2,600 savers and Gs. 310 bn moved to three institutions in five weeks; sanctions against directors still pending in 2022 |
| Paraguay 1995-2003 | Recoveries described in 2015 as very low; BNT convictions confirmed in 2010; BPO prosecution time-barred in 2007 |
| Baninter, Dominican Republic, 2003 | 21.7% of central-bank outlays recovered in 20 years; civil award against the main owner unpaid |

By 2017 fewer than three resolutions under this law had been completed, none of a bank this size. The pattern: good assets and small deposits move fast; the related book returns little and slowly. The JSON lists two further records (tax filings, home-banking logs).

---

## 6. Early-warning indicators

| Date | Watch | Why it matters |
|---|---|---|
| From 19 Nov 2026 | Grupo Vázquez coupon payments (status unknown) | A default accelerates USD 204 M of bonds against the same assets |
| 30 Nov | End of the penalty-interest waiver; target date for transfers | December collections are the first test of the retail book |
| About 2 Dec | Extended guarantee deadline; exclusion balance | Assets included, provisions on the questioned book, treatment of deposits above the guarantee |
| December | Tender of lots | Bidders, share of deposits taken, and whether the fund tops up or is repaid |
| 4 Dec | End of the Kaitel suspension | Whether ITTI is kept alive for sale |
| December | Temporary-administration bill; ruling on lifting the inhibition | Who controls the obligor's assets |
| December | Supreme Court on the added laundering charge | Scope of forfeiture |
| 4 May 2027 | End of the six-month preparatory stage | Indictment or extension |
| 2027 | ITTI bond service of about USD 10 M; holding principal of USD 4.3 M | Second test of group solvency |

---

## Opinions

1. **Opinion: the hole is in the questioned book and the capitalised expenses, and most of it is not recoverable from anyone.** About Gs. 10.5 trillion of the Gs. 24.3 trillion book (questioned loans, trust, other assets) returns under 10% in the central case. Basis: `press:fact:0265`, `0266`; `rec:flow:0075`.
2. **Opinion: the BCP's "assets cover 100% of deposits" holds only if the bad book is the supervisor's Gs. 1.6 trillion and nothing else, or if "assets" includes the guarantee fund.** Basis: §2 test; `chrono:event:0070`, `0226`.
3. **Opinion: the split between the fund and uninsured depositors is the largest open variable**, worth about USD 630 M in the central case. Basis: §4.
4. **Opinion: the group can return perhaps a tenth of what is traced to it, and only through quick going-concern sales.** Basis: §3; `press:fact:0191`, `0138`, `0156`, `0302`.
5. **Opinion: bondholders of the bank should expect single-digit recoveries at best; holders of group bonds compete with the bank's estate and the State for the same thin assets.** Basis: §4; `chrono:event:0200`, `0087`.
6. **Opinion: seizures so far are small beside the loss** (reported values near USD 17 M) and do not flow to depositors automatically. Basis: `press:fact:0063`-`0065`.

## What would change my view

- The exclusion balance and a loan-by-loan schedule supporting or refuting Rey's USD 900 M.
- The bank's 2 November liquidity position and securities list.
- Accounts of REDISA, REDIPRO, Vinanzas, Kasas, Model and Technoma; a valuation of ITTI's core-banking business.
- A BCP ruling on the fund's rank and on deposits above the guarantee; the Ley 861/96 articles on depositor preference, which I did not retrieve.
- Any confirmed foreign freeze with a value.

Machine-readable version: `analysis/mm_recovery.json`. Model: `scratch/mm_recovery/model.py`.
