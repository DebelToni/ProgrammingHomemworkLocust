# Programming Homework Locust

Locust scenario that targets `https://example.org` by default, plus an optional FastAPI application you can run locally for practice.

## Prerequisites
- Python 3.10+
- `pip install -r requirements.txt`

## Load test example.org
- Launch the Locust web UI: `locust -f locustfile.py` (defaults to `https://example.org`)
- Run headless: `locust -f locustfile.py --headless -u 15 -r 5 -t 2m`
- Override the target with `--host` if you want to test another site (e.g., the sample API).
- Be considerate when hitting public endpoints—keep user counts low unless you have explicit permission.

## Optional local API
```bash
uvicorn app.main:app --reload
```

The service listens on `http://127.0.0.1:8000` with endpoints such as `/health`, `/items`, `/items/{item_id}`, `/orders`, and `/orders/estimate/{item_id}`. Restart the server to reset the in-memory inventory.

## GitHub Actions load test
Use the `.github/workflows/locust.yml` workflow from the Actions tab (`Run workflow`). It installs dependencies and runs Locust headlessly against `https://example.org`, saving CSV, HTML, and log artifacts.

## Project layout
```
.
├── app/
│   └── main.py           # FastAPI application for optional local testing
├── locustfile.py         # Locust scenario targeting example.org by default
├── requirements.txt      # Runtime dependencies
└── .github/workflows/    # CI workflow for manual load test runs
```
