# CLAUDE.md

Guidance for working on this repo. `claude-for-legal` is a Claude Code plugin
marketplace — twelve first-party legal plugins, one vendor plugin, and five
managed-agent cookbooks. Most work here is editing prompt content (skills,
agents, hooks), plugin metadata, or cookbook config — not application code.

## Layout

```
.claude-plugin/marketplace.json   # the marketplace manifest — one entry per plugin
<plugin>/                         # 12 first-party plugins (commercial-legal, privacy-legal, ...)
  .claude-plugin/plugin.json      # plugin manifest (name, version, description, author)
  .mcp.json                       # MCP servers the plugin connects to
  CLAUDE.md                       # practice-profile TEMPLATE (see "Plugin CLAUDE.md" below)
  README.md                       # per-plugin docs
  skills/<name>/SKILL.md          # one skill per directory
  agents/<name>.md                # subagent definitions
  hooks/hooks.json                # hook config (most plugins ship an empty stub)
  .gitignore
external_plugins/<vendor>/        # vendor-maintained plugins (CoCounsel)
managed-agent-cookbooks/<name>/   # CMA agent.yaml + subagents/ + steering-examples.json
scripts/                          # validate.py, lint-tool-scope.py, orchestrate.py,
                                  # deploy-managed-agent.sh, test-cookbooks.sh
references/                       # shared templates (company-profile, dashboard)
```

## Validation — run before opening a PR

This repo follows the same conventions `anthropics/claude-plugins-official`
enforces in CI. Run the equivalent checks locally:

```bash
# 1. Marketplace + per-plugin schema validation (source of truth)
claude plugin validate .claude-plugin/marketplace.json
for d in */; do [ -f "$d/.claude-plugin/plugin.json" ] && claude plugin validate "$d"; done
claude plugin validate external_plugins/cocounsel-legal

# 2. Cookbook tool-scope lint (orchestrators must not over-grant tools)
python3 scripts/lint-tool-scope.py

# 3. JSON/YAML sanity
python3 -c "import json,glob; [json.load(open(f)) for f in glob.glob('**/*.json', recursive=True)]"
```

### Marketplace invariants (I1–I11)

`claude-plugins-official` layers these on top of the schema check. They apply
here too — the ones most likely to trip a contributor:

- **I1** — `plugins[]` should be alpha-sorted by name (case-insensitive).
  *Currently a known warning: the array is in a curated display order. If you
  add a plugin, ask before re-sorting the whole array.*
- **I2** — no duplicate plugin names.
- **I3** — `description` 10–2000 chars, no leading/trailing whitespace.
- **I8** — every vendored `source` (`"./<dir>"`) must point at a directory that
  contains `.claude-plugin/plugin.json`.
- **I9** — `source` paths/URLs must contain no shell metacharacters or `..`.
- **I10** — no hidden Unicode (zero-width chars, bidi controls) in
  `name`/`description`.
- **I11** — `name` must match `^[a-z0-9][a-z0-9-]{1,63}$`.

### Frontmatter requirements

Every `agents/*.md` needs `name` and `description`. Every
`skills/<name>/SKILL.md` needs `description`. Every `commands/*.md` needs
`description`. Multi-line descriptions use `>` block scalars and that's fine —
`claude plugin validate` parses them correctly.

## Conventions

### Keep `marketplace.json` in sync with `plugin.json`

For first-party plugins, `marketplace.json`'s `name`, `description`, and
`author` should match the plugin's own `.claude-plugin/plugin.json` field for
field. If you change a plugin's description in one place, change it in the
other.

### Skill names in prose must be canonical

When a `SKILL.md` (especially `customize` or `cold-start-interview`) tells the
user "run `/foo`," `foo` must be the actual `skills/<foo>/` directory name.
Short forms like `/triage` for `/use-case-triage` look right in prose but are
dead commands — the user types them and nothing happens. Refs to Claude Code
built-ins (`/mcp`, `/plugin`) and to other plugins (`/<other-plugin>:<skill>`)
are fine.

### Plugin CLAUDE.md is a template, not project context

Each `<plugin>/CLAUDE.md` is a practice-profile template that the
`cold-start-interview` skill copies to `~/.claude/plugins/config/claude-for-legal/<plugin>/CLAUDE.md`
on the user's machine. It is *not* loaded as project context when the plugin is
installed — `claude plugin validate` warns about this and the warning is
expected. Don't "fix" it by moving the content into a skill.

### `external_plugins/` is vendor-maintained

Plugins under `external_plugins/` are built and maintained by the vendor
(README.md has the policy). Don't change vendor-authored content without
checking with them first; whitespace normalization and formatting are usually
fine since the vendor lands changes via PR rather than mirroring a fork.

### Formatting

- 2-space indent in all JSON and `.mcp.json` files.
- Final newline at end of every text file.
- No trailing whitespace.
- Markdown tables: pipe-aligned columns are nice but not required; just keep
  the column count consistent.

## Cookbooks

Each `managed-agent-cookbooks/<name>/` has `agent.yaml` (the orchestrator),
`subagents/*.yaml` (the leaves), `steering-examples.json`, and `README.md`. Two
rules that `scripts/lint-tool-scope.py` enforces:

1. The orchestrator gets local-only tools (`read`, `grep`, `glob`,
   `agent_toolset`); MCP and write tools belong to specific subagent leaves.
2. The README's security table and the `agent.yaml` comments must match what
   the YAML actually grants. Don't claim a tool a subagent doesn't have.

## Things to leave alone

- Per-plugin `.gitignore` files differ slightly across plugins. Probably
  intentional; ask before unifying.
- `hooks/hooks.json` is missing in two plugins. Hooks are optional; the missing
  files are not a bug.
- `references/` lives only at repo root and is not shipped inside any plugin
  directory. Several plugin `CLAUDE.md` templates reference it as if it were —
  that's a known gap, not a thing to silently move.

---

## Legal Consultant fork (jurisdiction-pluggable edition)

This repository is `basimkhoja/legal-consultant`, a fork of
`anthropics/claude-for-legal`. Everything above this line is upstream's
guidance and still applies. The fork's full brief is `KICKOFF_PROMPT.md` at
the repo root; read it before any work on this fork. The fork-specific
contributor notes live in `CONTRIBUTING-LEGAL-CONSULTANT.md` (written in
Phase 4).

### Scope

- Plugins in scope: `commercial-legal`, `corporate-legal`, `employment-legal`.
  Every other plugin is left untouched so upstream merges stay clean.
- Jurisdictions: doctrine lives under `references/jurisdictions/<code>/`
  (ISO 3166 alpha-3 lowercase). `ksa` is populated first; `gbr`, `fra`, `che`
  are phase-two stubs; `usa` is reserved for upstream's implicit doctrine.
  `references/jurisdictions/REGISTRY.md` lists every folder and its status.
- Runtimes: Claude Code (this marketplace layout), OpenAI Codex CLI
  (`.agents/` + `AGENTS.md`), Gemini CLI (`gemini-extension/` + `GEMINI.md`).
  Adapters are generated by `scripts/build-runtimes.py`; never hand-edit them.

### Working rules (summary; the kickoff file is authoritative)

1. Doctrine only from primary sources, tagged. Source hierarchy: official
   legislation portal text in the authoritative language > official English
   translation > issuing ministry or authority page > law-firm commentary.
   Every rule carries article, instrument, effective date, and one of
   `[settled — last confirmed YYYY-MM-DD]` (primary text read on that date)
   or `[model knowledge — verify]`.
2. Check for amendments issued after the model's training cutoff (mid-2026)
   before tagging anything settled.
3. Never delete the shared guardrails in any plugin `CLAUDE.md`. Add to them.
   Replace US doctrine tables inside skills; do not merely caveat them.
4. Stay mergeable with upstream: additive files over rewrites, keep
   invariants I1–I11, run the validators before every commit.
5. Commit at the end of every phase with the phase in the message. Never
   push without asking. Never commit client documents (`*.pdf`, `*.docx`,
   `*.xlsx`, `client-docs/` are gitignored).
6. No confident wrong answers. If a rule cannot be confirmed from a primary
   source, the skill says so and stops ("no silent supplement"), encoded in
   the skill itself, not only in the guardrail.
7. Ask before scope changes: a fourth plugin, a different config path
   scheme, or touching another plugin's skill.

### Jurisdiction architecture

- Skills branch on the practice profile's primary jurisdiction and footprint
  list, never on a hard-coded country. Skill prose says "the applicable
  jurisdiction file".
- An unpopulated jurisdiction (`MANIFEST.md` says `populated: no`) is a hard
  stop. No fallback to another jurisdiction's doctrine.
- Multi-jurisdiction matters run the relevant files side by side and label
  every finding with its jurisdiction code.
- Authoritative language and source portal come from the manifest. Output is
  English plus the authoritative language when the profile asks for it.
- Nothing outside the jurisdiction folders and the profile carries a country
  name.

### Runtime-neutral config path

Practice profiles live at
`${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/<plugin>/CLAUDE.md`.
Upstream's `~/.claude/plugins/config/claude-for-legal/<plugin>/CLAUDE.md` is
the legacy path: a populated profile found there is copied forward once,
following upstream's own migration rule. Phase 4 replaces every hard-coded
path with this scheme.


### Where to start in a fresh session

Read `docs/TRACKER.md` first: it lists the remaining tasks one per session, what
to read for each, and what not to load. Then `docs/phase-reports.md` for what
is already done. Do not reload the doctrine files or the inventory unless a
task names them.

### Fork scripts

- `scripts/fetch-law.py` — fetch an instrument from an official portal (`boe` adapter); renders amendment blocks, warns on repealed laws.
- `scripts/build-jurisdiction-index.py <code>` — regenerate `INDEX.md`; refuses untagged rule rows; `--check` in CI.
- `scripts/sync-jurisdictions.py` — copy `references/jurisdictions/` into the in-scope plugins; `--check` in CI.
- `scripts/build-runtimes.py` — generate `.agents/`, `AGENTS.md`, `gemini-extension/`; `--check` in CI.
- Validation order before a commit is in `CONTRIBUTING-LEGAL-CONSULTANT.md`.

### Git authorship

Commits are authored as Basim Khoja <basim.khoja@gmail.com>.
