import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../services/api'
import type { ReportResponse } from '../types'

export function ReportView() {
  const { runId } = useParams<{ runId: string }>()
  const [format, setFormat] = useState<'json' | 'markdown'>('json')
  const [report, setReport] = useState<ReportResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!runId) return
    setLoading(true)
    api.getReport(runId, format)
      .then(setReport)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [runId, format])

  const handleDownload = () => {
    if (!report) return
    const content = typeof report.content === 'string'
      ? report.content
      : JSON.stringify(report.content, null, 2)
    const ext = format === 'markdown' ? 'md' : 'json'
    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `agentshield-report-${runId?.slice(0, 12)}.${ext}`
    a.click()
    URL.revokeObjectURL(url)
  }

  if (loading) return <div className="loading">Loading report...</div>
  if (error) return <div className="error-msg">{error}</div>
  if (!report) return <div className="error-msg">Report not found</div>

  const content = typeof report.content === 'string'
    ? report.content
    : JSON.stringify(report.content, null, 2)

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <h2>Evaluation Report</h2>
        <div style={{ display: 'flex', gap: 8 }}>
          <button
            className={`btn ${format === 'json' ? 'btn-primary' : ''}`}
            onClick={() => setFormat('json')}
          >JSON</button>
          <button
            className={`btn ${format === 'markdown' ? 'btn-primary' : ''}`}
            onClick={() => setFormat('markdown')}
          >Markdown</button>
          <button className="btn" onClick={handleDownload}>Download</button>
          <Link to={`/evaluations/${runId}`} className="btn">Results</Link>
          <Link to="/" className="btn">Dashboard</Link>
        </div>
      </div>

      <div className="card" style={{ maxHeight: '70vh', overflow: 'auto' }}>
        <pre style={{
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-word',
          fontSize: 13,
          lineHeight: 1.6,
          fontFamily: 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace',
        }}>
          {content}
        </pre>
      </div>
    </div>
  )
}
