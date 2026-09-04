# Jurisdiction manifest: ksa

| Field | Value |
|---|---|
| code | `ksa` |
| name | Kingdom of Saudi Arabia (المملكة العربية السعودية) |
| legal_family | Civil-law style codified statutes (أنظمة) applied under Islamic Sharia as the constitutional baseline (Basic Law of Governance, Art. 1, 7, 48); no binding precedent, published judicial principles are persuasive |
| authoritative_language | Arabic. Official English translations are published by the Bureau of Experts "for guidance"; the Arabic text governs |
| source_portal | https://laws.boe.gov.sa (Bureau of Experts at the Council of Ministers, هيئة الخبراء بمجلس الوزراء) |
| issuing_authorities | HRSD (hrsd.gov.sa), Ministry of Commerce (mc.gov.sa), Ministry of Investment (misa.gov.sa), ZATCA (zatca.gov.sa), Capital Market Authority (cma.gov.sa), GOSI (gosi.gov.sa), SDAIA (sdaia.gov.sa), Ministry of Justice (moj.gov.sa), General Authority for Competition (gac.gov.sa), Qiwa (qiwa.sa), SCCA (sadr.org) |
| calendar | Official dates are Hijri (Umm al-Qura); Gregorian equivalents are shown on the portal. Weekend is Friday and Saturday. Public holidays: Eid al-Fitr, Eid al-Adha, National Day (23 September), Founding Day (22 February) |
| currency | SAR (Saudi riyal) |
| populated | **yes** |
| last_reviewed | 2026-09-04 |
| research_tool | `python3 scripts/fetch-law.py --portal boe --id <law-guid> --lang ar` (see `SOURCES.md` for GUIDs); the Claude Code web-fetch tool rejects the portal's TLS chain, `curl` on macOS accepts it |
| provenance_tags | `[BOE — Arabic]` text read from laws.boe.gov.sa Arabic page; `[BOE — official English]` read from the Bureau of Experts translation; `[authority — <name>]` read from the issuing authority's site; `[model knowledge — verify]` everything else |
| output_language_rule | English plus Arabic rendering of the bottom line, findings table, and any counterparty-facing text; Arabic legal terms follow the Bureau of Experts glossary spellings used in its official translations |
| disclaimer | Arabic text is authoritative; English translations are for convenience; a licensed Saudi lawyer must review before reliance. (النص العربي هو النص المعتمد، والترجمة الإنجليزية للاستئناس فقط، ويجب مراجعة محامٍ سعودي مرخص قبل الاعتماد على هذا المستند.) |

See `INDEX.md` for the instrument files and `SOURCES.md` for the source hierarchy and every URL read.
