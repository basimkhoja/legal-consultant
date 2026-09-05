# Employment Law Practice Profile (test fixture, synthetic)

## Who we are

Example Telematics Co. Employee count: 180. HR lead: HR Lead (synthetic). Employment counsel: external Saudi counsel (synthetic).
**Practice setting:** In-house

## Who's using this

**Role:** Non-lawyer with attorney access
**Attorney contact:** External Saudi counsel (synthetic)

## Jurisdiction

**Primary jurisdiction:** `gbr`
**Footprint (other jurisdictions this practice operates in):** none
**Authoritative language of the primary jurisdiction:** English
**Output language:** English plus the authoritative language for the bottom line, findings table, and counterparty-facing text (bilingual)
**Calendar for deadlines:** Friday-Saturday weekend; Eid al-Fitr, Eid al-Adha, National Day (23 September), Founding Day (22 February); Hijri dates on official instruments
**Currency for thresholds:** SAR
**Primary-source portal:** https://laws.boe.gov.sa
**Local counsel available for escalation:** N/A
**Jurisdiction playbook defaults accepted:** all rows of `references/jurisdictions/gbr/playbook-defaults.md` accepted as written

**Unpopulated jurisdiction rule.** If any code above resolves to a manifest with `populated: no`, every skill stops for that code and says so.

## Available integrations

| Integration | Status | Fallback if unavailable |
|---|---|---|
| HRIS | ✗ | Leave data tracked in the local leave register |
| Document storage | ✗ | Read local paths |
| Slack | ✗ | Reviews emitted as files only |

## Jurisdictional footprint

**Primary jurisdiction and sub-jurisdictions with employees:** gbr (England and Wales)
**Other countries with employees:** none
**Headcount by nationality:** 70 Saudi nationals, 110 non-Saudi
**Nationalisation-quota band:** Low Green N/A (no nationalisation quota recorded for this jurisdiction)
**Work-permit sponsorship:** we sponsor; pipeline of 5 permits per quarter
**Contract types in use:** indefinite and fixed-term, all documented on Qiwa
**Social-insurance and labour-platform registrations:** GOSI, Qiwa establishment, Mudad wage files (synthetic numbers)
**Remote-first or office-based:** office-based

## Hiring review

**When legal reviews hires:** all offers with restrictive covenants; all non-Saudi hires
**Offer letter template:** local folder
**Restrictive covenant policy:** non-competes only for senior roles, per the jurisdiction file
**Background check policy:** standard

## Termination review

**When legal reviews terminations:** all
**Statutory end-of-service entitlement:** per `references/jurisdictions/gbr/labor-law.md`; the skill computes it
**Standard severance above the statutory entitlement:** none
**Standard notice periods by contract type:** per the jurisdiction file unless the contract gives more
**Release required for severance:** N
**High-risk termination flags (auto-escalate):**
- per the jurisdiction file

## Handbook

**Current version:** work regulations certified 2025-06-01 (synthetic)
**Update cadence:** annual
**Jurisdiction supplements:** none
**Regulatory approval of work regulations:** HRSD-certified work regulations, 2025-06-01
**Language versions:** Arabic prevails; English courtesy copy

## Wage & hour

**Overtime policy:** statutory
**Known classification risk areas:** field technicians on call

## Systems

**HRIS:** none
**Leave data access:** manual, local leave register
**Handbook location:** local folder

## Escalation

| Issue | Handle at | Escalate to | When |
|---|---|---|---|
| Routine offer letter | HR | Legal Lead | Restrictive covenants, non-Saudi hire |
| Performance termination | HR + Legal Lead | External counsel | High-risk flags present |
| Agency complaint or claim (labour office, Labor Court) | — | Legal Lead immediately | Always |
