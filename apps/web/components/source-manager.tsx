"use client";

import { useMemo, useState } from "react";
import { Plus, Search } from "lucide-react";

import { SourceCard } from "@/components/source-card";
import { TagChip } from "@/components/tag-chip";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { api, type Source, type SourceType } from "@/lib/api";

const sourceTypes: Array<SourceType | "all"> = ["all", "book", "paper", "course", "project", "report", "misc"];
const sourceTypeLabels: Record<SourceType | "all", string> = {
  all: "全部来源",
  book: "书籍",
  paper: "论文",
  course: "课程",
  project: "项目",
  report: "汇报",
  misc: "其他",
};

const emptyForm: Omit<Source, "id"> = {
  title: "",
  type: "paper",
  author_or_origin: "",
  research_direction: "LLM, RAG, KG",
  description: "",
  status: "未开始",
  priority: "中",
};

export function SourceManager({ initialSources }: { initialSources: Source[] }) {
  const [sources, setSources] = useState(initialSources);
  const [query, setQuery] = useState("");
  const [type, setType] = useState<SourceType | "all">("all");
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState(emptyForm);
  const directions = useMemo(() => ["全部方向", ...Array.from(new Set(sources.flatMap((source) => source.research_direction.split(",").map((item) => item.trim()).filter(Boolean)))).sort()], [sources]);
  const [direction, setDirection] = useState("全部方向");

  const filtered = sources.filter((source) => {
    const text = `${source.title} ${source.author_or_origin} ${source.description} ${source.research_direction}`.toLowerCase();
    return (!query || text.includes(query.toLowerCase())) && (type === "all" || source.type === type) && (direction === "全部方向" || source.research_direction.includes(direction));
  });

  async function createSource() {
    if (!form.title.trim()) return;
    const created = await api.createSource(form);
    setSources((items) => [created, ...items]);
    setForm(emptyForm);
    setShowForm(false);
  }

  return (
    <div className="space-y-5">
      <Card>
        <CardContent className="grid gap-4 p-4 lg:grid-cols-[1fr_auto] lg:items-center">
          <div className="relative">
            <Search className="absolute left-3 top-3.5 h-4 w-4 text-muted-foreground" />
            <Input className="pl-9" placeholder="搜索书籍、论文、课程、项目或研究方向" value={query} onChange={(event) => setQuery(event.target.value)} />
          </div>
          <Button onClick={() => setShowForm((value) => !value)}>
            <Plus className="h-4 w-4" />
            添加资料
          </Button>
        </CardContent>
      </Card>

      <div className="flex flex-wrap gap-2">
        {sourceTypes.map((item) => (
          <TagChip key={item} label={sourceTypeLabels[item]} active={type === item} onClick={() => setType(item)} />
        ))}
      </div>
      <div className="flex flex-wrap gap-2">
        {directions.map((item) => (
          <TagChip key={item} label={item} active={direction === item} onClick={() => setDirection(item)} />
        ))}
      </div>

      {showForm && (
        <Card>
          <CardHeader>
            <CardTitle>新增学习资料</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-3 md:grid-cols-2">
            <Input placeholder="资料标题" value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} />
            <Input placeholder="作者或来源" value={form.author_or_origin} onChange={(event) => setForm({ ...form, author_or_origin: event.target.value })} />
            <select className="min-h-11 rounded-md border bg-background/80 px-3 text-sm focus-ring" value={form.type} onChange={(event) => setForm({ ...form, type: event.target.value as SourceType })}>
              {sourceTypes.filter((item) => item !== "all").map((item) => <option key={item} value={item}>{sourceTypeLabels[item]}</option>)}
            </select>
            <Input placeholder="研究方向，例如 LLM, RAG, KG" value={form.research_direction} onChange={(event) => setForm({ ...form, research_direction: event.target.value })} />
            <select className="min-h-11 rounded-md border bg-background/80 px-3 text-sm focus-ring" value={form.status} onChange={(event) => setForm({ ...form, status: event.target.value as Source["status"] })}>
              {["未开始", "进行中", "已完成"].map((item) => <option key={item} value={item}>{item}</option>)}
            </select>
            <select className="min-h-11 rounded-md border bg-background/80 px-3 text-sm focus-ring" value={form.priority} onChange={(event) => setForm({ ...form, priority: event.target.value as Source["priority"] })}>
              {["高", "中", "低"].map((item) => <option key={item} value={item}>{item}</option>)}
            </select>
            <Textarea className="md:col-span-2" placeholder="简介" value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} />
            <div className="md:col-span-2">
              <Button onClick={createSource}>保存资料</Button>
            </div>
          </CardContent>
        </Card>
      )}

      {filtered.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {filtered.map((source) => (
            <SourceCard key={source.id} source={source} />
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="p-10 text-center text-sm text-muted-foreground">没有匹配的学习资料。</CardContent>
        </Card>
      )}
    </div>
  );
}
