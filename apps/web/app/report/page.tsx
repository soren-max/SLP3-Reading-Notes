import { ReportCard } from "@/components/report-card";
import { api } from "@/lib/api";

export default async function ReportPage() {
  const sources = await api.sources();
  const report = await api.report(sources[0]?.id);
  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm text-muted-foreground">Report</p>
        <h2 className="mt-2 text-3xl font-semibold tracking-normal">导师汇报材料</h2>
      </div>
      <ReportCard initialReport={report} sources={sources} />
    </div>
  );
}
