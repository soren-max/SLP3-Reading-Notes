import { ArrowRight } from "lucide-react";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

export default async function RoadmapPage() {
  const roadmap = await api.roadmap();
  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm text-muted-foreground">Roadmap</p>
        <h2 className="mt-2 text-3xl font-semibold tracking-normal">KG-RAG 与大模型推理学习路线</h2>
      </div>
      <div className="grid gap-4">
        {roadmap.map((phase, phaseIndex) => (
          <Card key={phase.phase}>
            <CardHeader>
              <CardDescription>Phase {phaseIndex + 1}</CardDescription>
              <CardTitle>{phase.phase}</CardTitle>
              <p className="text-sm leading-6 text-muted-foreground">{phase.goal}</p>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col gap-2 lg:flex-row lg:items-center lg:flex-wrap">
                {phase.steps.map((step, index) => (
                  <div key={step} className="flex items-center gap-2">
                    <div className="rounded-md border bg-background px-3 py-2 text-sm font-medium">{step}</div>
                    {index < phase.steps.length - 1 && <ArrowRight className="hidden h-4 w-4 text-muted-foreground lg:block" />}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
