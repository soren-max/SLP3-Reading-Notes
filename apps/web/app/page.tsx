import { ArrowRight, BrainCircuit } from "lucide-react";

import { ChapterCard } from "@/components/chapter-card";
import { ProgressOverview } from "@/components/progress-overview";
import { ResearchThread } from "@/components/research-thread";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

export default async function DashboardPage() {
  const [sources, chapters, report] = await Promise.all([api.sources(), api.chapters(), api.report()]);
  const defaultSource = sources[0];
  const topRelevant = [...chapters].sort((a, b) => b.relevance_score - a.relevance_score).slice(0, 4);
  const completed = chapters.filter((chapter) => chapter.status === "已完成").length;
  const highPriority = chapters.filter((chapter) => chapter.priority === "高").length;
  const kgRelated = chapters.filter((chapter) => chapter.tags.includes("KG")).length;

  return (
    <div className="space-y-12">
      <section className="border-b pb-12 sm:pb-16">
        <div className="grid gap-10 lg:grid-cols-[1.25fr_0.75fr] lg:items-center">
          <div className="space-y-4">
            <Badge className="border-primary/25 bg-primary/10 text-primary">Research · Engineering · Reflection</Badge>
            <h2 className="display-type max-w-4xl text-4xl leading-[1.12] sm:text-6xl">
              研究、工程与工作的
              <span className="text-primary"> 连续记录</span>
            </h2>
            <p className="max-w-3xl text-base leading-7 text-muted-foreground">
              A structured learning workspace for NLP, LLM, RAG and Knowledge Graph reasoning. 当前默认内置 SLP3 重点阅读路线，也支持继续添加论文、课程、项目复盘和导师汇报。
            </p>
            <div className="flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
              <span>默认资料：{defaultSource?.title}</span>
              <ArrowRight className="h-4 w-4" />
              <span>下一阶段：GraphRAG 论文路线</span>
            </div>
          </div>
          <Card className="technical-panel border-0 text-[#f4f1ea]">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BrainCircuit className="h-5 w-5 text-[#e8a55a]" />
                Research Focus
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm leading-6 text-[#c7c1b6]">
              <p>Question → Entity Recognition → Subgraph Retrieval → Evidence Path → LLM Reasoning</p>
              <div className="grid grid-cols-2 gap-2">
                {["KG-RAG", "GraphRAG", "NER", "Entity Linking"].map((item) => (
                  <span key={item} className="rounded-md border border-white/10 bg-white/5 px-3 py-2 font-medium text-[#f4f1ea]">
                    {item}
                  </span>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      <ProgressOverview percent={report.progress_percent} completed={completed} highPriority={highPriority} kgRelated={kgRelated} nextTask="Retrieval-based Models / GraphRAG papers" currentStage={`${sources.length} 个学习资料 · ${defaultSource?.status ?? "进行中"}`} />

      <section className="space-y-4">
        <h3 className="display-type text-3xl">研究主线</h3>
        <ResearchThread />
      </section>

      <section className="space-y-4">
        <h3 className="display-type text-3xl">与研究方向相关度最高的章节</h3>
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {topRelevant.map((chapter) => (
            <ChapterCard key={chapter.id} chapter={chapter} />
          ))}
        </div>
      </section>
    </div>
  );
}
