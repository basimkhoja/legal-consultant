# EMP-03 — Overtime during the fasting month

**Skill:** `/employment-legal:wage-hour-qa`

**Profile fixture.** As EMP-01.

**Input.** "A Muslim technician on SAR 9,000 basic worked 8 hours a day for 6 days during Ramadan. How much overtime is due for the week?"

**Expected behaviours.**
1. Step 0 runs; the answer uses the ksa scaffold: Ramadan hours (6 a day / 36 a week) from `labor-law.md` Arts. 98-100, overtime at hourly wage plus 50% from Art. 107, weekly rest Art. 104; the hourly-wage divisor is stated as the file states it or flagged `[review]` if the file leaves it open.
2. The computed amount carries the `[computed — …; inputs: …]` tag; the regular-rate/§207(e) scaffold does not appear.
3. Limitation on wage claims from `labor-dispute-route.md` mentioned if exposure is discussed.

**Forbidden.** §207(e), 0.5× posture, liquidated-damages doubling, "50-state survey".
