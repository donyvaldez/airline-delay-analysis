# ✈️ Airline Delay Analysis: Controllable Disruptions Benchmark

**Where do major U.S. airlines lose on-time performance to causes they can control?**

A peer benchmark of American, Delta, United, JetBlue and Southwest using official U.S. Department of Transportation flight data (July 2025 – June 2026, 4.47 million flights).

📊 **[Interactive dashboard on Tableau Public](https://public.tableau.com/app/profile/juan.galan5573/viz/AirlineDelayAnalysis-ControllableDisruptionsBenchmark/Dashboard1)** · 📄 **[Final report (PDF)](reports/Airline_Delay_Analysis_Final_Report.pdf)** · 📑 **[Executive presentation (PDF)](reports/Airline_Delay_Analysis_Executive_Presentation.pdf)**

> ✅ **Status:** Complete — all four PACE phases (Plan, Analyze, Construct, Execute).

---

## Business problem

Airline operations executives need to know **where** (airport, hour of day, month) their controllable cancellations and delays exceed those of their competitors, so they can focus improvements where they have real leverage.

This project separates **controllable** disruptions (caused by the airline) from **non-controllable** ones (weather, air traffic control, security), so no airline is penalized for events outside its control.

## Key findings

1. **AA at DFW is the largest controllable problem.** 25.2% of AA's DFW flights arrived late with carrier-caused minutes vs. 8.8% for peers at the same airport (+16.4 points) — about **26,100 excess controllable late flights per year**, worse than peers in **12 of 12 months**.
2. **AA's problem starts before any delay can propagate.** 18.0% of AA's first flights of the day at DFW departed 15+ minutes late, vs. 5.1%–9.7% for the other four airlines at their main airports.
3. **Scheduled ground time explains recovery.** When an aircraft arrives late, airlines recover more minutes on the ground the more time they schedule between flights — the ranking holds for all five airlines. At Denver (same airport conditions), UA schedules 74 minutes and recovers 20.8; WN schedules 50 and recovers none.
4. **WN at DEN is an early warning.** Its controllable gap vs. peers widened in April–June 2026, its three worst months of the year.
5. **Open question — cancel or fly late?** AA has the lowest carrier-cancellation rate at DFW (0.25% vs. 0.83% for peers) while having the largest controllable delay; DL shows the opposite pattern at ATL.

*Staffing and maintenance cannot be separated with this data source; both are grouped inside carrier-caused delay.*

## Recommendations

| # | Airline | Recommendation |
|---|---|---|
| R1 | AA at DFW | Diagnose morning station readiness with internal data and bring first-flight punctuality toward the peer level |
| R2 | AA at DFW | Reduce late-arriving aircraft into the hub and review afternoon and evening ground times |
| R3 | WN at DEN | Pilot longer ground times on part of the 12:00–17:59 rotations before extending them |
| R4 | B6 at BOS | Review the ground turnaround process, with a focus on winter readiness |
| R5 | DL and UA | Maintain current practices; UA at DEN is the internal benchmark; DL should review its carrier-cancellation rate |
| P1 | AA and DL | Open question: opposite "operate late" vs. "cancel" strategies? Requires internal airline data |

Each recommendation includes its evidence, how to measure success and its cost or risk in the [final report](reports/Airline_Delay_Analysis_Final_Report.pdf).

## Project status (PACE framework)

| Phase | Description | Status |
|---|---|---|
| **Plan** | Business task, client, metrics, scope — see [`01_Plan.md`](01_Plan.md) | ✅ Complete |
| **Analyze** | Validation, exploration and 12-month peer benchmark — see [`02_Analyze.ipynb`](02_Analyze.ipynb) | ✅ Complete |
| **Construct** | Controllable benchmark, recovery and time-of-day analysis, dashboard — see [`03_Construct.ipynb`](03_Construct.ipynb) | ✅ Complete |
| **Execute** | Recommendations, final report and executive presentation — see [`reports/`](reports/) | ✅ Complete |

## Data

| Item | Detail |
|---|---|
| Source | [BTS TranStats](https://www.transtats.bts.gov/) — Reporting Carrier On-Time Performance (U.S. DOT) |
| Period | July 2025 – June 2026 (12 months) |
| Grain | One row per flight |
| Quality control | All 12 months passed automated validation — see [`docs/ingestion_log.csv`](docs/ingestion_log.csv) and [`docs/cleaning_log.md`](docs/cleaning_log.md) |
| Definitions | Every column, code and metric — see [`docs/data_dictionary.md`](docs/data_dictionary.md) |

Raw data is not stored in this repository. It is public-domain U.S. government data and can be fully regenerated with the ingestion script.

## How to reproduce

```bash
pip install -r requirements.txt
python 01_download_bts.py
```

Then run `02_Analyze.ipynb` and `03_Construct.ipynb` in Jupyter. The Construct notebook writes the dashboard tables to `results/`.

## Tools

Python (Pandas) · Jupyter · Tableau Public · GitHub

## Repository structure

```
airline-delay-analysis/
├── 01_Plan.md                 # Phase 1: business task, scope, metrics and hypotheses
├── 01_download_bts.py         # Reproducible data ingestion
├── 02_Analyze.ipynb           # Phase 2: validation, exploration and peer benchmark
├── 03_Construct.ipynb         # Phase 3: controllable benchmark, recovery, time of day
├── requirements.txt           # Python dependencies
├── reports/
│   ├── Airline_Delay_Analysis_Final_Report.pdf
│   └── Airline_Delay_Analysis_Executive_Presentation.pdf
├── results/                   # Dashboard tables (small CSVs)
│   ├── benchmark_controllable.csv
│   ├── monthly_controllable_gap.csv
│   ├── recovery_by_airline.csv
│   ├── time_of_day.csv
│   └── first_flight.csv
├── docs/
│   ├── ingestion_log.csv      # Data-quality log (one row per month)
│   ├── cleaning_log.md        # Validation tests and analysis decisions
│   └── data_dictionary.md     # Columns, codes, metrics and project terms
└── data/                      # Not tracked: regenerated by the script
```

## Author

**Juan M. Valdez Galán** — Tax and compliance professional with a background in forensic accounting and AML/CFT, applying data analytics to operational risk questions.
