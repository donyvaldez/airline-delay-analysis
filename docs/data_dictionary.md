# Data Dictionary & Glossary

*Project: airline-delay-analysis · Covers phases Plan, Analyze and Construct · Last updated: 2026-09-28 (v2)*

Every column, code, metric and project term used in this repository. Definitions follow the U.S. DOT / BTS *Technical Reporting Directive #40* (On-Time Performance, effective January 1, 2026) where applicable.

---

## 1. Source columns (BTS Reporting Carrier On-Time Performance)

One row = one flight. The ingestion script keeps these 31 columns.

### Date and flight identification

| Column | Definition | En simple (ES) |
|---|---|---|
| `Year` | Calendar year of the flight | Año |
| `Month` | Month of the flight (1–12) | Mes |
| `DayofMonth` | Day of the month (1–31) | Día del mes |
| `DayOfWeek` | Day of the week: 1 = Monday … 7 = Sunday | Día de la semana (1 = lunes) |
| `FlightDate` | Full flight date (YYYY-MM-DD). Flights crossing midnight at month-end are counted in the month they start | Fecha completa del vuelo |
| `Reporting_Airline` | Two-character code of the airline that operated and reported the flight (see section 2) | Código de la aerolínea |
| `Flight_Number_Reporting_Airline` | Flight number assigned by the airline | Número de vuelo (ruta y horario) |
| `Tail_Number` | Aircraft registration number | Matrícula del avión |

### Airports

| Column | Definition | En simple (ES) |
|---|---|---|
| `Origin` | Three-letter code of the departure airport | Aeropuerto de salida |
| `OriginCityName` / `OriginState` | City and state of the departure airport | Ciudad y estado de salida |
| `Dest` | Three-letter code of the arrival airport | Aeropuerto de destino |
| `DestCityName` / `DestState` | City and state of the arrival airport | Ciudad y estado de destino |
| `Distance` | Distance between the two airports, in miles | Distancia en millas |

### Times and delays

All times are **local time** of each airport, 24-hour clock, stored as text `hhmm` (e.g., `0832` = 8:32 a.m.).

| Column | Definition | En simple (ES) |
|---|---|---|
| `CRSDepTime` | Scheduled departure time (CRS = Computer Reservation System) | Hora de salida programada |
| `DepTime` | Actual departure time | Hora real de salida |
| `DepDelay` | Actual minus scheduled departure, in minutes. Negative = left early | Minutos de retraso en la salida |
| `DepDel15` | 1 if departure was 15+ minutes late, else 0 | ¿Salió 15+ min tarde? |
| `CRSArrTime` | Scheduled arrival time | Hora de llegada programada |
| `ArrTime` | Actual arrival time | Hora real de llegada |
| `ArrDelay` | Actual minus scheduled arrival, in minutes. Negative = arrived early | Minutos de retraso en la llegada |
| `ArrDel15` | 1 if arrival was 15+ minutes late, else 0. **Basis of the on-time standard** | ¿Llegó 15+ min tarde? |

### Cancellations and diversions

| Column | Definition | En simple (ES) |
|---|---|---|
| `Cancelled` | 1 if the flight was cancelled, else 0 | ¿Se canceló? |
| `CancellationCode` | Reason for cancellation (see section 3). Empty if not cancelled | Motivo de la cancelación |
| `Diverted` | 1 if the flight landed at an airport other than its destination, else 0 | ¿Aterrizó en otro aeropuerto? |

### Delay causes (minutes)

Reported **only for flights arriving 15+ minutes late**. The five fields add up to `ArrDelay` (Directive #40, sec. III.5). Empty on flights that were not late: missing by design, not an error.

| Column | Definition (DOT) | En simple (ES) |
|---|---|---|
| `CarrierDelay` | Circumstances within the airline's control: maintenance, crew, aircraft cleaning, baggage loading, fueling, etc. | Culpa de la aerolínea |
| `WeatherDelay` | Extreme weather (e.g., tornado, blizzard, hurricane) | Clima extremo |
| `NASDelay` | National Aviation System: non-extreme weather, airport operations, heavy traffic volume, air traffic control | Sistema aéreo: control de tráfico, congestión, clima no extremo |
| `SecurityDelay` | Security events: evacuations, re-boarding after a security breach, screening problems | Seguridad |
| `LateAircraftDelay` | The previous flight with the same aircraft arrived late | El avión venía tarde de otro vuelo (efecto dominó) |

---

## 2. Airline codes

| Code | Airline | Role in project |
|---|---|---|
| **AA** | American Airlines | Client |
| **DL** | Delta Air Lines | Client |
| **UA** | United Airlines | Client |
| **B6** | JetBlue Airways | Client |
| **WN** | Southwest Airlines | Client |
| F9 | Frontier | Other reporting carrier |
| NK | Spirit | Other reporting carrier |
| AS | Alaska | Other reporting carrier |
| G4 | Allegiant | Other reporting carrier |
| HA | Hawaiian | Other reporting carrier |
| MQ | Envoy (American regional) | Regional affiliate — excluded in v1 |
| OH | PSA (American regional) | Regional affiliate — excluded in v1 |
| OO | SkyWest (regional for several airlines) | Regional affiliate — excluded in v1 |
| YX | Republic (regional for several airlines) | Regional affiliate — excluded in v1 |

## 3. Cancellation codes

| Code | Cause | Controllable in this project? |
|---|---|---|
| **A** | Carrier | ✅ Yes |
| B | Weather | ❌ No |
| C | National Aviation System (NAS) | ❌ No |
| D | Security | ❌ No |

## 4. Airports referenced in findings

| Code | Airport |
|---|---|
| ATL | Atlanta Hartsfield-Jackson |
| BOS | Boston Logan |
| CLT | Charlotte Douglas |
| DAL | Dallas Love Field |
| DEN | Denver |
| DFW | Dallas/Fort Worth |
| EWR | Newark Liberty |
| IAH | Houston George Bush Intercontinental |
| LGA | New York LaGuardia |
| MCO | Orlando |
| MIA | Miami |
| ORD | Chicago O'Hare |
| TPA | Tampa |

---

## 5. Project terms

| Term | Definition | En simple (ES) |
|---|---|---|
| **Client airlines** | AA, DL, UA, B6 and WN, flights under their own reporting code | Las 5 aerolíneas del informe |
| **Peers** | The other client airlines departing from the **same airport** in the same period | Las competidoras en el mismo aeropuerto |
| **Main airport** | For each client, the airport with the most departures in the period (decision D9) | Donde más vuelos tiene cada aerolínea |
| **Hub** | Airport where an airline concentrates connections and rotates aircraft | Centro de operaciones |
| **Route** | Airline + origin + destination | Aerolínea + salida + destino |
| **Scheduled flights** | All flights in the data, including cancelled and diverted | Vuelos programados |
| **Operated flights** | Flights neither cancelled nor diverted | Vuelos que sí llegaron a su destino |
| **Late** | Arrived 15+ minutes after schedule (`ArrDel15 = 1`) | Tarde |
| **On time** | Arrived less than 15 minutes after schedule (`ArrDel15 = 0`) | A tiempo |
| **Controllable** | Cancellation code A + `CarrierDelay` minutes. A project category grounded in Directive #40, not an official DOT field | Lo que la aerolínea pudo evitar |
| **Non-controllable** | Weather, NAS and security causes | Lo que no depende de la aerolínea |
| **Late-aircraft effect** | Delay inherited from the aircraft's previous flight; reported separately from controllable | Efecto dominó |
| **Missing by design** | Empty field because it does not apply (e.g., no causes on on-time flights) | Vacío que no es error |

---

## 6. Metrics

Unless stated otherwise, rates use **operated flights** as the base (D1) and cancellation rates use **scheduled flights** (D2). Percentages are 0–100. Differences between percentages are in **percentage points (pts)**.

### All-cause metrics (Analyze phase)

| Metric (code name) | Formula | Meaning | En simple (ES) |
|---|---|---|---|
| `pct_tarde` — late rate | late operated flights ÷ operated flights × 100 | Share of flights arriving 15+ min late | % de vuelos tarde |
| On-time rate | 100 − late rate | Share arriving on time | % puntualidad |
| `pct_tarde_pares` — peer late rate | late ÷ operated for **all peers combined** × 100 (pooled, D7) | Benchmark at the same airport | % tarde de las competidoras |
| `brecha_vs_pares` — gap vs. peers | `pct_tarde` − `pct_tarde_pares` | Positive = worse than peers | Diferencia contra competidoras |
| `exceso_vuelos_tarde` — excess late flights | operated flights × gap ÷ 100 | Estimated late flights above the peer level | Vuelos tarde de más |
| `min_por_vuelo` — delay minutes per flight | sum of 5 cause fields ÷ operated flights | Average delay intensity | Minutos de retraso promedio |
| Cause mix (`pct_carrier`, `pct_late_aircraft`, …) | minutes of one cause ÷ minutes of all causes × 100 | How delay minutes split by cause (sums to 100) | Reparto del retraso por causa |
| Average monthly gap | simple average of the 12 monthly gaps | Summary of the 12-month trend | Brecha promedio del año |

### Controllable metrics (Construct phase)

| Metric (code name) | Formula | Meaning | En simple (ES) |
|---|---|---|---|
| `ctrl_pct` — controllable late rate | operated flights with `ArrDel15 = 1` **and** `CarrierDelay > 0` ÷ operated flights × 100 | Share of flights late with at least some carrier-caused minutes | % de vuelos tarde con culpa propia |
| `ctrl_pct_pares` | Same, for all peers combined at the same airport | Peer benchmark | Lo mismo, para las competidoras |
| `brecha_ctrl` — controllable gap | `ctrl_pct` − `ctrl_pct_pares` | Positive = worse than peers on controllable delay | Diferencia controlable |
| `exceso_ctrl` — excess controllable late flights | operated flights × `brecha_ctrl` ÷ 100 | Estimated controllable late flights above the peer level; an estimate that assumes the peer level is achievable | Vuelos tarde por culpa propia que sobran |
| `min_carrier` — carrier minutes per flight | sum of `CarrierDelay` ÷ operated flights | Intensity of controllable delay | Minutos de culpa propia por vuelo |
| `cancel_A` — carrier cancellation rate | code A cancellations ÷ scheduled flights × 100 | Share of flights cancelled for carrier reasons | % cancelado por culpa propia |
| `pct_vuelos_retraso_controlable` | Same formula as `ctrl_pct` (name used in the Analyze DFW test) | — | Igual que `ctrl_pct` |
| `min_late_aircraft_por_vuelo` | sum of `LateAircraftDelay` ÷ operated flights | Intensity of the late-aircraft effect | Minutos de efecto dominó por vuelo |

### Recovery and time-of-day metrics (Construct phase)

Built from **consecutive flight pairs**: two operated flights of the same aircraft (`Tail_Number`) on the same day, where the first flight's arrival airport is the second flight's departure airport.

| Metric (code name → export name) | Formula | Meaning | En simple (ES) |
|---|---|---|---|
| `tierra_prog` → `ground_time_median_min` | next scheduled departure − previous scheduled arrival (minutes); reported as the **median** | Buffer the airline schedules between flights | Colchón programado en tierra |
| `pct_recibe_tarde` → `pct_inbound_late` | pairs where the previous flight arrived 15+ min late ÷ all pairs × 100 | How often the aircraft reaches the hub late | % de aviones que llegan tarde al hub |
| `llega_con_min` → `inbound_delay_min` | average `ArrDelay` of the previous flight, among late inbound pairs | Delay the aircraft brings in | Con cuánto retraso llega |
| `sale_con_min` → `outbound_delay_min` | average `DepDelay` of the next flight, among late inbound pairs | Delay the aircraft leaves with | Con cuánto retraso sale |
| `recupera_en_tierra` → `recovery_min` | `inbound_delay_min` − `outbound_delay_min` | Minutes recovered on the ground. Negative = more delay added on the ground | Minutos recuperados en tierra |
| `pct_sale_a_tiempo` → `pct_departs_on_time_after_late_inbound` | late inbound pairs whose next flight departs < 15 min late ÷ late inbound pairs × 100 | Ability to fully absorb a late arrival | % que sale a tiempo tras recibir un avión tarde |
| `tramos_por_dia` → `legs_per_aircraft_day` | average number of operated flights per aircraft per day | Aircraft utilization | Vuelos por avión al día |
| `franja` → `time_band` | 3-hour band of scheduled local departure: before 09 (00:00–08:59), 09-11, 12-14, 15-17, 18-20, 21+ | Time-of-day grouping | Franja horaria |
| `sale_tarde` → `pct_departing_late` | departures with `DepDelay` ≥ 15 ÷ departures × 100 | Share of departures leaving 15+ min late | % de salidas tarde |
| `salidas_antes_09` → `departures_before_09` | departures scheduled before 09:00 | Volume of the first wave | Salidas antes de las 9 |
| `pct_primer_vuelo_del_dia` → `pct_first_flight_of_day` | pre-09:00 departures that are the aircraft's first operated flight of the day ÷ pre-09:00 departures × 100 | Checks the "morning = first flight" assumption | % que es el primer vuelo del día |
| `pct_tarde_primer_vuelo` → `pct_first_flights_late` | first flights of the day departing 15+ min late ÷ first flights × 100 | Station readiness; no inbound aircraft, so no propagation possible | % de primeros vuelos que salen tarde |

### Quality flags

| Flag | Rule | En simple (ES) |
|---|---|---|
| `confiable` — reliable | 100+ flights in the group (D8) | Suficientes vuelos para concluir |
| Ingestion `estado` | OK if all ingestion checks pass, REVISAR otherwise | Resultado del control de cada mes |

---

## 7. Dashboard tables (`results/`)

Exported by `03_Construct.ipynb`; column names in English for the public dashboard.

| File | Rows | Columns |
|---|---|---|
| `benchmark_controllable.csv` | 19 | airport, airline, scheduled_flights, operated_flights, ctrl_late_pct, peer_ctrl_late_pct, ctrl_gap_pts, carrier_min_per_flight, peer_carrier_min_per_flight, carrier_cancel_pct, peer_carrier_cancel_pct, excess_ctrl_late_flights, is_main_airport |
| `monthly_controllable_gap.csv` | 60 | airline, airport, month, ctrl_late_pct, peer_ctrl_late_pct, ctrl_gap_pts |
| `recovery_by_airline.csv` | 5 | consecutive_pairs, ground_time_median_min, pct_inbound_late, inbound_delay_min, outbound_delay_min, pct_departs_on_time_after_late_inbound, recovery_min, legs_per_aircraft_day, airline, airport |
| `time_of_day.csv` | 30 | pct_departing_late, recovery_min, ground_time_median_min, time_band, airline, airport |
| `first_flight.csv` | 5 | departures_before_09, pct_first_flight_of_day, pct_first_flights_late, airline, airport |

## 8. Technical terms

| Term | Definition | En simple (ES) |
|---|---|---|
| Parquet | Compressed, column-based file format | Como un CSV, pero más liviano y rápido |
| `category` (pandas type) | Stores repeated text values as codes to save memory | Guardar códigos en vez de repetir el texto |
| `NaN` / `<NA>` | Empty value in pandas | Celda vacía |
| Pooled average | Total of events ÷ total of flights across a group | Promedio donde quien vuela más pesa más |
| Percentage point (pt) | Arithmetic difference between two percentages | 30% − 25% = 5 puntos |
| Reconciliation | Checking that a figure matches an independent source or total | Conciliación: que los números cuadren |
| Consecutive flight pair | Two operated flights of the same aircraft on the same day, where the first lands where the second departs | Dos vuelos seguidos del mismo avión |
| Aircraft-day | One aircraft (`Tail_Number`) on one date | La jornada de un avión |
| First flight of the day | The aircraft's first **operated** flight that day (an earlier cancelled flight is not visible) | Primer vuelo del avión ese día |
| Median | Middle value of a sorted list; robust to extreme values | Valor del medio |
| Tableau Public | Free platform to publish interactive dashboards; published data is public | Donde está publicado el dashboard |
