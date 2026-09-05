# Upstream sync

## Base

| Field | Value |
|---|---|
| Upstream | `https://github.com/anthropics/claude-for-legal` (Apache 2.0) |
| Fork | `https://github.com/basimkhoja/legal-consultant` |
| Base commit | `4a6c651889c97cc9140580363c73e0eb17379c2b` — "Update plugin content (#104)" |
| Fork branch | `multi-jurisdiction` (from `main` at the base commit) |
| Remotes | `origin` = fork, `upstream` = Anthropic |
| Marketplace name | `legal-consultant` (renamed from upstream's `claude-for-legal` on 2026-09-05 so both marketplaces can be configured side by side; plugin ids are `<plugin>@legal-consultant`) |
| First push | 2026-09-05: `multi-jurisdiction` pushed to `origin` at `644f6d6` ("B1: OCR the HRSD scanned decisions"), then `6b7f7c8` (marketplace rename). `main` is still at the base commit, not merged. The marketplace is added from the branch: `claude plugin marketplace add basimkhoja/legal-consultant#multi-jurisdiction` (the CLI accepts the `#ref` form, so no merge to `main` was needed). |

## What the fork changes, by merge risk

| Area | Fork change | Merge risk |
|---|---|---|
| Root `CLAUDE.md` | Appended fork section at the end | Low: append-only |
| `.gitignore` | Appended rules | Low |
| `commercial-legal/`, `corporate-legal/`, `employment-legal/` `CLAUDE.md` | Inserted `## Jurisdiction` section, disclaimer and bilingual rule in `## Outputs`, fork tags in the tag vocabulary, "Fork addition" under Jurisdiction recognition, new profile fields | Medium: insertions inside upstream sections; conflicts resolve by keeping both |
| The three plugins' `skills/*/SKILL.md` and `agents/*.md` | Step 0 inserted before the first workflow step; US content wrapped under "When the applicable code is `usa`"; jurisdiction-file branches beside it; config path replaced | Medium to high on skills upstream rewrites; resolve by re-applying the fork's branch around the new upstream text |
| The three plugins' `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` | Version 2.0.0 | Low: take the fork's version |
| `<plugin>/references/jurisdictions/` | New (generated copy) | None: upstream has no such folder |
| `references/jurisdictions/`, `scripts/fetch-law.py`, `scripts/sync-jurisdictions.py`, `scripts/build-jurisdiction-index.py`, `scripts/build-runtimes.py`, `docs/`, `tests/`, `.agents/`, `AGENTS.md`, `gemini-extension/`, `CONTRIBUTING-LEGAL-CONSULTANT.md`, `README-LEGAL-CONSULTANT.md`, `KICKOFF_PROMPT.md` | New | None |
| Every other plugin | Untouched | None |

## Merge procedure

```bash
git fetch upstream
git checkout multi-jurisdiction
git merge upstream/main            # or: git rebase upstream/main, if the fork has not been shared
```

Then, in this order:

1. Resolve conflicts in the three plugin `CLAUDE.md` files by keeping upstream's new text and re-inserting the fork's blocks (they are marked "Fork addition" or sit under `## Jurisdiction`).
2. Resolve conflicts in skills by keeping upstream's new step text and re-wrapping: the fork's "Step 0" block stays first; any US table upstream changed goes back under "When the applicable code is `usa`"; the jurisdiction-file branch beside it is re-read against `references/jurisdictions/<code>/INDEX.md` in case an instrument file name changed.
3. Re-run the config-path replacement if upstream added new `~/.claude/plugins/config/claude-for-legal/` references: `grep -rn "plugins/config/claude-for-legal" commercial-legal corporate-legal employment-legal`.
4. If upstream added a skill to an in-scope plugin, add Step 0 to it and record the new US doctrine rows in `docs/us-doctrine-inventory.md` and `docs/doctrine-coverage.md`.
5. Regenerate and validate:

```bash
python3 scripts/sync-jurisdictions.py
python3 scripts/build-runtimes.py
python3 scripts/build-jurisdiction-index.py ksa --check
python3 scripts/sync-jurisdictions.py --check
python3 scripts/build-runtimes.py --check
claude plugin validate .claude-plugin/marketplace.json
for d in commercial-legal corporate-legal employment-legal; do claude plugin validate "$d"; done
python3 scripts/lint-tool-scope.py
```

6. Re-run the scenarios in `tests/scenarios/` and log the results in `tests/results/<date>.md`.
7. Update the base commit in this file.

## Contributing back

Changes that are jurisdiction-neutral (the Step 0 mechanism, the calendar-from-manifest rule, the currency field, the registry pattern) are candidates for an upstream pull request. The doctrine files are not: upstream's policy is that skills do not store jurisdiction-specific rules.
