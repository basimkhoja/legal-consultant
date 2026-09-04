---
name: customize
description: >
  Guided customization of your employment practice profile — change one thing
  without re-running the whole cold-start interview. Adjust jurisdiction
  codes and footprint, output language, local counsel, jurisdiction playbook
  defaults, risk posture, escalation contacts, hiring review rules,
  termination review rules, handbook positions, investigation preferences,
  or matter workspace paths. Use when the user says "change my [thing]",
  "add a jurisdiction", "update my profile", "edit my config", or "customize".
argument-hint: "[section name, or describe what you want to change]"
---

# /customize

## When this runs

The user typed `/employment-legal:customize`. They want to change something
in their practice profile — a jurisdiction, a risk posture, an escalation
contact, a handbook position — without re-running the whole cold-start
interview and without hand-editing YAML.

## What to do

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

For this skill, Step 0 is short in practice: the profile's `## Jurisdiction` section is what customize edits. If it is missing or still a placeholder, route to `/employment-legal:cold-start-interview` (the stop text in item 1) rather than editing around it. The remaining items apply when a change is made to a jurisdiction-derived field (items 3 and 6 for a code change, item 7 for output-language and disclaimer changes).

**Jurisdiction files this skill loads:**
- `references/jurisdictions/REGISTRY.md` — codes and populated status, for any change to the primary code or footprint.
- `references/jurisdictions/<code>/MANIFEST.md` — `populated`, `authoritative_language`, `calendar`, `currency`, `disclaimer`, `output_language_rule`, for the fields that follow a code change.
- `references/jurisdictions/<code>/playbook-defaults.md` — the Labor table, for re-accepting or editing defaults and for the consistency check in the guardrails.

### Steps

1. **Read the config.** Read
   `~/.claude/plugins/config/claude-for-legal/employment-legal/CLAUDE.md`
   (and `~/.claude/plugins/config/claude-for-legal/company-profile.md` one
   level up). If the plugin config does not exist or still contains
   `[PLACEHOLDER]` values, say:

   > You haven't run setup yet. Run `/employment-legal:cold-start-interview`
   > first — customize is for adjusting a profile you already have.

2. **Show the customizable map.** List what's in the profile, grouped, with a
   one-line summary of the current value:

   - **Company / who you are** — name, industry, practice setting, jurisdictions
     *(shared across all 12 plugins — changes flow through
     `company-profile.md`)*
   - **Jurisdiction** — primary jurisdiction code, footprint codes, output
     language (English / bilingual), calendar and currency (from the
     manifest), local counsel for escalation, and the jurisdiction playbook
     defaults accepted at cold-start (re-accept or edit any row of
     `references/jurisdictions/<code>/playbook-defaults.md`, Labor table).
   - **Jurisdictional footprint** — jurisdiction codes and sub-jurisdictions
     where employees work (state / canton / nation, or the nationality,
     sector and entity-type segments a code without territorial
     sub-jurisdictions uses), single- vs. multi-jurisdiction, headcount by
     nationality, nationalisation band, work-permit sponsorship, contract
     types, registrations, and any upcoming expansion. This drives
     jurisdiction-supplement logic.
   - **Risk posture** — conservative / middle / aggressive, what each means
     for flagging termination risk, restrictive covenant enforceability, and
     leave accommodation
   - **People** — HR partners, people team lead, outside counsel, escalation
     chain, investigation sponsor
   - **Hiring review** — offer letter / employment-contract template,
     restrictive covenants posture, background check vendor, contract type
     and notice period (at-will language is a `usa`-only item under this
     heading)
   - **Termination review** — end-of-service and severance framework
     (statutory entitlement from the applicable jurisdiction file — for
     `ksa`, `labor-law.md` Arts. 84-87 — plus any top-up; for `usa`, the
     severance formula), release / settlement language, final-settlement
     timing per jurisdiction (from the jurisdiction file), notice periods by
     contract type, high-risk flags
   - **Handbook** — handbook / work-regulations file path, jurisdiction
     supplements approach and axis, regulatory approval status, language
     versions, review cadence
   - **Investigation preferences** — privileged labeling, interview protocol,
     audience-specific summary templates
   - **Workflow** — matter workspaces, leave tracker cadence, expansion
     project paths
   - **Integrations** — HRIS / Slack / document storage status, fallbacks

3. **Ask what they want to change.**

   > What would you like to adjust? Pick a section, or describe the change in
   > your own words.

4. **Make the change.** Show the current value, ask for the new value, explain
   what changes downstream, confirm, write it to the config.

   **Jurisdiction changes (stop rule lives here).** When the change is to
   the primary code or adds a footprint code: look the code up in
   `references/jurisdictions/REGISTRY.md` and read
   `references/jurisdictions/<code>/MANIFEST.md`.
   - Changing the **primary** code to one whose `populated` is not `yes`
     (and is not `usa`) is refused: "Jurisdiction `<code>` (<name>) is
     registered but not populated: no reference files exist for it, so every
     skill in this plugin would stop on your first matter. I will not set
     an unpopulated primary jurisdiction. Options: (1) choose `usa`, (2)
     choose a populated code — currently: [rows of REGISTRY.md whose
     Populated column is `yes`], (3) populate
     `references/jurisdictions/<code>/` first and re-run." Wait.
   - Adding an unpopulated **footprint** code is allowed; write it with
     `[not populated — no rule applied]` and say that matters in it go to
     local counsel.
   - A primary-code change re-derives the manifest-driven fields
     (Authoritative language, Calendar, Currency, Primary-source portal,
     disclaimer) and resets "Jurisdiction playbook defaults accepted" to
     `not reviewed for <new code>`; offer to walk the new code's
     `playbook-defaults.md` Labor table now, row by row with its Basis, or
     route to `/employment-legal:cold-start-interview --redo`.
   - **Output language** (English / bilingual per the manifest's
     `output_language_rule`) and **local counsel** are single-field edits;
     explain that bilingual switches on the authoritative-language rendering
     of the bottom line, findings table and counterparty-facing text in every
     skill (plugin CLAUDE.md `## Outputs`).
   - **Re-accept playbook defaults:** show each Labor-table row of
     `references/jurisdictions/<code>/playbook-defaults.md` with its Basis;
     never state a default whose Basis is missing; an edit below a statutory
     floor named in the Basis is written with `[review — below the statutory
     floor in <file> <article>; the file's row prevails in every skill]`.

   Examples:
   - *Adding a populated jurisdiction code to the footprint:*
     "`/wage-hour-qa` and `/termination-review` will start loading
     `references/jurisdictions/<code>/` for matters in it. `/handbook-updates`
     will prompt for a `<code>` supplement on the axis that code uses."
   - *Adding Washington to the jurisdictional footprint (`usa` example):*
     "`/wage-hour-qa` and `/termination-review` will start applying WA rules.
     `/handbook-updates` will prompt for a WA supplement. `/hiring-review`
     will now flag non-compete attempts in WA (unenforceable) `[model
     knowledge — verify]`."
   - *Severance framework 2 weeks/year → 4 weeks/year (`usa` example):*
     "`/termination-review` will use the new baseline in severance
     calculations."
   - *End-of-service top-up "none" → "statutory + 0.25 month per year"
     (populated-code example, `ksa`):* "`/termination-review` computes the
     statutory award from `labor-law.md` Arts. 84-87 and adds the top-up as a
     separate line; the statutory figure cannot be reduced by this field."
   - *Risk posture middle → conservative:* "I'll flag more terminations for
     escalation, recommend more protective release language, and be stricter
     on restrictive covenants."

5. **For shared-profile changes** (company name, industry, jurisdictions,
   practice setting, stage): write to
   `~/.claude/plugins/config/claude-for-legal/company-profile.md` and note:

   > This change affects all 12 plugins — any plugin that reads your
   > jurisdiction footprint now sees [new value].

6. **Close.**

   > Done. Your next output will reflect the change. Anything else? You can
   > run `/employment-legal:customize` anytime.

## Guardrails

- **Never delete a section.** If the user wants to "remove" a jurisdiction,
  offer to mark it `[Not currently staffed — retain rules for re-entry]` and
  explain that going to `[Not configured]` will drop jurisdiction-specific
  flagging.
- **Flag internal inconsistency.** If the change would make the profile
  inconsistent (e.g., CA in the footprint + aggressive non-compete posture;
  or risk posture aggressive + "every termination goes to outside counsel"),
  flag the tension. For a populated code, the consistency rules come from
  `references/jurisdictions/<code>/playbook-defaults.md` (Labor table) and
  the instrument files it cites; e.g., for `ksa` a non-compete posture
  longer than two years conflicts with `labor-law.md` Art. 83, a notice
  period shorter than `labor-law.md` Art. 75, or an end-of-service formula
  below `labor-law.md` Arts. 84-87, conflicts with the statutory floor. Flag
  with the file and article; do not refuse, but write the `[review — below
  the statutory floor …]` tag described in step 4.
- **Flag guardrail degradation.** The pre-flight citation check, source
  attribution tags, and `[verify]` tags on cited statutes are load-bearing —
  do not remove. The `[review]` flag is load-bearing — explain the trade-off
  before adjusting.
- **One change at a time.** Don't re-ask the whole interview.
- **Output.** The rewritten profile is a configuration file and carries no
  header. If the user asks for the change written up as a deliverable (a
  memo on the new position), prepend the work-product header from the
  profile's `## Outputs`, then the jurisdiction disclaimer line from the
  profile for a non-`usa` primary code, and apply the bilingual house-style
  rule in the plugin CLAUDE.md `## Outputs` when Output language is
  bilingual.
