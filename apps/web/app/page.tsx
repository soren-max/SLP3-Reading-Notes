import { BrainCircuit, CheckCircle2, Target, TrendingUp } from "lucide-react";

import { ChapterCard } from "@/components/chapter-card";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { api } from "@/lib/api";

export default async function DashboardPage() {
  const [chapters, report] = await Promise.all([api.chapters(), api.report()]);
  const topRelevant = [...chapters].sort((a, b) => b.relevance_score - a.relevance_score).slice(0, 4);
  const route = ["Words and Tokens", "Embeddings", "Neural Networks", "LLM", "Transformers", "Post-training", "Retrieval", "IE", "Entity Linking"];

  return (
    <div className="space-y-6">
      <section className="rounded-lg border bg-card p-6 shadow-sm">
        <div className="grid gap-6 lg:grid-cols-[1.4fr_0.8fr] lg:items-center">
          <div className="space-y-4">
            <Badge className="border-teal-200 bg-teal-50 text-teal-800">Speech and Language Processing, Third Edition draft</Badge>
            <h2 className="max-w-3xl text-3xl font-semibold tracking-normal sm:text-4xl">重点阅读笔记系统：知识图谱 + 大语言模型推理</h2>
            <p className="max-w-3xl text-base leading-7 text-muted-foreground">
              用交互式方式管理章节重点、导师汇报、研究路线与后续资料，重点围绕 KG-RAG、GraphRAG、信息抽取、实体链接和多跳推理。
            </p>
          </div>
          <Card>
            <CardHeader>
              <CardDescription>整体学习进度</CardDescription>
              <CardTitle className="text-4xl">{report.progress_percent}%</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Progress value={report.progress_percent} />
              <p className="text-sm text-muted-foreground">{report.current_stage}</p>
            </CardContent>
          </Card>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader>
            <CheckCircle2 className="h-5 w-5 text-teal-700" />
            <CardTitle>当前阶段</CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">Large Language Models 已基本完成，正在进入检索增强和信息抽取主线。</CardContent>
        </Card>
        <Card>
          <CardHeader>
            <Target className="h-5 w-5 text-sky-700" />
            <CardTitle>后续重点</CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">Retrieval-based Models、Named Entities、Information Extraction、SRL、Entity Linking。</CardContent>
        </Card>
        <Card>
          <CardHeader>
            <BrainCircuit className="h-5 w-5 text-cyan-700" />
            <CardTitle>研究落点</CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">问题实体识别、子图检索、证据路径构造与 LLM evidence-aware reasoning。</CardContent>
        </Card>
      </section>

      <section className="space-y-3">
        <div className="flex items-center gap-2">
          <TrendingUp className="h-5 w-5 text-primary" />
          <h3 className="text-xl font-semibold">整本书阅读路线</h3>
        </div>
        <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-5">
          {route.map((item, index) => (
            <div key={item} className="rounded-lg border bg-card p-4">
              <p className="text-xs text-muted-foreground">Step {index + 1}</p>
              <p className="mt-2 font-medium">{item}</p>
            </div>
          ))}
        </div>
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
