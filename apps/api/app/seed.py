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
    **details: object,
) -> dict:
    concepts = tags[:4] + ["Reading Notes"]
    data = {
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
    data.update(details)
    return data


CHAPTER_9_NOTE = r"""# Chapter 9 · Masked Language Models

> 本章关键词：**双向编码器、掩码语言建模（MLM）、上下文表示、预训练—微调、序列标注**。

## 1. 本章主题

本章介绍以 BERT 为代表的 **Masked Language Model（MLM）**。它不同于从左到右预测下一个 token 的 causal language model：MLM 会遮盖输入中的部分 token，再利用左右两侧上下文恢复原 token。

因此，MLM 通常使用 bidirectional Transformer encoder。它的核心产物不是连续生成的文本，而是每个 token 的上下文相关表示，尤其适合语言理解和信息抽取任务。

## 2. Bidirectional Transformer Encoder

Causal Transformer 使用 attention mask，禁止当前位置关注未来 token；bidirectional encoder 则移除这一限制，让每个 token 都能关注输入序列中的所有位置。

这种双向上下文特别适合需要理解整段输入的任务，例如：

- named entity recognition（NER）；
- text classification；
- relation extraction；
- entity linking；
- natural language inference（NLI）。

## 3. Masked Language Modeling

BERT 预训练时，随机选择约 **15%** 的 token 进行扰动：

- 80% 替换为 `[MASK]`；
- 10% 替换为随机 token；
- 10% 保持不变。

模型根据完整上下文预测这些位置原来的 token。若 \(M\) 是被选择的位置集合，训练目标只在这些位置计算交叉熵：

\[
\mathcal{L}_{\mathrm{MLM}} = - \sum_{i \in M} \log p_\theta(x_i \mid \tilde{x})
\]

其中，\(x_i\) 是原 token，\(\tilde{x}\) 是扰动后的输入。MLM 可以看作一种 denoising learning：先破坏输入，再训练模型恢复原始信息。

## 4. Contextual Embeddings

Static embedding 为一个词提供固定向量；contextual embedding 则会为同一个词在不同上下文中的实例生成不同向量。

例如，“**苹果发布了手机**”和“**吃了一个苹果**”中的“苹果”应有不同表示：前者更接近公司实体，后者更接近食物。这样的上下文敏感性使 MLM encoder 适合词义消歧、实体类型判断和实体链接。

## 5. Pretrain–Fine-tune Paradigm

模型先在大规模无标注文本上完成 MLM 预训练，学习通用语言表示；再在少量有标注数据上添加 task-specific head 并进行微调。这是一种 transfer learning：将预训练获得的语言知识迁移到具体下游任务。

实际使用时，需要区分两层能力：预训练提供可迁移的表示空间，微调则让表示适配任务标签、领域术语和评价目标。

## 6. Fine-Tuning for Classification

对于 sequence classification，BERT 通常在序列开头加入 `[CLS]`，取其最后一层向量作为整段文本的表示，再送入分类器。

对于 sequence-pair classification，输入两个由 `[SEP]` 分隔的序列。这一形式可用于自然语言推理、语义匹配，以及问题与候选证据的相关性判断。

## 7. Named Entity Recognition

NER 的目标是识别文本中的实体 span，并判断实体类型。常见类型包括 PER、ORG、LOC 和 GPE，也可以扩展为产品、作品、时间、金额等领域类型。

BIO tagging 中，B 表示实体开始、I 表示实体内部、O 表示非实体。做法是将每个 token 的 contextual embedding 输入同一个分类头，预测对应 BIO 标签。注意：实际实现需要处理 subword 与原始词边界的对齐，并可用 CRF 或约束解码减少非法标签序列。

## 8. 与知识图谱研究的关系

NER 是知识图谱构建的入口：先识别 entity mention，再通过 entity linking 将 mention 对齐到知识库的规范实体；随后可进行 relation extraction 和 event extraction，构建实体之间的边。

在 KG-RAG 中，encoder 模型可用于 query NER、entity linking、候选证据召回、reranking 和事实一致性判断；decoder LLM 则更适合问题分解、工具调用和自然语言答案生成。二者形成“**编码器负责找准证据，解码器负责组织推理与回答**”的互补分工。

## 重点总结

- MLM 通过双向上下文恢复被遮盖 token，学习上下文相关表示，而非自回归生成能力。
- contextual embeddings 是 NER、实体链接和关系抽取等理解任务的重要基础。
- 预训练—微调范式将大规模无标注语料中的知识迁移到具体下游任务。
- 在 KG-RAG 管线中，encoder 适合检索与判别，decoder LLM 适合推理与生成。

## 导师可能提问

- MLM 与 causal language model 的训练目标、可见上下文和典型用途分别有什么差异？
- 为什么 contextual embedding 能帮助实体消歧和 entity linking？
- 在 KG-RAG 中，哪些环节更适合 encoder，哪些环节更适合 decoder LLM？

## 后续补充资料

- Devlin et al. (2019), *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*。
- 比较 BERT、RoBERTa、DeBERTa 的预训练策略与下游迁移表现。
"""


CHAPTERS = [
    chapter(2, "Words and Tokens", "高", "精读", 90, "Tokenization 决定实体边界、检索粒度和 LLM 输入表示，是 NER 与实体链接的前置基础。", ["LLM", "NER", "Entity Linking", "KG"], "已完成"),
    chapter(5, "Embeddings", "高", "精读", 92, "Embedding 是 dense retrieval、实体表示、语义匹配和向量检索的核心基础。", ["LLM", "RAG", "KG", "Reasoning"], "已完成"),
    chapter(7, "Large Language Models", "高", "精读", 96, "LLM 是后续 KG-RAG、GraphRAG 与证据增强推理的生成和推理核心。", ["LLM", "Reasoning", "RAG", "KG"], "已完成"),
    chapter(8, "Transformers", "高", "精读", 94, "Transformer 提供上下文建模、注意力机制和 LLM 推理能力的结构基础。", ["LLM", "Reasoning", "RAG"], "已完成"),
    chapter(
        9,
        "Masked Language Models",
        "高",
        "理解",
        88,
        "MLM 训练出的双向上下文表示，是 query NER、实体链接、候选证据召回、reranking 和事实一致性判断的重要基础；它与负责分解和生成的 decoder LLM 形成互补。",
        ["LLM", "IE", "NER", "Entity Linking", "KG-RAG"],
        "已完成",
        positioning="第 9 章建立从双向预训练表示到 NER、实体链接和 KG-RAG 证据判别模块的连接。",
        core_concepts=["Masked Language Model", "BERT", "Bidirectional Encoder", "Contextual Embedding", "BIO Tagging"],
        outline="从双向 Transformer encoder 的可见上下文出发，理解 MLM 的扰动—恢复目标，并连接预训练—微调、分类和 NER 等下游任务。",
        formulas_algorithms="MLM 仅在被选择的掩码位置计算交叉熵：L_MLM = -Σ_{i∈M} log pθ(x_i | x̃)。BERT 的 15% 扰动中，80% 使用 [MASK]、10% 使用随机 token、10% 保持原 token。",
        examples="“苹果发布了手机”与“吃了一个苹果”中的“苹果”具有不同 contextual embedding；在 KG-RAG 中可据此辅助实体类型判断与实体链接。",
        summary="MLM 的价值在于学习适合理解和判别的双向上下文表示。encoder 擅长证据定位与一致性判断，decoder LLM 擅长推理编排与答案生成。",
        mentor_questions=[
            "MLM 与 causal language model 在训练目标、可见上下文和适用任务上有什么差异？",
            "为什么 contextual embedding 能帮助实体消歧和 entity linking？",
            "在 KG-RAG 管线中，encoder 和 decoder LLM 应如何分工？",
        ],
        resources=[
            "Speech and Language Processing, Third Edition draft, Chapter 9",
            "Devlin et al. (2019), BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
            "比较 BERT、RoBERTa、DeBERTa 的预训练策略与下游迁移表现",
        ],
    ),
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
                    content=CHAPTER_9_NOTE if chapter_obj.number == 9 else NOTE_TEMPLATE.format(
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
