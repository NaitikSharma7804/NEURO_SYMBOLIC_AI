import React from 'react';
import { ProofGraph } from '../types';
import { GitCommit, ArrowDown, CornerDownRight } from 'lucide-react';

interface ProofDAGViewerProps {
  proof?: ProofGraph;
}

export const ProofDAGViewer: React.FC<ProofDAGViewerProps> = ({ proof }) => {
  if (!proof || proof.steps.length === 0) {
    return (
      <div className="bg-slate-900/40 border border-slate-800 rounded-xl p-8 text-center text-slate-400">
        <GitCommit className="w-10 h-10 mx-auto mb-3 text-slate-600 animate-pulse" />
        <h3 className="text-sm font-semibold text-slate-300 mb-1">No Active Proof DAG</h3>
        <p className="text-xs text-slate-500 max-w-sm mx-auto">
          Execute a query in the Reasoning Playground to generate and inspect its interactive deductive proof graph.
        </p>
      </div>
    );
  }

  // Group steps by depth
  const stepsByDepth: Record<number, typeof proof.steps> = {};
  proof.steps.forEach((s) => {
    const d = s.depth || 0;
    if (!stepsByDepth[d]) stepsByDepth[d] = [];
    stepsByDepth[d].push(s);
  });

  const sortedDepths = Object.keys(stepsByDepth).map(Number).sort((a, b) => a - b);

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-base font-semibold text-white flex items-center gap-2">
            <GitCommit className="w-5 h-5 text-indigo-400" />
            Proof Trace DAG Visualization
          </h2>
          <p className="text-xs text-slate-400">
            Topological derivation hierarchy from ground premises to theorem target.
          </p>
        </div>
        <div className="flex items-center gap-3 text-xs font-mono">
          <span className="bg-slate-800 px-3 py-1 rounded border border-slate-700 text-slate-300">
            Goal: <strong className="text-indigo-300">{proof.goal}</strong>
          </span>
          <span className="bg-slate-800 px-3 py-1 rounded border border-slate-700 text-slate-300">
            Total Depth: <strong className="text-emerald-300">{proof.depth}</strong>
          </span>
        </div>
      </div>

      {/* Hierarchical DAG View */}
      <div className="space-y-8">
        {sortedDepths.map((depth) => (
          <div key={depth} className="relative">
            <div className="text-xs font-mono uppercase tracking-wider text-slate-500 mb-3 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-indigo-500" />
              Tier {depth} {depth === 0 ? '(Base Axioms & Rules)' : `(Inference Hop ${depth})`}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {stepsByDepth[depth].map((step) => (
                <div
                  key={step.id}
                  className={`p-4 rounded-xl border transition-all ${
                    step.type === 'FACT'
                      ? 'bg-sky-950/20 border-sky-800/80 hover:border-sky-600'
                      : step.type === 'RULE'
                      ? 'bg-purple-950/20 border-purple-800/80 hover:border-purple-600'
                      : 'bg-emerald-950/20 border-emerald-800/80 hover:border-emerald-600'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-bold font-mono text-indigo-400">Step #{step.id}</span>
                    <span
                      className={`text-[10px] font-mono px-2 py-0.5 rounded border uppercase ${
                        step.type === 'FACT'
                          ? 'bg-sky-950 text-sky-300 border-sky-700'
                          : step.type === 'RULE'
                          ? 'bg-purple-950 text-purple-300 border-purple-700'
                          : 'bg-emerald-950 text-emerald-300 border-emerald-700'
                      }`}
                    >
                      {step.type}
                    </span>
                  </div>

                  <div className="text-sm font-mono font-semibold text-slate-100 mb-2">
                    {step.statement}
                  </div>

                  {step.from_steps && step.from_steps.length > 0 && (
                    <div className="text-xs text-slate-400 font-mono flex items-center gap-1 mt-2 pt-2 border-t border-slate-800/60">
                      <CornerDownRight className="w-3.5 h-3.5 text-indigo-400" />
                      <span>Derived from: [{step.from_steps.join(', ')}]</span>
                    </div>
                  )}

                  {step.substitutions && Object.keys(step.substitutions).length > 0 && (
                    <div className="text-[11px] text-slate-500 font-mono mt-1">
                      θ = {JSON.stringify(step.substitutions)}
                    </div>
                  )}
                </div>
              ))}
            </div>

            {depth < sortedDepths[sortedDepths.length - 1] && (
              <div className="flex justify-center my-4">
                <ArrowDown className="w-5 h-5 text-slate-600 animate-bounce" />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
