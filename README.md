# AgentShield

An AI Agent Security & Evaluation platform that runs controlled adversarial tests against target AI agents and produces structured security evaluation reports.

## Problem

AI agents are increasingly deployed with tool access, system prompts, and sensitive data handling. There is no lightweight, standardized way to evaluate whether these agents resist common security attacks. AgentShield addresses this by providing a repeatable evaluation pipeline.

## Architecture

```
Frontend (React + TypeScript)
    |
    v
FastAPI REST API
    |
    v
Evaluation Pipeline
    |
    +-------------------+
    |                   |
    v                   v
Test Suite Loader    Target Agent Adapter (httpx)
    |                   |
    v                   v
JSON Test Cases      Target Agent API
                         |
                         v
                      Raw Response
                         |
                         v
                   Evaluation Engine
                         |
           +-------------+-------------+
           |             |             |
           v             v             v
     Deterministic   Semantic      Tool/Policy
     Evaluators      Evaluator     Evaluators
           |             |             |
           +-------------+-------------+
                         |
                         v
                  Normalized Result
                         |
                         v
               Structured Findings
                         |
                         v
                      Report (JSON / Markdown)
```

**Modular monolith** — no microservices, no Kubernetes, no distributed queues.

## Features

- **5 security test categories**: Prompt injection, jailbreak, data leakage, tool security, unsafe behavior
- **26 curated test cases** with structured metadata
- **Deterministic evaluators** using pattern matching (no LLM required for basic detection)
- **Optional semantic evaluator** using an OpenAI-compatible model endpoint
- **4-state verdict system**: pass, fail, inconclusive, error
- **5-level severity**: critical, high, medium, low, informational
- **Structured findings** with evidence, reasoning, and recommendations
- **JSON and Markdown report export**
- **SSRF protection** with configurable localhost/private-IP blocking
- **Professional security dashboard** (React + TypeScript)
- **61 automated tests** (unit + integration + security)

## Current Status

**Phase 2: Core Engine** — Fully implemented. The evaluation pipeline is functional end-to-end.

## Security Model

- Target agent credentials are held in memory only, never persisted or logged
- SSRF protection blocks private/internal IPs in production mode
- Target agent responses are treated as untrusted input
- Report generation sanitizes output
- API key never appears in any API response
- Global exception handler prevents stack trace leakage

See `docs/security.md` for the full threat model.

## Local Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`. The Vite dev server proxies `/api` to the backend.

### Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Default | Description |
|----------|---------|-------------|
| `ALLOW_LOCALHOST_TARGETS` | `true` | Allow localhost/private-IP targets (set `false` in production) |
| `EVALUATION_TIMEOUT_SECONDS` | `30` | Default timeout for target agent requests |
| `EVALUATOR_MODEL_ENDPOINT` | (empty) | Optional: OpenAI-compatible endpoint for semantic evaluation |
| `EVALUATOR_MODEL_API_KEY` | (empty) | Optional: API key for semantic evaluator |
| `EVALUATOR_MODEL_NAME` | (empty) | Optional: Model name for semantic evaluator |

## API Overview

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health/` | Health check |
| GET | `/test-suites/` | List available test suites |
| GET | `/test-suites/{id}` | Get suite with test cases |
| GET | `/evaluations/` | List evaluation runs |
| POST | `/evaluations/` | Start an evaluation |
| GET | `/evaluations/{id}` | Get evaluation status and results |
| GET | `/evaluations/{id}/report?format=json` | Get JSON report |
| GET | `/evaluations/{id}/report?format=markdown` | Get Markdown report |

## Evaluation Methodology

AgentShield uses a two-tier evaluation approach:

1. **Deterministic evaluators** — Pattern-based detection using regex matching for known compliance/refusal indicators, secret patterns, unsafe tool commands, and harmful content markers. Fast, reproducible, zero cost.

2. **Semantic evaluator** (optional) — Model-assisted analysis when deterministic checks are inconclusive. Uses structured JSON output with strict Pydantic validation. Failures become "inconclusive" rather than crashes.

**Verdict policy:**
- Deterministic confirmed violation → **fail**
- Deterministic confirmed safe → **pass**
- Conflicting or absent signals → **inconclusive**
- Semantic evaluator supplements inconclusive cases only
- Any execution error → **error**

See `docs/evaluation.md` for details.

## Testing

```bash
cd backend
python -m pytest tests/ -v
```

Runs 61 tests covering:
- Schema validation
- All 5 evaluator categories with known-good and known-bad inputs
- Test suite loading and validation
- API endpoints
- SSRF protection
- Full end-to-end evaluation with mocked target agents
- API key leakage prevention

## Project Structure

```
agentshield/
├── backend/
│   ├── app/
│   │   ├── api/routes/       # REST API endpoints
│   │   ├── core/             # Config, logging
│   │   ├── models/           # Domain models (Pydantic)
│   │   ├── services/         # Evaluation orchestrator
│   │   ├── evaluators/       # Security evaluators
│   │   ├── adapters/         # Target agent communication
│   │   └── test_suites/      # Test suite loader
│   └── tests/                # pytest tests
├── frontend/src/
│   ├── pages/                # Dashboard, NewEvaluation, Results, Report
│   ├── services/             # API client
│   └── types/                # TypeScript interfaces
├── test_cases/               # JSON test suites
└── docs/                     # Architecture, security, evaluation docs
```

## Limitations

- **In-memory state**: Evaluation results survive only for the running process
- **No authentication**: No user auth in MVP
- **Limited test coverage**: 26 test cases across 5 categories — not exhaustive
- **Deterministic detection limits**: Pattern matching cannot catch all attack variations
- **Semantic evaluator uncertainty**: Model-assisted evaluation can produce false positives/negatives
- **Single-turn only**: Does not evaluate multi-turn conversations
- **No real tool execution**: Tool security tests evaluate the agent's *stated intent*, not actual tool behavior

## Roadmap

See `docs/roadmap.md` for the full roadmap.

## Deployment

AgentShield is a modular monolith designed for simple public deployment. No Kubernetes, distributed queues, or databases are required.

### Production Checklist

Before any public deployment, address the [MVP security limitations](docs/security.md):

- [ ] Add authentication and authorization
- [ ] Implement rate limiting on API endpoints
- [ ] Enable audit logging
- [ ] Set `ALLOW_LOCALHOST_TARGETS=false`
- [ ] Add encryption at rest (database or persistent storage)
- [ ] Reverse proxy (nginx) with TLS termination

### Docker

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run
cd backend
docker build -t agentshield-backend .
docker run -p 8000:8000 -e ALLOW_LOCALHOST_TARGETS=false agentshield-backend
```

### Static Frontend Build

```bash
cd frontend
npm install
npm run build
```

Serve the `dist/` directory with any static host (Vercel, Netlify, nginx, etc.). Point the frontend's API base URL at your backend.

### Environment Variables for Production

| Variable | Required | Description |
|----------|----------|-------------|
| `APP_NAME` | Yes | Application name |
| `APP_VERSION` | Yes | Application version |
| `DEBUG` | No | Set to `false` in production |
| `LOG_LEVEL` | No | Set to `WARNING` in production |
| `BACKEND_HOST` | No | Bind address (default `0.0.0.0`) |
| `BACKEND_PORT` | No | Bind port (default `8000`) |
| `ALLOW_LOCALHOST_TARGETS` | Yes | Must be `false` in production |
| `EVALUATION_TIMEOUT_SECONDS` | No | Default timeout for target agent requests |
| `MAX_PAYLOAD_SIZE_KB` | No | Max request payload size |
| `RATE_LIMIT_PER_MINUTE` | No | Rate limit (requires middleware) |

### Scaling Notes

- **State**: Currently in-memory. For horizontal scaling, move evaluation results to a database (PostgreSQL) and add a shared cache.
- **CORS**: Update `allow_origins` in `backend/app/main.py` to restrict frontend origins in production.
- **Background tasks**: Long-running evaluations should use a task queue (Celery, RQ) instead of synchronous execution.

## License

MIT