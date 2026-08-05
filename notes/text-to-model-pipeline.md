# 文本—模型接口：从字符串到下游任务

## 完整处理链

```text
原始文本
  ↓
Unicode / Normalization
  ↓
Tokenizer
  ↓
Token / Subword
  ↓
Token ID
  ↓
Embedding Lookup
  ↓
Positional Information
  ↓
Transformer Encoder
  ↓
Contextual Representation
  ↓
NER / Entity Linking / Retrieval / Classification
```

| 阶段 | 输入 | 输出 | 核心作用 |
|---|---|---|---|
| Tokenizer | 原始字符串 | token 序列 | 决定模型处理单位 |
| ID Mapping | token | 整数 ID | 在词表中定位 token |
| Embedding | token ID | 初始向量 | 将离散符号变为连续表示 |
| Positional Information | 初始向量 | 带位置信息的向量 | 让模型知道 token 的顺序 |
| Transformer | 向量序列 | 上下文向量 | 融合左右或历史上下文 |
| Task Head | 上下文向量 | 标签或分数 | 完成 NER、检索、分类 |

## 关键解释：同一个“苹果”为何不同？

在“苹果发布了新产品”和“我吃了一个苹果”中，tokenizer 可能都产出同样的 token `苹果`。此时它们的 token ID，甚至 embedding lookup 得到的初始词向量都可能相同。

差异来自 Transformer：自注意力会把“发布”“新产品”以及“吃”“一个”等上下文融合到该 token 的表示中。因此，两个位置最后的 contextual representation 不同：前者更接近科技公司语义，后者更接近水果语义。

## 学习结论

Tokenizer 只定义模型看见的离散切分边界，不负责理解词义。Embedding 将 ID 映射为可学习向量；Transformer 才依据上下文动态重写每个位置的表示。最后，任务头根据这些表示输出实体标签、检索分数或分类结果。
