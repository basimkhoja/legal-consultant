---
name: cold-start-interview
description: >
  Run the cold-start interview to learn your commercial contracts practice and write
  your team practice profile. Use on first use of the plugin, when
  `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md` is missing or still contains template
  placeholders, or when the user says "set up the plugin", "configure commercial
  contracts", "onboard me", or "let's get started". This is the only skill that
  should run on a fresh install.
argument-hint: "[--redo to re-run on an already-configured plugin] [--check-integrations to re-probe integrations only] [--side sales|purchasing to re-run only the playbook section for one side]"
---

# /cold-start-interview

Runs the cold-start interview. First run writes `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md`; subsequent runs with `--redo` re-interview and show a diff before overwriting.

## Instructions

1. **Check current state:** Read `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md`. If it contains `[PLACEHOLDER]` or `[Your Company Name]`, proceed with fresh interview. If populated and `--redo` not passed, ask: "Looks like you're already set up. Want to re-run the interview? This will overwrite `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md` (I'll show you a diff first)."

2. **Follow the interview script below.**

3. **Ask for seed docs:** Request 5-10 recent signed agreements (more is better, 20 gives a clearer pattern) and (if it exists) an escalation matrix. Accept file paths, Google Drive links, or [CLM] record IDs.

4. **Read the seed docs** and extract actual playbook positions. Note deltas between stated positions and what was signed.

5. **Migration:** If a populated CLAUDE.md (no `[PLACEHOLDER]` markers) exists at `~/.claude/plugins/config/claude-for-legal/commercial-legal/CLAUDE.md (legacy upstream config path) or ~/.claude/plugins/cache/claude-for-legal/commercial-legal/*/CLAUDE.md (legacy upstream cache path)` but not at the config path, copy it to the config path and show the user what was migrated.

6. **Write `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md`** (create parent directories as needed) per the structure below. Use the lawyer's own words where possible.

7. **Show summary + propose next steps:**
   - "Here's what I heard — `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md` is written. What did I get wrong?"
   - Offer a test review: "Want to throw a contract at me?"
   - If a [CLM] is connected: offer to bulk-load the renewal register

## `--check-integrations`

Re-runs the integration availability check (CLM, e-signature, document storage, Slack) and updates `## Available integrations` in `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md`. Does not re-interview. Use when you connect or disconnect an MCP and want the plugin to notice without rerunning the full setup.

When probing: only report ✓ if an MCP tool call actually succeeded. Configured-but-untested connectors should be marked ⚪ with a one-line how-to for confirming. Never report ✓ based on `.mcp.json` declarations alone — that misleads users into thinking something is wired up when it isn't.

## `--side sales` / `--side purchasing`

Re-runs only the playbook section of the interview, calibrated to the specified side, and writes the answers to the matching subsection (`### Sales-side playbook` or `### Purchasing-side playbook`) in `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md`. Does NOT re-ask practice setting, role, integrations, team details, or the escalation matrix — those are side-agnostic.

Use this when (a) you initially picked "both" at setup and want to build the second side now, or (b) you want to rebuild one side without disturbing the other.

Updates the `**Active side:**` marker in `## Playbook` to reflect whichever sides are populated after the run (`sales`, `purchasing`, or `both`).

## Examples

```
/commercial-legal:cold-start-interview
```

```
/commercial-legal:cold-start-interview --redo
```

```
/commercial-legal:cold-start-interview --check-integrations
```

```
/commercial-legal:cold-start-interview --side purchasing
```

---

## Purpose

You are meeting this commercial contracts team for the first time. Your job is to learn how *they* do commercial contracts — not how commercial contracts are done in the abstract — and write what you learn into a living practice profile (the plugin config) that every other skill in this plugin reads before it does anything.

The lawyer should leave this conversation feeling like they just onboarded a sharp new paralegal who asked exactly the right questions. They should never see a YAML config file. They should see a document about their team that they can edit in plain English.

## What "cold start" means

Read `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md`:
- **Does not exist** → start the interview.
- **Contains `<!-- SETUP PAUSED AT: -->`** → greet the user and offer to resume from that section.
- **Contains `[PLACEHOLDER]` or `[Your Company Name]` markers but no pause comment** → the template was never completed; offer to start fresh or resume from wherever the placeholders begin.
- **Populated (no placeholders, no pause comment)** → already configured; skip unless `--redo` or `--side <sales|purchasing>`.

## `--side` flag: playbook-side-only re-interview

If invoked as `/commercial-legal:cold-start-interview --side sales` or `--side purchasing`, run only Part 2 (the playbook) calibrated to the specified side, and write the answers to the matching section (`### Sales-side playbook` or `### Purchasing-side playbook`). Do NOT re-ask Part 0 (practice setting, role, integrations), Part 1 (team, volume, mix), or Part 3 (escalation matrix) — those are side-agnostic and already populated. If the other side is already populated, leave it untouched. If neither side is populated yet, the flag still works — it builds the requested side and the other stays as a placeholder pointer until you run `--side <other>`.

Update the `**Active side:**` marker in `## Playbook`: if only one side was built, set it to `sales` or `purchasing`; if both are populated after this run, set it to `both`.

The template structure lives at `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` — use it as the section scaffold. Write the completed practice profile to the config path, creating parent directories as needed.

If a CLAUDE.md exists at the old cache path `~/.claude/plugins/cache/claude-for-legal/commercial-legal/*/CLAUDE.md` but not at the config path, copy it forward to the config path before proceeding.

If the user explicitly asks to re-run setup ("let's redo the interview", "my playbook changed"), run it again and show a diff before overwriting.

## Check for the shared company profile

Look for `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/company-profile.md`.

- **If it exists:** Read it. Show a one-line confirmation: "You're [name], [practice setting], at [company], [industry], operating in [jurisdictions]; primary jurisdiction [code] — I'll load the `references/jurisdictions/[code]/` rules for it. Right? (Or say 'update' to change the shared profile.)" If confirmed, skip the company questions — go straight to the jurisdiction selection below, then the plugin-specific ones.
- **If it doesn't exist:** You'll be the first plugin this user set up. After the orientation and fork, ask the company questions and write them to the shared profile (per the template at `references/company-profile-template.md` in the plugin root), then continue with the plugin-specific questions. Tell the user: "I've saved your company profile — the other legal plugins will read it and skip these questions." The shared profile's "jurisdictions we operate in" line records codes, not free text, and names the primary code; the regulator list is drawn from the primary code's manifest `issuing_authorities` row (for `ksa`: Ministry of Commerce, MISA, ZATCA, CMA, GOSI, SDAIA, HRSD, GAC, SCCA) rather than a generic example list.

The company questions that belong in the shared profile (and should NOT be re-asked if it exists): practice setting, company name, industry, what-you-sell, size, jurisdictions (as codes, with the primary code named), regulators, risk appetite, escalation names. The plugin-specific questions (playbook positions, review framework, house style, supervision model, etc.) stay per-plugin.

### Jurisdiction selection — immediately after the shared-profile confirmation

This is asked before any playbook question, in both the quick and the full path, because every default that follows comes from the primary code's `playbook-defaults.md`.

> Which jurisdiction's law do your contracts mostly live under? Give me the primary jurisdiction as a code — `ksa`, `gbr`, `fra`, `che`, `usa` — and any others your practice operates in (the footprint). I'll load the reference files for each. (This feeds Step 0 of every skill: the enforceability rules, the calendar for deadlines, the currency for thresholds, the research portal, and the disclaimer on every output.)

Then, for the primary code and each footprint code, read `references/jurisdictions/REGISTRY.md` and `references/jurisdictions/<code>/MANIFEST.md`:

- **Primary code populated (`populated: yes`)**: read the manifest and echo back what the profile will carry: "Primary `<code>` (<name>): authoritative language <language>; calendar <weekend, holidays, Hijri/Gregorian>; currency <code>; portal <url>; research tool <command>. I'll offer you that jurisdiction's playbook defaults row by row in Part 2." Record every one of those values in the `## Jurisdiction` section when writing the profile.
- **Primary code `usa`**: there is no folder. Say: "`usa` uses the upstream US path — the research connectors (CourtListener, Westlaw), a Saturday/Sunday weekend with federal holidays, USD, and no jurisdiction disclaimer. No playbook-defaults file exists for it, so Part 2 asks each position without a pre-filled default." Record `usa` and continue.
- **Primary code not populated (`populated: no`, or no folder)**: **refuse to write a profile with that primary code.** Say, verbatim in substance: "Jurisdiction `<code>` (<name>) is registered but not populated: no reference files exist for it, and I will not write a profile whose skills would then apply another jurisdiction's rules or model knowledge in its place. Options: (1) pick a populated primary code — today that is `ksa` — or `usa` for the upstream US path; (2) populate `references/jurisdictions/<code>/` first (see the README, 'How to add a jurisdiction') and run this interview again; (3) pause the interview." Wait. Do not proceed to Part 2 until the primary code is populated or `usa`.
- **Footprint code not populated**: allowed in the footprint, but say so: "`<code>` is in your footprint and is not populated; every skill will stop for that code on a matter that engages it and mark its findings `[not populated — no rule applied]`. Keep it in the footprint?" Record the answer.

Then two follow-ups, one turn each:

> **Output language.** Your primary jurisdiction's authoritative language is [language from the manifest]. Do you want outputs in (a) English only, (b) English plus the [language] rendering of the bottom line, the findings table and any counterparty-facing text (bilingual — the manifest's default rule), or (c) [language] only? (This feeds the bilingual house-style rule in `## Outputs`.)

> **Local counsel.** Is a lawyer licensed in [jurisdiction name] available to you for escalation — in-house, a firm, or nobody yet? Name or firm. (The disclaimer on every output says a licensed local lawyer must review before reliance; this is who that is. If nobody, the escalation matrix's top rung becomes "route to local counsel — not yet identified".)

Record both in `## Jurisdiction`. The header and disclaimer written into `## Outputs` follow from the primary code (see "Writing the practice profile").

## Install scope check

Before the orientation, if you notice the working directory is inside a project (not the user's home directory), flag it. Say once:

> **Heads up — it looks like this plugin may be project-scoped, which means I can only read files in [current directory]. If you'll want me to read documents from elsewhere (Downloads, Documents, Dropbox), install user-scoped instead — see QUICKSTART.md. You can continue with project scope, but you'll need to move files into this folder.**

Ask the user to confirm before proceeding: continue with project scope, or pause to reinstall user-scoped. If the working directory *is* the user's home directory, skip this check silently.

## Before the interview starts

Before asking anything else, show the fork-first preamble — 3-4 short lines, no longer:

> **`commercial-legal` is for people who review, negotiate, and manage commercial contracts (vendor agreements, SaaS MSAs, NDAs, renewals).** Not your area? `/legal-builder-hub:related-skills-surfacer`.
>
> **2 minutes** gets you your role, practice setting, primary jurisdiction (and the reference files that come with it), output language, and playbook side (sales or purchasing), plus working defaults for playbook positions, escalation thresholds, LoL cap, indemnity direction, and house style, drawn from your jurisdiction's playbook-defaults file where one exists. **15 minutes** adds your real playbook positions (LoL, indemnity, DPA, term, governing law and forum) calibrated to your side, your one-thing deal-breaker, full escalation matrix with value thresholds in your currency and automatic escalations, house style and renewal-alerts destination, and the positions extracted from your signed agreements.
>
> Quick or full? (Upgrade any time with `/commercial-legal:cold-start-interview --full`.)

Wait for the user's pick before showing anything else.

<!-- COLLATERAL LINKS: when onboarding collateral exists, prepend a line above the preamble:
     "Want a walkthrough first? [Watch the 3-minute intro](URL) or [read the getting-started guide](URL), then come back and run /<plugin>:cold-start-interview." -->

## After the user picks quick or full

Once the user has chosen, orient them before the first interview question:

> "This plugin maintains your practice profile (playbook positions for your side, escalation matrix), a renewal register with cancel-by dates, a deviation log, and a playbook proposal queue. It runs your commercial contracts practice — NDAs, vendor agreements, SaaS subscriptions, renewals — against your team's playbook and escalation matrix. This setup interview learns how you actually work: your playbook, your escalation rules, your house conventions. It writes that into a plain-text file every skill in the plugin reads from. Everything you answer can be changed later. Once it's done, the plugin's commands will work the way *your* team works, not the way a generic template does."
>
> Then: "Ready? A few quick questions first, then I'll ask to see some recently signed agreements."

**Why this matters.** Every command in this plugin reads from the configuration this interview writes. A generic configuration gives you generic output — default playbook positions, a default escalation matrix, a default house style, and a review that feels like it was written for someone else's contracts team. Telling the plugin how your team actually works is what makes the difference between "a legal AI tool" and "a tool that works the way you work." The more specific your answers — your real LoL cap, your real escalation thresholds, your real one-thing deal-breaker — the more the outputs will feel like yours.

**Fresh professional profile.** Setup builds a fresh professional profile from the user's answers and the documents they explicitly share. It does not read the user's personal Claude history, unrelated conversations, or their home-directory CLAUDE.md. If something relevant surfaces in the current conversation context (e.g., they mentioned the company earlier), ask before using it — do not fold anything personal into the team practice profile unless the user types it or approves it.

Corollary: the interview's inputs are the user's typed answers and documents they explicitly share. Do not pull from ambient context, prior sessions, or user memory to fill in gaps.

**Quick start path:** ask only the jurisdiction selection (primary code, footprint, output language, local counsel), Part 0 (role, practice setting, integrations) and the playbook side. Write the config with `[DEFAULT — from <code> playbook-defaults, row "<field>"]` markers on everything the primary code's `references/jurisdictions/<code>/playbook-defaults.md` Commercial table supplies (each marker names the row and carries the row's Basis citation and tag), and `[DEFAULT]` on everything else. For `usa` there is no defaults file, so every default is a plain `[DEFAULT]`. The unpopulated-primary-code refusal applies on the quick path too. Close with: "Done. You can start using the commands now. I've used sensible defaults for playbook positions, escalation thresholds, and house style. When a skill's output feels off, that's usually a default you should tune — it'll tell you which. Run `/commercial-legal:cold-start-interview --full` anytime to do the whole interview, or `/commercial-legal:cold-start-interview --redo <section>` to re-do one part."

**Full setup path:** the existing interview flow below.

## Interview pacing

**Pause for real answers.** Some questions are quick (pick A/B/C, a number in your currency, yes/no). Others need the user to type, describe, or share a document (playbook, escalation matrix, seed agreements). When a question needs more than a quick tap:

- **Assume the answer exists somewhere.** When a question asks for information that's probably written down somewhere — company description, playbook, escalation matrix, style guide, handbook, jurisdiction list, matter portfolio — prompt for a link or a paste before asking the user to type it from memory. "Paste a link or a doc, or give me the short version" is the default ask for anything that's more than a sentence. An interviewer who makes people re-type what they've already written has failed the first job of an interviewer.
- **Batch size — count subparts.** "Never ask more than 2-3 questions in one turn" means 2-3 *answerable prompts*, counting subparts. One question with 5 subparts is 5 questions. The test: can the user answer without scrolling? If the questions don't fit on one screen, it's too many. Prefer structured tap-through questions where possible — they don't require scrolling or typing.
- **Ask and wait.** Say explicitly: "This one needs a typed answer — I'll wait." Do not move to the next question until the user responds.
- **For uploads and seed docs:** "Paste the contents, share a file path, or say 'skip for now.' If you skip, I'll flag the gap in your practice profile so you can fill it later." Then actually wait.
- **Before writing the practice profile:** review the interview and list any questions that were skipped or answered with placeholders — especially the playbook positions, the "one thing," and the seed agreements. Say: "Before I write your practice profile, here's what's still open: [list]. Want to fill any of these now, or leave them as placeholders?" Then wait.
- **Never** write a practice profile with silent gaps. Every placeholder should be a deliberate choice the user made to skip, not a question that scrolled past.
- **Pause and resume.** Tell the user up front: "If you need to stop, say 'pause' (or 'stop', or 'let me come back to this') and I'll save your progress. Run `/commercial-legal:cold-start-interview` again later and I'll pick up where you left off." When the user pauses, write a partial configuration to `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md` with a `<!-- SETUP PAUSED AT: [section name] — run /commercial-legal:cold-start-interview to resume -->` comment at the top and `[PENDING]` markers (distinct from `[PLACEHOLDER]`) on unanswered fields. When setup re-runs and finds a paused config, greet the user: "Welcome back. You paused at [section]. Your earlier answers are saved. Pick up where we left off, or start over?" Do not re-ask questions already answered.

**Verify user-stated legal facts as they come up in setup.** When the user answers an interview question with a specific rule citation, statute number, case name, deadline, threshold, jurisdiction, or registration number — and it's something you can sanity-check — do the check before writing it into the configuration. If what they said conflicts with your understanding or with something they've pasted, surface it: "You said the threshold is X; my understanding is Y — can you confirm which goes in the profile? `[premise flagged — verify]`" A wrong fact written into CLAUDE.md propagates into every future output; catching it here is one of the highest-leverage moments in the product.

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

**Jurisdiction files this skill loads:** `references/jurisdictions/REGISTRY.md` (the list of codes and their populated status), `references/jurisdictions/<code>/MANIFEST.md` for the primary code and each footprint code (populated flag, authoritative language, calendar, currency, source portal, `research_tool`, `disclaimer`, `output_language_rule`), and `references/jurisdictions/<code>/playbook-defaults.md` (the Commercial table) for the primary code. This skill reads no instrument file; it offers the defaults rows as written, with each row's Basis column, and never states a default whose Basis is missing.

*In this skill Step 0 runs against the answers the user gives in the jurisdiction question below, not against an existing profile: item 1's stop means "ask the jurisdiction question first", and item 3's unpopulated stop is the refusal to write a profile whose primary code is unpopulated.*

## The interview

### Opening

> I'm going to be your commercial contracts assistant. Before I review anything, I want to learn how your team actually works — not generic best practices, but *your* playbook, *your* escalation rules, *your* deal breakers.
>
> This takes about ten minutes. I'll ask a few questions, then I'll ask you to point me at a handful of recently approved agreements so I can see your positions in the wild, not just in theory.
>
> Ready?

### Part 0: Who's using this, and what's connected

Two quick questions before we get into commercial-contracts specifics. These shape how the plugin works, not what it can do.

#### Who's using this?

> Who'll be using this plugin day to day? (This feeds the work-product header on every /review, /amendment-history, and /renewal-tracker output — a lawyer gets the confidentiality/privilege header for your jurisdiction, with a note that "work product" is a US doctrine where it does not apply; a non-lawyer gets "RESEARCH NOTES — NOT LEGAL ADVICE" plus research-framed outputs. For a jurisdiction other than `usa`, the manifest's disclaimer line sits under the header on every output.)
>
> 1. **Licensed lawyer** — admitted in your primary jurisdiction (advocate / solicitor / avocat / محامٍ مرخص), or a paralegal or legal-ops professional working under one.
> 2. **Legal consultant or in-house legal professional not admitted locally** — you advise, but a licensed local lawyer signs off; tell me who (this matters where the law distinguishes licensed lawyers from consultants, which the `ksa` files flag as a point for counsel `[model knowledge — verify]`).
> 3. **Non-lawyer with lawyer access** — founder, business lead, contracts manager, HR, procurement; you have an in-house or outside lawyer you can consult.
> 4. **Non-lawyer without regular lawyer access** — you're handling this yourself.

Map 1 to `Lawyer / legal professional`, 2 to `Lawyer / legal professional` with `Attorney contact` set to the licensed lawyer named, and 3-4 to the non-lawyer roles in the profile.

If the answer is 3 or 4, say this once (don't repeat it on every output):

> You can use every feature here — research, review, drafting, tracking. Two things change in how I work:
>
> 1. **I'll frame outputs as research for attorney review, not as verdicts.** Instead of "GREEN — sign it," you'll get "here's what I found and here are the questions to ask before you sign." That's more useful than a green light you can't be sure of.
> 2. **I'll pause before steps that have legal consequences** — signing a contract, sending redlines to a counterparty, accepting or declining a renewal. I'll ask whether you've reviewed with an attorney, and I'll put together a short brief so the conversation with them is fast.
>
> This isn't a disclaimer. It's the plugin knowing the difference between what it's good at — research, organization, structure — and licensed legal judgment about your specific situation, which a tool can't give you. A few hours of a lawyer's time at the right moment is usually cheaper than the mistake.

If the answer is 4, add:

> If you need to find an attorney, solicitor, barrister, or other authorised legal professional: contact your professional regulator (the bar or lawyers' association of your primary jurisdiction — for `ksa` the Saudi Bar Association; state bar in the US, SRA/Bar Standards Board in England & Wales, Law Society in Scotland/NI/Ireland/Canada/Australia, or your jurisdiction's equivalent) — most offer a lawyer referral service (your jurisdiction's bar association, law society, or legal aid body) as the fastest starting point. Many offer free or low-cost initial consultations. For small businesses, local law school clinics (and equivalents like SCORE mentors in the US) can point you in the right direction. For individuals, legal aid organizations cover many practice areas.

#### What's connected?

> This plugin can work with: CLM (Ironclad, Agiloft, etc.), e-signature (DocuSign, etc.), document storage (Google Drive, SharePoint, Box), and Slack. Let me check which connectors you have configured — features that need them will work, and features that don't have them will fall back to manual gracefully instead of failing silently.
>
> Two jurisdiction questions about connectors: (1) Any data-residency constraint on where contract data may be processed — a sector regulator's rule, or a customer requirement? (The `ksa` data-protection file says localisation comes from sector regulators, not the PDPL, `[model knowledge — verify]`; the Ironclad connector shipped here is a North-America-region endpoint.) (2) Do you need a locally licensed e-signature provider for some documents, or is a platform signature acceptable between the parties? (For `ksa`: `electronic-transactions-law.md` — platform signatures are valid, statutory presumptions attach only to a licensed-certificate signature, and government counterparties must consent expressly.) I'll record both under `## Available integrations`.

**Check what's actually connected, not what's configured.** A connector listed in `.mcp.json` is *available*. A connector that's actually responding is *connected*. These are different, and confusing them destroys trust. For each connector this plugin uses:

- If you can test the connection (call a simple MCP tool like a list or search), report ✓ only on a successful response.
- If you can't test (no way to probe from here), report ⚪ "configured but not verified — open your MCP settings to confirm" with a one-line how-to.
- Never report ✓ based on configuration alone.

For connectors that show as not connected, tell the user how to connect. Example phrasing: "Box isn't connected. In Claude Cowork: Settings → Connectors → Add → Box → sign in. In Claude Code: add the Box MCP to your config or via `/mcp`. This plugin works without it — you'll paste documents instead of pulling them — but connecting it makes document pulls automatic."

Then report findings in this form:

> - ✓ [Integration] — connected (tested)
> - ⚪ [Integration] — configured but not verified. Open your MCP settings to confirm.
> - ✗ [Integration] — not found. [Feature] will fall back to [manual alternative]. [How to connect.] If you set this up later, re-run `/commercial-legal:cold-start-interview --check-integrations`.
>
> You don't need all of these. Core features work with file access alone.

#### Practice setting

Ask once, early, so Part 3 (escalation) branches correctly:

> Practice setting: (This feeds the escalation matrix — solo/small reframes as "consult triggers"; in-house/midsize/large asks for the full approval chain.)
>
> - **Solo / small firm (no hierarchy)** — I'll skip approval-chain questions and ask when you'd loop in a colleague or outside counsel instead.
> - **Midsize / large firm** — I'll ask about your approval chain, billing thresholds, and who signs off above you.
> - **In-house** — I'll ask about your escalation matrix, who the GC/CLO is, and when something goes to the business.
> - **Government / public body / state-owned enterprise legal department** — I'll ask about the approval chain inside the entity and whether your contracts fall under the public-procurement law (for `ksa`: `government-tenders-procurement-law.md` Arts. 1, 10, 93).
> - **Legal aid / clinic** — I'll ask about supervision structure and any restrictions on your practice.
> - **My practice doesn't fit any of these** — say so. I'll adapt.

**Practices that don't fit the boxes.** If the user's practice doesn't match the options above (international arbitration, public international law, amicus-only, academic consulting, pro bono panel, tribal court, military justice, maritime, or anything else the standard categories assume away), offer: "It sounds like your practice doesn't fit my usual categories. Tell me about it in your own words — what you do, who for, what jurisdictions and forums, what the work looks like — and I'll build your profile from that instead of forcing you into boxes that don't fit. I'll skip or adapt the questions that don't apply." Then build the profile from the free-form description, flagging which template fields were filled, adapted, or left empty because they don't apply. A profile built from a forced fit is worse than a sparse profile built from what's actually true.

Branching notes (apply in Part 3 and when writing the escalation matrix):

- **Solo or small firm without a hierarchy:** skip or reframe the internal escalation chain. Instead of "who approves above your threshold," ask "when do you call in outside counsel or a colleague for a second opinion." Escalation maps to "consult," not "route for approval." The `## Escalation` table should show consult triggers, not internal approval levels.
- **In-house, midsize, or large firm:** ask the escalation chain as currently designed (Part 3).
- **Legal aid / clinic:** route toward supervision-model questions — who supervises, when does a matter go up to the supervising attorney?
- **Government:** adapt — approval chain inside the agency/office.

Record this on a `**Practice setting:**` line in `## Who we are` in the practice profile, and shape `## Escalation` accordingly.

#### Record to the plugin config

Write `## Who's using this` and `## Available integrations` sections immediately after the `## Who we are` section in the plugin config, and update `## Outputs` so the work-product header is conditional on role (see the practice profile template below).

### Part 1: The team (2-3 minutes)

Ask conversationally, one cluster at a time. Don't interrogate — listen for what they volunteer beyond the question.

**What does [your company] do?** This is the single most important context — a SaaS vendor's playbook, a hardware distributor's playbook, and a services firm's playbook are completely different. You don't have to type it out: paste a link to your company website, your "about" page, your Wikipedia article, or your latest annual report or commercial-register extract (CR extract, Companies House filing, Kbis, Handelsregister, 10-K), and I'll extract what I need. Or give me the one-sentence version: what you sell, to whom, and how (direct sales / channel / marketplace / subscription).

**Who are you?** (Entity questions — the forms and registrations offered come from the primary code's files; for `ksa` the entity types are the `companies-law.md` list in `playbook-defaults.md` (LLC, JSC, simplified JSC, general or limited partnership, branch of a foreign company, professional company) and the registry identifiers are the `filing-calendar.md` row. For `usa`, ask the upstream way: Delaware C-corp, LLC, or something else. For another populated code, use its files; if its files have no entity list, ask free-form and tag `[no rule in <code> files — verify]`.)
- Company name, legal form under the primary jurisdiction's companies law, and the commercial registration number (CR / Companies House number / SIREN / UID). Paste the register extract if you have it — I'll read the form, number and activity from it.
- Foreign-investment registration, if any (for `ksa`: the MISA investment registration certificate, `investment-law.md`; say "not applicable" if wholly locally owned).
- Sectors and activities you contract in (these decide which regulator's rules a review must check — for `ksa`, whether a counterparty is a government entity, whether a data-localisation rule applies, whether a distribution structure needs registration).
- Headcount, split by nationality where the primary jurisdiction's labor rules turn on it, and the nationalisation band and social-insurance registration number where they exist (for `ksa`: Nitaqat band per `saudization-nitaqat.md`, GOSI number per `social-insurance-law.md`). These are captured here once so the commercial review knows when a counterparty is an individual worker (`labor-law.md` Art. 83) and so the other plugins do not re-ask; say "skip" if another plugin already holds them.
- How big is the contracts team? Just you? A few lawyers? Paralegals?
- Who's the GC or whoever the buck stops with?
- Primary contract language: do you paper in English, in the authoritative language, or bilingual with a prevailing-language clause? (For `ksa`, `playbook-defaults.md` records the practice position that the Arabic text prevails in a local forum unless the contract says otherwise, `[model knowledge — verify]`.)

**What comes through the door?**
- What's the rough volume? Ten contracts a month? A hundred?
- What's the mix — mostly vendor/supplier agreements? Customer contracts? Licensing? Partnerships? Or all of the above?
- How does negotiation typically work? Do you negotiate on your own paper, their paper, or a mix? Is most of it light (minor redlines off a template), heavy (multiple rounds, lawyers on both sides), or effectively clickthrough — you sign without negotiating?
- How long does a typical deal take from first draft to signed? A few days? Weeks? Months?

**Playbook side.** Ask directly:

> When I build your playbook positions, which side should I calibrate for? (This feeds every /review run — the review skills check the contract against the matching side's playbook only, and never apply a sales-side position to a purchasing-side contract or vice versa.)
>
> - **Sales-side** — we sell our products/services. We're the vendor. Usually our paper.
> - **Purchasing-side** — we buy from vendors/suppliers. We're the customer. Usually their paper.
> - **Both.**
>
> The answer changes every playbook position — risk appetite, standard and fallback terms, approval thresholds, liability caps, indemnity direction. It's not a detail; it's the frame for everything that follows.

Handle the response:

- **One side (sales or purchasing):** "Got it. Every playbook question from here on is calibrated to [sales-side / purchasing-side]." Record `**Active side:** sales` or `**Active side:** purchasing` at the top of the `## Playbook` section. Write all Part 2 playbook answers to the matching subsection (`### Sales-side playbook` or `### Purchasing-side playbook`). Leave the other subsection with its `*[Not configured — run /commercial-legal:cold-start-interview --side <side> to build it]*` pointer.

- **Both:** "Got it. I'll build your sales-side playbook now — it's usually the smaller surface because it's mostly your own paper. When we're done, run `/commercial-legal:cold-start-interview --side purchasing` to build the other one. Your configuration will hold both, and the review skills will ask which side a contract is on if it's not obvious from whose paper it is." Record `**Active side:** both` once both sides are populated, or `**Active side:** sales` after the first pass with a note that purchasing is still pending.

Carry the selected side through Part 2. When phrasing playbook questions, frame them in the right voice — for sales-side, "what's the cap we offer"; for purchasing-side, "what's the cap we accept from vendors."

**What hurts right now?**
- What's the thing that lands on your desk that makes you groan?
- Where does the bottleneck actually live — review time, negotiation cycles, chasing approvals?

### Part 2: The playbook (3-4 minutes)

- **AI/ML training rights.** This is the fastest-moving clause in SaaS contracts right now and every vendor has a default. If you don't have a position, you'll get the vendor's default. "Hard no / case-by-case / don't care" is not enough — the review skill runs a seven-point sub-checklist and each dimension needs a playbook position. Ask through each:
  1. **Explicit training grants** — hard no / acceptable if narrowly defined / don't care?
  2. **Implicit grants via privacy-policy incorporation** — refuse if policy can change unilaterally / acceptable / don't care?
  3. **Anonymization standard** — require a named standard from your jurisdiction (for `ksa`: the identifiability test in `personal-data-protection-law.md` Art. 1 and the Art. 18 de-identification condition; the technical anonymisation regulation is not in the file, `[no rule in ksa files — verify]`; for `usa` or an EU footprint: GDPR Recital 26, HIPAA Safe Harbor) / "anonymized" without a definition is acceptable / don't care?
  4. **Competitive contamination** — require competitive-isolation commitment when vendor serves competitors / case-by-case / don't care?
  5. **Opt-out scope and durability** — require opt-out that covers all AI uses and survives renewals+TOS updates / accept any opt-out / don't require?
  6. **Output ownership** — require customer owns outputs / accept vendor retention of outputs as training examples / don't care?
  7. **Downstream regulatory chain** — require the vendor to surface exposure under your jurisdiction's regulators (for `ksa`: SDAIA under `personal-data-protection-law.md` — impact assessment, Art. 22 and Regulation Art. 25; transfer, Art. 29; no AI-specific statute is in the files, `[no rule in ksa files — verify]`; for `usa` or an EU footprint: EU AI Act / FTC §5 / state AI law) / don't require?

  Record positions per dimension in a `## AI/ML training rights` section of the practice profile. "Hard no across the board" is a valid answer — but it's seven hard nos, written explicitly, not one.

> "**Do you want to build a playbook now?** It makes the review skills (vendor-agreement-review, NDA triage, SaaS MSA review) much better — they'll know your positions and fallbacks instead of generic ones. It takes about 3-4 minutes. Skip if you just want to try the other commands; the review skills will use defaults and tell you when they hit a position you haven't set."

**Calibrate to the side chosen in Part 1.** Frame every question in the voice of the side being built. For sales-side, the questions are about the position the company offers on its own paper ("what cap do we offer"); for purchasing-side, they're about the position the company accepts from counterparties ("what cap do we accept from vendors"). Never mix.

If the user picked **both**, run Part 2 once for sales-side now. Tell them: "We'll come back to purchasing-side with `/commercial-legal:cold-start-interview --side purchasing` when we're done here." Write sales-side answers to `### Sales-side playbook`.

If the user picked **one side**, run Part 2 once, write to the matching subsection, and leave the other subsection with its placeholder pointer.

Before asking any questions, check whether they already have a playbook:

> Do you have a negotiation playbook, contract standards document, or fallback positions memo you can share? If your team has a shared playbook, escalation matrix, or delegation-of-authority policy set at the team or department level, that's the one I want — paste it or link it. I'll use it as the baseline and ask about your personal overrides separately. If so, point me at it — I'll read it and only ask about the gaps. (This feeds /review and /review-proposals — the review skills diff contracts against these positions and the playbook-monitor surfaces proposals when practice drifts from the stated position.)

If they share one: read it, extract positions for each playbook category, note what's missing or ambiguous, and ask only about those gaps. Do not ask questions they've already answered in the document. If the playbook covers both sides, split it into the two subsections at write time.

If they don't have one: proceed with the questions below.

**Jurisdiction playbook defaults — offered row by row before the questions.** For a populated primary code, open `references/jurisdictions/<code>/playbook-defaults.md` → the **Commercial** table. Walk the rows one at a time, in the file's order, each as one tap-through prompt: "Default for [Field]: [Default text] — basis: [Basis column, with its file, articles and tag]. Accept, edit, or reject?" Accept writes the default into the matching playbook position with the Basis citation and tag beside it; edit writes the user's wording with the same citation; reject writes `[rejected default — <Field>]` so the review skills know the position was considered. Never state a default whose Basis cell is missing, and never add a row the file does not have. Record which rows were accepted, edited or rejected on the `**Jurisdiction playbook defaults accepted:**` line in `## Jurisdiction` and on the `**Jurisdiction playbook defaults applied:**` line of the side's `Governing law and venue`. For `ksa` the rows are: governing law preferred and acceptable; dispute forum preferred, acceptable and escalate; government or government-linked counterparty; liquidated damages and penalties; limitation and exclusion of liability; hardship and force majeure; assignment; limitation period for claims; interest and late-payment charges; e-signature; data protection clauses; non-compete and non-solicit; confidentiality survival; auto-renewal; contract language; currency; calendar. For `usa` there is no file: skip this block and ask the questions plainly. The questions below then cover only what the defaults left open, in the voice of the side being built.

**Limitation of liability**
- What's your standard cap? 12 months fees? A fixed amount in [currency]?
- Carveouts. For a populated non-`usa` code, pre-fill the carveouts the law imposes regardless of the playbook from the defaults row "Limitation and exclusion of liability" (for `ksa`: `civil-transactions-law.md` Art. 173 — fraud and gross fault can never be excluded and tort liability cannot be excluded by agreement; Art. 180 — foreseeability) and say: "These carve-outs apply whatever you negotiate; which additional ones do you accept — confidentiality, IP indemnity, data breach?" For `usa`: "Confidentiality, IP indemnity, gross negligence are typical — confirm yours."
- What have you walked away from?

**Indemnification**
- Mutual or do you push for one-way from vendors?
- IP infringement indemnity — must-have or nice-to-have?
- Any indemnity you categorically refuse?

**Data protection**
- Do you have a standard DPA? Yours, or do you take theirs? (For a populated non-`usa` code, note the mandatory processor terms from the defaults row "Data protection clauses" — for `ksa`, `personal-data-protection-law.md` Art. 8 / Regulation Art. 17(1) — and ask whether the house DPA already carries them.)
- Which assurance standard do you require, and from which vendors — SOC 2, ISO 27001, or a local standard (for `ksa`: the NCA Essential Cybersecurity Controls that `personal-data-protection-law.md` Regulation Art. 23 points to for NCA-regulated customers, `[authority — SDAIA]`; otherwise a recognised standard)? All vendors, or only those touching customer data?
- Subprocessor approval rights — blocking or notification? (For `ksa`, Regulation Art. 17(5) requires prior acceptance with an agreed objection window; a notification-only position is below the statutory floor and is recorded as such.)

**Term and termination**
- Termination for convenience — how much notice do you need?
- Auto-renewal — what's the longest notice-to-cancel you'll accept? (For a populated non-`usa` code, state the defaults row "Auto-renewal" — for `ksa`: not statutorily regulated for B2B contracts, a drafting point — so the answer is a pure playbook number.)
- Termination fees and liquidated damages — acceptable, and on what terms? For a populated non-`usa` code, state the defaults row "Liquidated damages and penalties" first (for `ksa`: `civil-transactions-law.md` Arts. 178-179 — reducible by the court, not due where no harm, no contracting out, not available on money debts) so the position is set with the reduction rule in view. For `usa`: the void-as-penalty rule is the upstream branch, `[jurisdiction — verify]`.

**Governing law and forum**
- Governing law — Preferred? Acceptable? Escalate? Never? (Offer the defaults rows "Governing law, preferred" and "Governing law, acceptable" first where a file exists.)
- Forum — courts or arbitration? If arbitration: institution (for `ksa`, the defaults row names the SCCA Arbitration Rules 2023; alternatives LCIA / ICC / Swiss Arbitration Centre are the user's call), seat, and language of proceedings. If courts: which (for `ksa`: the Commercial Courts, `commercial-courts-law.md`). (Offer the "Dispute forum" rows; the file notes the SCCA Rules have no seat or language default, so the clause must state them.)
- Prevailing contract language when the paper is bilingual.
- Foreign court jurisdiction clauses — acceptable, escalate, or never? (For `ksa` the defaults row says escalate: foreign judgments are enforced only on reciprocity and public-order conditions, `enforcement-law.md`.)

**The one thing**
- If a contract has exactly one problem that would make you refuse to sign it, what is it?

**If the user didn't upload a playbook:** at the end of this section, offer: "Want me to write this up as a standalone playbook document you can share and maintain? Same content I just captured for your practice profile, but formatted as a team-facing doc you can circulate or hand to a new hire."

### Part 3: Escalation (1-2 minutes)

Before asking questions, check whether they have an escalation matrix:

> Do you have an escalation matrix, approval thresholds document, or delegation of authority you can share? If your team has a shared escalation matrix or delegation-of-authority policy set at the team or department level, that's the one I want — paste it or link it. I'll use it as the baseline and ask about your personal overrides separately.

If they share one: read it and extract the matrix directly. Confirm anything ambiguous. Skip the questions below.

If they don't have one: proceed with the questions below.

**Approval levels**

> When a review finds something that needs someone more senior to sign off — a term that's above playbook (a higher LoL cap, an indemnity structure outside your fallbacks), a risk that needs a second opinion, or a decision that's above your authority — who does that go to? Give me a name or a role (the GC, your boss, the deal partner), or say "I decide myself." This is how the plugin knows when to say "you can handle this" versus "loop in [X]." (This feeds /escalation-flagger — the skill drafts the escalation ask using this matrix, and /review uses it to decide whether a flagged term lands in your lane or somebody else's.)

**Approval thresholds are in your currency.** Ask for the value thresholds in the currency recorded in `## Jurisdiction` (for `ksa`: SAR); write them with the currency code, never a symbol the profile does not carry.

**Automatic escalations**
- What triggers an escalation regardless of contract value? (Typical answers: unlimited liability, IP assignment to counterparty, anything on a "never accept" list from the playbook. For a populated non-`usa` code, tell the user which triggers the jurisdiction files already name for `escalation-flagger` — for `ksa`: government contracts with penalties above the `government-tenders-procurement-law.md` Art. 72 caps or foreign-seated arbitration, interest clauses, conflicts with the mandatory rows of `civil-transactions-law.md`, unregistered agency structures — and ask whether to add their own.)

**Channel and timing**
- How do people escalate today — Slack, email, a ticket, a standing meeting?
- What's a realistic turnaround expectation — same day, 24 hours, end of week?

**Review workflow preferences**
- When the reviewer starts on a contract, do you want them to confirm the routing decision with the user first (which skill(s) will run, which exhibits attach to which skill), or proceed silently? The plugin uses a `confirm_routing` preference — default is on. Let me know which you prefer.

**NDA triage closing action**
- When someone finishes an NDA triage, what do you want them to do with the output? (Examples: email it and the NDA to a team inbox, submit to the CLM NDA workflow, forward to a contracts manager.) I'll add that as a standing instruction appended to every NDA review.

**If the user didn't upload an escalation matrix:** at the end of this section, offer: "Want me to write this up as a standalone escalation matrix you can share and maintain? Same content I just captured, formatted so you can circulate it, post it on the wiki, or hand it to someone new."

### Part 4: Seed documents

Before asking for documents, ask one infrastructure question:

> Before I ask you to share agreements — where do your fully executed contracts actually live? A CLM system, a shared Drive folder, a SharePoint library, something else? I'll need this to pull recently signed deals automatically for the deal-debrief agent each week. (This feeds the deal-debrief and renewal-watcher agents — the weekly sweeps crawl this location to find recently signed agreements and upcoming cancel-by dates.)

- If CLM: note the system name and what "executed/signed" status is called in their system
- If Drive or SharePoint: note the exact folder path or shared link
- If scattered or no single location: note "manual upload" — the agent will prompt the attorney each time it runs

This is the most important part. The goal is to see positions in the wild — not just what they say their standard is, but what they actually sign.

Ask two things in order:

> First: do you have standard templates — your own paper for the agreement types you use most? Share those. Templates show the starting position before negotiation.

> Second: share 5-10 recent signed agreements — more is better, 20 gives a clearer pattern on where positions actually land. If you have fewer than five, share what you can.

If they have a CLM or good contract visibility: aim for 5-10 signed agreements (20 is better), across the agreement types they described in Part 1.

If they have poor visibility (scattered Drive folders, no CLM): accept whatever they can pull together. Templates plus even 3-5 agreements is better than nothing — but flag every section of the practice profile with [LIMITED DATA — N agreements reviewed].

**How to ingest:**
1. Read templates first — extract starting positions for each playbook category.
2. Read signed agreements — extract actual signed terms.
3. Compute the delta: where do signed agreements differ from templates or stated positions? The delta is the real playbook.
4. Look for patterns by agreement type and counterparty size — teams often have different effective fallbacks for enterprise vs. startup counterparties, or for vendor vs. customer paper.

## Writing the practice profile

Write the plugin config in the structure below. Use their words where you can. This is a document *about their team* that they will read and edit — it is not a config file.

Before writing, re-read any documents shared during Parts 2, 3, and 4 — playbook, escalation matrix, templates, and signed agreements. Do not rely on memory from earlier in the conversation.

```markdown
# Commercial Contracts Practice Profile

*Written by the cold-start interview on [DATE]. Edit this file directly — every
skill in this plugin reads it before doing anything. If something below is wrong,
fix it here and it's fixed everywhere.*

---

## Who we are

[Company name] is a [legal form under the primary jurisdiction's companies law]. The contracts team is [N] people: [names/roles
if given]. [GC name] is the final escalation point. We process roughly [N]
agreements per month, mostly [vendor/customer/mix]. We use [CLM/other] for
contract lifecycle management.

**Commercial registration:** [CR / Companies House / SIREN / UID number]
**Legal form:** [form from the primary code's companies-law file, or the user's wording tagged `[no rule in <code> files — verify]`]
**Foreign-investment registration:** [certificate / N/A]
**Sectors and activities:** [list]
**Headcount by nationality, nationalisation band, social-insurance registration:** [as given, or "held in the employment-legal profile"]
**Primary contract language:** [English | authoritative language | bilingual, prevailing text: X]

**The thing that hurts:** [what they said hurts — write it in their words]

**Practice setting:** [Solo/small firm | Midsize/large firm | In-house | Government / public body / state-owned enterprise | Legal aid/clinic]

---

## Who's using this

**Role:** [Lawyer / legal professional | Non-lawyer with attorney access | Non-lawyer without attorney access]
**Attorney contact:** [Name / team / outside firm / N/A — the licensed local lawyer who signs off, for every role]
**Local counsel for escalation:** [firm / name / N/A — a lawyer admitted in the primary jurisdiction; also recorded in `## Jurisdiction`]

---

## Jurisdiction

*Written by the cold-start interview. Every skill reads this section first (Step 0: Resolve the applicable jurisdiction) and loads `references/jurisdictions/<code>/` for each code. See `references/jurisdictions/REGISTRY.md` for the codes and their populated status.*

**Primary jurisdiction:** [ISO 3166-1 alpha-3 lowercase code, e.g. `ksa`]
**Footprint (other jurisdictions this practice operates in):** [list of codes, or none — an unpopulated footprint code is listed with "(not populated)"]
**Authoritative language of the primary jurisdiction:** [from the jurisdiction manifest]
**Output language:** [English | English plus the authoritative language for the bottom line, findings table, and counterparty-facing text (bilingual) | authoritative language only]
**Calendar for deadlines:** [from the jurisdiction manifest: weekend days, public holidays, Hijri or Gregorian]
**Currency for thresholds:** [from the manifest, e.g. SAR]
**Primary-source portal:** [from the manifest, e.g. https://laws.boe.gov.sa]
**Local counsel available for escalation:** [name / firm / N/A; a licensed lawyer admitted in the primary jurisdiction]
**Jurisdiction playbook defaults accepted:** [which rows of `references/jurisdictions/<code>/playbook-defaults.md` the user accepted at cold-start, and which they changed or rejected]

**Unpopulated jurisdiction rule.** If any code above resolves to a manifest with `populated: no`, every skill stops for that code and says so. It never applies another jurisdiction's rules or model knowledge in its place.

---

## Available integrations

| Integration | Status | Fallback if unavailable |
|---|---|---|
| CLM (Ironclad, Agiloft, etc.) | [✓ / ✗] | Manual record-keeping; renewal-tracker runs against a local register |
| E-signature (DocuSign, etc.) | [✓ / ✗] | User routes for signature outside the plugin |
| Document storage (Drive / SharePoint / Box) | [✓ / ✗] | User uploads agreements directly for each review |
| Slack | [✓ / ✗] | Alerts and stakeholder summaries delivered inline instead of posted |

**Data-residency constraint on connectors:** [none stated / rule and source / customer requirement]
**E-signature regime:** [platform signature acceptable between the parties / licensed local certificate required for: … — per the primary code's `electronic-transactions-law.md` rows, or N/A for `usa`]

*Re-check: `/commercial-legal:cold-start-interview --check-integrations`*

---

## Playbook

**Active side:** [sales / purchasing / both]

*Sales-side = the company sells its products or services. We're the vendor. Usually our paper. Purchasing-side = the company buys from third-party vendors or suppliers. We're the customer. Usually their paper. The answer changes every playbook position.*

> Skills that review or assess a contract against this playbook first determine which side the company is on (usually obvious from whose paper it is — if the counterparty is buying your product, you're sales-side; if you're buying theirs, you're purchasing-side). If it's not obvious, ask. Read the matching playbook section. Never apply a sales-side position to a purchasing-side contract or vice versa.

### Sales-side playbook

*Applies when the company is the vendor. Usually our paper.*

*[If not configured yet: leave the pointer "[Not configured — run /commercial-legal:cold-start-interview --side sales to build it]" in place of the subsections below.]*

#### Limitation of liability

**Standard position:** [their stated position for deals where they're selling]

**Acceptable fallbacks:** [what the signed agreements show they actually accept]

**Never accept:** [their hard nos]

**Carveouts we accept:** [list]

> *From the seed docs:* [If you found a delta between stated and actual, note
> it here. E.g., "Stated standard is a 12-month cap. 3 of 5 reviewed agreements
> closed at 24 months. Treating 24 months as an acceptable fallback."]

#### Indemnification

[same structure]

#### Data protection

[same structure]

#### Term and termination

[same structure]

#### Governing law and venue

**Preferred:** [list]
**Acceptable:** [list]
**Escalate:** [list]
**Never:** [list]
**Forum:** [courts | arbitration]
**Arbitration institution and seat:** [e.g. SCCA, Riyadh — or N/A]
**Language of proceedings and prevailing contract language:** [as answered]
**Jurisdiction playbook defaults applied:** [rows accepted from `references/jurisdictions/<code>/playbook-defaults.md`, each with its Basis citation and tag; rejected rows listed as rejected]

#### The one thing

[The deal-breaker they named for sales-side deals. This is the first thing every sales-side review checks.]

---

### Purchasing-side playbook

*Applies when the company is the customer. Usually their paper.*

*[If not configured yet: leave the pointer "[Not configured — run /commercial-legal:cold-start-interview --side purchasing to build it]" in place of the subsections below.]*

[Same subsection structure as Sales-side: Limitation of liability, Indemnification, Data protection, Term and termination, Governing law and venue (with Forum, Arbitration institution and seat, Language of proceedings and prevailing contract language, Jurisdiction playbook defaults applied), The one thing. Calibrated for purchasing — what we accept from vendors, not what we offer customers.]

---

## Escalation

| Can approve | Without escalation | Escalate to | Via |
|---|---|---|---|
| [Junior] | [their threshold, in the profile currency] | [You] | [Slack/email] |
| [You] | [your threshold] | [GC] | [method] |
| [GC] | [GC threshold] | [Business owner] | [method] |

**Value thresholds (in the profile currency, see `## Jurisdiction`):** [if they mentioned any — written with the currency code]

**Automatic escalations regardless of contract value:**
- [their list — unlimited liability, unfavorable IP, etc.]
- [the jurisdiction-file triggers the user kept, each with its file and article]

---

## House style

**Tone in redlines:** [terse? collaborative? depends on counterparty?]

**Stakeholder summaries:** [who reads them? how long should they be?]

**Where work product goes:** [[CLM]? Google Drive folder? Slack thread?]

**Where signed contracts live:** [CLM system + executed filter / Google Drive folder path / SharePoint library / manual upload]

**Output language and calendar:** [from `## Jurisdiction` — English | bilingual | authoritative language only; dates Gregorian with Hijri alongside where the manifest calendar is Hijri; number format]

---

## Outputs

**Work-product header** (prepended to every analysis, memo, review, or assessment this plugin generates):

- If Role is Lawyer / legal professional: `PRIVILEGED & CONFIDENTIAL — ATTORNEY WORK PRODUCT — PREPARED AT THE DIRECTION OF COUNSEL`
- If Role is Non-lawyer: `RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY, SOLICITOR, BARRISTER, OR OTHER AUTHORISED LEGAL PROFESSIONAL IN YOUR JURISDICTION BEFORE ACTING`

[When the primary jurisdiction or the footprint is not `usa`, copy the template's "The header's protection is jurisdiction-specific" paragraph and its bullets here from `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` `## Outputs`, and add the jurisdiction note under the lawyer header: `[Note: "work product" protection is a US doctrine. Protections in [primary jurisdiction name] differ — confirm the applicable privilege/confidentiality regime before relying on this marking to shield the document from disclosure.]` The privilege position for `ksa` is not in the reference files and is a point for local counsel, `[no rule in ksa files — verify]`.]

**Jurisdiction disclaimer line.** For every deliverable that applies a jurisdiction other than `usa`, add the manifest's `disclaimer` line directly under the work-product header, in English and in the authoritative language: [copy the `disclaimer` row of `references/jurisdictions/<primary code>/MANIFEST.md` here verbatim, both languages]. The line is part of the header: it is never stripped from an internal deliverable, and it stays on counterparty-facing text.

**Bilingual house style.** [Copy the template's "Bilingual house style" paragraph from `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` `## Outputs` here, filled with the output-language answer from `## Jurisdiction` and the manifest's `output_language_rule`.]

Remove the header from externally-facing deliverables (counterparty-facing redlines, stakeholder summaries forwarded outside legal) — see the specific skill's instructions. Confirm the correct marking for your jurisdiction and matter.

---

## Seed documents reviewed

| Agreement | Counterparty | Date signed | Notable terms |
|---|---|---|---|
| [filename] | [name] | [date] | [what you learned from it] |

---

## Review preferences

confirm_routing: true   # Set to false to skip routing confirmation and proceed automatically

---

## NDA triage preferences

closing_action: "[what the user said to append to every NDA triage output — e.g., 'Forward this output and the NDA to your contracts manager.']"

---

## Playbook monitor settings

pattern_threshold: 5
lookback_months: 12

*Increase threshold if your deal volume is high and you want fewer, more confident proposals. Decrease if you want earlier signals.*

---

*To re-run the interview: `/commercial-legal:cold-start-interview --redo`*
```

## After writing the practice profile

**Show what this plugin can do.** Before closing, offer:

> **Want to see what I can help with?**

If yes, show this tailored list (not a generic template — these are the concrete things this plugin does best):

> **Here's what I'm good at in commercial contracts:**
>
> - **Review a vendor MSA against your playbook** — e.g., "A procurement team sent a draft SaaS agreement — flag deviations, propose redlines, route to the right approver." Try: `/commercial-legal:review`
> - **Triage an inbound NDA to GREEN / YELLOW / RED** — e.g., "Sales needs to sign an NDA — fast triage so lawyer time only goes to the ones that need it." Try: `/commercial-legal:review`
> - **Track renewal deadlines** — e.g., "See what's renewing in the next 90 days so you never miss a cancel-by window." Try: `/commercial-legal:renewal-tracker`
> - **Trace a clause across amendments** — e.g., "A contract has three amendments — show how the indemnity clause has evolved." Try: `/commercial-legal:amendment-history`
> - **Escalate a deviation** — e.g., "A proposed change exceeds your authority — route to the right approver with a drafted ask." Try: `/commercial-legal:escalation-flagger`
> - **Review pending playbook updates** — e.g., "The deviation monitor flagged positions to revise — approve or reject the proposals." Try: `/commercial-legal:review-proposals`
>
> **My suggestion for your first one:** Triage an inbound NDA you're sitting on — it's a 2-minute feel-out of how the playbook reads. Or tell me what's on your plate and I'll pick.

This solves the cold-start problem (the supervisor doesn't know what to do first) and the value-prop problem (they don't know what the plugin can do) in one offer. Make the list specific. Skip this step if the supervisor already named a concrete first task during the interview.


1. **Show it to them.** Not the whole thing — a summary. "Here's what I heard. Take a look at the plugin config and tell me what I got wrong."

2. **Research source prompt.** Branch on the primary code:

   - *Populated non-`usa` code:* "Before your first contract review, make sure the primary-source portal is reachable: for `<code>` it is [manifest `source_portal`], fetched with `[manifest research_tool]` (for `ksa`: `python3 scripts/fetch-law.py --portal boe --id <guid> --lang ar`, GUIDs in `references/jurisdictions/ksa/SOURCES.md`; the built-in web-fetch tool rejects the portal's TLS chain, so the script or `curl` is used). Every skill probes it before citing and records `portal: <host> ✓ reachable | unreachable` in the reviewer note; when it is unreachable, articles are cited from the reference files with their `[settled — last confirmed …]` dates and nothing is supplied from memory." Run the probe now (`scripts/fetch-law.py --portal boe --index`, or a `curl` of the portal home) and report the result the same way the connector check does: ✓ only on a real response.
   - *`usa`:* "Before your first contract review: connect a research tool (CourtListener, Westlaw, or a statute/regulator MCP). Without one, I'll flag every citation as unverified — with one, I verify them against a current database. In Cowork: Settings → Connectors. In Claude Code: authorize when a skill prompts you."

3. **Propose starter skills.** Based on what hurts:
   - "You said renewals sneak up on you — I have a renewal tracker. Want me to scan [CLM] for everything expiring in the next 90 days?"
   - "You said junior folks escalate too much — want me to draft a triage guide they can use before they ping you?"

4. **Offer a test run.** "Want to throw a contract at me and see how I do with the playbook I just learned?"

5. **Close with a note on changeability.** End with something like:

   > "Done. Your practice profile is at `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md` — it's a plain text file you can read and edit directly. Anything you answered can be changed:
   >
   > - Edit the file directly for a quick change (a new fallback, a revised threshold, a name swap)
   > - Run `/commercial-legal:cold-start-interview --redo` for a full re-interview
   > - Run `/commercial-legal:cold-start-interview --check-integrations` to re-check what's connected
   >
   > The sections most often adjusted after first setup are the escalation thresholds and approval matrix, the playbook positions on LoL / indemnity / DPA, and the 'one thing' deal-breaker. To change the jurisdiction itself, run `/commercial-legal:customize jurisdiction` — it re-offers the playbook defaults for the new code and re-checks every position against its files."

## Your practice profile learns

After writing the practice profile, close with this note:

> **Your practice profile learns.** It gets better as you use the plugins:
>
> - When a skill's output feels off, that's usually a position to tune. The output will tell you which one.
> - The `playbook-monitor` agent watches for patterns. If you approve the same deviation five times, it'll propose updating the playbook to match how you actually practice.
> - You can always say "update my playbook to prefer X" or "change my escalation threshold to Y" and the relevant skill will write the change.
> - Run `/commercial-legal:cold-start-interview --redo <section>` to re-interview one part, or edit the config file directly.
>
> Ten minutes of setup gets you a working profile. A month of use gets you one that reads like you wrote it yourself.

## Tone

Warm, curious, a little bit delighted to be here. You're the new hire who did their homework. You're not a form. Don't say "please provide" — say "what's the deal with". Don't say "configure your settings" — say "tell me how your team works".

If they give you a short answer, it's fine to follow up once ("12 months — is that a cap on direct damages only, or total liability?") but don't drill. You can always ask later when it comes up in a real review.

## Failure modes to avoid

- **Don't write YAML.** The practice profile is prose with occasional tables. They edit it in a text editor, not a schema validator.
- **Don't skip the seed docs.** The interview tells you what they think their playbook is. The docs tell you what it actually is. Both matter.
- **Don't write a generic playbook.** If their answers are generic ("reasonable market terms"), push gently: "Give me a number. When a vendor says 24-month cap, do you counter or sign?"
- **Don't write a profile for an unpopulated primary jurisdiction, and don't invent a default.** Every jurisdiction default offered comes from `references/jurisdictions/<code>/playbook-defaults.md` with its Basis cell; a position the file does not cover is asked plainly and written without a citation. Never write any jurisdiction's rule into the profile from memory.
- **Don't promise things the other skills can't deliver.** Check what skills exist in this plugin before offering them.
- **Don't run this interview on every session.** Check the plugin config first. If it's populated, you're done.
