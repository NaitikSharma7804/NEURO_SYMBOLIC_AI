import React, { useState, useEffect } from 'react';
import { fetchDatasets, fetchDatasetSamples } from '../services/api';
import { Database } from 'lucide-react';

export const DatasetExplorer: React.FC = () => {
  const [datasets, setDatasets] = useState<any[]>([]);
  const [selectedId, setSelectedId] = useState<string>('custom');
  const [samples, setSamples] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDatasets()
      .then((data) => {
        setDatasets(data.datasets);
        loadSamples(selectedId);
      })
      .catch(() => {});
  }, []);

  const loadSamples = async (id: string) => {
    setSelectedId(id);
    setLoading(true);
    try {
      const res = await fetchDatasetSamples(id);
      setSamples(res.samples || []);
    } catch {
      setSamples([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 backdrop-blur">
        <h2 className="text-base font-semibold text-white flex items-center gap-2 mb-1">
          <Database className="w-5 h-5 text-indigo-400" />
          Benchmark Dataset Explorer
        </h2>
        <p className="text-xs text-slate-400">
          Browse standardized reasoning benchmarks across multiple deduction depths and logical formalisms.
        </p>

        {/* Dataset Selection Tabs */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 mt-4">
          {datasets.map((ds) => (
            <button
              key={ds.id}
              onClick={() => loadSamples(ds.id)}
              className={`p-3 rounded-lg border text-left transition-all ${
                selectedId === ds.id
                  ? 'bg-indigo-950/40 border-indigo-600 text-white'
                  : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'
              }`}
            >
              <div className="text-xs font-semibold text-slate-200 mb-1 flex items-center justify-between">
                <span>{ds.name}</span>
                <span className="text-[10px] font-mono bg-slate-800 px-2 py-0.5 rounded text-indigo-300">
                  {ds.sample_count} items
                </span>
              </div>
              <p className="text-[11px] text-slate-500 line-clamp-2">{ds.description}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Samples List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
          <span>Displaying {samples.length} Benchmark Samples for '{selectedId}'</span>
        </div>

        {loading ? (
          <div className="p-8 text-center text-xs text-slate-500">Loading samples...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {samples.map((s, idx) => (
              <div
                key={idx}
                className="bg-slate-900/40 border border-slate-800 rounded-xl p-5 space-y-3 hover:border-slate-700 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono font-bold text-indigo-400">{s.id}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">
                      {s.category}
                    </span>
                    <span
                      className={`text-[10px] font-mono px-2 py-0.5 rounded border font-semibold ${
                        s.gold_label === 'ENTAILED'
                          ? 'bg-emerald-950 text-emerald-300 border-emerald-800'
                          : s.gold_label === 'CONTRADICTED'
                          ? 'bg-rose-950 text-rose-300 border-rose-800'
                          : 'bg-amber-950 text-amber-300 border-amber-800'
                      }`}
                    >
                      {s.gold_label}
                    </span>
                  </div>
                </div>

                <div>
                  <span className="text-[11px] text-slate-500 uppercase font-mono block mb-1">Premises:</span>
                  <ul className="text-xs text-slate-300 space-y-1 list-disc list-inside">
                    {s.premises.map((p: string, pIdx: number) => (
                      <li key={pIdx}>{p}</li>
                    ))}
                  </ul>
                </div>

                <div className="pt-2 border-t border-slate-800/80">
                  <span className="text-[11px] text-slate-500 uppercase font-mono block mb-1">Query:</span>
                  <div className="text-xs font-semibold text-slate-100">{s.query}</div>
                </div>

                <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 pt-2 border-t border-slate-800/60">
                  <span>Reasoning Depth: {s.depth}</span>
                  <span>Difficulty: {s.difficulty} / 5</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
