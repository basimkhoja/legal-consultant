---
name: deal-team-summary
description: >
  Aggregate diligence findings into a deal team briefing at the right altitude
  for the audience — exec summary for leadership, working summary for the team.
  Use when user says "brief the deal team", "what's the state of diligence",
  "summarize findings for [audience]", "deal update", or on the briefing cadence.
---

# Deal Team Summary

## Matter context

**Matter context.** Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗` (the default for in-house users), skip the rest of this paragraph — skills use practice-level context and the matter machinery is invisible. If enabled and there is no active matter, ask: "Which matter is this for? Run `/corporate-legal:matter-workspace switch <slug>` or say `practice-level`." Load the active matter's `matter.md` for matter-specific context and overrides. Write outputs to the matter folder at `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/matters/<matter-slug>/`. Never read another matter's files unless `Cross-matter context` is `on`.

---

## Purpose

The deal lead doesn't read 200 findings. They read: what's material, what changed since last brief, what needs a decision. This skill compresses the diligence output to the right level for the reader.

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

- `references/jurisdictions/<code>/MANIFEST.md` — currency, disclaimer, authoritative language (Step 0; the summary).
- No instrument file is applied by this skill: it carries the jurisdiction labels (`[ksa]`, `[usa]`, …), the source tags and the severities that `diligence-issue-extraction` attached, and never re-analyses a finding against a file.

---

## Load context

- `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/CLAUDE.md` → Deal team briefing (cadence, format, what the business reads)
- `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/deals/[code]/deal-context.md` → deal lead, timeline
- Current findings from diligence-issue-extraction output

## Audience tiers

Per `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/CLAUDE.md` — what the business reads vs. what's for the file. Default tiers:

| Audience | Gets | Doesn't get |
|---|---|---|
| **Board / exec sponsor** | Top 3-5 material issues, price/structure impact, decision items | Category detail, green findings, process |
| **Deal lead** | All reds, all yellows, progress, decision items, next steps | Green finding detail |
| **Working team** | Everything — full findings, status by category, gaps | Nothing withheld |

Ask which tier if not obvious.

## The summary

Every tier: prepend the work-product header, then, for a non-`usa` code, the jurisdiction disclaimer line from the profile `## Jurisdiction` / the manifest, and apply the bilingual house-style rule from the plugin `CLAUDE.md` `## Outputs` — when the profile's output language is bilingual, the bottom line (Status and Material findings headlines) and the findings tables (open issues, progress) are rendered in the authoritative language as well as English, using the manifest's spellings; analysis paragraphs stay in English unless the profile says authoritative language only. Every amount (price adjustment, indemnity ask, exposure) is stated in the profile currency, with the original currency in parentheses where the finding carried one. Every finding keeps the jurisdiction label (`[ksa]`, `[usa]`, …) and the source tag it arrived with from `diligence-issue-extraction`; findings for an unpopulated code stay marked `[not populated — no rule applied]` and are never merged into a populated code's paragraph.

### Exec tier

```markdown
[WORK-PRODUCT HEADER — per plugin config ## Outputs — differs by role; see `## Who's using this`]
[JURISDICTION DISCLAIMER LINE — from the profile ## Jurisdiction, for a non-usa code]

> This brief aggregates privileged diligence findings and inherits the sources' privilege and confidentiality status. Distribution beyond the privilege circle (including to broader business teams) can waive privilege — confirm the distribution list matches the privilege circle before sending.

# [Deal code] — Diligence Brief — [date]

**Status:** [On track / Issues identified / Material findings]
**Coverage:** [X]% of VDR reviewed
**Jurisdiction:** [codes applied]; files: [list]; portal fetched: yes/no; unpopulated codes: [list or none]

## Material findings

[3-5 max. One paragraph each, labelled with its jurisdiction code. What it is, why it matters to the deal, what
we're doing about it.]

## Decisions needed

- [ ] [Specific decision — price adjustment, indemnity ask, walk-away trigger, in [currency]]
  — [who decides] — [by when, on the manifest calendar]

## Since last brief

[What changed. New findings, findings resolved, coverage progress.]
```

### Deal lead tier

Same as above plus:

```markdown
## All open issues by category

### 🔴 Red
[Finding title + one-line — link to full finding for detail]

### 🟡 Yellow
[same]

## Progress

| Category | Code | Docs reviewed | Coverage | Reds | Yellows | Status |
|---|---|---|---|---|---|---|
| [name — house or jurisdiction overlay category] | [ksa] | [N/M] | [%] | [N] | [N] | [Complete / In progress / Blocked] |

## Gaps and follow-ups

- [Supplemental request items outstanding]
- [Questions to management]

## Next 72 hours

[What's getting reviewed, what briefings are scheduled]
```

### Working team tier

Full finding detail. Same structure as above but every finding gets its full house-format block, not a one-liner.

## Deltas

If this is a recurring brief (per `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/CLAUDE.md` cadence), lead with what changed:

- New findings since last brief
- Findings upgraded/downgraded in severity
- Findings resolved (consent obtained, issue clarified away)
- Coverage movement

Deal leads care more about movement than state. "Still 12 yellows" is less useful than "2 new yellows, 3 resolved."

## Handoffs

- **From diligence-issue-extraction:** This skill reads the accumulated findings.
- **To closing-checklist:** Any "decision needed" items that resolve into closing conditions go on the checklist.

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs`. Customize the options to what this skill just produced — the five default branches (draft the X, escalate, get more facts, watch and wait, something else) are a starting point, not a lock-in. The tree is the output; the lawyer picks.

## What this skill does not do

- It doesn't make the materiality call — it reports the calls that were made at extraction time.
- It doesn't decide what the deal team does about a finding — it surfaces the decision.
- It doesn't distribute the brief — drafts it, human sends.
