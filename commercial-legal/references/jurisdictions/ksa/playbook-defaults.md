# Playbook defaults — ksa

Defaults the cold-start interviews offer when the practice profile's primary jurisdiction is `ksa`. They are starting positions for the profile, not rules of law; the user accepts, edits, or rejects each one during the interview, and the profile records the result. Every default that rests on a statutory rule cites the instrument file; the interview must not state a default whose citation is missing.

## Commercial (vendor, NDA, SaaS review)

| Field | Default | Basis |
|---|---|---|
| Governing law, preferred | Laws of the Kingdom of Saudi Arabia | Practice; Saudi courts apply Saudi law and Sharia public order regardless of a foreign choice where a Saudi court is seised `[model knowledge — verify]` |
| Governing law, acceptable | English law for international counterparties, with a Saudi-seated or offshore arbitration clause | Practice `[model knowledge — verify]`; enforcement of a foreign judgment or award runs through `enforcement-law.md` (from 2026-10-28) and the Enforcement Law 1433H until then |
| Dispute forum, preferred | Arbitration under the SCCA Arbitration Rules 2023, seat Riyadh, language English with Arabic where the counterparty requires it | `arbitration-law.md` (Law Arts. 2, 9, 10, 14, 25, 38, 49-55; SCCA rules rows); the Rules have no seat or language default, so the clause must state them |
| Dispute forum, acceptable | Saudi Commercial Courts (Najiz) | `commercial-courts-law.md` (jurisdiction rows); appeal window 30 days |
| Dispute forum, escalate | Foreign court jurisdiction clauses | Foreign judgments are enforced only on reciprocity and public-order conditions, `enforcement-law.md` |
| Government or government-linked counterparty | Check whether the counterparty is bound by the Government Tenders and Procurement Law before accepting its penalty, bond, and variation terms; state-owned companies are generally outside it unless their statutes say otherwise `[model knowledge — verify]` | `government-tenders-procurement-law.md` (scope row, delay-penalty caps, bonds, grievance route) |
| Liquidated damages and penalties | Accept a fixed compensation clause only with the statutory reduction in view: a Saudi court may reduce it where excessive or the obligation was partly performed, disallow it where no harm occurred, and the parties cannot contract out; pre-agreed compensation on a money debt is barred | `civil-transactions-law.md` Arts. 178-179 |
| Limitation and exclusion of liability | Caps and exclusions are enforceable for contractual liability but never for fraud or gross fault; tort liability cannot be excluded; contractual damages are limited to foreseeable loss absent fraud or gross fault | `civil-transactions-law.md` Arts. 173, 180 |
| Hardship and force majeure | Hardship rebalancing is mandatory and cannot be waived; force-majeure risk may be shifted to the debtor by clause | `civil-transactions-law.md` Arts. 97, 174 |
| Assignment | Assignment of a whole contract needs counterparty consent; advance consent valid on notice; a share sale does not transfer contracts | `civil-transactions-law.md` Arts. 98, 255 |
| Limitation period for claims | 10 years general; 5 years periodic payments and professional fees; 1 year traders-to-non-traders; cannot be shortened or lengthened by contract; must be pleaded; Hijri years | `civil-transactions-law.md` Arts. 295-306 |
| Interest and late-payment charges | No contractual interest; pre-agreed compensation on money debts barred; state the position and flag any interest clause `[review]` | `civil-transactions-law.md` Arts. 178, 385; Sharia position `[model knowledge — verify]` |
| E-signature | Simple electronic signatures on DocuSign-type platforms are valid between the parties; statutory presumptions attach only to signatures under a licensed Saudi certificate; personal-status and real-property deeds excluded | `electronic-transactions-law.md` |
| Data protection clauses | Controller-to-processor contract terms, cross-border transfer conditions, 72-hour breach notification to SDAIA | `personal-data-protection-law.md` |
| Non-compete and non-solicit (commercial) | No statutory bar; reasonableness under general contract rules; employment non-competes are capped at two years and must be written | `civil-transactions-law.md` general rows; `labor-law.md` Art. 83 |
| Confidentiality survival | Confidentiality and dispute-resolution clauses survive termination by statute | `civil-transactions-law.md` Art. 113 |
| Auto-renewal | Not statutorily regulated for B2B contracts; treat as a drafting point, not a statutory-override point | `civil-transactions-law.md` (absence row) |
| Contract language | Arabic prevails in any Saudi forum; a bilingual contract should state which text governs | Practice `[model knowledge — verify]`; `commercial-courts-law.md` (language of proceedings) |
| Currency for thresholds | SAR | `MANIFEST.md` |
| Calendar for deadlines | Friday-Saturday weekend; Eid al-Fitr, Eid al-Adha, National Day, Founding Day; Hijri dates on official instruments | `MANIFEST.md` |

## Corporate (entity compliance, diligence, consents)

| Field | Default | Basis |
|---|---|---|
| Entity types offered | LLC (شركة ذات مسؤولية محدودة), JSC (شركة مساهمة), simplified JSC (شركة مساهمة مبسطة), general partnership, limited partnership, branch of a foreign company, professional company | `companies-law.md` |
| Registry identifiers captured | Commercial registration number (one national CR), MISA investment registration certificate, UBO filing status, ZATCA number, GOSI number, Qiwa establishment number, Chamber membership, municipal licence | `commercial-register-law.md`, `investment-law.md`, `ultimate-beneficial-ownership-rules.md`, `filing-calendar.md` |
| Filing calendar | From `filing-calendar.md`, indexed by entity type then authority; rows tagged model knowledge must be confirmed with the company's accountant before they drive an alert | `filing-calendar.md` |
| Diligence categories added | Tasattur exposure, MISA registration validity and activity match, Saudization band, GOSI arrears, ZATCA standing, UBO filing, merger-control thresholds, Commercial Agencies registration | `anti-concealment-law.md`, `investment-law.md`, `saudization-nitaqat.md`, `social-insurance-law.md`, `filing-calendar.md`, `ultimate-beneficial-ownership-rules.md`, `competition-law.md`, `commercial-agencies-law.md` |
| Board and shareholder formalities | Resolutions by circulation, notice periods, quorum and majorities from the Companies Law and the articles; listed companies add the CMA regulations | `companies-law.md`, `corporate-governance-regulations.md` |
| Listed-company regulator | CMA / Tadawul | `corporate-governance-regulations.md` |

## Labor (termination, hiring, classification, leave, policies)

| Field | Default | Basis |
|---|---|---|
| Contract types | Fixed-term (Arabic, documented on Qiwa) and indefinite; conversion and renewal rules per the Law | `labor-law.md` Arts. 51-58 |
| Probation | Up to 180 days total, in writing | `labor-law.md` Art. 53 |
| Notice on indefinite contracts | Employer 60 days, worker 30 days (monthly-paid) | `labor-law.md` Art. 75 |
| End-of-service award | Half a month's wage per year for the first five years, one month per year after, last wage as base, resignation fractions | `labor-law.md` Arts. 84-87 |
| Compensation for invalid termination | 15 days' wage per year of service (indefinite) or the remaining term (fixed), minimum two months, unless the contract fixes a figure | `labor-law.md` Art. 77 |
| Termination without award or notice | Only on the Art. 80 grounds after hearing the worker | `labor-law.md` Art. 80 |
| Non-compete | Written, maximum two years, limited to what protects a legitimate interest | `labor-law.md` Art. 83 |
| Working time | 8 hours a day or 48 a week; 6 and 36 in Ramadan for Muslims; overtime at hourly wage plus 50% | `labor-law.md` Arts. 98-108 |
| Leave | Annual 21 days rising to 30 after five years; sick leave 30 full, 60 three-quarters, 30 unpaid; maternity 12 weeks; paternity, marriage, bereavement, Hajj, exam leave per the Law | `labor-law.md` Arts. 109-117, 151-160 |
| Dispute route | Friendly settlement at HRSD, then the Labor Courts; 12-month limitation | `labor-dispute-route.md` |
| Saudization | Nitaqat band and profession quotas checked before every hire | `saudization-nitaqat.md` |
| Social insurance | GOSI registration for every worker; contribution rates by law and transitional schedule | `social-insurance-law.md` |
| Platforms | Qiwa contract documentation, Mudad wage files, work-permit renewals | `platform-obligations.md` |
| Work regulations | Employer's work regulations follow the HRSD model and need certification or approval | `labor-law-implementing-regulations.md` |
