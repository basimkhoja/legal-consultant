# EMP-02 — Hiring review with nationalisation quota and work permit

**Skill:** `/employment-legal:hiring-review`

**Profile fixture.** As EMP-01; Nitaqat band "Low Green" for the establishment.

**Input.** "Offer letter for a non-Saudi senior accountant, fixed-term 2 years, probation 6 months, non-compete 3 years nationwide, salary SAR 18,000, start 2026-11-01, to be sponsored by us."

**Expected behaviours.**
1. Step 0 runs; classification (exempt/non-exempt) does not appear.
2. Checks from the files: profession-specific quota for accounting roles and the band consequences (`saudization-nitaqat.md`, with model-knowledge tags where the file is), work permit and sponsorship (`labor-law.md` Arts. 32-40, `platform-obligations.md`), contract contents and Qiwa documentation (Arts. 51-52), probation cap of 180 days flagged against the 6-month proposal (Art. 53), non-compete cut to the two-year written cap and legitimate interest (Art. 83), GOSI occupational-hazards registration (`social-insurance-law.md`).
3. Each flag cites the file row; output bilingual for the counterparty-facing offer text.

**Forbidden.** Pay-transparency, ban-the-box, I-9, salary-history, FLSA exemption.
