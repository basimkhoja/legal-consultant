# Scenario results — corporate-legal — Claude Code

| Field | Value |
|---|---|
| Runtime | Claude Code (Claude Agent SDK), model claude-fable-5-1, this session |
| Date | 2026-09-04 |
| Plugin | `corporate-legal` |
| Scenarios | COR-01, COR-02, COR-03, COR-04, ALL-01 (corporate part only) |
| Staged homes | `LEGAL_CONSULTANT_HOME=<scratchpad>/homes/ksa` (COR-01..04), `<scratchpad>/homes/gbr` (ALL-01) |
| Jurisdiction tree | `references/jurisdictions/` at the repo root (verified identical to `corporate-legal/references/jurisdictions/` by `diff -r`) |
| Portal probe (live) | `python3 scripts/fetch-law.py --portal boe --index` → returned the law index (first row `5535039e-… Arbitration Law ( Old )`): laws.boe.gov.sa ✓ reachable at 2026-09-04 |
| Portal probe (COR-04, blocked) | `https_proxy=http://127.0.0.1:9 python3 scripts/fetch-law.py --portal boe --index` → `fetch failed … curl: (7) Failed to connect to 127.0.0.1 port 9` |
| Files written | `tests/results/2026-09-04-claude-code-corporate-legal.md` (this file); `<scratchpad>/homes/ksa/corporate-legal/entities/compliance-tracker.yaml` (COR-03). Nothing else in the repo or the real home was touched. |

## Summary

| ID | Skill | Result | Notes |
|---|---|---|---|
| COR-01 | `diligence-issue-extraction` | **PASS** | All 9 overlay findings present with file cites and tags; Tasattur 🔴; disclaimer + Arabic findings table; no forbidden item. Friction: skill's "ask which deal" pre-condition (deal-context.md absent) had to be recorded rather than waited on. |
| COR-02 | `written-consent` | **PASS** | Bilingual قرار بالتمرير; Arts. 166 / 165 / 172 cited from `companies-law.md`; e-signature from `electronic-transactions-law.md` with `[review]`; articles clause cited as a placeholder because the articles are not on file (skill's own instruction). Skill-text issue found (Art. 166 "written request defeats it" claim not in the file row). |
| COR-03 | `entity-compliance --init` then `--report --days 90` | **PASS** | Tracker uses `jurisdiction_code: ksa`, `entity_type_local`, `registry_number`; LLC (Arts. 165/167) and JSC (Arts. 88/121-122) rows differ; ZATCA/GOSI/Qiwa rows `status: unconfirmed`; dates rolled back against the Friday-Saturday weekend. Skill-text inconsistency found on the UBO row's tag. |
| COR-04 | `diligence-issue-extraction` (portal blocked) | **PASS** | Fetch attempted through `scripts/fetch-law.py`, exit code 3 reported verbatim, options offered, run stopped; nothing tagged `[BOE — Arabic]`; losses-rule finding marked pending; reviewer note records the unreachable portal. |
| ALL-01 (corporate) | `entity-compliance --init` with `gbr` primary | **PASS** | `gbr/MANIFEST.md` → `populated: no` → stop message and three options; no tracker written; no UK, Saudi or US rule applied. |

Skill-text fixes needed (none caused a FAIL; listed at the end under "Skill-text observations").

---

## COR-01 — LLC diligence run

### Transcript summary

- Read: `tests/scenarios/COR-01-llc-diligence.md`; `corporate-legal/CLAUDE.md` (template + guardrails); staged profile `homes/ksa/corporate-legal/CLAUDE.md` and `homes/ksa/company-profile.md`; `corporate-legal/skills/diligence-issue-extraction/SKILL.md` (no `references/` folder exists under the skill); input `tests/fixtures/inputs/COR-01-data-room.md`.
- Step 0: profile `## Jurisdiction` → primary `ksa`, footprint none, bilingual output, SAR, portal laws.boe.gov.sa. Matter facts: target incorporated in `ksa`, customer contracts governed by Saudi law, German and French counterparties do not add a governing-law code → codes applied: `ksa` only. Read `references/jurisdictions/ksa/MANIFEST.md` (`populated: yes`), `INDEX.md`, then the rows of the files the skill names: `companies-law.md`, `anti-concealment-law.md`, `investment-law.md`, `saudization-nitaqat.md`, `platform-obligations.md`, `social-insurance-law.md`, `filing-calendar.md`, `ultimate-beneficial-ownership-rules.md`, `competition-law.md`, `commercial-agencies-law.md`, `civil-transactions-law.md`, `commercial-register-law.md`, `electronic-transactions-law.md`, `personal-data-protection-law.md` (row list only), `bankruptcy-law.md` (row list only). `corporate-governance-regulations.md` not loaded (target unlisted).
- Pre-flight: portal probe run (`fetch-law.py --portal boe --index`) → reachable. No article fetched (no rule needed quoting in this scenario). No web search run.
- Matter workspaces: `Enabled ✗` (in-house) → practice-level context.
- Load context: `deals/[code]/deal-context.md` does not exist in the staged home. Skill text says "ask which deal this is for"; the scenario supplies the deal inline, so the run recorded the question in the reviewer note and used deal code `TFS` (Target Fleet Services Co.) rather than blocking.
- Steps 1-5 run: inventory, materiality filter (contracts above SAR 500,000), Step 2.5 `ksa` overlay, extraction, findings in house format (R/Y/G scheme mapped onto the canonical 🔴/🟠/🟡/🟢 scale, rounding up), assembly with header, disclaimer, bilingual bottom line and findings table, gaps, handoffs, decision tree, dashboard offer.

### Deliverable

~~~~markdown
> **⚠️ Reviewer note**
> - **Sources:** portal: laws.boe.gov.sa ✓ reachable (`scripts/fetch-law.py --portal boe --index`, 2026-09-04); no article fetched this session — every rule cite below carries the tag of its row in `references/jurisdictions/ksa/`; upstream connectors (CourtListener/Westlaw) not probed because `usa` is not in the footprint.
> - **Read:** all 9 items in the data-room index (synthetic extracts, not full documents — the three customer contracts and the management, distribution and articles texts were read only as extracted).
> - **Flagged for your judgment:** 11 items marked `[review]` inline.
> - **Currency:** could not search (no web search run this session). Two currency points are flagged inline `[model knowledge — verify]`: the Nitaqat 2026-2028 phase and the April-2026 Qiwa-documentation credit rule.
> - **Before relying:** (1) have external Saudi counsel read the management agreement in full against Anti-Concealment Law Arts. 2-4 and 15 — Issue #1 decides deal structure; (2) obtain the target's MISA annual-update confirmation for 2026 and the current MISA excluded-activities list before treating Issue #2 as closed.
> - **Jurisdiction:** ksa; files: MANIFEST.md, INDEX.md, companies-law.md, anti-concealment-law.md, investment-law.md, saudization-nitaqat.md, platform-obligations.md, social-insurance-law.md, filing-calendar.md, ultimate-beneficial-ownership-rules.md, competition-law.md, commercial-agencies-law.md, civil-transactions-law.md, commercial-register-law.md, electronic-transactions-law.md, personal-data-protection-law.md, bankruptcy-law.md; portal fetched: no; unpopulated codes: none.
> - **Deal context:** no `deals/<code>/deal-context.md` in the profile home — the skill asks which deal this is for; deal code `TFS` assumed from the index title. Materiality and side taken from the practice profile (buy-side; contracts above SAR 500,000; litigation all pending).

RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY, SOLICITOR, BARRISTER, OR OTHER AUTHORISED LEGAL PROFESSIONAL IN YOUR JURISDICTION BEFORE ACTING
Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance. / النص العربي هو النص المعتمد، والترجمة الإنجليزية للاستئناس فقط، ويجب مراجعة محامٍ سعودي مرخص قبل الاعتماد على هذا المستند.

> This output is derived from VDR materials that are privileged, confidential, or both. It inherits the source's privilege and confidentiality status — distribution beyond the privilege circle can waive privilege. Store with the matter's privileged files and make distribution decisions deliberately.

# Diligence Issues: TFS — All categories (Corporate, Contracts, Employment, Regulatory, Litigation, IP, Data)

**Documents reviewed:** 9 of 9 in the index
**Coverage:** All; contracts above SAR 500,000 annual value (all three customer contracts qualify at > SAR 800,000 each)
**Findings:** 2🔴 4🟠 3🟡 0🟢
**Jurisdiction:** ksa; files: companies-law.md, anti-concealment-law.md, investment-law.md, saudization-nitaqat.md, platform-obligations.md, social-insurance-law.md, filing-calendar.md, ultimate-beneficial-ownership-rules.md, competition-law.md, commercial-agencies-law.md, civil-transactions-law.md, commercial-register-law.md; portal fetched: no; unpopulated codes: none

---

### Attorney brief (for the non-lawyer reader — take this to External Saudi counsel)

1. **The management agreement (doc 6) may make the target a concealment ("tasattur") vehicle.** The German partner runs everything, controls the bank accounts and takes 95% of profit while holding 49% and a MISA registration that covers only "IT consulting". If the arrangement is concealment, the agreement is void, the company can be dissolved and both partners face up to five years' imprisonment and SAR 5,000,000. This is a structure question, not a price question.
2. **Three customer contracts (all above SAR 800,000 a year) let the customer walk on a change of control.** Consents or waivers from all three are closing deliverables.
3. **Four regulatory arrears sit behind the deal:** the MISA registration's activity mismatch and possibly lapsed annual update; SAR 210,000 of unpaid GOSI contributions (which blocks commercial-register changes); an unregistered distribution agreement (which, for a company with a foreign partner, can lead to administrative liquidation); and accumulated losses at 56% of capital, which required a partners' assembly within 60 days.
4. **Ask before advising:** the buyer's and target's last audited revenue (merger-control test), the German partner's own ownership chain (UBO test), the target's UBO filing, the 2026 MISA update confirmation, the articles in full, and the employees' wage data.

---

### Bottom line

[🔴 2 blocking · 🟠 4 high · 🟡 3 medium] — Do not sign on the current structure: the 95%-profit management agreement is a Tasattur indicator that puts the target's existence, not just its price, at risk; the three change-of-control termination rights and the GOSI, MISA, agency-registration and losses-rule arrears are pre-closing deliverables, not post-closing covenants.

**الخلاصة:** [🔴 2 مانع · 🟠 4 مرتفع · 🟡 3 متوسط] — لا يُنصح بالتوقيع على الهيكل الحالي: اتفاقية الإدارة التي تمنح الشريك غير السعودي 95% من الأرباح والسيطرة على الحسابات البنكية مؤشر تستر يعرّض وجود الشركة المستهدفة للخطر لا سعرها فقط؛ كما أن حقوق الإنهاء عند تغيير السيطرة في العقود الثلاثة، ومتأخرات التأمينات الاجتماعية، وتسجيل الاستثمار لدى وزارة الاستثمار، وقيد الوكالة التجارية، وقاعدة الخسائر، كلها متطلبات يجب استيفاؤها قبل الإتمام لا تعهدات لاحقة له.

**One question I'd ask that isn't in my checklist:** who has actually been signing the target's bank instructions and Qiwa/GOSI filings for the last three years — Mr. A, Mr. B, or someone at Overseas Fleet GmbH? The management agreement says who is *entitled* to control; the bank mandates and platform logs show who *did*, and that is what a Ministry inspector under Anti-Concealment Law Art. 4(a)-(c) will read.

---

## Findings

### Corporate

**Issue #1: Tasattur (commercial concealment) exposure from the management agreement** `[ksa]`
Category: Corporate / Regulatory
Severity: 🔴 Red — Blocking (affects deal structure)
Documents: /06 Management agreement (2023); /01 CR extract; /03 MISA certificate
Finding: Overseas Fleet GmbH (Germany, 49%) "shall manage all operations of the Company, control its bank accounts and receive 95% of net profits as a management fee"; Mr. A (Saudi, 51%) "shall have no role in management and receives a fixed annual amount of SAR 60,000". Tested against the three elements of Art. 2 (an agreement or arrangement; a non-Saudi practising an activity it is not licensed to practise; use of the Saudi party's licence, CR or name) — `anti-concealment-law.md` Art. 2 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` — the arrangement is caught on its face for "fleet management services", which is on the CR (doc 1) but not on the MISA certificate (doc 3): for that activity the non-Saudi partner is not "licensed to practise it" under the Investment Law row (Art. 7(2): a foreign investor must register before investing; registration covers the activities registered) — `anti-concealment-law.md` Investment Law interplay row `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`. (Plain English: the German partner is running a business line it never registered for, through the Saudi partner's licence.) For "IT consulting", which the registration does cover, the 95% profit entitlement and total control still map to the Art. 4(a)-(b) administrative violations (instruments giving a non-Saudi absolute disposal over the establishment) and to the Diligence checklist indicators (c) de facto ownership rights in a side agreement and (a) sole bank control — `anti-concealment-law.md` Art. 4 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`; Diligence checklist row `[model knowledge — verify]`; whether a registered investor taking more than its registered share is itself concealment is not settled by the text `[model knowledge — verify]` `[review]`. Consequences: Art. 15 — "every contract or act whose object or purpose is tasattur is void", so the management agreement and the profit split are unenforceable and the target's profit entitlement is unsettled `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`; Art. 9 — imprisonment up to five years and/or fine up to SAR 5,000,000 per convicted person, doubled on recidivism; Art. 12 — dissolution of the establishment, cancellation of licences, deletion of the CR, five-year trade ban, joint liability of both convicted parties for zakat, taxes and fees; Art. 14 — for an Art. 4 violation, fine up to SAR 500,000 and/or closure up to 90 days, plus a possible five-year reporting order that survives a share sale — all `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`. Art. 3(c) exposes advisers who knowingly assist `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`. Cross-check: the CR names a German national (Mr. B) as manager — a non-Saudi general manager is an overlay trigger; his registered powers should be read from the CR extract (`commercial-register-law.md` Art. 6(e) `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`).
Recommendation: Walk or restructure. Do not acquire the vehicle while the management agreement stands: require (i) termination and unwinding of the 2023 agreement before signing, with distributions since 2023 reconciled to the registered 51/49 split; (ii) a MISA registration amendment adding "fleet management services" (Issue #2); (iii) a specific indemnity from both sellers for Anti-Concealment Law and joint-tax exposure (Art. 12), backed by escrow; (iv) confirmation that the target is not under an Art. 14 reporting order. Escalate to the Legal Lead and External Saudi counsel now `[review]`.

**Issue #2: MISA investment registration — activity mismatch and possibly lapsed annual update** `[ksa]`
Category: Regulatory
Severity: 🟠 High
Documents: /03 MISA certificate; /01 CR extract
Finding: The certificate (issued 2024-08-01, "valid one year, renewed 2025-08-01") covers "IT consulting" only; the CR also lists "fleet management services". Diligence checklist item (2): CR activities must match the activities registered with MISA (Reg. Art. 11(2)(b)) — a mismatch is an Art. 7 violation — `investment-law.md` Diligence checklist row `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` (Law); `[authority — MISA]` (Reg.). Annual update: the registered investor must file an annual update; window 60 working days before the due date, 30 working days' grace, reactivation within three years, then re-registration — Reg. Art. 13 `[settled — last confirmed 2026-09-04]` `[authority — MISA]`. Nothing in the VDR evidences the 2026 update (anniversary 2026-08-01 fell on a Saturday; the working-day grace is still running as at 2026-09-04) `[review]`. (Plain English: the German partner's investment permit may have quietly expired last month, and it never covered half the business.) The certificate's own "valid one year" wording is `[user provided]`; the Law sets no term. Sanction tier: activity mismatch and lapse are Art. 7 breaches; a non-serious breach gets a remedy period of not less than 30 working days (Reg. Art. 28); serious violations (Reg. Art. 30) — investing without registration, unapproved ownership change in a restricted activity — carry warning, fine up to SAR 300,000 (doubled on repetition) or cancellation of registration — Art. 11 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` (Law); `[authority — MISA]` (Reg.). Ownership change: if either activity is on the excluded list as *restricted*, the share transfer needs prior Examination Committee approval (Art. 8(3); Reg. Art. 20) — the excluded-activities list row is `[model knowledge — verify]`, so no activity is classified here; obtain the current list from MISA's Investor Guide `[review]`. The buyer's own Art. 7(2) registration/update is a parallel closing item.
Recommendation: Condition precedent: MISA registration amended to add the second activity and 2026 annual update confirmed; excluded-list classification obtained; Art. 8(3) approval if restricted. Rep and warranty on registration compliance since 2024-08-01. Hand to closing-checklist.

**Issue #3: Share-transfer restrictions (pre-emption) and the losses rule** `[ksa]`
Category: Corporate
Severity: 🟠 High
Documents: /02 Articles (Arts. 9, 14); /09 Financial statements FY2025; /01 CR extract
Finding: (a) Pre-emption — the articles' Art. 9 (30-day first offer to the other partners at the same price) tracks the statutory rule: a third-party transfer needs manager-routed notice and a 30-day redemption window, or written waivers from every non-selling partner; the articles may lengthen the period — `companies-law.md` Art. 178 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` `[BOE — official English]`. Ownership passes only on registration with the Commercial Register — Art. 25 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` — so the closing deliverable is the registered amended articles, not the signed transfer. (b) Majorities — the articles' Art. 14 requires 75% for partners' decisions and unanimity for amendments; the statutory floor is ≥ 75% of capital for amendments (Art. 172 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`), so the articles are stricter: both partners must sign the amended articles and any change to Art. 9 or Art. 14 `[review]`. Written amendments and Commercial Register registration are mandatory (Art. 8; Regs Art. 2 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` `[authority — MoC]`). (c) Losses rule — accumulated losses SAR 280,000 against capital SAR 500,000 = 56% `[computed — companies-law.md Art. 182, settled 2026-09-04; inputs: accumulated losses SAR 280,000, capital SAR 500,000, entity type LLC]`, above the half-capital trigger: the manager must call the partners' assembly within 60 days of learning of it to decide continuation or dissolution — Art. 182 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` `[BOE — official English]`; failure to call it is an offence for the manager (imprisonment up to one year and/or fine up to SAR 1,000,000) — Art. 261 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`. No assembly minutes or Art. 165 minutes register in the VDR `[review]`. (Plain English: the company has lost more than half its capital, which by law forces a partners' meeting the file shows no sign of.) The 2022 Law does not impose automatic dissolution or partner liability for the debts `[model knowledge — verify]` per the file row.
Recommendation: Closing checklist: Art. 178 waivers (or expiry of the window) from the non-selling partner; unanimous amended articles registered (Art. 25); evidence of the Art. 182 assembly or a pre-closing recapitalisation / Art. 176 loss-absorbing reduction; request the Art. 165 minutes register and the full articles.

**Issue #4: Ultimate beneficial ownership — filing status not evidenced; tier-2 control points at the non-Saudi partner** `[ksa]`
Category: Corporate / Regulatory
Severity: 🟡 Medium
Documents: /01 CR extract; /06 Management agreement
Finding: No UBO register, initial-disclosure acknowledgement or annual confirmation is in the VDR — request all three plus every 15-day update since (Diligence implication row `[model knowledge — verify]`). Tier 1 (ownership): Mr. A holds 51% directly → UBO — method `[settled — last confirmed 2026-09-04]` `[authority — MoC]` (Rules Art. 4(1)), number `[computed from user-supplied cap table: CR extract 51%]`; Overseas Fleet GmbH holds 49% — its own natural-person owners are UBOs only after multiplying through its chain (49% × their holding, aggregated per person, tested at 25%); the German cap table is not in the VDR, so the tier-1 result for that side is *not computed* — ask. Tier 2 (effective control): the management agreement gives Overseas Fleet GmbH control of all operations and bank accounts, so the natural persons who control Overseas Fleet GmbH are UBOs under Rules Art. 4(2) whatever the 25% arithmetic says `[settled — last confirmed 2026-09-04]` `[authority — MoC]`; a filing that names only Mr. A would mismatch the facts — a Rules breach (Companies Law Art. 262, fine up to SAR 500,000, attaching to the company and any official — Penalties row `[settled — last confirmed 2026-09-04]` `[authority — MoC]`) and a direct Tasattur cross-check (Issue #1). Post-closing: UBO update within 15 days of completion (Change notification row `[settled — last confirmed 2026-09-04]` `[authority — MoC]`). LLCs are inside the Rules (Scope row).
Recommendation: Pre-closing: obtain the filings and reconcile them to the tier-1 computation and the management agreement; each shareholder of record to confirm it holds for its own account or give its nominee disclosure (Nominee row `[settled — last confirmed 2026-09-04]` `[authority — MoC]`). Post-closing checklist: 15-day UBO update in parallel with the CR Art. 10 update and the MISA Reg. Art. 13 update.

**Issue #5: Corporate records and filing standing for FY2025 not evidenced** `[ksa]`
Category: Corporate
Severity: 🟡 Medium (gap — listed under Gaps; no severity beyond the sanction cited)
Documents: none responsive
Finding: For FY2025 (assumed calendar year `[review]`) the LLC should show: annual assembly within six months of year end (Art. 165) and financial-statements deposit within six months (Art. 17; Regs Art. 5), both by 2026-06-30 `[computed — companies-law.md Arts. 17, 165, settled 2026-09-04; inputs: fiscal year end 2025-12-31 assumed]`; CR annual confirmation (Commercial Register Law Art. 11; suspension after 90 days + 14-day warning, Art. 15) — all `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`; the due date of the CR confirmation is `[model knowledge — verify]` (Regulations not read). Sanction for a late assembly or undeposited statements: Companies Law Art. 262(b), (e), fine up to SAR 500,000, on the manager as well as the company. ZATCA zakat/tax return (FYE + 120 days) and VAT/WHT/e-invoicing standing: `[model knowledge — verify]` — confirm with the accountant.
Recommendation: Request: CR active-status extract dated within the last few weeks, FY2025 assembly minutes, deposit receipt, ZATCA certificate. Any suspension (Art. 15) is a critical finding.

### Regulatory

**Issue #6: Social-insurance (GOSI) arrears — SAR 210,000 for three months** `[ksa]`
Category: Regulatory / Employment
Severity: 🟠 High
Documents: /04 GOSI statement (2026-08); /05 Qiwa page
Finding: Outstanding contributions of SAR 210,000 including late-payment charges. The employer alone is liable to GOSI; late payment attracts a 2% fine per month or part of a month, uncapped in the Law — `social-insurance-law.md` Art. 9 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`. Art. 10: government bodies and state-owned companies must require a GOSI certificate before the employer can collect dues, bid, **amend, renew or cancel its commercial register**, or recruit from abroad `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` — so the arrears sit in front of the Art. 25 registration of the share transfer (implementation through MoC/Qiwa integrations is `[model knowledge — verify]`). (Plain English: the government will not process the share transfer while GOSI is owed money.) Art. 11: contributions and fines are secured by a lien ranking immediately after wages, enforceable on certified schedules without a merits judgment `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`. Art. 59: fines up to SAR 50,000 per violation, multiplied per contributor, doubled on repeat; fictitious registration ("ghost Saudis") penalised; five-year limitation from the violation — so the look-back is five years of GOSI filings `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`. Headcount reconciliation: GOSI 42 registered workers = Qiwa 42; Saudi count on Qiwa 9 — reconcile to GOSI Saudi registrations and payroll (payroll not in VDR).
Recommendation: Pre-closing deliverable: arrears settled, GOSI compliance certificate (شهادة الالتزام) and statement of account; price adjustment or escrow for the 2% accrual; rep on five-year GOSI compliance. Hand to closing-checklist.

**Issue #7: Nationalisation (Nitaqat) band Low Green and two undocumented Saudi contracts** `[ksa]`
Category: Regulatory / Employment
Severity: 🟡 Medium
Documents: /05 Qiwa establishment page (2026-08); /04 GOSI statement
Finding: Band Low Green from a dated Qiwa export (2026-08) — taken from the export, not inferred. Consequences: an entity in Low Green cannot apply for new expatriate visas or change occupations, but can renew existing work permits — `saudization-nitaqat.md` Services-by-Range row `[settled — last confirmed 2026-09-04]` `[authority — HRSD]`; a non-Saudi may not work without a work permit, and the Ministry may refuse renewal where the employer breaches localisation standards — Labor Law Arts. 33, 35 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`. With 33 of 42 workers non-Saudi (Saudi rate 21.4% `[computed — inputs: 9 Saudi of 42 workers per the Qiwa page]`), a growth freeze is material for a services target `[review]`. Saudis needed for Medium Green: **not computed** — the coefficients in the file are the 2023-2024 values and the 2026-2028 phase (from 26 April 2026, as claimed) superseded them `[model knowledge — verify]`; take the number from the Qiwa Nitaqat calculator/dashboard `[model knowledge — verify]` for its location. Two Saudi employees' contracts are not documented on Qiwa: documentation is a statutory duty — Labor Law Art. 51 (as amended by M/44) with Regulation Art. 18(2) — `platform-obligations.md` `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` (Art. 51) / `[authority — HRSD]` (Reg. Art. 18); exposure Art. 229: fine up to SAR 100,000 per person, closure — ceiling SAR 200,000 `[computed — labor-law Art. 229 via saudization-nitaqat.md, settled 2026-09-04; inputs: 2 undocumented contracts stated in the Qiwa page]`; the schedule amount actually charged is `[model knowledge — verify]`; loss of Nitaqat credit for undocumented Saudi contracts from April 2026 `[model knowledge — verify]`. Recruitment suspension (Regulation Art. 14 First item 12): none evidenced `[settled — last confirmed 2026-09-04]` `[authority — HRSD]`. Deal structure: a share sale with the CR retained is a "name amendment", not a transfer of services — no worker-by-worker Qiwa transfers and no consumption of the buyer's Nitaqat headroom — Regulation Art. 14 Second items 19-20 `[settled — last confirmed 2026-09-04]` `[authority — HRSD]`; an asset deal into a new CR would need each expatriate's consent and the receiving entity's band. Twelve months of WPS compliance: not in VDR `[model knowledge — verify]` — request.
Recommendation: Pre-closing: document the two contracts on Qiwa; obtain a Qiwa export showing the Saudis needed for Medium Green and price the hiring plan; keep a share-deal structure (item 19-20) unless Issue #1 forces a new vehicle `[review]`.

**Issue #8: Distribution agreement with EuroTrack S.A. not registered on the Commercial Agencies Register** `[ksa]`
Category: Contracts / Regulatory
Severity: 🟠 High
Documents: /07 Distribution agreement (2022); /01 CR extract
Finding: Distributors are inside the Commercial Agencies Law ("whether as agent or as distributor in any form") — Added Art. 1 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`. No one may carry on the work of an agent unless entered in the Ministry of Commerce register — Art. 3 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`; the three-month application deadline is `[model knowledge — verify]`. Missing registration is a regulatory breach by the target, not a validity defect: amended Art. 4 fines SAR 5,000-50,000 with publication and preserves civil claims; **where the violation is attributed to a Saudi company with one or more non-Saudi partners — which this target is — the penalty is in addition the administrative liquidation of the business, with a possible trade ban, and referral of the non-Saudi partner to the Minister of Interior** `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`; enforceability of the unregistered contract between the parties `[model knowledge — verify]`. (Plain English: an unregistered distributorship is normally a small fine, but for a company with a foreign partner the Law also allows the business to be wound up.) Art. 1: on its face a company with a non-Saudi partner cannot be a commercial agent at all; the Ministry's relaxation for MISA-registered companies is `[model knowledge — verify]` `[review]`. After-sales: the distributor must secure spare parts and maintenance throughout the agency and for one year after it ends — Added Art. 2 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`; allocation with the principal not visible in the extract. Exclusivity: screen the exclusive-distribution terms against the Art. 5 note row of `competition-law.md` (vertical restraints are "between establishments") `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`.
Recommendation: Pre-closing: registration application (or a reasoned counsel opinion on the Art. 1 position); confirm the agreement's term, territory and after-sales allocation; rep and specific indemnity for Art. 4 exposure. Post-closing: register update on change of ownership `[model knowledge — verify]`.

**Issue #9: Merger-control threshold — cannot be concluded; revenue inputs missing** `[ksa]`
Category: Regulatory
Severity: 🟡 Medium (pending inputs)
Documents: /08 Customer contracts (revenue floor only); /09 FY2025 extract
Finding: Notification to GAC is required at least 90 days before completion where the three cumulative tests are met: (A) worldwide sales of all participating entities > SAR 200 million; (B) target worldwide sales > SAR 40 million; (C) Saudi sales of all parties > SAR 40 million — `competition-law.md` Art. 7 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`; Reg. Art. 12 and Guidelines s.6 `[authority — GAC]`. Participating entities are the buyer's whole group plus the target, not the seller, measured on the last audited statements (Guidelines s.6 `[authority — GAC]`). Inputs: the buyer group's revenue is not in the profile and the target's revenue is not in the FY2025 extract; the three customer contracts give a floor of SAR 2,400,000 `[computed — inputs: 3 contracts each above SAR 800,000 per year]`, which says nothing about test (B). **No conclusion is drawn** — ask for both revenue figures. Gun-jumping: completing before clearance breaches Art. 11; fine up to 10% of the sales subject of the violation or SAR 10 million, unwinding possible — Art. 19(1), Art. 21 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`. Fee 0.02% of participating sales capped at SAR 250,000 `[authority — GAC]`. Dominance screen: combined share ≥ 40% in any Saudi market signals remedies risk (Art. 6 / Reg. Art. 10 `[BOE — Arabic]` / `[authority — GAC]`) — telematics market shares not in VDR.
Recommendation: Get more facts (revenues); if tests met, GAC filing is a condition precedent with a 90-day clock; pre-notification two weeks before filing (Guidelines s.7 `[authority — GAC]`).

### Contracts

**Issue #10: Change-of-control termination rights in all three material customer contracts; assignment position** `[ksa]`
Category: Contracts
Severity: 🔴 Red — Blocking (change of control requiring major customer consent)
Documents: /08 Customer contracts (three, each above SAR 800,000 per year; Saudi law)
Finding: Each contract: "Customer may terminate this Agreement on written notice if there is a change in the control of Supplier." A share sale does not by itself transfer or terminate the target's contracts — the company remains the party — so a change-of-control right exists only because it was drafted, and here it was — `civil-transactions-law.md` Arts. 98-99 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`. All three exceed the SAR 500,000 materiality threshold; together they are at least SAR 2,400,000 of annual revenue at the customers' option. Assignment (relevant only if the structure moves to an asset deal): transfer of a party's position needs the counterparty's consent; advance consent is valid if it identifies the contract and takes effect on notice; absent release the assignor stays jointly liable — Arts. 255-258 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`. One contract's "assign to affiliates without consent" clause is the Art. 255 advance consent (affiliates only); the two silent contracts need consent for any assignment. Contract dates are not in the extract: contracts dated before 16 December 2023 remain governed by the Law unless a party pleads a contrary settled judicial principle — Royal Decree M/191 para. Fifthly `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` `[review]`. Penalty/claw-back terms not visible in the extract (Arts. 178-179, 183) — request full texts.
Recommendation: Consents or written waivers from all three customers as closing deliverables (or a covenant with a revenue-based price adjustment); hand to closing-checklist and material-contract-schedule.

### Employment

**Issue #11: Employment set — end-of-service accrual not computable; workforce continuity** `[ksa]`
Category: Employment
Severity: 🟡 Medium (pending inputs)
Documents: /04 GOSI; /05 Qiwa
Finding: End-of-service award accrual per employee — formula 0.5 × W × min(S, 5) + W × max(S − 5, 0) on the last wage (`labor-law.md` Arts. 84-87 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` as carried in the skill) — **not computed**: no wage or service data in the VDR; ask for the payroll and hire dates for 42 workers. Transfer of the establishment: on a change of ownership contracts continue, service is continuous, and successor and predecessor are jointly liable for accrued rights — Art. 18 (per the skill's file list; row not re-read this session) `[model knowledge — verify]` for the exact wording. Qiwa treatment of the share deal: Issue #7. Work permits and occupation matches for 33 non-Saudis (Art. 33): not in VDR — gap.
Recommendation: Get the payroll; aggregate the award as a liability finding in SAR; request permit list.

### Litigation / IP / Data / Government contracts / Insolvency

No responsive documents — see Gaps.

---

## Findings table

| # | Issue | Severity | Category | Rule (file · article · tag) | Action |
|---|---|---|---|---|---|
| 1 | Tasattur exposure — 95%-profit management agreement | 🔴 | Corporate/Regulatory | anti-concealment-law.md Arts. 2, 3, 4, 9, 12, 14, 15 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`; Investment Law row; checklist row `[model knowledge — verify]` | Restructure or walk; unwind agreement; indemnity + escrow |
| 2 | MISA registration — activity mismatch; 2026 update not evidenced | 🟠 | Regulatory | investment-law.md Art. 7(2), Reg. Art. 13, Art. 8(3), Reg. Art. 30, Art. 11 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` / `[authority — MISA]`; excluded list `[model knowledge — verify]` | CP: amended registration + update confirmation |
| 3 | Pre-emption, unanimity in articles, losses at 56% | 🟠 | Corporate | companies-law.md Arts. 178, 25, 172, 8, 182, 261 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` | Waivers; registered amended articles; Art. 182 assembly or recapitalisation |
| 4 | UBO filing not evidenced; tier-2 control | 🟡 | Corporate/Regulatory | ultimate-beneficial-ownership-rules.md Rules Art. 4(1)-(2), change notification, penalties `[settled — last confirmed 2026-09-04]` `[authority — MoC]` | Obtain filings; reconcile; 15-day post-closing update |
| 5 | FY2025 corporate records / filing standing not evidenced | 🟡 | Corporate | filing-calendar.md; companies-law.md Arts. 17, 165, 262; commercial-register-law.md Arts. 11, 15 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`; ZATCA rows `[model knowledge — verify]` | Request extract, minutes, deposit receipt, ZATCA certificate |
| 6 | GOSI arrears SAR 210,000 | 🟠 | Regulatory/Employment | social-insurance-law.md Arts. 9, 10, 11, 59 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` | Settle pre-closing; certificate; escrow |
| 7 | Nitaqat Low Green; 2 undocumented Saudi contracts | 🟡 | Regulatory/Employment | saudization-nitaqat.md Services-by-Range, Arts. 33/35, 229 `[settled — last confirmed 2026-09-04]` `[authority — HRSD]`/`[BOE — Arabic]`; platform-obligations.md Art. 51 + Reg. Art. 18, Reg. Art. 14 items 12, 19-20; next-band number `[model knowledge — verify]` | Document contracts; Qiwa export for next band; keep share-deal structure |
| 8 | Distribution agreement unregistered (foreign-partner liquidation exposure) | 🟠 | Contracts/Regulatory | commercial-agencies-law.md Added Art. 1, Art. 3, amended Art. 4, Added Art. 2, Art. 1 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`; relaxation/validity `[model knowledge — verify]` | Register or counsel opinion; indemnity |
| 9 | Merger control — inputs missing | 🟡 | Regulatory | competition-law.md Art. 7, Reg. Art. 12, Guidelines s.6, Arts. 11, 19(1), 21, 40% row `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`/`[authority — GAC]` | Get revenues; file if tests met (90 days) |
| 10 | Change-of-control termination in 3 contracts > SAR 800,000 | 🔴 | Contracts | civil-transactions-law.md Arts. 98-99, 255-258, Decree para. 5 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` | Customer consents/waivers as closing deliverables |
| 11 | EOSB accrual not computable; workforce continuity | 🟡 | Employment | labor-law.md Arts. 84-87, 18 (per skill file list) `[model knowledge — verify]` for wording not re-read | Get payroll; compute in SAR |

**جدول الملاحظات (النسخة العربية)**

| # | الموضوع | الدرجة | الفئة | السند النظامي (الملف · المادة · الوسم) | الإجراء |
|---|---|---|---|---|---|
| 1 | التعرض لجريمة التستر — اتفاقية إدارة تمنح 95% من الأرباح | 🔴 مانع | حوكمة/تنظيمي | نظام مكافحة التستر، المواد 2، 3، 4، 9، 12، 14، 15 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` | إعادة الهيكلة أو الانسحاب؛ إنهاء الاتفاقية؛ تعويض وضمان محتجز |
| 2 | تسجيل الاستثمار لدى وزارة الاستثمار — عدم تطابق النشاط؛ عدم إثبات التحديث السنوي لعام 2026 | 🟠 مرتفع | تنظيمي | نظام الاستثمار، المادة 7(2)، اللائحة المادة 13، المادة 8(3)، اللائحة المادة 30، المادة 11 | شرط مسبق: تعديل التسجيل وتأكيد التحديث |
| 3 | حق الاسترداد (الأولوية)، الإجماع في عقد التأسيس، الخسائر 56% من رأس المال | 🟠 مرتفع | حوكمة | نظام الشركات، المواد 178، 25، 172، 8، 182، 261 | تنازلات الشركاء؛ قيد عقد التأسيس المعدل؛ جمعية المادة 182 أو إعادة الرسملة |
| 4 | عدم إثبات الإفصاح عن المستفيد الحقيقي؛ السيطرة الفعلية | 🟡 متوسط | حوكمة/تنظيمي | قواعد المستفيد الحقيقي، المادة 4(1)-(2)، الإشعار بالتغيير، العقوبات | الحصول على الإفصاحات والمطابقة؛ تحديث خلال 15 يومًا بعد الإتمام |
| 5 | عدم إثبات السجلات النظامية والالتزامات الدورية للسنة المالية 2025 | 🟡 متوسط | حوكمة | تقويم الالتزامات؛ نظام الشركات المواد 17، 165، 262؛ نظام السجل التجاري المادتان 11، 15 | طلب مستخرج السجل، محاضر الجمعية، إيصال الإيداع، شهادة الزكاة والضريبة |
| 6 | متأخرات التأمينات الاجتماعية 210,000 ريال | 🟠 مرتفع | تنظيمي/عمالي | نظام التأمينات الاجتماعية، المواد 9، 10، 11، 59 | السداد قبل الإتمام؛ شهادة الالتزام؛ ضمان محتجز |
| 7 | نطاق أخضر منخفض؛ عقدان سعوديان غير موثقين على قوى | 🟡 متوسط | تنظيمي/عمالي | التوطين ونطاقات (الخدمات حسب النطاق؛ المادتان 33، 35؛ المادة 229)؛ المادة 51 من نظام العمل مع المادة 18 من اللائحة | توثيق العقدين؛ مستخرج قوى لعدد السعوديين المطلوب؛ الإبقاء على هيكل بيع الحصص |
| 8 | اتفاقية توزيع غير مقيدة في سجل الوكالات التجارية (تعرض للتصفية الإدارية لوجود شريك غير سعودي) | 🟠 مرتفع | عقود/تنظيمي | نظام الوكالات التجارية، المادة الأولى المضافة، المادة 3، المادة 4 المعدلة، المادة الثانية المضافة، المادة 1 | القيد أو رأي مستشار؛ تعويض |
| 9 | التركز الاقتصادي — البيانات غير مكتملة | 🟡 متوسط | تنظيمي | نظام المنافسة، المادة 7، اللائحة المادة 12، الدليل البند 6، المواد 11، 19(1)، 21 | الحصول على الإيرادات؛ الإبلاغ قبل 90 يومًا إن تحققت الاختبارات |
| 10 | حق الإنهاء عند تغيير السيطرة في ثلاثة عقود تتجاوز 800,000 ريال | 🔴 مانع | عقود | نظام المعاملات المدنية، المواد 98-99، 255-258، البند خامسًا من المرسوم | موافقات أو تنازلات العملاء كمتطلبات إتمام |
| 11 | تعذر احتساب مكافأة نهاية الخدمة؛ استمرارية العمالة | 🟡 متوسط | عمالي | نظام العمل، المواد 84-87، 18 | الحصول على مسيّرات الرواتب؛ الاحتساب بالريال |

---

## Gaps

- Corporate: full articles of incorporation (only Arts. 9 and 14 extracted); Art. 165 minutes register; FY2025 assembly minutes and financial-statements deposit receipt; current CR active-status extract; UBO register and filings; Overseas Fleet GmbH's own ownership chain.
- Regulatory: MISA 2026 annual-update confirmation; current MISA excluded-activities list `[model knowledge — verify]`; GOSI compliance certificate; twelve months of WPS files `[model knowledge — verify]`; work-permit list for 33 non-Saudis; ZATCA certificate and returns `[model knowledge — verify]`; whether the target is under an Anti-Concealment Law Art. 14 reporting order.
- Contracts: full texts and dates of the three customer contracts and the distribution agreement (term, territory, after-sales allocation, penalties); any government contracts (none listed — `government-tenders-procurement-law.md` not applied).
- Employment: payroll, hire dates and contract forms for 42 workers (EOSB); pending HRSD friendly-settlement or Labour Court matters (`labor-dispute-route.md`).
- Litigation: no register of pending or threatened matters; Bankruptcy Register search (`bankruptcy-law.md` Art. 227) not evidenced.
- IP: no ownership chain or registrations; any registration or recordal point is `[no rule in ksa files — verify]` (no jurisdiction file covers the IP registry).
- Data: telematics processes vehicle-location personal data — no privacy policy (PDPL Art. 12), records of processing (Art. 31) or transfer mechanism for data flowing to the German parent (Art. 29; transfer regulation `[model knowledge — verify]`) in the VDR.
- Point the files do not settle: successor-liability doctrine generally — `[no rule in ksa files — verify]`; the files give only `bankruptcy-law.md` Arts. 210-212, 23, 200-203, 227, `labor-law.md` Art. 18, `civil-transactions-law.md` Arts. 98, 255-256, 252, 183 and `companies-law.md` Arts. 225-229, 231-234, none of which was triggered by a document in this VDR beyond Issues #10-11.

---

## Handoffs

- **closing-checklist:** Art. 178 waivers; unanimous amended articles registered (Art. 25); Art. 182 assembly evidence or recapitalisation; MISA amendment + 2026 update (+ Art. 8(3) approval if restricted); GOSI settlement + certificate; Commercial Agencies registration; three customer consents; GAC clearance if Issue #9 tests met; post-closing CR update within 15 days (Commercial Register Law Art. 10) and UBO update within 15 days; Qiwa "name amendment" step.
- **material-contract-schedule:** Issue #10 (three contracts) and Issue #8.
- **deal-team-summary:** Issues #1 and #10 headline.
- **ai-tool-handoff:** not triggered (no bulk-review tool configured; 9 documents).

---

**What next? Pick one and I'll help you build it out:**
1. **Draft the escalation on Issue #1** — a one-page note to the Legal Lead and External Saudi counsel with the management-agreement facts, the Arts. 2-4/15 mapping and the two structuring options (unwind pre-signing vs. walk).
2. **Escalate** — I'll draft a short escalation to the Legal Lead (then External Saudi counsel per your profile) with the key facts, the risk, and what decision is needed.
3. **Get more facts** — before advising further I'd want: the buyer's and target's last audited revenue (Issue #9); Overseas Fleet GmbH's cap table and the target's UBO filing (Issue #4); the MISA 2026 update confirmation and the current excluded-activities list (Issue #2); the full articles and the Art. 165 register (Issue #3); payroll and hire dates (Issue #11). I'll draft those as a supplemental request list to the seller.
4. **Build the closing checklist** — I'll seed `/corporate-legal:closing-checklist` with the handoff items above, each with its statutory source and tag.
5. **Watch and wait** — add to the deal tracker with a note on why and when to revisit.
6. **Something else** — tell me what you'd do with this.

📊 **See this as a dashboard?** 11 findings with severity, category and VDR source — I'll build an interactive view with summary stats (2🔴 4🟠 3🟡), a colour-coded sortable grid by house category and materiality, a severity-distribution chart, and the reviewer note carried over. In Claude Code I'll write an HTML file to the deal folder you can open in a browser; Excel on request.
~~~~

### Grading — COR-01

| # | Item | Result | Evidence |
|---|---|---|---|
| E1 | Step 0 runs; overlay adds; findings cover Tasattur (`anti-concealment-law.md`), MISA (`investment-law.md`), Nitaqat (`saudization-nitaqat.md`), GOSI (`social-insurance-law.md`), Commercial Agencies (`commercial-agencies-law.md`), UBO (`ultimate-beneficial-ownership-rules.md`), pre-emption + losses (`companies-law.md`), CoC assignment (`civil-transactions-law.md` Arts. 98/255), merger control (`competition-law.md`) | PASS | Reviewer note "Jurisdiction: ksa; files: …"; Issue #1 "`anti-concealment-law.md` Art. 2 … Art. 15"; #2 "`investment-law.md` Diligence checklist row … Reg. Art. 13"; #7 "`saudization-nitaqat.md` Services-by-Range row"; #6 "`social-insurance-law.md` Art. 9 … Art. 10 … Art. 11 … Art. 59"; #8 "Commercial Agencies Law … Added Art. 1 … Art. 3 … amended Art. 4"; #4 "Rules Art. 4(1) … Rules Art. 4(2)"; #3 "`companies-law.md` Art. 178 … Art. 182"; #10 "`civil-transactions-law.md` Arts. 98-99 … Arts. 255-258"; #9 "`competition-law.md` Art. 7 … Reg. Art. 12 and Guidelines s.6" |
| E2 | Each finding carries the file's tag; unsettled points tagged `[model knowledge — verify]` / `[no rule in ksa files — verify]` | PASS | Every cite carries `[settled — last confirmed 2026-09-04]` with `[BOE — Arabic]` / `[authority — …]`; Issue #7 "Saudis needed for Medium Green: **not computed** — … `[model knowledge — verify]`"; Gaps "IP … `[no rule in ksa files — verify]`", "successor-liability doctrine generally — `[no rule in ksa files — verify]`" |
| E3 | Canonical severity scale; Tasattur is 🔴 | PASS | "Findings: 2🔴 4🟠 3🟡 0🟢"; Issue #1 "Severity: 🔴 Red — Blocking" |
| E4 | Disclaimer and Arabic rendering of the findings table | PASS | Line under header "Arabic text is authoritative; … / النص العربي هو النص المعتمد…"; section "جدول الملاحظات (النسخة العربية)" with 11 rows; Arabic bottom line "الخلاصة:" |
| F1 | No successor-liability doctrines (de facto merger, mere continuation) | PASS | Absent; Gaps says the doctrine is `[no rule in ksa files — verify]` and lists only the file rows |
| F2 | No HSR / CFIUS | PASS | Absent (regulatory filings are GAC, MISA, MoC only) |
| F3 | No Delaware good-standing certificates | PASS | Absent; Issue #5 asks for a "CR active-status extract" |
| F4 | No "Corp/LLC" US typing | PASS | Entity typed "LLC" as the `ksa` local type from `companies-law.md`; no "Inc./Corp." |
| F5 | No dollar signs | PASS | All amounts "SAR …"; no "$" in the deliverable (grep-checked) |

**Result: PASS.**

---

## COR-02 — Written consent by circulation for an LLC decision

### Transcript summary

- Read: scenario; plugin `CLAUDE.md`; staged profile (`## Board & Secretary`: LLC, 3 managers, consent format "قرر الشركاء / RESOLVED", recital minimal, e-signatures accepted; no consents repository line); `corporate-legal/skills/written-consent/SKILL.md` (no `references/` under the skill); input: "Draft a partners' resolution approving the appointment of a new manager and the opening of a branch in Jeddah; the 20% partner is abroad and will sign electronically." Entity per scenario: one `ksa` LLC with three partners 50 / 30 / 20 (the staged profile's entity table shows "Founders 100" — the scenario's 50/30/20 split was applied and recorded).
- Gates: no same-day-signature signal → "Major action + urgency" gate not triggered; action classified **routine** (officer appointment; branch opening treated like a registered-office change) → no outside-counsel flag. No-precedent hard stop: condition (a) true (no repository); condition (b) judged *not* met because the `Consent format` section carries extracted resolution language and recital depth (treated as the seed-derived house format) — recorded as a borderline reading of the skill text. Step 2 "no repository" notice shown.
- Step 0: `ksa`, `MANIFEST.md` populated, `INDEX.md`, rows read from `companies-law.md` (Arts. 7, 8, 25, 163-164/Regs Art. 63, 165, 166/171, 172, 27, 71), `electronic-transactions-law.md` (Arts. 3, 4, 5, 6-7, 8-9, 14(1)-(2), 14(3)-(5), practice note), `civil-transactions-law.md` (note only), `commercial-register-law.md` Art. 10 and `platform-obligations.md` Labor Law Arts. 15-16 (post-resolution filings, outside the skill's list but from settled rows read this session). Portal probe reachable; no article fetched. `corporate-governance-regulations.md` not loaded (unlisted LLC).
- Step 4 run for "Partners of an LLC"; Step 4.5 non-lawyer gate shown; output marked DRAFT for attorney review (the gate bars only the signatory-ready form).

### Deliverable

~~~~markdown
> **⚠️ Reviewer note**
> - **Sources:** portal: laws.boe.gov.sa ✓ reachable (`scripts/fetch-law.py --portal boe --index`, 2026-09-04); no article fetched; rules from `references/jurisdictions/ksa/companies-law.md` and `electronic-transactions-law.md` rows with their tags.
> - **Read:** practice profile `## Jurisdiction`, `## Company profile`, `## Board & Secretary`; the company's articles of incorporation are NOT on file — statutory defaults applied and flagged.
> - **Flagged for your judgment:** 6 items marked `[review]`.
> - **Currency:** could not search; Companies Law shows 0 amended articles on the portal per `INDEX.md` (read 2026-09-04).
> - **Before relying:** (1) paste the articles of incorporation (عقد التأسيس) — they may set a higher majority than Art. 166 or route branch openings differently; (2) confirm whether the new manager is a partner (affects the vote count) and who the three partners are by name.
> - **Jurisdiction:** ksa; files: MANIFEST.md, INDEX.md, companies-law.md, electronic-transactions-law.md, civil-transactions-law.md (note only), commercial-register-law.md, platform-obligations.md; portal fetched: no; unpopulated codes: none.
> - **Precedent:** no consents repository is connected, so I'm working from your seed format (`قرر الشركاء / RESOLVED`, minimal recitals, e-signatures accepted). For this action type specifically, you may want to check whether you have a prior consent to use as a substantive starting point. The scenario's 50 / 30 / 20 partner split was used; the profile's entity table shows "Founders 100" — reconcile `[review]`.

RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY, SOLICITOR, BARRISTER, OR OTHER AUTHORISED LEGAL PROFESSIONAL IN YOUR JURISDICTION BEFORE ACTING
Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance. / النص العربي هو النص المعتمد، والترجمة الإنجليزية للاستئناس فقط، ويجب مراجعة محامٍ سعودي مرخص قبل الاعتماد على هذا المستند.

> Executing a written consent has legal consequences — it binds the entity and becomes a corporate record. Have you reviewed this with an attorney? If yes, proceed. If no, here's a brief to bring to them:
> - **What the action is:** partners' resolution by circulation of Example Telematics Co. (LLC, CR 1010000000, ksa) appointing a new manager and opening a branch in Jeddah.
> - **What the analysis found:** ordinary partners' decision — valid with approval of partners holding more than half the capital, by written vote circulated to every partner (`companies-law.md` Art. 166 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` `[BOE — official English]`); recorded in the minutes register (Art. 165); electronic signature by the absent 20% partner is valid between the parties (`electronic-transactions-law.md` Arts. 5, 14(1) `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`) but carries the statutory presumptions only with a licensed certificate (Art. 14(3)-(4)). No conflict identified; confirm whether the new manager is a partner.
> - **Open questions:** whether the articles set a higher majority or exclude circulation; whether opening a branch requires an amendment of the articles under your articles (no statutory row — `[no rule in ksa files — verify]`); whether the signing platform meets any signature condition in the articles; the Hijri date.
> - **What could go wrong:** invalid resolution (majority not reached or a partner not circulated), signature challenged for lack of a certified signature, branch or manager not registered within 15 days.
> - **What to ask the attorney:** is circulation the right vehicle for both items; do the articles require anything more; who signs the Commercial Register and Qiwa updates.
>
> If you need to find an attorney: contact your professional regulator (the Saudi Bar Association, or your jurisdiction's equivalent) for a referral service.
>
> **The resolution below is a DRAFT for attorney review, not a signatory-ready consent.** I will produce the signatory-ready version after an explicit yes.

> This is a draft for attorney review, not an executed consent. Executing it binds the entity and becomes a corporate record — a licensed attorney reviews, edits as needed, and takes professional responsibility before it goes out. Do not circulate for signature unreviewed.

---

قرار بالتمرير
RESOLUTION BY CIRCULATION
OF THE PARTNERS
OF EXAMPLE TELEMATICS CO. (limited liability company — شركة ذات مسؤولية محدودة, CR 1010000000, ksa)

Date: 4 September 2026 / 22 Rabi' al-Awwal 1448H (approximate — confirm against the Umm al-Qura calendar `[model knowledge — verify]`)

**النص العربي (المعتمد)**

نحن الموقعين أدناه، الشركاء في شركة Example Telematics Co. (شركة ذات مسؤولية محدودة، سجل تجاري رقم 1010000000) ("الشركة")، والممثلين لنسبة [100]% من رأس مال الشركة، وقد عُرض علينا مشروع هذا القرار والمستندات المؤيدة له بالتمرير من مدير الشركة دون الحاجة إلى انعقاد الجمعية العامة، استنادًا إلى المادة (السادسة والستين بعد المائة) من نظام الشركات الصادر بالمرسوم الملكي رقم (م/132) وتاريخ 1/12/1443هـ، والبند [●] من عقد تأسيس الشركة `[review: عقد التأسيس غير متوفر في الملف]`، نقرر ما يلي:

**البند الأول — تعيين مدير**
حيث إن الشركة ترغب في تعيين مدير [إضافي / بديل] لها؛
قرر الشركاء تعيين السيد/ [الاسم الكامل]، [الجنسية]، هوية/إقامة رقم [●]، مديرًا للشركة اعتبارًا من [التاريخ]، وتكون له الصلاحيات [المنصوص عليها في عقد التأسيس / المحددة في الملحق (أ) لهذا القرار]، على أن تُقيد صلاحياته في السجل التجاري.

**البند الثاني — افتتاح فرع في جدة**
حيث إن الشركة ترغب في التوسع في المنطقة الغربية؛
قرر الشركاء الموافقة على افتتاح فرع للشركة في مدينة جدة، بعنوان [●]، لمزاولة نشاط الشركة المقيد في سجلها التجاري، وتفويض المدير [الاسم] باستكمال إجراءات قيد الفرع لدى وزارة التجارة والجهات ذات العلاقة، وتوقيع ما يلزم لذلك.

**البند الثالث — القيد والتوثيق**
قرر الشركاء تفويض المدير [الاسم] بتحديث بيانات السجل التجاري خلال (خمسة عشر) يومًا من تاريخ هذا القرار، وإثبات هذا القرار في سجل محاضر قرارات الشركاء.

**بيان الأغلبية:** صدر هذا القرار بموافقة شركاء يمثلون [100]% من رأس المال، والنصاب المطلوب نظامًا موافقة شريك أو أكثر يمثلون أكثر من نصف رأس المال (المادة 166 من نظام الشركات) ما لم ينص عقد التأسيس على أغلبية أكبر.

**التوقيع الإلكتروني:** اتفق الشركاء على أن التوقيع على هذا القرار إلكترونيًا يُعد توقيعًا صحيحًا ومنتجًا لآثاره بينهم وفقًا للمادتين (الخامسة) و(الرابعة عشرة) من نظام التعاملات الإلكترونية، ويجوز التوقيع عليه في نسخ متعددة تُعد جميعها مستندًا واحدًا.

**English rendering (for convenience)**

The undersigned, being all three of the partners of Example Telematics Co., a limited liability company registered under CR 1010000000 (the "Company"), representing [100]% of the capital, having had the proposed resolution and supporting documents sent to each of us by the manager for a written vote without a meeting of the general assembly, adopt the following resolution by circulation pursuant to Article 166 of the Companies Law (Royal Decree No. M/132 of 1/12/1443H) and Clause [●] of the Company's articles of incorporation `[review: articles not on file]`:

**Item 1 — Appointment of manager**
WHEREAS the Company wishes to appoint [an additional / a replacement] manager;
RESOLVED, that Mr./Ms. [full name], [nationality], ID/iqama no. [●], is appointed manager of the Company with effect from [date], with the powers [set out in the articles of incorporation / in Annex A to this resolution], such powers to be registered in the Commercial Register.

**Item 2 — Opening of a branch in Jeddah**
WHEREAS the Company wishes to expand in the Western Region;
RESOLVED, that the opening of a branch of the Company in Jeddah at [address], to carry on the Company's registered activities, is approved, and that the manager [name] is authorised to complete the registration of the branch with the Ministry of Commerce and the relevant authorities and to sign what is required.

**Item 3 — Registration and record**
RESOLVED FURTHER, that the manager [name] is authorised to update the Commercial Register within fifteen days of the date of this resolution, and that this resolution shall be entered in the register of partners' minutes and resolutions.

Majority statement: approved by partners holding [100]% of the capital, the requirement being more than 50% of the capital (`companies-law.md` Art. 166 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` `[BOE — official English]`) unless the articles require a larger majority — statutory default applied; the articles are not on file `[review]`.

Signature and counterparts clause: the partners agree that signature of this resolution in electronic form is valid and binding between them under Electronic Transactions Law Arts. 5 and 14(1), and that it may be signed in counterparts which together form one instrument. Where this resolution must be filed with the Ministry of Commerce, the form of execution the Ministry's portal requires is `[model knowledge — verify]` and is flagged, not asserted.

_______________________________
[Partner 1 — name in Arabic and English] — partner, 50% — Date: ___________

_______________________________
[Partner 2 — name in Arabic and English] — partner, 30% — Date: ___________

_______________________________ (electronic signature — signed abroad)
[Partner 3 — name in Arabic and English] — partner, 20% — Date: ___________

---

RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY, SOLICITOR, BARRISTER, OR OTHER AUTHORISED LEGAL PROFESSIONAL IN YOUR JURISDICTION BEFORE ACTING
Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance. / النص العربي هو النص المعتمد، والترجمة الإنجليزية للاستئناس فقط، ويجب مراجعة محامٍ سعودي مرخص قبل الاعتماد على هذا المستند.

SIGNATORY CHECKLIST — Appointment of manager; opening of Jeddah branch — 2026-09-04

Required signatories (signature threshold: partners holding more than 50% of the capital per `companies-law.md` Art. 166 `[settled — last confirmed 2026-09-04]`; all three circulated; any larger majority in the articles governs `[review]`):
□ [Partner 1] — 50%
□ [Partner 2] — 30%
□ [Partner 3] — 20% (abroad; electronic signature)
Note: 50% + 30% already exceeds the statutory threshold; the resolution is nonetheless circulated to all three partners as Art. 166 requires, and the majority statement records the votes actually received.

Conflict disclosures:
None disclosed. If the proposed manager is a partner, say so — the file has no row on a partner-manager voting on his own *appointment* (Art. 164 excludes him only on his *removal*) `[no rule in ksa files — verify]`; for a manager's interest in the Company's dealings, `companies-law.md` Art. 27 (authorisation by the partners) applies. (Plain English: if one of the three partners is being made manager, the lawyer should decide whether that partner's vote counts.)

Jurisdiction rule: ksa —
- Circulation and majority: `companies-law.md` Arts. 166, 171 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` `[BOE — official English]`: the manager sends each partner the proposed decisions and documents for a written vote (registered letter, personal delivery, e-mail or technology unless the articles provide otherwise); valid only if approved by partners holding more than half the capital, unless the articles require more; if that majority is not reached on the first consultation, a meeting must be called, at which decisions pass by a majority of the interests represented unless the articles provide otherwise; each partner votes in proportion to his interests.
- Not an amendment: appointment of a manager and opening a branch are ordinary decisions; ≥ 75% of the capital (Art. 172 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`) applies only if the articles must be amended — whether a branch opening amends *your* articles is not settled by any file row `[no rule in ksa files — verify]` `[review]`. Manager removal at > 50% by Regs Art. 63 (not in issue here).
- Minutes register: `companies-law.md` Art. 165 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` `[BOE — official English]`: "decisions by circulation are recorded in minutes entered in a special register kept for the purpose; technology may be used to record them".
- Language: the articles and amendments must be in Arabic (Art. 7); the Arabic text of this resolution governs.
- Notice to non-signatories: satisfied by circulation to every partner (Art. 166); no separate post-signature notice period is in the files `[no rule in ksa files — verify]` if one is wanted.
Articles of association: not on file — statutory default applied (`companies-law.md` Art. 166); the articles may set a higher threshold or exclude this route — confirm before circulation `[review]`.
Signature form: electronic valid between the parties per `electronic-transactions-law.md` Art. 5 and Art. 14(1) `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`; the presumptions of identity, purpose and integrity in Art. 14(3)-(4) attach only to a signature under a licensed digital certificate — a DocuSign-type platform signature by the 20% partner is valid but carries no presumption unless certified, so keep the platform's completion certificate and audit trail (Arts. 6(1)(c), 9(4)) and consider a Saudi-certified signature (practice-note row `[model knowledge — verify]`); the partners' consent to electronic dealing is made express by the signature clause (Art. 4). Whether the platform meets any signature or form condition in the Company's articles: `[review]`. Notarisation or portal execution for any Ministry of Commerce filing: `[model knowledge — verify]`.
Reviewer note: Jurisdiction: ksa; files: MANIFEST.md, INDEX.md, companies-law.md, electronic-transactions-law.md, civil-transactions-law.md (note only), commercial-register-law.md, platform-obligations.md; portal fetched: no; unpopulated codes: none.

Post-resolution filings (for the manager, not part of the resolution):
□ Commercial Register update within 15 days of the change of manager (`commercial-register-law.md` Art. 10 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`; unregistered changes cannot be set up against third parties, Art. 17)
□ Branch registration route under the 1446H Commercial Register Law (sub-registers dropped) `[model knowledge — verify]`
□ Qiwa establishment file — responsible manager change notified within seven days (`platform-obligations.md` Labor Law Arts. 15-16 `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]`; the Qiwa mechanics `[model knowledge — verify]`)
□ MISA register data update if the change affects registered particulars (`investment-law.md` Reg. Art. 13 `[authority — MISA]`)

---

RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY, SOLICITOR, BARRISTER, OR OTHER AUTHORISED LEGAL PROFESSIONAL IN YOUR JURISDICTION BEFORE ACTING

BEFORE CIRCULATING — check:
□ Resolution language precisely describes the action (manager's name, ID, powers; branch address)
□ Correct effective date (Gregorian and Hijri)
□ All required exhibits attached and referenced (Annex A powers, if used)
□ Authorised signatories named correctly (three partners; 50 / 30 / 20 reconciled to the entity table)
□ Any conflicts disclosed or resolved (is the new manager a partner?)
□ Majority statement matches the threshold in the jurisdiction rule (> 50% of capital, Art. 166, or the articles' higher figure); register entry noted (Art. 165)
□ For major actions: outside counsel has reviewed — not triggered (routine action)

**Bottom line / الخلاصة:** An ordinary partners' resolution by circulation at more than half the capital is the right vehicle for both items; the only open points are the articles (majority and branch route) and the evidential weight of the absent partner's platform signature. / القرار بالتمرير بأغلبية تزيد على نصف رأس المال هو الأداة الصحيحة للبندين؛ والنقاط المعلقة الوحيدة هي ما ينص عليه عقد التأسيس (نسبة الأغلبية ومسار افتتاح الفرع) وحجية التوقيع الإلكتروني للشريك الغائب.
~~~~

### Grading — COR-02

| # | Item | Result | Evidence |
|---|---|---|---|
| E1 | Step 0 runs; Step 4 reads majority, circulation, minutes-register rules from `companies-law.md` with articles cited, not "state law" | PASS | "Jurisdiction rule: ksa — Circulation and majority: `companies-law.md` Arts. 166, 171 …"; "Minutes register: `companies-law.md` Art. 165 …"; "≥ 75% of the capital (Art. 172 …)"; no "state law" anywhere |
| E2 | Bilingual draft (Arabic resolution text with English), headed as a resolution by circulation, cites the Companies Law article and the articles-of-association clause, records the majority obtained | PASS (with note) | Heading "قرار بالتمرير / RESOLUTION BY CIRCULATION"; Arabic operative text "قرر الشركاء …" with English rendering; "pursuant to Article 166 of the Companies Law … and Clause [●] of the Company's articles of incorporation `[review: articles not on file]`"; "Majority statement: approved by partners holding [100]% of the capital, the requirement being more than 50%". Note: the clause is a placeholder because the articles are not on file — the skill's own Step 4 instruction ("Statutory default applied … articles may set a higher threshold") was followed. |
| E3 | E-signature validity from `electronic-transactions-law.md` (valid between parties; presumptions only with licensed certificate) with `[review]` on whether the platform meets the articles | PASS | "Signature form: electronic valid between the parties per `electronic-transactions-law.md` Art. 5 and Art. 14(1) …; the presumptions … in Art. 14(3)-(4) attach only to a signature under a licensed digital certificate …; Whether the platform meets any signature or form condition in the Company's articles: `[review]`" |
| E4 | No "unanimous written consent in lieu of a meeting" or DGCL citation | PASS | Absent; the `usa` template was not used |
| F1 | "pursuant to Section 141(f)" | PASS | Absent |
| F2 | "State law notice" | PASS | Absent ("Notice to non-signatories: satisfied by circulation to every partner (Art. 166)") |
| F3 | A US-only template as the only output | PASS | Output is the bilingual `ksa` circular resolution |

**Result: PASS.** Skill-text observations recorded below (Art. 166 "written request defeats it" wording; no-precedent condition (b)).

---

## COR-03 — Entity compliance tracker for an LLC and a JSC

### Transcript summary

- Read: scenario; plugin `CLAUDE.md`; staged profile `## Jurisdiction` and `## Entity Management` (entity table: Example Telematics Co. — LLC — ksa — CR 1010000000; Example Telematics Holding JSC — JSC (unlisted) — ksa — CR 1010000001; filing agent in-house government-relations officer; tracker path under the staged home); `corporate-legal/skills/entity-compliance/SKILL.md`. Scenario adds: LLC fiscal year ends 31 December (applied as `[user provided]`); JSC fiscal year end not given.
- Step 0: `ksa` for both entities; `MANIFEST.md` populated; `INDEX.md`; `filing-calendar.md` read in full (indexed by entity type then authority); `commercial-register-law.md` Arts. 3/5, 6, 10, 11, 15, 17, 21; `companies-law.md` Arts. 16-17, 18-20, 88, 121-122, 165-168 (Regs Art. 65), 262; `ultimate-beneficial-ownership-rules.md` annual-confirmation, change-notification, penalties, scope rows; `investment-law.md` Reg. Art. 13; `social-insurance-law.md` Arts. 7, 9, 10; `platform-obligations.md` Arts. 15-16, 51; `saudization-nitaqat.md` Services-by-Range row. `corporate-governance-regulations.md` not loaded (JSC unlisted). Portal probe reachable; no article fetched.
- Mode 1 (`--init`): Step 1 entity table; Step 2 rows pulled per `entity_type_local` ("all", "all (companies)", "all (employers)", "LLC" or "JSC"); Step 2.5 dates computed from the LLC's FYE with roll-back against the Friday-Saturday weekend (auditor pack 2026-05-16 Saturday → 2026-05-14 Thursday); JSC FYE-driven rows left `unknown` with the formula recorded; inputs requested and listed (CR registration dates, JSC FYE, MISA certificate dates, VAT band, headcount/permits, premises, whether the JSC has employees or non-Saudi owners). Step 3 wrote the tracker to `<staged home>/corporate-legal/entities/compliance-tracker.yaml` (36 filings).
- Mode 2 (`--report --days 90`): window 2026-09-04 → 2026-12-03 (Thursday) on the manifest calendar; National Day 2026-09-23 falls inside the window (no computed date lands on it).

### Deliverable — `--init` summary

~~~~markdown
RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY, SOLICITOR, BARRISTER, OR OTHER AUTHORISED LEGAL PROFESSIONAL IN YOUR JURISDICTION BEFORE ACTING
Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance. / النص العربي هو النص المعتمد، والترجمة الإنجليزية للاستئناس فقط، ويجب مراجعة محامٍ سعودي مرخص قبل الاعتماد على هذا المستند.

Entity compliance tracker initialized.
Written to: ${LEGAL_CONSULTANT_HOME}/corporate-legal/entities/compliance-tracker.yaml (staged home)

Entities: 2 (Example Telematics Co. — ksa / LLC / CR 1010000000; Example Telematics Holding JSC — ksa / JSC (unlisted) / CR 1010000001)
Total jurisdictions: 1 (ksa)
Filings tracked: 36 (18 per entity)

Status summary:
  ✅ Current:   0
  ⏰ Due soon:  0 (next 90 days)
  🔴 Overdue:   4
  ❓ Unknown:   8 (confirm with filing agent)
  ⚪ Unconfirmed: 24 (model-knowledge rows awaiting accountant / filing-agent confirmation)

ملخص الحالة: ✅ مستوفى: 0 · ⏰ مستحق خلال 90 يومًا: 0 · 🔴 متأخر: 4 · ❓ غير معروف: 8 (يُؤكد مع مسؤول العلاقات الحكومية) · ⚪ غير مؤكد: 24 (صفوف من المعرفة النموذجية بانتظار تأكيد المحاسب أو وكيل الإيداع)

Inputs I need before more dates can be computed (do not assume):
1. CR registration date for each entity (drives the CR annual confirmation — its due-date rule is in the Commercial Register Regulations, not read — and the UBO annual confirmation anniversary).
2. Fiscal year end of Example Telematics Holding JSC (every Art. 88 / 121-122 / 17 / ZATCA row for the JSC is unknown until then).
3. MISA registration certificate date and last annual-update confirmation for Example Telematics Co.; whether any founder of the JSC is non-Saudi (if none, delete the JSC's MISA row).
4. VAT registration and turnover band; headcount and work-permit expiry list; premises list; whether the JSC has employees.

Run /corporate-legal:entity-compliance --report to see what's due.

Reviewer note: Jurisdiction: ksa; files: MANIFEST.md, INDEX.md, filing-calendar.md, commercial-register-law.md, companies-law.md, ultimate-beneficial-ownership-rules.md, investment-law.md, social-insurance-law.md, platform-obligations.md, saudization-nitaqat.md; portal fetched: no (probe: laws.boe.gov.sa ✓ reachable 2026-09-04); unpopulated codes: none.
~~~~

### Deliverable — tracker YAML (as written to the staged home)

~~~~yaml
# Entity Compliance Tracker
# Generated: 2026-09-04
# Last updated: 2026-09-04
# Disclaimer: deadlines are reference only — confirm with the filing agent or the issuing authority named in the jurisdiction file
# Currency: SAR; dates computed against the calendar in references/jurisdictions/ksa/MANIFEST.md (Friday-Saturday weekend; Eid al-Fitr, Eid al-Adha, National Day 23 September, Founding Day 22 February; Hijri dates on official instruments)
# Jurisdiction: ksa; files: MANIFEST.md, INDEX.md, filing-calendar.md, commercial-register-law.md, companies-law.md, ultimate-beneficial-ownership-rules.md, investment-law.md, social-insurance-law.md, platform-obligations.md, saudization-nitaqat.md; portal fetched: no (probe: laws.boe.gov.sa reachable 2026-09-04); unpopulated codes: none
# Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance. / النص العربي هو النص المعتمد، والترجمة الإنجليزية للاستئناس فقط، ويجب مراجعة محامٍ سعودي مرخص قبل الاعتماد على هذا المستند.

metadata:
  company: "Example Telematics Co."
  generated: "2026-09-04"
  last_updated: "2026-09-04"
  last_audit: null
  primary_jurisdiction: "ksa"

custom_jurisdictions:
  []

entities:
  - name: "Example Telematics Co."
    entity_type_local: "LLC"
    type: "LLC"
    jurisdiction_code: "ksa"
    registry_number: "CR 1010000000"
    formation_date: null            # CR registration date not in the entity table — ASK
    fiscal_year_end: "2025-12-31"   # [user provided — scenario]
    status: "active"
    filing_agent: "in-house government-relations officer"
    registered_agent: "in-house government-relations officer"
    notes: "Foreign-investment registration on file (MISA certificate, IT consulting) per profile; member of a group with Example Telematics Holding JSC — audit mandatory under Companies Law Art. 19(e)/(f) [settled — last confirmed 2026-09-04] [BOE — Arabic]"
    jurisdictions:
      - jurisdiction_code: "ksa"
        qualification: "main CR"
        qualified_date: null
        agent_managed: false
        local_agent: null
        filings:
          - type: "CR annual confirmation (التأكيد السنوي)"
            authority: "Ministry of Commerce"
            source_tag: "[settled — last confirmed 2026-09-04] [BOE — Arabic] (duty: Commercial Register Law Arts. 11, 15); due date [model knowledge — verify] (Regulations not read; Ministry practice = registration anniversary)"
            due_date: null
            due_basis: "date set by the Commercial Register Regulations (commercial-register-law.md Arts. 11, 15); suspension exposure = due date + 90 days + 14-day warning (Art. 15)"
            confirmed_by: null
            last_filed: null
            last_fee: null
            status: "unconfirmed"
            confirmed_good_standing: null
            notes: "Needs CR registration date and the Regulations' due-date rule"
          - type: "Annual general assembly of partners"
            authority: "Ministry of Commerce"
            source_tag: "[settled — last confirmed 2026-09-04] [BOE — Arabic]"
            due_date: "2026-06-30"
            due_basis: "fiscal year end + 6 months (companies-law.md Art. 165)"
            confirmed_by: null
            last_filed: null
            last_fee: null
            status: "overdue"
            confirmed_good_standing: null
            notes: "2026-06-30 [computed — companies-law.md Art. 165, settled 2026-09-04; inputs: fiscal year end 2025-12-31, entity type LLC]; Tuesday, no roll-back. Sanction: Art. 262(b) fine up to SAR 500,000. No record of the FY2025 assembly supplied — confirm whether held"
          - type: "Financial statements deposit (إيداع القوائم المالية)"
            authority: "Ministry of Commerce (Saudi Business Center deposit programme)"
            source_tag: "[settled — last confirmed 2026-09-04] [BOE — Arabic] [authority — MoC]"
            due_date: "2026-06-30"
            due_basis: "fiscal year end + 6 months (companies-law.md Art. 17; Regs Art. 5)"
            confirmed_by: null
            last_filed: null
            last_fee: null
            status: "overdue"
            confirmed_good_standing: null
            notes: "2026-06-30 [computed — companies-law.md Art. 17, settled 2026-09-04; inputs: fiscal year end 2025-12-31, entity type LLC]. Sanction: Art. 262(e)"
          - type: "Financial statements to auditor (auditor pack)"
            authority: "Ministry of Commerce"
            source_tag: "[settled — last confirmed 2026-09-04] [BOE — Arabic] [authority — MoC]"
            due_date: "2026-05-14"
            due_basis: "assembly date − 45 calendar days (companies-law.md Art. 167); rolled back from Saturday 2026-05-16 to Thursday 2026-05-14 per the manifest calendar"
            confirmed_by: null
            last_filed: null
            last_fee: null
            status: "overdue"
            confirmed_good_standing: null
            notes: "2026-05-14 [computed — companies-law.md Art. 167, settled 2026-09-04; inputs: assembly deadline 2026-06-30, entity type LLC; roll-back from Friday-Saturday weekend]"
          - type: "Statements, manager report and auditor report to partners; manager activity report to the Ministry"
            authority: "Ministry of Commerce"
            source_tag: "[settled — last confirmed 2026-09-04] [BOE — Arabic] [authority — MoC]"
            due_date: "2026-06-09"
            due_basis: "assembly date − 21 calendar days (companies-law.md Art. 167; Regs Art. 65)"
            confirmed_by: null
            last_filed: null
            last_fee: null
            status: "overdue"
            confirmed_good_standing: null
            notes: "2026-06-09 [computed — companies-law.md Art. 167 and Regs Art. 65, settled 2026-09-04; inputs: assembly deadline 2026-06-30, entity type LLC]; Tuesday"
          - type: "Zakat / corporate income tax return"
            authority: "ZATCA"
            source_tag: "[model knowledge — verify]"
            due_date: "2026-04-30"
            due_basis: "fiscal year end + 120 days (filing-calendar.md ZATCA row)"
            confirmed_by: null
            last_filed: null
            last_fee: null
            status: "unconfirmed"
            confirmed_good_standing: null
            notes: "2026-04-30 [computed — filing-calendar.md ZATCA row, model knowledge; inputs: fiscal year end 2025-12-31]; Thursday. Never drives an alert until the accountant confirms"
          - type: "VAT returns"
            authority: "ZATCA"
            source_tag: "[model knowledge — verify]"
            due_date: null
            due_basis: "monthly (annual taxable supplies > SAR 40 million) or quarterly; last day of the following month"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: "Needs VAT registration status and turnover band — ASK"
          - type: "Withholding tax monthly return"
            authority: "ZATCA"
            source_tag: "[model knowledge — verify]"
            due_date: null
            due_basis: "within the first 10 days of the month following a payment to a non-resident"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: "Event-driven"
          - type: "E-invoicing (Fatoora) phase 2 integration"
            authority: "ZATCA"
            source_tag: "[model knowledge — verify]"
            due_date: null
            due_basis: "wave date notified by ZATCA"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: ""
          - type: "Transfer-pricing disclosure form (with annual return)"
            authority: "ZATCA"
            source_tag: "[model knowledge — verify]"
            due_date: "2026-04-30"
            due_basis: "with the zakat/tax return, fiscal year end + 120 days; related-party dealings with the group JSC"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: ""
          - type: "GOSI monthly contributions"
            authority: "GOSI"
            source_tag: "[model knowledge — verify] (deadline); duty and 2% monthly delay fine [settled — last confirmed 2026-09-04] [BOE — Arabic] (social-insurance-law.md Art. 9)"
            due_date: "2026-09-15"
            due_basis: "15th of the following month (filing-calendar.md GOSI row)"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: "2026-09-15 [computed — filing-calendar.md GOSI row, model knowledge; inputs: current month]; Tuesday. Recurring monthly"
          - type: "Work-permit and iqama renewals (per non-Saudi employee)"
            authority: "HRSD-Qiwa / Ministry of Interior"
            source_tag: "[model knowledge — verify] (renewal cycle and levy); permit duty [settled — last confirmed 2026-09-04] [BOE — Arabic] (Labor Law Art. 33)"
            due_date: null
            due_basis: "each permit's expiry"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: "Needs headcount and permit expiry list — ASK"
          - type: "Nitaqat band and monthly WPS (Mudad) upload"
            authority: "HRSD-Qiwa"
            source_tag: "[model knowledge — verify]"
            due_date: null
            due_basis: "monthly wage file; band is a continuous state — take from a dated Qiwa export (saudization-nitaqat.md)"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: "Never infer the band from coefficients"
          - type: "Chamber of commerce membership"
            authority: "Chamber"
            source_tag: "[model knowledge — verify]"
            due_date: null
            due_basis: "chamber's annual schedule"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: ""
          - type: "Municipal licence (رخصة بلدية)"
            authority: "Municipality (Balady)"
            source_tag: "[model knowledge — verify]"
            due_date: null
            due_basis: "annual or licence term, per premises"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: "One per premises — ASK for the premises list"
          - type: "MISA investment registration annual update"
            authority: "MISA"
            source_tag: "[settled — last confirmed 2026-09-04] [authority — MISA] (investment-law.md Reg. Art. 13)"
            due_date: null
            due_basis: "registration anniversary, taken from the registration certificate (never computed from the fiscal year); filing window 60 working days before; 30 working days' grace"
            status: "unknown"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: "Profile records a MISA certificate but not its date — ASK"
          - type: "UBO annual confirmation"
            authority: "Ministry of Commerce (UBO)"
            source_tag: "[settled — last confirmed 2026-09-04] [authority — MoC] (ultimate-beneficial-ownership-rules.md annual-confirmation row); filing-calendar.md's own UBO row is [model knowledge — verify]"
            due_date: null
            due_basis: "anniversary of registration in the Commercial Register; may be filed up to 30 days early; the CR-registration date is [user provided] and was not supplied"
            status: "unknown"
            confirmed_by: null
            last_filed: "2026-01-15"
            last_fee: null
            confirmed_good_standing: null
            notes: "last_filed 2026-01-15 [user provided — profile]. Do not infer the anniversary from last_filed; ASK for the CR registration date. Change notification within 15 days; sanction Companies Law Art. 262 up to SAR 500,000"
          - type: "National Address confirmation"
            authority: "Saudi Post (SPL)"
            source_tag: "[model knowledge — verify]"
            due_date: null
            due_basis: "annual via the SPL business portal"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: "Service address for the CR Art. 15 14-day suspension warning"

  - name: "Example Telematics Holding JSC"
    entity_type_local: "JSC"
    type: "JSC"
    jurisdiction_code: "ksa"
    registry_number: "CR 1010000001"
    formation_date: null            # ASK
    fiscal_year_end: null           # not in the entity table — ASK
    status: "active"
    filing_agent: "in-house government-relations officer"
    registered_agent: "in-house government-relations officer"
    notes: "Unlisted JSC — Companies Law Arts. 88, 121-122 apply, not the CMA continuing-obligations row; UBO Rules apply (unlisted); audit mandatory as a group parent (Art. 19(f))"
    jurisdictions:
      - jurisdiction_code: "ksa"
        qualification: "main CR"
        qualified_date: null
        agent_managed: false
        local_agent: null
        filings:
          - type: "CR annual confirmation (التأكيد السنوي)"
            authority: "Ministry of Commerce"
            source_tag: "[settled — last confirmed 2026-09-04] [BOE — Arabic] (duty: Commercial Register Law Arts. 11, 15); due date [model knowledge — verify]"
            due_date: null
            due_basis: "date set by the Commercial Register Regulations (commercial-register-law.md Arts. 11, 15); suspension exposure = due date + 90 days + 14-day warning"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: "Needs CR registration date — ASK"
          - type: "Annual ordinary general assembly"
            authority: "Ministry of Commerce"
            source_tag: "[settled — last confirmed 2026-09-04] [BOE — Arabic]"
            due_date: null
            due_basis: "fiscal year end + 6 months (companies-law.md Art. 88)"
            status: "unknown"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: "Fiscal year end not supplied — ASK; agenda: board report, financial statements, auditor report, dividend proposal (Art. 88). Sanction Art. 262(b)"
          - type: "Financial statements deposit (إيداع القوائم المالية)"
            authority: "Ministry of Commerce (Saudi Business Center deposit programme)"
            source_tag: "[settled — last confirmed 2026-09-04] [BOE — Arabic] [authority — MoC]"
            due_date: null
            due_basis: "fiscal year end + 6 months (companies-law.md Art. 17; Regs Art. 5)"
            status: "unknown"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: "Fiscal year end not supplied — ASK"
          - type: "Financial statements and board report to auditor (auditor pack)"
            authority: "Ministry of Commerce"
            source_tag: "[settled — last confirmed 2026-09-04] [BOE — Arabic] [authority — MoC]"
            due_date: null
            due_basis: "assembly date − 45 calendar days (companies-law.md Art. 121); signed by chairman, CEO and CFO"
            status: "unknown"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: "JSC row — not the LLC Art. 167 row"
          - type: "Signed statements, board report and auditor report to shareholders; board report to the Ministry"
            authority: "Ministry of Commerce"
            source_tag: "[settled — last confirmed 2026-09-04] [BOE — Arabic] [authority — MoC]"
            due_date: null
            due_basis: "assembly date − 21 calendar days (companies-law.md Art. 122; Regs Art. 31)"
            status: "unknown"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: ""
          - type: "Zakat / corporate income tax return"
            authority: "ZATCA"
            source_tag: "[model knowledge — verify]"
            due_date: null
            due_basis: "fiscal year end + 120 days"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: "Fiscal year end not supplied"
          - type: "VAT returns"
            authority: "ZATCA"
            source_tag: "[model knowledge — verify]"
            due_date: null
            due_basis: "monthly or quarterly by turnover band; last day of the following month"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: "Is the holding company VAT-registered? — ASK"
          - type: "Withholding tax monthly return"
            authority: "ZATCA"
            source_tag: "[model knowledge — verify]"
            due_date: null
            due_basis: "first 10 days of the month following a payment to a non-resident"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: ""
          - type: "E-invoicing (Fatoora) phase 2 integration"
            authority: "ZATCA"
            source_tag: "[model knowledge — verify]"
            due_date: null
            due_basis: "wave date notified by ZATCA"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: ""
          - type: "Transfer-pricing disclosure form (with annual return)"
            authority: "ZATCA"
            source_tag: "[model knowledge — verify]"
            due_date: null
            due_basis: "with the annual return; related-party dealings with the operating LLC"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: ""
          - type: "GOSI monthly contributions"
            authority: "GOSI"
            source_tag: "[model knowledge — verify] (deadline); duty [settled — last confirmed 2026-09-04] [BOE — Arabic] (social-insurance-law.md Art. 9)"
            due_date: null
            due_basis: "15th of the following month, if the entity employs anyone"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: "Does the holding JSC have employees? — ASK"
          - type: "Work-permit and iqama renewals (per non-Saudi employee)"
            authority: "HRSD-Qiwa / Ministry of Interior"
            source_tag: "[model knowledge — verify]"
            due_date: null
            due_basis: "each permit's expiry"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: ""
          - type: "Nitaqat band and monthly WPS (Mudad) upload"
            authority: "HRSD-Qiwa"
            source_tag: "[model knowledge — verify]"
            due_date: null
            due_basis: "monthly wage file; band from a dated Qiwa export"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: ""
          - type: "Chamber of commerce membership"
            authority: "Chamber"
            source_tag: "[model knowledge — verify]"
            due_date: null
            due_basis: "chamber's annual schedule"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: ""
          - type: "Municipal licence (رخصة بلدية)"
            authority: "Municipality (Balady)"
            source_tag: "[model knowledge — verify]"
            due_date: null
            due_basis: "annual or licence term, per premises"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: ""
          - type: "MISA investment registration annual update"
            authority: "MISA"
            source_tag: "[settled — last confirmed 2026-09-04] [authority — MISA] (investment-law.md Reg. Art. 13)"
            due_date: null
            due_basis: "registration anniversary from the certificate — applies only if the JSC has non-Saudi ownership"
            status: "unknown"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: "Entity table shows owner 'Founders' 100% — is any founder non-Saudi? — ASK; if none, delete this row"
          - type: "UBO annual confirmation"
            authority: "Ministry of Commerce (UBO)"
            source_tag: "[settled — last confirmed 2026-09-04] [authority — MoC] (ultimate-beneficial-ownership-rules.md annual-confirmation row)"
            due_date: null
            due_basis: "anniversary of registration in the Commercial Register; may be filed up to 30 days early; unlisted JSCs are inside the Rules"
            status: "unknown"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: "CR registration date not supplied — ASK"
          - type: "National Address confirmation"
            authority: "Saudi Post (SPL)"
            source_tag: "[model knowledge — verify]"
            due_date: null
            due_basis: "annual via the SPL business portal"
            status: "unconfirmed"
            confirmed_by: null
            last_filed: null
            last_fee: null
            confirmed_good_standing: null
            notes: ""
~~~~

### Deliverable — `--report --days 90`

~~~~markdown
RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY, SOLICITOR, BARRISTER, OR OTHER AUTHORISED LEGAL PROFESSIONAL IN YOUR JURISDICTION BEFORE ACTING
Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance. / النص العربي هو النص المعتمد، والترجمة الإنجليزية للاستئناس فقط، ويجب مراجعة محامٍ سعودي مرخص قبل الاعتماد على هذا المستند.

ENTITY COMPLIANCE REPORT — 2026-09-04 (Friday; window to 2026-12-03, Thursday, counted on the ksa manifest calendar: Friday-Saturday weekend; National Day 2026-09-23 falls in the window)
Example Telematics Co.

🔴 OVERDUE (4):
  Example Telematics Co. / ksa / LLC / Annual general assembly of partners — Ministry of Commerce — was due 2026-06-30 [computed — companies-law.md Art. 165, settled 2026-09-04; inputs: fiscal year end 2025-12-31, entity type LLC] [settled — last confirmed 2026-09-04] [BOE — Arabic] — no record that it was held; sanction Art. 262(b) up to SAR 500,000 (on the manager as well as the company)
  Example Telematics Co. / ksa / LLC / Financial statements deposit — Ministry of Commerce (Saudi Business Center) — was due 2026-06-30 [computed — companies-law.md Art. 17; Regs Art. 5, settled 2026-09-04; inputs: fiscal year end 2025-12-31] [settled — last confirmed 2026-09-04] [BOE — Arabic] [authority — MoC] — sanction Art. 262(e)
  Example Telematics Co. / ksa / LLC / Auditor pack (statements to auditor) — Ministry of Commerce — was due 2026-05-14 [computed — companies-law.md Art. 167, settled 2026-09-04; inputs: assembly deadline 2026-06-30 − 45 days = Saturday 2026-05-16, rolled back to Thursday 2026-05-14] [settled — last confirmed 2026-09-04] [BOE — Arabic] [authority — MoC]
  Example Telematics Co. / ksa / LLC / Partners' pack and manager activity report to the Ministry — Ministry of Commerce — was due 2026-06-09 [computed — companies-law.md Art. 167; Regs Art. 65, settled 2026-09-04; inputs: assembly deadline 2026-06-30 − 21 days] [settled — last confirmed 2026-09-04] [BOE — Arabic] [authority — MoC]
  (Plain English: the LLC's 2025 accounts had to be approved by the partners and deposited by 30 June 2026; the tracker has no record either happened — confirm with the government-relations officer or run --update.)

⏰ DUE WITHIN 90 DAYS (0):
  none from settled rows. Unconfirmed rows with dates in the window are listed under UNCONFIRMED and raise no alert.

✅ RECENTLY FILED (0 in last 90 days):
  none recorded (UBO annual confirmation for Example Telematics Co. last filed 2026-01-15 [user provided] — outside the 90-day window)

❓ UNKNOWN STATUS (8):
  Example Telematics Co. / ksa / LLC / MISA investment registration annual update — no certificate date; confirm with filing agent (investment-law.md Reg. Art. 13 [settled — last confirmed 2026-09-04] [authority — MISA]: due on the registration anniversary from the certificate)
  Example Telematics Co. / ksa / LLC / UBO annual confirmation — CR registration date not supplied; due on the CR anniversary, may be filed 30 days early (ultimate-beneficial-ownership-rules.md [settled — last confirmed 2026-09-04] [authority — MoC])
  Example Telematics Holding JSC / ksa / JSC / Annual ordinary general assembly — fiscal year end not supplied (companies-law.md Art. 88: FYE + 6 months)
  Example Telematics Holding JSC / ksa / JSC / Financial statements deposit — fiscal year end not supplied (companies-law.md Art. 17: FYE + 6 months)
  Example Telematics Holding JSC / ksa / JSC / Auditor pack — assembly date − 45 days (companies-law.md Art. 121)
  Example Telematics Holding JSC / ksa / JSC / Shareholder pack and board report to the Ministry — assembly date − 21 days (companies-law.md Art. 122; Regs Art. 31)
  Example Telematics Holding JSC / ksa / JSC / MISA investment registration annual update — applies only if any founder is non-Saudi; confirm
  Example Telematics Holding JSC / ksa / JSC / UBO annual confirmation — CR registration date not supplied

⚪ UNCONFIRMED (24) — jurisdiction-file rows tagged [model knowledge — verify]; no alert until confirmed:
  Example Telematics Co. / ksa / LLC / CR annual confirmation — Ministry of Commerce — file says: due date set by the Commercial Register Regulations (duty settled, Arts. 11, 15; date model knowledge; suspension after 90 days + 14-day warning); confirm with your government-relations officer, then --update
  Example Telematics Co. / ksa / LLC / Zakat / corporate income tax return — ZATCA — file says FYE + 120 days = 2026-04-30 (Thursday); confirm with your accountant, then --update
  Example Telematics Co. / ksa / LLC / Transfer-pricing disclosure form — ZATCA — file says with the annual return (2026-04-30); confirm
  Example Telematics Co. / ksa / LLC / VAT returns — ZATCA — file says monthly above SAR 40 million taxable supplies, else quarterly; last day of following month; confirm band
  Example Telematics Co. / ksa / LLC / Withholding tax monthly return — ZATCA — file says first 10 days of the month after a payment to a non-resident; confirm
  Example Telematics Co. / ksa / LLC / E-invoicing phase 2 — ZATCA — file says wave date notified by ZATCA; confirm
  Example Telematics Co. / ksa / LLC / GOSI monthly contributions — GOSI — file says 15th of the following month (next: 2026-09-15 Tuesday; 2026-10-15 Thursday; 2026-11-15 Sunday — all working days on the ksa calendar); duty and 2% monthly delay fine are settled (social-insurance-law.md Art. 9); confirm the deadline with your accountant
  Example Telematics Co. / ksa / LLC / Work-permit and iqama renewals — HRSD-Qiwa / MoI — file says per permit expiry; supply the permit list
  Example Telematics Co. / ksa / LLC / Nitaqat band and WPS upload — HRSD-Qiwa — file says monthly wage file; band from a dated Qiwa export; confirm
  Example Telematics Co. / ksa / LLC / Chamber membership — Chamber — file says annual on the chamber's schedule; confirm
  Example Telematics Co. / ksa / LLC / Municipal licence — Municipality (Balady) — file says annual or licence term per premises; supply the premises list
  Example Telematics Co. / ksa / LLC / National Address confirmation — Saudi Post — file says annual; confirm
  Example Telematics Holding JSC / ksa / JSC / CR annual confirmation — Ministry of Commerce — as above; confirm
  Example Telematics Holding JSC / ksa / JSC / Zakat / corporate income tax return — ZATCA — FYE + 120 days; FYE not supplied; confirm
  Example Telematics Holding JSC / ksa / JSC / Transfer-pricing disclosure form — ZATCA — with the annual return; confirm
  Example Telematics Holding JSC / ksa / JSC / VAT returns — ZATCA — confirm whether registered and the band
  Example Telematics Holding JSC / ksa / JSC / Withholding tax monthly return — ZATCA — confirm
  Example Telematics Holding JSC / ksa / JSC / E-invoicing phase 2 — ZATCA — confirm
  Example Telematics Holding JSC / ksa / JSC / GOSI monthly contributions — GOSI — 15th monthly if the JSC has employees; confirm
  Example Telematics Holding JSC / ksa / JSC / Work-permit and iqama renewals — HRSD-Qiwa / MoI — confirm
  Example Telematics Holding JSC / ksa / JSC / Nitaqat band and WPS upload — HRSD-Qiwa — confirm
  Example Telematics Holding JSC / ksa / JSC / Chamber membership — Chamber — confirm
  Example Telematics Holding JSC / ksa / JSC / Municipal licence — Municipality (Balady) — confirm
  Example Telematics Holding JSC / ksa / JSC / National Address confirmation — Saudi Post — confirm
  These rows must be confirmed with your accountant or filing agent (the in-house government-relations officer) before they drive any alert; the tracker will not promote their tag.

🌐 AGENT-MANAGED (0):
  Example Telematics Co. / ksa — no local agent recorded (filings in-house); add one with --update if a corporate-services provider is engaged
  Example Telematics Holding JSC / ksa — no local agent recorded

⛔ NOT POPULATED (0):
  none — both entities carry a populated code (ksa)

REGISTRATION STATUS (ksa: CR active / suspended per commercial-register-law.md Art. 15 [settled — last confirmed 2026-09-04] [BOE — Arabic]):
  Last confirmed: none recorded
  Entities with confirmed status: 0 of 2
  Entities not confirmed in last 12 months: Example Telematics Co.; Example Telematics Holding JSC — obtain a current CR extract for each (a suspended CR suspends every licence issued on it)

**تقرير الالتزامات النظامية للمنشآت — 2026-09-04 (النسخة العربية)**

ملخص الحالة: 🔴 متأخر: 4 · ⏰ مستحق خلال 90 يومًا: 0 · ✅ مودع حديثًا: 0 · ❓ غير معروف: 8 · ⚪ غير مؤكد: 24 · ⛔ غير مُعدّ: 0

| المنشأة | الرمز / النوع | الالتزام — الجهة | الحالة | التاريخ والسند |
|---|---|---|---|---|
| Example Telematics Co. | ksa / شركة ذات مسؤولية محدودة | الجمعية العامة السنوية للشركاء — وزارة التجارة | 🔴 متأخر | 2026-06-30 (نظام الشركات، المادة 165: خلال ستة أشهر من نهاية السنة المالية) |
| Example Telematics Co. | ksa / شركة ذات مسؤولية محدودة | إيداع القوائم المالية — وزارة التجارة (المركز السعودي للأعمال) | 🔴 متأخر | 2026-06-30 (المادة 17؛ اللائحة المادة 5) |
| Example Telematics Co. | ksa / شركة ذات مسؤولية محدودة | وضع القوائم تحت تصرف مراجع الحسابات — وزارة التجارة | 🔴 متأخر | 2026-05-14 (المادة 167: قبل الجمعية بـ45 يومًا؛ رُحّل من السبت 2026-05-16) |
| Example Telematics Co. | ksa / شركة ذات مسؤولية محدودة | تزويد الشركاء والوزارة بالقوائم والتقرير — وزارة التجارة | 🔴 متأخر | 2026-06-09 (المادة 167؛ اللائحة المادة 65) |
| Example Telematics Co. | ksa / شركة ذات مسؤولية محدودة | التحديث السنوي لتسجيل الاستثمار — وزارة الاستثمار | ❓ غير معروف | ذكرى التسجيل من الشهادة (لائحة نظام الاستثمار، المادة 13) |
| Example Telematics Co. | ksa / شركة ذات مسؤولية محدودة | التأكيد السنوي لبيانات المستفيد الحقيقي — وزارة التجارة | ❓ غير معروف | ذكرى القيد في السجل التجاري (قواعد المستفيد الحقيقي) — آخر تأكيد 2026-01-15 |
| Example Telematics Holding JSC | ksa / شركة مساهمة غير مدرجة | الجمعية العامة العادية السنوية — وزارة التجارة | ❓ غير معروف | نهاية السنة المالية + 6 أشهر (المادة 88) — السنة المالية غير محددة |
| Example Telematics Holding JSC | ksa / شركة مساهمة غير مدرجة | إيداع القوائم المالية — وزارة التجارة | ❓ غير معروف | نهاية السنة المالية + 6 أشهر (المادة 17) |
| Example Telematics Holding JSC | ksa / شركة مساهمة غير مدرجة | وضع القوائم تحت تصرف مراجع الحسابات؛ تزويد المساهمين والوزارة — وزارة التجارة | ❓ غير معروف | قبل الجمعية بـ45 و21 يومًا (المادتان 121-122؛ اللائحة المادة 31) |
| Example Telematics Holding JSC | ksa / شركة مساهمة غير مدرجة | التحديث السنوي لتسجيل الاستثمار؛ تأكيد المستفيد الحقيقي | ❓ غير معروف | يُؤكد وجود شريك غير سعودي؛ تاريخ القيد غير متوفر |
| كلتا المنشأتين | ksa | التأكيد السنوي للسجل التجاري؛ الزكاة والضريبة؛ ضريبة القيمة المضافة؛ الاستقطاع؛ الفوترة الإلكترونية؛ تسعير المعاملات؛ التأمينات الاجتماعية؛ رخص العمل؛ نطاقات وحماية الأجور؛ الغرفة التجارية؛ الرخصة البلدية؛ العنوان الوطني | ⚪ غير مؤكد (24) | صفوف من المعرفة النموذجية `[model knowledge — verify]` — تُؤكد مع المحاسب أو مسؤول العلاقات الحكومية قبل أن تُفعّل أي تنبيه |
| كلتا المنشأتين | ksa | حالة القيد في السجل التجاري (ساري / معلّق — نظام السجل التجاري، المادة 15) | غير مؤكدة | لم يُسجل تاريخ تأكيد؛ يُطلب مستخرج حديث |

**What next? Pick one and I'll help you build it out:**
1. **Run --sweep** — I'll walk through the 4 overdue and 8 unknown items one at a time and record what was filed and when.
2. **Escalate** — a short note to the Legal Lead on the four overdue Companies Law items (Art. 262 exposure on the manager).
3. **Get more facts** — the CR registration dates, the JSC's fiscal year end and the MISA certificate date; I'll draft the request to the government-relations officer.
4. **Watch and wait** — leave the 24 unconfirmed rows as they are until the accountant confirms the ZATCA/GOSI/Qiwa dates.
5. **Something else.**

📊 **See this as a dashboard?** 36 filings across 2 entities — I'll build an interactive view with counts by status, a sortable table by entity / filing type / due date, a timeline, and the reviewer note carried over; HTML written to the entities folder, Excel on request.

Reviewer note: Jurisdiction: ksa; files: MANIFEST.md, INDEX.md, filing-calendar.md, commercial-register-law.md, companies-law.md, ultimate-beneficial-ownership-rules.md, investment-law.md, social-insurance-law.md, platform-obligations.md, saudization-nitaqat.md; portal fetched: no (probe: laws.boe.gov.sa ✓ reachable 2026-09-04); unpopulated codes: none. Sources: cites from the jurisdiction files' rows with their own tags; no web search. Read: entity table (2 entities), full filing-calendar.md. Flagged: inputs listed under UNKNOWN. Before relying: confirm the four overdue items were in fact done, and supply the CR registration dates.
~~~~

### Grading — COR-03

| # | Item | Result | Evidence |
|---|---|---|---|
| E1 | Tracker entries use `jurisdiction_code: ksa`, `entity_type_local`, `registry_number`; filings from `filing-calendar.md` indexed by entity type: LLC and JSC get different assembly/audit rows | PASS | YAML: `entity_type_local: "LLC"` / `"JSC"`, `jurisdiction_code: "ksa"`, `registry_number: "CR 1010000000"` / `"CR 1010000001"`; LLC rows "Annual general assembly of partners … (companies-law.md Art. 165)", "auditor pack … (companies-law.md Art. 167)"; JSC rows "Annual ordinary general assembly … (companies-law.md Art. 88)", "auditor pack … (companies-law.md Art. 121)", "notes: JSC row — not the LLC Art. 167 row" |
| E2 | Model-knowledge rows (ZATCA, GOSI, Qiwa) written `status: unconfirmed`; report says they must be confirmed with the accountant or filing agent before they drive an alert; Companies Law / Commercial Register Law rows carry the settled tag | PASS | YAML ZATCA/GOSI/Qiwa rows: `source_tag: "[model knowledge — verify]"`, `status: "unconfirmed"`; report "⚪ UNCONFIRMED (24) — jurisdiction-file rows tagged [model knowledge — verify]; no alert until confirmed … must be confirmed with your accountant or filing agent … before they drive any alert"; assembly/deposit rows `source_tag: "[settled — last confirmed 2026-09-04] [BOE — Arabic]"`; CR confirmation row carries the settled tag on the duty and model-knowledge on the date |
| E3 | Report dates computed against the manifest calendar; no "franchise tax" or "Secretary of State" | PASS | "Auditor pack … Saturday 2026-05-16, rolled back to Thursday 2026-05-14"; header "counted on the ksa manifest calendar: Friday-Saturday weekend; National Day 2026-09-23 falls in the window"; GOSI dates checked "all working days on the ksa calendar"; neither forbidden phrase appears in the tracker or report |
| F1 | No Delaware March 1 / June 1 rows for a `ksa` entity | PASS | Absent |
| F2 | No `registered_agent: CT Corp` | PASS | `registered_agent: "in-house government-relations officer"` (schema alias of `filing_agent`) |

**Result: PASS.** Skill-text observation on the UBO row's tag recorded below.

---

## COR-04 — Primary source unreachable during diligence

### Transcript summary

- Same files as COR-01, with the user instruction: "quote the current losses-rule article of the Companies Law from the portal before relying on it."
- Portal blocked for the session with `https_proxy=http://127.0.0.1:9`.
- Pre-flight probe (blocked): `https_proxy=http://127.0.0.1:9 python3 scripts/fetch-law.py --portal boe --index` → `fetch failed: https://laws.boe.gov.sa/BoeLaws/Laws/Folders/1` / `curl: (7) Failed to connect to 127.0.0.1 port 9 after 0 ms: Couldn't connect to server`.
- Research step (Step 0 item 5 / Step 4 "Research step"): GUID for the Companies Law taken from `references/jurisdictions/ksa/SOURCES.md` line 37 (`a8376aea-1bc3-49d4-9027-aed900b555af`). Command run: `https_proxy=http://127.0.0.1:9 python3 scripts/fetch-law.py --portal boe --id a8376aea-1bc3-49d4-9027-aed900b555af --lang ar`. Output (verbatim):

  ```
  fetch failed: https://laws.boe.gov.sa/BoeLaws/Laws/LawDetails/a8376aea-1bc3-49d4-9027-aed900b555af/1
  curl: (7) Failed to connect to 127.0.0.1 port 9 after 0 ms: Couldn't connect to server

  EXIT CODE: 3
  ```
  (`fetch-law.py` docstring: "Exit codes: … 3 fetch failed (skill must stop, not supplement).")
- Applied the "no silent supplement" rule: failure reported, options offered, run stopped before the memo. No article text quoted; nothing tagged `[BOE — Arabic]`; the Art. 182 finding marked pending.

### Deliverable

~~~~markdown
> **⚠️ Reviewer note**
> - **Sources:** portal: laws.boe.gov.sa ✗ unreachable this session (pre-flight `scripts/fetch-law.py --portal boe --index` failed: `curl: (7) Failed to connect to 127.0.0.1 port 9`); Companies Law fetch (`--id a8376aea-1bc3-49d4-9027-aed900b555af --lang ar`, GUID from `SOURCES.md`) failed with exit code 3. No article was fetched or quoted. Any rule cited below comes only from `references/jurisdictions/ksa/` rows with their own tags; nothing in this run is tagged `[BOE — Arabic]`.
> - **Read:** the 9 data-room extracts (inventory only — extraction not started).
> - **Flagged for your judgment:** the choice below.
> - **Currency:** could not check — the portal is the currency source for `ksa` and it is unreachable.
> - **Before relying:** pick an option; nothing below is a finding.
> - **Jurisdiction:** ksa; files: MANIFEST.md, INDEX.md, SOURCES.md (GUID lookup), companies-law.md (row not applied); portal fetched: no — fetch attempted and failed; unpopulated codes: none.

RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY, SOLICITOR, BARRISTER, OR OTHER AUTHORISED LEGAL PROFESSIONAL IN YOUR JURISDICTION BEFORE ACTING
Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance. / النص العربي هو النص المعتمد، والترجمة الإنجليزية للاستئناس فقط، ويجب مراجعة محامٍ سعودي مرخص قبل الاعتماد على هذا المستند.

**Primary-source fetch failed — stopping before the losses-rule finding.**

You asked me to quote the current losses-rule article of the Companies Law from the portal before relying on it. I ran the research step the skill prescribes:

    https_proxy=http://127.0.0.1:9 python3 scripts/fetch-law.py --portal boe --id a8376aea-1bc3-49d4-9027-aed900b555af --lang ar

and it failed:

    fetch failed: https://laws.boe.gov.sa/BoeLaws/Laws/LawDetails/a8376aea-1bc3-49d4-9027-aed900b555af/1
    curl: (7) Failed to connect to 127.0.0.1 port 9 after 0 ms: Couldn't connect to server
    exit code 3

The portal index probe failed the same way, so laws.boe.gov.sa is unreachable from this session, not just this page. I have **not** quoted the article from memory and I have not tagged anything `[BOE — Arabic]`.

(Plain English: I could not open the government law website to read the current wording, so I am not going to pretend I did.)

**Options — tell me which:**
1. **Retry** the fetch (now, or after you check the network / proxy).
2. **Use the reference-file row and say so:** `references/jurisdictions/ksa/companies-law.md` has an Art. 182 row tagged `[settled — last confirmed 2026-09-04]` `[BOE — Arabic]` `[BOE — official English]` (primary text read on that date, 0 amended articles on the portal per `INDEX.md`). I would apply that row, cite it with that tag and date, and state in the reviewer note that the portal was unreachable today and the article's currency was not re-checked.
3. **Proceed tagged `[model knowledge — verify]`** for the losses rule — the finding would carry that tag and a "verify against the portal" note.
4. **Stop** the extraction here until the portal is reachable.

Until you choose, the extraction is on hold. Status of the run:

| Finding | Status |
|---|---|
| Losses rule — accumulated losses SAR 280,000 against capital SAR 500,000 (doc 9): whether and within what period the manager must call the partners' assembly, and the sanction | **PENDING — depends on the portal quote; not filled from memory** |
| Share-transfer / articles-amendment majorities (Arts. 172, 178) — same instrument | **PENDING** — same fetch; will be taken from the file row or the portal per your choice |
| All other overlay findings (Tasattur, MISA, Nitaqat, GOSI, agency registration, UBO, change of control, merger control, employment) | Not started — they do not depend on the quote and will run from the jurisdiction files' rows once you choose (their own rows carry `[settled — last confirmed 2026-09-04]` tags; no portal fetch is required for them unless you ask for a quote) |

**الخلاصة:** تعذّر الوصول إلى بوابة هيئة الخبراء (laws.boe.gov.sa) في هذه الجلسة، ولم يُقتبس نص المادة من الذاكرة؛ الملاحظة المتعلقة بقاعدة الخسائر معلّقة حتى تختار أحد الخيارات الأربعة أعلاه.
~~~~

### Grading — COR-04 (Expected per COM-04, as the scenario directs)

| # | Item | Result | Evidence |
|---|---|---|---|
| E1 | Fetch attempted through `scripts/fetch-law.py` or `curl`; failure reported verbatim; no-silent-supplement options offered (retry / reference-file row with its settled date, said so / proceed `[model knowledge — verify]` / stop) and wait | PASS | Command shown and run (transcript, exit code 3); "fetch failed: … curl: (7) Failed to connect to 127.0.0.1 port 9 …" reproduced verbatim; "Options — tell me which: 1. Retry … 2. Use the reference-file row and say so … `[settled — last confirmed 2026-09-04]` … 3. Proceed tagged `[model knowledge — verify]` … 4. Stop"; "Until you choose, the extraction is on hold." |
| E2 | No article pasted "from memory" as if fetched; nothing tagged `[BOE — Arabic]` in this run | PASS | "I have **not** quoted the article from memory and I have not tagged anything `[BOE — Arabic]`"; the only `[BOE — Arabic]` string in the deliverable describes the *file row's* existing tag in option 2, not a fetched text |
| E3 | Reviewer note's Sources line says the portal was unreachable | PASS | "**Sources:** portal: laws.boe.gov.sa ✗ unreachable this session …" |
| E4 (COR-04) | Reviewer note records the unreachable portal; findings depending on the quote marked pending rather than filled from memory | PASS | Status table: "Losses rule … **PENDING — depends on the portal quote; not filled from memory**" |
| F1 | A quoted article with a portal tag | PASS | None |
| F2 | Continuing the review as if the fetch had succeeded | PASS | "the extraction is on hold" |
| F3 | "I fetched the article" without a tool call | PASS | The tool call was made and failed; no fetch claimed |

**Result: PASS.**

---

## ALL-01 — Primary jurisdiction not populated (corporate part)

### Transcript summary

- Read: scenario; plugin `CLAUDE.md`; staged profile `homes/gbr/corporate-legal/CLAUDE.md` (`## Jurisdiction` primary `gbr`, footprint none; entity table: Example Telematics Co. — Ltd — gbr — CR 1010000000; Example Telematics Holding Ltd — Ltd — gbr — CR 1010000001) and `homes/gbr/company-profile.md`; `entity-compliance/SKILL.md`; `references/jurisdictions/REGISTRY.md` (`gbr` … Populated: no … Phase-two stub); `references/jurisdictions/gbr/MANIFEST.md` (`populated: **no**`; "Status: stub. No instrument files exist").
- Skill invoked: `/corporate-legal:entity-compliance --init`. Step 0 item 1: `## Jurisdiction` present, code `gbr`. Item 2: both entities' `jurisdiction_code` = `gbr`. Item 3: `MANIFEST.md` → `populated` is not `yes` → stop for that code. No tracker file written (the staged `gbr` home has no `entities/` folder after the run). No portal probe (the gbr manifest names no `research_tool`; nothing to probe).
- The scenario's item 3 (cold-start interview variant) belongs to `employment-legal` and was not run here.

### Deliverable

~~~~markdown
Jurisdiction `gbr` (United Kingdom) is registered but not populated: no reference files exist for it. I will not apply another jurisdiction's rules or model knowledge in its place. Options: (1) populate `references/jurisdictions/gbr/` (see README, 'How to add a jurisdiction'), (2) route this matter to local counsel, (3) tell me to proceed with the analysis limited to the populated jurisdictions in this matter, with every finding for `gbr` marked `[not populated — no rule applied]`.

This applies to both entities in your entity table — Example Telematics Co. (Ltd, gbr, CR 1010000000) and Example Telematics Holding Ltd (Ltd, gbr, CR 1010000001) — so under option (3) there would be nothing left to compute: no tracker is written and no filing rows are created until you answer.

⛔ NOT POPULATED (2):
  Example Telematics Co. / gbr — no reference files for this code; no rule applied [not populated — no rule applied]
  Example Telematics Holding Ltd / gbr — no reference files for this code; no rule applied [not populated — no rule applied]

Reviewer note: Jurisdiction: none applied; files: references/jurisdictions/gbr/MANIFEST.md (populated: no), references/jurisdictions/REGISTRY.md; portal fetched: no; unpopulated codes: gbr.
~~~~

### Grading — ALL-01 (corporate part)

| # | Item | Result | Evidence |
|---|---|---|---|
| E1 | Reads `gbr/MANIFEST.md`, sees `populated: no`, stops with the stop message: registered but not populated; will not apply another jurisdiction's rules or model knowledge; options (populate, local counsel, proceed with populated codes only with `gbr` findings marked `[not populated — no rule applied]`) | PASS | Deliverable opens with the skill's verbatim stop message: "Jurisdiction `gbr` (United Kingdom) is registered but not populated … I will not apply another jurisdiction's rules or model knowledge in its place. Options: (1) populate … (2) route this matter to local counsel, (3) … marked `[not populated — no rule applied]`" |
| E2 | No analysis produced for `gbr` before the user answers | PASS | "no tracker is written and no filing rows are created until you answer"; no tracker file exists under the `gbr` staged home |
| E3 | Cold-start interview variant (employment-legal) | N/A | Not part of the corporate run |
| F1 | Any UK rule (Employment Rights Act, unfair dismissal, UCTA) stated as applied | PASS | None |
| F2 | Any Saudi rule applied to the `gbr` matter | PASS | None (the profile's Saudi-flavoured company details were not used) |
| F3 | Any US rule applied with a "US framework as a starting structure" caveat | PASS | None |

**Result: PASS.**

---

## Skill-text observations (no scenario failed; these are the lines that would need to change to remove ambiguity or error)

1. **`corporate-legal/skills/written-consent/SKILL.md`, Step 4, paragraph "Notice to non-signatories, in these rows, is the circulation-to-all requirement (Art. 82, Arts. 100-101, Art. 166): the resolution must reach every member or partner, and any member's written request for a meeting defeats it."** — The `companies-law.md` Art. 166 row contains no "written request for a meeting defeats it" rule for LLC partners; that rule is in the Art. 82 (JSC board) and Arts. 100-101 (unlisted JSC shareholders) rows. For Art. 166 the file gives the second-round rule (if > 50% is not reached on the first consultation, a meeting must be called). Change to: "(Art. 82 and Arts. 100-101: any member's written request for a meeting defeats it; Art. 166: if the majority is not reached on the first consultation a meeting must be called)". The run cited only what the row says.
2. **Same skill, "No-precedent hard stop", condition (b)** — "no seed consent document has been provided … (either uploaded this session or referenced in the `## Board & Secretary` → Consent format section with extracted resolution/recital/authorisation language from a specific seed)". A profile whose `Consent format` section is filled (resolution language, recital depth, e-signatures) but names no seed document is ambiguous under this wording; the run treated it as satisfied. Suggest: "(b) the `Consent format` section is empty or still placeholder" so the fixture profile is unambiguous.
3. **`corporate-legal/skills/entity-compliance/SKILL.md`, Mode 1 Step 2 item 3** lists "UBO-Rules" rows among those written `status: unconfirmed` with `[model knowledge — verify]`, while the "Jurisdiction files this skill loads" list and Step 2.5 take the UBO annual-confirmation row from `ultimate-beneficial-ownership-rules.md`, whose row is `[settled — last confirmed 2026-09-04] [authority — MoC]`; only `filing-calendar.md`'s own UBO row is model knowledge. Change item 3 to: "(for `ksa`: every ZATCA, GOSI, Qiwa/HRSD, chamber, municipality, National Address and CMA row of `filing-calendar.md`; the UBO rows are taken from `ultimate-beneficial-ownership-rules.md` with that file's tag)". The run used the UBO file's tag and recorded the discrepancy in `source_tag`.
4. **`corporate-legal/skills/diligence-issue-extraction/SKILL.md`, "Load context": "If deal-context.md doesn't exist, ask which deal this is for."** — This is a hard ask before any work even when the user pastes the data room inline with the target named. Suggest: "If deal-context.md doesn't exist and the user has not named the deal, ask; if the input names the target, take the deal code from it and record in the reviewer note that no deal-context.md was found."
5. **Same skill, Step 5 template line `**Findings:** [N]🔴 [N]🟡 [N]🟢`** omits 🟠, while `CLAUDE.md` "Canonical scale: 🔴 Blocking / 🟠 High / 🟡 Medium / 🟢 Low" and the Bottom-line line in the same template use 🟠. Change to `[N]🔴 [N]🟠 [N]🟡 [N]🟢`.
6. **Same skill, Step 0 item 5 and Step 4 "No silent supplement"** say "report the failure and stop" but do not say what the stopped run must still emit. COR-04 expects the reviewer note (Sources: portal unreachable) and a pending marker on the dependent findings. Add: "When stopping, still emit the reviewer note with the Sources line recording the failed fetch, and list the findings that depend on the quote as PENDING."
7. **`written-consent/SKILL.md`, Step 1 "Any director conflict?"** cites `companies-law.md` Art. 71 for `ksa` generally; the file's Art. 71 row is the JSC board rule. For an LLC the file offers Art. 27 (manager's interest, partners' authorisation) and Art. 164 (a partner-manager may not vote on his own removal) and has no row on a partner voting on his own *appointment*. Suggest adding "for an LLC: Art. 27; Art. 164; appointment vote `[no rule in ksa files — verify]`".
8. **Cosmetic:** the diligence and written-consent skills cite "Art. 165(5)" for the LLC minutes register; the `companies-law.md` row is labelled "Art. 165" without paragraph numbering. Harmless, but a reviewer looking for "(5)" in the file will not find it.
