import { NoteEditor } from "@/components/note-editor";
import { api } from "@/lib/api";

type Props = { searchParams: Promise<{ chapterId?: string; sourceId?: string }> };

export default async function NotesPage({ searchParams }: Props) {
  const params = await searchParams;
  const [sources, chapters, notes] = await Promise.all([api.sources(), api.chapters(), api.notes()]);
  const initialChapterId = params.chapterId ? Number(params.chapterId) : undefined;
  const initialSourceId = params.sourceId ? Number(params.sourceId) : undefined;

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm text-muted-foreground">Notes</p>
        <h2 className="mt-2 text-3xl font-semibold tracking-normal">AI 研究笔记编辑器</h2>
        <p className="mt-3 max-w-3xl text-muted-foreground">按资料来源组织书籍、论文、课程和项目笔记。支持来源类型、研究方向、标签、状态和优先级筛选。</p>
      </div>
      <NoteEditor sources={sources} chapters={chapters} initialNotes={notes} initialChapterId={Number.isNaN(initialChapterId) ? undefined : initialChapterId} initialSourceId={Number.isNaN(initialSourceId) ? undefined : initialSourceId} />
    </div>
  );
}
