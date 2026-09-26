import React, { useState } from 'react';
import { executeReason } from '../services/api';
import { ReasoningResponse, ExplanationMode, ProofGraph } from '../types';
import {
  Play,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Brain,
  FileCode,
  Layers,
  Sparkles,
  Timer,
  Info
} from 'lucide-react';

const PRESETS = [
  {
    title: 'Scenario 1: Simple Entailment',
    text: 'All humans are mortal.\nSocrates is human.\nIs Socrates mortal?',
  },
  {
    title: 'Scenario 2: Unknown / Open-World',
    text: 'Tweety is a bird.\nDoes Tweety fly?',
  },
  {
    title: 'Scenario 3: Explicit Contradiction',
    text: 'Penguins do not fly.\nTweety is a penguin.\nDoes Tweety fly?',
  },
  {
    title: 'Scenario 4: Multi-Hop Reasoning',
    text: 'Alice is a student.\nStudents are people.\nPeople are mortal.\nIs Alice mortal?',
  },
  {
    title: 'Scenario 5: Conflicting Knowledge',
    text: 'Tweety is a bird.\nBirds fly.\nTweety does not fly.\nDoes Tweety fly?',
  },
];

interface PlaygroundProps {
  initialQuery?: string;
  onProofGenerated?: (proof: ProofGraph) => void;
  onNavigateToProofDAG?: () => void;
}

export const Playground: React.FC<PlaygroundProps> = ({ initialQuery, onProofGenerated, onNavigateToProofDAG }) => {
  const [queryText, setQueryText] = useState(initialQuery || PRESETS[0].text);
  const [mode, setMode] = useState<ExplanationMode>('DETAILED');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<ReasoningResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  React.useEffect(() => {
    if (initialQuery) {
      setQueryText(initialQuery);
    }
  }, [initialQuery]);

  const handleRun = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await executeReason(queryText, mode);
      setResponse(res);
      if (res.proof && res.proof.steps.length > 0) {
        onProofGenerated?.(res.proof);
      }
    } catch (err: any) {
      setError(err.message || 'Reasoning pipeline execution failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Input & Presets Section */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 backdrop-blur">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
          <div>
            <h2 className="text-base font-semibold text-white flex items-center gap-2">
              <Brain className="w-5 h-5 text-indigo-400" />
              Neuro-Symbolic Reasoning Playground
            </h2>
            <p className="text-xs text-slate-400">
              Enter natural-language premises and query. The LLM translates; the deterministic engine proves.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400">Explanation Mode:</span>
            <select
              value={mode}
              onChange={(e) => setMode(e.target.value as ExplanationMode)}
              className="bg-slate-950 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            >
              <option value="SHORT">SHORT</option>
              <option value="DETAILED">DETAILED</option>
              <option value="STEP_BY_STEP">STEP_BY_STEP</option>
              <option value="TECHNICAL">TECHNICAL</option>
            </select>
          </div>
        </div>

        {/* Presets */}
        <div className="flex flex-wrap gap-2 mb-4">
          {PRESETS.map((p, idx) => (
            <button
              key={idx}
              onClick={() => setQueryText(p.text)}
              className="text-xs bg-slate-800/80 hover:bg-indigo-950 hover:border-indigo-700 border border-slate-700 text-slate-300 px-3 py-1.5 rounded-lg transition-colors"
            >
              {p.title}
            </button>
          ))}
        </div>

        {/* Query Input */}
        <textarea
          rows={5}
          value={queryText}
          onChange={(e) => setQueryText(e.target.value)}
          placeholder="Enter problem premises and query..."
          className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-sm font-mono text-slate-200 focus:outline-none focus:border-indigo-500 transition-colors"
        />

        <div className="flex justify-between items-center mt-4">
          <div className="text-xs text-slate-500 flex items-center gap-1">
            <Info className="w-3.5 h-3.5" />
            Deterministic proof verification eliminates LLM hallucinated conclusions.
          </div>
          <button
            onClick={handleRun}
            disabled={loading}
            className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-xs font-semibold px-5 py-2.5 rounded-lg transition-all shadow-lg shadow-indigo-600/20"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <span className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                Reasoning...
              </span>
            ) : (
              <>
                <Play className="w-4 h-4" /> Run Neuro-Symbolic Pipeline
              </>
            )}
          </button>
        </div>

        {error && (
          <div className="mt-4 p-3 bg-red-950/60 border border-red-800 rounded-lg text-xs text-red-300">
            {error}
          </div>
        )}
      </div>

      {/* Response Results Section */}
      {response && (
        <div className="space-y-6">
          {/* Top Result Banner */}
          <div
            className={`border rounded-xl p-6 ${
              response.result === 'ENTAILED'
                ? 'bg-emerald-950/20 border-emerald-800/80 text-emerald-200'
                : response.result === 'CONTRADICTED'
                ? 'bg-rose-950/20 border-rose-800/80 text-rose-200'
                : 'bg-amber-950/20 border-amber-800/80 text-amber-200'
            }`}
          >
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                {response.result === 'ENTAILED' ? (
                  <CheckCircle2 className="w-8 h-8 text-emerald-400" />
                ) : response.result === 'CONTRADICTED' ? (
                  <XCircle className="w-8 h-8 text-rose-400" />
                ) : (
                  <AlertTriangle className="w-8 h-8 text-amber-400" />
                )}
                <div>
                  <div className="text-xs uppercase tracking-wider font-semibold opacity-80">
                    Logical Classification (Open-World Semantics)
                  </div>
                  <div className="text-2xl font-bold tracking-tight font-mono">{response.result}</div>
                </div>
              </div>

              <div className="flex items-center gap-3 text-xs font-mono">
                <div className="bg-slate-900/80 border border-slate-800 px-3 py-1.5 rounded-lg flex items-center gap-1.5">
                  <Timer className="w-3.5 h-3.5 text-indigo-400" />
                  <span>{response.metadata.latency_ms || 0} ms</span>
                </div>
                <div className="bg-slate-900/80 border border-slate-800 px-3 py-1.5 rounded-lg">
                  Backend: <span className="text-indigo-300">{response.metadata.backend}</span>
                </div>
              </div>
            </div>

            {response.contradiction?.conflict_detected && (
              <div className="mt-4 p-3 bg-red-950/70 border border-red-700/80 rounded-lg text-xs text-red-200 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-red-400 flex-shrink-0" />
                <span>
                  <strong>Conflict Detected:</strong> Both the target query and its explicit negation are derivable
                  from the provided premises. Dual proof branches have been preserved.
                </span>
              </div>
            )}

            {response.result === 'UNKNOWN' && (
              <div className="mt-4 p-3 bg-amber-950/50 border border-amber-800 rounded-lg text-xs text-amber-200">
                <strong>Open-World Assessment:</strong> The premises do not contain sufficient evidence to establish
                either the proposition or its explicit refutation. The system does not assume closed-world falsehood.
              </div>
            )}
          </div>

          {/* Grid Layout: Formalization & Proof */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Formalization & Validation */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <FileCode className="w-4 h-4 text-sky-400" />
                  Structured Logic Representation
                </h3>
                <span
                  className={`text-xs px-2.5 py-0.5 rounded border font-mono ${
                    response.validation?.valid
                      ? 'bg-emerald-950 text-emerald-300 border-emerald-800'
                      : 'bg-rose-950 text-rose-300 border-rose-800'
                  }`}
                >
                  {response.validation?.valid ? 'VALIDATED' : 'VALIDATION ERROR'}
                </span>
              </div>

              {response.formalization ? (
                <div className="bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs font-mono text-slate-300 max-h-64 overflow-y-auto">
                  <pre>{JSON.stringify(response.formalization, null, 2)}</pre>
                </div>
              ) : (
                <div className="text-xs text-slate-400">No valid formalization generated.</div>
              )}

              {response.validation?.errors && response.validation.errors.length > 0 && (
                <div className="space-y-1">
                  <span className="text-xs font-semibold text-rose-400">Validation Issues:</span>
                  {response.validation.errors.map((err, i) => (
                    <div key={i} className="text-xs bg-rose-950/40 text-rose-300 p-2 rounded border border-rose-900">
                      [{err.code}] {err.message}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Proof-Grounded Explanation */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-violet-400" />
                  Proof-Grounded Explanation ({response.explanation?.mode})
                </h3>
                <span
                  className={`text-xs px-2.5 py-0.5 rounded border font-mono ${
                    response.explanation?.is_faithful
                      ? 'bg-emerald-950 text-emerald-300 border-emerald-800'
                      : 'bg-amber-950 text-amber-300 border-amber-800'
                  }`}
                >
                  {response.explanation?.is_faithful ? 'FAITHFUL TO PROOF' : 'UNVERIFIED GROUNDING'}
                </span>
              </div>

              <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed font-sans whitespace-pre-line">
                {response.explanation?.text}
              </div>

              {response.explanation?.grounded_steps && response.explanation.grounded_steps.length > 0 && (
                <div className="text-xs text-slate-400">
                  Grounded Proof Step IDs:{' '}
                  <span className="font-mono text-indigo-300">
                    {response.explanation.grounded_steps.join(', ')}
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Proof DAG Steps Table */}
          {response.proof && response.proof.steps.length > 0 && (
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <Layers className="w-4 h-4 text-indigo-400" />
                  Deterministic Proof DAG (Depth: {response.proof.depth})
                </h3>
                <div className="flex items-center gap-2">
                  <span
                    className={`text-xs px-2.5 py-0.5 rounded border font-mono ${
                      response.proof_validation?.valid
                        ? 'bg-emerald-950 text-emerald-300 border-emerald-800'
                        : 'bg-rose-950 text-rose-300 border-rose-800'
                    }`}
                  >
                    {response.proof_validation?.valid ? 'INDEPENDENT PROOF VALIDATED' : 'PROOF INVALID'}
                  </span>
                  {onNavigateToProofDAG && (
                    <button
                      onClick={onNavigateToProofDAG}
                      className="text-xs bg-indigo-600/80 hover:bg-indigo-500 text-white font-mono px-2.5 py-1 rounded transition-colors"
                    >
                      Inspect in Proof DAG Tab →
                    </button>
                  )}
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs font-mono">
                  <thead className="bg-slate-950 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                    <tr>
                      <th className="p-3">Step</th>
                      <th className="p-3">Type</th>
                      <th className="p-3">Statement</th>
                      <th className="p-3">Derived From</th>
                      <th className="p-3">Substitutions</th>
                      <th className="p-3">Depth</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 text-slate-300">
                    {response.proof.steps.map((step) => (
                      <tr key={step.id} className="hover:bg-slate-800/30">
                        <td className="p-3 font-bold text-indigo-400">#{step.id}</td>
                        <td className="p-3">
                          <span
                            className={`px-2 py-0.5 rounded text-[10px] ${
                              step.type === 'FACT'
                                ? 'bg-sky-950 text-sky-300 border border-sky-800'
                                : step.type === 'RULE'
                                ? 'bg-purple-950 text-purple-300 border border-purple-800'
                                : 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                            }`}
                          >
                            {step.type}
                          </span>
                        </td>
                        <td className="p-3 font-semibold text-slate-100">{step.statement}</td>
                        <td className="p-3 text-slate-400">
                          {step.from_steps && step.from_steps.length > 0 ? (
                            `[${step.from_steps.join(', ')}]`
                          ) : (
                            <span className="text-slate-600">—</span>
                          )}
                        </td>
                        <td className="p-3 text-slate-400">
                          {step.substitutions && Object.keys(step.substitutions).length > 0 ? (
                            JSON.stringify(step.substitutions)
                          ) : (
                            <span className="text-slate-600">—</span>
                          )}
                        </td>
                        <td className="p-3 text-slate-400">{step.depth}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
