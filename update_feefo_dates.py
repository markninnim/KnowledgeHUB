#!/usr/bin/env python3
"""
Update the Date field in the Airtable Feefo table using Feedback Date from the Excel export.
Matches records by Review text.

Usage:
  AIRTABLE_API_KEY=your_key python3 update_feefo_dates.py
"""

import os, sys, json, time
import urllib.request, urllib.error
import openpyxl
from datetime import datetime

API_KEY   = os.environ.get('AIRTABLE_API_KEY', '')
BASE_ID   = 'appqQv0Xog8yZMwI9'
TABLE_ID  = 'tblU58wJ0rNFPMiKp'
DATE_FLD  = 'fldtrxDQcYIcJHWVp'   # Date field in Feefo table
REVIEW_FLD = 'fldkiTpnNhlnS8hmO'  # Review field
XLSX_PATH = os.path.join(os.path.dirname(__file__), 'dates.xlsx')
URL = f'https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}'

if not API_KEY:
    sys.exit('ERROR: AIRTABLE_API_KEY not set.\nRun: AIRTABLE_API_KEY=your_key python3 update_feefo_dates.py')

# ── 1. Read Excel → build lookup: normalised_review → YYYY-MM-DD date ─────────
print('Reading Excel...')
wb = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)
ws = wb.active

headers = None
lookup  = {}   # normalised review text → date string

for row in ws.iter_rows(values_only=True):
    if headers is None:
        if row[0] and 'Customer Name' in str(row[0]):
            headers = row
        continue

    h = {str(k): v for k, v in zip(headers, row)}
    review      = (h.get('Review') or '').strip()
    feedback_dt = h.get('Feedback Date') or h.get('feedback_date') or ''

    if not review or not feedback_dt:
        continue

    # Parse date — handle ISO string or datetime object
    if isinstance(feedback_dt, datetime):
        date_str = feedback_dt.strftime('%Y-%m-%d')
    else:
        date_str = str(feedback_dt)[:10]   # take YYYY-MM-DD from ISO string

    lookup[review.lower().strip()] = date_str

wb.close()
print(f'  {len(lookup)} Excel rows with review + feedback date\n')

# ── 2. Fetch all Airtable records (paginated) ──────────────────────────────────
def at_get(path, params=''):
    req = urllib.request.Request(
        f'https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}{path}{params}',
        headers={'Authorization': f'Bearer {API_KEY}'}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

print('Fetching Airtable records...')
all_records = []
offset = ''
while True:
    qs = f'?fields[]=Review&pageSize=100'
    if offset:
        qs += f'&offset={offset}'
    data    = at_get('', qs)
    all_records.extend(data.get('records', []))
    offset  = data.get('offset', '')
    print(f'  fetched {len(all_records)} so far...', end='\r')
    if not offset:
        break
    time.sleep(0.2)

print(f'\n  {len(all_records)} records loaded\n')

# ── 3. Match and build update list ─────────────────────────────────────────────
updates    = []
unmatched  = 0

for rec in all_records:
    review_val = (rec.get('fields', {}).get('Review') or '').strip()
    date = lookup.get(review_val.lower().strip())
    if date:
        updates.append({'id': rec['id'], 'fields': {'Date': date}})
    else:
        unmatched += 1

print(f'Matched: {len(updates)}  |  Unmatched: {unmatched}\n')

if not updates:
    sys.exit('Nothing to update.')

# ── 4. Patch in batches of 10 ─────────────────────────────────────────────────
def patch_batch(batch):
    payload = json.dumps({'records': batch}).encode()
    req = urllib.request.Request(
        URL,
        data=payload,
        method='PATCH',
        headers={
            'Authorization':  f'Bearer {API_KEY}',
            'Content-Type':   'application/json',
        }
    )
    try:
        with urllib.request.urlopen(req) as r:
            return len(json.loads(r.read()).get('records', []))
    except urllib.error.HTTPError as e:
        print(f'\n  HTTP {e.code}: {e.read().decode()}')
        return 0

done  = 0
total = len(updates)
BATCH = 10

for i in range(0, total, BATCH):
    chunk = updates[i:i + BATCH]
    done += patch_batch(chunk)
    print(f'  Updated {done}/{total}...', end='\r')
    time.sleep(0.25)

print(f'\n\nDone! {done}/{total} records updated.')
