import Link from "next/link";
import { notFound } from "next/navigation";
import { BookOpen, FileText } from "lucide-react";

import { ChapterCard } from "@/components/chapter-card";
import { TagChip } from "@/components/tag-chip";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

type Props = { params: Promise<{ id: string }> };

const paperBlocks = [
  "背景",
  "问题",
  "方法",
  "实验",
  "创新点",
  "不足",
  "和研究方向的联系",
  "可复现思路",
];

export default async function SourceDetailPage({ params }: Props) {
  const { id } = await params;
  const sourceId = Number(id);
  if (Number.isNaN(sourceId)) notFound();

  let source;
  try {
    source = await api.source(sourceId);
  } catch {
    notFound();
  }
  const chapters = await api.chaptersBySource(source.id);
  const directions = source.research_direction.split(",").map((item) => item.trim()).filter(Boolean);

  return (
    <div className="space-y-6">
      <section className="rounded-lg border bg-card/80 p-6 shadow-sm backdrop-blur-xl">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
          <div className="space-y-3">
            <div className="flex flex-wrap gap-2">
              <Badge>{source.type}</Badge>
              <Badge>{source.status}</Badge>
              <Badge>优先级 {source.priority}</Badge>
            </div>
            <h2 className="text-3xl font-semibold tracking-normal">{source.title}</h2>
            <p className="text-sm text-muted-foreground">{source.author_or_origin}</p>
            <p className="max-w-4xl leading-7 text-muted-foreground">{source.description}</p>
            <div className="flex flex-wrap gap-2">
              {directions.map((item) => <TagChip key={item} label={item} />)}
            </div>
          </div>
          <Link className="inline-flex min-h-11 items-center justify-center rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground no-underline" href={`/notes?sourceId=${source.id}`}>
            编辑资料笔记
          </Link>
        </div>
      </section>

      {(source.type === "book" || source.type === "course") ? (
        <section className="space-y-3">
          <h3 className="flex items-center gap-2 text-xl font-semibold">
            <BookOpen className="h-5 w-5 text-primary" />
            章节目录
          </h3>
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {chapters.map((chapter) => <ChapterCard key={chapter.id} chapter={chapter} />)}
          </div>
        </section>
      ) : (
        <section className="space-y-3">
          <h3 className="flex items-center gap-2 text-xl font-semibold">
            <FileText className="h-5 w-5 text-primary" />
            论文/资料阅读模块
          </h3>
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {paperBlocks.map((block) => (
              <Card key={block}>
                <CardHeader>
                  <CardTitle>{block}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm leading-6 text-muted-foreground">在 Notes 页面补充 {block} 相关笔记，并关联到当前资料。</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
