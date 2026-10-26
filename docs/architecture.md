# Architecture and pipeline

## Version 1: public static deployment

Texas SOS report → manual review and normalization → `data/turnout.csv` → static site (HTML/CSS/JS) → public visitors.

The public client fetches the CSV on page load, validates records, renders historical series and source links. No database, authentication, tracking cookies, API credentials, or paid hosting required. Updates are published as version-controlled CSV commits.

## Version 2: automated verified ingestion

1. Scheduled server-side collector downloads official report files using a verified and permitted method.
2. Raw snapshots stored immutably with fetch timestamp and checksum.
3. Parser normalizes county, vote method, reporting date, cumulative votes, and reporting coverage.
4. Validation checks duplicate rows, monotonicity (flag revisions; don't discard), missing counties, source consistency, county universe, and registration denominator.
5. Reviewer approval or automated gate publishes a canonical daily aggregate and an audit trail.
6. Static CSV/JSON materialized and published to CDN; frontend remains unchanged.

Do not treat absent counties as zero turnout. Prefer a completeness indicator and preserve previous snapshot. Keep reports by `as_of` timestamp to trace revisions.

## Data entities

- `elections`: jurisdiction, cycle, election date, EV calendar, source.
- `counties`: Texas county identifiers and names.
- `report_snapshots`: immutable source URL, retrieved timestamp, checksum, parser version.
- `county_turnout`: report snapshot, county, day, in-person cumulative, mail cumulative, reported total, registration denominator.
- `coverage_sets` and `coverage_members`: exact county universe for fair historical comparisons.
- `state_day_aggregates`: publication-ready, coverage-specific totals, EV day, year, provenance.
- `party_models`: separate modeled outputs with methodology, model version, license, uncertainty, and population definition; no implied official status.

## Party-model design (not implemented)

Texas has no party registration. Do not call primary history or precinct partisan lean an official party registration split or actual vote choice. Any estimated composition must identify what it models (voter history, precinct partisanship, or modeled candidate support), uncertainty, coverage, and assumptions. `Independent/NPA` must not be inferred as the residual of a two-party partisan *lean* model unless that model actually estimates a third category. Daily shift compares matching definitions and populations.
