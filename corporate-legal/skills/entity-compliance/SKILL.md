---
name: entity-compliance
description: >
  Entity compliance tracker — initialize, report upcoming deadlines, update
  status, run health audit, export to CSV. Maintains a compliance-tracker.yaml
  built from the entity table, calculates filing deadlines by entity and
  jurisdiction, and surfaces what's due in the next 30/60/90 days. Use when
  user says "entity compliance", "filing deadlines", "annual filings due",
  "annual confirmation", "what filings are due", "entity health", or "good standing".
argument-hint: "[--init | --report [--days N] | --update [--from-report] | --sweep | --audit | --export [--format csv|table]]"
---

# /entity-compliance

0. Run Step 0 (resolve the applicable jurisdiction) below before any mode; every entity carries its own `jurisdiction_code`, so a tracker can span several codes.
1. Load `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/CLAUDE.md` → `## Jurisdiction` and `## Entity Management` (entity table with local type, jurisdiction code and registry number; filing agent).
2. Route to the correct mode below based on flag:
   - No flag or `--init`: Mode 1 — initialize tracker from entity table
   - `--report`: Mode 2 — surface upcoming deadlines and overdue items
   - `--update`: Mode 3a (manual) or 3b (--from-report upload) — update status
   - `--sweep`: Mode 3c — walk through unknown/overdue items one by one
   - `--audit`: Mode 4 — full health audit
   - `--export`: Mode 5 — produce CSV or table export
3. Read/write `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/entities/compliance-tracker.yaml`.
4. After any update: show summary of changes and next action.

---

## Purpose

Annual confirmations, annual assemblies, financial-statement deposits, tax and
social-insurance filings, licence renewals — every entity in every jurisdiction
has its own schedule and its own consequences for missing the deadline. The
filing vocabulary is the jurisdiction's own: for a populated non-`usa` code it
comes from `references/jurisdictions/<code>/filing-calendar.md` (for `ksa`:
commercial-register annual confirmation, annual assembly, financial statements,
zakat/tax and VAT returns, GOSI, Qiwa work permits and Nitaqat, chamber
membership, municipal licence, MISA annual update, UBO annual confirmation);
for `usa` it is annual reports, franchise taxes, Statements of Information and
biennial filings. This skill maintains a single YAML tracker that knows
what's due, when, and for which entity. It's lightweight by design: the tracker
is a file you own, Claude updates it on command, and you export it when you need
to share it.

## Important: deadline reference caveat

> The filing deadlines this skill computes reflect the jurisdiction file's rows as
> of the date in each row's `[settled — last confirmed YYYY-MM-DD]` tag, or the
> user's own confirmation. Filing requirements and due dates change. **Always
> confirm deadlines with your filing agent or directly with the issuing authority
> named in the jurisdiction file's Authority column before relying on them for
> compliance purposes** (for `ksa`: the Ministry of Commerce, ZATCA, GOSI,
> HRSD/Qiwa, MISA, the chamber of commerce, the municipality; for `usa`: the
> relevant Secretary of State). If you use a filing agent — a registered-agent
> service, a corporate-services provider, or a government-relations officer —
> their compliance calendar is authoritative for your specific entities; use this
> tracker to organize and surface their data, not to replace it. Rows the
> jurisdiction file tags `[model knowledge — verify]` never drive an alert until
> the user's accountant or filing agent has confirmed them (they sit at
> `status: unconfirmed`).

## Jurisdiction assumption

> This tracker computes deadlines against the `jurisdiction_code` of formation / registration recorded per entity (Step 0 resolves the profile's codes; each entity may carry a different one). Filing rules, due-date mechanics, and fee structures vary materially by jurisdiction. For a populated non-`usa` code the rules come only from `references/jurisdictions/<code>/`; for `usa` they come from the upstream path below; an unpopulated code is a hard stop for that entity (Step 0, item 3). If an entity's actual footprint differs from what's in `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/CLAUDE.md` (undisclosed registration in another jurisdiction, dissolved entities, re-domestication, filings managed by a local agent), the output may not apply as written — confirm with the filing agent or local counsel for that jurisdiction.

## Entity-type disambiguation

> The filing calendar depends on **entity type**, not just jurisdiction. Treating a "[jurisdiction] entity" as a single bucket is a common and consequential error — different legal forms in the same jurisdiction have different filings, different deadlines, and different consequences for a miss. Confirm the entity type (`entity_type_local`) from the entity table before computing or reporting a deadline, and never copy a deadline from one entity type to another in the same jurisdiction. This is the design rule for every reference table this skill reads: **it must be indexed by entity type, not just by jurisdiction.** An entity without a local type is `type_unknown` and gets no computed deadline until the user confirms the type.
>
> **When the applicable code is a populated non-`usa` code:** `references/jurisdictions/<code>/filing-calendar.md` is indexed by entity type first (for `ksa`: all / LLC / JSC / JSC (listed) / simplified JSC / branch of foreign company / professional company) and then by authority. Pull only the rows whose Entity type column names this entity's `entity_type_local` or says "all". The file's own warning applies verbatim: a skill must never apply an LLC, JSC or simplified-JSC row to a different entity type, or a company row to a branch, on the basis that "the rule is probably the same". If the file has no rows for the entity's type, say so, tag the entity `[no rule in <code> files — verify]`, and set its filings to `unknown` — do not borrow another type's rows.
>
> **When the applicable code is `usa`:** the same discipline, with the Delaware split as the canonical example.
>
> **Delaware — the split that matters:**
>
> - **DE Corporation (Inc., Corp.):** Annual report AND franchise tax, both due **March 1**. Franchise tax is calculated by the authorized-shares method or the assumed-par-value capital method (whichever is lower); the annual report captures director / officer information. Statutory basis: 8 Del. C. §§ 501–502 [verify current].
> - **DE LLC:** No annual report required. Annual tax is a **flat $300**, due **June 1**. Statutory basis: 6 Del. C. § 18-1107(d) [verify current fee and date].
> - **DE LP:** No annual report required. Annual tax is a **flat $300**, due **June 1** (parallel to the LLC rule). Statutory basis: 6 Del. C. § 17-1109 [verify current].
>
> A DE LLC is NOT required to file a March 1 annual report — writing that deadline for an LLC carries real risk (spurious "overdue" flags that mask actual June 1 exposure, or worse, the inverse: a user who treats the March 1 corporation rule as universal and misses the June 1 LLC deadline). If the entity table records a Delaware entity without a type, flag it as `type_unknown` and ask the user to confirm before computing either deadline.
>
> The same entity-type discipline applies in every other `usa` state with divergent filing regimes by entity type (e.g., CA corp Statement of Information vs. CA LLC SOI cadence; TX franchise tax applies to corporations, LLCs, and LPs but with different no-tax-due thresholds). When the reference table for a jurisdiction is populated, make sure it is indexed by entity type, not just by jurisdiction.

---

## Tracker file

Lives at `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/entities/compliance-tracker.yaml`. Structure:

```yaml
# Entity Compliance Tracker
# Generated: [date]
# Last updated: [date]
# Disclaimer: deadlines are reference only — confirm with the filing agent or the issuing authority named in the jurisdiction file
# Currency: [profile currency, from ## Jurisdiction]; dates computed against the calendar in references/jurisdictions/<code>/MANIFEST.md

metadata:
  company: "[Company Name]"
  generated: "[date]"
  last_updated: "[date]"
  last_audit: "[date or null]"
  primary_jurisdiction: "[code from ## Jurisdiction]"

custom_jurisdictions:   # manually added — `usa` states, or user-supplied rows for a populated code that its file lacks (tagged [user provided])
  []                    # populated when a new jurisdiction is encountered

entities:
  - name: "[Entity Name]"
    entity_type_local: "[type under the jurisdiction's companies law — for a non-usa code, one of the Entity type values in its filing-calendar.md (for ksa: LLC / JSC / simplified JSC / branch of foreign company / professional company); for usa: Corporation / LLC / LP / other]"
    type: "[alias of entity_type_local, kept so trackers written under the old schema still parse]"
    jurisdiction_code: "[ISO 3166-1 alpha-3 lowercase; add the sub-jurisdiction after a slash where the code needs it — e.g. usa/DE, ksa]"
    registry_number: "[commercial-registration / registry number, or null]"
    formation_date: "[date or null]"
    status: "[active / dormant / dissolving]"
    filing_agent: "[in-house / law firm or government-relations officer / corporate-services provider / registered-agent service name]"
    registered_agent: "[alias of filing_agent — read for usa entities in trackers written under the old schema; write filing_agent going forward]"
    notes: ""

    jurisdictions:
      - jurisdiction_code: "[code, with sub-jurisdiction where the code needs it]"
        qualification: "[usa: domestic / foreign; non-usa: the registration type from the jurisdiction file — e.g. for ksa: main CR / branch CR / MISA registration]"
        qualified_date: "[date or null]"
        agent_managed: false   # set true where a local agent handles compliance; the tracker still computes from the jurisdiction file
        local_agent: "[name or null]"
        filings:
          - type: "[non-usa: the row name from filing-calendar.md, e.g. for ksa: CR annual confirmation / annual assembly / financial statements deposit / zakat-tax return / VAT return / GOSI contributions / work-permit renewal / chamber membership / municipal licence / MISA annual update / UBO annual confirmation; usa: Annual Report / Franchise Tax / Statement of Information / Biennial Statement / other]"
            authority: "[from the file's Authority column — for ksa: Ministry of Commerce / ZATCA / GOSI / HRSD-Qiwa / Chamber / municipality / MISA / MoC (UBO); for usa: Secretary of State / Franchise Tax Board / other]"
            source_tag: "[the provenance tag of the file row this filing came from — [settled — last confirmed YYYY-MM-DD] / [authority — <name>] / [model knowledge — verify] / [user provided]]"
            due_date: "[YYYY-MM-DD]"
            due_basis: "[fixed date / anniversary month / fiscal year end + N days / registration anniversary / other — with the article, e.g. FYE + 6 months (companies-law.md Art. 88)]"
            confirmed_by: "[accountant or filing agent name and date, or null — required before a model-knowledge row drives an alert]"
            last_filed: "[date or null]"
            last_fee: "[amount in the profile currency, or null]"
            status: "[current / due_soon / overdue / unknown / unconfirmed]"
            confirmed_good_standing: "[date or null — the jurisdiction's own status evidence: usa good-standing certificate; ksa CR active-status extract]"
            notes: ""
```

Status values:
- `current` — filed for current period, nothing due within 90 days
- `due_soon` — due within 90 days
- `overdue` — past due date with no filed date recorded
- `unknown` — no information; needs manual confirmation
- `unconfirmed` — the filing came from a jurisdiction-file row tagged `[model knowledge — verify]` and the user's accountant or filing agent has not yet confirmed it; it is listed but never raises an overdue or due-soon alert

---

### Step 0: Resolve the applicable jurisdiction

1. **Read the practice profile's `## Jurisdiction` section.** It gives the primary jurisdiction code, the footprint list (other codes the practice operates in), the output-language preference, and whether local counsel is available for escalation. Codes are ISO 3166-1 alpha-3 lowercase (`ksa`, `gbr`, `fra`, `che`, `usa`). If the section is missing or still a placeholder, stop: "The practice profile has no jurisdiction. Run the cold-start interview; nothing in this skill can run against the wrong jurisdiction."
2. **Determine the matter's jurisdiction(s).** Start from the primary code. Then read the matter facts: governing-law clause, seat of arbitration, place of employment, jurisdiction of incorporation, place of performance. If the facts point to a code not in the profile, add it for this matter and say so in the reviewer note. A matter may have more than one code (a contract governed by English law with a Saudi counterparty and Saudi performance is `gbr` + `ksa`).
3. **Load the jurisdiction folder for each code.** The folder is `references/jurisdictions/<code>/` in this plugin (the same tree ships at the repo root and in every runtime adapter). Read `MANIFEST.md` first.
   - If `populated` is not `yes`: **stop for that code.** Say: "Jurisdiction `<code>` (<name>) is registered but not populated: no reference files exist for it. I will not apply another jurisdiction's rules or model knowledge in its place. Options: (1) populate `references/jurisdictions/<code>/` (see README, 'How to add a jurisdiction'), (2) route this matter to local counsel, (3) tell me to proceed with the analysis limited to the populated jurisdictions in this matter, with every finding for `<code>` marked `[not populated — no rule applied]`." Wait for the answer. Never fall back silently.
   - If the code is `usa`: there is no folder. Follow this skill's US path (the upstream doctrine and the upstream research connectors, CourtListener or Westlaw, with the upstream "no silent supplement" rule). Label findings `[usa]`.
   - If `populated` is `yes`: read `INDEX.md`, then the instrument files this skill names in its "Jurisdiction files" list. A row tagged `[settled — last confirmed YYYY-MM-DD]` may be applied and cited by article. A row tagged `[model knowledge — verify]` may be applied only with that tag carried onto the finding. If a rule this skill needs is not in the files at all, do not supply it from memory: say what is missing, tag the gap `[no rule in <code> files — verify]`, and continue only with the rules that exist.
4. **Multi-jurisdiction matters.** Run the relevant files side by side. Label every finding with its code in square brackets, `[ksa]`, `[gbr]`, `[usa]`, and never merge two jurisdictions' rules into one sentence. Where the codes conflict (a clause valid under one law and reducible under another), state both and flag `[review]` for the lawyer to decide which governs.
5. **Research step (when a rule must be quoted or its currency checked).** Use the portal named in `MANIFEST.md` → `research_tool`. For `ksa`: `python3 scripts/fetch-law.py --portal boe --id <guid> --lang ar` (GUIDs in `SOURCES.md`), or `curl -sS https://laws.boe.gov.sa/BoeLaws/Laws/LawDetails/<guid>/1`; the built-in web-fetch tool rejects the portal's TLS chain. Quote the article, tag `[BOE — Arabic]` (or `[BOE — official English]` when quoting the translation), and check the status line and the "تعديلات المادة" block for amendments. If the fetch fails or the article is not found, apply the "no silent supplement" rule: report the failure and stop, or continue with the rule tagged `[model knowledge — verify]` only if the user says so.
6. **Calendar and language.** Take the weekend, public-holiday, calendar (Hijri or Gregorian) and currency rules from `MANIFEST.md`. Compute every date and roll-back against that calendar, never against a Saturday/Sunday weekend or US federal holidays. Produce the deliverable in English; when the profile's output-language preference is bilingual, or the manifest's authoritative language is not English and counterparty-facing text is produced, add the authoritative-language rendering of the bottom line, the findings table, and any counterparty-facing text, using the spellings in the manifest's `output_language_rule`.
7. **Header and disclaimer.** Prepend the manifest's `disclaimer` line under the work-product header for every deliverable that applies a non-`usa` jurisdiction. For `ksa`: "Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance." with its Arabic rendering from the manifest.
8. **Record in the reviewer note.** `Jurisdiction: <codes applied>; files: <list>; portal fetched: yes/no; unpopulated codes: <list or none>.`

**Jurisdiction files this skill loads:**

- `references/jurisdictions/<code>/MANIFEST.md` — calendar, currency, disclaimer, research tool (Step 0; every mode).
- `references/jurisdictions/<code>/filing-calendar.md` — the filing list indexed by entity type then authority (Mode 1 Step 2 and Step 2.5; Mode 2; Mode 4). For `ksa`: the Ministry of Commerce rows (Commercial Register Law Arts. 5, 10, 11, 15; Companies Law Arts. 16, 17, 18-19, 88, 121-122, 165-168, 145-147, 236-238, 197-199, 274(3)), the ZATCA, GOSI, HRSD/Qiwa, Chamber, municipality, MISA, National Address and UBO rows, and the Art. 262 sanctions row.
- `references/jurisdictions/<code>/commercial-register-law.md` — registration status and update duties (Mode 1 Step 2; Mode 3 gate; Mode 4). For `ksa`: Arts. 3/5, 6, 10, 11, 15, 17, 21 and the Royal Decree item Third (branch-CR deadline).
- `references/jurisdictions/<code>/companies-law.md` — annual-assembly, financial-statement, auditor and register deadlines by entity type (Mode 1 Step 2.5). For `ksa`: Arts. 16-20, 88, 93, 112, 121-122, 147, 148, 165, 167, 238, 262-267.
- `references/jurisdictions/<code>/corporate-governance-regulations.md` — the listed-company calendar (Mode 1 Step 2, listed entities only). For `ksa`: CGR Arts. 13(b), 30(b), 54, 19(b), 62(7), 93; LJSC Art. 3.
- `references/jurisdictions/<code>/ultimate-beneficial-ownership-rules.md` — annual confirmation and 15-day change notification (Mode 1 Step 2; Mode 4). For `ksa`: the annual-confirmation, change-notification and Art. 262 penalty rows.
- `references/jurisdictions/<code>/investment-law.md` — foreign-investment registration validity and annual update (Mode 1 Step 2; Mode 4). For `ksa`: Art. 7(2), Reg. Art. 13, Art. 8(3).
- `references/jurisdictions/<code>/social-insurance-law.md`, `platform-obligations.md`, `saudization-nitaqat.md` — social-insurance and labour-platform standing (Mode 1 Step 2; Mode 4). For `ksa`: Social Insurance Law Arts. 7, 8(4), 9, 10, 58; Labor Law Arts. 15-16, 33, 51 with Regulation Art. 18; Nitaqat band export and Regulation Art. 8.
- `references/jurisdictions/<code>/anti-concealment-law.md` — standing rule on the entity's own bank accounts (Mode 4). For `ksa`: Arts. 4(c), 17.
- `references/jurisdictions/<code>/electronic-transactions-law.md` — note only, for electronically filed confirmations (Mode 3).

---

## Mode 1: Initialise

Run when no tracker exists, or with `--rebuild` to regenerate from scratch.

### Step 1: Load entity table

Read `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/CLAUDE.md` → `## Entity Management` → Entity table. If the entity table
is populated (from org chart upload at cold-start), use it directly. If not,
ask the user to either run the cold-start module or provide the entity list.

### Step 2: For each entity × jurisdiction, confirm the filing requirements

Resolve each entity's `jurisdiction_code` and `entity_type_local` first (Step 0; the entity table). Then branch:

#### When the applicable code is a populated non-`usa` code

The filing list comes from `references/jurisdictions/<code>/filing-calendar.md`, indexed by entity type and then by authority (for `ksa`: Ministry of Commerce, ZATCA, GOSI, Qiwa, Chamber, municipality, MISA, UBO). Do not ask the user to type a filing list the file already holds; ask only for the inputs the rows need.

1. Read `MANIFEST.md`; if `populated` is not `yes`, stop for this entity per Step 0 and record it as `[not populated — no rule applied]`. Never substitute another code's rows.
2. Read the entity's rows: every row whose Entity type column names `entity_type_local` or says "all" (and, for a listed entity, the rows of `corporate-governance-regulations.md` — for `ksa`: CGR Arts. 13(b), 30(b), 54). If `entity_type_local` is empty, mark the entity `type_unknown`, ask the user, and compute nothing.
3. For each row create one filing. Carry the row's provenance tag into `source_tag` verbatim and the Authority column into `authority`. A row tagged `[settled — last confirmed YYYY-MM-DD]` or `[authority — <name>]` may be computed and reported with that tag. A row tagged `[model knowledge — verify]` (for `ksa`: every ZATCA, GOSI, Qiwa/HRSD, chamber, municipality, National Address, UBO-Rules and CMA row) is written with `status: unconfirmed` and `confirmed_by: null`; it appears in the report under UNCONFIRMED and never raises an alert until the user's accountant or filing agent confirms it, at which point `confirmed_by` is filled and the status is recomputed. Do not promote the tag.
4. Ask the user for the inputs the rows need and nothing else: fiscal year end, commercial-registration date and number, MISA registration date (the MISA due date is investor-specific and is taken from the certificate, never computed from the fiscal year — `investment-law.md` Reg. Art. 13 row), whether the entity is VAT-registered and its turnover band, headcount, whether there is any non-Saudi shareholder (MISA and UBO rows), whether the entity is listed.
5. If a filing the entity plainly needs has no row in the file (for `ksa`: a sector-regulator licence renewal; the annual-confirmation due date under the Commercial Register Regulations), say so, write it as a filing with `source_tag: "[no rule in <code> files — verify]"` and `status: unknown`, and ask the user to obtain the date from the authority or counsel. Do not infer it.
6. Where the row text must be quoted or its currency checked, use the research step: `python3 scripts/fetch-law.py --portal boe --id <guid> --lang ar` (GUIDs in `references/jurisdictions/<code>/SOURCES.md`; the built-in web-fetch tool rejects the portal's TLS chain, use the script or `curl`), quote the article, tag `[BOE — Arabic]` or `[BOE — official English]`. If the fetch fails, apply the "no silent supplement" rule: report the failure and stop, or continue on the file's row with its existing tag only if the user says so.

Then go to Step 2.5 to compute the dates.

#### When the applicable code is `usa`

For each entity, confirm the current filing schedule with the registered agent or the relevant Secretary of State. State filing schedules change (some states move from fixed dates to anniversary-based schedules and back, fee structures are revised, filing categories are reclassified). Do not rely on a cached schedule. The tracker below records the dates you confirm; update them when your registered agent sends reminders.

For each jurisdiction where the entity is registered (domestic or foreign):

1. Ask the user whether they have a current compliance report from the registered agent — that's the most authoritative source.
2. If not, ask the user what they know (filing type, due-date basis, last filed date, typical fee). Record what they provide.
3. For anything the user does not know, flag the entity × jurisdiction entry as `unknown` — do not populate dates from a cached reference. The user's next step is to confirm with the registered agent or Secretary of State.

**Capture details in the tracker rather than a reference table:**

> I don't have filing requirements for [Jurisdiction] in the reference table.
> Let me capture them so we can track this going forward.
>
> For [Entity] in [Jurisdiction]:
> 1. What type of filing is required? (Annual report, franchise tax, confirmation
>    statement, annual return, or something else?)
> 2. When is it due? (Fixed date like May 1, anniversary month, or other?)
> 3. What's the typical fee? (Approximate is fine — or "unknown".)
> 4. Who is your filing agent or local filing agent there?

Store the answer in a `custom_jurisdictions` block in the tracker:

```yaml
custom_jurisdictions:
  - jurisdiction_code: "[code, with sub-jurisdiction where the code needs it — e.g. usa/NV]"
    jurisdiction_type: "[US state / Canada province / EU member state / GCC state / Swiss canton / other]"
    filings:
      - type: "[filing type]"
        due_basis: "[fixed: MM-DD / anniversary month / other description]"
        typical_fee: "[amount in the profile currency, or unknown]"
        source_tag: "[user provided — <who confirmed it, and against what>]"
        notes: "[any other relevant information — e.g., local agent required, filing in local language]"
    added_by: "manual"
    added_date: "[date]"
```

This custom definition is then applied to all entities in that jurisdiction.
Future `--init` runs and entity additions will use it automatically. For a
populated non-`usa` code, a custom row supplements the jurisdiction file for a
filing the file lacks; it is tagged `[user provided]` with the user's source and
never replaces a row the file already has.

**Jurisdictions outside the shipped reference tree:**

Filings vary enormously by jurisdiction. A code whose `MANIFEST.md` says
`populated: no` is a hard stop for that entity (Step 0, item 3) — the custom
definition flow above is not a substitute for a populated folder and must not be
used to reconstruct a jurisdiction's calendar from memory. Only a `usa`
sub-jurisdiction not covered above, or a user-confirmed extra filing for a
populated code, goes through the custom flow.

For every entity outside the primary code, also ask:
- Is there a local filing agent or registered office agent handling compliance?
  If yes, note the agent name — the tracker can flag when to follow up with them
  as well as computing the due date from the jurisdiction file.
- Is the entity required to file any group-level reports in this jurisdiction
  (e.g., country-by-country reporting, economic substance filings)? Beneficial-
  ownership filings are not free text: for a populated code they are rows of the
  jurisdiction file (for `ksa`: `ultimate-beneficial-ownership-rules.md`,
  annual confirmation on the CR anniversary and a 15-day change notification).

Flag entities with a local agent as `agent_managed: true` in the tracker. The
report mode lists them separately with a note to confirm status with the local
agent; for a populated code it still shows the computed due date and its tag.

### Step 2.5: Compute the dates and tag the numbers

For anniversary-based filings: calculate from `formation_date` (or the
registration date the row names) in the tracker. If the input date is null: set
status to `unknown` and flag for confirmation.

For a populated non-`usa` code, compute every date from the row's formula and
show the inputs. For `ksa`, the formulas the files give are:

- annual assembly / presentation deadline = fiscal year end + 6 months (`companies-law.md` Art. 88 for a JSC, Art. 165 for an LLC, Art. 147 for a simplified JSC; none for a branch);
- financial-statement deposit = fiscal year end + 6 months (Art. 17; Art. 238 for a branch);
- auditor pack date = assembly date − 45 calendar days and shareholder/Ministry pack date = assembly date − 21 calendar days (Arts. 121-122 JSC, Art. 167 LLC; Regs Arts. 31, 65; calendar days per Art. 1);
- CR annual confirmation = the date the Commercial Register Regulations set (`commercial-register-law.md` Arts. 11, 15 — `[model knowledge — verify]` until the Regulations are read, so `unconfirmed`); CR suspension exposure = due date + 90 days + 14-day warning (Art. 15);
- UBO annual confirmation = CR-registration anniversary, may be filed 30 days early (`ultimate-beneficial-ownership-rules.md`); the CR-registration date is `[user provided]`;
- MISA annual update = registration anniversary from the certificate (`investment-law.md` Reg. Art. 13, `[authority — MISA]`);
- zakat/tax return = fiscal year end + 120 days, VAT by turnover band, GOSI on the 15th monthly (`filing-calendar.md` ZATCA and GOSI rows, all `[model knowledge — verify]` → `unconfirmed`).

Roll every date back from the weekend and public holidays in the manifest's
`calendar` row (for `ksa`: Friday-Saturday weekend; Eid al-Fitr, Eid al-Adha,
National Day, Founding Day; Hijri dates on official instruments), never from a
Saturday-Sunday weekend or US federal holidays. Write each computed date with the
tag on the number, in this form: `2027-06-30 [computed — companies-law.md
Art. 165, settled 2026-09-04; inputs: fiscal year end 2026-12-31, entity type LLC]`.
If any input is missing, ask; do not assume.

For `usa`, dates come from the user's confirmation or the registered agent's
report and are tagged `[user provided]`.

### Step 3: Write the tracker

Generate `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/entities/compliance-tracker.yaml` with all entities and their
calculated filing requirements. Set initial status:
- `current` if last_filed is within the current filing period
- `due_soon` if due within 90 days and no last_filed for current period
- `overdue` if due date has passed and no last_filed for current period
- `unknown` if formation_date is missing, or the (`jurisdiction_code`, `entity_type_local`) pair has no rows in the jurisdiction file and no custom definition (tag the entity `[no rule in <code> files — verify]` and ask)
- `unconfirmed` for every filing whose `source_tag` is `[model knowledge — verify]` and whose `confirmed_by` is null

Show a summary after generating:

```
Entity compliance tracker initialized.

Entities: [N]
Total jurisdictions: [N]
Filings tracked: [N]

Status summary:
  ✅ Current:   [N]
  ⏰ Due soon:  [N] (next 90 days)
  🔴 Overdue:   [N]
  ❓ Unknown:   [N] (confirm with filing agent)
  ⚪ Unconfirmed: [N] (model-knowledge rows awaiting accountant / filing-agent confirmation)

Run /corporate-legal:entity-compliance --report to see what's due.
```

---

## Output rules (every mode)

Every report, audit and export this skill produces: prepend the work-product header from `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/CLAUDE.md` `## Outputs` (it differs by role — see `## Who's using this`); directly under it, for any entity whose code is not `usa`, add the jurisdiction disclaimer line from the profile `## Jurisdiction` / the manifest; then apply the bilingual house-style rule from `## Outputs` — when the profile's output language is bilingual, render the bottom line (the status summary) and the findings table (the report's entity rows) in the authoritative language as well as English, using the manifest's spellings. Amounts are in the profile currency. Label every entity row with its jurisdiction code, local entity type and the local status name. Close with the reviewer-note line from Step 0 item 8.

---

## Mode 2: Report

Surfaces upcoming deadlines and flags overdue items. Default: next 90 days, counted on the calendar in the manifest.

```
/corporate-legal:entity-compliance --report [--days 30|60|90|180]
```

Output format:

```
ENTITY COMPLIANCE REPORT — [date]
[Company Name]

🔴 OVERDUE ([N]):
  [Entity] / [jurisdiction code] / [local type] / [Filing type — authority] — was due [date] [source_tag]

⏰ DUE WITHIN [N] DAYS ([N]):
  [Entity] / [jurisdiction code] / [local type] / [Filing type — authority] — due [date] [source_tag]  [filing agent]
  [Entity] / [jurisdiction code] / [local type] / [Filing type — authority] — due [date] [source_tag]

✅ RECENTLY FILED ([N] in last 90 days):
  [Entity] / [jurisdiction code] / [local type] / [Filing type] — filed [date]

❓ UNKNOWN STATUS ([N]):
  [Entity] / [jurisdiction code] / [local type] / [Filing type] — no information; confirm with filing agent

⚪ UNCONFIRMED ([N]) — jurisdiction-file rows tagged [model knowledge — verify]; no alert until confirmed:
  [Entity] / [jurisdiction code] / [local type] / [Filing type — authority] — file says [due basis]; confirm with your accountant or filing agent, then --update

🌐 AGENT-MANAGED ([N]):
  [Entity] / [jurisdiction code] / [Filing type] — managed by [local agent]; computed due [date] [source_tag]; confirm status directly
  [Entity] / [jurisdiction code] — no local agent recorded; add one with --update

⛔ NOT POPULATED ([N]):
  [Entity] / [jurisdiction code] — no reference files for this code; no rule applied [not populated — no rule applied]

REGISTRATION STATUS ([local status name — usa: good standing; ksa: CR active / suspended per commercial-register-law.md Art. 15]):
  Last confirmed: [date]
  Entities with confirmed status: [N] of [total]
  Entities not confirmed in last 12 months: [list]
```

If the tracker covers more than ~10 entities, or any time the user asks: offer the dashboard (see CLAUDE.md `## Outputs → Dashboard offer for data-heavy outputs`). Shape the offer for this output — counts by filing status (overdue / due soon / filed / unknown), counts by good-standing state, and a sortable entity table with jurisdiction, filing type, and next due date.

---

## Mode 3: Update

Updates one or more entities in the tracker. Three sub-modes:

### Consequential-action gate (file SOI / annual report)

**Before directing or confirming a filing:** Read `## Who's using this` in `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/CLAUDE.md`. If the Role is **Non-lawyer**:

> Filing a [filing type] with [the issuing authority from the jurisdiction file — for `usa`: a Secretary of State; for `ksa`: the Ministry of Commerce, ZATCA, GOSI, Qiwa, MISA] has legal consequences — it's a formal representation from the entity, it carries fees, and missed or incorrect filings carry the consequences the jurisdiction file names (for `usa`: loss of good standing, franchise-tax defaults, dissolution; for `ksa`: suspension of the commercial register per `commercial-register-law.md` Art. 15 and fines up to SAR 500,000 per `companies-law.md` Art. 262, plus the ZATCA, GOSI and Qiwa service blocks in `filing-calendar.md`, which are `[model knowledge — verify]`). Have you reviewed this with an attorney (or a qualified filing agent) before filing? If yes, proceed to record the filing. If no, here's a brief to bring to them:
>
> - Entity, jurisdiction code, local entity type, filing type, authority, and due date with its source tag
> - What the tracker says about the last filing (date, fee, officer/director or manager information last reported)
> - Open questions (is the officer/director or manager information still accurate; has the filing agent changed; has the registered address changed)
> - What could go wrong (out-of-date officer information, missed deadline triggering the jurisdiction's sanction, fee calculation error)
> - What to ask the attorney (is a filing actually needed this year; are there any articles amendments or officer changes that need to be reflected; who should sign)
>
> If you need to find an attorney, solicitor, barrister, or other authorised legal professional: contact your professional regulator (state bar in the US, SRA/Bar Standards Board in England & Wales, Law Society in Scotland/NI/Ireland/Canada/Australia, the Saudi Bar Association, or your jurisdiction's equivalent) for a referral service.

Do not record a new `last_filed` date past this gate without an explicit yes. Tracker reads, deadline reports, and "what's due soon" output do not require the gate.

### 3a: Manual update

```
/corporate-legal:entity-compliance --update
```

Attorney tells Claude what was filed:
> "We filed the Delaware annual report for [Entity] on March 1. Fee was $450."

Claude updates:
- `last_filed` → March 1 date
- `last_fee` → $450
- `status` → `current`
- `last_updated` in metadata

A confirmation of a jurisdiction-file row ("our accountant confirmed the zakat return is due 30 April") sets `confirmed_by` and moves the filing from `unconfirmed` to the computed status; the `source_tag` keeps the file's tag and gains `[user provided — confirmed by <name>, <date>]`.

### 3b: Filing agent report upload

```
/corporate-legal:entity-compliance --update --from-report
```

User uploads a compliance report from the filing agent — a registered-agent
service (for `usa`, e.g. CT Corp or National Registered Agents), a
corporate-services provider, a government-relations officer, or the accountant
(PDF, CSV, or Excel). Claude reads it and updates matching entities:

From the report, extract for each entity:
- Filing type and due date
- Last filed date (if present)
- Registration status (good standing / CR active) and date confirmed
- Any flags or warnings from the agent

Match report entities to tracker entities by name (flag near-matches for
confirmation — "Acme Holdings LLC" vs. "Acme Holdings, LLC" are probably
the same entity).

After processing:
```
Updated [N] entities from report.

Matched: [N]
Unmatched (in report, not in tracker): [list — may need to add to entity table]
Not in report (in tracker, no update): [list — status unchanged]
```

### 3c: Bulk status sweep

```
/corporate-legal:entity-compliance --sweep
```

Walks through each entity with `unknown` or `overdue` status and asks for
current information one at a time:

> [Entity] / [jurisdiction code] / [local type] / [Filing type — authority] — currently showing as [status].
> Has this been filed? If yes, when and what was the fee? [For `unconfirmed`: has your accountant or filing agent confirmed the due date the jurisdiction file gives?]

Updates tracker after each confirmation. Produces a completion summary.

---

## Mode 4: Health audit

```
/corporate-legal:entity-compliance --audit
```

Broader review beyond just filing status. Surfaces:

**Filing compliance:**
- Overdue items (from report mode)
- Unknown status items

**Entity health:**
- Entities marked as `dormant` — flag for review: should these be dissolved?
  Carrying dormant entities costs money (annual fees, filing agent fees)
  and creates ongoing compliance obligations.
- Entities with formation_date older than 5 years and status `dormant` — flag
  as dissolution candidates.
- Entities missing formation_date — flag as data gap.

**Registration status gaps** (the jurisdiction's own status evidence — `usa`: good-standing certificate; `ksa`: CR active status per `commercial-register-law.md` Art. 15, evidenced by a current CR extract):
- Entities with no `confirmed_good_standing` date — unknown whether in good
  standing / active; risk if a transaction requires a certificate or extract on short notice.
- Entities with `confirmed_good_standing` older than 12 months — stale; worth
  refreshing, especially if M&A or financing is anticipated.

**Registration gaps per the jurisdiction file:**
- When the applicable code is `usa`: based on `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/CLAUDE.md` entity table, are there states in the company's
  operational footprint (offices, employees) where entities are not foreign
  qualified? This requires the attorney to confirm operational presence —
  Claude can flag the question but cannot determine presence independently.
- When the applicable code is a populated non-`usa` code: test each entity against the registrations its jurisdiction files make mandatory, and flag the ones with no evidence on file. For `ksa`: foreign-investment registration validity and activity match (`investment-law.md` Art. 7(2), Reg. Art. 13, Art. 8(3)) for any entity with non-Saudi ownership; CR annual confirmation filed and no suspension (`commercial-register-law.md` Arts. 11, 15); UBO initial disclosure and latest annual confirmation on file (`ultimate-beneficial-ownership-rules.md`); GOSI registration and certificate and Qiwa establishment file, documented contracts and Nitaqat band (`social-insurance-law.md` Arts. 7, 10; `platform-obligations.md` Labor Law Arts. 15-16, 51; `saudization-nitaqat.md` — the band is taken from a dated Qiwa export, never inferred); the entity's own bank accounts in use (`anti-concealment-law.md` Arts. 4(c), 17). A registration the files do not cover (a sector-regulator licence) is listed as `[no rule in ksa files — verify]`.

**Intercompany agreement gaps:**
- From `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/CLAUDE.md`: if intercompany agreements are marked as partial or no,
  flag which entity relationships likely need agreements (parent-subsidiary
  services, IP licenses, loans).

Output format:

```
ENTITY HEALTH AUDIT — [date]

FILING COMPLIANCE
  Overdue: [N]
  Unknown status: [N]
  Action: run --sweep to confirm unknown items

DORMANT ENTITIES ([N])
  [List of dormant entities with age and annual carrying cost if known]
  Dissolution candidates (>5 years dormant): [list]

REGISTRATION STATUS ([local status name per jurisdiction code])
  No record: [N] entities
  Stale (>12 months): [N] entities
  Consider refreshing before: [any upcoming transactions or contract renewals if known]

POTENTIAL GAPS
  Registration gaps per the jurisdiction file:
    [usa — foreign qualification: flag question — confirm operational presence in:]
    [list of states from `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/CLAUDE.md` footprint not in tracker as qualified]
    [non-usa — per entity: registration / file row / evidence on file or missing, e.g. for ksa: MISA registration — investment-law.md Reg. Art. 13 — missing; UBO annual confirmation — ultimate-beneficial-ownership-rules.md — filed 2026-03-01]
  Unconfirmed model-knowledge rows: [N] filings awaiting accountant / filing-agent confirmation
  Intercompany agreements: [status from `${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/CLAUDE.md`]

RECOMMENDED ACTIONS
  1. [Highest priority action]
  2. [etc.]
```

---

## Mode 5: Export

```
/corporate-legal:entity-compliance --export [--format csv|table]
```

Produces a flat export suitable for sharing with finance, legal ops, or the
filing agent. Default: CSV.

CSV columns:
`Entity Name, Local Entity Type, Jurisdiction Code of Formation, Registry Number, Formation Date, Status,
Filing Agent, Jurisdiction Code, Registration Type, Filing Type, Authority, Source Tag, Confirmed By, Due Date,
Last Filed, Last Fee ([profile currency]), Registration Status Confirmed, Notes`

One row per filing per jurisdiction. Multiple rows per entity (one per
jurisdiction × filing type combination).

If `--format table`: produce a markdown table suitable for pasting into
a report or Slack message, showing only the next 90 days of filings.

---

## What this skill does not do

- It does not file anything. Output is a tracker and a to-do list; filing
  is done by the attorney, outside counsel, or filing agent.
- It does not pull good-standing certificates or registry extracts. It tracks
  when status was last confirmed; obtaining the evidence is manual or via the
  filing agent.
- It does not determine whether registration is required in a given
  jurisdiction (foreign qualification under `usa`; a branch CR or
  foreign-investment registration under `ksa`). That analysis depends on facts
  about business activity that the attorney must confirm.
- It does not replace a filing agent for companies with complex
  multi-entity structures. Registered-agent services, corporate-services
  providers and government-relations officers have dedicated compliance teams
  and direct relationships with the authorities.
  This skill is best suited for smaller organizations without agent support,
  or as a lightweight layer on top of agent data for organizations that do
  have support.
- The jurisdiction files' filing rows are not legal advice and may not reflect
  current requirements. Confirm all deadlines before relying on them; rows
  tagged `[model knowledge — verify]` are never treated as confirmed by this skill.


## Formula injection defense

Before writing any cell in Excel, Sheets, or CSV output, neutralize formula injection. Counterparty-sourced text (contract quotes, party names, registered agent data, CLM exports) is attacker-controlled. A cell starting with `=`, `+`, `-`, `@`, `	`, `
`, or `
` will be interpreted as a formula or break the row structure.

- **Prefix with a single quote:** `'=SUM(A1:A10)` → `=SUM(A1:A10)` (displayed as text, not executed)
- **Applies to every cell that contains text sourced from a document, a tool result, or a user paste.** Column headers you control and computed values you produce are safe.
- **CSV: also escape embedded commas, double quotes, newlines** (RFC 4180 quoting).
- This is not optional. A spreadsheet your user opens in Excel that triggers a macro or exfiltrates data via DDE is a supply-chain attack on your user.
