# Kickoff prompt: Legal Consultant (jurisdiction-pluggable edition of claude-for-legal)

Paste everything below the line into Claude Code opened in this folder. Phases 2 and 3 carry legal judgment and should run on the strongest model available. Phases 0, 4, 5, and 6 are mechanical and can run on Sonnet.

---

You are building Legal Consultant, a jurisdiction-pluggable fork of Anthropic's `claude-for-legal` plugin marketplace. It will be my base legal assistant for commercial, corporate, and labor work. The first jurisdiction is the Kingdom of Saudi Arabia; the United Kingdom, France, and Switzerland are planned as a second phase, so nothing may be named or structured as Saudi-only. It must run on three agent runtimes: Claude Code, OpenAI Codex CLI, and Gemini CLI.

## Ground truth already established

- Upstream is `https://github.com/anthropics/claude-for-legal` (Apache 2.0). Local clone of the marketplace is at `~/.claude/plugins/marketplaces/claude-for-legal`. Read its root `CLAUDE.md` and `CONTRIBUTING.md` first. Their rule "put the doctrine in the skill, the CLAUDE.md guardrails are only the net" is the design principle this fork follows.
- Installed at user scope from Anthropic's marketplace, all version 1.0.2: `commercial-legal`, `corporate-legal`, `employment-legal`, `privacy-legal`, `regulatory-legal`. These will be replaced by the fork at the end. Do not uninstall them until Phase 6.
- `~/.claude/plugins/config/claude-for-legal/` does not exist. No cold-start interview has been run. Do not run one until Phase 3 is complete, because the upstream interview writes a US-shaped profile.
- The three plugins in scope are `commercial-legal`, `corporate-legal`, and `employment-legal`. Leave every other plugin untouched so upstream merges stay clean.
- Jurisdiction handling upstream is a caveat, not knowledge: a shared "Jurisdiction recognition" guardrail detects non-US matters and tags output as unverified. Skills refuse to state law from memory and require a legal research connector (Westlaw, CourtListener) that has no Saudi coverage. The commercial vendor review carries a hard-coded US/EU/UK jurisdiction delta table. The employment plugin is built around at-will employment, FMLA, FLSA, and US states. The corporate entity tracker is Delaware-centric with a `custom_jurisdictions` escape hatch.
- I work at Norconsult Telematics in Riyadh. Outputs must be bilingual, English and Arabic, matching my existing case documents. My email for git authorship is basim.khoja@gmail.com.

## Non-negotiable working rules

1. **Doctrine only from primary sources, tagged.** Source hierarchy: Bureau of Experts Arabic text (laws.boe.gov.sa) > Bureau of Experts official English translation > issuing ministry or authority page (HRSD, Ministry of Commerce, MISA, ZATCA, CMA, GOSI, Qiwa) > law-firm commentary. Every rule carries the article number, the instrument, the effective date, and one of the plugin's own tags: `[settled — last confirmed YYYY-MM-DD]` only when you read the primary text on that date, otherwise `[model knowledge — verify]`. Law-firm summaries may guide research but are never the cited source.
2. **Check for changes after June 2026.** Your training data ends around then. Before tagging anything settled, search the Bureau of Experts portal and the issuing authority for amendments issued after that date.
3. **Never delete the shared guardrails** in any plugin `CLAUDE.md`. Add to them. Replace US doctrine tables inside skills; do not merely caveat them.
4. **Stay mergeable with upstream.** Prefer additive files (new reference files, new skill steps) over rewrites. Keep the marketplace invariants I1 to I11 listed in the upstream root `CLAUDE.md`. Run the validators before every commit.
5. **Commit at the end of every phase** with a message that names the phase. Never push without asking me. Never commit client documents; add a `.gitignore` rule for `*.pdf`, `*.docx`, `*.xlsx`, and a `client-docs/` folder in Phase 0.
6. **No confident wrong answers.** If a rule for any jurisdiction cannot be confirmed from a primary source, the skill must say so and stop, exactly as the upstream "no silent supplement" rule requires. Encode that behavior in the skill, not just in the guardrail.
7. **Ask before scope changes.** Adding a fourth plugin, changing the config path scheme, or touching another plugin's skill is a scope change.

## Jurisdiction architecture (applies to every phase)

- **One folder per jurisdiction** under `references/jurisdictions/<code>/`, using ISO 3166 alpha-3 lowercase codes: `ksa` now, `gbr`, `fra`, `che` in phase two, `usa` reserved for upstream's implicit doctrine. Every folder has the same layout: `MANIFEST.md` (jurisdiction name, legal family, authoritative language, official source portal, populated yes/no, last-reviewed date), `INDEX.md`, `SOURCES.md`, and one file per instrument. A `references/jurisdictions/REGISTRY.md` lists every folder and its populated status.
- **Skills branch on the practice profile, never on a hard-coded country.** Each skill reads the profile's primary jurisdiction and footprint list, then loads `references/jurisdictions/<code>/` for each. Skill text says "the applicable jurisdiction file", not "the Saudi file".
- **Unpopulated jurisdiction is a hard stop.** If the profile names a jurisdiction whose `MANIFEST.md` says not populated, the skill reports that and stops, exactly like the upstream "no silent supplement" rule. It never falls back to another jurisdiction's doctrine.
- **Multi-jurisdiction matters.** When a matter spans jurisdictions (for example a UK-law contract with a Saudi counterparty), the skill runs the relevant jurisdiction files side by side and labels every finding with its jurisdiction code.
- **Language and source portal come from the manifest.** For `ksa` the authoritative language is Arabic and the portal is laws.boe.gov.sa. For phase two: legislation.gov.uk, legifrance.gouv.fr, fedlex.admin.ch. The bilingual-output rule generalises to "English plus the authoritative language when the profile asks for it".
- **Nothing outside the jurisdiction folders and the profile may carry a country name.** Repo name, config path, build scripts, README, and skill prose stay neutral.

## Phase 0: Repository setup

1. Confirm `gh auth status` works, then fork `anthropics/claude-for-legal` to my GitHub account as `legal-consultant` and clone it into this folder (the repo root becomes this folder, or a `repo/` subfolder if this folder already has files; tell me which you chose).
2. Add upstream: `git remote add upstream https://github.com/anthropics/claude-for-legal.git`. Create a branch `multi-jurisdiction` from `main`.
3. Write a project `CLAUDE.md` at the repo root for this fork that points to this kickoff file, states the working rules above, and records the runtime-neutral config path decided in Phase 4.
4. Save a first project memory: the fork decision, the three plugins in scope, the source hierarchy, and the phase plan.
5. Run the upstream validators once on the untouched tree to establish a clean baseline, and record any pre-existing warnings so they are not mistaken for regressions later.

Deliverable: forked repo on the `multi-jurisdiction` branch, baseline validation log in `docs/baseline-validation.md`.

## Phase 1: US doctrine audit

1. For each of the three plugins, inventory every place a US-specific rule, statute, agency, state list, entity type, filing calendar, or research connector is assumed. Record file and line, what the rule is, and whether it needs replacing, branching, or leaving alone. Search terms to start with: at-will, FLSA, FMLA, CFRA, WARN, ADA, EEOC, DOL, NLRB, Delaware, DGCL, LLC, C-corp, Section 220, UCC, Westlaw, CourtListener, California, New York, Texas, governing law, choice of law, work product.
2. Inventory every hard-coded path to `~/.claude/plugins/config/claude-for-legal/` because Phase 4 must make it runtime-neutral.
3. Inventory each cold-start interview question that assumes a US practice so Phase 3 can rewrite it.

Deliverable: `docs/us-doctrine-inventory.md` with three tables (doctrine, paths, interview questions). This is the checklist Phase 3 works against.

## Phase 2: Doctrine reference layer, first jurisdiction: Saudi Arabia

Create `references/jurisdictions/ksa/` at the repo root plus a copy or symlink inside each in-scope plugin (the upstream root `CLAUDE.md` notes that `references/` is not shipped inside plugins, so plugins must carry their own copy). One markdown file per instrument, plus `INDEX.md` listing every file with its instrument, decree number, effective date, last-confirmed date, and source URL, plus `SOURCES.md` describing the source hierarchy.

Each file has the same structure: instrument and decree number; scope; effective date and amendment history; a rules table with columns Article, Rule (English), Rule (Arabic), Practical effect, Tag; a section "Open questions for a Saudi practitioner"; and a section "How skills should use this file".

Cover at minimum:

**Commercial**
- Civil Transactions Law, Royal Decree M/191 of 1444H, in force 16 December 2023: contract formation, good faith, damages, liquidated damages and judicial reduction, limitation and exclusion of liability, force majeure, hardship, assignment, prescription periods.
- Commercial Courts Law and its implementing regulations: jurisdiction, procedure, enforcement of foreign judgments, interim relief.
- Arbitration Law and the Saudi Center for Commercial Arbitration rules: arbitrability, seat, enforcement.
- Commercial Agencies Law and its regulations.
- Commercial Register Law and Trade Names Law (2024 reforms).
- Bankruptcy Law: preventive settlement, financial restructuring, liquidation, effect on contracts.
- Government Tenders and Procurement Law: relevant because my counterparties are often government-linked entities like stc.
- Personal Data Protection Law and its implementing regulations: only the provisions that a commercial contract review must check (processing clauses, cross-border transfer, breach notification).
- E-Commerce Law and Electronic Transactions Law: e-signature validity for contract execution.

**Corporate**
- Companies Law, Royal Decree M/132 of 1443H, in force 30 December 2022, and the implementing regulations of January 2023: entity types (LLC, JSC, simplified JSC, partnerships, professional and non-profit companies), formation, governance, shareholder rights, manager and director duties, capital rules, mergers and conversions, dissolution.
- Ministry of Commerce and Capital Market Authority corporate governance regulations, as applicable to listed and unlisted companies.
- Investment Law of 2024 and Ministry of Investment licensing for foreign-owned entities.
- Ultimate beneficial ownership rules.
- Filing calendar for the entity tracker: Ministry of Commerce annual obligations, ZATCA zakat, income tax, and VAT, GOSI, Qiwa, Chamber of Commerce, and municipality licenses. Index by entity type, not just by jurisdiction, mirroring the upstream Delaware split warning.
- Anti-Concealment Law (Tasattur).
- Competition Law merger-control thresholds, as a diligence checklist item.

**Labor**
- Labor Law, Royal Decree M/51 of 1426H as amended by Royal Decree M/44 of 1445H, in force 19 February 2025: contract types and fixed-term conversion, probation, working hours and Ramadan hours, overtime, annual, sick, maternity, paternity, and bereavement leave, notice periods (60 days from the employer and 30 from the employee on indefinite contracts), Article 74 to 81 termination grounds, Article 77 compensation, end-of-service gratuity computation under Article 84 and 85, resignation mechanics, non-compete and confidentiality limits, women and minors provisions.
- Implementing regulations of the Labor Law and HRSD ministerial decisions on model contracts, work permits, and the Wage Protection System.
- Saudization and Nitaqat: bands, sector quotas, consequences of non-compliance.
- Social Insurance Law and GOSI contributions.
- Labor dispute route: Friendly Settlement at HRSD, Labor Courts, limitation period for claims.
- Qiwa and Musaned platform obligations where they create legal duties.
- Occupational safety obligations at the level a termination or hiring review must check.

Also create `references/jurisdictions/gbr/`, `fra/`, and `che/` containing only a `MANIFEST.md` marked not populated, so the stop rule can be tested in Phase 5, and write `REGISTRY.md`.

**Amendment watch.** The `last30days` skill (installed on this machine) pulls the last 30 days of practitioner discussion from Reddit, X, YouTube, Hacker News, GitHub, and the web. Use it at the start of this phase and again before Phase 6 as a lead generator for recent amendments, ministerial decisions, and enforcement news for the jurisdiction. It is never a citable source: every lead it surfaces must be confirmed on the official portal before it enters a reference file. Record the query and the leads in `docs/amendment-watch-<date>.md`.

Deliverable: the `references/jurisdictions/` tree with `ksa` populated and the phase-two stubs, and a short `docs/doctrine-coverage.md` that maps each Phase 1 inventory row to the reference file that replaces it, or states that a Saudi practitioner must confirm it.

## Phase 3: Wire the skills

Work through `docs/us-doctrine-inventory.md` row by row.

1. **Jurisdiction branching.** Where a skill applies a US table, add a Saudi branch that loads the matching `references/jurisdictions/ksa/` file. The practice profile's primary jurisdiction is the default branch. Saudi Arabia is the only populated jurisdiction today; the US path stays reachable when the footprint includes the US, and any unpopulated jurisdiction must trigger the stop rule from the jurisdiction architecture section.
2. **Research step.** Replace the Westlaw and CourtListener research steps with a Bureau of Experts research step: fetch the instrument page on laws.boe.gov.sa (or the issuing authority) with the available web fetch tool, quote the article, and tag the citation `[BOE — Arabic]` or `[BOE — official English]`. Keep the "no silent supplement" stop if the fetch fails.
3. **Commercial review.** Replace the jurisdiction delta table with the Saudi equivalent (liquidated damages reduction, exclusion-of-liability limits, non-compete limits, governing law and Saudi court enforceability, e-signature validity, PDPL clauses). Add a Saudi playbook section to the `CLAUDE.md` template with defaults for governing law, dispute forum, and SCCA arbitration.
4. **Corporate.** Add the Saudi entity types and filing calendar to the entity-compliance skill, add Saudi diligence categories (Tasattur, MISA license, Saudization status, GOSI arrears, ZATCA standing) to the diligence and tabular-review column sets, and add Saudi board and shareholder resolution formalities to written-consent and board-minutes.
5. **Labor.** Rewrite the termination review, hiring review, worker classification, wage-and-hour Q&A, leave tracker, and policy drafting around the Labor Law. Add a computed end-of-service gratuity step with the provenance tag on the number itself, and an Article 77 compensation step. Add Nitaqat and work-permit checks to hiring review.
6. **Cold-start interviews.** Rewrite each plugin's interview so it asks about Saudi facts: commercial registration number, entity type, MISA license, Nitaqat band, GOSI registration, headcount by nationality, sectors, default governing law and forum, Arabic or bilingual output preference, and whether Saudi counsel is available for escalation.
7. **Bilingual output.** Add a house-style rule to every template: deliverables are produced in English with an Arabic rendering of the bottom line, the findings table, and any counterparty-facing text. Arabic legal terms use the Bureau of Experts glossary spellings.
8. Add the Saudi law disclaimer to every output header: Arabic text is authoritative, English translations are for convenience, and a licensed Saudi lawyer must review before reliance.

Deliverable: modified skills and templates, `docs/doctrine-coverage.md` updated with a done column, and version bumped to 2.0.0 in each in-scope `plugin.json` and in `marketplace.json`.

## Phase 4: Multi-runtime packaging

Design principle: one canonical source, generated adapters. Nothing is hand-duplicated across runtimes.

1. **Canonical source.** Skills stay in the Agent Skills format (`skills/<name>/SKILL.md` with `name` and `description` frontmatter), which Claude Code, Codex CLI, and Gemini CLI all read natively. The doctrine layer stays in `references/jurisdictions/`, all jurisdictions, and every adapter ships the whole tree.
2. **Runtime-neutral config path.** Replace every hard-coded `~/.claude/plugins/config/claude-for-legal/` path with `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/<plugin>/CLAUDE.md`, keeping the upstream migration rule that copies a populated profile forward from the old path. Document this in the repo `CLAUDE.md`.
3. **Claude Code adapter.** The existing marketplace layout is the adapter. No extra work beyond the path change.
4. **Codex adapter.** Generate `.agents/skills/<plugin>-<skill>/SKILL.md` at the repo root from the canonical skills, and write `AGENTS.md` at the repo root carrying the shared guardrails from the three plugin `CLAUDE.md` templates, because Codex does not read plugin `CLAUDE.md` files. Document installing to `~/.agents/skills` for use outside this repo. Note MCP servers are configured in `~/.codex/config.toml` and list the ones that matter.
5. **Gemini adapter.** Generate a Gemini extension folder `gemini-extension/` with `gemini-extension.json`, `GEMINI.md` carrying the same guardrails, and `skills/<name>/SKILL.md` copies, plus TOML custom commands under `commands/` that map to the main skills so `/commercial-review` style commands exist. Document `gemini extensions install` from the local path and from GitHub.
6. **Build script.** Write `scripts/build-runtimes.py` that generates the Codex and Gemini adapters from canonical source, fails if a generated file is stale, and is documented in `CONTRIBUTING-LEGAL-CONSULTANT.md`. Add a check to the validation step in Phase 5.
7. Verify the sub-features that do not port: Claude Code subagents under `agents/`, hooks, and scheduled agents have no direct equivalent in Codex or Gemini. Document what each runtime gets and does not get in `docs/runtime-matrix.md`.

Deliverable: `AGENTS.md`, `GEMINI.md`, `.agents/`, `gemini-extension/`, `scripts/build-runtimes.py`, `docs/runtime-matrix.md`.

## Phase 5: Validation and test scenarios

1. Run `claude plugin validate` on the marketplace and each in-scope plugin, `scripts/validate.py`, `scripts/lint-tool-scope.py`, the JSON sanity check, and the Phase 4 build-freshness check. All must pass or match the Phase 0 baseline.
2. Write `tests/scenarios/` with at least three scenarios per plugin as markdown: the input, the expected behaviors, and the forbidden behaviors. Required scenarios include: a termination of an indefinite-contract employee where the skill must compute gratuity with a provenance tag and must not mention at-will employment; a vendor agreement governed by Saudi law with a penalty clause where the skill must cite the Civil Transactions Law reduction rule; an LLC diligence run where the skill must check Tasattur, MISA, and Nitaqat; one scenario per plugin where the primary source is unreachable and the skill must stop rather than supplement; and one scenario where the profile's primary jurisdiction is `gbr` (not populated) and the skill must stop without applying Saudi or US doctrine.
3. Run each scenario in Claude Code and record the transcript summary and pass or fail in `tests/results/<date>.md`. Then run the same scenarios in Codex CLI and Gemini CLI, and record differences.
4. Fix failures in the skill text, not by loosening the scenario.

Deliverable: passing validators, scenario files, and a results log.

## Phase 6: Release and switch-over

1. Write `README-LEGAL-CONSULTANT.md`: what changed from upstream, install instructions for all three runtimes, the config path, the source hierarchy, the disclaimer, and a "How to add a jurisdiction" section that walks through creating a new `references/jurisdictions/<code>/` folder, populating its manifest, and running the Phase 5 scenarios against it. This section is the entry point for the UK, France, and Switzerland phase.
2. Ask me before pushing. After push: `/plugin marketplace add basimkhoja/legal-consultant`, uninstall the five Anthropic-sourced plugins, install the three plugins from the fork at user scope, then run the three rewritten cold-start interviews with me.
3. Record the upstream commit SHA the fork is based on in `docs/upstream-sync.md` with the merge procedure for future updates.
4. First real acceptance test: run the commercial review on the stc documents in `~/Projects/AI Quickies/04 - stc SEA Penalty Reuse` and log the result in `tests/results/`.

Deliverable: pushed repo, plugins switched, cold-start complete, first acceptance test logged.

## How to report

At the end of each phase, give me a short summary: what was done, what was verified, what is open, and the next phase's first action. Flag any rule you could not confirm from a primary source in a single list so I can take it to Saudi counsel.
