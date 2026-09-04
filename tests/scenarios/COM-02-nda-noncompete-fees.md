# COM-02 — NDA with an individual non-compete and fee shifting

**Skill:** `/commercial-legal:nda-review`

**Profile fixture.** As COM-01.

**Input.** An inbound NDA from a consultant (natural person) with: a 3-year post-engagement non-compete covering "any business in the Kingdom"; perpetual confidentiality; a prevailing-party attorneys'-fee clause; governing law of the primary jurisdiction; disputes to "the courts of London".

**Expected behaviours.**
1. Step 0 runs before any GREEN/YELLOW/RED verdict; GREEN is not issued.
2. The non-compete is flagged against the two-year written cap and legitimate-interest limit in `labor-law.md` Art. 83 (the file's row is cited) with `[review]` on whether the consultant is a worker or an independent contractor.
3. Perpetual confidentiality: the skill cites the survival rule in `civil-transactions-law.md` Art. 113 and does not assert a "reasonable period" limit from another jurisdiction.
4. Fee shifting: tagged `[no rule in ksa files — verify]` (or the file's row if one exists), not asserted from the "American rule".
5. The London forum clause is flagged with the enforcement position from `enforcement-law.md` and `commercial-courts-law.md` (foreign judgments enforced on reciprocity and public-order conditions), with the Enforcement Law's effective date noted.
6. Output carries the disclaimer line and the Arabic rendering of the triage result.

**Forbidden.** "Unenforceable in CA (§16600)"; any US state statute; GREEN before the enforceability step.
