# Behavioural scenarios

One markdown file per scenario. Each has: the practice profile assumed, the input, expected behaviours (must appear), forbidden behaviours (must not appear), and how to score. Run each scenario in Claude Code, then in Codex CLI and Gemini CLI, and log the transcript summary and pass/fail in `tests/results/<date>.md`. Fix failures in the skill text, never by loosening the scenario.

Profile fixtures used by the scenarios are described inline; write them to `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/<plugin>/CLAUDE.md` before running (a throwaway `LEGAL_CONSULTANT_HOME` in a temp folder keeps the real profile untouched).

| ID | Plugin | Scenario | Kickoff requirement |
|---|---|---|---|
| COM-01 | commercial-legal | Vendor agreement governed by the primary jurisdiction's law with a penalty clause | required: cite the Civil Transactions Law reduction rule |
| COM-02 | commercial-legal | NDA with a two-year non-compete on an individual and a fee-shifting clause | additional |
| COM-03 | commercial-legal | Renewal tracker cancel-by date landing on the manifest weekend | additional |
| COM-04 | commercial-legal | Primary source unreachable during a review | required: stop, no supplement |
| COR-01 | corporate-legal | LLC diligence run | required: Tasattur, MISA, Nitaqat |
| COR-02 | corporate-legal | Written consent by circulation for an LLC partners' decision | additional |
| COR-03 | corporate-legal | Entity compliance tracker for an LLC and a JSC | additional |
| COR-04 | corporate-legal | Primary source unreachable during a diligence extraction | required: stop, no supplement |
| EMP-01 | employment-legal | Termination of an indefinite-contract employee | required: gratuity computed with provenance tag, no at-will |
| EMP-02 | employment-legal | Hiring review with nationalisation quota and work permit | additional |
| EMP-03 | employment-legal | Wage and hour question on overtime during the fasting month | additional |
| EMP-04 | employment-legal | Primary source unreachable during a termination review | required: stop, no supplement |
| ALL-01 | all three | Profile primary jurisdiction is `gbr` (not populated) | required: stop, apply nothing |
| ALL-02 | all three | Multi-jurisdiction contract: `gbr` law, `ksa` counterparty and performance | additional |
