#!/usr/bin/env python3
"""
Import reviews.csv into Airtable Feefo table.
Usage:
  AIRTABLE_API_KEY=your_key python3 import_feefo.py
"""

import csv, os, sys, time, json
import urllib.request, urllib.error

API_KEY  = os.environ.get('AIRTABLE_API_KEY', '')
BASE_ID  = 'appqQv0Xog8yZMwI9'
TABLE_ID = 'tblU58wJ0rNFPMiKp'
CSV_PATH = os.path.join(os.path.dirname(__file__), 'reviews.csv')
URL      = f'https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}'

if not API_KEY:
    sys.exit('ERROR: AIRTABLE_API_KEY environment variable not set.\nRun: AIRTABLE_API_KEY=your_key python3 import_feefo.py')

def push_batch(records):
    payload = json.dumps({'records': records}).encode()
    req = urllib.request.Request(
        URL,
        data=payload,
        method='POST',
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type':  'application/json',
        }
    )
    try:
        with urllib.request.urlopen(req) as r:
            return len(json.loads(r.read())['records'])
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f'  HTTP {e.code}: {body}')
        return 0

def main():
    with open(CSV_PATH, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))

    total   = len(rows)
    skipped = 0
    done    = 0
    batch   = []

    print(f'Found {total} rows — importing to Feefo table...\n')

    for i, row in enumerate(rows):
        review = (row.get('Review') or '').strip()
        if not review:
            skipped += 1
            continue

        # Service Rating: Airtable rating field expects an integer 1–5
        try:
            rating = int(float(row.get('Service Rating') or 0))
            rating = max(1, min(5, rating)) if rating else None
        except (ValueError, TypeError):
            rating = None

        # NPS: integer 0–10
        try:
            nps = int(float(row.get('NPS') or ''))
        except (ValueError, TypeError):
            nps = None

        fields = {
            'Customer Name': (row.get('Customer Name') or '').strip() or None,
            'Adviser':        (row.get('Adviser')       or '').strip() or None,
            'Review':         review,
        }
        if rating is not None:
            fields['Service Rating'] = rating
        if nps is not None:
            fields['NPS'] = nps

        # Remove None values
        fields = {k: v for k, v in fields.items() if v is not None}
        batch.append({'fields': fields})

        if len(batch) == 10:
            done += push_batch(batch)
            batch = []
            print(f'  {done}/{total - skipped} imported...', end='\r')
            time.sleep(0.25)  # stay well under rate limit

    # Final partial batch
    if batch:
        done += push_batch(batch)

    print(f'\n\nDone! {done} records imported, {skipped} skipped (empty review).')

if __name__ == '__main__':
    main()
