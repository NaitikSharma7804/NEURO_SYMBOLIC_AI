import React, { useState, useEffect } from 'react';
import { fetchDatasets, fetchDatasetSamples } from '../services/api';
import { Database, Search, ArrowUpRight, Filter } from 'lucide-react';

interface DatasetExplorerProps {
  onLoadQueryIntoPlayground?: (query: string) => void;
}

export const DatasetExplorer: React.FC<DatasetExplorerProps> = ({ onLoadQueryIntoPlayground }) => {
  const [datasets, setDatasets] = useState<any[]>([]);
  const [selectedId, setSelectedId] = useState<string>('custom');
  const [samples, setSamples] = useState<any[]>([]);
  const [filterText, setFilterText] = useState<string>('');
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
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
    setSelectedCategory('ALL');
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

  const categories = ['ALL', ...Array.from(new Set(samples.map((s) => s.category)))];

  const filteredSamples = samples.filter((s) => {
    const matchesSearch =
      s.id.toLowerCase().includes(filterText.toLowerCase()) ||
      s.query.toLowerCase().includes(filterText.toLowerCase()) ||
      s.premises.some((p: string) => p.toLowerCase().includes(filterText.toLowerCase()));
    const matchesCategory = selectedCategory === 'ALL' || s.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h2 className="text-base font-semibold text-white flex items-center gap-2 mb-1">
          <Database className="w-5 h-5 text-indigo-400" />
          Benchmark Dataset Explorer
        </h2>
        <p className="text-xs text-slate-400">
          Browse standardized reasoning benchmarks across multiple deduction depths and logical formalisms. Total corpus: 80+ curated diagnostic and multi-hop instances.
        </p>

        {/* Dataset Selection Tabs */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 mt-4">
          {datasets.map((ds) => (
            <button
              key={ds.id}
              onClick={() => loadSamples(ds.id)}
              className={`p-3 rounded-lg border text-left transition-all ${
                selectedId === ds.id
                  ? 'bg-indigo-950/60 border-indigo-500 text-white shadow-md'
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

      {/* Filter and Search Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-2 flex-1 min-w-[200px] max-w-md">
          <Search className="w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="Search premises, queries, or sample IDs..."
            value={filterText}
            onChange={(e) => setFilterText(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-indigo-500 font-mono"
          />
        </div>

        <div className="flex items-center gap-2 overflow-x-auto text-xs font-mono">
          <Filter className="w-3.5 h-3.5 text-slate-500" />
          <span className="text-slate-400 text-[11px]">Category:</span>
          {categories.slice(0, 6).map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-2.5 py-1 rounded text-[10px] transition-all ${
                selectedCategory === cat
                  ? 'bg-indigo-600 text-white font-semibold'
                  : 'bg-slate-950 border border-slate-800 text-slate-400 hover:text-slate-200'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Samples Grid */}
      <div className="space-y-4">
        <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
          <span>Displaying {filteredSamples.length} of {samples.length} Benchmark Samples for '{selectedId}'</span>
        </div>

        {loading ? (
          <div className="p-12 text-center text-xs text-slate-500 font-mono">Loading benchmark samples...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredSamples.map((s, idx) => (
              <div
                key={idx}
                className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3 hover:border-slate-700 transition-colors flex flex-col justify-between"
              >
                <div className="space-y-3">
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
                    <span className="text-[10px] text-slate-500 uppercase font-mono block mb-1">Premises:</span>
                    <ul className="text-xs text-slate-300 space-y-1 list-disc list-inside">
                      {s.premises.map((p: string, pIdx: number) => (
                        <li key={pIdx}>{p}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="pt-2 border-t border-slate-800">
                    <span className="text-[10px] text-slate-500 uppercase font-mono block mb-1">Query:</span>
                    <div className="text-xs font-semibold text-slate-100">{s.query}</div>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-3 border-t border-slate-800 text-[11px] font-mono text-slate-500">
                  <div className="flex items-center gap-3">
                    <span>Depth: {s.depth}</span>
                    <span>Diff: {s.difficulty}/5</span>
                  </div>
                  {onLoadQueryIntoPlayground && (
                    <button
                      onClick={() => {
                        const fullText = `${s.premises.join('\n')}\n${s.query}`;
                        onLoadQueryIntoPlayground(fullText);
                      }}
                      className="flex items-center gap-1 text-indigo-400 hover:text-indigo-300 text-[11px] transition-colors"
                    >
                      <span>Test in Playground</span>
                      <ArrowUpRight className="w-3 h-3" />
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
