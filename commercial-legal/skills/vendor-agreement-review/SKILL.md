---
name: vendor-agreement-review
description: >
  Reference: review of an inbound vendor agreement against the team playbook in
  `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md`. Flags deviations, assesses risk, generates
  specific redline language, and routes to the right approver. Loaded by
  /commercial-legal:review when a vendor MSA, services agreement, or similar is detected.
user-invocable: false
---

# Vendor Agreement Review

## Matter context

**Matter context.** Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗` (the default for in-house users), skip the rest of this paragraph — skills use practice-level context and the matter machinery is invisible. If enabled and there is no active matter, ask: "Which matter is this for? Run `/commercial-legal:matter-workspace switch <slug>` or say `practice-level`." Load the active matter's `matter.md` for matter-specific context and overrides. Write outputs to the matter folder at `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/matters/<matter-slug>/`. Never read another matter's files unless `Cross-matter context` is `on`.

---

## Destination check

Before producing output, check where it's going. If the user has named a destination (a channel, a distribution list, a counterparty, "everyone"), ask whether it's inside the privilege circle. Public channels, company-wide lists, counterparty/opposing counsel, vendors, and clients (for work product) waive the protection. When the destination looks outside the circle, flag it and offer (a) the privileged version for legal only, (b) a sanitized version for the broader channel, or (c) both — don't silently apply a privileged header and then help paste it somewhere the header won't protect it. See the canonical `## Shared guardrails → Destination check` in this plugin's CLAUDE.md.

## Purpose

Read a vendor agreement against the playbook this team actually uses (in `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md`), find every term that deviates, and tell the lawyer what to do about each one — with specific redline language, not vague "consider revising."

The output is a review memo the lawyer can act on in one pass. Every issue has a severity, a business-impact explanation, a proposed fix, and an escalation call if one is needed.

## Precondition: load the playbook

**Before reading the contract, read `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md`.** If it's missing or still has placeholders, surface this bounce:

> I notice you haven't configured your practice profile yet — that's how I tailor playbook positions, escalation, and house style to your practice.
>
> **Two choices:**
> - Run `/commercial-legal:cold-start-interview` (2 minutes) to configure your profile, then I'll review tailored to YOUR playbook.
> - Say **"provisional"** and I'll review against generic defaults — middle risk appetite, lawyer role, no playbook (flag all common vendor-contract risks from first principles) — and tag every output `[PROVISIONAL — configure your profile for tailored output]` so you can see what I do before committing. Provisional mode still needs a jurisdiction: I'll ask you for the code before I read the contract.

### Provisional mode

If the user says "provisional," run the review normally using these generic defaults: middle risk appetite, lawyer role, no playbook (flag the common vendor-side risks from first principles — unlimited liability, no data-breach carveout, uncapped indemnity, auto-renewal without notice, etc. — rather than matching to configured positions). Tag the reviewer note and every finding block with `[PROVISIONAL]`.

**Provisional mode has no default jurisdiction.** The jurisdiction is the profile's primary code when a profile with a `## Jurisdiction` section exists (a profile that is otherwise placeholders may still carry it). When there is no profile, or its `## Jurisdiction` section is missing or a placeholder, **ask** before reading the contract: "Provisional review needs a jurisdiction. Which code applies — `ksa`, `gbr`, `fra`, `che`, `usa`? (`references/jurisdictions/REGISTRY.md` lists which are populated.)" Then run Step 0 items 2-8 against the answer, including the unpopulated-jurisdiction stop. Never assume `usa`; a review that silently applies one jurisdiction's enforceability rules to another's contract is the confident-wrong output this plugin exists to prevent. Tag the memo `[PROVISIONAL — jurisdiction <code> supplied by user]`. At the end of the output, append:

> "That was a generic run against default assumptions. Run `/commercial-legal:cold-start-interview` to get output calibrated to YOUR practice — your playbook, your jurisdiction, your risk appetite. 2 minutes."

**Which side?** Before applying the playbook, determine which side the company is on for this contract. Usually obvious: if the counterparty is a vendor/supplier providing goods or services, you're purchasing-side. If the counterparty is a customer buying your product/service, you're sales-side. If it's not obvious (a reseller agreement, a partnership, a revenue share), ask: "Which side is [company] on for this agreement — vendor or customer?" Read the matching playbook section (`### Sales-side playbook` or `### Purchasing-side playbook`) from the config. Note which side in the output so the reviewer knows which playbook was applied. If the matching side is `[Not configured]`, stop and tell the user to run `/commercial-legal:cold-start-interview --side <side>` before this review can proceed.

This skill is typically used for purchasing-side contracts (vendors supplying you), but the side check still applies — a "vendor agreement" could be your own template sent to a vendor as part of a reseller arrangement (sales-side).

The playbook in `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md` is the source of truth. It tells you:
- What this team's standard positions are (not market standard — *their* standard)
- What fallbacks they've accepted before
- What they never accept
- Who approves what
- The one deal-breaker to check first

If the contract has the deal-breaker, flag it at the top of the memo and stop the detailed review. There's no point spending 30 minutes on liability caps if the agreement gives the vendor rights to use customer data for training.

## Workflow

### Step 0: Resolve the applicable jurisdiction

1. **Read the practice profile's `## Jurisdiction` section.** It gives the primary jurisdiction code, the footprint list (other codes the practice operates in), the output-language preference, and whether local counsel is available for escalation. Codes are ISO 3166-1 alpha-3 lowercase (`ksa`, `gbr`, `fra`, `che`, `usa`). If the section is missing or still a placeholder, stop: "The practice profile has no jurisdiction. Run the cold-start interview; nothing in this skill can run against the wrong jurisdiction."
2. **Determine the matter's jurisdiction(s).** Start from the primary code. Then read the matter facts: governing-law clause, seat of arbitration, place of employment, jurisdiction of incorporation, place of performance. If the facts point to a code not in the profile, add it for this matter and say so in the reviewer note. A matter may have more than one code (a contract governed by English law with a Saudi counterparty and Saudi performance is `gbr` + `ksa`). A foreign court forum or arbitral seat under a populated governing law is analysed from the populated code's enforcement rows (whether that forum's judgment or award would be enforced there); it does not add the foreign code unless the user asks for that law's view, and the reviewer note says the forum-side question was not analysed.
3. **Load the jurisdiction folder for each code.** The folder is `references/jurisdictions/<code>/` in this plugin (the same tree ships at the repo root and in every runtime adapter). Read `MANIFEST.md` first.
   - If `populated` is not `yes`: **stop for that code.** Say: "Jurisdiction `<code>` (<name>) is registered but not populated: no reference files exist for it. I will not apply another jurisdiction's rules or model knowledge in its place. Options: (1) populate `references/jurisdictions/<code>/` (see README, 'How to add a jurisdiction'), (2) route this matter to local counsel, (3) tell me to proceed with the analysis limited to the populated jurisdictions in this matter, with every finding for `<code>` marked `[not populated — no rule applied]`." Wait for the answer. Never fall back silently.
   - If the code is `usa`: there is no folder. Follow this skill's US path (the upstream doctrine and the upstream research connectors, CourtListener or Westlaw, with the upstream "no silent supplement" rule). Label findings `[usa]`.
   - If `populated` is `yes`: read `INDEX.md`, then the instrument files this skill names in its "Jurisdiction files" list. A row tagged `[settled — last confirmed YYYY-MM-DD]` may be applied and cited by article. A row tagged `[model knowledge — verify]` may be applied only with that tag carried onto the finding. If a rule this skill needs is not in the files at all, do not supply it from memory: say what is missing, tag the gap `[no rule in <code> files — verify]`, and continue only with the rules that exist.
4. **Multi-jurisdiction matters.** Run the relevant files side by side. Label every finding with its code in square brackets, `[ksa]`, `[gbr]`, `[usa]`, and never merge two jurisdictions' rules into one sentence. Where the codes conflict (a clause valid under one law and reducible under another), state both and flag `[review]` for the lawyer to decide which governs.
5. **Research step (when a rule must be quoted or its currency checked).** Use the portal named in `MANIFEST.md` → `research_tool`. For `ksa`: `python3 scripts/fetch-law.py --portal boe --id <guid> --lang ar` (GUIDs in `SOURCES.md`), or `curl -sS https://laws.boe.gov.sa/BoeLaws/Laws/LawDetails/<guid>/1`; the built-in web-fetch tool rejects the portal's TLS chain. Quote the article, tag `[BOE — Arabic]` (or `[BOE — official English]` when quoting the translation), and check the status line and the "تعديلات المادة" block for amendments. If the fetch fails or the article is not found, apply the "no silent supplement" rule: report the failure and stop. A stopped run still emits: the reviewer note (item 8) with `portal fetched: no` and a Sources line recording which fetch failed; every finding or number that depends on the unfetched article, listed as PENDING; and the options: (1) cite the jurisdiction file's row under its own `[settled — last confirmed YYYY-MM-DD]` tag, stating that the portal was not re-checked this session, (2) retry the fetch by another route (`curl`, the script) or hand the check to local counsel, (3) continue with the rule tagged `[model knowledge — verify]`. Take none of them until the user chooses. Nothing in a stopped run is tagged `[BOE — Arabic]` or `[BOE — official English]`.
6. **Calendar and language.** Take the weekend, public-holiday, calendar (Hijri or Gregorian) and currency rules from `MANIFEST.md`. Compute every date and roll-back against that calendar, never against a Saturday/Sunday weekend or US federal holidays. Produce the deliverable in English; when the profile's output-language preference is bilingual, or the manifest's authoritative language is not English and counterparty-facing text is produced, add the authoritative-language rendering of the bottom line, the findings table, and any counterparty-facing text, using the spellings in the manifest's `output_language_rule`.
7. **Header and disclaimer.** Prepend the manifest's `disclaimer` line under the work-product header for every deliverable that applies a non-`usa` jurisdiction. For `ksa`: "Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance." with its Arabic rendering from the manifest.
8. **Record in the reviewer note.** `Jurisdiction: <codes applied>; files: <list>; portal fetched: yes/no; unpopulated codes: <list or none>.`

**Jurisdiction files this skill loads** (for each populated non-`usa` code resolved in Step 0; article numbers are the `ksa` rows that exist today, other codes use the same file names):

- `civil-transactions-law.md` — Step 3 enforceability: Arts. 178-179 (agreed compensation, penalties, service credits: reduction, no-harm defence, no contracting out, not for money debts), Art. 173 (exclusion limits: fraud/gross fault carve-out mandatory, tort not excludable), Art. 180 (foreseeability), Art. 97 (hardship, mandatory), Arts. 110, 125, 174 (force majeure and risk allocation), Arts. 98, 238-240, 248-254, 255-258 (assignment of rights, debts, contract), Arts. 295-306 (limitation: 10/5/1 Hijri years, no contractual shortening), Art. 113 (confidentiality and dispute-resolution survival), Arts. 171, 178, 385 (interest and late-payment charges), Arts. 107-108, 111 (termination, i'thar, prospective effect), Arts. 114, 191, 281-288 (suspension and set-off), Arts. 109, 338-344 (warranties), Arts. 578-606 (guarantees), Arts. 40, 96, 104 (adhesion terms, interpretation), Royal Decree M/191 para. 5 (retroactivity).
- `electronic-transactions-law.md` — Step 3 execution and notices: Arts. 4(3), 5, 6-7, 10-11, 12-13, 14(1), 14(3)-(4), Art. 3 exclusions.
- `personal-data-protection-law.md` — Step 3 data protection: Art. 8 and Regulation Art. 17(1) (seven mandatory processor terms), Regulation Art. 17(2)-(5) (instructions, deviation notice, assessment right, sub-processor acceptance), Art. 20 and Regulation Art. 24 (breach notice, 72-hour controller deadline), Art. 18 (deletion on termination), Art. 29 (transfer purpose and conditions), Art. 31 and Regulation Art. 33 (records), Arts. 36 and 40 (exposure for caps and indemnities), Art. 2 (extraterritorial reach).
- `labor-law.md` — Step 3 restrictive covenants when the counterparty is an individual: Art. 83 (written, specific as to time, place and type of work, two-year cap, one-year limitation from discovery).
- `government-tenders-procurement-law.md` — Step 1 counterparty type, when the counterparty is a government entity: the applicable procurement rows by matter date (the file's header says which law applies; cite every article as "1448H Art. N" or "2019 Art. N"): who is bound (1448H Arts. 1, 10, 11, 95 / 2019 Arts. 1, 10, 11, 93), form of contract (1448H Arts. 52, 93 / 2019 Arts. 55, 91), performance bond (1448H Arts. 59-61 / 2019 Arts. 61-63), variation limits (1448H Art. 67 / 2019 Art. 69), assignment and subcontracting consents (1448H Arts. 68-69 / 2019 Arts. 70-71), delay-penalty cap (1448H Art. 70 / 2019 Art. 72), extension and penalty relief (1448H Art. 72 / 2019 Art. 74), termination (1448H Arts. 74-76 / 2019 Arts. 76-78), grievance route (1448H Arts. 84-86 / 2019 Arts. 86-87), disputes and arbitration (1448H Art. 94 / 2019 Art. 92).
- `commercial-agencies-law.md` — Step 3 regulatory compliance for distribution, reseller and agency structures: Arts. 1, 3, Added Arts. 1-2 (registration, distributors in scope, spare-parts tail), Art. 4 (penalties).
- `arbitration-law.md` — Step 3 dispute resolution: Law Arts. 2, 9, 10, 14, 22-23, 28-29, 40, 51; SCCA Rules rows only when the clause names the SCCA.
- `commercial-courts-law.md` — Step 3 governing law, forum and notices: Arts. 6, 9-12, 13, 16, 17, 19, 24, 38, 74.
- `enforcement-law.md` — Step 3 dispute resolution, security and payment terms: Arts. 7, 8, 9, 11, 18, 24, Decree para. 5, with the effective-date gate stated in that file.
- `playbook-defaults.md` (Commercial table) — only to explain a profile position that the cold-start interview took from it; never as a rule of law.

### Step 1: Orient

Read the whole agreement once, fast. Answer:

| Question | Answer |
|---|---|
| What kind of agreement is this? | MSA / SaaS subscription / Professional services / License / Other |
| Who are we? | Customer / Vendor (this plugin assumes customer — flag if not) |
| Counterparty | Name, and are they a BigCo (won't negotiate) or a startup (will)? |
| Counterparty type | Private company / individual (sole trader, consultant) / government entity or a company acting on its behalf / state-owned company / distributor or agent. This row decides which jurisdiction files Step 3 loads: an individual counterparty brings in `labor-law.md` Art. 83 for any restrictive covenant; a government entity brings in `government-tenders-procurement-law.md` (for `ksa`: check the who-is-bound row of the applicable procurement rows by matter date, 1448H Arts. 1, 10, 11, 95 / 2019 Arts. 1, 10, 11, 93 — a state-owned company is presumptively outside that Law, `[model knowledge — verify]`, so review its own terms); a distribution, reseller or agency structure brings in `commercial-agencies-law.md`. |
| Governing law, forum, place of performance | As written in the contract. Compare with the codes resolved in Step 0 (or passed in by the router); if the clause points to a code not yet resolved, add it now, run Step 0 item 3 for it (including the unpopulated stop), and say so in the reviewer note. |
| Contract value ([currency] from the profile `## Jurisdiction`) | Annual / total contract value if stated, in the currency the contract states; convert to the profile currency only for threshold routing and show both |
| Term | Length, renewal mechanics |
| Is there a DPA? | Attached / referenced by URL / missing |
| Is there an order form? | Separate doc or integrated |
| Signed before the applicable civil code took effect? | For `ksa`: a contract dated before 2023-12-16 is still governed by the Civil Transactions Law unless a party pleads a contrary pre-Law judicial principle — state Royal Decree M/191 para. 5 from `civil-transactions-law.md` and flag `[review]`. Other codes: the equivalent row in their file, or `[no rule in <code> files — verify]`. |

**Contract-value handling.** If the main agreement does not state a contract value (the MSA sets terms but the Order Form carries price, which is typical), **stop and ask** before running escalation math or applying value thresholds:

> The MSA itself doesn't state an annual contract value. The Order Form carries the price. Your escalation threshold is [currency] [X from the matrix]. Before I route this, I need the annual contract value. Options:
> 1. Paste the Order Form value (preferred — I'll use it for routing and the memo).
> 2. Tell me if this is above or below [currency] [threshold] and I'll route accordingly; the memo will flag that the routing assumed [above/below threshold] without a contract value in hand.
> 3. Route conservatively to the higher approver regardless — safer for a review you haven't priced.

Do NOT silently assume a value and then use the assumed value to drive routing. The assumption propagates into the approval call, which is a place the review shouldn't be guessing. `[currency]` is the code in the profile `## Jurisdiction` → Currency for thresholds (for `ksa`: SAR); never write a currency symbol the profile does not carry.

**DPA-by-reference handling.** If the main agreement incorporates a DPA "available at [URL]" or "as set forth at [URL]" or similar by reference, the DPA is part of the contract but is not in front of you. Note it explicitly in the Orient table and in the review memo:

> This agreement incorporates a DPA by URL reference at `[URL]`. The DPA carries the real data terms — subprocessor rights, breach-notification timing, data-return mechanics, standard contractual clauses, audit rights. Without reading it, the data-protection analysis below is partial. Offer to route the DPA to `/privacy-legal:dpa-review` (if installed) for a separate review, or fetch and read it inline before completing Step 3's data-protection analysis.

If the user is installed with `privacy-legal`, explicitly offer:

> Want me to hand the DPA URL to `/privacy-legal:dpa-review` once you're ready? That skill is built for the DPA work and will catch subprocessor / SCC / breach-notification issues that this skill only flags at the gate.

Do not silently proceed as if the DPA were absent when it is incorporated by reference. A missing DPA and an unread DPA are different gaps — label them differently.

### Step 2: Deal-breaker check

Check the "one thing" from `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md` first. If present:

```markdown
## ⛔ DEAL-BREAKER PRESENT

**Section [X.X]** contains [the deal-breaker]. Per the team playbook, this is a
hard no. Recommend:

- [ ] Push back — propose [specific alternative language]
- [ ] Walk — if counterparty won't move, we don't sign

Detailed review below is provided for completeness but is moot unless this is
resolved.
```

### Step 3: Term-by-term comparison

For each playbook category in `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md`, find the corresponding contract section and compare.

**For each deviation, produce:**

```markdown
### [Section X.X]: [Issue name]

**Playbook says:** [our standard position, quoted from `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md`]

**Contract says:**
> "[exact quote from the contract]"

**Gap:** [Missing term | Weaker than standard | Weaker than fallback | Non-standard structure | Unacceptable]

**Legal risk:** 🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low
**Business friction:** 🔴 Blocks deals | 🟠 Slows deals | 🟡 Confuses customers | 🟢 Invisible

**Why it matters:** [one or two sentences in plain English — what goes wrong
for the business if this term stays as-is]

**Proposed redline:**
> "[the specific replacement language — ready to paste into a markup]"

**If they won't move:** [the fallback from `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md`, or "escalate to [person]"
if no fallback exists]
```

**Severity calibration:**

| Level | Means |
|---|---|
| 🔴 Critical | Don't sign without fixing. A term on the team's "never accept" list in `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md`, or a deal-breaker. |
| 🟠 High | Strongly push; escalate if they won't move. A term outside the playbook's stated fallback range. |
| 🟡 Medium | Push in first round; accept if it's the last open item. A term inside the fallback range but short of the standard position. |
| 🟢 Low | Note it, don't spend capital. A term the playbook explicitly tolerates, or a purely stylistic deviation. |

Severity is always applied *against `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md`*. If a term doesn't map cleanly to a playbook position, ask the user which bucket it belongs in and offer to record the answer in `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md`.

#### Liability cap decision procedure

**The cap amount is the least important part of the cap.** When reviewing the limitation-of-liability clause, do not produce a single "check liability cap against playbook" line item. Work through the four dimensions below and state each one explicitly in the finding:

1. **Direct vs. indirect/consequential damages.** Does the cap apply to ALL liability, or only direct damages? A 12-month cap on direct damages with uncapped consequential damages is a completely different position than a 12-month aggregate cap. State both treatments explicitly.

2. **The cap base — quote it verbatim.** "12-month cap" could mean: (a) fees paid in the 12 months preceding the claim, (b) fees payable in the current 12-month period, (c) fees over the last 12 months of usage, (d) fees under the current order form, (e) total fees ever paid. These can differ by an order of magnitude. Quote the exact language. If ambiguous, flag it: "Cap base is ambiguous — `[the quoted language]` — could mean [X] or [Y]. Confirm before signing."

3. **Cap-carveout interaction.** A [currency] 100K cap with uncapped indemnity for data breach, IP, and confidentiality is functionally uncapped for the claims that actually arise in SaaS disputes. Enumerate what sits ABOVE the cap (the carveouts), what sits BELOW (what's actually capped), and assess whether the capped surface is meaningful: "The cap covers [general contract breach]. Data breach, IP indemnity, and confidentiality are carved out and uncapped. For this vendor's risk profile, the capped surface is [meaningful / nominal]."

4. **Your playbook position per dimension.** The practice profile should have positions for: direct cap (multiple of fees), indirect damages (excluded / capped / uncapped), carveout list (what's acceptable above the cap), and cap base (which definition you'll accept). If the playbook has one "standard position" field, note: "Your playbook has a single cap position — consider splitting into direct/indirect/carveouts/base for more precise review."

#### Jurisdiction enforceability check

**The playbook applies one governing-law preference globally. Enforceability varies materially.** Before accepting a playbook position at face value, run this check for every code resolved in Step 0, labelling each finding with its code (`[ksa]`, `[gbr]`, `[usa]`) when more than one applies. The branch is chosen by the code, never by a country name in the contract.

**When the applicable code is populated and not `usa`:** apply the rows of the jurisdiction files named in the "Jurisdiction files this skill loads" block, quoting the article and carrying the row's tag verbatim on the finding. Work through the clauses in this order; the article numbers are the `ksa` rows that exist today, and for another populated code the same file names are read for the equivalent rows.

1. **Agreed compensation: liquidated damages, delay penalties, termination fees, service credits** → `civil-transactions-law.md` Arts. 178-179 (for `ksa`: valid only for non-monetary obligations; nothing is due if the debtor proves no harm; the court reduces an exaggerated sum or pro-rates for partial performance; the creditor exceeds the sum only for fraud or gross fault; any contrary agreement is void). Use the penalty-clause finding template below. A late-payment charge fixed as a percentage running with time is outside Art. 178 and is flagged under item 9.
2. **Limitation and exclusion of liability** → `civil-transactions-law.md` Art. 173 (exclusions valid for contractual liability, never for fraud or gross fault, never for tort) and Art. 180 (contract damages limited to foreseeable loss absent fraud or gross fault). A cap that does not carve out fraud and gross fault is partly void; state that in the finding and redline the carve-out in. Feed this into the liability-cap decision procedure above as a fifth dimension: "statutory carve-outs the cap cannot cover".
3. **Hardship and change in circumstances** → `civil-transactions-law.md` Art. 97 (mandatory; a no-adjustment or fixed-price clause purporting to exclude judicial rebalancing is void to that extent) and Art. 471(3) for SOW or muqawala work.
4. **Force majeure** → `civil-transactions-law.md` Arts. 110, 125, 174 (impossibility standard; automatic dissolution on total impossibility; the risk may be shifted to the debtor by clause). A missing force-majeure clause is therefore a drafting gap, not an absence of protection; say so in Step 4.
5. **Assignment and change of control** → `civil-transactions-law.md` Arts. 98 (share sale does not transfer contracts), 238-240 (rights assignable unless the contract says otherwise), 248-254 (debt transfer needs creditor consent), 255-258 (transfer of the whole contract needs consent; advance consent valid on notice; assignor stays jointly liable absent release).
6. **Limitation of claims and claims-bar clauses** → `civil-transactions-law.md` Arts. 295-306 (10 Hijri years general, 5 for periodic payments and professional fees, 1 for traders' claims against non-traders unless a written instrument exists; suspended by good-faith negotiation; cannot be shortened or lengthened by contract; must be pleaded). A "claims must be brought within 12 months" clause is flagged as void under Art. 305, `[model knowledge — verify]` on the warranty-condition alternative.
7. **Confidentiality and dispute-resolution survival** → `civil-transactions-law.md` Art. 113 (both survive termination by statute); other survival items only if the survival clause lists them.
8. **Termination mechanics** → `civil-transactions-law.md` Arts. 107-108 (judicial termination is the default; a contractual termination right works but i'thar must be expressly waived), Art. 111 (prospective for continuing contracts), Arts. 175-177 (notice by the agreed means).
9. **Interest, late-payment charges, financing terms** → `civil-transactions-law.md` Arts. 171, 178, 385 (delay damages must be proved as actual loss; pre-agreed compensation on a money debt is barred; a loan increase is void); the riba position beyond those articles is `[model knowledge — verify]` in the file, so flag every interest clause `[review]` and do not state a broader prohibition from memory.
10. **Suspension, set-off, no-set-off clauses** → `civil-transactions-law.md` Arts. 114, 191, 281-288 (no-set-off clauses are exposed under Art. 282, `[model knowledge — verify]`).
11. **Warranties and acceptance windows** → `civil-transactions-law.md` Arts. 109, 338-344 (statutory implied warranty; 180 Hijri-day defect window extendable by a longer contractual warranty drafted as an undertaking, not as a limitation period).
12. **Guarantees and parent-company support** → `civil-transactions-law.md` Arts. 578-606 (a guarantee of future debts needs a stated maximum; subsidiary unless expressed as joint and several).
13. **Adhesion terms and interpretation** → `civil-transactions-law.md` Arts. 40, 96, 104 (abusive terms in non-negotiable standard terms may be rewritten by the court and the clause cannot opt out; B2B application is an open question in the file, so tag `[model knowledge — verify]`; ambiguity is read against the obligee and the drafter of standard terms).
14. **Electronic execution and notices** → `electronic-transactions-law.md` Arts. 4(3), 5, 6-7, 10-11, 12-13, 14(1) and 14(3)-(4) (platform signatures are valid between the parties; statutory presumptions attach only to a licensed-certificate signature; a government counterparty must consent expressly, Art. 4(2)). Never state that a particular platform's signatures carry the Art. 14(3) presumptions; the file's practice-note row is `[model knowledge — verify]`.
15. **Data protection** → `personal-data-protection-law.md`: check the agreement against the Art. 8 / Regulation Art. 17(1) seven-item list (purpose, categories, duration, breach notice, foreign-law exposure, mandatory local disclosures with notice, sub-processors), Regulation Art. 17(2)-(5) (instructions, deviation notice, assessment right, sub-processor prior acceptance with an objection window), Art. 20 / Regulation Art. 24 (breach content; processor notice short enough for the controller's 72-hour filing), Art. 18 (deletion on termination), Art. 29 (transfer purpose and conditions; the Transfer Regulation row is `[model knowledge — verify]`, so never state a transfer mechanism as compliant), Art. 31 / Regulation Art. 33 (records information), Arts. 36 and 40 (exposure for caps and indemnities). Art. 2 answers a foreign vendor's "not subject to local law" position.
16. **Restrictive covenants binding an individual** → `labor-law.md` Art. 83 when the counterparty, or a person the clause restricts, is an individual worker: written, specific as to time, place and type of work, two-year cap for a non-compete, one-year limitation from discovery. A commercial non-compete between companies has no statutory cap in the files; it is `civil-transactions-law.md` Art. 169 subject to public order, `[model knowledge — verify]`.
17. **Government counterparty** → `government-tenders-procurement-law.md` when the Orient table says the counterparty is a government entity. First apply the file's matter-date rule (the 2019 law up to 2027-01-01, the 1448H law from its in-force date) and use the applicable procurement rows by matter date, citing each article as "1448H Art. N" or "2019 Art. N": the government's terms are largely non-negotiable (1448H Arts. 52, 93 / 2019 Arts. 55, 91); check delay penalties against the cap row (1448H Art. 70: 6% supply, 15% other / 2019 Art. 72: 6%, 20%), extension grounds (1448H Art. 72 / 2019 Art. 74), performance bond (1448H Arts. 59-61 / 2019 Arts. 61-63), variation limits (1448H Art. 67 / 2019 Art. 69), assignment and subcontracting consents (1448H Arts. 68-69 / 2019 Arts. 70-71), termination and bond forfeiture (1448H Arts. 74-76 / 2019 Arts. 76-78), the grievance route and its time limits (1448H Arts. 84-86 / 2019 Arts. 86-87), and forum (1448H Art. 94 / 2019 Art. 92: the competent or administrative court, arbitration only within that article). If the user is a subcontractor to a government prime contractor, check the subcontract for back-to-back terms. Anything that depends on the Regulations (payment timing, advance-payment cap, arbitration threshold) is not in the file: say so and stop that finding.
18. **Distribution, reseller and agency structures** → `commercial-agencies-law.md` Arts. 1, 3, Added Arts. 1-2, Art. 4 (registration by the local party; distributors are inside the Law; spare-parts and maintenance tail; penalties for non-registration). Termination compensation and the consequences of non-registration between the parties are `[model knowledge — verify]` or open questions in the file: flag, do not assert.
19. **Governing law and forum** → `arbitration-law.md` (form of the agreement, Law Art. 9; government-entity approval, Art. 10; arbitrability, Art. 2; seat and language, Arts. 28-29; tribunal qualifications, Art. 14; interim measures, Arts. 22-23; award time limit, Art. 40; annulment window, Art. 51; SCCA rows only when the clause names the SCCA), `commercial-courts-law.md` (jurisdiction and threshold, Arts. 6, 9-12, 16; pre-filing notice, Art. 19; limitation, Art. 24; language of proceedings and multi-tier clauses, Arts. 13, 38, 74 and draft Regs Art. 101, `[authority — MoJ]` draft), and `enforcement-law.md` (enforceable instruments, Art. 7; foreign judgments and awards, Arts. 7(1)(g), 9 — reciprocity and public order; the effective-date gate in that file must be stated on every citation, and an enforcement step dated before the gate stops and routes to counsel). A foreign governing-law clause with local performance: the file has no conflict-of-laws chapter, so the enforceability of the choice is `[no rule in <code> files — verify]`; state the profile's own position from `playbook-defaults.md` (`[model knowledge — verify]`) and flag `[review]`.

For each item, if the clause exists and the file has the row: cite it. If the clause exists and the file is silent: tag the finding `[no rule in <code> files — verify]` and do not supply the rule from memory. If the row is tagged `[model knowledge — verify]`, carry the tag onto the finding and mark it for local counsel. If the portal must be fetched to quote or check currency of an article and the fetch fails, apply the "no silent supplement" stop in Step 6 and do not continue that finding from memory.

**Penalty-clause finding template** (agreed compensation of any kind: delay LDs, termination fees, service credits, minimum-commitment shortfall charges). Use it in place of the generic deviation block for item 1:

```markdown
### [Section X.X]: Agreed compensation — [delay penalty / termination fee / service credit / shortfall charge]

**Playbook says:** [position from the profile, e.g. "Accept a fixed compensation clause only with the statutory reduction in view"]

**Contract says:**
> "[exact quote, including any 'payable whether or not loss is suffered' or 'not subject to reduction' wording]"

**Enforceability [<code>]:** [quote the reduction rule from `civil-transactions-law.md`; for `ksa` Art. 179: not due if the debtor proves no harm; reducible on the debtor's application if exaggerated or the obligation was partly performed; increasable only for the creditor's proof of fraud or gross fault; any contrary agreement void. Art. 178: not available where the obligation is to pay money.] `[settled — last confirmed <date>] [BOE — Arabic]`
**Exposure as written:** [currency] [amount] [computed — civil-transactions-law.md Arts. 178-179, settled <date>; inputs: <rate or formula in the clause>, <base>, <period>, <cap if any>]
**Exposure after the statutory rule:** [the same number is the ceiling absent fraud or gross fault; state that it is reducible and that "payable regardless of loss" and "not subject to adjustment" language is void; where a partial-performance pro-rating is arguable, show the recomputed figure the same way: [currency] [amount] [computed — civil-transactions-law.md Art. 179, settled <date>; inputs: <performed share>, <original sum>]]

**Gap:** [Missing term | Weaker than standard | Non-standard structure | Unacceptable]
**Legal risk:** 🔴 | 🟠 | 🟡 | 🟢 **Business friction:** 🔴 | 🟠 | 🟡 | 🟢

**Why it matters:** [plain English — the clause does not do what the counterparty thinks it does, or it caps our own recovery]

**Proposed redline:**
> "[surgical language that states the sum as a genuine pre-estimate reducible in accordance with law, removes 'regardless of loss' and 'sole remedy' language where we are the creditor, or adds it where we are the debtor and the file supports it (Art. 179 cap effect)]"

Never propose "payable regardless of loss" or "not subject to court adjustment" language: it is void under the reduction rule and the finding must say so.
```

**When the applicable code is `usa`:** there is no jurisdiction folder. Check the contract's actual governing law against the upstream divergences below before accepting playbook positions at face value, using the upstream research connectors, and label the findings `[usa]`:

- **Non-solicits/non-competes:** Unenforceable in CA (Bus. & Prof. Code §16600). Restricted in many EU jurisdictions. Enforceable with limitations elsewhere. `[jurisdiction — verify]`
- **Auto-renewal:** CA GBL §17600-17606, NY GBL §527-a, IL 815 ILCS 601 have specific consumer/B2B notice requirements. Other states vary. `[jurisdiction — verify]`
- **Liability exclusions:** EU and UK unfair contract terms rules (UCTA 1977, Consumer Rights Act 2015) constrain consumer exclusions. Some US states limit exclusion of gross negligence or willful misconduct. `[jurisdiction — verify]`
- **Indemnification:** Some states void indemnification for the indemnitee's own negligence. `[jurisdiction — verify]`
- **Confidentiality term:** Some jurisdictions limit "perpetual" confidentiality to a reasonable period. `[jurisdiction — verify]`

When the playbook position conflicts with the contract's governing-law enforceability under either branch, flag: "Your playbook prefers [X], but this contract is governed by [Y] law where [X] is [unenforceable / restricted / reducible by the court / subject to statutory override] — [file and article, or `[jurisdiction — verify]` on the `usa` branch]." Where two codes apply and their rules conflict, state both and flag `[review]` for the lawyer to decide which governs.

### Step 4: Favorable terms and gaps

Two short lists:

**Better than our standard:** Terms where the vendor gave us more than we'd ask for. Note these — they're trade bait if you need to give something up elsewhere.

**Missing entirely:** Standard provisions that just aren't there. Most common: assignment restrictions, audit rights (if we want them), force majeure, insurance requirements. For a populated non-`usa` code, say what the jurisdiction file supplies by default when a clause is missing, citing the row (for `ksa`: force majeure and impossibility, `civil-transactions-law.md` Arts. 110, 174; good-faith performance and implied terms, Art. 95; contract assignment needs consent even without an anti-assignment clause, Art. 255; confidentiality survival, Art. 113), so "missing" is weighed as "statutory default applies" rather than "no protection". Where the file has no row for the missing provision, tag `[no rule in <code> files — verify]`.

### Step 5: Escalation routing

Check the escalation matrix in `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md` against:
- Contract value, in the profile currency (`## Jurisdiction` → Currency for thresholds); state the conversion if the contract is priced in another currency
- Presence of any 🔴 critical issues
- Any automatic-escalation triggers (unlimited liability, IP assignment, etc.)
- For a populated non-`usa` code, the jurisdiction-specific triggers the files name for `escalation-flagger` (for `ksa`: a government contract with delay penalties above the `government-tenders-procurement-law.md` delay-penalty cap in the applicable procurement rows by matter date (1448H Art. 70 / 2019 Art. 72) or a foreign-seated arbitration clause (1448H Art. 94 / 2019 Art. 92); an interest clause, `civil-transactions-law.md` Arts. 178, 385; a mandatory-rule conflict under Arts. 96, 97, 173, 179, 305; an unregistered agency or distribution structure, `commercial-agencies-law.md`)

State clearly who needs to approve this:

```markdown
## Approval routing

Based on [contract value in [currency] / issue severity], this agreement requires:

- [ ] **[Name/role]** approval — [reason]
- [ ] **Business owner sign-off** on [specific commercial term they should weigh in on]

**Recommended next step:** [Send redlines to counterparty | Escalate to GC before
responding | Get business input on commercial term X before legal responds]
```

**Before proceeding to send redlines to the counterparty:** Read `## Who's using this` in `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md`. If the Role is Non-lawyer:

> Sending redlines is a legal act — the counterparty will treat every edit as our negotiating position. Have you reviewed this with an attorney? If yes, proceed. If no, here's a brief to bring to them:
>
> [Generate a 1-page summary: counterparty, agreement type, the specific redlines proposed, the playbook positions behind each, the fallbacks, and what to ask the attorney before the package leaves.]
>
> If you need to find an attorney, solicitor, barrister, or other authorised legal professional: contact your professional regulator (state bar in the US, SRA/Bar Standards Board in England & Wales, Law Society in Scotland/NI/Ireland/Canada/Australia, or your jurisdiction's equivalent) for a referral service.

Do not proceed past this gate without an explicit yes.

## Redline granularity

**Edit at the smallest possible granularity.** A redline is a negotiation artifact, not a rewrite. Wholesale clause replacement signals "we threw out your drafting" — it's aggressive, it forces the counterparty to re-read the whole clause, and it discards the parts of their drafting that were fine. Surgical redlines — strike a word, insert a phrase, restructure a subclause — signal "we have specific asks" and are faster to read, understand, and accept.

Default to the smallest edit that achieves the playbook position:
- Replace a **word** before a phrase. ("twelve (12)" → "twenty-four (24)")
- Replace a **phrase** before a sentence. ("paid by the Buyer" → "paid and payable by the Buyer")
- Restructure a **subclause** before replacing the sentence. (Add "(a)" and "(b)" to split a compound condition.)
- Replace a **sentence** before replacing the clause.
- Only replace a **whole clause** when the counterparty's version is so far from your position that surgical edits would be harder to read than a fresh draft — and when you do, say so in the transmittal: "We've replaced §8.2 rather than marking it up because the changes were extensive. Happy to walk you through the delta."

When in doubt, smaller. A client who receives a surgical redline trusts that you read carefully. A client who receives a wholesale replacement wonders whether you read at all.

### Step 6: Assemble the memo

Prepend the work-product header from `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md` `## Outputs` (it differs by user role — see `## Who's using this`). Directly under it, for every code applied other than `usa`, add the jurisdiction disclaimer line from the profile `## Jurisdiction` (the manifest's `disclaimer`, in English and in the authoritative language); it is part of the header and is never stripped, including from counterparty-facing redlines.

**Bilingual rule.** Apply the bilingual house-style rule from the profile `## Outputs`: when the profile's output language is bilingual, or the memo carries counterparty-facing text (proposed redlines, transmittal wording, the redline package) in a jurisdiction whose authoritative language is not English, add the authoritative-language rendering of (1) the bottom line, (2) the findings table (issue counts and the per-issue one-liners), and (3) every counterparty-facing passage, using the spellings in the manifest's `output_language_rule`. Do not translate the analysis paragraphs unless the profile says authoritative-language only.

This memo and the underlying agreement may be privileged, confidential, or both. The output inherits that status from the source. Distribute only within the privilege circle; mark and store it where privileged materials live; strip the work-product header before any external delivery (e.g., counterparty redlines, stakeholder summaries).

The playbook positions applied below reflect the jurisdiction recorded in `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md` → `## Jurisdiction` and `Governing law and venue`, and the jurisdiction files loaded in Step 0. Name them in the reviewer note: `Jurisdiction: <codes applied>; files: <list>; portal fetched: yes/no; unpopulated codes: <list or none>`. If the contract's governing-law, forum or performance clause points to a code other than the profile's primary code, the memo says so in the bottom line, labels every finding with its code, runs the enforceability check for each populated code side by side, and flags `[review]` where the codes conflict; an unpopulated code is the Step 0 hard stop, never a caveat.

**Research step (quoting an article or checking its currency).** For a populated non-`usa` code, fetch the instrument from the portal named in the manifest: `python3 scripts/fetch-law.py --portal boe --id <guid> --lang ar` (GUIDs in `references/jurisdictions/<code>/SOURCES.md`; the built-in web-fetch tool rejects the portal's TLS chain, use the script or `curl`), quote the article, tag `[BOE — Arabic]` or `[BOE — official English]`, and check the status line and the amendment block for changes since the file's `[settled — last confirmed …]` date. For `usa`, use the upstream research connectors (Westlaw, CourtListener). Record the probe result in the reviewer note Sources line (`portal: <host> ✓ reachable | unreachable`, or the connector name).

> **No silent supplement.** If the portal fetch fails, the article is not found, or a research query to the configured legal research tool returns few or no results for a rule the memo needs (enforceability of a limitation clause, indemnity scope, governing-law choice), report what was found and stop. Do NOT fill the gap from web search or model knowledge without asking. Say: "The search returned [N] results from [tool / portal]. Coverage appears thin for [rule / jurisdiction]. Options: (1) broaden the search query, (2) try a different research tool, (3) search the web — results will be tagged `[web search — verify]` and should be checked against a primary source before relying, or (4) flag as unverified and stop. Which would you like?" A lawyer decides whether to accept lower-confidence sources. A rule the jurisdiction file does not carry at all is reported as `[no rule in <code> files — verify]` and is never supplied from memory. When the portal fetch fails for a rule the jurisdiction file does carry, the options also include citing the file row under its own `[settled — last confirmed …]` tag with a note that the portal was not re-checked this session (Step 0 item 3 permits it); the stopped run still emits the reviewer note with `portal fetched: no`, lists the findings that depend on the quote as PENDING, and tags nothing `[BOE — Arabic]`.
>
> **Source attribution.** Where the memo cites a statute, regulation, or case, tag the citation: `[BOE — Arabic]` / `[BOE — official English]` / `[authority — <name>]` for text fetched from the portal or issuing authority named in the manifest; `[Westlaw]`, `[statute / regulator site]`, or the MCP tool name for citations retrieved from a legal research connector; `[settled — last confirmed YYYY-MM-DD]` carried verbatim from a jurisdiction-file row; `[web search — verify]` for web-search citations; `[model knowledge — verify]` for citations recalled from training data; `[user provided]` for citations from the counterparty draft or house files. Citations tagged `verify` carry higher fabrication risk and should be checked first. Never strip or collapse the tags.

```markdown
[WORK-PRODUCT HEADER — per plugin config ## Outputs]
[JURISDICTION DISCLAIMER LINE — from the profile ## Jurisdiction, for every code other than `usa`]

# Vendor Agreement Review: [Counterparty] [Agreement Type]

**Reviewed:** [date — Gregorian; do not convert to Hijri (no converter in the toolset); copy a Hijri date only when the document itself carries one, tagged `[user provided]`]
**Jurisdiction:** [codes applied, e.g. `ksa`; files loaded]
**Contract value:** [currency] [amount] / [term]
**Our role:** Customer

---

## Bottom line

[Two sentences. Can we sign this? What has to change first?]

**Issues (legal risk):** [N]🔴 [N]🟠 [N]🟡 [N]🟢
**Issues (business friction):** [N]🔴 [N]🟠 [N]🟡 [N]🟢

**Approval needed from:** [name]

---

## Deal-breaker check

[✅ Clear | ⛔ Present — see above]

---

## Issues by severity

[All the deviation blocks from Step 3, grouped Critical → Low]

---

## Favorable terms

[list]

## Missing provisions

[list]

---

## Approval routing

[from Step 5]

---

## Redline package

[If requested: consolidated markup-ready language for all proposed changes]
```

## Integration: [CLM]

If a [CLM] MCP is connected, after the review:

- Check if this counterparty already has agreements with us (may inform negotiating posture — "we already gave them 24-month cap on the last deal")
- Pull the workflow template that matches this agreement type
- Offer to create the [CLM] record with the review memo attached and approvers pre-routed

## Integration: DocuSign

If DocuSign MCP is connected and the agreement is ready to sign (all greens or all issues accepted), offer to:
- Generate the envelope
- Route to signers in the right order per the escalation matrix

Do **not** send anything for signature without explicit instruction. "Ready to sign" is the lawyer's call, not yours.

**Before generating a signature envelope or routing for countersignature:** Read `## Who's using this` in `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md`. If the Role is Non-lawyer:

> This step has legal consequences (signing binds the company to the whole agreement). Have you reviewed this with an attorney? If yes, proceed. If no, here's a brief to bring to them:
>
> [Generate a 1-page summary: counterparty, contract value, the issues found and how they resolved, any risk the lawyer accepted, and what to ask the attorney before envelope goes out.]
>
> If you need to find an attorney, solicitor, barrister, or other authorised legal professional: contact your professional regulator (state bar in the US, SRA/Bar Standards Board in England & Wales, Law Society in Scotland/NI/Ireland/Canada/Australia, or your jurisdiction's equivalent) for a referral service.

Do not proceed past this gate without an explicit yes.

## Output formats

**Full memo (default):** As above. Goes in the [CLM] record or the Drive folder from `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md` house-style section.

**Slack-sized summary:** Two lines and a link. For when someone asks "is this okay?" in a channel.

```
[Counterparty] [type] — NEEDS WORK. 1🔴 (uncapped liability §8.2), 2🟠. Full review: [link]. Needs [GC] approval.
```

**Redline doc:** If the user asks for it, output a .docx with tracked changes. Use the docx skill. Comments on each change cite the playbook position.

## Quality checks before delivering

- [ ] `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/commercial-legal/CLAUDE.md` was loaded and quoted — not generic market positions
- [ ] Deal-breaker checked first
- [ ] Every issue has specific replacement language
- [ ] Risk levels are calibrated (not everything is Critical)
- [ ] Approver is named, not "escalate to legal"
- [ ] Counterparty context considered (BigCo vs. startup — affects what's worth fighting over)
- [ ] Step 0 record line is in the reviewer note; every finding under a non-`usa` code cites a file and article and carries the row's tag; no rule was supplied from memory where the file is silent
- [ ] Every computed exposure number carries its `[computed — …; inputs: …]` tag
- [ ] Disclaimer line under the header and the bilingual rendering present where the profile asks for it; values in `[currency]`, not a symbol the profile does not carry

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs`. Customize the options to what this skill just produced — the five default branches (draft the X, escalate, get more facts, watch and wait, something else) are a starting point, not a lock-in. The tree is the output; the lawyer picks.

