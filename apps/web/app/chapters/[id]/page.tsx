import { notFound } from "next/navigation";

import { ChapterWorkstation } from "@/components/chapter-workstation";
import { api } from "@/lib/api";

type Props = { params: Promise<{ id: string }> };

export default async function ChapterDetailPage({ params }: Props) {
  const { id } = await params;
  const chapterId = Number(id);
  if (Number.isNaN(chapterId)) notFound();

  let chapter;
  try {
    chapter = await api.chapter(chapterId);
  } catch {
    notFound();
  }

  const notes = await api.notes(new URLSearchParams({ chapter_id: String(chapterId) }));

  return <ChapterWorkstation chapter={chapter} notes={notes} />;
}
