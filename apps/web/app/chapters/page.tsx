import { ChapterCard } from "@/components/chapter-card";
import { api, type Chapter } from "@/lib/api";

function groupByPriority(chapters: Chapter[], priority: Chapter["priority"]) {
  return chapters.filter((chapter) => chapter.priority === priority);
}

export default async function ChaptersPage() {
  const chapters = await api.chapters();
  const groups: Chapter["priority"][] = ["高", "中", "低"];

  return (
    <div className="space-y-8">
      <div>
        <p className="text-sm text-muted-foreground">Chapters</p>
        <h2 className="mt-2 text-3xl font-semibold tracking-normal">章节目录与阅读优先级</h2>
        <p className="mt-3 max-w-3xl text-muted-foreground">按 KG-LLM 推理方向重新组织 SLP3 章节，突出检索增强、信息抽取、实体链接和推理相关内容。</p>
      </div>
      {groups.map((priority) => (
        <section key={priority} className="space-y-3">
          <h3 className="text-xl font-semibold">{priority}优先级</h3>
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {groupByPriority(chapters, priority).map((chapter) => (
              <ChapterCard key={chapter.id} chapter={chapter} />
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}
