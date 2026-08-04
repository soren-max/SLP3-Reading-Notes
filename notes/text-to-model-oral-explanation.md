# 文本—模型接口：3–5 分钟口头讲解稿

自然语言进入模型后，首先经过 tokenizer，被切分成 token 或 subword，并映射为 token ID。Token ID 只是词表里的整数索引，不表示语义，也不能把不同 tokenizer 的 ID 直接比较。

模型接着用 embedding matrix 把 ID 转换成初始向量，并加入位置信息。随后 Transformer 利用 self-attention 融合上下文，输出每个位置的 contextual representation。

这一步很关键。例如“苹果发布了新产品”和“我吃了一个苹果”中的“苹果”，在 tokenizer 阶段可能完全一样，初始 embedding 也可能一样；但 Transformer 会分别利用“发布、新产品”和“吃、一个”等周边线索，所以最终向量不同，能够区分科技公司与水果。

这些上下文化表示可用于 NER、实体链接、语义检索和分类。但 tokenization 的错误会端到端传播。以 `GraphReasoner-X2.5 使用了什么数据集？` 为例：若模型名被切得很碎，NER 可能只识别出 `GraphReasoner`，实体链接便可能链接到错误的 KG 节点，之后图检索走到错误关系，LLM 最终仍能生成流畅但不正确的答案。

最后，embedding 的相似并不等于实体同一。苹果公司和微软公司在语义空间里可能很近，因为两者都是科技公司，但它们显然不是同一知识库实体。因此 KG-RAG 除了 embedding，还需要实体类型、别名匹配、字符级候选召回、KG 邻居与全局一致性校验。

我的结论是：tokenizer 是文本进入模型和知识图谱系统的接口。必须暴露 token、offset、实体 span、候选和最终规范实体，才能观察并调试 KG-RAG 的真实错误传播。
