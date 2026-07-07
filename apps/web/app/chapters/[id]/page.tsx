import Link from "next/link";
import { notFound } from "next/navigation";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

type Props = { params: Promise<{ id: string }> };

export default async function ChapterDetailPage({ params }: Props) {
  const { id } = await params;
  const chapterId = Number(id);
  if (Number.isNaN(chapterId)) notFound();

  let chapter;
  try {
    chapter = await api.chapter(chapterId);
  } catch {
    notFound();
  }

  const blocks = [
    ["章节定位", chapter.positioning],
    ["内容梳理", chapter.outline],
    ["公式与算法解释", chapter.formulas_algorithms],
    ["例子说明", chapter.examples],
    ["重点总结", chapter.summary],
    ["和研究方向的联系", chapter.research_links],
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <p className="text-sm text-muted-foreground">Chapter {chapter.number}</p>
          <h2 className="mt-2 text-3xl font-semibold tracking-normal">{chapter.title}</h2>
          <div className="mt-4 flex flex-wrap gap-2">
            <Badge>优先级 {chapter.priority}</Badge>
            <Badge>{chapter.status}</Badge>
            <Badge>{chapter.mastery}</Badge>
            <Badge>{chapter.relevance_score}% 相关度</Badge>
          </div>
        </div>
        <Link className="inline-flex min-h-11 items-center justify-center rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground no-underline" href={`/notes?chapterId=${chapter.id}`}>
          编辑本章笔记
        </Link>
      </div>

      <div className="grid gap-4 lg:grid-cols-[1fr_320px]">
        <div className="space-y-4">
          {blocks.map(([title, content]) => (
            <Card key={title}>
              <CardHeader>
                <CardTitle>{title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="leading-7 text-muted-foreground">{content}</p>
              </CardContent>
            </Card>
          ))}
        </div>
        <aside className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>核心概念</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-wrap gap-2">
              {chapter.core_concepts?.map((item) => (
                <Badge key={item} className="bg-secondary">
                  {item}
                </Badge>
              ))}
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>导师可能提问</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3 text-sm leading-6 text-muted-foreground">
                {chapter.mentor_questions?.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>后续补充资料</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                {chapter.resources?.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </aside>
      </div>
    </div>
  );
}
