# Tracker: remaining work, one task per fresh session

Each task below is written so a fresh Claude Code session can pick it up cold, with a small context budget. Start every session the same way, then do exactly one task, commit, tick the status table, and stop.

## Session bootstrap (every task)

1. The root `CLAUDE.md` fork section loads automatically. Read **only** these three files before starting: `.planning/TRACKER.md` (this file), `docs/phase-reports.md`, and the task's own "Read first" list. Do not read `KICKOFF_PROMPT.md`, the 26 doctrine files, `docs/us-doctrine-inventory.md`, or `docs/doctrine-coverage.md` unless the task names them; they are large and already applied.
2. Confirm the tree is clean and the validators pass (about 60 seconds):
   ```bash
   git status --short && git log --oneline -3
   python3 scripts/build-jurisdiction-index.py ksa --check && python3 scripts/sync-jurisdictions.py --check && python3 scripts/build-runtimes.py --check
   for d in commercial-legal corporate-legal employment-legal; do claude plugin validate "$d" | grep -E "✔|✖"; done
   ```
   The validators need `pyyaml` and `jsonschema` (`pip install --user pyyaml jsonschema`).
3. Do not spawn more than one subagent at a time; the 2026-09-04 session lost three parallel runs to the API spend limit and a memory kill. One task, one session.
4. Never push, never uninstall or install plugins, and never write to `~/.legal-consultant` unless the task says so and Basim has confirmed in that session.
5. Finish by: committing with a message that names the task ID, ticking the status table below, and adding one line to `docs/phase-reports.md` if the task closes a phase.

## Status

| ID | Task | Status | Session / commit |
|---|---|---|---|
| T1 | Apply the six skill-text friction fixes from the Claude Code runs | done | 2026-09-05, commit "T1: skill-text fixes from the 2026-09-04 scenario runs" |
| T2 | Run the four required scenarios in Codex CLI and log | done | 2026-09-05, commit "T2: Codex CLI scenario runs"; all four PASS; fetcher and AGENTS.md fixes for the Codex sandbox (`tests/results/2026-09-05-codex.md`) |
| T3 | Run the four required scenarios in Gemini CLI and log | blocked on credentials (partial) | 2026-09-05, commit "T3 (partial): Gemini CLI setup findings; scenario runs blocked on auth"; extension linked, `--consent`/trust/skill-conflict facts recorded; every `gemini -p` call fails with `IneligibleTierError` (free OAuth tier); needs `GEMINI_API_KEY` or Vertex, then rerun per `tests/results/2026-09-05-gemini.md` |
| T4 | Rerun the amendment watch before release and confirm leads on the portal | open | |
| T5 | Phase 6a: push, add the marketplace, switch the installed plugins | open, needs Basim's go-ahead | |
| T6 | Phase 6b: run the three cold-start interviews with Basim | open, interactive | |
| T7 | Phase 6c: first acceptance test on the stc documents | open | |
| B1 | Backlog: OCR the two scanned HRSD PDFs and settle their rows | backlog | |
| B2 | Backlog: Saudi counsel review of `docs/open-questions-ksa-2026-09-04.md` | backlog | |
| B3 | Backlog: populate `gbr`, `fra`, `che` (phase two) | backlog | |
| B4 | Backlog: propose the jurisdiction-neutral mechanism upstream | backlog | |

Done before this tracker existed: Phases 0 to 4 in full, Phase 5 for the Claude Code runtime (16 scenario runs, all PASS). See `docs/phase-reports.md`.

---

## T1 — Apply the six skill-text friction fixes

**Why.** The Claude Code scenario runners passed every scenario but recorded six places where the skill text is ambiguous. None changed a verdict; all are cheap.

**Read first.** `tests/results/2026-09-04-summary.md` (the "Friction" list), then the "Skill-text observations" section at the end of each of `tests/results/2026-09-04-claude-code-commercial-legal.md`, `…-corporate-legal.md`, `…-employment-legal.md` (use `grep -n "Skill-text observations"` and read from there; do not read the whole files). Then only the skill files named there.

**Do.**
1. `references/jurisdictions/JURISDICTION-STEP.md` item 5 and every skill's copy of it: after "report the failure and stop", add what the stopped run still emits (the reviewer note with the portal status, the options list, nothing tagged `[BOE — Arabic]`). Because skills carry the block verbatim, edit the canonical file first, then replace the block in every skill with a script (`grep -rl "### Step 0: Resolve the applicable jurisdiction"`), not by hand.
2. Hijri dates: in `commercial-legal/skills/vendor-agreement-review/SKILL.md` (about line 332) either drop the "add the Hijri date" instruction or point it at `[model knowledge — verify]` explicitly. Prefer dropping it; there is no converter in the repo.
3. `corporate-legal/skills/written-consent/SKILL.md` Step 1 conflict check: cite the LLC manager rows of `references/jurisdictions/ksa/companies-law.md` for LLCs, and Art. 71 only for JSC boards.
4. `employment-legal/skills/wage-hour-qa/SKILL.md` Step 2b: state which inputs are mandatory (basic wage, hours) and which are flagged `[review]` when absent (allowances forming part of the actual wage).
5. `tests/scenarios/EMP-01-termination-gratuity.md`: change the forbidden word "WARN" to "WARN Act".
6. Any other observation in the three lists that is a one-line change; skip anything needing a doctrine decision and note it in `docs/open-questions-ksa-2026-09-04.md` instead.
7. `python3 scripts/sync-jurisdictions.py && python3 scripts/build-runtimes.py`, then the validators from the bootstrap.

**Done when.** Validators pass, `build-runtimes.py --check` passes, commit "T1: skill-text fixes from the 2026-09-04 scenario runs".

**Context budget.** Small. About 40k tokens.

---

## T2 — Codex CLI scenario runs

**Why.** Kickoff Phase 5 step 3 requires the scenarios to run in Codex CLI and the differences to be recorded. Not done on 2026-09-04.

**Read first.** `tests/scenarios/README.md`, then the four scenario files `EMP-01`, `COM-01`, `COR-01`, `ALL-01`, and `tests/results/2026-09-04-summary.md` (the "Codex CLI and Gemini CLI runtimes" section has the commands). Nothing else.

**Do.**
1. Stage the profiles: `H=$(mktemp -d); cp -R tests/fixtures/profiles/ksa "$H/ksa"; cp -R tests/fixtures/profiles/gbr "$H/gbr"`.
2. Run ONE scenario at a time, foreground, with a 25-minute timeout, from the repo root so Codex discovers `.agents/skills` and `AGENTS.md`:
   ```bash
   LEGAL_CONSULTANT_HOME=$H/ksa codex exec -s read-only -C "$PWD" --skip-git-repo-check "<prompt>" > tests/results/raw/EMP-01-codex.md 2> tests/results/raw/EMP-01-codex.err
   ```
   Prompt shape (adapt per scenario): "Use the $employment-legal-termination-review skill and run it as written. The practice profile is at $H/ksa/employment-legal/CLAUDE.md (read that absolute path). The jurisdiction tree is at references/jurisdictions/ in this repository. Facts: tests/fixtures/inputs/EMP-01-termination-facts.md. Today is <date>. Produce the full deliverable including the computed numbers with inputs and tags, the disclaimer line, and the bilingual rendering. Do not ask questions; state assumptions inline with [review] tags." For ALL-01 use `$H/gbr` and the London variant from the scenario file.
3. Grade each output against the scenario's Expected and Forbidden lists, item by item, quoting evidence. Write `tests/results/<date>-codex.md` with a summary table, per-scenario grading, and a "Differences from Claude Code" section (compare with the same scenario in the 2026-09-04 files).
4. If a FAIL is caused by skill text, fix the canonical skill (never the `.agents/` copy), regenerate with `scripts/build-runtimes.py`, rerun that one scenario.

**Done when.** Four graded runs logged, fixes (if any) committed as "T2: Codex CLI scenario runs".

**Context budget.** Medium. Each Codex output is 5 to 15k tokens; read them one at a time.

---

## T3 — Gemini CLI scenario runs

**Why.** Same requirement as T2 for Gemini CLI.

**Read first.** As T2, plus the "Runtime findings" section of `tests/results/2026-09-05-codex.md`: Codex's sandbox blocked the portal fetch twice (no network in `read-only`; no Keychain in `workspace-write`), fixed by `scripts/fetch-law.py`'s `--cacert` fallback. Check first whether Gemini's sandbox has the same limits; if the fetch fails, look for `curl: (60)` or `Could not resolve host` in the raw log before blaming the skill.

**Do.**
1. Link the extension from the checkout: `gemini extensions link "$PWD/gemini-extension"` and confirm with `gemini extensions list`. (Uninstall afterwards only if Basim says so; leaving it linked is part of the switch-over.)
2. Stage profiles as in T2. Run one scenario at a time:
   ```bash
   LEGAL_CONSULTANT_HOME=$H/ksa gemini -p "<prompt>" --approval-mode plan > tests/results/raw/EMP-01-gemini.md 2> tests/results/raw/EMP-01-gemini.err
   ```
   In the prompt, name the skill as "the employment-legal-termination-review skill in the legal-consultant extension"; the `/employment-legal:termination-review` command form also works interactively.
3. Grade and log as in T2, in `tests/results/<date>-gemini.md`, with the "Differences from Claude Code" section.
4. If the GitHub install form (`gemini extensions install https://github.com/basimkhoja/legal-consultant`) is tested and fails because the manifest is in a sub-folder, record that in `docs/runtime-matrix.md` and `README-LEGAL-CONSULTANT.md` and leave the local-path route as primary.

**Done when.** Four graded runs logged, commit "T3: Gemini CLI scenario runs".

**Context budget.** Medium, as T2.

---

## T4 — Amendment watch before release

**Why.** The kickoff requires the `last30days` amendment watch to run again before Phase 6, and every lead to be confirmed on the official portal before it enters a file.

**Read first.** `docs/amendment-watch-2026-09-04.md` (structure and the three queries), `references/jurisdictions/ksa/SOURCES.md` (the GUID table and the post-cutoff check table). Nothing else.

**Do.**
1. Run the three queries through the `last30days` skill; write `docs/amendment-watch-<date>.md` in the same structure. The skill is a lead generator only.
2. For each lead that names an instrument in the GUID table: `python3 scripts/fetch-law.py --portal boe --id <guid> --lang ar --out /tmp/x.md` and compare the `articles marked as amended` count and the status line with the values in `SOURCES.md`; also re-read the portal updates log (`https://laws.boe.gov.sa/boelaws/laws/lawupdated/1?PageNumber=1&LanguageId=1&IsDisplayWithUpdated=True`, pages 1 to 3, with `curl`).
3. If an instrument changed: update the affected rows in its file (read only that file), set the `Post-cutoff amendment check` field, rebuild the index, sync, regenerate adapters. If nothing changed, add a dated row to the post-cutoff table in `SOURCES.md` saying so.
4. Also check whether HRSD has published a text version of the friendly-settlement rules or Decision 115921 (see B1); if so, note it for B1.

**Done when.** New watch file, `SOURCES.md` updated, validators pass, commit "T4: amendment watch <date>".

**Context budget.** Small to medium. Do not open more than one instrument file.

---

## T5 — Phase 6a: push and switch the installed plugins

**Blocked on Basim.** Ask at the start of the session: "May I push `multi-jurisdiction` to `origin` and switch the installed plugins?" Do nothing below until the answer is yes.

**Read first.** `README-LEGAL-CONSULTANT.md` (Install section), `docs/upstream-sync.md`.

**Do, in order.**
1. `git push -u origin multi-jurisdiction`. Do not merge into `main` unless Basim asks; the marketplace can be added from the branch (`/plugin marketplace add basimkhoja/legal-consultant#multi-jurisdiction` if the CLI accepts a ref; otherwise merge to `main` first with his go-ahead).
2. In Claude Code: `/plugin marketplace add basimkhoja/legal-consultant`.
3. Uninstall the five upstream plugins at user scope: `commercial-legal@claude-for-legal`, `corporate-legal@claude-for-legal`, `employment-legal@claude-for-legal`, `privacy-legal@claude-for-legal`, `regulatory-legal@claude-for-legal`. Note the fork carries `privacy-legal` and `regulatory-legal` unchanged; reinstall those two from the fork too if Basim wants them.
4. Install `commercial-legal`, `corporate-legal`, `employment-legal` from `legal-consultant` at user scope; run `claude plugin list` and `claude plugin validate` on the installed cache to confirm version 2.0.0.
5. For Codex: copy `.agents/skills/*` to `~/.agents/skills/` and append `AGENTS.md` to `~/.codex/AGENTS.md` if Basim wants the skills outside the repo. For Gemini: the link from T3, or `gemini extensions install <local path>`.
6. Record the upstream commit SHA and the push in `docs/upstream-sync.md` (already lists the base; add the push date).

**Done when.** `claude plugin list` shows the three fork plugins at 2.0.0 and none from `claude-for-legal`; commit "T5: Phase 6a switch-over" (docs only).

**Context budget.** Small.

---

## T6 — Phase 6b: cold-start interviews with Basim

**Interactive.** Run with Basim present, one plugin per session if needed: `/commercial-legal:cold-start-interview`, `/corporate-legal:cold-start-interview`, `/employment-legal:cold-start-interview`. Each writes `~/.legal-consultant/<plugin>/CLAUDE.md` and the shared `~/.legal-consultant/company-profile.md`.

**Read first.** Nothing beyond the bootstrap; the skill carries its own flow. Useful to know: the interview offers the rows of `references/jurisdictions/ksa/playbook-defaults.md` one by one; it must refuse an unpopulated primary code; Basim's facts are Norconsult Telematics, Riyadh, bilingual output, counterparties often government-linked (stc).

**Do.** Run the three interviews; after each, open the written profile and check the `## Jurisdiction` section is filled (primary `ksa`, output language bilingual, calendar, currency SAR, portal, local counsel). Do not commit the profiles (they live outside the repo).

**Done when.** Three populated profiles exist; add a line to `docs/phase-reports.md` under Phase 6.

---

## T7 — Phase 6c: first acceptance test on the stc documents

**Read first.** `tests/scenarios/COM-01-vendor-penalty-clause.md` (as the grading model), `tests/results/2026-09-04-summary.md`.

**Do.**
1. Documents are in `~/Projects/AI Quickies/04 - stc SEA Penalty Reuse`. They are client documents: never copy them into the repo (`*.pdf`, `*.docx`, `*.xlsx`, `client-docs/` are gitignored, but do not rely on that; work from the original folder).
2. Run `/commercial-legal:review` on the agreement(s) with the real profile from T6. Because the counterparty is government-linked, the review should route through `government-tenders-procurement-law.md` scope rows and the Civil Transactions Law penalty rows; the bottom line and findings table should be bilingual.
3. Log `tests/results/<date>-acceptance-stc.md`: what was run, which files and articles were cited, the tags on every number, what Basim judged right and wrong, and the skill-text changes that follow. Describe the documents generically (no client text in the log).

**Done when.** Log committed as "T7: first acceptance test"; any skill fixes committed separately.

---

## Backlog

**B1 — OCR the scanned HRSD PDFs.** `brew install tesseract tesseract-lang` (Arabic pack), then OCR `hrsd-friendly-settlement-rules-ar.pdf` and `hrsd-decision-115921-ar.pdf` (URLs in `references/jurisdictions/ksa/SOURCES.md`; re-download, they are not in the repo). Settle the model-knowledge rows in `labor-dispute-route.md` and the Instrument table of `labor-law-implementing-regulations.md`. Rebuild index, sync, regenerate.

**B2 — Saudi counsel review.** Send `docs/open-questions-ksa-2026-09-04.md` (220 items). When answers come back, record each in the instrument file's row (change the tag only if counsel cites the primary text) and in `~/.legal-consultant/<plugin>/verification-log.md`.

**B3 — Phase two jurisdictions.** Follow `README-LEGAL-CONSULTANT.md`, "How to add a jurisdiction". One jurisdiction per session at most; the `ksa` layer took ten writer agents. Add a portal adapter to `scripts/fetch-law.py` first (legislation.gov.uk, legifrance.gouv.fr, fedlex.admin.ch).

**B4 — Upstream contribution.** The jurisdiction-neutral pieces (Step 0 mechanism, registry pattern, calendar-from-manifest, currency field, `build-runtimes.py`) could go to `anthropics/claude-for-legal` as a PR; the doctrine files cannot (upstream policy). See `docs/upstream-sync.md`.

## Known environment facts

- `laws.boe.gov.sa` fails TLS verification in the Claude Code web-fetch tool; `curl` and `scripts/fetch-law.py` work.
- The portal keeps original article text in the body and amendments in pop-ups; the fetcher renders both, and the last "تعديلات المادة" block is the wording in force.
- The portal lists repealed laws under current-looking titles; the fetcher warns on status `لاغي`.
- `pdftotext` is installed; `tesseract` is not.
- Codex CLI 0.153 and Gemini CLI 0.58 are installed; both have MCP settings files already.
- The 2026-09-04 session's runner subagents were cut off by the account's monthly spend limit; their result files were complete before the cut.
