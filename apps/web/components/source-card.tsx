import Link from "next/link";
import { ArrowUpRight, BookOpen, FileText, FlaskConical, GraduationCap, Layers3, Library } from "lucide-react";

import { PriorityBadge } from "@/components/priority-badge";
import { TagChip } from "@/components/tag-chip";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { Source, SourceType } from "@/lib/api";

const typeLabel: Record<SourceType, string> = {
  book: "书籍",
  paper: "论文",
  course: "课程",
  project: "项目复盘",
  report: "导师汇报",
  misc: "其他资料",
};

const icons: Record<SourceType, typeof BookOpen> = {
  book: BookOpen,
  paper: FileText,
  course: GraduationCap,
  project: FlaskConical,
  report: Layers3,
  misc: Library,
};

export function SourceCard({ source }: { source: Source }) {
  const Icon = icons[source.type];
  const directions = source.research_direction.split(",").map((item) => item.trim()).filter(Boolean).slice(0, 5);
  return (
    <Link href={`/sources/${source.id}`} className="block h-full no-underline">
      <Card className="group h-full hover:-translate-y-1 hover:border-primary/45 hover:shadow-xl hover:shadow-indigo-500/10">
        <CardHeader>
          <div className="flex items-start justify-between gap-3">
            <div className="flex gap-3">
              <div className="grid h-11 w-11 shrink-0 place-items-center rounded-lg bg-gradient-to-br from-indigo-600 to-cyan-500 text-white">
                <Icon className="h-5 w-5" />
              </div>
              <div>
                <div className="flex flex-wrap gap-2">
                  <Badge>{typeLabel[source.type]}</Badge>
                  <Badge>{source.status}</Badge>
                  <PriorityBadge priority={source.priority} />
                </div>
                <CardTitle className="mt-3 leading-snug group-hover:text-primary">{source.title}</CardTitle>
              </div>
            </div>
            <ArrowUpRight className="h-4 w-4 text-muted-foreground transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5 group-hover:text-primary" />
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-muted-foreground">{source.author_or_origin}</p>
          <p className="line-clamp-3 text-sm leading-6 text-muted-foreground">{source.description}</p>
          <div className="flex flex-wrap gap-2">
            {directions.map((item) => (
              <TagChip key={item} label={item} />
            ))}
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
