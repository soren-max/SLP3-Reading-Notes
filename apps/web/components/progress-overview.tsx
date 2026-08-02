import { BookMarked, BrainCircuit, CheckCircle2, Route, Sparkles } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

export function ProgressOverview({
  percent,
  completed,
  highPriority,
  kgRelated,
  nextTask,
  currentStage = "AI Research Workspace",
}: {
  percent: number;
  completed: number;
  highPriority: number;
  kgRelated: number;
  nextTask: string;
  currentStage?: string;
}) {
  const stats = [
    { label: "已完成章节", value: completed, icon: CheckCircle2, tone: "text-emerald-500" },
    { label: "高优先级章节", value: highPriority, icon: Sparkles, tone: "text-rose-500" },
    { label: "KG 相关章节", value: kgRelated, icon: BrainCircuit, tone: "text-primary" },
    { label: "下一步阅读任务", value: nextTask, icon: BookMarked, tone: "text-amber-700" },
  ];

  return (
    <section className="grid gap-4 lg:grid-cols-[360px_1fr]">
      <Card className="technical-panel overflow-hidden border-0 text-[#f4f1ea]">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Route className="h-5 w-5" />
            Reading Progress
          </CardTitle>
        </CardHeader>
        <CardContent className="flex items-center gap-6">
          <div
            className="grid h-32 w-32 place-items-center rounded-full"
            style={{ background: `conic-gradient(rgba(255,255,255,0.96) ${percent * 3.6}deg, rgba(255,255,255,0.18) 0deg)` }}
            aria-label={`整体进度 ${percent}%`}
          >
            <div className="grid h-24 w-24 place-items-center rounded-full bg-white/10 text-3xl font-semibold">{percent}%</div>
          </div>
          <div className="space-y-3">
            <p className="text-sm text-white/75">当前阶段</p>
            <p className="text-xl font-semibold">{currentStage}</p>
            <p className="text-sm leading-6 text-white/75">下一阶段聚焦 {nextTask}，并连接 RAG、IE、实体链接与知识图谱推理。</p>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((item) => {
          const Icon = item.icon;
          return (
            <Card key={item.label} className="hover:border-primary/40">
              <CardHeader className="pb-3">
                <Icon className={`h-5 w-5 ${item.tone}`} />
                <CardTitle className="text-sm text-muted-foreground">{item.label}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-semibold">{item.value}</div>
                {typeof item.value === "number" && <Progress value={Math.min(100, item.value * 8)} />}
              </CardContent>
            </Card>
          );
        })}
      </div>
    </section>
  );
}
