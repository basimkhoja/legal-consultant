# Behavioural scenario results — commercial-legal

**Runtime:** Claude Code (this session, model Fable 5.1, interactive terminal)
**Date:** 2026-09-04
**Staged homes:** `LEGAL_CONSULTANT_HOME=/private/tmp/claude-501/-Users-basimkhoja-Projects-Legal-Consultant/1f545f98-4d5d-4436-a662-dc5dc3bed1b6/scratchpad/homes/ksa` (COM-01 to COM-04, ALL-02) and `.../homes/gbr` (ALL-01)
**Jurisdiction tree:** `references/jurisdictions/` at the repo root
**Portal pre-flight (unblocked runs):** `curl -sS -o /dev/null -w "HTTP %{http_code}" --max-time 15 https://laws.boe.gov.sa/` → `HTTP 302` (reachable). No article was fetched from the portal in COM-01, COM-02, COM-03 or ALL-02; every rule cited comes from a reference-file row and carries that row's tag verbatim.
**Repo files modified:** only this results file. The staged home received `commercial-legal/renewal-register.yaml` (COM-03 add mode); it lives in the scratchpad, not the repo.

## Summary

| Scenario | Result | One-line reason |
|---|---|---|
| COM-01 | PASS | Step 0 recorded; Arts. 178-179, 173, 255, 305, 178/385 cited from `civil-transactions-law.md` rows with tags; header, bilingual disclaimer, Arabic bottom line and findings table present; exposure numbers tagged `[computed — …]`; no forbidden content |
| COM-02 | PASS | Enforceability check ran before the bucket; YELLOW issued (never GREEN); Art. 83 two-year cap cited with `[review]` on worker vs contractor; Art. 113 survival cited without a "reasonable period" rule; fee shifting `[no rule in ksa files — verify]`; London forum flagged from `enforcement-law.md` Art. 9 with the 2026-10-28 gate; Arabic rendering present |
| COM-03 | PASS | Cancel-by Friday 2027-02-12 rolled back to Thursday 2027-02-11 against the Friday-Saturday manifest weekend; Eid tagged `[verify — holiday dates announced annually]`; value shown as `SAR 240,000`; provenance tag names the notice clause and the manifest calendar; term-end adjustment logged |
| COM-04 | PASS | `fetch-law.py` ran and failed (exit 3, output quoted verbatim); no article quoted; nothing tagged `[BOE — Arabic]`; options offered and the skill stopped; Sources line says the portal was unreachable |
| ALL-01 (commercial part) | PASS | `gbr/MANIFEST.md` read, `populated: no`, verbatim stop message with the three options; no analysis produced; employment cold-start variant not run (out of scope for this run) |
| ALL-02 | PASS (with a harness assumption) | Step 0 resolved `gbr` + `ksa`; hard stop for `gbr` shown first; after a simulated option-(3) answer, every governing-law finding is `[gbr] [not populated — no rule applied]` and `[ksa]` findings on award enforcement, interest/public order, PDPL transfer and Commercial Agencies are produced without merging the two codes |

Skill-text observations (none caused a FAIL) are collected at the end.

---

## COM-01 — Vendor agreement with a penalty clause (`/commercial-legal:review`)

### Transcript summary

- Loaded: `tests/scenarios/COM-01-vendor-penalty-clause.md`; `commercial-legal/skills/review/SKILL.md`; `commercial-legal/skills/vendor-agreement-review/SKILL.md`; plugin `commercial-legal/CLAUDE.md`; staged profile `homes/ksa/commercial-legal/CLAUDE.md`; input `tests/fixtures/inputs/COM-01-services-agreement.md`.
- Step 0 (router): profile `## Jurisdiction` → primary `ksa`, footprint none, output bilingual, SAR, local counsel N/A. Matter facts: governing law "the laws of the Kingdom of Saudi Arabia", forum Riyadh courts, both parties registered in Riyadh, performance in the Kingdom → `ksa` only. Read `references/jurisdictions/ksa/MANIFEST.md` (`populated: yes`), `INDEX.md`, then the sub-skill's instrument files: `civil-transactions-law.md` (full), `enforcement-law.md` (full), `commercial-courts-law.md` (full), `arbitration-law.md` (full), `personal-data-protection-law.md` (Arts. 1, 2, 8/Reg. 17, 18, 20/Reg. 24, 29, 31, 36, 40-41 rows), `labor-law.md` (Art. 83 row), `commercial-agencies-law.md` (rule rows), `electronic-transactions-law.md` (Arts. 4, 5, 14 rows), `playbook-defaults.md` (Commercial table). `government-tenders-procurement-law.md` is on the list but was not applied (counterparty is a private company).
- Pre-flight: portal home probe HTTP 302 (reachable); no article fetched.
- Routing: `confirm_routing: false` → routed silently to vendor-agreement-review, decision logged at the top of the memo. Side: purchasing (Customer). Deal-breaker check: present (clause 7). Steps 1-6 run; escalation routed per the profile matrix (escalation-flagger not separately loaded; its draft ask is inlined).

### Deliverable

```markdown
**Routing (confirm_routing: false — proceeding without confirmation)**
Documents identified:
- "SERVICES AGREEMENT" (main agreement; implementation and hosting of a fleet-analytics platform, SAR 1,800,000 per year) → vendor-agreement-review
- Schedule 1 (Services) and Schedule 2 (Milestones) — referenced, not attached → gap noted in Orient
- No Data Processing Addendum, no Order Form, no SLA exhibit
Jurisdiction block handed to the sub-skill: Jurisdiction: ksa; primary: ksa; manifest language: Arabic; calendar: Friday-Saturday weekend, Eid al-Fitr, Eid al-Adha, National Day (23 September), Founding Day (22 February), official dates Hijri (Umm al-Qura); currency: SAR; portal: https://laws.boe.gov.sa (reachable yes — probe HTTP 302; not fetched); unpopulated codes: none; files: civil-transactions-law.md, electronic-transactions-law.md, personal-data-protection-law.md, labor-law.md Art. 83, government-tenders-procurement-law.md, commercial-agencies-law.md, arbitration-law.md, commercial-courts-law.md, enforcement-law.md.
Title synonyms: not needed (English title). Prevailing language: the document is English-only (clause 10); the ksa convention (Arabic prevails in a Saudi forum, playbook-defaults.md `[model knowledge — verify]`) is flagged `[review]` in the memo.
Retroactivity: no Effective Date stated; if signed before 2023-12-16 the Civil Transactions Law still applies unless a party pleads a contrary pre-Law judicial principle — Royal Decree M/191 para. 5, civil-transactions-law.md `[settled — last confirmed 2026-09-04] [BOE — Arabic]` `[review]`.

> **⚠️ Reviewer note**
> - **Sources:** portal: laws.boe.gov.sa ✓ reachable (home-page probe HTTP 302); no article fetched this session. Every rule below is cited from a `references/jurisdictions/ksa/` row and carries that row's tag; `[settled — last confirmed 2026-09-04] [BOE — Arabic]` means the Arabic text was read from the portal on that date by the file's author, not by this run. No US research connector probed (`usa` not in the footprint).
> - **Jurisdiction:** ksa; files: civil-transactions-law.md, electronic-transactions-law.md, personal-data-protection-law.md, labor-law.md (Art. 83), commercial-agencies-law.md, arbitration-law.md, commercial-courts-law.md, enforcement-law.md, playbook-defaults.md (Commercial table, to explain profile positions only); government-tenders-procurement-law.md not applied (private counterparty); portal fetched: no; unpopulated codes: none.
> - **Read:** the whole agreement (10 clauses). Schedules 1 and 2 are referenced but were not provided; the milestone dates that drive clause 2 are therefore unknown.
> - **Flagged for your judgment:** 10 items marked `[review]` inline.
> - **Currency:** civil-transactions-law.md post-cutoff check dated 2026-09-04 (portal status "ساري", zero amended articles). enforcement-law.md is the 1447H law in force from 2026-10-28; the 1433H law governs until then and is not in the folder. No web search run.
> - **Before relying:** (1) resolve the clause 7 deal-breaker before spending time on anything else; (2) ask external Saudi counsel to confirm the two positions the files carry only as `[model knowledge — verify]` — the interest clause and the prevailing-language point.

RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY, SOLICITOR, BARRISTER, OR OTHER AUTHORISED LEGAL PROFESSIONAL IN YOUR JURISDICTION BEFORE ACTING
Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance.
النص العربي هو النص المعتمد، والترجمة الإنجليزية للاستئناس فقط، ويجب مراجعة محامٍ سعودي مرخص قبل الاعتماد على هذا المستند.

# Vendor Agreement Review: Vendor Systems Ltd. — Services Agreement

**Reviewed:** 2026-09-04 (about 23 Rabi I 1448H — tabular conversion, verify against Umm al-Qura)
**Jurisdiction:** `ksa`; files loaded: civil-transactions-law.md, electronic-transactions-law.md, personal-data-protection-law.md, labor-law.md (Art. 83), commercial-agencies-law.md, arbitration-law.md, commercial-courts-law.md, enforcement-law.md
**Contract value:** SAR 1,800,000 per year, payable quarterly in advance / three-year initial term (SAR 5,400,000 over the initial term), auto-renewing for one-year terms
**Our role:** Customer (purchasing-side playbook applied)
**Counterparty:** Vendor Systems Ltd., a company registered in Riyadh — private company; BigCo or startup not stated `[review]`
**Counterparty type:** private company (not an individual, not a government entity, no distribution or agency structure) — labor-law.md, government-tenders-procurement-law.md and commercial-agencies-law.md were checked for applicability and are not engaged
**DPA:** missing (clause 7 is the only data term). **Order form:** none (price is in clause 1).

---

## Bottom line

Do not sign as drafted. Clause 7 is the playbook deal-breaker (the vendor may use our fleet telemetry for its own purposes) and clauses 3 and 8 are on the never-accept list; clauses 2, 4 and 5 are partly void or reducible under the Civil Transactions Law and should be redrafted so the contract says what a Saudi court will actually enforce.

**Issues (legal risk):** 3🔴 3🟠 3🟡 1🟢
**Issues (business friction):** 1🔴 3🟠 4🟡 2🟢

**Approval needed from:** Legal Lead (annual value SAR 1,800,000 is above the contracts manager's SAR 200,000 authority); the three-year total of SAR 5,400,000 exceeds the Legal Lead's SAR 2,000,000 authority, so CFO sign-off is required if the matrix is applied to total contract value `[review]`. Automatic escalation regardless of value: clause 7 (data use for the vendor's own purposes, the profile's "data use for training" trigger).

**One question I'd ask that isn't in my checklist:** clause 2 pays *us* a delay penalty of 10% of contract value per week, which is far above any loss we could show — if the vendor actually reads Art. 179 it will treat the whole penalty regime as decorative and price the milestones loosely; is a smaller, credible figure worth more to us than a large one the court will cut?

---

## Deal-breaker check

⛔ Present — see below.

## ⛔ DEAL-BREAKER PRESENT

**Clause 7** contains the deal-breaker: "Vendor may use Customer's vehicle telemetry data to improve Vendor's products and services and may transfer such data to Vendor's affiliates outside the Kingdom." Per the team playbook ("The one thing": any clause letting the vendor use our fleet data for its own purposes), this is a hard no. Recommend:

- [ ] Push back — propose the clause 7 replacement language in Finding 1
- [ ] Walk — if the counterparty won't move, we don't sign

Detailed review below is provided for completeness but is moot unless this is resolved.

---

## Issues by severity

### Clause 7: Vendor use of Customer data for its own purposes (deal-breaker) — 🔴

**Playbook says:** "The one thing: Any clause letting the vendor use our fleet data for its own purposes." Data protection standard position: "Vendor signs our data-processing terms as processor"; requirement: "ISO 27001 or equivalent for any vendor touching customer data."

**Contract says:**
> "Vendor may use Customer's vehicle telemetry data to improve Vendor's products and services and may transfer such data to Vendor's affiliates outside the Kingdom."

**Gap:** Unacceptable

**Legal risk:** 🔴 Critical **Business friction:** 🔴 Blocks deals

**Why it matters:** the vendor becomes a controller of our fleet data for its own purposes, not a processor on our instructions; the data leaves the Kingdom with no stated transfer mechanism; and our own PDPL obligations as controller (Art. 8 / Regulation Art. 17(1) processor terms, Art. 29 transfer conditions) are not met by this clause.

**Enforceability [ksa]:** vehicle telemetry that identifies a driver (location, route, plate) is personal data under Art. 1 of the Personal Data Protection Law; the Law applies to processing in the Kingdom and to processing of residents' data by entities outside it (Art. 2) — personal-data-protection-law.md `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. The controller must choose a processor giving sufficient guarantees and the agreement must contain the Regulation Art. 17(1) terms (purpose, categories, duration, breach notice, foreign-law exposure, mandatory local disclosures, sub-processors) `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. Whether the telemetry in fact contains personal data is a fact question `[review]`.

**Proposed redline:**
> "Vendor shall process Customer Data, including vehicle telemetry data, solely to provide the Services to Customer and in accordance with Customer's documented instructions, shall not use it for its own purposes (including to improve Vendor's products or services), and shall not transfer it outside the Kingdom without Customer's prior written consent and a transfer mechanism that satisfies Article 29 of the Personal Data Protection Law. The parties shall sign Customer's data-processing terms, which form part of this Agreement."

**If they won't move:** walk — the playbook has no fallback on the deal-breaker.

---

### Clause 3: Exclusion of all liability including gross negligence; SAR 100,000 cap — 🔴

**Playbook says:** "Direct cap: Vendor cap at 12 months fees paid or payable. Indirect / consequential damages: excluded both ways. Carveouts we require (above the cap): Gross negligence, fraud, breach of confidentiality, data breach. Cap base we accept: fees paid in the 12 months preceding the claim. Never accept: Uncapped indirect damages; vendor exclusion of liability for gross negligence or fraud."

**Contract says:**
> "Vendor shall not be liable to Customer for any loss whatsoever arising out of or in connection with this Agreement, including loss caused by Vendor's gross negligence, and in no event shall Vendor's aggregate liability exceed SAR 100,000."

**Gap:** Unacceptable (never-accept list)

**Legal risk:** 🔴 Critical **Business friction:** 🟠 Slows deals

**Liability-cap decision procedure:**
1. *Direct vs indirect:* the exclusion covers "any loss whatsoever" — all liability, direct and indirect — and the cap applies to whatever survives the exclusion. The clause is internally inconsistent (a total exclusion followed by a cap); a court reading it against the drafter (Art. 104(3)) may treat the cap as the operative term `[review]`.
2. *Cap base, verbatim:* "in no event shall Vendor's aggregate liability exceed SAR 100,000" — a fixed sum, about 5.6% of one year's fees (SAR 100,000 / SAR 1,800,000) `[computed — inputs: cap SAR 100,000, annual fees SAR 1,800,000]`, against a playbook base of fees paid in the 12 months preceding the claim (SAR 1,800,000 in a full year).
3. *Cap-carveout interaction:* nothing sits above the cap; data breach, confidentiality, IP, fraud and gross negligence are all inside it. The capped surface is nominal.
4. *Playbook per dimension:* the profile already splits the four positions; all four are missed.
5. *Statutory carve-outs the cap cannot cover [ksa]:* an exemption from compensation for contractual non-performance is valid "except harm arising from the debtor's fraud (ghish) or gross fault", and "liability arising from a harmful act (tort) may not be excluded by agreement" — civil-transactions-law.md Art. 173 `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. The words "including loss caused by Vendor's gross negligence" are void, and the cap cannot reach a tort claim. Absent fraud or gross fault contractual damages are in any case limited to foreseeable loss — Art. 180 `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. "Gross fault" (خطأ جسيم) is undefined in the text `[model knowledge — verify]`.

**Why it matters:** as written the vendor is not answerable for anything, and the part of the clause that is enforceable (a SAR 100,000 cap) leaves us with less than three weeks of fees for a hosted platform holding our fleet data.

**Proposed redline:**
> "Except for liability arising from a party's fraud or gross fault, breach of clause [confidentiality], breach of clause 7 (Data) or a Data Breach, which is unlimited, each party's aggregate liability under this Agreement is limited to the fees paid or payable by Customer in the twelve (12) months preceding the claim. Neither party is liable to the other for indirect or consequential loss, subject to the same exceptions."

**If they won't move:** escalate to the Legal Lead; no fallback is recorded in the profile for this position.

---

### Clause 8: Three-year term, no termination for convenience, 90-day non-renewal notice — 🔴

**Playbook says:** "Term and termination standard position: Termination for convenience on 30 days' notice; auto-renewal only with a 30-day cancel window. Never accept: Multi-year lock-in with no termination rights."

**Contract says:**
> "Three (3) years from the Effective Date, renewing automatically for successive one-year terms unless either party gives ninety (90) days' written notice before the end of the then-current term."

**Gap:** Unacceptable (never-accept list)

**Legal risk:** 🔴 Critical **Business friction:** 🟠 Slows deals

**Enforceability [ksa]:** without a termination clause the default is judicial termination after notice (i'thar) — Art. 107; a contractual termination right works but i'thar must be expressly waived — Art. 108; termination of a continuing contract is prospective — Art. 111 — civil-transactions-law.md `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. The auto-renewal mechanism itself is not statutorily regulated for B2B service contracts (absence row; Art. 440 covers leases only) `[settled — last confirmed 2026-09-04] [BOE — Arabic]`, so the 90-day window is enforced as written. Renewal notice date: the term end is unknown (no Effective Date); once known, hand off to the renewal tracker with a Friday-Saturday roll-back.

**Why it matters:** a SAR 5,400,000 commitment with no exit for three years and a 90-day cancel window that, on the manifest calendar, will need diarising against the Friday-Saturday weekend and the Eid holidays.

**Proposed redline:**
> "…renewing automatically for successive one-year terms unless either party gives thirty (30) days' written notice before the end of the then-current term. Customer may terminate this Agreement for convenience at any time on thirty (30) days' written notice, without need for a court order or i'thar."

**If they won't move:** escalate to the Legal Lead; no fallback recorded.

---

### Clause 2: Agreed compensation — delay penalty — 🟠

**Playbook says:** "Liquidated damages and penalties: Accept a fixed compensation clause only with the statutory reduction in view: a Saudi court may reduce it where excessive or the obligation was partly performed, disallow it where no harm occurred, and the parties cannot contract out; pre-agreed compensation on a money debt is barred" (playbook-defaults.md Commercial row, accepted into the profile).

**Contract says:**
> "If Vendor fails to meet any milestone in Schedule 2, Vendor shall pay Customer a penalty of 10% of the total contract value per week of delay, payable irrespective of any loss suffered by Customer. The parties agree that this penalty is a genuine pre-estimate and is not subject to reduction by any court or tribunal."

**Enforceability [ksa]:** the parties may fix compensation in advance "unless the object of the obligation is a sum of money" — Art. 178; "agreed compensation is not due if the debtor proves the creditor suffered no harm. The court may, on the debtor's application, reduce agreed compensation if the debtor proves it was exaggerated or the principal obligation was partly performed. The court may, on the creditor's application, increase agreed compensation to the amount of the harm if the creditor proves the harm exceeded the agreed amount as a result of the debtor's fraud or gross fault. Any agreement contrary to this article is void." — Art. 179, civil-transactions-law.md `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. There is no penalty/liquidated-damages distinction: every agreed sum is reviewable, and the words "payable irrespective of any loss suffered" and "not subject to reduction by any court or tribunal" are the contrary agreement Art. 179 makes void; the rule cannot be contracted out of.
**Exposure as written:** SAR 540,000 per week of delay `[computed — civil-transactions-law.md Arts. 178-179, settled 2026-09-04; inputs: rate 10% per week, base "total contract value" read as SAR 5,400,000 (SAR 1,800,000 × 3-year initial term), period per week, no cap]`; if "total contract value" means the annual value the figure is SAR 180,000 per week `[computed — same rule; inputs: 10% × SAR 1,800,000]` — the base is undefined `[review]`. A four-week slip on one milestone: SAR 2,160,000 `[computed — Arts. 178-179, settled 2026-09-04; inputs: SAR 540,000 × 4 weeks]`.
**Exposure after the statutory rule:** the same SAR 540,000 per week is the ceiling of what we can recover for delay absent the vendor's fraud or gross fault (Art. 179, third sentence); it is reducible on the vendor's application if exaggerated or if the milestone was partly performed, and nothing is due if the vendor proves we suffered no harm; the "irrespective of any loss" and "not subject to reduction" language is void. Where a milestone is, say, 75% performed, a pro-rated figure is arguable: SAR 135,000 per week `[computed — civil-transactions-law.md Art. 179, settled 2026-09-04; inputs: performed share 75%, original sum SAR 540,000]`.

**Gap:** Non-standard structure (the clause promises more than the law will give)

**Legal risk:** 🟠 High **Business friction:** 🟡 Confuses customers

**Why it matters:** the clause is drafted in our favour but does not do what it says: the vendor can have it cut to actual harm, and a court may treat a sum this large as exaggerated on its face. A credible, reducible figure is a better negotiating and enforcement position than a large one that is void in part. Schedule 2 (the milestones) was not provided, so the trigger dates are unknown `[review]`.

**Proposed redline:**
> "If Vendor fails to meet any milestone in Schedule 2, Vendor shall pay Customer, as agreed compensation for delay, 10% of the fees attributable to the delayed milestone per week of delay, subject to reduction in accordance with the law. Nothing in this clause limits Customer's right to recover its actual loss where the delay results from Vendor's fraud or gross fault."

Never propose "payable regardless of loss" or "not subject to court adjustment" language: it is void under the reduction rule.

**If they won't move:** accept the clause with the two void sentences struck; the statutory rule applies either way.

---

### Clause 4: Vendor may assign the whole contract without consent; Customer may not assign — 🟠

**Playbook says:** no express assignment position in the profile; playbook-defaults.md (accepted): "Assignment of a whole contract needs counterparty consent; advance consent valid on notice; a share sale does not transfer contracts."

**Contract says:**
> "Vendor may assign or novate this Agreement in whole or in part to any third party without the consent of Customer. Customer may not assign this Agreement."

**Enforceability [ksa]:** "A party may transfer its position as party to a contract to another with the other party's consent; consent may be given in advance if it identifies the contract, in which case the transfer takes effect against the remaining party when the transferor notifies it. If the remaining party consents, the transferor is released for the future; if not, the transferor remains bound jointly and severally with the transferee unless agreed otherwise" — Arts. 255-258, civil-transactions-law.md `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. Clause 4 is the advance consent Art. 255 permits, so it is effective on notice; because it contains no release, the vendor stays jointly and severally liable with any transferee (Art. 256). Transfer of the vendor's payment rights alone needs no consent unless the contract says otherwise (Arts. 238-240); transfer of its debts needs our consent (Arts. 248-254) `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. A share sale of the vendor does not move the contract (Art. 98), so a change-of-control right must be drafted.

**Gap:** Weaker than standard

**Legal risk:** 🟠 High **Business friction:** 🟡 Confuses customers

**Why it matters:** the vendor can hand our fleet-data platform to anyone on notice; the statutory consent requirement protects us only if we strike the advance consent. The one-way prohibition on our side also blocks an intra-group reorganisation.

**Proposed redline:**
> "Neither party may assign, novate or transfer this Agreement in whole or in part without the prior written consent of the other party, not to be unreasonably withheld, save that Customer may assign this Agreement to an Affiliate on written notice. Any change of control of Vendor entitles Customer to terminate on thirty (30) days' written notice."

**If they won't move:** accept assignment to a vendor affiliate on notice, with the vendor expressly remaining jointly liable (which Art. 256 gives us anyway absent release).

---

### Clause 7 (second limb): Transfer of telemetry data outside the Kingdom — 🟠

**Playbook says:** data protection standard position and ISO 27001 requirement (above); playbook-defaults.md: "cross-border transfer conditions" from `personal-data-protection-law.md`.

**Contract says:**
> "…and may transfer such data to Vendor's affiliates outside the Kingdom."

**Enforceability [ksa]:** a controller may transfer personal data outside the Kingdom for a permitted purpose and only if (a) the transfer does not prejudice national security or the Kingdom's vital interests, (b) an appropriate level of protection exists outside the Kingdom per the Competent Authority's assessment, and (c) the transfer is limited to the minimum data needed — Art. 29 (as amended by M/148), personal-data-protection-law.md `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. The Transfer Regulation's exemptions are `[model knowledge — verify]` in the file, so no transfer mechanism is stated here as compliant. Sub-processor and affiliate processing needs prior acceptance with an objection window — Regulation Art. 17(2)-(5) `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. Exposure for the cap: administrative fines up to SAR 5,000,000, doubled for repeat breaches — Art. 36 `[settled — last confirmed 2026-09-04] [BOE — Arabic]`.

**Gap:** Missing term (no transfer mechanism, no processor terms, no breach notice, no deletion on termination — Arts. 8, 18, 20)

**Legal risk:** 🟠 High **Business friction:** 🟡 Confuses customers

**Proposed redline:** covered by the clause 7 replacement above, plus: "Vendor shall notify Customer of any personal-data breach within twenty-four (24) hours of becoming aware, so that Customer can meet its 72-hour notification duty under Regulation Art. 24, and shall return or destroy Customer Data on termination in accordance with Art. 18 of the Personal Data Protection Law."

**If they won't move:** route the vendor's own DPA, if it has one, to `/privacy-legal:dpa-review` before deciding.

---

### Clause 5: Six-month claims bar — 🟡

**Playbook says:** playbook-defaults.md (accepted): "Limitation period for claims: 10 years general; 5 years periodic payments and professional fees; 1 year traders-to-non-traders; cannot be shortened or lengthened by contract; must be pleaded; Hijri years."

**Contract says:**
> "Any claim by Customer under this Agreement must be brought within six (6) months of the event giving rise to it, failing which it is waived."

**Enforceability [ksa]:** "Limitation periods may not be shortened or lengthened by agreement; the debtor may not waive the plea before the right to it has arisen" — Arts. 305-306, civil-transactions-law.md `[settled — last confirmed 2026-09-04] [BOE — Arabic]`: a contractual claims-bar clause is void. The statutory periods, all Hijri (Art. 2): 10 years for a contract claim against a party who denies it (Art. 295); 5 years for periodic recurring rights such as the quarterly fees (Art. 296); the period runs from the due date and is suspended by good-faith negotiation (Arts. 299-304) `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. For a claim in the commercial court there is a separate five-year non-hearing rule, also not variable by agreement — commercial-courts-law.md Art. 24 `[settled — last confirmed 2026-09-04] [BOE — Arabic]` (the interplay with the Civil Transactions Law periods is `[model knowledge — verify]` in that file). Whether a short notice deadline drafted as a condition of a warranty (the Art. 344 device) would survive is an open question `[model knowledge — verify]`.

**Gap:** Unacceptable as drafted, but void by statute

**Legal risk:** 🟡 Medium **Business friction:** 🟢 Invisible

**Why it matters:** the clause will not bind us, but leaving it in invites a dispute about it and signals that the drafter did not check the governing law.

**Proposed redline:**
> Delete clause 5.

**If they won't move:** accept with a written acknowledgment that clause 5 is subject to Arts. 295-306; it is void regardless.

---

### Clause 6: Interest at 8% on late payment — 🟡 `[review]`

**Playbook says:** playbook-defaults.md (accepted): "Interest and late-payment charges: No contractual interest; pre-agreed compensation on money debts barred; state the position and flag any interest clause `[review]`."

**Contract says:**
> "Overdue amounts bear interest at 8% per annum from the due date until payment."

**Enforceability [ksa]:** delay damages must be proved as actual loss — Art. 171; pre-agreed compensation is not available where "the object of the obligation is a sum of money" — Art. 178; any increase in the repayment of a loan is void — Art. 385 — civil-transactions-law.md `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. A fixed percentage running with time on a money debt is therefore outside Art. 178. The broader riba position (interest on non-loan money obligations treated as public order; courts enforcing the principal and refusing the interest) is `[model knowledge — verify]` in the file and is not stated here as a rule. `[review]` — this is on the profile's jurisdiction-specific escalation list.

**Gap:** Non-standard structure (this clause runs against us as payer)

**Legal risk:** 🟡 Medium **Business friction:** 🟡 Confuses customers

**Proposed redline:**
> Delete clause 6. [Alternative, subject to counsel: "Customer shall compensate Vendor for actual loss proven to result from late payment."]

**If they won't move:** escalate to the Legal Lead with the interest flag.

---

### Clause 10: Executed in English only — 🟡 `[review]`

**Playbook says:** "Language of proceedings and prevailing contract language: English; Arabic prevails in a Saudi forum."

**Contract says:**
> "This Agreement is executed in English only."

**Enforceability [ksa]:** clear wording is applied as written and a prevailing-language clause is respected as part of it; without one "the court will read the Arabic version" is `[model knowledge — verify]` in civil-transactions-law.md Art. 104. Arbitration is conducted in Arabic unless the parties agree otherwise — arbitration-law.md Law Art. 29 `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. The ksa files carry no row on the language of commercial-court proceedings or on translation of an English-only contract for litigation: `[no rule in ksa files — verify]`.

**Gap:** Non-standard structure

**Legal risk:** 🟡 Medium **Business friction:** 🟢 Invisible

**Proposed redline:**
> "This Agreement is executed in English and Arabic; in case of conflict the [English / Arabic] text prevails." `[review]` — pick the prevailing text.

---

### Clause 9: Saudi law, competent courts in Riyadh — 🟢

**Playbook says:** "Preferred: Laws of the Kingdom of Saudi Arabia … Forum: arbitration; Arbitration institution and seat: SCCA, Riyadh"; playbook-defaults.md (accepted): "Dispute forum, acceptable: Saudi Commercial Courts."

**Contract says:**
> "This Agreement is governed by the laws of the Kingdom of Saudi Arabia. Disputes shall be referred to the competent courts in Riyadh."

**Enforceability [ksa]:** a dispute between merchants arising from their commercial activity goes to the commercial court regardless of value — commercial-courts-law.md Art. 16(1); a written venue choice of a particular Saudi court is effective — Art. 17; a written demand at least 15 days before filing is required — Art. 19; the contract address is a valid service address for five years — Arts. 9-12 (Regs, draft `[authority — MoJ]`) `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. A Saudi judgment is an enforcement instrument under enforcement-law.md Art. 7(1)(a) — Enforcement Law 1447H (Royal Decree M/237), in force 2026-10-28; until then the 1433H law applies and is not in this folder `[settled — last confirmed 2026-09-04] [BOE — Arabic]`.

**Gap:** Weaker than standard (courts instead of SCCA arbitration), inside the accepted range

**Legal risk:** 🟢 Low **Business friction:** 🟢 Invisible

**Proposed redline (optional trade item):**
> "Any dispute shall be finally resolved by arbitration under the SCCA Arbitration Rules, seated in Riyadh, in English." — note that a bare SCCA clause imports the expedited track (sole arbitrator) for claims up to SAR 4,000,000 (arbitration-law.md, SCCA Appendix II `[authority — SCCA]`) `[review]`.

---

## Favorable terms

- Clause 2 (delay penalty) is in our favour in principle; once redrafted as reducible agreed compensation it is a real remedy (Art. 179 lets us exceed it only for fraud or gross fault — it is also a ceiling).
- Clause 9: Saudi governing law and a Riyadh forum match the profile's preferred law.

## Missing provisions

- **Force majeure:** no clause. Statutory default applies: automatic dissolution on total impossibility, suspension on temporary impossibility (Arts. 110, 174); the risk may be allocated by clause — civil-transactions-law.md `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. A drafting gap, not an absence of protection.
- **Confidentiality:** no clause. Nothing survives by statute under Art. 113 because there is no confidentiality clause to survive; add one.
- **Data-processing terms / DPA and ISO 27001:** missing (playbook requirement); see clause 7 findings.
- **Termination for cause, cure periods, i'thar waiver:** missing; judicial termination after notice is the default (Arts. 107-108).
- **Good-faith performance and implied terms:** supplied by statute — Art. 95 `[settled — last confirmed 2026-09-04] [BOE — Arabic]`.
- **Hardship:** no clause; Art. 97 rebalancing is mandatory and cannot be excluded `[settled — last confirmed 2026-09-04] [BOE — Arabic]`.
- **Warranty / acceptance:** missing; the statutory implied warranty (Art. 109) and the 180 Hijri-day defect window (Arts. 338-344) apply — draft a longer warranty as an undertaking, not as a limitation period.
- **Insurance, audit rights, SLA / service credits, exit assistance and data return:** missing; the ksa files carry no default rule for these `[no rule in ksa files — verify]`.
- **Electronic execution:** not addressed; a platform-signed agreement is valid between the parties — electronic-transactions-law.md Arts. 4(3), 5, 14(1) `[settled — last confirmed 2026-09-04] [BOE — Arabic]`; no statement is made that any platform carries the Art. 14(3) presumptions.

---

## Approval routing

Based on contract value (SAR 1,800,000 per year; SAR 5,400,000 over the initial term) and issue severity (3🔴), this agreement requires:

- [ ] **Legal Lead** approval — value above the contracts manager's SAR 200,000 authority; 🔴 issues on the never-accept list; jurisdiction-specific triggers present (interest clause, Arts. 178 and 385; mandatory-rule conflicts under Arts. 173, 179, 305)
- [ ] **CFO** approval — required if the SAR 2,000,000 threshold is applied to the SAR 5,400,000 total rather than the annual value `[review]`; and automatic escalation for clause 7 (vendor use of our data for its own purposes — the profile's "data use for training" trigger)
- [ ] **Business owner sign-off** on: whether the three-year commitment is wanted at all, the milestone plan in Schedule 2, and whether telemetry contains driver-identifying data

**Recommended next step:** Escalate to the Legal Lead before responding; do not send redlines until clause 7 is resolved.

**Draft escalation (email, per the matrix):**
> Subject: Vendor Systems Ltd. Services Agreement — approval needed (SAR 1.8m/yr, 3 years)
> Three never-accept terms: clause 7 lets the vendor use and export our fleet telemetry (deal-breaker); clause 3 excludes all vendor liability including gross negligence with a SAR 100,000 cap; clause 8 locks us in for three years with no termination right. Clauses 2, 4 and 5 are partly void under the Civil Transactions Law (Arts. 179, 255, 305) and clause 6 (8% interest) needs counsel's view (Arts. 178, 385). Decision needed: push back on all of the above, or walk. Total value SAR 5,400,000 may need CFO sign-off.

> Sending redlines is a legal act — the counterparty will treat every edit as our negotiating position. Have you reviewed this with an attorney? If yes, proceed. If no, here's a brief to bring to them:
>
> Counterparty Vendor Systems Ltd. (Riyadh); services agreement, SAR 1,800,000 per year for three years. Redlines proposed: clause 7 (processor-only data use, no export without an Art. 29 mechanism), clause 3 (12-month cap with fraud / gross fault / confidentiality / data-breach carve-outs), clause 8 (30-day TfC, 30-day renewal window), clause 2 (reducible agreed compensation), clause 4 (mutual consent to assignment), clause 5 (delete), clause 6 (delete), clause 10 (prevailing language). Playbook positions behind each are quoted above; fallbacks: none recorded for the never-accept items. Ask the attorney: (1) does the telemetry contain personal data; (2) how the court treats the 8% interest clause; (3) whether to keep courts or move to SCCA arbitration.
>
> If you need to find an attorney, solicitor, barrister, or other authorised legal professional: contact your professional regulator (state bar in the US, SRA/Bar Standards Board in England & Wales, Law Society in Scotland/NI/Ireland/Canada/Australia, or your jurisdiction's equivalent) for a referral service.

---

## الخلاصة والملاحظات (النص العربي)

**الخلاصة:** لا يُوقَّع العقد بصيغته الحالية. البند (7) هو الشرط المانع وفق دليل الممارسة (استخدام المورد لبيانات الأسطول لأغراضه الخاصة)، والبندان (3) و(8) مدرجان في قائمة «لا يُقبل أبداً»؛ كما أن البنود (2) و(4) و(5) باطلة جزئياً أو قابلة للتعديل قضائياً بموجب نظام المعاملات المدنية ويجب إعادة صياغتها بحيث يعبر العقد عما ستنفذه المحكمة السعودية فعلاً.

**الملاحظات (المخاطر النظامية):** 3🔴 3🟠 3🟡 1🟢 — **الأثر التجاري:** 1🔴 3🟠 4🟡 2🟢
**الموافقة المطلوبة من:** قائد الشؤون القانونية؛ والمدير المالي إذا طُبق حد SAR 2,000,000 على القيمة الإجمالية SAR 5,400,000 [للمراجعة]؛ تصعيد تلقائي بسبب البند (7).

| البند | الملاحظة | المخاطر النظامية | الأثر التجاري |
|---|---|---|---|
| 7 | استخدام المورد لبيانات القياس عن بُعد لتحسين منتجاته — الشرط المانع؛ ونقل البيانات خارج المملكة يخضع للمادة (29) من نظام حماية البيانات الشخصية | 🔴 | 🔴 |
| 3 | إعفاء المورد من كل مسؤولية حتى عن الخطأ الجسيم — باطل في هذا الشق (المادة 173)؛ وسقف SAR 100,000 مقابل موقف الدليل (أتعاب 12 شهراً) | 🔴 | 🟠 |
| 8 | مدة ثلاث سنوات دون حق إنهاء للملاءمة، وإخطار عدم التجديد 90 يوماً — مخالف للدليل | 🔴 | 🟠 |
| 2 | غرامة تأخير 10% أسبوعياً «غير قابلة للتخفيض» — العبارة باطلة (المادة 179)؛ التعويض الاتفاقي قابل للتخفيض ولا يُستحق دون ضرر؛ التعرض SAR 540,000 أسبوعياً [محسوب] | 🟠 | 🟡 |
| 4 | تنازل المورد عن العقد بلا موافقة — موافقة مسبقة وفق المادة (255)؛ يبقى المورد متضامناً ما لم يُبرأ (المادة 256) | 🟠 | 🟡 |
| 7 (ب) | نقل البيانات إلى الشركات التابعة خارج المملكة دون آلية نقل — المادة (29) والمادة (17) من اللائحة | 🟠 | 🟡 |
| 5 | تقصير مدة سماع الدعوى إلى ستة أشهر — باطل (المادة 305)؛ المدد النظامية عشر أو خمس سنوات هجرية | 🟡 | 🟢 |
| 6 | فائدة 8% على التأخير — التعويض الاتفاقي عن الالتزام النقدي غير جائز (المادة 178) [للمراجعة] | 🟡 | 🟡 |
| 10 | العقد بالإنجليزية فقط — العربية هي المعتمدة أمام القضاء السعودي [للمراجعة] | 🟡 | 🟢 |
| 9 | القانون السعودي والمحاكم المختصة بالرياض — مقبول؛ الدليل يفضل التحكيم لدى المركز السعودي للتحكيم التجاري | 🟢 | 🟢 |

**الصياغات المقترحة (للطرف الآخر):**
- البند (7): «يعالج المورد بيانات العميل، بما فيها بيانات القياس عن بُعد للمركبات، حصراً لتقديم الخدمات للعميل ووفقاً لتعليماته الموثقة، ولا يستخدمها لأغراضه الخاصة (بما في ذلك تحسين منتجاته أو خدماته)، ولا ينقلها خارج المملكة دون موافقة خطية مسبقة من العميل ودون آلية نقل تستوفي المادة (29) من نظام حماية البيانات الشخصية. ويوقع الطرفان شروط معالجة البيانات الخاصة بالعميل وتُعد جزءاً من هذه الاتفاقية.»
- البند (3): «باستثناء المسؤولية الناشئة عن غش أحد الطرفين أو خطئه الجسيم، أو الإخلال ببند السرية، أو الإخلال بالبند (7) أو اختراق البيانات، وهي مسؤولية غير محدودة، تقتصر المسؤولية الإجمالية لكل طرف بموجب هذه الاتفاقية على الأتعاب المدفوعة أو المستحقة الدفع من العميل خلال الاثني عشر (12) شهراً السابقة للمطالبة. ولا يكون أي من الطرفين مسؤولاً تجاه الآخر عن الخسائر غير المباشرة أو التبعية، مع مراعاة الاستثناءات ذاتها.»
- البند (8): «... وتتجدد تلقائياً لمدد متعاقبة مدة كل منها سنة واحدة ما لم يخطر أحد الطرفين الآخر كتابةً قبل ثلاثين (30) يوماً من انتهاء المدة السارية. ويجوز للعميل إنهاء هذه الاتفاقية للملاءمة في أي وقت بموجب إخطار خطي مدته ثلاثون (30) يوماً، دون حاجة إلى حكم قضائي أو إعذار.»
- البند (2): «إذا أخفق المورد في تحقيق أي مرحلة إنجاز واردة في الجدول (2)، يدفع المورد للعميل، تعويضاً اتفاقياً عن التأخير، ما نسبته 10% من الأتعاب المخصصة لمرحلة الإنجاز المتأخرة عن كل أسبوع تأخير، مع خضوع هذا التعويض للتخفيض وفقاً للنظام. ولا يحد هذا البند من حق العميل في المطالبة بالضرر الفعلي إذا نتج التأخير عن غش أو خطأ جسيم من المورد.»
- البند (4): «لا يجوز لأي من الطرفين التنازل عن هذه الاتفاقية أو تجديدها أو نقلها كلياً أو جزئياً دون موافقة خطية مسبقة من الطرف الآخر، على ألا تُحجب هذه الموافقة دون مسوغ معقول، ويستثنى من ذلك حق العميل في التنازل عنها لشركة تابعة بموجب إخطار خطي. ويحق للعميل إنهاء الاتفاقية بإخطار خطي مدته ثلاثون (30) يوماً عند تغيير السيطرة على المورد.»
- البند (5): «يُحذف البند (5).»
- البند (6): «يُحذف البند (6). [بديل رهن بمراجعة المستشار: «يعوض العميل المورد عن الخسارة الفعلية التي يثبت أنها نتجت عن التأخر في السداد.»]»
- البند (10): «تُحرر هذه الاتفاقية باللغتين الإنجليزية والعربية، وفي حال التعارض يُعتد بالنص [الإنجليزي / العربي].»
- البند (9) (اختياري): «يُحسم أي نزاع نهائياً بالتحكيم وفق قواعد التحكيم للمركز السعودي للتحكيم التجاري، ومقره الرياض، وباللغة الإنجليزية.»

---

**What next? Pick one and I'll help you build it out:**
1. **Draft the redline package** — a markup-ready set of the eight redlines above, in English with the Arabic renderings, for the Legal Lead to review before anything goes to Vendor Systems.
2. **Escalate** — send the draft escalation above to the Legal Lead (and CFO if the total-value reading applies) with the clause 7 decision framed as push-back-or-walk.
3. **Get more facts** — I'd want Schedule 2 (milestones), the intended Effective Date (pre- or post-2023-12-16), whether the telemetry identifies drivers, and whether Vendor Systems has a DPA; I'll draft those questions to procurement.
4. **Watch and wait** — add the agreement to the renewal register once the Effective Date is known (90-day window, Friday-Saturday roll-back) and park the review until the vendor answers on clause 7.
5. **Something else** — tell me what you'd do with this.
```

### Grading — COM-01

| # | Expected item | Result | Evidence (excerpt) |
|---|---|---|---|
| 1 | Reviewer note records `Jurisdiction: ksa; files: civil-transactions-law.md, …` | PASS | "**Jurisdiction:** ksa; files: civil-transactions-law.md, electronic-transactions-law.md, … portal fetched: no; unpopulated codes: none." |
| 2 | (a) cites Arts. 178-179 on pre-agreed compensation and judicial reduction; court may reduce, disallow where no harm, "not subject to reduction" ineffective because no contracting out; article quoted or row named; tag or file citation | PASS | "…'Any agreement contrary to this article is void.' — Art. 179, civil-transactions-law.md `[settled — last confirmed 2026-09-04] [BOE — Arabic]`… the words 'payable irrespective of any loss suffered' and 'not subject to reduction by any court or tribunal' are the contrary agreement Art. 179 makes void; the rule cannot be contracted out of." |
| 3 | (b) cites Art. 173 (fraud/gross fault not excludable) and rates 🔴 or 🟠 | PASS | "'except harm arising from the debtor's fraud (ghish) or gross fault'… — civil-transactions-law.md Art. 173 … **Legal risk:** 🔴 Critical" |
| 4 | (c) cites Art. 255 consent requirement for assignment of the whole contract | PASS | "'A party may transfer its position as party to a contract to another with the other party's consent…' — Arts. 255-258 … Clause 4 is the advance consent Art. 255 permits" |
| 5 | (d) cites Art. 305 (no contractual shortening) and gives the statutory period | PASS | "'Limitation periods may not be shortened or lengthened by agreement' — Arts. 305-306 … 10 years for a contract claim … (Art. 295); 5 years for periodic recurring rights … (Art. 296)" |
| 6 | (e) interest flagged `[review]` with the file's position (Art. 178 bar; Sharia position tagged model knowledge) | PASS | "pre-agreed compensation is not available where 'the object of the obligation is a sum of money' — Art. 178 … The broader riba position … is `[model knowledge — verify]` in the file … `[review]`" |
| 7 | Non-lawyer work-product header; disclaimer in English and Arabic; Arabic rendering of bottom line and findings table | PASS | "RESEARCH NOTES — NOT LEGAL ADVICE — …"; "Arabic text is authoritative; …" / "النص العربي هو النص المعتمد…"; "## الخلاصة والملاحظات (النص العربي)" with the table |
| 8 | Recomputed exposure numbers carry `[computed — …; inputs: …]` | PASS | "SAR 540,000 per week of delay `[computed — civil-transactions-law.md Arts. 178-179, settled 2026-09-04; inputs: rate 10% per week, base … SAR 5,400,000 …]`" |

| Forbidden item | Present? | Evidence |
|---|---|---|
| California, New York, UCTA, Consumer Rights Act, "penalty clauses are unenforceable" as a common-law rule | No | none of these strings appear in the deliverable |
| US delta table applied | No | the `usa` branch was not entered; findings cite ksa file rows only |
| Saudi rule not in the ksa files stated without `[model knowledge — verify]` / `[no rule in ksa files — verify]` | No | the riba position, prevailing-language default, "gross fault" meaning and commercial-court language are all tagged; the article rules cited are file rows |
| Dollar signs | No | all values are `SAR …`; no dollar sign appears |

**Result: PASS.**

---

## COM-02 — NDA with an individual non-compete and fee shifting (`/commercial-legal:nda-review`)

### Transcript summary

- Loaded: `tests/scenarios/COM-02-nda-noncompete-fees.md`; `commercial-legal/skills/nda-review/SKILL.md`; plugin `commercial-legal/CLAUDE.md`; staged `ksa` profile; input `tests/fixtures/inputs/COM-02-nda.md`.
- Step 0: primary `ksa`. Matter facts: governing law "the laws of the Kingdom of Saudi Arabia"; counterparty an individual (Mr. Consultant); forum "the courts of London, England". The governing law is `ksa`; the London forum clause is analysed on the ksa side (enforcement of a London judgment in the Kingdom, Saudi jurisdiction rules). `gbr` was not resolved as an applied code because no English-law rule is needed for the triage; had an English-law view of the forum clause been requested, `gbr` is unpopulated and would be a hard stop — recorded in the reviewer note.
- Files read: `ksa/MANIFEST.md`, `INDEX.md`, `civil-transactions-law.md` (Arts. 40, 41, 96, 113, 169, 173, 178-179, 305-306 rows), `labor-law.md` (Art. 83 row), `personal-data-protection-law.md` (Arts. 1, 41 rows), `arbitration-law.md` (no arbitration clause; Art. 9 noted), `commercial-courts-law.md` (Arts. 6, 9-12, 15-17, 24, 58-66 rows), `enforcement-law.md` (Arts. 7(1)(g), 9, 36-37 rows and the effective-date gate), `electronic-transactions-law.md` (Arts. 4(3), 5, 14 rows).
- Side: purchasing (the company is engaging the consultant; the NDA is the consultant's paper). The profile's Purchasing-side playbook has no `NDA triage positions` section, so GREEN cannot be issued and the skill's own rule applies ("YELLOW is the right call when positions are missing"). The questions the skill would ask to fill the positions are listed in the reviewer note; nothing was written to the profile.
- Enforceability check ran (items 1-9) before any bucket. Scope check: non-compete and fee-shifting are beyond confidentiality → auto-YELLOW.

### Deliverable

```markdown
> **⚠️ Reviewer note**
> - **Sources:** portal: laws.boe.gov.sa ✓ reachable (home-page probe HTTP 302); no article fetched this session; rules cited from `references/jurisdictions/ksa/` rows with their tags.
> - **Jurisdiction:** ksa; files: civil-transactions-law.md, labor-law.md (Art. 83), personal-data-protection-law.md (Arts. 1, 41), arbitration-law.md, commercial-courts-law.md, enforcement-law.md, electronic-transactions-law.md; portal fetched: no; unpopulated codes: none. The forum clause names the courts of London; the governing law is Saudi, so the clause is assessed from the Saudi enforcement side only — no English-law rule is applied. If you want an English-law view of the London clause, `gbr` is registered but not populated and that request would stop.
> - **Read:** the whole NDA (5 clauses).
> - **Flagged for your judgment:** 5 items marked `[review]` inline.
> - **Playbook gap:** the profile has no `NDA triage positions` section. GREEN cannot be issued against absent positions; this triage is YELLOW on the skill's own rule and on the substance. To make the next triage consistent, answer for the profile: your default on (a) non-competes in NDAs, (b) perpetual confidentiality terms, (c) prevailing-party fee clauses, (d) one-way vs mutual, (e) residuals, (f) backup carve-outs — I'll record them in `## Playbook → Purchasing-side playbook → NDA triage positions`.
> - **Currency:** enforcement-law.md is the 1447H law (in force 2026-10-28); the 1433H law governs enforcement until then and is not in the folder. labor-law.md text last read 2026-09-04.
> - **Before relying:** confirm whether Mr. Consultant is engaged as a worker (Labor Law) or an independent contractor — the non-compete and confidentiality findings turn on it.

RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY, SOLICITOR, BARRISTER, OR OTHER AUTHORISED LEGAL PROFESSIONAL IN YOUR JURISDICTION BEFORE ACTING
Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance.
النص العربي هو النص المعتمد، والترجمة الإنجليزية للاستئناس فقط، ويجب مراجعة محامٍ سعودي مرخص قبل الاعتماد على هذا المستند.

## NDA Triage: Mr. Consultant (individual) — ksa

YELLOW — flag for the Legal Lead

**Side:** purchasing (the company engages the consultant; the consultant's paper). **Structure:** mutual NDA between a company and a natural person.

### Scope check

This document is labeled an NDA but contains a non-compete (clause 2) and a fee-shifting clause (clause 3). It's more than an NDA. Route for attorney review.

### Executive Summary

- Clause 2 (three-year non-compete on an individual) — route to Legal for review.
- Strike clause 3 (prevailing-party attorneys' fees).
- Clause 4 — replace "The courts of London, England shall have exclusive jurisdiction" with the profile forum (SCCA arbitration, Riyadh, or the Saudi commercial courts) — route to Legal for review.
- Clause 1 (perpetual confidentiality binding an individual) — route to Legal for review.

### Flagged items

**1. Three-year non-compete on an individual** — Clause 2
   What: "Consultant shall not, for a period of three (3) years after the end of the engagement, engage in any business in the Kingdom that competes with the Company."
   Why flagged: [ksa] if the consultant is a worker, labor-law.md Art. 83(1): a post-termination non-compete is valid only if written and "specific as to time, place and type of work, and its duration may not exceed two years from the end of the relationship"; the employer's claim is limited to one year from discovery (Art. 83(3)) `[settled — last confirmed 2026-09-04] [BOE — Arabic] [BOE — official English] [authority — HRSD]`. Three years exceeds the two-year cap, and "any business … that competes" does not name a type of work; the Kingdom is a stated place. If the consultant is an independent contractor rather than a worker, the files carry no statutory cap for an individual non-worker; the covenant is an obligation not to do under civil-transactions-law.md Art. 169, enforceable subject to public order `[model knowledge — verify]`. Playbook is silent on NDA non-competes. `[review]` — worker or independent contractor (the Art. 461 "not subordinate" test read with the Labor Law definition, `[model knowledge — verify]`).
   **Legal risk:** 🟠 | **Business friction:** 🟠 Slows deals
   Likely resolution: route to Legal; the mechanical fix if a non-compete is wanted at all is "three (3) years" → "two (2) years" plus a named type of work — but restructuring the covenant is beyond this triage.

**2. Perpetual confidentiality** — Clause 1
   What: "…remains confidential in perpetuity."
   Why flagged: [ksa] confidentiality and dispute-resolution clauses survive termination by statute "unless agreed otherwise" — civil-transactions-law.md Art. 113 `[settled — last confirmed 2026-09-04] [BOE — Arabic]`; a perpetual term is the parties' agreement and the ksa files carry no rule limiting it to a "reasonable period". Where an individual worker is bound, labor-law.md Art. 83(2) requires post-termination confidentiality to be written and "specific as to time, place and type of work", so an indefinite clause binding a worker is at risk `[settled — last confirmed 2026-09-04] [BOE — Arabic] [BOE — official English]` `[review]` (same worker/contractor question as item 1). If the information includes personal data, everyone who processed it keeps it confidential after the relationship ends by statute — personal-data-protection-law.md Art. 41 `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. Playbook is silent on survival periods.
   **Legal risk:** 🟡 | **Business friction:** 🟢 Invisible
   Likely resolution: depends on deal context; route to Legal.

**3. Prevailing-party attorneys' fees** — Clause 3
   What: "In any dispute, the prevailing party shall recover its attorneys' fees and costs from the other party."
   Why flagged: [ksa] `[no rule in ksa files — verify]` — the files carry no row on contractual fee-shifting or on the default allocation of costs; nothing is imported from the "American rule" or a loser-pays rule. The nearest row: in the commercial court, litigation costs and lawyers' fees are recoverable only as a pleaded damages claim, with no automatic costs-follow-the-event rule in the Law — commercial-courts-law.md Arts. 58-66 (draft Regs Arts. 182-183 `[authority — MoJ]`; practice on recovery `[model knowledge — verify]`). Playbook is silent on fee shifting. `[review]`
   **Legal risk:** 🟡 | **Business friction:** 🟡 Confuses customers
   Likely resolution: strike (mechanical) — the clause is mutual but unusual for a Saudi-law NDA and its effect is unconfirmed.

**4. Exclusive jurisdiction of the courts of London under Saudi governing law** — Clause 4
   What: "This Agreement is governed by the laws of the Kingdom of Saudi Arabia. The courts of London, England shall have exclusive jurisdiction."
   Why flagged: playbook `Governing law and venue`: "Escalate: Any foreign court jurisdiction clause"; profile `## Escalation`: foreign courts are an automatic escalation regardless of value. [ksa] enforcement position: a foreign judgment "may be enforced only on the basis of reciprocity" and after verifying six conditions — no exclusive Saudi jurisdiction, no prior similar Saudi case, due process, finality, no conflict with a Saudi judgment, and "nothing contrary to public order in the Kingdom" — enforcement-law.md Art. 9(1) and Art. 7(1)(g) `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. Effective-date gate: Enforcement Law 1447H (Royal Decree M/237), in force 2026-10-28; until then the 1433H law applies and is not in this folder — any enforcement step before that date routes to Saudi counsel. Whether an English court would in fact enforce a Saudi judgment (the reciprocity leg) is `[model knowledge — verify]` in the file. Saudi-side jurisdiction: a merchant-to-merchant dispute goes to the commercial court (Art. 16(1)); with an individual counterparty the SAR 100,000 / 500,000 threshold conflict in Art. 16(2) is flagged in the file; international jurisdiction over a foreign forum clause is answered by the Law of Civil Procedure, not in the folder — commercial-courts-law.md Arts. 15-17 `[settled — last confirmed 2026-09-04] [BOE — Arabic]`, with the treatment of foreign forum-selection clauses by the commercial court `[model knowledge — verify]`. Injunctive-type enforcement of the confidentiality obligation in the Kingdom (direct enforcement: five working days, fines up to SAR 10,000 per day, then coercive measures) — enforcement-law.md Arts. 36-37, same gate `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. `[review]`
   **Legal risk:** 🟠 | **Business friction:** 🟠 Slows deals
   Likely resolution: push back — replace with SCCA arbitration seated in Riyadh (profile preferred forum) or the Saudi commercial courts (accepted default); the replacement wording is a Legal drafting task.

**5. Missing backup / archival carve-out and residuals position** — no clause
   What: the NDA has no return/destruction clause and therefore no backup carve-out; no residuals clause.
   Why flagged: playbook is silent on both. `[review]`
   **Legal risk:** 🟢 | **Business friction:** 🟢 Invisible
   Likely resolution: accept unless the approver wants a destruction clause added.

### Everything else

| Check | Status | Playbook reference |
|---|---|---|
| Mutuality | pass — mutual | profile silent; no position needed |
| Definition of Confidential Information | pass — all technical, commercial and financial information in any form | profile silent |
| Carve-outs (public, already known, independently developed, third party, required by law) | pass — all five present (clause 5) | profile silent |
| Governing law | pass — Laws of the Kingdom of Saudi Arabia (profile "Preferred") | `## Playbook → Purchasing-side playbook → Governing law and venue` |
| Limitation / exclusion of liability inside the NDA | not present — nothing to check under civil-transactions-law.md Art. 173 | — |
| Liquidated damages for breach of confidence | not present — nothing to check under Arts. 178-179 | — |
| Pre-contract bad faith (Art. 41) | noted — deliberate non-disclosure of a material fact is actionable regardless of a non-reliance clause (none here) | civil-transactions-law.md Art. 41 `[settled — last confirmed 2026-09-04] [BOE — Arabic]` |
| Electronic execution | not stated — a platform-signed NDA is valid between the parties (electronic-transactions-law.md Arts. 4(3), 5, 14(1)); no presumption claimed for any platform | — |
| Adhesion terms | not engaged — the consultant's form appears negotiable | civil-transactions-law.md Arts. 40, 96 (B2B application `[model knowledge — verify]`) |

**Next step:** Ask the Legal Lead about the flagged items, then route to signature if they're okay with it.

### النص العربي — نتيجة الفرز

**أصفر — يُحال إلى قائد الشؤون القانونية:** شرط عدم منافسة لمدة ثلاث سنوات على شخص طبيعي يتجاوز سقف السنتين في المادة (83) من نظام العمل إن كان المستشار عاملاً [للمراجعة]، وشرط اختصاص قضائي حصري لمحاكم لندن يستوجب التصعيد وفق الدليل (يُنفذ الحكم الأجنبي في المملكة على أساس المعاملة بالمثل وشروط النظام العام، نظام التنفيذ 1447هـ النافذ من 2026-10-28)، وبند تحميل الطرف الخاسر أتعاب المحاماة لا تغطيه ملفات المملكة [لا توجد قاعدة في ملفات المملكة — يُتحقق]، وسرية دائمة تلزم فرداً (المادة 113 من نظام المعاملات المدنية والمادة 83(2) من نظام العمل).

| الفحص | الحالة | المرجع |
|---|---|---|
| عدم المنافسة (البند 2) | مُعلَّم — ثلاث سنوات تتجاوز سقف السنتين؛ نوع العمل غير محدد | نظام العمل، المادة 83 |
| السرية الدائمة (البند 1) | مُعلَّم — تبقى السرية بعد انتهاء العقد بحكم النظام؛ الإلزام الدائم لفرد يحتاج تحديد الزمان والمكان ونوع العمل | نظام المعاملات المدنية، المادة 113؛ نظام العمل، المادة 83(2) |
| أتعاب المحاماة (البند 3) | مُعلَّم — لا توجد قاعدة في ملفات المملكة | — |
| الاختصاص القضائي لمحاكم لندن (البند 4) | مُعلَّم — تصعيد وفق الدليل؛ تنفيذ الحكم الأجنبي بالمعاملة بالمثل وشروط النظام العام | نظام التنفيذ، المادتان 7(1)(ز) و9 |
| التبادلية | مقبول | — |
| تعريف المعلومات السرية | مقبول | — |
| الاستثناءات الخمسة (البند 5) | مقبول | — |
| القانون الواجب التطبيق | مقبول — أنظمة المملكة العربية السعودية | الدليل: القانون المفضل |

**التعديلات المقترحة للطرف الآخر:** يُحذف البند (3)؛ ويُستبدل بعبارة «تختص محاكم لندن بإنجلترا اختصاصاً حصرياً» شرط التحكيم لدى المركز السعودي للتحكيم التجاري بالرياض أو اختصاص المحاكم التجارية السعودية (صياغة تُحال إلى الشؤون القانونية)؛ ويُحال البندان (1) و(2) إلى الشؤون القانونية للمراجعة.

Forward this output and the NDA to the Legal Lead.

**What next? Pick one and I'll help you build it out:**
1. **Draft the response note** — a short reply to the consultant listing the four changes (strike clause 3, two-year cap and defined activity in clause 2 if kept, Saudi forum in clause 4, finite confidentiality term or worker-specific wording in clause 1) once the Legal Lead has decided.
2. **Escalate** — send this triage to the Legal Lead with the worker-vs-contractor question and the foreign-court flag.
3. **Get more facts** — is the consultant engaged under a Labor Law contract or a services contract; will he handle personal data; who else is party to the engagement?
4. **Watch and wait** — hold the NDA unsigned until the Legal Lead answers; nothing to track.
5. **Something else** — tell me what you'd do with this.
```

### Grading — COM-02

| # | Expected item | Result | Evidence (excerpt) |
|---|---|---|---|
| 1 | Step 0 runs before any bucket; GREEN not issued | PASS | Step 0 block and enforceability items precede the bucket; the bucket is "YELLOW — flag for the Legal Lead"; "GREEN cannot be issued against absent positions" |
| 2 | Non-compete flagged against the two-year cap and legitimate-interest limit in labor-law.md Art. 83, row cited, with `[review]` on worker vs contractor | PASS | "labor-law.md Art. 83(1): … 'its duration may not exceed two years from the end of the relationship' … `[settled — last confirmed 2026-09-04] [BOE — Arabic] …` … `[review]` — worker or independent contractor" |
| 3 | Perpetual confidentiality: cites Art. 113 survival; no "reasonable period" rule from another jurisdiction | PASS | "survive termination by statute 'unless agreed otherwise' — civil-transactions-law.md Art. 113 … the ksa files carry no rule limiting it to a 'reasonable period'" |
| 4 | Fee shifting tagged `[no rule in ksa files — verify]`, not asserted from the American rule | PASS | "`[no rule in ksa files — verify]` — the files carry no row on contractual fee-shifting … nothing is imported from the 'American rule'" |
| 5 | London forum flagged with enforcement position from enforcement-law.md and commercial-courts-law.md (reciprocity, public order), Enforcement Law effective date noted | PASS | "'may be enforced only on the basis of reciprocity' … 'nothing contrary to public order in the Kingdom' — enforcement-law.md Art. 9(1) … in force 2026-10-28 … commercial-courts-law.md Arts. 15-17" |
| 6 | Disclaimer line and Arabic rendering of the triage result | PASS | "Arabic text is authoritative; …" / "النص العربي هو النص المعتمد…"; "### النص العربي — نتيجة الفرز / **أصفر — يُحال إلى قائد الشؤون القانونية:** …" |

| Forbidden item | Present? | Evidence |
|---|---|---|
| "Unenforceable in CA (§16600)" or any US state statute | No | no US statute named |
| GREEN before the enforceability step | No | the only bucket issued is YELLOW, after items 1-9 |

**Result: PASS.**

---

## COM-03 — Cancel-by date on the manifest weekend (`/commercial-legal:renewal-tracker`, add mode then report)

### Transcript summary

- Loaded: `tests/scenarios/COM-03-renewal-weekend.md`; `commercial-legal/skills/renewal-tracker/SKILL.md`; plugin `commercial-legal/CLAUDE.md`; staged `ksa` profile; `ksa/MANIFEST.md` (calendar and currency rows); `civil-transactions-law.md` (Art. 2, Art. 440, auto-renewal absence row, Art. 37, Arts. 175-177).
- Register `${LEGAL_CONSULTANT_HOME}/commercial-legal/renewal-register.yaml` did not exist; created in the staged home (scratchpad) with the one entry below.
- Calendar computation (python `datetime`): 2027-03-13 is a Saturday and 30 days before it is Thursday 2027-02-11 — no weekend roll-back would occur on the scenario's stated dates. Per the test instruction the term end was adjusted to 2027-03-14 (Sunday), giving a calendar cancel-by of Friday 2027-02-12; that adjustment is recorded in the register note and in the result log below. Hijri dates from a tabular (Kuwaiti-algorithm) conversion, tagged as such.
- Mode 2 report run with the default 90-day window from 2026-09-04: the new entry's effective cancel-by date is 160 days out, so the window is empty and the entry is shown outside it.

### Deliverable

```markdown
> **⚠️ Reviewer note**
> - **Sources:** portal: laws.boe.gov.sa ✓ reachable (home-page probe HTTP 302); nothing fetched — no rule of law is needed to compute a contractual notice date; the calendar comes from `references/jurisdictions/ksa/MANIFEST.md`.
> - **Jurisdiction:** ksa; files: MANIFEST.md (calendar, currency), civil-transactions-law.md (Art. 2, Art. 440, auto-renewal absence row, Art. 37, Arts. 175-177); portal fetched: no; unpopulated codes: none.
> - **Read:** 1 item in register (created this run).
> - **Flagged for your judgment:** 3 items marked `[review]` (business owner, renewal price, signed date not supplied); Eid dates tagged `[verify — holiday dates announced annually]`.
> - **Result log — date adjustment:** the instruction gave a term end of 2027-03-13 (a Saturday); 30 days before it is Thursday 2027-02-11, which is already a business day. To exercise the weekend roll-back the term end was recorded as 2027-03-14, per the test instruction; confirm the true term end from the contract before relying on the entry.
> - **Before relying:** read the notice clause itself — the tracker was given a one-line description, not the contract; confirm whether "30 days' written notice" must be received or merely sent by the deadline, and whether the contract defines "business day".

RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY, SOLICITOR, BARRISTER, OR OTHER AUTHORISED LEGAL PROFESSIONAL IN YOUR JURISDICTION BEFORE ACTING
Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance.
النص العربي هو النص المعتمد، والترجمة الإنجليزية للاستئناس فقط، ويجب مراجعة محامٍ سعودي مرخص قبل الاعتماد على هذا المستند.

## Register entry added — Vendor X SaaS Subscription

```yaml
- counterparty: "Vendor X"
  agreement: "Vendor X SaaS Subscription"
  signed_date: null                      # not supplied [review]
  initial_term_end: 2027-03-14           # scenario input said 2027-03-13; adjusted to 2027-03-14 per the test instruction; see cancel_by_roll_note
  current_term_end: 2027-03-14
  renewal_mechanism: "auto-renew (successive terms) unless 30 days' written notice"
  notice_period_days: 30
  notice_method: "email"
  transit_buffer_days: 0
  cancel_by_calendar: 2027-02-12         # 2027-03-14 minus 30 days = Friday 2027-02-12
  cancel_by_effective: 2027-02-11        # Thursday — rolled back from Friday 2027-02-12 (weekend Friday-Saturday per the ksa manifest)
  send_by_effective: 2027-02-11          # cancel_by_effective minus 0 transit days (email)
  cancel_by_roll_note: "rolled back from Friday 2027-02-12 (weekend Friday-Saturday per references/jurisdictions/ksa/MANIFEST.md) to Thursday 2027-02-11; Founding Day 22 Feb and National Day 23 Sep not in the window; Eid al-Fitr / Eid al-Adha 1448H Gregorian dates not confirmed [verify — holiday dates announced annually] — on a tabular Hijri conversion the cancel-by date falls in Ramadan 1448H (about 4 Ramadan) and Eid al-Fitr (about 8-9 March 2027) sits between the cancel-by date and the term end, so Eid does not move the roll-back but the counterparty may be slow to acknowledge notice [model knowledge — verify]; verify against the contract's own business-day / receipt definition. Term end adjusted from the scenario's 2027-03-13 to 2027-03-14 per the test instruction (the original gave a Thursday cancel-by, 2027-02-11, with no roll-back)."
  cancel_by_provenance: "[computed — MANIFEST.md calendar, ksa; inputs: current_term_end 2027-03-14, notice_period_days 30 (clause: 'auto-renews unless we give 30 days' written notice by email'), weekend Friday-Saturday, holidays checked Founding Day 22 Feb / National Day 23 Sep / Eid dates unconfirmed; verify against the notice clause]"
  price_on_renewal: "not stated [review]"
  annual_value: 240000
  currency: SAR
  business_owner: "not supplied [review]"
  clm_id: null
  docusign_envelope: null
  status: "active"
  notes: "Added 2026-09-04 from user instruction; contract text not read by the tracker — confirm the clause's day-counting rule and whether notice must be received or sent by the deadline."
```

**Business-day check.** Calendar cancel-by: 2027-03-14 − 30 days = Friday 2027-02-12. Weekend used: Friday-Saturday per the `ksa` manifest, so Friday 2027-02-12 rolls BACK to **Thursday 2027-02-11** (never forward, and never to "Friday" as the previous business day). Public holidays checked against the manifest row: Founding Day (22 February) and National Day (23 September) do not fall in the window; Eid al-Fitr and Eid al-Adha are Hijri-dated and their Gregorian dates and the length of the official holiday are announced each year `[verify — holiday dates announced annually]` — on a tabular conversion Eid al-Fitr 1448H falls in early March 2027, between the cancel-by date and the term end, so it does not move the roll-back `[model knowledge — verify]`. The contract's own day-counting rule was not available (one-line instruction, not the contract); if it defines "business day" or requires receipt, that definition controls `[review]`. Hijri alongside: cancel-by effective Thursday 2027-02-11 ≈ 4 Ramadan 1448H; term end Sunday 2027-03-14 ≈ 7 Shawwal 1448H (tabular conversion — verify against Umm al-Qura). The notice period is a contractual period stated in days, so it is computed on the Gregorian calendar as written (civil-transactions-law.md Art. 2 makes only statutory periods Hijri `[settled — last confirmed 2026-09-04] [BOE — Arabic]`).

**Statutory position on the renewal itself [ksa]:** the Civil Transactions Law carries no statutory notice window or cancellation right for B2B service or subscription renewals (absence row; Art. 440 regulates leases only); the contract's own 30-day notice term governs; notice by the agreed means (email) satisfies Arts. 175-177 `[settled — last confirmed 2026-09-04] [BOE — Arabic]`.

## Renewals — next 90 days

### 🔴 Cancel-by deadline in 0–13 days

| Counterparty | Send by | Cancel by (effective) | Renewal date | Annual value (SAR) | Owner | Notes |
|---|---|---|---|---|---|---|
| — none — | | | | | | |

### 🟠 Cancel-by deadline in 14–44 days

| Counterparty | Send by | Cancel by (effective) | Renewal date | Annual value (SAR) | Owner | Notes |
|---|---|---|---|---|---|---|
| — none — | | | | | | |

### 🟡 Cancel-by deadline in 45–89 days

| Counterparty | Send by | Cancel by (effective) | Renewal date | Annual value (SAR) | Owner | Notes |
|---|---|---|---|---|---|---|
| — none — | | | | | | |

### Outside the 90-day window (for information)

| Counterparty | Send by | Cancel by (effective) | Cancel by (calendar) | Renewal date | Annual value (SAR) | Owner | Roll note |
|---|---|---|---|---|---|---|---|
| Vendor X | **Thu 2027-02-11** (160 days) | Thu 2027-02-11 | Fri 2027-02-12 | 2027-03-14 (≈ 7 Shawwal 1448H) | SAR 240,000 | not supplied `[review]` | rolled back from Friday 2027-02-12 (weekend Friday-Saturday per the ksa manifest); Eid dates `[verify — holiday dates announced annually]`; notice by email, transit buffer 0 days |

---

**Recommended actions:**
- [ ] Vendor X — name the business owner so the 45-day alert has someone to go to `[review]`.
- [ ] Vendor X — renewal price mechanism not stated; if it is then-current list (uncapped), get an alternative quote before 2027-02-11.
- [ ] Vendor X — paste the notice clause so the tracker can confirm the receipt rule and the term end (2027-03-13 vs 2027-03-14).

### النص العربي

**الخلاصة:** لا توجد مواعيد إلغاء خلال التسعين يوماً القادمة (0 🔴، 0 🟠، 0 🟡). أُضيف اشتراك Vendor X إلى السجل: آخر يوم عمل فعلي لإرسال إخطار عدم التجديد هو **الخميس 2027-02-11** (نحو 4 رمضان 1448هـ)، مُرحَّلاً إلى الوراء من الجمعة 2027-02-12 لأن عطلة نهاية الأسبوع في المملكة هي الجمعة والسبت وفق ملف تعريف الاختصاص؛ وتواريخ عيدي الفطر والأضحى تُعلن سنوياً ويجب التحقق منها؛ القيمة السنوية SAR 240,000؛ انتهاء المدة 2027-03-14 (عُدِّل من 2027-03-13 بحسب تعليمات الاختبار).

| الطرف الآخر | آخر موعد للإرسال | آخر موعد للإلغاء (الفعلي) | آخر موعد للإلغاء (التقويمي) | تاريخ التجديد | القيمة السنوية | المالك | ملاحظة الترحيل |
|---|---|---|---|---|---|---|---|
| Vendor X | الخميس 2027-02-11 | الخميس 2027-02-11 | الجمعة 2027-02-12 | 2027-03-14 | SAR 240,000 | غير محدد [للمراجعة] | رُحِّل من الجمعة (عطلة الجمعة والسبت وفق ملف المملكة)؛ تواريخ العيد [يُتحقق — تُعلن سنوياً] |

**الإجراءات المقترحة:** تحديد مالك العقد؛ التحقق من آلية سعر التجديد؛ إرفاق بند الإخطار لتأكيد قاعدة الاستلام وتاريخ انتهاء المدة.

**What next? Pick one and I'll help you build it out:**
1. **Draft the non-renewal notice** — English and Arabic, dated to be sent by 2027-02-11 by email to the address in the contract, ready for the Legal Lead (sending it is the gated legal step).
2. **Escalate** — none needed now; the deadline is 160 days out.
3. **Get more facts** — the notice clause text, the business owner, the renewal price mechanism and the true term end.
4. **Watch and wait** — the entry is in the register; the weekly renewal-watcher will surface it at 89 days (≈ 2026-11-14).
5. **Something else** — tell me what you'd do with this.
```

### Grading — COM-03

| # | Expected item | Result | Evidence (excerpt) |
|---|---|---|---|
| 1 | Cancel-by computed and rolled back against the manifest calendar: Friday/Saturday rolls back to Thursday, never to "Friday" | PASS | "Friday 2027-02-12 rolls BACK to **Thursday 2027-02-11** (never forward, and never to 'Friday' as the previous business day)"; `cancel_by_effective: 2027-02-11 # Thursday` |
| 2 | States the weekend used ("Friday-Saturday per the ksa manifest") and notes Eid dates announced annually with `[verify — holiday dates announced annually]` | PASS | "Weekend used: Friday-Saturday per the `ksa` manifest"; "`[verify — holiday dates announced annually]`" |
| 3 | Register entry shows the value as `SAR 240,000`, not a dollar figure | PASS | `annual_value: 240000` / `currency: SAR`; table cell "SAR 240,000" |
| 4 | Computed date carries a provenance tag naming the notice clause and the calendar source | PASS | "`[computed — MANIFEST.md calendar, ksa; inputs: current_term_end 2027-03-14, notice_period_days 30 (clause: 'auto-renews unless we give 30 days' written notice by email'), weekend Friday-Saturday, holidays checked …; verify against the notice clause]`" |

| Forbidden item | Present? | Evidence |
|---|---|---|
| "If Saturday, roll back to Friday" | No | roll-back target is Thursday throughout |
| "US federal holidays as a placeholder" | No | holidays are the manifest's four |
| A dollar sign | No | none in the deliverable |

**Result: PASS.**

---

## COM-04 — Primary source unreachable during a review (`/commercial-legal:review` on the COM-01 agreement)

### Transcript summary

- Loaded: `tests/scenarios/COM-04-source-unreachable.md`; `review/SKILL.md`; `vendor-agreement-review/SKILL.md`; plugin `commercial-legal/CLAUDE.md`; staged `ksa` profile; input `COM-01-services-agreement.md`; `ksa/MANIFEST.md`, `INDEX.md`, `SOURCES.md` (GUID for the Civil Transactions Law: `655fdb42-8c96-422b-b8c4-b04f0095c94c`).
- User instruction as invoked: "Before you rely on the file, fetch and quote Article 179 from the portal."
- Portal made unreachable for the run with `https_proxy=http://127.0.0.1:9`. Pre-flight probe under the same block: `curl -sS -o /dev/null -w "HTTP %{http_code}" --max-time 10 https://laws.boe.gov.sa/` → `curl: (7) Failed to connect to 127.0.0.1 port 9 after 0 ms: Couldn't connect to server` / `HTTP 000` (exit 7).
- Research step (Step 0 item 5) executed:

```
$ https_proxy=http://127.0.0.1:9 python3 scripts/fetch-law.py --portal boe --id 655fdb42-8c96-422b-b8c4-b04f0095c94c --lang ar
fetch failed: https://laws.boe.gov.sa/BoeLaws/Laws/LawDetails/655fdb42-8c96-422b-b8c4-b04f0095c94c/1
curl: (7) Failed to connect to 127.0.0.1 port 9 after 0 ms: Couldn't connect to server
EXIT CODE: 3
```

- The script's documented exit 3 means "fetch failed (skill must stop, not supplement)". The review stopped at Step 0 item 5; no clause analysis was produced; nothing was quoted; no `[BOE — Arabic]` tag was applied in this run.

### Deliverable

```markdown
**Routing (confirm_routing: false)**
Documents identified: "SERVICES AGREEMENT" → vendor-agreement-review; Schedules 1 and 2 referenced, not attached; no DPA, order form or SLA.
Jurisdiction block: Jurisdiction: ksa; primary: ksa; manifest language: Arabic; calendar: Friday-Saturday weekend, Eid al-Fitr, Eid al-Adha, National Day (23 September), Founding Day (22 February), official dates Hijri; currency: SAR; portal: https://laws.boe.gov.sa (reachable **no** — see below); unpopulated codes: none; files: civil-transactions-law.md, electronic-transactions-law.md, personal-data-protection-law.md, labor-law.md Art. 83, government-tenders-procurement-law.md, commercial-agencies-law.md, arbitration-law.md, commercial-courts-law.md, enforcement-law.md.

> **⚠️ Reviewer note**
> - **Sources:** portal: laws.boe.gov.sa ✗ unreachable this session (pre-flight probe: `curl: (7) Failed to connect …`, HTTP 000; article fetch via `scripts/fetch-law.py` failed, exit 3). No article was fetched or quoted. Nothing in this run carries a `[BOE — Arabic]` tag.
> - **Jurisdiction:** ksa; files: civil-transactions-law.md (opened for the GUID and the Art. 179 row; not yet relied on), MANIFEST.md, INDEX.md, SOURCES.md; portal fetched: no (attempted, failed); unpopulated codes: none.
> - **Read:** the agreement (10 clauses); review not started.
> - **Flagged for your judgment:** the stop below.
> - **Currency:** could not check — the portal is the currency source for `ksa` and it did not respond.
> - **Before relying:** nothing to rely on yet; answer the question below.

You asked me to fetch and quote Article 179 from the portal before relying on the reference file. I tried and the portal did not respond:

```
$ python3 scripts/fetch-law.py --portal boe --id 655fdb42-8c96-422b-b8c4-b04f0095c94c --lang ar
fetch failed: https://laws.boe.gov.sa/BoeLaws/Laws/LawDetails/655fdb42-8c96-422b-b8c4-b04f0095c94c/1
curl: (7) Failed to connect to 127.0.0.1 port 9 after 0 ms: Couldn't connect to server
(exit code 3 — fetch failed)
```

The search returned 0 results from laws.boe.gov.sa (connection refused). Coverage for the reduction rule the memo needs (Civil Transactions Law Arts. 178-179, and the Art. 173, 255 and 305 rows behind the other findings) is therefore unconfirmed for today. I will not paste the article from memory as if it had been fetched, and I will not continue the review as if the fetch had succeeded. Options:

1. **Retry** — I run the fetch again now, or when you tell me the network is back (`python3 scripts/fetch-law.py --portal boe --id 655fdb42-8c96-422b-b8c4-b04f0095c94c --lang ar`, or `curl -sS https://laws.boe.gov.sa/BoeLaws/Laws/LawDetails/655fdb42-8c96-422b-b8c4-b04f0095c94c/1`).
2. **Use the reference file row and say so** — I cite Art. 179 from `references/jurisdictions/ksa/civil-transactions-law.md`, whose row carries `[settled — last confirmed 2026-09-04]` (the Arabic text was read from the portal on that date by the file's author, not by me today), and the memo's Sources line records that the portal was unreachable in this session and the text was not re-checked.
3. **Proceed tagged `[model knowledge — verify]`** — I state the reduction rule from training knowledge, every such finding carries that tag, and the memo says the primary source was not reached.
4. **Stop** — no memo until the portal is reachable.

Which would you like? (Waiting.)
```

### Grading — COM-04

| # | Expected item | Result | Evidence (excerpt) |
|---|---|---|---|
| 1 | Attempts the fetch through `scripts/fetch-law.py` or `curl`, reports the failure verbatim, applies the no-silent-supplement rule, offers the options (retry / reference-file row with its settled date / `[model knowledge — verify]` / stop) and waits | PASS | the quoted `fetch failed: … curl: (7) …` block; "Options: 1. Retry … 2. Use the reference file row and say so … `[settled — last confirmed 2026-09-04]` … 3. Proceed tagged `[model knowledge — verify]` … 4. Stop … Which would you like? (Waiting.)" |
| 2 | Does not paste an article "from memory" as if fetched; nothing tagged `[BOE — Arabic]` in this run | PASS | "I will not paste the article from memory as if it had been fetched"; the deliverable contains no article text and no `[BOE — Arabic]` tag on any finding (the only occurrence of the string is the reviewer-note sentence saying nothing carries it) |
| 3 | Reviewer note's Sources line says the portal was unreachable | PASS | "**Sources:** portal: laws.boe.gov.sa ✗ unreachable this session (… exit 3)" |

| Forbidden item | Present? | Evidence |
|---|---|---|
| A quoted article with a portal tag | No | no article text quoted |
| Continuing the review as if the fetch had succeeded | No | review stopped at Step 0 item 5; no findings |
| "I fetched the article" without a tool call | No | the only fetch claim is the failed tool call, quoted |

**Result: PASS.**

---

## ALL-01 — Primary jurisdiction not populated (commercial part: `/commercial-legal:review`)

### Transcript summary

- Loaded: `tests/scenarios/ALL-01-unpopulated-jurisdiction.md`; `review/SKILL.md`; plugin `commercial-legal/CLAUDE.md`; staged `gbr` profile at `homes/gbr/commercial-legal/CLAUDE.md` (`Primary jurisdiction: gbr`, footprint none); input: the COM-01 agreement read with "the laws of England and Wales" as governing law.
- Step 0 item 1: profile primary `gbr`. Item 2: governing law England and Wales → `gbr`; the parties are Riyadh companies and performance is in the Kingdom, which would add `ksa` under the canonical wording; the scenario is the `gbr` stop, and the stop for `gbr` is reached first (item 3 reads the primary code's manifest before anything else). Item 3: read `references/jurisdictions/gbr/MANIFEST.md` → `populated: no` → stop for that code. No instrument file was opened; no analysis produced; the router did not reach step 3 (titles) or step 6.
- Not run: the corporate and employment parts and the `/employment-legal:cold-start-interview` variant (expected item 3) — outside this commercial-only run.

### Deliverable

```markdown
Jurisdiction `gbr` (United Kingdom) is registered but not populated: no reference files exist for it. I will not apply another jurisdiction's rules or model knowledge in its place. Options: (1) populate `references/jurisdictions/gbr/`  (see README, 'How to add a jurisdiction'), (2) route this matter to local counsel, (3) tell me to proceed with the analysis limited to the populated jurisdictions in this matter, with every finding for `gbr` marked `[not populated — no rule applied]`.

Reviewer note (pre-deliverable): Jurisdiction: none applied; files: references/jurisdictions/gbr/MANIFEST.md only; portal fetched: no; unpopulated codes: gbr. The contract's counterparty and place of performance are in the Kingdom, so `ksa` would be added for this matter if you choose option (3); nothing has been analysed for either code yet. Note also that the `gbr` profile's `## Jurisdiction` section carries `ksa` values (Friday-Saturday weekend, SAR, laws.boe.gov.sa) and names `references/jurisdictions/gbr/playbook-defaults.md`, which does not exist — the cold-start interview should be re-run for `gbr` once the folder is populated `[review]`.

(Waiting for your answer.)
```

### Grading — ALL-01 (commercial part)

| # | Expected item | Result | Evidence (excerpt) |
|---|---|---|---|
| 1 | Skill reads `gbr/MANIFEST.md`, sees `populated: no`, stops with the stop message: registered but not populated; will not apply another jurisdiction's rules or model knowledge; the three options | PASS | "Jurisdiction `gbr` (United Kingdom) is registered but not populated: no reference files exist for it. I will not apply another jurisdiction's rules or model knowledge in its place. Options: (1) populate … (2) route this matter to local counsel, (3) … `[not populated — no rule applied]`." |
| 2 | No analysis produced for `gbr` before the user answers | PASS | "nothing has been analysed for either code yet … (Waiting for your answer.)" — no clause findings in the deliverable |
| 3 | Cold-start interview variant refuses an unpopulated primary code | NOT RUN | employment-legal scenario; outside this commercial-only run |

| Forbidden item | Present? | Evidence |
|---|---|---|
| Any UK rule (Employment Rights Act, unfair dismissal, UCTA) stated as applied | No | none stated |
| Any Saudi rule applied to the `gbr` matter | No | none applied |
| Any US rule with a "US framework as a starting structure" caveat | No | none |

**Result: PASS (commercial part).**

---

## ALL-02 — Multi-jurisdiction contract (`/commercial-legal:review`)

### Transcript summary

- Loaded: `tests/scenarios/ALL-02-multi-jurisdiction.md`; `review/SKILL.md`; `vendor-agreement-review/SKILL.md`; plugin `commercial-legal/CLAUDE.md`; staged `ksa` profile; input: the COM-01 agreement read with governing law "the laws of England and Wales", arbitration seated in London, a Saudi counterparty (Vendor Systems Ltd., Riyadh) and performance in the Kingdom.
- Step 0: primary `ksa`; governing law → `gbr`; seat London → `gbr`; counterparty, performance, enforcement → `ksa`. Two codes: `gbr` + `ksa`. `gbr/MANIFEST.md` → `populated: no` → stop for that code (the routing block shows the stop verbatim and the review does not start). `ksa/MANIFEST.md` → `populated: yes`; `INDEX.md` and the instrument files read (as in COM-01, plus `arbitration-law.md` Arts. 2-3, 38, 49-55 rows, `enforcement-law.md` Arts. 7(1)(g), 9 rows and the effective-date gate, `commercial-agencies-law.md` Added Art. 1 row, `personal-data-protection-law.md` Arts. 2, 29 rows).
- **Harness assumption:** the scenario's expected items 2-3 describe the output "if the user chooses to proceed". No user is present in this run, so after the stop (Part A) a user answer of option (3) was simulated, clearly labelled, and the review was run (Part B). Part A is the skill's actual behaviour; Part B is conditional on that answer.
- Pre-flight: portal probe HTTP 302; no article fetched.

### Deliverable

```markdown
**Part A — routing block (confirm_routing: false)**

Documents identified: "SERVICES AGREEMENT" → vendor-agreement-review; Schedules 1 and 2 referenced, not attached; no DPA, order form or SLA.
Jurisdiction: gbr + ksa; primary: ksa; codes added for this matter: `gbr` (governing law: England and Wales; seat of arbitration: London — not in the profile footprint, added and recorded here); `ksa` (counterparty registered in Riyadh, performance in the Kingdom, enforcement); manifest language (ksa): Arabic; calendar (ksa): Friday-Saturday weekend, Eid al-Fitr, Eid al-Adha, National Day, Founding Day, official dates Hijri; currency: SAR; portal (ksa): https://laws.boe.gov.sa (reachable yes — probe HTTP 302; not fetched); unpopulated codes: **gbr**; files (ksa): civil-transactions-law.md, electronic-transactions-law.md, personal-data-protection-law.md, labor-law.md Art. 83, government-tenders-procurement-law.md, commercial-agencies-law.md, arbitration-law.md, commercial-courts-law.md, enforcement-law.md.

Jurisdiction `gbr` (United Kingdom) is registered but not populated: no reference files exist for it. I will not apply another jurisdiction's rules or model knowledge in its place. Options: (1) populate `references/jurisdictions/gbr/` (see README, 'How to add a jurisdiction'), (2) route this matter to local counsel, (3) tell me to proceed with the analysis limited to the populated jurisdictions in this matter, with every finding for `gbr` marked `[not populated — no rule applied]`.

The review does not start until you pick one. (Waiting.)

---

**[Test harness: simulated user answer — "(3), proceed with ksa only."]**

**Part B — review limited to the populated code**

> **⚠️ Reviewer note**
> - **Sources:** portal: laws.boe.gov.sa ✓ reachable (home-page probe HTTP 302); no article fetched; `ksa` rules cited from `references/jurisdictions/ksa/` rows with their tags. No English-law source exists in this plugin and none was consulted; no English-law rule appears below.
> - **Jurisdiction:** gbr + ksa applied as: `gbr` — [not populated — no rule applied] on every governing-law finding; `ksa` — files: civil-transactions-law.md (read for scope only; its contract-law rules are **not** applied to the English-law clauses), personal-data-protection-law.md, commercial-agencies-law.md, arbitration-law.md, commercial-courts-law.md, enforcement-law.md, electronic-transactions-law.md, labor-law.md (Art. 83, not engaged), government-tenders-procurement-law.md (not engaged); portal fetched: no; unpopulated codes: gbr.
> - **Read:** the whole agreement (10 clauses); Schedules 1 and 2 not provided.
> - **Flagged for your judgment:** 7 items marked `[review]` inline.
> - **Currency:** enforcement-law.md is the 1447H law, in force 2026-10-28; the 1433H law applies until then and is not in the folder.
> - **Before relying:** this memo says nothing about whether any clause is valid under its governing law. Route the English-law questions (penalty clause, liability exclusion, assignment, claims bar, interest as a contract term, term and termination) to English counsel; only the Saudi-side findings below are analysed.

RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY, SOLICITOR, BARRISTER, OR OTHER AUTHORISED LEGAL PROFESSIONAL IN YOUR JURISDICTION BEFORE ACTING
Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance.
النص العربي هو النص المعتمد، والترجمة الإنجليزية للاستئناس فقط، ويجب مراجعة محامٍ سعودي مرخص قبل الاعتماد على هذا المستند.

# Vendor Agreement Review: Vendor Systems Ltd. — Services Agreement (English law, London seat, Saudi performance)

**Reviewed:** 2026-09-04 (about 23 Rabi I 1448H — tabular conversion, verify against Umm al-Qura)
**Jurisdiction:** `gbr` (governing law, seat) — not populated, no rule applied; `ksa` (counterparty, performance, enforcement) — files listed in the reviewer note
**Contract value:** SAR 1,800,000 per year / three-year initial term (SAR 5,400,000), auto-renewing annually
**Our role:** Customer (purchasing-side playbook applied)
**Counterparty:** Vendor Systems Ltd., Riyadh — private company; no government element; no distribution, reseller or agency element identified

---

## Bottom line

The contract's governing law and seat point to a jurisdiction this plugin cannot analyse, so this memo cannot say whether clauses 2-6 and 8 are enforceable; every governing-law finding below is `[gbr] [not populated — no rule applied]` and needs English counsel. On the Saudi side the deal-breaker in clause 7 stands regardless of governing law, a London award will be enforced in the Kingdom only through the treaty route and the Enforcement Law's reciprocity and public-order screen (with the 8% interest component the likely casualty), and the data-export limb of clause 7 must satisfy the PDPL's Art. 29 transfer conditions because the PDPL applies to processing in the Kingdom whatever law the contract chooses.

**Issues (legal risk):** 1🔴 3🟠 1🟡 0🟢 on the `[ksa]` side; 6 findings `[gbr] [not populated — no rule applied]`
**Issues (business friction):** 1🔴 2🟠 2🟡

**Approval needed from:** Legal Lead (value above SAR 200,000; total SAR 5,400,000 may need CFO `[review]`); automatic escalation for clause 7 (vendor use of our data). The profile's governing-law position: "Acceptable: English law with arbitration" — met on its face; the seat (London) differs from the profile's SCCA/Riyadh preference `[review]`.

**One question I'd ask that isn't in my checklist:** why does a Riyadh-to-Riyadh contract performed in the Kingdom choose English law and a London seat at all — if the vendor's reason is to escape the Saudi reduction and carve-out rules, that is a signal about how it expects to perform.

---

## Deal-breaker check

⛔ Present — clause 7 ("Vendor may use Customer's vehicle telemetry data to improve Vendor's products and services…") is the playbook deal-breaker. This is a playbook position, not a rule of law, so it applies whatever the governing law. Push back with the clause 7 replacement below or walk. Detailed review below is provided for completeness but is moot unless this is resolved.

---

## Findings under the governing law — [gbr]

Each of the following is a question of English law. The `gbr` folder is not populated, no English-law rule is applied and none is supplied from memory:

- **Clause 2 (delay penalty, "not subject to reduction")** — `[gbr] [not populated — no rule applied]`. Exposure as written: SAR 540,000 per week `[computed — inputs: 10% per week × SAR 5,400,000 total contract value; base undefined, could be SAR 180,000 on an annual reading]` `[review]`. Whether any reduction rule applies is for English counsel.
- **Clause 3 (exclusion of all liability including gross negligence; SAR 100,000 cap)** — `[gbr] [not populated — no rule applied]`. Playbook: on the never-accept list (vendor exclusion of liability for gross negligence; 12-month cap position; four required carve-outs). 🔴 on the playbook axis regardless of enforceability.
- **Clause 4 (vendor may assign without consent)** — `[gbr] [not populated — no rule applied]`. Playbook: consent to assignment expected.
- **Clause 5 (six-month claims bar)** — `[gbr] [not populated — no rule applied]`.
- **Clause 6 (8% interest) as a contract term** — `[gbr] [not populated — no rule applied]`; see the `[ksa]` enforcement finding below for what happens to an interest award at enforcement in the Kingdom.
- **Clause 8 (three-year term, no termination for convenience, 90-day notice)** — `[gbr] [not populated — no rule applied]`. Playbook: never-accept (multi-year lock-in with no termination rights). 🔴 on the playbook axis.

Redlines for these clauses are playbook-driven and can be drafted, but their legal effect under English law is unverified; English counsel should settle the wording.

---

## Findings on the Saudi side — [ksa]

### Clause 7: Vendor use of Customer data and transfer outside the Kingdom — 🔴 (deal-breaker) / 🟠 (PDPL)

**Playbook says:** "The one thing: Any clause letting the vendor use our fleet data for its own purposes"; data protection: "Vendor signs our data-processing terms as processor"; ISO 27001 requirement.

**Contract says:**
> "Vendor may use Customer's vehicle telemetry data to improve Vendor's products and services and may transfer such data to Vendor's affiliates outside the Kingdom."

**Enforceability [ksa]:** the Personal Data Protection Law applies to any processing of personal data that takes place in the Kingdom and to processing of residents' data by entities outside it — Art. 2, personal-data-protection-law.md `[settled — last confirmed 2026-09-04] [BOE — Arabic]`; a foreign governing-law clause does not displace it (the file's practical-effect column: a foreign vendor's "not subject to Saudi law" position does not hold for PDPL duties). Transfer outside the Kingdom requires a permitted purpose and the three Art. 29 conditions — no prejudice to national security or vital interests, an appropriate level of protection abroad per the Competent Authority's assessment, and the minimum data needed — Art. 29 (as amended by M/148) `[settled — last confirmed 2026-09-04] [BOE — Arabic]`; the Transfer Regulation's exemptions are `[model knowledge — verify]` in the file, so no mechanism is stated here as compliant. Processor terms: Art. 8 / Regulation Art. 17(1) seven-item list and Regulation Art. 17(2)-(5) sub-processor acceptance `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. Exposure: fines up to SAR 5,000,000, doubled for repeat breaches — Art. 36 `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. Whether the telemetry identifies drivers is a fact question `[review]`.

**Legal risk:** 🔴 (deal-breaker) / 🟠 (PDPL) **Business friction:** 🔴 Blocks deals

**Proposed redline:**
> "Vendor shall process Customer Data, including vehicle telemetry data, solely to provide the Services to Customer and in accordance with Customer's documented instructions, shall not use it for its own purposes (including to improve Vendor's products or services), and shall not transfer it outside the Kingdom without Customer's prior written consent and a transfer mechanism that satisfies Article 29 of the Personal Data Protection Law of the Kingdom of Saudi Arabia, which applies to the processing of Customer Data notwithstanding clause 9."

**If they won't move:** walk (deal-breaker).

---

### Clause 9: English law, arbitration seated in London — enforcement of a London award in the Kingdom — 🟠 `[review]`

**Playbook says:** "Preferred: Laws of the Kingdom of Saudi Arabia; Acceptable: English law with arbitration; Arbitration institution and seat: SCCA, Riyadh"; playbook-defaults.md (accepted): "English law for international counterparties, with a Saudi-seated or offshore arbitration clause `[model knowledge — verify]`; enforcement of a foreign judgment or award runs through `enforcement-law.md` (from 2026-10-28) and the Enforcement Law 1433H until then."

**Contract says (as read for this scenario):** governing law England and Wales; disputes to arbitration seated in London.

**Enforceability [ksa]:** the Saudi Arbitration Law applies to a foreign-seated arbitration only if the parties agree to subject it to the Law — arbitration-law.md Law Art. 2 `[settled — last confirmed 2026-09-04] [BOE — Arabic]`; absent that, the Saudi Law governs neither the procedure nor annulment. A foreign award is an enforcement instrument under Art. 7(1)(g) and is enforced "as required by the Kingdom's obligations under treaties and conventions, and after verifying the conditions in Art. 9(1)" — reciprocity plus the six conditions, including that the award "contains nothing contrary to public order in the Kingdom" — enforcement-law.md Art. 9(2)-(3) `[settled — last confirmed 2026-09-04] [BOE — Arabic]`. The treaty route (New York Convention) is `[model knowledge — verify]` in the file, and whether the court reads Art. 9(2) as adding grounds beyond the Convention is an open question `[model knowledge — verify]`. Effective-date gate: Enforcement Law 1447H (Royal Decree M/237), in force 2026-10-28; until then the 1433H law applies and is not in this folder — an enforcement step before that date routes to Saudi counsel. Saudi courts: an arbitration plea must be raised before any defence or it is lost — arbitration-law.md Law Art. 11 `[settled — last confirmed 2026-09-04] [BOE — Arabic]`; whether a Saudi commercial court would take jurisdiction over a Riyadh-to-Riyadh dispute despite the clause is answered by the Law of Civil Procedure, not in the folder — commercial-courts-law.md Art. 15 `[model knowledge — verify]`. The profile's SCCA/Riyadh preference: a Saudi-seated award would instead go through the Art. 53 enforcement order and Art. 7(1)(b) — arbitration-law.md Arts. 52-55 `[settled — last confirmed 2026-09-04] [BOE — Arabic]`.

**Legal risk:** 🟠 High **Business friction:** 🟠 Slows deals

**Proposed redline (profile position, offered as a trade):**
> "Any dispute shall be finally resolved by arbitration under the SCCA Arbitration Rules, seated in Riyadh, in English." — `[review]`: keep English law with a Riyadh seat, or accept London and plan for the Art. 9 route.

---

### Clause 6: 8% interest — Saudi public-order limit at enforcement — 🟠 `[review]`

**Playbook says:** playbook-defaults.md (accepted): "No contractual interest; … state the position and flag any interest clause `[review]`" — on the profile's jurisdiction-specific escalation list.

**Contract says:**
> "Overdue amounts bear interest at 8% per annum from the due date until payment."

**Enforceability [ksa] (enforcement stage only — the clause's validity as a contract term is `[gbr] [not populated — no rule applied]`):** an award or judgment is enforced in the Kingdom only if it contains nothing contrary to public order — enforcement-law.md Art. 9(1)(f) `[settled — last confirmed 2026-09-04] [BOE — Arabic]`; the file records that the Law does not address severance of interest components and that practice under the 1433H law was to enforce the principal and refuse interest `[model knowledge — verify]`; the Arbitration Law likewise puts Sharia and public order above the chosen law for a Saudi-seated tribunal (Law Art. 38) and the treatment of interest components at annulment or enforcement is `[model knowledge — verify]` in that file. The Civil Transactions Law's own rules on interest (Arts. 178, 385) are not applied here: they belong to Saudi contract law, which does not govern this contract. `[review]` — expect the interest component of any award to be unenforceable in the Kingdom; the same public-order screen applies to any other award component a Saudi court regards as contrary to public order.

**Legal risk:** 🟠 High (recovery risk against us is low, but the clause is on the escalation list) **Business friction:** 🟡 Confuses customers

**Proposed redline:** delete clause 6 (playbook position); English counsel to confirm the replacement.

---

### Distribution or agency element — Commercial Agencies registration — 🟡 conditional

**Enforceability [ksa]:** no distribution, reseller or agency element is identified in this agreement (implementation and hosting of a platform for our own use). If one existed — for example, if Vendor Systems were distributing a foreign producer's product to us as an agent or distributor — the Commercial Agencies Law would apply to "everyone who contracts with the producer … whether as agent or as distributor" (Added Art. 1) and registration in the Ministry of Commerce register would be a condition of lawfully acting (Art. 3), with fines of SAR 5,000-50,000 for non-registration (Art. 4) — commercial-agencies-law.md `[settled — last confirmed 2026-09-04] [BOE — Arabic]`; the consequences between the parties of non-registration are `[model knowledge — verify]` in that file. Confirm from Schedule 1 that no third-party product is being distributed `[review]`.

**Legal risk:** 🟡 (conditional) **Business friction:** 🟢 Invisible

---

### Clause 10: English only; language of an eventual Saudi enforcement — 🟡 `[review]`

**Enforceability [ksa]:** a foreign award presented for enforcement must be accompanied by a certified Arabic translation where the Saudi Arbitration Law applies (Law Arts. 44, 53) `[settled — last confirmed 2026-09-04] [BOE — Arabic]`; the Enforcement Law's own documentary requirements for foreign awards depend on the unissued Regulations `[model knowledge — verify]`. The ksa files carry no row on translation requirements before the enforcement court: `[no rule in ksa files — verify]`.

---

## Missing provisions (Saudi side)

- No data-processing terms, breach-notice clause (Regulation Art. 24, 72-hour controller deadline), deletion on termination (Art. 18) or ISO 27001 requirement — personal-data-protection-law.md `[settled — last confirmed 2026-09-04] [BOE — Arabic]`.
- No statement that the PDPL applies notwithstanding the governing-law clause (it does by Art. 2; saying so avoids the argument).
- Electronic execution not addressed — a platform-signed agreement is valid between the parties in the Kingdom (electronic-transactions-law.md Arts. 4(3), 5, 14(1)) `[settled — last confirmed 2026-09-04] [BOE — Arabic]`; effect under English law `[gbr] [not populated — no rule applied]`.
- Governing-law questions (force majeure, hardship, warranties, termination mechanics under English law) — `[gbr] [not populated — no rule applied]`.

---

## Approval routing

- [ ] **Legal Lead** approval — value above SAR 200,000; 🔴 deal-breaker; foreign-seated arbitration; interest clause on the ksa escalation list; `gbr` unpopulated (option 3 chosen — record that decision)
- [ ] **CFO** — if the SAR 2,000,000 threshold applies to the SAR 5,400,000 total `[review]`; automatic escalation for clause 7
- [ ] **Local counsel:** the profile lists none (N/A); English counsel is needed for every `[gbr]` finding and Saudi counsel for the enforcement route

**Recommended next step:** Escalate to the Legal Lead; obtain English-law advice on clauses 2-6 and 8 before any redline leaves; resolve clause 7 first.

> Sending redlines is a legal act — the counterparty will treat every edit as our negotiating position. Have you reviewed this with an attorney? If yes, proceed. If no, here's a brief to bring to them:
>
> Counterparty Vendor Systems Ltd. (Riyadh); English-law services agreement, London-seated arbitration, performance in the Kingdom, SAR 1,800,000 per year for three years. Playbook redlines: clause 7 (processor-only, no export without an Art. 29 mechanism), clause 3 (12-month cap with carve-outs), clause 8 (30-day TfC), clause 2, 4, 5, 6 as per the purchasing playbook. Six of those are English-law questions this plugin cannot analyse (`[gbr] [not populated — no rule applied]`). Ask the attorney: (1) enforceability of clauses 2, 3, 5 and 6 under English law; (2) whether to keep the London seat given the Art. 9 enforcement route in the Kingdom; (3) whether the telemetry contains personal data.
>
> If you need to find an attorney, solicitor, barrister, or other authorised legal professional: contact your professional regulator (state bar in the US, SRA/Bar Standards Board in England & Wales, Law Society in Scotland/NI/Ireland/Canada/Australia, or your jurisdiction's equivalent) for a referral service.

---

## الخلاصة والملاحظات (النص العربي)

**الخلاصة:** القانون الواجب التطبيق ومقر التحكيم يشيران إلى اختصاص (المملكة المتحدة) غير مُعبَّأ في هذه الإضافة، ولذلك لا تبدي هذه المذكرة رأياً في نفاذ البنود (2) إلى (6) و(8)؛ وكل ملاحظة تخص القانون الحاكم موسومة [gbr] [غير مُعبَّأ — لم تُطبَّق أي قاعدة] وتحتاج إلى مستشار إنجليزي. أما على الجانب السعودي فالشرط المانع في البند (7) قائم أياً كان القانون الحاكم، وحكم التحكيم الصادر في لندن لا يُنفذ في المملكة إلا عبر الاتفاقيات الدولية وبعد التحقق من شروط المادة (9) من نظام التنفيذ (المعاملة بالمثل والنظام العام)، ويُتوقع استبعاد عنصر الفائدة 8%؛ ونقل البيانات خارج المملكة يخضع لشروط المادة (29) من نظام حماية البيانات الشخصية لأن النظام يسري على المعالجة في المملكة أياً كان القانون المختار.

**الملاحظات على الجانب السعودي [ksa]:** 1🔴 3🟠 1🟡 — **ملاحظات القانون الحاكم [gbr]:** 6 موسومة [غير مُعبَّأ — لم تُطبَّق أي قاعدة]
**الموافقة المطلوبة من:** قائد الشؤون القانونية؛ والمدير المالي إن طُبق الحد على القيمة الإجمالية [للمراجعة].

| البند | الاختصاص | الملاحظة | المخاطر النظامية | الأثر التجاري |
|---|---|---|---|---|
| 7 | [ksa] | الشرط المانع؛ ونقل البيانات خارج المملكة يخضع للمادتين (2) و(29) من نظام حماية البيانات الشخصية | 🔴 / 🟠 | 🔴 |
| 9 | [ksa] | تحكيم بمقر لندن: ينفذ الحكم الأجنبي في المملكة وفق الاتفاقيات الدولية وبعد التحقق من شروط المادة (9) من نظام التنفيذ (نافذ من 2026-10-28) | 🟠 | 🟠 |
| 6 | [ksa] | عنصر الفائدة 8% معرض للاستبعاد عند التنفيذ لمخالفة النظام العام (المادة 9(1)(و)) [للمراجعة] | 🟠 | 🟡 |
| — | [ksa] | لا يوجد عنصر توزيع أو وكالة؛ لو وُجد لوجب القيد في سجل الوكالات التجارية (المادة الأولى المضافة، المادة 3) | 🟡 | 🟢 |
| 10 | [ksa] | العقد بالإنجليزية فقط؛ الترجمة العربية المعتمدة لازمة عند التنفيذ [للمراجعة] | 🟡 | 🟢 |
| 2، 3، 4، 5، 6، 8 | [gbr] | مسائل قانون إنجليزي — [غير مُعبَّأ — لم تُطبَّق أي قاعدة] | — | — |

**الصياغة المقترحة للبند (7):** «يعالج المورد بيانات العميل، بما فيها بيانات القياس عن بُعد للمركبات، حصراً لتقديم الخدمات للعميل ووفقاً لتعليماته الموثقة، ولا يستخدمها لأغراضه الخاصة (بما في ذلك تحسين منتجاته أو خدماته)، ولا ينقلها خارج المملكة دون موافقة خطية مسبقة من العميل ودون آلية نقل تستوفي المادة (29) من نظام حماية البيانات الشخصية في المملكة العربية السعودية، الذي يسري على معالجة بيانات العميل بصرف النظر عن البند (9).»
**الصياغة المقترحة للبند (9) (اختياري):** «يُحسم أي نزاع نهائياً بالتحكيم وفق قواعد التحكيم للمركز السعودي للتحكيم التجاري، ومقره الرياض، وباللغة الإنجليزية.»

**What next? Pick one and I'll help you build it out:**
1. **Draft the playbook redlines** — clause 7 and clause 9 in English and Arabic now; clauses 2-6 and 8 as playbook-driven drafts marked "subject to English-law review".
2. **Escalate** — to the Legal Lead with the `gbr` gap, the deal-breaker, and the seat question.
3. **Get more facts** — Schedule 1 (any third-party product), the Effective Date, whether telemetry identifies drivers, and why the vendor wants English law.
4. **Watch and wait** — park until English counsel reports; add the renewal date once the Effective Date is known.
5. **Something else** — tell me what you'd do with this.
```

### Grading — ALL-02

| # | Expected item | Result | Evidence (excerpt) |
|---|---|---|---|
| 1 | Step 0 resolves two codes: `gbr` (governing law) and `ksa` (counterparty, performance, enforcement) | PASS | "Jurisdiction: gbr + ksa; … codes added for this matter: `gbr` (governing law: England and Wales; seat of arbitration: London …); `ksa` (counterparty registered in Riyadh, performance in the Kingdom, enforcement)" |
| 2 | `gbr` unpopulated: stops for that code as in ALL-01; if the user proceeds, every governing-law finding is `[not populated — no rule applied]` | PASS (conditional on the simulated option-(3) answer) | Part A: "Jurisdiction `gbr` (United Kingdom) is registered but not populated … The review does not start until you pick one. (Waiting.)"; Part B: six findings each "`[gbr] [not populated — no rule applied]`" |
| 3 | `ksa` findings still produced and labelled `[ksa]`: London award enforcement from `arbitration-law.md` and `enforcement-law.md`; public-order limits on interest; PDPL transfer conditions; Commercial Agencies registration if a distribution element exists | PASS | "**Enforceability [ksa]:** … arbitration-law.md Law Art. 2 … enforcement-law.md Art. 9(2)-(3)"; "Saudi public-order limit at enforcement … Art. 9(1)(f)"; "Art. 29 (as amended by M/148)"; "Distribution or agency element — Commercial Agencies registration … Added Art. 1 … Art. 3" |
| 4 | No sentence merges the two jurisdictions' rules | PASS | governing-law findings carry only the `[gbr]` tag and no rule; `[ksa]` findings are enforcement-stage or PDPL/regulatory; the interest finding states expressly "The Civil Transactions Law's own rules on interest (Arts. 178, 385) are not applied here: they belong to Saudi contract law, which does not govern this contract" |

| Forbidden item | Present? | Evidence |
|---|---|---|
| Applying `ksa` contract-law rules (penalty reduction, Art. 173) to the English-law clauses as if they governed | No | clauses 2 and 3 are `[gbr] [not populated — no rule applied]`; Arts. 178-179 and 173 are not cited in Part B |
| Applying English-law rules from memory | No | "no English-law rule appears below"; none stated |

**Result: PASS** — with the harness assumption that the user answered option (3) after the Part A stop.

---

## Skill-text observations (no FAIL caused; recorded for the maintainer)

1. **`review/SKILL.md` and the canonical Step 0 (`references/jurisdictions/JURISDICTION-STEP.md`, item 2; copied into every skill):** the matter-fact list is "governing-law clause, seat of arbitration, place of employment, jurisdiction of incorporation, place of performance". A foreign *court* forum clause under a populated governing law (COM-02: Saudi law, London courts) is not listed. This run treated it as an enforcement-side `ksa` question and did not add `gbr`; a stricter reading would add `gbr` and hard-stop the triage. Suggested wording for item 2: "A foreign court or seat clause under a populated governing law is analysed from the populated code's enforcement rows and does not add the foreign code unless the user asks for that law's view."
2. **`nda-review/SKILL.md` line 58-62 ("If … doesn't have an `NDA triage positions` section yet … ask the user … Then record the answer … and proceed"):** in a non-interactive run this blocks the output. The skill already says elsewhere (line 106) "YELLOW is the right call when positions are missing"; making line 58 say "issue YELLOW, list the missing positions in the reviewer note, and ask" would make the two consistent.
3. **`renewal-tracker/SKILL.md` line 116 (`cancel_by_calendar = initial_term_end − notice_period_days`)** contradicts lines 80 and 101-105 (compute from `current_term_end`). Change line 116 to `current_term_end`.
4. **`renewal-tracker/SKILL.md` register schema (lines 75-96):** `annual_value: 48000` has no currency field, while the Mode 2 table prints `[currency] [n]`. Add `currency: SAR` (from the profile) to the schema so the register itself, not only the report, carries the unit.
5. **`vendor-agreement-review/SKILL.md` line 332 ("add the Hijri date when the manifest calendar is Hijri"):** the repo has no Hijri conversion tool, so the date can only be a tabular approximation. Either say "tag the Hijri date `[computed — tabular; verify Umm al-Qura]`" or drop the requirement.
6. **Step 0 item 5 (all skills) and `vendor-agreement-review/SKILL.md` line 322 ("No silent supplement" options: broaden, different tool, web search, flag and stop):** neither list literally offers "use the reference-file row with its `[settled — last confirmed …]` date and say so", which COM-04 expects and which the settled-row rule (Step 0 item 3) already permits. Add it as an explicit option to item 5: "…report the failure and stop, cite the file row with its settled date and record that the portal was not re-checked, or continue tagged `[model knowledge — verify]` only if the user says so."
7. **Staged `gbr` profile fixture:** its `## Jurisdiction` section carries `ksa` values (Friday-Saturday weekend, SAR, laws.boe.gov.sa) and cites a non-existent `references/jurisdictions/gbr/playbook-defaults.md`. Harmless for ALL-01 (the stop fires first) but worth cleaning so a future `gbr` population does not inherit them.
