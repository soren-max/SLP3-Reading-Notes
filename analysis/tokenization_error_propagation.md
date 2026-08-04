# Tokenization 错误如何传播到 KG-RAG

## 案例

用户问题：`GraphReasoner-X2.5 使用了什么数据集？`

目标是找到知识图谱中规范实体 `kg:GraphReasoner-X2.5`，检索其 `trained_on` 或 `evaluated_on` 关系，再由 LLM 基于证据作答。

## 完整错误链

```text
GraphReasoner-X2.5 被 tokenizer 切成 Graph / Reason / ##er / - / X / ##2 / . / 5
        ↓
NER 只识别出 GraphReasoner，实体 span 漏掉 “-X2.5”
        ↓
Entity Linking 以部分字符串召回 kg:GraphReasoner，而非 kg:GraphReasoner-X2.5
        ↓
KG retrieval 从相似但错误的模型节点出发
        ↓
检索到 kg:GraphReasoner --evaluated_on--> WrongDataset 的关系
        ↓
LLM 根据错误路径生成一段流畅、带有“证据”的答案
```

这里的风险不是模型简单地“幻觉”，而是前端表示、实体识别、链接和检索的每一层都把前一层错误当作输入。最终答案即使有引用路径，也可能是从错误节点检索得到的错误路径。

## 可观察的中间状态

| 阶段 | 期望 | 失败输出 | 可观测信号 |
|---|---|---|---|
| Tokenizer | 完整实体可由 offset 合并 | 8 个碎片 | token 数量异常、offset 连续 |
| NER | `GraphReasoner-X2.5 / MODEL` | `GraphReasoner / MODEL` | `end_char` 太早 |
| Entity Linking | `kg:GraphReasoner-X2.5` | `kg:GraphReasoner` | top-1 只为部分匹配 |
| KG Retrieval | 正确模型邻居 | 相似模型邻居 | 路径首节点不一致 |
| Generation | 基于正确三元组回答 | 基于错误三元组回答 | answer 与规范实体不一致 |

## 修复方法：多层防线

1. **Tokenizer offset 对齐**：保存 token 到字符的右开区间 offset；预测后以 offset 还原实体，而不是只拼接表面 token。
2. **领域实体词典**：将常见模型名、版本号和连字符形式加入识别与候选生成词典。
3. **Alias Matching**：维护 `GraphReasoner X2.5`、`GraphReasoner-X2.5`、`GR-X2.5` 等规范名与别名。
4. **Character-level Candidate Recall**：即使 NER span 不完整，也从原始字符窗口召回包含版本号的候选，而不只依赖 token 边界。
5. **Entity Type Filtering**：问题中的对象应为 `MODEL`；过滤数据集、论文或组织等同名候选。
6. **KG Coherence Verification**：检索前后检查问题实体、规范实体、路径首节点的一致性；若候选置信度低或路径冲突，要求重链接或澄清。

## 结论

Tokenization 是 KG-RAG 的输入接口，而不是隐藏的预处理细节。将 token、offset、mention、候选实体和最终规范实体都暴露到 trace 中，才能定位端到端错误源，并避免“检索增强”把早期错误包装为更可信的答案。
