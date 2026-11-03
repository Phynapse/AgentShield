import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../services/api'
import type { EvaluationStatus, TestResultOut } from '../types'

function SeverityBadge({ severity }: { severity: string }) {
  return <span className={`badge badge-${severity}`}>{severity}</span>
}

function VerdictBadge({ verdict }: { verdict: string }) {
  return <span className={`badge badge-${verdict}`}>{verdict}</span>
}

export function EvaluationResults() {
  const { runId } = useParams<{ runId: string }>()
  const [data, setData] = useState<EvaluationStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [expandedTest, setExpandedTest] = useState<string | null>(null)

  useEffect(() => {
    if (!runId) return
    api.getEvaluation(runId)
      .then(setData)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [runId])

  if (loading) return <div className="loading">Loading evaluation...</div>
  if (error) return <div className="error-msg">{error}</div>
  if (!data) return <div className="error-msg">Evaluation not found</div>

  const categories = [...new Set(data.results.map(r => r.category))]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <h2>Evaluation Results</h2>
        <div style={{ display: 'flex', gap: 8 }}>
          <Link to={`/evaluations/${runId}/report`} className="btn">View Report</Link>
          <Link to="/" className="btn">Back</Link>
        </div>
      </div>

      <div style={{ marginBottom: 8, fontSize: 14, color: 'var(--text-muted)' }}>
        <strong>Target:</strong> {data.target_agent_name} &nbsp;|&nbsp;
        <strong>Status:</strong> <span className={`badge badge-${data.status}`}>{data.status}</span>
        {data.error && <span style={{ color: 'var(--red)', marginLeft: 8 }}>{data.error}</span>}
      </div>

      <div className="card-grid" style={{ marginBottom: 24 }}>
        <div className="card stat">
          <div className="stat-value">{data.total_tests}</div>
          <div className="stat-label">Total Tests</div>
        </div>
        <div className="card stat">
          <div className="stat-value" style={{ color: 'var(--green)' }}>{data.passed}</div>
          <div className="stat-label">Passed</div>
        </div>
        <div className="card stat">
          <div className="stat-value" style={{ color: 'var(--red)' }}>{data.failed}</div>
          <div className="stat-label">Failed</div>
        </div>
        <div className="card stat">
          <div className="stat-value" style={{ color: 'var(--yellow)' }}>{data.inconclusive}</div>
          <div className="stat-label">Inconclusive</div>
        </div>
        <div className="card stat">
          <div className="stat-value" style={{ color: 'var(--text-muted)' }}>{data.errors}</div>
          <div className="stat-label">Errors</div>
        </div>
      </div>

      {categories.map(cat => {
        const catResults = data.results.filter(r => r.category === cat)
        const catFailed = catResults.filter(r => r.verdict === 'fail').length
        return (
          <div key={cat} style={{ marginBottom: 24 }}>
            <h3 style={{ fontSize: 16, marginBottom: 8 }}>
              {cat.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
              {catFailed > 0 && <span style={{ color: 'var(--red)', fontSize: 14, marginLeft: 8 }}>
                {catFailed} finding(s)
              </span>}
            </h3>
            <div className="card">
              <table>
                <thead>
                  <tr><th>Test</th><th>Verdict</th><th>Severity</th><th>Time</th><th></th></tr>
                </thead>
                <tbody>
                  {catResults.map(r => (
                    <>
                      <tr key={r.test_case_id} style={{ cursor: 'pointer' }}
                        onClick={() => setExpandedTest(expandedTest === r.test_case_id ? null : r.test_case_id)}>
                        <td>{r.test_case_name || r.test_case_id}</td>
                        <td><VerdictBadge verdict={r.verdict} /></td>
                        <td><SeverityBadge severity={r.severity} /></td>
                        <td>{r.execution_time_ms.toFixed(0)}ms</td>
                        <td style={{ color: 'var(--text-muted)' }}>{expandedTest === r.test_case_id ? '▲' : '▼'}</td>
                      </tr>
                      {expandedTest === r.test_case_id && (
                        <tr key={`${r.test_case_id}-detail`}>
                          <td colSpan={5} style={{ background: 'var(--bg)', padding: 16 }}>
                            <FindingDetail result={r} />
                          </td>
                        </tr>
                      )}
                    </>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )
      })}
    </div>
  )
}

function FindingDetail({ result }: { result: TestResultOut }) {
  return (
    <dl className="finding-body">
      {result.reasoning && <>
        <dt>Reasoning</dt>
        <dd>{result.reasoning}</dd>
      </>}
      {result.evidence && <>
        <dt>Evidence</dt>
        <dd style={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace', fontSize: 13 }}>{result.evidence}</dd>
      </>}
      {result.error && <>
        <dt>Error</dt>
        <dd style={{ color: 'var(--red)' }}>{result.error}</dd>
      </>}
    </dl>
  )
}
