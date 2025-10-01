# Books Monitor: Crawler + Scheduler + API (FastAPI + MongoDB)

This project crawls the demo site https://books.toscrape.com, detects changes daily, and serves data via a secure REST API.

## Features

- Async crawler with retries, pagination, and raw HTML snapshots.
- MongoDB storage (Motor) with indexes for efficient queries and deduplication.
- Change detection using content hashing and change logs.
- Daily scheduler (APScheduler) and change report generation (JSON).
- FastAPI server with API key auth, rate limiting, pagination, filtering and sorting.
- Config via `.env` (Pydantic Settings), structured logging, and tests.

## Tech Stack

- Python 3.11+
- FastAPI, Uvicorn
- Motor (MongoDB async driver)
- httpx (async HTTP)
- BeautifulSoup + lxml (HTML parsing)
- APScheduler (daily jobs)
- Pydantic v2 + pydantic-settings

## Quick Start

1. Create and activate a virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Copy environment and edit if needed

```
cp .env.example .env
```

4. Start MongoDB (Docker Compose)

```
docker compose up -d mongo
```

5. Initialize and run the API

```
uvicorn app.api.main:app --reload --port 8000
```

6. Run a one-off crawl

```
python -m app.crawler.runner
```

7. Run the scheduler

```
python -m app.scheduler.main
```

## API

- Swagger UI: http://localhost:8000/docs
- Authentication: Header `X-API-Key: <your key>` (configure in `.env` via `API_KEYS`)
- Rate limit: default 100 req/hour per API key (in-memory; can be extended)

### Endpoints

- GET `/books` with filters: `category`, `min_price`, `max_price`, `rating`, `sort_by` in {`rating`, `price`, `reviews`}, `order` in {`asc`, `desc`}, pagination `page`, `page_size`.
- GET `/books/{book_id}` where `book_id` = UPC.
- GET `/changes` with optional filters.

## Folder Structure

```
app/
  api/
    main.py
    deps.py
    routers/
      books.py
      changes.py
  config/
    settings.py
    logging.py
  crawler/
    crawler.py
    parser.py
    runner.py
  db/
    mongo.py
    indexes.py
  models/
    book.py
    change.py
  scheduler/
    main.py
    report.py
  utils/
    http_client.py
    hashing.py
    rate_limiter.py
    auth.py
    time.py
tests/
```

## MongoDB Documents

### `books` Collection (sample)

```
{
  "_id": ObjectId(...),
  "upc": "a1b2c3d4",
  "name": "A Light in the Attic",
  "description": "...",
  "category": "Poetry",
  "price_excl_tax": 51.77,
  "price_incl_tax": 51.77,
  "availability": 22,
  "num_reviews": 0,
  "image_url": "https://.../media/cache/xx.jpg",
  "rating": 3,
  "source_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "content_hash": "sha256:...",
  "raw_html": "<html>...</html>",
  "first_seen": "2025-09-30T00:00:00+00:00",
  "last_seen": "2025-09-30T00:00:00+00:00"
}
```

### `changes` Collection (sample)

```
{
  "_id": ObjectId(...),
  "book_upc": "a1b2c3d4",
  "change_type": "update",  // or "new"
  "changes": [
    {"field": "price_excl_tax", "old": 49.99, "new": 51.77}
  ],
  "timestamp": "2025-09-30T00:00:00+00:00"
}
```

## Testing

```
pytest -q
```

## Security Notes

- Keep API keys secret. Do not commit `.env`.
- In production, use a real rate limiter backed by Redis and reverse proxy protections.

## License

MIT
