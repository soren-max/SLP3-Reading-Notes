from app.database import Base, SessionLocal, engine, init_db
from app.models.chapter import Chapter
from app.models.note import Note
from app.models.source import Source


def chapter(
    number: int,
    title: str,
    priority: str,
    mastery: str,
    relevance_score: int,
    relation: str,
    tags: list[str],
    status: str = "未开始",
) -> dict:
    concepts = tags[:4] + ["Reading Notes"]
    return {
        "source_id": 1,
        "number": number,
        "title": title,
        "priority": priority,
        "status": status,
        "mastery": mastery,
        "relevance_score": relevance_score,
        "research_relation": relation,
        "positioning": f"第 {number} 章用于支撑 KG-LLM 阅读路线中关于 {', '.join(tags[:3])} 的知识模块。",
        "core_concepts": concepts,
        "outline": "按概念定义、模型假设、训练/推理流程、典型例子、与研究方向的连接五个层次梳理。",
        "formulas_algorithms": "记录关键公式、目标函数、解码或检索算法，并补充变量含义与适用边界。",
        "examples": "为每个核心概念补一个面向 KG-RAG 或 GraphRAG 的文本例子，说明输入、输出和中间表示。",
        "summary": "提炼本章最应掌握的概念、容易混淆的点，以及可迁移到研究实验中的方法。",
        "mentor_questions": [
            "本章方法解决 NLP 流水线中的哪一类问题？",
            "它如何服务 KG-RAG、GraphRAG 或多跳推理？",
            "如果放到研究实验里，输入输出和评价指标是什么？",
        ],
        "research_links": relation,
        "resources": [
            "Speech and Language Processing, Third Edition draft",
            "相关论文与课程笔记后续补充",
        ],
        "tags": tags,
    }


CHAPTERS = [
    chapter(2, "Words and Tokens", "高", "精读", 90, "Tokenization 决定实体边界、检索粒度和 LLM 输入表示，是 NER 与实体链接的前置基础。", ["LLM", "NER", "Entity Linking", "KG"], "已完成"),
    chapter(5, "Embeddings", "高", "精读", 92, "Embedding 是 dense retrieval、实体表示、语义匹配和向量检索的核心基础。", ["LLM", "RAG", "KG", "Reasoning"], "已完成"),
    chapter(7, "Large Language Models", "高", "精读", 96, "LLM 是后续 KG-RAG、GraphRAG 与证据增强推理的生成和推理核心。", ["LLM", "Reasoning", "RAG", "KG"], "已完成"),
    chapter(8, "Transformers", "高", "精读", 94, "Transformer 提供上下文建模、注意力机制和 LLM 推理能力的结构基础。", ["LLM", "Reasoning", "RAG"], "已完成"),
    chapter(9, "Masked Language Models", "高", "理解", 82, "MLM 有助于理解预训练表示、实体上下文表征和下游 IE 任务迁移。", ["LLM", "IE", "NER"], "阅读中"),
    chapter(10, "Post-training", "高", "精读", 91, "Post-training/alignment 影响 LLM 在证据遵循、问答和工具调用中的行为。", ["LLM", "Reasoning", "RAG"], "已完成"),
    chapter(11, "Retrieval-based Models", "高", "精读", 98, "检索模型直接连接 RAG、KG-RAG 和 GraphRAG，是后续研究的关键章节。", ["RAG", "KG", "GraphRAG", "Reasoning"], "阅读中"),
    chapter(17, "Sequence Labeling for POS and Named Entities", "高", "精读", 95, "NER 是知识图谱构建、问题实体识别和实体链接的入口任务。", ["NER", "KG", "IE", "Entity Linking"]),
    chapter(20, "Information Extraction", "高", "精读", 99, "信息抽取覆盖关系、事件和槽填充，是从文本构建知识图谱的核心技术。", ["IE", "KG", "Relation Extraction", "RAG"]),
    chapter(21, "Semantic Role Labeling", "高", "精读", 88, "SRL 提供谓词-论元结构，可辅助事件抽取、证据路径和可解释推理。", ["IE", "Reasoning", "KG"]),
    chapter(23, "Coreference Resolution and Entity Linking", "高", "精读", 97, "指代消解与实体链接负责跨句实体归并和知识库对齐，是 GraphRAG 证据一致性的关键。", ["Entity Linking", "KG", "Reasoning", "GraphRAG"]),
    chapter(3, "N-gram Language Models", "中", "理解", 58, "用于理解语言模型历史和概率建模思想，对现代 LLM 是背景知识。", ["LLM"], "已完成"),
    chapter(4, "Logistic Regression", "中", "理解", 62, "分类基础有助于理解传统 NER/IE 特征模型和评价方式。", ["NER", "IE"]),
    chapter(6, "Neural Networks", "中", "理解", 72, "神经网络基础支撑 embedding、sequence labeling 和 Transformer。", ["LLM", "NER"], "已完成"),
    chapter(18, "Context-Free Grammars", "中", "理解", 52, "句法结构有助于理解 IE 中的结构约束和语义角色分析。", ["IE", "Reasoning"]),
    chapter(19, "Dependency Parsing", "中", "理解", 68, "依存分析可辅助关系抽取、事件抽取和证据路径解释。", ["IE", "KG", "Relation Extraction"]),
    chapter(24, "Discourse Coherence", "中", "理解", 57, "篇章连贯性影响多文档证据组织和长上下文推理。", ["Reasoning", "RAG"]),
    chapter(25, "Conversation and its Structure", "中", "理解", 50, "对导师问答、对话式检索和多轮研究助手有背景价值。", ["LLM", "Reasoning"]),
    chapter(12, "Machine Translation", "低", "略读", 40, "主要作为 seq2seq 和 attention 发展背景，非当前 KG-RAG 主线。", ["LLM"]),
    chapter(13, "RNNs and LSTMs", "低", "略读", 38, "作为序列建模历史背景，帮助对比 Transformer。", ["LLM"]),
    chapter(14, "Phonetics and Speech Feature Extraction", "低", "略读", 20, "语音特征与当前文本 KG-LLM 方向关联较弱。", ["Speech"]),
    chapter(15, "Automatic Speech Recognition", "低", "略读", 26, "可作为语音到文本入口了解，不是当前阅读重点。", ["Speech", "LLM"]),
    chapter(16, "Text-to-Speech", "低", "略读", 18, "与当前知识图谱和大模型推理方向关联较弱。", ["Speech"]),
    chapter(22, "Lexicons for Sentiment, Affect, and Connotation", "低", "略读", 34, "情感词典可作为 IE 的特殊知识资源了解。", ["IE", "KG"]),
]


NOTE_TEMPLATE = """# {number} {title}

## 章节定位
{positioning}

## 核心概念
- 

## 内容梳理
- 

## 公式与算法解释
- 

## 例子说明
- 

## 重点总结
- 

## 导师可能提问
- {question}

## 我的学习笔记
- 

## 和研究方向的联系
{relation}

## 后续补充资料
- 
"""


def seed() -> None:
    Base.metadata.drop_all(bind=engine)
    init_db()
    db = SessionLocal()
    try:
        source = Source(
            id=1,
            title="Speech and Language Processing, Third Edition draft",
            type="book",
            author_or_origin="Dan Jurafsky and James H. Martin",
            research_direction="LLM, RAG, KG, GraphRAG, IE, Entity Linking, Knowledge Graph Reasoning",
            description="默认内置的 NLP 重点阅读路线，围绕知识图谱、大语言模型推理、KG-RAG、GraphRAG、信息抽取和实体链接组织章节。",
            status="进行中",
            priority="高",
        )
        db.add(source)
        db.flush()
        for item in CHAPTERS:
            chapter_obj = Chapter(**item)
            db.add(chapter_obj)
            db.flush()
            db.add(
                Note(
                    source_id=source.id,
                    chapter_id=chapter_obj.id,
                    title=f"{chapter_obj.number} {chapter_obj.title} 阅读笔记",
                    content=NOTE_TEMPLATE.format(
                        number=chapter_obj.number,
                        title=chapter_obj.title,
                        positioning=chapter_obj.positioning,
                        question=chapter_obj.mentor_questions[0],
                        relation=chapter_obj.research_relation,
                    ),
                    tags=",".join(chapter_obj.tags),
                )
            )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("Seeded SLP3 reading notes data.")
