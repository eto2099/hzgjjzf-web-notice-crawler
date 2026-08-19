---
name: web-notice-crawler
description: Build and run an information-collection crawler for notice/announcement columns on JCMS-style government or enterprise websites. Use when a task must collect structured notice lists and detail pages from a paginated JSON API with anti-bot protection, write CSV + per-date JSON, support incremental dedup, and backfill by date.
---

# Web Notice Crawler

Collects notices/announcements from a target website column: the list is loaded via a JSON API, detail pages are parsed into structured fields, and results are saved as CSV plus per-date JSON.

## When to use

- A column/list page whose items are loaded dynamically via a JSON API (e.g. `/api-gateway/.../page/build/unit`).
- The task needs structured fields (title, publish date, source, notice object, detail content, HTML, url, id) with incremental dedup.
- Backfill of a specific date is required.

## Template layout

The reusable crawler lives in `template/` (imports are absolute; run from the `template/` directory):

- `config.py` - all site-specific settings. Edit this first.
- `main.py` - CLI entry: `--date YYYY-MM-DD` for backfill, no arg defaults to latest date.
- `spider.py` - crawl orchestration: date fallback, pagination, dedup, stop conditions.
- `list_parser.py` - parse list `<li>` items.
- `detail_parser.py` - parse detail meta tags + content div; splits notice object vs detail content.
- `storage.py` - CSV (utf-8-sig, append) + per-date JSON + `last_date.txt`.
- `base.py` - requests, random delay, retry with 2^n backoff.
- `anti_anti_spider.py` - random UA / Referer per request.

## Workflow

1. Inspect the target column page HTML/JS and find the script that loads the list (search for the API path, e.g. `build/unit`, and its `queryData`). Capture:
   - API base params (`webId`, `pageId`, `tagId`, `tplSetId`, ...).
   - The pagination mechanism. JCMS-style backends paginate via a `paramJson` JSON-string parameter (`{"pageNo": N, "pageSize": N, "search": ""}`). Top-level `pageNo`/`rows` query params are often IGNORED (every page returns the same first page).
2. Edit `template/config.py`: `TARGET_DOMAIN`, `LIST_API_PATH`, `LIST_API_PARAMS`, `PAGE_SIZE`, `DETAIL_FIELDS`.
3. Inspect one detail page and confirm:
   - `Content-Encoding: br` (brotli) -> `brotli` must be installed, otherwise `resp.text` is garbage and every field parses empty.
   - Field sources: `<meta name="ArticleTitle|PubDate|...">` and a content div (e.g. `div#zoom`). Adjust `detail_parser.py` selectors if the target differs.
4. Run:
   ```
   pip install -r template/requirements.txt
   python template/main.py
   python template/main.py --date 2026-08-18   # backfill one date
   ```
5. Verify output: `data/report.csv` (utf-8-sig, append) gains rows; `data/<date>/<id>.json` files appear; `data/last_date.txt` records the crawled date.
6. Report: target date, item count, files added, CSV row count, or the error from the log.

## Critical non-obvious facts

- **Pagination**: use `paramJson` (JSON string) for JCMS backends; top-level `pageNo`/`rows` do nothing.
- **Brotli**: detail pages are often brotli-compressed. Missing `brotli` yields empty/garbled parses that look like a site change but are an environment problem. Empty `publish_date` -> records fall into `data/unknown/`, which is the failure signal.
- **Date fallback**: when the target day has no items, fall back to the latest date present in the list and log it (in English).
- **Incremental dedup**: `data/last_date.txt` gate plus a per-run `seen_urls` set; stop on earlier date, duplicate URL, or empty URL.
- **Anti-bot**: random UA + Referer, 3-8s delay, 2^n backoff. Deliberately slow; never remove or reduce delays during development/testing.
- **Logs in English only** (project convention).
- **CSV columns** are driven by `config.DETAIL_FIELDS`; keep `storage.py` row mapping in sync when adding fields.

## Failure signals

- Records with only `url` populated -> detail parse failed. Check `brotli` first, then the meta names / content div selectors.
- Every page returns the same items -> pagination param is wrong; use `paramJson`.