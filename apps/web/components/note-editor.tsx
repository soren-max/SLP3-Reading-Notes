"use client";

import { useEffect, useMemo, useState } from "react";
import { marked } from "marked";
import { Clipboard, Download, FileText, Plus, Save, Search, Sparkles, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { TagChip } from "@/components/tag-chip";
import { api, type Chapter, type Note } from "@/lib/api";
import { cn } from "@/lib/utils";

function buildReportDraft(note?: Note, chapter?: Chapter) {
  return `老师您好，我本阶段在整理 ${chapter ? `${chapter.number} ${chapter.title}` : "SLP3 重点章节"} 的阅读笔记，当前重点关注 ${chapter?.tags.join("、") ?? "KG-RAG、GraphRAG、信息抽取与实体链接"}。本章与研究方向的关系是：${chapter?.research_relation ?? "将章节内容映射到知识图谱构建、检索增强和大模型推理流程中"}。后续我会继续补充核心概念、公式算法和可用于实验设计的例子。`;
}

export function NoteEditor({ chapters, initialNotes, initialChapterId }: { chapters: Chapter[]; initialNotes: Note[]; initialChapterId?: number }) {
  const [notes, setNotes] = useState(initialNotes);
  const [selectedId, setSelectedId] = useState(initialNotes.find((n) => n.chapter_id === initialChapterId)?.id ?? initialNotes[0]?.id);
  const [query, setQuery] = useState("");
  const [tag, setTag] = useState("");
  const [saving, setSaving] = useState(false);
  const [toast, setToast] = useState("");
  const selected = notes.find((note) => note.id === selectedId) ?? notes[0];
  const [draft, setDraft] = useState<Note | undefined>(selected);
  const chapter = chapters.find((item) => item.id === draft?.chapter_id);

  useEffect(() => {
    setDraft(selected);
  }, [selected]);

  useEffect(() => {
    if (!toast) return;
    const timer = window.setTimeout(() => setToast(""), 2600);
    return () => window.clearTimeout(timer);
  }, [toast]);

  const tags = useMemo(() => Array.from(new Set(notes.flatMap((note) => note.tags.split(",").map((t) => t.trim()).filter(Boolean)))).sort(), [notes]);

  const filteredNotes = notes.filter((note) => {
    const matchesQuery = !query || `${note.title} ${note.content}`.toLowerCase().includes(query.toLowerCase());
    const matchesTag = !tag || note.tags.toLowerCase().includes(tag.toLowerCase());
    return matchesQuery && matchesTag;
  });

  async function save() {
    if (!draft) return;
    setSaving(true);
    const saved = await api.updateNote(draft.id, {
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
    const firstChapter = chapters[0];
    const created = await api.createNote({
      chapter_id: firstChapter.id,
      title: "新的阅读笔记",
      content: "# 新的阅读笔记\n\n## 核心问题\n- \n\n## 研究联系\n- ",
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
    <div className="relative grid gap-4 xl:grid-cols-[300px_minmax(0,1fr)_minmax(0,1fr)]">
      {toast && (
        <div className="fixed right-4 top-24 z-50 rounded-lg border bg-card px-4 py-3 text-sm font-medium shadow-lg" role="status" aria-live="polite">
          {toast}
        </div>
      )}

      <aside className="space-y-4 xl:sticky xl:top-24 xl:self-start">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              章节导航
              <Button size="sm" onClick={create} aria-label="新建笔记">
                <Plus className="h-4 w-4" />
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input className="pl-9" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="搜索关键词" />
            </div>
            <select className="min-h-11 w-full rounded-md border bg-background/80 px-3 text-sm focus-ring" value={tag} onChange={(event) => setTag(event.target.value)} aria-label="按标签筛选">
              <option value="">全部标签</option>
              {tags.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
            <div className="max-h-[58dvh] space-y-2 overflow-auto pr-1">
              {filteredNotes.length > 0 ? (
                filteredNotes.map((note) => {
                  const noteChapter = chapters.find((item) => item.id === note.chapter_id);
                  return (
                    <button
                      key={note.id}
                      onClick={() => setSelectedId(note.id)}
                      className={cn("w-full cursor-pointer rounded-lg border bg-background/55 p-3 text-left text-sm transition-all hover:-translate-y-0.5 hover:border-primary/40 hover:bg-muted focus-ring", selectedId === note.id && "border-primary bg-secondary shadow-sm")}
                    >
                      <span className="block font-medium">{note.title}</span>
                      <span className="mt-1 block text-xs text-muted-foreground">{noteChapter?.number}. {noteChapter?.title}</span>
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
              <select className="min-h-11 w-full rounded-md border bg-background/80 px-3 text-sm focus-ring" value={draft.chapter_id} onChange={(event) => setDraft({ ...draft, chapter_id: Number(event.target.value) })} aria-label="选择章节">
                {chapters.map((item) => (
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
                <Button variant="outline" onClick={() => copyNote(buildReportDraft(draft, chapter), "导师汇报草稿已复制")}>
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
              <p className="mt-2 text-sm text-muted-foreground">新建一条章节笔记后即可开始编辑。</p>
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
