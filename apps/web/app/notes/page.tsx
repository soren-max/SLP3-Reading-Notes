import { NoteEditor } from "@/components/note-editor";
import { api } from "@/lib/api";

type Props = { searchParams: Promise<{ chapterId?: string }> };

export default async function NotesPage({ searchParams }: Props) {
  const params = await searchParams;
  const [chapters, notes] = await Promise.all([api.chapters(), api.notes()]);
  const initialChapterId = params.chapterId ? Number(params.chapterId) : undefined;

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm text-muted-foreground">Notes</p>
        <h2 className="mt-2 text-3xl font-semibold tracking-normal">阅读笔记编辑器</h2>
        <p className="mt-3 max-w-3xl text-muted-foreground">左侧选择章节和笔记，中间编辑 Markdown，右侧实时预览。支持保存、更新、删除、标签筛选和关键词搜索。</p>
      </div>
      <NoteEditor chapters={chapters} initialNotes={notes} initialChapterId={Number.isNaN(initialChapterId) ? undefined : initialChapterId} />
    </div>
  );
}
