# COM-03 — Cancel-by date on the manifest weekend

**Skill:** `/commercial-legal:renewal-tracker` (add mode, then report)

**Profile fixture.** As COM-01.

**Input.** "Add this to the renewal tracker: SaaS subscription with Vendor X, annual value SAR 240,000, term ends 2027-03-13, auto-renews unless we give 30 days' written notice by email." (2027-02-11 is a Thursday; 30 days before 2027-03-13 is 2027-02-11. Choose the dates so that the computed cancel-by date falls on a Friday or Saturday; adjust the term end if the calendar differs and note the adjustment in the result log.)

**Expected behaviours.**
1. The cancel-by date is computed and then rolled back against the manifest calendar: a Friday or Saturday cancel-by date rolls back to Thursday, never "Friday" as the previous business day.
2. The skill states the weekend it used ("Friday-Saturday per the ksa manifest") and notes that Eid dates are announced annually and must be confirmed `[verify — holiday dates announced annually]`.
3. The register entry shows the value as `SAR 240,000`, not `$`.
4. The computed date carries a provenance tag naming the notice clause and the calendar source.

**Forbidden.** "If Saturday, roll back to Friday"; "US federal holidays as a placeholder"; a dollar sign.
