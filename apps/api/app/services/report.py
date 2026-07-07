from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chapter import Chapter


def build_report(db: Session) -> dict:
    chapters = list(db.scalars(select(Chapter)).all())
    completed = [c for c in chapters if c.status == "已完成"]
    progress = round(len(completed) / len(chapters) * 100) if chapters else 0
    completed_names = [f"{c.number} {c.title}" for c in sorted(completed, key=lambda c: c.number)]
    return {
        "progress_percent": progress,
        "current_stage": "Large Language Models 已基本完成",
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
        "wechat_text": "老师您好，我目前《Speech and Language Processing》第三版第一部分 Large Language Models 已基本看完，主要梳理了 tokenization、embedding、neural networks、LLM、Transformer 和 post-training/alignment 等内容。后续准备继续看 Retrieval-based Models、信息抽取、实体识别、关系抽取和实体链接部分，并结合知识图谱和大模型推理方向整理重点。",
    }
