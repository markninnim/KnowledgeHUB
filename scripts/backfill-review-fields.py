#!/usr/bin/env python3
"""
One-off backfill: fills in Service Rating / NPS / Date on Airtable Feefo
records that were created by an older version of import-reviews-xlsx.py
(before it captured those fields). Matches records by exact Adviser + Review
text, only updates records where those fields are currently empty.

Usage:
    AIRTABLE_API_KEY=xxxx python3 scripts/backfill-review-fields.py path/to/already-imported-file.csv

Point it at a file already in public/feefo/imported/ (or anywhere) — it just
needs the original rows to know what rating/NPS/date each review should have.
"""
import sys
import os
import datetime
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
import importlib.util

spec = importlib.util.spec_from_file_location(
    "import_reviews", os.path.join(os.path.dirname(os.path.abspath(__file__)), "import-reviews-xlsx.py")
)
imp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(imp)

BASE_ID = imp.BASE_ID
TABLE_ID = imp.TABLE_ID
FIELD_ADVISER = imp.FIELD_ADVISER
FIELD_REVIEW = imp.FIELD_REVIEW
FIELD_RATING = imp.FIELD_RATING
FIELD_NPS = imp.FIELD_NPS
FIELD_DATE = imp.FIELD_DATE

API_KEY = os.environ.get("AIRTABLE_API_KEY")


def fetch_all_records():
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    records = []
    offset = None
    while True:
        params = {"pageSize": 100}
        if offset:
            params["offset"] = offset
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        records.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset:
            break
    return records


def update_records(updates):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    updated = 0
    for i in range(0, len(updates), 10):
        batch = updates[i:i + 10]
        resp = requests.patch(url, headers=headers, json={"records": batch})
        if resp.status_code >= 300:
            print(f"  ERROR on batch {i}: {resp.status_code} {resp.text}")
            continue
        updated += len(resp.json().get("records", []))
    return updated


def main():
    if not API_KEY:
        sys.exit("Set AIRTABLE_API_KEY env var first.")
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 scripts/backfill-review-fields.py path/to/file.csv")

    path = sys.argv[1]
    rows = imp.load_rows(path)
    print(f"Read {len(rows)} rows from {path}")

    # index by (adviser lower, review text) -> row data
    row_by_key = {}
    for r in rows:
        row_by_key[(r["adviser"].strip().lower(), r["review"].strip())] = r

    records = fetch_all_records()
    print(f"Fetched {len(records)} existing Airtable records")

    import_date = datetime.date.today().isoformat()
    updates = []
    for rec in records:
        f = rec.get("fields", {})
        adv = (f.get(FIELD_ADVISER) or "").strip().lower()
        rev = (f.get(FIELD_REVIEW) or "").strip()
        key = (adv, rev)
        if key not in row_by_key:
            continue
        # only backfill if currently missing
        needs_rating = FIELD_RATING not in f and row_by_key[key].get("rating") is not None
        needs_nps = FIELD_NPS not in f and row_by_key[key].get("nps") is not None
        needs_date = FIELD_DATE not in f
        if not (needs_rating or needs_nps or needs_date):
            continue
        fields = {}
        if needs_rating:
            fields[FIELD_RATING] = row_by_key[key]["rating"]
        if needs_nps:
            fields[FIELD_NPS] = row_by_key[key]["nps"]
        if needs_date:
            fields[FIELD_DATE] = row_by_key[key].get("date") or import_date
        updates.append({"id": rec["id"], "fields": fields})

    print(f"{len(updates)} record(s) need backfilling")
    if updates:
        updated = update_records(updates)
        print(f"Updated {updated} record(s).")
    else:
        print("Nothing to backfill.")


if __name__ == "__main__":
    main()
