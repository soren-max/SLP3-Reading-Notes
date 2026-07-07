"use client";

import { useEffect, useState } from "react";
import { Clipboard, FileText, Lightbulb, Link2, ListChecks } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import type { Report } from "@/lib/api";

export function ReportCard({ report }: { report: Report }) {
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!copied) return;
    const timer = window.setTimeout(() => setCopied(false), 2400);
    return () => window.clearTimeout(timer);
  }, [copied]);

  async function copy() {
    await navigator.clipboard.writeText(report.wechat_text);
    setCopied(true);
  }

  return (
    <div className="space-y-4">
      {copied && (
        <div className="fixed right-4 top-24 z-50 rounded-lg border bg-card px-4 py-3 text-sm font-medium shadow-lg" role="status" aria-live="polite">
          微信汇报文本已复制
        </div>
      )}
      <div className="grid gap-4 lg:grid-cols-[0.9fr_1.1fr]">
        <Card className="border-primary/20 bg-gradient-to-br from-indigo-600 via-violet-600 to-cyan-600 text-white">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              阶段性学习汇报生成器
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="text-5xl font-semibold">{report.progress_percent}%</div>
            <Progress value={report.progress_percent} />
            <p className="text-sm text-white/80">{report.current_stage}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Link2 className="h-5 w-5 text-cyan-500" />
              研究方向联系
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="leading-7 text-muted-foreground">{report.research_relation}</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <SummaryList title="已完成章节" icon={<ListChecks className="h-5 w-5 text-emerald-500" />} items={report.completed_chapters} />
        <SummaryList title="本阶段收获" icon={<Lightbulb className="h-5 w-5 text-indigo-500" />} items={report.current_gains} />
        <SummaryList title="后续计划" icon={<ListChecks className="h-5 w-5 text-cyan-500" />} items={report.next_plan} />
      </div>

      <Card className="overflow-hidden">
        <CardHeader className="border-b bg-gradient-to-r from-indigo-500/10 to-cyan-500/10">
          <CardTitle className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            可复制微信汇报文本
            <Button onClick={copy}>
              <Clipboard className="h-4 w-4" />
              一键复制
            </Button>
          </CardTitle>
        </CardHeader>
        <CardContent className="p-5">
          <textarea className="min-h-36 w-full rounded-md border bg-background/80 p-3 text-sm leading-7 outline-none focus-visible:ring-2 focus-visible:ring-ring" defaultValue={report.wechat_text} aria-label="微信汇报文本" />
        </CardContent>
      </Card>
    </div>
  );
}

function SummaryList({ title, icon, items }: { title: string; icon: React.ReactNode; items: string[] }) {
  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          {icon}
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2 text-sm leading-6 text-muted-foreground">
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}
