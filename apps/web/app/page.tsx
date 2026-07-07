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
    <div className="space-y-8">
      <section className="relative overflow-hidden rounded-lg border bg-card/80 p-6 shadow-sm backdrop-blur-xl sm:p-8">
        <div className="absolute right-0 top-0 h-72 w-72 rounded-full bg-indigo-500/15 blur-3xl" />
        <div className="absolute bottom-0 left-1/2 h-56 w-56 rounded-full bg-cyan-500/10 blur-3xl" />
        <div className="relative grid gap-8 lg:grid-cols-[1.25fr_0.75fr] lg:items-center">
          <div className="space-y-4">
            <Badge className="border-indigo-200 bg-indigo-50 text-indigo-700 dark:border-indigo-400/30 dark:bg-indigo-400/10 dark:text-indigo-200">AI Research Notes Workspace</Badge>
            <h2 className="max-w-4xl text-4xl font-semibold tracking-normal sm:text-5xl">
              研究生 AI 学习笔记工作台：
              <span className="gradient-text">知识图谱 + 大语言模型推理</span>
            </h2>
            <p className="max-w-3xl text-base leading-7 text-muted-foreground">
              A structured learning workspace for NLP, LLM, RAG and Knowledge Graph reasoning. 当前默认内置 SLP3 重点阅读路线，也支持继续添加论文、课程、项目复盘和导师汇报。
            </p>
            <div className="flex flex-wrap items-center gap-3 text-sm">
              <span className="rounded-full border bg-background/70 px-4 py-2">默认资料：{defaultSource?.title}</span>
              <ArrowRight className="h-4 w-4 text-muted-foreground" />
              <span className="rounded-full border bg-background/70 px-4 py-2">下一阶段：添加 GraphRAG 论文路线</span>
            </div>
          </div>
          <Card className="border-primary/20 bg-background/65">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BrainCircuit className="h-5 w-5 text-primary" />
                Research Focus
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm leading-6 text-muted-foreground">
              <p>Question → Entity Recognition → Subgraph Retrieval → Evidence Path → LLM Reasoning</p>
              <div className="grid grid-cols-2 gap-2">
                {["KG-RAG", "GraphRAG", "NER", "Entity Linking"].map((item) => (
                  <span key={item} className="rounded-md border bg-card px-3 py-2 font-medium text-foreground">
                    {item}
                  </span>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      <ProgressOverview percent={report.progress_percent} completed={completed} highPriority={highPriority} kgRelated={kgRelated} nextTask="Retrieval-based Models / GraphRAG papers" currentStage={`${sources.length} 个学习资料 · ${defaultSource?.status ?? "进行中"}`} />

      <section className="space-y-3">
        <h3 className="text-xl font-semibold">研究主线</h3>
        <ResearchThread />
      </section>

      <section className="space-y-3">
        <h3 className="text-xl font-semibold">与研究方向相关度最高的章节</h3>
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {topRelevant.map((chapter) => (
            <ChapterCard key={chapter.id} chapter={chapter} />
          ))}
        </div>
      </section>
    </div>
  );
}
