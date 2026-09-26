import React, { useState } from 'react';
import { ProofGraph } from '../types';
import { GitCommit, ArrowDown, CornerDownRight, CheckCircle2, Sparkles } from 'lucide-react';

const DEFAULT_PROOF_PRESETS: { name: string; description: string; proof: ProofGraph }[] = [
  {
    name: 'Socrates Entailment (Depth 1)',
    description: 'Classic deduction from base axiom and universal mortal rule',
    proof: {
      goal: 'mortal(socrates)',
      status: 'verified',
      depth: 1,
      is_valid: true,
      validation_errors: [],
      steps: [
        { id: 1, type: 'FACT', statement: 'human(socrates)', from_steps: [], depth: 0 },
        { id: 2, type: 'RULE', statement: 'human(X) -> mortal(X)', from_steps: [], depth: 0 },
        {
          id: 3,
          type: 'INFERENCE',
          statement: 'mortal(socrates)',
          from_steps: [1, 2],
          rule_applied: 'human(X) -> mortal(X)',
          substitutions: { X: 'socrates' },
          depth: 1
        }
      ]
    }
  },
  {
    name: 'Alice Multi-Hop (Depth 2)',
    description: 'Two-tier chaining: student(alice) -> person(alice) -> mortal(alice)',
    proof: {
      goal: 'mortal(alice)',
      status: 'verified',
      depth: 2,
      is_valid: true,
      validation_errors: [],
      steps: [
        { id: 1, type: 'FACT', statement: 'student(alice)', from_steps: [], depth: 0 },
        { id: 2, type: 'RULE', statement: 'student(X) -> person(X)', from_steps: [], depth: 0 },
        {
          id: 3,
          type: 'INFERENCE',
          statement: 'person(alice)',
          from_steps: [1, 2],
          rule_applied: 'student(X) -> person(X)',
          substitutions: { X: 'alice' },
          depth: 1
        },
        { id: 4, type: 'RULE', statement: 'person(X) -> mortal(X)', from_steps: [], depth: 0 },
        {
          id: 5,
          type: 'INFERENCE',
          statement: 'mortal(alice)',
          from_steps: [3, 4],
          rule_applied: 'person(X) -> mortal(X)',
          substitutions: { X: 'alice' },
          depth: 2
        }
      ]
    }
  },
  {
    name: 'Penguin Contradiction (Depth 1)',
    description: 'Explicit negation proof deriving not flies(tweety)',
    proof: {
      goal: 'not flies(tweety)',
      status: 'verified',
      depth: 1,
      is_valid: true,
      validation_errors: [],
      steps: [
        { id: 1, type: 'FACT', statement: 'penguin(tweety)', from_steps: [], depth: 0 },
        { id: 2, type: 'RULE', statement: 'penguin(X) -> not flies(X)', from_steps: [], depth: 0 },
        {
          id: 3,
          type: 'INFERENCE',
          statement: 'not flies(tweety)',
          from_steps: [1, 2],
          rule_applied: 'penguin(X) -> not flies(X)',
          substitutions: { X: 'tweety' },
          depth: 1
        }
      ]
    }
  },
  {
    name: 'Multi-Variable Grandparent (Depth 1)',
    description: 'Multi-variable unification: parent(john, mary) & parent(mary, alice) -> grandparent(john, alice)',
    proof: {
      goal: 'grandparent(john, alice)',
      status: 'verified',
      depth: 1,
      is_valid: true,
      validation_errors: [],
      steps: [
        { id: 1, type: 'FACT', statement: 'parent(john, mary)', from_steps: [], depth: 0 },
        { id: 2, type: 'FACT', statement: 'parent(mary, alice)', from_steps: [], depth: 0 },
        { id: 3, type: 'RULE', statement: 'parent(X, Y) & parent(Y, Z) -> grandparent(X, Z)', from_steps: [], depth: 0 },
        {
          id: 4,
          type: 'INFERENCE',
          statement: 'grandparent(john, alice)',
          from_steps: [1, 2, 3],
          rule_applied: 'parent(X, Y) & parent(Y, Z) -> grandparent(X, Z)',
          substitutions: { X: 'john', Y: 'mary', Z: 'alice' },
          depth: 1
        }
      ]
    }
  }
];

interface ProofDAGViewerProps {
  proof?: ProofGraph | null;
}

export const ProofDAGViewer: React.FC<ProofDAGViewerProps> = ({ proof: incomingProof }) => {
  const [selectedProof, setSelectedProof] = useState<ProofGraph>(
    incomingProof && incomingProof.steps.length > 0 ? incomingProof : DEFAULT_PROOF_PRESETS[0].proof
  );

  const activeProof = incomingProof && incomingProof.steps.length > 0 ? incomingProof : selectedProof;

  // Group steps by depth
  const stepsByDepth: Record<number, typeof activeProof.steps> = {};
  activeProof.steps.forEach((s) => {
    const d = s.depth || 0;
    if (!stepsByDepth[d]) stepsByDepth[d] = [];
    stepsByDepth[d].push(s);
  });

  const sortedDepths = Object.keys(stepsByDepth).map(Number).sort((a, b) => a - b);

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-6">
      {/* Header & Controls */}
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
          <span className="bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800 text-slate-300">
            Goal: <strong className="text-indigo-300">{activeProof.goal}</strong>
          </span>
          <span className="bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800 text-slate-300">
            Total Depth: <strong className="text-emerald-300">{activeProof.depth}</strong>
          </span>
          <span className="bg-emerald-950/60 text-emerald-300 border border-emerald-800 px-3 py-1.5 rounded-lg font-semibold flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            VERIFIED PROOF
          </span>
        </div>
      </div>

      {/* Proof Presets Selector */}
      <div className="bg-slate-950/80 border border-slate-800 p-4 rounded-xl space-y-2">
        <div className="text-xs font-semibold text-slate-400 flex items-center gap-2">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
          Select a Precomputed Proof DAG or view your Playground execution:
        </div>
        <div className="flex flex-wrap gap-2">
          {DEFAULT_PROOF_PRESETS.map((preset, idx) => (
            <button
              key={idx}
              onClick={() => setSelectedProof(preset.proof)}
              className={`text-xs px-3 py-1.5 rounded-lg border font-mono transition-all ${
                activeProof.goal === preset.proof.goal && activeProof.steps.length === preset.proof.steps.length
                  ? 'bg-indigo-600 border-indigo-500 text-white font-semibold shadow-md shadow-indigo-600/20'
                  : 'bg-slate-900 border-slate-700 text-slate-300 hover:border-slate-500'
              }`}
            >
              {preset.name}
            </button>
          ))}
          {incomingProof && incomingProof.steps.length > 0 && (
            <button
              onClick={() => setSelectedProof(incomingProof)}
              className={`text-xs px-3 py-1.5 rounded-lg border font-mono transition-all ${
                activeProof === incomingProof
                  ? 'bg-indigo-600 border-indigo-500 text-white font-semibold'
                  : 'bg-slate-900 border-indigo-800 text-indigo-300 hover:border-indigo-600'
              }`}
            >
              Latest Playground Query ({incomingProof.goal})
            </button>
          )}
        </div>
      </div>

      {/* Hierarchical DAG View */}
      <div className="space-y-8 pt-2">
        {sortedDepths.map((depth) => (
          <div key={depth} className="relative">
            <div className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-indigo-500 shadow-sm shadow-indigo-500/50" />
              <span className="font-semibold text-slate-200">
                Tier {depth} {depth === 0 ? '(Axiomatic Ground Facts & Deductive Rules)' : `(Deductive Hop ${depth})`}
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {stepsByDepth[depth].map((step) => (
                <div
                  key={step.id}
                  className={`p-4 rounded-xl border transition-all ${
                    step.type === 'FACT'
                      ? 'bg-sky-950/20 border-sky-800/80 hover:border-sky-600 shadow-sm'
                      : step.type === 'RULE'
                      ? 'bg-purple-950/20 border-purple-800/80 hover:border-purple-600 shadow-sm'
                      : 'bg-emerald-950/20 border-emerald-800/80 hover:border-emerald-600 shadow-sm'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-bold font-mono text-indigo-400">Step #{step.id}</span>
                    <span
                      className={`text-[10px] font-mono px-2 py-0.5 rounded border uppercase font-semibold ${
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
                    <div className="text-[11px] text-slate-400 font-mono mt-1">
                      Unification: θ = {JSON.stringify(step.substitutions)}
                    </div>
                  )}
                </div>
              ))}
            </div>

            {depth < sortedDepths[sortedDepths.length - 1] && (
              <div className="flex justify-center my-4">
                <ArrowDown className="w-5 h-5 text-indigo-400/80 animate-bounce" />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
