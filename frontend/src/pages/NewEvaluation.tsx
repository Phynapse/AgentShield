import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import type { TestSuiteInfo, EvaluationRequest } from '../types'

export function NewEvaluation() {
  const navigate = useNavigate()
  const [suites, setSuites] = useState<TestSuiteInfo[]>([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  const [name, setName] = useState('')
  const [endpoint, setEndpoint] = useState('')
  const [apiKey, setApiKey] = useState('')
  const [model, setModel] = useState('')
  const [timeout, setTimeout_] = useState(30)
  const [selectedSuites, setSelectedSuites] = useState<string[]>([])

  useEffect(() => {
    api.listSuites()
      .then(s => { setSuites(s); setSelectedSuites(s.map(x => x.id)) })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  const toggleSuite = (id: string) => {
    setSelectedSuites(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    )
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!name || !endpoint || !apiKey) {
      setError('Name, endpoint, and API key are required.')
      return
    }
    if (selectedSuites.length === 0) {
      setError('Select at least one test suite.')
      return
    }

    setSubmitting(true)
    try {
      const req: EvaluationRequest = {
        target_agent: { name, endpoint, api_key: apiKey, model, timeout_seconds: timeout },
        suite_ids: selectedSuites,
      }
      const resp = await api.createEvaluation(req)
      navigate(`/evaluations/${resp.run_id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Evaluation failed')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <div className="loading">Loading test suites...</div>

  return (
    <div>
      <h2>New Evaluation</h2>

      {error && <div className="error-msg">{error}</div>}

      <form onSubmit={handleSubmit} style={{ maxWidth: 600 }}>
        <div className="card" style={{ marginBottom: 16 }}>
          <h3 style={{ fontSize: 15, marginBottom: 12 }}>Target Agent Configuration</h3>
          <p style={{ fontSize: 13, color: 'var(--text-muted)', marginBottom: 16 }}>
            The API key is used only for this evaluation session and is not stored permanently.
          </p>

          <div className="form-group">
            <label>Agent Name</label>
            <input type="text" value={name} onChange={e => setName(e.target.value)}
              placeholder="e.g. My AI Agent" />
          </div>

          <div className="form-group">
            <label>API Endpoint</label>
            <input type="text" value={endpoint} onChange={e => setEndpoint(e.target.value)}
              placeholder="https://api.openai.com" />
          </div>

          <div className="form-group">
            <label>API Key</label>
            <input type="password" value={apiKey} onChange={e => setApiKey(e.target.value)}
              placeholder="sk-..." />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <div className="form-group">
              <label>Model (optional)</label>
              <input type="text" value={model} onChange={e => setModel(e.target.value)}
                placeholder="gpt-4o-mini" />
            </div>
            <div className="form-group">
              <label>Timeout (seconds)</label>
              <input type="number" value={timeout} onChange={e => setTimeout_(+e.target.value)}
                min={5} max={120} />
            </div>
          </div>
        </div>

        <div className="card" style={{ marginBottom: 16 }}>
          <h3 style={{ fontSize: 15, marginBottom: 12 }}>Test Suites</h3>
          <div className="checkbox-group">
            {suites.map(s => (
              <label key={s.id}>
                <input type="checkbox" checked={selectedSuites.includes(s.id)}
                  onChange={() => toggleSuite(s.id)} />
                {s.name} ({s.test_count})
              </label>
            ))}
          </div>
        </div>

        <button type="submit" className="btn btn-primary" disabled={submitting}>
          {submitting ? 'Running Evaluation...' : 'Start Evaluation'}
        </button>
      </form>
    </div>
  )
}
