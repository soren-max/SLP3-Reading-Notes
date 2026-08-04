# NER 的 Subword 对齐案例

句子：`GraphReasoner-X2.5 improves entity linking.`

原始实体：`GraphReasoner-X2.5 → MODEL`

假设 tokenizer 输出如下：

| Token | BIO 标签（标签复制策略） |
|---|---|
| Graph | B-MODEL |
| Reason | I-MODEL |
| ##er | I-MODEL |
| - | I-MODEL |
| X | I-MODEL |
| ##2 | I-MODEL |
| . | I-MODEL |
| 5 | I-MODEL |
| improves | O |
| entity | O |
| linking | O |
| . | O |

```json
{
  "entity_text": "GraphReasoner-X2.5",
  "start_char": 0,
  "end_char": 19,
  "start_token": 0,
  "end_token": 7
}
```

> `end_char` 和 `end_token` 采用右开区间：字符位置 19 与 token 位置 7 之后的边界分别不属于实体。

## 策略一：标签复制

将原始词标签复制到全部 subword，例如 `Graph` 是 `B-MODEL`，其余七个组成部分均为 `I-MODEL`。

- 优点：实现直接，模型对实体的每个片段都得到监督。
- 代价：长实体被拆得越碎，loss 中的权重越大，样本权重会受 tokenizer 影响。

## 策略二：只训练首个 subword

```text
Graph     B-MODEL
Reason    IGNORE
##er      IGNORE
-         IGNORE
X         IGNORE
##2       IGNORE
.         IGNORE
5         IGNORE
```

计算 loss 时忽略后续 subword（常用标签为 `-100`）。这避免碎片数改变一个词对 loss 的贡献，但预测完成后仍必须用 offset 或 word-id 映射恢复完整实体边界。

## 实践检查清单

1. offset 与原始字符串的位置约定要一致（推荐右开区间）。
2. special token 不参与实体标签和 loss。
3. 解码 BIO 序列后，按 token offset 合并回原始字符跨度。
4. 评估时在实体级别计算 precision / recall / F1，而不是只看 subword 级准确率。
