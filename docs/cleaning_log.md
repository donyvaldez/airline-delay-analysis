# Cleaning & Analysis Decisions Log

*Project: airline-delay-analysis · Phases 2 (Analyze) and 3 (Construct) · Last updated: 2026-09-28*

This log records every decision about how the data was filtered, validated and used. **No records were deleted or altered.** Raw files in `data/raw/` and Parquet files in `data/interim/` remain exactly as produced by `01_download_bts.py`.

## Validation tests

| # | Test | Rule | Result |
|---|---|---|---|
| 1 | Ingestion checks (period, duplicates, cancellation codes, client airlines present) | Project quality checks | 12 of 12 months OK — see `ingestion_log.csv` |
| 2 | Delay-cause minutes reconcile to arrival delay | DOT Directive #40, sec. III.5 | July 2025: 177,012 of 177,012 late flights reconcile (100%) |
| 3 | Row counts reconcile across analyses | Internal consistency | July row count (631,428) matches ingestion log; airline-level late flights sum to test 2 total; 12-month July gaps match single-month results |
| 4 | Construct load reconciles to Analyze | Internal consistency | 4,471,010 client flights in both phases; unchanged after adding `CRSArrTime` |
| 5 | Excess controllable flights recompute from components | Internal consistency | AA at DFW: 158,920 operated × 16.45% gap = 26,136 |
| 6 | Monthly and annual controllable gaps agree | Internal consistency | AA at DFW: average monthly gap +16.4 = 12-month pooled gap +16.4 |
| 7 | "Pre-09:00 departure = first flight of the day" assumption | Assumption test | **Rejected as a proxy:** only 43%–89% of pre-09:00 departures are first flights. The reported metric was changed to the first-flight late rate |
| 8 | Dashboard exports complete | Row counts | 19, 60, 5, 30 and 5 rows, as designed |

## Decisions

| # | Decision | Reason |
|---|---|---|
| D1 | On-time and late rates use **operated flights only** (cancelled and diverted excluded) | A cancelled flight never arrived, so it cannot be on time or late |
| D2 | Cancellation rates use **all scheduled flights** | Cancellations must be counted in their own denominator |
| D3 | Empty delay-cause fields on on-time flights are **left empty, not filled** | Missing by design: DOT only requires causes for flights 15+ min late |
| D4 | Empty cancellation code on operated flights is **left empty** | Missing by design: no cancellation occurred |
| D5 | **Controllable** = cancellation code A + `CarrierDelay` minutes; `LateAircraftDelay` reported separately | Defined in `01_Plan.md`; late aircraft mixes upstream causes |
| D6 | Comparisons use **departures** (`Origin`) from each airport | Consistent perspective across all tests |
| D7 | Peer average is **pooled** (total late ÷ total flights of the other clients) | Prevents low-volume airlines from distorting the average |
| D8 | Minimum **100 flights** for any route or airline-airport result used in conclusions | Small samples produce unreliable percentages |
| D9 | Each client's **main airport** = its airport with the most departures in the period | Objective, data-driven rule; for WN it is not a traditional hub |
| D10 | Scope limited to AA, DL, UA, B6, WN under their own reporting code; regional affiliates excluded | Defined in `01_Plan.md` (version 1 limitation) |
| D11 | Scheduled and actual times kept as **text** (e.g., `0605`) | Preserves leading zeros in 24-hour local times |
| D12 | Repeated text columns converted to pandas `category` when loading 12 months | Reduces memory to about 1 GB; values unchanged |
| D13 | Aircraft rotations built per `Tail_Number` + `FlightDate`, ordered by scheduled departure; operated flights with a tail number only | A cancelled or unidentified flight breaks the chain |
| D14 | A consecutive pair is valid only if the previous arrival airport equals the next departure airport | Excludes gaps where a flight is missing from the chain |
| D15 | Scheduled ground time must be 1–360 minutes | Longer gaps are parked aircraft, not turnarounds |
| D16 | Late inbound = previous flight `ArrDelay` ≥ 15; late departure = `DepDelay` ≥ 15 | Same 15-minute threshold as the DOT on-time standard |
| D17 | Scheduled ground time summarized with the **median** | Robust to a few very long ground times |
| D18 | Time bands of 3 hours by scheduled **local** departure; "before 09" includes 00:00–08:59 | Readable grouping; local time follows DOT reporting |
| D19 | First flight of the day = first **operated** flight of the aircraft that day | An earlier cancelled flight cannot be seen in the chain |
| D20 | Controllable benchmark uses 12 months and the 100-flight minimum (D8) on **scheduled** flights | Includes groups with enough annual volume |

## Open items

- ~~Extend the controllable-delay comparison to all 12 months~~ — done in Construct.
- ~~Follow aircraft by `Tail_Number`~~ — done in Construct (recovery analysis).
- Possible extensions: secondary hubs per airline; overnight propagation; aircraft type (requires an external fleet registry).
