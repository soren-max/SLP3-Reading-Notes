# Part I：Large Language Models（导读）

《Speech and Language Processing》第三版将 **Large Language Models** 作为全书开篇，体现了现代自然语言处理研究范式的根本变化。与传统教材按照"统计模型 → 机器学习 → 深度学习"的发展顺序不同，新版教材直接从 LLM 出发，介绍现代 NLP 的核心思想。

## 为什么第三版教材一开始就讲 LLM？

因为 LLM 已经成为现代 NLP 的核心范式，几乎所有自然语言任务都建立在预训练大模型基础上，因此新版教材直接围绕 LLM 展开。

## LLM 和传统 NLP 最大区别是什么？

传统 NLP 更多依赖人工设计规则和统计模型，而 LLM 通过海量数据预训练学习语言规律，能够统一完成多种 NLP 任务。

## 本部分内容主线

本部分首先介绍 LLM 的基本概念及其在自然语言处理中的重要地位，随后引出 **Words** 与 **Tokens** 的区别。作者强调，大语言模型真正处理的对象不是自然语言文本本身，而是经过 Tokenizer 切分后的 Token 序列。Token 经过 **Embedding** 转换为向量表示后，输入 Transformer 模型完成下一 Token 的预测，因此 **Token 是现代 LLM 的基础数据表示**。

从 Ch 4 开始，教材逐步展开语言模型的基础构件：Logistic Regression（线性分类基础）、N-gram Language Models（统计语言模型）、Neural Networks（表示学习和非线性变换），并在 Ch 7 将这些知识串联为完整的 Large Language Model 体系。Ch 8 进一步进入 Transformer 架构，解释 self-attention、multi-head attention、residual stream、KV cache 和 LoRA 等现代 LLM 的核心机制。

理解 **Token、Embedding 与 Transformer** 之间的关系，是后续学习语言模型、注意力机制以及生成模型的重要前提。

## 章节概览

| 章节 | 主题 | 核心内容 |
|---|---|---|
| Ch 1 | Introduction | LLM 范式、教材定位 |
| Ch 2 | Words and Tokens | 分词、Tokenization、子词、KG-LLM 输入层基础 |
| Ch 3 | Embeddings | 词向量、表示学习 |
| Ch 4 | Logistic Regression | 分类模型、Sigmoid、特征工程 |
| Ch 5 | N-gram Language Models | 统计语言模型、平滑方法 |
| Ch 6 | Neural Networks | 表示学习、激活函数、Softmax |
| Ch 7 | Large Language Models | 自回归生成、In-context Learning、训练三阶段、安全 |
| Ch 8 | Transformers | Self-attention、QKV、Transformer Block、KV Cache、LoRA |
