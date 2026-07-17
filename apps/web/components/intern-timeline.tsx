"use client";

import { useMemo, useState } from "react";
import { marked } from "marked";
import { Calendar, ChevronDown, ChevronUp, Hash, Tag, Building2, Clipboard } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { TagChip } from "@/components/tag-chip";
import { type InternRecord } from "@/lib/api";
import { cn } from "@/lib/utils";

export function InternTimeline({ records }: { records: InternRecord[] }) {
  const [search, setSearch] = useState("");
  const [expandedId, setExpandedId] = useState<number | null>(null);

  const filtered = useMemo(() => {
    if (!search) return records;
    const needle = search.toLowerCase();
    return records.filter(
      (r) =>
        r.title.toLowerCase().includes(needle) ||
        r.content.toLowerCase().includes(needle) ||
        r.tags.toLowerCase().includes(needle)
    );
  }, [records, search]);

  const toggleExpand = (id: number) => {
    setExpandedId((prev) => (prev === id ? null : id));
  };

  const copyContent = async (content: string) => {
    await navigator.clipboard.writeText(content);
  };

  if (records.length === 0) {
    return (
      <Card>
        <CardContent className="p-12 text-center">
          <Building2 className="mx-auto h-10 w-10 text-muted-foreground" />
          <p className="mt-4 text-lg font-semibold">暂无实习记录</p>
          <p className="mt-2 text-sm text-muted-foreground">实习记录将通过 API 自动同步。</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <div className="relative max-w-md">
        <Input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="搜索实习记录..."
          aria-label="搜索实习记录"
        />
      </div>

      <div className="space-y-4">
        {filtered.map((record) => {
          const expanded = expandedId === record.id;
          const tagList = record.tags
            .split(",")
            .map((t) => t.trim())
            .filter(Boolean);
          const previewHtml = expanded
            ? (marked.parse(record.content, { async: false }) as string)
            : "";

          return (
            <Card key={record.id} className="overflow-hidden transition-all duration-200 hover:shadow-md">
              <button
                onClick={() => toggleExpand(record.id)}
                className="w-full cursor-pointer text-left focus-ring"
                aria-expanded={expanded}
              >
                <CardHeader className="flex flex-row items-start justify-between gap-4 pb-2">
                  <div className="space-y-1">
                    <div className="flex items-center gap-3">
                      <span className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-indigo-600 to-cyan-500 text-sm font-bold text-white shadow-sm">
                        {record.day}
                      </span>
                      <div>
                        <CardTitle className="text-lg">{record.title}</CardTitle>
                        <div className="mt-1 flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
                          <span className="flex items-center gap-1">
                            <Hash className="h-3 w-3" />
                            Day {record.day}
                          </span>
                          <span className="flex items-center gap-1">
                            <Calendar className="h-3 w-3" />
                            {record.record_date}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="shrink-0">
                    {expanded ? (
                      <ChevronUp className="h-5 w-5 text-muted-foreground" />
                    ) : (
                      <ChevronDown className="h-5 w-5 text-muted-foreground" />
                    )}
                  </div>
                </CardHeader>
              </button>

              <CardContent>
                {tagList.length > 0 && (
                  <div className="mb-3 flex flex-wrap items-center gap-1.5">
                    <Tag className="h-3.5 w-3.5 text-muted-foreground" />
                    {tagList.map((t) => (
                      <TagChip key={t} label={t} />
                    ))}
                  </div>
                )}

                {expanded ? (
                  <div className="space-y-4">
                    <article
                      className="prose prose-slate max-w-none dark:prose-invert"
                      dangerouslySetInnerHTML={{ __html: previewHtml }}
                    />
                    <div className="flex gap-2 pt-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => copyContent(record.content)}
                      >
                        <Clipboard className="h-4 w-4" />
                        复制内容
                      </Button>
                    </div>
                  </div>
                ) : (
                  <p className={cn("line-clamp-3 text-sm text-muted-foreground")}>
                    {record.content.replace(/[#*\[\]`>_\-|]/g, "").slice(0, 200)}...
                  </p>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>

      {filtered.length === 0 && (
        <div className="rounded-lg border border-dashed p-10 text-center text-sm text-muted-foreground">
          没有匹配的实习记录
        </div>
      )}
    </div>
  );
}