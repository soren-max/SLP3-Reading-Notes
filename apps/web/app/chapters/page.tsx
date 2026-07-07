import { ChapterExplorer } from "@/components/chapter-explorer";
import { api } from "@/lib/api";

export default async function ChaptersPage() {
  const chapters = await api.chapters();

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm text-muted-foreground">Chapters</p>
        <h2 className="mt-2 text-3xl font-semibold tracking-normal">章节目录与研究优先级</h2>
        <p className="mt-3 max-w-3xl text-muted-foreground">按 KG-LLM 推理方向重新组织 SLP3 章节，突出检索增强、信息抽取、实体链接和推理相关内容。</p>
      </div>
      <ChapterExplorer chapters={chapters} />
    </div>
  );
}
