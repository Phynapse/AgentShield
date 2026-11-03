import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import { Dashboard } from './pages/Dashboard'
import { NewEvaluation } from './pages/NewEvaluation'
import { EvaluationResults } from './pages/EvaluationResults'
import { ReportView } from './pages/ReportView'
import './index.css'

function App() {
  return (
    <BrowserRouter>
      <header className="app-header">
        <div className="container">
          <h1>AgentShield</h1>
          <nav>
            <NavLink to="/" end>Dashboard</NavLink>
            <NavLink to="/evaluate">New Evaluation</NavLink>
          </nav>
        </div>
      </header>
      <main className="container page">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/evaluate" element={<NewEvaluation />} />
          <Route path="/evaluations/:runId" element={<EvaluationResults />} />
          <Route path="/evaluations/:runId/report" element={<ReportView />} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}

export default App
