# EMP-01 — Termination of an indefinite-contract employee

**Skill:** `/employment-legal:termination-review`

**Profile fixture.** `## Jurisdiction`: primary `ksa`, output bilingual, currency SAR; headcount by nationality given; contract types "indefinite (Qiwa-documented)"; statutory end-of-service per `labor-law.md`; no top-up; local counsel "N/A".

**Input.** "We want to terminate Ahmed, a Saudi national on an indefinite contract, hired 2021-03-01, last basic wage SAR 12,000 plus SAR 3,000 housing allowance, for repeated lateness after two written warnings. Planned termination date 2026-09-30. We will give notice today."

**Expected behaviours.**
1. Step 0 runs; the facts step asks for anything missing that the ksa file needs (e.g. whether the warnings followed the work regulations; whether the worker is on any leave) rather than age or decisional unit.
2. The termination ground is mapped to the Labor Law articles (Art. 75 notice with legitimate reason vs Art. 80 grounds) with the file's rows cited; the notice period is stated as 60 days from the employer and the notice date computed against the manifest calendar with a provenance tag.
3. **End-of-service award computed** from Arts. 84-85 with inputs shown: last wage (with the file's position on whether the housing allowance is part of the wage, and `[review]` if the file leaves it open), service period, employer-initiated termination (full award), half-month per year for the first five years then one month per year, fractions pro rata. The number carries `[computed — labor-law.md Arts. 84-85, settled 2026-09-04; inputs: …]`.
4. **Art. 77 exposure computed** for the case where the reason is found illegitimate: 15 days' wage per year of service, two-month floor, contractual figure prevails if any; tagged the same way.
5. Nitaqat impact of losing a Saudi employee is noted from `saudization-nitaqat.md`; Qiwa termination, GOSI deregistration, and final settlement timing from `platform-obligations.md` and `labor-law.md` Art. 88.
6. Dispute route and the 12-month limitation from `labor-dispute-route.md` (Art. 234).
7. Output has the disclaimer and an Arabic rendering of the bottom line and the numbers table.

**Forbidden.** The words "at-will", "OWBPA", "COBRA", "WARN", "FMLA", "decisional unit"; a severance formula not from the file; a computed number without inputs; citing Art. 222 or Art. 224 as current law.
