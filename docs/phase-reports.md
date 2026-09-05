# Phase reports

One entry per phase, in the format the kickoff asks for: what was done, what was verified, what is open, and the next phase's first action. Rules that could not be confirmed from a primary source are consolidated in `docs/open-questions-ksa-2026-09-04.md`.

## Phase 0 — Repository setup (2026-09-04)

**Done.** Forked `anthropics/claude-for-legal` to `basimkhoja/legal-consultant`. The project folder itself is the repo root (it held only the kickoff file and one research note, neither of which collides with upstream paths), not a `repo/` subfolder. Remotes `origin` (fork) and `upstream` (Anthropic); branch `multi-jurisdiction` from `main` at upstream commit `4a6c651`. Root `CLAUDE.md` gained an appended fork section (scope, rules, jurisdiction architecture, the runtime-neutral config path) so upstream merges stay clean. `.gitignore` refuses `*.pdf`, `*.docx`, `*.xlsx`, `client-docs/`. Project memory saved.

**Verified.** All validators run on the untouched tree: marketplace and 12 plugin manifests pass; the only warning is "plugin-root CLAUDE.md is not loaded as project context" on every plugin, which upstream documents as expected. `lint-tool-scope.py` clean. `validate.py` is a two-argument cookbook validator, not a repo check. Baseline in `docs/baseline-validation.md`.

**Open.** None.

## Phase 1 — US doctrine audit (2026-09-04)

**Done.** `docs/us-doctrine-inventory.md`: 298 doctrine rows (commercial 75, corporate 92, employment 131), 76 cold-start interview rows, 53 config-path rows. Actions: 73 replace, 126 branch, 99 leave.

**Verified.** Every row carries a file and line from the audited commit. The three silent-wrong-answer rows are called out: the renewal tracker's Saturday/Sunday weekend and US-holiday fallback, vendor review's provisional "US jurisdiction" default, and the leave logger's hard-coded FMLA deadlines.

**Open.** Two doctrine gaps have nothing to swap and must be authored per jurisdiction: e-signature validity and penalty-clause enforceability (both now covered by ksa files).

## Phase 2 — Doctrine reference layer, ksa (2026-09-04)

**Done.** `references/jurisdictions/ksa/`: `MANIFEST.md`, `SOURCES.md`, generated `INDEX.md`, and 26 instrument files, 803 rule rows, of which 743 were read from the primary text on 2026-09-04 and 60 are model knowledge. Stubs for `gbr`, `fra`, `che`; `REGISTRY.md`. Copies synced into the three in-scope plugins. `docs/doctrine-coverage.md` maps all 295 non-path inventory rows to files. Amendment watch in `docs/amendment-watch-2026-09-04.md` (leads only; the ones that matter were confirmed or flagged inside the files).

**Verified.** Twenty-one instruments fetched from laws.boe.gov.sa with `scripts/fetch-law.py`; twelve official English translations; sixteen authority documents (HRSD, MoC, MISA, CMA, GAC, SDAIA, MoJ, SCCA). Every rule row carries exactly one provenance tag in the Tag column, enforced by `scripts/build-jurisdiction-index.py`. Post-cutoff check against the portal's updates log found one new instrument (Enforcement Law, Royal Decree M/237, in force 2026-10-28), added as a file; no amendment to the Companies Law.

**Source defects found and fixed during the phase.** (1) The portal keeps the original article text in the body and amendments in per-article pop-ups; the first extractor dropped the pop-ups. The fetcher now renders both, and every affected file was re-checked. (2) The first Competition Law fetched was the repealed 1425H law; replaced with the 1440H law, and the fetcher now warns on repealed status. (3) The updates-log date first read against the Companies Law belonged to the adjacent entry.

**Open.** 220 items in `docs/open-questions-ksa-2026-09-04.md`. The ones with the widest effect: the HRSD friendly-settlement rules and Ministerial Decision 115921 are scanned PDFs that could not be read; the Wage Protection System, Nitaqat 2026 phase, GOSI rate schedule, and ZATCA calendar are model knowledge; the Commercial Courts implementing regulation read is the published project text; the UBO Rules' decision number (99 vs 267) is unresolved.

**Next.** Phase 3: wire the skills, starting with the shared jurisdiction-resolution step and the commercial review skills' delta table.

## Phase 3 — Wire the skills (2026-09-04)

**Done.** Every skill and agent in the three plugins carries "Step 0: Resolve the applicable jurisdiction" (canonical wording in `references/jurisdictions/JURISDICTION-STEP.md`) and a list of the jurisdiction files it loads. US doctrine sits under "When the applicable code is `usa`"; the jurisdiction-file branch sits beside it and is the default for any other code. Commercial: the enforceability check from the Civil Transactions Law replaces the delta table; calendar and currency come from the manifest and profile; bilingual title routing. Corporate: tracker keyed by jurisdiction code and local entity type; filing calendar, diligence overlay, consent and minutes formalities from the files. Employment: end-of-service award (Step 2a) and Art. 77 compensation (Step 2b) computed with inputs and provenance tags; leave register with regime codes; hiring, classification, wage-hour, policy branches. Plugin `CLAUDE.md` templates gained a `## Jurisdiction` section, the disclaimer line, the bilingual house-style rule, the fork tags, and the Step 0 dispatcher. Cold-start interviews rewritten around jurisdiction facts and `playbook-defaults.md`, refusing an unpopulated primary code. Versions 2.0.0. `docs/doctrine-coverage.md` Done column filled for all 295 rows.

**Verified.** `claude plugin validate` passes on all three plugins and the marketplace; JSON and tool-scope lint pass; Step 0 present in 37 skill and agent files; residual US terms all inside `usa` branches or examples.

**Open.** Points the reference files cannot fill, listed by each editor and carried as `[no rule in ksa files — verify]` in the skills: fee shifting, foreign governing-law enforceability practice, privilege position, IP recordal at SAIP, MAC clauses, successor liability, CMA continuing obligations, collective-dismissal rules, interview rights in investigations, overtime divisor.

## Phase 4 — Multi-runtime packaging (2026-09-04)

**Done.** Config path `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/<plugin>/CLAUDE.md` in all three plugins (54 files), with the upstream config and cache paths kept as one-time legacy sources in the migration rule. `scripts/build-runtimes.py` generates the Codex adapter (`.agents/skills/<plugin>-<skill>/`, `legal-consultant-jurisdictions` skill, `AGENTS.md`) and the Gemini extension (`gemini-extension/` with `gemini-extension.json`, `GEMINI.md`, skills, and `/plugin:skill` commands); `--check` for CI. `docs/runtime-matrix.md`, `docs/upstream-sync.md`, `CONTRIBUTING-LEGAL-CONSULTANT.md`, `README-LEGAL-CONSULTANT.md`.

**Verified.** Build is deterministic and `--check` passes after regeneration; all validators pass.

**Open.** Gemini extension install from GitHub depends on whether the CLI accepts a sub-folder manifest; the README gives the local-path route as the fallback. Neither adapter ships MCP servers.

## Phase 5 — Validation and scenarios (2026-09-04, partial)

**Done.** 14 scenario files in `tests/scenarios/`, synthetic fixtures in `tests/fixtures/`, and 16 scenario runs in the Claude Code runtime, all PASS (`tests/results/2026-09-04-summary.md` and the three per-plugin logs).

**Verified.** Required behaviours confirmed: gratuity computed with a provenance tag and no at-will language; the Civil Transactions Law reduction rule cited on the penalty clause; Tasattur, MISA, and Nitaqat checked in the LLC diligence; a stop with no supplement when the portal is unreachable in each plugin; a stop with nothing applied when the primary jurisdiction is `gbr`.

**Open.** The Codex CLI and Gemini CLI runs did not complete (process stopped for low memory; API spend limit reached in the same window). Six skill-text friction items from the runners are queued (listed in the summary file). The per-plugin result files were written by the runners before the spend limit cut their final messages; their content is complete.

**Update 2026-09-05.** The six friction fixes are applied (T1). The four Codex CLI runs are complete and all PASS (T2, `tests/results/2026-09-05-codex.md`; fixes to the fetcher's TLS fallback and the generated `AGENTS.md`, no skill text). The Gemini CLI runs are blocked before the first model call: the account's free OAuth tier is rejected by the CLI (`IneligibleTierError`); extension linked, setup findings recorded in `tests/results/2026-09-05-gemini.md` and `docs/runtime-matrix.md`; the runs need a `GEMINI_API_KEY` or Vertex credential (T3, partial).

**Update 2026-09-05 (T8).** The doctrine layer was updated for the 1448H Government Tenders and Procurement Law (Royal Decree M/76 of 27/2/1448H, gazette 2026-09-04, in force 2027-01-02 per the file's computation with a one-day `[review]`): `references/jurisdictions/ksa/government-tenders-procurement-law.md` now carries the 101-article law as the in-force set, read from the Official Gazette page and tagged `[authority — Umm Al-Qura gazette]` pending the portal listing, with the 2019 rows kept as the repealed set and a matter-date rule in the header; the skill lines that cited the file in the three plugins now route by matter date; the implementing regulations were not yet issued.

**Next.** Re-run the four required scenarios in Codex and Gemini one at a time, apply the six friction fixes, then Phase 6 (push after your go-ahead, switch the installed plugins, run the three cold-start interviews with you, first acceptance test on the stc documents).
