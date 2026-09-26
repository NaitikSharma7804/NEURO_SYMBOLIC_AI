import React, { useEffect, useState } from 'react';
import { fetchHealth } from './services/api';
import { HealthStatus } from './types';
import { ShieldCheck, Activity, BrainCircuit, Cpu, Terminal } from 'lucide-react';

export const App: React.FC = () => {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
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
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur px-6 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-indigo-500/10 rounded-lg border border-indigo-500/30 text-indigo-400">
            <BrainCircuit className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-lg font-semibold tracking-tight text-white">Neuro-Symbolic AI Reasoning Framework</h1>
            <p className="text-xs text-slate-400">Deterministic Logic Grounding & Theorem Proving</p>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-xs bg-slate-800/80 px-3 py-1.5 rounded-full border border-slate-700">
            <Activity className={`w-3.5 h-3.5 ${health?.status === 'ok' ? 'text-emerald-400' : 'text-amber-400 animate-pulse'}`} />
            <span className="text-slate-300">
              {loading ? 'Checking backend...' : health?.status === 'ok' ? 'Backend Online' : 'Connecting...'}
            </span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Status Card */}
        <div className="col-span-1 md:col-span-3 bg-slate-900/40 border border-slate-800/80 rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-indigo-400" />
              Phase 0 System Status
            </h2>
            <span className="text-xs font-mono bg-indigo-950 text-indigo-300 px-2.5 py-0.5 rounded border border-indigo-800">
              v0.1.0-alpha
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-2">
            <div className="bg-slate-950/60 border border-slate-800 p-4 rounded-lg">
              <span className="text-xs text-slate-400 block mb-1">Architecture State</span>
              <span className="text-emerald-400 font-medium text-sm">Phase 0 Initialized</span>
            </div>
            <div className="bg-slate-950/60 border border-slate-800 p-4 rounded-lg">
              <span className="text-xs text-slate-400 block mb-1">LLM Provider</span>
              <span className="text-sky-400 font-mono text-sm">{health?.llm_provider || 'mock'}</span>
            </div>
            <div className="bg-slate-950/60 border border-slate-800 p-4 rounded-lg">
              <span className="text-xs text-slate-400 block mb-1">Reasoning Backend</span>
              <span className="text-violet-400 font-mono text-sm">{health?.reasoning_backend || 'pure'}</span>
            </div>
            <div className="bg-slate-950/60 border border-slate-800 p-4 rounded-lg">
              <span className="text-xs text-slate-400 block mb-1">Symbolic Grounding</span>
              <span className="text-indigo-400 font-medium text-sm">Deterministic Solver</span>
            </div>
          </div>

          {error && (
            <div className="mt-4 p-3 bg-red-950/50 border border-red-800/80 rounded-lg text-xs text-red-300">
              Connection Notice: {error} (Ensure backend server is running on port 8000)
            </div>
          )}
        </div>

        {/* Pipeline Preview Card */}
        <div className="col-span-1 md:col-span-3 bg-slate-900/30 border border-slate-800 rounded-xl p-6">
          <h2 className="text-sm font-semibold uppercase tracking-wider text-slate-400 mb-4 flex items-center gap-2">
            <Cpu className="w-4 h-4 text-emerald-400" />
            Core Pipeline Architecture
          </h2>
          <div className="flex flex-wrap items-center justify-between gap-3 text-xs font-mono">
            {[
              "1. Natural Language Query",
              "2. LLM Formalization",
              "3. Representation Validator",
              "4. Knowledge Base",
              "5. Symbolic Engine",
              "6. Contradiction Analysis",
              "7. Proof Generation",
              "8. Proof Validator",
              "9. Grounded XAI"
            ].map((step, idx) => (
              <div key={idx} className="bg-slate-800/60 border border-slate-700/60 px-3 py-2 rounded-lg text-slate-200">
                {step}
              </div>
            ))}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 px-6 py-4 text-xs text-slate-500 flex justify-between items-center">
        <span>Neuro-Symbolic Automated Reasoning & Theorem Proving</span>
        <span className="font-mono flex items-center gap-1">
          <Terminal className="w-3.5 h-3.5" /> Phase 0 Verified
        </span>
      </footer>
    </div>
  );
};

export default App;
