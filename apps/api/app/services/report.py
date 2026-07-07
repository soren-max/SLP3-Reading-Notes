from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chapter import Chapter
from app.models.source import Source


def build_report(db: Session, source_id: int | None = None) -> dict:
    source = db.get(Source, source_id) if source_id else db.scalars(select(Source).order_by(Source.id.asc())).first()
    stmt = select(Chapter)
    if source:
        stmt = stmt.where(Chapter.source_id == source.id)
    chapters = list(db.scalars(stmt).all())
    completed = [c for c in chapters if c.status == "已完成"]
    progress = round(len(completed) / len(chapters) * 100) if chapters else 0
    completed_names = [f"{c.number} {c.title}" for c in sorted(completed, key=lambda c: c.number)]
    source_title = source.title if source else "AI Research Notes"
    if source and source.type == "paper":
        wechat = f"老师您好，我本周重点阅读了论文《{source.title}》，主要围绕背景问题、核心方法、实验设计、创新点和不足进行整理，并重点思考它与 {source.research_direction} 方向的关系。后续准备补充可复现思路，并把方法拆解到自己的研究任务中。"
    elif source and source.type == "project":
        wechat = f"老师您好，我本周整理了项目复盘《{source.title}》，主要记录了目标、方法、实验结果、工程问题和后续改进计划，并结合 {source.research_direction} 方向梳理可沉淀的经验。"
    else:
        wechat = f"老师您好，我目前《{source_title}》阶段阅读已推进到 {progress}%，主要梳理了 LLM、RAG、信息抽取、实体链接和知识图谱推理相关内容。后续准备继续补充重点章节笔记，并结合知识图谱和大模型推理方向整理可汇报的研究问题。"
    return {
        "progress_percent": progress,
        "current_stage": f"{source_title} 阶段学习汇报",
        "completed_chapters": completed_names,
        "current_gains": [
            "梳理了 tokenization、embedding、neural networks、LLM、Transformer 与 post-training/alignment 的主线。",
            "明确了检索增强和知识图谱增强推理需要连接检索、结构化抽取与证据链构造。",
            "形成了后续围绕 KG-RAG、GraphRAG 和实体链接补齐实验能力的阅读计划。",
        ],
        "next_plan": [
            "精读 Retrieval-based Models，整理 BM25、dense retrieval 与 RAG 的衔接。",
            "继续阅读 NER、Information Extraction、Semantic Role Labeling 和 Entity Linking。",
            "将章节知识映射到 KG 构建、子图检索、多跳推理和导师汇报材料中。",
        ],
        "research_relation": "当前阅读路径从 LLM 基础过渡到检索增强和信息抽取，最终服务于知识图谱驱动的大模型推理：实体识别负责问题和文本锚定，关系/事件抽取负责图谱构建，实体链接解决知识库对齐，GraphRAG/KG-RAG 负责证据子图检索与路径组织。",
        "wechat_text": wechat,
    }
