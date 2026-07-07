# Chapter 3: Embeddings

## 章节定位

本章连接 Token 与 Transformer。Token 是离散的符号（ID），而模型需要在连续向量空间中计算。Embedding 就是将离散 Token 映射到连续向量空间的关键技术，是现代深度学习语言模型的基石。

## 核心概念

- **Embedding**：将离散的 Token ID 映射为稠密向量（Dense Vector）
- **嵌入维度（d_model）**：每个 Token 映射到的向量维度
- **Embedding Matrix**：词汇表大小 × 嵌入维度的查找表
- **语义空间**：向量之间的距离反映语义相似性
- **静态 vs. 上下文嵌入**：Word2Vec / GloVe 是静态的；BERT / GPT 的嵌入是上下文相关的

## 内容梳理

1. 为什么需要 Embedding？—— 离散符号无法直接输入神经网络
2. One-hot 编码 vs. 分布式表示
3. Embedding 矩阵的训练与查找
4. 从静态词向量（Word2Vec / GloVe）到上下文嵌入（ELMo / BERT）
5. 嵌入向量的语义性质：类比推理（king - man + woman ≈ queen）

## 公式与算法解释

**Word2Vec（Skip-gram 模型）：**

给定中心词 w，预测上下文词 c 的概率：

$$P(c|w) = \frac{\exp(v_c \cdot v_w)}{\sum_{c' \in V} \exp(v_{c'} \cdot v_w)}$$

其中 v_w、v_c 分别为中心词和上下文词的嵌入向量。

## 例子说明

**One-hot vs. Dense Embedding 对比：**

假设词汇表只有 5 个词：`[king, queen, man, woman, apple]`

**One-hot 编码（向量长度 = 词汇表大小 = 5）：**

| 词 | 向量 |
|---|---|
| king | [1, 0, 0, 0, 0] |
| queen | [0, 1, 0, 0, 0] |
| man | [0, 0, 1, 0, 0] |
| woman | [0, 0, 0, 1, 0] |
| apple | [0, 0, 0, 0, 1] |

问题：任意两个词的余弦相似度都为 0，无法表达语义关系。

**Dense Embedding（假设 d_model=3）：**

| 词 | 向量 |
|---|---|
| king | [0.82, 0.35, 0.12] |
| queen | [0.79, 0.38, 0.15] |
| man | [0.55, 0.62, 0.30] |
| woman | [0.52, 0.65, 0.33] |
| apple | [0.05, 0.92, 0.71] |

**语义类比推理：**

$$\text{king} - \text{man} + \text{woman} \approx \text{queen}$$

在向量空间中：
- king 和 queen 距离近（语义都是王室）
- man 和 woman 距离近（语义都是人类）
- apple 离所有词都较远（语义不同类）

这就是 Embedding 的核心价值：**将离散符号映射到语义连续的向量空间**。

## 重点总结

- Embedding 将离散 Token ID 转换为连续向量，是模型理解语言的基础
- 嵌入向量的质量决定了模型对语义关系的捕捉能力
- 现代 LLM 的 Embedding 不再是静态的，而是随着上下文动态变化

## 导师可能提问

**Q4：模型真的认识中文和英文吗？**

不是。模型最终接收的是 Token ID 对应的数字表示，再通过 Embedding 映射到向量空间进行计算。模型既不"认识"中文也不"认识"英文——它只认识向量空间中的几何关系。"苹果"和 "apple" 在嵌入空间中如果距离较近，模型就能跨语言理解它们的语义相似性。

## 我的理解

Embedding 层本质上是一张巨大的查找表。训练过程就是在调整这张表中每个 Token 对应的向量，使得语义相近的 Token 在向量空间中靠得更近。

这也可以解释为什么 LLM 能"理解"多种语言——并不是模型学会了中英文语法，而是中英文中语义相同的 Token（如 "苹果" 和 "apple"）在训练数据中频繁出现在相似的上下文里，从而被映射到嵌入空间中相近的位置。

## 与大语言模型 / AI Agent / RAG 的联系

- **LLM**：Embedding 是现代 LLM 的第一层，不可训练的 Embedding 层在推理时就是查表
- **AI Agent**：工具描述的语义匹配可以通过 Embedding 相似度实现
- **RAG**：文档 Embedding（向量化）是整个 RAG 管线的核心——用 Embedding 模型将文本转为向量，然后通过向量相似度检索相关文档
