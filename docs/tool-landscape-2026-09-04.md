# Tool Landscape Research (last30days)

Generated via the `/last30days` skill (engine v3.18.4), synced 2026-09-04. Two queries were run through the full engine + WebSearch-supplement protocol. Note on limitations: the sandboxed environment returned `Operation not permitted` when trying to list/append to files under `~/Documents/Last30Days` (the skill's raw-file save directory), so Step 2.5 (appending WebSearch supplements to the saved raw `.md` files) could not be completed — the engine itself successfully wrote the raw files (per its own log lines, permissions inside the engine's own process differ from this later shell access attempt), but this session could not read them back or append to them. That is recorded here rather than improvised around.

---

## Query 1 (verbatim last30days output)

**Query run:** `AI legal assistant plugins and skills for Claude Code, Codex CLI, Gemini CLI — contract review, employment law, corporate diligence (alternatives to Anthropic claude-for-legal)`

🌐 last30days v3.18.4 · synced 2026-09-04

What I learned:

**Anthropic's own claude-for-legal is the clear center of gravity, and it isn't a single plugin — it's a suite.** The official `anthropics/claude-for-legal` GitHub repo (9.4K stars, 69 open issues) ships reference agents, skills, and data connectors across commercial, corporate, privacy, product, employment, litigation, regulatory, AI-governance, and IP practice areas — the "alternatives" landscape is really a set of narrower single-purpose skills competing with pieces of that suite, not a rival full platform.

**The most credible non-Anthropic alternative is evolsb/claude-legal-skill, precisely because it's cross-tool by design.** It's a CUAD-risk-detection contract review skill (built on CUAD's 41 risk categories, ContractEval, and LegalBench) that explicitly targets Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI, and "26+ tools" — it reviews NDAs, employment agreements, SaaS terms, and M&A documents, flags governing-law issues (e.g. non-competes void in CA/ND/OK/MN), and is positioned for first-pass review, not a replacement for attorney sign-off.

**A second cluster of GitHub-native competitors targets the same Claude Code skill format specifically.** zubair-trabzada/ai-legal-claude (1.7K stars, 6 open issues) bundles 14 skills and 5 parallel agents for contract review, risk analysis, NDA generation, compliance auditing, negotiation strategy, and PDF reports. borghei's "legal-skills" plugin adds 17 skills (contract review, NDA, privacy, DPIA, breach response, risk assessment, vendor due diligence). rohasnagpal/legal-ai-skills ships a "Marco" contract-reviewer skill that risk-scores pasted contracts and gives a negotiation priority list, and — like the others — is tool-agnostic (works in Claude, ChatGPT, and Gemini as a plain markdown system prompt).

**Directory sites are starting to aggregate this fragmented ecosystem rather than build their own tools.** HAQQ Academy curates 300+ (elsewhere cited as 338 or "160+") legal AI skills for Claude, ChatGPT, and Gemini sourced from Anthropic, OpenAI, Lawvable, Skala, and the community — split by practice area (Litigation 19, Employment 18, AI Governance 12, Corporate 10, Contract 8, etc.) — signaling that discovery/curation, not a single dominant tool, is the current bottleneck.

**The community's skepticism is aimed at reliability, not at the concept.** On Bluesky, [@hillcat98.bsky.social](https://bsky.app/profile/hillcat98.bsky.social/post/3muirrnb3uc22) wrote: "yeah a very notable feature of the AI bros is that they legitimately do not understand what middle management, accountants, lawyers, etc actually *do.* the dead giveaway is that they'll talk about how AI will replace lawyers and then go describe the job of an intern or a legal assistant." A Digg-surfaced story the same window ("AI-Generated Legal Memo Reaches Wrong Conclusion") reinforces the theme — a law expert flagged an AI-assisted memo that reached an incorrect regulatory conclusion, which is the exact failure class every one of these skills claims to mitigate with human-review gates.

KEY PATTERNS from the research:
1. The "alternatives to claude-for-legal" space is mostly single-purpose contract-review skills, not full practice-area suites — per [evolsb/claude-legal-skill](https://github.com/evolsb/claude-legal-skill)
2. Cross-tool compatibility (Claude Code + Codex + Cursor + Gemini CLI, often via a plain markdown skill file) is the differentiator third-party tools lead with, since none can match Anthropic's native distribution — per [r/legaltech](https://www.reddit.com/r/legaltech/comments/1w4jglp/ai_tools_for_law/)
3. Trust/hallucination risk is the recurring criticism across every source, not tool-specific complaints — per [@hillcat98.bsky.social](https://bsky.app/profile/hillcat98.bsky.social/post/3muirrnb3uc22)
4. Skill-directory aggregators (HAQQ Academy, claudeskills.info, awesomeskill.ai) are emerging faster than any single alternative tool is gaining traction — per HAQQ Academy

---
✅ All agents reported back!
├─ 🟠 Reddit: 14 threads │ 8,348 upvotes │ 869 comments │ ⚠ partial after 14 items: Reddit backup failed after 0 public items: HTTP 402: Payment Required (run doctor for fixes)
├─ 🔵 X: 19 posts │ 1,386 likes │ 420 reposts
├─ 🟡 HN: 35 storys │ 8,378 points │ 6,386 comments
├─ 🦋 Bluesky: 6 posts │ 62 likes │ 33 reposts
├─ 🐙 GitHub: 2 items │ 11,079 stars │ 75 comments
├─ ⛏️ Digg: 14 clusters │ 66 posts │ 38 authors
├─ 🗣️ Top voices: @alexgroberman, @BestOfAllTylers, @AlexRiad84837 │ r/legaltech, r/LawFirm, r/ClaudeAI
└─ 📎 Raw results saved to ~/Documents/Last30Days/ai-legal-assistant-plugins-and-skills-for-claude-code-codex-cli-gemini-cli-contract-review-employment-law-corporate-diligence-alternatives-to-claude-for-legal-raw-q1.md
---

I have all the links to the 14 Reddit threads, 19 X posts, 35 HN stories, 6 Bluesky posts, 2 GitHub repos, and 14 Digg clusters I pulled from. Just ask.

**Engine warnings on this run (relayed honestly):** TikTok, Instagram, Threads, and LinkedIn all failed with `HTTP 402 Payment Required` (ScrapeCreators credits not available in this environment); Polymarket failed with repeated connection resets; Reddit's ScrapeCreators backfill also 402'd, so Reddit coverage came from the free keyless path only. YouTube returned videos but no usable transcripts (yt-dlp and SC transcript fetch both failed/timed out for all 4 candidate videos). None of this should be read as "no discussion exists" on those platforms — it means those sources weren't actually searched successfully this run.

---

## Query 2 (verbatim last30days output)

**Query run:** `last30days Saudi Arabia legal AI tools and legal research platforms (Arabic law, Bureau of Experts, Nazaha, Lexis Middle East, Westlaw Gulf)`

🌐 last30days v3.18.4 · synced 2026-09-04

What I learned:

**The social-listening engine came back thin and largely off-topic for this specific query, so this section leans on the WebSearch supplements rather than the social evidence clusters.** The 73 items the engine surfaced (Reddit, X, HN, Bluesky, GitHub, Digg) were dominated by adjacent-but-different stories — Saudi's HUMAIN/PIF sovereign AI infrastructure deals (a $5B chip deal with Together Compute, a Mistral partnership), a UK VAT-registration complaint from an unrelated AI startup, an Odoo GitHub PR about Saudi ZATCA invoicing thresholds, and a joke thread about a hypothetical furry convention — none of which describe legal-AI tools or legal-research platforms in active use. Given the GENERAL nothing-solid floor, that evidence is treated as absent for this specific ask rather than forced into the narrative.

**Arabic-native consumer legal-AI apps are the most concrete and traction-proven part of the landscape.** Per HAQQ's research, at least seven Arabic-native legal-AI products already serve Saudi users, making it "the deepest consumer legal-AI cluster in MENA." Adel is the most traction-proven: 663 App Store ratings (4.6 stars), a claimed 500K downloads, 70,000+ indexed Saudi legal documents, and published pricing (SAR 149-199/month). Shwra has the widest distribution (iOS, Android, Huawei, ~1,400 ratings) and is a hybrid model — an AI assistant called "Mishir" triages the question and routes to a licensed human lawyer. Qaanoon and Malakah were also named as Saudi-specific, Arabic-first entrants.

**The state legal-infrastructure layer (Bureau of Experts, Nazaha) is regulatory/institutional, not an AI product itself.** The Bureau of Experts at the Council of Ministers (established 1953) is Saudi Arabia's law-drafting and amendment authority and runs a searchable English-translation database of Saudi Basic Laws — it is the canonical source-of-truth that any legal-AI or legal-research tool covering Saudi law needs to ingest, not a competing AI platform. Nazaha (the Oversight and Anti-Corruption Authority) got sweeping new powers under a November 2024 law requiring officials to prove the legitimacy of unexplained wealth — relevant as a compliance/diligence data source (unexplained-wealth and anti-corruption checks) rather than as a legal-AI vendor. SDAIA (Saudi Data & AI Authority) is the actual national AI policy body; a draft "AI Hub Law" was under public consultation as of April 2025 and had not been enacted as of the most recent web results.

**On the enterprise/multi-jurisdiction side, LexisNexis has built a Middle East-localized product, while Westlaw's Gulf presence is narrower and less documented.** Lexis Middle East runs on Lexis+ with "Protégé" AI, with curated content across the UAE, Saudi Arabia, Qatar, Kuwait, Bahrain, and Oman, plus 1,700+ GCC-specific Practice Notes from Gulf Legal Advisor. Westlaw's AI layer (Westlaw Edge, AI-Assisted Research, GenAI summaries) was named as relevant to Gulf practice in general legal-tech coverage, but no source in this pass named a distinct "Westlaw Gulf" product or found direct community commentary on it — treat "Westlaw Gulf" as Westlaw Edge used regionally rather than a confirmed standalone offering.

**Independent industry lists converge on a mixed roster of global tools being used by Saudi legal professionals, not Saudi-built ones.** Nucamp's "Top 10 AI Tools Every Legal Professional in Saudi Arabia Should Know" names Casetext CoCounsel, ChatGPT, Claude, Westlaw Edge, Lexis+, RelativityOne, Everlaw, Spellbook, "ChronoVault 2.0 + NeXa," and Smith.ai — citing Thomson Reuters' estimate of ~240 hours saved per lawyer/year and 31% personal / 21% firm-level adoption in 2024, alongside recurring PDPL (Saudi's data-protection law) and accuracy concerns.

KEY PATTERNS from the research:
1. Arabic-native legal AI (Adel, Shwra, Qaanoon, Malakah) is a distinct, more mature layer from the global enterprise tools (Lexis, Westlaw) — they solve different problems (consumer-facing legal Q&A vs. professional research) — per HAQQ's MENA legal-AI coverage
2. Bureau of Experts and Nazaha are institutional/regulatory data sources a legal-AI tool must integrate, not AI vendors themselves
3. No source in this pass surfaced a standalone "Westlaw Gulf" brand distinct from Westlaw Edge used regionally — worth verifying directly with Thomson Reuters if this matters for a specific decision
4. Live social discussion specific to "Saudi legal AI tools" was essentially absent this window; what surfaced instead was sovereign AI-infrastructure news (HUMAIN/PIF), suggesting the Saudi AI conversation online right now skews toward compute/infrastructure deals rather than legal-tech product chatter

---
✅ All agents reported back!
├─ 🟠 Reddit: 12 threads │ 422 upvotes │ 479 comments │ ⚠ partial after 12 items: HTTP 429: Too Many Requests (run doctor for fixes)
├─ 🔵 X: 23 posts │ 383 likes │ 100 reposts
├─ 🟡 HN: 7 storys │ 38 points │ 2 comments
├─ 🦋 Bluesky: 1 post │ 19 likes │ 1 reposts
├─ 🐙 GitHub: 12 items │ 1 reactions │ 10 comments
├─ ⛏️ Digg: 18 clusters │ 134 posts │ 77 authors
├─ 🗣️ Top voices: @HUMAIN, @IOPn_newsroom, @togethercompute │ r/legaltech
└─ 📎 Raw results saved to ~/Documents/Last30Days/saudi-arabia-legal-ai-tools-and-legal-research-platforms-arabic-law-bureau-of-experts-nazaha-lexis-middle-east-westlaw-gulf-raw-q2.md
---

I have all the links to the 12 Reddit threads, 23 X posts, 7 HN stories, 1 Bluesky post, 12 GitHub items, and 18 Digg clusters I pulled from. Just ask.

**Engine warnings on this run (relayed honestly):** TikTok, Instagram, Threads, and YouTube all failed with `HTTP 402 Payment Required`; LinkedIn also 402'd; Polymarket failed with repeated connection resets; Reddit hit `HTTP 429 Too Many Requests` after 12 items (rate-limited, not "only 12 threads exist"). Treat every one of those as "not actually searched this run," not as evidence of silence on that platform.

---

## My own listing of concrete tools/repos/products named across both queries

### Query 1 — AI legal assistant plugins/skills for Claude Code, Codex CLI, Gemini CLI

| Tool / Repo | URL | What it does | Saudi / multi-jurisdiction coverage |
|---|---|---|---|
| **claude-for-legal** (Anthropic, official) | https://github.com/anthropics/claude-for-legal | Official plugin suite: 12 plugins, 90+ agents, 20+ MCP connectors across commercial, corporate, privacy, product, employment, litigation, regulatory, AI-governance, IP, and legal-learning practice areas. Installed via `/plugin install commercial-legal@claude-for-legal` etc. | No Saudi/Gulf-specific content found; appears US/generic-common-law oriented (jurisdiction notes reference CA/ND/OK/MN, Delaware/NY/CA) |
| **claude-legal-skill** (evolsb) | https://github.com/evolsb/claude-legal-skill | CUAD-risk-detection contract review skill (41 risk categories, ContractEval, LegalBench benchmarks); reviews contracts, NDAs, employment agreements, SaaS terms, M&A docs; works with Claude Code, Codex, Cursor, Copilot, Gemini CLI, "26+ tools" | US-jurisdiction-flagging only (state non-compete enforceability); no Saudi/multi-jurisdiction claim found |
| **ai-legal-claude** (zubair-trabzada) | https://github.com/zubair-trabzada/ai-legal-claude | 14-skill / 5-parallel-agent Claude Code skill: contract review, risk analysis, NDA generation, compliance auditing, negotiation strategy, PDF reports | No jurisdiction-specific claims found |
| **legal-skills plugin** (borghei) | https://claudeskills.info/plugins/borghei/Claude-Skills/legal-skills/ | 17 legal skills: contract review, NDA, privacy, DPIA, breach response, risk assessment, vendor due diligence | Not jurisdiction-specific |
| **legal-ai-skills / "Marco" contract reviewer** (rohasnagpal) | https://github.com/rohasnagpal/legal-ai-skills | Paste-a-contract skill: risk-scores clauses, flags one-sided terms, gives a negotiation priority list; markdown-based, works in Claude, ChatGPT, Gemini | Not jurisdiction-specific |
| **HAQQ Academy legal skills directory** | https://www.haqq.ai/best-legal-skills (also academy.haqq.ai/skills) | Curated directory of 300+ (elsewhere "338" or "160+") legal AI skills for Claude/ChatGPT/Gemini from Anthropic, OpenAI, Lawvable, Skala, and community contributors, organized by practice area | Aggregator, not a tool itself — but HAQQ separately runs Arabic/MENA legal-AI coverage (see below) |
| **knowledge-work-plugins/legal** (Anthropic) | https://github.com/anthropics/knowledge-work-plugins/blob/main/legal/README.md | Related Anthropic legal-plugin documentation surfaced alongside claude-for-legal | US/generic |

### Query 2 — Saudi Arabia legal AI and legal research platforms

| Tool / Product | URL | What it does | Saudi / multi-jurisdiction coverage |
|---|---|---|---|
| **Adel** | (via HAQQ coverage) https://www.haqq.ai/blog/arabic-ai-lawyer-app | Arabic-native consumer legal-AI app; 500K+ downloads claimed, 70,000+ indexed Saudi legal documents, SAR 149-199/month pricing | Saudi-specific |
| **Shwra** | (via HAQQ coverage) https://www.haqq.ai/blog/arabic-ai-lawyer-app | Hybrid AI + human-lawyer legal app; AI assistant "Mishir" triages then routes to a licensed lawyer; widest consumer distribution (iOS/Android/Huawei) | Saudi-specific |
| **Qaanoon** | (named via HAQQ coverage) | Saudi-specific Arabic-first legal AI app | Saudi-specific |
| **Malakah** | (named via HAQQ coverage) | Saudi-specific Arabic-first legal AI app | Saudi-specific |
| **HAQQ** | https://www.haqq.ai/ | Arabic-native legal AI chat + "eFirm" for law firms; reads/writes Arabic natively (RTL), treats civil-law/Sharia-influenced systems as the default; publishes a 3,000-answer / 300-task / 10-model legal-AI benchmark (Claude Opus 4.8 rated top overall in their run, GPT-5.5 most accurate on citations, Gemini 3.1 Pro strongest on long documents; 24% of all answers cited or misapplied law) | Saudi/MENA-focused, multi-model benchmark |
| **Judicio** | https://judicio.ai/jurisdictions/middle-east | AI legal research positioned for the Middle East & UAE | Middle East/UAE-focused (Saudi coverage not confirmed in this pass) |
| **Bureau of Experts at the Council of Ministers** | (per Saudipedia/Wikidata coverage) | Saudi state authority (est. 1953) that drafts/amends Saudi law; runs a searchable English-translation database of Saudi Basic Laws | Saudi-specific — institutional data source, not an AI product |
| **Nazaha (Oversight and Anti-Corruption Authority)** | https://www.mof.gov.sa/en/Pages/nazaha.aspx | Saudi anti-corruption regulator; new Nov-2024 law gives it power to require officials to prove legitimacy of unexplained wealth | Saudi-specific — regulator, not an AI product; relevant as a diligence/compliance data source |
| **SDAIA (Saudi Data & AI Authority)** | (referenced via CMS/Lexology AI-regulation coverage) | National AI policy body; drafted an "AI Hub Law" (public consultation April 2025, not yet enacted per latest results found) | Saudi-specific regulator |
| **Lexis® Middle East / Lexis+ with Protégé** (LexisNexis) | https://www.lexis.ae/ , https://www.lexisnexis.com/en-ae/products/lexis-middle-east-law | Localized AI legal-research platform for the Gulf: curated content for UAE, Saudi Arabia, Qatar, Kuwait, Bahrain, Oman; 1,700+ GCC Practice Notes (Gulf Legal Advisor) | Explicitly multi-jurisdiction Gulf coverage including Saudi Arabia |
| **Westlaw Edge / AI-Assisted Research** (Thomson Reuters) | (general coverage, no single Gulf-specific product page confirmed) | AI-assisted, citation-first legal research; named in Saudi-focused "top tools" lists | Global tool used regionally; a distinct branded "Westlaw Gulf" product was NOT confirmed in this research pass |
| **Casetext CoCounsel, ChatGPT, Claude, Lexis+, RelativityOne, Everlaw, Spellbook, Smith.ai** | (via Nucamp's Saudi legal-tools list) https://www.nucamp.co/blog/coding-bootcamp-saudi-arabia-sau-legal-top-10-ai-tools-every-legal-professional-in-saudi-arabia-should-know-in-2025 | General-purpose/global legal-AI and drafting/e-discovery tools cited as in active use by Saudi legal professionals | Global tools with reported Saudi adoption, not Saudi-built |

### Notes / gaps
- "claude-for-legal" is Anthropic's own product (this task's stated baseline for comparison), so it is included above for reference but is not itself an "alternative."
- No source in either query confirmed a standalone product literally branded "Westlaw Gulf" — treat that as Westlaw Edge/Thomson Reuters used in the Gulf market until verified directly.
- Community/social evidence for query 2 was thin and largely off-topic (dominated by Saudi sovereign AI-infrastructure deal news, not legal-tech chatter); the tool list above leans on WebSearch results rather than social engagement data, and that imbalance is called out explicitly in the query-2 synthesis above.
- Raw per-query engine output files were saved by the engine to `~/Documents/Last30Days/` (filenames logged as `ai-legal-assistant-plugins-and-skills-for-claude-code-codex-cli-gemini-cli-contract-review-employment-law-corporate-diligence-alternatives-to-claude-for-legal-raw-q1.md` and `saudi-arabia-legal-ai-tools-and-legal-research-platforms-arabic-law-bureau-of-experts-nazaha-lexis-middle-east-westlaw-gulf-raw-q2.md`), but this session's shell could not `ls` or append to that directory (`Operation not permitted`), so Step 2.5 (appending WebSearch citations to the raw files) was not completed — recorded here as an error rather than skipped silently.
