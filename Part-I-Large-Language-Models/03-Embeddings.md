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

# Chapter 5: Embeddings

## 1. 章节定位 / Chapter Focus

本章介绍词义表示和 embedding 的基本思想。Token 是离散符号，神经网络不能直接从 token ID 中理解语义。Embedding 将离散 token、词、句子、文档或知识图谱节点映射到连续向量空间，使模型能够计算相似度、进行泛化，并支持语义检索。

This chapter introduces lexical semantics and embeddings. Tokens are discrete symbols, and neural networks cannot infer semantics from token IDs alone. Embeddings map tokens, words, sentences, documents, or knowledge graph nodes into continuous vector spaces, enabling similarity computation, generalization, and semantic retrieval.

从 KG-RAG 和 GraphRAG 的角度看，embedding 是连接文本、检索和知识图谱的语义入口。系统需要把 user query、document chunk、entity mention 和 KG node 映射到可比较的向量空间，才能进行候选召回、实体链接、子图检索和多跳问答。

From the perspective of KG-RAG and GraphRAG, embeddings are the semantic interface between text, retrieval, and knowledge graphs. A system needs to map user queries, document chunks, entity mentions, and KG nodes into comparable vector spaces for candidate retrieval, entity linking, subgraph retrieval, and multi-hop QA.

## 2. 核心概念 / Key Concepts

- **Lexical semantics（词汇语义）**：研究词义及词义关系，例如 synonymy、similarity、relatedness 和 connotation。
- **Lemma（词元）**：词的词典形式，例如 `mice` 的 lemma 是 `mouse`。
- **Word sense（词义）**：一个词在具体语境中的某个意义，例如 `mouse` 可以表示动物或电脑鼠标。
- **Synonymy（同义关系）**：意义相近的词之间的关系，但完全同义很少存在。
- **Similarity（相似性）**：词义相近，例如 `cat` 和 `dog`。
- **Relatedness（相关性）**：语义场景相关但不一定相似，例如 `coffee` 和 `cup`。
- **Semantic field（语义场）**：覆盖同一领域的一组词，例如 `hospital`、`doctor`、`nurse`。
- **Distributional hypothesis（分布假说）**：出现在相似上下文中的词往往具有相似意义。
- **Vector semantics（向量语义）**：用向量空间表示词义的方法。
- **Embedding（嵌入）**：对象的稠密向量表示，可以表示词、句子、文档、实体或图节点。
- **Co-occurrence matrix（共现矩阵）**：用上下文词出现频率表示目标词的矩阵。
- **Cosine similarity（余弦相似度）**：通过向量方向衡量语义接近程度。
- **Word2Vec / SGNS**：通过 skip-gram with negative sampling 学习静态词向量的经典方法。
- **Static embedding（静态嵌入）**：每个词只有一个固定向量，不能区分上下文词义。
- **Contextual embedding（上下文嵌入）**：同一个词在不同上下文中可以有不同向量表示。
- **Bias in embeddings（嵌入偏见）**：embedding 可能继承并放大训练语料中的社会偏见。

## 3. 从离散符号到向量语义 / From Symbols to Vectors

传统 NLP 中，词常被表示为字符串或词表编号。例如 `car` 和 `automobile` 是两个不同的离散 ID，模型无法仅凭 ID 知道它们语义相近。

In traditional NLP, words are often represented as strings or vocabulary IDs. For example, `car` and `automobile` are two different discrete IDs, so a model cannot know from the IDs alone that they are semantically close.

Embedding 的核心思想是把词映射到连续向量空间中。语义相近的词在向量空间中距离更近，出现在类似上下文中的词会形成相似的表示。

The central idea of embeddings is to map words into a continuous vector space. Semantically similar words should be close in this space, and words that occur in similar contexts should have similar representations.

这一思想来自 distributional hypothesis：You shall know a word by the company it keeps。也就是说，词义可以通过上下文分布来学习。

This idea comes from the distributional hypothesis: a word can be understood by the company it keeps. In other words, word meaning can be learned from contextual distribution.

## 4. Count-based Embeddings / 基于计数的嵌入

Count-based embeddings 使用共现矩阵表示词义。矩阵中的每一行表示一个目标词，每一列表示一个上下文词，元素表示它们在窗口内共同出现的次数。

Count-based embeddings represent word meaning with a co-occurrence matrix. Each row represents a target word, each column represents a context word, and each cell records how often they co-occur within a window.

示例：

Example:

| Target word | Context: doctor | Context: hospital | Context: engine |
|---|---:|---:|---:|
| nurse | 25 | 31 | 0 |
| surgeon | 19 | 28 | 0 |
| car | 0 | 1 | 34 |

`nurse` 和 `surgeon` 的上下文分布相似，因此它们的向量更接近。`car` 与医学语义场中的词距离更远。

The context distributions of `nurse` and `surgeon` are similar, so their vectors are closer. `car` is farther away from words in the medical semantic field.

这种方法直观、可解释，但矩阵通常高维、稀疏，并且容易受高频词影响。因此实际系统常使用降维、权重调整或神经方法学习低维稠密向量。

This approach is intuitive and interpretable, but the matrix is usually high-dimensional, sparse, and affected by frequent words. Practical systems often use dimensionality reduction, weighting schemes, or neural methods to learn low-dimensional dense vectors.

## 5. 向量相似度 / Vector Similarity

### 5.1 Dot Product

Dot product 衡量两个向量在相同维度上的共同强度：

The dot product measures the shared strength of two vectors across dimensions:

$$
v \cdot w = \sum_i v_i w_i
$$

Dot product 受向量长度影响。如果一个向量整体数值较大，即使方向不完全相同，也可能得到较高分数。

The dot product is affected by vector length. A vector with larger magnitude may receive a high score even when its direction is not very similar.

### 5.2 Cosine Similarity

Cosine similarity 更关注向量方向，而不是长度：

Cosine similarity focuses more on vector direction than vector length:

$$
\cos(v,w) = \frac{v \cdot w}{\|v\|\|w\|}
$$

其中：

Where:

$$
\|v\| = \sqrt{\sum_i v_i^2}
$$

在 RAG 中，cosine similarity 常用于比较 query embedding 和 document embedding。在实体链接中，它可以比较 mention embedding 和 candidate entity embedding。

In RAG, cosine similarity is commonly used to compare query embeddings and document embeddings. In entity linking, it can compare mention embeddings and candidate entity embeddings.

## 6. PMI 与 PPMI / PMI and PPMI

PMI（Pointwise Mutual Information）衡量两个词共同出现的强度是否高于随机独立情况下的预期。

PMI measures whether two words co-occur more often than expected under independence.

$$
PMI(w,c) = \log \frac{P(w,c)}{P(w)P(c)}
$$

PPMI（Positive PMI）将负值截断为 0：

PPMI clips negative PMI values to 0:

$$
PPMI(w,c) = \max(PMI(w,c), 0)
$$

PPMI 可以降低无意义低频或负相关值的影响，是从原始共现矩阵构造词向量的一种经典权重方式。

PPMI reduces the effect of unhelpful negative association values and is a classic weighting method for constructing word vectors from co-occurrence matrices.

## 7. Word2Vec 与 SGNS

Word2Vec 的代表方法之一是 skip-gram with negative sampling（SGNS）。它不直接保存完整共现矩阵，而是训练一个预测任务：给定 target word，判断某个 context word 是否可能出现在它附近。

One representative Word2Vec method is skip-gram with negative sampling (SGNS). Instead of storing a full co-occurrence matrix, it trains a prediction task: given a target word, decide whether a context word is likely to appear nearby.

SGNS 的直觉是：

The intuition of SGNS is:

- 真实共现的 target-context pair 应该被拉近。
- 随机采样的 negative pair 应该被推远。
- 训练完成后，模型权重就可以作为 word embeddings 使用。

SGNS objective 的简化形式：

Simplified SGNS objective:

$$
\log \sigma(v_c \cdot v_w) + \sum_{i=1}^{k}\log \sigma(-v_{n_i} \cdot v_w)
$$

其中 \(w\) 是 target word，\(c\) 是真实 context word，\(n_i\) 是 negative sample，\(k\) 是 negative samples 数量。

Here, \(w\) is the target word, \(c\) is a true context word, \(n_i\) is a negative sample, and \(k\) is the number of negative samples.

## 8. Analogy 与向量关系 / Analogy and Vector Relations

Embedding 空间有时可以捕捉某些关系方向。例如：

Embedding spaces can sometimes capture relation directions. For example:

$$
king - man + woman \approx queen
$$

这说明向量空间可能编码某些语义关系，例如性别、时态、国家与首都等。但这不是严格的逻辑推理，不能把 analogy 当作知识图谱中的确定关系。

This suggests that vector spaces may encode certain semantic relations, such as gender, tense, or country-capital patterns. However, this is not strict logical reasoning, and analogy should not be treated as a guaranteed knowledge graph relation.

## 9. Static 与 Contextual Embeddings

Static embedding 为每个词分配一个固定向量。例如 `bank` 无论出现在 `river bank` 还是 `bank account` 中，向量都相同。这会导致多义词表示不准确。

Static embeddings assign one fixed vector to each word. For example, `bank` has the same vector in `river bank` and `bank account`, which makes polysemy difficult to represent.

Contextual embedding 会根据上下文动态生成向量。同一个词在不同句子中可以有不同表示。这是 BERT、Transformer 和现代 LLM 的重要优势。

Contextual embeddings generate vectors dynamically based on context. The same word can have different representations in different sentences. This is a major advantage of BERT, Transformers, and modern LLMs.

| 类型 / Type | 特点 / Feature | 局限 / Limitation |
|---|---|---|
| Static embedding | 每个词一个固定向量 | 无法区分多义词 |
| Contextual embedding | 根据上下文生成不同向量 | 成本更高，依赖模型上下文 |

## 10. Sentence 与 Document Embeddings

RAG 系统通常不只需要 word embeddings，还需要 sentence embeddings 或 document embeddings。它们用于把 query 和文档 chunk 映射到同一向量空间。

RAG systems usually need not only word embeddings, but also sentence or document embeddings. These embeddings map queries and document chunks into the same vector space.

典型流程：

Typical pipeline:

```text
User query -> embedding model -> query vector
Document chunks -> embedding model -> document vectors
query vector + document vectors -> similarity search -> retrieved evidence
```

Sentence/document embedding 的质量直接影响 RAG 的召回率、证据相关性和最终答案可靠性。

The quality of sentence or document embeddings directly affects RAG recall, evidence relevance, and final answer reliability.

## 11. 与 KG-RAG / GraphRAG 的关系

Embedding 是 KG-RAG 和 GraphRAG 的语义召回层，但它不应替代知识图谱结构和逻辑约束。

Embeddings serve as the semantic retrieval layer in KG-RAG and GraphRAG, but they should not replace graph structure or logical constraints.

| 场景 / Scenario | Embedding 的作用 / Role |
|---|---|
| Query-document retrieval | 召回语义相关文档 chunk |
| Entity linking | 比较 mention context 和 candidate entity |
| Entity clustering | 合并同一实体的不同表面形式 |
| Subgraph retrieval | 召回与问题语义相关的 KG 节点和边 |
| Multi-hop QA | 先召回候选实体和路径，再由图结构或 LLM 验证 |
| Tool selection | 在 AI Agent 中匹配用户意图和工具描述 |

例如，`Apple released a new chip` 中的 `Apple` 更可能链接到 Apple Inc.，而不是水果。Embedding 可以利用上下文 `released`、`chip` 来提升候选排序。

For example, in `Apple released a new chip`, `Apple` is more likely to refer to Apple Inc. than the fruit. Embeddings can use context words such as `released` and `chip` to improve candidate ranking.

## 12. 局限与风险 / Limitations and Risks

Embedding 很有用，但不能被误认为可靠推理本身。

Embeddings are useful, but they should not be mistaken for reliable reasoning itself.

- Embedding 表达语义相似度，不等同于事实关系或逻辑蕴含。
- Two vectors being close does not guarantee that the corresponding entities have a true relation.
- Embedding 会继承训练语料中的 bias，可能影响检索、公平性和实体链接。
- Static embeddings 不能处理多义词，contextual embeddings 虽然更强但计算成本更高。
- 向量召回可能漏掉关键词精确匹配的重要证据，因此常需要 hybrid retrieval。
- 在 KG-RAG 中，embedding 召回结果应由图结构、类型约束、关系路径或证据文本进一步验证。

## 13. 重点总结 / Key Takeaways

- Embedding 将离散符号映射到连续向量空间，是现代 NLP 的基础。
- Distributional hypothesis 认为词义可以从上下文分布中学习。
- Count-based embeddings 直观可解释，但高维稀疏。
- Cosine similarity 常用于比较词、句子、文档和实体向量。
- PMI / PPMI 是从共现统计构造向量表示的重要方法。
- Word2Vec / SGNS 通过正样本拉近、负样本推远来学习低维稠密向量。
- Static embeddings 不能区分多义词，contextual embeddings 能根据上下文动态表示词义。
- RAG 依赖 sentence/document embeddings 进行语义检索。
- KG-RAG 和 GraphRAG 应把 embedding 召回与图结构、证据和约束结合起来。

## 14. 导师可能提问 / Possible Oral Exam Questions

**Q1: Why are embeddings important in modern NLP?**

因为 embeddings 把离散词语转换成连续向量，使模型能够计算语义相似度，并泛化到相似表达。

Because embeddings convert discrete words into continuous vectors, allowing models to compute semantic similarity and generalize to similar expressions.

**Q2: What is the distributional hypothesis?**

分布假说认为，出现在相似上下文中的词往往具有相似意义。

The distributional hypothesis states that words appearing in similar contexts tend to have similar meanings.

**Q3: Why is cosine similarity commonly used?**

因为 cosine similarity 主要比较向量方向，而不是绝对长度，适合衡量语义接近程度。

Because cosine similarity mainly compares vector direction rather than absolute magnitude, making it suitable for semantic similarity.

**Q4: What is the difference between static and contextual embeddings?**

Static embedding 为每个词分配一个固定向量；contextual embedding 根据上下文生成不同向量，因此能更好处理多义词。

Static embeddings assign one fixed vector to each word. Contextual embeddings generate different vectors based on context, so they handle polysemy better.

**Q5: How do embeddings support KG-RAG?**

Embedding 可以把 query、document chunk、entity mention 和 KG node 映射到向量空间，用于语义检索、实体链接、节点聚类和候选路径召回。

Embeddings map queries, document chunks, entity mentions, and KG nodes into vector space for semantic retrieval, entity linking, node clustering, and candidate path retrieval.

**Q6: What is a key limitation of embeddings in reasoning?**

Embedding 只能表示相似度或相关性，不能保证事实正确或逻辑关系成立。因此 KG-RAG 需要结合图结构、关系约束和证据验证。

Embeddings represent similarity or relatedness, but they do not guarantee factual correctness or logical relations. Therefore, KG-RAG needs graph structure, relation constraints, and evidence verification.
