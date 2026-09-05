RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY, SOLICITOR, BARRISTER, OR OTHER AUTHORISED LEGAL PROFESSIONAL IN YOUR JURISDICTION BEFORE ACTING

> **⚠️ Reviewer note**
> - **Sources/read:** Read all three practice profiles at your supplied absolute paths, both fixtures, the skill instructions, and the repository’s registry and `gbr` manifest.
> - **Currency:** No legal research undertaken; the workflows stopped at the jurisdiction-population check. Portal fetched: no.
> - **Jurisdiction files:** `references/jurisdictions/REGISTRY.md` and `references/jurisdictions/gbr/MANIFEST.md`. The manifest specifies `populated: no` and contains no jurisdiction disclaimer.
> - **Scope:** Scenario date: **2026-09-04**. No jurisdiction’s substantive rules were applied. No files were written.

## 1. commercial-legal-review — COM-01

1. **Step 0.1:** The commercial profile identifies primary jurisdiction `gbr`, with no other footprint codes.
2. **Step 0.2:** Applied your governing-law override: “the laws of England and Wales.” The agreement retains Riyadh-registered parties, so `ksa` is an additional matter connection beyond the profile; no Saudi-law analysis was undertaken.
3. **Step 0.3:** The [`gbr` manifest](</Users/basimkhoja/Projects/Legal Consultant/references/jurisdictions/gbr/MANIFEST.md>) says `populated: no`. The [review skill](</Users/basimkhoja/Projects/Legal Consultant/.agents/skills/commercial-legal-review/SKILL.md>) requires this stop message:

> Jurisdiction `gbr` (United Kingdom) is registered but not populated: no reference files exist for it. I will not apply another jurisdiction's rules or model knowledge in its place. Options: (1) populate `references/jurisdictions/gbr/` (see README, 'How to add a jurisdiction'), (2) route this matter to local counsel, (3) tell me to proceed with the analysis limited to the populated jurisdictions in this matter, with every finding for `gbr` marked `[not populated — no rule applied]`.

**Result:** Stopped before routing or substantive review. The profile’s `confirm_routing: false` does not override Step 0. No findings, redlines, or escalation assessment produced. Moved to skill 2 as instructed.

## 2. corporate-legal-entity-compliance — --init

1. **Step 0.1:** The corporate profile identifies primary jurisdiction `gbr`.
2. **Step 0.2:** Used your expressly supplied one-entity scope: **Acme Ltd**, private company limited by shares, `gbr`, incorporated **2019-05-01**, financial year end **31 March**.
3. **Step 0.3:** The manifest says `populated: no`. The [entity-compliance skill](</Users/basimkhoja/Projects/Legal Consultant/.agents/skills/corporate-legal-entity-compliance/SKILL.md>) requires this stop message before initialization:

> Jurisdiction `gbr` (United Kingdom) is registered but not populated: no reference files exist for it. I will not apply another jurisdiction's rules or model knowledge in its place. Options: (1) populate `references/jurisdictions/gbr/` (see README, 'How to add a jurisdiction'), (2) route this matter to local counsel, (3) tell me to proceed with the analysis limited to the populated jurisdictions in this matter, with every finding for `gbr` marked `[not populated — no rule applied]`.

**Result:** **Acme Ltd / `gbr` / private company limited by shares — `[not populated — no rule applied]`.** Initialization stopped. No filing requirements, deadlines, or compliance statuses computed; no tracker generated. The custom-jurisdiction flow cannot substitute for an unpopulated folder. Moved to skill 3.

## 3. employment-legal-termination-review — EMP-01

1. **Context:** Read the employment profile; it describes an in-house practice and does not enable matter workspaces.
2. **Step 0.1–0.2:** Primary jurisdiction is `gbr`. Applied your overrides: Ahmed works in **London** under an **English-law contract**.
3. **Step 0.3:** The manifest says `populated: no`. The [termination-review skill](</Users/basimkhoja/Projects/Legal Consultant/.agents/skills/employment-legal-termination-review/SKILL.md>) requires this stop message:

> Jurisdiction `gbr` (United Kingdom) is registered but not populated: no reference files exist for it. I will not apply another jurisdiction's rules or model knowledge in its place. Options: (1) populate `references/jurisdictions/gbr/` (see README, 'How to add a jurisdiction'), (2) route this matter to local counsel, (3) tell me to proceed with the analysis limited to the populated jurisdictions in this matter, with every finding for `gbr` marked `[not populated — no rule applied]`.

**Result:** Stopped before the high-risk scan, notice assessment, settlement calculations, severance/release analysis, or go/no-go recommendation. The fixture’s Saudi nationality, Qiwa documentation, and SAR wage figures do not authorize substituting Saudi rules for the English-law review. Moved to the simulation.

## 4. employment-legal-cold-start-interview — simulated answer `gbr`

An ordinary invocation with the existing completed profile would **skip the interview unless `--redo`**. Your requested simulation places the interview at **Part 1’s primary-jurisdiction answer**, so the following is its handling of `gbr`.

1. Takes `gbr` from the simulated answer. The setup-mode exception allows the primary code to come from that answer without requiring a pre-existing jurisdiction section.
2. Looks up `gbr` in `REGISTRY.md` and reads its manifest.
3. Finds `populated: no`; **refuses to write a profile with `gbr` as primary**.
4. Prints the [cold-start skill’s Part 1 refusal](</Users/basimkhoja/Projects/Legal Consultant/.agents/skills/employment-legal-cold-start-interview/SKILL.md>), with the populated-code list filled from the registry:

> Jurisdiction `gbr` (United Kingdom) is registered but not populated: no reference files exist for it, so every skill in this plugin would stop on your first matter. I will not write a profile with an unpopulated primary jurisdiction. Options: (1) choose `usa` (upstream US path, upstream research connectors), (2) choose a populated code — currently: `ksa` (Kingdom of Saudi Arabia), (3) populate `references/jurisdictions/gbr/` first (see README, 'How to add a jurisdiction') and re-run setup.

**Result:** The skill waits for an answer before continuing. Under your simulation instruction, execution ends here without asking a question or writing a profile. It does not select a replacement code automatically. If the user later chooses option 1 or 2, the written instructions say to use that chosen primary code and retain `gbr` in the footprint as `[not populated — no rule applied]`.