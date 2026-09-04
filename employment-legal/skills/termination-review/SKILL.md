---
name: termination-review
description: >
  Termination review — high-risk flag detection, end-of-service award and
  compensation computation, notice, final settlement, and release, for the
  jurisdiction resolved from the practice profile. Rules come from the
  jurisdiction reference files, or per-review research for `usa`. Use when
  the user says "reviewing a termination", "can we end this contract", "term
  review", or describes a termination scenario.
argument-hint: "[describe the termination, or attach documentation]"
---

# /termination-review

1. Load `~/.claude/plugins/config/claude-for-legal/employment-legal/CLAUDE.md` → termination review triggers, high-risk flags, severance practice, jurisdiction rules.
2. Use the workflow below.
3. Walk the checklist. Check every high-risk flag.
4. Final settlement, notice, end-of-service award and compensation per the applicable jurisdiction file (Steps 2a, 2b, 3). Severance + release if applicable (Step 4).
5. If any high-risk flag fires: escalate per table, don't proceed without sign-off.

---

## Matter context

**Matter context.** Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗` (the default for in-house users), skip the rest of this paragraph — skills use practice-level context and the matter machinery is invisible. If enabled and there is no active matter, ask: "Which matter is this for? Run `/employment-legal:matter-workspace switch <slug>` or say `practice-level`." Load the active matter's `matter.md` for matter-specific context and overrides. Write outputs to the matter folder at `~/.claude/plugins/config/claude-for-legal/employment-legal/matters/<matter-slug>/`. Never read another matter's files unless `Cross-matter context` is `on`.

---

## Purpose

Most terminations are fine. A few are lawsuits waiting to happen. This skill
runs the checklist that catches the second kind before the decision is final.
The skill does not state the law from memory — for a populated jurisdiction
code every rule is a row of `references/jurisdictions/<code>/` cited by
article; for `usa` every jurisdiction-specific rule and release-period
requirement is researched and cited at the time of review.

## Load context

`~/.claude/plugins/config/claude-for-legal/employment-legal/CLAUDE.md` → termination review triggers, high-risk flags, standard severance,
jurisdiction table.

## Output header

Prepend the work-product header from `~/.claude/plugins/config/claude-for-legal/employment-legal/CLAUDE.md` → `## Outputs` (it differs by user role — see `## Who's using this`). Match the memo format from seed term memos referenced in that config where one exists. The work-product header is always first. For every code other than `usa`, the jurisdiction disclaimer line from `## Outputs` follows the header, and the bilingual house-style rule in `## Outputs` applies to the bottom line, the numbers table and any counterparty-facing text.

## Workflow

### Step 0: Resolve the applicable jurisdiction

1. **Read the practice profile's `## Jurisdiction` section.** It gives the primary jurisdiction code, the footprint list (other codes the practice operates in), the output-language preference, and whether local counsel is available for escalation. Codes are ISO 3166-1 alpha-3 lowercase (`ksa`, `gbr`, `fra`, `che`, `usa`). If the section is missing or still a placeholder, stop: "The practice profile has no jurisdiction. Run the cold-start interview; nothing in this skill can run against the wrong jurisdiction."
2. **Determine the matter's jurisdiction(s).** Start from the primary code. Then read the matter facts: governing-law clause, seat of arbitration, place of employment, jurisdiction of incorporation, place of performance. If the facts point to a code not in the profile, add it for this matter and say so in the reviewer note. A matter may have more than one code (a contract governed by English law with a Saudi counterparty and Saudi performance is `gbr` + `ksa`).
3. **Load the jurisdiction folder for each code.** The folder is `references/jurisdictions/<code>/` in this plugin (the same tree ships at the repo root and in every runtime adapter). Read `MANIFEST.md` first.
   - If `populated` is not `yes`: **stop for that code.** Say: "Jurisdiction `<code>` (<name>) is registered but not populated: no reference files exist for it. I will not apply another jurisdiction's rules or model knowledge in its place. Options: (1) populate `references/jurisdictions/<code>/` (see README, 'How to add a jurisdiction'), (2) route this matter to local counsel, (3) tell me to proceed with the analysis limited to the populated jurisdictions in this matter, with every finding for `<code>` marked `[not populated — no rule applied]`." Wait for the answer. Never fall back silently.
   - If the code is `usa`: there is no folder. Follow this skill's US path (the upstream doctrine and the upstream research connectors, CourtListener or Westlaw, with the upstream "no silent supplement" rule). Label findings `[usa]`.
   - If `populated` is `yes`: read `INDEX.md`, then the instrument files this skill names in its "Jurisdiction files" list. A row tagged `[settled — last confirmed YYYY-MM-DD]` may be applied and cited by article. A row tagged `[model knowledge — verify]` may be applied only with that tag carried onto the finding. If a rule this skill needs is not in the files at all, do not supply it from memory: say what is missing, tag the gap `[no rule in <code> files — verify]`, and continue only with the rules that exist.
4. **Multi-jurisdiction matters.** Run the relevant files side by side. Label every finding with its code in square brackets, `[ksa]`, `[gbr]`, `[usa]`, and never merge two jurisdictions' rules into one sentence. Where the codes conflict (a clause valid under one law and reducible under another), state both and flag `[review]` for the lawyer to decide which governs.
5. **Research step (when a rule must be quoted or its currency checked).** Use the portal named in `MANIFEST.md` → `research_tool`. For `ksa`: `python3 scripts/fetch-law.py --portal boe --id <guid> --lang ar` (GUIDs in `SOURCES.md`), or `curl -sS https://laws.boe.gov.sa/BoeLaws/Laws/LawDetails/<guid>/1`; the built-in web-fetch tool rejects the portal's TLS chain. Quote the article, tag `[BOE — Arabic]` (or `[BOE — official English]` when quoting the translation), and check the status line and the "تعديلات المادة" block for amendments. If the fetch fails or the article is not found, apply the "no silent supplement" rule: report the failure and stop, or continue with the rule tagged `[model knowledge — verify]` only if the user says so.
6. **Calendar and language.** Take the weekend, public-holiday, calendar (Hijri or Gregorian) and currency rules from `MANIFEST.md`. Compute every date and roll-back against that calendar, never against a Saturday/Sunday weekend or US federal holidays. Produce the deliverable in English; when the profile's output-language preference is bilingual, or the manifest's authoritative language is not English and counterparty-facing text is produced, add the authoritative-language rendering of the bottom line, the findings table, and any counterparty-facing text, using the spellings in the manifest's `output_language_rule`.
7. **Header and disclaimer.** Prepend the manifest's `disclaimer` line under the work-product header for every deliverable that applies a non-`usa` jurisdiction. For `ksa`: "Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance." with its Arabic rendering from the manifest.
8. **Record in the reviewer note.** `Jurisdiction: <codes applied>; files: <list>; portal fetched: yes/no; unpopulated codes: <list or none>.`

**Jurisdiction files this skill loads** (for a populated non-`usa` code; for `ksa` these are the files named, for another populated code the equivalent instrument files listed in that folder's `INDEX.md`):

- `references/jurisdictions/<code>/MANIFEST.md` (calendar, currency, disclaimer) and `INDEX.md`; `playbook-defaults.md` Labor table (the profile's accepted defaults).
- `references/jurisdictions/<code>/labor-law.md` — Art. 2 (wage, basic wage, actual wage, month, continuous service), Art. 8 (waivers void), Art. 37 (non-national contracts fixed-term), Arts. 53-56 (probation, conversion, renewals), Art. 64 (service certificate), Arts. 66-73 (discipline clocks, hearing, grievance), Arts. 74-82 (grounds, notice 75-76, compensation 77, garden leave 78, resignation 79 bis, summary dismissal 80, constructive termination 81, illness 82), Art. 83 (non-compete), Arts. 84-88 (award, resignation fractions, exclusions, exceptions, settlement window), Art. 96 (averages for commission pay), Art. 111 (leave payout), Art. 116 (unpaid-leave suspension), Art. 117 (sick-leave tiers), Art. 137 (work-injury absence), Arts. 151, 155, 160 (maternity, pregnancy protection, iddah). Steps 1, 2, 2a, 2b, 3, 4.
- `references/jurisdictions/<code>/labor-law-implementing-regulations.md` — Reg. Art. 12 (non-national fixed-term), Reg. Art. 14 Second (transfer routes), Reg. Art. 19 / Annex 5 cl. 6 (probation excluded days), Reg. Art. 22 bis(4) (compensatory-leave payout), Annex 5 cls. 8.2 and 11.9-11.10 (leave payout, settlement windows), Annex 5 cl. 14.1 (Portal notices), Annex 1 Arts. 57-71 (grounds, discipline, grievance). Steps 1, 2, 3.
- `references/jurisdictions/<code>/labor-dispute-route.md` — Art. 234(a) (12-month limitation), Art. 235 (no change of terms during suit), Art. 72 / Annex 1 Art. 71 (30-15-30 grievance ladder), Annex 5 cls. 13.4 and 14.1, Reg. Art. 14 Second 8(a), Art. 8 (releases), and its "Computed dates" rules. Steps 2, 3, 4.
- `references/jurisdictions/<code>/platform-obligations.md` — Art. 40 (return ticket, fees), Art. 90 (bank payment of final wages), Reg. Art. 14 Second items 5-8, 15, 21 (transfer without consent, unconditioned release), the exit/final-exit row and the GOSI row. Steps 2, 3, 4.
- `references/jurisdictions/<code>/social-insurance-law.md` — Art. 7 (deregistration), Art. 16 with Decision 1022 and Decree clause Fifth (retirement age), Art. 45 (unemployment-insurance disqualification). Steps 1, 2, 3.
- `references/jurisdictions/<code>/saudization-nitaqat.md` — Art. 26, Reg. Art. 8, Art. 35, the Services-by-Range row. Steps 1, 2.
- `references/jurisdictions/<code>/occupational-safety.md` — Arts. 80(2), 122, 81(6), 137, 139, 143 (safety-misconduct and medical-unfitness dismissals). Step 2.

### Step 1: The basic facts

Common to every code:

- Employee name (or role if staying abstract)
- Jurisdiction (place of employment, resolved in Step 0)
- Reason for termination (performance, misconduct, RIF, position elimination)
- How long employed
- When is the planned term date

**When the applicable code is `usa`**, also ask:

- Age (relevant to release requirements for older-worker protections)
- Whether any other employees are being terminated as part of the same
  decisional unit or program (relevant to group-termination release rules)

**When the applicable code is populated (non-`usa`)**, ask the facts the
jurisdiction file needs for its flags and computations. Ask them in one
block; if a fact that is a computation input is missing, Steps 2a and 2b
refuse to compute until it is supplied. For `ksa` (rows in
`references/jurisdictions/ksa/labor-law.md` unless another file is named):

- Nationality — drives contract type (Art. 37, Reg. Art. 12), work-permit
  and exit consequences (`platform-obligations.md`), and Nitaqat impact
  (`saudization-nitaqat.md`)
- Contract type: fixed-term or indefinite (Arts. 37, 55; a non-national's
  contract is fixed-term whatever it says, Reg. Art. 12), the expiry date, and
  the actual start date (the Art. 37 default term runs from actual start)
- Start date and continuous service in years and months (Art. 2 continuous
  service; Arts. 56 and 18 for renewals and ownership changes; any unpaid
  leave beyond 20 days, Art. 116)
- Last wage and its components from the documented contract (Annex 5
  cls. 9-10): basic wage, housing, transport, other allowances, commissions
  (Art. 2 actual wage; any Art. 86 exclusion agreement; Art. 96 averages for
  commission-based pay)
- Termination ground and which of Arts. 74, 75, 77, 80, 81 it falls under
  (Annex 1 Art. 57); for Art. 80: the ground number, whether the worker was
  heard (Art. 80 chapeau, Art. 71), the written-warning dates for grounds (2)
  and (7), the 24-hour report for ground (4), and the Art. 69 clocks
  (discovery date, investigation end date)
- Probation status: probation clause in the documented contract, stated
  length, and the excluded days (Art. 53, Reg. Art. 19 / Annex 5 cl. 6;
  Art. 54 no-award rule)
- Whether the worker is on sick leave (Art. 117 tier and days used in the
  sick-leave year; Art. 82), pregnant or on maternity leave (Art. 155), on
  work-injury absence (Art. 137, not Art. 82), or on other statutory leave
- Notice given or pay in lieu (Art. 75: 60 days employer / 30 days worker for
  monthly-paid indefinite contracts; Art. 76; Art. 78), and whether the
  notice went through the Portal (Annex 5 cl. 14.1)
- Any contractual compensation clause for unlawful termination (Art. 77
  chapeau)
- If the worker resigned: submission date, employer response or deferral
  dates (Art. 79 bis), and, for a non-national, whether it is really a
  Reg. Art. 14 Second transfer
- Nitaqat band impact: the entity's current band as a dated Qiwa export
  (`saudization-nitaqat.md` Services-by-Range row, Art. 35); never inferred
  from the coefficients in that file
- Retirement-age case (Art. 74(4)): the worker's social-insurance regime
  (new-law, legacy, or phased) per `social-insurance-law.md` Art. 16 and
  Decree clause Fifth

For another populated code, ask the facts the equivalent rows of that code's
labor-law file name; where the file has no row for a fact a computation needs,
tag `[no rule in <code> files — verify]` and do not compute.

### Step 2: High-risk flag scan

This is the most important step. Check every flag from `~/.claude/plugins/config/claude-for-legal/employment-legal/CLAUDE.md`. The
default set depends on the applicable code. The first seven rows of the
table below (recent complaint through contract/handbook promise) are neutral
and apply under every code; the leave, whistleblower and misclassification
wording is the `usa` version.

**When the applicable code is `usa`:** default set:

| Flag | Why it's high-risk | Check |
|---|---|---|
| **Recent complaint** | Retaliation claim | Has this employee filed any complaint (HR, ethics hotline, regulatory) recently? |
| **Protected leave** | Leave-law interference/retaliation | Currently on or recently returned from protected leave (FMLA/state equivalents, disability, parental, military)? |
| **Protected class + timing** | Discrimination claim | Protected class AND recently disclosed/visible (pregnancy announcement, religious accommodation request, disability disclosure)? |
| **Whistleblower** | Federal and state whistleblower statutes | Has this employee raised concerns about illegality, safety, fraud? |
| **Thin documentation** | "Why now?" problem | For performance terms: is there a PIP, written warnings, documented feedback? Or did this come out of nowhere? |
| **Comparator problem** | Disparate treatment | Is someone else doing the same thing and not being terminated? |
| **Contract/handbook promise** | Breach | Does the offer letter, handbook, or any writing promise a process that isn't being followed? |
| **Exempt misclassification** | FLSA + state wage claim with liquidated damages | See the classification check below. Fires on state + classification + title. |

**Exempt/non-exempt classification flag.** Fire this flag when ALL of the
following are true:

1. The employee works in a state with a high exempt salary threshold — **CA,
   NY, WA, CO, AK** (and any other state listed in
   `~/.claude/plugins/config/claude-for-legal/employment-legal/CLAUDE.md` →
   `## Wage & hour` → Known classification risk areas as a high-threshold
   state) — **AND**
2. The employee is classified **exempt** (salaried, no overtime) — **AND**
3. The employee's title contains **"supervisor," "lead," "coordinator,"
   "analyst," "administrator,"** or **"specialist"** (case-insensitive, and
   any equivalent-scope title the practice profile flags as risky).

When all three fire, emit:

> 🔴 **Potential exempt misclassification** — [title] earning $[X] in
> [state]. The exempt salary threshold in [state] is approximately $[Y]
> `[model knowledge — verify]`. Before termination, route to
> `/employment-legal:wage-hour-qa` for a classification check — a misclassified
> employee who's terminated has a ready-made FLSA and state-wage claim with
> liquidated damages, attorneys' fees, and (in CA) PAGA exposure, which
> the separation agreement may not be able to release cleanly. A terminated
> plaintiff with unpaid-OT exposure is the most litigated wage-and-hour
> fact pattern in these states.

Do not suppress this flag because the title "looks managerial" — the whole
premise of the misclassification claim is that titles lie. Route to
`/employment-legal:wage-hour-qa` for the actual duties-and-salary test.

**If a back-pay number is being computed as part of this review (severance
modeling, settlement posture, exposure estimate), do NOT compute it in this
skill.** Route to `wage-hour-qa` → Step 2a and use the branch for the
applicable code: for `usa`, its regular-rate scaffold (§207(e) inclusions
(non-discretionary bonuses, commissions, shift diffs) in the regular rate,
0.5× premium when straight time was already paid for OT hours (else 1.5×),
liquidated damages under §216(b), and 2-year / 3-year willful SOL under
§255(a)); for a populated code, its jurisdiction-file scaffold (for `ksa`:
overtime at the hourly wage plus 50% of the basic wage per `labor-law.md`
Art. 107, limitation per `labor-dispute-route.md` Art. 234). Every back-pay
number carries `[verify — consult wage-and-hour counsel before asserting or
paying]` and, for a populated code, the computed-number tag with its inputs.
A clean-looking wrong number here is the specific failure mode this scaffold
prevents.

**When the applicable code is populated (non-`usa`):** the flag list comes
from the jurisdiction files. Keep the neutral rows of the table above (recent
complaint, thin documentation, comparator, contract/handbook promise, and
protected class + timing read against the file's non-discrimination rows —
for `ksa`, `labor-law.md` Arts. 3 and 61(4)) and add the file's flags. For
`ksa`:

| Flag | Source row | Check |
|---|---|---|
| **Termination during protected leave** | `labor-law.md` Art. 82 (no termination for illness before the Art. 117 sick-leave periods are exhausted), Art. 155 (no dismissal or warning of dismissal during pregnancy or maternity leave, up to 180 days' absence a year), Art. 137 via `occupational-safety.md` (work-injury absence is not sick leave) | Which tier of Art. 117 is the worker in, and how many days remain? Is the worker pregnant or on maternity leave? Is the absence a work injury? |
| **Art. 80 ground not met or worker not heard** | `labor-law.md` Art. 80 (nine closed grounds; hearing opportunity in the chapeau), Art. 71 (written charge, interview, minutes), Art. 69 (30-day discovery-to-charge and finding-to-penalty clocks), Annex 1 Arts. 63-68 in `labor-law-implementing-regulations.md`; for ground (2) safety breaches also `occupational-safety.md` Arts. 80(2) and 122 (posting, written warning) | Does the fact pattern sit inside one numbered ground? Was the worker heard? Were the ground-(2)/(7) warnings and the ground-(4) 24-hour report done on time? A failed condition falls back to Art. 77 plus Art. 76 plus the full award (Art. 80 row) |
| **Notice defect** | `labor-law.md` Art. 75 (60 days employer / 30 days worker, monthly-paid indefinite; 30 days otherwise), Art. 76 (pay in lieu at the actual wage for the full period), Annex 5 cl. 14.1 (notices effective only through the Portal) | Was written notice given for the statutory or longer contractual period, stating a legitimate reason, through the Portal? |
| **WPS arrears / late wages** | `platform-obligations.md` Art. 90 row (bank payment by the due date) and WPS row (`[model knowledge — verify]`); `labor-law.md` Art. 81(1) (unpaid wages let the worker leave with full rights), Art. 94 (refund order and fine up to double); Reg. Art. 14 Second 8 (three months unpaid lets a non-national transfer without consent) | Are wages and allowances current and paid through an approved bank? Any Mudad non-compliance? |
| **Art. 77 exposure** | `labor-law.md` Art. 77 (compensation where the reason is not legitimate); Art. 75 row ("legitimate reason" is not defined in the Law) | Is the stated reason one the file treats as legitimate? If not, compute Step 2b |
| **Nitaqat impact** | `saudization-nitaqat.md` Services-by-Range row, Art. 35 (non-renewal of permits for a nationalisation-quota breach), Reg. Art. 8 (service withholding) | Does a national's departure move the entity's dated platform band? |
| **Work-permit and exit consequences** | `platform-obligations.md` Art. 40 (employer bears exit fees and the return ticket), Reg. Art. 14 Second items 5-8 and 21 (transfer without consent), the exit/final-exit row (`[model knowledge — verify]`) | Is the worker a non-national? Transfer or final exit? Who bears which fee? |
| **Retirement-age termination** | `labor-law.md` Art. 74(4) with `social-insurance-law.md` Art. 16, Decision 1022 and Decree clause Fifth | Which regime is the worker on (new-law 65, legacy 60, or phased)? Classify before treating retirement as a lawful end |
| **Waiver or release during the contract** | `labor-law.md` Art. 8 | See Step 4 |
| **Grievance ladder and litigation freeze** | `labor-dispute-route.md` Art. 72 / Annex 1 Art. 71 (30-15-30), Art. 235 (no change of terms during suit), Art. 234(a) (12 months from the end of the relationship), Reg. Art. 14 Second 8(a) (mobility sanction for stalling) | Has the worker grieved or sued? Any change of terms since? |
| **Unemployment-insurance coding** | `social-insurance-law.md` Art. 45 (dismissal attributable to the worker disqualifies); coding practice `[model knowledge — verify]` | Which exit category will be recorded at de-registration? |

For another populated code, build the table from the equivalent rows of
that code's files. **Row missing:** if the facts raise a flag the files do not
cover, say so, tag it `[no rule in <code> files — verify]`, and do not supply
the rule from memory.

**Any flag fires → escalate per `~/.claude/plugins/config/claude-for-legal/employment-legal/CLAUDE.md` before the term proceeds.** Not
after. Before.

### Step 2a: End-of-service award computation (populated non-`usa` codes)

Skip for `usa` (no statutory end-of-service award in the upstream path;
severance is Step 4). For a populated code, compute the statutory award from
the jurisdiction file's rows and nothing else. For `ksa` the rows are
`references/jurisdictions/ksa/labor-law.md` Arts. 84-88 (with Arts. 2, 54,
81, 86, 96, 116 as input rules):

1. **Inputs — refuse to compute if any is missing; ask, do not assume:**
   - W = last monthly **actual** wage (Art. 2: basic plus allowances,
     commissions and customary bonuses; in-kind benefits at up to two months'
     basic wage a year); commission-type elements excluded only under an
     Art. 86 agreement; commission-only or piece-rate pay uses the Art. 96
     average; whether allowances paid in kind are in "last wage" carries
     `[model knowledge — verify]` per the Art. 84 row.
   - S = continuous service in years and fractions (Art. 2; from the first
     start date across renewals, Art. 56, and ownership changes, Art. 18;
     deduction of unpaid leave beyond 20 days under Art. 116 carries
     `[model knowledge — verify]` per the Art. 84 row).
   - Mode of ending: employer termination, expiry, mutual agreement, Art. 74
     event, Art. 81 departure, resignation (Art. 79 bis or Art. 75 notice),
     Art. 87 exception, probation (Art. 54), Art. 80 dismissal.
2. **Base award (Art. 84):** Award = 0.5 × W × min(S, 5) + 1.0 × W ×
   max(S − 5, 0), pro rata for fractions of a year; a month is 30 days
   (Art. 2).
3. **Multiplier by mode:**
   - Employer termination, expiry, mutual agreement, Art. 74 events,
     Art. 81 departure (the full-award reading of Art. 81 is tagged
     `[model knowledge — verify]` in that row): × 1.
   - Resignation (Art. 85): S < 2 years: × 0; 2 ≤ S ≤ 5 years: × 1/3;
     5 < S < 10 years: × 2/3; S ≥ 10 years: × 1 (exactly five years falls in
     the 1/3 band on the wording).
   - Art. 87 exceptions: × 1 (force majeure beyond the worker's control; a
     female worker ending the contract within six months of marriage or
     three months of childbirth).
   - Whether a worker's Art. 75 notice termination of an indefinite contract
     is a "resignation" for Art. 85 after the M/44 definition is an open
     question in the Art. 85 row: state both results and tag
     `[model knowledge — verify]`.
   - Termination during a valid probation (Art. 54) or on a proven Art. 80
     ground: no award; if the Art. 80 procedure fails, the full award is the
     fallback (Art. 80 row).
4. **Emit the number with the computed-number tag and the inputs**, e.g.
   `[currency] 41,250 [computed — labor-law.md Arts. 84-85, settled 2026-09-04;
   inputs: last wage [currency] 15,000, service 4y 6m, employer termination]`.
   Show the formula line and the multiplier chosen. Add the untaken annual
   leave payout (Art. 111, pro rata for fractions of a year) and any
   compensatory-leave balance (Reg. Art. 22 bis(4)) as separate lines with
   their own tags; do not fold them into the award.

For another populated code, apply the award rows of that code's labor-law
file in the same way. **Row missing:** if the file has no award formula, say
so, tag `[no rule in <code> files — verify]`, and do not compute.

### Step 2b: Compensation for termination without a legitimate reason (populated non-`usa` codes)

Skip for `usa`. For `ksa` the row is `references/jurisdictions/ksa/labor-law.md`
Art. 77 (with Arts. 2, 37, 76, 80, 96 and Reg. Art. 14 Second (21)):

1. **When it applies:** the party harmed by a termination for a reason that
   is not legitimate — an employer termination without a legitimate reason
   (Art. 75 row: the Law does not define "legitimate reason"), an Art. 80
   dismissal whose ground or procedure fails, or a fixed-term contract ended
   before expiry. A worker who leaves a fixed-term contract early may owe it
   to the employer (Reg. Art. 14 Second (21) row, `[model knowledge — verify]`
   as to court practice). It is **in addition to** the end-of-service award
   (Step 2a) and pay in lieu of notice (Art. 76).
2. **Inputs — refuse to compute if any is missing:** contract type (a
   non-national's contract is fixed-term, Reg. Art. 12); W = actual monthly
   wage (Art. 2; "last wage in practice" is `[model knowledge — verify]` per
   the Art. 77 row); S = years of service (indefinite); months and days
   remaining to expiry, counted from the actual start date for a defaulted
   Art. 37 term (fixed); any contractual compensation figure.
3. **Formula:**
   - Contractual figure in the contract → it prevails (Art. 77 chapeau);
     whether a figure below the statutory result survives Art. 8 is open
     (Art. 77 row) — state the statutory figure beside it and tag
     `[model knowledge — verify]`.
   - Indefinite: 15 × daily wage × S, daily wage = W ÷ 30 (Art. 2);
     treatment of fractional years is not stated in the text (Art. 77 row) —
     compute on whole years and on pro-rata years, show both, tag
     `[model knowledge — verify]`.
   - Fixed: W × months remaining (plus any partial month pro rata).
   - Floor: not less than 2 × W in either case (Art. 77(3)).
4. **Emit the number with the computed-number tag and the inputs**, e.g.
   `[currency] 30,000 [computed — labor-law.md Art. 77(1),(3), settled
   2026-09-04; inputs: actual wage [currency] 15,000, service 3y, indefinite,
   no contractual figure; two-month floor applied]`.

For another populated code, apply the equivalent compensation row; if none
exists, say so and tag `[no rule in <code> files — verify]`.

### Step 3: Jurisdiction-specific requirements

**When the applicable code is `usa`:**

> **Research the applicable rules for the employee's jurisdiction before
> finalizing the plan.** Specifically:
>
> - Final-pay timing — this varies widely by state and often depends on
>   whether the employee was terminated or resigned. Research the currently
>   operative rule, including any waiting-time or late-pay penalties.
> - Accrued-PTO payout — research whether the jurisdiction requires payout,
>   and any interaction with accrual-cap or use-it-or-lose-it policies.
> - Required notices — research any jurisdiction-specific notices required at
>   termination (e.g., state unemployment, continuation-coverage notices
>   beyond federal COBRA, benefits continuation).
> - Mass-layoff / plant-closing notices — research federal WARN Act and any
>   state "mini-WARN" or local ordinance that may apply if this is part of a
>   larger reduction. Coverage thresholds and notice periods differ.
>
> Cite primary sources. Verify currency.
>
> **No silent supplement.** If a research query to the configured legal research tool returns few or no results for the jurisdiction's final-pay, PTO, notice, or WARN rule, report what was found and stop. Do NOT fill the gap from web search or model knowledge without asking. Say: "The search returned [N] results from [tool]. Coverage appears thin for [jurisdiction / rule]. Options: (1) broaden the search query, (2) try a different research tool, (3) search the web — results will be tagged `[web search — verify]` and should be checked against a primary source before relying, or (4) stop here and flag for attorney verification. Which would you like?" A lawyer decides whether to accept lower-confidence sources.
>
> **Source attribution.** Tag every citation in the plan — final-pay rule, PTO rule, notices, WARN / mini-WARN, OWBPA consideration periods, state release restrictions — with where it came from: `[Westlaw]`, `[CourtListener]`, or the MCP tool name for citations retrieved from a legal research connector; `[web search — verify]` for web-search citations; `[model knowledge — verify]` for citations recalled from training data; `[user provided]` for citations the user supplied. Citations tagged `verify` carry higher fabrication risk and should be checked first. Never strip or collapse the tags.

**When the applicable code is populated (non-`usa`):** the requirements come
from the jurisdiction files, cited by row. For `ksa`:

- **Final settlement window** — `labor-law.md` Art. 88: wages and all dues
  within one week of the end of the relationship where the employer ended it
  or the term expired, two weeks where the worker ended it (restated in
  Annex 5 cls. 11.9-11.10); set-off limited to quantified work-related debts
  (Art. 88 row, `[model knowledge — verify]` as to clearance holds). Compute
  the due date against the calendar in the manifest.
- **Final settlement contents** — wages to date; untaken annual leave at the
  wage, pro rata for fractions of a year (Art. 111; Annex 5 cl. 8.2);
  overtime due and any compensatory-leave balance (Reg. Art. 22 bis(4));
  end-of-service award (Step 2a); Art. 77 compensation where it applies
  (Step 2b); pay in lieu of notice (Art. 76); the return ticket and any
  exit fees for a non-national (Art. 40, `platform-obligations.md`); paid
  through an approved bank (Art. 90). Present the amounts in a numbers table,
  each with its tag.
- **Notice and pay in lieu** — Arts. 75-76 (60/30 days, monthly-paid
  indefinite; 30 days otherwise; pay in lieu at the actual wage for the whole
  period); Art. 78 job-search day and garden leave (service continues);
  notice through the Portal (Annex 5 cl. 14.1). A fixed-term contract has no
  Art. 75 notice; early ending is Step 2b.
- **End-of-service documents** — service certificate with joining date, end
  date, profession and last wage, no damaging content (Art. 64); return of
  the worker's certificates and documents (Art. 64); Qiwa termination or
  resignation record (Annex 5 cl. 14.1; `platform-obligations.md` Art. 51 /
  Reg. Art. 18 row); social-insurance de-registration with the exit reason
  (`social-insurance-law.md` Art. 7; the 15-day practice deadline and the
  unemployment-insurance coding point are `[model knowledge — verify]`);
  for a non-national, transfer of services or final exit (`platform-obligations.md`
  Reg. Art. 14 Second rows; the final-exit mechanics are `[model knowledge —
  verify]`); the Art. 83 non-compete and confidentiality terms, if any,
  restated to the worker.
- **Collective terminations** — the file lists no redundancy ground: a
  restructuring dismissal is framed as termination of the activity
  (Art. 74(7)) or an Art. 75 legitimate-reason termination with Art. 77
  exposure (Art. 74 row). The files carry no collective-dismissal
  notification rule: tag `[no rule in ksa files — verify]` and route to
  local counsel.
- **Timeline** — limitation deadline = end of relationship + 12 months
  (Art. 234(a)); grievance deadlines = notification + 30 days excluding
  official holidays, then 15 days, then 30 days (Art. 72); computed per the
  "Computed dates" rules in `labor-dispute-route.md`, on the calendar the
  contract elects (Gregorian under Annex 5 cl. 14.6, otherwise Hijri per
  Art. 10), never on a Saturday/Sunday weekend.
- **Research step.** To quote or currency-check an article, fetch the
  instrument from the portal named in the manifest (`scripts/fetch-law.py
  --portal boe --id <guid> --lang ar`, GUIDs in
  `references/jurisdictions/<code>/SOURCES.md`; the built-in web-fetch tool
  rejects the portal's TLS chain — use the script or `curl`), quote the
  article, and tag `[BOE — Arabic]` or `[BOE — official English]`. If the
  fetch fails or the article is not found, apply the "no silent supplement"
  rule above: report the failure and stop, or continue with the file's row
  tagged as the file tags it only if the user says so.

For another populated code, take the same headings from that code's files.
**Row missing:** where a file is silent on a settlement, notice or document
item the plan needs, say so and tag `[no rule in <code> files — verify]`.

### Step 4: Severance and release

Per `~/.claude/plugins/config/claude-for-legal/employment-legal/CLAUDE.md` → standard severance:

- Is severance being offered? Per formula or discretionary?
- Release required? (Usually yes if paying severance — that's the
  consideration.)

**When the applicable code is `usa`:**

> **Research the applicable release-consideration rules.** If the employee is
> 40 or over, federal law (OWBPA) imposes specific requirements that affect
> the consideration period, revocation period, required advisements, and —
> for group terminations — required decisional-unit disclosures. The specific
> consideration period differs between an individual termination, a group
> RIF, and a group exit incentive; the rule also depends on the employee's
> age and the number of employees affected. Do not state the day count from
> memory — research the currently operative rule for the specific situation
> and cite primary sources. Also research any state-law analogs or parallel
> release requirements. Verify currency.

Separately, consider whether any of the following apply to the release:
- State-specific waiver restrictions (some states limit what can be released
  or require specific language).
- Federal or state restrictions on non-disclosure or non-disparagement
  clauses that relate to sexual harassment, discrimination, or other
  protected categories.
- Separation-agreement rules on NLRA-protected activity.

**When the applicable code is populated (non-`usa`):** the release rules are
the file's rows. For `ksa`:

- **Statutory rights cannot be waived during the contract** —
  `labor-law.md` Art. 8 (`[settled — last confirmed 2026-09-04]`): any
  release or settlement of the worker's statutory rights while the contract
  is running is void unless more beneficial to the worker. The end-of-service
  award (Step 2a), leave payout, wages and Art. 77 compensation are statutory
  floors, not consideration; a "severance" is only the amount above the
  statutory entitlement recorded in the profile (`## Termination review` →
  Standard severance above the statutory entitlement).
- **Settlement after the relationship has ended** — the Art. 8 row and
  `labor-dispute-route.md` (Art. 8 row) tag court treatment of a
  post-termination release below the statutory floor `[model knowledge —
  verify]`, and the practice of recording a settlement before the labour
  authority after termination as the enforceable form `[model knowledge —
  verify]`; carry those tags onto the finding and route the drafting to local
  counsel.
- **Release as the price of a transfer** — `platform-obligations.md`
  Reg. Art. 14 Second item 15: the employer's consent to a non-national's
  transfer may not be conditioned; a settlement clause trading the transfer
  approval for a waiver is unenforceable as a condition of the approval
  (`[model knowledge — verify]` for court practice).
- **Non-compete and confidentiality** — `labor-law.md` Art. 83 (written,
  specific as to time, place and type of work, two years maximum; employer's
  claim within one year of discovery).
- Age-based consideration periods, decisional-unit disclosures and NLRA
  separation-agreement rules are `usa` doctrine and do not apply; do not
  import them.

For another populated code, cite that code's waiver and settlement rows.
**Row missing:** if the files carry no settlement-agreement rule for the
point at issue, say so and tag `[no rule in <code> files — verify]`.

### Step 5: Documentation check

For performance terminations especially:

- Is there a paper trail? Written warnings, PIP, feedback docs?
- Does the paper trail tell a consistent story?
- Is there anything in writing that contradicts the reason (recent positive
  review, bonus, promotion)?

The "why now" question: if this person has been underperforming for a year,
what changed? The answer should be documented.

## Output

> **Research-connector pre-flight.** Before emitting the memo, check whether a legal research connector is reachable for this session — for `usa`, Westlaw, CourtListener, or any firm-configured research MCP; for a populated non-`usa` code, the portal named in `references/jurisdictions/<code>/MANIFEST.md` → `research_tool` (for `ksa`, `scripts/fetch-law.py --portal boe --index` or a `curl` of the portal home). Collect this into the reviewer note per CLAUDE.md `## Outputs`: if no connector returns results in Step 3 (or none is configured at run time), record it in the **Sources:** line of the reviewer note — for `usa`, e.g., `not connected — cites from training knowledge; the highest-fabrication topics in termination-law memos are final-pay timing, OWBPA group/individual distinctions, state-specific NDA / non-disparagement rules (e.g., CA SB 331), and NLRB positions (e.g., McLaren Macomb) — spot-check those first`; for a populated code, `portal: <host> ✓ reachable | unreachable` plus the files applied, and the highest-fabrication topics are the wage components in "last wage", the resignation fractions, and any fine amount or platform deadline the files tag `[model knowledge — verify]`. Per-citation tags remain inline. Do not emit a standalone banner above the memo.

> **Jurisdiction assumption.** This review assumes the jurisdiction code(s) resolved in Step 0 and any defaults from `~/.claude/plugins/config/claude-for-legal/employment-legal/CLAUDE.md` → `## Jurisdiction` and Jurisdictional footprint. Employment rules, settlement timing, release requirements, and notice obligations vary materially by jurisdiction. If the employee works under a different code, or if choice-of-law is contested, this analysis may not apply as written. An unpopulated code is a stop, not a caveat (Step 0).

> **Header, disclaimer and language.** Prepend the work-product header, then — for every code other than `usa` — the jurisdiction disclaimer line from the profile (`## Outputs` → Jurisdiction disclaimer line; for `ksa` the manifest's `disclaimer` row, in English and Arabic). Apply the bilingual house style in CLAUDE.md `## Outputs`: when the profile's output language is bilingual, or the memo contains counterparty-facing text (termination letter, settlement wording), add the authoritative-language rendering of the bottom line, the numbers table (award, compensation, notice, leave payout, settlement total) and every counterparty-facing passage, using the spellings in the manifest's `output_language_rule`. Money in `[currency]` from the profile; dates on the manifest's calendar. Terminability without cause or notice is `usa` doctrine and appears only inside the `usa` branch of this skill; for a populated code the ground, notice and award rows of the file govern.

Match the memo format from seed term memos referenced in `~/.claude/plugins/config/claude-for-legal/employment-legal/CLAUDE.md`. If none:

```markdown
[WORK-PRODUCT HEADER — per plugin config ## Outputs — differs by role; see `## Who's using this`]
[JURISDICTION DISCLAIMER LINE — per plugin config ## Outputs, for every code other than `usa`, English and authoritative language]

## Termination Review: [Role/Name] — [Date]

**Jurisdiction:** [code(s) from Step 0, e.g. `[ksa]`; for `usa` the state]
**Contract type / nationality:** [fixed-term or indefinite / nationality — populated codes]
**Reason:** [Performance / Misconduct / RIF / Elimination — and, for a populated code, the article the ground falls under]
**Planned date:** [Date, on the manifest's calendar]

---

### Bottom line

[Can you proceed / Need to fix X first / Stop — one-sentence why]
[Authoritative-language rendering of the bottom line when the profile asks — see `## Outputs`]

---

### High-risk flags

[Every flag from Step 2 (the `usa` table or the jurisdiction-file table). ✅ Clear or 🔴 FLAG with detail and the source row.]

**Escalation:** [None needed | Escalate to [name] before proceeding — [which flag]]

---

### Jurisdiction requirements ([code] — populated non-`usa` codes; for `ksa` the rows of Step 3)

- End-of-service award: [Step 2a number with the computed-number tag and inputs; formula line; multiplier]
- Compensation for termination without a legitimate reason: [Step 2b number with tag and inputs, or "not applicable — ground [article] met"]
- Notice: [statutory period per the file row, given / pay in lieu amount with tag, Portal record yes/no]
- Leave and other balances: [untaken annual leave payout, compensatory leave, overtime — each with tag]
- Final settlement: [due date per the file's window on the manifest's calendar; total in `[currency]`; bank payment]
- Documents: [service certificate, document return, platform termination record, social-insurance de-registration, transfer or exit for a non-national — each with its row and tag]
- Timeline: [limitation and grievance dates computed per the dispute-route file]
- Gaps: [every `[no rule in <code> files — verify]` item]

**Numbers table** (repeat in the authoritative language when the profile asks):

| Item | Amount ([currency]) | Source row and tag | Inputs |
|---|---|---|---|
| [end-of-service award] | [n] | [file, articles, settled date] | [W, S, mode] |
| [compensation] | [n] | [file, article] | [W, S or months remaining, floor] |
| [pay in lieu of notice] | [n] | [file, article] | [W, days] |
| [leave payout] | [n] | [file, article] | [days] |
| [total settlement] | [n] | [Art. 88 window] | [due date] |

---

### Jurisdiction requirements ([State] — when the applicable code is `usa`)

- Final pay: [researched rule and cite; state whether PTO is included per the
  researched rule and any team policy]
- Required notices: [list, each researched and cited]
- Mass-layoff notice (if applicable): [researched rule and cite]

---

### Severance and release

- Severance: [amount above the statutory entitlement per the profile formula / none; for a populated code the statutory items above are not severance]
- Release: [`usa`: required / not — if required, research and apply the
  consideration-period, revocation-period, advisement, and (for groups)
  decisional-unit-disclosure requirements that govern this specific
  situation; cite primary sources and verify currency. Populated code: the
  file's waiver rule (for `ksa`, `labor-law.md` Art. 8) and the settlement
  practice with the file's tag]
- [Any state-law release rules or non-disclosure/non-disparagement
  restrictions that apply — `usa`]

---

### Documentation

[Assessment of paper trail. Gaps flagged.]

---

### Go / No-go

[Clear to proceed | Proceed with changes below | Hold — escalation pending]

### Checklist for term day

When the applicable code is `usa`:

- [ ] Final paycheck ready, correct amount, delivered per researched rule
- [ ] Continuation-coverage notices (COBRA / state analogs) prepared
- [ ] [State] unemployment notice prepared
- [ ] Severance agreement (if applicable) with the consideration period
      required for this specific situation
- [ ] Return of property / access cutoff coordinated
- [ ] [etc.]

When the applicable code is populated (non-`usa`) — items from the file rows in Step 3; for `ksa`:

- [ ] Written notice for the statutory or contractual period through the Portal, or pay in lieu computed (Arts. 75-76, Annex 5 cl. 14.1)
- [ ] End-of-service award, leave payout, compensatory-leave balance and any Art. 77 amount computed with tags (Steps 2a, 2b, Art. 111, Reg. Art. 22 bis(4))
- [ ] Final settlement paid through an approved bank within the Art. 88 window (7 / 14 days on the manifest's calendar)
- [ ] Service certificate and returned documents (Art. 64)
- [ ] Platform termination record; social-insurance de-registration with the exit reason (`platform-obligations.md`, `social-insurance-law.md` Art. 7)
- [ ] Non-national: transfer of services or final exit, return ticket and fees on the employer (Art. 40; Reg. Art. 14 Second) — mechanics `[model knowledge — verify]`
- [ ] Settlement wording, if any, drafted after the relationship ends and reviewed by local counsel (Art. 8)
- [ ] Return of property / access cutoff coordinated
- [ ] Reviewer-note line: `Jurisdiction: <codes>; files: <list>; portal fetched: yes/no; unpopulated codes: <list or none>`
```

## Consequential-action gate (terminate an employee)

**Before producing a "Go" recommendation or a term-day checklist marked ready:** Read `## Who's using this` in `~/.claude/plugins/config/claude-for-legal/employment-legal/CLAUDE.md`. If the Role is **Non-lawyer**:

> Terminating an employee has legal consequences — wrongful-termination, discrimination, retaliation, and wage-law claims all trace back to how this decision is structured. Have you reviewed this termination with an attorney? If yes, proceed. If no, here's a brief to bring to them:
>
> - Employee, jurisdiction, reason, planned date
> - Every high-risk flag the review surfaced (recent complaint, protected leave, protected class + timing, whistleblower, thin documentation, comparator, contract/handbook promise) — with detail
> - Jurisdiction-specific findings — for `usa`: final pay, PTO, required notices, mass-layoff rules; for a populated code: the end-of-service award and compensation numbers with their tags and inputs, the notice and settlement window, the documents list, and every `[no rule in <code> files — verify]` gap — and where each was cited from
> - Severance/release analysis — for `usa`, including any OWBPA/older-worker-protection angles; for a populated code, the file's waiver rule and the settlement practice with its tag
> - Open questions and what's unresolved
> - What could go wrong (the claim theory this fact pattern supports)
> - What to ask the attorney (is this a clean term; do we need more documentation first; does the release need specific language; for `usa`, do we need to stagger decisional units; for a populated code, is the stated ground one the file treats as legitimate and is the local counsel named in the profile available)
>
> If you need to find an attorney, solicitor, barrister, or other authorised legal professional: contact your professional regulator (state bar in the US, SRA/Bar Standards Board in England & Wales, Law Society in Scotland/NI/Ireland/Canada/Australia, or your jurisdiction's equivalent) for a referral service. Employment is one of the practice areas where a short consult before the termination meeting consistently outvalues a post-termination claim defense.

Do not produce a "Clear to proceed" output past this gate without an explicit yes. A marked-DRAFT flagged for attorney review is fine.

---

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs`. Customize the options to what this skill just produced — the five default branches (draft the X, escalate, get more facts, watch and wait, something else) are a starting point, not a lock-in. The tree is the output; the lawyer picks.

## What this skill does not do

- Make the termination decision. It checks the decision.
- Have the conversation. The manager does that.
- State release or jurisdiction rules from memory — every rule is a cited row
  of the applicable jurisdiction file or, for `usa`, researched and cited at
  the time of review.
- Apply another jurisdiction's rules to an unpopulated code, or compute a
  number with a missing input.
- Guarantee no lawsuit. It reduces the risk by catching the obvious problems.
