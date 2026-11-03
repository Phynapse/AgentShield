# AgentShield Roadmap

## MVP (Current Phase)

- [x] Project structure and foundation
- [x] Backend FastAPI application shell
- [x] Core domain schemas (Pydantic)
- [x] API contracts (health, test-suites, evaluations)
- [x] Test suite JSON files (representative samples)
- [x] Evaluator abstractions (base classes)
- [x] Target agent adapter abstraction
- [x] Security documentation
- [x] Initial pytest suite
- [x] Frontend structural shell (React + Vite)
- [x] README and project documentation

## Phase 2: Core Engine

- [ ] Implement OpenAI-compatible target agent adapter
- [ ] Implement deterministic evaluators (prompt injection, jailbreak, leakage)
- [ ] Evaluation orchestration service
- [ ] Synchronous evaluation execution
- [ ] Report generation (JSON + Markdown)
- [ ] Basic frontend dashboard
- [ ] Evaluation results view
- [ ] Frontend API integration
- [ ] Expanded test suite JSON files

## Phase 3: Enhanced Evaluation

- [ ] Model-assisted evaluators
- [ ] Multi-turn conversation evaluation
- [ ] Tool-use simulation
- [ ] Baseline comparison
- [ ] Historical result tracking (local)
- [ ] Report export (PDF)

## Phase 4: Advanced Features

- [ ] Custom test suite builder
- [ ] Scheduled evaluations
- [ ] CI/CD integration
- [ ] Evaluation templates
- [ ] Benchmarking and scoring rubrics
- [ ] Agent comparison views

## Future Enterprise Features

These are explicitly out of scope for the portfolio project but noted for architectural discussion:

- Kubernetes deployment
- Microservices architecture
- Distributed task queues (Celery, Kafka)
- Hosted databases (PostgreSQL, etc.)
- Enterprise authentication (SSO, OAuth)
- Multi-tenancy
- Audit logging and compliance reporting
- Vector database for finding similarity
- Advanced rate limiting and API gateways
- Cloud orchestration
