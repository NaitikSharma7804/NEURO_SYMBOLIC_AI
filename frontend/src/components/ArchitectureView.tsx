import React from 'react';
import { Cpu, ShieldCheck, Network } from 'lucide-react';

export const ArchitectureView: React.FC = () => {
  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 backdrop-blur">
        <h2 className="text-base font-semibold text-white flex items-center gap-2 mb-1">
          <Cpu className="w-5 h-5 text-indigo-400" />
          Neuro-Symbolic Framework Architecture & Theoretical Foundation
        </h2>
        <p className="text-xs text-slate-400">
          Formal decoupling of natural-language translation from deterministic symbolic reasoning and independent verification.
        </p>
      </div>

      {/* 9-Stage Pipeline Flow */}
      <div className="bg-slate-900/40 border border-slate-800 rounded-xl p-6 space-y-4">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-2">
          <Network className="w-4 h-4 text-emerald-400" />
          End-to-End Reasoning Pipeline Flow
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs font-mono">
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <span className="text-indigo-400 font-bold">STAGE 1: TRANSLATION</span>
            <div className="text-slate-200 font-semibold">LLM Natural Language Understanding</div>
            <p className="text-slate-500 font-sans text-[11px]">
              Extracts facts, rules, variables, and query propositions into strict JSON abstract syntax trees.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <span className="text-amber-400 font-bold">STAGE 2: VALIDATION</span>
            <div className="text-slate-200 font-semibold">Representation Validator & Recovery</div>
            <p className="text-slate-500 font-sans text-[11px]">
              Detects unbound head variables, malformed negation, and arity mismatches with bounded correction loops.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <span className="text-emerald-400 font-bold">STAGE 3: GROUNDING</span>
            <div className="text-slate-200 font-semibold">Deterministic Symbolic Engine</div>
            <p className="text-slate-500 font-sans text-[11px]">
              Forward chaining over definite clauses computes deductive closure to fixed point with cycle termination.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <span className="text-rose-400 font-bold">STAGE 4: DUAL ANALYSIS</span>
            <div className="text-slate-200 font-semibold">Contradiction & Open-World Check</div>
            <p className="text-slate-500 font-sans text-[11px]">
              Evaluates both Q and ¬Q separately to detect explicit refutation or knowledge base conflicts.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <span className="text-purple-400 font-bold">STAGE 5: PROOF ENGINE</span>
            <div className="text-slate-200 font-semibold">Topological DAG Generation</div>
            <p className="text-slate-500 font-sans text-[11px]">
              Backtraces provenance from goals to axioms, emitting step-by-step DAG derivation nodes.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <span className="text-teal-400 font-bold">STAGE 6: INDEPENDENT CHECK</span>
            <div className="text-slate-200 font-semibold">Independent Proof Validator</div>
            <p className="text-slate-500 font-sans text-[11px]">
              Independently verifies every premise existence, substitution binding, and conclusion soundly.
            </p>
          </div>
        </div>
      </div>

      {/* Contradiction Semantics Matrix */}
      <div className="bg-slate-900/40 border border-slate-800 rounded-xl p-6 space-y-4">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-indigo-400" />
          Three-Way Open-World Assumption (OWA) Truth Table
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-slate-950 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
              <tr>
                <th className="p-3">Query Q Provable</th>
                <th className="p-3">Opposite ¬Q Provable</th>
                <th className="p-3">Classification</th>
                <th className="p-3">Conflict Detected</th>
                <th className="p-3 font-sans">Semantics & Provenance Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              <tr className="bg-emerald-950/10">
                <td className="p-3 text-emerald-400 font-bold">TRUE</td>
                <td className="p-3 text-slate-500">FALSE</td>
                <td className="p-3 text-emerald-400 font-bold">ENTAILED</td>
                <td className="p-3 text-slate-500">FALSE</td>
                <td className="p-3 font-sans text-slate-300">
                  Monotonically established from knowledge base. Valid proof DAG generated.
                </td>
              </tr>
              <tr className="bg-rose-950/10">
                <td className="p-3 text-slate-500">FALSE</td>
                <td className="p-3 text-rose-400 font-bold">TRUE</td>
                <td className="p-3 text-rose-400 font-bold">CONTRADICTED</td>
                <td className="p-3 text-slate-500">FALSE</td>
                <td className="p-3 font-sans text-slate-300">
                  Explicit counter-evidence established. Proof DAG for ¬Q provided.
                </td>
              </tr>
              <tr className="bg-rose-950/20">
                <td className="p-3 text-rose-400 font-bold">TRUE</td>
                <td className="p-3 text-rose-400 font-bold">TRUE</td>
                <td className="p-3 text-rose-400 font-bold">CONTRADICTED</td>
                <td className="p-3 text-rose-300 font-bold">TRUE (CONFLICT)</td>
                <td className="p-3 font-sans text-rose-200">
                  Inconsistent premises: both Q and ¬Q derivable. Both proof traces preserved.
                </td>
              </tr>
              <tr className="bg-amber-950/10">
                <td className="p-3 text-slate-500">FALSE</td>
                <td className="p-3 text-slate-500">FALSE</td>
                <td className="p-3 text-amber-400 font-bold">UNKNOWN</td>
                <td className="p-3 text-slate-500">FALSE</td>
                <td className="p-3 font-sans text-slate-300">
                  Neither Q nor ¬Q derivable. Open-world assumption avoids false negative bias.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
