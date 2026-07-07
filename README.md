# AI Research Notes Workspace

A structured learning workspace for NLP, LLM, RAG and Knowledge Graph reasoning.

这是一个面向研究生阶段 AI 学习、论文阅读、课程整理、项目复盘和导师汇报的本地全栈笔记工作台。当前默认内置《Speech and Language Processing, Third Edition draft》的重点阅读路线，但数据模型已经抽象为通用 `Source`，后续可以继续添加书籍、论文、课程、项目复盘、导师汇报和其他资料。

研究方向聚焦：

- KG-RAG / GraphRAG
- Knowledge Graph Reasoning
- Information Extraction
- Named Entity Recognition
- Relation Extraction
- Entity Linking
- Multi-hop Reasoning with LLMs

## 为什么做这个项目

研究生阶段的 AI 学习资料通常分散在书、论文、课程、项目实验和每周汇报中。只用 Markdown 记录容易出现资料来源混乱、研究主线断裂、导师汇报重复整理等问题。本项目将资料来源、章节/论文模块、笔记、学习路线和阶段汇报统一到一个本地工作台中。

核心目标：

- 以 `Source` 为核心组织学习资料，而不是写死某一本书。
- 默认内置 SLP3 的 KG-LLM 重点阅读路线。
- 支持继续添加 GraphRAG 论文、KG-RAG 课程、AI Agent 项目复盘和导师汇报。
- 用 Dashboard、Sources、Roadmap、Notes、Report 串起学习、复盘和展示。
- 本地优先，不依赖真实 LLM API，适合作为 GitHub 展示项目和科研学习系统。

## Source 数据模型

每个学习资料都是一个 Source：

- `title`: 资料标题
- `type`: `book` / `paper` / `course` / `project` / `report` / `misc`
- `author_or_origin`: 作者或来源
- `research_direction`: 研究方向，例如 LLM、RAG、KG、GraphRAG、IE、Entity Linking
- `description`: 简介
- `status`: 未开始 / 进行中 / 已完成
- `priority`: 高 / 中 / 低

每条 Note 都关联 `source_id`。书籍和课程可以继续关联章节；论文、项目和汇报可以不关联章节，直接作为资料笔记管理。

## 技术栈

- Frontend: Next.js 15, TypeScript, TailwindCSS, shadcn/ui style components, lucide-react
- Backend: FastAPI, SQLAlchemy, SQLite, Pydantic
- Tooling: npm workspaces, ESLint, pytest
- Structure: `apps/web` and `apps/api`

## 功能截图占位

运行项目后可将截图放到以下路径：

```text
docs/screenshots/dashboard.png
docs/screenshots/sources.png
docs/screenshots/source-detail.png
docs/screenshots/roadmap.png
docs/screenshots/notes.png
docs/screenshots/report.png
```

README 展示示例：

```md
![Dashboard](docs/screenshots/dashboard.png)
![Sources](docs/screenshots/sources.png)
![Notes Workspace](docs/screenshots/notes.png)
![Report Generator](docs/screenshots/report.png)
```

## 核心页面

### Dashboard

AI Research Notes Workspace 首页，展示默认资料、学习进度、统计卡片、高相关章节和研究主线：

```text
LLM Foundation -> RAG -> Information Extraction -> Entity Linking -> KG Reasoning
```

### Sources

学习资料库，用于管理不同类型的资料：

- book：书籍
- paper：论文
- course：课程
- project：项目复盘
- report：导师汇报
- misc：其他资料

支持搜索、来源类型筛选、研究方向筛选，以及手动新增资料。

### Source Detail

资料详情页根据 source 类型展示不同结构：

- `book` / `course`: 展示章节目录、优先级、状态、标签和研究关联。
- `paper`: 展示论文阅读模块，包括背景、问题、方法、实验、创新点、不足、研究联系和可复现思路。
- `project` / `report` / `misc`: 作为资料模块进入 Notes 页面沉淀笔记。

`/chapters` 保留为默认 SLP3 Source 的快捷入口。

### Roadmap

保留 SLP3 主线，并增加自定义学习路线：

- LLM 基础路线
- KG-RAG 路线
- GraphRAG 论文路线
- 信息抽取路线
- AI Agent 工程路线

### Notes

三栏 Markdown 研究笔记工作区：

- 左侧固定资料/笔记导航
- 中间 Markdown 编辑器
- 右侧实时预览
- 新增、保存、删除笔记
- 复制笔记、导出 Markdown
- 生成导师汇报草稿
- 按来源类型、研究方向、标签、阅读状态和优先级筛选

### Report

阶段性学习汇报生成器：

- 按 source 生成汇报
- 支持 SLP3 阶段阅读汇报
- 支持论文阅读汇报
- 支持项目复盘汇报
- 支持每周学习进展汇报
- 一键复制微信汇报文本

## 本地启动

### 1. 准备环境变量

```bash
cp .env.example .env
```

### 2. 安装前端依赖

```bash
npm install
```

### 3. 安装后端依赖并初始化数据库

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed
cd ../..
```

### 4. 启动开发服务

保持后端虚拟环境已激活，然后运行：

```bash
npm run dev
```

Open:

- Web: http://localhost:3000
- API docs: http://localhost:8000/docs

也可以分别启动：

```bash
npm run dev:web
cd apps/api && source .venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API

- `GET /api/sources`
- `GET /api/sources/{id}`
- `POST /api/sources`
- `PATCH /api/sources/{id}`
- `DELETE /api/sources/{id}`
- `GET /api/chapters`
- `GET /api/chapters?source_id={id}`
- `GET /api/chapters/{id}`
- `PATCH /api/chapters/{id}/progress`
- `GET /api/notes`
- `POST /api/notes`
- `PATCH /api/notes/{id}`
- `DELETE /api/notes/{id}`
- `GET /api/roadmap`
- `GET /api/report`
- `GET /api/report?source_id={id}`

## 质量检查

```bash
npm --workspace apps/web run lint
npm --workspace apps/web run build
cd apps/api && source .venv/bin/activate && python -m pytest
```

## 目录结构

```text
apps/
  api/
    app/
      database.py
      main.py
      seed.py
      models/
        source.py
        chapter.py
        note.py
      routers/
      schemas/
      services/
    tests/
  web/
    app/
      sources/
      chapters/
      notes/
      report/
      roadmap/
    components/
      SourceCard
      SourceManager
      ChapterCard
      NoteEditor
      ProgressOverview
      ReportCard
      RoadmapTimeline
    lib/
```

## 默认 Seed 数据

默认导入一个 `book` 类型 Source：

```text
Speech and Language Processing, Third Edition draft
```

高优先级章节重点覆盖：

- Embeddings
- Large Language Models
- Transformers
- Post-training
- Retrieval-based Models
- Sequence Labeling for POS and Named Entities
- Information Extraction
- Semantic Role Labeling
- Coreference Resolution and Entity Linking

每章包含优先级、阅读状态、推荐掌握程度、研究方向关联、标签、导师可能提问和初始 Markdown 笔记模板。

## 后续计划

- 增加 Source 编辑和删除的完整 UI。
- 增加论文详情的结构化字段编辑。
- 增加学习进度图表和阅读时间记录。
- 支持笔记全文导入/导出。
- 将 SLP3 章节与 KG-RAG / GraphRAG 论文路线互相关联。
- 接入本地或远程 LLM，生成章节总结、论文批注、导师问题和实验 idea。
- 增加知识图谱可视化，把资料、概念、方法和研究任务连成图。

## Notes

The project is local-first and does not call any LLM API by default. It is designed as a research-oriented AI learning notes workspace and GitHub showcase project.
