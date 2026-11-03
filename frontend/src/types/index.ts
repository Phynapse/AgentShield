export interface TestSuiteInfo {
  id: string
  name: string
  description: string
  category: string
  test_count: number
}

export interface TestCaseOut {
  id: string
  category: string
  name: string
  description: string
  severity: string
  expected_property: string
  tags: string[]
  evaluator: string
}

export interface TestSuiteDetail extends TestSuiteInfo {
  test_cases: TestCaseOut[]
}

export interface TargetAgentIn {
  name: string
  endpoint: string
  api_key: string
  model: string
  timeout_seconds: number
}

export interface EvaluationRequest {
  target_agent: TargetAgentIn
  suite_ids: string[]
  categories?: string[]
}

export interface EvaluationResponse {
  run_id: string
  status: string
  message: string
}

export interface TestResultOut {
  test_case_id: string
  test_case_name: string
  category: string
  verdict: 'pass' | 'fail' | 'inconclusive' | 'error'
  severity: string
  evidence: string
  reasoning: string
  execution_time_ms: number
  error: string | null
}

export interface FindingOut {
  finding_id: string
  test_case_id: string
  category: string
  severity: string
  title: string
  description: string
  evidence: string
  recommendation: string
  evaluator_type: string
  confidence: number
}

export interface EvaluationStatus {
  run_id: string
  status: string
  target_agent_name: string
  suite_ids: string[]
  categories: string[]
  total_tests: number
  completed_tests: number
  passed: number
  failed: number
  inconclusive: number
  errors: number
  results: TestResultOut[]
  error: string | null
}

export interface RunSummary {
  run_id: string
  status: string
  target_agent_name: string
  total_tests: number
  completed_tests: number
  started_at: string | null
  completed_at: string | null
}

export interface ReportResponse {
  run_id: string
  format: string
  content: string | Record<string, unknown>
}
