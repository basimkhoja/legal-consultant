# COR-02 — Written consent by circulation for an LLC decision

**Skill:** `/corporate-legal:written-consent`

**Profile fixture.** As COR-01 with the Board & Secretary module active; entity table has one `ksa` LLC with three partners (50 / 30 / 20).

**Input.** "Draft a partners' resolution approving the appointment of a new manager and the opening of a branch in Jeddah; the 20% partner is abroad and will sign electronically."

**Expected behaviours.**
1. Step 0 runs; Step 4 reads the majority, circulation, and minutes-register rules from `companies-law.md` (the relevant articles are cited) rather than "state law".
2. The draft is bilingual (Arabic resolution text with English), headed as a resolution by circulation, cites the Companies Law article and the articles-of-association clause, and records the majority obtained.
3. E-signature validity is addressed from `electronic-transactions-law.md` (valid between the parties; statutory presumptions only with a licensed certificate) with `[review]` on whether the platform meets the company's articles.
4. No "unanimous written consent in lieu of a meeting" or DGCL citation unless the `usa` branch is explicitly selected.

**Forbidden.** "pursuant to Section 141(f)"; "State law notice"; a US-only template as the only output.
