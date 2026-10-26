# Texas Early Vote Tracker

A working, responsive, static public election-turnout website with **no invented live data**. Open `index.html` through a local HTTP server or deploy to GitHub Pages / Netlify / Cloudflare Pages. No build process or API keys needed.

## Run locally

```bash
cd texas-early-vote-tracker
python -m http.server 8000
```

Open http://localhost:8000. The empty-state dashboard is intentional until verified data is entered.

## Publish publicly (GitHub Pages)

1. Create a public GitHub repository and upload the contents of this folder (not the parent folder).
2. Under **Settings → Pages**, choose **Deploy from a branch**, `main`, `/ (root)`.
3. Visit the Pages URL GitHub supplies. Push CSV updates to update the public dashboard.

Alternatively drag the folder into Netlify's manual deployment interface. The `.github/workflows/validate.yml` workflow checks CSV formatting when pushed to GitHub.

## Enter data

Edit `data/turnout.csv` with one row per `(year, ev_day, coverage_id)`. CSV header:

`year,ev_day,report_date,cumulative_ballots,coverage_id,coverage_label,source_url,registered_voters,notes`

- `year`: 2018, 2022, 2024, or 2026.
- `ev_day`: ordinal early-voting day, starting at 1. Match comparable voting-day definitions across years; document holidays/weekends.
- `report_date`: ISO `YYYY-MM-DD` corresponding to the actual reporting period, not necessarily the publication timestamp.
- `cumulative_ballots`: verified cumulative total; do not use candidate vote counts.
- `coverage_id`: **identical** for series covering the same county set (e.g. `tx_254` for 254 counties or `tx_2018_15_counties` for the exact historical 15-county cohort). The UI only compares identical coverage IDs. Do not assign the same ID to different sets.
- `coverage_label`: human-readable description.
- `source_url`: direct link to the election report or archive.
- `registered_voters`: optional denominator for the exact coverage population.
- `notes`: optional reporting caveats.

Example shape only (NOT REAL DATA; DO NOT COPY AS FACT):

```csv
year,ev_day,report_date,cumulative_ballots,coverage_id,coverage_label,source_url,registered_voters,notes
2026,1,2026-10-19,100000,tx_254,Texas statewide 254 counties,https://www.sos.texas.gov/elections/historical/index.shtml,,DEMO ONLY
```

**Important**: If you want to compare 2018 to 2026, add a *separate* 2026 series aggregated to the exact 2018 county cohort. A single statewide 2026 series must never be compared to a partial-county 2018 series.

## Data architecture

See `docs/architecture.md` and `docs/schema.sql`. Static CSV is the first publication path. A future ingestion worker and database can produce the same CSV contract, without changing the frontend.

## Metrics

- **Cumulative**: `cumulative_ballots`.
- **Added**: difference from previous day in same year and coverage; can include reporting corrections.
- **Historical delta**: `(2026 cumulative / historical cumulative - 1) * 100`, only when matching `coverage_id` and `ev_day` exist.
- **Party split / Independent / NPA / daily mix shift**: intentionally unavailable for Texas until a documented independent model is developed and reviewed. Texas does not register voters by party.

## Data governance

Do not scrape copyrighted third-party dashboards or reuse proprietary modeled party data without permission. Obtain source reports from the Texas SOS. Preserve source URLs, reporting dates, county coverage, and revisions. Label unofficial and incomplete reports. Do not claim turnout is a forecast of election results.

## Next build phase

- County-level ingest, revisions, and historical cohort aggregates.
- Automated scheduled imports after validating the official portal's access method and terms.
- Audited modeled composition module with uncertainty bounds and licensing.
- Shareable charts, county drilldown, data freshness timestamps, accessibility review.
