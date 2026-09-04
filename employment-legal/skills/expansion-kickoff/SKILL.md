---
name: expansion-kickoff
description: >
  Kick off international expansion planning for a new country — gathers intake,
  runs EOR vs. entity framing, drafts cross-functional questions, surfaces
  country-specific flags, and creates a persistent tracker. Use when someone
  says "we're hiring in [country]", "expansion to [country]", or "first hire
  in [country]".
argument-hint: "[country name]"
---

# /expansion-kickoff

Starts an international expansion project for a new country — gathers intake,
runs EOR vs. entity framing, drafts cross-functional questions, surfaces
country-specific flags, and creates a persistent tracker.

## Instructions

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

For this skill the "matter" in item 2 is the expansion: the target country given as the argument (or asked for) is the matter's jurisdiction, alongside the HQ country from the company profile. If the target resolves to a code whose manifest says `populated: no`, stop with the Step 0 wording before running the workflow; the outside-counsel briefing is the only substantive path and nothing in it is pre-filled from model knowledge.

**Jurisdiction files this skill loads:** the list under "Jurisdiction files this skill loads" in the `international-expansion` reference skill (`MANIFEST.md`, `INDEX.md`, `playbook-defaults.md` Labor table, `labor-law.md` Arts. 32-40, 51-53, 74-77, 84-88, 98-117, `saudization-nitaqat.md`, `platform-obligations.md`, `social-insurance-law.md`, `personal-data-protection-law.md`, `investment-law.md`, `companies-law.md`, `labor-dispute-route.md`), read through that skill's Steps 2 and 4.

1. Load `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/CLAUDE.md` → jurisdictional footprint, escalation table.
2. Load the `international-expansion` reference skill and run the full workflow. When the target folder is populated, run its populated-folder branch (pre-filled briefing, jurisdiction rows in the EOR-vs-entity table, each item with the file's tag and a "currency check" label); otherwise run the upstream outside-counsel path.
3. If a tracker file already exists for this country (`${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/expansion-[slug].yaml`),
   flag it: "An expansion tracker for [country] already exists. Use
   `/employment-legal:expansion-update [country]` to update it, or confirm
   you want to start over."
4. Create `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/expansion-[slug].yaml` on completion.
5. Output: prepend the work-product header, then, for a target that is not `usa`, the jurisdiction disclaimer line from the practice profile `## Outputs`; apply the bilingual house-style rule from the plugin CLAUDE.md `## Outputs` where the profile asks for it; amounts in `[currency]`, dates against the calendar in the manifest; record `Jurisdiction: <codes>; files: <list>; portal fetched: yes/no; unpopulated codes: <list or none>` in the reviewer note.

## Examples

```
/employment-legal:expansion-kickoff Germany
```
(Example only. `Germany` resolves through Step 0 to `deu`, which has no folder today: the skill runs the outside-counsel path with nothing pre-filled. A populated target such as `ksa` runs the populated-folder branch.)

```
/employment-legal:expansion-kickoff
(skill will ask which country)
```

> Detailed EOR vs. entity framework, cross-functional questions, briefing
> templates, and tracker schema live in the `international-expansion`
> reference skill — load it before doing substantive work.
