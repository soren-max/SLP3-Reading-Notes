import { SourceManager } from "@/components/source-manager";
import { api } from "@/lib/api";

export default async function SourcesPage() {
  const sources = await api.sources();
  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm text-muted-foreground">Sources</p>
        <h2 className="mt-2 text-3xl font-semibold tracking-normal">学习资料库</h2>
        <p className="mt-3 max-w-3xl text-muted-foreground">
          管理书籍、论文、课程、项目复盘和导师汇报。当前默认内置 SLP3 重点阅读路线，后续可继续添加论文、课程和项目笔记。
        </p>
      </div>
      <SourceManager initialSources={sources} />
    </div>
  );
}
