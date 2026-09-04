# COR-01 — LLC diligence run

**Skill:** `/corporate-legal:diligence-issue-extraction` (or `tabular-review` with the M&A template)

**Profile fixture.** `## Jurisdiction`: primary `ksa`, output bilingual, currency SAR. M&A module active, buy-side, materiality "contracts above SAR 500,000".

**Input.** A small data room (5-8 documents, synthetic): the target's commercial register extract showing an LLC with two partners, one a Saudi individual holding 51% and one a foreign company holding 49%; articles of association; a MISA investment registration certificate dated two years ago listing "IT consulting"; a GOSI statement showing 3 months of unpaid contributions; a Qiwa establishment page showing a Nitaqat band; a management agreement under which the foreign partner "manages all operations and receives 95% of profits"; a distribution agreement with a European principal not registered with the Ministry of Commerce; three customer contracts with change-of-control termination rights.

**Expected behaviours.**
1. Step 0 runs; the jurisdiction category overlay adds, and the findings cover: Tasattur exposure from the 95%-profits management arrangement (cites `anti-concealment-law.md`), MISA registration validity and activity match (cites `investment-law.md`), Nitaqat band and consequences (cites `saudization-nitaqat.md`), GOSI arrears (cites `social-insurance-law.md`), Commercial Agencies registration (cites `commercial-agencies-law.md`), UBO filing status (cites `ultimate-beneficial-ownership-rules.md`), pre-emption on the share transfer and the losses rule (cites `companies-law.md`), change-of-control assignment consent (cites `civil-transactions-law.md` Arts. 98/255), and a merger-control threshold check (cites `competition-law.md`).
2. Each finding carries the file's tag; anything the files do not settle (e.g. the exact Nitaqat coefficients) is tagged `[model knowledge — verify]` or `[no rule in ksa files — verify]`.
3. Severity uses the canonical scale; the Tasattur finding is 🔴.
4. Output has the disclaimer and the Arabic rendering of the findings table.

**Forbidden.** Successor-liability doctrines (de facto merger, mere continuation), HSR, CFIUS, Delaware good-standing certificates, "Corp/LLC" US typing, dollar signs.
