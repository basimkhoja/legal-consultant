# Employment Counsel Plugin

In-house employment law workflows: hiring review, termination review, policy drafting, handbook updates, jurisdiction-aware wage & hour Q&A. Built around a jurisdictional footprint learned at cold-start — the plugin knows which jurisdictions (and sub-jurisdictions) you're in and what's different about each, and loads the reference files under `references/jurisdictions/<code>/` for every populated jurisdiction code (`usa` keeps the upstream research-per-review path).

**Every output is a draft for attorney review — cited, flagged, and gated — not a legal conclusion.** The plugin does the work: reads the documents, applies your playbook, finds the issues, drafts the memo. A lawyer reviews, verifies, and decides. Citations are tagged by source so you know which ones came from a research tool and which ones need checking. Privilege markers are applied conservatively so nothing waives by accident. Consequential actions — filing, sending, executing — are gated behind explicit confirmation.

## Who this is for

| Role | Primary workflows |
|---|---|
| **Employment counsel** | Termination review, policy drafting, wage/hour analysis |
| **HR business partners** | Hiring review, handbook questions, first-line wage/hour Q&A |
| **GC** | Escalation recipient for high-risk terms and RIFs |

## First run: cold-start

Asks which jurisdiction codes and sub-jurisdictions you have employees in (headcount by nationality, nationalisation band, registrations, contract types, output language, local counsel), offers the jurisdiction's playbook defaults, reads your handbook or work regulations and three recent termination memos, and builds a jurisdiction-aware escalation table. It refuses to write a profile whose primary jurisdiction is unpopulated.

```
/employment-legal:cold-start-interview
```

Your configuration is stored at `~/.claude/plugins/config/claude-for-legal/employment-legal/CLAUDE.md` and survives plugin updates.

## Prerequisites

- **Persistent data path.** The leave register, investigation logs, and expansion trackers are written to `~/.claude/plugins/config/claude-for-legal/employment-legal/`, a version-independent path that survives plugin updates. These files contain privileged and sensitive personnel information — make sure that directory is backed up and access-controlled.
- **Legal research access.** Skills in this plugin do not carry substantive legal rules in their own text. For a populated jurisdiction code the rules are the tagged rows of `references/jurisdictions/<code>/` (cited by article, currency-checked against the primary-source portal named in that jurisdiction's manifest, e.g. `scripts/fetch-law.py --portal boe`); for `usa`, every jurisdiction-specific rule (salary thresholds, restrictive-covenant enforceability, final-pay timing, release consideration periods) is researched and cited at the time of review. An unpopulated jurisdiction is a hard stop, never a fallback to another jurisdiction's rules. Make sure the session has access to the research tools you rely on (the portal script or `curl`, web search, internal legal research integrations, team reference materials).
- **Outside counsel.** No country-specific or jurisdiction-specific legal advice is produced without outside counsel engagement on any close call or new jurisdiction.

## Skills

| Skill | Does |
|---|---|
| `/employment-legal:cold-start-interview` | Cold-start interview — learns jurisdictional footprint + escalation rules from handbook + term memos |
| `/employment-legal:hiring-review` | Offer letter + restrictive covenant review, jurisdiction check |
| `/employment-legal:termination-review` | Termination review with high-risk flag detection |
| `/employment-legal:policy-drafting [topic]` | Draft a policy with jurisdiction supplements where needed (by state for `usa`; by nationality, sector, gender-specific rules or entity type for a populated code) |
| `/employment-legal:wage-hour-qa [question]` | Wage/hour or general employment Q&A, jurisdiction-aware |
| `/employment-legal:worker-classification` | Classify a proposed worker engagement and flag misclassification gaps |
| `/employment-legal:expansion-kickoff [country]` | Kick off international expansion planning for a new country |
| `/employment-legal:expansion-update [country]` | Update an in-progress expansion tracker |
| `/employment-legal:investigation-open` | Open a new internal investigation matter |
| `/employment-legal:investigation-add` | Add documents, interview notes, or observations to an open investigation |
| `/employment-legal:investigation-query` | Ask questions against an open investigation log |
| `/employment-legal:investigation-memo` | Draft or update the privileged investigation memo |
| `/employment-legal:investigation-summary` | Draft an audience-specific summary from the investigation memo |
| `/employment-legal:leave-tracker` | Check open leaves for deadline alerts and required decisions |
| `/employment-legal:log-leave` | Add a new leave to the leave register |
| `/employment-legal:matter-workspace` | Manage matter workspaces (multi-client private practice only) — new, list, switch, close, none |
| **handbook-updates** | Diff proposed changes against current handbook or work regulations, flag jurisdiction-supplement impact and any re-certification step |

Reference skills `internal-investigation` and `international-expansion` carry the detailed frameworks and templates — the per-mode skills above load them as needed.

## Interactive skills vs. scheduled agents

The skills above run when you invoke them — for when you're working a matter. The agents below run on a schedule — for what moves while you're not looking:

| Agent | What it watches | Default cadence |
|---|---|---|
| **leave-tracker** | Open leaves with hard legal clocks — for `usa`: FMLA, state equivalents (CA CFRA, NY PFL), USERRA, ADA leave as accommodation; for a populated code: the statutory leave regimes, pay tiers and protection periods in its jurisdiction file; fires decision-point alerts before deadlines are missed | Weekly (first working day on the jurisdiction's calendar) |

## How it learns

Your practice profile at `~/.claude/plugins/config/claude-for-legal/employment-legal/CLAUDE.md` isn't static — it improves as you use the plugin. Skills tell you when an output used a default you should tune. You can re-run setup, edit the file directly, or tell a skill to record a new position.

## Notes

- Jurisdiction awareness is the whole point. For a populated jurisdiction the plugin computes the end-of-service award, compensation and settlement window from the jurisdiction file and tags every number with its source and inputs; for `usa` it researches the state rule (California final pay and New York's next-regular-payday rule are the classic contrast) at review time.
- Termination review is NOT a replacement for the conversation with HR and the manager. It's a checklist that catches the thing everyone forgot.
- Wage/hour Q&A cites the rule but flags close calls for human review. Classification decisions have consequences.
