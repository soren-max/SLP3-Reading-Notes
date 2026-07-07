"use client";

import { useMemo, useState } from "react";
import { Search, SlidersHorizontal } from "lucide-react";

import { ChapterCard } from "@/components/chapter-card";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { TagChip } from "@/components/tag-chip";
import type { Chapter } from "@/lib/api";

const priorities = ["全部", "高", "中", "低"] as const;
const statuses = ["全部", "未开始", "阅读中", "已完成"] as const;

export function ChapterExplorer({ chapters }: { chapters: Chapter[] }) {
  const [query, setQuery] = useState("");
  const [priority, setPriority] = useState<(typeof priorities)[number]>("全部");
  const [status, setStatus] = useState<(typeof statuses)[number]>("全部");
  const [tag, setTag] = useState("全部");
  const tags = useMemo(() => ["全部", ...Array.from(new Set(chapters.flatMap((chapter) => chapter.tags))).sort()], [chapters]);

  const filtered = chapters.filter((chapter) => {
    const text = `${chapter.number} ${chapter.title} ${chapter.research_relation} ${chapter.tags.join(" ")}`.toLowerCase();
    return (
      (!query || text.includes(query.toLowerCase())) &&
      (priority === "全部" || chapter.priority === priority) &&
      (status === "全部" || chapter.status === status) &&
      (tag === "全部" || chapter.tags.includes(tag))
    );
  });

  return (
    <div className="space-y-5">
      <Card>
        <CardContent className="grid gap-4 p-4 lg:grid-cols-[1fr_auto_auto] lg:items-center">
          <div className="relative">
            <Search className="absolute left-3 top-3.5 h-4 w-4 text-muted-foreground" />
            <Input className="pl-9" placeholder="搜索章节、标签或研究关系" value={query} onChange={(event) => setQuery(event.target.value)} />
          </div>
          <div className="flex flex-wrap gap-2">
            {priorities.map((item) => (
              <TagChip key={item} label={item === "全部" ? "全部优先级" : `${item}优先级`} active={priority === item} onClick={() => setPriority(item)} />
            ))}
          </div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <SlidersHorizontal className="h-4 w-4" />
            {filtered.length} / {chapters.length}
          </div>
        </CardContent>
      </Card>

      <div className="flex flex-wrap gap-2">
        {statuses.map((item) => (
          <TagChip key={item} label={item} active={status === item} onClick={() => setStatus(item)} />
        ))}
      </div>
      <div className="flex flex-wrap gap-2">
        {tags.map((item) => (
          <TagChip key={item} label={item} active={tag === item} onClick={() => setTag(item)} />
        ))}
      </div>

      {filtered.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {filtered.map((chapter) => (
            <ChapterCard key={chapter.id} chapter={chapter} />
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="p-10 text-center">
            <p className="text-lg font-semibold">没有匹配章节</p>
            <p className="mt-2 text-sm text-muted-foreground">调整搜索词、优先级、状态或方向标签后再试。</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
