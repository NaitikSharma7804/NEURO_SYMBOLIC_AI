import React, { useState, useEffect } from 'react';
import { fetchReasoningSessions, fetchSessionDetail } from '../services/api';
import {
  Database,
  Clock,
  CheckCircle2,
  XCircle,
  HelpCircle,
  Code,
  FileText,
  ArrowUpRight
} from 'lucide-react';

interface SessionSummary {
  session_id: string;
  created_at: string;
  query_text: string;
  reasoning_result: string;
  llm_provider: string;
  latency_ms: number;
}

interface KnowledgeBaseInspectorProps {
  onLoadQueryIntoPlayground?: (query: string) => void;
}

export const KnowledgeBaseInspector: React.FC<KnowledgeBaseInspectorProps> = ({ onLoadQueryIntoPlayground }) => {
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null);
  const [sessionDetail, setSessionDetail] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [detailLoading, setDetailLoading] = useState<boolean>(false);
  const [filterText, setFilterText] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  const loadSessions = () => {
    setLoading(true);
    fetchReasoningSessions()
      .then((data) => {
        setSessions(data.sessions || []);
        if (data.sessions && data.sessions.length > 0 && !selectedSessionId) {
          setSelectedSessionId(data.sessions[0].session_id);
        }
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadSessions();
  }, []);

  useEffect(() => {
    if (selectedSessionId) {
      setDetailLoading(true);
      fetchSessionDetail(selectedSessionId)
        .then((detail) => {
          setSessionDetail(detail);
          setDetailLoading(false);
        })
        .catch(() => {
          setDetailLoading(false);
        });
    }
  }, [selectedSessionId]);

  const filteredSessions = sessions.filter((s) =>
    s.query_text.toLowerCase().includes(filterText.toLowerCase()) ||
    s.session_id.toLowerCase().includes(filterText.toLowerCase()) ||
    s.reasoning_result.toLowerCase().includes(filterText.toLowerCase())
  );

  const getResultBadge = (res: string) => {
    switch (res?.toUpperCase()) {
      case 'ENTAILED':
        return (
          <span className="font-mono text-[10px] px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-300 border border-emerald-800 flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3 text-emerald-400" /> ENTAILED
          </span>
        );
      case 'CONTRADICTED':
        return (
          <span className="font-mono text-[10px] px-2 py-0.5 rounded bg-rose-950/80 text-rose-300 border border-rose-800 flex items-center gap-1">
            <XCircle className="w-3 h-3 text-rose-400" /> CONTRADICTED
          </span>
        );
      default:
        return (
          <span className="font-mono text-[10px] px-2 py-0.5 rounded bg-amber-950/80 text-amber-300 border border-amber-800 flex items-center gap-1">
            <HelpCircle className="w-3 h-3 text-amber-400" /> UNKNOWN
          </span>
        );
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Database className="w-5 h-5 text-indigo-400" />
              Knowledge Base & Persistent Session History
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              SQLite relational storage of reasoning sessions, formal logic schemas, deductive proofs, and XAI explanations.
            </p>
          </div>
          <button
            onClick={loadSessions}
            className="text-xs font-mono bg-indigo-600 hover:bg-indigo-500 text-white px-3 py-1.5 rounded-lg transition-all"
          >
            Refresh Records
          </button>
        </div>
      </div>

      {loading && (
        <div className="p-12 text-center text-slate-400 font-mono text-sm">
          Loading persisted session records from database...
        </div>
      )}

      {error && (
        <div className="p-4 bg-amber-950/40 border border-amber-800 rounded-xl text-xs text-amber-300">
          Database notice: {error}
        </div>
      )}

      {!loading && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Sessions List */}
          <div className="space-y-3">
            <div className="flex items-center justify-between px-1">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Sessions ({filteredSessions.length})
              </span>
              <div className="relative w-44">
                <input
                  type="text"
                  placeholder="Filter sessions..."
                  value={filterText}
                  onChange={(e) => setFilterText(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-md px-2 py-1 text-xs text-slate-300 placeholder-slate-600 focus:outline-none focus:border-indigo-500 font-mono"
                />
              </div>
            </div>

            {filteredSessions.length === 0 ? (
              <div className="bg-slate-900/40 border border-slate-800 rounded-xl p-8 text-center text-slate-500 text-xs">
                No recorded sessions yet. Execute a reasoning query in the Playground to record your first trace.
              </div>
            ) : (
              <div className="space-y-2 max-h-[600px] overflow-y-auto pr-1">
                {filteredSessions.map((s) => {
                  const isSelected = selectedSessionId === s.session_id;
                  return (
                    <div
                      key={s.session_id}
                      onClick={() => setSelectedSessionId(s.session_id)}
                      className={`p-3 rounded-xl border text-xs cursor-pointer transition-all ${
                        isSelected
                          ? 'bg-slate-800/90 border-indigo-500 shadow-md'
                          : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
                      }`}
                    >
                      <div className="flex items-center justify-between gap-2 mb-1.5">
                        <span className="font-mono text-[11px] text-indigo-400 font-bold">
                          {s.session_id}
                        </span>
                        {getResultBadge(s.reasoning_result)}
                      </div>
                      <p className="text-slate-300 text-xs font-mono line-clamp-2 mb-2">
                        {s.query_text}
                      </p>
                      <div className="flex items-center justify-between text-[10px] font-mono text-slate-500">
                        <span className="flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {s.created_at ? new Date(s.created_at).toLocaleTimeString() : 'Recent'}
                        </span>
                        <span>{s.latency_ms ? `${s.latency_ms.toFixed(1)}ms` : ''}</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Session Detail Inspector */}
          <div className="lg:col-span-2 space-y-4">
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-1">
              Session Trace & Provenance
            </div>

            {detailLoading ? (
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center text-slate-400 font-mono text-xs">
                Loading session trace from SQLite database...
              </div>
            ) : sessionDetail ? (
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-5 text-xs">
                <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-white text-sm">
                        {sessionDetail.session_id}
                      </span>
                      {getResultBadge(sessionDetail.reasoning_result)}
                    </div>
                    <span className="text-[11px] font-mono text-slate-500">
                      Timestamp: {sessionDetail.created_at} • Provider: {sessionDetail.llm_provider || 'mock'}
                    </span>
                  </div>

                  {onLoadQueryIntoPlayground && (
                    <button
                      onClick={() => onLoadQueryIntoPlayground(sessionDetail.query_text)}
                      className="flex items-center gap-1.5 bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-300 border border-indigo-500/40 px-3 py-1.5 rounded-lg font-mono text-xs transition-all"
                    >
                      <span>Load into Playground</span>
                      <ArrowUpRight className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>

                {/* Input Text */}
                <div>
                  <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                    Query Prompt
                  </div>
                  <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 font-mono text-slate-200 whitespace-pre-wrap">
                    {sessionDetail.query_text}
                  </div>
                </div>

                {/* Formalization */}
                {sessionDetail.formalization && (
                  <div>
                    <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1.5 flex items-center gap-1">
                      <Code className="w-3.5 h-3.5 text-sky-400" />
                      Structured Logic Schema
                    </div>
                    <pre className="bg-slate-950 p-3 rounded-lg border border-slate-800 font-mono text-[11px] text-sky-300 overflow-x-auto max-h-48">
                      {JSON.stringify(sessionDetail.formalization, null, 2)}
                    </pre>
                  </div>
                )}

                {/* Explanation */}
                {sessionDetail.explanation_text && (
                  <div>
                    <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1.5 flex items-center gap-1">
                      <FileText className="w-3.5 h-3.5 text-emerald-400" />
                      Proof-Grounded Human Explanation
                    </div>
                    <div className="bg-slate-950 p-3.5 rounded-lg border border-slate-800 text-slate-300 leading-relaxed font-sans">
                      {sessionDetail.explanation_text}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="bg-slate-900/40 border border-slate-800/80 rounded-xl p-12 text-center text-slate-500 text-xs">
                Select a session from the left column to view its formal logical representation, proof DAG, and explanation.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
