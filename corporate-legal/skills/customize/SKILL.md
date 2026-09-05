---
name: customize
description: >
  Guided customization of your corporate practice profile — change one thing
  without re-running the whole cold-start interview. Adjust risk posture,
  escalation contacts, jurisdiction and output language, active modules (M&A /
  Board / Listed Company / Entity Management), materiality thresholds,
  disclosure schedule format, consent precedents, or matter workspace paths.
  Use when the user says "change my [thing]", "update my profile", "edit my
  config", or "customize".
argument-hint: "[section name, or describe what you want to change]"
---

# /customize

## When this runs

The user typed `/corporate-legal:customize`. They want to change something
in their practice profile — a risk posture, an escalation contact, a module
toggle, an output format — without re-running the whole cold-start interview
and without hand-editing YAML.

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

**Jurisdiction files this skill loads:**

- `references/jurisdictions/REGISTRY.md` and `references/jurisdictions/<code>/MANIFEST.md` — when the user changes the primary jurisdiction or footprint (step 4 below): the new code must be populated or `usa`; an unpopulated code is refused.
- `references/jurisdictions/<code>/playbook-defaults.md` — when the user changes a position the cold-start interview took from that file, show the file's row beside the current value (step 4).

---

## What to do

1. **Read the config.** Read
   `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/CLAUDE.md`
   (and `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/company-profile.md` one
   level up). If the plugin config does not exist or still contains
   `[PLACEHOLDER]` values, say:

   > You haven't run setup yet. Run `/corporate-legal:cold-start-interview`
   > first — customize is for adjusting a profile you already have.

2. **Show the customizable map.** List what's in the profile, grouped, with a
   one-line summary of the current value:

   - **Company / who you are** — name, industry, jurisdictions, stage, listed
     vs. private (regulator and exchange), practice setting *(shared across
     all 12 plugins — changes flow through `company-profile.md`)*; the
     registration lines of `## Company profile` (commercial registration
     number and registry, legal form under the local companies law,
     foreign-investment registration, statutory registrations, UBO filing)
   - **Jurisdiction** (`## Jurisdiction`) — primary code, footprint, output
     language (English / bilingual / authoritative language only), calendar,
     currency, portal, local counsel, and which playbook defaults from
     `references/jurisdictions/<code>/playbook-defaults.md` were accepted or
     changed. Every skill reads this section first.
   - **Active modules** — which of M&A, Board & Secretary, Listed Company
     (config heading `## Public Company`, flag `--module public`), Entity
     Management are on. Turning a module on/off changes which skills
     prompt for setup.
   - **Risk posture** — conservative / middle / aggressive, what each means
     for diligence materiality and disclosure schedule scope
   - **People** — deal team, board secretary, entity management owner,
     escalation chain
   - **M&A module** — materiality thresholds (contract value, headcount,
     revenue — in the profile currency), jurisdiction diligence categories
     accepted, data room platforms trusted, AI bulk-review trust level
     (Luminance / Kira), deal-team briefing cadence
   - **Board & Secretary module** — house consent format (written consent or
     resolution by circulation, e-signature position), signatory
     preferences, committee structure
   - **Listed Company module** — regulator and exchange; reporting calendar
     and disclosure controls (10-K/10-Q review timing under `usa`; the
     `corporate-governance-regulations.md` items — board cadence, audit
     committee, related-party thresholds, CMA notifications — under `ksa`)
   - **Entity Management module** — entity table (local type, jurisdiction
     code, registry number), filing agent, jurisdiction codes, filing
     calendar from `references/jurisdictions/<code>/filing-calendar.md`
   - **Workflow** — matter workspaces (deal rooms), closing checklist
     location, VDR watcher cadence
   - **Integrations** — Box / Intralinks / Datasite / filing agent / Slack
     status, fallbacks; the primary-source portal's reachability

3. **Ask what they want to change.**

   > What would you like to adjust? Pick a section, or describe the change in
   > your own words.

4. **Make the change.** Show the current value, ask for the new value, explain
   what changes downstream, confirm, write it to the config.

   Examples:
   - *Materiality threshold [currency] 250K → [currency] 500K:* "`/diligence-issue-extraction`
     and `/material-contract-schedule` will now treat [currency] 500K as the cutoff.
     Existing findings stay as logged; re-run if you want the new threshold
     applied retroactively."
   - *Turning on the Listed Company module:* "I'll prompt you for your
     regulator's items next time you run anything in that area."
   - *Changing the primary jurisdiction or adding a footprint code:* read
     `references/jurisdictions/REGISTRY.md` and the code's `MANIFEST.md`
     first. If the code is not populated (and not `usa`): "Jurisdiction
     `<code>` is registered but not populated — I won't set it as primary,
     because every skill would stop or run against the wrong rules. I can
     add it to the footprint, where findings for it are marked
     `[not populated — no rule applied]`, or you can populate the folder
     first." If populated: rewrite the manifest-derived lines (authoritative
     language, calendar, currency, portal, disclaimer) from the new manifest,
     then re-offer the rows of the new code's `playbook-defaults.md` the
     way the cold-start interview does (Part 1J), and say: "Every threshold
     is now in [currency] and every date rule follows the [code] calendar;
     the entity table rows keep their own codes."
   - *Changing the output language to bilingual:* "Every skill will now add
     the authoritative-language rendering of the bottom line, findings table
     and counterparty-facing text, per `## Outputs`."
   - *Changing a position the interview took from `playbook-defaults.md`:*
     show the file's row and its citation beside the current value; record
     the change on the `**Jurisdiction playbook defaults accepted:**` line
     so the deviation is visible.
   - *AI bulk-review trust "check every row" → "spot-check 10%":* "`/ai-tool-
     handoff` will QA a 10% sample rather than every extraction."

5. **For shared-profile changes** (company name, industry, jurisdictions,
   practice setting, stage): write to
   `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/company-profile.md` and note:

   > This change affects all 12 plugins — any plugin that reads your
   > jurisdiction footprint now sees [new value].

6. **Close.**

   > Done. Your next output will reflect the change. Anything else? You can
   > run `/corporate-legal:customize` anytime.

## Guardrails

- **Never delete a section.** If the user wants to "remove" something, set it
  to `[Not configured]` and explain what that means for the plugin's behavior.
- **Flag internal inconsistency.** If the change would make the profile
  inconsistent (e.g., Listed Company module off + "SEC counsel" or "CMA
  counsel" in escalation; aggressive risk posture + a [currency] 25K
  materiality threshold; a threshold in a currency other than the
  `## Jurisdiction` currency; an entity row whose code is not in the
  footprint), flag the tension.
- **Never write a jurisdiction rule from memory.** A change to a position
  that rests on a `references/jurisdictions/<code>/` row is shown against
  that row; a position the files do not cover is written as the user's own
  with `[user provided]`, never as a rule.
- **Flag guardrail degradation.** The `[review]` flag, source attribution
  tags on retrieved documents, and `[verify]` tags on cited authorities are
  load-bearing — explain the trade-off before removing.
- **One change at a time.** Don't re-ask the whole interview.
