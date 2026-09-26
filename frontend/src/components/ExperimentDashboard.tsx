import React, { useState, useEffect } from 'react';
import { runExperiment, listExperiments } from '../services/api';
import { ExperimentRunRecord } from '../types';
import { Play, BarChart3, FlaskConical, Gauge } from 'lucide-react';

export const ExperimentDashboard: React.FC = () => {
  const [selectedDataset, setSelectedDataset] = useState('custom');
  const [selectedBaseline, setSelectedBaseline] = useState('proposed');
  const [loading, setLoading] = useState(false);
  const [currentRun, setCurrentRun] = useState<ExperimentRunRecord | null>(null);
  const [pastRuns, setPastRuns] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  const loadPastRuns = () => {
    listExperiments()
      .then((data) => setPastRuns(data.experiments))
      .catch(() => {});
  };

  useEffect(() => {
    loadPastRuns();
  }, []);

  const handleRunExperiment = async () => {
    setLoading(true);
    setError(null);
    try {
      const record = await runExperiment(selectedDataset, selectedBaseline);
      setCurrentRun(record);
      loadPastRuns();
    } catch (err: any) {
      setError(err.message || 'Experiment run failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Configuration & Controls */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 backdrop-blur space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h2 className="text-base font-semibold text-white flex items-center gap-2">
              <FlaskConical className="w-5 h-5 text-indigo-400" />
              Empirical Evaluation & Ablation Suite
            </h2>
            <p className="text-xs text-slate-400">
              Run benchmark experiments to evaluate logical validity, contradiction F1, and proof accuracy.
            </p>
          </div>

          <button
            onClick={handleRunExperiment}
            disabled={loading}
            className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-xs font-semibold px-5 py-2.5 rounded-lg transition-all shadow-lg shadow-indigo-600/20"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <span className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                Evaluating...
              </span>
            ) : (
              <>
                <Play className="w-4 h-4" /> Run Benchmark Evaluation
              </>
            )}
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
          <div>
            <label className="text-xs text-slate-400 block mb-1">Target Benchmark Dataset:</label>
            <select
              value={selectedDataset}
              onChange={(e) => setSelectedDataset(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 text-xs text-slate-200 rounded-lg p-2.5 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            >
              <option value="custom">Custom Diagnostic Suite (6 test categories)</option>
              <option value="ruletaker">RuleTaker (Reasoning depth benchmarks)</option>
              <option value="proofwriter">ProofWriter (Multi-hop proof chains)</option>
              <option value="folio">FOLIO (First-Order Logic translation)</option>
            </select>
          </div>

          <div>
            <label className="text-xs text-slate-400 block mb-1">Baseline or Ablation Variant:</label>
            <select
              value={selectedBaseline}
              onChange={(e) => setSelectedBaseline(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 text-xs text-slate-200 rounded-lg p-2.5 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            >
              <optgroup label="Core Pipeline">
                <option value="proposed">Proposed: Neuro-Symbolic Verified Pipeline</option>
              </optgroup>
              <optgroup label="Baselines">
                <option value="baseline_a">Baseline A: LLM Direct Zero-Shot</option>
                <option value="baseline_b">Baseline B: LLM + Chain-of-Thought</option>
                <option value="baseline_c">Baseline C: LLM -&gt; Unvalidated Solver</option>
                <option value="baseline_d">Baseline D: LLM -&gt; Solver with Feedback</option>
              </optgroup>
              <optgroup label="Ablations">
                <option value="ablation_b">Ablation B: Without Representation Validation</option>
                <option value="ablation_c">Ablation C: Without Contradiction Analysis</option>
                <option value="ablation_d">Ablation D: Without Proof Validation</option>
                <option value="ablation_e">Ablation E: Without Proof-Grounded XAI</option>
                <option value="ablation_f">Ablation F: Without Symbolic Verification</option>
              </optgroup>
            </select>
          </div>
        </div>

        {error && (
          <div className="p-3 bg-red-950/60 border border-red-800 rounded-lg text-xs text-red-300">
            {error}
          </div>
        )}
      </div>

      {/* Metrics Cards */}
      {currentRun && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <Gauge className="w-4 h-4 text-emerald-400" />
              Latest Experiment Telemetry ({currentRun.experiment_id})
            </h3>
            <span className="text-xs font-mono bg-slate-800 text-slate-300 px-2.5 py-1 rounded border border-slate-700">
              Dataset: {currentRun.dataset} | Mode: {currentRun.baseline}
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="bg-slate-900/40 border border-slate-800 p-4 rounded-xl">
              <span className="text-xs text-slate-400 block mb-1">Answer Accuracy</span>
              <span className="text-2xl font-bold font-mono text-emerald-400">
                {(currentRun.metrics.answer_accuracy * 100).toFixed(1)}%
              </span>
            </div>

            <div className="bg-slate-900/40 border border-slate-800 p-4 rounded-xl">
              <span className="text-xs text-slate-400 block mb-1">Contradiction F1</span>
              <span className="text-2xl font-bold font-mono text-indigo-400">
                {(currentRun.metrics.contradiction_f1 * 100).toFixed(1)}%
              </span>
            </div>

            <div className="bg-slate-900/40 border border-slate-800 p-4 rounded-xl">
              <span className="text-xs text-slate-400 block mb-1">Unknown Accuracy</span>
              <span className="text-2xl font-bold font-mono text-amber-400">
                {(currentRun.metrics.unknown_accuracy * 100).toFixed(1)}%
              </span>
            </div>

            <div className="bg-slate-900/40 border border-slate-800 p-4 rounded-xl">
              <span className="text-xs text-slate-400 block mb-1">Proof Accuracy</span>
              <span className="text-2xl font-bold font-mono text-purple-400">
                {(currentRun.metrics.proof_accuracy * 100).toFixed(1)}%
              </span>
            </div>

            <div className="bg-slate-900/40 border border-slate-800 p-4 rounded-xl">
              <span className="text-xs text-slate-400 block mb-1">Logical Validity</span>
              <span className="text-2xl font-bold font-mono text-sky-400">
                {(currentRun.metrics.logical_validity * 100).toFixed(1)}%
              </span>
            </div>

            <div className="bg-slate-900/40 border border-slate-800 p-4 rounded-xl">
              <span className="text-xs text-slate-400 block mb-1">Unsupported Rate</span>
              <span className="text-2xl font-bold font-mono text-rose-400">
                {(currentRun.metrics.unsupported_conclusion_rate * 100).toFixed(1)}%
              </span>
            </div>

            <div className="bg-slate-900/40 border border-slate-800 p-4 rounded-xl">
              <span className="text-xs text-slate-400 block mb-1">XAI Faithfulness</span>
              <span className="text-2xl font-bold font-mono text-teal-400">
                {(currentRun.metrics.explanation_faithfulness * 100).toFixed(1)}%
              </span>
            </div>

            <div className="bg-slate-900/40 border border-slate-800 p-4 rounded-xl">
              <span className="text-xs text-slate-400 block mb-1">Avg Latency</span>
              <span className="text-2xl font-bold font-mono text-slate-200">
                {currentRun.metrics.average_latency_ms} ms
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Historical Runs */}
      {pastRuns.length > 0 && (
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-3">
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-indigo-400" />
            Experiment Run Registry
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-slate-950 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                <tr>
                  <th className="p-3">Run ID</th>
                  <th className="p-3">Dataset</th>
                  <th className="p-3">Variant / Baseline</th>
                  <th className="p-3">Accuracy</th>
                  <th className="p-3">Contradiction F1</th>
                  <th className="p-3">Timestamp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-300">
                {pastRuns.slice(0, 8).map((r, i) => (
                  <tr key={i} className="hover:bg-slate-800/30">
                    <td className="p-3 font-semibold text-indigo-400">{r.experiment_id}</td>
                    <td className="p-3">{r.dataset}</td>
                    <td className="p-3 font-semibold text-slate-200">{r.baseline}</td>
                    <td className="p-3 text-emerald-400">{(r.accuracy * 100).toFixed(1)}%</td>
                    <td className="p-3 text-indigo-300">{(r.f1 * 100).toFixed(1)}%</td>
                    <td className="p-3 text-slate-500">{new Date(r.timestamp).toLocaleTimeString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
