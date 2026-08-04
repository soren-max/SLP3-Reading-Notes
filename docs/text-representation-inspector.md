# Text Representation Inspector

## 输入

```json
{
  "text": "GraphReasoner-X2.5 使用了什么数据集？"
}
```

## 输出契约

```json
{
  "normalized_text": "GraphReasoner-X2.5 使用了什么数据集？",
  "tokens": ["Graph", "Reason", "##er", "-", "X", "##2", ".", "5", "使用", "了", "什么", "数据集", "？"],
  "token_ids": [1001, 1138, 1275, 1412, 1549, 1686, 1823, 1960, 2097, 2234, 2371, 2508, 2645],
  "offset_mapping": [[0, 5], [5, 11], [11, 13], [13, 14], [14, 15], [15, 17], [17, 18], [18, 19]],
  "token_count": 13,
  "detected_mentions": [
    {"text": "GraphReasoner-X2.5", "type": "MODEL", "start_char": 0, "end_char": 19, "start_token": 0, "end_token": 7}
  ],
  "mention_embeddings": [],
  "entity_candidates": [
    {"entity": "kg:GraphReasoner-X2.5", "score": 0.94},
    {"entity": "kg:GraphReasoner", "score": 0.61}
  ]
}
```

当前前端展页在 `/text-to-model` 提供这个契约的交互式 mock：展示原始文本、切分结果、数量、实体 span、字符 / token offset、候选实体与最终规范实体。接入实际 KG-RAG 服务时，替换 mock 的 `inspectText()` 为 tokenizer、NER 和 entity-linking API 即可；字段契约不变。
