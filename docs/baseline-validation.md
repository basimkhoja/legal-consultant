# Baseline validation — untouched upstream tree

Recorded in Phase 0 so pre-existing warnings are not mistaken for regressions.

- Fork base: `anthropics/claude-for-legal` commit `4a6c651889c97cc9140580363c73e0eb17379c2b` ("Update plugin content (#104)")
- Date run: 2026-09-04
- Branch: `multi-jurisdiction`
- Python: 3.14 (user site). `pyyaml 6.0.3` and `jsonschema 4.26.0` installed with `pip install --user` because the tree does not vendor them.

## Results

| Check | Command | Result | Notes |
|---|---|---|---|
| Marketplace manifest | `claude plugin validate .claude-plugin/marketplace.json` | PASS | No warnings. |
| Per-plugin manifests (12 first-party) | `for d in */; do claude plugin validate "$d"; done` | PASS with 1 warning each | Warning on every plugin: "CLAUDE.md at the plugin root is not loaded as project context." Expected per upstream root `CLAUDE.md` ("Plugin CLAUDE.md is a template, not project context"). Do not fix. |
| Vendor plugin | `claude plugin validate external_plugins/cocounsel-legal` | PASS | No warnings. |
| Tool-scope lint | `python3 scripts/lint-tool-scope.py` | PASS | 5 cookbooks clean: diligence-grid, docket-watcher, launch-radar, reg-monitor, renewal-watcher. |
| Schema validator | `python3 scripts/validate.py` | N/A | This script validates a managed-agent output JSON against a schema (two positional args). It is not a repo-wide validator. With no args it prints usage and exits 2. Nothing to baseline. |
| JSON sanity | `python3 -c "import json,glob; [json.load(open(f)) for f in glob.glob('**/*.json', recursive=True)]"` | PASS | |

## Pre-existing warnings to ignore later

1. The "CLAUDE.md at the plugin root is not loaded as project context" warning on all 12 first-party plugins.
2. Invariant I1 (alpha-sorted `plugins[]`) is a known, accepted warning upstream: the array is in curated display order. `claude plugin validate` did not surface it in this run.

## Phase 5 comparison rule

A validator run passes if its output matches this baseline exactly, plus any new checks added by the fork (build-freshness check from Phase 4).
