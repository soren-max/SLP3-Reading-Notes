const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export type Chapter = {
  id: number;
  source_id: number;
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

export type SourceType = "book" | "paper" | "course" | "project" | "report" | "misc";

export type Source = {
  id: number;
  title: string;
  type: SourceType;
  author_or_origin: string;
  research_direction: string;
  description: string;
  status: "未开始" | "进行中" | "已完成";
  priority: "高" | "中" | "低";
};

export type Note = {
  id: number;
  source_id: number;
  chapter_id: number | null;
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

export type CustomRoadmap = {
  name: string;
  steps: string[];
};

export type RoadmapResponse = {
  slp3: RoadmapPhase[];
  custom: CustomRoadmap[];
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
  chaptersBySource: (sourceId: number) => request<Chapter[]>(`/api/chapters?source_id=${sourceId}`),
  chapter: (id: number) => request<Chapter>(`/api/chapters/${id}`),
  updateProgress: (id: number, status: Chapter["status"]) =>
    request<Chapter>(`/api/chapters/${id}/progress`, { method: "PATCH", body: JSON.stringify({ status }) }),
  notes: (params?: URLSearchParams) => request<Note[]>(`/api/notes${params ? `?${params}` : ""}`),
  sources: (params?: URLSearchParams) => request<Source[]>(`/api/sources${params ? `?${params}` : ""}`),
  source: (id: number) => request<Source>(`/api/sources/${id}`),
  createSource: (payload: Omit<Source, "id">) => request<Source>("/api/sources", { method: "POST", body: JSON.stringify(payload) }),
  updateSource: (id: number, payload: Partial<Omit<Source, "id">>) => request<Source>(`/api/sources/${id}`, { method: "PATCH", body: JSON.stringify(payload) }),
  deleteSource: (id: number) => request<void>(`/api/sources/${id}`, { method: "DELETE" }),
  createNote: (payload: Pick<Note, "source_id" | "chapter_id" | "title" | "content" | "tags">) =>
    request<Note>("/api/notes", { method: "POST", body: JSON.stringify(payload) }),
  updateNote: (id: number, payload: Partial<Pick<Note, "source_id" | "chapter_id" | "title" | "content" | "tags">>) =>
    request<Note>(`/api/notes/${id}`, { method: "PATCH", body: JSON.stringify(payload) }),
  deleteNote: (id: number) => request<void>(`/api/notes/${id}`, { method: "DELETE" }),
  roadmap: () => request<RoadmapResponse>("/api/roadmap"),
  report: (sourceId?: number) => request<Report>(`/api/report${sourceId ? `?source_id=${sourceId}` : ""}`),
};
