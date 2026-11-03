# AgentShield Architecture

## Overview

AgentShield is a lightweight, API-first platform for security and safety evaluation of AI agents. It follows a modular monolithic architecture designed for local development, simple public deployment, and clear interview demonstration.

## Components

```
User
|
v
Frontend (React + TypeScript + Vite)
|
v
Backend REST API (FastAPI)
|
+----------------------+
|                      |
v                      v
Test Suite Manager     Evaluation Engine
|
v
Target Agent Adapter
|
v
Target Agent API
|
v
Response
|
v
Security Evaluators
|
v
Structured Findings
|
v
Evaluation Report
```

## Boundaries

1. **API Layer** (`backend/app/api/`)
   - FastAPI routes and request/response schemas
   - Input validation, serialization, error handling

2. **Evaluation Orchestration** (`backend/app/services/`)
   - Coordinates test execution
   - Manages test suite loading
   - Produces evaluation results and reports

3. **Target-Agent Integration** (`backend/app/adapters/`)
   - Abstraction over target agent communication
   - OpenAI-compatible adapter (reference implementation)
   - Generic interface for future providers

4. **Test Case Definitions** (`backend/app/test_suites/`, `test_cases/`)
   - JSON-based test suite files
   - Structured metadata for each test case
   - Loader utilities

5. **Security Evaluators** (`backend/app/evaluators/`)
   - Base evaluator interface
   - Deterministic and model-assisted evaluators
   - Category-specific implementations

6. **Result Schemas** (`backend/app/schemas/`, `backend/app/models/`)
   - Strongly typed Pydantic models
   - Validation and serialization contracts

7. **Reporting** (`backend/app/services/reporting.py`)
   - JSON and Markdown report generation
   - Risk summarization

## Data Flow

1. User configures a target agent via API
2. User selects test suite(s)
3. Evaluation engine loads test cases
4. Adapter sends prompts to target agent
5. Responses are collected
6. Evaluators analyze responses
7. Findings are structured and enriched
8. Report is generated and returned

## Technology Choices

- **Backend**: Python, FastAPI, Pydantic v2, httpx
- **Frontend**: React, TypeScript, Vite
- **State**: In-memory (no database in MVP)
- **Tests**: JSON files for static suites, pytest for backend
- **Reports**: JSON and Markdown

## Extension Points

- New evaluators: subclass `BaseEvaluator`
- New adapters: subclass `TargetAgentAdapter`
- New test suites: add JSON files to `test_cases/`
- New report formats: extend reporting service
