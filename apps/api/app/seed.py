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


CHAPTER_10_NOTE = r"""# Chapter 10 · Post-training

> 本章关键词：**instruction tuning、preference alignment、reward model、DPO、test-time compute**。

## 1. 本章主题

本章讨论大语言模型完成预训练后的三个关键环节：instruction tuning、preference alignment 和 test-time compute。

预训练模型以预测下一个 token 为目标，因此具备广泛的语言能力，却不必然能正确理解和完成用户指令。Post-training 的作用是调整模型行为：让它更会遵循指令、更符合人类偏好，并能在复杂任务上使用更多推理计算。

## 2. Instruction Tuning

Instruction tuning 也称 supervised fine-tuning（SFT）。训练样本通常由自然语言指令、任务输入和目标回答组成；模型继续最小化语言模型的 cross-entropy loss，学习在给定指令下生成合适回答。

它与单任务微调的差别在于：SFT 往往覆盖多个任务和表达方式，目标是提升模型在新任务上的一般指令遵循能力，而不只是记住某一种标签映射。

## 3. Preference Learning

即使经过 instruction tuning，模型仍可能给出不安全、不忠实或帮助性不足的回答。Preference learning 使用同一 prompt 下多个候选回答之间的偏好关系继续训练模型。

常见的一条偏好数据写作 \((x, o_w, o_l)\)：

- \(x\)：prompt；
- \(o_w\)：preferred output（获偏好的回答）；
- \(o_l\)：dispreferred output（未获偏好的回答）。

这类数据直接表达“哪个回答更好”，但“更好”应由明确标准定义，例如帮助性、无害性、证据充分性与事实忠实度。

## 4. Reward Model

Reward model 接收 prompt 和回答，输出一个标量分数。Bradley–Terry model 用两个回答 reward 的差值表示偏好概率：

\[
P(o_w \succ o_l \mid x) = \sigma\bigl(r(x, o_w) - r(x, o_l)\bigr)
\]

Reward model 可用于模型对齐，也可用于 best-of-N candidate selection；但 reward 只反映训练数据中的偏好信号，不能直接等同于事实正确性。因此，在知识密集任务中仍需结合外部证据与事实验证。

## 5. Preference Alignment

从强化学习视角看，LLM 是 policy，生成 token 是 action，当前上下文是 state，reward model 为完整回答提供 reward。为防止优化后的模型过度偏离原模型，目标函数通常加入相对于 reference policy 的 KL penalty：

\[
\max_\pi\; \mathbb{E}[r(x, y)] - \beta\, D_{\mathrm{KL}}\bigl(\pi(\cdot\mid x)\,\|\,\pi_{\mathrm{ref}}(\cdot\mid x)\bigr)
\]

KL 项相当于行为约束：模型可以为偏好而调整，但不应丢失预训练或 SFT 阶段已有的通用能力。

## 6. DPO

Direct Preference Optimization（DPO）直接利用 preference pairs 训练模型：提高 preferred output 的概率，降低 dispreferred output 的概率，同时以 reference model 约束更新幅度。

DPO 不需要单独训练显式 reward model，训练流程通常比完整的 reward model + PPO 路线更简单。它的优势是工程链路较短；其效果仍取决于偏好数据的覆盖范围、标注准则与参考模型的质量。

## 7. Test-Time Compute

Test-time compute 指在推理阶段增加计算。教材重点介绍 chain-of-thought prompting：通过分步推理 demonstrations 引导模型解决复杂问题。

在 KG-RAG 中，test-time compute 可具体表现为：

- 问题分解；
- 实体识别与实体链接；
- 子图或候选证据检索；
- 候选路径比较；
- 证据验证与答案生成前的事实一致性检查。

这里增加的不是模型参数，而是为了可靠推理而执行的中间步骤、搜索和验证。

## 8. 对研究方向的意义

Post-training 决定模型如何使用其已有能力。对知识图谱增强推理而言，SFT 可以教模型遵守抽取、检索与引用流程；preference alignment 可以奖励有证据、路径正确和合理拒答的输出；test-time compute 则可以增加多跳检索与验证步骤。

一个可操作的研究问题是：将“答案是否可由检索到的知识图谱路径支撑”转化为偏好数据或奖励信号，并在推理时显式保留检索、比较和验证轨迹。

## 重点总结

- Post-training 将“会续写”的预训练模型转化为更能遵循指令、对齐偏好和完成复杂任务的助手。
- SFT 学习高质量示范；偏好学习学习回答之间的相对优劣。
- Reward 不能替代事实正确性，知识密集任务需要外部证据验证。
- DPO 以更简洁的训练链路直接使用偏好对；test-time compute 则在推理阶段补充搜索与验证。

## 导师可能提问

- Instruction tuning、preference alignment 和 test-time compute 分别改变模型的什么能力？
- 为什么 reward model 的高分不能保证答案事实正确？
- 如何把 KG-RAG 的证据路径正确性设计成可训练的偏好或奖励信号？

## 后续补充资料

- Ouyang et al. (2022), *Training language models to follow instructions with human feedback*。
- Rafailov et al. (2023), *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*。
- 比较 PPO、DPO 与基于 verifier 的 test-time scaling 在知识密集推理任务中的取舍。
"""


CHAPTER_11_NOTE = r"""# Chapter 11 · Retrieval-based Models

> 本章关键词：**Information Retrieval、BM25、dense retrieval、RAG、retriever、reranker、KG-RAG**。

## 1. 本章主题

本章介绍 Information Retrieval、dense retrieval 和 Retrieval-Augmented Generation（RAG）。其核心目标是让语言模型在生成答案前访问外部知识，而不是完全依赖模型参数中的记忆。

一个基础 RAG 系统由 retriever 和 generator 两部分组成：retriever 根据 query 从文档集合取回相关 passages，generator 将 query 和 passages 作为上下文，生成最终回答。检索质量决定模型是否能看到正确证据，生成质量决定模型是否正确使用证据。

## 2. Sparse Retrieval

Sparse retrieval 将 query 和 document 表示为词表维度上的稀疏向量。常见方法包括 tf-idf 和 BM25。

- TF 衡量一个词在当前文档中的重要性；
- IDF 衡量该词在整个文档集合中的区分能力；
- BM25 在此基础上加入词频饱和和文档长度归一化，通常是强而稳定的词法检索基线。

倒排索引建立“词项 → 文档列表”的映射，因此可以快速定位包含查询词的候选文档，而无须逐篇扫描整个集合。

## 3. Dense Retrieval

Dense retrieval 使用语言模型将 query 和 document 编码为低维向量，并通过 dot product 或 cosine similarity 计算相关性。其主要优势是处理 vocabulary mismatch：即使 query 和 document 未使用相同词语，只要语义接近，仍可能被匹配。

Bi-encoder 分别编码 query 与 document，可预先索引文档向量，效率高，适合大规模召回。Cross-encoder 联合编码 query 与 document，判断更精确但计算更昂贵，适合对少量候选进行 reranking。

一个常见的两阶段结构是：

1. bi-encoder 从全库召回 Top-k 候选；
2. cross-encoder 对候选重排；
3. 将高质量证据交给 generator。

## 4. Retrieval Evaluation

Precision 衡量返回结果中相关文档的比例，Recall 衡量全部相关文档中被成功取回的比例。二者需要结合任务目标取舍：问答的证据召回不足会直接限制后续生成，而候选过多又会引入噪声和上下文成本。

对于 ranked retrieval，还应考虑相关文档的排名位置。Average Precision（AP）对单个 query 在每个相关结果出现位置的 precision 求平均；MAP 则对多个 query 的 AP 再求平均。实践中还常报告 Recall@k、MRR 或 nDCG，以观察证据是否出现在模型可见的前几名。

## 5. Retrieval-Augmented Generation

基本 RAG 包括三步：

1. retriever 返回 Top-k passages；
2. 将 passages、query 和 instruction 组成 prompt；
3. LLM 基于 prompt 生成答案。

RAG 可以接入动态知识、企业私有文档和模型训练完成后出现的新知识，也能在回答中提供引用。它并不自动保证真实性：系统仍需确保 retrieved context 覆盖问题、噪声受控，并要求 generator 基于证据作答或在证据不足时拒答。

## 6. RAG 的主要错误来源

RAG 的错误可能来自多个环节：

- 文档集合中没有正确知识；
- chunk 划分不合理；
- retriever 未召回正确证据；
- 正确证据排名过低；
- 上下文包含过多噪声；
- LLM 没有正确使用证据；
- 答案与引用不一致。

因此，必须分别评价 retrieval 和 generation。端到端答案分数低时，应先定位是语料、切分、召回、重排、上下文构造，还是生成与引用阶段的问题。

## 7. 对 KG-RAG 的意义

KG-RAG 在普通文本 RAG 的基础上加入 entity linking 和 graph retrieval。系统可以检索实体、三元组、邻居和多跳路径，再将这些结构化证据与文本 passages 一起交给 LLM。

GraphRAG 进一步把检索对象扩展为子图和社区摘要，适合关系型问题、多跳问题和全局性问题。一个关键设计原则是按问题选择证据粒度：实体事实可优先检索三元组，关系解释可联合路径与段落，全局概览可使用社区摘要。

## 重点总结

- Sparse retrieval 依赖词项匹配，BM25 是必须保留的强基线；dense retrieval 缓解词汇不匹配。
- Bi-encoder 擅长高效召回，cross-encoder 擅长精确重排，二者通常组合使用。
- RAG 的可靠性取决于检索与生成两个独立环节，不能只看最终答案。
- KG-RAG 与 GraphRAG 通过实体、路径、子图和社区摘要，为多跳与关系型问题提供结构化证据。

## 导师可能提问

- Sparse retrieval 与 dense retrieval 各自解决什么问题，为什么 BM25 仍是重要基线？
- 为什么 bi-encoder 常用于召回、cross-encoder 常用于 reranking？
- 如何定位一个 KG-RAG 回答错误究竟来自检索、证据组织还是生成？

## 后续补充资料

- Robertson and Zaragoza (2009), *The Probabilistic Relevance Framework: BM25 and Beyond*。
- Karpukhin et al. (2020), *Dense Passage Retrieval for Open-Domain Question Answering*。
- Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*。
"""


NOTE_CONTENT_BY_NUMBER = {
    9: CHAPTER_9_NOTE,
    10: CHAPTER_10_NOTE,
    11: CHAPTER_11_NOTE,
}


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
    chapter(
        10,
        "Post-training",
        "高",
        "精读",
        95,
        "Post-training 决定模型如何使用已有能力：SFT 可教会模型遵守 KG-RAG 的抽取与检索流程，偏好对齐可奖励有证据、路径正确和合理拒答的输出，test-time compute 可加入多跳检索与验证。",
        ["LLM", "Alignment", "Reasoning", "RAG", "KG-RAG"],
        "已完成",
        positioning="第 10 章从后训练与推理时计算两个层面，连接模型行为对齐、证据遵循和知识图谱增强推理。",
        core_concepts=["Instruction Tuning", "Preference Alignment", "Reward Model", "DPO", "Test-Time Compute"],
        outline="依次理解 SFT 的多任务指令学习、偏好对的相对监督、reward model 与 KL 约束、DPO 的直接优化，以及推理阶段的分步计算。",
        formulas_algorithms="偏好概率可写为 P(ow ≻ ol|x)=σ(r(x,ow)-r(x,ol))；对齐目标在期望 reward 外加入相对 reference policy 的 KL penalty，以限制策略偏移。",
        examples="在 KG-RAG 中，SFT 学习抽取—检索—回答流程；偏好数据奖励受证据支撑的答案；推理时通过问题分解、子图检索、路径比较和事实验证增加计算。",
        summary="后训练塑造模型行为而非凭空赋予知识。可靠的知识增强推理需要高质量偏好标准、外部证据验证和显式的推理时搜索。",
        mentor_questions=[
            "Instruction tuning、preference alignment 和 test-time compute 分别改变模型的什么能力？",
            "为什么 reward model 的高分不能保证答案事实正确？",
            "如何把 KG-RAG 的证据路径正确性设计成可训练的偏好或奖励信号？",
        ],
        resources=[
            "Speech and Language Processing, Third Edition draft, Chapter 10",
            "Ouyang et al. (2022), Training language models to follow instructions with human feedback",
            "Rafailov et al. (2023), Direct Preference Optimization",
        ],
    ),
    chapter(
        11,
        "Retrieval-based Models",
        "高",
        "精读",
        98,
        "检索模型直接连接 RAG、KG-RAG 和 GraphRAG：文本与图结构证据的召回、重排、组织和验证，共同决定知识增强推理的可靠性。",
        ["RAG", "KG", "GraphRAG", "Reasoning", "Retrieval"],
        "已完成",
        positioning="第 11 章建立从词法/语义检索到 RAG、KG-RAG 与 GraphRAG 的证据增强生成主线。",
        core_concepts=["BM25", "Dense Retrieval", "Bi-encoder", "Cross-encoder", "RAG"],
        outline="从 sparse retrieval 与倒排索引出发，对比 dense retrieval 的语义匹配能力，再讨论检索评估、RAG 流程、错误诊断与图结构检索。",
        formulas_algorithms="稀疏检索以 tf-idf/BM25 匹配词项；稠密检索以 query/document 向量的 dot product 或 cosine similarity 打分。两阶段系统先 Top-k 召回，再以 cross-encoder 重排。",
        examples="对 KG-RAG 问题，先链接 query 实体并召回相关三元组、邻居和文本段落，再比较候选多跳路径，将受支持的结构化与非结构化证据输入 LLM。",
        summary="RAG 不是单一模型，而是一条可诊断的检索—证据组织—生成链路。需要分别评价召回覆盖、排名质量、上下文噪声、证据遵循和引用一致性。",
        mentor_questions=[
            "Sparse retrieval 与 dense retrieval 各自解决什么问题，为什么 BM25 仍是重要基线？",
            "为什么 bi-encoder 常用于召回、cross-encoder 常用于 reranking？",
            "如何定位一个 KG-RAG 回答错误究竟来自检索、证据组织还是生成？",
        ],
        resources=[
            "Speech and Language Processing, Third Edition draft, Chapter 11",
            "Karpukhin et al. (2020), Dense Passage Retrieval for Open-Domain Question Answering",
            "Lewis et al. (2020), Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        ],
    ),
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
                    content=NOTE_CONTENT_BY_NUMBER.get(chapter_obj.number) or NOTE_TEMPLATE.format(
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
