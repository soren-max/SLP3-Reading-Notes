import { ReportCard } from "@/components/report-card";
import { api } from "@/lib/api";

export default async function ReportPage() {
  const report = await api.report();
  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm text-muted-foreground">Report</p>
        <h2 className="mt-2 text-3xl font-semibold tracking-normal">导师汇报材料</h2>
      </div>
      <ReportCard report={report} />
    </div>
  );
}
