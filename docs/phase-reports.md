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
