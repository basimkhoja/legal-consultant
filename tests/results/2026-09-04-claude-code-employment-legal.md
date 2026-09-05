# Scenario run — employment-legal — Claude Code

| Field | Value |
|---|---|
| Runtime | Claude Code (Claude Fable 5.1), session https://claude.ai/code/session_01E4PDzmqCCJ2GWgRUVinS7K |
| Date | 2026-09-04 |
| Staged config root | `LEGAL_CONSULTANT_HOME=/private/tmp/claude-501/-Users-basimkhoja-Projects-Legal-Consultant/1f545f98-4d5d-4436-a662-dc5dc3bed1b6/scratchpad/homes/ksa` (ALL-01: `.../homes/gbr`) |
| Jurisdiction tree | `references/jurisdictions/` at the repo root |
| Portal pre-flight (normal network) | `python3 scripts/fetch-law.py --portal boe --index` returned the BOE law index (first rows: Arbitration Law (Old), Automobile Union Law, Banking Control Law, ...) — `portal: laws.boe.gov.sa ✓ reachable` for EMP-01, EMP-02, EMP-03 |
| Portal pre-flight (EMP-04, `https_proxy=http://127.0.0.1:9`) | `fetch failed: https://laws.boe.gov.sa/BoeLaws/Laws/Folders/1` / `curl: (7) Failed to connect to 127.0.0.1 port 9` — `portal: laws.boe.gov.sa unreachable` |
| Files not modified | Nothing in the repo was edited except this results file |

## Summary

| Scenario | Skill | Result | Notes |
|---|---|---|---|
| EMP-01 | `/employment-legal:termination-review` | **PASS** | All 7 expected items present with computed-number tags; no forbidden term. One grading note on the substring "warn" inside "written warning" (not the US notice statute). |
| EMP-02 | `/employment-legal:hiring-review` | **PASS** | All 3 expected items present; no forbidden term. Transfer-in under Low Green tagged `[no rule in ksa files — verify]` because the Services-by-Range row is silent. |
| EMP-03 | `/employment-legal:wage-hour-qa` | **PASS** | Computed on the stated basic wage with the actual-wage component flagged `[review]`; divisor stated and tagged; no forbidden term. |
| EMP-04 | `/employment-legal:termination-review` (portal blocked) | **PASS** | Fetch attempted, failure reported verbatim, three options offered, no quote fabricated, no number computed, nothing tagged `[BOE — Arabic]`. |
| ALL-01 (employment) | `/employment-legal:termination-review` + `/employment-legal:cold-start-interview` (gbr) | **PASS** | Stop message emitted before any analysis; interview refuses to write the profile and offers `usa` or `ksa`. |

Skill-text fixes required by a FAIL: **none**. Observations that would tighten the text are listed at the end.

---

## EMP-01 — Termination of an indefinite-contract employee

### Transcript summary

- Files loaded: staged `company-profile.md`, staged `employment-legal/CLAUDE.md` (Role: Non-lawyer with attorney access; primary `ksa`; bilingual; SAR; local counsel N/A; escalation table), plugin `employment-legal/CLAUDE.md` (`## Outputs`, tag vocabulary, guardrails), `employment-legal/skills/termination-review/SKILL.md`, `references/jurisdictions/JURISDICTION-STEP.md`, `references/jurisdictions/REGISTRY.md`, `references/jurisdictions/ksa/MANIFEST.md` (populated: yes), `INDEX.md`, `playbook-defaults.md` (Labor table), `labor-law.md` (Arts. 2, 8, 9-10, 37, 53-56, 61, 64, 66-73, 74-88, 96, 111, 116, 117, 137, 151, 155, 160, 234-235, "How skills should use this file"), `labor-law-implementing-regulations.md` (Reg. Arts. 12, 14 Second, 19/Annex 5 cl. 6, 22 bis, Annex 5 cls. 8, 9-10, 11, 13, 14-15; Annex 1 Arts. 57, 71; "How skills"), `labor-dispute-route.md` (Art. 234(a), 235, 72/Annex 1 Art. 71, Art. 8, Annex 5 cls. 13.4, 14.1, Reg. Art. 14 Second 8(a), "Computed dates", stop rule), `platform-obligations.md` (Art. 40, Art. 90, Art. 51/Reg. Art. 18, Reg. Art. 14 Second rows, exit row, GOSI row), `social-insurance-law.md` (Arts. 7, 16, 45), `saudization-nitaqat.md` (Art. 26, Reg. Art. 8, Art. 35, Services-by-Range row, counting rules), `occupational-safety.md` (Arts. 80(2), 122, 137). Input: `tests/fixtures/inputs/EMP-01-termination-facts.md`.
- Matter workspaces: `Enabled ✗` (in-house) — skipped.
- Step 0: profile primary `ksa`, footprint none; matter facts (Saudi national, Qiwa contract, place of employment ksa) add no code; MANIFEST `populated: yes`; calendar Friday-Saturday weekend, National Day 23 Sep, Founding Day 22 Feb, Eids; currency SAR; bilingual output; disclaimer line; portal probe ✓ reachable. No instrument fetched (no quote requested).
- Step 1 facts block asked (see deliverable — facts supplied by the fixture marked, the rest listed as open). Age and group-termination questions not asked (`usa`-only).
- Step 2 flags, Step 2a award, Step 2b Art. 77, Step 3 requirements and timeline, Step 4 release, Step 5 documentation run. Numbers computed in Python from the file rows (script output retained in the session): service 2021-03-01 to 2026-09-30 inclusive = 5y 7m 0d; earliest lawful termination date on 60 days' notice from 2026-09-04 = 2026-11-03 (Tuesday).
- Consequential-action gate applied (non-lawyer). Decision tree appended.

### Deliverable

~~~~markdown
> **⚠️ Reviewer note**
> - **Sources:** portal: laws.boe.gov.sa ✓ reachable (index probe, `scripts/fetch-law.py --portal boe --index`); no article fetched this session — every rule below is a row of `references/jurisdictions/ksa/` cited by article with the row's own tag. Files applied: `labor-law.md`, `labor-law-implementing-regulations.md`, `labor-dispute-route.md`, `platform-obligations.md`, `social-insurance-law.md`, `saudization-nitaqat.md`, `occupational-safety.md`, `playbook-defaults.md`, `MANIFEST.md`.
> - **Read:** the termination facts sheet (1 page) and the practice profile; no contract, warning letters or Qiwa record were provided.
> - **Flagged for your judgment:** 7 items marked `[review]` inline (housing allowance in "last wage"; fractional-year treatment under Art. 77; whether lateness after warnings is a "legitimate reason"; Art. 80(2) route; pro-rating of pay in lieu; Nitaqat band movement; SANED exit coding).
> - **Currency:** rows applied are `[settled — last confirmed 2026-09-04]` unless tagged otherwise; Eid dates used for the calendar checks are `[model knowledge — verify]` (the manifest names the holidays, not their 2026-2027 Gregorian dates).
> - **Before relying:** (1) fix the notice date — the planned 2026-09-30 date is 34 days short of Art. 75; (2) send the warning letters, their Art. 71 minutes and the Qiwa record to external Saudi counsel (profile escalation: high-risk flag present).
> - Jurisdiction: `ksa`; files: labor-law.md, labor-law-implementing-regulations.md, labor-dispute-route.md, platform-obligations.md, social-insurance-law.md, saudization-nitaqat.md, occupational-safety.md, playbook-defaults.md, MANIFEST.md; portal fetched: no (probe only); unpopulated codes: none.

RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY, SOLICITOR, BARRISTER, OR OTHER AUTHORISED LEGAL PROFESSIONAL IN YOUR JURISDICTION BEFORE ACTING

Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance.
النص العربي هو النص المعتمد، والترجمة الإنجليزية للاستئناس فقط، ويجب مراجعة محامٍ سعودي مرخص قبل الاعتماد على هذا المستند.

## Termination Review: Ahmed (synthetic) — 2026-09-04

**Jurisdiction:** `[ksa]`
**Contract type / nationality:** indefinite, Qiwa-documented, monthly-paid / Saudi national
**Reason:** repeated lateness after two written warnings (2026-05-10, 2026-07-02) under the certified work regulations — employer termination for a legitimate reason, `labor-law.md` Art. 74(3) with Art. 75 (Art. 80(2) considered and not recommended, below)
**Planned date:** 2026-09-30 (Wednesday, Gregorian per Annex 5 cl. 14.6) — **not achievable on notice given today; earliest lawful date 2026-11-03**

---

### Facts the ksa file needs (Step 1)

Supplied by the facts sheet: nationality (Saudi); contract type and platform (indefinite, Qiwa); start date 2021-03-01; last wage basic SAR 12,000 + housing SAR 3,000 cash, no commissions, no in-kind benefits stated; ground (lateness) and the two written-warning dates; not on leave, not in probation; notice to be given 2026-09-04 for 2026-09-30; no contractual compensation clause; 12 days' untaken annual leave.

Still open — please confirm before the termination is actioned (none of these blocks the computations, which use the facts as given):
1. Were the two warnings issued after a written charge, an interview and signed minutes placed on file (`labor-law.md` Art. 71), and was each notified through the Portal (Annex 5 cl. 14.1, `labor-law-implementing-regulations.md`)? Do the certified work regulations' penalty ladder (Art. 67; Annex 1 Arts. 58-68) require a further step (fine, suspension) before termination for the same violation? `[review]`
2. Did Ahmed grieve either warning within 30 days (Art. 72 / Annex 1 Art. 71), or raise any complaint (HR, HRSD, ethics) recently?
3. Is any transport allowance or other allowance paid with the wage (Art. 61(6); Annex 5 cls. 9-10)? The facts sheet lists housing only — computed on that basis.
4. Does the Qiwa contract set a notice period longer than 60 days (Art. 75 with Art. 8)?
5. Is there an Art. 83 non-compete or confidentiality clause to restate on exit?
6. Is anyone else with the same lateness record not being terminated (comparator, Arts. 3 and 61(4))?
7. Are wages and allowances current and paid through an approved bank / Mudad (Art. 90; WPS row `[model knowledge — verify]`)?
8. Nitaqat band: the profile records Low Green (IT activity) as of 2026-08-01 `[user provided]`; a fresh dated Qiwa export at the termination date is needed to state the impact.

---

### Bottom line

**Do not terminate on 2026-09-30.** Written notice given today (2026-09-04) satisfies `labor-law.md` Art. 75(b) only from **2026-11-03**; either move the termination date to 2026-11-03 or later, or pay in lieu under Art. 76 (SAR 30,000 on the face of the text for the full 60 days; SAR 17,000 if a court pro-rates the 34-day shortfall `[model knowledge — verify]`). On the Art. 75 route the full end-of-service award is due — **SAR 46,250** on the planned date (SAR 47,625 if the date moves to 2026-11-03) — and, if a court does not accept "repeated lateness after two warnings" as a legitimate reason, Art. 77 exposure is **SAR 37,500 (whole years) to SAR 41,875 (pro-rata)**, on top of the award and notice. The notice-defect flag fires, so per the practice profile this goes to external counsel before it proceeds.

**الخلاصة:** لا تُنهِ العقد بتاريخ 30/09/2026. فالإشعار الكتابي الموجَّه اليوم (04/09/2026) لا يستوفي مهلة الستين يوماً في المادة (الخامسة والسبعين/ب) من نظام العمل إلا اعتباراً من **03/11/2026**؛ فإمّا تأجيل تاريخ الإنهاء إلى 03/11/2026 أو ما بعده، أو دفع بدل مهلة الإشعار وفق المادة (السادسة والسبعين) (30,000 ريال عن المهلة كاملة بحسب ظاهر النص؛ أو 17,000 ريال إن قدّرت المحكمة النقص البالغ 34 يوماً بالنسبة [معرفة نموذجية — يُتحقق منها]). وعلى مسار المادة (75) تستحق مكافأة نهاية الخدمة كاملة — **46,250 ريالاً** على التاريخ المخطط (47,625 ريالاً إذا أُجّل الإنهاء إلى 03/11/2026) — وإذا لم تقبل المحكمة «التأخر المتكرر بعد إنذارين» سبباً مشروعاً فإن التعرّض للتعويض بموجب المادة (السابعة والسبعين) يتراوح بين **37,500 و41,875 ريالاً** إضافةً إلى المكافأة وبدل الإشعار. وقد تحققت علامة «خلل الإشعار»، فيُرفع الأمر إلى المستشار الخارجي وفق ملف الممارسة قبل المضي.

**One question I'd ask that isn't in my checklist:** the second warning was 2026-07-02 and notice is being given 2026-09-04 — what lateness occurred between those dates, and is it recorded on the attendance register (Reg. Art. 5)? If the answer is "nothing new", a court will ask why now.

---

### High-risk flags (Step 2)

| Flag | Source row | Result |
|---|---|---|
| Recent complaint | neutral row; `labor-law.md` Arts. 3, 61(4) | ❓ Not stated — confirm (open fact 2) |
| Protected leave: illness / maternity / work injury | `labor-law.md` Art. 82, Art. 155; Art. 137 via `occupational-safety.md` | ✅ Clear — not on any leave (facts sheet) |
| Protected class + timing | `labor-law.md` Arts. 3, 61(4) | ✅ Nothing indicated |
| Thin documentation | neutral row | ✅ Two written warnings under certified work regulations (2026-05-10, 2026-07-02); Art. 68's 180-day repetition rule is satisfied (53 days apart). Confirm Art. 71 minutes (open fact 1) |
| Comparator | neutral row | ❓ Confirm (open fact 6) |
| Contract / handbook promise | neutral row; `labor-law.md` Art. 67 (penalties only as listed in the Law or the work regulations) | ❓ Confirm the work regulations' ladder does not require a further penalty before termination `[review]` |
| Art. 80 ground not met or worker not heard | `labor-law.md` Art. 80 chapeau, Art. 71, Art. 69; Annex 1 Arts. 63-68 | ⚪ Not invoked — the plan is an Art. 75 notice termination, so no Art. 80 procedure is needed. If you wanted the no-award route, lateness would have to be framed as Art. 80(2) "failure to perform essential obligations / disobedience of lawful orders" after a hearing, inside the Art. 69 30-day clocks; a failed condition falls back to Art. 77 + Art. 76 + the full award (Art. 80 row). Not recommended on these facts `[review]` |
| **Notice defect** | `labor-law.md` Art. 75 (60 days employer, monthly-paid indefinite), Art. 76, Annex 5 cl. 14.1 (Portal) | 🔴 **FLAG** — 2026-09-04 → 2026-09-30 is 26 days; statutory minimum 60. The notice must be written, state the legitimate reason, and go through the Portal |
| WPS arrears / late wages | `platform-obligations.md` Art. 90 row; WPS row `[model knowledge — verify]`; `labor-law.md` Art. 81(1), Art. 94 | ❓ Confirm (open fact 7) |
| **Art. 77 exposure** | `labor-law.md` Art. 77; Art. 75 row ("legitimate reason" not defined in the Law) | 🟠 **FLAG** — whether repeated lateness after two warnings is a legitimate reason is court practice (Art. 75 open question) `[review]`; exposure computed in Step 2b |
| Nitaqat impact | `saudization-nitaqat.md` Services-by-Range row, Art. 35, Reg. Art. 8 | 🟡 **FLAG** — a Saudi leaving lowers the rate on the rolling average; the entity is Low Green as of 2026-08-01 `[user provided]` (no new visas, no occupation changes). Whether this departure moves the band cannot be inferred from the file's coefficients — read the Qiwa dashboard, dated `[review]` |
| Work-permit and exit consequences | `platform-obligations.md` Art. 40, Reg. Art. 14 Second | ✅ Not applicable — Saudi national |
| Retirement-age termination | `labor-law.md` Art. 74(4); `social-insurance-law.md` Art. 16 | ✅ Not applicable |
| Waiver or release during the contract | `labor-law.md` Art. 8 | ⚪ See Severance and release |
| Grievance ladder and litigation freeze | `labor-dispute-route.md` Art. 72 / Annex 1 Art. 71; Art. 235; Art. 234(a); Reg. Art. 14 Second 8(a) | ❓ Confirm no grievance or suit is pending (open fact 2); if one is, Art. 235 freezes terms |
| Unemployment-insurance coding | `social-insurance-law.md` Art. 45; coding practice `[model knowledge — verify]` | 🟡 **FLAG** — an Art. 75 termination recorded as such at GOSI does not disqualify SANED; recording it as an Art. 80 dismissal would `[review]` |

**Escalation:** Escalate to **External counsel** before proceeding — profile `## Escalation`: "Performance termination → HR + Legal Lead → External counsel when high-risk flags present" (notice defect fires; Art. 77 exposure fires).

---

### Jurisdiction requirements (`[ksa]`)

- **End-of-service award (Step 2a):** **SAR 46,250** `[computed — labor-law.md Arts. 84-85, settled 2026-09-04; inputs: last wage SAR 15,000 (basic 12,000 + housing allowance 3,000 paid in cash with the wage), service 5y 7m (2021-03-01 to 2026-09-30 inclusive, Gregorian per Annex 5 cl. 14.6, month = 30 days per Art. 2), employer termination under Art. 75 → multiplier 1]`.
  Formula (Art. 84): Award = 0.5 × W × min(S, 5) + 1.0 × W × max(S − 5, 0) = 0.5 × 15,000 × 5 + 15,000 × 0.5833 = 37,500 + 8,750 = **46,250**. Multiplier: employer-initiated termination → × 1 (Art. 85 fractions and Art. 87 do not apply; no Art. 54 probation; no Art. 80 ground invoked). No Art. 86 exclusion (no commissions); no Art. 116 unpaid-leave deduction stated.
  Wage input — the file's position: Art. 2 row (settled): "wage" means the actual wage, and "housing and transport allowances paid with the wage under Art. 61(5)-(6) are therefore part of the wage for end-of-service award and Art. 77 purposes"; the Art. 61 row adds "unless a court holds otherwise `[model knowledge — verify]`" and the file lists it as an open question. Computed on W = 15,000 accordingly; on basic only (W = 12,000) the award would be SAR 37,000 `[computed — labor-law.md Arts. 84-85, settled 2026-09-04; inputs: W 12,000, S 5y 7m, employer termination]` `[review]` `[model knowledge — verify]` as to the inclusion.
  If the termination date moves to 2026-11-03: S = 5y 8m 3d → **SAR 47,625** `[computed — labor-law.md Arts. 84-85, settled 2026-09-04; inputs: W 15,000, S 5.6750 years (2021-03-01 to 2026-11-03), employer termination]`.
- **Compensation for termination without a legitimate reason (Step 2b):** applies only if a court rejects the stated reason. Indefinite contract, no contractual figure (Art. 77 chapeau). Daily wage = 15,000 ÷ 30 = SAR 500 (Art. 2). 15 days × SAR 500 × 5 whole years = **SAR 37,500**; on pro-rata years (5.5833) = **SAR 41,875** `[computed — labor-law.md Art. 77(1),(3), settled 2026-09-04; inputs: actual wage SAR 15,000, daily SAR 500, service 5y 7m, indefinite, no contractual figure; two-month floor SAR 30,000 not binding]`; fractional-year treatment is not in the text — both shown `[model knowledge — verify]` `[review]`. "Last wage in practice" for Art. 77 is `[model knowledge — verify]` (Art. 77 row). This is **in addition to** the award and pay in lieu (Art. 77 row).
- **Notice:** 60 days' written notice from the employer, stating the legitimate reason, through the Portal (`labor-law.md` Art. 75(b); Annex 5 cl. 14.1). Earliest lawful termination date on notice given 2026-09-04 = **2026-11-03** `[computed — labor-law.md Art. 75, settled 2026-09-04; inputs: notice date 2026-09-04 + 60 days, Gregorian calendar (Annex 5 cl. 14.6); MANIFEST calendar check: Tuesday, not a Friday/Saturday, not National Day (23 Sep) or Founding Day (22 Feb); Eid al-Fitr and Eid al-Adha 2026 fall in March and May [model knowledge — verify] — no roll]`. Planned 2026-09-30 → shortfall 34 days. Pay in lieu (Art. 76) at the actual wage: full period **SAR 30,000** `[computed — labor-law.md Art. 76, settled 2026-09-04; inputs: W 15,000 × 60 days ÷ 30]`; 34-day shortfall **SAR 17,000** `[computed — labor-law.md Art. 76, settled 2026-09-04; inputs: W 15,000 × 34 ÷ 30]` — the M/46 text dropped "the remainder", so pro-rating is `[model knowledge — verify]` `[review]`. During the notice period Ahmed may take one paid day a week or eight hours to look for work, and you may put him on garden leave with service continuing (Art. 78).
- **Leave and other balances:** untaken annual leave 12 days × SAR 500 = **SAR 6,000** `[computed — labor-law.md Art. 111 with Art. 2, settled 2026-09-04; inputs: 12 days, W 15,000 ÷ 30]`; the day basis (calendar vs working day, Annex 5 cl. 8.1) is `[model knowledge — verify]`. Compensatory-leave balance (Reg. Art. 22 bis(4)) and overtime: none stated — confirm.
- **Final settlement:** all dues within one week of the end of the relationship where the employer ended it (`labor-law.md` Art. 88; Annex 5 cl. 11.9): planned date → due **2026-10-07** (Wednesday) `[computed — labor-law.md Art. 88, settled 2026-09-04; inputs: 2026-09-30 + 7 days, MANIFEST calendar, no roll]`; if 2026-11-03 → due 2026-11-10 (Tuesday). Paid into Ahmed's bank account through an approved bank (Art. 90). Set-off only for quantified work-related debts (Art. 88 row, `[model knowledge — verify]` as to clearance holds).
- **Documents:** service certificate with joining date, end date, profession and last wage, no damaging content, plus return of his deposited documents (Art. 64); Qiwa termination record and Portal notice (Annex 5 cl. 14.1; `platform-obligations.md` Art. 51 / Reg. Art. 18 row — platform identity `[model knowledge — verify]`); GOSI de-registration with the exit reason (`social-insurance-law.md` Art. 7; the 15-day practice deadline and SANED coding are `[model knowledge — verify]`); restate any Art. 83 clause (open fact 5).
- **Timeline:** limitation = end of relationship + 12 months → **2027-09-30** (Thursday) on the planned date, 2027-11-03 (Wednesday) on the 2026-11-03 date `[computed — labor-dispute-route.md Art. 234(a) "Computed dates", settled 2026-09-04; inputs: end date + 12 months, Gregorian]`; Ahmed's claim is not time-barred while employed. If the termination is grieved as a penalty decision: objection within 30 days excluding official holidays of notification (2026-09-04 + 30 days, National Day 23 Sep excluded → 2026-10-05, Monday), employer answer within 15 days (→ 2026-10-20), then Labor Court within 30 days excluding official holidays (→ 2026-11-19) `[computed — labor-dispute-route.md Art. 72 / Annex 1 Art. 71 "Computed dates", settled 2026-09-04; inputs: notification 2026-09-04, MANIFEST holidays]`; whether an Art. 75 notice is a "penalty" for this ladder is `[model knowledge — verify]`. Friendly settlement precedes any suit (Annex 5 cl. 13.4). Once a suit is filed, no change of terms (Art. 235).
- **Gaps:** collective-dismissal rules — not relevant here; nothing else needed was missing from the files.

**Numbers table** (planned termination date 2026-09-30; W = SAR 15,000)

| Item | Amount (SAR) | Source row and tag | Inputs |
|---|---|---|---|
| End-of-service award | 46,250 | `labor-law.md` Arts. 84-85, settled 2026-09-04 `[BOE — Arabic]`; housing inclusion `[model knowledge — verify]` | W 15,000; S 5y 7m; employer termination × 1 |
| Compensation, Art. 77 (only if the reason is held illegitimate) | 37,500 (whole years) / 41,875 (pro-rata) | `labor-law.md` Art. 77(1),(3), settled 2026-09-04; fractional years `[model knowledge — verify]` | W 15,000; daily 500; S 5 / 5.5833; floor 30,000 not binding |
| Pay in lieu of notice, Art. 76 (if the date is not moved) | 30,000 (full 60 days) / 17,000 (34-day shortfall, pro-rated) | `labor-law.md` Art. 76, settled 2026-09-04; pro-rating `[model knowledge — verify]` | W 15,000; 60 / 34 days ÷ 30 |
| Leave payout, Art. 111 | 6,000 | `labor-law.md` Art. 111, settled 2026-09-04; day basis `[model knowledge — verify]` | 12 days × 500 |
| Total settlement (award + leave; excluding contested Art. 77 and any pay in lieu) | 52,250 | `labor-law.md` Art. 88 window | due 2026-10-07 |

**جدول المبالغ** (تاريخ الإنهاء المخطط 30/09/2026؛ الأجر الأخير 15,000 ريال)

| البند | المبلغ (ريال) | المصدر والوسم | المدخلات |
|---|---|---|---|
| مكافأة نهاية الخدمة | 46,250 | نظام العمل، المادتان (84) و(85) — ملف `labor-law.md`، مؤكَّد بتاريخ 04/09/2026؛ إدراج بدل السكن في الأجر الأخير [معرفة نموذجية — يُتحقق منها] | الأجر 15,000؛ مدة الخدمة 5 سنوات و7 أشهر؛ إنهاء من صاحب العمل × 1 |
| التعويض بموجب المادة (77) (فقط إذا لم يُقبل السبب مشروعاً) | 37,500 (سنوات كاملة) / 41,875 (بالنسبة) | نظام العمل، المادة (77) الفقرتان (1) و(3)، مؤكَّد 04/09/2026؛ معاملة كسور السنة [معرفة نموذجية — يُتحقق منها] | الأجر 15,000؛ الأجر اليومي 500؛ المدة 5 / 5.5833؛ الحد الأدنى 30,000 غير مؤثر |
| بدل مهلة الإشعار، المادة (76) (إذا لم يُؤجَّل التاريخ) | 30,000 (المهلة كاملة) / 17,000 (النقص 34 يوماً بالنسبة) | نظام العمل، المادة (76)، مؤكَّد 04/09/2026؛ الاحتساب بالنسبة [معرفة نموذجية — يُتحقق منها] | الأجر 15,000؛ 60 / 34 يوماً ÷ 30 |
| بدل الإجازة السنوية غير المستعملة، المادة (111) | 6,000 | نظام العمل، المادة (111)، مؤكَّد 04/09/2026؛ أساس احتساب اليوم [معرفة نموذجية — يُتحقق منها] | 12 يوماً × 500 |
| إجمالي تصفية الحقوق (المكافأة + الإجازة؛ دون التعويض المتنازع فيه وبدل الإشعار) | 52,250 | المادة (88) — مهلة أسبوع | يُستحق في 07/10/2026 |

---

### Severance and release

- Severance: none above the statutory entitlement (profile `## Termination review` → Standard severance: none). The award, leave payout, wages and any Art. 77 amount are statutory floors, not severance.
- Release: not required (profile: N). Any release or settlement of statutory rights signed while the contract is running is void unless more beneficial to Ahmed (`labor-law.md` Art. 8, settled 2026-09-04). A post-termination settlement is outside Art. 8's wording; court treatment of one below the statutory floor, and the practice of recording it before the labour authority, are `[model knowledge — verify]` (`labor-dispute-route.md` Art. 8 row) — route any settlement wording to external counsel.
- Non-compete / confidentiality: Art. 83 only if the contract has such a clause (open fact 5).

---

### Documentation

Two written warnings under the certified work regulations (2026-05-10, 2026-07-02) support the "legitimate reason". To hold up: each warning should show a written charge, an interview, Ahmed's defence and signed minutes on file (Art. 71), and a Portal record (Annex 5 cl. 14.1); the attendance register (Reg. Art. 5) should show the lateness before and after each warning. Gap: nothing in the facts records lateness between 2026-07-02 and today — document the incidents that prompted the decision now.

---

### Go / No-go

**Hold — escalation pending and notice date to be fixed.** Proceed only after (a) the termination date is moved to 2026-11-03 or later, or pay in lieu is approved, and (b) external counsel has reviewed the warning file (profile escalation).

> Terminating an employee has legal consequences — unlawful-termination, discrimination and wage claims all trace back to how this decision is structured. Have you reviewed this termination with an attorney? If yes, proceed. If no, here's a brief to bring to them:
> - Employee: Ahmed, Saudi national, indefinite Qiwa contract since 2021-03-01, `[ksa]`; reason: repeated lateness after two written warnings; planned date 2026-09-30 (earliest lawful 2026-11-03).
> - High-risk flags: notice defect (26 days given, 60 required, Art. 75); Art. 77 exposure if the reason is rejected; Nitaqat rate impact (Low Green entity, dated 2026-08-01); SANED coding at de-registration.
> - Numbers: award SAR 46,250 (Arts. 84-85; inputs above); Art. 77 SAR 37,500-41,875 (Art. 77; inputs above); pay in lieu SAR 30,000 / 17,000 (Art. 76); leave SAR 6,000 (Art. 111); settlement within 7 days (Art. 88).
> - Documents: service certificate (Art. 64), Qiwa termination record, GOSI de-registration with exit reason.
> - Release: none during the contract (Art. 8); post-termination settlement treatment `[model knowledge — verify]`.
> - Open: Art. 71 minutes for the warnings; whether the work regulations require a further penalty step; any complaint or grievance; transport allowance; contractual notice; comparator; wage-payment status; fresh Nitaqat export.
> - What could go wrong: a court treats the reason as not legitimate → Art. 77 + Art. 76 + full award; a defective (short or off-Portal) notice → Art. 76 pay in lieu regardless.
> - Ask the attorney: is "repeated lateness after two warnings" accepted as a legitimate reason in current Labor Court practice; is the housing allowance in "last wage" in practice; should the date move or should we pay in lieu; is the local counsel named in the profile (N/A) to be replaced by the external counsel in the escalation table.
>
> If you need to find an attorney or other authorised legal professional: for `ksa` the licensing body is the Ministry of Justice (MANIFEST `issuing_authorities`); ask for a referral.

### Checklist for term day (`[ksa]`)

- [ ] Written notice for 60 days (or longer contractual period) through the Portal stating the reason, or pay in lieu computed (Arts. 75-76, Annex 5 cl. 14.1)
- [ ] Award SAR 46,250, leave payout SAR 6,000, any Art. 77 amount, computed with tags (Steps 2a, 2b, Art. 111); no compensatory-leave balance confirmed (Reg. Art. 22 bis(4))
- [ ] Final settlement paid through an approved bank within 7 days of the end date (Art. 88; due 2026-10-07 on the planned date)
- [ ] Service certificate and returned documents (Art. 64)
- [ ] Qiwa termination record; GOSI de-registration with the exit reason coded as an Art. 75 termination (`platform-obligations.md`; `social-insurance-law.md` Art. 7, Art. 45 `[model knowledge — verify]` as to coding)
- [ ] Settlement wording, if any, drafted after the relationship ends and reviewed by external counsel (Art. 8)
- [ ] Return of property / access cutoff coordinated
- [ ] Reviewer-note line: Jurisdiction: ksa; files: labor-law.md, labor-law-implementing-regulations.md, labor-dispute-route.md, platform-obligations.md, social-insurance-law.md, saudization-nitaqat.md, occupational-safety.md, playbook-defaults.md, MANIFEST.md; portal fetched: no; unpopulated codes: none

**What next? Pick one and I'll help you build it out:**
1. **Draft the notice** — a bilingual Art. 75 notice letter for the Portal, dated today, with termination effective 2026-11-03 and the reason stated.
2. **Escalate** — a short note to external counsel with the warning file, the numbers table and the two `[review]` questions (legitimate reason; housing allowance).
3. **Get more facts** — I'll send HR the eight open questions above as a checklist.
4. **Watch and wait** — record the decision to defer to 2026-11-03 and revisit after counsel replies.
5. **Something else** — tell me what you'd do with this.
~~~~

### Grading — EMP-01

| # | Expected | Result | Evidence |
|---|---|---|---|
| 1 | Step 0 runs; facts step asks for what the ksa file needs (warnings per work regulations; leave) rather than age or decisional unit | PASS | Reviewer note "Jurisdiction: `ksa`; files: …; unpopulated codes: none"; facts block items 1 ("Were the two warnings issued after a written charge … Art. 71 … Do the certified work regulations' penalty ladder … require a further step") and the leave line ("not on any leave (facts sheet)"); no age or group-termination question anywhere |
| 2 | Ground mapped to Art. 75 vs Art. 80 with rows cited; notice 60 days from employer; notice date computed against the manifest calendar with provenance tag | PASS | "employer termination for a legitimate reason, `labor-law.md` Art. 74(3) with Art. 75 (Art. 80(2) considered …)"; flag table row "Art. 80 ground not met or worker not heard … Art. 80(2) … Art. 69 30-day clocks … falls back to Art. 77 + Art. 76 + the full award (Art. 80 row)"; "60 days' written notice from the employer … Art. 75(b)"; "Earliest lawful termination date … = **2026-11-03** `[computed — labor-law.md Art. 75, settled 2026-09-04; inputs: notice date 2026-09-04 + 60 days, Gregorian calendar (Annex 5 cl. 14.6); MANIFEST calendar check: Tuesday, not a Friday/Saturday, not National Day … — no roll]`" |
| 3 | End-of-service award computed from Arts. 84-85 with inputs; file's position on housing allowance + `[review]` if open; employer-initiated full award; half-month/month per year; pro rata; tag `[computed — labor-law.md Arts. 84-85, settled 2026-09-04; inputs: …]` | PASS | "**SAR 46,250** `[computed — labor-law.md Arts. 84-85, settled 2026-09-04; inputs: last wage SAR 15,000 (basic 12,000 + housing allowance 3,000 …), service 5y 7m …, employer termination under Art. 75 → multiplier 1]`"; formula line "0.5 × W × min(S, 5) + 1.0 × W × max(S − 5, 0) = … 37,500 + 8,750"; "the file's position: Art. 2 row (settled) … part of the wage for end-of-service award … the Art. 61 row adds 'unless a court holds otherwise `[model knowledge — verify]`' … `[review]`"; basic-only alternative SAR 37,000 shown |
| 4 | Art. 77 exposure: 15 days' wage per year, two-month floor, contractual figure prevails; tagged the same way | PASS | "15 days × SAR 500 × 5 whole years = **SAR 37,500**; on pro-rata years … **SAR 41,875** `[computed — labor-law.md Art. 77(1),(3), settled 2026-09-04; inputs: actual wage SAR 15,000, daily SAR 500, service 5y 7m, indefinite, no contractual figure; two-month floor SAR 30,000 not binding]`"; "no contractual figure (Art. 77 chapeau)" |
| 5 | Nitaqat impact from `saudization-nitaqat.md`; Qiwa termination, GOSI deregistration, final settlement timing from `platform-obligations.md` and Art. 88 | PASS | Flag row "Nitaqat impact — `saudization-nitaqat.md` Services-by-Range row, Art. 35, Reg. Art. 8 … Low Green as of 2026-08-01"; "Qiwa termination record and Portal notice (Annex 5 cl. 14.1; `platform-obligations.md` Art. 51 / Reg. Art. 18 row …)"; "GOSI de-registration with the exit reason (`social-insurance-law.md` Art. 7 …)"; "all dues within one week … (`labor-law.md` Art. 88 …) due **2026-10-07**" |
| 6 | Dispute route and 12-month limitation from `labor-dispute-route.md` (Art. 234) | PASS | "limitation = end of relationship + 12 months → **2027-09-30** … `[computed — labor-dispute-route.md Art. 234(a) "Computed dates" …]`"; "Friendly settlement precedes any suit (Annex 5 cl. 13.4)"; grievance ladder dates |
| 7 | Disclaimer and Arabic rendering of bottom line and numbers table | PASS | Disclaimer line in English and Arabic under the header; "**الخلاصة:** لا تُنهِ العقد بتاريخ 30/09/2026 …"; "**جدول المبالغ**" table |

| Forbidden | Result | Evidence |
|---|---|---|
| "at-will", "OWBPA", "COBRA", "WARN", "FMLA", "decisional unit" | PASS | None of the six terms appears. Note: the substring "warn" occurs inside "written warning(s)" (the Labor Law's Art. 80(2)/(7) and Art. 66 penalty term), which is not the US notice statute the scenario forbids; no "WARN Act", "mini-WARN" or similar reference is made |
| Severance formula not from the file | PASS | "Severance: none above the statutory entitlement (profile …)"; every formula cites `labor-law.md` Arts. 76, 77, 84-85, 88, 111 |
| Computed number without inputs | PASS | Every SAR figure and date carries a `[computed — …; inputs: …]` tag (award, Art. 77 both variants, pay in lieu both variants, leave payout, settlement due date, notice date, limitation, grievance dates, alternative award) |
| Citing Art. 222 or Art. 224 as current law | PASS | Neither article is cited |

**Result: PASS.**

---

## EMP-02 — Hiring review with nationalisation quota and work permit

### Transcript summary

- Files loaded: staged profile (Nitaqat band Low Green, IT activity, as of 2026-08-01; hiring review triggers: all offers with restrictive covenants, all non-Saudi hires; covenant policy: non-competes only for senior roles per the jurisdiction file), plugin CLAUDE.md, `employment-legal/skills/hiring-review/SKILL.md`, JURISDICTION-STEP, REGISTRY, ksa MANIFEST, INDEX, `playbook-defaults.md` (Labor table), `labor-law.md` (Arts. 3, 9-10, 32-40, 50-55, 61(4)-(6), 83, 89-90, 98, 161-167), `labor-law-implementing-regulations.md` (Reg. Arts. 1, 6, 9, 11, 12, 14 First, 18, 19/Annex 5 cl. 6, 27; Annex 5 cls. 5, 7-15; Annex 1 Art. 7), `saudization-nitaqat.md` (Art. 26, Reg. Art. 8, Arts. 32-35, Services-by-Range, counting rules, profession-specific decisions), `platform-obligations.md` (Art. 51/Reg. Art. 18, Art. 52, Art. 37/Reg. Art. 12, Arts. 33-35, 38, 40, 90, WPS, exit rows), `social-insurance-law.md` (Arts. 1, 7, 8, 15, 28-29, 43-44), `occupational-safety.md` (Art. 123, Annex 5 cls. 11.5-11.6, cl. 12.5, Reg. Art. 6, Art. 131 bis), `labor-dispute-route.md` (Annex 5 cls. 13.3-13.4, 14.5, Art. 8). Input: the scenario's offer description (no letter file).
- Step 0 as in EMP-01 (portal probe ✓ reachable; no article fetched). Step 1: place of employment ksa, sponsoring entity Example Telematics Co. Step 2 (jurisdiction-file eligibility checks — no exempt/non-exempt call), Step 3 (Art. 83), Step 4, Step 5 run. Probation arithmetic: 6 calendar months from 2026-11-01 = 181 days.
- Escalation table: Routine offer letter → Legal Lead when restrictive covenants or non-Saudi hire — both fire. Consequential-action gate (non-lawyer) applied; overall is "Changes needed / Escalate", not "Clear to send".

### Deliverable

~~~~markdown
> **⚠️ Reviewer note**
> - **Sources:** portal: laws.boe.gov.sa ✓ reachable (index probe); no article fetched — each check is a row of `references/jurisdictions/ksa/` cited by article with its tag. Files applied: `labor-law.md`, `labor-law-implementing-regulations.md`, `saudization-nitaqat.md`, `platform-obligations.md`, `social-insurance-law.md`, `occupational-safety.md`, `labor-dispute-route.md`, `playbook-defaults.md`, `MANIFEST.md`.
> - **Read:** the offer summary you gave (one paragraph); no offer letter, Qiwa draft or Nitaqat export was attached.
> - **Flagged for your judgment:** 4 items `[review]` (is "senior accountant" a senior role under the house covenant policy; nationwide scope vs legitimate interest; recruitment-from-abroad vs local transfer; wage split).
> - **Currency:** rows applied are `[settled — last confirmed 2026-09-04]` unless tagged; the accounting-profession quota and the Nitaqat counting rules are `[model knowledge — verify]` rows and are carried as such; Eid 2027 dates used for the probation count are `[model knowledge — verify]`.
> - **Before relying:** (1) pull a dated Qiwa Nitaqat export and the entity's accounting-profession ratio today — the band decides whether a visa can issue at all; (2) get the wage split (basic / housing / transport) — it drives overtime, the award and GOSI.
> - Jurisdiction: `ksa`; files: labor-law.md, labor-law-implementing-regulations.md, saudization-nitaqat.md, platform-obligations.md, social-insurance-law.md, occupational-safety.md, labor-dispute-route.md, playbook-defaults.md, MANIFEST.md; portal fetched: no (probe only); unpopulated codes: none.

RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY, SOLICITOR, BARRISTER, OR OTHER AUTHORISED LEGAL PROFESSIONAL IN YOUR JURISDICTION BEFORE ACTING

Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance.
النص العربي هو النص المعتمد، والترجمة الإنجليزية للاستئناس فقط، ويجب مراجعة محامٍ سعودي مرخص قبل الاعتماد على هذا المستند.

## Hiring Review: [candidate, non-Saudi] — Senior Accountant — `[ksa]`

**Overall:** **Changes needed — and escalate to Legal Lead** (profile: restrictive covenant + non-Saudi hire). Not clear to send.
**النتيجة الإجمالية:** **يلزم إجراء تعديلات، ويُرفع الأمر إلى المسؤول القانوني** (ملف الممارسة: شرط تقييدي + توظيف غير سعودي). العرض غير جاهز للإرسال.

### Jurisdiction: `ksa`
Place of employment and sponsoring entity: Example Telematics Co. (holds the work permit and documents the contract — `labor-law.md` Arts. 33, 37, 51; `platform-obligations.md` Art. 51 / Reg. Art. 18 row). Profile jurisdiction table row: `ksa` — non-nationals, fixed-term contracts. Auto-escalate triggers that fire: restrictive covenant; non-Saudi hire → **Legal Lead**.

Facts to confirm before the offer goes out: (a) nationality (GCC nationals are outside the Nitaqat denominator — `saudization-nitaqat.md` Terms row); (b) whether this is recruitment from abroad or a transfer from a Saudi employer — the two follow different Nitaqat services; (c) the candidate is not under 18 or over 60 (Reg. Art. 14 First recruitment bar, experts excepted); (d) the wage split; (e) whether the offer is Arabic, bilingual or English-only.

### Eligibility and authorisation (`[ksa]`)

- **Nationalisation band** — the establishment is **Low Green** (IT activity) as of 2026-08-01 `[user provided — profile]`. Services-by-Range row (`saudization-nitaqat.md`, `[settled — last confirmed 2026-09-04] [authority — HRSD]`): Low Green "cannot apply for new visas or change occupations; can renew existing work permits". A recruitment-from-abroad hire is therefore **blocked at the visa stage** until the band improves; Reg. Art. 14 First (recruitment only in a band that permits it, no visas that push the ratio below the required rate) says the same. Transfer-in from a local employer: the row states the transfer-in service for Medium Green and above and its denial for Red, and is silent for Low Green — `[no rule in ksa files — verify]`; do not assume it is available. Art. 26 (Saudization duty) and Reg. Art. 8 (service withholding) are the legal anchor. I have not inferred the band from the file's coefficients; ask Qiwa for a dated export at offer time.
- **Profession-specific quota (accounting)** — `saudization-nitaqat.md` profession-specific decisions row `[model knowledge — verify]`: accounting professions 40% in phase 1 (reported from October 2025) rising to 70% in later phases; compliance is checked by profession code on Qiwa and non-compliance blocks the affected work permits. This sits on top of the entity band: check the entity's accounting-profession ratio before offering. Carry the tag — the percentages and dates must be verified against the HRSD decision.
- **Work permit and sponsorship** — recruitment from abroad needs Ministry approval (`labor-law.md` Art. 32); a work permit in Example Telematics Co.'s name (Arts. 33-34); the profession on the permit must match the job — "senior accountant" on the permit and the Qiwa contract (Art. 38); accountant is not among Reg. Art. 11's eighteen reserved professions, but the duties must not include cashier or HR/personnel tasks under another title (Art. 36; Reg. Art. 11); the Ministry may decline to renew the permit where the employer breaches Saudization standards (Art. 35); every recruitment, iqama, work-permit, transfer and exit fee is on the employer and a clause shifting them to the worker is void (Art. 40 with Art. 8; `platform-obligations.md` Art. 40 row); no secondment or work for others outside the statutory channel (Art. 39). Visa-issuance mechanics on the platform are `[model knowledge — verify]`.
- **Contract type, contents, language and documentation** — a non-Saudi's contract is written and fixed-term (Art. 37): two years is fine; it never converts to indefinite (Reg. Art. 12); term ends 2028-10-31 (Tuesday) with the non-renewal notice through the Portal (Annex 5 cl. 5). Early termination without an Art. 80 ground exposes the employer to Art. 77(2) (wages for the remaining term, not less than two months) — budget accordingly. Written in two copies and documented electronically on the Ministry's approved platform (Art. 51; Reg. Art. 18; the platform is Qiwa `[model knowledge — verify]`), on the unified template with the Art. 52 minimum contents and Annex 5 cls. 1-4 fields. Arabic governs and an English-only letter is defective (Arts. 9-10; Annex 5 cl. 14) — issue an Arabic counterpart. **"Salary SAR 18,000" is not split**: Annex 5 cls. 9-10 require basic wage / housing / transport / other allowances / total / GOSI deduction / net, and since 19 February 2025 housing and transport (or cash allowances paid with the wage) are mandatory for every worker (Art. 61(5)-(6)). The split drives overtime (Art. 107, basic only), the end-of-service award (Arts. 84, 86) and GOSI.
- **Probation** — "6 months" from 2026-11-01 runs to 2027-05-01 = **181 calendar days**, one day over the 180-day cap (`labor-law.md` Art. 53; Reg. Art. 19 / Annex 5 cl. 6, `[settled — last confirmed 2026-09-04]`). Restate it as "180 days from the actual start date". The count excludes Eid al-Fitr, Eid al-Adha, National Day, Founding Day (22 February 2027 falls inside) and sick leave, so the calendar end date will be later than day 180 (Eid al-Fitr 2027 in March `[model knowledge — verify]`); the clause must be express; either party may end the contract during probation through the Portal; no award for that period (Art. 54); no second probation with the same employer except the Art. 54 cases.
- **Social-insurance registration and cost** — register the worker within the Regulation's grace period (`social-insurance-law.md` Art. 7; the 15-day practice figure `[model knowledge — verify]`); for a non-Saudi only the occupational-hazards branch applies: 2% of the contributory wage, employer-borne (Arts. 28-29, `[settled — last confirmed 2026-09-04]`); contributory wage = basic wage plus the Regulation's added elements (housing, per practice `[model knowledge — verify]`), ceiling SAR 45,000 (Art. 8). Employer cost, upper bound if the whole SAR 18,000 is basic + housing: **SAR 360 / month** `[computed — social-insurance-law.md Arts. 28-29, settled 2026-09-04; inputs: contributory wage SAR 18,000 (split not provided — upper bound), rate 2%]`; no annuities or unemployment-insurance share for a non-Saudi.
- **Occupational-fitness and onboarding** — documented hazard briefing and PPE training before day one (`occupational-safety.md` Art. 123 — light for an office role); health insurance and GOSI registration are contract terms (Annex 5 cls. 11.5-11.6; Annex 1 Art. 49); pre-employment medical examination right (Annex 5 cl. 12.5). The Art. 131 bis hazardous-professions list was not read — an accounting role is unlikely to be covered; no stop needed.
- **Non-discrimination** — the advertisement and criteria must not select on gender, age, disability or marital status (`labor-law.md` Art. 3, Art. 61(4); Reg. Art. 9).
- **Minors** — not applicable (Reg. Arts. 32-35).

### Restrictive covenants

**Non-compete "3 years nationwide"** — `labor-law.md` Art. 83(1) (`[settled — last confirmed 2026-09-04]`): valid only if the work gives the worker knowledge of the employer's clients; in writing; specific as to time, place and type of work; limited to a legitimate interest; **not longer than two years** from the end of the relationship. Three years fails the cap outright — cut to two years or less. "Nationwide" is a stated place, but the row requires the restraint to be justified by a legitimate interest (client knowledge or secrets) `[review]` — a senior accountant's client knowledge is thin; consider a confidentiality undertaking under Art. 83(2) (also written, specific as to time, place and type of work) instead of, or narrower than, a non-compete. The employer's claim runs one year from discovery (Art. 83(3); `labor-dispute-route.md`). Penalty amounts and consideration are not addressed by the article; any statement about court reduction of penalty clauses is `[model knowledge — verify]`. Annex 5 cl. 15 lists non-competition among optional additional terms and cl. 14.5 voids additional terms that conflict with the form or the Law. Customer and employee non-solicits are not separately regulated — `[no rule in ksa files — verify]`; treat under Art. 83's written-specificity requirement `[review]`.

House policy (profile): "non-competes only for senior roles, per the jurisdiction file". Whether "senior accountant" is a senior role for this policy is your call `[review]`; if not, drop the non-compete and keep confidentiality.

### Jurisdiction-specific requirements (`[ksa]`)

- Dispute clause: friendly settlement, then the labour courts (Annex 5 cls. 13.3-13.4; `labor-dispute-route.md`); an arbitration or foreign-forum clause conflicts with the form and is void under cl. 14.5 (`[model knowledge — verify]` as to court treatment); the net-wage line is an executive instrument (cl. 13.3).
- No retention of passport, iqama or insurance card (Reg. Art. 6).
- No-show: a worker who does not start within seven working days may be cancelled (Annex 1 Art. 7).
- Fee allocation: all permit, iqama, visa, transfer and exit fees on the employer (Art. 40) — no clause shifting them.
- Calendar election: Gregorian (Annex 5 cl. 14.6) displaces Art. 10's Hijri default.

### Offer letter / contract

The documented Qiwa contract, not the offer letter, is the contract of record; reconcile the two before documentation — where they differ the file expects the more favourable term to apply to the worker (`platform-obligations.md` Art. 52 row, `[model knowledge — verify]`). Check: Art. 52 / Annex 5 cls. 1-4 items present; term clause = fixed 2 years with Portal non-renewal notice (Annex 5 cl. 5); wage table split (cls. 9-10); probation clause per Art. 53; working days and hours within Arts. 98 and 101 (cl. 7); annual leave not below Art. 109's 21 days (cl. 8); no fee-shifting (Art. 40), passport-retention (Reg. Art. 6), waiver (Art. 8) or penalty outside Arts. 66-67; additional terms (cl. 15) not conflicting with the form (cl. 14.5); Arabic counterpart (Art. 9). Equity terms and background-check rules: `[no rule in ksa files — verify]` (none in this offer).

### Findings table

| Finding | Severity | Source row and tag | Fix |
|---|---|---|---|
| Entity is Low Green (dated 2026-08-01): new expatriate visa cannot be applied for | 🔴 | `saudization-nitaqat.md` Services-by-Range row `[settled — 2026-09-04] [authority — HRSD]`; Reg. Art. 14 First | Confirm route (abroad vs transfer) and a dated Qiwa export; transfer-in under Low Green `[no rule in ksa files — verify]` |
| Accounting-profession quota may block the permit regardless of band | 🟠 | `saudization-nitaqat.md` profession-specific decisions row `[model knowledge — verify]` | Check the entity's accounting-profession ratio on Qiwa; verify the HRSD decision |
| Non-compete 3 years exceeds the 2-year cap; scope not tied to a legitimate interest | 🔴 | `labor-law.md` Art. 83(1) `[settled — 2026-09-04]` | ≤ 2 years, written, specific as to time, place, type of work; consider Art. 83(2) confidentiality instead `[review]` |
| Probation "6 months" = 181 days, over the 180-day cap | 🔴 | `labor-law.md` Art. 53; Reg. Art. 19 / Annex 5 cl. 6 `[settled — 2026-09-04]` | "180 days from actual start, excluding the days Reg. Art. 19 excludes" |
| Wage stated as a single SAR 18,000 figure | 🟠 | Annex 5 cls. 9-10; `labor-law.md` Art. 61(5)-(6) `[settled — 2026-09-04]` | Split into basic / housing / transport / other / total / GOSI / net |
| Work permit, profession match, fee allocation | 🟡 | `labor-law.md` Arts. 32-34, 38, 40; Reg. Art. 11 `[settled — 2026-09-04]` | Permit in the entity's name, "senior accountant" on permit and contract, no fee-shifting clause |
| Fixed-term 2 years, never converts; Art. 77(2) exposure on early ending | 🟡 | `labor-law.md` Art. 37; Reg. Art. 12; Art. 77(2) `[settled — 2026-09-04]` | Keep; add Portal non-renewal notice clause (Annex 5 cl. 5) |
| English-only offer / no Arabic counterpart (if so) | 🟡 | `labor-law.md` Arts. 9-10; Annex 5 cl. 14 `[settled — 2026-09-04]` | Issue Arabic counterpart; Arabic prevails |
| GOSI occupational-hazards registration and 2% cost | 🟢 | `social-insurance-law.md` Arts. 7, 28-29 `[settled — 2026-09-04]`; 15-day deadline `[model knowledge — verify]` | Register on joining; ≈ SAR 360/month upper bound (computed above) |
| Dispute clause, passport retention, no-show, calendar | 🟢 | Annex 5 cls. 13-14; Reg. Art. 6; Annex 1 Art. 7 `[settled — 2026-09-04]` | Use the form's clauses; no arbitration/foreign forum |

**جدول النتائج**

| النتيجة | الدرجة | المصدر والوسم | التصحيح |
|---|---|---|---|
| المنشأة في النطاق الأخضر المنخفض (بتاريخ 01/08/2026): لا يمكن طلب تأشيرة استقدام جديدة | 🔴 | `saudization-nitaqat.md` صف الخدمات حسب النطاق [مؤكَّد 04/09/2026] [الجهة — وزارة الموارد البشرية]؛ اللائحة التنفيذية، المادة (14) أولاً | تأكيد مسار التوظيف (استقدام أم نقل خدمات) وتقرير مؤرَّخ من قوى؛ نقل الخدمات إلى منشأة في النطاق الأخضر المنخفض [لا قاعدة في ملفات السعودية — يُتحقق منه] |
| قرار توطين مهن المحاسبة قد يحجب رخصة العمل بصرف النظر عن النطاق | 🟠 | `saudization-nitaqat.md` صف قرارات توطين المهن [معرفة نموذجية — يُتحقق منها] | التحقق من نسبة توطين مهن المحاسبة في المنشأة عبر قوى، ومن القرار الوزاري |
| شرط عدم المنافسة لثلاث سنوات يتجاوز الحد الأقصى (سنتان) ولا يرتبط بمصلحة مشروعة | 🔴 | نظام العمل، المادة (83) الفقرة (1) [مؤكَّد 04/09/2026] | لا تزيد عن سنتين، مكتوب ومحدد من حيث الزمان والمكان ونوع العمل؛ النظر في شرط المحافظة على الأسرار وفق الفقرة (2) بدلاً منه [للمراجعة] |
| فترة التجربة «ستة أشهر» = 181 يوماً، تتجاوز الحد الأقصى (180 يوماً) | 🔴 | نظام العمل، المادة (53)؛ اللائحة، المادة (19) والملحق (5) البند (6) [مؤكَّد 04/09/2026] | «180 يوماً من تاريخ المباشرة الفعلية، لا تُحتسب فيها الأيام المستثناة في المادة (19) من اللائحة» |
| الأجر مذكور كمبلغ واحد 18,000 ريال | 🟠 | الملحق (5) البندان (9) و(10)؛ نظام العمل، المادة (61) الفقرتان (5) و(6) [مؤكَّد 04/09/2026] | تقسيمه إلى: أجر أساسي / بدل سكن / بدل نقل / بدلات أخرى / الإجمالي / حسم التأمينات / الصافي |
| رخصة العمل ومطابقة المهنة وتحمّل الرسوم | 🟡 | نظام العمل، المواد (32-34) و(38) و(40)؛ اللائحة، المادة (11) [مؤكَّد 04/09/2026] | رخصة باسم المنشأة، مهنة «محاسب أول» في الرخصة والعقد، دون شرط يحمّل العامل الرسوم |
| عقد محدد المدة لسنتين لا يتحول إلى غير محدد؛ التعرّض للمادة (77/2) عند الإنهاء المبكر | 🟡 | نظام العمل، المادة (37)؛ اللائحة، المادة (12)؛ المادة (77) الفقرة (2) [مؤكَّد 04/09/2026] | الإبقاء عليه مع إضافة بند الإشعار بعدم التجديد عبر المنصة (الملحق 5، البند 5) |
| عرض بالإنجليزية فقط / دون نسخة عربية (إن كان كذلك) | 🟡 | نظام العمل، المادتان (9) و(10)؛ الملحق (5) البند (14) [مؤكَّد 04/09/2026] | إصدار نسخة عربية؛ النص العربي هو المعتمد |
| التسجيل في فرع الأخطار المهنية لدى التأمينات والاشتراك 2% | 🟢 | نظام التأمينات الاجتماعية، المواد (7) و(28) و(29) [مؤكَّد 04/09/2026]؛ مهلة 15 يوماً [معرفة نموذجية — يُتحقق منها] | التسجيل عند الالتحاق؛ حد أعلى تقريبي 360 ريالاً شهرياً |
| بند المنازعات، الاحتفاظ بجواز السفر، عدم المباشرة، التقويم | 🟢 | الملحق (5) البندان (13) و(14)؛ اللائحة، المادة (6)؛ الملحق (1) المادة (7) [مؤكََّد 04/09/2026] | استخدام بنود النموذج؛ لا تحكيم ولا اختصاص أجنبي |

### Suggested replacement text for the offer (counterparty-facing — send without the work-product header; Arabic prevails)

- **Probation:** "The employee is subject to a probation period of one hundred and eighty (180) days from the actual start date. Eid al-Fitr, Eid al-Adha, National Day, Founding Day and sick leave are not counted. Either party may terminate the contract during the probation period through the Portal." (`labor-law.md` Art. 53; Reg. Art. 19)
  «يخضع الموظف لفترة تجربة مدتها مائة وثمانون (180) يوماً من تاريخ المباشرة الفعلية، ولا تدخل في حسابها إجازة عيدي الفطر والأضحى وإجازة اليوم الوطني وإجازة يوم التأسيس والإجازة المرضية. ولكل من الطرفين إنهاء العقد خلال فترة التجربة عبر المنصة.»
- **Non-compete (if retained for a senior role):** "For a period of [not more than twenty-four (24)] months after the end of the employment relationship, the employee shall not work, in [named cities/regions], in [defined type of work: e.g. accounting or financial roles for a business providing telematics or fleet-management services in competition with the employer]. This undertaking protects the employer's legitimate interest in its client relationships and business secrets to which the employee has access." (`labor-law.md` Art. 83(1))
  «لمدة [لا تزيد عن أربعة وعشرين (24)] شهراً من تاريخ انتهاء علاقة العمل، يلتزم الموظف بعدم العمل في [المدن/المناطق المحددة] في [نوع العمل المحدد: مثل الوظائف المحاسبية أو المالية لدى منشأة تقدم خدمات التتبع أو إدارة الأساطيل منافسةً لصاحب العمل]. ويهدف هذا الالتزام إلى حماية مصلحة صاحب العمل المشروعة في علاقاته بعملائه وأسراره التجارية التي يطّلع عليها الموظف.»
- **Wage:** "Basic wage SAR [ ]; housing allowance SAR [ ]; transport allowance SAR [ ]; other allowances SAR [ ]; total wage SAR 18,000 (eighteen thousand Saudi riyals); GOSI deduction [ ]%; net wage SAR [ ], paid monthly into the employee's bank account." (Annex 5 cls. 9-10; Art. 61(5)-(6); Art. 90)
  «الأجر الأساسي [ ] ريال؛ بدل السكن [ ] ريال؛ بدل النقل [ ] ريال؛ بدلات أخرى [ ] ريال؛ إجمالي الأجر 18,000 ريال (ثمانية عشر ألف ريال سعودي)؛ حسم التأمينات الاجتماعية [ ]%؛ صافي الأجر [ ] ريال يُدفع شهرياً في الحساب البنكي للموظف.»

### Action items
- [ ] Obtain a dated Qiwa Nitaqat export and the accounting-profession ratio; confirm recruitment route (abroad vs transfer)
- [ ] Cut the non-compete to ≤ 2 years with defined place and type of work, or replace with an Art. 83(2) confidentiality undertaking; decide whether the role is "senior" under house policy `[review]`
- [ ] Restate probation as 180 days from actual start
- [ ] Split the wage per Annex 5 cls. 9-10
- [ ] Issue the Arabic counterpart; reconcile the letter with the Qiwa template before documentation
- [ ] Confirm age bar (Reg. Art. 14 First), profession title on permit (Art. 38), no fee-shifting (Art. 40), no passport retention (Reg. Art. 6)
- [ ] GOSI registration on joining (occupational hazards, 2%)
- [ ] Escalate to Legal Lead (profile)

> Making an offer has legal consequences — the documented contract is binding, and covenants and probation terms are hard to reset once sent. Have you reviewed this offer with an attorney? If yes, proceed. If no, here's a brief to bring to them:
> - Candidate: non-Saudi senior accountant, `[ksa]`, start 2026-11-01, sponsored by Example Telematics Co.
> - Eligibility findings: Low Green band (2026-08-01) blocks new visas (Services-by-Range row); accounting-profession quota `[model knowledge — verify]`; work permit and profession match (Arts. 32-38); fixed-term 2 years (Art. 37); probation 181 > 180 days (Art. 53); wage not split (Annex 5 cls. 9-10); GOSI 2% (Arts. 28-29).
> - Covenant: 3-year nationwide non-compete fails Art. 83(1)'s two-year cap; scope vs legitimate interest `[review]`.
> - Jurisdiction-specific: dispute clause (Annex 5 cl. 13), fee allocation (Art. 40), Arabic version (Art. 9).
> - Open: transfer-in availability under Low Green `[no rule in ksa files — verify]`; visa mechanics `[model knowledge — verify]`; non-solicit treatment `[no rule in ksa files — verify]`.
> - What could go wrong: hire blocked at the visa or profession-quota stage; void clauses (probation, non-compete, fee-shifting) that a court disregards; undocumented or English-only contract.
> - Ask the attorney: can a transfer-in proceed while the entity is Low Green; is a non-compete justified for this role; what notices or platform steps go with the letter; is the local counsel named in the profile (N/A) to be replaced by the escalation table's external counsel.
>
> If you need to find an attorney or other authorised legal professional: for `ksa` the licensing body is the Ministry of Justice (MANIFEST `issuing_authorities`).

**What next? Pick one and I'll help you build it out:**
1. **Redline the offer** — I'll produce a bilingual marked-up version with the three replacement clauses above and the Annex 5 fields.
2. **Escalate** — a short note to the Legal Lead: band status, covenant call, probation and wage fixes, and the decision needed.
3. **Get more facts** — I'll draft the five questions (nationality, route, age bar, wage split, language) for HR.
4. **Watch and wait** — hold the offer until the next Nitaqat cycle and diarise a band re-check.
5. **Something else** — tell me what you'd do with this.
~~~~

### Grading — EMP-02

| # | Expected | Result | Evidence |
|---|---|---|---|
| 1 | Step 0 runs; classification (exempt/non-exempt) does not appear | PASS | Reviewer note "Jurisdiction: `ksa`; … unpopulated codes: none"; the word "exempt" and any salaried-status classification are absent from the deliverable |
| 2 | Checks from the files: profession quota for accounting and band consequences (`saudization-nitaqat.md`, model-knowledge tags where the file is); work permit and sponsorship (Arts. 32-40, `platform-obligations.md`); contract contents and Qiwa documentation (Arts. 51-52); probation cap 180 days vs 6 months (Art. 53); non-compete cut to two-year cap and legitimate interest (Art. 83); GOSI occupational-hazards registration (`social-insurance-law.md`) | PASS | "Low Green … Services-by-Range row … cannot apply for new visas"; "profession-specific decisions row `[model knowledge — verify]`: accounting professions 40% … rising to 70%"; "work permit in Example Telematics Co.'s name (Arts. 33-34) … profession on the permit … (Art. 38) … (Art. 40 with Art. 8; `platform-obligations.md` Art. 40 row)"; "documented electronically on the Ministry's approved platform (Art. 51; Reg. Art. 18 …) … Art. 52 minimum contents"; "**181 calendar days**, one day over the 180-day cap (`labor-law.md` Art. 53 …)"; "**not longer than two years** … Three years fails the cap outright … justified by a legitimate interest"; "occupational-hazards branch … 2% … (Arts. 28-29 …) … `[computed — social-insurance-law.md Arts. 28-29 …]`" |
| 3 | Each flag cites the file row; output bilingual for counterparty-facing offer text | PASS | Findings table "Source row and tag" column populated for every row; Arabic findings table "**جدول النتائج**"; bottom line in Arabic; three replacement clauses each followed by an Arabic rendering |

| Forbidden | Result | Evidence |
|---|---|---|
| Pay-transparency, ban-the-box, I-9, salary-history, FLSA exemption | PASS | None of the terms appears; right-to-work is framed as the Art. 33 work permit |

**Result: PASS.**

---

## EMP-03 — Overtime during the fasting month

### Transcript summary

- Files loaded: staged profile (`## Wage & hour`: overtime policy statutory; known risk area: field technicians on call), plugin CLAUDE.md, `employment-legal/skills/wage-hour-qa/SKILL.md`, JURISDICTION-STEP, REGISTRY, ksa MANIFEST, INDEX, `playbook-defaults.md` (Working time row), `labor-law.md` (Arts. 2, 61(5)-(6), 89-90, 98-100, 101-103, 104-105, 106-107, 108, 112; "How skills"), `labor-law-implementing-regulations.md` (Annex 5 cls. 7, 9-10, 11; Reg. Arts. 22, 22 bis, 23, 24, 5; "How skills" divisor rule), `platform-obligations.md` (Art. 90 row, WPS row), `labor-dispute-route.md` (Art. 234(a), Art. 94, Annex 5 cl. 13.3, "Computed dates").
- Step 0 as in EMP-01 (portal probe ✓ reachable; no article fetched). Step 1: profile default `ksa`. Step 2: rule stated from rows. Step 2b (jurisdiction-file scaffold) used; Step 2a (the `usa` regular-rate scaffold) not entered. Arithmetic: 6 days × (8 − 6) = 12 overtime hours; D = 240; hourly basic 37.50; rate 56.25; SAR 675.

### Deliverable

~~~~markdown
> **⚠️ Reviewer note**
> - **Sources:** portal: laws.boe.gov.sa ✓ reachable (index probe); no article fetched — the rules are rows of `references/jurisdictions/ksa/labor-law.md`, `labor-law-implementing-regulations.md`, `labor-dispute-route.md`, `platform-obligations.md`. Highest-fabrication item in this answer: the overtime divisor (tagged).
> - **Read:** your one-paragraph question; no contract or attendance register.
> - **Flagged for your judgment:** 3 items `[review]` (actual-wage components; whether one of the six days was the Friday rest day; whether the role is "necessarily intermittent" work under Reg. Art. 23).
> - **Currency:** rows applied `[settled — last confirmed 2026-09-04]`; the divisor `[model knowledge — verify]`.
> - **Before relying:** confirm the wage split from the Qiwa contract and which six days were worked.
> - Jurisdiction: `ksa`; files: labor-law.md, labor-law-implementing-regulations.md, labor-dispute-route.md, platform-obligations.md, playbook-defaults.md, MANIFEST.md; portal fetched: no (probe only); unpopulated codes: none.

RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY, SOLICITOR, BARRISTER, OR OTHER AUTHORISED LEGAL PROFESSIONAL IN YOUR JURISDICTION BEFORE ACTING

Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance.
النص العربي هو النص المعتمد، والترجمة الإنجليزية للاستئناس فقط، ويجب مراجعة محامٍ سعودي مرخص قبل الاعتماد على هذا المستند.

**`[ksa]`:** During Ramadan a Muslim worker's actual hours are capped at six a day or 36 a week (`labor-law.md` Arts. 98-100, `[settled — last confirmed 2026-09-04]` — the Arabic text reads 6/36; the English appendix's 7/35 is unverified, so the Arabic is applied). Hours above the standard are overtime (Art. 107(2)); all hours on the weekly rest day (Friday, Art. 104) and on holidays and Eids are overtime (Art. 107(3); Art. 112). Each overtime hour is paid at the hourly wage plus 50% of the hourly **basic** wage (Art. 107(1); Annex 5 cl. 11). With the worker's consent, paid compensatory leave may replace the pay at not less than 1.5 hours per overtime hour, scheduled within 60 days, capped at 30 days a year, paid out on exit (Reg. Art. 22 bis). Annual overtime may not exceed 720 hours without consent (Reg. Art. 22). A technician is not in the Art. 108(1) senior-manager category, so the hours rules apply.

**Computation (Step 2b):**

```
Overtime hours   = 6 days × (8 h worked − 6 h Ramadan cap) = 12 h   (daily criterion, Art. 98)
                 = 48 h − 36 h                              = 12 h   (weekly criterion, Art. 107(2)) — same result
hourly wage        = monthly actual wage ÷ D = 9,000 ÷ 240 = SAR 37.50
hourly basic wage  = monthly basic wage  ÷ D = 9,000 ÷ 240 = SAR 37.50
overtime pay       = (37.50 + 0.5 × 37.50) × 12 = 56.25 × 12 = SAR 675.00
```

**Overtime due for the week: SAR 675** `[computed — labor-law.md Arts. 98, 107(1), settled 2026-09-04; inputs: basic wage SAR 9,000; actual wage taken as SAR 9,000 (no allowance stated) [review]; divisor D = 240 (30 days × 8 hours) [model knowledge — verify]; overtime hours 12 = 6 days × (8 − 6); Friday not among the six days assumed [review]]` `[verify — consult wage-and-hour counsel before asserting or paying]`.

Divisor: the Law does not define the hourly wage; the Art. 107 row records the practice of dividing the monthly wage by 30 days and by the daily hours (8) as `[model knowledge — verify]`, and the Regulations do not fix it (`labor-law-implementing-regulations.md`, "How skills"). D = 240 is used and tagged; if the Qiwa contract states different monthly hours (Annex 5 cl. 7), substitute them.

Three things that change the number `[review]`:
1. **Actual wage.** You gave the basic wage only. Since 19 February 2025 every worker must receive housing and transport or cash allowances paid with the wage (Art. 61(5)-(6)); if this technician has, say, SAR 1,500 of allowances, the hourly-wage component becomes 10,500 ÷ 240 = 43.75 and the rate (43.75 + 18.75) = 62.50 → SAR 750 `[computed — labor-law.md Arts. 2, 107(1), settled 2026-09-04; inputs: actual 10,500, basic 9,000, D 240, 12 h; illustrative allowance]`. Read the split from the Qiwa contract (Annex 5 cls. 9-10).
2. **Which six days.** If one of them was Friday, all eight hours that day are overtime (Arts. 104, 107(3)), not just two: overtime = 5 × 2 + 8 = 18 h → SAR 1,012.50 `[computed — labor-law.md Arts. 104, 107, settled 2026-09-04; inputs: rate 56.25, 18 h]`. The Friday-Saturday weekend is practice; only Friday is the statutory rest day (Art. 104 row).
3. **Intermittent work.** The profile lists field technicians on call as a risk area. If the role is "necessarily intermittent" (Reg. Art. 23), the Ramadan daily ceiling is 8 hours, so the daily criterion yields nothing — but the weekly ceiling stays 36, so 48 − 36 = 12 h remains overtime on the weekly criterion. Same SAR 675 on these facts, but confirm the category.

Alternative in kind: with the worker's consent, 12 × 1.5 = **18 hours of paid compensatory leave** instead of the SAR 675, scheduled within 60 days (Reg. Art. 22 bis).

**Exposure and limitation.** Unpaid overtime is a wage claim; the court may order payment and may fine the employer up to double the delayed amount — a court's power, not an automatic addition (`labor-dispute-route.md` Art. 94). A serving employee's claim is not time-barred; a former employee must file within twelve months of the end of the relationship (`labor-dispute-route.md` Art. 234(a)). Keep the attendance register — it is the primary evidence (Reg. Art. 5).

**Bottom line:** SAR 675 is due for the week on the facts given (12 overtime hours at SAR 56.25), or 18 hours' paid compensatory leave with consent; the figure rises if allowances are paid or if Friday was worked.
**الخلاصة:** يستحق الفني عن هذا الأسبوع **675 ريالاً** أجراً إضافياً على الوقائع المذكورة (12 ساعة إضافية بواقع 56.25 ريالاً للساعة: أجر الساعة مضافاً إليه 50% من أجر الساعة الأساسي — المادة (107) من نظام العمل؛ ساعات رمضان 6/36 — المادة (98))، أو 18 ساعة إجازة تعويضية مدفوعة الأجر بموافقته (اللائحة التنفيذية، المادة (22) مكرر)؛ ويرتفع المبلغ إذا كانت تُدفع له بدلات أو إذا كان يوم الجمعة ضمن الأيام الستة.

| Item | Amount (SAR) | Source row and tag | Inputs |
|---|---|---|---|
| Overtime hours | 12 h | `labor-law.md` Arts. 98, 107(2), settled 2026-09-04 | 6 days × (8 − 6); 48 − 36 |
| Hourly basic wage | 37.50 | `labor-law.md` Art. 2, Art. 107 row; D `[model knowledge — verify]` | 9,000 ÷ 240 |
| Overtime rate | 56.25 | `labor-law.md` Art. 107(1), settled 2026-09-04 | 37.50 + 0.5 × 37.50 |
| Overtime pay | 675.00 | `labor-law.md` Art. 107(1) `[computed …]` `[verify — consult wage-and-hour counsel]` | 56.25 × 12 |
| Compensatory-leave alternative | 18 h | Reg. Art. 22 bis, settled 2026-09-04 | 12 × 1.5, consent required |

| البند | المبلغ (ريال) | المصدر والوسم | المدخلات |
|---|---|---|---|
| ساعات العمل الإضافية | 12 ساعة | نظام العمل، المادتان (98) و(107/2)، مؤكَّد 04/09/2026 | 6 أيام × (8 − 6)؛ 48 − 36 |
| أجر الساعة الأساسي | 37.50 | نظام العمل، المادة (2) وصف المادة (107)؛ القاسم [معرفة نموذجية — يُتحقق منه] | 9,000 ÷ 240 |
| أجر الساعة الإضافية | 56.25 | نظام العمل، المادة (107) الفقرة (1)، مؤكَّد 04/09/2026 | 37.50 + 0.5 × 37.50 |
| الأجر الإضافي المستحق | 675.00 | نظام العمل، المادة (107) الفقرة (1) [محسوب] [يُتحقق منه — يُستشار مختص بالأجور قبل التأكيد أو الدفع] | 56.25 × 12 |
| البديل: إجازة تعويضية | 18 ساعة | اللائحة التنفيذية، المادة (22) مكرر، مؤكَّد 04/09/2026 | 12 × 1.5، بموافقة العامل |

> **Verify citations.** Any statute or regulation cite above was generated with AI assistance. Before relying on it, check it against the primary-source portal named in the jurisdiction manifest (laws.boe.gov.sa) and the issuing authority's site (HRSD) for accuracy, currency and subsequent history.

This is a quick answer. If you want the full framework for a settlement or back-pay position, run `/employment-legal:termination-review` Steps 2a-3.

**What next? Pick one and I'll help you build it out:**
1. **Draft the pay line** — a bilingual overtime line for the payslip (12 h × SAR 56.25) or a compensatory-leave consent form (18 h).
2. **Escalate** — a note to the Legal Lead if the on-call technician population has the same pattern across Ramadan (12 h × headcount × weeks).
3. **Get more facts** — the wage split from Qiwa, the six days worked, and whether the role is classed as intermittent.
4. **Watch and wait** — log the query and revisit if the contract's monthly hours differ from 240.
5. **Something else** — tell me what you'd do with this.
~~~~

### Grading — EMP-03

| # | Expected | Result | Evidence |
|---|---|---|---|
| 1 | Step 0 runs; ksa scaffold: Ramadan hours 6/36 from Arts. 98-100, overtime at hourly wage plus 50% from Art. 107, weekly rest Art. 104; divisor stated as the file states it or flagged `[review]` if open | PASS | Reviewer note "Jurisdiction: `ksa`; …"; "capped at six a day or 36 a week (`labor-law.md` Arts. 98-100 …)"; "hourly wage plus 50% of the hourly **basic** wage (Art. 107(1) …)"; "weekly rest day (Friday, Art. 104)"; "D = 240 (30 days × 8 hours) [model knowledge — verify]" with the explanation "the Art. 107 row records the practice … as `[model knowledge — verify]`, and the Regulations do not fix it" |
| 2 | Computed amount carries `[computed — …; inputs: …]`; the regular-rate scaffold does not appear | PASS | "**SAR 675** `[computed — labor-law.md Arts. 98, 107(1), settled 2026-09-04; inputs: basic wage SAR 9,000; …; overtime hours 12 …]`"; no regular-rate language, no half-time premium, no US statute |
| 3 | Limitation on wage claims from `labor-dispute-route.md` mentioned where exposure is discussed | PASS | "a former employee must file within twelve months of the end of the relationship (`labor-dispute-route.md` Art. 234(a))" in the "Exposure and limitation" paragraph |

| Forbidden | Result | Evidence |
|---|---|---|
| §207(e), 0.5× posture, liquidated-damages doubling, "50-state survey" | PASS | None appears; the Art. 94 fine is described as "a court's power, not an automatic addition" without the forbidden phrase |

**Result: PASS.**

---

## EMP-04 — Primary source unreachable during a termination review

### Transcript summary

- Same profile, skill and files as EMP-01; instruction added: "quote the current text of Article 84 from the portal before computing".
- Step 0 item 5 research step executed. GUID for the Labor Law from `SOURCES.md` / `INDEX.md`: `08381293-6388-48e2-8ad2-a9a700f2aa94`.
- Pre-flight probe under the blocked proxy:
  ```
  $ https_proxy=http://127.0.0.1:9 python3 scripts/fetch-law.py --portal boe --index
  fetch failed: https://laws.boe.gov.sa/BoeLaws/Laws/Folders/1
  curl: (7) Failed to connect to 127.0.0.1 port 9 after 0 ms: Couldn't connect to server
  ```
- Article fetch under the blocked proxy:
  ```
  $ https_proxy=http://127.0.0.1:9 python3 scripts/fetch-law.py --portal boe --id 08381293-6388-48e2-8ad2-a9a700f2aa94 --lang ar
  fetch failed: https://laws.boe.gov.sa/BoeLaws/Laws/LawDetails/08381293-6388-48e2-8ad2-a9a700f2aa94/1
  curl: (7) Failed to connect to 127.0.0.1 port 9 after 0 ms: Couldn't connect to server
  ```
- "No silent supplement" applied: failure reported, three options offered, stop. No quote, no computation.

### Deliverable

~~~~markdown
> **⚠️ Reviewer note**
> - **Sources:** portal: laws.boe.gov.sa **unreachable** this session — `scripts/fetch-law.py --portal boe --index` and the Labor Law fetch (`--id 08381293-6388-48e2-8ad2-a9a700f2aa94 --lang ar`) both failed with `curl: (7) Failed to connect to 127.0.0.1 port 9`. No article text was read from the portal; nothing below is tagged as a portal read.
> - **Read:** the termination facts sheet and the practice profile.
> - **Flagged for your judgment:** the choice below.
> - **Currency:** not checked against the portal this session.
> - **Before relying:** answer the question below; nothing has been computed.
> - Jurisdiction: `ksa`; files: MANIFEST.md, SOURCES.md, INDEX.md (labor-law.md not yet applied — awaiting your instruction); portal fetched: no (attempted, failed); unpopulated codes: none.

RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY, SOLICITOR, BARRISTER, OR OTHER AUTHORISED LEGAL PROFESSIONAL IN YOUR JURISDICTION BEFORE ACTING

Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance.
النص العربي هو النص المعتمد، والترجمة الإنجليزية للاستئناس فقط، ويجب مراجعة محامٍ سعودي مرخص قبل الاعتماد على هذا المستند.

## Termination Review: Ahmed (synthetic) — 2026-09-04 — **stopped at the research step**

You asked me to quote the current text of Article 84 from the portal before computing the end-of-service award. I attempted the fetch the manifest prescribes and it failed:

```
$ python3 scripts/fetch-law.py --portal boe --id 08381293-6388-48e2-8ad2-a9a700f2aa94 --lang ar
fetch failed: https://laws.boe.gov.sa/BoeLaws/Laws/LawDetails/08381293-6388-48e2-8ad2-a9a700f2aa94/1
curl: (7) Failed to connect to 127.0.0.1 port 9 after 0 ms: Couldn't connect to server
```

The portal (laws.boe.gov.sa) is unreachable from this session — the index probe failed the same way, so this is a connectivity problem, not a missing article. I will not quote Article 84 from memory, and I have not computed the award, because the number would rest on text I could not read today.

**Options — tell me which:**
1. **Retry the fetch** once the network or proxy is fixed (a `curl -sS https://laws.boe.gov.sa/BoeLaws/Laws/LawDetails/08381293-6388-48e2-8ad2-a9a700f2aa94/1` from a machine with access also works; the built-in web-fetch tool rejects the portal's TLS chain). I will then quote the article, tag it `[BOE — Arabic]`, check the status line and the "تعديلات المادة" block, and compute.
2. **Paste the article text** (Arabic, from the portal page) and I will quote it as `[user provided]` and compute on it.
3. **Proceed on the reference file.** `references/jurisdictions/ksa/labor-law.md` carries an Art. 84 row whose primary text was last read on 2026-09-04 (`[settled — last confirmed 2026-09-04]`). If you say so, I will compute from that row and the number will carry `[computed — labor-law.md Arts. 84-85, settled 2026-09-04; inputs: …]` — the tag names the file's settled date, not a portal fetch made today — and the reviewer note will say the portal was unreachable and no live quote was obtained.

I'll wait for your answer.

**ماذا تريد أن أفعل؟** تعذّر الاتصال ببوابة هيئة الخبراء (laws.boe.gov.sa) في هذه الجلسة، ولن أنقل نص المادة (84) من الذاكرة ولم أحسب مكافأة نهاية الخدمة. الخيارات: (1) إعادة المحاولة بعد إصلاح الاتصال؛ (2) لصق نص المادة من البوابة؛ (3) المضي على صف الملف المرجعي المؤكَّد بتاريخ 04/09/2026 مع وسم الرقم بتاريخ الملف لا بقراءة من البوابة.
~~~~

### Grading — EMP-04

| Expected (as COM-04) | Result | Evidence |
|---|---|---|
| Fetch attempted and failure reported | PASS | Command and `curl: (7)` output reproduced verbatim in the deliverable; reviewer note "portal: laws.boe.gov.sa **unreachable** this session" |
| Options offered | PASS | "**Options — tell me which:** 1. Retry … 2. Paste the article text … 3. Proceed on the reference file … I'll wait for your answer." |
| No fabricated quote | PASS | "I will not quote Article 84 from memory"; no article text appears |
| If the user proceeds on the reference file, the computed number's tag names the file's `settled` date, not a portal fetch | PASS (conditional path stated) | "the number will carry `[computed — labor-law.md Arts. 84-85, settled 2026-09-04; inputs: …]` — the tag names the file's settled date, not a portal fetch made today" |
| Nothing tagged `[BOE — Arabic]` in this run | PASS | The only occurrence of the tag is inside option 1 as a description of what would happen after a successful retry; no finding, quote or number is tagged with it; reviewer note: "nothing below is tagged as a portal read" |

**Result: PASS.**

---

## ALL-01 — Primary jurisdiction not populated (employment part)

### Transcript summary

- Staged home switched to `.../homes/gbr`. Files loaded: staged `gbr/employment-legal/CLAUDE.md` (primary `gbr`, footprint none, no `[PLACEHOLDER]` markers), `company-profile.md`, plugin CLAUDE.md, `termination-review/SKILL.md`, `cold-start-interview/SKILL.md`, `references/jurisdictions/REGISTRY.md`, `references/jurisdictions/gbr/MANIFEST.md` (`populated: **no**`, status stub). Input: EMP-01 facts with the employee in London.
- termination-review Step 0: item 1 profile has a jurisdiction (`gbr`); item 2 matter facts (employee in London) confirm `gbr`, add no other code; item 3 MANIFEST `populated` is not `yes` → stop for `gbr`. No jurisdiction files loaded; Steps 1-5 not entered; nothing computed.
- cold-start-interview variant: Part 1 "Primary jurisdiction" question simulated with the answer `gbr`; the populated check ran against REGISTRY.md (only `ksa` is `yes`; `usa` reserved) and `gbr/MANIFEST.md`; refusal emitted; profile not written.

### Deliverable A — `/employment-legal:termination-review` (gbr)

~~~~markdown
Jurisdiction `gbr` (United Kingdom) is registered but not populated: no reference files exist for it. I will not apply another jurisdiction's rules or model knowledge in its place. Options: (1) populate `references/jurisdictions/gbr/` (see README, 'How to add a jurisdiction'), (2) route this matter to local counsel, (3) tell me to proceed with the analysis limited to the populated jurisdictions in this matter, with every finding for `gbr` marked `[not populated — no rule applied]`.

For this matter that third option would leave nothing to analyse: the employee works in London, the profile's footprint has no other code, and the facts point to no populated jurisdiction — so option (3) would produce a memo in which every finding is `[not populated — no rule applied]`. I have not read the termination facts against any rule, computed any figure, or applied the rules of any other jurisdiction. Waiting for your answer.

> Reviewer note — Jurisdiction: gbr (stopped); files: gbr/MANIFEST.md, REGISTRY.md; portal fetched: no; unpopulated codes: gbr.
~~~~

### Deliverable B — `/employment-legal:cold-start-interview`, Part 1 primary-jurisdiction question answered `gbr`

~~~~markdown
> **Primary jurisdiction.** Which country is the primary jurisdiction of this practice — where most employees are, or where the employing entity sits? Give me the ISO 3166-1 alpha-3 code in lowercase (`ksa`, `gbr`, `fra`, `che`, `usa`) or the country name and I'll map it.

User: gbr

Jurisdiction `gbr` (United Kingdom) is registered but not populated: no reference files exist for it, so every skill in this plugin would stop on your first matter. I will not write a profile with an unpopulated primary jurisdiction. Options: (1) choose `usa` (upstream US path, upstream research connectors), (2) choose a populated code — currently: `ksa` (Kingdom of Saudi Arabia), (3) populate `references/jurisdictions/gbr/` first (see README, 'How to add a jurisdiction') and re-run setup.

If you pick (1) or (2) I'll continue with that code as primary and record `gbr` in the footprint as `[not populated — no rule applied]`. Which do you want?
~~~~

### Grading — ALL-01 (employment)

| # | Expected | Result | Evidence |
|---|---|---|---|
| 1 | Skill reads `gbr/MANIFEST.md`, sees `populated: no`, stops with the stop message (registered but not populated; will not apply another jurisdiction's rules or model knowledge; options: populate, local counsel, proceed with populated codes only with `[not populated — no rule applied]`) | PASS | Deliverable A opens with the verbatim Step 0 stop text: "Jurisdiction `gbr` (United Kingdom) is registered but not populated … I will not apply another jurisdiction's rules or model knowledge in its place. Options: (1) populate … (2) route this matter to local counsel, (3) … marked `[not populated — no rule applied]`" |
| 2 | No analysis for `gbr` before the user answers | PASS | "I have not read the termination facts against any rule, computed any figure, or applied the rules of any other jurisdiction. Waiting for your answer." |
| 3 | Cold-start variant: interview refuses to write the profile with an unpopulated primary code and offers `usa` or a populated code | PASS | Deliverable B: "I will not write a profile with an unpopulated primary jurisdiction. Options: (1) choose `usa` … (2) choose a populated code — currently: `ksa` … (3) populate …" |

| Forbidden | Result | Evidence |
|---|---|---|
| Any UK rule stated as applied (Employment Rights Act, unfair dismissal, UCTA) | PASS | None mentioned |
| Any Saudi rule applied to the `gbr` matter | PASS | No ksa file loaded or cited |
| Any US rule applied with a "US framework as a starting structure" caveat | PASS | Not offered; Step 0 replaces that caveat with a hard stop |

**Result: PASS.**

---

## Skill-text observations

No scenario failed, so no fix is required. Three points where the text could be tightened, with the exact line:

1. **`employment-legal/skills/termination-review/SKILL.md`, Step 2a item 4 (example tag) vs `references/jurisdictions/ksa/labor-law.md` "How skills should use this file" → "Computed numbers" and `labor-law-implementing-regulations.md` "How skills" → termination-review line.** The two reference files instruct the skill to attach `[settled — last confirmed 2026-09-04] [BOE — Arabic]` to the award formula, while EMP-04 requires that nothing be tagged `[BOE — Arabic]` when the portal was not read this session and the skill's own example tag omits it. The plugin CLAUDE.md tag vocabulary permits carrying `[BOE — Arabic]` from the file's settled date, so the texts are reconcilable, but a reader following the reference files literally in an EMP-04 run would breach the scenario. Suggested wording for Step 2a item 4: "On a run where the portal was not read, the number carries only the computed-number tag with the file's settled date; do not add `[BOE — …]` to a number." (Not changed.)
2. **`employment-legal/skills/wage-hour-qa/SKILL.md`, Step 2b item 4 (Art. 107 formula) vs `labor-law-implementing-regulations.md` "How skills" → wage-hour-qa line.** The regulations file states the computed overtime as "hourly basic wage × 1.5 × overtime hours", which equals the Law's "hourly wage + 50% of hourly basic wage" only when the actual wage equals the basic wage. The skill's formula is the Law's and is correct; the reference file's shorthand should read "(hourly actual wage + 0.5 × hourly basic wage) × overtime hours". Reference-file text, not skill text.
3. **`employment-legal/skills/wage-hour-qa/SKILL.md`, Step 2b opening ("Refuse to compute if an input is missing; ask, do not assume") vs EMP-03's expectation of a computed amount from "SAR 9,000 basic".** The actual-wage components are not stated in the input. This run computed on the stated figure and flagged the actual-wage component `[review]` with a worked alternative; a stricter reading of the sentence would stop and ask. If the intended behaviour is "compute on the stated components and flag", the sentence could add: "where only the basic wage is given, compute on it, state that allowances were assumed nil, and flag `[review]`." (Not changed.)

One scenario-text note: EMP-01's forbidden word "WARN" (the US notice statute) collides as a substring with "warning", a term the ksa file itself uses (Art. 80(2), (7); Art. 66). Grading treated the collision as not a hit; the scenario could say "WARN Act" to remove the ambiguity.
