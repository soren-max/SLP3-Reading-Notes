import Link from "next/link";
import { ArrowUpRight } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { Chapter } from "@/lib/api";
import { cn } from "@/lib/utils";

const priorityClass = {
  高: "border-teal-200 bg-teal-50 text-teal-800",
  中: "border-sky-200 bg-sky-50 text-sky-800",
  低: "border-slate-200 bg-slate-50 text-slate-700",
};

export function ChapterCard({ chapter }: { chapter: Chapter }) {
  return (
    <Link href={`/chapters/${chapter.id}`} className="block h-full no-underline">
      <Card className="h-full transition-colors hover:border-primary/50">
        <CardHeader>
          <div className="flex items-start justify-between gap-3">
            <div>
              <CardDescription>Chapter {chapter.number}</CardDescription>
              <CardTitle className="mt-2 leading-snug">{chapter.title}</CardTitle>
            </div>
            <ArrowUpRight className="mt-1 h-4 w-4 text-muted-foreground" />
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-wrap gap-2">
            <Badge className={cn(priorityClass[chapter.priority])}>优先级 {chapter.priority}</Badge>
            <Badge>{chapter.status}</Badge>
            <Badge>{chapter.mastery}</Badge>
          </div>
          <p className="line-clamp-3 text-sm leading-6 text-muted-foreground">{chapter.research_relation}</p>
          <div className="flex flex-wrap gap-2">
            {chapter.tags.map((tag) => (
              <span key={tag} className="rounded-md bg-secondary px-2 py-1 text-xs text-secondary-foreground">
                {tag}
              </span>
            ))}
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
