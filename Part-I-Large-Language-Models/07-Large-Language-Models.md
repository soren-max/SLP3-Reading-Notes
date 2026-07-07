# Chapter 7: Large Language Models

## 章节定位

本章将前六章的知识串联起来，正式介绍大语言模型（LLM）的基本思想、生成方式、训练流程、评价方法以及安全问题。大语言模型本质上仍然是语言模型，其核心任务是根据已有上下文预测下一个 Token。与 N-gram 模型相比，大语言模型能够利用更长的上下文，并通过神经网络学习复杂的语言、语义和世界知识。

## 核心概念

- **自回归生成（Autoregressive Generation）**：从左到右逐 Token 生成文本
- **Decoder-only 架构**：GPT、Claude、Llama 等常见生成式 LLM 采用的结构
- **In-context Learning（上下文学习）**：通过 Prompt 中的示例临时学习任务格式，不更新参数
- **Temperature Sampling**：通过调节概率分布的平滑程度，在多样性和稳定性之间取得平衡
- **训练三阶段**：Pretraining → Instruction Tuning → Preference Alignment
- **Hallucination（幻觉）**：模型生成看似合理但与事实不符的内容

## 内容梳理

1. **三类架构**：Encoder（如 BERT）、Decoder（如 GPT）、Encoder-Decoder（如 T5）
2. **Decoder 生成方式**：自回归，每步根据已有上下文预测下一个 Token，生成结果继续加入上下文
3. **NLP 任务的统一**：情感分析、问答、翻译、摘要等都可转化为条件生成任务
4. **Prompt 与 In-context Learning**：Prompt 不仅是输入，也可作为任务说明；含示例时可临时学习
5. **解码策略**：Greedy Decoding、Random Sampling、Temperature Sampling
6. **训练流程**：Pretraining（自监督，预测下一个 Token）→ Instruction Tuning（遵循指令）→ Preference Alignment（对齐人类偏好）
7. **安全与伦理**：Hallucination、Bias、Privacy Leakage 及应对方法

## 公式与算法解释

**自回归生成：**

$$P(w_1, w_2, ..., w_n) = \prod_{i=1}^{n} P(w_i | w_1, w_2, ..., w_{i-1})$$

与 N-gram 相同的链式法则，但条件概率由神经网络（Transformer）计算，而非简单的频率统计。

**Temperature Softmax：**

$$P(w_i | context) = \frac{\exp(z_i / T)}{\sum_{j} \exp(z_j / T)}$$

- T → 0：分布趋于 one-hot（等价于 Greedy Decoding）
- T = 1：原始 Softmax 分布
- T → ∞：分布趋于均匀（完全随机）

## 例子说明

**三类架构的任务对比：**

| 架构 | 代表模型 | 典型任务 | 生成方式 |
|---|---|---|---|
| Encoder-only | BERT | 文本分类、实体识别 | 双向编码，不生成 |
| Decoder-only | GPT / Claude / Llama | 文本生成、对话、翻译 | 自回归从左到右 |
| Encoder-Decoder | T5 / BART | 翻译、摘要、问答 | 编码后解码生成 |

**Prompt 如何将不同任务统一为条件生成：**

| 任务 | Prompt 示例 | 模型续写 |
|---|---|---|
| 情感分析 | `评论：这部电影太棒了。情感：` | `正面` |
| 翻译 | `Translate to Chinese: I love NLP →` | `我爱自然语言处理` |
| 摘要 | `以下文章的摘要：<文章> → 摘要：` | `……` |
| 问答 | `Q：什么是 Transformer？A：` | `一种基于注意力机制的神经网络架构` |

**Temperature 对生成效果的影响：**

输入 Prompt：`"The best movie I have ever"`

| Temperature | 可能的续写 | 特点 |
|---|---|---|
| T = 0（Greedy） | `seen.` | 最安全，但可能重复单调 |
| T = 0.7 | `seen in years. It was amazing!` | 平衡多样性与流畅性 |
| T = 1.5 | `seen... wait, no, the worst film. Actually...` | 多样性高，可能不连贯 |

## 重点总结

- 大语言模型本质仍是语言模型，核心任务不变：预测下一个 Token
- Decoder-only 架构是当前生成式 LLM 的主流选择
- Prompt 将不同 NLP 任务统一为条件生成范式
- In-context Learning 通过示例临时学习，**不更新模型参数**
- Temperature 控制生成多样性：T 越低越稳定，T 越高越多样
- 训练三阶段：Pretraining → Instruction Tuning → Preference Alignment
- LLM 的优化目标主要是生成连贯文本，而不是保证事实正确 → 需关注 Hallucination、Bias 等安全问题

## 导师可能提问

**Q1：Decoder-only 架构和 Encoder-Decoder 架构有什么区别？**

Decoder-only 是纯自回归结构，输入和输出共享同一上下文窗口；Encoder-Decoder 先用 Encoder 编码输入，再由 Decoder 生成输出，适合输入输出差异较大的任务（如翻译）。

**Q2：In-context Learning 和 Fine-tuning 有什么区别？**

In-context Learning 通过在 Prompt 中加入示例让模型临时学习任务格式，**不更新模型参数**；Fine-tuning 需要在任务数据上继续训练，**更新模型参数**。

**Q3：Temperature 为 0 时会发生什么？**

等价于 Greedy Decoding，每次选择概率最高的 Token，生成结果确定且稳定，但容易陷入重复循环。

**Q4：为什么 LLM 会产生 Hallucination？**

因为 LLM 的训练目标是生成高概率的连贯文本，而不是保证事实正确。模型学到的是 Token 之间的统计相关性，而非真正的"知识"。

**Q5：Preference Alignment（如 RLHF）解决的是什么问题？**

Pretraining 阶段模型只学会预测下一个 Token，不一定符合人类期望。Preference Alignment 通过人类反馈数据，让模型学会输出更有用、更少有害的回答。

## 我的理解

本章介绍了大语言模型的基本思想、生成方式、训练流程、评价方法以及安全问题。大语言模型本质上仍然是语言模型，其核心任务是根据已有上下文预测下一个 Token。与 N-gram 模型相比，大语言模型能够利用更长的上下文，并通过神经网络学习复杂的语言、语义和世界知识。

本章首先介绍了语言模型的三类主要架构：Encoder、Decoder 和 Encoder-Decoder。其中，GPT、Claude、Llama 等常见生成式大语言模型主要采用 Decoder 架构。Decoder 模型按照从左到右的方式生成文本，每一步根据已有上下文预测下一个 Token，并将生成结果继续加入上下文中。

大语言模型的一个重要能力是将不同 NLP 任务转化为条件生成任务。情感分析、问答、翻译和摘要等任务都可以通过 Prompt 描述出来，再由模型继续生成答案。Prompt 不仅是输入文本，也可以作为一种任务说明。当 Prompt 中包含示例时，模型可以通过 In-context Learning 临时学习任务格式和规律，但这一过程不会更新模型参数。

在生成阶段，模型需要从概率分布中选择下一个 Token。Greedy Decoding 每次选择概率最高的 Token，稳定但容易重复；Random Sampling 更有多样性，但可能生成低质量内容；Temperature Sampling 通过调节概率分布，在稳定性和多样性之间取得平衡。

本章还介绍了大语言模型的训练流程，通常包括 Pretraining、Instruction Tuning 和 Preference Alignment 三个阶段。Pretraining 使用大规模文本进行自监督训练，目标是预测下一个 Token；Instruction Tuning 让模型学会遵循人类指令；Preference Alignment 则通过人类偏好数据，使模型输出更加有用且更少有害。

最后，本章指出大语言模型不仅要从性能角度评价，也要关注安全和伦理问题。由于模型训练目标主要是生成连贯且高概率的文本，而不是保证事实正确，因此可能出现 Hallucination、Bias、Privacy Leakage 等问题。在实际应用中，应结合检索、验证、人工审核和安全对齐等方法降低风险。

## 与大语言模型 / AI Agent / RAG 的联系

- **LLM**：本章是全书核心，将前六章的技术整合为完整的 LLM 系统
- **AI Agent**：Agent 利用 LLM 的指令跟随能力和 In-context Learning 进行工具调用与任务规划
- **RAG**：RAG 通过外部知识检索缓解 LLM 的 Hallucination 问题，是安全部署的重要补充手段
