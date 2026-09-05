# Legal Consultant

A jurisdiction-pluggable fork of Anthropic's [`claude-for-legal`](https://github.com/anthropics/claude-for-legal) plugin marketplace, for commercial, corporate, and employment work. Version 2.0.0 of the `commercial-legal`, `corporate-legal`, and `employment-legal` plugins; every other upstream plugin is carried unchanged. Runs on Claude Code, OpenAI Codex CLI, and Gemini CLI from one canonical source.

The first populated jurisdiction is the Kingdom of Saudi Arabia (`ksa`). The United Kingdom (`gbr`), France (`fra`), and Switzerland (`che`) are registered as unpopulated stubs; the United States (`usa`) is the upstream doctrine, reachable when it is in the practice profile's footprint.

## What changed from upstream

| Upstream | This fork |
|---|---|
| Jurisdiction handling is a caveat: a guardrail detects non-US matters and tags output as unverified; skills refuse to state law from memory and rely on US research connectors | Jurisdiction handling is knowledge: `references/jurisdictions/<code>/` holds one file per instrument with a rules table, and every skill runs "Step 0: Resolve the applicable jurisdiction" before it reads a document |
| US doctrine tables inside skills (the commercial delta table, the entity-compliance Delaware calendar, at-will/FLSA/FMLA logic) | The US tables sit under "When the applicable code is `usa`"; the jurisdiction-file branch sits beside them and is the default for any other code |
| Unknown jurisdiction: "flag the gap and continue with a US caveat" | Unpopulated jurisdiction: hard stop, no fallback |
| Research step: Westlaw / CourtListener | Research step: the official portal named in the jurisdiction manifest (`scripts/fetch-law.py`), citations tagged `[BOE — Arabic]` / `[BOE — official English]` / `[authority — …]` |
| Saturday/Sunday weekend, US holidays, `$` | Calendar and currency from the manifest and the profile |
| English deliverables, US work-product header | English plus the authoritative language for the bottom line, findings, and counterparty-facing text when the profile asks; a jurisdiction disclaimer line under the header |
| Config at `~/.claude/plugins/config/claude-for-legal/` | Config at `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/<plugin>/CLAUDE.md`; a populated legacy profile is copied forward once |

Full inventory of the changes: `docs/us-doctrine-inventory.md` (what was US-specific) and `docs/doctrine-coverage.md` (what replaced it).

## Install

### Claude Code

```
/plugin marketplace add basimkhoja/legal-consultant#multi-jurisdiction
/plugin install commercial-legal@legal-consultant
/plugin install corporate-legal@legal-consultant
/plugin install employment-legal@legal-consultant
```

The `#multi-jurisdiction` ref is needed while the fork lives on that branch (`main` is still upstream's base commit); the same commands work from the terminal as `claude plugin marketplace add …` and `claude plugin install -s user …`. The fork's `privacy-legal` and `regulatory-legal` are unchanged upstream copies and can be installed the same way if you used them before.

Then run each plugin's cold-start interview (`/commercial-legal:cold-start-interview`, `/corporate-legal:cold-start-interview`, `/employment-legal:cold-start-interview`). The interview writes the profile, including the `## Jurisdiction` section, and offers the jurisdiction's playbook defaults row by row. If you had the upstream plugins installed, uninstall them first; the fork's plugins use the same names.

### OpenAI Codex CLI

From a clone of this repository, the skills are discovered automatically from `.agents/skills/` and the guardrails from `AGENTS.md`. For use outside the repository:

```bash
cp -R .agents/skills/* ~/.agents/skills/
cat AGENTS.md >> ~/.codex/AGENTS.md
```

Invoke a skill with `$commercial-legal-review`, `$employment-legal-termination-review`, and so on, or let Codex pick it by description. MCP servers (Slack, Google Drive, DocuSign, …) go in `~/.codex/config.toml` under `[mcp_servers.<name>]`; none are required for the jurisdiction files.

### Gemini CLI

```bash
gemini extensions install /path/to/legal-consultant/gemini-extension     # from a local clone
gemini extensions install https://github.com/basimkhoja/legal-consultant  # from GitHub, if the CLI accepts a sub-folder manifest; otherwise use the local path
```

Commands are `/commercial-legal:review`, `/corporate-legal:entity-compliance`, `/employment-legal:termination-review`, and so on; the same skills are also selectable by description. Guardrails are in the extension's `GEMINI.md`.

Notes (Gemini CLI 0.58.0, 2026-09-05): add `--consent` when installing or linking from a script, otherwise the command waits on a prompt; headless `gemini -p` runs need a trusted folder (`--skip-trust` or `GEMINI_CLI_TRUST_WORKSPACE=true`); inside a clone the `.agents/skills/` copies trigger a harmless `Skill conflict detected` warning per skill. The free individual OAuth tier is no longer accepted by the CLI (`IneligibleTierError`); use a `GEMINI_API_KEY` or Vertex AI. Details in `docs/runtime-matrix.md`.

What each runtime gets and does not get (subagents, hooks, scheduled runs): `docs/runtime-matrix.md`.

## Config path

`${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/<plugin>/CLAUDE.md`, plus the shared `company-profile.md` one level up. Set `LEGAL_CONSULTANT_HOME` to relocate it (for example to a per-client folder or a test fixture). On first run, a populated profile found at the upstream path is copied forward once.

## Source hierarchy and provenance

Every rule in `references/jurisdictions/<code>/` carries one tag in its Tag column:

- `[settled — last confirmed YYYY-MM-DD]` — the primary text was read on that date, from the source tier named beside it (`[BOE — Arabic]`, `[BOE — official English]`, `[authority — HRSD]`, …).
- `[model knowledge — verify]` — not read from a source; the reader must confirm before relying.

The hierarchy for `ksa`: Bureau of Experts Arabic text > Bureau of Experts official English translation > issuing ministry or authority page > law-firm commentary (never cited). Skills carry the tag onto every finding and onto every computed number, with the inputs. See `references/jurisdictions/ksa/SOURCES.md` for every URL read and the post-cutoff amendment check, and `docs/open-questions-ksa-2026-09-04.md` for the points the texts do not settle.

## Disclaimer

For `ksa` deliverables: **Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance.** النص العربي هو النص المعتمد، والترجمة الإنجليزية للاستئناس فقط، ويجب مراجعة محامٍ سعودي مرخص قبل الاعتماد على هذا المستند. This line is part of every deliverable's header. Nothing this software produces is legal advice.

## How to add a jurisdiction

This is the entry point for the UK, France, and Switzerland phase.

1. **Register the code.** Pick the ISO 3166-1 alpha-3 lowercase code. Create `references/jurisdictions/<code>/MANIFEST.md` from the `gbr` stub: name, legal family, authoritative language(s), source portal, issuing authorities, calendar (weekend, public holidays, calendar system), currency, `populated: no` for now, `research_tool`, provenance tags, output-language rule, disclaimer line in English and the authoritative language. Add the row to `REGISTRY.md`.
2. **Add a portal adapter if needed.** `scripts/fetch-law.py` has one adapter (`boe`). Add one for legislation.gov.uk, legifrance.gouv.fr, or fedlex.admin.ch following the same shape (detail URL, index, attachments, status line, amendment rendering). Test that the fetch tool in your runtime can reach the portal; if not, document the `curl` route in the manifest.
3. **Write `SOURCES.md`** with the hierarchy for that jurisdiction, then fetch every instrument the three plugins need. The list to cover is the kickoff's Phase 2 list translated to local law: contract law (formation, good faith, damages, penalty clauses, exclusion of liability, force majeure, hardship, assignment, limitation), courts and enforcement, arbitration, agencies and distribution, company registry, insolvency, public procurement, data protection as it touches contracts, e-signature; companies law, governance regulations, foreign-investment rules, beneficial ownership, filing calendar by entity type, anti-fraud rules, merger control; labour law, implementing regulations, nationalisation or quota rules, social insurance, dispute route, platform obligations, occupational safety.
4. **Write one file per instrument** from `_TEMPLATE-instrument.md`, following `WRITER-BRIEF` discipline: read the text before writing a row, tag every row, put professional judgement only in Practical effect with inline tags, list open questions, and name the skills and steps that use the file. Add `playbook-defaults.md` with the defaults the cold-start interviews will offer.
5. **Generate and validate.** `python3 scripts/build-jurisdiction-index.py <code>` (it refuses untagged rows), then set `populated: yes` in the manifest, update `REGISTRY.md`, run `scripts/sync-jurisdictions.py` and `scripts/build-runtimes.py`.
6. **Run the scenarios.** Copy the `tests/scenarios/` files, swap the profile fixture to the new code and the inputs to local facts, run them in all three runtimes, and log `tests/results/<date>.md`. The ALL-01 stop scenario must keep passing for every code that is still unpopulated.
7. **Skills need no change** unless the new jurisdiction has a concept the current step structure cannot express (for example a works-council consultation step). In that case add the step under a jurisdiction-file branch, never as a country-named step.

## Repository map

```
references/jurisdictions/     canonical doctrine layer (see CONTRIBUTING-LEGAL-CONSULTANT.md)
commercial-legal/ corporate-legal/ employment-legal/   the three plugins (v2.0.0), each with a synced copy of the tree
.agents/  AGENTS.md            Codex adapter (generated)
gemini-extension/              Gemini adapter (generated)
scripts/                       fetch-law, build-jurisdiction-index, sync-jurisdictions, build-runtimes
docs/                          inventory, coverage, amendment watch, open questions, phase reports, runtime matrix, upstream sync
tests/scenarios/  tests/results/
KICKOFF_PROMPT.md              the brief this fork was built from
```

## Licence

Apache 2.0, as upstream. See `LICENSE`.
