import { api } from "@/lib/api";
import { InternTimeline } from "@/components/intern-timeline";

export default async function InternsPage() {
  const records = await api.internRecords();

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm text-muted-foreground">Internship</p>
        <h2 className="mt-2 text-3xl font-semibold tracking-normal">实习记录</h2>
        <p className="mt-3 max-w-3xl text-muted-foreground">
          中汇亿达全栈开发实习记录 · 中科曙光旗下 · 内部运维管理平台全栈开发
        </p>
      </div>
      <InternTimeline records={records} />
    </div>
  );
}