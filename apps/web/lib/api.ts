const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export type Chapter = {
  id: number;
  number: number;
  title: string;
  priority: "高" | "中" | "低";
  status: "未开始" | "阅读中" | "已完成";
  mastery: "精读" | "理解" | "略读";
  relevance_score: number;
  research_relation: string;
  positioning?: string;
  core_concepts?: string[];
  outline?: string;
  formulas_algorithms?: string;
  examples?: string;
  summary?: string;
  mentor_questions?: string[];
  research_links?: string;
  resources?: string[];
  tags: string[];
};

export type Note = {
  id: number;
  chapter_id: number;
  title: string;
  content: string;
  tags: string;
  created_at: string;
  updated_at: string;
};

export type RoadmapPhase = {
  phase: string;
  goal: string;
  steps: string[];
};

export type Report = {
  progress_percent: number;
  current_stage: string;
  completed_chapters: string[];
  current_gains: string[];
  next_plan: string[];
  research_relation: string;
  wechat_text: string;
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`${res.status} ${res.statusText}`);
  }
  if (res.status === 204) {
    return undefined as T;
  }
  return res.json();
}

export const api = {
  chapters: () => request<Chapter[]>("/api/chapters"),
  chapter: (id: number) => request<Chapter>(`/api/chapters/${id}`),
  updateProgress: (id: number, status: Chapter["status"]) =>
    request<Chapter>(`/api/chapters/${id}/progress`, { method: "PATCH", body: JSON.stringify({ status }) }),
  notes: (params?: URLSearchParams) => request<Note[]>(`/api/notes${params ? `?${params}` : ""}`),
  createNote: (payload: Pick<Note, "chapter_id" | "title" | "content" | "tags">) =>
    request<Note>("/api/notes", { method: "POST", body: JSON.stringify(payload) }),
  updateNote: (id: number, payload: Partial<Pick<Note, "chapter_id" | "title" | "content" | "tags">>) =>
    request<Note>(`/api/notes/${id}`, { method: "PATCH", body: JSON.stringify(payload) }),
  deleteNote: (id: number) => request<void>(`/api/notes/${id}`, { method: "DELETE" }),
  roadmap: () => request<RoadmapPhase[]>("/api/roadmap"),
  report: () => request<Report>("/api/report"),
};
