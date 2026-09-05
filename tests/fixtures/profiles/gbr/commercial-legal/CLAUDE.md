# Commercial Contracts Practice Profile (test fixture, synthetic)

## Who we are

Example Telematics Co. is a limited liability company. The contracts team is 2 people. The Legal Lead is the final escalation point. We process roughly 15 agreements per month, mostly purchasing. We use no CLM system.
**Commercial registration:** CR 1010000000 (synthetic)
**Legal form:** LLC under the Companies Law
**Practice setting:** In-house

## Who's using this

**Role:** Non-lawyer with attorney access
**Attorney contact:** External Saudi counsel on retainer (synthetic)
**Local counsel for escalation:** N/A for these tests

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
| CLM | ✗ | Manual record-keeping; renewal-tracker runs against a local register |
| E-signature | ✗ | User routes for signature outside the plugin |
| Document storage | ✗ | User uploads agreements directly |
| Slack | ✗ | Alerts delivered inline |

## Playbook

**Active side:** purchasing

### Purchasing-side playbook

#### Limitation of liability
**Direct cap (multiple of fees):** Vendor cap at 12 months fees paid or payable
**Indirect / consequential damages:** excluded both ways
**Carveouts we require (above the cap):** Gross negligence, fraud, breach of confidentiality, data breach
**Cap base definition we accept:** fees paid in the 12 months preceding the claim
**Never accept:** Uncapped indirect damages; vendor exclusion of liability for gross negligence or fraud

#### Indemnification
**Standard position:** Vendor indemnifies for IP infringement and data breach; we indemnify for our data

#### Data protection
**Standard position:** Vendor signs our data-processing terms as processor
**Requirements:** ISO 27001 or equivalent for any vendor touching customer data

#### Term and termination
**Standard position:** Termination for convenience on 30 days' notice; auto-renewal only with a 30-day cancel window
**Never accept:** Multi-year lock-in with no termination rights

#### Governing law and venue
**Preferred:** Laws of the Kingdom of Saudi Arabia
**Acceptable:** English law with arbitration
**Escalate:** Any foreign court jurisdiction clause
**Never:** Foreign law with foreign courts and no arbitration
**Forum:** arbitration
**Arbitration institution and seat:** SCCA, Riyadh
**Language of proceedings and prevailing contract language:** English; Arabic prevails in a Saudi forum
**Jurisdiction playbook defaults applied:** all Commercial rows accepted

#### The one thing
Any clause letting the vendor use our fleet data for its own purposes.

## Escalation

| Can approve | Without escalation | Escalates to | Via |
|---|---|---|---|
| Contracts manager | Standard terms, under SAR 200,000 | Legal Lead | email |
| Legal Lead | Under SAR 2,000,000 | CFO | email |

**Value thresholds (in the profile currency, see `## Jurisdiction`):** SAR 200,000 / SAR 2,000,000
**Automatic escalations regardless of contract value:** Uncapped liability, foreign courts, data use for training

## House style

**Tone in redlines:** Firm, courteous
**Stakeholder summaries:** Procurement lead reads them; one page
**Where work product goes:** Local folder
**Renewal alerts go to:** email

## Review preferences

confirm_routing: false

## NDA triage preferences

closing_action: "Forward this output and the NDA to the Legal Lead."
