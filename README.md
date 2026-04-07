## AI Schools (District Evaluator)

Small, runnable demo that helps parents and educators **search and rank US school districts** using
public-style metrics (graduation rate, proficiency, class size proxy, spending). It ships with a
small CSV dataset so it works out of the box, and keeps scoring logic isolated + unit tested.

### What’s included

- **Web UI**: `GET /` simple search + “top districts” view
- **API**:
  - `GET /api/health`
  - `GET /api/districts?q=&state=&min_enrollment=&max_enrollment=&limit=&offset=`
  - `GET /api/districts/{id}`
  - `GET /api/districts/{id}/score`
  - `POST /api/top` body: `{ "n": 10, "state": "CA", "weights": { ... } }`
- **Data**: `data/districts_sample.csv`
- **Testing**: pytest with **100% coverage enforced**
- **Deployment**: Dockerfile for container deployment

### Run locally (recommended)

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -U pip
./.venv/bin/python -m pip install -e ".[dev]"
./.venv/bin/python -m ai_schools
```

Then open `http://127.0.0.1:8000`.

### Run tests (100% coverage)

```bash
./.venv/bin/python -m pytest
```

### Run with Docker

```bash
docker build -t ai-schools .
docker run --rm -p 8000:8000 ai-schools
```

Open `http://127.0.0.1:8000`.

