# AgentShield Security Model

## Threat Model

AgentShield evaluates external AI agents. The system itself must be secure by design.

### Assets to Protect

- Target agent credentials (API keys, tokens)
- Evaluation data and findings
- Generated reports
- The AgentShield service itself

### Trust Boundaries

1. **Frontend → Backend**: Unauthenticated in MVP; treat as partially trusted
2. **Backend → Target Agent**: Untrusted external service; credentials must be protected
3. **Backend → Storage**: In-memory; no persistent sensitive data exposure
4. **Backend → Reports**: Reports may contain sensitive test inputs; sanitize before distribution

### Security Controls

- **Never log API keys or credentials**
- **Validate URLs** before making outbound requests
- **Apply request timeouts** to all target agent calls
- **Limit payload sizes** to prevent abuse
- **Treat target-agent responses as untrusted input**; sanitize before display
- **Separate target-agent credentials from evaluation data** in memory structures
- **Sanitize generated reports** to avoid leaking credentials or internal state
- **Validate all request payloads** with Pydantic schemas

### Credential Handling

- Target agent credentials are stored in memory only
- Credentials are never returned through API responses
- Credentials are never logged
- Credentials are scoped to the evaluation run and cleared after completion

### Network Security

- Outbound requests are limited to configured target agent endpoints
- No arbitrary server-side network access
- All outbound calls go through the adapter layer with timeout enforcement

### Input Validation

- All API inputs validated via Pydantic schemas
- URL validation for target agent endpoints
- Payload size limits enforced
- Timeout limits enforced

### Current Limitations (MVP)

- No authentication or authorization
- No rate limiting on API endpoints
- No audit logging
- No encryption at rest (in-memory only)

These are acceptable for local development and portfolio demonstration. They should be addressed before any public production deployment.
