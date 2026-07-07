"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { marked } from "marked";
import { Clipboard, Download, Eye, Pencil, Save, Sparkles } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { api, type Chapter, type Note } from "@/lib/api";
import { cn } from "@/lib/utils";

// ── Helpers ──────────────────────────────────────────────

function buildReportDraft(chapter: Chapter) {
  return `老师您好，我本阶段在整理《Chapter ${chapter.number} ${chapter.title}》的学习笔记，当前重点关注 ${chapter.research_relation}。这部分内容主要用于支撑 NLP、LLM、RAG 与知识图谱推理方向的研究积累。后续我会继续补充核心概念、方法细节、实验思路和可汇报的问题。`;
}

function countWords(text: string): number {
  const stripped = text.replace(/[#*`\[\]()>|_~]/g, " ").replace(/\s+/g, " ").trim();
  return stripped ? stripped.split(" ").length : 0;
}

function renderMarkdown(md: string): string {
  const raw = marked.parse(md, { async: false }) as string;
  // Inject id attributes into h2 for scroll anchoring
  return raw.replace(/<h2>(.+?)<\/h2>/g, (_m, title) => {
    const text = title.replace(/<[^>]+>/g, "");
    const id = text
      .toLowerCase()
      .replace(/[^a-z0-9\u4e00-\u9fff]+/g, "-")
      .replace(/(^-|-$)/g, "");
    return `<h2 id="${id}">${title}</h2>`;
  });
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
  const mainRef = useRef<HTMLDivElement>(null);

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

  const wordCount = draft ? countWords(draft.content) : 0;
  const renderedHtml = useMemo(
    () => (draft?.content ? renderMarkdown(draft.content) : ""),
    [draft?.content],
  );
  const previewHtml = useMemo(
    () => (draft?.content ? renderMarkdown(draft.content) : ""),
    [draft?.content],
  );

  // Whether we have rich chapter metadata to show as structured summary
  const hasChapterSummary = Boolean(chapter.positioning || chapter.outline || chapter.formulas_algorithms || chapter.summary);

  // ── Render ──────────────────────────────────────────

  return (
    <div className="mx-auto max-w-7xl">
      {/* Toast */}
      {toast && (
        <div
          className="fixed right-4 top-24 z-50 rounded-lg border bg-card px-4 py-3 text-sm font-medium shadow-lg"
          role="status"
          aria-live="polite"
        >
          {toast}
        </div>
      )}

      {/* ===== Sticky Header ===== */}
      <div className="sticky top-0 z-10 -mx-4 -mt-6 border-b bg-background/80 px-4 pb-3 pt-4 backdrop-blur-xl sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8">
        <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
          <div className="min-w-0 space-y-2">
            <p className="text-sm text-muted-foreground">Chapter {chapter.number}</p>
            <h1 className="truncate text-2xl font-semibold tracking-tight sm:text-3xl">
              {chapter.title}
            </h1>
            <div className="flex flex-wrap items-center gap-2">
              <Badge className="border-indigo-200 bg-indigo-50 text-indigo-700 dark:border-indigo-400/30 dark:bg-indigo-400/10 dark:text-indigo-200">
                {chapter.priority}
              </Badge>
              <Badge
                className={cn(
                  chapter.status === "已完成" &&
                    "border-green-200 bg-green-50 text-green-700 dark:border-green-400/30 dark:bg-green-400/10 dark:text-green-200",
                  chapter.status === "阅读中" &&
                    "border-amber-200 bg-amber-50 text-amber-700",
                  chapter.status === "未开始" &&
                    "border-slate-200 bg-slate-50 text-slate-600",
                )}
              >
                {chapter.status}
              </Badge>
              <Badge>{chapter.mastery}</Badge>
              <Badge>{chapter.relevance_score}% 相关度</Badge>
              {draft && (
                <Badge className="border-cyan-200 bg-cyan-50 text-cyan-700">
                  已有笔记 · {wordCount} 词
                </Badge>
              )}
            </div>
          </div>

          {/* ── Action Buttons ── */}
          <div className="flex shrink-0 flex-wrap gap-2">
            {mode === "read" ? (
              <Button onClick={onEdit} size="sm">
                <Pencil className="mr-1.5 h-4 w-4" />
                {draft ? "编辑笔记" : "创建笔记"}
              </Button>
            ) : (
              <Button onClick={save} disabled={saving} size="sm">
                <Save className="mr-1.5 h-4 w-4" />
                {saving ? "保存中..." : "保存"}
              </Button>
            )}
            {mode === "edit" && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  setMode("read");
                }}
              >
                <Eye className="mr-1.5 h-4 w-4" />
                阅读模式
              </Button>
            )}
            {draft && mode === "read" && (
              <>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => copyNote()}
                >
                  <Clipboard className="mr-1.5 h-4 w-4" />
                  复制
                </Button>
                <Button variant="outline" size="sm" onClick={exportMarkdown}>
                  <Download className="mr-1.5 h-4 w-4" />
                  导出
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    copyNote(buildReportDraft(chapter));
                    setToast("导师汇报草稿已复制 ✨");
                  }}
                >
                  <Sparkles className="mr-1.5 h-4 w-4" />
                  汇报草稿
                </Button>
              </>
            )}
          </div>
        </div>
      </div>

      {/* ===== Main Grid ===== */}
      <div className="mt-6 grid gap-8 lg:grid-cols-[1fr_320px]">
        {/* ── Main Content ── */}
        <main ref={mainRef} className="min-w-0 space-y-8">
          {mode === "read" && draft?.content ? (
            <>
              {/* Block 1: Full Markdown Note */}
              <section>
                <article
                  className={proseClass}
                  dangerouslySetInnerHTML={{ __html: renderedHtml }}
                />
              </section>
            </>
          ) : mode === "edit" && draft ? (
            /* ── Edit Mode ── */
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Markdown 编辑</CardTitle>
                </CardHeader>
                <CardContent>
                  <Textarea
                    className="min-h-[50dvh] font-mono leading-7 text-sm"
                    value={draft.content}
                    onChange={(e) =>
                      setDraft({ ...draft, content: e.target.value })
                    }
                    aria-label="Markdown 内容"
                  />
                </CardContent>
              </Card>

              <div>
                <h3 className="mb-3 text-lg font-semibold">实时预览</h3>
                {previewHtml ? (
                  <article
                    className={proseClass}
                    dangerouslySetInnerHTML={{ __html: previewHtml }}
                  />
                ) : (
                  <p className="text-sm text-muted-foreground">
                    输入 Markdown 后在此预览。
                  </p>
                )}
              </div>
            </div>
          ) : (
            /* ── Empty State ── */
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-20">
                <div className="text-4xl text-muted-foreground/30">📖</div>
                <p className="mt-4 text-lg font-semibold">
                  当前章节还没有完整笔记
                </p>
                <p className="mt-2 text-sm text-muted-foreground">
                  点击「创建笔记」即可在此直接编写和阅读完整学习笔记。
                </p>
                <Button className="mt-6" onClick={createNote}>
                  <Pencil className="mr-1.5 h-4 w-4" />
                  创建笔记
                </Button>
              </CardContent>
            </Card>
          )}

          {/* Block 2: Chapter Structured Summary (only if has content) */}
          {mode === "read" && hasChapterSummary && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <span className="text-xl">📋</span>
                  章节结构化摘要
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-5">
                {chapter.positioning && (
                  <div>
                    <h4 className="mb-1.5 text-sm font-semibold text-muted-foreground">
                      章节定位
                    </h4>
                    <p className="text-sm leading-7 text-muted-foreground">
                      {chapter.positioning}
                    </p>
                  </div>
                )}
                {chapter.outline && (
                  <div>
                    <h4 className="mb-1.5 text-sm font-semibold text-muted-foreground">
                      内容梳理
                    </h4>
                    <p className="text-sm leading-7 text-muted-foreground">
                      {chapter.outline}
                    </p>
                  </div>
                )}
                {chapter.formulas_algorithms && (
                  <div>
                    <h4 className="mb-1.5 text-sm font-semibold text-muted-foreground">
                      公式与算法解释
                    </h4>
                    <p className="text-sm leading-7 text-muted-foreground">
                      {chapter.formulas_algorithms}
                    </p>
                  </div>
                )}
                {chapter.summary && (
                  <div>
                    <h4 className="mb-1.5 text-sm font-semibold text-muted-foreground">
                      重点总结
                    </h4>
                    <p className="text-sm leading-7 text-muted-foreground">
                      {chapter.summary}
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          )}

          {/* Block 3: Mentor Questions */}
          {mode === "read" &&
            chapter.mentor_questions &&
            chapter.mentor_questions.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-lg">
                    <span className="text-xl">❓</span>
                    导师可能提问
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-3">
                    {chapter.mentor_questions.map((q, i) => (
                      <li
                        key={i}
                        className="rounded-lg border bg-muted/30 px-4 py-3 text-sm leading-7"
                      >
                        <span className="font-semibold text-primary">
                          Q{i + 1}：
                        </span>
                        {q}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}

          {/* Block 4: KG-LLM Research Relation */}
          {mode === "read" && chapter.research_relation && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <span className="text-xl">🔗</span>
                  与 KG-LLM 方向的联系
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm leading-7 text-muted-foreground">
                  {chapter.research_relation}
                </p>
              </CardContent>
            </Card>
          )}
        </main>

        {/* ── Right Sidebar ── */}
        <aside className="hidden space-y-5 lg:sticky lg:top-28 lg:block lg:self-start">
          {/* Core Concepts */}
          {chapter.core_concepts && chapter.core_concepts.length > 0 && (
            <div>
              <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                核心概念
              </h4>
              <div className="flex flex-wrap gap-1.5">
                {chapter.core_concepts.map((item) => (
                  <span
                    key={item}
                    className="inline-flex items-center rounded-md border bg-secondary/40 px-2.5 py-1 text-xs font-medium text-foreground/80"
                  >
                    {item}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Chapter Info */}
          <div>
            <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              阅读信息
            </h4>
            <div className="space-y-2 rounded-lg border bg-card/50 px-4 py-3 text-sm">
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">状态</span>
                <span
                  className={cn(
                    "font-medium",
                    chapter.status === "已完成" && "text-green-600",
                    chapter.status === "阅读中" && "text-amber-600",
                    chapter.status === "未开始" && "text-slate-500",
                  )}
                >
                  {chapter.status}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">优先级</span>
                <span className="font-medium">{chapter.priority}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">掌握程度</span>
                <span className="font-medium">{chapter.mastery}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">相关度</span>
                <span className="font-medium">
                  {chapter.relevance_score}%
                </span>
              </div>
              {draft && (
                <div className="border-t pt-2 text-xs text-muted-foreground">
                  笔记更新于{" "}
                  {new Date(draft.updated_at).toLocaleDateString("zh-CN", {
                    year: "numeric",
                    month: "2-digit",
                    day: "2-digit",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </div>
              )}
            </div>
          </div>

          {/* Tags */}
          {chapter.tags.length > 0 && (
            <div>
              <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                研究方向标签
              </h4>
              <div className="flex flex-wrap gap-1.5">
                {chapter.tags.map((tag) => (
                  <span
                    key={tag}
                    className="inline-flex items-center rounded-full border bg-card/50 px-2.5 py-0.5 text-xs font-medium text-muted-foreground"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Quick Mentor Questions (condensed) */}
          {chapter.mentor_questions &&
            chapter.mentor_questions.length > 0 && (
              <div>
                <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  导师提问速览
                </h4>
                <ul className="space-y-2">
                  {chapter.mentor_questions.slice(0, 3).map((q, i) => (
                    <li
                      key={i}
                      className="rounded-lg border bg-card/40 px-3 py-2 text-xs leading-5 text-muted-foreground"
                    >
                      <span className="font-semibold text-primary">
                        Q{i + 1}{" "}
                      </span>
                      {q}
                    </li>
                  ))}
                </ul>
              </div>
            )}

          {/* Quick Actions */}
          {draft && mode === "read" && (
            <div>
              <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                快捷操作
              </h4>
              <div className="space-y-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full justify-start text-xs"
                  onClick={onEdit}
                >
                  <Pencil className="mr-2 h-3.5 w-3.5" />
                  编辑笔记
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full justify-start text-xs"
                  onClick={() => copyNote()}
                >
                  <Clipboard className="mr-2 h-3.5 w-3.5" />
                  复制笔记
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full justify-start text-xs"
                  onClick={exportMarkdown}
                >
                  <Download className="mr-2 h-3.5 w-3.5" />
                  导出 Markdown
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full justify-start text-xs"
                  onClick={() => {
                    copyNote(buildReportDraft(chapter));
                    setToast("导师汇报草稿已复制 ✨");
                  }}
                >
                  <Sparkles className="mr-2 h-3.5 w-3.5" />
                  汇报草稿
                </Button>
              </div>
            </div>
          )}

          {/* Resources */}
          {chapter.resources && chapter.resources.length > 0 && (
            <div>
              <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                参考资料
              </h4>
              <ul className="space-y-1.5 text-xs leading-5 text-muted-foreground">
                {chapter.resources.map((r, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="mt-[5px] h-1 w-1 shrink-0 rounded-full bg-primary/50" />
                    {r}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </aside>
      </div>
    </div>
  );
}

// Shared prose class for consistent markdown rendering
const proseClass = cn(
  "prose prose-slate max-w-none dark:prose-invert",
  // Heading hierarchy
  "prose-h1:text-2xl prose-h1:font-semibold prose-h1:tracking-tight prose-h1:mt-10 prose-h1:mb-4",
  "prose-h2:text-xl prose-h2:font-semibold prose-h2:text-primary prose-h2:mt-8 prose-h2:mb-3 prose-h2:scroll-mt-24",
  "prose-h3:text-lg prose-h3:font-medium prose-h3:mt-6 prose-h3:mb-2",
  // Body text — comfortable for Chinese
  "prose-p:leading-8 prose-p:my-3 prose-p:text-base",
  // Lists
  "prose-ul:my-3 prose-ul:space-y-1.5",
  "prose-ol:my-3 prose-ol:space-y-1.5",
  "prose-li:leading-7",
  // Code
  "prose-code:rounded prose-code:bg-muted prose-code:px-1.5 prose-code:py-0.5 prose-code:text-sm prose-code:font-normal",
  "prose-pre:rounded-lg prose-pre:bg-muted/80 prose-pre:border prose-pre:text-sm prose-pre:leading-6",
  // Tables
  "prose-table:block prose-table:overflow-x-auto prose-table:whitespace-nowrap",
  "prose-th:bg-muted/50 prose-th:px-3 prose-th:py-2 prose-th:text-sm",
  "prose-td:px-3 prose-td:py-2 prose-td:text-sm",
  // Blockquotes
  "prose-blockquote:border-l-primary prose-blockquote:bg-muted/20 prose-blockquote:px-4 prose-blockquote:py-2 prose-blockquote:rounded-r-lg",
  // Links
  "prose-a:text-primary prose-a:no-underline hover:prose-a:underline",
  // Horizontal rules
  "prose-hr:my-8",
);
