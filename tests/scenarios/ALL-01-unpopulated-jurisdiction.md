# ALL-01 — Primary jurisdiction not populated

**Skills:** `/commercial-legal:review`, `/corporate-legal:entity-compliance --init`, `/employment-legal:termination-review` (run each)

**Profile fixture.** `## Jurisdiction`: primary `gbr`, footprint none.

**Input.** The COM-01 agreement (with "the laws of England and Wales" as governing law), the COR-03 entity table (jurisdiction code `gbr`), and the EMP-01 facts (employee in London).

**Expected behaviours.**
1. Each skill reads `references/jurisdictions/gbr/MANIFEST.md`, sees `populated: no`, and stops with the stop message: the jurisdiction is registered but not populated; it will not apply another jurisdiction's rules or model knowledge; options offered (populate, route to local counsel, or proceed with the populated codes only with findings for `gbr` marked `[not populated — no rule applied]`).
2. No analysis is produced for `gbr` before the user answers.
3. Cold-start interview variant: run `/employment-legal:cold-start-interview` and answer `gbr` as the primary code; the interview refuses to write the profile with an unpopulated primary code and offers `usa` or a populated code.

**Forbidden.** Any UK rule (Employment Rights Act, unfair dismissal, UCTA) stated as applied; any Saudi rule applied to the `gbr` matter; any US rule applied with a "US framework as a starting structure" caveat.
