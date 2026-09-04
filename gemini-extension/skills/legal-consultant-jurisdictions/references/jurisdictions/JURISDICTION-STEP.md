# Jurisdiction resolution step (canonical wording)

Every skill in the in-scope plugins carries this step in its own text, as "Step 0", before it reads a document or applies a table. This file is the single source for the wording; a skill copies it rather than pointing at it, because the upstream design rule is that the skill must behave correctly on its own and the plugin `CLAUDE.md` guardrails are only the net. When this wording changes, update the skills that carry it (`grep -rl "Step 0: Resolve the applicable jurisdiction"`).

---

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

---

## Provenance tags added by the fork

These join the upstream tag vocabulary; the upstream tags keep their meaning.

- `[BOE — Arabic]` — the article text was read from laws.boe.gov.sa in Arabic this session or on the date shown in the reference file's `[settled — last confirmed …]` tag.
- `[BOE — official English]` — read from the Bureau of Experts translation.
- `[authority — <name>]` — read from the issuing authority's published document (HRSD, MoC, MISA, CMA, GAC, SDAIA, MoJ, SCCA, GOSI).
- `[settled — last confirmed YYYY-MM-DD]` — upstream tag, used in the reference files with the date the primary text was read.
- `[model knowledge — verify]` — upstream tag; the default for anything not read from a source.
- `[not populated — no rule applied]` — a finding for a jurisdiction whose folder is not populated; no analysis was done for it.
- `[no rule in <code> files — verify]` — the jurisdiction is populated but the files do not cover the point; nothing was supplied from memory.
- `[ksa]`, `[gbr]`, `[fra]`, `[che]`, `[usa]` — jurisdiction labels on findings in multi-jurisdiction matters.

## Computed numbers

Any number a skill computes from a jurisdiction file (end-of-service award, compensation for invalid termination, notice date, penalty reduction, filing deadline) carries the tag on the number itself, in this form: `SAR 41,250 [computed — labor-law.md Arts. 84-85, settled 2026-09-04; inputs: last wage SAR 15,000, service 4y 6m, employer termination]`. The inputs travel with the number so a reviewer can recompute it. If any input is missing, ask; do not assume.
