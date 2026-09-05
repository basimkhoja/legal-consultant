---
name: worker-classification
description: >
  Classify a proposed worker engagement — employee, contractor, seconded,
  agency or outsourced — by running the tests and categories of the
  jurisdiction resolved from the practice profile (jurisdiction-file rows, or
  researched tests for `usa`) and flagging misclassification gaps between the
  intended arrangement and what the facts support. Prospective use only. Use
  when someone says "we want to bring on a contractor", "is this a vendor or
  a temp", "how should we classify this person", or describes a proposed
  working arrangement.
argument-hint: "[describe the proposed arrangement, or just start and I'll ask]"
---

# /worker-classification

Runs the applicable classification tests for the jurisdiction and flags where
the proposed arrangement doesn't match the structure you're trying to use.
Prospective only — for existing relationships, consult counsel.

## Instructions

1. Load `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/CLAUDE.md` → jurisdictional footprint, escalation table.
2. Run the full workflow below.
3. If the attorney provides details upfront, extract what's available and ask
   only about the gaps. Do not re-ask information already provided.

## Examples

```
/employment-legal:worker-classification
We want to bring on a data scientist for 6 months, working out of our
SF office, using our tools, embedded in our analytics team.
```

```
/employment-legal:worker-classification
Is our recruiter contractor arrangement okay? She works exclusively for
us, sets her own hours, uses her own laptop, project fee per placement.
```

```
/employment-legal:worker-classification
(skill will ask for details)
```

---

## Matter context

**Matter context.** Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗` (the default for in-house users), skip the rest of this paragraph — skills use practice-level context and the matter machinery is invisible. If enabled and there is no active matter, ask: "Which matter is this for? Run `/employment-legal:matter-workspace switch <slug>` or say `practice-level`." Load the active matter's `matter.md` for matter-specific context and overrides. Write outputs to the matter folder at `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/matters/<matter-slug>/`. Never read another matter's files unless `Cross-matter context` is `on`.

---

## Purpose

The most expensive classification decision is the one nobody made consciously.
Someone describes what they want ("a contractor"), the engagement starts, and
two years later the facts look like employment. This skill walks the applicable
tests on the proposed arrangement before it starts — and tells you when what
you're describing doesn't match the structure you're trying to use.

This skill teaches the reasoning pattern. It does not state the law from
memory. For `usa`, every test formulation, statutory citation, threshold, and
carve-out must come from current research; for a populated jurisdiction code,
from the rows of `references/jurisdictions/<code>/` cited by article.

## Prospective-only hard gate — run BEFORE intake

**This skill analyzes a PROPOSED engagement before the work starts.** Before any substantive intake (Step 1), ask:

> Has this work already started? Is the worker currently engaged, or have they been performing work under this arrangement for any period of time (days, weeks, months, or years)?

If the answer is yes — the engagement already exists, in any form, for any duration — **STOP**. Do not proceed to Step 1 intake. Classifying an existing arrangement is not a planning exercise; it's a liability assessment with remediation implications. When the applicable code is `usa`: back pay (OT, meal/rest premiums), unpaid employer-side payroll tax, benefits eligibility that was denied, unemployment and workers' comp back-exposure, state penalties (in CA, PAGA), IRS § 530 relief analysis, and — in strict-test jurisdictions with ongoing work — the prospective exposure of letting it run another day. When the applicable code is populated (non-`usa`), the exposure list comes from the jurisdiction files — for `ksa`: Labor Law coverage from day one of the relationship (`labor-law.md` Art. 5; Reg. Art. 1 for a "temporary" hire past 90 days), with the award, leave and overtime entitlements that follow; social-insurance back-contributions with the Art. 9 delay fine and Art. 59 per-contributor penalties and five-year look-back (`social-insurance-law.md`); the Art. 39 / Art. 30 exposure for a non-national working for someone other than the permit holder, including the Art. 229 bis fine for unlicensed outsourcing (`platform-obligations.md`); and the worker's inclusion in the client's nationalisation ratio (`saudization-nitaqat.md` labour-services row). The files carry no back-pay multiplier or tax-relief analogue; do not import one. That analysis is privileged where the jurisdiction recognises privilege (CLAUDE.md `## Outputs`), led by counsel, and coupled with a remediation plan.

Output exactly this block and wait for a response:

> **Out of scope — existing arrangement.**
>
> This skill is designed to analyze a worker engagement *before it starts*, so the classification choice informs how to structure the contract and operations. You've described an arrangement that already exists. Analyzing an existing engagement retroactively is a different exercise: reclassification risk assessment coupled with remediation planning — back-pay exposure, payroll-tax back-exposure, penalty exposure, benefits exposure, IRS § 530 relief analysis, and prospective restructuring. That work should be privileged, led by an attorney, and likely coupled with outside-counsel review given the dollar and enforcement exposure.
>
> Recommended next step: escalate per your config's escalation table (for retroactive classification, this typically routes to GC + outside employment counsel). I've flagged this for escalation routing.
>
> **If you want to proceed with the prospective-style analysis anyway for planning purposes, say "proceed anyway" — but understand:**
>
> - The output is NOT a remediation plan and should not be treated as one.
> - The output does NOT scope back-pay, penalty, or payroll-tax exposure for the period already worked.
> - The output does NOT substitute for the reclassification-risk assessment that this fact pattern actually calls for.
> - The output will carry a prominent banner reflecting this scope mismatch, and the consequential-action gate will require an attorney yes before the analysis is treated as reliable.
>
> Only say "proceed anyway" if you're using this skill for forward-looking planning (e.g., "if we were structuring this fresh today, how should we think about it?") and you have a separate plan for the remediation question.

**Only proceed past this gate with an explicit `"proceed anyway"` (or equivalent user instruction). A hesitant "I guess" does not count — re-prompt. If the user proceeds anyway, prepend this banner to every output of this skill for this session:**

```
⚠️ SCOPE MISMATCH — OUT-OF-SCOPE USE
This skill analyzes prospective worker engagements. The arrangement here
already exists. This output is the prospective-style analysis the user
requested for planning purposes only — it is NOT a remediation plan, does
NOT scope existing back-pay / penalty / payroll-tax exposure, and does
NOT substitute for the reclassification-risk assessment this fact pattern
requires. The remediation question has been flagged for escalation to
counsel per your config's escalation table.
```

If the answer to "has this work already started?" is no (the engagement is genuinely prospective, not yet begun), proceed to load context.

---

## Load context

Read `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/CLAUDE.md` → jurisdictional footprint, any classification history or
prior settlements noted, escalation table, and any house classification
policy the team has recorded.

## Output header

Prepend the work-product header from `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/CLAUDE.md` → `## Outputs` (it differs by user role — see `## Who's using this`).

## Workflow

### Step 0: Resolve the applicable jurisdiction

1. **Read the practice profile's `## Jurisdiction` section.** It gives the primary jurisdiction code, the footprint list (other codes the practice operates in), the output-language preference, and whether local counsel is available for escalation. Codes are ISO 3166-1 alpha-3 lowercase (`ksa`, `gbr`, `fra`, `che`, `usa`). If the section is missing or still a placeholder, stop: "The practice profile has no jurisdiction. Run the cold-start interview; nothing in this skill can run against the wrong jurisdiction."
2. **Determine the matter's jurisdiction(s).** Start from the primary code. Then read the matter facts: governing-law clause, seat of arbitration, place of employment, jurisdiction of incorporation, place of performance. If the facts point to a code not in the profile, add it for this matter and say so in the reviewer note. A matter may have more than one code (a contract governed by English law with a Saudi counterparty and Saudi performance is `gbr` + `ksa`). A foreign court forum or arbitral seat under a populated governing law is analysed from the populated code's enforcement rows (whether that forum's judgment or award would be enforced there); it does not add the foreign code unless the user asks for that law's view, and the reviewer note says the forum-side question was not analysed.
3. **Load the jurisdiction folder for each code.** The folder is `references/jurisdictions/<code>/` in this plugin (the same tree ships at the repo root and in every runtime adapter). Read `MANIFEST.md` first.
   - If `populated` is not `yes`: **stop for that code.** Say: "Jurisdiction `<code>` (<name>) is registered but not populated: no reference files exist for it. I will not apply another jurisdiction's rules or model knowledge in its place. Options: (1) populate `references/jurisdictions/<code>/` (see README, 'How to add a jurisdiction'), (2) route this matter to local counsel, (3) tell me to proceed with the analysis limited to the populated jurisdictions in this matter, with every finding for `<code>` marked `[not populated — no rule applied]`." Wait for the answer. Never fall back silently.
   - If the code is `usa`: there is no folder. Follow this skill's US path (the upstream doctrine and the upstream research connectors, CourtListener or Westlaw, with the upstream "no silent supplement" rule). Label findings `[usa]`.
   - If `populated` is `yes`: read `INDEX.md`, then the instrument files this skill names in its "Jurisdiction files" list. A row tagged `[settled — last confirmed YYYY-MM-DD]` may be applied and cited by article. A row tagged `[model knowledge — verify]` may be applied only with that tag carried onto the finding. If a rule this skill needs is not in the files at all, do not supply it from memory: say what is missing, tag the gap `[no rule in <code> files — verify]`, and continue only with the rules that exist.
4. **Multi-jurisdiction matters.** Run the relevant files side by side. Label every finding with its code in square brackets, `[ksa]`, `[gbr]`, `[usa]`, and never merge two jurisdictions' rules into one sentence. Where the codes conflict (a clause valid under one law and reducible under another), state both and flag `[review]` for the lawyer to decide which governs.
5. **Research step (when a rule must be quoted or its currency checked).** Use the portal named in `MANIFEST.md` → `research_tool`. For `ksa`: `python3 scripts/fetch-law.py --portal boe --id <guid> --lang ar` (GUIDs in `SOURCES.md`), or `curl -sS https://laws.boe.gov.sa/BoeLaws/Laws/LawDetails/<guid>/1`; the built-in web-fetch tool rejects the portal's TLS chain. Quote the article, tag `[BOE — Arabic]` (or `[BOE — official English]` when quoting the translation), and check the status line and the "تعديلات المادة" block for amendments. If the fetch fails or the article is not found, apply the "no silent supplement" rule: report the failure and stop. A stopped run still emits: the reviewer note (item 8) with `portal fetched: no` and a Sources line recording which fetch failed; every finding or number that depends on the unfetched article, listed as PENDING; and the options: (1) cite the jurisdiction file's row under its own `[settled — last confirmed YYYY-MM-DD]` tag, stating that the portal was not re-checked this session, (2) retry the fetch by another route (`curl`, the script) or hand the check to local counsel, (3) continue with the rule tagged `[model knowledge — verify]`. Take none of them until the user chooses. Nothing in a stopped run is tagged `[BOE — Arabic]` or `[BOE — official English]`.
6. **Calendar and language.** Take the weekend, public-holiday, calendar (Hijri or Gregorian) and currency rules from `MANIFEST.md`. Compute every date and roll-back against that calendar, never against a Saturday/Sunday weekend or US federal holidays. Produce the deliverable in English; when the profile's output-language preference is bilingual, or the manifest's authoritative language is not English and counterparty-facing text is produced, add the authoritative-language rendering of the bottom line, the findings table, and any counterparty-facing text, using the spellings in the manifest's `output_language_rule`.
7. **Header and disclaimer.** Prepend the manifest's `disclaimer` line under the work-product header for every deliverable that applies a non-`usa` jurisdiction. For `ksa`: "Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance." with its Arabic rendering from the manifest.
8. **Record in the reviewer note.** `Jurisdiction: <codes applied>; files: <list>; portal fetched: yes/no; unpopulated codes: <list or none>.`

**Jurisdiction files this skill loads** (for a populated non-`usa` code; for `ksa` these are the files named, for another populated code the equivalent instrument files listed in that folder's `INDEX.md`):

- `references/jurisdictions/<code>/MANIFEST.md`, `INDEX.md`, `playbook-defaults.md` Labor table (contract types, platforms, social insurance rows).
- `references/jurisdictions/<code>/labor-law.md` — Art. 2 (worker, employer, wage definitions; temporary work; assignment), Art. 5 and Art. 6 (scope; the subordination test; casual, seasonal and temporary workers), Art. 7 (exclusions, including the visiting specialist of two months or less), Art. 11 (assignment of work to another person), Arts. 30, 33, 37, 39 (licensed activities, work permit, fixed term for non-nationals, work for others), Arts. 119-120 (part-time and flexible work), Art. 50 (contract definition). Steps 2, 3, 4.
- `references/jurisdictions/<code>/labor-law-implementing-regulations.md` — Reg. Art. 1 (90-day conversion of temporary or casual contracts), Reg. Art. 10 and Annexes 3-4 (licensed placement, recruitment and labour-services suppliers), Reg. Art. 13 (Ajeer secondment), Reg. Art. 16 bis (training contracts), Reg. Art. 27 First and Second (part-time and flexible-work definitions and caps), Reg. Art. 6 / Law Arts. 49, 120 (safety protection reaches every category). Steps 2, 4.
- `references/jurisdictions/<code>/platform-obligations.md` — Art. 39 with Reg. Art. 13, Art. 30 with Art. 229 bis, Reg. Art. 14 First item 16 (no recruitment or transfer without actual work), Art. 33 (permit only under an employer's responsibility). Steps 2, 4.
- `references/jurisdictions/<code>/social-insurance-law.md` — Art. 1 (worker and employer definitions), Art. 7 (registration), Art. 9 (payment and delay fine), Art. 59 (penalties per contributor, five-year limitation). Steps 2, 4.
- `references/jurisdictions/<code>/saudization-nitaqat.md` — the labour-services row (supplied workers count in the client's ratio), Reg. Art. 14 First item 16 via `platform-obligations.md`, the part-time and flexible-work counting row. Steps 2, 4.
- `references/jurisdictions/<code>/occupational-safety.md` — Reg. Art. 6, Arts. 49, 120 (exclusions step). Step 4.
- `references/jurisdictions/<code>/labor-dispute-route.md` — Reg. Arts. 1(2), 17, 27 Third, 28(5) (labour courts hear status disputes for every category). Step 4.

### Step 1 — Information gathering

Ask all of the following in a single block. Do not drip questions one at a
time. Briefly explain why you're asking — attorneys answer better when they
understand what the question is testing.

> To run the right classification tests I need to understand the proposed
> arrangement in detail. Please answer as many of these as you can — the more
> complete the picture, the more accurate the analysis:
>
> **The work**
> - What will this person actually do day-to-day?
> - Is this work part of your company's core business, or peripheral to it?
>   (e.g., a software engineer at a software company = core; an IT
>   contractor at a law firm = more peripheral)
> - Is this a defined project with a clear end, or ongoing indefinite work?
> - How specialized is the skill? Does this person have expertise your team
>   doesn't?
>
> **Control**
> - Who sets their hours and schedule — them or you?
> - Where will they work — your office, their location, or either?
> - Will you direct how they do the work (methods, process, sequence), or
>   just what the end result should be?
> - Will they supervise any of your employees?
>
> **Economics**
> - How will they be paid — hourly, daily, or fixed project fee?
> - Will you provide equipment, tools, or software, or do they use their own?
> - Do they work for other companies, or will this be exclusive?
> - Will they bear any financial risk — can they profit beyond the fee, or
>   lose money on the engagement?
> - Do they have their own business entity? (`usa`: LLC, S-corp, sole
>   proprietor. Populated code: the entity forms the file names — for `ksa`
>   a commercial registration under `commercial-register-law.md`, or a
>   licensed labour-services or placement company under Reg. Art. 10 /
>   Annex 4; the `ksa` files carry no freelancer or self-employed permit
>   rule, so that route is `[no rule in ksa files — verify]`.)
>
> **The arrangement**
> - How do you want to structure this — direct contractor, staffing agency
>   temp, or vendor/SOW (company-to-company)?
> - If staffing agency: who pays the worker — the agency or you? Who controls
>   day-to-day work?
> - Will there be a written contract? Do you have a template in mind?
> - Roughly how long is the engagement — weeks, months, over a year?
> - Will they work alongside your employees doing similar work?
>
> **Purpose(s) of the classification**
> - What legal purposes does the classification need to serve? `usa`:
>   federal payroll tax, FLSA wage/hour, state wage/hour, unemployment
>   insurance, workers' compensation, benefits eligibility — different
>   purposes are often governed by different tests, and the answers can
>   diverge. Populated code: the purposes the files name — for `ksa`: Labor
>   Law coverage (`labor-law.md` Art. 5), social-insurance registration
>   (`social-insurance-law.md` Art. 1), the nationalisation count
>   (`saudization-nitaqat.md`), work-permit and licensed-activity compliance
>   (`platform-obligations.md` Arts. 30, 33, 39); tax treatment is not in the
>   `ksa` files (`[no rule in ksa files — verify]`).
>
> **Jurisdiction and nationality** (populated codes)
> - Where will this person physically perform the work?
> - Nationality, and — for a non-national — which entity holds or will hold
>   the work permit (`labor-law.md` Art. 33; `platform-obligations.md`)
> - If seconded or supplied: does the supplier hold the licence the file
>   requires, and is the placement documented on the platform the file names
>   (Reg. Art. 10 / Annex 4; Reg. Art. 13)?

Wait for responses before proceeding. If the attorney can't answer certain
questions, note the gaps — they affect the analysis.

### Step 2 — Identify the applicable tests

**When the applicable code is populated (non-`usa`):** the test and the
category labels are the file's rows; research is used only to quote or
currency-check them (Step 0, item 5: `scripts/fetch-law.py --portal boe --id
<guid> --lang ar`, GUIDs in `references/jurisdictions/<code>/SOURCES.md`, tag
`[BOE — Arabic]`; if the fetch fails, apply the "no silent supplement" rule
below). For `ksa`:

- **The test** — `labor-law.md` Art. 2 (worker: any natural person working
  for an employer and under his management or supervision for a wage, even
  if not under his direct control; employer definition) and Art. 5 (the Law
  applies to every contract whereby a person works for an employer under his
  management or supervision for a wage). The Art. 5 row states that this
  subordination-for-a-wage test **is** the classification test and that
  there is no separate statutory contractor test. `social-insurance-law.md`
  Art. 1 uses the same definition for registration. The files enumerate no
  factor list, weighting or presumption beyond the definition: say so and tag
  any weighing of factors `[no rule in ksa files — verify]`.
- **Statutory routes and categories the files do define** — casual, seasonal
  and temporary work (Art. 6; temporary work capped at 90 days and converted
  by Reg. Art. 1); part-time and flexible work (Arts. 119-120; Reg. Art. 27:
  part-time under half the establishment's hours, written and fixed-term;
  flexible work hourly, nationals only, one year and 160 hours a month with
  one employer); training contracts (Reg. Art. 16 bis); assignment of a
  worker through a licensed establishment (Art. 2 "assignment", Art. 30,
  Reg. Art. 10 / Annex 4, Art. 229 bis); secondment of a non-national through
  Ajeer (Art. 39, Reg. Art. 13); the visiting specialist for a specific task
  of two months or less, outside the Law (Art. 7(e)); no recruitment or
  transfer without actual work (Reg. Art. 14 First item 16).
- **Purpose tracks** — Labor Law coverage, social-insurance registration and
  the nationalisation count run on the same definition; the licensed-activity
  and work-permit rules are the second track for non-nationals and supplied
  workers.

For another populated code, cite that code's definition and route rows.
**Row missing:** if the files carry no test for a purpose the user needs
(for `ksa`: tax, a freelancer permit, remote work — the regulations file
records that it has no remote-work article), say so, tag `[no rule in <code>
files — verify]`, and do not supply a test from memory.

**When the applicable code is `usa`:**

> **Research the applicable tests before proceeding.** For the jurisdiction(s)
> and purpose(s) identified in intake, research the currently operative
> classification test(s). Jurisdictions commonly use one or more of: an ABC
> test, an economic-realities test, a common-law right-to-control test, a
> hybrid, or a purpose-specific statutory test. The test that governs for
> federal payroll tax may not be the same test that governs for state
> wage/hour, unemployment, or workers' compensation — run each purpose on its
> own track. Cite the controlling statute, regulation, or case. Note the
> effective date of each rule and whether it has been recently amended.
> Identify any carve-outs or exceptions that may apply (e.g., B2B,
> professional services, construction, referral-agency, business-to-business
> contracting relationship). Verify currency. If you are uncertain about the
> current state of the law in any jurisdiction, flag it for attorney
> verification — do not state a test you haven't confirmed.

If `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/CLAUDE.md` records the company's house classification policy, apply it
first and flag any tension with the researched test.

> **No silent supplement.** If a research query to the configured legal research tool returns few or no results for a jurisdiction-and-purpose combination, report what was found and stop. Do NOT fill the gap from web search or model knowledge without asking. Say: "The search returned [N] results from [tool]. Coverage appears thin for [jurisdiction / purpose / test]. Options: (1) broaden the search query, (2) try a different research tool, (3) search the web — results will be tagged `[web search — verify]` and should be checked against a primary source before relying, or (4) flag as unverified and stop. Which would you like?" A lawyer decides whether to accept lower-confidence sources.
>
> **Source attribution.** Tag every citation — each classification test, statute, regulation, or case — with where it came from: `[Westlaw]`, `[CourtListener]`, or the MCP tool name for citations retrieved from a legal research connector; `[web search — verify]` for web-search citations; `[model knowledge — verify]` for citations recalled from training data; `[user provided]` for citations the attorney supplied. Citations tagged `verify` carry higher fabrication risk and should be checked first. Never strip or collapse the tags.

### Step 3 — Apply the researched tests to the facts

For each test identified in Step 2, apply it to the intake facts. Score each
factor or prong explicitly — do not summarize. The attorney needs to see which
factors are clean and which are problems.

Use a structure like the one below, but populate the *factors* from the
researched test (`usa`) or the file's definition rows (populated code), not
from this file. For `ksa` the rows to score are: work performed for the
employer; under the employer's management or supervision (the "even if not
under his direct control" clause in Art. 2); for a wage; plus the route
facts (duration against the 90-day and one-year caps, hours against the
part-time and flexible-work thresholds, nationality and permit holder,
supplier licence and platform record). Any inference beyond those elements
is tagged `[no rule in ksa files — verify]`.

```
Test: [name of test, per research]
Purpose: [what this test governs — federal tax / state wage-hour / UI / etc.]
Source: [pinpoint cite to statute/regulation/case]
Currency: [verified as of date]

| Factor / prong | Intake facts | Signal / pass-fail |
|---|---|---|
| [Factor 1 from researched test] | [from intake] | [direction or pass/fail] |
| [Factor 2] | [from intake] | [direction or pass/fail] |
| ...                            |                |                   |

Structure of the test:
[How the test weighs factors — e.g., a multi-factor balancing test, or a
conjunctive test where each prong must be satisfied, or a hybrid. State this
from research, not from memory.]

Result under this test:
[Employee-leaning / IC-leaning / Fails prong X / Uncertain — contested prong]
```

Repeat for each applicable test.

**Notes on contested prongs.** Some prongs of some tests are heavily contested
in case law and fact-sensitive. Identify contested prongs explicitly — do not
paper over them. The fact that a test is stated does not mean its application
to these facts is settled; flag prongs that require attorney judgment or that
have generated recent litigation in the jurisdiction.

### Step 4 — Classify and flag gaps

**The classification call**

Based on the test results, state the most accurate classification for this
proposed arrangement. The category labels depend on the code.

**When the applicable code is populated (non-`usa`):** use the file's
categories. For `ksa`:

- **Worker under a Labor Law contract** (`labor-law.md` Arts. 2, 5, 50):
  fixed-term or indefinite (Art. 37 and Art. 55: a non-national's contract is
  always fixed-term), part-time (Reg. Art. 27 First), flexible-work
  (Reg. Art. 27 Second, nationals only), temporary or casual (Art. 6, with
  Reg. Art. 1 conversion at 90 days). Documentation on the approved platform
  and social-insurance registration follow (`platform-obligations.md`
  Art. 51 / Reg. Art. 18; `social-insurance-law.md` Art. 7).
- **Trainee** under a training contract (Reg. Art. 16 bis): not an employee,
  but a written contract is required and safety protection applies.
- **Seconded non-national** through Ajeer (Art. 39, Reg. Art. 13): lawful
  only with the platform notice; otherwise an Art. 39 finding.
- **Supplied worker** from a licensed labour-services or placement company
  (Art. 30, Reg. Art. 10 / Annex 4): the supplier must hold the licence; the
  worker counts in the client's nationalisation ratio unless the ministry
  sets conditions (`saudization-nitaqat.md` labour-services row); an
  unlicensed supplier exposes both parties (Art. 229 bis; Annex 4 Art. 70).
- **Visiting specialist** for a specific task of two months or less
  (Art. 7(e)): outside the Law; longer stays need a permit and a contract.
- **Independent contractor with its own establishment:** the files give no
  contractor test beyond the Art. 2 / Art. 5 definition; if the facts fail
  "management or supervision for a wage" the arrangement is outside the Law
  on the definition, but any further criteria are `[no rule in ksa files —
  verify]`, and a non-national still needs a permit held by the entity under
  whose responsibility he works (Art. 33).
- **Unclear / close call:** the definition cuts both ways — state which
  element is the problem.

For another populated code, use that code's category rows; where a category
the user proposes has no row, say so and tag `[no rule in <code> files —
verify]`.

**When the applicable code is `usa`:**

- **Employee (W-2):** Facts support employment under one or more applicable
  tests for the relevant purpose(s).
- **Independent Contractor (1099):** Facts support IC status under all
  applicable tests for the relevant purpose(s).
- **Temp via staffing agency:** Worker will be on the agency's payroll;
  company is a client — co-employment risk exists if company exercises
  day-to-day control. Research the applicable joint-employer standard if
  relevant.
- **Vendor/SOW:** Company-to-company engagement; worker is employed by the
  vendor entity — cleanest structure if facts support it.
- **Unclear / close call:** Facts cut both ways under one or more tests —
  state which test is the problem and why.

If tests give different answers for different purposes (e.g., defensible as
IC for federal tax but fails a state wage/hour test), say so explicitly and
name the controlling purpose and jurisdiction. For a populated code, state
the exposure per purpose track from the files — for `ksa`: Labor Law
entitlements from day one (Art. 5, Reg. Art. 1), social-insurance
back-contributions and Art. 59 penalties (per contributor, five-year
look-back; do not compute back-contributions without the contributory-wage
rows and the hire-date test in `social-insurance-law.md`), the
nationalisation count (`saudization-nitaqat.md`), and the Art. 39 / Art. 30 /
Art. 229 bis exposure for non-nationals and supplied workers
(`platform-obligations.md`). Any number carries the computed-number tag with
its inputs; a missing input means no number.

**The gap analysis**

This is the most important output. Compare the intended structure against what
the facts actually support:

```
Intended structure: [what they said they want]
What the facts suggest: [what the researched tests say this actually is]

Gaps — where the arrangement doesn't match the intended structure:
🔴 [Factor]: [What they described] conflicts with [intended classification]
   because [specific researched test language + cite]. This is a significant
   misclassification risk if the engagement proceeds as described.
🟡 [Factor]: [What they described] is a weaker point under [test]. Not
   disqualifying alone, but combined with other factors increases risk.
✅ [Factor]: Supports [intended classification]. No issue.
```

**Escalation trigger**

Escalate per `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/CLAUDE.md` if any of the following, or any team-specific
triggers recorded in that config:
- The jurisdiction uses a strict test and the proposed work is core to the
  company's business — do not proceed without counsel review.
- Prior misclassification settlement or audit noted in the config — heightened
  scrutiny applies.
- Worker will supervise employees or have significant budget authority.
- Engagement expected to exceed 12 months with no clear project endpoint.
- Any contested prong where the outcome changes the classification.

### Step 5 — Output

> **Research-connector pre-flight.** Before emitting the analysis, check whether the research source for the applicable code is reachable — for `usa`, Westlaw, CourtListener, or any firm-configured research MCP; for a populated non-`usa` code, the portal named in `references/jurisdictions/<code>/MANIFEST.md` → `research_tool` (for `ksa`, `scripts/fetch-law.py --portal boe --index` or a `curl` of the portal home). Collect this into the reviewer note per CLAUDE.md `## Outputs`: if no connector returns results in Step 2 (or none is configured at run time), record it in the **Sources:** line of the reviewer note — for `usa`, e.g., `not connected — cites from training knowledge; the highest-fabrication pinpoints in classification analyses are ABC-test codifications, state carve-out subsections (e.g., CA Lab. Code §§ 2775/2776/2783), element counts in B2B exemptions, and purpose-specific test selection — spot-check those first`; for a populated code, `portal: <host> ✓ reachable | unreachable` plus the files applied. End the note with `Jurisdiction: <codes applied>; files: <list>; portal fetched: yes/no; unpopulated codes: <list or none>`. Per-citation tags remain inline. Do not emit a standalone banner above the output.

> **Jurisdiction assumption.** This analysis applies the tests operative in the jurisdiction code(s) resolved in Step 0. Classification rules vary materially by jurisdiction, and for `usa` the test that governs for one purpose (e.g., federal payroll tax) often differs from the test that governs another (e.g., state wage/hour). If the work will be performed in a jurisdiction not analyzed here, or if a new purpose is added later, this analysis may not apply as written. An unpopulated code is a stop, not a caveat (Step 0).

> **Header, disclaimer and language.** Prepend the work-product header, then — for every code other than `usa` — the jurisdiction disclaimer line from the profile (`## Outputs`). Apply the bilingual house style in `## Outputs`: when the profile's output language is bilingual, or the analysis contains counterparty-facing text (contract terms), add the authoritative-language rendering of the bottom line, the gap-analysis table and every counterparty-facing passage. Money in `[currency]`; dates on the manifest's calendar.

```markdown
[WORK-PRODUCT HEADER — per plugin config ## Outputs — differs by role; see `## Who's using this`]
[JURISDICTION DISCLAIMER LINE — per plugin config ## Outputs, for every code other than `usa`]

## Worker Classification Analysis
**Proposed arrangement:** [what they described]
**Jurisdiction:** [code(s) from Step 0; state for `usa`]
**Purpose(s):** [`usa`: federal tax / state wage-hour / UI / WC / benefits. Populated code: the file's purpose tracks — for `ksa`: Labor Law coverage / social insurance / nationalisation count / permit and licensed activity]
**Tests applied:** [`usa`: list, each with pinpoint cite and currency date. Populated code: the definition rows with their `[settled — last confirmed …]` tags]

---

### Bottom line

[Can you proceed / Need to fix X first / Stop — one-sentence why]

---

### Classification

**Closest classification:** [`usa`: Employee / IC / Temp via agency / Vendor-SOW / Unclear. Populated code: the file's category — for `ksa`: Labor Law worker (fixed-term / indefinite / part-time / flexible-work / temporary) / trainee / seconded via Ajeer / supplied by licensed labour-services company / visiting specialist ≤ 2 months / contractor with own establishment `[no rule in ksa files — verify]` / Unclear]
[Authoritative-language rendering of the bottom line and this line when the profile asks]

[One paragraph summary of why — test results in plain language, tied to the
cited sources.]

---

### Test results

#### [Test name — per research]
Purpose: [...] | Source: [...] | Currency: [...]
[Scored table from Step 3]
**Result:** [Employee-leaning / IC-leaning / Fails prong X / Mixed]

#### [Additional researched tests — repeat the block]

---

### Gap analysis

[Flags as structured in Step 4 — 🔴 significant risks, 🟡 weaker points,
✅ clean factors]

---

### Escalation

[None needed | Escalate to [name] before proceeding — [reason]]

---

### Next steps

[If IC viable: "Proceed — ensure the written agreement reflects the terms that
support IC status under the researched test."]
[If gaps exist: "Address the following before using IC structure: [list]"]
[If agency/vendor is cleaner: "Consider restructuring as [agency/SOW] — here's
why it's cleaner for this fact pattern."]
[If escalation needed: "Do not proceed until counsel reviews the [specific
issue]."]
[If employee confirmed: "Classification confirmed as employee (`usa`: W-2;
populated code: a worker under the file's contract types) — run
`/employment-legal:hiring-review` to review the offer letter or contract,
restrictive covenants, and jurisdiction-specific requirements (permit,
documentation, social-insurance registration)."]
[If IC confirmed: "Classification confirmed as independent contractor — no
offer letter review needed. Ensure the written agreement reflects IC-supporting
terms before the engagement starts."]
[If agency/vendor: "Engagement should be structured through [agency/vendor
entity] — coordinate with them on worker agreement. No `/hiring-review` needed."]
```

## Consequential-action gate (classify a worker)

**Before producing a "Proceed as IC / employee / agency / vendor" final recommendation:** Read `## Who's using this` in `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/CLAUDE.md`. If the Role is **Non-lawyer**:

> Classifying a worker has legal consequences — misclassification exposes the company to back wages, taxes, benefits, penalties, and private-action risk, and in several jurisdictions is strict-liability (`usa` states; for a populated code the exposure rows of its files). Have you reviewed this classification call with an attorney? If yes, proceed. If no, here's a brief to bring to them:
>
> - The arrangement (work, control, economics, structure) as described
> - Jurisdiction and which tests were applied
> - Test-by-test results with cites and currency
> - Gap analysis (🔴 / 🟡 / ✅) with the weak prongs called out
> - Open questions and what's unresolved
> - What could go wrong (the misclassification theory this arrangement most likely fails on; prior-audit/settlement overlay if any)
> - What to ask the attorney (is IC viable here; would restructuring through an agency or vendor remove the risk; what contract terms do we need to support the classification)
>
> If you need to find an attorney, solicitor, barrister, or other authorised legal professional: contact your professional regulator (state bar in the US, SRA/Bar Standards Board in England & Wales, Law Society in Scotland/NI/Ireland/Canada/Australia, or your jurisdiction's equivalent) for a referral service.

Do not produce a final "IC viable" / "use this classification" output past this gate without an explicit yes. A marked-DRAFT analysis for attorney review is fine.

---

## What this skill does NOT do

- Analyze an existing relationship retroactively — this is prospective only.
- Draft the contractor agreement or SOW.
- Advise on remediation if misclassification has already occurred.
- State the law for any jurisdiction on its own — every test, factor, and
  carve-out must come from verified current research (`usa`) or from a
  cited row of the applicable jurisdiction file.
- Invent a factor list, presumption or contractor test where the
  jurisdiction file carries none — it says so and tags the gap.
- Substitute for outside counsel on close calls — strict-test jurisdictions,
  contested prongs, and prior-audit situations should always get a human
  review before the engagement starts.

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs`. Customize the options to what this skill just produced — the five default branches (draft the X, escalate, get more facts, watch and wait, something else) are a starting point, not a lock-in. The tree is the output; the lawyer picks.

