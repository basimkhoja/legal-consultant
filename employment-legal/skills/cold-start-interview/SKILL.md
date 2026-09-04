---
name: cold-start-interview
description: >
  Cold-start setup — learns your jurisdictional footprint and escalation rules
  from your handbook and termination memos. Asks which jurisdictions (country
  codes and sub-jurisdictions) have employees, offers the jurisdiction
  playbook defaults, reads seed documents, and builds a jurisdiction-aware
  escalation table. Use on fresh install, when CLAUDE.md still has
  [PLACEHOLDER] markers, or when re-running with --redo or --check-integrations.
argument-hint: "[--redo | --check-integrations]"
---

# /cold-start-interview

1. Check `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/CLAUDE.md`. If `--check-integrations`, skip the interview — re-run only the Part 0 `What's connected?` check and rewrite the `## Available integrations` table at that config path. When probing: only report ✓ if an MCP tool call actually succeeded. Configured-but-untested connectors should be marked ⚪ with a one-line how-to for confirming. Never report ✓ based on `.mcp.json` declarations alone — that misleads users into thinking something is wired up when it isn't.
2. Run the interview below (Part 0 first — role + integrations — then footprint): primary jurisdiction code, sub-jurisdictions, other countries; the jurisdiction playbook defaults; hiring/termination triggers; end-of-service and severance policy.
3. Seed docs: work regulations / handbook + 3 termination memos.
4. Build jurisdiction-specific escalation table (rows seeded from `references/jurisdictions/<code>/playbook-defaults.md` for the primary code).
4a. Refuse to write a profile whose primary code is unpopulated (see Step 0 and Part 1). Never write a profile that would make every skill stop.
5. If a populated CLAUDE.md (no `[PLACEHOLDER]` markers) exists at `~/.claude/plugins/config/claude-for-legal/employment-legal/CLAUDE.md (legacy upstream config path) or ~/.claude/plugins/cache/claude-for-legal/employment-legal/*/CLAUDE.md (legacy upstream cache path)` but not at the config path, copy it to the config path and tell the user what was migrated.
6. Write `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/CLAUDE.md`, creating parent directories as needed.

---

# Cold-Start Interview: Employment Counsel

## Purpose

Employment law is jurisdictional down to the bone. The right answer in one jurisdiction is the wrong answer in the next. This interview maps your footprint — every country and sub-jurisdiction with employees — resolves the primary jurisdiction code against `references/jurisdictions/REGISTRY.md`, offers that jurisdiction's playbook defaults, and builds an escalation table that knows which rules apply where.

## Cold-start check

Read `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/CLAUDE.md`:
- **Does not exist** → start the interview.
- **Contains `<!-- SETUP PAUSED AT: -->`** → greet the user and offer to resume from that section.
- **Contains `[PLACEHOLDER]` markers but no pause comment** → the template was never completed; offer to start fresh or resume from wherever the placeholders begin.
- **Populated (no placeholders, no pause comment)** → already configured; skip unless `--redo`.

The template structure lives at `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` — use it as the section scaffold. Write the completed practice profile to the config path, creating parent directories as needed. If a CLAUDE.md exists at the old cache path `~/.claude/plugins/cache/claude-for-legal/employment-legal/*/CLAUDE.md` but not here, copy it forward.

## Check for the shared company profile

Look for `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/company-profile.md`.

- **If it exists:** Read it. Show a one-line confirmation: "You're [name], [practice setting], at [company], [industry], operating in [jurisdictions]. Right? (Or say 'update' to change the shared profile.)" If confirmed, skip the company questions — go straight to the plugin-specific ones.
- **If it doesn't exist:** You'll be the first plugin this user set up. After the orientation and fork, ask the company questions and write them to the shared profile (per the template at `references/company-profile-template.md` in the plugin root), then continue with the plugin-specific questions. Tell the user: "I've saved your company profile — the other legal plugins will read it and skip these questions."

The company questions that belong in the shared profile (and should NOT be re-asked if it exists): practice setting, company name, industry, what-you-sell, size, jurisdictions, regulators, risk appetite, escalation names. The plugin-specific questions (playbook positions, review framework, house style, supervision model, etc.) stay per-plugin.

## Install scope check

Before the orientation, if you notice the working directory is inside a project (not the user's home directory), flag it. Say once:

> **Heads up — it looks like this plugin may be project-scoped, which means I can only read files in [current directory]. If you'll want me to read documents from elsewhere (Downloads, Documents, Dropbox), install user-scoped instead — see QUICKSTART.md. You can continue with project scope, but you'll need to move files into this folder.**

Ask the user to confirm before proceeding: continue with project scope, or pause to reinstall user-scoped. If the working directory *is* the user's home directory, skip this check silently.

## Before the interview starts

Open with the fork-first preamble. Keep it to 3-4 short lines. Ask quick-or-full before anything else.

> **`employment-legal` is for people who handle hiring, terminations, investigations, leave, policies, worker classification, and international expansion.** Not your area? `/legal-builder-hub:related-skills-surfacer`.
>
> **2 minutes** gets you your role, practice setting, and jurisdictional footprint (countries + sub-jurisdictions with employees), plus working defaults for termination risk flags, end-of-service posture, and handbook policies taken from the jurisdiction's playbook defaults. **15 minutes** adds your real termination review triggers and high-risk flags extracted from prior memos, employment-contract and settlement templates, jurisdiction supplements (state / canton / sector / nationality as applicable), worker-classification defaults, and leave-tracker integration.
>
> Quick or full? (Upgrade any time with `/cold-start-interview --full`.)

**Quick start path:** ask only Part 0 (role, practice setting, integrations), Part 1 (jurisdictional footprint, including the primary code and the Step 0 populated check), and the output-language and local-counsel questions. Write the config with `[DEFAULT]` markers on everything else; every `[DEFAULT]` for a populated code is the matching row of `references/jurisdictions/<code>/playbook-defaults.md` (Labor table) with its Basis cited, and the profile's "Jurisdiction playbook defaults accepted" field says `all rows accepted as [DEFAULT] — not reviewed`. Close with: "Done. You can start using the commands now. I've used the [jurisdiction] playbook defaults for termination flags, end-of-service posture, and handbook policies. When a skill's output feels off, that's usually a default you should tune — it'll tell you which. Run `/employment-legal:cold-start-interview --full` anytime to do the whole interview, or `/employment-legal:cold-start-interview --redo <section>` to re-do one part."

**Full setup path:** the existing interview flow below. After the user picks, give the fuller orientation described next, then proceed to Part 0.

## After the user picks quick or full

Give the fuller orientation. One paragraph, in your own voice:

> "This plugin maintains: your practice profile (jurisdictional footprint, termination flags, handbook references), a leave register with deadline alerts, and an investigation case file structure. It learns how you actually work — your practice, your risk calibration, your house conventions — and writes that into a plain-text file the plugin reads from every time. Everything you answer can be changed later."

Then the fresh-profile note:

> "Setup builds a fresh professional profile from your answers. It does not read your personal Claude history, other conversations, or your home-directory CLAUDE.md. If I notice relevant information in our conversation context — e.g., you mentioned your firm earlier — I'll ask before using it. Nothing personal gets folded into your practice configuration unless you type it or approve it."

Then: "Ready? A few quick questions first, then we'll go deeper."

**Why this matters** (offer if the user pushes back on the time cost). Every command in this plugin reads from the configuration this interview writes. A generic configuration gives generic output — a default jurisdiction table, a default list of high-risk termination flags, a default escalation matrix, and a review that treats two jurisdictions in your footprint the same way (a fixed-term expatriate contract and an indefinite national contract, say, or two sub-jurisdictions with different rules). Telling the plugin the actual footprint, the actual hiring and termination triggers, and the actual reporting lines is what makes the difference between "an employment AI tool" and "a tool that knows where your people are and what has bitten you before."

The interview's information comes only from the user's typed answers and documents they explicitly upload. Do not read `~/CLAUDE.md`, personal notes, or any ambient context to fill in practice details. If relevant context is already visible in the conversation (company name, prior mentions), surface it as a question ("I think you mentioned X earlier — should I use that?") before using it.

## Interview pacing

- **Assume the answer exists somewhere.** When a question asks for information that's probably written down somewhere — company description, playbook, escalation matrix, style guide, handbook, jurisdiction list, matter portfolio — prompt for a link or a paste before asking the user to type it from memory. "Paste a link or a doc, or give me the short version" is the default ask for anything that's more than a sentence. An interviewer who makes people re-type what they've already written has failed the first job of an interviewer.
- **Batch size — count subparts.** "Never ask more than 2-3 questions in one turn" means 2-3 *answerable prompts*, counting subparts. One question with 5 subparts is 5 questions. The test: can the user answer without scrolling? If the questions don't fit on one screen, it's too many. Prefer structured tap-through questions where possible — they don't require scrolling or typing.

**Pause for real answers.** Some questions have quick tap-through answers (who's using this, which states). Others need the user to type something, describe something, or upload a document (handbook, term memos, jurisdiction table). When a question needs more than a quick tap:

- **Ask the question and wait.** Say explicitly: "This one needs a typed answer — I'll wait." Do not move to the next question until the user responds.
- **For uploads:** "Paste the contents, share a file path, or say 'skip for now.' If you skip, I'll flag the gap in your configuration so you can fill it later." Then actually wait.
- **Before writing the configuration:** review the interview. List any questions that were skipped or answered with placeholders. Say: "Before I write your configuration, here's what's still open: [list]. Want to fill any of these now, or leave them as placeholders?" Then wait for the answer.
- **Never** write a configuration with silent gaps. Every placeholder should be a deliberate choice the user made to skip, not a question that scrolled past. The LIMITED DATA flag only applies to documents the user chose to skip — not to questions the interview skipped on them.
- **Pause and resume.** Tell the user up front: "If you need to stop, say 'pause' (or 'stop', or 'let me come back to this') and I'll save your progress. Run `/employment-legal:cold-start-interview` again later and I'll pick up where you left off." When the user pauses, write a partial configuration to `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/CLAUDE.md` with a `<!-- SETUP PAUSED AT: [section name] — run /employment-legal:cold-start-interview to resume -->` comment at the top and `[PENDING]` markers (distinct from `[PLACEHOLDER]`) on unanswered fields. When setup re-runs and finds a paused config, greet the user: "Welcome back. You paused at [section]. Your earlier answers are saved. Pick up where we left off, or start over?" Do not re-ask questions already answered.

**Verify user-stated legal facts as they come up in setup.** When the user answers an interview question with a specific rule citation, statute number, case name, deadline, threshold, jurisdiction, or registration number — and it's something you can sanity-check — do the check before writing it into the configuration. If what they said conflicts with your understanding or with something they've pasted, surface it: "You said the threshold is X; my understanding is Y — can you confirm which goes in the profile? `[premise flagged — verify]`" A wrong fact written into CLAUDE.md propagates into every future output; catching it here is one of the highest-leverage moments in the product.

## The interview

### Opening

> Employment law is the practice area where "it depends" is most often the honest answer. I need your map before I can tell you anything useful — where are your people, and what have you already dealt with?

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

**Setup mode for this skill.** This is the one skill that runs before the profile exists, so Step 0 item 1 cannot stop on a missing `## Jurisdiction` section: the primary code is taken from the user's answer in Part 1 below, and items 2-8 apply from the moment that code is known. Item 3's populated check is enforced in Part 1 as a refusal to write the profile (not merely a stop for one matter). On `--redo` or `--check-integrations` with an existing profile, Step 0 runs as written and the code comes from the profile.

**Jurisdiction files this skill loads:**
- `references/jurisdictions/REGISTRY.md` — the list of codes and their populated status (Part 1: primary code and footprint check).
- `references/jurisdictions/<code>/MANIFEST.md` — `populated`, `authoritative_language`, `calendar`, `currency`, `source_portal`, `research_tool`, `output_language_rule`, `disclaimer` (Part 1 and the profile-writing step).
- `references/jurisdictions/<code>/playbook-defaults.md` — the Labor table, every row, offered as defaults in Part 2a and seeded into the jurisdiction table.
- `references/jurisdictions/<code>/labor-law.md` — Arts. 75 (notice), 84-87 (end-of-service award and resignation fractions), 53 (probation), 83 (non-compete), 9 (Arabic prevails), as the Basis for the defaults offered in Part 2a and the language question in Part 3.
- `references/jurisdictions/<code>/saudization-nitaqat.md` — the nationalisation-band question in Part 1a (band comes from the establishment's platform dashboard, dated; the file's coefficient rows are not used to state a band).
- `references/jurisdictions/<code>/social-insurance-law.md` — the social-insurance registration question in Part 1a (Arts. 7-10).
- `references/jurisdictions/<code>/platform-obligations.md` — the documentation-platform and registrations questions in Part 1a (Arts. 15-16, 51, Regulation Art. 18).
- `references/jurisdictions/<code>/labor-law-implementing-regulations.md` — Reg. Arts. 3-4 (work regulations model, certification/approval route) for the approval-status question in Part 3.
- `references/jurisdictions/<code>/labor-dispute-route.md` — the default forum row (friendly settlement, labor courts, Art. 234 limitation) offered in Part 2a.

For `ksa` these files exist today; for another populated code, load the files with the same names, and where a file is absent say so and tag the corresponding profile field `[no rule in <code> files — verify]`.

### Part 0: Who's using this, and what's connected

Three quick questions before we get into employment specifics. These shape how the plugin works, not what it can do.

#### Who's using this?

> Who'll be using this plugin day to day? (This feeds the work-product header on every termination memo, handbook draft, and investigation summary — lawyer outputs get the confidentiality/privilege header appropriate to your jurisdiction per the plugin CLAUDE.md `## Outputs`, non-lawyer outputs get the "research notes, review with counsel" header.)
>
> 1. **Lawyer or legal professional** — attorney, paralegal, legal ops working under attorney oversight.
> 2. **Non-lawyer with attorney access** — founder, business lead, contracts manager, HR, procurement; you have an in-house or outside attorney you can consult.
> 3. **Non-lawyer without regular attorney access** — you're handling this yourself.

If the answer is 2 or 3, say this once (don't repeat it on every output):

> You can use every feature here — research, review, drafting, tracking. Two things change in how I work:
>
> 1. **I'll frame outputs as research for attorney review, not as verdicts.** Instead of "GREEN — sign it," you'll get "here's what I found and here are the questions to ask before you sign." That's more useful than a green light you can't be sure of.
> 2. **I'll pause before steps that have legal consequences** — signing a contract, terminating someone, sending a demand, filing something, clearing a launch, responding to a regulator. I'll ask whether you've reviewed with an attorney, and I'll put together a short brief so the conversation with them is fast.
>
> This isn't a disclaimer. It's the plugin knowing the difference between what it's good at — research, organization, structure — and licensed legal judgment about your specific situation, which a tool can't give you. A few hours of a lawyer's time at the right moment is usually cheaper than the mistake.

If the answer is 3, add:

> If you need to find an attorney, solicitor, barrister, or other authorised legal professional: contact your jurisdiction's bar or licensing body (examples: state bar in the US, SRA/Bar Standards Board in England & Wales, Law Society in Scotland/NI/Ireland/Canada/Australia; for a populated non-`usa` code, the licensing body is among the `issuing_authorities` in `references/jurisdictions/<code>/MANIFEST.md` — for `ksa` that row lists the Ministry of Justice) — most offer a lawyer referral service as the fastest starting point. Many offer free or low-cost initial consultations. For small businesses, local law school clinics (and equivalents like SCORE mentors in the US) can point you in the right direction. For individuals, legal aid organizations cover many practice areas.

#### Practice setting

> Which of these best describes where you're practicing? (This feeds every skill's escalation framing — in-house gets "loop in GC," solo/small gets "call outside counsel," clinic gets "route to supervising attorney.")
>
> - **Solo / small firm (no hierarchy)** — I'll skip approval-chain questions and ask when you'd loop in a colleague or outside counsel instead.
> - **Midsize / large firm** — I'll ask about your approval chain, billing thresholds, and who signs off above you.
> - **In-house** — I'll ask about your escalation matrix, who the GC/CLO is, and when something goes to the business.
> - **Government / legal aid / clinic** — I'll ask about supervision structure and any restrictions on your practice.
> - **My practice doesn't fit any of these** — say so. I'll adapt.

**Practices that don't fit the boxes.** If the user's practice doesn't match the options above (international arbitration, public international law, amicus-only, academic consulting, pro bono panel, tribal court, military justice, maritime, or anything else the standard categories assume away), offer: "It sounds like your practice doesn't fit my usual categories. Tell me about it in your own words — what you do, who for, what jurisdictions and forums, what the work looks like — and I'll build your profile from that instead of forcing you into boxes that don't fit. I'll skip or adapt the questions that don't apply." Then build the profile from the free-form description, flagging which template fields were filled, adapted, or left empty because they don't apply. A profile built from a forced fit is worse than a sparse profile built from what's actually true.

This one changes how the rest of the interview runs:

- **Solo / small firm (no hierarchy):** Skip or reframe escalation-chain questions later in the interview. Instead of "who approves above your threshold," ask "when do you call in outside counsel or a colleague for a second opinion." Escalation in the practice profile maps to "consult" not "route for approval." The escalation table at the end should have no internal tiers above the user; it lists outside counsel, an insurer, or "no further escalation" instead.
- **Midsize / large firm / in-house:** Ask the escalation question below — reporting line, who approves terminations above severance threshold, who signs off on RIFs, etc.
- **Government / legal aid / clinic:** Route to the supervision model — who reviews work product, what the sign-off chain looks like for client communications, whether a supervising attorney of record is assigned per matter.

**Escalation question (ask after the practice-setting answer, adapted to the branch above):**

> If your team has a shared escalation matrix or delegation-of-authority policy set at the team or department level, that's the one I want — paste it or link it. I'll use it as the baseline and ask about your personal overrides separately.

> "When a review finds something that needs someone more senior to sign off — a termination with unlawful-dismissal or protected-status risk, an investigation that escalates, a status/contract-type call at the edge, a reasonable-adjustment refusal, or a decision that's above your authority — who does that go to? Give me a name or a role (the GC, your boss, the head of HR, local counsel in the primary jurisdiction), or say 'I decide myself.' This is how the plugin knows when to say 'you can handle this' versus 'loop in [X].' (This feeds /termination-review, /worker-classification, /investigation-open, and every other skill's escalation routing.)"

Record the answer in the plugin config as `## Practice setting` (or include in the `## Who we are` section).

#### What's connected?

> This plugin can work with: HRIS (e.g., Workday, SAP SuccessFactors, Oracle HCM, BambooHR, Rippling, ADP, or a local system such as Bayzat/Jisr/ZenHR), document storage (Google Drive, SharePoint, Box), Slack, and — for a populated non-`usa` jurisdiction — the government platforms named in `references/jurisdictions/<code>/platform-obligations.md` (for `ksa`: Qiwa, Mudad, GOSI online), which are not MCP connectors: record whether you have login access, and the skills will ask you for exports. Let me check which connectors you have configured — features that need them will work, and features that don't have them will fall back to manual gracefully instead of failing silently.

**Check what's actually connected, not what's configured.** A connector listed in `.mcp.json` is *available*. A connector that's actually responding is *connected*. These are different, and confusing them destroys trust. For each connector this plugin uses:

- If you can test the connection (call a simple MCP tool like a list or search), report ✓ only on a successful response.
- If you can't test (no way to probe from here), report ⚪ "configured but not verified — open your MCP settings to confirm" with a one-line how-to.
- Never report ✓ based on configuration alone.

For connectors that show as not connected, tell the user how to connect. Example phrasing: "Box isn't connected. In Claude Cowork: Settings → Connectors → Add → Box → sign in. In Claude Code: add the Box MCP to your config or via `/mcp`. This plugin works without it — you'll paste documents instead of pulling them — but connecting it makes document pulls automatic."

Then report findings in this form:

> - ✓ [Integration] — connected (tested)
> - ⚪ [Integration] — configured but not verified. Open your MCP settings to confirm.
> - ✗ [Integration] — not found. [Feature] will fall back to [manual alternative]. [How to connect.] If you set this up later, re-run `/employment-legal:cold-start-interview --check-integrations`.
>
> You don't need all of these. Core features work with file access alone — leave tracking falls back to a local register if there's no HRIS.

#### Write to the config CLAUDE.md

Write `## Who's using this`, `## Available integrations`, and `## Outputs` sections immediately after the first section of the config-path CLAUDE.md (the plugin config) per the template in `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md`. These drive work-product header choice and feature-fallback behavior across every skill in this plugin.

### Part 1: The footprint (2-3 min)

> **What does [your company] do?** This is the single most important context — a SaaS vendor's playbook, a hardware distributor's playbook, and a services firm's playbook are completely different. You don't have to type it out: paste a link to your company website, your "about" page, your Wikipedia article, or your latest annual report, commercial-register extract, or exchange filing, and I'll extract what I need. Or give me the one-sentence version: what you sell, to whom, and how (direct sales / channel / marketplace / subscription).

> Before I ask the footprint questions: do you have a jurisdiction table, a country / sub-jurisdiction coverage memo, or a list of active employee locations from your HRIS I can read (for a populated non-`usa` code, a headcount export from the platform named in `references/jurisdictions/<code>/platform-obligations.md` — for `ksa`, a Qiwa or GOSI headcount export — is ideal)? Paste the contents, share a file path, or say 'no' and I'll ask the questions one at a time. If you share one, I'll extract the footprint rather than making you list it from memory. (This feeds /wage-hour-qa, /worker-classification, /hiring-review, /termination-review, /policy-drafting — every wage-hour question, worker-classification check, and handbook supplement branches on your jurisdictions.)

If not:

- **Primary jurisdiction.** Which country is the primary jurisdiction of this practice — where most employees are, or where the employing entity sits? Give me the ISO 3166-1 alpha-3 code in lowercase (`ksa`, `gbr`, `fra`, `che`, `usa`) or the country name and I'll map it. Home country = the HQ recorded in the company profile unless you say otherwise.
- **Populated check (stop rule — do not skip).** Look the code up in `references/jurisdictions/REGISTRY.md` and read `references/jurisdictions/<code>/MANIFEST.md`. If `populated` is not `yes` (and the code is not `usa`), **refuse to write the profile** and say: "Jurisdiction `<code>` (<name>) is registered but not populated: no reference files exist for it, so every skill in this plugin would stop on your first matter. I will not write a profile with an unpopulated primary jurisdiction. Options: (1) choose `usa` (upstream US path, upstream research connectors), (2) choose a populated code — currently: [list every row of REGISTRY.md whose Populated column is `yes`], (3) populate `references/jurisdictions/<code>/` first (see README, 'How to add a jurisdiction') and re-run setup." Wait for the answer. If the user picks (1) or (2), continue with that code as primary and record the originally requested code in the footprint as `[not populated — no rule applied]`. If the code is not in REGISTRY.md at all, treat it as unpopulated.
- **Sub-jurisdictions.** Every sub-jurisdiction the primary code treats as distinct (for `usa` the states, for `che` the cantons, for `gbr` the nations; for `ksa` there is no territorial sub-jurisdiction — the variance axes are nationality, sector, gender-specific rules and entity type, captured in Part 1a). All of them.
- **Other countries.** Every other country with employees, as codes. Run the populated check on each: an unpopulated footprint code is allowed in the profile (skills stop for that code per Step 0 item 3 when a matter touches it), but tell the user now which footprint codes are unpopulated and that matters in them go to local counsel.
- Remote-first or office-based? (Remote-first means the footprint keeps expanding without anyone telling you.)
- Which jurisdiction has the most employees? That's your default when a question doesn't specify.

**If the user didn't upload a jurisdiction list:** at the end of this section, offer: "Want me to write this up as a standalone jurisdiction table you can maintain and share? Same footprint data I just captured, in a format that's easier to edit as the company grows."

### Part 1a: The entity and the registrations (2-3 min)

Ask these only for a populated non-`usa` primary code (for `usa`, skip to Part 2 — the upstream profile has no slot for them). Batch them 2-3 at a time; each answer maps to a field in `## Jurisdiction` or `## Jurisdictional footprint` of the profile (see "Writing the practice profile"). Where a document exists (commercial-register extract, platform dashboard export, social-insurance certificate), ask for a paste before asking the user to type.

> A few registration facts the jurisdiction files key off. If any of these lives in a document or a platform dashboard, paste it.

- **Employing entity.** Commercial registration number, entity type (from the entity types in `references/jurisdictions/<code>/playbook-defaults.md` → Corporate table, "Entity types offered"), and any foreign-investment registration (for `ksa`, the registration in `references/jurisdictions/ksa/investment-law.md`; state N/A if wholly locally owned). One entity per row if there are several employing entities.
- **Sectors / activities.** The licensed activity of each employing entity (drives the nationalisation quota and any sector regulator).
- **Headcount by nationality.** Nationals / non-nationals per entity (and GCC nationals separately where the nationalisation file treats them differently — for `ksa`, `saudization-nitaqat.md` "Nitaqat guide, Terms" row).
- **Nationalisation band.** The current band per entity and activity as shown on the government platform, with the date it was read (for `ksa`: the Nitaqat band from the Qiwa establishment dashboard, dated). Do not compute or infer the band from the coefficient rows in `saudization-nitaqat.md`; that file's "How skills should use this file" section forbids it. Record `[not provided]` if the user cannot read it now.
- **Work-permit sponsorship.** Do you sponsor non-national workers? Pipeline of pending permits? Any roles in the professions the jurisdiction reserves to nationals (for `ksa`, `labor-law-implementing-regulations.md` Reg. Art. 11)?
- **Contract types in use and documentation platform.** Fixed-term / indefinite / part-time / flexible / remote, and where contracts are documented (for `ksa`, contracts must be documented electronically on the ministry's platform, in practice Qiwa — `platform-obligations.md` Art. 51 row and Regulation Art. 18; note the file tags the platform's identity `[model knowledge — verify]`).
- **Social-insurance and labour-platform registrations.** Social-insurance registration number and status (for `ksa`, GOSI — `social-insurance-law.md` Arts. 7-10), establishment file on the labour platform (for `ksa`, the Qiwa establishment number — `platform-obligations.md` Arts. 15-16 row), and wage-file compliance status (for `ksa`, Mudad / Wage Protection System — the WPS row of `platform-obligations.md` is `[model knowledge — verify]`; record the user's answer as `[user provided]`).
- **Calendar and currency.** Confirm the manifest's calendar (weekend days, public holidays, Hijri or Gregorian) and currency; if the employment contracts elect a different calendar (for `ksa`, Annex 5 cl. 14 of `labor-law-implementing-regulations.md` elects Gregorian), record that as the contract calendar.

**Verify user-stated registration facts.** A registration number, band or status the user types is `[user provided]`; do not promote it. If the user pastes a dashboard export, tag it `[user provided — <platform> export dated YYYY-MM-DD]`.

### Part 2: The review triggers (2-3 min)

> "**Do you want to build your positions now?** It makes the review skills (hiring-review, termination-review, policy-drafting) much better — they'll know your stance and fallbacks instead of generic ones. It takes about 3-4 minutes. Skip if you just want to try the other commands; the review skills will use defaults and tell you when they hit a position you haven't set."

> If your team has a shared playbook, escalation matrix, or delegation-of-authority policy set at the team or department level, that's the one I want — paste it or link it. I'll use it as the baseline and ask about your personal overrides separately.

> Before the questions: do you have a termination checklist, a settlement or end-of-service document template, an employment-contract or offer template, or an existing review-trigger playbook I can read? Paste the contents, share file paths, or say 'no' and I'll walk through the questions. If you share them, I'll extract the triggers and escalation points rather than making you describe them.

If not:

**Hiring:** When does legal see an offer?
- Every offer? Only exec? Only with restrictive covenants? Never?
- What's in the standard employment contract or offer template? Do you use restrictive covenants? (Enforceability rules come from the applicable jurisdiction file — for `ksa`, `labor-law.md` Art. 83: written, specific as to time, place and type of work, maximum two years; for `usa`, the upstream research path, state by state. Do not state a rule here; the defaults step below offers the file's row.)

**Termination:** When does legal see a termination?
- Every term? Performance only? Restructurings only?
- Contract types in use (fixed-term / indefinite) and standard notice periods by contract type — the statutory floor comes from the jurisdiction file (for `ksa`, `labor-law.md` Art. 75), the contract may give more.
- End-of-service benefit policy: statutory only, or statutory plus a top-up? (For a populated code the statutory entitlement is computed by /termination-review from the file — for `ksa`, `labor-law.md` Arts. 84-87; the profile records only the top-up formula. For `usa`, severance is discretionary unless a plan or contract says otherwise: formula, discretionary, none?)
- Settlement or release practice: is a release or settlement document required, always or only above a threshold? (For `ksa`, `labor-law.md` Art. 8 makes a release of statutory rights during the contract void; record the practice, and /termination-review applies the row.)

**The high-risk flags:** What makes a termination scary? Start from the jurisdiction's default flags — for a populated code, the rows /termination-review reads from the files (for `ksa`: termination during protected leave `labor-law.md` Arts. 82 and 155; Art. 80 grounds not met or worker not heard; notice defect Art. 75; wage arrears per `platform-obligations.md`; Art. 77 exposure; nationalisation-band impact per `saudization-nitaqat.md`; work-permit and exit consequences); for `usa`, the upstream set below. Then ask what else has bitten you. (This feeds /termination-review — every future termination memo gets checked against these flags before the skill concludes.)
- Recent complaint (harassment, discrimination, whistleblower)
- Recently returned from protected leave
- Protected status + thin documentation
- Anything else that's bitten you before?

### Part 2a: The jurisdiction playbook defaults (2-3 min, populated non-`usa` primary code only)

Open `references/jurisdictions/<code>/playbook-defaults.md` and walk the **Labor** table row by row (Contract types, Probation, Notice, End-of-service award, Compensation for invalid termination, Termination without award or notice, Non-compete, Working time, Leave, Dispute route, Saudization / nationalisation, Social insurance, Platforms, Work regulations — the row names are the file's). For each row:

> **[Field]** — default: [Default column, verbatim]. Basis: [Basis column, verbatim — file and article]. Accept, edit, or reject?

Rules for this step:
- **Never state a default whose Basis cell is empty or does not name a file.** Skip the row, tell the user "the defaults file carries no citation for [field]; I won't offer a default", and leave the profile field `[no rule in <code> files — verify]`.
- Carry the Basis tag onto the profile: a default whose Basis row is `[settled — last confirmed …]` in the instrument file is written with that tag; one whose Basis says "Practice" or carries `[model knowledge — verify]` is written with `[model knowledge — verify]`.
- An edit that goes **below** a statutory floor named in the Basis (a notice period shorter than the file's Art. 75 row, an end-of-service formula below Arts. 84-87, a non-compete longer than Art. 83's two years) is not refused, but is written with `[review — below the statutory floor in <file> <article>; the file's row prevails in every skill]`.
- Record the outcome in the profile field **Jurisdiction playbook defaults accepted** as: `accepted: [rows]; edited: [row → new value]; rejected: [rows]`.
- Quick-start path: all rows are written as `[DEFAULT]` with their Basis, and the field says `all rows accepted as [DEFAULT] — not reviewed`.

For `usa` there is no defaults file; the upstream questions above are the defaults and the field says `n/a — usa`.

**If the user didn't upload a termination checklist or severance template:** at the end of this section, offer: "Want me to write this up as standalone termination-review checklist and high-risk-flag memo you can share? Same content I just captured, formatted so HR partners can read it without a legal decoder."

### Part 3: Seed documents (3-4 min)

**Where does leave data live?**

Before asking for documents, ask one infrastructure question:

> Do you have an HRIS or payroll system that tracks employee leave — Workday, SAP SuccessFactors, BambooHR, Rippling, ADP, a local system, or something else? And does legal have read access to it? (For a populated non-`usa` code: is the social-insurance and wage-platform data accessible too — for `ksa`, GOSI and Mudad exports?) (This feeds /leave-tracker and /log-leave — with HRIS access, the tracker pulls leaves automatically; without, it runs off a local register you update manually.)

- If HRIS with legal read access: note the system name
- If HRIS without legal access, or no leave tracking module: note "manual"
- If no HRIS: note "manual"

**Seed documents**

> This is the most important part — I want to see how your team actually works, not just what your policies say. I need two things:
>
> 1. **Your work regulations / handbook.** Current version, and its approval status if the jurisdiction requires one (for `ksa`, work regulations must follow the ministry model and be certified or approved — `labor-law-implementing-regulations.md` Reg. Arts. 3-4; tell me the certification date or "not yet"). Which language versions exist and which prevails (for `ksa`, `labor-law.md` Art. 9: the Arabic text is the authoritative one). I'll read it to know what you've promised employees and where the gaps are. (This feeds /policy-drafting and /hiring-review — every policy draft and offer-letter check gets cross-referenced against what the handbook already commits to.)
>
> 2. **Recent employment documents — the more the better.** Ten is a good floor; twenty gives a much clearer picture. Mix it up: employment contracts or offer letters, termination letters, settlement or end-of-service documents, warning letters, PIPs, accommodation or adjustment requests — whatever you have. If you have fewer than ten, share what you can, but flag it. (These feed /termination-review and /hiring-review — the skills extract your house format, end-of-service and severance posture, and high-risk patterns from your actual documents, not a generic template.)

If they have an HRIS or good document visibility: aim for 10-20 documents across the types described above.

If they have poor visibility (scattered folders, no system): accept whatever they can pull. Flag every section of the practice profile built from fewer than 10 documents with [LIMITED DATA — N documents reviewed].

**From the handbook:** Policies with jurisdictional variants (leave accrual, final settlement, working time). Jurisdiction / segment supplements if any (state, canton, nationality, sector, gender-specific rules — whichever axis the primary code uses). Language versions and which prevails. Regulatory approval status. The gaps — things the handbook doesn't cover that it should (for a populated code, diff the headings against the model work regulations the file names — for `ksa`, Annex 1 of `labor-law-implementing-regulations.md`).

**From the seed documents:** What got checked on terminations. What high-risk flags look like in practice. Employment contract / offer template format and standard restrictive covenant language. Settlement or end-of-service document format for the termination-review skill to match. Any patterns in what the team actually approves vs. what the policies say.

**Output language and local counsel (ask here, both paths):**

> Two last profile settings. (1) **Output language:** English only, or English plus the authoritative language of the primary jurisdiction for the bottom line, findings table and any counterparty-facing text (bilingual)? The authoritative language comes from `references/jurisdictions/<code>/MANIFEST.md` → `authoritative_language` (for `usa`, English — the question is moot). (2) **Local counsel:** is a lawyer licensed in the primary jurisdiction available for escalation — name or firm, or N/A? For `usa` this is your outside employment counsel.

## Build the jurisdiction table

This is the core output. For each jurisdiction in the footprint, one row (plus one row per sub-jurisdiction or segment the code treats as distinct):

**When the applicable code is populated (non-`usa`):** seed the primary code's row(s) from the Labor table of `references/jurisdictions/<code>/playbook-defaults.md` as accepted or edited in Part 2a — the "Special rules" cell lists the accepted rows with their Basis (file and article), the "Auto-escalate" cell lists the high-risk flags from Part 2 and the escalation answer from Part 0. Example shape for `ksa` (the cells are the file's rows, not restated law):

| Jurisdiction | Special rules | Auto-escalate |
|---|---|---|
| `ksa` — nationals, indefinite contracts | Notice 60/30 days (`labor-law.md` Art. 75); end-of-service award (`labor-law.md` Arts. 84-87); Art. 77 compensation; non-compete ≤ 2 years (`labor-law.md` Art. 83); dispute route (`labor-dispute-route.md`) — each `[settled — last confirmed <date>]` as tagged in the file | Any termination without an Art. 80 ground; any termination during protected leave (Arts. 82, 155); any restrictive covenant |
| `ksa` — non-nationals, fixed-term contracts | Fixed-term only (`labor-law.md` Art. 37; `labor-law-implementing-regulations.md` Reg. Art. 12); work permit and sponsorship (`platform-obligations.md`); Nitaqat band `[user provided, dated]` (`saudization-nitaqat.md`) | Any termination before expiry (Art. 77(2) remainder of term); any hire that moves the band |

Segment the rows the way the files vary the rules (for `ksa`: nationality and contract type; the Handbook section's supplement axis records the rest). Footprint codes that are unpopulated get a single row: `[<code>: N employees — not populated — no rule applied; route to local counsel]`.

**When the applicable code is `usa`:** the upstream seed rows, kept as illustrations and retagged — every rule stated in them is `[model knowledge — verify]` and must be researched through the upstream connectors on first use:

| Jurisdiction | Special rules | Auto-escalate |
|---|---|---|
| California | No non-competes. Final pay due last day (or 72hrs if employee quits w/o notice). Meal/rest break penalties. PAGA exposure. `[model knowledge — verify]` | Any termination. Any restrictive covenant. |
| New York | Pay transparency in postings. NYC has separate rules. Final pay next regular payday. `[model knowledge — verify]` | Exec hires (pay transparency). |
| [etc.] | | |

Don't invent rules for jurisdictions they didn't name. If they have one employee in a sub-jurisdiction and no memo ever mentioned it, note `[<sub-jurisdiction>: 1 employee, no history — research on first issue]` (upstream example: `[Montana: 1 employee, no history — research on first issue]`). For a populated code, "research on first issue" means the jurisdiction files first, then the portal in the manifest.

## Writing the practice profile

Per the template structure at `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md`. Write the completed practice profile to the plugin config, creating parent directories as needed. Key sections: jurisdictional footprint, hiring/termination review triggers, high-risk flags, the jurisdiction-specific escalation table.

**Refusal (repeat of the Part 1 stop).** Before writing, re-read the primary code: if its `MANIFEST.md` says `populated` is not `yes` and the code is not `usa`, do not write the file — return to Part 1 and offer `usa` or a populated code. A profile whose primary code is unpopulated makes every skill stop on its first matter.

**Field map — each answer goes to exactly these fields of the template:**

| Answer (interview step) | Profile field |
|---|---|
| Primary code (Part 1) | `## Jurisdiction` → Primary jurisdiction |
| Other countries, with populated status (Part 1) | `## Jurisdiction` → Footprint; `## Jurisdictional footprint` → Other countries with employees |
| `MANIFEST.md` → `authoritative_language` | `## Jurisdiction` → Authoritative language of the primary jurisdiction |
| Output language (Part 3) | `## Jurisdiction` → Output language |
| `MANIFEST.md` → `calendar` (+ contract calendar from Part 1a) | `## Jurisdiction` → Calendar for deadlines |
| `MANIFEST.md` → `currency` | `## Jurisdiction` → Currency for thresholds |
| `MANIFEST.md` → `source_portal` / `research_tool` | `## Jurisdiction` → Primary-source portal |
| Local counsel (Part 3) | `## Jurisdiction` → Local counsel available for escalation; `## Escalation` table rows that name local counsel |
| Part 2a outcome | `## Jurisdiction` → Jurisdiction playbook defaults accepted |
| Sub-jurisdictions (Part 1) | `## Jurisdictional footprint` → Primary jurisdiction and sub-jurisdictions with employees |
| Headcount by nationality (Part 1a) | `## Jurisdictional footprint` → Headcount by nationality |
| Nationalisation band, dated (Part 1a) | `## Jurisdictional footprint` → Nationalisation-quota band |
| Work-permit sponsorship (Part 1a) | `## Jurisdictional footprint` → Work-permit sponsorship |
| Contract types and documentation platform (Part 1a) | `## Jurisdictional footprint` → Contract types in use |
| Social-insurance and platform registrations (Part 1a) | `## Jurisdictional footprint` → Social-insurance and labour-platform registrations; `## Systems` |
| Commercial registration, entity type, foreign-investment registration, sectors (Part 1a) | `company-profile.md` (shared) and, where the template has no slot, a `**Employing entities:**` line under `## Who we are` |
| Restrictive-covenant answer (Part 2) with the file's row | `## Hiring review` → Restrictive covenant policy |
| End-of-service answer (Part 2 / 2a) | `## Termination review` → Statutory end-of-service entitlement (file and articles, e.g. `labor-law.md` Arts. 84-87 for `ksa`) and Standard severance above the statutory entitlement (the top-up or "none") |
| Notice periods (Part 2 / 2a) | `## Termination review` → Standard notice periods by contract type |
| Release / settlement practice (Part 2) | `## Termination review` → Release required for severance |
| High-risk flags (Part 2) | `## Termination review` → High-risk termination flags |
| Work regulations approval status, supplements axis, language versions (Part 3) | `## Handbook` → Regulatory approval of work regulations; Jurisdiction supplements; Language versions |
| Jurisdiction table | `## Jurisdiction-specific escalation rules` |

Fields the interview could not fill because a reference file lacked the rule are written as `[no rule in <code> files — verify]`, never left as `[PLACEHOLDER]` (a placeholder makes every skill refuse to run). For `usa`, the jurisdiction-file-derived fields (Authoritative language, Calendar, Currency, Primary-source portal, Playbook defaults accepted) are written as `English`, `Saturday-Sunday weekend, US federal holidays [model knowledge — verify]`, `USD`, `upstream research connectors (CourtListener / Westlaw)`, `n/a — usa`.

**Research step at setup.** For a populated non-`usa` primary code, probe the portal named in `MANIFEST.md` → `research_tool` once (for `ksa`: `python3 scripts/fetch-law.py --portal boe --index`, or `curl -sS` of the portal home; the built-in web-fetch tool rejects the portal's TLS chain) and record `portal: <host> ✓ reachable | unreachable` in the profile's `## Available integrations` table as a "Primary-source portal" row. Do not fetch instruments during setup — the defaults come from the files, not from a live read. For `usa`, probe the upstream connectors (CourtListener / Westlaw) as Part 0 already does. If the probe fails, say so and continue; the skills apply the "no silent supplement" stop at run time.

**Output of this skill.** The written profile is a configuration file, not a deliverable, and carries no work-product header. The one deliverable this skill may emit — the standalone jurisdiction table offered in Part 1 — gets the work-product header from the profile's `## Outputs`, then the jurisdiction disclaimer line from the profile (for a non-`usa` primary code), and follows the bilingual house-style rule in the plugin CLAUDE.md `## Outputs` when the profile's Output language is bilingual (the table is the findings table; render it in the authoritative language as well).

## After writing

**Show what this plugin can do.** Before closing, offer:

> **Want to see what I can help with?**

If yes, show this tailored list (not a generic template — these are the concrete things this plugin does best):

> **Here's what I'm good at in employment law practice:**
>
> - **Review an offer letter and restrictive covenants** — e.g., "Jurisdiction check on covenants, mandatory clauses and registrations." Try: `/employment-legal:hiring-review`
> - **Termination review with risk flags** — e.g., "End-of-service award, notice, settlement, final-settlement timing, and high-risk indicators flagged before the decision." Try: `/employment-legal:termination-review`
> - **Classify a worker engagement** — e.g., "Employee / contractor / seconded / outsourced — categories per the applicable jurisdiction file, with misclassification gap analysis." Try: `/employment-legal:worker-classification`
> - **Ask a jurisdiction-aware wage/hour question** — e.g., "Multi-jurisdiction workforce question routed against the jurisdictions in your footprint." Try: `/employment-legal:wage-hour-qa`
> - **Kick off international expansion** — e.g., "New country on the roadmap — plan the employment-law workstream." Try: `/employment-legal:expansion-kickoff`
> - **Open an internal investigation** — e.g., "Create the privileged workspace, start the log, route interviews." Try: `/employment-legal:investigation-open`
>
> **My suggestion for your first one:** Run `/termination-review` on a hypothetical termination — it's the skill most likely to surface how the risk calibration reads. Or tell me what's on your plate and I'll pick.

This solves the cold-start problem (the supervisor doesn't know what to do first) and the value-prop problem (they don't know what the plugin can do) in one offer. Make the list specific. Skip this step if the supervisor already named a concrete first task during the interview.


- "Here's your jurisdiction table. The [high-attention jurisdiction from `## Jurisdictional footprint`] row is the one to double-check."
- "What's the next termination? Let me take a look."
- Flag handbook gaps: "Your handbook doesn't have a remote work policy and you're remote-first. Want one?"
- Check HRIS field: "You said your HRIS is [system] — want me to run the leave tracker now to see if anything is open?"
- If manual leave tracking: "You don't have an HRIS leave module — I'll track leaves in a register file. Use /employment-legal:log-leave to add any leaves that are currently open."

**Before your first review**: make sure the primary source is reachable. For a populated non-`usa` code that is the portal in `references/jurisdictions/<code>/MANIFEST.md` → `research_tool` (for `ksa`: `python3 scripts/fetch-law.py --portal boe --id <guid> --lang ar`, GUIDs in `references/jurisdictions/<code>/SOURCES.md`; the built-in web-fetch tool rejects the portal's TLS chain, use the script or `curl`), and citations from it carry `[BOE — Arabic]` or `[BOE — official English]`. For `usa`, connect a research tool (CourtListener / Westlaw). Without a source, I'll flag every citation as unverified — with one, I verify them against the primary text. In Cowork: Settings → Connectors. In Claude Code: authorize when a skill prompts you.

<!-- COLLATERAL LINKS: when onboarding collateral exists, add here:
     "Want a walkthrough? [Watch the 3-minute intro](URL) or [read the getting-started guide](URL)." -->


### Close with the "you can change anything later" note

After writing the configuration, say:

> "Done. Your configuration is at `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/employment-legal/CLAUDE.md` — a plain text file you can read and edit directly. Anything you answered can be changed:
>
> - Edit the file directly for a quick change
> - Run `/employment-legal:cold-start-interview --redo` for a full re-interview
> - Run `/employment-legal:cold-start-interview --check-integrations` to re-check what's connected
>
> The settings people adjust most: the **jurisdiction list** (as your footprint grows), the **playbook defaults** you accepted from the jurisdiction file, the **output language**, the **high-risk termination flags** (as you calibrate what's actually scary vs. what's noise), and the **escalation matrix** (as reporting lines shift). `/employment-legal:customize` changes one of these at a time."

## Your practice profile learns

After writing the configuration, close with this note:

> **Your practice profile learns.** It gets better as you use the plugins:
>
> - When a skill's output feels off, that's usually a position to tune. The output will tell you which one.
> - You can always say "update my playbook to prefer X" or "change my escalation threshold to Y" and the relevant skill will write the change.
> - Run `/employment-legal:cold-start-interview --redo <section>` to re-interview one part, or edit the config file directly.
>
> Ten minutes of setup gets you a working profile. A month of use gets you one that reads like you wrote it yourself.
