# Amendment watch — 2026-09-05 (lead generator, then portal confirmation)

Task T4 of `.planning/TRACKER.md`: the pre-release rerun of the 2026-09-04 watch. Same three queries through the `last30days` skill (`last30days v3.18.4 · synced 2026-09-05`; window 2026-08-06 to 2026-09-05), three WebSearch supplements per query, then every lead that names an instrument in the GUID table of `references/jurisdictions/ksa/SOURCES.md` checked on laws.boe.gov.sa with `scripts/fetch-law.py`, and the portal's updates log re-read (pages 1 to 3). Every item in the query tables is an UNCONFIRMED LEAD unless the "Confirmed on an official source" section says otherwise.

Method note: each query ran once with a host-authored plan file (`--plan`), the first-party X handles from the 2026-09-04 run (`@HRSD_SA`, `@MCgovSA`, `@SDAIA_SA`, plus `@MISA`, `@MojKsa`, `@ArgaamPlus` as related voices) and `r/saudiarabia`, `r/Riyadh`, `r/jeddah`, `r/expats`. As on 2026-09-04 the engine's ranked clusters were general Saudi news (nuclear deal, Diriyah, deportation statistics); the on-topic leads come from the first-party posts in the raw files and from the web supplements. Raw files: `~/Documents/Last30Days/*-raw-v3-q{1,2,3}-0905.md`.

## Result in one line

One instrument in the folder is being replaced: a **new Government Tenders and Procurement Law** (Royal Decree M/76 of 27/2/1448H) was published in the Official Gazette on 2026-09-05 and enters into force on 2027-01-03; the 2019 law in `government-tenders-procurement-law.md` stays in force until then. No other instrument in the folder changed on the portal between 2026-09-04 and 2026-09-05.

## Query 1: `Saudi Arabia Labor Law amendments 2026 HRSD ministerial decisions end-of-service Nitaqat Saudization Qiwa`
### Leads
| # | Lead (one line) | Instrument / authority it concerns | Source type and URL | Confirm at |
|---|---|---|---|---|
| 1.1 | Ministry of Interior weekly enforcement statistics (14,905 deportations, 14,434 arrests 20–26 Aug 2026 for residency, labor and border violations); enforcement-intensity signal, no instrument | Labor Law / residency enforcement | x: https://x.com/tvsaab/status/2096146596786282960 ; https://x.com/Tekie4Yonas/status/2095991585875845530 | moi.gov.sa / spa.gov.sa (not needed for the files) |
| 1.2 | Bangladeshi workers' wage protest in Riyadh (4 Sept 2026), single video post; wage-protection enforcement signal, no instrument | Labor Law wages; Wage Protection System | x: https://x.com/alf84728/status/2095989214672458238 | n/a |
| 1.3 | Web supplements repeat the pre-window items already logged on 2026-09-04 (penalties schedule 25 Feb 2026; Nitaqat 2026–2028 phase 26 Apr 2026; Qiwa-documented contracts counted from 15 Apr 2026; new-establishment visa quotas 26 Aug 2026). No first-party HRSD post in the window announced an amendment to the Labor Law or its regulations | Labor Law; Nitaqat; Qiwa | web: https://me.peoplemattersglobal.com/news/strategic-hr/saudi-arabias-hr-ministry-tightens-labour-laws-48588 ; https://www.middleeastbriefing.com/news/saudi-arabias-nitaqat-2026-update-latest-quotas-by-sector-and-what-foreign-employers-need-to-comply-now/ ; https://www.visasupdate.com/post/saudi-arabia-work-visa-quotas-revised-2026 | hrsd.gov.sa news; laws.boe.gov.sa (checked, see below) |
| 1.4 | End-of-service commentary sites restate Arts. 84–85 and the settlement timelines (one week on employer termination, two on resignation); no change claimed | Labor Law Arts. 84–85, 88 | web: https://hlbhamt.com/insights/ksa-end-of-service-gratuity-in-2026/ ; https://ensaantech.com/blog/saudi-labor-law/ | n/a (matches the file) |

### Engine summary (verbatim from the skill)
```
✅ All agents reported back!
├─ 🟠 Reddit: 6 threads │ 157 upvotes │ 35 comments │ ⚠ partial after 6 items: HTTP 429: Too Many Requests (run doctor for fixes)
├─ 🔵 X: 66 posts │ 2,777 likes │ 883 reposts
├─ 🟡 HN: 10 storys │ 64 points │ 5 comments
├─ 🐙 GitHub: 12 items │ 21 reactions │ 60 comments
├─ ⛏️ Digg: 32 clusters │ 181 posts │ 122 authors
├─ 🗣️ Top voices: @alf84728, @JsNungari, @TheDebriefing17 │ r/expats, r/saudiarabia, r/Riyadh
└─ 📎 Raw results saved to ~/Documents/Last30Days/saudi-arabia-labor-law-amendments-2026-hrsd-ministerial-decisions-end-of-service-nitaqat-saudization-qiwa-raw-v3-q1-0905.md
```

## Query 2: `Saudi Arabia Companies Law Ministry of Commerce Commercial Register Investment Law MISA ultimate beneficial ownership Tasattur 2026`
### Leads
| # | Lead (one line) | Instrument / authority it concerns | Source type and URL | Confirm at |
|---|---|---|---|---|
| 2.1 | **New Government Tenders and Procurement Law**: Council of Ministers approval 4 Aug 2026 (Ministry of Finance statement dated 5 Aug 2026); 101 articles; direct-purchase ceiling raised from SAR 100,000 to SAR 1 million; bid-opening and evaluation committees merged; limited tendering opened to liberal-profession practitioners; private-sector dues must be settled before new commitments; in force 120 days after gazette publication | Government Tenders and Procurement Law (replaces M/128 of 1440H) | x (news, @ArgaamPlus): https://x.com/ArgaamPlus/status/2096171092519874777 ; web: https://www.mof.gov.sa/en/MediaCenter/news/Pages/News_05082026.aspx ; https://www.gtlaw.com/en/insights/2026/8/the-kingdom-of-saudi-arabia-approves-new-government-tenders-and-procurement-law ; https://www.alweeam.com.sa/1293631/2026/ | **CONFIRMED** on mof.gov.sa and uqn.gov.sa; see below |
| 2.2 | Ministry of Commerce FAQ post (3 Sept 2026): must micro and small companies exempt from appointing an auditor still prepare and file financial statements (same as lead 2.1 of 2026-09-04) | Companies Law financial statements; MoC | x (first-party, @MCgovSA): https://x.com/MCgovSA/status/2095421358221955533 | mc.gov.sa FAQ; Companies Law portal page (unchanged, see below) |
| 2.3 | Web claims of an "April 2026" round of Companies Law amendments (UBO disclosure, related-party approvals, unified commercial register) repeat the low-reliability 2026-09-04 lead 2.3; the portal shows zero amended articles on the Companies Law and the Commercial Register Law | Companies Law; Commercial Register Law | web: https://globaladvisoryexperts.com/companies-law-saudi-arabia/ ; https://globallawexperts.com/new-saudi-companies-law-2026/ | laws.boe.gov.sa (checked: no amendment) |
| 2.4 | UBO Rules: MoC Decision 267 of 26 Nov 2025, effective 4 Jan 2026 (same as 2026-09-04 lead 2.4; still the operative instrument per law-firm notes; decision number 99 vs 267 remains open in `docs/open-questions-ksa-2026-09-04.md`) | UBO Rules; MoC | web: https://www.bclplaw.com/en-US/events-insights-news/saudi-arabia-new-ultimate-beneficial-owner-ubo-rules-issued.html ; https://www.clydeco.com/en/insights/2026/01/saudi-arabia-s-new-beneficial-owner-rules ; https://mc.gov.sa/en/mediacenter/News/Pages/09-12-25-01.aspx | mc.gov.sa UBO page |
| 2.5 | @MISA was the top first-party voice in the window with investment-promotion posts only (LEAP26 MoUs, China dialogue); no Investment Law or regulation change signalled | Investment Law; MISA | x (first-party, @MISA) | misa.gov.sa; portal (checked: no amendment) |

### Engine summary (verbatim from the skill)
```
✅ All agents reported back!
├─ 🟠 Reddit: 8 threads │ 310 upvotes │ 67 comments │ ⚠ partial after 8 items: HTTP 429: Too Many Requests (run doctor for fixes)
├─ 🔵 X: 71 posts │ 660 likes │ 259 reposts
├─ 🟡 HN: 11 storys │ 81 points │ 7 comments
├─ 🦋 Bluesky: 3 posts │ 99 likes │ 66 reposts
├─ 🐙 GitHub: 9 items │ 12 comments
├─ ⛏️ Digg: 14 clusters │ 88 posts │ 47 authors
├─ 📰 Techmeme: 1 headline
├─ 🗣️ Top voices: @MISA, @BlossomAccel, @rajkaria_ │ r/saudiarabia, r/expats, r/Riyadh
└─ 📎 Raw results saved to ~/Documents/Last30Days/saudi-arabia-companies-law-ministry-of-commerce-commercial-register-investment-law-misa-ultimate-beneficial-ownership-tasattur-2026-raw-v3-q2-0905.md
```

## Query 3: `Saudi Arabia Civil Transactions Law Commercial Courts arbitration SCCA PDPL SDAIA enforcement 2026`
### Leads
| # | Lead (one line) | Instrument / authority it concerns | Source type and URL | Confirm at |
|---|---|---|---|---|
| 3.1 | Draft Arbitration Law (consultation 24 Sept 2025) still not enacted; no royal decree found in the window | Arbitration Law M/34 of 1433H | web: https://www.bclplaw.com/en-US/events-insights-news/a-first-look-at-saudi-arabias-new-draft-arbitration-law.html ; https://globalarbitrationreview.com/review/the-middle-eastern-and-african-arbitration-review/2026/article/saudi-arabia-driving-arbitration-reform-modernised-laws-expanding-caselaw-and-rapidly-growing-scca-caseload | laws.boe.gov.sa (checked: Arbitration Law unchanged, 3 amended articles as before) |
| 3.2 | SDAIA PDPL enforcement: 48 decisions announced by mid-January 2026; marketing-consent failures the most penalised; five-day response window on indictment (as claimed); no new decision reported for August 2026 | PDPL; SDAIA | web: https://iapp.org/news/a/saudi-arabia-s-data-protection-authority-steps-up-enforcement ; https://www.clydeco.com/en/insights/2026/03/enforcement-of-the-saudi-pdp-law ; https://www.globalprivacyblog.com/2026/05/active-enforcement-of-saudi-arabia-privacy-regime-implications-for-businesses/ | sdaia.gov.sa; portal (checked: PDPL unchanged, 24 amended articles as before) |
| 3.3 | Minister of Justice met the appeal-court presidents (2 Sept 2026): judicial-quality and data initiatives; no instrument | Judicial administration; MoJ | x (first-party, @MojKsa): https://x.com/MojKsa/status/2095194865885749490 | moj.gov.sa |
| 3.4 | No item in the window evidenced an amendment to the Civil Transactions Law or the Commercial Courts Law; negative finding, confirmed on the portal below | Civil Transactions Law; Commercial Courts Law | n/a | laws.boe.gov.sa (checked) |

### Engine summary (verbatim from the skill)
```
✅ All agents reported back!
├─ 🟠 Reddit: 6 threads │ 330 upvotes │ 131 comments │ ⚠ partial after 6 items: HTTP 429: Too Many Requests (run doctor for fixes)
├─ 🔵 X: 65 posts │ 674 likes │ 207 reposts
├─ 🟡 HN: 10 storys │ 64 points │ 5 comments
├─ 🦋 Bluesky: 3 posts │ 67 likes │ 23 reposts
├─ 🐙 GitHub: 3 items │ 9 comments
├─ ⛏️ Digg: 27 clusters │ 148 posts │ 90 authors
├─ 🗣️ Top voices: @SudaneseEcho, @jezzaica, @RichDog0 │ r/saudiarabia, r/expats, r/Riyadh
└─ 📎 Raw results saved to ~/Documents/Last30Days/saudi-arabia-civil-transactions-law-commercial-courts-arbitration-scca-pdpl-sdaia-enforcement-2026-raw-v3-q3-0905.md
```

## Confirmed on an official source (2026-09-05)

### New Government Tenders and Procurement Law (نظام المنافسات والمشتريات الحكومية 1448هـ)

| Fact | Source and tier | Status |
|---|---|---|
| Council of Ministers approved the new law on 4 Aug 2026; key changes as listed in lead 2.1 (SAR 1 million direct-purchase ceiling; merged committees; liberal professions; private-sector dues) | Ministry of Finance statement, https://www.mof.gov.sa/en/MediaCenter/news/Pages/News_05082026.aspx (authority page, tier 3) | `[authority — Ministry of Finance]` |
| Issuing instrument: Royal Decree No. M/76 of 27/2/1448H | Ministry of Finance knowledge centre: the law is hosted as `نظام المنافسات والمشتريات الحكومية الصادر بالمرسوم الملكي رقم (م 76) وتاريخ 27-2-1448هـ.pdf` under https://www.mof.gov.sa/Knowledgecenter/newGovTendandProcLow/ (44 pages, image-only, no text layer) | `[authority — Ministry of Finance]`; decree number not yet visible on the BOE portal |
| Full Arabic text published in the Official Gazette (Umm Al-Qura), page dated 23 Rabi' al-Awwal 1448H / 5 September 2026 | https://www.uqn.gov.sa/decisions-and-regulations/4001762 (text-extractable) | primary Arabic text; portal entry pending |
| Art. 100: the law replaces the Government Tenders and Procurement Law of Royal Decree M/128 of 13/11/1440H | same UQN page | read 2026-09-05 |
| Art. 101: in force 120 days after publication in the Official Gazette → 2027-01-03 (publication 2026-09-05 + 120 days) | same UQN page | `[computed — Art. 101; inputs: gazette date 2026-09-05, 120 days]` |
| Arts. 98–99: the Council of Ministers' regulations (local-content preference and others) and the Minister's implementing regulation are to be issued within 120 days of publication and apply from the in-force date | same UQN page | read 2026-09-05 |
| Ministry of Finance summary of the changes ("أبرز التعديلات ... 1448هـ"): limited tendering no longer available below SAR 500,000; direct purchase up to SAR 1 million with documented reasons; direct purchase allowed for R&D, liberal professions, software licences and subscriptions; country-of-origin references banned in tenders; new chapter on bidders' enquiries | https://www.mof.gov.sa/Knowledgecenter/newGovTendandProcLow/Pages/Regulation.aspx | `[authority — Ministry of Finance]` |
| BOE portal: the 2019 law (GUID `24c563f9-…`) still shows status ساري with 0 amended articles; a `--search "المنافسات والمشتريات"` returns only the conflict-of-interest and ethics regulations; the other GUID surfaced by search, `c2c05ee1-201a-48de-91e7-a9a700f2d14f`, is the repealed 2006 law (M/58 of 1427H, status لاغي). The 1448H law is not on the portal yet and is not in the updates log | `scripts/fetch-law.py`, 2026-09-05 | recheck the portal before T8 |

**What this means for the files.** `government-tenders-procurement-law.md` keeps its rows: the 2019 law governs every tender and contract until 2027-01-03. The file header now records the replacement (this task). Authoring the 1448H law's rows from the gazette text is a separate session (tracker T8), to be done before 2027-01-03 and after the portal lists the law with its decree number.

### Instruments rechecked on the portal (2026-09-05)

All fetched with `scripts/fetch-law.py --portal boe --id <guid> --lang ar`; status and amended-article count compared with the value recorded in each instrument file's header.

| Instrument | Status | Amended articles | Matches file |
|---|---|---|---|
| Labor Law | ساري | 106 | yes |
| Civil Transactions Law | ساري | 0 | yes |
| Companies Law | ساري | 0 | yes |
| Arbitration Law | ساري | 3 | yes |
| Commercial Courts Law | ساري | 1 | yes |
| Personal Data Protection Law | ساري | 24 | yes |
| Commercial Register Law | ساري | 0 | yes |
| Anti-Concealment Law | ساري | 0 | yes |
| Investment Law | ساري | 0 | yes |
| Competition Law (1440H) | ساري | 0 | yes |
| Social Insurance Law 1445H | ساري | 0 | yes |
| Enforcement Law 1447H | ساري بعد مدة 180 يوم من تاريخ النشر | 0 | yes |
| Commercial Agencies Law | ساري | 3 | yes |
| Government Tenders and Procurement Law (2019) | ساري | 0 | yes (replacement published, not in force) |

**Updates log** (`/boelaws/laws/lawupdated/1`, pages 1 to 3, read 2026-09-05): the newest entry is still the Enforcement Law (issued 1447/11/03H, published 1447/11/14H); the entries and dates on all three pages match the 2026-09-04 read. Nothing new above it.

### HRSD scanned PDFs (for backlog B1)

Re-downloaded 2026-09-05 with percent-encoded URLs. The friendly-settlement rules decision (2024) is still a 10 MB image-only PDF (0 text characters). The Decision 115921 PDF now carries a one-page text layer of 808 characters, but it is glyph-mapped garbage (no readable Arabic), so it still needs OCR. B1 stands.

## Consolidated lead list

1. **New Government Tenders and Procurement Law (M/76 of 27/2/1448H)**: confirmed; gazette 2026-09-05; in force 2027-01-03. Action: header note now (done); full rows in T8.
2. **MoC financial-statement FAQ positions (3 Sept 2026)**: still a lead for `companies-law.md` (auditor-exemption and dormant-company filing duties); obtain the FAQ text from mc.gov.sa.
3. **UBO decision number (99 vs 267)**: unchanged open question.
4. **Nitaqat 2026–2028, Qiwa-documentation condition, penalties schedule**: pre-window, already in the files or in the open-questions list; nothing new.
5. **Draft Arbitration Law**: still a draft; no action.
6. **PDPL enforcement**: no rule change; no action.
7. **Negative findings**: no amendment to the Labor Law, Civil Transactions Law, Companies Law, Commercial Courts Law, Investment Law, PDPL, Commercial Register Law, Anti-Concealment Law, Competition Law, Social Insurance Law, Commercial Agencies Law, or Enforcement Law on the portal as of 2026-09-05.

## Limitations

- Engine coverage as on 2026-09-04: Instagram, TikTok, Threads, LinkedIn, YouTube `HTTP 402: Payment Required`; Polymarket `Connection reset by peer`; Reddit partial after 6 to 8 items (`HTTP 429`); Brave web backend not configured (`BRAVE_API_KEY is required`, query 1 only; dropped for queries 2 and 3); library context `Operation not permitted` on the SQLite file. Ranked clusters were general Saudi news; the on-topic material came from first-party posts and the web supplements.
- The gazette page shows Hijri and Gregorian dates for the issue (23/3/1448H, 5 Sept 2026) but not the decree number in its extracted text; the decree number rests on the Ministry of Finance PDF title until the BOE portal lists the law.
- The 44-page MoF PDF has no text layer; the gazette page is the text source for T8.
- The skill's Step 2.5 (appending supplements to the raw files under `~/Documents/Last30Days/`) was not done, as on 2026-09-04; the supplements are listed in this file instead.
