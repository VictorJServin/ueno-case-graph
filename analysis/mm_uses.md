# Ueno Bank S.A. (Case 89/2026): where the questioned money went

**Status.** Analysis and labelled hypothesis by an AI forensic accountant and corporate-finance analyst, not a licensed professional. Nothing here is a finding. All conduct is alleged and everyone named is presumed innocent. The prosecution record (`rec.*`, pp. 1-19) is authoritative for what the prosecution alleges; pp. 19-24 are Julio Rey's own claims. Press rows mostly relay the bank supervisor. Guaraníes are converted at G. 6,500 per USD, so converted totals are good to about ±5%. Corrections in `edit.corrections.jsonl` are applied. Companion file: `mm_uses.json`.

## 1. Answer in brief

- **Amount to explain: about USD 915 million** of questioned credit outstanding (range 620 to 990). My own computation lands within 2% of Rey's "about USD 900 million" (`rec:flow:0075`), which I did not use as an input.
- **Central allocation:** operating costs of the digital-bank model booked outside the bank 48%; servicing the group's debt including interest on the questioned loans 15%; circular support of the bank's own capital and income 7%; assets 5.5%; sponsorship and marketing 4%; abroad, fees and cash together under 2%. **Unexplained: USD 170 million, 19%.**
- **Most of the traced money did not go anywhere new.** Of USD 749 million of disbursements that carry an amount, USD 291 million (39%) came back to the bank as principal repayments or as the price of the June 2026 portfolio sale. That money circulated; it is not missing.
- **The loans look like a second layer.** Where a use is stated it is nearly always "to cover overdrafts" of ITTI, REDISA or REDIPRO (`press:flow:0121`, `0122`, `0098`). The loans to shells replaced earlier direct borrowing by the group's service companies. What those first overdrafts paid for is not in any source, and that is the real question.
- **The allocation is a constrained guess.** Only H3 and H8 rest mainly on arithmetic over record rows. H1 rests on Rey plus rating-agency scale checks. H4 to H7 rest on a handful of press figures.

## 2. The total being explained

| Component | USD million | Basis | Rows |
|---|---|---|---|
| Six record borrowers, outstanding before the June 2026 sale (USD 166.98 M + G. 395.5 bn) | 227.8 | Record loan tables; ties to the supervisor's USD figure | `rec:loan:0001`-`0035`; `press:fact:0103` |
| Unofficial debtor list, 20 group-linked names (G. 4,938.8 bn), excluding the social-security institute and an outside broker | 759.8 | Press, undated, medium reliability | `press:fact:0001`-`0021` |
| Less loans of 11-15 June 2026 that refinanced the six (USD 81.841 M + G. 280.5 bn) | -125.0 | They are on the list and replaced the sold loans and overdrafts | `rec:loan:0036`-`0040`; `press:loan:0002`, `0004`, `0007`, `0008` |
| La Tropa SAE (capital owed, prospectus) | 33.9 | Not on the list | `press:fact:0055` |
| Infocenter (low confidence) | 18.0 | One article | `press:loan:0047` |
| **Questioned stock, de-duplicated** | **914.6** | Used as 915 | |

Sensitivity: USD 620 million if only the six, the June companies and the regulator's described cases (Nubicom, GSR, Office Design, Berilo, Galadriel, Nuevo Mundo) are counted; USD 990 million with no de-duplication.

Stock and flow are different things. The six borrowers were granted USD 354.8 million and owed USD 227.8 million; USD 127.2 million (36%) had been cancelled, in each case, as alleged, with money from group companies (`rec:flow:0009`, `0024`, `0031`, `0034`). The allocation below explains the **stock**: net cash that left the bank and did not come back.

Two bank-side items sit outside the 915 and may overlap with Rey's figure: the merger-expenses trust of G. 2,105.7 bn, about USD 324 million (`press:fact:0265`), and placements in REDISA and REDIPRO of G. 876.6 bn, about USD 135 million (`press:fact:0126`).

## 3. Sources and uses of the group outside the bank, 2024 to mid-2026

This is not a closed cash-flow statement. No accounts exist for REDISA, REDIPRO, Vinanzas or any shell. It lines up the figures that can be sized.

| Side | Item | USD M | Period | Kind | Source |
|---|---|---|---|---|---|
| Source | Questioned credit outstanding | 915 | 2025-26 | computed | section 2 |
| Source | Bank funds placed in REDISA and REDIPRO | 135 | Dec 2025 | reported | `press:fact:0126` |
| Source | Merger trust (share paid to group suppliers unknown) | 324 | 2024-25 | reported | `press:fact:0265`; `chrono:event:0044` |
| Source | OTP equity into U Holdings | 47 | Dec 2025, Jun 2026 | reported | `chrono:event:0036` |
| Source | Net new group debt outside the bank | 45 | 2025, Q1 2026 | reported | FIX annex [N1] |
| Source | ITTI revenue from outside clients (41%) | 115 | 2025 | computed | `press:fact:0179`, `0299` |
| Source | Cash Rey says was brought into the bank; origin unknown | 20 | 2025 | Rey | `rec:flow:0071`, `0072` |
| Use | ITTI cost base (G. 710 bn in 2024; G. 1,511 bn in 2025) | 342 | 2024-25 | reported | Solventa [N2] |
| Use | of which billed to related parties in 2025 | 168 | 2025 | reported | `press:fact:0299` |
| Use | ITTI intangibles and fixed assets, increase | 40 | 2025 | reported | [N2] |
| Use | Group gross interest outside the bank | 67 | 2024 to Q1 2026 | reported | [N1] |
| Use | Short-term maturities, Grupo Vázquez 54 and ITTI 22 | 76 | Jun 2026 | reported | `press:fact:0305`, `0312` |
| Use | ITTI bank debt reduced | 22 | 2025 | computed | `press:fact:0194`, `0195` |
| Use | Capital paid into the bank (77 committed) | 50 | 2025 | reported | [N1] |
| Use | Returns to the bank, 11-15 June 2026 | 116 | Jun 2026 | computed | `rec:flow:0061`, `0055`; `press:loan:0029`, `0030` |
| Use | Six borrowers' loans cancelled | 127 | 2025-26 | computed | `rec:loan:0003`, `0005`, `0007`, `0021`, `0023`-`0026`, `0030`-`0033` |
| Use | Cover of 72-hour cheques, ITTI to Red Digital | 51 | Jul 2026 | reported | `press:flow:0092` |
| Use | Interest accrued on the six, to 2 Nov 2026 | 23 | 2025-26 | assumption | `rec:loan:0001`-`0035` |
| Use | Property payments | 9 to 16 | Apr 2024 to Aug 2026 | reported | `press:fact:0076`, `0077` |
| Use | Transfers abroad with an amount | 5.8 | Jun 2026 | reported | `press:flow:0090`, `0135` |
| Use | Football-association contract | 12 | 2023-27 | reported | [N7] |
| Use | 0.5% uplift on record loans | 0.7 | 2025-26 | computed | `rec:issue:0007` |
| Use | Cash prepared at the bank for the group | 0.7 | Jan, Oct 2026 | reported | `press:flow:0140`-`0146` |

Three readings.

1. **Scale fits.** ITTI alone cost about USD 342 million to run in 2024-25 and billed related parties USD 168 million in 2025. Extending 59% of revenue to 2024 and half of 2026 gives roughly USD 350 million of related-party billing (my extrapolation). Rey's "about USD 300 million technology and other" is in range.
2. **The holding could not pay its own way.** It received G. 12.1 bn of dividends in 2025 against group interest of about G. 251 bn and a commitment to put USD 77 million into the bank (`press:fact:0158`, [N1]).
3. **The bank funded the group through three doors**: the questioned loans, the trust, and the placements. Together about USD 1.37 billion, against bank equity of USD 326 million at December 2025 (`press:fact:0254`).

## 4. Hypotheses

### H1. Operating burn booked outside the bank: USD 440 million central (250 to 600). Confidence medium. Money spent.

**For.**
- Rey: technology, product and cashback costs were deferred through asset sales and then moved into loans; about 300 cashback and 300 technology and other (`rec:flow:0074`, `0075`; `src:acta-p22`). He describes ITTI doing technology, REDISA (Wepa) running the former Visión branches, and REDIPRO (Upay) doing card acquiring (`src:acta-p20`).
- Prosecution: all six borrowers forwarded proceeds at once to ITTI, REDISA, REDIPRO, Vinanzas or Grupo Vázquez (`rec:flow:0001`-`0040`). Of first hops with an amount, 92% of dollars and 100% of guaraníes reached those five (`analysis/fin_flows.md`).
- ITTI's selling and administrative expenses rose from G. 217 bn to G. 874 bn in one year, about USD 101 million more [N2].
- Nubicom, with G. 200,000 of paid-in capital, paid ITTI G. 415 bn under a services contract one day after a G. 417 bn loan; that is 23% of ITTI's 2025 revenue (`press:flow:0091`; `press:loan:0045`; `press:fact:0097`).
- Mowi's funds went to REDIPRO labelled as a Upay credit (`press:flow:0123`); REDISA and REDIPRO paid G. 227.9 bn to Hendy and Mowi booked as "service refunds" (`press:flow:0055`-`0058`).
- Grupo M's proceeds reached Kaitel (`rec:flow:0016`), whose Argentine branch had 800 to 900 developers working for the bank, half their pay sent by ITTI from Paraguay [N6].

**Against.**
- The bank's own promotion rules say the bank credits the cashback to the customer [N4]. No source shows it re-invoiced to a group company. The cashback half is Rey's word alone.
- ITTI reported a profit of G. 170 bn in 2025 (`press:fact:0185`). The money may have been ITTI's revenue and margin, not a pass-through of costs.
- The trust may already hold some of the same costs; ITTI and Ueno Holding were among its suppliers (`chrono:event:0044`).
- Amounts exist for 16% of the six borrowers' dollar principal.

**Confirm or refute.** Ledgers and statements of ITTI, REDISA and REDIPRO matched to payroll, suppliers and merchant settlement; the bank's cashback ledger; the "Delirio Colectivo" attachment (`rec:event:0056`).

### H2. Servicing the group's own debt: USD 140 million central (70 to 220). Confidence medium. External part spent; own-loan interest circulated to the bank.

| Part | Central | Basis |
|---|---|---|
| Coupons, maturities, bank debt and cheques at other banks | 75 | Group interest about USD 39 M in 2025 and USD 10 M in Q1 2026 [N1]; maturities (`press:fact:0305`, `0312`, `0169`); ITTI bank debt down G. 140 bn |
| Interest on the questioned loans, paid with new loans or capitalised | 65 | USD 23 M accrued on the six at contract rates (weighted 12.6%); second ring at an assumed 9 to 10% for about half a year |

**For.**
- USD 26.8 million of the June 2026 loans bought bonds of ITTI, Grupo Vázquez, Kasas and Model through the group's broker (`rec:flow:0048`-`0053`; `press:fact:0062`).
- A cattle company's bond programme earmarked USD 13.6 million for obligations at the bank (`press:fact:0059`).
- ITTI passed G. 329.5 bn to Red Digital to cover 72-hour cheques (`press:flow:0092`); AIME funds ended in cheques at another bank (`press:flow:0029`); Vinanzas was fed with such cheques (`rec:flow:0026`-`0028`).
- No interest or instalment is shown paid from a borrower's revenue; the one recorded instalment came from ITTI (`rec:flow:0020`). Guaraní overdrafts at 24.15% have no schedule (`rec:loan:0006`, `0010`, `0022`).
- Franede's USD 10,593,000 loan equals its cancelled USD 10 million plus 5.93%, about 270 days at 8% (`rec:loan:0023`, `0027`).

**Against.** Group debt outside the bank grew, so part of the service was refinanced in the market. No loan is traced to a specific coupon. Cheque cover overlaps with H3.

**Confirm or refute.** Paying-agent records per coupon and maturity; the bank's interest-income ledger with the paying account; cheque clearing data.

### H3. Circular support of the bank's own numbers: USD 65 million of the stock (25 to 135); USD 291 million of gross traced flows. Confidence medium. Circulated.

**Gross circulation (computed).**

| Return to the bank | USD M | Rows |
|---|---|---|
| Six borrowers' loans cancelled, by group funds as alleged | 127.2 | `rec:loan:0003`, `0005`, `0007`, `0021`, `0023`, `0024`, `0026`, `0030`-`0033` |
| 15 June 2026 sale price | 74.4 | `rec:flow:0061` |
| Hendy and Mowi overdrafts (G. 227.9 bn) and Grupo M overdraft, June 2026 | 41.4 | `press:loan:0029`, `0030`; `rec:flow:0055` |
| Nubicom repayment of 31 July 2026 (G. 285.6 bn) | 43.9 | `press:flow:0093` |
| Grupo M instalment paid by ITTI | 4.3 | `rec:flow:0020` |
| **Returned** | **291.3** | |
| Amount-traced disbursements | 749.4 | six 354.8; June 125.0; second ring 269.6 |
| **Share that circulated** | **39%** | a floor: most repayment legs carry no amount |

On 11 and 15 June the bank lent about USD 125 million and got back about USD 116 million, 93% (`rec:flow:0041`-`0047`; `rec:event:0064`).

**Inside the stock**, only returns that were not repayments of questioned loans count:

| Item | Central | Basis |
|---|---|---|
| Capital paid into the bank by the group in 2025 | 35 | FIX: 77 committed, 50 paid [N1]; one outlet says OTP's 30 completed an 85 plan (`chrono:event:0029`), so the group's cash is 20 to 55 |
| Certificates of deposit bought with cash, per Rey | 20 | `rec:flow:0071`-`0073`; hearsay; origin of the cash unknown |
| Accrued interest collected in the portfolio sale | 3 | price 103.8% of principal (`rec:flow:0060`) |
| Bank and holding paper bought by borrowers | 7 | `press:flow:0050`; `press:fact:0056` |

**Against.** The certificate account is single-source and its date conflicts (`rec:issue:0009`). A former director denied indirect financing (`chrono:event:0063`). The 2025 capital increase may be partly capitalised profit.

**Confirm or refute.** Certificate register; capital account with origin of funds; SIPAP logs on capital dates; time-stamped Vinanzas statements.

### H4. Acquisition of assets: USD 50 million central (20 to 120). Confidence low. Held as assets.

**For.** Internal documents cited by ABC list 71 property payments totalling G. 61.1 bn and 15 dollar payments totalling USD 6.23 million from April 2024 to August 2026 (`press:fact:0076`-`0079`; `press:flow:0079`-`0081`; [N5]). Franede runs a hotel and borrowed G. 314 bn for hotel projects (`press:fact:0070`). Berilo's first loan was for land and works (`press:loan:0048`). Nubicom paid an equipment supplier USD 1.2 million (`press:flow:0135`). ITTI capitalised about USD 32 million of intangibles in 2025 [N2]. Seized: three ranches valued at USD 15.95 million, vehicles, a yacht, aircraft (`press:fact:0063`-`0065`; `chrono:event:0150`).

**Against.** The supervisor, as relayed, says the hotel loan went the same day to Vinanzas and ITTI "to cover debits" and that port-project money covered overdrafts and cheques (`press:flow:0074`-`0078`). Nothing dates the ranches, vehicles, yacht or aircraft inside the lending period. The Visión Banco price is not public; the merger was by absorption [N3]. ITTI's capitalised development is the same spending as H1.

**Confirm or refute.** Asset registers with invoices; property registry entries with dates and prices; the Visión share-purchase agreement.

### H5. Sponsorship and marketing (task item 7): USD 35 million central (15 to 70). Confidence low. Spent.

**For.** Priced contracts: football association USD 12 million over four years, rally USD 1 million, Olympic committee USD 300,000; club and stadium deals to 2030 unpriced [N7], [N8]. ITTI selling expenses G. 268 bn in 2025 against G. 38 bn [N2]. Nuevo Mundo Entertainment owed G. 199 bn (`press:fact:0030`); ITTI passed G. 74 bn to a firm called Match S.A. (`press:flow:0103`).

**Against.** No source says who paid the sponsorships. If the bank paid from its own income statement they are outside the questioned credit. Match S.A. is not described anywhere. The priced contracts total under USD 14 million.

### H6. Transfers abroad (item 5): USD 8 million central (6 to 40). Confidence low. Destination unknown.

**For.** Nubicom sent USD 4.6 million to an account of an Argentine company and USD 1.2 million to an equipment supplier (`press:flow:0090`, `0135`). Prosecutors announced cooperation with Luxembourg, Argentina and the United States and asked to freeze crypto-assets (`chrono:event:0158`).

**Against.** The Luxembourg holding was built with contributions in kind (`chrono:event:0010`); the only cash reported there is OTP's coming in. The Argentine company says it had sold its shares and never managed the funds (`press:event:0030`). No foreign authority has confirmed an amount. Argentine payroll is counted in H1.

### H7. Fees kept inside the bank (item 8): USD 5 million central (1 to 9). Confidence medium. Circulated.

**For.** Ten record loans equal a round amount times 1.005, eleven if G. 64,923 million is read as G. 64,600 million plus 0.5%; three Franede balances exceed principal by exactly 0.5% (`rec:issue:0007`; `rec:loan:0006`, `0008`, `0009`, `0012`-`0014`, `0017`-`0019`, `0031`). Those uplifts sum to USD 0.70 million. The pattern repeats at Nubicom, Berilo and Office Design (`press:loan:0045`, `0048`, `0050`). Half a per cent of USD 750 to 1,200 million of gross lending is USD 4 to 6 million.

**Against.** No source names the item; it could be a tax or insurance passed on. Small in money, but it suggests the borrowers did not fund even their origination cost.

### H8. Cash extraction and off-book payments (item 6): USD 2 million central (1 to 25). Confidence low. Extracted.

**For.** ABC reports seven cash requests prepared at the bank on the group's instructions: G. 1,176 million in January 2026 and G. 3,591 million in October 2026, about USD 0.73 million in all, some in bags and envelopes (`press:flow:0140`-`0146`). Rey says instalments on a land sale were assumed by the group through a supposed fodder payment (`rec:flow:0076`, `0077`).

**Against.** Reported outbound cash is 0.08% of the total. No source says who received it or why. Rey's USD 17 million plus G. 17,000 million is cash coming **into** the bank (`rec:flow:0071`, `0072`); the high case assumes it had first been taken out of the circuit, which no source says.

## 5. Allocation

| Rank | Bucket | Low | Central | High | Central share | Nature |
|---|---|---|---|---|---|---|
| 1 | Operating burn outside the bank | 250 | 440 | 600 | 48.1% | spent |
| 2 | Group debt service and own-loan interest | 70 | 140 | 220 | 15.3% | spent; part circulated |
| 3 | Circular support (capital, certificates, sale interest) | 25 | 65 | 135 | 7.1% | circulated |
| 4 | Assets | 20 | 50 | 120 | 5.5% | held |
| 5 | Sponsorship and marketing | 15 | 35 | 70 | 3.8% | spent |
| 6 | Transfers abroad | 6 | 8 | 40 | 0.9% | unknown |
| 7 | Fees kept by the bank | 1 | 5 | 9 | 0.5% | circulated |
| 8 | Cash and off-book payments | 1 | 2 | 25 | 0.2% | extracted |
| | **Explained** | **388** | **745** | **1,219** | 81.4% | |
| | **Unexplained** | **0** | **170** | **527** | 18.6% | |
| | **Total** | | **915** | | 100% | |

USD million. The high bounds exceed the total, so they cannot all hold together. Unexplained "high" pairs with the low bounds.

The USD 170 million sits mainly in second-ring borrowers with no traced first hop (Henrici, Technoma, Kasas, Model, most of GSR and Office Design; `press:fact:0002`, `0003`, `0007`-`0009`, `0016`), and in whatever lies behind the third of Rey's total he did not break down. He says he had no information on the family's expenses (`src:acta-p22`). I do not fill that gap.

About USD 133 million of the central case (own-loan interest 65, H3 65, H7 5) went back to the bank and propped up its income and capital. About USD 520 million was, on this hypothesis, consumed.

## 6. What the pattern does not show

- No questioned loan or interest paid from a borrower's own revenue.
- No questioned money traced to a foreign bank account beyond USD 5.8 million; no confirmed foreign freeze.
- No questioned money shown reaching a public official; the related case rests on other facts not sized here.
- No link between any seized vehicle, aircraft, yacht or ranch and a specific loan.
- No document that sizes cashback or shows which company bore it.
- No origin for the cash Rey describes, and no proof that capital was paid with certificates.
- No amounts in the record for the forwarding and repayment legs of the six.
- No accounts for REDISA, REDIPRO, Vinanzas, Kasas, Model or any shell.
- No evidence of large personal spending funded by the loans; documented property payments are USD 9 to 16 million over 29 months.
- Nothing on what the first-generation overdrafts of ITTI, REDISA and REDIPRO were drawn for.

## 7. Ten documents that would settle it fastest

1. Time-stamped statements of ITTI, REDISA, REDIPRO, Vinanzas and Grupo Vázquez at Ueno and other banks, January 2024 to November 2026, with the SIPAP log.
2. Ledgers and accounts of REDISA, REDIPRO and Vinanzas, 2024-26.
3. ITTI's related-party revenue schedule by customer and contract, with payroll and supplier files including remittances to Kaitel.
4. The bank's cashback ledger: monthly amounts, account debited, any re-invoicing.
5. The "Delirio Colectivo" email of 13 October 2025 with its 20-page attachment.
6. The merger trust ledger with invoices, and BCP Resolution 32 of 27 May 2024 with the feasibility plan.
7. The certificate-of-deposit register and the capital account with origin of funds, plus the receipts and schedules Rey filed.
8. Broker trade tickets and paying-agent records for every group bond coupon and maturity.
9. The bank's SWIFT log, foreign-exchange tickets, vault log and cash-withdrawal vouchers.
10. Credit files and settlement sheets of every questioned loan, and the Superintendency's reports 006, 007 and 011 of 2026 with annexes.

## 8. Evidence quality and gaps

- **Strongest:** the June 2026 loop, which closes to the cent (`rec:flow:0041`-`0061`); the cancelled-loan arithmetic in the record tables; the 0.5% pattern; rating-agency figures for ITTI.
- **Weakest:** the cashback half of H1 (Rey only, and the promotion rules point the other way); the certificate story (hearsay); sponsorship (payer unknown); assets (no purchase dates); the debtor list behind 83% of the total (unofficial, undated).
- **Gaps:** no forwarding amounts in the record; no accounts for the hub companies; second-ring loan dates and rates mostly missing; the FIX cash-flow annex mixes units and should be re-read; the Visión purchase price and the composition of the trust are unknown.

## New sources opened

| # | Outlet | Title | Date | URL |
|---|---|---|---|---|
| N1 | FIX SCR | Grupo Vázquez S.A.E. rating report (cash-flow annex) | 2026-07-02 | https://www.grupovazquez.com/wp-content/uploads/sites/2/2026/08/Grupo-Vazquez-S.A.E._compressed.pdf |
| N2 | Solventa&Riskmétrica | ITTI PEG G1 rating report, cut-off Dec 2025 | 2026-05-12 | https://syr.com.py/wp-content/uploads/2025/09/Informe-de-Calificacion-PEG-G1-ITTI-Dic25.pdf |
| N3 | FIX SCR | ueno bank rating report, December 2024 | 2025-04 | https://ueno.com.py/wp-content/uploads/2025/04/Fix-Scr-Fitch-Ratings_Diciembre-2024.pdf |
| N4 | ueno bank | Promotion rules, 30% cashback at participating merchants | 2025-12 | https://www.ueno.com.py/wp-content/uploads/2025/12/Promocion-Reintegro-30-de-reintegro-en-comercios-adheridos_-DIC-2025v3.docx-1.pdf |
| N5 | ABC Color | Costosos inmuebles, parte del esquema de triangulación de Ueno | 2026-11-19 | https://www.abc.com.py/politica/2026/11/19/costosos-inmuebles-parte-del-esquema-de-triangulacion-de-ueno/ |
| N6 | Chequeado | Del Ueno Bank a Buenos Aires | 2026-11-11 | https://chequeado.com/el-explicador/del-ueno-bank-a-buenos-aires-asi-operaba-el-grupo-vazquez-con-sus-trabajadores-en-argentina/ |
| N7 | InfoNegocios Paraguay | ¿Qué compromisos están en juego y quiénes podrían verse afectados? | 2026-11-04 | https://infonegocios.com.py/default/que-compromisos-estan-en-juego-y-quienes-podrian-verse-afectados |
| N8 | EFE via Primicias | La caída de Ueno Bank deja al descubierto la fragilidad financiera del deporte | 2026-11-11 | https://www.primicias.ec/deportes/futbol/crisis-financiera-paraguay-ueno-bank-deporte-bancos-136872/ |
| N9 | EFE via El Mostrador | Autos de lujo, avionetas, un yate y documentos | 2026-11-08 | https://www.elmostrador.cl/noticias/2026/11/08/autos-de-lujo-avionetas-un-yate-y-documentos-las-incautaciones-en-caso-ueno-en-paraguay/ |
