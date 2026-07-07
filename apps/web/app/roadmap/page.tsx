import { CustomRoadmaps, RoadmapTimeline } from "@/components/roadmap-timeline";
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
      <RoadmapTimeline phases={roadmap.slp3} />
      <section className="space-y-3">
        <h3 className="text-xl font-semibold">自定义学习路线</h3>
        <p className="max-w-3xl text-sm leading-6 text-muted-foreground">除默认 SLP3 主线外，工作台也预留了论文、课程和工程项目的路线规划入口。</p>
        <CustomRoadmaps routes={roadmap.custom} />
      </section>
    </div>
  );
}
