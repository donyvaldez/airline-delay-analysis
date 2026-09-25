Cleaning & Analysis Decisions Log

Project: airline-delay-analysis · Phase 2 (Analyze) · Last updated: 2026-09-25

This log records every decision about how the data was filtered, validated and used. No records were deleted or altered. Raw files in data/raw/ and Parquet files in data/interim/ remain exactly as produced by 01_download_bts.py.

Validation tests
#	Test	Rule	Result
1	Ingestion checks (period, duplicates, cancellation codes, client airlines present)	Project quality checks	12 of 12 months OK — see ingestion_log.csv
2	Delay-cause minutes reconcile to arrival delay	DOT Directive #40, sec. III.5	July 2025: 177,012 of 177,012 late flights reconcile (100%)
3	Row counts reconcile across analyses	Internal consistency	July row count (631,428) matches ingestion log; airline-level late flights sum to test 2 total; 12-month July gaps match single-month results
Decisions
#	Decision	Reason
D1	On-time and late rates use operated flights only (cancelled and diverted excluded)	A cancelled flight never arrived, so it cannot be on time or late
D2	Cancellation rates use all scheduled flights	Cancellations must be counted in their own denominator
D3	Empty delay-cause fields on on-time flights are left empty, not filled	Missing by design: DOT only requires causes for flights 15+ min late
D4	Empty cancellation code on operated flights is left empty	Missing by design: no cancellation occurred
D5	Controllable = cancellation code A + CarrierDelay minutes; LateAircraftDelay reported separately	Defined in 01_Plan.md; late aircraft mixes upstream causes
D6	Comparisons use departures (Origin) from each airport	Consistent perspective across all tests
D7	Peer average is pooled (total late ÷ total flights of the other clients)	Prevents low-volume airlines from distorting the average
D8	Minimum 100 flights for any route or airline-airport result used in conclusions	Small samples produce unreliable percentages
D9	Each client's main airport = its airport with the most departures in the period	Objective, data-driven rule; for WN it is not a traditional hub
D10	Scope limited to AA, DL, UA, B6, WN under their own reporting code; regional affiliates excluded	Defined in 01_Plan.md (version 1 limitation)
D11	Scheduled and actual times kept as text (e.g., 0605)	Preserves leading zeros in 24-hour local times
Open items for next phases
Extend the controllable-delay comparison (D5) at each main airport to all 12 months.
Test the delay-propagation hypothesis by following aircraft (Tail_Number) through the day.
