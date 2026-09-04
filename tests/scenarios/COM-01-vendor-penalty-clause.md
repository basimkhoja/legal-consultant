# COM-01 — Vendor agreement with a penalty clause under the primary jurisdiction's law

**Skill:** `/commercial-legal:review` (routes to `vendor-agreement-review`)

**Profile fixture.** `## Jurisdiction`: primary `ksa`, footprint none, output language bilingual, currency SAR, calendar from the manifest, local counsel "N/A". Purchasing-side playbook configured with a 12-month liability cap position and "never accept uncapped indirect damages". Role: non-lawyer with attorney access.

**Input.** A services agreement (paste or attach) between the company as customer and a vendor, governed by "the laws of the Kingdom of Saudi Arabia", with: (a) a clause fixing "a penalty of 10% of the total contract value per week of delay, payable irrespective of any loss suffered, which the parties agree is not subject to reduction"; (b) an exclusion of the vendor's liability "for any loss whatsoever, including loss caused by gross negligence"; (c) an assignment clause letting the vendor assign the whole contract without consent; (d) a 6-month limitation period for claims; (e) interest at 8% on late payments.

**Expected behaviours.**
1. Step 0 runs: the reviewer note records `Jurisdiction: ksa; files: civil-transactions-law.md, …`.
2. Finding on (a) cites the Civil Transactions Law articles on pre-agreed compensation and judicial reduction (Arts. 178-179 in `civil-transactions-law.md`), states that the court may reduce it, disallow it where no harm occurred, and that the "not subject to reduction" wording is ineffective because the rule cannot be contracted out; the article is quoted or the row is named; the tag `[settled — last confirmed 2026-09-04] [BOE — Arabic]` or the file citation appears.
3. Finding on (b) cites the rule that liability for fraud or gross fault cannot be excluded (Art. 173) and rates the clause 🔴 or 🟠.
4. Finding on (c) cites the consent requirement for assignment of the whole contract (Art. 255).
5. Finding on (d) cites the rule that limitation periods cannot be shortened by agreement (Art. 305) and gives the statutory period.
6. Finding on (e) flags the interest clause `[review]` with the position from the file (pre-agreed compensation on a money debt barred, Art. 178; Sharia position tagged model knowledge).
7. The memo has the work-product header for a non-lawyer, the jurisdiction disclaimer line in English and Arabic, and an Arabic rendering of the bottom line and the findings table.
8. Any recomputed exposure number carries the `[computed — …; inputs: …]` tag.

**Forbidden behaviours.**
- Any mention of California, New York, UCTA, the Consumer Rights Act, or "penalty clauses are unenforceable" as a general common-law rule.
- Applying the US delta table.
- Stating a Saudi rule that is not in the ksa files without `[model knowledge — verify]` or `[no rule in ksa files — verify]`.
- Dollar signs in the memo.

**Scoring.** Pass only if 1-7 all appear and no forbidden behaviour appears.
