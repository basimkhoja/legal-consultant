# ALL-02 — Multi-jurisdiction contract

**Skill:** `/commercial-legal:review`

**Profile fixture.** As COM-01 (primary `ksa`).

**Input.** The COM-01 agreement with governing law "the laws of England and Wales", arbitration seated in London, a Saudi counterparty, and performance in the Kingdom.

**Expected behaviours.**
1. Step 0 resolves two codes: `gbr` (governing law) and `ksa` (counterparty, performance, enforcement).
2. `gbr` is unpopulated: the skill stops for that code as in ALL-01 and, if the user chooses to proceed, marks every governing-law finding `[not populated — no rule applied]`.
3. `ksa` findings are still produced and labelled `[ksa]`: enforcement of a London award in the Kingdom from `arbitration-law.md` and `enforcement-law.md`, Saudi public-order limits on interest, PDPL transfer conditions for data leaving the Kingdom, Commercial Agencies registration if a distribution element exists.
4. No sentence merges the two jurisdictions' rules.

**Forbidden.** Applying `ksa` contract-law rules (penalty reduction, Art. 173) to the English-law clauses as if they governed; applying English-law rules from memory.
