# Jurisdiction registry

One folder per jurisdiction under `references/jurisdictions/<code>/`, ISO 3166-1 alpha-3 lowercase. Every folder carries `MANIFEST.md`; a populated folder also carries `INDEX.md`, `SOURCES.md`, and one file per instrument. Skills read `MANIFEST.md` first: if `populated` is not `yes`, the skill stops and reports that the jurisdiction is not populated (see the root `CLAUDE.md`, "Jurisdiction architecture").

| Code | Jurisdiction | Populated | Authoritative language | Source portal | Last reviewed | Notes |
|---|---|---|---|---|---|---|
| `ksa` | Kingdom of Saudi Arabia | **yes** | Arabic | https://laws.boe.gov.sa | 2026-09-04 | Commercial, corporate, and labor instruments; see `ksa/INDEX.md` |
| `gbr` | United Kingdom | no | English | https://www.legislation.gov.uk | — | Phase-two stub |
| `fra` | France | no | French | https://www.legifrance.gouv.fr | — | Phase-two stub |
| `che` | Switzerland | no | German, French, Italian | https://www.fedlex.admin.ch | — | Phase-two stub |
| `usa` | United States | reserved | English | — | — | Upstream `claude-for-legal` doctrine is implicitly US; no folder. When the practice profile's footprint includes `usa`, skills follow the upstream US path with the upstream research connectors (CourtListener, Westlaw) rather than a reference folder. |

## Adding a jurisdiction

Copy `_TEMPLATE-instrument.md` for each instrument, fill `MANIFEST.md` with `populated: yes` only after `INDEX.md` lists at least the instruments the in-scope skills load, and run the Phase 5 scenarios in `tests/scenarios/` against the new code. The full procedure is in `README-LEGAL-CONSULTANT.md`, "How to add a jurisdiction".
