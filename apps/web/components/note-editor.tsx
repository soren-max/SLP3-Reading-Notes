"use client";

import { useEffect, useMemo, useState } from "react";
import { marked } from "marked";
import { Clipboard, Download, FileText, Plus, Save, Search, Sparkles, Trash2 } from "lucide-react";

import { TagChip } from "@/components/tag-chip";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { api, type Chapter, type Note, type Source, type SourceType } from "@/lib/api";
import { cn } from "@/lib/utils";

const sourceTypeLabels: Record<SourceType | "全部类型", string> = {
  全部类型: "全部类型",
  book: "书籍",
  paper: "论文",
  course: "课程",
  project: "项目",
  report: "汇报",
  misc: "其他",
};

function buildReportDraft(note?: Note, source?: Source, chapter?: Chapter) {
  const target = chapter ? `${chapter.number} ${chapter.title}` : source?.title ?? "AI 研究资料";
  const direction = source?.research_direction ?? "KG-RAG、GraphRAG、信息抽取与实体链接";
  return `老师您好，我本阶段在整理《${target}》的学习笔记，当前重点关注 ${direction}。这部分内容主要用于支撑 NLP、LLM、RAG 与知识图谱推理方向的研究积累。后续我会继续补充核心概念、方法细节、实验思路和可汇报的问题。`;
}

export function NoteEditor({
  sources,
  chapters,
  initialNotes,
  initialChapterId,
  initialSourceId,
}: {
  sources: Source[];
  chapters: Chapter[];
  initialNotes: Note[];
  initialChapterId?: number;
  initialSourceId?: number;
}) {
  const [notes, setNotes] = useState(initialNotes);
  const [selectedId, setSelectedId] = useState(initialNotes.find((note) => note.chapter_id === initialChapterId || note.source_id === initialSourceId)?.id ?? initialNotes[0]?.id);
  const [query, setQuery] = useState("");
  const [tag, setTag] = useState("");
  const [sourceType, setSourceType] = useState<SourceType | "全部类型">("全部类型");
  const [direction, setDirection] = useState("全部方向");
  const [status, setStatus] = useState("全部状态");
  const [priority, setPriority] = useState("全部优先级");
  const [saving, setSaving] = useState(false);
  const [toast, setToast] = useState("");
  const selected = notes.find((note) => note.id === selectedId) ?? notes[0];
  const [draft, setDraft] = useState<Note | undefined>(selected);
  const source = sources.find((item) => item.id === draft?.source_id);
  const chapter = chapters.find((item) => item.id === draft?.chapter_id);

  useEffect(() => {
    setDraft(selected);
  }, [selected]);

  useEffect(() => {
    if (!toast) return;
    const timer = window.setTimeout(() => setToast(""), 2600);
    return () => window.clearTimeout(timer);
  }, [toast]);

  const tags = useMemo(() => Array.from(new Set(notes.flatMap((note) => note.tags.split(",").map((item) => item.trim()).filter(Boolean)))).sort(), [notes]);
  const directions = useMemo(() => ["全部方向", ...Array.from(new Set(sources.flatMap((item) => item.research_direction.split(",").map((directionItem) => directionItem.trim()).filter(Boolean)))).sort()], [sources]);
  const sourceTypes = useMemo(() => ["全部类型", ...Array.from(new Set(sources.map((item) => item.type)))] as Array<SourceType | "全部类型">, [sources]);

  const filteredNotes = notes.filter((note) => {
    const noteSource = sources.find((item) => item.id === note.source_id);
    const matchesQuery = !query || `${note.title} ${note.content} ${noteSource?.title ?? ""}`.toLowerCase().includes(query.toLowerCase());
    const matchesTag = !tag || note.tags.toLowerCase().includes(tag.toLowerCase());
    const matchesType = sourceType === "全部类型" || noteSource?.type === sourceType;
    const matchesDirection = direction === "全部方向" || noteSource?.research_direction.includes(direction);
    const matchesStatus = status === "全部状态" || noteSource?.status === status;
    const matchesPriority = priority === "全部优先级" || noteSource?.priority === priority;
    return matchesQuery && matchesTag && matchesType && matchesDirection && matchesStatus && matchesPriority;
  });

  async function save() {
    if (!draft) return;
    setSaving(true);
    const saved = await api.updateNote(draft.id, {
      source_id: draft.source_id,
      chapter_id: draft.chapter_id,
      title: draft.title,
      content: draft.content,
      tags: draft.tags,
    });
    setNotes((items) => items.map((item) => (item.id === saved.id ? saved : item)));
    setSaving(false);
    setToast("笔记已保存");
  }

  async function create() {
    const selectedSource = sources.find((item) => item.id === initialSourceId) ?? sources[0];
    const firstChapter = chapters.find((item) => item.source_id === selectedSource.id);
    const created = await api.createNote({
      source_id: selectedSource.id,
      chapter_id: firstChapter?.id ?? null,
      title: "新的研究笔记",
      content: "# 新的研究笔记\n\n## 核心问题\n- \n\n## 方法/内容\n- \n\n## 研究联系\n- ",
      tags: "LLM,RAG",
    });
    setNotes((items) => [created, ...items]);
    setSelectedId(created.id);
    setToast("已创建新笔记");
  }

  async function remove() {
    if (!draft) return;
    await api.deleteNote(draft.id);
    const next = notes.filter((item) => item.id !== draft.id);
    setNotes(next);
    setSelectedId(next[0]?.id);
    setToast("笔记已删除");
  }

  async function copyNote(text = draft?.content ?? "", message = "已复制到剪贴板") {
    await navigator.clipboard.writeText(text);
    setToast(message);
  }

  function exportMarkdown() {
    if (!draft) return;
    const blob = new Blob([draft.content], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${draft.title.replace(/[\\/:*?"<>|]/g, "-")}.md`;
    a.click();
    URL.revokeObjectURL(url);
    setToast("Markdown 已导出");
  }

  const preview = draft ? (marked.parse(draft.content, { async: false }) as string) : "";

  return (
    <div className="relative grid gap-4 xl:grid-cols-[320px_minmax(0,1fr)_minmax(0,1fr)]">
      {toast && (
        <div className="fixed right-4 top-24 z-50 rounded-lg border bg-card px-4 py-3 text-sm font-medium shadow-lg" role="status" aria-live="polite">
          {toast}
        </div>
      )}

      <aside className="space-y-4 xl:sticky xl:top-24 xl:self-start">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              资料与笔记
              <Button size="sm" onClick={create} aria-label="新建笔记">
                <Plus className="h-4 w-4" />
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input className="pl-9" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="搜索资料或笔记" />
            </div>
            <select className="min-h-11 w-full rounded-md border bg-background/80 px-3 text-sm focus-ring" value={sourceType} onChange={(event) => setSourceType(event.target.value as SourceType | "全部类型")} aria-label="来源类型">
              {sourceTypes.map((item) => <option key={item} value={item}>{sourceTypeLabels[item]}</option>)}
            </select>
            <select className="min-h-11 w-full rounded-md border bg-background/80 px-3 text-sm focus-ring" value={direction} onChange={(event) => setDirection(event.target.value)} aria-label="研究方向">
              {directions.map((item) => <option key={item} value={item}>{item}</option>)}
            </select>
            <div className="grid grid-cols-2 gap-2">
              <select className="min-h-11 rounded-md border bg-background/80 px-3 text-sm focus-ring" value={status} onChange={(event) => setStatus(event.target.value)} aria-label="阅读状态">
                {["全部状态", "未开始", "进行中", "已完成"].map((item) => <option key={item} value={item}>{item}</option>)}
              </select>
              <select className="min-h-11 rounded-md border bg-background/80 px-3 text-sm focus-ring" value={priority} onChange={(event) => setPriority(event.target.value)} aria-label="优先级">
                {["全部优先级", "高", "中", "低"].map((item) => <option key={item} value={item}>{item}</option>)}
              </select>
            </div>
            <select className="min-h-11 w-full rounded-md border bg-background/80 px-3 text-sm focus-ring" value={tag} onChange={(event) => setTag(event.target.value)} aria-label="按标签筛选">
              <option value="">全部标签</option>
              {tags.map((item) => <option key={item} value={item}>{item}</option>)}
            </select>
            <div className="max-h-[50dvh] space-y-2 overflow-auto pr-1">
              {filteredNotes.length > 0 ? (
                filteredNotes.map((note) => {
                  const noteSource = sources.find((item) => item.id === note.source_id);
                  const noteChapter = chapters.find((item) => item.id === note.chapter_id);
                  return (
                    <button
                      key={note.id}
                      onClick={() => setSelectedId(note.id)}
                      className={cn("w-full cursor-pointer rounded-lg border bg-background/55 p-3 text-left text-sm transition-all hover:-translate-y-0.5 hover:border-primary/40 hover:bg-muted focus-ring", selectedId === note.id && "border-primary bg-secondary shadow-sm")}
                    >
                      <span className="block font-medium">{note.title}</span>
                      <span className="mt-1 block text-xs text-muted-foreground">{noteSource?.title}</span>
                      {noteChapter && <span className="mt-1 block text-xs text-muted-foreground">{noteChapter.number}. {noteChapter.title}</span>}
                    </button>
                  );
                })
              ) : (
                <div className="rounded-lg border border-dashed p-6 text-center text-sm text-muted-foreground">没有匹配笔记</div>
              )}
            </div>
          </CardContent>
        </Card>
      </aside>

      <Card>
        <CardHeader>
          <CardTitle>Markdown 编辑</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {draft ? (
            <>
              <Input value={draft.title} onChange={(event) => setDraft({ ...draft, title: event.target.value })} aria-label="笔记标题" />
              <select className="min-h-11 w-full rounded-md border bg-background/80 px-3 text-sm focus-ring" value={draft.source_id} onChange={(event) => {
                const nextSourceId = Number(event.target.value);
                setDraft({ ...draft, source_id: nextSourceId, chapter_id: chapters.find((item) => item.source_id === nextSourceId)?.id ?? null });
              }} aria-label="选择资料来源">
                {sources.map((item) => <option key={item.id} value={item.id}>{item.title}</option>)}
              </select>
              <select className="min-h-11 w-full rounded-md border bg-background/80 px-3 text-sm focus-ring" value={draft.chapter_id ?? ""} onChange={(event) => setDraft({ ...draft, chapter_id: event.target.value ? Number(event.target.value) : null })} aria-label="选择章节">
                <option value="">不关联章节</option>
                {chapters.filter((item) => item.source_id === draft.source_id).map((item) => (
                  <option key={item.id} value={item.id}>
                    {item.number}. {item.title}
                  </option>
                ))}
              </select>
              <Input value={draft.tags} onChange={(event) => setDraft({ ...draft, tags: event.target.value })} aria-label="标签" placeholder="LLM,RAG,KG" />
              <div className="flex flex-wrap gap-2">
                {draft.tags.split(",").filter(Boolean).map((item) => <TagChip key={item.trim()} label={item.trim()} />)}
              </div>
              <Textarea className="min-h-[50dvh] font-mono leading-6" value={draft.content} onChange={(event) => setDraft({ ...draft, content: event.target.value })} aria-label="Markdown 内容" />
              <div className="flex flex-wrap gap-2">
                <Button onClick={save} disabled={saving}>
                  <Save className="h-4 w-4" />
                  {saving ? "保存中" : "保存"}
                </Button>
                <Button variant="secondary" onClick={() => copyNote()}>
                  <Clipboard className="h-4 w-4" />
                  复制笔记
                </Button>
                <Button variant="outline" onClick={exportMarkdown}>
                  <Download className="h-4 w-4" />
                  导出 Markdown
                </Button>
                <Button variant="outline" onClick={() => copyNote(buildReportDraft(draft, source, chapter), "导师汇报草稿已复制")}>
                  <Sparkles className="h-4 w-4" />
                  生成导师汇报草稿
                </Button>
                <Button variant="destructive" onClick={remove}>
                  <Trash2 className="h-4 w-4" />
                  删除
                </Button>
              </div>
            </>
          ) : (
            <div className="rounded-lg border border-dashed p-10 text-center">
              <FileText className="mx-auto h-8 w-8 text-muted-foreground" />
              <p className="mt-3 font-semibold">还没有笔记</p>
              <p className="mt-2 text-sm text-muted-foreground">新建一条资料笔记后即可开始编辑。</p>
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>实时预览</CardTitle>
        </CardHeader>
        <CardContent>
          {draft ? (
            <article className="prose prose-slate max-w-none dark:prose-invert" dangerouslySetInnerHTML={{ __html: preview }} />
          ) : (
            <div className="rounded-lg border border-dashed p-10 text-center text-sm text-muted-foreground">选择或创建笔记后显示预览。</div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
