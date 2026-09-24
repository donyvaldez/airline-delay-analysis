# 01 – Plan · Airline Delay Analysis: Controllable Disruptions Benchmark

*PACE framework — Phase 1 of 4 (Plan → Analyze → Construct → Execute)*
*Author: Juan M. Valdez Galán · Repository: `airline-delay-analysis` · Status: v2 · Last updated: 2026-09-24*

---

## 1. Business task

> **Identify where U.S. airlines lose on-time performance to controllable causes**, so that operations executives can target improvements where they have real leverage.

## 2. Stakeholders

| Stakeholder | Role |
|---|---|
| Operations executive teams of **American (AA), Delta (DL), United (UA), JetBlue (B6) and Southwest (WN)** | Primary audience of a peer benchmark report: each airline compared against the other four |

## 3. Decision supported

Where (airport, hour of day, month) each airline's **controllable** cancellations and delays exceed the average of the other four airlines, so operations teams know where to focus staffing, maintenance and turnaround improvements.

## 4. Business questions

| # | Question |
|---|---|
| Q1 | How do the 5 airlines rank on on-time rate, cancellation rate and controllable share? |
| Q2 | At which airports is each airline's controllable cancellation or delay rate above the peer average? |
| Q3 | At which hours of the day does controllable disruption concentrate, and does it grow through the day? |
| Q4 | In which months is the gap versus peers largest? |

## 5. Success criteria

The project is successful if it:

1. Ranks the 5 airlines by **on-time rate** (arrival less than 15 minutes after schedule — DOT standard), **cancellation rate** and **controllable share**.
2. Lists, for each airline, the **airport × hour × month** combinations where its controllable rate is above the peer average.
3. Separates controllable from non-controllable causes, so no airline is penalized for weather or air traffic control.

## 6. Metric definitions

| Metric | Definition |
|---|---|
| On-time rate | Operated flights arriving < 15 min late ÷ operated flights |
| Cancellation rate | Cancelled flights ÷ scheduled flights |
| **Controllable cancellation** | Cancellation code **A** (air carrier) |
| **Controllable delay minutes** | `CarrierDelay` minutes |
| Late-aircraft delay | `LateAircraftDelay` — reported **separately** (mixes upstream causes) |
| Non-controllable | Weather (B / `WeatherDelay`), NAS (C / `NASDelay`), Security (D / `SecurityDelay`) |
| Peer average | Average of the other four client airlines in the same airport / hour / month |

## 7. Scope

- **Airlines:** AA, DL, UA, B6, WN — flights operated under their own reporting code.
- **Period:** July 2025 – June 2026 (12 complete months).
- **Flights:** Scheduled, nonstop, domestic passenger flights reported to DOT under 14 CFR Part 234.

**Out of scope:** international flights, cargo, charters, fares, passengers per flight, and regional affiliates (Envoy, PSA, SkyWest, Republic) in version 1.

## 8. Data source

| Item | Detail |
|---|---|
| Dataset | BTS TranStats — Reporting Carrier On-Time Performance (U.S. DOT) |
| Grain | One row per flight |
| Ingestion | `01_download_bts.py` — downloads monthly ZIPs, verifies integrity, keeps 31 columns, saves Parquet |
| Validation | All 12 months passed quality checks (period, duplicates, cancellation codes, client airlines present) — see `docs/ingestion_log.csv` |
| Alternative rejected | Kaggle "2015 Flight Delays and Cancellations" — outdated for a 2025–2026 analysis |

All data is U.S. federal public-domain information. No personally identifiable information is used.

## 9. Limitations

1. Regional affiliates fly under their parent brands but report under their own codes; version 1 excludes them, so results reflect mainline operations only.
2. Delay causes are self-reported by airlines under DOT rules.
3. All times are local; hourly comparisons use each airport's local clock.
4. Flights crossing midnight at month-end are counted in the month they start (BTS rule).

## 10. Tools

| Stage | Tool |
|---|---|
| Ingestion & cleaning | Python (Pandas) |
| Analysis | SQL in Google BigQuery (sandbox) |
| Dashboard | Tableau Public |
| Documentation & versioning | GitHub |

## 11. Deliverables

- [x] `01_download_bts.py` — reproducible ingestion
- [x] `docs/ingestion_log.csv` — data-quality log
- [ ] `docs/cleaning_log.md` — every cleaning decision and why
- [ ] SQL analysis scripts
- [ ] Tableau Public dashboard (link in README)
- [ ] README with key findings and recommendations per airline

## 12. Timeline

| Phase | Output | Status |
|---|---|---|
| Plan | This document + data ingestion | ✅ Done |
| Analyze | Cleaning, EDA, cleaning log | Next |
| Construct | Metrics, peer benchmark, dashboard | — |
| Execute | Findings, recommendations, final README | — |

## Sources

- U.S. DOT, BTS — *Technical Reporting Directive #40, On-Time Performance* (effective January 1, 2026)
- U.S. DOT, BTS — TranStats: Reporting Carrier On-Time Performance (1987–present)
