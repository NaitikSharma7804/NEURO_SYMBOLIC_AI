import {
  HealthStatus,
  ReasoningResponse,
  ExplanationMode,
  ExperimentRunRecord
} from '../types';

const API_BASE = '';

export async function fetchHealth(): Promise<HealthStatus> {
  const response = await fetch(`${API_BASE}/health`);
  if (!response.ok) {
    throw new Error(`Health check failed with status: ${response.status}`);
  }
  return response.json();
}

export async function executeReason(
  query: string,
  explanationMode: ExplanationMode = 'DETAILED'
): Promise<ReasoningResponse> {
  const response = await fetch(`${API_BASE}/api/reason`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query,
      mode: 'full',
      explanation_mode: explanationMode
    })
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(errorData.detail || `Reasoning request failed with status: ${response.status}`);
  }

  return response.json();
}

export async function fetchDatasets(): Promise<{ datasets: Array<{ id: string; name: string; description: string; sample_count: number }> }> {
  const response = await fetch(`${API_BASE}/api/datasets`);
  if (!response.ok) {
    throw new Error(`Failed to load datasets: ${response.status}`);
  }
  return response.json();
}

export async function fetchDatasetSamples(datasetId: string): Promise<any> {
  const response = await fetch(`${API_BASE}/api/datasets/${datasetId}/samples`);
  if (!response.ok) {
    throw new Error(`Failed to load samples: ${response.status}`);
  }
  return response.json();
}

export async function runExperiment(dataset: string, baseline: string): Promise<ExperimentRunRecord> {
  const response = await fetch(`${API_BASE}/api/experiments/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ dataset, baseline })
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(err.detail || `Experiment failed: ${response.status}`);
  }

  return response.json();
}

export async function listExperiments(): Promise<{ experiments: any[] }> {
  const response = await fetch(`${API_BASE}/api/experiments`);
  if (!response.ok) {
    throw new Error(`Failed to list experiments: ${response.status}`);
  }
  return response.json();
}

export async function fetchErrorAnalysis(): Promise<any> {
  const response = await fetch(`${API_BASE}/api/experiments/error-analysis`);
  if (!response.ok) {
    throw new Error(`Failed to fetch error analysis: ${response.status}`);
  }
  return response.json();
}

export async function fetchReasoningSessions(): Promise<{ total: number; sessions: any[] }> {
  const response = await fetch(`${API_BASE}/api/sessions`);
  if (!response.ok) {
    throw new Error(`Failed to fetch sessions: ${response.status}`);
  }
  return response.json();
}

export async function fetchSessionDetail(sessionId: string): Promise<any> {
  const response = await fetch(`${API_BASE}/api/sessions/${sessionId}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch session detail: ${response.status}`);
  }
  return response.json();
}
