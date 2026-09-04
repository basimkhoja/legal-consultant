# COR-03 — Entity compliance tracker for an LLC and a JSC

**Skill:** `/corporate-legal:entity-compliance --init` then `--report --days 90`

**Profile fixture.** As COR-01 with Entity Management active; entity table: one `ksa` LLC (registry number given, financial year ending 31 December) and one `ksa` unlisted JSC.

**Expected behaviours.**
1. Tracker entries use `jurisdiction_code: ksa`, `entity_type_local`, `registry_number`; filings come from `filing-calendar.md` indexed by entity type: the LLC and the JSC get different assembly/audit rows.
2. Rows tagged model knowledge in the file (ZATCA, GOSI, Qiwa deadlines) are written with `status: unconfirmed` and the report says they must be confirmed with the accountant or filing agent before they drive an alert; rows read from the Companies Law and Commercial Register Law carry their settled tag.
3. The report's dates are computed against the manifest calendar; no "franchise tax" or "Secretary of State".

**Forbidden.** Delaware March 1 / June 1 rows for a `ksa` entity; `registered_agent: CT Corp`.
