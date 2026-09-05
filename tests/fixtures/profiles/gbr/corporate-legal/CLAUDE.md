# Corporate Practice Profile (test fixture, synthetic)
*Active modules: M&A | Board & Secretary | Entity Management*

## Company profile

**Entity name:** Example Telematics Co.
**Industry / sector:** Telematics
**Stage:** private
**Primary jurisdiction:** gbr
**Legal team size:** 2
**Escalation:** Legal Lead, then external Saudi counsel (synthetic)
**Commercial registration number and registry:** CR 1010000000, Ministry of Commerce (synthetic)
**Legal form under the local companies law:** LLC
**Foreign-investment registration:** MISA investment registration certificate (synthetic number), IT consulting
**Statutory registrations:** ZATCA, GOSI, Qiwa, Chamber, municipal licence (all synthetic)
**Ultimate beneficial ownership filing:** filed; last annual confirmation 2026-01-15 (synthetic)
**Listed-company regulator and exchange:** not listed
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
| VDR | ✗ | Diligence pulls from local folder |
| Board portal | ✗ | Minutes/consents from local templates |
| Document storage | ✗ | Read local paths |
| Slack | ✗ | Briefs emitted as files only |

## M&A

**Typical side:** buy-side
**Deal cadence:** bespoke each deal
**Deal lead:** legal

### Diligence structure
**Request list categories:** Corporate, Contracts, Employment, Regulatory, Litigation, IP, Data
**Materiality thresholds:**
- Contracts: above SAR 500,000 annual value
- Litigation: all pending

### Issues memo format
**Severity scheme:** Red/Yellow/Green
**Audience:** deal team
**Depth:** tiered by severity

## Board & Secretary

**Role:** Attorney-advisor without formal secretary role
**Board size:** 3 managers (LLC)
**Committees:** none
**Minutes format:** action minutes
**Written consents:**
- Used for: manager appointments, branch openings, routine approvals
- Limits: per the articles of association
**Consent format:**
- Resolution language: "قرر الشركاء / RESOLVED"
- Recital depth: minimal
- Electronic signatures: accepted

## Entity Management

**Active entities:** 2
**Key jurisdictions:** gbr
**Filing agent (registered agent, corporate-services provider, government-relations officer, or in-house):** in-house government-relations officer
**Entity management system:** manual spreadsheet
**Routine filing owner:** legal
**Compliance tracker:** ${LEGAL_CONSULTANT_HOME:-~/.legal-consultant}/corporate-legal/entities/compliance-tracker.yaml

**Entity table:**

| Entity name | Local type | Jurisdiction code | Registry number | Owner | Ownership % | Status |
|---|---|---|---|---|---|---|
| Example Telematics Co. | Ltd | gbr | CR 1010000000 | Founders | 100 | Active |
| Example Telematics Holding Ltd | Ltd | gbr | CR 1010000001 | Founders | 100 | Active |
