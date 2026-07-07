import { RoadmapTimeline } from "@/components/roadmap-timeline";
import { api } from "@/lib/api";

export default async function RoadmapPage() {
  const roadmap = await api.roadmap();
  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm text-muted-foreground">Roadmap</p>
        <h2 className="mt-2 text-3xl font-semibold tracking-normal">KG-RAG 与大模型推理学习路线</h2>
        <p className="mt-3 max-w-3xl text-muted-foreground">从 LLM 基础进入检索增强，再连接信息抽取和知识图谱推理，每个阶段都有明确产出物。</p>
      </div>
      <RoadmapTimeline phases={roadmap} />
    </div>
  );
}
