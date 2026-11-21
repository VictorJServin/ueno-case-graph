# FIBO alignment for the Ueno case knowledge graph

Companion to `data/ontology.ttl` (namespace `https://w3id.org/ueno-case/ont#`, prefix `uc:`; instances `https://w3id.org/ueno-case/id/`, prefix `ucr:`).

Instance IRIs follow the SPEC.md IDs with `:` turned into `/`: `org:ueno-bank` becomes `<https://w3id.org/ueno-case/id/org/ueno-bank>`, `src:acta-p05` becomes `<https://w3id.org/ueno-case/id/src/acta-p05>`, `rec:loan:0007` becomes `<https://w3id.org/ueno-case/id/rec/loan/0007>`. Because of the `/`, these cannot be written as plain `ucr:` prefixed names in Turtle or SPARQL: write the full IRI (or escape the slash, `ucr:org\/ueno-bank`). Named graphs: `<https://w3id.org/ueno-case/id/graph/prosecution>`, `<https://w3id.org/ueno-case/id/graph/rey>`, `<https://w3id.org/ueno-case/id/graph/press>`.

## How the IRIs were verified

- **FIBO**: `git clone --depth 1 https://github.com/edmcouncil/fibo` on 2026-11-20, master at commit `33a92cd` (2026-10-27). Module version IRIs seen: FBC `20260901`, BE `20260701`, LOAN `20251201`. All 293 `.rdf` files outside `etc/` were parsed with rdflib into an index of class / property / individual IRIs, labels and `owl:deprecated` flags. A term counts as verified only if it is *declared* in the file named below and is not deprecated.
- **OMG Commons Ontology Library**: `www.omg.org` is blocked from the shell in this environment, so the RDF/XML files were taken from a GitHub mirror (`tetherless-world/ontology-engineering`, folder `oe2026/Commons`, version IRIs `20250801` and `20260801`). Two cross-checks: 23 of the 25 Commons IRIs below are also referenced by the current FIBO files (the exceptions, `cmns-dt:hasDateValue` and `cmns-pts:hasRelatedPartyRole`, rest on the mirror alone), and `https://www.omg.org/spec/Commons/PartiesAndSituations.ttl` was fetched directly and shows the same version IRI (`.../Commons/20250801/PartiesAndSituations/`) and the same terms. File paths are shown as `Commons/<Module>.rdf`.
- **PROV-O and schema.org** terms used in `ontology.ttl` (`prov:Entity`, `prov:Agent`, `prov:Bundle`, `prov:wasDerivedFrom`, `prov:wasAttributedTo`, `schema:CreativeWork`, `schema:Person`, `schema:Organization`, `schema:Event`, `schema:MoneyTransfer`) were checked against the term lists bundled with rdflib, not against a fresh download.

**Result: 35 concepts. 29 fully verified, 5 partially verified (main class found, one requested facet missing), 1 not found. 164 individual IRIs verified in files.**

## Prefixes

| prefix | namespace |
|---|---|
| `cmns-dt:` | `https://www.omg.org/spec/Commons/DatesAndTimes/` |
| `cmns-id:` | `https://www.omg.org/spec/Commons/Identifiers/` |
| `cmns-org:` | `https://www.omg.org/spec/Commons/Organizations/` |
| `cmns-pts:` | `https://www.omg.org/spec/Commons/PartiesAndSituations/` |
| `cmns-qtu:` | `https://www.omg.org/spec/Commons/QuantitiesAndUnits/` |
| `cmns-ra:` | `https://www.omg.org/spec/Commons/RegulatoryAgencies/` |
| `fibo-be-ge-ge:` | `https://spec.edmcouncil.org/fibo/ontology/BE/GovernmentEntities/GovernmentEntities/` |
| `fibo-be-ge-sajur:` | `https://spec.edmcouncil.org/fibo/ontology/BE/GovernmentEntities/LatinAmericanJurisdiction/SouthAmericanGovernmentEntitiesAndJurisdictions/` |
| `fibo-be-le-cb:` | `https://spec.edmcouncil.org/fibo/ontology/BE/LegalEntities/CorporateBodies/` |
| `fibo-be-le-lei:` | `https://spec.edmcouncil.org/fibo/ontology/BE/LegalEntities/LEIEntities/` |
| `fibo-be-le-lp:` | `https://spec.edmcouncil.org/fibo/ontology/BE/LegalEntities/LegalPersons/` |
| `fibo-be-oac-cctl:` | `https://spec.edmcouncil.org/fibo/ontology/BE/OwnershipAndControl/CorporateControl/` |
| `fibo-be-oac-cown:` | `https://spec.edmcouncil.org/fibo/ontology/BE/OwnershipAndControl/CorporateOwnership/` |
| `fibo-be-oac-exec:` | `https://spec.edmcouncil.org/fibo/ontology/BE/OwnershipAndControl/Executives/` |
| `fibo-fbc-dae-dbt:` | `https://spec.edmcouncil.org/fibo/ontology/FBC/DebtAndEquities/Debt/` |
| `fibo-fbc-dae-gty:` | `https://spec.edmcouncil.org/fibo/ontology/FBC/DebtAndEquities/Guaranty/` |
| `fibo-fbc-fct-fse:` | `https://spec.edmcouncil.org/fibo/ontology/FBC/FunctionalEntities/FinancialServicesEntities/` |
| `fibo-fbc-fi-fi:` | `https://spec.edmcouncil.org/fibo/ontology/FBC/FinancialInstruments/FinancialInstruments/` |
| `fibo-fbc-pas-caa:` | `https://spec.edmcouncil.org/fibo/ontology/FBC/ProductsAndServices/ClientsAndAccounts/` |
| `fibo-fbc-pas-fpas:` | `https://spec.edmcouncil.org/fibo/ontology/FBC/ProductsAndServices/FinancialProductsAndServices/` |
| `fibo-fnd-aap-ppl:` | `https://spec.edmcouncil.org/fibo/ontology/FND/AgentsAndPeople/People/` |
| `fibo-fnd-acc-4217:` | `https://spec.edmcouncil.org/fibo/ontology/FND/Accounting/ISO4217-CurrencyCodes/` |
| `fibo-fnd-acc-cur:` | `https://spec.edmcouncil.org/fibo/ontology/FND/Accounting/CurrencyAmount/` |
| `fibo-fnd-agr-ctr:` | `https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/` |
| `fibo-fnd-dt-oc:` | `https://spec.edmcouncil.org/fibo/ontology/FND/DatesAndTimes/Occurrences/` |
| `fibo-fnd-law-cor:` | `https://spec.edmcouncil.org/fibo/ontology/FND/Law/LegalCore/` |
| `fibo-fnd-oac-ctl:` | `https://spec.edmcouncil.org/fibo/ontology/FND/OwnershipAndControl/Control/` |
| `fibo-fnd-oac-own:` | `https://spec.edmcouncil.org/fibo/ontology/FND/OwnershipAndControl/Ownership/` |
| `fibo-fnd-pas-pas:` | `https://spec.edmcouncil.org/fibo/ontology/FND/ProductsAndServices/ProductsAndServices/` |
| `fibo-fnd-pas-psch:` | `https://spec.edmcouncil.org/fibo/ontology/FND/ProductsAndServices/PaymentsAndSchedules/` |
| `fibo-fnd-pty-pty:` | `https://spec.edmcouncil.org/fibo/ontology/FND/Parties/Parties/` |
| `fibo-fnd-rel-rel:` | `https://spec.edmcouncil.org/fibo/ontology/FND/Relations/Relations/` |
| `fibo-loan-ln-evt:` | `https://spec.edmcouncil.org/fibo/ontology/LOAN/LoansGeneral/LoanEvents/` |
| `fibo-loan-ln-ln:` | `https://spec.edmcouncil.org/fibo/ontology/LOAN/LoansGeneral/Loans/` |
| `fibo-loan-reln-mtg:` | `https://spec.edmcouncil.org/fibo/ontology/LOAN/RealEstateLoans/Mortgages/` |
| `fibo-loan-spc-prod:` | `https://spec.edmcouncil.org/fibo/ontology/LOAN/LoansSpecific/LoanProducts/` |
| `fibo-sec-dbt-bnd:` | `https://spec.edmcouncil.org/fibo/ontology/SEC/Debt/Bonds/` |

## Mapping table

| # | Concept | Status | FIBO / Commons IRI (label, kind) | Verified in file | How the case graph uses it | Notes, moves, deprecations |
|---|---|---|---|---|---|---|
| 1 | Bank / depository institution | VERIFIED | `fibo-fbc-fct-fse:Bank` ("bank", class)<br>`fibo-fbc-fct-fse:DepositoryInstitution` ("depository institution", class)<br>`fibo-fbc-fct-fse:CommercialBank` ("commercial bank", class)<br>`fibo-fbc-fct-fse:FinancialInstitution` ("financial institution", class) | `FBC/FunctionalEntities/FinancialServicesEntities.rdf` | `rdf:type` of the node for `org:ueno-bank` and the other banks (Visión, Zeta, OTP). | Bank is a subclass of DepositoryInstitution, which is a subclass of FinancialInstitution. |
| 2 | Central bank | VERIFIED | `fibo-fbc-fct-fse:CentralBank` ("central bank", class) | `FBC/FunctionalEntities/FinancialServicesEntities.rdf` | `rdf:type` of the node for `auth:bcp`. | Subclass of both Bank and MonetaryAuthority. |
| 3 | Regulatory agency | VERIFIED | `cmns-ra:RegulatoryAgency` ("None", class)<br>`cmns-ra:regulates` ("regulates", object property)<br>`cmns-ra:isRegulatedBy` ("is regulated by", object property)<br>`fibo-be-ge-ge:GovernmentAgency` ("government agency", class) | `FBC/FunctionalEntities/RegulatoryAgencies.rdf`<br>`Commons/RegulatoryAgencies.rdf`<br>`BE/GovernmentEntities/GovernmentEntities.rdf` | `rdf:type` of the superintendencies; `uc:Authority` records it as `uc:fiboAnalogue`. | MOVED: no `RegulatoryAgency` class in FIBO any more. `FBC/FunctionalEntities/RegulatoryAgencies.rdf` still exists but only re-uses the Commons class (it defines TaxAuthority, Examiner, RegulatoryCapacity...). |
| 4 | Broker-dealer | VERIFIED | `fibo-fbc-pas-fpas:BrokerDealer` ("None", class)<br>`fibo-fbc-pas-fpas:Broker` ("broker", class)<br>`fibo-fbc-pas-fpas:Dealer` ("dealer", class) | `FBC/FunctionalEntities/NorthAmericanEntities/USNationalInformationCenterControlledVocabularies.rdf`<br>`FBC/ProductsAndServices/FinancialProductsAndServices.rdf` | `rdf:type` of the nodes for `org:ueno-casa-de-bolsa`, `org:cadiem`. | Lives in FBC/ProductsAndServices/FinancialProductsAndServices, not in FunctionalEntities/FinancialServicesEntities. It is a FunctionalEntity (a role-like classification), not a legal form. |
| 5 | Legal entity / legal person | VERIFIED | `cmns-org:LegalEntity` ("None", class)<br>`cmns-org:LegalPerson` ("None", class)<br>`cmns-org:Organization` ("None", class)<br>`cmns-org:FormalOrganization` ("None", class)<br>`fibo-be-le-lp:LegallyCompetentNaturalPerson` ("legally competent natural person", class)<br>`fibo-be-le-lp:BusinessEntity` ("business entity", class) | `FBC/FunctionalEntities/BusinessRegistries.rdf`<br>`BE/LegalEntities/LegalPersons.rdf`<br>`FND/Organizations/FormalOrganizations.rdf` | `uc:Organisation` is a subclass of `cmns-org:Organization`; companies with a known legal form are also typed `cmns-org:LegalEntity`. | MOVED: `fibo-be-le-lp:LegalEntity` and `fibo-be-le-lp:LegalPerson` no longer exist (0 definitions, 0 references). `FND/Organizations/Organizations.rdf` is gone too. Commons labels use British spelling ("formal organisation"). |
| 6 | Stock corporation | VERIFIED | `fibo-be-le-cb:StockCorporation` ("stock corporation", class)<br>`fibo-be-le-cb:Corporation` ("corporation", class)<br>`fibo-be-le-cb:PrivatelyHeldCompany` ("privately held company", class)<br>`fibo-be-le-cb:JointStockCompany` ("joint stock company", class) | `BE/LegalEntities/CorporateBodies.rdf` | `rdf:type` of the S.A. companies (Ueno Bank S.A., ITTI S.A.E.C.A., ...). | No class for S.R.L. in this module; see BE/PrivateLimitedCompanies. |
| 7 | Person | VERIFIED | `fibo-fnd-aap-ppl:Person` ("person", class) | `FND/AgentsAndPeople/People.rdf` | `uc:Person` is a subclass. | Still in FIBO (FND/AgentsAndPeople/People), now a subclass of `cmns-pts:Party`. `fibo-fnd-aap-agt:AutonomousAgent` is gone. |
| 8 | Shareholder and shareholding with percentage | PARTIAL | `fibo-be-oac-cown:Shareholder` ("shareholder", class)<br>`fibo-be-oac-cown:Shareholding` ("None", class)<br>`fibo-be-oac-cown:consistsOfNumberOfUnits` ("consists of number of units", datatype property)<br>`fibo-fbc-fi-fi:hasShareholder` ("has shareholder", object property)<br>`fibo-be-le-lei:hasOwnershipPercentage` ("has ownership percentage", datatype property)<br>`cmns-qtu:Percentage` ("percentage", class) | `BE/OwnershipAndControl/CorporateOwnership.rdf`<br>`SEC/Equities/EquityInstruments.rdf`<br>`FBC/FinancialInstruments/FinancialInstruments.rdf`<br>`BE/LegalEntities/LEIEntities.rdf`<br>`Commons/QuantitiesAndUnits.rdf` | `uc:role_shareholder skos:closeMatch` Shareholder; `uc:percentage` has `uc:fiboAnalogue` hasOwnershipPercentage. | Shareholder and Shareholding VERIFIED. Percentage: Shareholding is a FinancialAsset counted in units (`consistsOfNumberOfUnits`); it has NO percentage property. The only ownership-percentage term is the datatype property `hasOwnershipPercentage` in the LEI module (GLEIF relationship records). `hasShareholder` has domain Issuer and range Shareholder (roles). |
| 9 | Beneficial owner | VERIFIED | `fibo-be-oac-cown:BeneficialOwner` ("None", class)<br>`fibo-be-oac-cown:BeneficialOwnership` ("beneficial ownership", class)<br>`fibo-be-oac-cown:hasBeneficialOwner` ("has beneficial owner", object property)<br>`fibo-be-oac-cown:isBeneficialOwnerOf` ("is beneficial owner of", object property) | `BE/OwnershipAndControl/Executives.rdf`<br>`BE/OwnershipAndControl/CorporateOwnership.rdf` | `uc:role_beneficial_owner skos:closeMatch` BeneficialOwner. | hasBeneficialOwner has domain Asset (not the company). |
| 10 | Control / controlling party | VERIFIED | `fibo-fnd-oac-ctl:Control` ("control", class)<br>`fibo-fnd-oac-ctl:ControllingParty` ("controlling party", class)<br>`fibo-fnd-oac-ctl:hasControllingParty` ("has controlling party", object property)<br>`fibo-fnd-oac-ctl:isControlledPartyOf` ("is controlled party of", object property)<br>`fibo-fnd-oac-ctl:DeFactoControl` ("de facto control", class)<br>`fibo-fnd-oac-ctl:DeJureControl` ("de jure control", class) | `FND/OwnershipAndControl/Control.rdf` | `uc:role_controlling_group skos:closeMatch` ControllingParty; `uc:RoleHolding` lists Control as `uc:fiboAnalogue`. | Control is a `cmns-pts:Situation`; ControllingParty is a `cmns-pts:Actor` (a role). |
| 11 | Affiliate / related party | PARTIAL | `fibo-be-oac-cctl:Affiliate` ("affiliate", class)<br>`fibo-be-oac-cctl:Affiliation` ("affiliation", class)<br>`fibo-be-oac-cctl:isAffiliateOf` ("is affiliate of", object property)<br>`fibo-be-oac-cctl:hasAffiliate` ("has affiliate", object property)<br>`fibo-be-oac-cctl:SignificantShareholder` ("significant shareholder", class)<br>`cmns-pts:hasRelatedPartyRole` ("has related party role", object property) | `BE/OwnershipAndControl/CorporateControl.rdf`<br>`Commons/PartiesAndSituations.rdf` | `uc:declaredRelatedTo` / `uc:assessedRelatedTo` carry `uc:fiboAnalogue` isAffiliateOf; `uc:role_related_group_member skos:relatedMatch` Affiliate. | Affiliate VERIFIED. "Related party" in the banking-regulation sense (parte vinculada: includes relatives, directors, common operators) is NOT FOUND as a class. `cmns-pts:hasRelatedPartyRole` is only a generic role-to-role link. FIBO affiliation is defined purely by control. |
| 12 | Board member / director / corporate officer | VERIFIED | `fibo-be-oac-exec:BoardMember` ("board member", class)<br>`fibo-be-oac-exec:BoardMembership` ("board membership", class)<br>`fibo-be-oac-exec:BoardOfDirectors` ("board of directors", class)<br>`fibo-be-oac-exec:hasDirector` ("has director", object property)<br>`fibo-be-oac-exec:isDirectorOf` ("is director of", object property)<br>`fibo-be-oac-exec:CorporateOfficer` ("corporate officer", class)<br>`fibo-be-oac-exec:isOfficerOf` ("is officer of", object property)<br>`fibo-be-oac-exec:Executive` ("executive", class)<br>`fibo-be-oac-exec:Auditor` ("auditor", class)<br>`fibo-be-oac-exec:Signatory` ("signatory", class) | `BE/OwnershipAndControl/Executives.rdf` | Role-type concepts `uc:role_director`, `uc:role_president`, `uc:role_officer`, `uc:role_statutory_auditor`, `uc:role_legal_representative` map here. | There is no `Director` class: the class is BoardMember and the properties are hasDirector / isDirectorOf. No class for president, alternate director or síndico. Several Executives terms (AuthorizedParty, Authorization, LegallyDelegatedAuthority, hasResponsibleParty...) are DEPRECATED and moved to Commons BusinessAuthorizations. |
| 13 | Loan | VERIFIED | `fibo-loan-ln-ln:Loan` ("None", class)<br>`fibo-fbc-dae-dbt:CreditAgreement` ("None", class)<br>`fibo-fbc-fi-fi:DebtInstrument` ("None", class) | `LOAN/LoansSpecific/LoanProducts.rdf`<br>`FBC/ProductsAndServices/ClientsAndAccounts.rdf`<br>`SEC/Debt/DebtInstruments.rdf` | `uc:Loan rdfs:subClassOf` Loan. | Loan is a subclass of CreditAgreementRepaidPeriodically and DebtInstrument. |
| 14 | Unsecured loan | VERIFIED | `fibo-loan-ln-ln:UnsecuredLoan` ("unsecured loan", class)<br>`fibo-loan-ln-ln:SecuredLoan` ("secured loan", class)<br>`fibo-loan-ln-ln:CollateralizedLoan` ("collateralized loan", class)<br>`fibo-loan-ln-ln:GuaranteedLoan` ("guaranteed loan", class) | `LOAN/LoansGeneral/Loans.rdf` | Extra `rdf:type` on a `uc:Loan` whose `uc:collateral` is "none" (as asserted). |  |
| 15 | Line of credit / overdraft / open-end credit | PARTIAL | `fibo-loan-ln-ln:OpenEndCredit` ("open-end credit", class)<br>`fibo-loan-ln-ln:ClosedEndCredit` ("closed-end credit", class)<br>`fibo-fbc-dae-dbt:RevolvingLineOfCredit` ("revolving line of credit", class)<br>`fibo-fbc-dae-dbt:CreditFacility` ("None", class)<br>`fibo-fbc-dae-dbt:UncommittedCreditFacility` ("uncommitted credit facility", class)<br>`fibo-fbc-dae-dbt:hasCreditLimit` ("has credit limit", object property)<br>`fibo-loan-spc-prod:OverdraftFacilityPurpose` ("overdraft facility purpose", class) | `LOAN/LoansGeneral/Loans.rdf`<br>`FBC/DebtAndEquities/Debt.rdf`<br>`FBC/FinancialInstruments/FinancialInstruments.rdf`<br>`LOAN/LoansSpecific/LoanProducts.rdf` | `uc:Overdraft rdfs:subClassOf` OpenEndCredit. | OpenEndCredit and RevolvingLineOfCredit VERIFIED. Overdraft: NOT FOUND as a class. It appears only in a `skos:example` of OpenEndCredit and as OverdraftFacilityPurpose (a loan purpose). OpenEndCredit is disjoint with ClosedEndCredit. |
| 16 | Lender | VERIFIED | `fibo-fbc-dae-dbt:Lender` ("lender", class)<br>`fibo-fbc-dae-dbt:hasLender` ("has lender", object property) | `FBC/DebtAndEquities/Debt.rdf` | `uc:lender` has `uc:fiboAnalogue` hasLender. | In FBC/DebtAndEquities/Debt, not in LOAN. hasLender has range Lender (a party role), so `uc:lender` is not a sub-property. |
| 17 | Borrower / debtor / creditor | VERIFIED | `fibo-fbc-dae-dbt:Borrower` ("borrower", class)<br>`fibo-fbc-dae-dbt:hasBorrower` ("has borrower", object property)<br>`fibo-fbc-dae-dbt:Debtor` ("debtor", class)<br>`fibo-fbc-dae-dbt:Creditor` ("creditor", class)<br>`fibo-fbc-dae-dbt:Debt` ("debt", class) | `FBC/DebtAndEquities/Debt.rdf` | `uc:nominalBorrower` has `uc:fiboAnalogue` hasBorrower. | Same role pattern: hasBorrower has range Borrower. No notion of a nominal versus real borrower. |
| 18 | Principal amount | VERIFIED | `fibo-loan-ln-ln:hasPrincipalAmount` ("has principal amount", object property)<br>`fibo-fbc-dae-dbt:hasPrincipal` ("has principal", object property)<br>`fibo-fbc-dae-dbt:Principal` ("principal", class)<br>`fibo-fbc-dae-dbt:hasOutstandingAmount` ("has outstanding amount", object property)<br>`fibo-loan-ln-ln:hasLoanBalance` ("has loan balance", object property)<br>`fibo-loan-ln-ln:TotalOutstandingPrincipal` ("total outstanding principal", class) | `LOAN/LoansGeneral/Loans.rdf`<br>`FBC/DebtAndEquities/Debt.rdf` | `uc:principal`, `uc:outstanding` (plain decimals) point here via `uc:fiboAnalogue`. | hasPrincipalAmount has range MonetaryAmount (an object, not a number). |
| 19 | Interest rate | VERIFIED | `fibo-fnd-acc-cur:InterestRate` ("interest rate", class)<br>`fibo-fbc-dae-dbt:hasInterestRate` ("has interest rate", object property)<br>`fibo-fnd-acc-cur:hasRateValue` ("has rate value", datatype property)<br>`fibo-fbc-dae-dbt:FixedInterestRate` ("fixed interest rate", class) | `FND/Accounting/CurrencyAmount.rdf`<br>`FBC/DebtAndEquities/Debt.rdf` | `uc:ratePct` via `uc:fiboAnalogue`. | InterestRate class is in FND/Accounting/CurrencyAmount; the property is in FBC Debt. |
| 20 | Maturity / term | VERIFIED | `fibo-fbc-dae-dbt:hasMaturityDate` ("has maturity date", object property)<br>`fibo-fbc-dae-dbt:hasOriginalTimeToMaturity` ("has time to maturity", object property)<br>`fibo-fnd-agr-ctr:hasTerm` ("has term", object property)<br>`fibo-fnd-agr-ctr:hasEffectiveDate` ("has effective date", object property) | `FBC/DebtAndEquities/Debt.rdf`<br>`FND/Agreements/Contracts.rdf` | `uc:termYears`, `uc:termDays` via `uc:fiboAnalogue`. | `hasOriginalTimeToMaturity` carries the label "has time to maturity". hasTerm has range `cmns-dt:Duration`. |
| 21 | Collateral | VERIFIED | `fibo-fbc-dae-dbt:Collateral` ("collateral", class)<br>`fibo-fbc-dae-dbt:isCollateralizedBy` ("is collateralized by", object property) | `FBC/DebtAndEquities/Debt.rdf` | `uc:collateral` (a short code such as "none", "mortgage_claimed") via `uc:fiboAnalogue`. |  |
| 22 | Mortgage | VERIFIED | `fibo-loan-reln-mtg:Mortgage` ("mortgage", class)<br>`fibo-loan-reln-mtg:LoanSecuredByRealEstate` ("None", class) | `LOAN/RealEstateLoans/Mortgages.rdf`<br>`LOAN/RealEstateLoans/MortgageOrigination.rdf` | Documentation only; a claimed mortgage is recorded as `uc:collateral "mortgage_claimed"`. | In FIBO a Mortgage is a SecurityAgreement (the lien on real property), NOT a loan. The loan is LoanSecuredByRealEstate. |
| 23 | Promissory note | VERIFIED | `fibo-fbc-fi-fi:PromissoryNote` ("promissory note", class) | `FBC/FinancialInstruments/FinancialInstruments.rdf` | Documentation only (pagarés mentioned in the record). | In FBC/FinancialInstruments, a subclass of DebtInstrument. |
| 24 | Bond and issuer | VERIFIED | `fibo-sec-dbt-bnd:Bond` ("bond", class)<br>`fibo-fbc-fi-fi:Issuer` ("None", class)<br>`fibo-fnd-rel-rel:isIssuedBy` ("is issued by", object property)<br>`fibo-fnd-rel-rel:issues` ("issues", object property) | `SEC/Debt/Bonds.rdf`<br>`SEC/Securities/SecuritiesIssuance.rdf`<br>`FND/Relations/Relations.rdf` | `uc:instr_bond_purchase skos:relatedMatch` Bond. | There is no `hasIssuer` property; the pair is `fibo-fnd-rel-rel:isIssuedBy` / `issues`. |
| 25 | Certificate of deposit | VERIFIED | `fibo-fbc-pas-caa:CertificateOfDeposit` ("certificate of deposit", class) | `FBC/ProductsAndServices/ClientsAndAccounts.rdf` | Documentation only (CDAs held by IPS and others). | In FBC/ProductsAndServices/ClientsAndAccounts as a CashInstrument, not in SEC. |
| 26 | Deposit account | VERIFIED | `fibo-fbc-pas-caa:DepositAccount` ("deposit account", class)<br>`fibo-fbc-pas-caa:DemandDepositAccount` ("demand deposit account", class)<br>`fibo-fbc-pas-caa:Account` ("account", class) | `FBC/ProductsAndServices/ClientsAndAccounts.rdf` | Documentation only; accounts are not modelled as nodes. |  |
| 27 | Payment / funds transfer event | PARTIAL | `fibo-fnd-pas-psch:Payment` ("payment", class)<br>`fibo-fnd-pas-psch:PaymentEvent` ("payment event", class)<br>`fibo-fnd-pas-psch:Payer` ("payer", class)<br>`fibo-fnd-pas-psch:Payee` ("payee", class)<br>`fibo-fnd-pas-psch:hasPaymentAmount` ("has payment amount", object property)<br>`fibo-fbc-pas-caa:IndividualTransaction` ("individual transaction", class)<br>`fibo-loan-ln-ln:IndividualPaymentTransaction` ("individual payment transaction", class)<br>`fibo-fbc-fct-fse:ElectronicFundsTransferService` ("electronic funds transfer service", class) | `FND/ProductsAndServices/PaymentsAndSchedules.rdf`<br>`FBC/ProductsAndServices/ClientsAndAccounts.rdf`<br>`LOAN/LoansGeneral/Loans.rdf`<br>`FBC/FunctionalEntities/FinancialServicesEntities.rdf` | `uc:Flow` lists Payment as `uc:fiboAnalogue`; `uc:fromParty` / `uc:toParty` point to Payer / Payee. | Payment VERIFIED (an Occurrence). PaymentEvent is an OccurrenceKind (a classifier), not an individual event. A funds-transfer event between two arbitrary parties is NOT FOUND; only ElectronicFundsTransferService (a service) exists. |
| 28 | Monetary amount with currency | VERIFIED | `fibo-fnd-acc-cur:MonetaryAmount` ("monetary amount", class)<br>`fibo-fnd-acc-cur:AmountOfMoney` ("amount of money", class)<br>`fibo-fnd-acc-cur:hasAmount` ("has amount", datatype property)<br>`fibo-fnd-acc-cur:hasCurrency` ("has currency", object property)<br>`fibo-fnd-acc-cur:Currency` ("currency", class)<br>`fibo-fnd-acc-cur:hasMonetaryAmount` ("has monetary amount", object property)<br>`fibo-fnd-acc-4217:PYG` ("PYG", individual)<br>`fibo-fnd-acc-4217:USD` ("USD", individual) | `FND/Accounting/CurrencyAmount.rdf`<br>`FND/Accounting/ISO4217-CurrencyCodes.rdf` | `uc:currency` has range Currency and takes the individuals `fibo-fnd-acc-4217:PYG` / `:USD`; `uc:amount` is a plain decimal. | hasAmount is a datatype property (xsd:decimal). The ISO 4217 individuals PYG, Guarani, USD exist. |
| 29 | Contract with buyer and seller | VERIFIED | `fibo-fnd-agr-ctr:Contract` ("contract", class)<br>`fibo-fnd-agr-ctr:hasContractParty` ("has contract party", object property)<br>`fibo-fnd-agr-ctr:Counterparty` ("counterparty", class)<br>`fibo-fnd-pas-pas:Buyer` ("buyer", class)<br>`fibo-fnd-pas-pas:Seller` ("seller", class)<br>`fibo-fnd-pas-pas:hasBuyer` ("has buyer", object property)<br>`fibo-fnd-pas-pas:hasSeller` ("has seller", object property)<br>`fibo-fnd-pas-pas:Sale` ("sale", class) | `FND/Agreements/Contracts.rdf`<br>`FND/ProductsAndServices/ProductsAndServices.rdf` | `uc:PortfolioSale` lists Sale as `uc:fiboAnalogue`. | Buyer and Seller are in FND/ProductsAndServices, not FND/Agreements/Contracts. Sale is modelled as a subclass of TransactionEvent (an OccurrenceKind) and of Situation, so it is not used as a superclass. |
| 30 | Assignment / sale of a loan | NOT FOUND | `fibo-fnd-pas-pas:Sale` ("sale", class)<br>`fibo-fnd-agr-ctr:AssignableContract` ("assignable contract", class)<br>`fibo-fnd-agr-ctr:TransferableContract` ("transferable contract", class)<br>`fibo-fnd-agr-ctr:isAssignable` ("is assignable", datatype property)<br>`fibo-fnd-oac-own:Portfolio` ("portfolio", class) | `FND/ProductsAndServices/ProductsAndServices.rdf`<br>`FND/Agreements/Contracts.rdf`<br>`FND/OwnershipAndControl/Ownership.rdf` | `uc:PortfolioSale`, `uc:instr_portfolio_sale_price`, `uc:instr_portfolio_assignment`. | NOT FOUND: no loan sale, loan assignment, assignor or assignee term in LOAN, FBC or SEC. Nearest alternatives listed (generic Sale; contracts that can be assigned; a Portfolio collection). |
| 31 | Guaranty | VERIFIED | `fibo-fbc-dae-gty:Guaranty` ("guaranty", class)<br>`fibo-fbc-dae-gty:Guarantor` ("guarantor", class)<br>`fibo-fbc-dae-gty:hasGuarantor` ("has guarantor", object property) | `FBC/DebtAndEquities/Guaranty.rdf` | Documentation only (personal guarantees mentioned by the record). | Spelled "guaranty"; own module FBC/DebtAndEquities/Guaranty. |
| 32 | Tax identifier | VERIFIED | `fibo-fnd-pty-pty:TaxIdentifier` ("tax identifier", class)<br>`fibo-fnd-pty-pty:TaxIdentificationScheme` ("tax identification scheme", class)<br>`cmns-id:identifies` ("None", object property) | `FND/Parties/Parties.rdf`<br>`Commons/MappingCommonsToBFO.rdf` | Company RUC, where a source states it, could be typed TaxIdentifier. Never recorded for persons (SPEC rule 4). | No `hasTaxIdentifier` property; link with `cmns-id:identifies` / `isIdentifiedBy`. |
| 33 | Law / jurisdiction | VERIFIED | `fibo-fnd-law-cor:Law` ("law", class)<br>`fibo-fnd-law-cor:StatuteLaw` ("statute law", class)<br>`fibo-fnd-law-cor:CourtOfLaw` ("court of law", class)<br>`cmns-ra:Jurisdiction` ("jurisdiction", class)<br>`cmns-ra:hasJurisdiction` ("has jurisdiction", object property)<br>`fibo-fnd-agr-ctr:hasGoverningJurisdiction` ("has governing jurisdiction", object property)<br>`fibo-be-ge-sajur:JurisdictionOfParaguay` ("jurisdiction of Paraguay", individual)<br>`fibo-be-ge-sajur:GovernmentOfTheRepublicOfParaguay` ("Government of the Republic of Paraguay", individual) | `FND/Law/LegalCore.rdf`<br>`Commons/RegulatoryAgencies.rdf`<br>`FND/Agreements/Contracts.rdf`<br>`BE/GovernmentEntities/LatinAmericanJurisdiction/SouthAmericanGovernmentEntitiesAndJurisdictions.rdf` | `uc:allegedOffence` is free text; the jurisdiction individual can be attached to the case node. | Law is in FIBO (FND/Law/LegalCore); Jurisdiction MOVED to Commons RegulatoryAgencies (`FND/Law/Jurisdiction.rdf` is gone). FIBO ships a `JurisdictionOfParaguay` individual. |
| 34 | Date and date period | VERIFIED | `cmns-dt:Date` ("date", class)<br>`cmns-dt:ExplicitDate` ("None", class)<br>`cmns-dt:DatePeriod` ("date period", class)<br>`cmns-dt:ExplicitDatePeriod` ("explicit date period", class)<br>`cmns-dt:hasDate` ("has date", object property)<br>`cmns-dt:hasDateValue` ("has date value", datatype property)<br>`cmns-dt:hasStartDate` ("has start date", object property)<br>`cmns-dt:hasEndDate` ("has end date", object property)<br>`cmns-dt:Duration` ("None", class) | `Commons/DatesAndTimes.rdf`<br>`Commons/MappingDatesAndTimesToOWLTime.rdf` | Not instantiated: `uc:onDate`, `uc:startDate`, `uc:endDate` are typed literals with `uc:datePrecision`. | MOVED: `fibo-fnd-dt-fd:Date`, `DatePeriod`, `hasDate` no longer exist; FinancialDates.rdf only keeps schedules and business-day terms. Commons dates are objects (a Date node with `hasDateValue`), not literals. |
| 35 | Occurrence / event with participants | PARTIAL | `fibo-fnd-dt-oc:Occurrence` ("occurrence", class)<br>`fibo-fnd-dt-oc:OccurrenceKind` ("occurrence kind", class)<br>`fibo-fnd-dt-oc:hasEventDate` ("has event date", object property)<br>`fibo-fnd-dt-oc:hasEventDateValue` ("has event date value", datatype property)<br>`cmns-pts:Situation` ("None", class)<br>`cmns-pts:hasParty` ("has party", object property)<br>`cmns-pts:hasActor` ("has actor", object property)<br>`cmns-pts:hasUndergoer` ("has undergoer", object property)<br>`fibo-loan-ln-evt:LegalProceeding` ("legal proceeding", class) | `FND/DatesAndTimes/Occurrences.rdf`<br>`Commons/MappingCommonsToBFO.rdf`<br>`Commons/PartiesAndSituations.rdf`<br>`LOAN/LoansGeneral/LoanEvents.rdf` | `uc:Flow` and `uc:CaseEvent` are subclasses of Occurrence; `uc:involvesParty rdfs:subPropertyOf cmns-pts:hasParty`. | Occurrence VERIFIED. It has NO participant property (only hasEventDate, hasInput/hasOutput, isTriggeredBy). Participants are modelled on `cmns-pts:Situation` (hasParty, hasActor, hasUndergoer). |

## FIBO terms that differ from common assumptions

1. **`LegalEntity`, `LegalPerson`, `Organization`, `FormalOrganization`, `RegulatoryAgency`, `Jurisdiction`, `Date`, `DatePeriod`, `PartyRole`, `Situation`, `Identifier` are no longer FIBO classes.** They live in the OMG Commons Ontology Library (`https://www.omg.org/spec/Commons/...`). The old IRIs (`fibo-be-le-lp:LegalEntity`, `fibo-fnd-org-org:Organization`, `fibo-fnd-org-fm:FormalOrganization`, `fibo-fbc-fct-rga:RegulatoryAgency`, `fibo-fnd-law-jur:Jurisdiction`, `fibo-fnd-dt-fd:Date`, `fibo-fnd-pty-rl:PartyInRole`, `fibo-fnd-pty-pty:IndependentParty`, `fibo-fnd-aap-agt:AutonomousAgent`, `fibo-fnd-rel-rel:hasIdentity`) are not declared in any file of the current repository. `FND/Parties/Roles.rdf`, `FND/Organizations/Organizations.rdf` and `FND/Law/Jurisdiction.rdf` no longer exist.
2. **Lender, Borrower, Debtor, Creditor, Collateral, hasLender, hasBorrower, hasInterestRate, hasMaturityDate are in `FBC/DebtAndEquities/Debt`, not in `LOAN`.** `LOAN/LoansGeneral/Loans` keeps Loan, SecuredLoan, UnsecuredLoan, OpenEndCredit, ClosedEndCredit and `hasPrincipalAmount`.
3. **Object properties point at roles, not parties.** `hasBorrower` has range `Borrower`, `hasLender` range `Lender`, `hasBuyer` range `Buyer`, `hasShareholder` domain `Issuer` and range `Shareholder`; all of these are `cmns-pts:PartyRole` subclasses. A faithful FIBO graph needs an extra role node per party per relationship.
4. **There is no `Director` class** (use `BoardMember`; properties `hasDirector` / `isDirectorOf`) and **no `hasIssuer`** (use `fibo-fnd-rel-rel:isIssuedBy`).
5. **`Mortgage` is the security agreement, not the loan** (`LoanSecuredByRealEstate` is the loan).
6. **`PaymentEvent`, `TransactionEvent` and therefore `Sale` are `OccurrenceKind`s**, i.e. classifiers of events, not events. The individual event class is `Payment` (an `Occurrence`).
7. **`Shareholding` has no percentage.** The only ownership-percentage property is `fibo-be-le-lei:hasOwnershipPercentage` in the LEI (GLEIF) module.
8. **`BrokerDealer` sits in `FBC/ProductsAndServices/FinancialProductsAndServices`**, and `CertificateOfDeposit` in `FBC/ProductsAndServices/ClientsAndAccounts`.
9. **Deprecated in `BE/OwnershipAndControl/Executives`**: `AuthorizedParty`, `AuthorizingParty`, `Authorization`, `LegallyDelegatedAuthority`, `hasResponsibleParty`, `hasAuthorizedParty`, `delegatesControlTo` and related properties (replaced by Commons `BusinessAuthorizations`). **Deprecated in `FND/Accounting/AccountingEquity`**: `ShareholdersEquity`, `OwnersEquity`, `RetainedEarnings`, `FinancialAsset`, `PhysicalAsset`, `Income` (moved to `FND/OwnershipAndControl/Ownership`).
10. Commons labels use British spelling ("organisation", "formal organisation") while the IRIs keep the `z`.

## What FIBO lacks for this use case

- **Claim-level provenance.** FIBO describes what is the case. It has no way to say who asserts a loan, a shareholding or a flow, from which page, with what reading confidence, or that two voices disagree. Hence `uc:Assertion`, `uc:assertedBy`, `uc:confidence`, `uc:locator`, `uc:quote`, `uc:sameSubjectAs`, `uc:Issue`, plus PROV-O and named graphs.
- **Nominal borrower versus ultimate recipient.** A loan has a borrower role and nothing for the party alleged to have really received the money (`uc:nominalBorrower`, `uc:ultimateRecipient`).
- **Related party in the prudential sense.** Only control-based `Affiliate`. Nothing for "declared as related by the bank" versus "assessed as related by the supervisor" (`uc:declaredRelatedTo`, `uc:assessedRelatedTo`), nor for the indicators used to argue it: kinship (`uc:relativeOf`, `uc:kinshipDegree`), shared address (`uc:sharesAddressWith`), shared operator (`uc:sharesOperatorWith`). No related-party lending limit or exposure concept.
- **Kinship between persons.** No family-relationship property at all.
- **Overdraft** as a product class, and **sale / assignment of a loan or loan portfolio** (`uc:Overdraft`, `uc:PortfolioSale`).
- **A generic money movement between two arbitrary parties** with an instrument (cash, cheque, transfer, bond purchase): `Payment` assumes an obligation being fulfilled (`uc:Flow`, `uc:instrument`).
- **Ownership percentage on a shareholding**, and time-bounded role holdings with a role type in one node (`uc:RoleHolding`). FIBO needs Shareholder + Shareholding + Ownership situation + date period nodes.
- **Civil-law corporate roles**: síndico (statutory auditor) and suplentes (alternates), president / vice-president of the board, registry agent (gestor).
- **Criminal procedure**: no offence, charge, indictment, suspect or precautionary-measure terms (only `LegalProceeding` / `CourtJudgment` in LOAN, for loan defaults). Hence `uc:Charge`, `uc:allegedOffence`, `uc:proceduralMeasure`.
- **Supervisory actions** (inspection, finding, sanction, intervention) and **depositor events**: nothing beyond `RegulatoryAgency` / `regulates`.
- **Imprecise dates** (month or year only) and **participants on `Occurrence`**.
- **Paraguay-specific reference data**: FIBO has `JurisdictionOfParaguay`, `GovernmentOfTheRepublicOfParaguay` and the `PYG` currency, but no BCP, Superintendencia de Bancos, RUC scheme or Paraguayan legal forms (S.A., S.A.E.C.A., S.R.L., E.A.S.).

## Example SPARQL queries

All queries assume these prefixes and run on the default (union) graph unless a `GRAPH` clause is shown.

```sparql
PREFIX uc:   <https://w3id.org/ueno-case/ont#>
PREFIX ucr:  <https://w3id.org/ueno-case/id/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
```

### Q1. Loans whose nominal borrower differs from the alleged ultimate recipients

```sparql
SELECT ?loan ?op ?borrower ?recipient ?principal ?cur ?who ?src ?conf
WHERE {
  ?loan a uc:Loan ;
        uc:nominalBorrower   ?borrower ;
        uc:ultimateRecipient ?recipient ;
        uc:assertedBy        ?who ;
        prov:wasDerivedFrom  ?src ;
        uc:confidence        ?conf .
  OPTIONAL { ?loan uc:operationNumber ?op }
  OPTIONAL { ?loan uc:principal ?principal }
  OPTIONAL { ?loan uc:currency ?cur }
  FILTER (?recipient != ?borrower)
}
ORDER BY DESC(?principal)
```

The result is "X alleges that the proceeds of loan L went to R", never "R received".

### Q2. Chains of flows that start and end at the same party within 7 days (2 or 3 hops)

```sparql
SELECT ?origin ?mid1 ?mid2 ?d1 ?dLast ?f1 ?f2 ?f3
WHERE {
  {
    # 2 hops: origin -> mid1 -> origin
    ?f1 a uc:Flow ; uc:fromParty ?origin ; uc:toParty ?mid1 ; uc:onDate ?d1 ; uc:assertedBy ?who .
    ?f2 a uc:Flow ; uc:fromParty ?mid1 ; uc:toParty ?origin ; uc:onDate ?dLast ; uc:assertedBy ?who .
    FILTER (?mid1 != ?origin)
  } UNION {
    # 3 hops: origin -> mid1 -> mid2 -> origin
    ?f1 a uc:Flow ; uc:fromParty ?origin ; uc:toParty ?mid1 ; uc:onDate ?d1 ; uc:assertedBy ?who .
    ?f2 a uc:Flow ; uc:fromParty ?mid1 ; uc:toParty ?mid2 ; uc:onDate ?d2 ; uc:assertedBy ?who .
    ?f3 a uc:Flow ; uc:fromParty ?mid2 ; uc:toParty ?origin ; uc:onDate ?dLast ; uc:assertedBy ?who .
    FILTER (?mid1 != ?origin && ?mid2 != ?origin && ?mid2 != ?mid1)
    FILTER (datatype(?d2) = xsd:date && ?d2 >= ?d1 && ?dLast >= ?d2)
  }
  FILTER (datatype(?d1) = xsd:date && datatype(?dLast) = xsd:date && ?dLast >= ?d1)
  FILTER (?dLast <= ?d1 + "P7D"^^xsd:dayTimeDuration)
}
ORDER BY ?d1
```

Only day-precision dates take part (month- and year-only literals are typed `xsd:gYearMonth` / `xsd:gYear`). The chain is kept inside one voice (`?who`) so that prosecution and suspect statements are not stitched together. The window test uses date + duration arithmetic (`?d1 + "P7D"`), which is an extension to SPARQL 1.1 that rdflib, Jena, GraphDB and Stardog support; the form `?dLast - ?d1 <= "P7D"` returns nothing in rdflib, so do not use it there.

### Q3. People holding roles in two or more borrowers

```sparql
SELECT ?person (COUNT(DISTINCT ?borrower) AS ?nBorrowers)
       (GROUP_CONCAT(DISTINCT STR(?borrower); separator=" | ") AS ?borrowers)
       (GROUP_CONCAT(DISTINCT STR(?role); separator=" | ") AS ?roles)
WHERE {
  ?loan a uc:Loan ; uc:nominalBorrower ?borrower .
  ?rh a uc:RoleHolding ;
      uc:holder ?person ;
      uc:organisation ?borrower ;
      uc:roleType ?role .
  ?person a uc:Person .
  FILTER (?role NOT IN (uc:role_relative_of, uc:role_charged_person))
}
GROUP BY ?person
HAVING (COUNT(DISTINCT ?borrower) >= 2)
ORDER BY DESC(?nBorrowers)
```

### Q4. Assertions made only by the suspect

Statements in the suspect's graph that no other voice corroborates: no `uc:sameSubjectAs` link to an assertion by anyone else and, for flows, no flow between the same two parties asserted by another voice.

```sparql
SELECT ?a ?type ?from ?to ?amount ?src ?locator
WHERE {
  GRAPH <https://w3id.org/ueno-case/id/graph/rey> {
    ?a uc:assertedBy uc:Rey ; a ?type ; prov:wasDerivedFrom ?src .
    OPTIONAL { ?a uc:locator ?locator }
    OPTIONAL { ?a uc:fromParty ?from ; uc:toParty ?to }
    OPTIONAL { ?a uc:amount ?amount }
  }
  FILTER (?type IN (uc:Flow, uc:Loan, uc:RoleHolding, uc:CaseEvent, uc:FinancialFact, uc:PortfolioSale))
  FILTER NOT EXISTS {
    ?a (uc:sameSubjectAs|^uc:sameSubjectAs) ?other .
    ?other uc:assertedBy ?v . FILTER (?v != uc:Rey)
  }
  FILTER NOT EXISTS {
    ?a uc:fromParty ?p1 ; uc:toParty ?p2 .
    ?o a uc:Flow ; uc:fromParty ?p1 ; uc:toParty ?p2 ; uc:assertedBy ?v2 .
    FILTER (?v2 != uc:Rey)
  }
}
ORDER BY ?src
```

### Q5. Data points with low confidence, with their source and any open data issue

```sparql
SELECT ?a ?type ?who ?src ?locator ?note ?issue
WHERE {
  ?a uc:confidence "low" ;
     a ?type ;
     uc:assertedBy ?who ;
     prov:wasDerivedFrom ?src .
  ?type rdfs:subClassOf uc:Assertion .
  OPTIONAL { ?a uc:locator ?locator }
  OPTIONAL { ?a uc:provenanceNote ?note }
  OPTIONAL { ?issue a uc:Issue ; uc:concerns ?a }
}
ORDER BY ?type ?src
```

Q5 needs `ontology.ttl` loaded alongside the data (for the `rdfs:subClassOf` join); drop that line to run on data alone.

### Q6. Analyst estimates and the sourced assertions each one rests on

Opinions live in their own named graph (`.../id/graph/analysis`) and are asserted by `uc:Analyst`. Each row pairs one estimate with one of the assertions it cites, showing that assertion's own voice, source tier, confidence and source, so a reader can see what an estimate stands on.

```sparql
SELECT ?opinion ?kind ?low ?central ?high ?cur ?basis ?who ?tier ?conf ?src
WHERE {
  GRAPH <https://w3id.org/ueno-case/id/graph/analysis> {
    ?opinion a uc:AnalystOpinion ;
             uc:assertedBy uc:Analyst ;
             uc:opinionKind ?kind .
    OPTIONAL { ?opinion uc:estimateLow ?low }
    OPTIONAL { ?opinion uc:estimateCentral ?central }
    OPTIONAL { ?opinion uc:estimateHigh ?high }
    OPTIONAL { ?opinion uc:currency ?cur }
    OPTIONAL { ?opinion uc:basedOn ?basis }
  }
  OPTIONAL {
    ?basis uc:assertedBy ?who ;
           uc:sourceTier ?tier ;
           uc:confidence ?conf ;
           prov:wasDerivedFrom ?src .
  }
}
ORDER BY ?opinion ?basis ?src
```

An opinion without `uc:basedOn` still appears, with the basis columns empty. A basis assertion that an editor corrected has more than one `prov:wasDerivedFrom` (its own source plus the correction's), so it appears once per source. The estimate is never a sourced figure: read `?low` / `?central` / `?high` as "the analysts estimate", and the basis columns as "X asserts".
