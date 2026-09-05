---
name: log-leave
description: >
  Add a new leave to the leave register with the minimum information needed to
  start tracking the statutory clocks of the applicable jurisdiction (for
  `usa`: designation, certification and exhaustion; for a populated code: the
  entitlement tiers, protection periods and scheduling clocks in its
  jurisdiction file). Use when an employee goes on leave and you want the
  tracker to watch the clocks from day one.
argument-hint: "[describe the leave — employee/role, type, jurisdiction, start date]"
---

# /log-leave

Adds a new leave entry to `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/leave-register.yaml` with the minimum
information needed to start tracking deadlines. Use when an employee goes on
leave and you want the tracker to watch the clocks from day one.

## Instructions

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

- `references/jurisdictions/<code>/MANIFEST.md` (calendar: weekend, public holidays, Hijri or Gregorian), `INDEX.md`, `playbook-defaults.md` Labor table (leave row).
- `references/jurisdictions/<code>/labor-law.md` — Art. 10 (calendar), Art. 82 (no termination for illness before the sick-leave periods are exhausted), Arts. 109-111 (annual leave: 21 days, 30 after five years; 30 days' notice; deferral 90 days; payout on leaving), Art. 112 (official holidays), Art. 113 (marriage, bereavement, paternity within seven days of birth), Art. 114 (Hajj), Art. 115 (exams), Art. 116 (unpaid leave; suspension beyond 20 days), Art. 117 (sick leave: 30 days full, 60 at three quarters, 30 unpaid, in a year from the first sick day), Art. 118, Art. 137 (work-injury absence — not sick leave), Arts. 151-155 (maternity 12 weeks; six weeks after delivery compulsory; medical care; nursing hour; no dismissal during pregnancy or maternity leave up to 180 days' absence), Art. 160 (iddah: four months and ten days, or 15 days).
- `references/jurisdictions/<code>/labor-law-implementing-regulations.md` — Annex 5 cl. 8 (annual-leave day basis), Annex 1 Arts. 33-44 (leave articles of the model regulations), Reg. Art. 22 bis (compensatory leave: 60-day scheduling, 30-day cap, payout), Reg. Art. 24 (holiday overlap rules), Reg. Art. 25 (day-21 suspension of unpaid leave), Reg. Art. 26 (sick-leave certificate; sick days during annual leave), Reg. Art. 31 (nursing breaks for 24 months), Annex 1 Art. 50 (maternity).
- `references/jurisdictions/<code>/social-insurance-law.md` — Arts. 30-33 (work-injury allowances paid by the fund, reporting deadlines `[model knowledge — verify]`), Arts. 41-42 (maternity compensation; interaction with employer-paid leave is an open question in that file).
- `references/jurisdictions/<code>/occupational-safety.md` — Art. 137 (work-injury absence: 60 days full wage then 75%; one-year total-disability rule), Art. 82.
- `references/jurisdictions/<code>/labor-dispute-route.md` — the "Computed dates" rules (calendar election under Annex 5 cl. 14.6, otherwise Hijri per Art. 10).

1. Read `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/CLAUDE.md` → `## Jurisdiction`, jurisdiction table and Systems section.

2. Ask all of the following in a single prompt — do not drip them one at a time. The leave-type list and the clock questions depend on the code resolved in Step 0:

   > A few quick questions to set up leave tracking:
   >
   > - Employee name or role (anonymized is fine)
   > - Where do they work? (Jurisdiction code and, for `usa`, the state; for a populated code, the sub-jurisdiction only if its file varies by it — this determines which rules apply)
   > - Leave type — `usa`: FMLA / state leave (which state) / USERRA / ADA accommodation. Populated code: one of the regimes in the jurisdiction file; for `ksa`: annual (`labor-law.md` Arts. 109-111) / sick (Art. 117) / maternity (Art. 151) / paternity, marriage or bereavement (Art. 113) / Hajj (Art. 114) / exam (Art. 115) / iddah (Art. 160) / unpaid (Art. 116) / compensatory leave in lieu of overtime (Reg. Art. 22 bis) / work-injury absence (Art. 137 — tracked as its own regime, not sick leave) / nursing breaks (Art. 154, Reg. Art. 31)
   > - Leave start date (and, for `ksa` sick leave, the date of the first sick day in the current sick-leave year — the Art. 117 year runs from that day, not from 1 January)
   > - Is this intermittent leave?
   > - Expected return date (if known — leave blank if not)
   > - `usa` only: has the designation notice been sent? If yes, when? Has medical certification been requested? If yes, when?
   > - Populated code, for `ksa`: is the illness proven by a certificate from the establishment's doctor or an approved medical body (Art. 117; Reg. Art. 26)? For maternity: the expected delivery date on a certified medical certificate and the actual delivery date once known (Art. 151). For marriage, bereavement, paternity, Hajj or exam leave: the event date and the supporting document (Arts. 113-115). For unpaid leave: the agreed length (Art. 116). For compensatory leave: the overtime date and hours and the agreed leave amount (Reg. Art. 22 bis).

3. Look up the entitlement:
   - `usa`: using the jurisdiction table in `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/CLAUDE.md`, look up the applicable leave entitlement (hours/weeks) for this leave type in this jurisdiction.
   - Populated code: from the jurisdiction file rows, cited by article with the row's tag. For `ksa`: annual 21 days (30 after five consecutive years), on the day basis the contract form uses (Annex 5 cl. 8.1 working days; the Law's wording is calendar days — state which basis the register uses and tag `[model knowledge — verify]` per the Art. 109 row); sick 30 days full pay, 60 at three-quarters, 30 unpaid, in a year from the first sick day (Art. 117); maternity 12 weeks at full pay, six weeks after delivery compulsory, at most four weeks before the expected date, one unpaid month extension, one paid month for a sick or disabled child (Art. 151); marriage 5 days, death of spouse, ascendant or descendant 5 days, sibling 3 days, paternity 3 days within seven days of birth (Art. 113); Hajj 10-15 days once, after two consecutive years (Art. 114); exam leave for the actual exam days (Art. 115); iddah four months and ten days, or 15 days for a non-Muslim worker (Art. 160); unpaid leave as agreed, contract suspended beyond 20 days (Art. 116, Reg. Art. 25); compensatory leave at not less than 1.5 hours per overtime hour, capped at 30 days a year (Reg. Art. 22 bis); work-injury absence at full wage for 60 days then 75% (Art. 137 via `occupational-safety.md`, only where the fund does not pay — `social-insurance-law.md` Art. 33). **Row missing:** if the leave type has no row in the file, say so, tag `[no rule in <code> files — verify]`, and log it with `entitlement: unknown` rather than inventing one. **Unpopulated code:** the Step 0 stop; do not log against another jurisdiction's entitlements.

4. Compute the first upcoming deadline based on the information provided, on the calendar in the manifest (for a populated code) — never on a Saturday/Sunday weekend or US federal holidays:
   - **When the applicable code is `usa`** (figures are upstream defaults, `[model knowledge — verify]` against the researched rule the agent cites):
     - Designation not yet sent → deadline is 5 business days from leave start
     - Med cert requested but not received → deadline is 15 days from request date
     - Both sent and received → next deadline is at 75% exhaustion
   - **When the applicable code is populated (non-`usa`)** — the clocks are the file's rows; each computed date carries the computed-date tag with its inputs (e.g. `2026-11-02 [computed — labor-law.md Art. 117, settled 2026-09-04; inputs: first sick day 2026-08-04, day 91]`). For `ksa`:
     - Sick leave: the tier transitions at day 31 (pay drops to three quarters), day 91 (unpaid) and day 121 (entitlement exhausted) of the sick-leave year, counted from the first sick day (Art. 117); the Art. 82 termination bar lifts only at exhaustion; the worker may append annual leave (Art. 82).
     - Maternity: the compulsory six weeks after delivery; the 12-week end date; the optional unpaid month; the Art. 155 protection against dismissal or warning of dismissal through pregnancy, maternity leave and related illness up to 180 days' absence a year.
     - Unpaid leave: day 21, when the contract is suspended and a fixed term is extended (Art. 116; Reg. Art. 25).
     - Compensatory leave: the 60-day scheduling window from the overtime date and the 30-day annual cap (Reg. Art. 22 bis).
     - Paternity: the seven-day window from the birth (Art. 113).
     - Annual leave: the 30-day notice of dates (Art. 109); the 90-day deferral limit after the entitlement year and the end of the following year with written consent (Art. 110); holiday days falling inside the leave extend it (Reg. Art. 24).
     - Iddah: four months and ten days from the date of death, extended unpaid to delivery if pregnant (Art. 160).
     - Work injury: day 61 (aid drops to 75%) and the one-year total-disability point (Art. 137); the fund's reporting deadline is `[model knowledge — verify]` (`social-insurance-law.md` Art. 33 row).
   - For another populated code, the clocks in that code's leave rows; where the file names none for the leave type, log `next_deadline: none in file` and tag `[no rule in <code> files — verify]`.

5. Write a new entry to `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/leave-register.yaml` using the leave register
   format from the leave-tracker agent (`jurisdiction_code`, `regime_code`, and the generic `clocks[]` list with name, owner, due date and source tag; the FMLA-shaped fields are filled only for `usa`). If the file doesn't exist, create it.

6. Confirm with a single line (add the authoritative-language rendering when the profile's output language is bilingual, per CLAUDE.md `## Outputs`):
   > "Logged. [Employee/Role] — [Leave type] — [Jurisdiction code] — started [date].
   > First deadline: [what it is and when, with its source row and tag]. Leave tracker will alert automatically."

## Examples

```
/employment-legal:log-leave
```

```
/employment-legal:log-leave
Sarah (Sr. Engineer, works in California) just started FMLA today for a
serious health condition. Intermittent. No designation sent yet.
```
*(a `usa` example)*

```
/employment-legal:log-leave
Site engineer (non-national) on the Riyadh contract started sick leave on
4 August on a certificate from the company clinic; first sick day this year.
Return date unknown.
```
*(an example under a populated code — `ksa`; the tracker computes the
Art. 117 tier dates and the Art. 82 bar from the first sick day)*
