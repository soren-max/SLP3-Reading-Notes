import { Badge } from "@/components/ui/badge";
import type { Chapter } from "@/lib/api";
import { cn } from "@/lib/utils";

const classes: Record<Chapter["priority"], string> = {
  高: "border-rose-200 bg-rose-50 text-rose-700 dark:border-rose-400/30 dark:bg-rose-400/10 dark:text-rose-200",
  中: "border-indigo-200 bg-indigo-50 text-indigo-700 dark:border-indigo-400/30 dark:bg-indigo-400/10 dark:text-indigo-200",
  低: "border-slate-200 bg-slate-50 text-slate-700 dark:border-slate-400/25 dark:bg-slate-400/10 dark:text-slate-200",
};

export function PriorityBadge({ priority, className }: { priority: Chapter["priority"]; className?: string }) {
  return <Badge className={cn(classes[priority], className)}>优先级 {priority}</Badge>;
}
