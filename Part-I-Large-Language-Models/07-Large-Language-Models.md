# Chapter 7: Large Language Models

## 1. 章节定位 / Chapter Focus

本章系统介绍大语言模型（Large Language Models, LLMs）的基本原理、生成机制、训练流程、评价方法和安全问题。LLM 的核心思想并不神秘：它本质上仍然是一个语言模型，主要任务是在给定上下文的条件下预测下一个 token。

This chapter introduces the basic principles of Large Language Models (LLMs), including conditional generation, prompting, decoding and sampling, training, evaluation, and safety. At its core, an LLM is still a language model: it predicts the next token given the previous context.

本章的重点不是 Transformer 的内部结构，而是理解 LLM 如何把自然语言任务统一为生成问题，以及为什么这种生成能力既强大又需要外部约束。

The focus is not the internal architecture of Transformers, but the general working mechanism of LLMs: how they convert many NLP tasks into generation problems, and why this ability requires careful grounding and safety control.

## 2. 核心概念 / Key Concepts

- **Large Language Model（大语言模型）**：在大规模文本上训练的神经语言模型，通常拥有大量参数和较强的上下文建模能力。
- **Next-token Prediction（下一 token 预测）**：根据已有上下文预测下一个 token，是 LLM 预训练的核心目标。
- **Conditional Generation（条件生成）**：模型在给定输入文本、任务说明或上下文的条件下继续生成输出。
- **Prompting（提示）**：通过自然语言指令、模板或示例引导模型完成任务。
- **In-context Learning（上下文学习）**：模型利用 prompt 中的示例改善输出表现，但不更新模型参数。
- **Sampling（采样）**：从模型输出的概率分布中选择下一个 token 的过程。
- **Alignment（对齐）**：通过偏好数据、奖励模型或安全策略，使模型输出更符合人类意图和安全要求。
- **Hallucination（幻觉）**：模型生成看似合理但事实上错误、无证据或与输入不一致的内容。

## 3. 三类语言模型架构 / Three Main Architectures

语言模型通常可以分为三类架构：encoder-only、decoder-only 和 encoder-decoder。

Language models can be broadly categorized into three architectures: encoder-only, decoder-only, and encoder-decoder models.

| 架构 / Architecture | 代表模型 / Examples | 主要能力 / Main Capability | 典型任务 / Typical Tasks |
|---|---|---|---|
| Encoder-only | BERT, RoBERTa | 双向理解输入文本 / Bidirectional understanding | 文本分类、实体识别、向量检索 |
| Decoder-only | GPT, Claude, Llama | 自回归生成文本 / Autoregressive generation | 对话、问答、写作、代码生成 |
| Encoder-decoder | T5, BART | 编码输入后生成输出 / Encode input, then decode output | 翻译、摘要、复杂文本转换 |

在 KG-RAG 系统中，这三类能力经常协同出现：encoder 模型用于向量检索、实体匹配和语义相似度计算；decoder LLM 用于自然语言答案生成；知识图谱则负责提供结构化事实、关系约束和多跳推理路径。

In KG-RAG systems, these capabilities often work together. Encoder models are used for retrieval, entity matching, and semantic similarity; decoder LLMs generate natural-language answers; knowledge graphs provide structured facts, relation constraints, and multi-hop reasoning paths.

## 4. Conditional Generation / 条件生成

Conditional generation 指模型在给定输入条件后继续生成文本。许多 NLP 任务都可以被重新表述为条件生成任务。

Conditional generation means generating text conditioned on an input. Many NLP tasks can be reformulated as conditional generation problems.

| 任务 / Task | 条件输入 / Condition | 目标输出 / Target Output |
|---|---|---|
| 情感分类 / Sentiment classification | `Review: This movie is wonderful. Sentiment:` | `positive` |
| 问答 / Question answering | `Q: What is a language model? A:` | A natural-language answer |
| 翻译 / Translation | `Translate into Chinese: I love NLP.` | `我爱自然语言处理。` |
| 摘要 / Summarization | `Summarize the following article: ...` | A concise summary |
| 信息抽取 / Information extraction | `Extract entities and relations as JSON: ...` | Structured JSON |

这种统一形式是 LLM 的重要优势。它使分类、抽取、问答、摘要和翻译等任务都可以通过相似的生成接口完成。但需要注意：模型能够生成答案，并不意味着答案一定正确。

This unified format is a major advantage of LLMs. Classification, extraction, QA, summarization, and translation can all be handled through a similar generation interface. However, the ability to generate an answer does not guarantee factual correctness.

## 5. Prompting 与 In-context Learning

Prompt 是用户提供给模型的输入，可以包含任务说明、上下文、格式约束和示例。Prompt engineering 的目标是让模型更稳定地理解任务，并输出符合预期格式的结果。

A prompt is the input given to the model. It may include instructions, context, formatting constraints, and examples. Prompt engineering aims to make the model understand the task more reliably and produce outputs in the expected format.

### 5.1 Zero-shot Prompting

Zero-shot prompting 不提供示例，只给出任务说明。

Zero-shot prompting provides only the task instruction without examples.

```text
Classify the sentiment of the sentence.
Sentence: The product is useful but too expensive.
Sentiment:
```

### 5.2 Few-shot Prompting

Few-shot prompting 在 prompt 中加入少量 demonstrations，让模型模仿示例的任务格式和输出模式。

Few-shot prompting includes a small number of demonstrations so that the model can imitate the desired format and behavior.

```text
Sentence: I love this book.
Sentiment: positive

Sentence: The service was slow and rude.
Sentiment: negative

Sentence: The interface is simple and elegant.
Sentiment:
```

### 5.3 In-context Learning

In-context learning 指模型从 prompt 中的上下文和示例中临时获得任务信息，但模型参数不会被更新。

In-context learning means that the model uses information and examples in the prompt to improve its behavior, without updating its parameters.

在 AI Agent 中，system prompt 常用于规定角色、任务边界、工具使用规则、输出格式和安全要求。但 system prompt 只是软约束，工程上仍需要工具权限控制、结构化输出校验、检索证据、日志记录和人工审核。

In AI agents, the system prompt is often used to define the role, task boundary, tool-use policy, output format, and safety requirements. However, a system prompt is only a soft constraint. Robust systems also need tool permission control, structured output validation, retrieved evidence, execution logs, and human review when necessary.

## 6. Generation and Sampling / 生成与采样

LLM 每一步都会根据当前上下文输出整个词表中每个 token 的 logits。Logits 是未归一化分数，不能直接解释为概率。Softmax 函数会将 logits 转换成概率分布，然后模型根据某种解码策略选择下一个 token。

At each generation step, an LLM produces logits for all tokens in the vocabulary. Logits are unnormalized scores, not probabilities. The softmax function converts them into a probability distribution, and a decoding strategy selects the next token.

### 6.1 Softmax

给定词表中第 i 个 token 的 logit 为 \(z_i\)，softmax 概率为：

Given the logit \(z_i\) for token \(i\), the softmax probability is:

$$
P(w_i \mid context) = \frac{\exp(z_i)}{\sum_{j=1}^{|V|}\exp(z_j)}
$$

其中 \(|V|\) 是词表大小。Softmax 会放大高 logit token 的概率，同时保证所有 token 的概率和为 1。

Here, \(|V|\) is the vocabulary size. Softmax emphasizes tokens with higher logits and ensures that all token probabilities sum to 1.

### 6.2 Temperature Softmax

Temperature 用于控制概率分布的平滑程度：

Temperature controls how sharp or smooth the probability distribution is:

$$
P_T(w_i \mid context) = \frac{\exp(z_i / T)}{\sum_{j=1}^{|V|}\exp(z_j / T)}
$$

| Temperature | 效果 / Effect | 适用场景 / Use Cases |
|---|---|---|
| \(T \to 0\) | 分布极尖锐，接近 greedy decoding | 事实问答、信息抽取、代码修复 |
| \(T = 1\) | 使用原始 softmax 分布 | 一般生成任务 |
| \(T > 1\) | 分布更平滑，随机性更高 | 创意写作、开放式改写 |

低 temperature 更稳定，但可能重复或保守；高 temperature 更多样，但更容易偏离事实或产生不连贯内容。

Lower temperature produces more stable but sometimes repetitive outputs. Higher temperature increases diversity but may reduce factuality and coherence.

### 6.3 常见解码策略 / Common Decoding Strategies

| 解码策略 / Strategy | 说明 / Description | 优点 / Strength | 风险 / Risk |
|---|---|---|---|
| Greedy decoding | 每次选择概率最高的 token | 稳定、确定性强 | 容易重复，缺少多样性 |
| Random sampling | 按概率分布随机采样 | 多样性更高 | 可能采到低质量 token |
| Temperature sampling | 调整分布后采样 | 可控制稳定性与创造性 | 参数不合适会影响质量 |
| Top-k sampling | 只在概率最高的 k 个 token 中采样 | 排除低概率 token | k 过小会限制表达 |
| Top-p sampling | 在累计概率达到 p 的 token 集合中采样 | 自适应控制候选集合 | p 过大仍可能发散 |

## 7. Training LLMs / 大语言模型训练

LLM 通常经历三个主要阶段：pretraining、instruction tuning 和 alignment。

LLMs are typically trained in three major stages: pretraining, instruction tuning, and alignment.

### 7.1 Pretraining

Pretraining 使用大规模文本进行自监督学习，目标是 next-token prediction。训练样本来自普通文本，不需要人工标注。

Pretraining uses large-scale text for self-supervised learning. The objective is next-token prediction, and the data does not require manual labels.

给定 token 序列 \(w_1, w_2, ..., w_n\)，自回归语言模型将联合概率分解为：

Given a token sequence \(w_1, w_2, ..., w_n\), an autoregressive language model factorizes the joint probability as:

$$
P(w_1, w_2, ..., w_n) = \prod_{i=1}^{n} P(w_i \mid w_1, ..., w_{i-1})
$$

这与 N-gram 模型使用的链式法则一致，但 LLM 使用神经网络估计条件概率，可以利用更长上下文和更复杂的语义模式。

This is the same chain rule used by N-gram language models, but LLMs estimate the conditional probabilities with neural networks, allowing them to use longer contexts and richer semantic patterns.

### 7.2 Cross-entropy Loss

预训练的常见损失函数是 cross-entropy loss。对于某一步预测，如果真实下一个 token 是 \(y\)，模型给它的概率是 \(P(y \mid context)\)，则损失为：

The common loss function for pretraining is cross-entropy loss. If the true next token is \(y\), and the model assigns probability \(P(y \mid context)\), the loss is:

$$
\mathcal{L} = -\log P(y \mid context)
$$

对于整个序列，平均 cross-entropy 可以写为：

For a whole sequence, the average cross-entropy can be written as:

$$
\mathcal{L}_{CE} = -\frac{1}{N}\sum_{i=1}^{N}\log P(w_i \mid w_1, ..., w_{i-1})
$$

如果模型给真实 token 的概率越高，loss 越低；如果真实 token 的概率越低，loss 越高。训练过程就是不断调整参数，使真实 token 的概率更高。

The higher the probability assigned to the true token, the lower the loss. Training adjusts model parameters so that the true next token receives higher probability.

### 7.3 Instruction Tuning

Instruction tuning 使用“指令-回答”格式的数据继续训练模型，使模型更擅长理解和遵循人类任务要求。

Instruction tuning further trains the model on instruction-response data so that it becomes better at understanding and following human instructions.

例如，预训练模型可能只会自然地续写文本，而 instruction-tuned 模型更倾向于按要求回答问题、总结文本、生成结构化结果或遵守格式约束。

For example, a pretrained model may simply continue text, while an instruction-tuned model is more likely to answer questions, summarize documents, generate structured outputs, and follow formatting constraints.

### 7.4 Alignment

Alignment 的目标是让模型输出更有帮助、更安全、更符合人类偏好。常见方法包括 RLHF（Reinforcement Learning from Human Feedback）、RLAIF（Reinforcement Learning from AI Feedback）和 DPO（Direct Preference Optimization）等。

The goal of alignment is to make model outputs more helpful, safer, and better aligned with human preferences. Common methods include RLHF, RLAIF, and DPO.

需要注意的是，alignment 不能从根本上消除 hallucination。它可以改善模型行为，但事实性仍然需要外部知识、检索证据、工具校验或结构化约束来增强。

Alignment cannot completely eliminate hallucination. It improves model behavior, but factuality still often requires external knowledge, retrieved evidence, tool verification, or structured constraints.

## 8. Evaluating LLMs / 大语言模型评价

### 8.1 Perplexity

Perplexity 是语言模型评价中的经典指标，用于衡量模型预测测试文本的能力。它可以看作模型在每一步预测时的“平均困惑程度”。

Perplexity is a classic metric for language modeling. It measures how well a model predicts a test sequence and can be interpreted as the model's average uncertainty at each prediction step.

如果平均 cross-entropy 为 \(\mathcal{L}_{CE}\)，则 perplexity 为：

If the average cross-entropy is \(\mathcal{L}_{CE}\), perplexity is:

$$
PPL = \exp(\mathcal{L}_{CE})
$$

等价地，对于长度为 \(N\) 的 token 序列：

Equivalently, for a token sequence of length \(N\):

$$
PPL = \exp\left(-\frac{1}{N}\sum_{i=1}^{N}\log P(w_i \mid w_1, ..., w_{i-1})\right)
$$

Perplexity 越低，说明模型越擅长预测该测试集中的 token。但 perplexity 不等于事实准确率，也不能直接代表推理能力或指令遵循能力。

Lower perplexity means the model predicts the test tokens better. However, perplexity is not the same as factual accuracy, reasoning ability, or instruction-following performance.

### 8.2 下游任务评价 / Downstream Evaluation

实际应用中，还需要针对具体任务进行评价：

In real applications, task-specific evaluation is also necessary:

| 任务 / Task | 常见指标 / Metrics |
|---|---|
| 问答 / QA | Accuracy, Exact Match, F1 |
| 分类 / Classification | Accuracy, Precision, Recall, F1 |
| 翻译 / Translation | BLEU, COMET, human evaluation |
| 摘要 / Summarization | ROUGE, factual consistency, human evaluation |
| 信息抽取 / Information extraction | Entity-level F1, relation-level F1 |
| 指令遵循 / Instruction following | Format accuracy, preference evaluation |

对于 KG-RAG 或 GraphRAG，评价不能只看最终答案，还需要检查证据和推理路径：

For KG-RAG or GraphRAG, evaluation should not only inspect the final answer, but also the evidence and reasoning path:

- **Evidence coverage**：检索到的证据是否覆盖回答所需事实。
- **Faithfulness**：回答是否忠实于证据，而不是自由编造。
- **Entity linking accuracy**：文本实体是否正确链接到知识图谱节点。
- **Path correctness**：图上的关系路径是否正确。
- **Multi-hop reasoning success rate**：多跳问题是否被正确分解并推理。

## 9. Safety Issues / 安全问题

LLM 不能被简单看作事实数据库。它们生成的是高概率文本，而不是经过验证的事实。

LLMs should not be treated as factual databases. They generate high-probability text, not necessarily verified facts.

| 安全问题 / Issue | 说明 / Explanation |
|---|---|
| Hallucination | 生成无依据或事实错误的内容 |
| Unsafe instructions | 可能响应有害、违法或危险请求 |
| Bias | 训练数据中的社会偏见可能被模型继承或放大 |
| Privacy leakage | 可能泄露训练数据、用户数据或敏感信息 |
| Misinformation | 可能生成误导性或虚假信息 |
| Copyright risk | 可能复现或模仿受版权保护内容 |

RAG 可以通过外部文档检索为回答提供证据。KG-RAG 进一步引入实体、关系和图结构约束。GraphRAG 则强调将知识组织为图结构，以支持多跳推理、社区摘要和更强的可解释性。

RAG provides external evidence through document retrieval. KG-RAG further adds entity, relation, and graph constraints. GraphRAG organizes knowledge as graph structures to support multi-hop reasoning, community summaries, and stronger interpretability.

## 10. 对研究方向的意义 / Relevance to My Research

本章为“知识图谱增强的大模型推理”提供了基础框架。LLM 负责语言理解、任务泛化和自然语言生成；RAG 负责外部知识检索；KG 负责结构化事实约束；GraphRAG 负责图结构组织和多跳推理。

This chapter provides a foundation for knowledge-graph-enhanced LLM reasoning. The LLM handles language understanding, task generalization, and natural-language generation. RAG retrieves external knowledge. The knowledge graph provides structured factual constraints. GraphRAG organizes knowledge as graph structures for multi-hop reasoning.

一个可靠的 KG-RAG / GraphRAG 系统不能只依赖 LLM 的生成能力，而应结合以下机制：

A reliable KG-RAG / GraphRAG system should not rely only on the generative ability of the LLM. It should combine:

- 检索证据 / retrieved evidence
- 实体链接 / entity linking
- 关系约束 / relation constraints
- 图路径推理 / graph-path reasoning
- 结构化输出校验 / structured output validation
- 答案与证据一致性检查 / answer-evidence consistency checking

因此，本章的关键启发是：LLM 是强大的语言接口和生成器，但可靠推理系统需要把 LLM 与检索、知识图谱和验证机制结合起来。

The key insight is that an LLM is a powerful language interface and generator, but reliable reasoning systems require integration with retrieval, knowledge graphs, and verification mechanisms.

## 11. 重点总结 / Key Takeaways

- LLM 的核心任务是根据上下文预测下一个 token。
- Many NLP tasks can be reformulated as conditional generation.
- Encoder、decoder 和 encoder-decoder 架构适合不同类型的任务。
- Prompting 通过指令、模板和示例引导模型输出。
- In-context learning 不更新模型参数，只利用 prompt 中的信息。
- Softmax 将 logits 转换为概率分布。
- Temperature 控制生成的稳定性与多样性。
- Cross-entropy loss 训练模型提高真实 token 的预测概率。
- Perplexity 衡量语言建模能力，但不能代表事实准确率或推理能力。
- LLM 存在 hallucination、bias、privacy leakage 等安全问题。
- KG-RAG 和 GraphRAG 可以通过外部证据、结构化事实和图推理增强 LLM 的可靠性。

## 12. 导师可能提问 / Possible Oral Exam Questions

**Q1: What is the basic objective of an LLM?**

LLM 的基本目标是在给定上下文的条件下预测下一个 token。通过不断预测和采样，模型可以生成完整文本。

The basic objective is to predict the next token given the previous context. By repeatedly predicting and sampling tokens, the model generates full text.

**Q2: What is the difference between in-context learning and fine-tuning?**

In-context learning 只利用 prompt 中的示例或上下文，不更新模型参数；fine-tuning 会在训练数据上继续优化模型参数。

In-context learning uses examples or context inside the prompt without updating model parameters. Fine-tuning continues training the model and updates its parameters.

**Q3: Why does temperature affect generation?**

Temperature 会改变 softmax 分布的尖锐程度。低 temperature 让高概率 token 更突出，输出更稳定；高 temperature 让分布更平滑，输出更多样但风险更高。

Temperature changes the sharpness of the softmax distribution. Lower temperature emphasizes high-probability tokens and makes outputs more stable. Higher temperature smooths the distribution and increases diversity, but also increases risk.

**Q4: Why is perplexity not enough to evaluate an LLM?**

Perplexity 只衡量模型预测测试文本 token 的能力，不能直接评价事实准确性、推理能力、安全性或指令遵循能力。

Perplexity only measures how well the model predicts tokens in a test set. It does not directly evaluate factual accuracy, reasoning ability, safety, or instruction following.

**Q5: Why can KG-RAG improve LLM reliability?**

KG-RAG 将 LLM 的语言生成能力与知识图谱的结构化事实约束结合起来，可以减少幻觉，提高证据可追溯性，并支持多跳关系推理。

KG-RAG combines the generative ability of LLMs with structured factual constraints from knowledge graphs. This can reduce hallucination, improve evidence traceability, and support multi-hop relational reasoning.
