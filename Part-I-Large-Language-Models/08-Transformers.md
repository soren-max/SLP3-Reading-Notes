---
note_title: "Transformers：LLM、Attention 与 KG-RAG 上下文融合机制"
source: "Speech and Language Processing, Third Edition draft"
chapter: "Chapter 8: Transformers"
section: "Full Chapter"
priority: "High"
status: "Reading"
tags:
  - LLM
  - Transformer
  - Attention
  - RAG
  - KG
  - GraphRAG
  - LoRA
  - KVCache
research_direction: "KG-enhanced LLM Reasoning"
---

# Chapter 8: Transformers

## 1. 章节定位 / Chapter Focus

本章介绍 Transformer 架构。Transformer 是现代大语言模型的核心结构，尤其是 GPT 类 decoder-only language model。它通过 self-attention、multi-head attention、feedforward network、residual connection 和 layer normalization，把输入 token 转换成上下文相关的 hidden representations，并用于预测下一个 token。

This chapter introduces the Transformer architecture. Transformers are the core architecture of modern LLMs, especially GPT-style decoder-only language models. Through self-attention, multi-head attention, feedforward networks, residual connections, and layer normalization, a Transformer converts input tokens into contextual hidden representations and uses them to predict the next token.

对 KG-RAG 和 GraphRAG 来说，Transformer 解释了 LLM 如何读取 prompt 中的问题、文档证据、知识图谱路径和输出约束，并将这些信息融合成最终答案。

For KG-RAG and GraphRAG, the Transformer explains how an LLM reads questions, retrieved evidence, knowledge graph paths, and output constraints in the prompt, then integrates them into a final answer.

## 2. 核心概念 / Key Concepts

- **Transformer**：基于 attention 的神经网络架构，是现代 LLM 的基础。
- **Self-attention（自注意力）**：每个 token 根据上下文中其他 token 的信息更新自己的表示。
- **Query, Key, Value, QKV**：attention 中用于匹配和信息汇总的三组向量。
- **Scaled dot-product attention**：用 query 和 key 的点积计算注意力分数，并除以 \(\sqrt{d_k}\) 稳定数值。
- **Multi-head attention（多头注意力）**：多个 attention head 并行学习不同关系。
- **Feedforward network, FFN（前馈网络）**：对每个 token 位置独立进行非线性变换。
- **Residual connection（残差连接）**：将子层输出加回原表示，帮助深层网络训练。
- **Layer normalization（层归一化）**：稳定训练，使每层表示分布更可控。
- **Positional embedding（位置嵌入）**：为模型提供 token 顺序信息。
- **Causal mask（因果掩码）**：decoder-only 模型中防止当前位置看到未来 token。
- **KV cache**：推理时缓存历史 token 的 keys 和 values，减少重复计算。
- **LoRA**：低秩适配方法，冻结原模型权重，只训练小规模低秩更新矩阵。

## 3. Transformer 输入：Token 与位置

输入文本首先经过 tokenizer，变成 token IDs。模型从 embedding matrix \(E\) 中查表得到 token embeddings：

Input text is first converted into token IDs by a tokenizer. The model then looks up token embeddings from the embedding matrix \(E\):

$$
x_i = E[t_i]
$$

其中 \(t_i\) 是第 \(i\) 个 token 的 ID，\(x_i\) 是对应的向量表示。

Here, \(t_i\) is the ID of the \(i\)-th token, and \(x_i\) is its vector representation.

Self-attention 本身不包含顺序信息，因此模型还需要 positional embedding：

Self-attention itself has no built-in order information, so the model also needs positional embeddings:

$$
h_i^{(0)} = x_i + p_i
$$

其中 \(p_i\) 表示第 \(i\) 个位置的位置向量。这样模型才能区分 `dog bites man` 和 `man bites dog` 这类词相同但顺序不同的句子。

Here, \(p_i\) is the positional vector for position \(i\). This allows the model to distinguish sentences with the same words but different orders, such as `dog bites man` and `man bites dog`.

## 4. Self-Attention / 自注意力

Self-attention 的目标是为每个 token 构建 contextual representation。一个 token 的含义不是固定的，而是依赖上下文。例如 `bank` 在 `river bank` 中表示河岸，在 `bank account` 中表示银行。

The goal of self-attention is to build a contextual representation for each token. A token's meaning is not fixed; it depends on context. For example, `bank` means a river side in `river bank`, but a financial institution in `bank account`.

Attention 可以理解为对上下文 token 的加权求和。当前 token 通过 query 与上下文 token 的 key 计算相似度，再用 softmax 得到 attention weights，最后对 value 加权汇总。

Attention can be understood as a weighted sum over context tokens. The current token uses its query to compare with the keys of context tokens, applies softmax to obtain attention weights, and then aggregates the values.

## 5. QKV 机制 / Query, Key, Value

Transformer 使用三个矩阵将输入 hidden state 投影成 query、key 和 value：

A Transformer uses three learned matrices to project hidden states into queries, keys, and values:

$$
q_i = h_iW_Q,\quad k_i = h_iW_K,\quad v_i = h_iW_V
$$

直觉上：

Intuitively:

- **Query** 表示当前 token 想找什么信息 / what the current token is looking for.
- **Key** 表示上下文 token 可被匹配的索引 / what each context token can be matched by.
- **Value** 表示上下文 token 真正贡献的信息 / the information each context token contributes.

第 \(i\) 个 token 对第 \(j\) 个 token 的 attention score 为：

The attention score from token \(i\) to token \(j\) is:

$$
score(i,j) = \frac{q_i \cdot k_j}{\sqrt{d_k}}
$$

其中 \(d_k\) 是 key/query 向量维度。除以 \(\sqrt{d_k}\) 可以防止点积随维度增大而过大，从而避免 softmax 过度饱和。

Here, \(d_k\) is the dimension of keys and queries. Dividing by \(\sqrt{d_k}\) prevents dot products from becoming too large as dimensionality grows, which keeps the softmax from becoming overly saturated.

## 6. Attention Softmax

Attention score 经过 softmax 转换成权重：

Attention scores are converted into weights with softmax:

$$
\alpha_{ij} = \frac{\exp(score(i,j))}{\sum_{m=1}^{n}\exp(score(i,m))}
$$

然后对 value 加权求和：

The output is then a weighted sum of values:

$$
z_i = \sum_{j=1}^{n}\alpha_{ij}v_j
$$

矩阵形式的 scaled dot-product attention 为：

The matrix form of scaled dot-product attention is:

$$
Attention(Q,K,V) = softmax\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

在 decoder-only LLM 中，还需要 causal mask，使第 \(i\) 个位置只能关注 \(\leq i\) 的 token，不能看到未来 token。

In decoder-only LLMs, a causal mask is also applied so that position \(i\) can only attend to tokens at positions \(\leq i\), not future tokens.

## 7. Multi-Head Attention / 多头注意力

Multi-head attention 使用多个 attention heads 并行建模上下文。不同 head 可以学习不同语言关系，例如实体指代、语法依存、关系触发词、局部搭配和长距离依赖。

Multi-head attention uses multiple attention heads in parallel. Different heads can learn different linguistic relations, such as coreference, syntactic dependency, relation triggers, local collocations, and long-distance dependencies.

每个 head 独立计算 attention：

Each head computes attention independently:

$$
head_r = Attention(QW_Q^{(r)}, KW_K^{(r)}, VW_V^{(r)})
$$

多个 head 的输出拼接后，再通过输出矩阵 \(W_O\) 投影回模型维度：

The outputs of multiple heads are concatenated and projected back to the model dimension with \(W_O\):

$$
MultiHead(Q,K,V) = Concat(head_1, ..., head_H)W_O
$$

这种机制让模型在同一层中从多个角度读取上下文，而不是只学习一种注意力模式。

This mechanism allows the model to read context from multiple perspectives in the same layer, instead of learning only one attention pattern.

## 8. Transformer Block

一个 Transformer block 通常包含 multi-head attention、feedforward network、residual connection 和 layer normalization。

A Transformer block usually contains multi-head attention, a feedforward network, residual connections, and layer normalization.

简化结构如下：

Simplified structure:

```text
Input hidden states
-> LayerNorm
-> Multi-head self-attention
-> Residual add
-> LayerNorm
-> Feedforward network
-> Residual add
-> Output hidden states
```

Residual stream 可以理解为每个 token 位置的信息通道。Attention 和 FFN 不断向这个通道添加信息，使 token 表示逐层变得更加丰富。

The residual stream can be understood as the information channel at each token position. Attention and FFN repeatedly add information to this channel, making token representations richer layer by layer.

### 8.1 Feedforward Network

FFN 对每个 token 位置独立应用同一个小型神经网络：

The FFN applies the same small neural network independently to each token position:

$$
FFN(x) = W_2 f(W_1x + b_1) + b_2
$$

其中 \(f\) 通常是 ReLU、GELU 或其他非线性激活函数。Attention 负责在 token 之间传递信息，FFN 负责对每个位置的表示做非线性变换。

Here, \(f\) is usually ReLU, GELU, or another nonlinear activation function. Attention moves information across tokens, while the FFN applies nonlinear transformation to each token representation.

### 8.2 Residual Connection and Layer Normalization

Residual connection 将子层输出加回输入：

A residual connection adds the sublayer output back to its input:

$$
y = x + Sublayer(x)
$$

Layer normalization 稳定每层表示：

Layer normalization stabilizes representations at each layer:

$$
LayerNorm(x) = \gamma \frac{x-\mu}{\sqrt{\sigma^2+\epsilon}} + \beta
$$

它们共同帮助深层 Transformer 更稳定地训练和推理。

Together, these mechanisms help deep Transformers train and infer more stably.

## 9. Language Modeling Head

最后一层 Transformer 输出每个位置的 hidden state。Language modeling head 将 hidden state 映射到词表大小的 logits：

The final Transformer layer outputs a hidden state at each position. The language modeling head maps the hidden state to vocabulary-sized logits:

$$
logits_i = h_iW_{vocab} + b
$$

然后通过 softmax 得到下一个 token 的概率分布：

Softmax then converts logits into the probability distribution for the next token:

$$
P(w_{i+1}=v \mid w_{\leq i}) = \frac{\exp(logit_v)}{\sum_{u \in V}\exp(logit_u)}
$$

Decoder-only LLM 就是基于这种方式逐 token 生成文本。

A decoder-only LLM generates text token by token in this way.

## 10. Training Objective: Cross-Entropy and Perplexity

Transformer language model 的训练目标仍然是 next-token prediction。给定真实下一个 token \(y\)，cross-entropy loss 为：

The training objective of a Transformer language model is still next-token prediction. Given the true next token \(y\), the cross-entropy loss is:

$$
\mathcal{L} = -\log P(y \mid context)
$$

对长度为 \(N\) 的序列，平均 loss 为：

For a sequence of length \(N\), the average loss is:

$$
\mathcal{L}_{CE} = -\frac{1}{N}\sum_{i=1}^{N}\log P(w_i \mid w_{<i})
$$

Perplexity 用于衡量语言建模能力：

Perplexity measures language modeling quality:

$$
PPL = \exp(\mathcal{L}_{CE})
$$

Perplexity 越低，表示模型越擅长预测测试文本。但它不能直接代表事实准确率、推理能力或 KG-RAG 的证据忠实性。

Lower perplexity means the model predicts the test text better. However, it does not directly measure factual accuracy, reasoning ability, or faithfulness to KG-RAG evidence.

## 11. Decoding and Sampling / 解码与采样

生成时，模型会从下一个 token 的概率分布中选择 token。常见策略包括 greedy decoding、temperature sampling、top-k sampling 和 top-p sampling。

During generation, the model selects tokens from the next-token probability distribution. Common strategies include greedy decoding, temperature sampling, top-k sampling, and top-p sampling.

| 策略 / Strategy | 说明 / Description | 适用场景 / Use Case |
|---|---|---|
| Greedy decoding | 每次选择概率最高的 token | 稳定任务、格式化输出 |
| Temperature sampling | 调整概率分布尖锐程度 | 控制稳定性与创造性 |
| Top-k sampling | 只从概率最高的 k 个 token 中采样 | 限制低质量候选 |
| Top-p sampling | 从累计概率达到 p 的候选集合中采样 | 自适应控制候选范围 |

事实问答、信息抽取和 KG-RAG 通常更适合低随机性设置，因为这类任务重视稳定性、证据一致性和可复现性。

Factual QA, information extraction, and KG-RAG usually benefit from lower randomness, because they prioritize stability, evidence consistency, and reproducibility.

## 12. Scale, KV Cache, and LoRA

### 12.1 Scale

大模型性能通常受模型规模、数据规模和计算量共同影响。更大的模型和更多数据可以提升能力，但也会增加训练成本、推理成本和部署复杂度。

Large model performance is often affected by model size, data size, and compute. Larger models and more data can improve capability, but they also increase training cost, inference cost, and deployment complexity.

### 12.2 KV Cache

在自回归生成中，模型每一步只新增一个 token。如果每一步都重新计算所有历史 token 的 keys 和 values，会造成大量重复计算。KV cache 会缓存历史 token 的 \(K\) 和 \(V\)，下一步只需要计算新 token 的 \(K\)、\(V\) 和 \(Q\)。

In autoregressive generation, the model adds one token at a time. Recomputing keys and values for all previous tokens at every step would waste computation. KV cache stores the \(K\) and \(V\) of past tokens, so the next step only needs to compute \(K\), \(V\), and \(Q\) for the new token.

KV cache 能显著降低长文本生成的延迟，但会占用额外显存，尤其在长上下文和大 batch 推理时更明显。

KV cache significantly reduces generation latency for long texts, but it consumes extra GPU memory, especially for long contexts and large batches.

### 12.3 LoRA

LoRA（Low-Rank Adaptation）是一种参数高效微调方法。它冻结原始权重矩阵 \(W\)，只训练低秩更新矩阵：

LoRA (Low-Rank Adaptation) is a parameter-efficient fine-tuning method. It freezes the original weight matrix \(W\) and trains only low-rank update matrices:

$$
W' = W + \Delta W,\quad \Delta W = BA
$$

其中 \(A \in \mathbb{R}^{r \times d}\)，\(B \in \mathbb{R}^{d \times r}\)，且 \(r \ll d\)。因此需要训练的参数远少于全量微调。

Here, \(A \in \mathbb{R}^{r \times d}\), \(B \in \mathbb{R}^{d \times r}\), and \(r \ll d\). Therefore, the number of trainable parameters is much smaller than full fine-tuning.

LoRA 适合领域适配，例如医学、法律、金融或企业内部 KG-RAG 场景。但它不能替代可靠检索和事实验证。

LoRA is useful for domain adaptation, such as biomedical, legal, financial, or internal enterprise KG-RAG scenarios. However, it does not replace reliable retrieval and factual verification.

## 13. Encoder, Decoder, and Encoder-Decoder Transformers

Transformer 可以构建 encoder-only、decoder-only 和 encoder-decoder 模型。

Transformers can be used to build encoder-only, decoder-only, and encoder-decoder models.

| 架构 / Architecture | Attention 方式 / Attention Pattern | 代表模型 / Examples | 典型用途 / Use Cases |
|---|---|---|---|
| Encoder-only | 双向 attention | BERT, RoBERTa | 分类、检索、NER、embedding |
| Decoder-only | causal self-attention | GPT, Claude, Llama | 文本生成、对话、代码、agent |
| Encoder-decoder | encoder 双向 + decoder causal | T5, BART | 翻译、摘要、输入输出转换 |

GPT 类 LLM 使用 decoder-only Transformer。它们通过 causal mask 保证生成时每个位置只依赖过去 token。

GPT-style LLMs use decoder-only Transformers. A causal mask ensures that each position only depends on previous tokens during generation.

## 14. 对 KG-RAG / GraphRAG 的意义

Transformer 负责把 prompt 中的自然语言问题、文档证据、KG triples、图路径和输出约束融合成上下文表示，并据此生成答案。

The Transformer integrates natural-language questions, retrieved documents, KG triples, graph paths, and output constraints in the prompt into contextual representations, then generates an answer.

在 KG-RAG 中，Transformer 的作用包括：

In KG-RAG, the Transformer helps with:

- 理解用户问题 / understanding the user question
- 融合检索证据 / integrating retrieved evidence
- 读取知识图谱路径 / reading knowledge graph paths
- 生成自然语言答案 / generating natural-language answers
- 按指定格式输出 / following output format constraints

但 Transformer 本身不能保证事实正确。它的训练目标是生成高概率 token，而不是验证事实。因此可靠系统需要把 Transformer 的语言建模能力与知识图谱的显式实体、关系、路径和证据校验结合起来。

However, a Transformer alone cannot guarantee factual correctness. Its training objective is to generate high-probability tokens, not to verify facts. Therefore, reliable systems need to combine Transformer language modeling with explicit entities, relations, paths, and evidence validation from knowledge graphs.

## 15. 重点总结 / Key Takeaways

- Transformer 是现代 LLM 的核心架构。
- Self-attention 为每个 token 构建 contextual representation。
- QKV 机制将匹配问题和信息汇总分开建模。
- Scaled dot-product attention 使用 \(\frac{QK^T}{\sqrt{d_k}}\) 计算注意力分数。
- Multi-head attention 让模型并行学习多种上下文关系。
- Positional embedding 为 self-attention 提供顺序信息。
- Decoder-only LLM 使用 causal mask 防止看到未来 token。
- Language modeling head 将 hidden state 映射为词表 logits。
- Cross-entropy 和 perplexity 仍然是语言建模训练与评价的核心公式。
- KV cache 降低自回归生成中的重复计算。
- LoRA 用低秩更新实现参数高效微调。
- KG-RAG 需要结合 Transformer 的上下文融合能力与 KG 的结构化事实约束。

## 16. 导师可能提问 / Possible Oral Exam Questions

**Q1: What problem does self-attention solve?**

Self-attention 让每个 token 根据上下文中其他 token 更新自己的表示，从而得到 contextual representation。

Self-attention allows each token to update its representation using information from other tokens in the context, producing contextual representations.

**Q2: What are query, key, and value?**

Query 表示当前 token 想找什么信息；key 表示上下文 token 可被匹配的索引；value 表示上下文 token 真正提供的信息。

The query represents what the current token is looking for; the key represents how a context token can be matched; the value represents the information contributed by that context token.

**Q3: Why divide attention scores by \(\sqrt{d_k}\)?**

因为 key/query 维度变大时，点积数值也会变大，导致 softmax 过于尖锐。除以 \(\sqrt{d_k}\) 可以稳定梯度和概率分布。

Because dot products grow larger as the key/query dimension increases, which can make softmax too sharp. Dividing by \(\sqrt{d_k}\) stabilizes gradients and probability distributions.

**Q4: Why does Transformer need positional embeddings?**

Self-attention 本身不包含顺序信息。如果没有 positional embeddings，模型难以区分相同词集合的不同顺序。

Self-attention has no built-in order information. Without positional embeddings, the model would struggle to distinguish different orders of the same words.

**Q5: What is KV cache used for?**

KV cache 在推理时缓存历史 token 的 keys 和 values，避免每一步重复计算完整历史，从而降低生成延迟。

KV cache stores keys and values of previous tokens during inference, avoiding repeated computation over the full history and reducing generation latency.

**Q6: What is LoRA and why is it useful?**

LoRA 冻结原模型权重，只训练低秩更新矩阵，因此能用较少参数完成领域适配。

LoRA freezes the original model weights and trains only low-rank update matrices, enabling domain adaptation with far fewer trainable parameters.

**Q7: Why is Transformer alone not enough for reliable KG-RAG?**

Transformer 擅长上下文融合和生成，但不能保证事实正确。KG-RAG 需要知识图谱实体、关系、路径和证据校验来增强可靠性。

Transformers are strong at context integration and generation, but they do not guarantee factual correctness. KG-RAG needs graph entities, relations, paths, and evidence validation to improve reliability.
