# AgentShield Evaluation Philosophy

## Purpose

AgentShield evaluates AI agents for security and safety properties. The evaluation is not about general capability or correctness—it is about whether the agent behaves securely and respects defined boundaries.

## Evaluation Dimensions

1. **Prompt Injection Resistance**
   - Does the agent resist attempts to override its instructions?

2. **Instruction Following**
   - Does the agent follow security-relevant instructions consistently?

3. **Tool Security**
   - Does the agent use tools safely and with appropriate permissions?

4. **Data Leakage Prevention**
   - Does the agent avoid exposing sensitive information?

5. **Policy Violation Detection**
   - Does the agent avoid violating defined policies?

6. **Jailbreak Susceptibility**
   - Does the agent resist jailbreak attempts?

7. **Permission Boundaries**
   - Does the agent respect permission constraints?

8. **Output Safety**
   - Does the agent produce safe, non-harmful outputs?

9. **Security Boundary Respect**
   - Does the agent respect security boundaries defined in its configuration?

## Evaluator Design

Evaluators are the core analysis units. They receive:

- A test case definition
- The target agent's response
- Optional context (target agent configuration, previous turns)

Evaluators produce:

- Pass/fail determination
- Severity assessment
- Evidence collection
- Reasoning/notes
- Structured finding (if applicable)

### Evaluator Types

- **Deterministic Evaluators**: Rule-based checks (e.g., regex for leaked keys, exact string matches)
- **Model-Assisted Evaluators**: Use an LLM to evaluate response quality (future enhancement)

Not every test requires an LLM evaluator. Deterministic checks are preferred where possible because they are:

- Faster
- Cheaper
- More reproducible
- Easier to reason about

## Test Case Design

Test cases are JSON files with structured metadata:

- `id`: Unique identifier (e.g., `PI-001`)
- `category`: Security category
- `name`: Human-readable name
- `description`: What the test evaluates
- `prompt`: The input to send to the target agent
- `expected_property`: The security property being tested
- `severity`: high, medium, low
- `tags`: Searchable labels
- `evaluator`: Reference to the evaluator type

## Scoring and Reporting

- Each test case produces a result
- Results are aggregated into category summaries
- Findings are enriched with evidence and recommendations
- Reports provide both detailed and summary views

## Limitations

- Evaluation is not exhaustive; it samples the space of possible attacks
- Model-assisted evaluation introduces its own biases
- False positives and false negatives are expected
- Results should be interpreted as evidence, not definitive proof
