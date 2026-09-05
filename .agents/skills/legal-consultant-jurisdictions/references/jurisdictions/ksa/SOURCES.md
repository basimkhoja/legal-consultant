# Sources: ksa

## Source hierarchy

Every rule in this folder cites one of these tiers, highest first. A lower tier may guide research but is never the cited source for a rule tagged settled.

1. **Bureau of Experts Arabic text** (هيئة الخبراء بمجلس الوزراء), https://laws.boe.gov.sa. The consolidated Arabic text of every law (نظام) and Council-of-Ministers-level regulation, with amended and repealed articles marked. Tag: `[BOE — Arabic]`.
2. **Bureau of Experts official English translation**, published on the same portal as a "Translated document" PDF. Provided "for guidance"; the Arabic governs. Tag: `[BOE — official English]`.
3. **Issuing ministry or authority page**: HRSD (implementing regulations of the Labor Law, Nitaqat, friendly settlement rules), Ministry of Commerce (Companies Law implementing regulations, UBO rules, Qawaem), Ministry of Investment (Investment Law and regulations), ZATCA, Capital Market Authority (corporate governance regulations, listed-company regulations), GOSI, SDAIA (PDPL implementing regulation and transfer regulation), Ministry of Justice (Commercial Courts implementing regulations), General Authority for Competition (concentration guidelines), SCCA (arbitration rules). Tag: `[authority — <name>]`.
4. **Law-firm commentary and practitioner discussion**: lead generation only (see `docs/amendment-watch-<date>.md`). Never cited. Anything taken from this tier is written as `[model knowledge — verify]`.

## How the texts were retrieved

- Portal pages were fetched with `python3 scripts/fetch-law.py --portal boe --id <guid> --lang ar` on 2026-09-04. The script uses `curl`; the macOS trust store accepts the portal's TLS chain, which some HTTP libraries reject.
- Official translations were downloaded from the "Translated document" attachment on each portal page (`--attachments`) and converted with `pdftotext`.
- Authority documents were downloaded from the URLs below and converted with `pdftotext`. Two documents are scanned images with no usable text layer: the HRSD friendly-settlement rules decision (2024) and HRSD Ministerial Decision 115921 (the adoption decision for the 2025 implementing regulations; the regulations themselves were read from the April 2025 consolidated PDF). On 2026-09-05 both were re-downloaded (`curl -A "Mozilla/5.0"`, percent-encoded URLs), rendered at 300 dpi with `pdftoppm -r 300 -png`, and OCR'd with tesseract 5.5.3 and the `ara` language pack (`--psm 6`, with `--psm 4` and per-line crops for the few lines the first pass dropped). The Arabic model garbles Arabic-Indic numerals and the Latin-digit header stamps, so every number quoted from them (decision numbers, Hijri dates, the 21-day figure, the Art. 9(3) reference) was read from the 300-dpi page image. The OCR text is kept outside the repository.

## Post-cutoff amendment check (2026-09-04)

The portal's "recent updates" log (`/boelaws/laws/lawupdated/1`, pages 1-3) was read on 2026-09-04. Entries relevant to this folder:

| Entry | Issued | Published | Finding |
|---|---|---|---|
| نظام التنفيذ (Enforcement Law) | 1447/11/03H (2026-04-20) | 1447/11/14H (2026-05-01) | New law, Royal Decree M/237, in force 180 days after publication (2026-10-28). Added as `enforcement-law.md`. |
| نظام الشركات (Companies Law) | 1443/12/01H | 1443/12/23H | Appears in the updates log; a first reading attached the adjacent entry's 1447/03/12H date to it. On re-reading, the dates that follow the Companies Law entry are its own 1443H issue and publication dates, the law page shows status "ساري", zero articles marked amended, and only Royal Decree M/132 and Council of Ministers Resolution 678 named. No amendment found. |
| Labor Law | — | — | yes (portal attachment, read 2026-09-04) |
| PDPL | — | — | Portal marks 24 articles as amended (Royal Decree M/148 of 5/9/1444H). Consolidated text read. |

## Post-cutoff amendment check (2026-09-05, pre-release rerun; `docs/amendment-watch-2026-09-05.md`)

Updates log pages 1 to 3 re-read: newest entry still the Enforcement Law; no new entry since 2026-09-04. Fourteen instruments re-fetched with `scripts/fetch-law.py`; every status line and amended-article count matched the value in the instrument file header (Labor 106, PDPL 24, Arbitration 3, Commercial Agencies 3, Commercial Courts 1, all others 0; Enforcement Law "ساري بعد مدة 180 يوم من تاريخ النشر").

| Entry | Issued | Published | Finding |
|---|---|---|---|
| نظام المنافسات والمشتريات الحكومية 1448هـ (new Government Tenders and Procurement Law) | Royal Decree M/76, 27/2/1448H (decree number from the Ministry of Finance's hosted PDF title; not visible on the gazette page) | Official Gazette (Umm Al-Qura) issue of Friday 22/3/1448H (2026-09-04; the page is dated 1448-3-22 / 04-09-2026 and its metadata carries `datePublished 2026-09-04T15:00+03:00`; the 23/3/1448H recorded on 2026-09-05 was the read date), https://www.uqn.gov.sa/decisions-and-regulations/4001762 | Replaces the 2019 law (its Art. 100); in force 120 days after publication (Art. 101): 2027-01-02 on the day-count convention used for the 2019 law, or 2027-01-03 if the 120th day is excluded; the file treats 2027-01-02 as `[review]`. **T8 done 2026-09-05:** all 101 articles read from the gazette page and written into `government-tenders-procurement-law.md` as the in-force set, tagged `[settled — last confirmed 2026-09-05]` `[authority — Umm Al-Qura gazette]`; the 2019 rows kept as the repealed set for matters before the in-force date. Still not on the BOE portal on 2026-09-05 (title search, `--search "المشتريات"` and the full `--index` return only the 2019 law, the repealed 2006 law, GUID `c2c05ee1-201a-48de-91e7-a9a700f2d14f`, and four related regulations), so the portal read is pending: when listed, fetch with `--lang ar`, confirm the status line and decree, add the GUID below and re-tag the 1448H rows `[BOE — Arabic]`. Implementing regulations under Arts. 98–99 (due by 2027-01-02): not issued as of 2026-09-05; the Ministry of Finance knowledge centre lists only the law PDF (image-only), a summary of changes, an FAQ and one further PDF, and Etimad exposes nothing without a login. |
| HRSD Ministerial Decision 91285 of 20/6/1445H (friendly-settlement rules) and Ministerial Decision 115921 of 19/8/1446H (adoption of the 2025 Regulations) | 20/6/1445H; 19/8/1446H | HRSD website (2024-01 and 2025-02 uploads) | 2026-09-05 (B1): both PDFs re-downloaded from the HRSD URLs in the authority table (10.26 MB, 7 pages; 252 KB, 1 page) and OCR'd with tesseract 5.5.3 (Arabic pack). No later version of either document is posted on the HRSD pages. Decision 91285: 27 articles read; the rows in `labor-dispute-route.md` are settled from the text (pre-suit settlement at the labor office of the workplace, first session within 10 working days, 21 working days from the first session, record of failure then a statement of claim at the labor court, ratified settlement record an executive instrument under Enforcement Law Art. 9(3)). Decision 115921: approval wording and the commencement clause (in force from 20 Sha'ban 1446H, the M/44 commencement date) read; Instrument table of `labor-law-implementing-regulations.md` settled. |
| All other instruments in the GUID table | — | — | No change on the portal between 2026-09-04 and 2026-09-05. |

The Official Gazette (جريدة أم القرى, https://www.uqn.gov.sa) is the publication of record and is used, tagged `[authority — Umm Al-Qura gazette]`, only for an instrument the BOE portal does not list yet; once the portal lists it, the portal text is re-read and the rows re-tagged.

## Instruments read from laws.boe.gov.sa

The portal lists repealed laws alongside current ones under similar titles. Every GUID below was checked for the status line `الحالة: ساري` (in force) on 2026-09-04; the 1425H Competition Law (status `لاغي`, repealed) was fetched first by mistake and replaced by the 1440H law. `scripts/fetch-law.py` now prints the status line in the file header so this is visible.

| Instrument | Portal GUID | Arabic page read | English translation |
|---|---|---|---|
| Labor Law (نظام العمل) | `08381293-6388-48e2-8ad2-a9a700f2aa94` | 2026-09-04 | yes (portal attachment, read 2026-09-04) |
| Civil Transactions Law (نظام المعاملات المدنية) | `655fdb42-8c96-422b-b8c4-b04f0095c94c` | 2026-09-04 | none on the portal as of 2026-09-04 |
| Companies Law (نظام الشركات) | `a8376aea-1bc3-49d4-9027-aed900b555af` | 2026-09-04 | yes (portal attachment, read 2026-09-04) |
| Arbitration Law (نظام التحكيم) | `5535039e-13da-43f6-8f53-a9a700f26485` | 2026-09-04 | yes (portal attachment, read 2026-09-04) |
| Arbitration Law Implementing Regulations | `12752a60-2a4a-4cab-a05d-a9a700f274a5` | 2026-09-04 | yes (portal attachment, read 2026-09-04) |
| Commercial Courts Law (نظام المحاكم التجارية) | `38334008-3b70-4c6c-b3af-aba3016a8061` | 2026-09-04 | yes (portal attachment, read 2026-09-04) |
| Bankruptcy Law (نظام الإفلاس) | `68204119-84f1-4789-8fad-a9ec014c3788` | 2026-09-04 | yes (portal attachment, read 2026-09-04) |
| Bankruptcy Law Implementing Regulations | `a748e485-620c-45c4-8ca8-a9f40166406d` | 2026-09-04 | none on the portal as of 2026-09-04 |
| Personal Data Protection Law (نظام حماية البيانات الشخصية) | `b7cfae89-828e-4994-b167-adaa00e37188` | 2026-09-04 | none on the portal as of 2026-09-04 |
| E-Commerce Law (نظام التجارة الإلكترونية) | `360de590-0286-4fa5-a243-aa9100c31979` | 2026-09-04 | yes (portal attachment, read 2026-09-04) |
| Electronic Transactions Law (نظام التعاملات الإلكترونية) | `6f509360-2c39-4358-ae2a-a9a700f2ed16` | 2026-09-04 | yes (portal attachment, read 2026-09-04) |
| Commercial Register Law (نظام السجل التجاري) | `98ee4b51-d398-4323-ae69-b2b8009f3156` | 2026-09-04 | none on the portal as of 2026-09-04 |
| Trade Names Law (نظام الأسماء التجارية) | `d4801a45-7f76-4414-bdca-b20900db6fc4` | 2026-09-04 | none on the portal as of 2026-09-04 |
| Anti-Concealment Law (نظام مكافحة التستر) | `bf9e0aae-6df6-4785-a305-ac2300bd0856` | 2026-09-04 | yes (portal attachment, read 2026-09-04) |
| Government Tenders and Procurement Law (نظام المنافسات والمشتريات الحكومية), 2019 law M/128 of 1440H (repealed from the 1448H law's in-force date; still the only version on the portal as of 2026-09-05) | `24c563f9-7292-49c8-b0fb-aa9800b999f1` | 2026-09-04 (re-read 2026-09-05, unchanged) | none on the portal as of 2026-09-04 |
| Investment Law (نظام الاستثمار) | `eda86cc3-3a00-4b90-900d-b1d000c8a863` | 2026-09-04 | none on the portal as of 2026-09-04 |
| Commercial Agencies Law (نظام الوكالات التجارية) | `b19a8aa6-7b50-43f0-ab8c-a9a700f1a446` | 2026-09-04 | yes (portal attachment, read 2026-09-04) |
| Competition Law (نظام المنافسة), Royal Decree M/75 of 1440H | `e3605c0d-ef87-4cff-b5da-aa3f0102bbb4` | 2026-09-04 | none on the portal as of 2026-09-04 (the translation attached to the repealed 1425H law, GUID `6b615a05-…`, was downloaded first by mistake and is not used) |
| Social Insurance Law 1445H (نظام التأمينات الاجتماعية) | `eaee8a20-3a54-4aaf-b0d9-b1ad00998962` | 2026-09-04 | none on the portal as of 2026-09-04 |
| Social Insurance Law 1421H (نظام التأمينات الاجتماعية 1421هـ) | `8ff3cd90-e466-4bf9-a071-a9a700f2a70d` | 2026-09-04 | none on the portal as of 2026-09-04 |
| Enforcement Law 1447H (نظام التنفيذ) | `67dd54bc-c33a-48c8-8356-b44700a9ab55` | 2026-09-04 | yes (portal attachment, read 2026-09-04) |

Portal URL pattern: `https://laws.boe.gov.sa/BoeLaws/Laws/LawDetails/<GUID>/1` (Arabic) and `/2` (English page; the translation itself is the PDF attachment).

## Authority documents read

| Document | Authority | URL | Read |
|---|---|---|---|
| Implementing Regulations of the Labor Law and annexes, April 2025 consolidated edition (Arabic) | HRSD | https://www.hrsd.gov.sa/sites/default/files/2025-04/اللائحة التنفيذية لنظام العمل وملحقاتها.pdf | 2026-09-04 |
| Implementing Regulations of the Labor Law and annexes, 2023 English translation (pre-amendment) | HRSD | https://www.hrsd.gov.sa/sites/default/files/2023-02/The Implementing Regulations of Labor Law and its Annexes.pdf | 2026-09-04 |
| Ministerial Decision 115921 of 19/8/1446H adopting the regulations (scanned; 252 KB) | HRSD | https://www.hrsd.gov.sa/sites/default/files/2025-02/قرار اعتماد اللائحة التنفيذية لنظام العمل وملحقاتها رقم 115921.pdf | 2026-09-05 (OCR, tesseract 5, Arabic pack; 1 page, fully legible; numerals and the header stamp read from the page image) |
| Nitaqat Mutawar procedural guideline v2.0 (English, 2021) | HRSD | https://www.hrsd.gov.sa/sites/default/files/2023-06/E20210523.pdf | 2026-09-04 |
| Rules and procedures for friendly settlement of labor disputes, Ministerial Decision 91285 of 20/6/1445H (2024, scanned; 10.26 MB) | HRSD | https://www.hrsd.gov.sa/sites/default/files/2024-01/قرار اعتماد القواعد والإجراءات المنظمة للتسوية الودية في الخلافات العمالية.pdf | 2026-09-05 (OCR, tesseract 5, Arabic pack; 7 pages, six of text and one blank, 27 articles, fully legible; four lines recovered from per-line crops; numerals read from the page image) |
| Implementing Regulations of the Companies Law 1444H/2023 (Arabic) | Ministry of Commerce | https://mc.gov.sa/ar/Documents/R.pdf | 2026-09-04 |
| Ultimate Beneficial Owner guidance document (Arabic) | Ministry of Commerce | https://mc.gov.sa/ar/guides/Documents/BOG.pdf | 2026-09-04 |
| Companies Law official English translation (Bureau of Experts, MISA-hosted) | MISA | https://misa.gov.sa/app/uploads/2025/07/Companies-Law.pdf | yes (portal attachment, read 2026-09-04) |
| Investment Law official English translation | MISA | https://misa.gov.sa/app/uploads/2025/07/Investment-Law.pdf | none on the portal as of 2026-09-04 |
| Implementing Regulations of the Investment Law (English) | MISA | https://misa.gov.sa/app/uploads/2025/06/THE-INVESTMENT-LAW-IMPLEMENTING-REGULATIONS.pdf | 2026-09-04 |
| Corporate Governance Regulations (English, as amended) | CMA | https://cma.gov.sa/en/RulesRegulations/Regulations/Documents/CorporateGovernanceRegulations1.pdf | 2026-09-04 |
| Implementing Regulation of the Companies Law for Listed Joint Stock Companies, 2026 edition (English) | CMA | https://cma.gov.sa/en/RulesRegulations/Regulations/Documents/Implementing_Regulation_of_the_Companies_Law_for_Listed_Joint_Stock_Companies_en2026.pdf | 2026-09-04 |
| Economic Concentration Review Guidelines v5, April 2025 (English) | GAC | https://gacbep.gac.gov.sa/cms/b9376edc-79a1-4573-a36d-4f3effaba838.pdf | 2026-09-04 |
| Implementing Regulation of the PDPL (English) | SDAIA | https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf | 2026-09-04 |
| Guide to the PDPL for controllers and processors (English, secondary) | SDAIA | https://dgp.sdaia.gov.sa/ (ENG-Guide to the saudi PDP law for controllers/processors) | 2026-09-04 |
| Commercial Courts Law implementing regulations (Arabic, file labelled مشروع) | Ministry of Justice | https://www.moj.gov.sa/Documents/ProjectExecution.pdf | yes (portal attachment, read 2026-09-04) |
| SCCA Arbitration Rules 2023 (English) | SCCA | https://www.sadr.org/public/upload/pdf-files/2023-Arbitration-Rules-En.pdf | 2026-09-04 |

## Not read (model knowledge only, flagged in the files that use them)

- GOSI contribution-rate schedule and the transitional retirement-age table (gosi.gov.sa pages are JavaScript-rendered).
- ZATCA filing deadlines and VAT thresholds (zatca.gov.sa; law text not on the BOE portal in a form the fetcher reads).
- Qiwa, Mudad, and Musaned platform rules (platform terms, not published as instruments).
- Commercial Agencies Law implementing regulations (Ministry of Commerce; not located as a PDF).
- (Closed 2026-09-05, backlog B1.) The HRSD friendly-settlement rules 2024 and Ministerial Decision 115921 were scanned PDFs; both were OCR'd on 2026-09-05 and are now read in full (rows in `labor-dispute-route.md` and `labor-law-implementing-regulations.md`). The Ministry of Justice filing procedures they refer to, and the Official Gazette issues in which they were published, remain unread.
- The Implementing Regulations, Preference Regulation and R&D, conflict-of-interest and ethics regulations of the 1448H Government Tenders and Procurement Law (Arts. 98–99; due within 120 days of the 2026-09-04 gazette publication): not issued as of 2026-09-05 (Ministry of Finance knowledge centre and Etimad checked). The 1448H law itself was read in full from the gazette page on 2026-09-05 (tracker T8); the Implementing Regulations of the repealed 2019 law were never read.
