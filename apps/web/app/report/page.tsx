import { Copy } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { api } from "@/lib/api";

export default async function ReportPage() {
  const report = await api.report();
  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm text-muted-foreground">Report</p>
        <h2 className="mt-2 text-3xl font-semibold tracking-normal">导师汇报材料</h2>
      </div>
      <div className="grid gap-4 lg:grid-cols-[0.9fr_1.1fr]">
        <Card>
          <CardHeader>
            <CardTitle>当前阅读进度</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="text-4xl font-semibold">{report.progress_percent}%</div>
            <Progress value={report.progress_percent} />
            <Badge>{report.current_stage}</Badge>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>和研究方向的关系</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="leading-7 text-muted-foreground">{report.research_relation}</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>已完成章节</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm text-muted-foreground">
              {report.completed_chapters.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>本阶段收获</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm leading-6 text-muted-foreground">
              {report.current_gains.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>后续计划</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm leading-6 text-muted-foreground">
              {report.next_plan.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Copy className="h-5 w-5" />
            可复制微信汇报文本
          </CardTitle>
        </CardHeader>
        <CardContent>
          <textarea className="min-h-32 w-full rounded-md border bg-background p-3 text-sm leading-7 outline-none focus-visible:ring-2 focus-visible:ring-ring" defaultValue={report.wechat_text} aria-label="微信汇报文本" />
        </CardContent>
      </Card>
    </div>
  );
}
