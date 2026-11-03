import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../services/api'
import type { RunSummary, TestSuiteInfo } from '../types'

export function Dashboard() {
  const [runs, setRuns] = useState<RunSummary[]>([])
  const [suites, setSuites] = useState<TestSuiteInfo[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([api.listEvaluations(), api.listSuites()])
      .then(([r, s]) => { setRuns(r); setSuites(s) })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="loading">Loading...</div>
  if (error) return <div className="error-msg">{error}</div>

  const totalTests = suites.reduce((a, s) => a + s.test_count, 0)
  const completedRuns = runs.filter(r => r.status === 'completed')

  return (
    <div>
      <h2>Dashboard</h2>

      <div className="card-grid">
        <div className="card stat">
          <div className="stat-value">{suites.length}</div>
          <div className="stat-label">Test Suites</div>
        </div>
        <div className="card stat">
          <div className="stat-value">{totalTests}</div>
          <div className="stat-label">Test Cases</div>
        </div>
        <div className="card stat">
          <div className="stat-value">{runs.length}</div>
          <div className="stat-label">Evaluations</div>
        </div>
        <div className="card stat">
          <div className="stat-value">{completedRuns.length}</div>
          <div className="stat-label">Completed</div>
        </div>
      </div>

      <h3 style={{ marginBottom: 12 }}>Test Suites</h3>
      <div className="card" style={{ marginBottom: 24 }}>
        <table>
          <thead>
            <tr><th>Suite</th><th>Category</th><th>Tests</th></tr>
          </thead>
          <tbody>
            {suites.map(s => (
              <tr key={s.id}>
                <td>{s.name}</td>
                <td><span className="badge badge-low">{s.category}</span></td>
                <td>{s.test_count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h3 style={{ marginBottom: 12 }}>Recent Evaluations</h3>
      {runs.length === 0 ? (
        <div className="empty-state">
          <h3>No evaluations yet</h3>
          <p>Run your first evaluation to see results here.</p>
          <Link to="/evaluate" className="btn btn-primary" style={{ marginTop: 12 }}>
            New Evaluation
          </Link>
        </div>
      ) : (
        <div className="card">
          <table>
            <thead>
              <tr><th>Run ID</th><th>Target</th><th>Status</th><th>Tests</th><th>Started</th><th></th></tr>
            </thead>
            <tbody>
              {runs.map(r => (
                <tr key={r.run_id}>
                  <td><code>{r.run_id.slice(0, 16)}</code></td>
                  <td>{r.target_agent_name}</td>
                  <td><span className={`badge badge-${r.status}`}>{r.status}</span></td>
                  <td>{r.completed_tests}/{r.total_tests}</td>
                  <td>{r.started_at ? new Date(r.started_at).toLocaleString() : '—'}</td>
                  <td><Link to={`/evaluations/${r.run_id}`}>View</Link></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
