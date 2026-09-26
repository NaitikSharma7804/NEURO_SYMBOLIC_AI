import React, { useEffect, useState } from 'react';
import { fetchHealth } from './services/api';
import { HealthStatus, ProofGraph } from './types';
import { Playground } from './components/Playground';
import { ProofDAGViewer } from './components/ProofDAGViewer';
import { ExperimentDashboard } from './components/ExperimentDashboard';
import { DatasetExplorer } from './components/DatasetExplorer';
import { ArchitectureView } from './components/ArchitectureView';
import {
  BrainCircuit,
  Activity,
  PlaySquare,
  GitCommit,
  FlaskConical,
  Database,
  Cpu,
  ShieldCheck
} from 'lucide-react';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'playground' | 'proof_dag' | 'experiments' | 'datasets' | 'architecture'>('playground');
  const [activeProof, setActiveProof] = useState<ProofGraph | null>(null);
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHealth()
      .then((data) => {
        setHealth(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Top Header */}
      <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur sticky top-0 z-50 px-6 py-3 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-indigo-500/10 rounded-lg border border-indigo-500/30 text-indigo-400">
            <BrainCircuit className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-base font-bold tracking-tight text-white flex items-center gap-2">
              Neuro-Symbolic Reasoning Framework
              <span className="text-[10px] font-mono bg-indigo-950 text-indigo-300 px-2 py-0.5 rounded border border-indigo-800">
                RESEARCH v0.1.0
              </span>
            </h1>
            <p className="text-xs text-slate-400">
              Deterministic Logic Grounding, Theorem Proving & Explainable AI
            </p>
          </div>
        </div>

        {/* System Health Status */}
        <div className="flex items-center space-x-4 text-xs font-mono">
          <div className="flex items-center space-x-2 bg-slate-950/80 px-3 py-1.5 rounded-full border border-slate-800">
            <Activity className={`w-3.5 h-3.5 ${health?.status === 'ok' ? 'text-emerald-400' : 'text-amber-400 animate-pulse'}`} />
            <span className="text-slate-300">
              {loading ? 'Checking...' : health?.status === 'ok' ? 'Backend Operational' : 'Offline'}
            </span>
          </div>
          <div className="hidden md:flex items-center space-x-2 bg-slate-950/80 px-3 py-1.5 rounded-full border border-slate-800 text-slate-400">
            <span>LLM: <strong className="text-sky-400">{health?.llm_provider || 'mock'}</strong></span>
            <span>•</span>
            <span>Solver: <strong className="text-violet-400">{health?.reasoning_backend || 'pure'}</strong></span>
          </div>
        </div>
      </header>

      {/* Navigation Bar */}
      <nav className="border-b border-slate-800/80 bg-slate-900/40 px-6 flex space-x-1 overflow-x-auto text-xs font-medium">
        {[
          { id: 'playground', label: 'Reasoning Playground', icon: PlaySquare },
          { id: 'proof_dag', label: 'Proof Trace & DAG', icon: GitCommit },
          { id: 'experiments', label: 'Experiments & Baselines', icon: FlaskConical },
          { id: 'datasets', label: 'Benchmark Datasets', icon: Database },
          { id: 'architecture', label: 'Architecture & Theory', icon: Cpu },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 py-3 px-4 border-b-2 transition-all whitespace-nowrap ${
                isActive
                  ? 'border-indigo-500 text-indigo-300 bg-indigo-500/5 font-semibold'
                  : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-indigo-400' : 'text-slate-500'}`} />
              {tab.label}
            </button>
          );
        })}
      </nav>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6">
        {error && (
          <div className="mb-6 p-4 bg-amber-950/40 border border-amber-800/80 rounded-xl text-xs text-amber-300 flex items-center justify-between">
            <span>Notice: Unable to connect to backend server ({error}). Ensure backend is running at http://127.0.0.1:8000.</span>
            <span className="font-mono text-[10px] bg-amber-900/60 px-2 py-1 rounded">Offline Mode</span>
          </div>
        )}

        {activeTab === 'playground' && (
          <Playground
            onProofGenerated={(proof) => setActiveProof(proof)}
            onNavigateToProofDAG={() => setActiveTab('proof_dag')}
          />
        )}
        {activeTab === 'proof_dag' && <ProofDAGViewer proof={activeProof} />}
        {activeTab === 'experiments' && <ExperimentDashboard />}
        {activeTab === 'datasets' && <DatasetExplorer />}
        {activeTab === 'architecture' && <ArchitectureView />}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 px-6 py-4 text-xs text-slate-500 flex flex-wrap justify-between items-center gap-4 bg-slate-900/30">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-indigo-400" />
          <span>Neuro-Symbolic AI Automated Reasoning & Theorem Proving Suite</span>
        </div>
        <div className="font-mono text-[11px] text-slate-600 flex items-center gap-4">
          <span>Three-Way OWA Logic</span>
          <span>•</span>
          <span>Zero Hallucinated Conclusion Policy</span>
          <span>•</span>
          <span>All 21 Phases Integrated</span>
        </div>
      </footer>
    </div>
  );
};

export default App;
