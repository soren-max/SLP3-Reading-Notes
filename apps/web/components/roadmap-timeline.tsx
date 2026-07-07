import { ArrowDown, FileCheck2, Layers3 } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TagChip } from "@/components/tag-chip";
import type { CustomRoadmap, RoadmapPhase } from "@/lib/api";

const outputs = [
  "LLM 基础概念图谱",
  "RAG / KG-RAG 检索笔记",
  "IE 到 KG 构建任务表",
  "多跳推理实验草案",
];

const chapterHints = [
  ["2", "5", "6", "7", "8", "10"],
  ["11", "Dense Retrieval", "RAG", "GraphRAG"],
  ["17", "20", "21", "23"],
  ["Question", "Subgraph", "Evidence", "Answer"],
];

export function RoadmapTimeline({ phases }: { phases: RoadmapPhase[] }) {
  return (
    <div className="relative space-y-4">
      <div className="absolute left-5 top-8 hidden h-[calc(100%-4rem)] w-px bg-gradient-to-b from-indigo-500 via-cyan-500 to-transparent md:block" />
      {phases.map((phase, index) => (
        <div key={phase.phase} className="relative md:pl-14">
          <div className="absolute left-0 top-6 hidden h-10 w-10 place-items-center rounded-lg border bg-card shadow-sm md:grid">
            <Layers3 className="h-5 w-5 text-primary" />
          </div>
          <Card className="overflow-hidden hover:border-primary/40 hover:shadow-lg hover:shadow-indigo-500/10">
            <CardHeader className="border-b bg-gradient-to-r from-indigo-500/10 to-cyan-500/10">
              <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Phase {index + 1}</p>
                  <CardTitle className="mt-1">{phase.phase}</CardTitle>
                </div>
                <div className="flex items-center gap-2 rounded-full border bg-background/70 px-3 py-2 text-sm font-medium">
                  <FileCheck2 className="h-4 w-4 text-cyan-500" />
                  {outputs[index]}
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-5 p-5">
              <p className="leading-7 text-muted-foreground">{phase.goal}</p>
              <div className="flex flex-wrap gap-2">
                {chapterHints[index].map((item) => (
                  <TagChip key={item} label={item} />
                ))}
              </div>
              <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
                {phase.steps.map((step, stepIndex) => (
                  <div key={step} className="rounded-lg border bg-background/70 p-3">
                    <p className="text-xs text-muted-foreground">Step {stepIndex + 1}</p>
                    <p className="mt-1 text-sm font-semibold">{step}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
          {index < phases.length - 1 && <ArrowDown className="mx-auto my-3 h-5 w-5 text-muted-foreground md:hidden" />}
        </div>
      ))}
    </div>
  );
}

export function CustomRoadmaps({ routes }: { routes: CustomRoadmap[] }) {
  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      {routes.map((route) => (
        <Card key={route.name} className="hover:-translate-y-1 hover:border-primary/40 hover:shadow-lg hover:shadow-indigo-500/10">
          <CardHeader>
            <CardTitle>{route.name}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {route.steps.map((step, index) => (
              <div key={step} className="flex items-center gap-3 rounded-lg border bg-background/70 p-3">
                <span className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-secondary text-xs font-semibold">{index + 1}</span>
                <span className="text-sm font-medium">{step}</span>
              </div>
            ))}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
