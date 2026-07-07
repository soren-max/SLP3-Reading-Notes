"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { marked } from "marked";
import { BookOpen, Clipboard, Download, Eye, Pencil, Save, Sparkles } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { api, type Chapter, type Note } from "@/lib/api";
import { cn } from "@/lib/utils";

// ── Helpers ──────────────────────────────────────────────

function getSections(markdown: string): { id: string; title: string }[] {
  const lines = markdown.split("\n");
  const sections: { id: string; title: string }[] = [];
  for (const line of lines) {
    const match = line.match(/^##\s+(.+)/);
    if (match) {
      const title = match[1].trim();
      const id = title
        .toLowerCase()
        .replace(/[^a-z0-9\u4e00-\u9fff]+/g, "-")
        .replace(/(^-|^-)/g, "")
        .replace(/-$/g, "");
      sections.push({ id, title });
    }
  }
  return sections;
}

function buildReportDraft(chapter: Chapter) {
  return `老师您好，我本阶段在整理《Chapter ${chapter.number} ${chapter.title}》的学习笔记，当前重点关注 ${chapter.research_relation}。这部分内容主要用于支撑 NLP、LLM、RAG 与知识图谱推理方向的研究积累。后续我会继续补充核心概念、方法细节、实验思路和可汇报的问题。`;
}

function countWords(text: string): number {
  const stripped = text.replace(/[#*`\[\]()>|_~]/g, " ").replace(/\s+/g, " ").trim();
  return stripped ? stripped.split(" ").length : 0;
}

// ── Component ────────────────────────────────────────────

type Props = {
  chapter: Chapter;
  notes: Note[];
};

export function ChapterWorkstation({ chapter, notes }: Props) {
  const [mode, setMode] = useState<"read" | "edit">("read");
  const [selectedNoteId, setSelectedNoteId] = useState<number | undefined>(
    notes.length > 0 ? notes[0].id : undefined,
  );
  const [draft, setDraft] = useState<Note | undefined>(
    notes.length > 0 ? notes[0] : undefined,
  );
  const [saving, setSaving] = useState(false);
  const [toast, setToast] = useState("");
  const [activeSection, setActiveSection] = useState("");
  const contentRef = useRef<HTMLDivElement>(null);

  // Sync draft when selected note changes
  useEffect(() => {
    if (mode === "read") {
      const note = notes.find((n) => n.id === selectedNoteId);
      setDraft(note);
    }
  }, [selectedNoteId, notes, mode]);

  // Toast auto-dismiss
  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(""), 2600);
    return () => clearTimeout(t);
  }, [toast]);

  // Scroll spy for section nav
  useEffect(() => {
    if (mode !== "read" || !contentRef.current) return;
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setActiveSection(entry.target.id);
          }
        }
      },
      { rootMargin: "-80px 0px -60% 0px" },
    );
    const headings = contentRef.current.querySelectorAll("h2[id]");
    headings.forEach((h) => observer.observe(h));
    return () => observer.disconnect();
  }, [mode, draft?.content]);

  // ── Actions ───────────────────────────────────────────

  async function save() {
    if (!draft) return;
    setSaving(true);
    try {
      if (notes.some((n) => n.id === draft.id)) {
        const saved = await api.updateNote(draft.id, {
          source_id: draft.source_id,
          chapter_id: draft.chapter_id,
          title: draft.title,
          content: draft.content,
          tags: draft.tags,
        });
        // Update notes in-place — parent page will re-fetch on navigation
        Object.assign(draft, saved);
      }
      setToast("笔记已保存 ✅");
    } catch {
      setToast("保存失败 ❌");
    } finally {
      setSaving(false);
    }
  }

  async function createNote() {
    try {
      const created = await api.createNote({
        source_id: chapter.source_id,
        chapter_id: chapter.id,
        title: `Chapter ${chapter.number}: ${chapter.title}`,
        content: `# Chapter ${chapter.number}: ${chapter.title}\n\n## 章节定位\n\n## 核心概念\n\n## 内容梳理\n\n## 公式与算法解释\n\n## 例子说明\n\n## 重点总结\n\n## 导师可能提问\n\n## 与 KG-LLM 推理的关系\n\n`,
        tags: chapter.tags.join(","),
      });
      notes.push(created);
      setSelectedNoteId(created.id);
      setDraft(created);
      setMode("edit");
      setToast("已创建空白笔记 ✨");
    } catch {
      setToast("创建失败 ❌");
    }
  }

  async function copyNote(text = draft?.content ?? "") {
    try {
      await navigator.clipboard.writeText(text);
      setToast("已复制到剪贴板 📋");
    } catch {
      setToast("复制失败");
    }
  }

  function exportMarkdown() {
    if (!draft) return;
    const blob = new Blob([draft.content], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `Chapter-${chapter.number}-${chapter.title.replace(/[\\/:*?"<>|]/g, "-")}.md`;
    a.click();
    URL.revokeObjectURL(url);
    setToast("Markdown 已导出 ⬇️");
  }

  function onEdit() {
    if (!draft && notes.length === 0) {
      createNote();
      return;
    }
    if (!draft && notes.length > 0) {
      setDraft(notes[0]);
      setSelectedNoteId(notes[0].id);
    }
    setMode("edit");
  }

  // ── Derived data ──────────────────────────────────────

  const sections = useMemo(() => {
    if (draft?.content) return getSections(draft.content);
    // Fallback: use chapter metadata sections
    return [
      { id: "positioning", title: "章节定位" },
      { id: "core-concepts", title: "核心概念" },
      { id: "outline", title: "内容梳理" },
      { id: "formulas", title: "公式与算法解释" },
      { id: "examples", title: "例子说明" },
      { id: "summary", title: "重点总结" },
      { id: "mentor-questions", title: "导师可能提问" },
      { id: "research-links", title: "与研究方向的联系" },
    ];
  }, [draft?.content]);

  const wordCount = draft ? countWords(draft.content) : 0;

  // Render the markdown with anchor IDs on h2
  const renderedHtml = useMemo(() => {
    if (!draft?.content) return "";
    const raw = (marked.parse(draft.content, { async: false }) as string);
    // Inject id attributes into <h2> tags for scroll-spy
    return raw.replace(/<h2>(.+?)<\/h2>/g, (_match, title) => {
      const text = title.replace(/<[^>]+>/g, "");
      const id = text
        .toLowerCase()
        .replace(/[^a-z0-9\u4e00-\u9fff]+/g, "-")
        .replace(/(^-|^-)/g, "")
        .replace(/-$/g, "");
      return `<h2 id="${id}">${title}</h2>`;
    });
  }, [draft?.content]);

  // Preview in edit mode
  const previewHtml = useMemo(() => {
    if (!draft?.content) return "";
    return (marked.parse(draft.content, { async: false }) as string)
      .replace(/<h2>(.+?)<\/h2>/g, (_m, title) => {
        const text = title.replace(/<[^>]+>/g, "");
        const id = text
          .toLowerCase()
          .replace(/[^a-z0-9\u4e00-\u9fff]+/g, "-")
          .replace(/(^-|^-)/g, "")
          .replace(/-$/g, "");
        return `<h2 id="${id}-preview">${title}</h2>`;
      });
  }, [draft?.content]);

  // ── Render ──────────────────────────────────────────

  return (
    <div className="space-y-6">
      {/* Toast */}
      {toast && (
        <div className="fixed right-4 top-24 z-50 rounded-lg border bg-card px-4 py-3 text-sm font-medium shadow-lg" role="status" aria-live="polite">
          {toast}
        </div>
      )}

      {/* ===== Header ===== */}
      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div className="space-y-3">
          <p className="text-sm text-muted-foreground">Chapter {chapter.number}</p>
          <h2 className="text-3xl font-semibold tracking-normal">{chapter.title}</h2>
          <div className="flex flex-wrap gap-2">
            <Badge className="border-indigo-200 bg-indigo-50 text-indigo-700 dark:border-indigo-400/30 dark:bg-indigo-400/10 dark:text-indigo-200">优先级 {chapter.priority}</Badge>
            <Badge className={cn(
              chapter.status === "已完成" && "border-green-200 bg-green-50 text-green-700 dark:border-green-400/30 dark:bg-green-400/10 dark:text-green-200",
              chapter.status === "阅读中" && "border-amber-200 bg-amber-50 text-amber-700",
              chapter.status === "未开始" && "border-slate-200 bg-slate-50 text-slate-600",
            )}>{chapter.status}</Badge>
            <Badge>{chapter.mastery}</Badge>
            <Badge>{chapter.relevance_score}% 相关度</Badge>
            {draft && <Badge className="border-cyan-200 bg-cyan-50 text-cyan-700">已创建笔记</Badge>}
          </div>
          {chapter.tags.length > 0 && (
            <div className="flex flex-wrap gap-1.5">
              {chapter.tags.map((tag) => (
                <span key={tag} className="inline-flex items-center rounded-full border bg-background/70 px-3 py-0.5 text-xs font-medium text-muted-foreground">{tag}</span>
              ))}
            </div>
          )}
          {draft && (
            <p className="text-xs text-muted-foreground">
              笔记字数：{wordCount} 词 · 最后更新：{new Date(draft.updated_at).toLocaleString("zh-CN")}
            </p>
          )}
        </div>

        {/* Action buttons */}
        <div className="flex flex-wrap gap-2">
          {mode === "read" ? (
            <Button onClick={onEdit}>
              <Pencil className="h-4 w-4" />
              {draft ? "编辑本章笔记" : "创建笔记"}
            </Button>
          ) : (
            <Button onClick={save} disabled={saving}>
              <Save className="h-4 w-4" />
              {saving ? "保存中" : "保存"}
            </Button>
          )}
          {mode === "edit" && (
            <Button variant="outline" onClick={() => { setMode("read"); }}>
              <Eye className="h-4 w-4" />
              返回阅读
            </Button>
          )}
          {draft && (
            <>
              <Button variant="secondary" onClick={() => copyNote()}>
                <Clipboard className="h-4 w-4" />
                复制笔记
              </Button>
              <Button variant="outline" onClick={exportMarkdown}>
                <Download className="h-4 w-4" />
                导出 Markdown
              </Button>
              <Button variant="outline" onClick={() => {
                copyNote(buildReportDraft(chapter));
                setToast("导师汇报草稿已复制 ✨");
              }}>
                <Sparkles className="h-4 w-4" />
                导师汇报草稿
              </Button>
            </>
          )}
        </div>
      </div>

      {/* ===== Main content grid ===== */}
      <div className="grid gap-6 lg:grid-cols-[200px_minmax(0,1fr)_260px]">

        {/* ── Left: Section Nav ── */}
        <aside className="order-2 lg:order-1 lg:sticky lg:top-24 lg:self-start">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-sm">
                <BookOpen className="h-4 w-4" />
                章节结构
              </CardTitle>
            </CardHeader>
            <CardContent>
              <nav className="space-y-0.5">
                {sections.map((section) => (
                  <a
                    key={section.id}
                    href={mode === "read" ? `#${section.id}` : undefined}
                    onClick={(e) => {
                      if (mode !== "read") return;
                      e.preventDefault();
                      const el = document.getElementById(section.id);
                      if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
                    }}
                    className={cn(
                      "block truncate rounded-md px-2 py-1.5 text-xs leading-relaxed transition-colors",
                      activeSection === section.id
                        ? "bg-primary/10 font-medium text-primary"
                        : "text-muted-foreground hover:bg-muted hover:text-foreground",
                    )}
                  >
                    {section.title}
                  </a>
                ))}
              </nav>
            </CardContent>
          </Card>
        </aside>

        {/* ── Center: Main Content ── */}
        <main className="order-3 min-w-0 lg:order-2">
          {mode === "read" && draft?.content ? (
            /* Read mode */
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BookOpen className="h-4 w-4 text-primary" />
                  {draft.title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <article
                  ref={contentRef}
                  className="prose prose-slate max-w-none dark:prose-invert prose-headings:scroll-mt-24 prose-headings:font-semibold prose-h1:text-2xl prose-h2:text-xl prose-h2:text-primary prose-h3:text-lg prose-a:text-primary prose-code:rounded prose-code:bg-muted prose-code:px-1.5 prose-code:py-0.5 prose-code:text-sm prose-pre:rounded-lg prose-pre:bg-muted prose-pre:text-sm prose-img:rounded-lg"
                  dangerouslySetInnerHTML={{ __html: renderedHtml }}
                />
              </CardContent>
            </Card>
          ) : mode === "edit" && draft ? (
            /* Edit mode */
            <div className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Markdown 编辑</CardTitle>
                </CardHeader>
                <CardContent>
                  <Textarea
                    className="min-h-[60dvh] font-mono leading-7 text-sm"
                    value={draft.content}
                    onChange={(e) => setDraft({ ...draft, content: e.target.value })}
                    aria-label="Markdown 内容"
                  />
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>实时预览</CardTitle>
                </CardHeader>
                <CardContent>
                  {previewHtml ? (
                    <article
                      className="prose prose-slate max-w-none dark:prose-invert prose-headings:font-semibold prose-h1:text-2xl prose-h2:text-xl prose-h2:text-primary prose-a:text-primary prose-code:rounded prose-code:bg-muted prose-code:px-1.5 prose-code:text-sm prose-pre:rounded-lg prose-pre:bg-muted"
                      dangerouslySetInnerHTML={{ __html: previewHtml }}
                    />
                  ) : (
                    <p className="text-sm text-muted-foreground">输入 Markdown 后在此预览。</p>
                  )}
                </CardContent>
              </Card>
            </div>
          ) : (
            /* Empty state — no note */
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-16">
                <BookOpen className="h-12 w-12 text-muted-foreground/40" />
                <p className="mt-4 text-lg font-semibold">当前章节还没有完整笔记</p>
                <p className="mt-2 text-sm text-muted-foreground">创建一条笔记即可在此直接查看和编辑。</p>
                <Button className="mt-6" onClick={createNote}>
                  <Pencil className="h-4 w-4" />
                  创建笔记
                </Button>
              </CardContent>
            </Card>
          )}
        </main>

        {/* ── Right: Info Sidebar ── */}
        <aside className="order-4 space-y-4 lg:order-3 lg:sticky lg:top-24 lg:self-start">
          {/* 导师可能提问 */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">导师可能提问</CardTitle>
            </CardHeader>
            <CardContent>
              {chapter.mentor_questions && chapter.mentor_questions.length > 0 ? (
                <ul className="space-y-2 text-sm leading-6 text-muted-foreground">
                  {chapter.mentor_questions.map((q, i) => (
                    <li key={i} className="before:mr-2 before:text-primary before:content-['Q:']">{q}</li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-muted-foreground">暂无预设问题</p>
              )}
            </CardContent>
          </Card>

          {/* 后续补充资料 */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">后续补充资料</CardTitle>
            </CardHeader>
            <CardContent>
              {chapter.resources && chapter.resources.length > 0 ? (
                <ul className="space-y-1.5 text-sm leading-6 text-muted-foreground">
                  {chapter.resources.map((r, i) => (
                    <li key={i} className="flex items-start gap-2 before:mt-[7px] before:h-1 before:w-1 before:shrink-0 before:rounded-full before:bg-primary/60">
                      {r}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-muted-foreground">暂无补充资料</p>
              )}
            </CardContent>
          </Card>

          {/* 相关标签 */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">相关标签</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-wrap gap-1.5">
              {chapter.tags.map((tag) => (
                <span key={tag} className="inline-flex items-center rounded-full border bg-secondary/50 px-2.5 py-0.5 text-xs font-medium text-muted-foreground">{tag}</span>
              ))}
            </CardContent>
          </Card>

          {/* 研究关联 */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">与研究方向的联系</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm leading-6 text-muted-foreground">{chapter.research_relation}</p>
            </CardContent>
          </Card>
        </aside>
      </div>
    </div>
  );
}
