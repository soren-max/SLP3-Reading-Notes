# SLP3 KG-LLM Reading Notes

研究生阶段 NLP 读书笔记系统，围绕《Speech and Language Processing, Third Edition draft》重点章节，聚焦知识图谱、大语言模型推理、KG-RAG、GraphRAG、信息抽取、实体识别、关系抽取、实体链接与多跳推理。

## Tech Stack

- Web: Next.js 15, TypeScript, TailwindCSS, shadcn/ui style components, lucide-react
- API: FastAPI, SQLAlchemy, SQLite, Pydantic
- Structure: `apps/web` and `apps/api`

## Quick Start

```bash
cp .env.example .env
npm install
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed
cd ../..
npm run dev
```

Open:

- Web: http://localhost:3000
- API docs: http://localhost:8000/docs

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

## Project Structure

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
  web/
    app/
    components/
    lib/
```

## Notes

The project is local-first and does not call any LLM API. Seed data includes SLP3 chapters, priorities, research relevance, reading depth, tags, roadmap phases, mentor questions, and starter note templates.
