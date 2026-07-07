---
note_title: "Embeddings：RAG、实体链接与语义检索的向量基础"
source: "Speech and Language Processing, Third Edition draft"
chapter: "Chapter 5: Embeddings"
section: "Full Chapter"
priority: "High"
status: "Reading"
tags:
  - LLM
  - Embedding
  - VectorSemantics
  - RAG
  - KG
  - IE
  - EntityLinking
  - Reasoning
research_direction: "KG-enhanced LLM Reasoning"
---

# Chapter 3: Embeddings

## 1. 本章定位

本章连接 Token 与 Transformer。Token 是离散的符号（ID），而模型需要在连续向量空间中计算。Embedding 就是将离散 Token 映射到连续向量空间的关键技术，是现代深度学习语言模型的基石。

从知识图谱增强大模型推理的角度来看，Embedding 是 KG-RAG、GraphRAG、实体链接和语义检索的语义入口。系统需要把用户 query、文档 chunk、实体 mention 和 KG node 都映射到同一向量空间，才能进行语义检索、候选召回和相似度计算。

## 2. 核心概念

- **lexical semantics**：研究词义及词义关系的领域，包括 synonymy、similarity、relatedness、connotation 等
- **lemma**：词元或词典形式，例如 mice 的 lemma 是 mouse
- **word sense**：一个词在具体语境中的某个意义，例如 mouse 可以表示动物或电脑鼠标
- **synonymy**：近义或同义关系，但完全同义很少存在
- **word similarity**：词义相似度，例如 cat 和 dog 语义相似
- **word relatedness**：词义相关性，例如 coffee 和 cup 不相似但在场景中相关
- **semantic field**：语义场，一组覆盖同一语义领域的词，如 hospital、doctor、nurse、scalpel
- **distributional hypothesis**：分布假说，出现在相似上下文中的词往往具有相似意义
- **vector semantics**：用向量空间表示词义的方法
- **embedding**：词语、句子或文档的稠密向量表示
- **co-occurrence matrix**：共现矩阵，用上下文词出现次数表示目标词
- **cosine similarity**：通过向量夹角计算语义相似度
- **Word2Vec / SGNS**：学习静态词向量的经典方法，skip-gram with negative sampling
- **static embedding**：每个词只有一个固定向量，不能区分不同上下文中的不同词义
- **bias in embeddings**：embedding 会学习并放大训练语料中的社会偏见

## 3. 关键理解

传统 NLP 中，词常被看成字符串或词表中的编号。这种表示方式不能表达词义相似性。例如 "car" 和 "automobile" 在离散词表中只是两个不同编号，模型无法天然知道它们相近。

Embedding 的核心思想是把词映射到向量空间中。语义相近的词，在向量空间中距离也应该更近。这一思想来自 **distributional hypothesis**：一个词的意义可以从它的上下文分布中学习。

Count-based embeddings 使用共现矩阵表示词义。每一行是目标词，每一列是上下文词，矩阵元素表示二者在窗口内共同出现的次数。这种方法直观，但向量维度高、稀疏，不适合大规模下游任务。

Word2Vec 进一步学习低维稠密向量。它不直接统计所有共现次数，而是训练一个预测任务：给定 target word，判断某个 context word 是否可能出现在它附近。训练完成后，模型权重就可以作为词向量使用。

## 4. 公式与方法

### Dot Product

$$v \cdot w = \sum_i v_i w_i$$

衡量两个向量在相同维度上的共同强度，但容易受向量长度影响。

### Cosine Similarity

$$\cos(v,w) = \frac{v \cdot w}{|v||w|}$$

更关注方向而不是长度。两个向量方向越接近，语义越相似。在 RAG 中用于 query 和 document 的相似度比较；在实体链接中用于 mention 和 candidate entity 的比较。

### Word2Vec / SGNS

将 embedding 学习转化为二分类任务：判断 context word 是否可能出现在 target word 附近；通过 negative sampling 提高训练效率。直觉是：真实共现的 pair 拉近，随机采样的 negative pair 推远。

### Analogy Vector

$$king - man + woman \approx queen$$

这说明 embedding 空间可能捕捉某些关系方向，但该方法有局限，不能当作可靠逻辑推理。

## 5. 与 KG-LLM 推理的关系

Embeddings 是 KG-RAG 和 GraphRAG 的语义入口。

在 **KG-RAG** 中，系统需要把用户 query、文档 chunk 和知识图谱节点映射到向量空间中，根据语义相似度召回相关文档和实体节点。

在 **GraphRAG** 中，embedding 帮助系统进行实体聚类、节点归一和子图召回。例如 "OpenAI"、"OpenAI Inc." 和 "OpenAI company" 可能合并为同一个 canonical entity。

在 **entity linking** 中，embedding 可以结合上下文区分多义实体。例如 "Apple released a new chip" 更可能链接到 Apple Inc.，而不是水果 apple。

在 **multi-hop QA** 中，embedding 可以先召回候选实体和候选路径，再由知识图谱结构或 LLM 进行更严格的推理。

## 6. 注意局限

- Embedding 主要表达语义相似度，**不等同于逻辑推理**。两个向量相近不能保证它们之间存在真实关系
- Embedding 会继承训练语料中的 bias，在知识图谱构建和问答系统中需要关注偏见和错误关联
- 向量模型的最终价值要通过下游任务评价，例如 RAG 检索效果、实体链接准确率、问答准确率

## 7. 复习重点

1. 理解 lexical semantics 和 vector semantics 的关系
2. 掌握 distributional hypothesis 的含义：上下文决定词义
3. 理解 count-based embeddings 的构造方式和局限
4. 会解释 cosine similarity 公式并手算简单例子
5. 理解 Word2Vec / SGNS 的训练直觉：正样本拉近，负样本推远
6. 能说明 embedding 如何用于 RAG 检索、实体链接和 GraphRAG
7. 知道 embedding 的局限：相似度不等于推理，语料偏见会进入向量空间

## 8. 导师可能提问

**Q1：为什么 embeddings 对现代 NLP 很重要？**

因为 embeddings 把离散词语转换成连续向量，使模型能够计算语义相似度，并在下游任务中泛化到相似表达。

**Q2：distributional hypothesis 的核心思想是什么？**

出现在相似上下文中的词往往具有相似意义，因此可以通过上下文分布学习词义表示。

**Q3：cosine similarity 为什么常用于语义相似度计算？**

因为它关注向量方向而不是绝对长度，适合比较词、句子或文档 embedding 的语义接近程度。

**Q4：Word2Vec 相比 count-based embedding 有什么优势？**

Word2Vec 学到的是低维稠密向量，参数更少，泛化能力更好，也更容易捕捉词义相似性。

**Q5：embedding 在知识图谱推理中有什么局限？**

embedding 擅长语义相似和候选召回，但不保证逻辑正确，也容易受语料偏见影响，需要和图结构、规则或 LLM 推理结合。

## 9. 与大语言模型 / AI Agent / RAG 的联系

- **LLM**：Embedding 是现代 LLM 的第一层，不可训练的 Embedding 层在推理时就是查表
- **AI Agent**：工具描述的语义匹配可以通过 Embedding 相似度实现
- **RAG**：文档 Embedding（向量化）是整个 RAG 管线的核心——用 Embedding 模型将文本转为向量，然后通过向量相似度检索相关文档
- **GraphRAG**：embedding 帮助实体聚类、节点归一和子图召回
- **Entity Linking**：embedding 结合上下文区分多义实体（如 Apple 是公司还是水果）
