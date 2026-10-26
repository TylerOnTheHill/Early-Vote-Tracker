#!/usr/bin/env python3
import csv, datetime, pathlib, sys
path=pathlib.Path(__file__).resolve().parents[1]/'data'/'turnout.csv'
required={'year','ev_day','report_date','cumulative_ballots','coverage_id','coverage_label','source_url'}
with path.open(newline='',encoding='utf-8-sig') as f:
    reader=csv.DictReader(f)
    assert required.issubset(reader.fieldnames or []), 'Missing CSV headers'
    seen=set()
    for lineno,r in enumerate(reader,2):
        assert all(r[k] for k in required), f'Missing value line {lineno}'
        assert int(r['year']) in (2018,2022,2024,2026), f'Invalid year line {lineno}'
        assert 1<=int(r['ev_day'])<=30, f'Invalid day line {lineno}'
        assert int(r['cumulative_ballots'])>=0, f'Negative ballots line {lineno}'
        datetime.date.fromisoformat(r['report_date'])
        assert r['source_url'].startswith(('https://','http://')), f'Invalid source line {lineno}'
        k=(r['year'],r['ev_day'],r['coverage_id'])
        assert k not in seen, f'Duplicate row {k}'
        seen.add(k)
print(f'CSV validated: {len(seen)} reports')
