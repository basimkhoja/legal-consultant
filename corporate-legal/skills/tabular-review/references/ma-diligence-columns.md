# M&A Diligence — Standard Column Set

The default schema for a buy-side target contract review. Start here, then add or cut columns based on the deal. This is a starting point, not a checklist — the purchase agreement's reps and the request list drive what actually matters. The `jurisdiction_code` column is always present; the jurisdiction overlay at the end adds optional columns for each populated non-`usa` code in the matter.

```yaml
schema:
  name: "M&A Diligence — Standard"
  columns:
    - id: jurisdiction_code
      label: "Jurisdiction Code"
      type: classify
      options: [ksa, gbr, fra, che, usa, other]
      prompt: "Which jurisdiction code does this document resolve to (governing-law clause; the contracting target entity's incorporation)? If two codes apply, put the governing law here and the second code in notes."

    - id: counterparty
      label: "Counterparty"
      type: verbatim
      prompt: "Name the contracting party other than the target entity, exactly as it appears."

    - id: agreement_type
      label: "Agreement Type"
      type: classify
      options: [msa, purchase_order, license_in, license_out, lease, services, supply, distribution, nda, joint_venture, loan, guaranty, employment, other]
      prompt: "What kind of agreement is this?"

    - id: effective_date
      label: "Effective Date"
      type: date
      prompt: "When did this agreement become effective?"

    - id: term
      label: "Term"
      type: duration
      prompt: "What is the initial term?"

    - id: auto_renewal
      label: "Auto-Renewal"
      type: classify
      options: [none, annual, fixed_period, evergreen]
      prompt: "Does the agreement auto-renew? On what cycle?"

    - id: termination_for_convenience
      label: "Termination for Convenience"
      type: classify
      options: [none, either_party, target_only, counterparty_only]
      prompt: "Can either party terminate without cause? Who?"

    - id: termination_notice
      label: "Termination Notice Period"
      type: duration
      prompt: "How much notice is required to terminate?"

    - id: change_of_control
      label: "Change of Control"
      type: classify
      options: [silent, consent_required, consent_not_unreasonably_withheld, automatic_termination, notice_only, counterparty_right_to_terminate]
      prompt: "Does the agreement address a change of control of the target? What triggers and what happens?"

    - id: assignment
      label: "Assignment"
      type: classify
      options: [silent, consent_required, consent_not_unreasonably_withheld, freely_assignable, assignable_to_affiliates, non_assignable]
      prompt: "Can the target assign this agreement? What restrictions apply?"

    - id: exclusivity
      label: "Exclusivity / Non-Compete"
      type: classify
      options: [none, exclusive_supplier, exclusive_customer, non_compete, non_solicit, territory_restriction, most_favored_nation]
      prompt: "Does the agreement restrict either party from competing or contracting with others?"

    - id: liability_cap
      label: "Liability Cap"
      type: currency
      prompt: "Is there a cap on liability? What is the amount or multiplier?"

    - id: indemnification
      label: "Indemnification"
      type: classify
      options: [none, mutual, target_indemnifies, counterparty_indemnifies, ip_only, third_party_claims_only]
      prompt: "Who indemnifies whom, and for what?"

    - id: governing_law
      label: "Governing Law"
      type: verbatim
      prompt: "What jurisdiction's law governs?"

    - id: dispute_resolution
      label: "Dispute Resolution"
      type: classify
      options: [litigation, arbitration_binding, arbitration_nonbinding, mediation_first, silent]
      prompt: "How are disputes resolved?"

    - id: most_favored_nation
      label: "MFN / Pricing Protection"
      type: classify
      options: [none, mfn_pricing, price_matching, benchmarking_right]
      prompt: "Is there a most-favored-nation or pricing protection clause?"

    - id: minimum_commitments
      label: "Minimum Purchase / Volume Commitments"
      type: currency
      prompt: "Are there minimum purchase, volume, or spend commitments?"

    - id: ip_ownership
      label: "IP Ownership"
      type: classify
      options: [each_owns_own, target_owns_work_product, counterparty_owns_work_product, joint, license_only, silent]
      prompt: "Who owns intellectual property created or used under the agreement?"

    - id: confidentiality_term
      label: "Confidentiality Survival"
      type: duration
      prompt: "How long do confidentiality obligations survive termination?"

    - id: insurance_requirements
      label: "Insurance Requirements"
      type: classify
      options: [none, general_liability, professional_liability, cyber, workers_comp, umbrella, statutory_scheme]
      prompt: "What insurance must be maintained? The options are the usa taxonomy; for a populated non-usa code, take the statutory scheme from the jurisdiction file — for ksa the GOSI occupational-hazards branch (social-insurance-law.md Arts. 28-29, 2% for all nationalities) stands where workers_comp would, so classify a clause requiring it as statutory_scheme and quote it."

    - id: audit_rights
      label: "Audit Rights"
      type: classify
      options: [none, counterparty_may_audit_target, target_may_audit_counterparty, mutual]
      prompt: "Does either party have audit rights?"

    - id: notices
      label: "Notice Requirements"
      type: verbatim
      prompt: "What is the notice address and method for the target?"
```

## Common additions by deal type

The regulator names below are the `usa` set. For a populated non-`usa` code, take the regulator and the filing trigger from the jurisdiction file that covers the sector, and where no file covers it (for `ksa`: healthcare, telecoms and financial-sector regulators are not in the files) write the column prompt with `[no rule in ksa files — verify]` and quote only what the document says. For `ksa` the files that do cover a sector are `government-tenders-procurement-law.md` (government contractors, using the applicable procurement rows by matter date: assignment consent 1448H Art. 68 / 2019 Art. 70, subcontracting 1448H Art. 69 / 2019 Art. 71, bond 1448H Art. 59 / 2019 Art. 61, penalty caps 1448H Art. 70 / 2019 Art. 72, termination triggers 1448H Art. 74 / 2019 Art. 76) and `corporate-governance-regulations.md` (listed targets: CGR Art. 1 and LJSC Art. 66 related-party definitions as the column definitions, CGR Art. 87 as the board-report source list).

- **Tech / IP-heavy targets:** source code escrow, open source restrictions, data rights, model training rights, API access
- **Healthcare / life sciences:** BAA presence, regulatory filing obligations, FDA correspondence, clinical trial obligations
- **Government contractors:** novation consent requirements, flow-down clauses, security clearance, FAR/DFARS citations
- **Real estate:** renewal options, rent escalation, CAM provisions, subordination, estoppel requirements
- **Regulated financial:** regulatory approval conditions, capital requirements, FINRA/SEC filing triggers

## Jurisdiction overlay — optional columns per populated non-`usa` code

Offered by `tabular-review` Step 1 for each populated non-`usa` code resolved in Step 0. Every column names the file and article its prompt applies; the cell carries the row's tag (`[settled — last confirmed YYYY-MM-DD]`, `[authority — <name>]`, or `[model knowledge — verify]`) in notes. A column marked `[no rule in <code> files — verify]` is offered only as a verbatim capture with no classification. The overlay adds columns; it never replaces the standard set.

### `ksa`

```yaml
    - id: ksa_tasattur_indicators
      label: "Tasattur Indicators"
      type: classify
      options: [none, non_saudi_signatory_or_poa, profit_sharing_side_letter, nominee_or_trust_declaration, personal_bank_account_use, management_agreement_transferring_control]
      prompt: "Does the document show a non-Saudi exercising ownership-type control or profit participation through a Saudi licence holder? Map to anti-concealment-law.md Arts. 2-4; cite Art. 15 (nullity) in notes. Indicators not in that file are tagged [model knowledge — verify]."

    - id: ksa_misa_registration
      label: "MISA Registration"
      type: classify
      options: [not_applicable_no_foreign_ownership, certificate_present_activity_matches, certificate_present_activity_mismatch, certificate_missing_or_lapsed, unclear]
      prompt: "For a document evidencing foreign ownership or a foreign-owned counterparty: is a MISA investment registration certificate present and does its activity match the business? investment-law.md Art. 7(2), Reg. Art. 13, Art. 8(3)."

    - id: ksa_nitaqat_band
      label: "Nitaqat Band (dated Qiwa export)"
      type: verbatim
      prompt: "Quote the Nitaqat band, rate and export date from a Qiwa export in the data room. saudization-nitaqat.md Services-by-Range row; never infer the band from coefficients."

    - id: ksa_qiwa_documentation
      label: "Qiwa Contract Documentation"
      type: classify
      options: [documented_on_qiwa, not_documented, unclear]
      prompt: "For an employment contract: is it documented on Qiwa per Labor Law Art. 51 with Regulation Art. 18 (platform-obligations.md)? Quote the authentication reference if present."

    - id: ksa_gosi_standing
      label: "GOSI Standing"
      type: classify
      options: [certificate_current, arrears_shown, no_evidence, unclear]
      prompt: "Is a current GOSI compliance certificate or statement of account present, and does it show arrears? social-insurance-law.md Art. 10 (services block), Art. 59 (five-year look-back)."

    - id: ksa_zatca_standing
      label: "ZATCA Standing"
      type: classify
      options: [certificate_current, returns_outstanding, no_evidence, unclear]
      prompt: "Is a ZATCA zakat/tax certificate or filing evidence present? filing-calendar.md ZATCA rows — every ZATCA rule is [model knowledge — verify]; record only what the document shows."

    - id: ksa_ubo_filing
      label: "UBO Filing"
      type: classify
      options: [initial_and_annual_on_file, initial_only, none_on_file, listed_jsc_out_of_scope, unclear]
      prompt: "Is the entity's UBO initial disclosure and latest annual confirmation on file? ultimate-beneficial-ownership-rules.md (annual confirmation on the CR anniversary; 15-day change notification). Note any nominee shareholder of record."

    - id: ksa_merger_control
      label: "Merger-Control Threshold Inputs"
      type: currency
      prompt: "Record the party's last audited annual revenue (SAR) for the three-test threshold in competition-law.md Art. 7 / Reg. Art. 12 / Guidelines s.6; the test itself is run by diligence-issue-extraction."

    - id: ksa_commercial_agency_registration
      label: "Commercial Agency Registration"
      type: classify
      options: [not_an_agency_or_distribution_agreement, registered_current_term, registration_missing_or_expired, unclear]
      prompt: "For an agency or distribution agreement: is a Ministry of Commerce Commercial Agencies Register certificate present for the current term (commercial-agencies-law.md Art. 3; Added Art. 1)? Note whether after-sales obligations are allocated (Added Art. 2)."

    - id: ksa_share_transfer_preemption
      label: "Share-Transfer Pre-emption / Restriction"
      type: classify
      options: [statutory_default_llc_art_178, articles_restriction, sha_restriction, none_found, unclear]
      prompt: "For articles of association or a shareholders' agreement: what restriction applies to a transfer of shares or interests? companies-law.md Art. 178 (LLC pre-emption, 30-day window), Art. 111 and Arts. 151-154 (JSC/SJSC), Arts. 113, 181 (drag/tag). Quote the clause."

    - id: ksa_losses_trigger
      label: "Losses Trigger"
      type: classify
      options: [losses_below_half_capital, losses_at_or_above_half_capital, unclear]
      prompt: "From the financial statements: have losses reached half of the capital? companies-law.md Art. 132 (JSC: 60-day disclosure, 180-day EGA) / Art. 182 (LLC: 60-day assembly); Art. 261(h)."

    - id: ksa_assignment_on_change_of_control
      label: "Assignment on Change of Control (Civil Transactions Law)"
      type: classify
      options: [share_sale_no_transfer_art_98, asset_transfer_needs_consent_art_255, advance_consent_present_art_255, unclear]
      prompt: "Given the deal structure: does this contract move without consent? civil-transactions-law.md Art. 98 (share sale does not transfer contracts; CoC right only if drafted), Art. 255 (consent to assign a contract; advance consent valid on notice), Art. 256 (assignor jointly liable absent release)."

    - id: ksa_pdpl_processor_terms
      label: "PDPL Processor Terms"
      type: classify
      options: [not_a_processing_contract, art_8_terms_present, art_8_terms_incomplete, transfer_clause_offshore, unclear]
      prompt: "Does the contract contain the controller-processor terms of PDPL Art. 8 / Regulation Art. 17 and a transfer mechanism for offshore processing (Art. 29)? personal-data-protection-law.md; the transfer-regulation row is [model knowledge — verify]."

    - id: ksa_insolvency_clause
      label: "Insolvency Termination Clause"
      type: classify
      options: [none, ipso_facto_clause_present, art_26_excluded_counterparty, unclear]
      prompt: "Is there a termination-on-insolvency clause, and is the counterparty a government entity or bank within bankruptcy-law.md Art. 26? Art. 23 voids ipso-facto clauses in a protective settlement or financial restructuring; the liquidation position is an open question in that file."

    - id: ksa_cr_status
      label: "Commercial Register Status"
      type: classify
      options: [active, suspended, no_extract, unclear]
      prompt: "From a CR extract: status (commercial-register-law.md Art. 15), and the Art. 6 data points — trade name, legal form, capital, managers and their powers, head office. Flag any Art. 20 court entry."

    - id: ksa_esignature_certificate
      label: "E-signature Completion Certificate"
      type: classify
      options: [wet_ink, platform_signed_certificate_present, platform_signed_no_certificate, unclear]
      prompt: "For a platform-signed contract: is the completion certificate present? electronic-transactions-law.md Art. 6(1)(c), 8, 9(4); Art. 14(3)-(4) presumptions attach only to certified signatures."
```

## Common cuts for a fast first pass

For a time-pressured initial screen, these 6 columns answer 80% of the early deal questions: counterparty, effective_date, term, change_of_control, assignment, termination_for_convenience. Run those first, expand the schema once the deal team has prioritized.
