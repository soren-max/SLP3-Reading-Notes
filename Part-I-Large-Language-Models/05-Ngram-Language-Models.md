# Chapter 5: N-gram Language Models

## 章节定位

本章介绍统计语言模型（Statistical Language Model）的基本思想。语言模型的目标是估计一段文本出现的概率，并根据已有上下文预测下一个词。N-gram 模型通过马尔可夫假设降低条件概率的计算复杂度，是理解后续神经网络语言模型和 Transformer 的重要基础。

## 核心概念

- **语言模型（Language Model）**：计算一段文本出现概率的模型
- **链式法则（Chain Rule）**：将句子联合概率分解为多个条件概率的乘积
- **N-gram**：基于前 N−1 个词预测第 N 个词的统计模型
- **马尔可夫假设（Markov Assumption）**：下一个词仅依赖于前 N−1 个词
- **数据稀疏（Data Sparsity）**：由于语料有限，大量 N-gram 从未出现，导致概率估计为零

## 内容梳理

1. Language Model 的任务：估计文本概率 + 预测下一个 Token
2. 从链式法则到 N-gram：用有限上下文近似完整历史
3. N-gram 的优缺点：降低复杂度 vs. 固定上下文窗口 + 数据稀疏
4. 平滑方法：处理未出现的 N-gram
5. 从 N-gram 到 Transformer：保留同一目标，突破上下文限制

## 公式与算法解释

**链式法则：**

$$P(w_1, w_2, ..., w_n) = \prod_{i=1}^{n} P(w_i | w_1, w_2, ..., w_{i-1})$$

**N-gram 近似（马尔可夫假设）：**

$$P(w_i | w_1, ..., w_{i-1}) \approx P(w_i | w_{i-N+1}, ..., w_{i-1})$$

例如 Bigram (N=2) 假设下一个词仅依赖前一个词：

$$P(w_i | w_1, ..., w_{i-1}) \approx P(w_i | w_{i-1})$$

## 例子说明

**小语料上的 Bigram 概率计算：**

假设训练语料只有以下 3 个句子：
```
<s> I love NLP </s>
<s> I love learning </s>
<s> NLP is fun </s>
```

**Step 1 — 统计所有 Bigram 出现次数：**

| Bigram | 计数 |
|---|---|
| `<s> I` | 2 |
| `I love` | 2 |
| `love NLP` | 1 |
| `NLP </s>` | 1 |
| `love learning` | 1 |
| `learning </s>` | 1 |
| `NLP is` | 1 |
| `is fun` | 1 |
| `fun </s>` | 1 |

**Step 2 — 计算 Bigram 概率（MLE 最大似然估计）：**

$$P(\text{love} | \text{I}) = \frac{\text{count(I love)}}{\text{count(I)}} = \frac{2}{2} = 1.0$$

$$P(\text{NLP} | \text{love}) = \frac{\text{count(love NLP)}}{\text{count(love)}} = \frac{1}{2} = 0.5$$

$$P(\text{learning} | \text{love}) = \frac{\text{count(love learning)}}{\text{count(love)}} = \frac{1}{2} = 0.5$$

**Step 3 — 计算整句概率：**

`P(I love NLP) = P(I|<s>) × P(love|I) × P(NLP|love) × P(</s>|NLP)`
`= 2/3 × 1.0 × 0.5 × 1.0 ≈ 0.33`

**数据稀疏问题体现：**

Bigram `love Python` 从未在语料中出现过，即使它在语义上完全合理，概率也被估计为 0 → 这就是需要 **平滑（Smoothing）** 的原因。

## 重点总结

- Language Model 用于计算一句话出现的概率，是 NLP 的核心基础
- N-gram 假设下一个词只依赖于前 N−1 个词，用局部上下文近似完整历史
- Chain Rule 可以将整句话概率分解为多个条件概率的乘积
- N-gram 能有效降低计算复杂度，但会引入信息丢失
- Data Sparsity（数据稀疏）是 N-gram 面临的主要挑战，也是后续提出平滑（Smoothing）等方法的原因
- 现代 Transformer 仍然遵循"根据已有上下文预测下一个 Token"这一基本思想，只是能够利用更长甚至整个上下文

## 导师可能提问

**Q1：Language Model 的任务是什么？**

估计一段文本的概率，或者根据已有上下文预测下一个词（Token）。

**Q2：为什么需要 N-gram？**

完整历史条件概率难以统计，N-gram 用有限上下文近似完整历史，降低了模型复杂度。

**Q3：N-gram 的主要缺点是什么？**

只能利用固定长度上下文，难以捕获长距离依赖，同时容易出现数据稀疏问题。

**Q4：Transformer 与 N-gram 有什么关系？**

两者目标相同，都是预测下一个 Token。区别在于 N-gram 只使用固定长度上下文，而 Transformer 通过注意力机制动态利用整个上下文，因此能够建模更复杂的语言关系。

## 我的理解

本章介绍了统计语言模型（Statistical Language Model）的基本思想。语言模型的目标是计算一段文本出现的概率，并根据已有上下文预测下一个词。根据链式法则，句子的联合概率可以分解为多个条件概率的乘积，但直接计算完整历史条件概率会遇到数据稀疏和计算复杂度过高的问题。

N-gram 模型采用马尔可夫假设（Markov Assumption），认为下一个词仅依赖于前 N−1 个词，从而将复杂的联合概率估计转化为局部条件概率估计。虽然这种方法有效降低了计算成本，但也限制了模型对长距离依赖关系的建模能力。现代神经网络语言模型和 Transformer 正是在保留"预测下一个 Token"目标的基础上，突破了 N-gram 固定上下文窗口的限制。

## 与大语言模型 / AI Agent / RAG 的联系

- **LLM**：N-gram 的"预测下一个 Token"目标被 Transformer 继承，但上下文窗口从固定 N 扩展到整个序列
- **AI Agent**：Agent 的推理过程本质也是一个自回归生成过程，每一步都在预测下一个 Action Token
- **RAG**：N-gram 时代的检索严重依赖词频统计；现代 RAG 用 Embedding 语义检索取代了词袋匹配
