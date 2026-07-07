import Link from "next/link";
import { ArrowUpRight, BookOpenCheck } from "lucide-react";

import { PriorityBadge } from "@/components/priority-badge";
import { TagChip } from "@/components/tag-chip";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { Chapter } from "@/lib/api";

export function ChapterCard({ chapter }: { chapter: Chapter }) {
  return (
    <Link href={`/chapters/${chapter.id}`} className="block h-full no-underline">
      <Card className="group h-full overflow-hidden hover:-translate-y-1 hover:border-primary/45 hover:shadow-xl hover:shadow-indigo-500/10">
        <div className="h-1 bg-gradient-to-r from-indigo-500 via-violet-500 to-cyan-500 opacity-80" />
        <CardHeader>
          <div className="flex items-start justify-between gap-3">
            <div>
              <CardDescription className="flex items-center gap-2">
                <BookOpenCheck className="h-4 w-4" />
                Chapter {chapter.number}
              </CardDescription>
              <CardTitle className="mt-2 leading-snug group-hover:text-primary">{chapter.title}</CardTitle>
            </div>
            <ArrowUpRight className="mt-1 h-4 w-4 text-muted-foreground transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5 group-hover:text-primary" />
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-wrap gap-2">
            <PriorityBadge priority={chapter.priority} />
            <Badge>{chapter.status}</Badge>
            <Badge>{chapter.mastery}</Badge>
            <Badge>{chapter.relevance_score}%</Badge>
          </div>
          <p className="line-clamp-3 text-sm leading-6 text-muted-foreground">{chapter.research_relation}</p>
          <div className="flex flex-wrap gap-2">
            {chapter.tags.map((tag) => (
              <TagChip key={tag} label={tag} />
            ))}
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
