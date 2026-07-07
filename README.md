# SLP3 KG-LLM Reading Notes

《Speech and Language Processing, Third Edition draft》重点阅读笔记系统。项目面向研究生阶段 NLP 阅读、导师汇报和后续研究选题，把普通 Markdown 笔记升级成一个可交互的 AI 学习工作台。

研究方向聚焦：

- KG-RAG / GraphRAG
- Knowledge Graph Reasoning
- Information Extraction
- Named Entity Recognition
- Relation Extraction
- Entity Linking
- Multi-hop Reasoning with LLMs

## 为什么做这个项目

SLP3 内容覆盖面很广，直接用 Markdown 仓库记录容易出现三个问题：章节优先级不清晰、研究方向关联分散、导师汇报材料需要重复整理。本项目将章节、笔记、进度、路线图和汇报文本统一到一个本地全栈系统中，方便持续阅读、复盘和展示。

核心目标：

- 将 SLP3 章节按“知识图谱 + 大语言模型推理”方向重新组织。
- 跟踪 Large Language Models、Retrieval-based Models、IE、NER、SRL、Entity Linking 等重点章节。
- 用 Dashboard、Roadmap、Report 辅助阶段性汇报和研究路线规划。
- 保持本地优先，不依赖真实 LLM API，适合作为课程/科研学习项目展示。

## 技术栈

- Frontend: Next.js 15, TypeScript, TailwindCSS, shadcn/ui style components, lucide-react
- Backend: FastAPI, SQLAlchemy, SQLite, Pydantic
- Tooling: npm workspaces, ESLint, pytest
- Structure: `apps/web` and `apps/api`

## 功能截图占位

运行项目后可将截图放到以下路径：

```text
docs/screenshots/dashboard.png
docs/screenshots/chapters.png
docs/screenshots/roadmap.png
docs/screenshots/notes.png
docs/screenshots/report.png
```

README 展示示例：

```md
![Dashboard](docs/screenshots/dashboard.png)
![Chapters](docs/screenshots/chapters.png)
![Notes Workspace](docs/screenshots/notes.png)
![Report Generator](docs/screenshots/report.png)
```

## 核心页面

### Dashboard

AI 学习工作台首页，展示整体学习进度、当前阶段、下一阶段、4 张统计卡片，以及研究主线：

```text
LLM Foundation -> RAG -> Information Extraction -> Entity Linking -> KG Reasoning
```

### Chapters

章节目录与研究优先级管理。支持：

- 展示所有 seed 章节
- 按高 / 中 / 低优先级筛选
- 按未开始 / 阅读中 / 已完成状态筛选
- 按 LLM、RAG、KG、IE、NER、Entity Linking、Reasoning 等标签筛选
- 搜索章节标题、标签和研究方向关联

### Roadmap

阶段路线图，突出从基础模型到知识图谱推理的学习路径：

```text
阶段一：LLM 基础
阶段二：RAG 与检索增强
阶段三：知识图谱构建
阶段四：大模型推理实践
```

### Notes

三栏 Markdown 笔记工作区：

- 左侧固定章节/笔记导航
- 中间 Markdown 编辑器
- 右侧实时预览
- 新增、保存、删除笔记
- 复制笔记、导出 Markdown
- 生成导师汇报草稿
- 保存成功 toast

### Report

阶段性学习汇报生成器：

- 当前阅读进度
- 已完成章节
- 本阶段收获
- 后续计划
- 与 KG-RAG / GraphRAG / Knowledge Graph Reasoning 的关系
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

- `GET /api/chapters`
- `GET /api/chapters/{id}`
- `PATCH /api/chapters/{id}/progress`
- `GET /api/notes`
- `POST /api/notes`
- `PATCH /api/notes/{id}`
- `DELETE /api/notes/{id}`
- `GET /api/roadmap`
- `GET /api/report`

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
      routers/
      schemas/
      services/
    tests/
  web/
    app/
      chapters/
      notes/
      report/
      roadmap/
    components/
      ChapterCard
      NoteEditor
      ProgressOverview
      ReportCard
      RoadmapTimeline
    lib/
```

## Seed 数据

内置章节包括高、中、低三个优先级。高优先级重点覆盖：

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

- 增加章节详情页内联编辑能力。
- 增加学习进度图表和阅读时间记录。
- 支持笔记全文导入/导出。
- 增加论文阅读模块，将 SLP3 章节与 KG-RAG / GraphRAG 论文关联。
- 接入本地或远程 LLM，生成章节总结、导师问题和实验 idea。
- 增加知识图谱可视化，把章节概念、方法和研究任务连成图。

## Notes

The project is local-first and does not call any LLM API by default. It is designed as a research-oriented reading notes system and GitHub showcase project.
