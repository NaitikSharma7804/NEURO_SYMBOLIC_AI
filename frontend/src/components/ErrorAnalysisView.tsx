import React, { useState, useEffect } from 'react';
import { fetchErrorAnalysis } from '../services/api';
import {
  Bug,
  CheckCircle2,
  ShieldAlert,
  Flame
} from 'lucide-react';

interface ErrorCase {
  case_id: string;
  category: string;
  description: string;
  premises: string[];
  query: string;
  gold_label: string;
  predicted_label: string;
  root_cause: string;
  remediation: string;
}

interface ErrorReport {
  total_evaluated: number;
  total_errors: number;
  error_rates_by_category: Record<string, number>;
  cases_by_category: Record<string, ErrorCase[]>;
  summary: string;
}

export const ErrorAnalysisView: React.FC = () => {
  const [report, setReport] = useState<ErrorReport | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [selectedCase, setSelectedCase] = useState<ErrorCase | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchErrorAnalysis()
      .then((data) => {
        setReport(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const categories = report ? Object.keys(report.cases_by_category) : [];

  const allCases: ErrorCase[] = report
    ? Object.values(report.cases_by_category).flat()
    : [];

  const displayedCases = selectedCategory === 'ALL'
    ? allCases
    : (report?.cases_by_category[selectedCategory] || []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Bug className="w-5 h-5 text-rose-400" />
              Automated Error Analysis & Diagnostic Taxonomy
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Phase 15 Error Taxonomy classifying failure cases across Formalization, Soundness, Proof, and Explanation layers.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs font-mono bg-rose-950/70 border border-rose-800/80 text-rose-300 px-3 py-1.5 rounded-lg flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-rose-400" />
              10 Formal Taxonomy Classes
            </span>
          </div>
        </div>
      </div>

      {loading && (
        <div className="p-12 text-center text-slate-400 font-mono text-sm">
          Loading diagnostic taxonomy report...
        </div>
      )}

      {error && (
        <div className="p-4 bg-rose-950/40 border border-rose-800 rounded-xl text-xs text-rose-300">
          Failed to load error analysis: {error}
        </div>
      )}

      {report && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Category Filter & Selector */}
          <div className="space-y-3">
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-1">
              Error Categories ({categories.length})
            </div>
            <button
              onClick={() => { setSelectedCategory('ALL'); setSelectedCase(null); }}
              className={`w-full text-left p-3 rounded-lg border text-xs font-mono transition-all flex items-center justify-between ${
                selectedCategory === 'ALL'
                  ? 'bg-indigo-600/20 border-indigo-500 text-indigo-300'
                  : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:border-slate-700'
              }`}
            >
              <span>ALL CATEGORIES</span>
              <span className="bg-slate-800 px-2 py-0.5 rounded text-[10px] text-slate-300">
                {allCases.length}
              </span>
            </button>
            <div className="space-y-1.5 max-h-[600px] overflow-y-auto pr-1">
              {categories.map((cat) => {
                const count = report.cases_by_category[cat]?.length || 0;
                const isSelected = selectedCategory === cat;
                return (
                  <button
                    key={cat}
                    onClick={() => { setSelectedCategory(cat); setSelectedCase(null); }}
                    className={`w-full text-left p-3 rounded-lg border text-xs font-mono transition-all flex items-center justify-between ${
                      isSelected
                        ? 'bg-rose-500/15 border-rose-500 text-rose-300 font-semibold'
                        : 'bg-slate-900/40 border-slate-800 text-slate-400 hover:border-slate-700 hover:text-slate-200'
                    }`}
                  >
                    <span className="truncate">{cat}</span>
                    <span className="bg-slate-800/80 px-2 py-0.5 rounded text-[10px] text-slate-400 ml-2">
                      {count}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Diagnostic Failure Cases List */}
          <div className="space-y-3">
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-1">
              Failure Cases ({displayedCases.length})
            </div>
            <div className="space-y-2 max-h-[600px] overflow-y-auto pr-1">
              {displayedCases.map((c) => {
                const isSelected = selectedCase?.case_id === c.case_id;
                return (
                  <div
                    key={c.case_id}
                    onClick={() => setSelectedCase(c)}
                    className={`p-4 rounded-xl border text-xs cursor-pointer transition-all ${
                      isSelected
                        ? 'bg-slate-800/90 border-indigo-500 shadow-lg shadow-indigo-950/50'
                        : 'bg-slate-900/70 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <span className="font-mono font-bold text-indigo-400 text-[11px]">
                        {c.case_id}
                      </span>
                      <span className="font-mono text-[9px] px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800">
                        {c.category}
                      </span>
                    </div>
                    <p className="text-slate-300 font-medium text-xs mb-2">
                      {c.description}
                    </p>
                    <div className="flex items-center gap-4 text-[10px] font-mono text-slate-400">
                      <span>Gold: <strong className="text-emerald-400">{c.gold_label}</strong></span>
                      <span>•</span>
                      <span>Pred: <strong className="text-rose-400">{c.predicted_label}</strong></span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Detailed Diagnosis & Remediation Panel */}
          <div className="space-y-3">
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-1">
              Root Cause & Remediation Strategy
            </div>
            {selectedCase ? (
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 text-xs">
                <div className="border-b border-slate-800 pb-3">
                  <div className="flex items-center justify-between">
                    <h3 className="font-mono font-bold text-white text-sm">
                      {selectedCase.case_id}
                    </h3>
                    <span className="font-mono text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                      {selectedCase.category}
                    </span>
                  </div>
                  <p className="text-slate-300 text-xs mt-1">
                    {selectedCase.description}
                  </p>
                </div>

                <div>
                  <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
                    Premises & Query
                  </div>
                  <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 font-mono text-[11px] text-slate-300 space-y-1">
                    {selectedCase.premises.map((p, idx) => (
                      <div key={idx} className="text-slate-400">P{idx + 1}: {p}</div>
                    ))}
                    <div className="text-indigo-300 pt-1 border-t border-slate-800 mt-1">
                      Query: {selectedCase.query}
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-2 text-center font-mono text-xs">
                  <div className="bg-emerald-950/40 border border-emerald-800/80 p-2.5 rounded-lg">
                    <span className="text-emerald-400 text-[10px] block">EXPECTED GOLD</span>
                    <strong className="text-emerald-300">{selectedCase.gold_label}</strong>
                  </div>
                  <div className="bg-rose-950/40 border border-rose-800/80 p-2.5 rounded-lg">
                    <span className="text-rose-400 text-[10px] block">ERRONEOUS PREDICTION</span>
                    <strong className="text-rose-300">{selectedCase.predicted_label}</strong>
                  </div>
                </div>

                <div>
                  <div className="text-[11px] font-semibold text-rose-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                    <Flame className="w-3.5 h-3.5 text-rose-400" />
                    Root Cause Analysis
                  </div>
                  <p className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-slate-300 leading-relaxed">
                    {selectedCase.root_cause}
                  </p>
                </div>

                <div>
                  <div className="text-[11px] font-semibold text-emerald-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    Systemic Remediation Strategy
                  </div>
                  <p className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-slate-300 leading-relaxed">
                    {selectedCase.remediation}
                  </p>
                </div>
              </div>
            ) : (
              <div className="bg-slate-900/40 border border-slate-800/80 rounded-xl p-8 text-center text-slate-500 text-xs">
                Select an error case from the list to view its root cause analysis and remediation policy.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
