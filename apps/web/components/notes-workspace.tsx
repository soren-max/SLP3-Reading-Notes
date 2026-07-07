"use client";

import { useEffect, useMemo, useState } from "react";
import { marked } from "marked";
import { Plus, Save, Search, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { api, type Chapter, type Note } from "@/lib/api";
import { cn } from "@/lib/utils";

export function NotesWorkspace({ chapters, initialNotes, initialChapterId }: { chapters: Chapter[]; initialNotes: Note[]; initialChapterId?: number }) {
  const [notes, setNotes] = useState(initialNotes);
  const [selectedId, setSelectedId] = useState(initialNotes.find((n) => n.chapter_id === initialChapterId)?.id ?? initialNotes[0]?.id);
  const [query, setQuery] = useState("");
  const [tag, setTag] = useState("");
  const [saving, setSaving] = useState(false);
  const selected = notes.find((note) => note.id === selectedId) ?? notes[0];
  const [draft, setDraft] = useState<Note | undefined>(selected);

  useEffect(() => {
    setDraft(selected);
  }, [selected?.id]);

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
  }

  async function create() {
    const chapter = chapters[0];
    const created = await api.createNote({
      chapter_id: chapter.id,
      title: "新的阅读笔记",
      content: "# 新的阅读笔记\n\n## 核心问题\n- \n\n## 研究联系\n- ",
      tags: "LLM,RAG",
    });
    setNotes((items) => [created, ...items]);
    setSelectedId(created.id);
  }

  async function remove() {
    if (!draft) return;
    await api.deleteNote(draft.id);
    const next = notes.filter((item) => item.id !== draft.id);
    setNotes(next);
    setSelectedId(next[0]?.id);
  }

  const preview = draft ? (marked.parse(draft.content, { async: false }) as string) : "";

  return (
    <div className="grid gap-4 xl:grid-cols-[280px_1fr_1fr]">
      <aside className="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              章节列表
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
            <select className="min-h-11 w-full rounded-md border bg-background px-3 text-sm" value={tag} onChange={(event) => setTag(event.target.value)} aria-label="按标签筛选">
              <option value="">全部标签</option>
              {tags.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
            <div className="max-h-[62dvh] space-y-2 overflow-auto pr-1">
              {filteredNotes.map((note) => {
                const chapter = chapters.find((item) => item.id === note.chapter_id);
                return (
                  <button
                    key={note.id}
                    onClick={() => setSelectedId(note.id)}
                    className={cn("w-full rounded-md border p-3 text-left text-sm transition-colors hover:bg-muted", selectedId === note.id && "border-primary bg-secondary")}
                  >
                    <span className="block font-medium">{note.title}</span>
                    <span className="mt-1 block text-xs text-muted-foreground">{chapter?.number}. {chapter?.title}</span>
                  </button>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </aside>

      <Card>
        <CardHeader>
          <CardTitle>Markdown 编辑器</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {draft && (
            <>
              <Input value={draft.title} onChange={(event) => setDraft({ ...draft, title: event.target.value })} aria-label="笔记标题" />
              <select className="min-h-11 w-full rounded-md border bg-background px-3 text-sm" value={draft.chapter_id} onChange={(event) => setDraft({ ...draft, chapter_id: Number(event.target.value) })} aria-label="选择章节">
                {chapters.map((chapter) => (
                  <option key={chapter.id} value={chapter.id}>
                    {chapter.number}. {chapter.title}
                  </option>
                ))}
              </select>
              <Input value={draft.tags} onChange={(event) => setDraft({ ...draft, tags: event.target.value })} aria-label="标签" placeholder="LLM,RAG,KG" />
              <Textarea className="min-h-[52dvh] font-mono leading-6" value={draft.content} onChange={(event) => setDraft({ ...draft, content: event.target.value })} aria-label="Markdown 内容" />
              <div className="flex gap-2">
                <Button onClick={save} disabled={saving}>
                  <Save className="h-4 w-4" />
                  {saving ? "保存中" : "保存"}
                </Button>
                <Button variant="destructive" onClick={remove}>
                  <Trash2 className="h-4 w-4" />
                  删除
                </Button>
              </div>
            </>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>实时预览</CardTitle>
        </CardHeader>
        <CardContent>
          <article className="prose prose-slate max-w-none" dangerouslySetInnerHTML={{ __html: preview }} />
        </CardContent>
      </Card>
    </div>
  );
}
