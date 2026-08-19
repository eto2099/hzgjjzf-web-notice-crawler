# web-notice-crawler

An open-source agent **skill** + reusable **crawler template** for collecting structured notice/announcement data from JCMS-style government or enterprise websites.

Distilled from a production crawler for a government notice column. Ships the hard-won, non-obvious knowledge as agent instructions plus a parameterized code template.

## Features

- **JSON list API with correct pagination** - JCMS-style backends paginate via a `paramJson` JSON-string parameter; top-level `pageNo`/`rows` are ignored.
- **Detail parsing** - extracts fields from `<meta>` tags and a content div; splits the notice object (first paragraph) from the detail content.
- **Brotli-safe** - handles `Content-Encoding: br` detail pages (requires `brotli`).
- **Anti-bot friendly** - random UA/Referer per request, 3-8s delay, 2^n retry backoff. Deliberately slow.
- **Storage** - `report.csv` (utf-8-sig, append) + per-date JSON files + `last_date.txt` incremental dedup.
- **CLI** - no argument = crawl latest date (fallback to the latest available date when today has none); `--date YYYY-MM-DD` = backfill a specific date.
- **English-only logs** (project convention).

## Layout

```
web-notice-crawler/
├── SKILL.md                  # agent-facing instructions (the skill)
├── README.md
└── template/                 # parameterized crawler you adapt per target site
    ├── config.py             # all site-specific settings
    ├── main.py               # CLI entry
    ├── spider.py             # crawl orchestration
    ├── list_parser.py
    ├── detail_parser.py
    ├── storage.py
    ├── base.py
    ├── anti_anti_spider.py
    └── requirements.txt
```

## Usage

1. Read `SKILL.md` for the full agent workflow.
2. Inspect the target column page's JS to capture the list API params and pagination mechanism.
3. Edit `template/config.py` (domain, API path/params, page size, detail fields) and adjust parser selectors if needed.
4. Run:

```bash
pip install -r template/requirements.txt
python template/main.py                 # latest date (today if available)
python template/main.py --date 2026-08-18   # backfill a specific date
```

## License

MIT