import type {
  TestSuiteInfo,
  TestSuiteDetail,
  EvaluationRequest,
  EvaluationResponse,
  EvaluationStatus,
  RunSummary,
  ReportResponse,
} from '../types'

const BASE = '/api'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(init?.headers as Record<string, string>) },
    ...init,
  })
  if (!res.ok) {
    const body = await res.text()
    throw new Error(`HTTP ${res.status}: ${body}`)
  }
  return res.json()
}

export const api = {
  health: () => request<{ status: string; name: string; version: string }>('/health/'),

  listSuites: () => request<TestSuiteInfo[]>('/test-suites/'),

  getSuite: (id: string) => request<TestSuiteDetail>(`/test-suites/${id}`),

  listEvaluations: () => request<RunSummary[]>('/evaluations/'),

  createEvaluation: (req: EvaluationRequest) =>
    request<EvaluationResponse>('/evaluations/', {
      method: 'POST',
      body: JSON.stringify(req),
    }),

  getEvaluation: (runId: string) => request<EvaluationStatus>(`/evaluations/${runId}`),

  getReport: (runId: string, format: 'json' | 'markdown' = 'json') =>
    request<ReportResponse>(`/evaluations/${runId}/report?format=${format}`),
}
