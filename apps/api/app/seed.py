from datetime import date

from app.database import Base, SessionLocal, engine, init_db
from app.models.chapter import Chapter
from app.models.intern import InternRecord
from app.models.note import Note
from app.models.source import Source


def chapter(
    number: int,
    title: str,
    priority: str,
    mastery: str,
    relevance_score: int,
    relation: str,
    tags: list[str],
    status: str = "未开始",
    **details: object,
) -> dict:
    concepts = tags[:4] + ["Reading Notes"]
    data = {
        "source_id": 1,
        "number": number,
        "title": title,
        "priority": priority,
        "status": status,
        "mastery": mastery,
        "relevance_score": relevance_score,
        "research_relation": relation,
        "positioning": f"第 {number} 章用于支撑 KG-LLM 阅读路线中关于 {', '.join(tags[:3])} 的知识模块。",
        "core_concepts": concepts,
        "outline": "按概念定义、模型假设、训练/推理流程、典型例子、与研究方向的连接五个层次梳理。",
        "formulas_algorithms": "记录关键公式、目标函数、解码或检索算法，并补充变量含义与适用边界。",
        "examples": "为每个核心概念补一个面向 KG-RAG 或 GraphRAG 的文本例子，说明输入、输出和中间表示。",
        "summary": "提炼本章最应掌握的概念、容易混淆的点，以及可迁移到研究实验中的方法。",
        "mentor_questions": [
            "本章方法解决 NLP 流水线中的哪一类问题？",
            "它如何服务 KG-RAG、GraphRAG 或多跳推理？",
            "如果放到研究实验里，输入输出和评价指标是什么？",
        ],
        "research_links": relation,
        "resources": [
            "Speech and Language Processing, Third Edition draft",
            "相关论文与课程笔记后续补充",
        ],
        "tags": tags,
    }
    data.update(details)
    return data


CHAPTER_3_NOTE = r"""# Chapter 3: N-gram Language Models

> 第二优先级章节：理解即可，不做深度推导。

## 章节定位

本章使用最简单的统计语言模型 n-gram，引出语言建模中的核心问题：如何根据上下文预测下一个 token、如何为句子分配概率、如何评价模型，以及如何处理训练语料中未出现的序列。现代 LLM 虽然使用 Transformer 代替计数表，但仍然延续了 next-token prediction 的基本任务。

## 核心概念

- **Language Model**：输入上下文，输出下一个 token 的概率分布。
- **N-gram**：由连续 n 个 token 构成的序列。n-gram 模型只使用前面 n-1 个 token 预测当前 token。
- **Markov Assumption**：用最近的少量 token 近似完整历史，使概率能够通过有限语料进行估计。
- **MLE**：通过语料中的相对频率估计概率。以 bigram 为例：

  \[
  P(w_t \mid w_{t-1}) = \frac{C(w_{t-1}, w_t)}{C(w_{t-1})}
  \]

- **Perplexity**：评价模型在测试集上的预测能力，通常越低表示模型对真实 token 的预测越准确。
- **Smoothing**：为训练集中未见过的序列分配非零概率，避免一句话中某一步概率为零后整个句子概率变为零。

## 方法直觉

句子概率可以通过概率链式法则拆成每个 token 的条件概率：

\[
P(w_{1:T}) = \prod_{t=1}^{T} P(w_t \mid w_{1:t-1})
\]

但完整历史很难统计，因此 n-gram 只保留最近的固定窗口：

\[
P(w_t \mid w_{1:t-1}) \approx P(w_t \mid w_{t-m+1:t-1})
\]

窗口越大，局部信息越丰富，但数据稀疏和存储问题也越严重。

## 关键公式

困惑度：

\[
PP(W) = P(w_{1:T})^{-1/T}
\]

模型给测试文本的概率越高，perplexity 越低。不同模型只有在相同测试集、词表和分词条件下才适合直接比较。

Laplace smoothing：

\[
P(w_t \mid w_{t-1}) = \frac{C(w_{t-1}, w_t) + 1}{C(w_{t-1}) + V}
\]

其目的是消除零概率，但 add-one 往往会向未见事件分配过多概率，因此主要作为理解平滑思想的基础。

## 简单例子

训练集中包含：

```text
查询 华为 创始人
查询 华为 总部
```

trigram 模型在看到“查询 华为”时，可以根据计数预测“创始人”或“总部”。若“查询 华为 CEO”没有出现，MLE 会给它概率 0，平滑后则会获得较小的非零概率。

## 优点与局限

优点是简单、可解释、训练快，适合学习概率语言模型的基础。局限是只能使用短上下文、数据稀疏严重、无法学习语义相似性，也无法进行长距离依赖建模和多跳推理。

Interpolation 可以组合 unigram、bigram 和 trigram：高阶模型提供具体上下文，低阶模型则在数据稀疏时提供更稳定的估计。

## 与 KG-LLM 方向的联系

n-gram 与现代 LLM 都预测下一个 token，但 LLM 使用 Transformer 学习长上下文和连续语义表示。n-gram 只能学习“华为—创始人”等表面共现，不能建立“华为—创始人—任正非”这样的结构化三元组，也不能完成知识检索、证据验证或多跳推理。

对 KG-RAG 而言，本章最重要的价值是理解生成模型的概率基础。KG-RAG 则在语言生成之外进一步加入图谱检索、实体链接、关系约束和推理路径。

## 导师可能提问

**Q1：为什么 n-gram 只使用有限上下文？**

为了缓解完整历史组合过多造成的数据稀疏问题。

**Q2：为什么需要 smoothing？**

因为未见 n-gram 的 MLE 概率为 0，会导致整个句子概率为 0。

**Q3：n-gram 与 LLM 的核心区别是什么？**

n-gram 依靠固定窗口计数，LLM 依靠神经网络学习长上下文和语义表示。

## 一句话总结

n-gram 是基于局部共现计数的经典语言模型，其主要价值是帮助理解 next-token prediction、perplexity、smoothing 以及现代 LLM 的概率建模基础。
"""


CHAPTER_4_NOTE = r"""# Chapter 4: Logistic Regression

## 章节定位

逻辑回归是经典的监督分类模型，也是理解神经网络分类器和 LLM 输出层的重要基础。本章建立了核心机器学习链路：

```text
输入特征 -> 线性打分 -> 概率 -> 损失 -> 参数更新
```

教材将概率分类器概括为输入表示、分类函数、目标函数和优化算法四个组成部分。

## 核心概念

- **Feature Representation**：把文本转换成数值向量。传统 NLP 使用词频、关键词、否定词和实体类型等人工特征。
- **Logit**：模型对某个类别给出的未归一化分数：

  \[
  z = w \cdot x + b
  \]

- **Sigmoid**：把一个实数映射到 0 到 1，用于二分类：

  \[
  P(y=1 \mid x) = \frac{1}{1+\exp(-(w \cdot x+b))}
  \]

- **Softmax**：把多个类别分数转换为总和为 1 的概率分布：

  \[
  P(y=k \mid x) = \frac{\exp(z_k)}{\sum_j \exp(z_j)}
  \]

- **Cross-Entropy**：衡量模型预测概率与真实标签的差异。

## 方法直觉

模型首先根据输入特征为各类别计算分数。一个特征的权重为正，表示它支持某个类别；权重为负，表示反对该类别。

二分类使用一个权重向量和 sigmoid。多分类为每个类别设置一组权重，组成矩阵 \(W\)，再通过 softmax 输出类别概率。

训练时，模型比较预测概率 \(\hat{y}\) 与真实标签 \(y\)。如果正确类别的概率太低，cross-entropy 就会增大；梯度下降再调整参数，使下一次正确类别的概率提高。

## 关键公式

二分类交叉熵：

\[
L = -[y\log \hat{y} + (1-y)\log(1-\hat{y})]
\]

多分类交叉熵：

\[
L = -\sum_{k=1}^{K} y_k \log \hat{y}_k
\]

对于 one-hot 标签，只有正确类别 \(c\) 对应的项不为零：

\[
L = -\log \hat{y}_c
\]

因此，cross-entropy 的直觉就是：提高正确类别的预测概率，惩罚自信的错误预测。

## 简单例子

对句子“乔布斯创立了苹果公司”进行关系分类。输入特征包括“是否包含创立”、实体类型是否为人物和组织、两个实体之间的距离等。模型为 `founder_of`、`works_for` 和 `located_in` 计算 logits，再通过 softmax 输出概率，最终选择概率最高的 `founder_of`。

## 优点与局限

优点是结构简单、训练快、能输出概率、权重具有一定可解释性，适合作为分类 baseline。

局限是本质上属于线性模型，效果依赖特征设计，难以自动理解复杂词序、语义组合、否定关系和长距离依赖。现代 NLP 因此使用 embedding 和神经网络自动学习表示。

## 与 KG-LLM 方向的联系

在知识图谱构建中，逻辑回归可以用于实体类型分类、关系分类和证据可信度判断。在 RAG 或 Agent 中，也可以用于查询路由和结果质量分类。

更重要的是，现代 LLM 同样通过线性层产生词表 logits，再使用 softmax 输出下一个 token 的概率，并通过 cross-entropy 训练。区别在于，LLM 的输入表示由 Transformer 自动学习，而不是人工设计。

## 导师可能提问

**Q1：sigmoid 和 softmax 有什么区别？**

sigmoid 常用于二分类；softmax 用于多个互斥类别，并保证类别概率之和为 1。

**Q2：cross-entropy 的直觉是什么？**

正确类别概率越低，损失越大；正确类别概率越接近 1，损失越小。

**Q3：逻辑回归与 Transformer 分类器有什么联系？**

Transformer 负责生成上下文表示，最后仍可通过线性层和 softmax 完成分类。

## 一句话总结

逻辑回归通过线性层、sigmoid/softmax 和 cross-entropy 完成概率分类，这套机制也是现代神经网络与 LLM 输出层的直接基础。
"""


CHAPTER_6_NOTE = r"""# Chapter 6: Neural Networks

## 章节定位

本章是从传统分类模型过渡到 Transformer 和 LLM 的基础章节。逻辑回归通常直接在人工特征上完成线性分类，而神经网络在输入和输出之间加入隐藏层，通过训练自动形成任务相关的内部表示。核心变化是从 feature engineering 转向 representation learning。

## 核心概念

- **Neural Unit**：先计算线性组合，再通过激活函数：

  \[
  z = w \cdot x + b,\quad a = g(z)
  \]

- **Feedforward Network**：信息从输入层依次流向隐藏层和输出层，网络中没有循环。
- **Hidden Representation**：隐藏层输出 \(h\) 是模型学习到的新表示。
- **Activation Function**：sigmoid、tanh、ReLU 等函数为网络引入非线性。
- **Backpropagation**：从最终损失开始，利用链式法则逐层计算参数梯度。

## 方法直觉

单隐藏层分类网络可以表示为：

\[
h = g(Wx+b)
\]

\[
z = Uh+c
\]

\[
\hat{y} = softmax(z)
\]

隐藏层先把原始输入变换到新的表示空间，输出层再基于该表示完成分类。神经网络可以看作在自动学习出的特征 \(h\) 上运行逻辑回归。

非线性激活至关重要。若每一层都只有线性变换，多层计算仍可合并为一个线性层，无法获得更强的表达能力。XOR 例子说明，隐藏层可以重新组织输入，使原本线性不可分的问题变得可分。

## 关键公式

前向传播：

\[
a^{[i]} = g^{[i]}(W^{[i]}a^{[i-1]} + b^{[i]})
\]

分类损失：

\[
L = -\sum_k y_k \log \hat{y}_k
\]

参数更新：

\[
W \leftarrow W - \eta \frac{\partial L}{\partial W}
\]

反向传播负责计算各层参数对最终损失的梯度。现阶段只需理解“前向算结果、反向算责任”，无需完整推导链式求导。

## 简单例子

对“任正非创立了华为”进行关系分类。模型先取得各 token 的 embedding，再通过隐藏层学习人物、组织和“创立”等信息的组合表示，最后通过 softmax 输出：

```text
founder_of   0.88
works_for    0.07
located_in   0.01
no_relation  0.04
```

预测结果可以转换为候选三元组：

```text
（任正非，founder_of，华为）
```

## 优点与局限

优点是能够自动学习特征、建模非线性关系并进行端到端训练。局限是需要较多数据和计算资源，训练过程不容易解释，且普通前馈网络无法自然处理长序列、图结构和显式多跳推理。

Pooling 可以把多个 token embedding 压缩为一个句子向量，效率较高但可能损失顺序；concatenation 能保留更多位置信息，但输入维度更大。

## 与 KG-LLM 方向的联系

Embedding 为 token、实体和关系提供初始向量，神经网络进一步把它们转换为任务相关表示。Transformer 和 LLM 仍然依赖线性层、非线性激活、多层表示与反向传播。

在知识图谱方向，神经网络可以用于实体链接、关系分类、三元组评分和证据排序；但普通 MLP 不直接理解图拓扑，也不能独立生成可解释的多跳路径。KG-RAG 需要将连续表示学习与实体关系、图检索和证据验证结合起来。

## 导师可能提问

**Q1：神经网络为什么比逻辑回归更强？**

因为隐藏层和非线性激活可以自动学习新表示，并建模非线性关系。

**Q2：为什么不能只堆叠线性层？**

多个线性层仍可合并为一个线性层，增加深度没有意义。

**Q3：反向传播的作用是什么？**

根据最终损失计算每个参数的梯度，为参数更新提供方向。

## 一句话总结

神经网络的核心价值是通过多层非线性计算自动学习表示，而这套表示学习机制构成了 Transformer、LLM 和神经信息抽取模型的基础。
"""


CHAPTER_18_NOTE = r"""# Chapter 18: Context-Free Grammars

## 章节定位

CFG 是传统 NLP 中描述句法结构的重要方法。它试图回答：一个句子中的词如何组成短语，短语如何组成完整句子。

相比 n-gram 只关注词序列概率，CFG 关注语言的层次结构。

## 核心概念

### Context-Free Grammar

CFG 是由非终结符、终结符、产生规则和开始符号组成的规则系统：

\[
G=(N,\Sigma,R,S)
\]

核心形式：

```text
S -> NP VP
```

表示句子可以由名词短语和动词短语组成。

### Parse Tree

句法树表示一句话内部的层次结构：

```text
句子 -> 短语 -> 单词
```

### Parsing

Parsing 是根据输入句子生成句法结构的过程。

### Constituency

成分句法认为句子由不同层次的组成部分构成，例如：

```text
The big dog
```

整体可以作为一个名词短语。

## 方法直觉

CFG 使用人工规则描述语言结构：

```text
文本
↓
匹配语法规则
↓
生成句法树
```

例如：

```text
Steve Jobs founded Apple.
```

可以分析为：

```text
NP + VP
```

进一步帮助识别：

```text
subject + verb + object
```

## 关键公式

CFG：

\[
G=(N,\Sigma,R,S)
\]

其中：

- \(N\)：非终结符；
- \(\Sigma\)：终结符；
- \(R\)：产生规则；
- \(S\)：开始符号。

现阶段只需理解 CFG 是规则系统，不需要掌握完整形式语言理论。

## 简单例子

句子：

```text
Steve Jobs founded Apple.
```

句法结构：

```text
NP:
Steve Jobs

VP:
founded Apple
```

可以进一步用于关系抽取：

```text
(Steve Jobs, founder_of, Apple)
```

## 优点与局限

优点：

- 可解释；
- 能表达层次结构；
- 适合规则明确场景。

局限：

- 规则难覆盖真实语言；
- 不理解语义；
- 难处理复杂歧义；
- 不适合直接完成知识推理。

## 与 KG-LLM 方向的联系

CFG 是早期信息抽取的重要工具：

```text
文本 -> 句法分析 -> 关系抽取 -> 知识图谱
```

现代 KG-LLM 系统更多使用 Transformer 和 LLM 自动学习句法和语义表示。

CFG 不负责知识推理，只提供语言结构信息。

## 导师可能提问

**Q1：CFG 为什么重要？**

因为它提供了语言层次结构的形式化表示。

**Q2：CFG 和 LLM 区别？**

CFG 使用人工规则，LLM 从数据中学习语言规律。

**Q3：CFG 能直接生成知识图谱吗？**

不能，只能辅助发现候选结构，真正的实体关系判断需要 IE 和 KG 方法。

## 一句话总结

CFG 是传统 NLP 中描述句法结构的方法，它帮助理解语言组成规律，但现代 LLM 更多通过神经表示学习自动获得类似能力。
"""


CHAPTER_19_NOTE = r"""# Chapter 19: Dependency Parsing

## 章节定位

Dependency Parsing 将句子表示为词与词之间的有向依存关系。与 CFG 通过 NP、VP 等短语节点描述层次结构不同，依存句法直接连接中心词（head）与依存词（dependent），因此更容易呈现谓词、主语、宾语和修饰语之间的关系。

对于关系抽取，本章比 CFG 更重要，因为实体之间的语义关系通常由句中的谓词—论元结构表达。

## 核心概念

**Head–Dependent**：每条依存边从中心词指向依存词。

**Dependency Relation**：依存边带有语法标签。常见标签包括：

- `nsubj`：主语；
- `obj`：直接宾语；
- `nmod`：名词修饰；
- `amod`：形容词修饰；
- `compound`：复合词；
- `root`：句子根节点。

**Dependency Tree**：通常有一个 root；除 root 外，每个 token 只有一个 head；从 root 到每个 token 存在唯一路径。

**Projectivity**：如果依存树可以画成无交叉边，则称为 projective。自由语序和复杂句式可能形成 non-projective tree。

## 方法直觉

依存解析需要解决两个问题：

1. 判断每个 token 的 head；
2. 判断该依存边的关系标签。

Transition-based parsing 维护 stack 和 buffer，通过 `SHIFT`、`LEFTARC`、`RIGHTARC` 等动作逐步构建依存树。它速度快，但早期错误可能向后传播。

Graph-based parsing 为所有可能的依存边打分，再寻找总分最高的合法树：

\[
\hat{T}=\arg\max_{T\in\mathcal{T}(S)} Score(T,S)
\]

现代神经解析器先用 encoder 生成 token 的上下文表示，再判断两个 token 构成 head-dependent 边的可能性。

## 关键公式

依存结构可以表示为：

\[
G=(V,A)
\]

其中 \(V\) 是 token 节点，\(A\) 是有向依存边。

评价指标：

\[
UAS=\frac{head正确的token数}{token总数}
\]

\[
LAS=\frac{head和label都正确的token数}{token总数}
\]

UAS 只检查中心词，LAS 同时检查中心词和关系标签。

## 简单例子

句子：

```text
任正非于1987年创立了华为。
```

核心依存结构：

```text
创立 ─nsubj→ 任正非
创立 ─obj──→ 华为
创立 ─obl──→ 1987年
```

## 后续补充

本章当前笔记保留到“简单例子”部分。优点与局限、与 KG-LLM 方向的联系、导师可能提问和一句话总结可在后续材料补充后继续扩展。
"""


CHAPTER_9_NOTE = r"""# Chapter 9 · Masked Language Models

> 本章关键词：**双向编码器、掩码语言建模（MLM）、上下文表示、预训练—微调、序列标注**。

## 1. 本章主题

本章介绍以 BERT 为代表的 **Masked Language Model（MLM）**。它不同于从左到右预测下一个 token 的 causal language model：MLM 会遮盖输入中的部分 token，再利用左右两侧上下文恢复原 token。

因此，MLM 通常使用 bidirectional Transformer encoder。它的核心产物不是连续生成的文本，而是每个 token 的上下文相关表示，尤其适合语言理解和信息抽取任务。

## 2. Bidirectional Transformer Encoder

Causal Transformer 使用 attention mask，禁止当前位置关注未来 token；bidirectional encoder 则移除这一限制，让每个 token 都能关注输入序列中的所有位置。

这种双向上下文特别适合需要理解整段输入的任务，例如：

- named entity recognition（NER）；
- text classification；
- relation extraction；
- entity linking；
- natural language inference（NLI）。

## 3. Masked Language Modeling

BERT 预训练时，随机选择约 **15%** 的 token 进行扰动：

- 80% 替换为 `[MASK]`；
- 10% 替换为随机 token；
- 10% 保持不变。

模型根据完整上下文预测这些位置原来的 token。若 \(M\) 是被选择的位置集合，训练目标只在这些位置计算交叉熵：

\[
\mathcal{L}_{\mathrm{MLM}} = - \sum_{i \in M} \log p_\theta(x_i \mid \tilde{x})
\]

其中，\(x_i\) 是原 token，\(\tilde{x}\) 是扰动后的输入。MLM 可以看作一种 denoising learning：先破坏输入，再训练模型恢复原始信息。

## 4. Contextual Embeddings

Static embedding 为一个词提供固定向量；contextual embedding 则会为同一个词在不同上下文中的实例生成不同向量。

例如，“**苹果发布了手机**”和“**吃了一个苹果**”中的“苹果”应有不同表示：前者更接近公司实体，后者更接近食物。这样的上下文敏感性使 MLM encoder 适合词义消歧、实体类型判断和实体链接。

## 5. Pretrain–Fine-tune Paradigm

模型先在大规模无标注文本上完成 MLM 预训练，学习通用语言表示；再在少量有标注数据上添加 task-specific head 并进行微调。这是一种 transfer learning：将预训练获得的语言知识迁移到具体下游任务。

实际使用时，需要区分两层能力：预训练提供可迁移的表示空间，微调则让表示适配任务标签、领域术语和评价目标。

## 6. Fine-Tuning for Classification

对于 sequence classification，BERT 通常在序列开头加入 `[CLS]`，取其最后一层向量作为整段文本的表示，再送入分类器。

对于 sequence-pair classification，输入两个由 `[SEP]` 分隔的序列。这一形式可用于自然语言推理、语义匹配，以及问题与候选证据的相关性判断。

## 7. Named Entity Recognition

NER 的目标是识别文本中的实体 span，并判断实体类型。常见类型包括 PER、ORG、LOC 和 GPE，也可以扩展为产品、作品、时间、金额等领域类型。

BIO tagging 中，B 表示实体开始、I 表示实体内部、O 表示非实体。做法是将每个 token 的 contextual embedding 输入同一个分类头，预测对应 BIO 标签。注意：实际实现需要处理 subword 与原始词边界的对齐，并可用 CRF 或约束解码减少非法标签序列。

## 8. 与知识图谱研究的关系

NER 是知识图谱构建的入口：先识别 entity mention，再通过 entity linking 将 mention 对齐到知识库的规范实体；随后可进行 relation extraction 和 event extraction，构建实体之间的边。

在 KG-RAG 中，encoder 模型可用于 query NER、entity linking、候选证据召回、reranking 和事实一致性判断；decoder LLM 则更适合问题分解、工具调用和自然语言答案生成。二者形成“**编码器负责找准证据，解码器负责组织推理与回答**”的互补分工。

## 重点总结

- MLM 通过双向上下文恢复被遮盖 token，学习上下文相关表示，而非自回归生成能力。
- contextual embeddings 是 NER、实体链接和关系抽取等理解任务的重要基础。
- 预训练—微调范式将大规模无标注语料中的知识迁移到具体下游任务。
- 在 KG-RAG 管线中，encoder 适合检索与判别，decoder LLM 适合推理与生成。

## 导师可能提问

- MLM 与 causal language model 的训练目标、可见上下文和典型用途分别有什么差异？
- 为什么 contextual embedding 能帮助实体消歧和 entity linking？
- 在 KG-RAG 中，哪些环节更适合 encoder，哪些环节更适合 decoder LLM？

## 后续补充资料

- Devlin et al. (2019), *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*。
- 比较 BERT、RoBERTa、DeBERTa 的预训练策略与下游迁移表现。
"""


CHAPTER_10_NOTE = r"""# Chapter 10 · Post-training

> 本章关键词：**instruction tuning、preference alignment、reward model、DPO、test-time compute**。

## 1. 本章主题

本章讨论大语言模型完成预训练后的三个关键环节：instruction tuning、preference alignment 和 test-time compute。

预训练模型以预测下一个 token 为目标，因此具备广泛的语言能力，却不必然能正确理解和完成用户指令。Post-training 的作用是调整模型行为：让它更会遵循指令、更符合人类偏好，并能在复杂任务上使用更多推理计算。

## 2. Instruction Tuning

Instruction tuning 也称 supervised fine-tuning（SFT）。训练样本通常由自然语言指令、任务输入和目标回答组成；模型继续最小化语言模型的 cross-entropy loss，学习在给定指令下生成合适回答。

它与单任务微调的差别在于：SFT 往往覆盖多个任务和表达方式，目标是提升模型在新任务上的一般指令遵循能力，而不只是记住某一种标签映射。

## 3. Preference Learning

即使经过 instruction tuning，模型仍可能给出不安全、不忠实或帮助性不足的回答。Preference learning 使用同一 prompt 下多个候选回答之间的偏好关系继续训练模型。

常见的一条偏好数据写作 \((x, o_w, o_l)\)：

- \(x\)：prompt；
- \(o_w\)：preferred output（获偏好的回答）；
- \(o_l\)：dispreferred output（未获偏好的回答）。

这类数据直接表达“哪个回答更好”，但“更好”应由明确标准定义，例如帮助性、无害性、证据充分性与事实忠实度。

## 4. Reward Model

Reward model 接收 prompt 和回答，输出一个标量分数。Bradley–Terry model 用两个回答 reward 的差值表示偏好概率：

\[
P(o_w \succ o_l \mid x) = \sigma\bigl(r(x, o_w) - r(x, o_l)\bigr)
\]

Reward model 可用于模型对齐，也可用于 best-of-N candidate selection；但 reward 只反映训练数据中的偏好信号，不能直接等同于事实正确性。因此，在知识密集任务中仍需结合外部证据与事实验证。

## 5. Preference Alignment

从强化学习视角看，LLM 是 policy，生成 token 是 action，当前上下文是 state，reward model 为完整回答提供 reward。为防止优化后的模型过度偏离原模型，目标函数通常加入相对于 reference policy 的 KL penalty：

\[
\max_\pi\; \mathbb{E}[r(x, y)] - \beta\, D_{\mathrm{KL}}\bigl(\pi(\cdot\mid x)\,\|\,\pi_{\mathrm{ref}}(\cdot\mid x)\bigr)
\]

KL 项相当于行为约束：模型可以为偏好而调整，但不应丢失预训练或 SFT 阶段已有的通用能力。

## 6. DPO

Direct Preference Optimization（DPO）直接利用 preference pairs 训练模型：提高 preferred output 的概率，降低 dispreferred output 的概率，同时以 reference model 约束更新幅度。

DPO 不需要单独训练显式 reward model，训练流程通常比完整的 reward model + PPO 路线更简单。它的优势是工程链路较短；其效果仍取决于偏好数据的覆盖范围、标注准则与参考模型的质量。

## 7. Test-Time Compute

Test-time compute 指在推理阶段增加计算。教材重点介绍 chain-of-thought prompting：通过分步推理 demonstrations 引导模型解决复杂问题。

在 KG-RAG 中，test-time compute 可具体表现为：

- 问题分解；
- 实体识别与实体链接；
- 子图或候选证据检索；
- 候选路径比较；
- 证据验证与答案生成前的事实一致性检查。

这里增加的不是模型参数，而是为了可靠推理而执行的中间步骤、搜索和验证。

## 8. 对研究方向的意义

Post-training 决定模型如何使用其已有能力。对知识图谱增强推理而言，SFT 可以教模型遵守抽取、检索与引用流程；preference alignment 可以奖励有证据、路径正确和合理拒答的输出；test-time compute 则可以增加多跳检索与验证步骤。

一个可操作的研究问题是：将“答案是否可由检索到的知识图谱路径支撑”转化为偏好数据或奖励信号，并在推理时显式保留检索、比较和验证轨迹。

## 重点总结

- Post-training 将“会续写”的预训练模型转化为更能遵循指令、对齐偏好和完成复杂任务的助手。
- SFT 学习高质量示范；偏好学习学习回答之间的相对优劣。
- Reward 不能替代事实正确性，知识密集任务需要外部证据验证。
- DPO 以更简洁的训练链路直接使用偏好对；test-time compute 则在推理阶段补充搜索与验证。

## 导师可能提问

- Instruction tuning、preference alignment 和 test-time compute 分别改变模型的什么能力？
- 为什么 reward model 的高分不能保证答案事实正确？
- 如何把 KG-RAG 的证据路径正确性设计成可训练的偏好或奖励信号？

## 后续补充资料

- Ouyang et al. (2022), *Training language models to follow instructions with human feedback*。
- Rafailov et al. (2023), *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*。
- 比较 PPO、DPO 与基于 verifier 的 test-time scaling 在知识密集推理任务中的取舍。
"""


CHAPTER_11_NOTE = r"""# Chapter 11 · Retrieval-based Models

> 本章关键词：**Information Retrieval、BM25、dense retrieval、RAG、retriever、reranker、KG-RAG**。

## 1. 本章主题

本章介绍 Information Retrieval、dense retrieval 和 Retrieval-Augmented Generation（RAG）。其核心目标是让语言模型在生成答案前访问外部知识，而不是完全依赖模型参数中的记忆。

一个基础 RAG 系统由 retriever 和 generator 两部分组成：retriever 根据 query 从文档集合取回相关 passages，generator 将 query 和 passages 作为上下文，生成最终回答。检索质量决定模型是否能看到正确证据，生成质量决定模型是否正确使用证据。

## 2. Sparse Retrieval

Sparse retrieval 将 query 和 document 表示为词表维度上的稀疏向量。常见方法包括 tf-idf 和 BM25。

- TF 衡量一个词在当前文档中的重要性；
- IDF 衡量该词在整个文档集合中的区分能力；
- BM25 在此基础上加入词频饱和和文档长度归一化，通常是强而稳定的词法检索基线。

倒排索引建立“词项 → 文档列表”的映射，因此可以快速定位包含查询词的候选文档，而无须逐篇扫描整个集合。

## 3. Dense Retrieval

Dense retrieval 使用语言模型将 query 和 document 编码为低维向量，并通过 dot product 或 cosine similarity 计算相关性。其主要优势是处理 vocabulary mismatch：即使 query 和 document 未使用相同词语，只要语义接近，仍可能被匹配。

Bi-encoder 分别编码 query 与 document，可预先索引文档向量，效率高，适合大规模召回。Cross-encoder 联合编码 query 与 document，判断更精确但计算更昂贵，适合对少量候选进行 reranking。

一个常见的两阶段结构是：

1. bi-encoder 从全库召回 Top-k 候选；
2. cross-encoder 对候选重排；
3. 将高质量证据交给 generator。

## 4. Retrieval Evaluation

Precision 衡量返回结果中相关文档的比例，Recall 衡量全部相关文档中被成功取回的比例。二者需要结合任务目标取舍：问答的证据召回不足会直接限制后续生成，而候选过多又会引入噪声和上下文成本。

对于 ranked retrieval，还应考虑相关文档的排名位置。Average Precision（AP）对单个 query 在每个相关结果出现位置的 precision 求平均；MAP 则对多个 query 的 AP 再求平均。实践中还常报告 Recall@k、MRR 或 nDCG，以观察证据是否出现在模型可见的前几名。

## 5. Retrieval-Augmented Generation

基本 RAG 包括三步：

1. retriever 返回 Top-k passages；
2. 将 passages、query 和 instruction 组成 prompt；
3. LLM 基于 prompt 生成答案。

RAG 可以接入动态知识、企业私有文档和模型训练完成后出现的新知识，也能在回答中提供引用。它并不自动保证真实性：系统仍需确保 retrieved context 覆盖问题、噪声受控，并要求 generator 基于证据作答或在证据不足时拒答。

## 6. RAG 的主要错误来源

RAG 的错误可能来自多个环节：

- 文档集合中没有正确知识；
- chunk 划分不合理；
- retriever 未召回正确证据；
- 正确证据排名过低；
- 上下文包含过多噪声；
- LLM 没有正确使用证据；
- 答案与引用不一致。

因此，必须分别评价 retrieval 和 generation。端到端答案分数低时，应先定位是语料、切分、召回、重排、上下文构造，还是生成与引用阶段的问题。

## 7. 对 KG-RAG 的意义

KG-RAG 在普通文本 RAG 的基础上加入 entity linking 和 graph retrieval。系统可以检索实体、三元组、邻居和多跳路径，再将这些结构化证据与文本 passages 一起交给 LLM。

GraphRAG 进一步把检索对象扩展为子图和社区摘要，适合关系型问题、多跳问题和全局性问题。一个关键设计原则是按问题选择证据粒度：实体事实可优先检索三元组，关系解释可联合路径与段落，全局概览可使用社区摘要。

## 重点总结

- Sparse retrieval 依赖词项匹配，BM25 是必须保留的强基线；dense retrieval 缓解词汇不匹配。
- Bi-encoder 擅长高效召回，cross-encoder 擅长精确重排，二者通常组合使用。
- RAG 的可靠性取决于检索与生成两个独立环节，不能只看最终答案。
- KG-RAG 与 GraphRAG 通过实体、路径、子图和社区摘要，为多跳与关系型问题提供结构化证据。

## 导师可能提问

- Sparse retrieval 与 dense retrieval 各自解决什么问题，为什么 BM25 仍是重要基线？
- 为什么 bi-encoder 常用于召回、cross-encoder 常用于 reranking？
- 如何定位一个 KG-RAG 回答错误究竟来自检索、证据组织还是生成？

## 后续补充资料

- Robertson and Zaragoza (2009), *The Probabilistic Relevance Framework: BM25 and Beyond*。
- Karpukhin et al. (2020), *Dense Passage Retrieval for Open-Domain Question Answering*。
- Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*。
"""


CHAPTER_17_NOTE = r"""# Chapter 17 · Sequence Labeling for POS and Named Entities

> 本章关键词：**sequence labeling、POS tagging、NER、BIO/BIOES、HMM、Viterbi、CRF**。

## 1. 章节主题

本章介绍 sequence labeling：为输入序列中的每个 token 分配一个标签。Part-of-speech tagging（POS）和 named entity recognition（NER）是两类典型任务。

重点模型包括 HMM 和 CRF。HMM 是生成式概率模型，CRF 是判别式条件概率模型；二者都不只逐 token 独立分类，而是通过全局序列解码寻找最合理的标签序列。

## 2. Part-of-Speech Tagging

POS tagging 为每个词预测词性，例如 NOUN、VERB、ADJ 和 PROPN。本质是上下文消歧：同一个词在不同句子中可能具有不同词性。

POS 信息可以辅助句法分析、关系抽取和事件触发词识别，但在现代知识图谱构建中通常不是最终输出。更重要的是理解它所代表的序列决策与上下文建模思想。

## 3. Named Entity Recognition

NER 的目标是识别实体 span，并判断实体类型。常见类型包括 PERSON、ORG、LOC、GPE、PRODUCT 和 WORK。

NER 面临两个核心歧义：

1. **实体边界歧义**：一个实体从哪个 token 开始、到哪个 token 结束；
2. **实体类型歧义**：同一个名称在不同上下文中可能表示不同类型。

因此，模型必须利用上下文而不能只依赖词表匹配。

## 4. BIO 与 BIOES

BIO tagging 将 span recognition 转为逐 token 分类：

- `B-X`：X 类实体的开始；
- `I-X`：X 类实体内部；
- `O`：实体外部。

BIOES 进一步使用 `E-X` 表示实体结束、`S-X` 表示单 token 实体。若有 \(n\) 类实体，BIO 的标签数为 \(2n + 1\)。标签体系把实体边界显式编码，也带来了合法转移约束，例如 `I-ORG` 不应直接跟在 `O` 后面。

## 5. Hidden Markov Model

HMM 将标签视为隐藏状态，将单词视为观测。模型包含：

- transition probability：\(P(y_i \mid y_{i-1})\)；
- emission probability：\(P(x_i \mid y_i)\)。

它假设当前标签只依赖前一个标签，当前观测只依赖当前标签。这个假设较强，但 HMM 清晰地展示了如何将局部概率组合为完整序列的联合分数。

## 6. Viterbi Algorithm

Viterbi 是一种动态规划算法。它维护每个时间步到达每个状态的最优路径概率，并使用 backpointer 保存最优前驱状态。序列结束后，从得分最高的终止状态回溯，即可得到概率最高的完整标签序列。

其关键价值是避免枚举所有标签组合：对长度为 \(T\)、标签数为 \(K\) 的线性链，解码可在约 \(O(TK^2)\) 的时间内完成。

## 7. Conditional Random Field

CRF 直接建模 \(P(Y \mid X)\)，可同时利用输入词、邻近词、词缀、word shape、embedding、POS、gazetteer 和标签转移等特征。

Linear-chain CRF 对完整标签序列进行全局归一化，并学习标签间的转移偏好。因此它可以减少非法 BIO 序列；在神经 NER 中，也常把 CRF 接在 contextual encoder 的 token 分类分数之上。

## 8. NER Evaluation

NER 使用实体级 precision、recall 和 F1。只有实体边界和类型都正确时，预测才算 true positive。

常见错误包括：

- 漏识别实体；
- 多识别实体；
- 边界错误；
- 类型错误。

实体级评估比 token accuracy 更严格，因为“边界近似正确”仍可能导致实体链接和关系抽取失败。

## 9. 与知识图谱的关系

NER 是知识图谱构建的基础步骤，但 NER 结果仍只是文本 mention。后续需要 entity linking 将 mention 对齐到规范实体，再进行 relation extraction 和 event extraction。

在 KG-RAG 中，NER 用于发现问题中的实体入口；在 GraphRAG 中，NER 用于从文档中生成图节点。高质量 NER 能提升后续链接、图检索和多跳证据追踪的召回上限。

## 重点总结

- Sequence labeling 关注整个标签序列的合理性，而不仅是单 token 的局部类别。
- BIO/BIOES 将实体边界编码为标签；CRF 和约束解码可降低非法转移。
- HMM 与 Viterbi 提供经典的概率建模与动态规划解码框架；CRF 能整合更丰富的判别特征。
- NER 是 KG 构建与 KG-RAG 实体入口的重要前置步骤，仍需通过 entity linking 完成规范化。

## 导师可能提问

- 为什么 NER 要使用实体级 F1，而不能只看 token accuracy？
- HMM 与 CRF 分别建模什么概率，二者的特征能力有什么差异？
- NER、entity linking、relation extraction 在知识图谱构建中如何衔接？

## 后续补充资料

- Lafferty, McCallum, Pereira (2001), *Conditional Random Fields*。
- Lample et al. (2016), *Neural Architectures for Named Entity Recognition*。
- 调研 domain-specific NER 中的 subword 对齐、弱监督与标签约束解码。
"""


CHAPTER_20_NOTE = r"""# Chapter 20 · Information Extraction: Relations, Events, and Time

> 本章关键词：**relation extraction、event extraction、temporal analysis、TimeML、template filling、knowledge graph**。

## 1. 章节主题

本章讨论如何从非结构化文本中抽取关系、事件和时间信息，并组织成结构化数据。第 17 章的 NER 主要识别实体 mention；本章进一步识别实体之间的关系、实体参与的事件、事件发生时间和事件之间的时间顺序。

因此，本章是知识图谱与事件知识图谱构建的核心基础：实体成为节点候选，关系成为边，事件成为可连接多个论元的节点，时间关系让图具备演化与推理能力。

## 2. Relation Extraction

Relation Extraction 识别实体之间的语义关系，典型输出为三元组：

`(head entity, relation, tail entity)`

例如：`(刘慈欣, author_of, 三体)`。关系通常有方向，并受到实体类型和 ontology schema 的约束。模型还必须能够输出 `no_relation`，避免为无关实体对强行生成关系。

## 3. Relation Extraction Methods

主要方法包括：

1. Pattern-based extraction；
2. Supervised relation classification；
3. Bootstrapping；
4. Distant supervision；
5. Open Information Extraction。

Pattern 方法精度高但召回率低；监督方法效果稳定，却需要较多标注数据。Bootstrapping 从少量 seed patterns 或 seed tuples 迭代扩展，需警惕 semantic drift。Distant supervision 用已有知识图谱自动构造训练数据，规模大但有标签噪声。Open IE 不预定义关系集合，直接抽取文本关系短语，后续还需做关系规范化。

## 4. Event Extraction

Event Extraction 识别文本中的事件 mention，并提取事件类型、trigger、arguments 和属性。事件可由动词或名词表达；论元可以包括参与者、地点、时间、金额和产品等信息。

事件比二元关系更适合表达动态场景。例如一次产品发布事件可同时连接发布机构、产品和发布时间，而不必把所有信息拆为彼此脱离的二元边。

## 5. Temporal Representation

时间分析通常包括：

1. temporal expression recognition；
2. temporal normalization；
3. event-time linking；
4. temporal relation classification。

时间表达往往需要结合 document creation time 或 anchor event 归一化，标准时间通常采用 ISO 8601。Allen interval algebra 用 before、after、overlaps、meets、starts、finishes、during 和 equals 等关系描述时间区间之间的关系，为事件顺序推理提供形式化语言。

## 6. Aspect

Aspect 描述事件的内部时间结构，主要类别包括 state、activity、accomplishment 和 achievement。它有助于判断事件是否持续、是否完成、是否存在自然终点，从而支持更细粒度的时间关系推理。

## 7. TimeBank and TimeML

TimeBank 使用 TimeML 标注事件、时间表达及其关系。主要对象包括：

- `EVENT`；
- `TIMEX3`；
- `TLINK`；
- `ALINK`；
- `SLINK`。

这种表示能够把文本转换为事件时间图，方便查询事件参与者、发生时间及先后依赖。

## 8. Template Filling

Template Filling 识别某类预定义场景，并为模板中的槽位填充值。系统通常先进行 template recognition，再进行 role-filler extraction。

现代 LLM 的 JSON structured extraction 可看作 schema-guided template filling：通过固定字段、类型约束和证据片段，使抽取输出更便于写入下游数据库或知识图谱。

## 9. 与知识图谱的关系

NER 产生实体节点候选，Relation Extraction 产生边，Event Extraction 产生事件节点，Temporal Analysis 为事件添加时间及先后关系。完整流程为：

`Text → NER → Entity Linking → Relation/Event Extraction → Temporal Normalization → Entity/Event Resolution → Knowledge Graph`

在 KG-RAG 中，这条链路可以把文档转化为可检索、可追溯的结构化证据；回答时再将相关实体、关系、事件路径与原文证据共同提供给 LLM。

## 重点总结

- 关系抽取构造实体边，事件抽取组织多论元动态事实，时间分析提供顺序与持续性约束。
- 监督、弱监督、开放抽取在标注成本、schema 约束与噪声控制上各有取舍。
- 事件与时间图使知识图谱能表达“谁在何时做了什么”，支持时间敏感的检索与推理。
- 结构化 JSON 抽取应以 schema、类型约束和证据定位降低幻觉与规范化成本。

## 导师可能提问

- 为什么动态场景通常更适合建模为事件，而不只是多条二元关系？
- Distant supervision 的标签噪声来自哪里，如何缓解？
- 如何把时间归一化和事件关系用于时间敏感的 KG-RAG 问答？

## 后续补充资料

- ACE Event Extraction 与 TimeBank/TimeML 标注规范。
- Mintz et al. (2009), *Distant Supervision for Relation Extraction without Labeled Data*。
- 调研 LLM schema-guided extraction 的验证、实体消歧和时间归一化策略。
"""


CHAPTER_21_NOTE = r"""# Chapter 21 · Semantic Role Labeling

> 本章关键词：**predicate、argument、semantic role、PropBank、FrameNet、selectional preference、event structure**。

## 1. 章节主题

Semantic Role Labeling（SRL）研究谓词与论元之间的语义关系，回答“谁对谁做了什么、何时、何地、以什么方式发生”等问题。

SRL 提供一种 shallow semantic representation：它比主语、宾语等句法关系更接近事件意义，又没有完整逻辑语义表示那么复杂，因此是把自然语言映射为事件参与结构的重要中间层。

## 2. Semantic Roles

常见语义角色包括：

- AGENT：主动引发事件的参与者；
- EXPERIENCER：感知或经历某种状态的参与者；
- FORCE：非自主事件原因；
- THEME：受到事件影响或移动的对象；
- INSTRUMENT：事件所使用的工具；
- SOURCE / GOAL：移动或转移的起点与终点；
- BENEFICIARY：事件受益者；
- CONTENT：言说或认知事件的内容。

语义角色不能与句法位置直接对应。主动句、被动句与论元结构交替会让同一角色出现在不同位置，因此 SRL 的目标是跨越表层词序恢复事件参与关系。

## 3. Diathesis Alternations

Diathesis alternation 指同一谓词的论元可以有不同句法实现。例如：

`Doris gave the book to Cary.`

`Doris gave Cary the book.`

两句中 Doris 都是 AGENT，book 都是 THEME，Cary 都是 GOAL。语义角色表示能够越过表层差异，保留稳定的事件结构。

## 4. Problems with Thematic Roles

传统 thematic roles 存在若干困难：没有 universally accepted role set；角色内部可能需要进一步细分；AGENT、THEME 等概念难以用严格条件定义；不同谓词的论元结构差异很大。

因此出现了 Proto-Agent / Proto-Patient、PropBank 和 FrameNet 等不同体系。它们不是完全等价的标签集，而是从不同角度平衡泛化性、词义细节与标注一致性。

## 5. PropBank

PropBank 为每个谓词词义定义 `ARG0`、`ARG1`、`ARG2` 等编号角色。通常 `ARG0` 接近 Proto-Agent，`ARG1` 接近 Proto-Patient，而 `ARG2–ARG4` 的含义取决于具体谓词。

PropBank 还定义修饰角色，如 `ARGM-TMP`（时间）、`ARGM-LOC`（地点）、`ARGM-MNR`（方式）和 `ARGM-CAU`（原因）。编号角色依赖谓词的 frameset，因此使用时需要结合谓词词义解释。

## 6. FrameNet

FrameNet 基于 frame semantics。Frame 是一个包含背景知识、谓词和参与角色的场景结构；角色称为 frame elements，并区分 core roles 与 non-core roles。

不同词可以激活同一 frame。例如 increase、rise 和 fall 都可与尺度变化 frame 相关。相比 PropBank 的逐谓词编号，FrameNet 更强调场景知识和语义概念的共享。

## 7. Semantic Role Labeling

SRL 通常包含五步：

1. predicate identification；
2. predicate sense disambiguation；
3. argument identification；
4. role classification；
5. global decoding。

传统模型依赖 constituency parse 或 dependency parse；神经模型可将 SRL 转化为带 predicate 条件的 BIO sequence labeling。无论方法如何，全局解码和角色约束都有助于避免相互冲突的论元结构。

## 8. Selectional Preferences

Selectional restriction 表示谓词对论元语义类型的要求，例如 eat 的 THEME 通常属于 FOOD。自然语言中的限制并不绝对，现代系统更常使用 selectional preference，以概率或关联强度表示谓词与论元类别之间的偏好。

这类偏好可用于候选论元排序、异常关系检测与知识图谱 schema 验证，但不应把低频事实简单判定为错误。

## 9. Primitive Decomposition

Primitive decomposition 将复杂谓词分解为基础语义成分，例如：

`KILL(x,y) ⇔ CAUSE(x, BECOME(NOT(ALIVE(y))))`

它有利于因果与状态变化推理，但构建通用语义原语体系较为困难，也难以覆盖语言中的全部细微差异。

## 10. 与知识图谱的关系

SRL 可以将句子转换为事件参与结构：谓词对应事件或关系类型，arguments 对应实体节点，semantic roles 对应事件节点与实体节点之间的边。

典型流程为：

`Text → NER → Entity Linking → Predicate Detection → SRL → Event/Relation Mapping → Knowledge Graph`

在 KG-RAG 中，SRL 可用于从候选证据中抽取“谁—做什么—对谁—何时何地”的结构，再与实体链接、关系抽取和事件时间图结合，提升多跳证据路径的可解释性。

## 重点总结

- SRL 以谓词—论元结构表达事件意义，能跨越主动/被动等表层句法差异。
- PropBank 侧重谓词编号角色，FrameNet 侧重共享的场景框架；二者适合不同的标注与知识建模需求。
- Selectional preferences 是概率偏好而非绝对规则，可辅助论元判断与 schema 验证。
- SRL 为知识图谱提供事件节点、参与者角色和可解释的证据结构。

## 导师可能提问

- SRL 相比 dependency parsing 为事件抽取补充了什么信息？
- PropBank 与 FrameNet 的角色体系有何差异，分别适合什么场景？
- 如何将 SRL 输出映射为可用于 KG-RAG 的事件节点和角色边？

## 后续补充资料

- Palmer, Gildea, Kingsbury (2005), *The Proposition Bank*。
- Gildea, Jurafsky (2002), *Automatic Labeling of Semantic Roles*。
- 调研 predicate-aware encoder、span-based SRL 与 LLM structured extraction 的结合方式。
"""


CHAPTER_23_NOTE = r"""# Chapter 23 · Coreference Resolution and Entity Linking

> 本章关键词：**mention、coreference cluster、mention ranking、entity linking、candidate generation、knowledge base**。

## 1. 章节主题

本章介绍 coreference resolution 和 entity linking。Coreference resolution 判断文本中的多个 mention 是否指向同一个 discourse entity，并将它们组成 coreference chain；entity linking 则将 mention 或 mention cluster 映射到 ontology 或 knowledge base 中的唯一实体。

两者是知识图谱构建、跨句信息抽取、GraphRAG 和多跳问答的重要基础：前者解决“文中是否同一对象”，后者解决“它在外部知识库中是谁”。

## 2. 基本概念

Mention 是文本中的指称表达，referent 是其实际指向的对象。Anaphor 回指前文实体，antecedent 是其先行词；多个指向同一实体的 mention 组成 coreference cluster。Singleton 指只出现一次、没有其他共指 mention 的实体。

Discourse model 是理解文本时逐步建立的实体、属性和关系表示。共指消解持续更新这一模型，使后续句子能够继承先前提到的对象。

## 3. Mention Detection

Mention detection 识别可能指称实体的 span，候选包括 noun phrases、named entities、pronouns 和 possessive pronouns。系统通常优先保证 recall，再过滤 pleonastic pronouns、非指称名词短语和不符合任务规范的 span。

候选漏掉会给后续共指带来不可恢复的 recall 损失，因此 span 提议与过滤阈值是端到端系统的重要设计点。

## 4. Coreference Architectures

- **Mention-pair model**：对每个 mention pair 二分类，判断是否共指；
- **Mention-ranking model**：统一为当前 mention 的 antecedent 候选评分，并加入 ε 表示没有 antecedent；
- **Entity-based model**：直接判断新 mention 是否加入已有 entity cluster，而非只链接某个单独 mention。

Entity-based 模型更贴近最终 cluster，但需要聚合已有 cluster 的信息；mention ranking 则在效率和建模能力之间较为实用。

## 5. Neural Mention Ranking

端到端神经模型通常枚举候选 span，用 Transformer 得到 contextual representation，并计算 mention score、antecedent compatibility score 和最终 coreference score。

Span representation 常包括 start token、end token 和 attention-weighted head representation。模型先裁剪低分 span，再为保留 mention 选择 antecedent，最后通过传递闭包形成 cluster。

## 6. Entity Linking

Entity linking 一般包括四步：

1. mention detection；
2. candidate generation；
3. candidate ranking；
4. entity ID selection。

传统方法可利用 Wikipedia anchor dictionary、entity prior 和 graph coherence。神经方法分别编码 mention context 与 entity title/description，以 dot product 或 cosine similarity 进行候选排序。对 NIL / 无法链接的 mention，需要显式允许拒绝或新实体处理。

## 7. Evaluation

Coreference 的输出是 clusters，需使用专门的 cluster metrics，包括 MUC、B³、CEAF、BLANC 和 LEA。CoNLL evaluation 通常取 MUC、B³ 和 CEAF-e 的平均值。

实体链接除候选召回外，还应评价最终 ID accuracy、top-k candidate recall 和 NIL 判定；只报告最终准确率会掩盖候选生成或排序阶段的失败。

## 8. 与知识图谱的关系

Coreference resolution 将同一实体的不同 mention 合并，减少知识图谱中的重复节点；entity linking 将合并后的 mention cluster 对齐到规范实体 ID。

完整链路为：

`Text → Mention Detection → Coreference Resolution → Entity Linking → Relation/Event Extraction → Knowledge Graph`

在 GraphRAG 中，正确归并与链接能使跨句事实落到一致节点，并让多跳检索沿正确实体边展开；错误链接则可能污染整条证据路径。

## 重点总结

- 共指消解处理文本内部的实体一致性，实体链接处理文本与知识库之间的规范化对齐。
- Mention ranking 用 ε 建模无 antecedent，neural span model 结合上下文表示和候选裁剪完成端到端聚类。
- Entity linking 需分解评估候选生成、排序与 NIL 处理，不能只看最终 ID。
- 两者是跨句抽取、知识图谱去重和 GraphRAG 证据一致性的关键前提。

## 导师可能提问

- 为什么 entity linking 不能只依赖字符串匹配？
- Mention-pair、mention-ranking 与 entity-based 共指模型各有什么局限？
- 共指或实体链接错误会怎样影响 GraphRAG 的多跳检索？

## 后续补充资料

- Lee et al. (2017), *End-to-end Neural Coreference Resolution*。
- Wu et al. (2020), *Scalable Zero-shot Entity Linking with Dense Entity Retrieval*。
- 调研跨文档共指、NIL entity 与面向领域知识库的实体链接。
"""


NOTE_CONTENT_BY_NUMBER = {
    3: CHAPTER_3_NOTE,
    4: CHAPTER_4_NOTE,
    6: CHAPTER_6_NOTE,
    9: CHAPTER_9_NOTE,
    10: CHAPTER_10_NOTE,
    11: CHAPTER_11_NOTE,
    18: CHAPTER_18_NOTE,
    19: CHAPTER_19_NOTE,
    17: CHAPTER_17_NOTE,
    20: CHAPTER_20_NOTE,
    21: CHAPTER_21_NOTE,
    23: CHAPTER_23_NOTE,
}


PRIORITY_CHAPTERS_SUMMARY = r"""# SLP3 第一优先级章节总结：知识图谱增强的大模型推理基础

## 整体定位

第一优先级章节共同回答一个系统问题：**如何把自然语言文本转化为可检索、可链接、可推理、可验证的知识，并让 LLM 基于这些知识生成答案？**

```text
原始文本 → Tokenization → Embedding / Contextual Representation
→ NER 与 Mention Detection → Coreference Resolution → Entity Linking
→ Relation / Event / Semantic Role Extraction → Knowledge Graph Construction
→ Sparse / Dense / Graph Retrieval → RAG / KG-RAG / GraphRAG
→ LLM Reasoning and Generation → Evidence Verification and Evaluation
```

## 五个能力模块

1. **语言表示**：Tokenization、Embedding、Transformer、MLM 决定文本如何被表示，并影响实体边界、语义匹配与上下文消歧。
2. **LLM 生成与对齐**：next-token prediction 提供生成能力；SFT、preference alignment 和 test-time compute 让模型遵循流程、使用证据并在复杂问题上增加搜索与验证。
3. **检索**：BM25 处理精确词项，dense retrieval 处理语义匹配，cross-encoder 负责重排；三者可与图检索组成 hybrid retrieval。
4. **信息抽取**：NER、关系抽取、事件抽取和 SRL 将文本转换为实体、关系、事件和参与角色。
5. **实体落地与图推理**：共指消解合并文本内 mention，实体链接映射知识库 ID，知识图谱保存可查询、可解释的多跳路径。

## 关键分工与区别

| 概念 | 主要作用 |
| --- | --- |
| Static / contextual embedding | 固定词向量 / 依上下文变化的表示 |
| Encoder / decoder | 表示、抽取、匹配、重排 / 规划、推理、生成、工具调用 |
| Attention / retrieval | 模型内部 token 交互 / 模型外部知识检索 |
| NER / entity linking | 识别“苹果”是 ORG / 对齐到 Apple Inc. 的唯一 ID |
| Coreference / entity linking | 合并“苹果公司”“该公司” / 映射到外部 KG 实体 |
| Relation extraction / SRL | 规范实体关系 / 谓词事件中的论元角色 |
| RAG / KG-RAG / GraphRAG | 文本证据 / 实体、三元组和路径 / 子图、社区与局部/全局图检索 |

## 从文本到 KG-RAG

离线建库：

```text
文档采集 → 清洗与切分 → NER / 共指 / 实体链接
→ 关系、事件、时间抽取 → 实体/事件消歧 → KG 构建
→ 文档与实体 embedding → 稀疏、稠密与图索引
```

在线问答：

```text
问题 → Query NER 与实体链接 → 问题分解
→ Sparse / Dense / Subgraph Retrieval → Reranking → Evidence Fusion
→ LLM 生成 → 引用、路径输出与答案验证
```

以“《三体》的作者出生在哪里？”为例：先将“三体”链接到作品实体，沿 `author` 边找到刘慈欣，再沿 `birthplace` 边和文本证据确认阳泉；最终输出答案、实体、路径、证据与置信度。

## 必须掌握的公式

- Cosine similarity：\(\cos(u,v)=\frac{u\cdot v}{\|u\|\|v\|}\)，用于 query、文档与实体向量匹配。
- 自回归生成：\(P(w_i \mid w_{<i})\)；RAG 条件生成：\(P(a_i \mid q,R(q),a_{<i})\)。
- 序列标注：\(\hat{Y}=\arg\max_Y P(Y\mid X)\)。
- 实体链接：\(\hat e=\arg\max_{e\in C(m)} P(e\mid m,context,KG)\)。
- 检索评价：\(Precision=TP/(TP+FP)\)、\(Recall=TP/(TP+FN)\)、\(F_1=2PR/(P+R)\)。

## 研究结论与评估

Embedding 负责召回“可能相关”的内容，知识图谱提供实体、关系、类型约束和路径证据；二者互补而非替代。LLM 擅长理解、规划与生成，但动态事实应来自文档库、数据库、KG 或 API。

可靠的多跳推理需要显式中间状态：起始实体 ID、关系类型、中间实体、三元组来源、路径得分、文本证据和验证状态。解释也应来自这些证据，而不是模型自述。

建议对比 Closed-book LLM、Vector RAG、Hybrid RAG、KG-RAG 和 GraphRAG，并分别报告 Retrieval Recall@K、Entity Linking Accuracy、Relation F1、Path Accuracy、Answer EM/F1、Faithfulness、Citation Correctness、Latency 和 Token Cost。错误分析应细分 Tokenization、NER、Coreference、Entity Linking、Relation Extraction、Retrieval、Path Search、Evidence Utilization、Generation 与 Citation。
"""


INTERN_RECORDS = [
    {
        "day": 1,
        "title": "环境熟悉与业务理解",
        "tags": "环境搭建,业务理解,全栈开发",
        "content": r"""## 今日工作内容

### 1. 熟悉实习环境

* 了解公司内部开发环境，包括前端（React）与后端（Node.js / Python）项目的构建、发布流程。
* 熟悉 Windows 操作机、开发工具安装方式以及离线环境下的软件部署流程。
* 初步了解企业内部对于安全、网络隔离、依赖版本管理的要求。

### 2. 明确项目方向

当前负责方向为内部运维管理平台的全栈开发。

初步思考：

* MVP 阶段聚焦搭建平台基础骨架，不直接深入复杂业务逻辑。
* 优先建立从界面到数据层的完整链路：

  * 服务器资产信息展示（CPU、内存、磁盘可视化）
  * 服务状态监控看板
  * 日志查询与异常分析页面
  * 基础运维知识问答面板

后续再逐步接入真实业务系统并完善权限、告警等功能。

### 3. 与 Mentor 沟通方向

沟通重点：

* 实习期间主要学习企业级全栈开发流程，包括前后端协作、接口设计、数据库建模与部署规范。
* 不仅关注代码实现，还需要理解：

  * 业务运维场景与痛点
  * 系统架构（前后端分离、微服务基础）
  * 研发规范（代码评审、分支策略、文档维护）
  * 工具设计思路（如何让内部平台更好用）

## 遇到的问题与解决记录

**问题：Win11 重装后的磁盘分区问题**

现象：安装 Windows 后只有 C 盘。
分析：安装过程中没有手动创建分区。
解决：使用磁盘管理重新划分空间。

**问题：操作机缺少 Wi-Fi 驱动**

解决：提前准备对应型号驱动包，企业环境安装系统后需同步补齐驱动。""",
    },
    {
        "day": 2,
        "title": "开发工具与 AI 辅助开发环境搭建",
        "tags": "VS Code,AI开发,环境配置,离线环境",
        "content": r"""## 今日工作内容

### 1. VS Code 离线环境配置

遇到问题：公司环境无法直接访问插件市场，前端开发常用插件（ESLint、Prettier、Vetur 等）无法在线安装。Mentor 提供离线插件包，需要手动安装。

学习内容：

* VSIX 插件安装流程。
* VS Code 扩展目录结构：extension、extension.vsixmanifest、extension.xml。

解决方案：使用离线 VSIX 包安装前端与后端开发必备插件。配置企业内网下的代码补全、格式化与调试环境。

### 2. AI Coding 工具调研

调研工具：Cline、Continue、Cherry Studio、Codex

重点关注：

* 如何连接企业内部大模型。
* 如何使用本地千问模型辅助全栈开发（生成组件代码、接口逻辑、测试用例）。

探索方案：VS Code + Continue + 内网大模型 API

配置思路：

* 本地模型地址
* API Key
* 模型名称
* MCP 工具调用能力（用于连接数据库、执行 shell 等）

目标：构建类似 Copilot 的企业内部 AI 开发助手，提升前后端代码编写效率。

### 3. 企业级 AI 开发规范思考

针对全栈项目中使用 AI 生成代码，需要提前建立规范，包括 AI_RULES.md：

约束内容：

* 项目架构规范（组件划分、状态管理、API 层设计）
* 代码风格（ESLint/Prettier 统一、命名规范）
* Git 工作流（feature 分支、commit message 格式）
* 提交规范（conventional commits）
* 测试要求（单元测试、接口测试）
* 文档维护要求（接口文档、组件说明）

目标：让 AI Coding 工具生成代码时遵循企业工程规范，生成可维护、可集成的业务代码。""",
    },
    {
        "day": 3,
        "title": "全栈项目 MVP 规划与问题整理",
        "tags": "MVP设计,系统架构,AI Agent,运维平台",
        "content": r"""## 今日工作内容

### 1. 运维管理平台 MVP 设计思考

当前规划：搭建前后端分离的运维管理平台 MVP。

**功能方向一：服务器资产管理模块**

* 前端（React + Ant Design）：主机列表、详情卡片、CPU/内存/磁盘使用率图表（基于 ECharts）。
* 后端（Node.js + Express 或 Python FastAPI）：提供 RESTful API，采集并返回主机信息。
* 数据库（MySQL）：存储资产信息与历史状态快照。

**功能方向二：日志辅助分析模块**

* 前端：日志查询页面，支持关键词搜索、异常关键词高亮、时间范围筛选。
* 后端：日志读取接口，支持分页与简单过滤逻辑。
* 未来可结合本地大模型实现智能分析。

**功能方向三：运维知识助手**

* 前端：聊天面板，用户输入异常描述或错误日志片段。
* 后端：调用内网千问大模型，返回问题分析、排查步骤、解决建议。
* 支持上下文记忆，可逐步引入 RAG 机制检索内部运维文档。

### 2. AI Agent 技术结合方向

结合之前 R&D Agent Copilot 项目经验，考虑在全栈平台中引入 Agent 架构：

**Router**：负责判断用户请求类型（日志分析、服务检查、配置对比、故障咨询）。

**Planner**：负责拆解任务。例如用户说 "nginx 服务异常"，Agent 会：
1. 调用后端接口查询服务状态
2. 拉取对应时间段日志
3. 通过大模型分析错误原因
4. 向前端返回处理建议并展示

**Tools**：连接真实运维能力，通过后端封装工具调用（执行受限 shell 命令、日志文件查询、配置一致性检查、数据库连接检测）。前端仅通过接口触发，确保安全可控。

## 遇到的问题与解决记录

**问题：企业环境下 AI 工具接入**
如何在无法访问公网的环境使用 AI 辅助全栈开发。

探索方案：
* 本地：Cherry Studio 作为模型管理入口，Continue/Cline 作为 IDE Agent
* 模型：内网部署千问大模型
* 目标：VS Code → Agent 插件 → 内网 LLM → 工具调用

## 阶段总结（前三天）

✅ 熟悉企业全栈开发环境（前端、后端、数据库工具链）
✅ 了解离线开发工具与插件部署流程
✅ 调研企业内部 AI Coding 使用方式，搭建 AI 辅助开发环境
✅ 明确内部运维管理平台 MVP 功能方向与前后端职责
✅ 思考 Agent 与全栈应用结合方案，设计 Router/Planner/Tools 架构

## 下一阶段计划

1. 完善平台需求分析，输出前端页面原型与接口设计文档
2. 设计 MVP 系统架构（前端 SPA、后端 API、数据库表结构）
3. 建立 Git 项目仓库，制定协作规范与 AI_RULES
4. 使用 AI Agent 辅助完成基础代码开发
5. 后续逐步接入真实运维数据，完善监控、告警与知识问答功能""",
    },
    {
        "day": 4,
        "record_date": date(2026, 7, 20),
        "title": "离线依赖排查与开发交付边界梳理",
        "tags": "离线依赖,npm,Windows,AI开发,交付",
        "content": r"""## 当天目标

围绕服务器运维工具的离线开发环境，定位前端依赖准备和内外网交付过程中的不确定点。

## 完成事项

* 检查前端项目离线安装时的缺包现象，并梳理 `package-lock.json` 与实际 npm 包之间的关系。
* 确认仅查看 lock 文件中的 `packages` 字段，不能证明离线安装所需的包已经完整准备。
* 研究在无法访问 npm 仓库的操作机中定位具体缺失依赖的方法；尝试将外网电脑下载的依赖压缩包传入内网操作机。
* 排查大型依赖压缩包在操作机中打开或解压无响应的问题。
* 对比 Cline、Continue、Codex 插件和内网千问模型在工程开发中的适用边界。

## 遇到的问题

内网操作机不能直接访问 npm 仓库，安装时提示的缺失依赖会变化；传入的大型压缩包也出现打开或解压异常。对于大量工程报错，内网模型的上下文理解和修复稳定性仍有限。

## 解决思路

不再根据报错逐个猜测依赖。后续会先在外网开发机完成一次干净安装，再结合 lock 文件和 npm 缓存统一制作离线依赖包；同时将“依赖是否完整”和“项目代码是否正确”拆开验证，在外网完成开发、构建和测试后再传输完整产物。

## 当天收获

离线交付不是简单复制 `node_modules`。操作系统、Node 版本、CPU 架构、锁文件和构建流程都需要保持一致；依赖问题必须依靠可复现的安装流程解决，而不能依赖 AI 临时修补。

## 下一步计划

完成外网环境的干净安装验证，并整理可在内网复用的离线依赖与构建产物清单。""",
    },
    {
        "day": 5,
        "record_date": date(2026, 7, 21),
        "title": "后端最小闭环与安全执行边界设计",
        "tags": "FastAPI,任务编排,Mock Executor,Dry Run,安全设计",
        "content": r"""## 当天目标

完善服务器运维工具的后端最小闭环，并明确真实执行能力接入前的安全边界。

## 完成事项

* 完成项目工程初始化和后端最小调用链设计：`API 请求 → 任务服务 → Executor → 输出解析 → 状态持久化`。
* 设计可替换执行器接口：`MockExecutor`、`LocalScriptExecutor`、`SshScriptExecutor`；同时设计 `MockOutputParser`、`StructuredJsonParser`、`LegacyServicesOutputParser` 三类输出解析器。
* 增加数据库模型、任务服务、Mock 执行器、任务运行器、种子数据和基础测试结构，并初始化 Alembic 数据库迁移配置。
* 初始化前端 Vite、TypeScript 和统一 API Client，前端构建已实际通过。
* 后端代码已落地；因本机缺少符合要求的 Python 3.12 环境，尚未实际完成后端启动、迁移和测试执行。

## 遇到的问题

真实服务器、SSH、Ansible 和生产脚本尚未联调，且本机 Python 版本不满足后端运行要求。如果直接将前端按钮连接到 Shell 命令，后续会难以控制权限、审计和环境差异。

## 解决思路

项目默认关闭真实写操作：`WRITE_OPERATIONS_ENABLED=false`、`PRODUCTION_OPERATIONS_ENABLED=false`。SSH 地址、账号、`services.sh` 路径、inventory、Playbook、tag 和堡垒机方式均通过配置注入，不写死在代码中；当前只使用 Fake Transport、Dry Run、脱敏 fixtures 与模拟 stdout/stderr。

## 当天收获

运维系统需要将执行器、协议适配层、输出解析器和任务状态解耦。这样从 Mock 环境切换到内网真实环境时，业务代码无需大规模重写。

## 下一步计划

补齐符合要求的 Python 环境后执行后端启动、迁移和测试；继续以 Mock 输出验证任务状态流转。""",
    },
    {
        "day": 6,
        "record_date": date(2026, 7, 22),
        "title": "MVP 范围、真实接入边界与离线交付方案",
        "tags": "MVP,Ansible,服务运维,适配器,Docker,离线部署",
        "content": r"""## 当天目标

继续拆解运维工具需求，明确 MVP 范围、真实环境接入边界和离线交付准备项。

## 完成事项

* 进一步梳理现有 `services.sh` 和 Ansible 脚本可能提供的能力。
* 明确 MVP 优先支持服务列表与状态查看、单个及批量服务操作、主机视角查询、服务拓扑、任务执行记录，以及 stdout、stderr 和退出码展示。
* 确认 `ops_adapter.sh` 当前只实现协议骨架和 Dry Run，真实命令映射等待进入内网、确认实际脚本参数后再补充。
* 规定项目报告需严格区分“已实现、已自动化测试、已模拟验证、等待内网真实验证”。
* 评估 LangGraph 与复杂 Agent 工作流的必要性；当前优先保证确定性运维流程、权限控制和可审计任务执行。
* 讨论外网开发、Docker 打包、离线导入内网操作机的交付方式。

## 遇到的问题

目前只有部分脚本截图，缺少完整业务脚本和真实命令参数；服务器、堡垒机、账号权限和 inventory 配置也尚未明确，内外网运行环境可能存在差异。

## 解决思路

先通过适配器接口稳定前后端协议，用 Mock 数据和模拟输出验证任务状态流转。进入内网后，只替换执行器、适配脚本和环境配置；Docker 镜像之外还应准备配置模板、启动脚本、镜像校验值和部署说明。

## 当天收获

MVP 的重点是建立安全、可替换、可审计的执行链路，而不是一次性覆盖所有运维能力。真实业务逻辑不完整时，固定协议比猜测脚本参数更可靠。

## 下一步计划

继续完善 Dry Run 的任务协议和模拟输出，并准备离线镜像与部署材料清单。""",
    },
    {
        "day": 7,
        "record_date": date(2026, 7, 23),
        "title": "Windows 与 Docker 离线部署环境排查",
        "tags": "Windows 10,WSL2,Docker,CPU虚拟化,离线部署",
        "content": r"""## 当天目标

排查 Windows 10、WSL2、Docker 与 CPU 虚拟化条件，为内网离线部署做准备。

## 完成事项

* 梳理 Windows 10 安装 WSL2 的完整流程，并检查不同机器的 CPU 虚拟化状态。
* 确认内网操作机已支持并开启虚拟化，可作为 Docker 运行环境。
* 排查联想开天 N80Z BIOS 中虚拟化选项不易定位的问题，并分析未开启虚拟化时 Docker Desktop 与 WSL2 的限制。
* 讨论替代交付路径：在外网个人电脑完成开发和 Linux 镜像构建，导出离线镜像文件，经安全介质传入内网操作机后加载并启动。
* 讨论对项目脱敏后上传 GitHub，再由外网开发机完成构建的可行性。

## 遇到的问题

部分机器的 BIOS 虚拟化选项难以确认；没有开启 CPU 虚拟化的设备无法满足 Docker Desktop 和 WSL2 的运行条件，也不适合作为构建环境。

## 解决思路

将“构建镜像”和“运行镜像”分离：不依赖问题机器构建，在具备条件的外网开发机生成 Linux 镜像并导出；内网操作机只承担镜像加载和启动。传输前保持项目脱敏，并按公司安全要求使用安全介质。

## 当天收获

离线部署的可行性不仅取决于代码，还取决于虚拟化能力、操作系统组件、镜像格式和传输流程。提前验证运行环境可以避免把部署问题误判为应用问题。

## 下一步计划

在已开启虚拟化的内网操作机上验证镜像导入与启动流程，并补充离线部署说明和校验步骤。""",
    },
    {
        "day": 8,
        "record_date": date(2026, 7, 27),
        "title": "进入内网环境，梳理运维平台真实执行链路",
        "tags": "运维开发,Ansible,FastAPI,内网环境,权限设计,实习记录",
        "content": r"""## 今日工作概览

**日期：** 2026-07-27<br />
**岗位：** 运维开发 / AI 应用开发实习生<br />
**项目：** CNP 服务器运维管理平台<br />
**工作状态：** 内网环境梳理与协议确认

我进入无外网的内网操作环境，重点核对运维平台与真实服务器环境之间的连接方式，以及 Ansible 调用链路。

## 完成事项

* 梳理 Windows 10 无网操作机、Linux Ansible 控制节点和被管理业务服务器三类节点的职责。
* 检查目标业务服务器后发现其本身没有可直接使用的 `ansible-playbook`，据此判断 Ansible 不应直接在业务服务器执行。
* 整理平台预期调用链：`Web 前端 → FastAPI 后端 → Task Service → Executor → Linux Ansible 控制节点 → 目标业务服务器`。
* 初步梳理用户、密码、组织架构和直属上下级等基础管理需求，并思考它们与运维权限、告警分派、审批流程的关系。
* 明确外网 Codex 修改的脱敏代码进入内网后需要人工同步，后续需保留完整文件变更清单。

## 遇到的问题

真实的 Ansible 执行节点尚未完全确认；操作机、控制节点和业务服务器的职责边界仍需继续核实。外网代码不能直接同步到内网，也容易带来版本不一致；真实路径和命令参数不完整，不能提前写死。

## 分析与处理思路

我继续将执行层抽象为可替换的 Executor，所有 SSH、Ansible、脚本路径和资产信息均通过配置注入。外网只处理脱敏代码与协议设计，不接触真实环境参数；确认控制节点后，再从只读状态查询与 Dry Run 开始验证。

## 今日收获

企业运维平台不是前端按钮直接调用 Shell 命令。先厘清操作机、控制节点和业务服务器的角色，才能正确处理权限、网络、配置和审计边界。

## 后续计划

继续确认真实 Ansible 控制节点和只读查询入口，并将每次外网修改整理为便于内网人工同步的文件级清单。""",
    },
    {
        "day": 9,
        "record_date": date(2026, 7, 28),
        "title": "确认 Ansible 控制节点，协助梳理蓝鲸监控告警流程",
        "tags": "运维开发,Ansible,蓝鲸监控,告警中心,智能体,实习记录",
        "content": r"""## 今日工作概览

**日期：** 2026-07-28<br />
**岗位：** 运维开发 / AI 应用开发实习生<br />
**项目：** CNP 服务器运维管理平台、蓝鲸监控告警<br />
**工作状态：** 控制节点确认与告警流程梳理

我继续确认 Ansible 控制节点，同时协助了解蓝鲸监控告警环境及告警处理流程。

## 完成事项

* 在 Linux 控制节点确认 `ansible-playbook` 位于用户目录下的 `.local/bin`，明确后续需配置完整绝对路径。
* 进一步确认当前拓扑为 `Windows 无网操作机 → 运维管理平台 → Linux Ansible 控制节点 → 业务服务器`；当前先在 Windows 测试，但架构不限定只能部署在 Windows。
* 协助梳理蓝鲸监控告警链路：指标采集、规则匹配、告警产生、通知、分派、负责人确认、处理与关闭。
* 梳理服务负责人、部门、值班人员、直属上级和升级通知对象与告警分派的关联，并初步考虑将蓝鲸告警事件接入运维智能体。

## 遇到的问题

`ansible-playbook` 不一定在系统 PATH 中，直接调用可能失败；部分真实脚本参数和 Inventory 配置仍待内网确认。告警系统与服务资产、负责人、组织数据尚未完全打通，智能体也不能直接根据告警执行生产命令。

## 分析与处理思路

将 Ansible 可执行文件路径配置化，并通过 `/ready` 或环境检查接口确认执行环境。告警接收先用脱敏样本和模拟事件验证，智能分析与真实执行严格解耦；高风险操作必须经过权限校验、人工审批和审计记录。

## 今日收获

监控系统负责发现问题，告警中心负责组织问题，智能体辅助理解问题，Executor 才执行受控操作。几部分必须分层，不能让大模型直接控制生产环境。

## 后续计划

继续补充执行环境检查项，梳理告警事件、服务资产与组织负责人之间的数据映射。""",
    },
    {
        "day": 10,
        "record_date": date(2026, 7, 29),
        "title": "完善只读安全边界，验证运维执行器异常场景",
        "tags": "运维开发,安全设计,Mock Executor,千问大模型,Python,实习记录",
        "content": r"""## 今日工作概览

**日期：** 2026-07-29<br />
**岗位：** 运维开发 / AI 应用开发实习生<br />
**项目：** CNP 服务器运维管理平台、运维智能体<br />
**工作状态：** 本地模拟验证与安全边界完善

我继续完善执行安全边界，并用模拟脚本检查执行器在异常场景下的行为。

## 完成事项

* 明确第一阶段只开放服务状态查询；前端暂时禁用启动、停止等写操作入口，后端对未开放写操作返回 `403`，并保留用户请求、任务状态和执行结果的审计记录。
* 对 `LocalServicesExecutor` 进行模拟验证，覆盖服务运行、已停止、主机不可达、非零退出码、超时和参数注入防护等场景。
* 确认 `command_profile=pending-confirmation` 时系统会在真实执行前安全终止，执行配置未确认时 `/ready` 返回未就绪。
* 明确当前仅属于本地模拟、Fake Script 和安全边界验证，尚未接入真实 `services.sh`、Inventory 或生产资产。
* 参与运维智能体方案梳理，明确内网千问主要用于告警解释、日志总结、知识检索、排障建议和结构化处理报告，不能自由拼接或执行 Shell 命令。

## 遇到的问题

真实脚本输出格式尚未完全确认，Mock 输出可能与真实脚本存在差异；大模型生成建议也有幻觉和越权风险，只在前端关闭按钮不足以保障安全。

## 分析与处理思路

我保留 `MockExecutor`、`LocalScriptExecutor`、`SshScriptExecutor` 和多种 Output Parser 的可替换设计；所有工具参数经过 Schema 校验，命令采用白名单和固定参数映射，写操作必须经后端权限校验。

## 今日收获

运维智能体的价值不是自动执行更多命令，而是在可控风险下帮助人收集证据、理解告警和生成建议。真实执行必须保持确定性、可审计、可回滚。

## 后续计划

待内网确认真实脚本协议后，继续完善 Parser，并开展只读状态查询链路验证。""",
    },
    {
        "day": 11,
        "record_date": date(2026, 7, 30),
        "title": "完成 Linux 离线交付准备，参与金融对话智能体研发",
        "tags": "Docker,Linux,离线交付,Codex,FICC,金融科技,智能体,实习记录",
        "content": r"""## 今日工作概览

**日期：** 2026-07-30<br />
**岗位：** 运维开发 / AI 应用开发实习生<br />
**项目：** CNP 服务器运维管理平台、中汇亿达对话机器人智能体<br />
**工作状态：** 交付材料准备与业务学习

我完成运维平台 Linux 离线交付相关的代码、配置和文档准备，同时参与金融业务与对话机器人智能体的学习和研发。

## 完成事项

* 完成交付所需的 `backend/Dockerfile`、`frontend/Dockerfile`、`docker-compose.yml`、`scripts/export-images.sh`、`scripts/import-images.sh` 和 `docs/DOCKER-OFFLINE-DEPLOY.md` 等材料准备。
* 区分 API、Worker、Web 的镜像、命令、日志和生命周期；生产配置默认运行构建镜像，开发 profile 挂载源码，配置、SQLite 数据和日志使用外部挂载。
* 内部脚本目录按只读方式挂载，未将真实业务脚本、SSH 密钥、证书或密码打进镜像。
* 重建 Python 虚拟环境，并完成已提供的验证记录：Python 3.13.14、后端 Pytest `144 passed, 1 warning`、Ruff、compileall、前端 typecheck、lint、`3 passed` 测试、build、`pip check`、Shell 语法、Compose YAML 与 `git diff --check` 均通过。
* 初步学习国内银行间金融市场、FICC 与量化分析基础；参与“中汇亿达”对话机器人智能体研发，了解问题理解、知识检索、多轮上下文、结构化回答与敏感信息保护。

## 遇到的问题

当前机器没有可用 Docker Socket 或 Compose v2，无法实际执行 Docker build、save、load 和内网启动；外网构建与内网运行环境可能有差异。金融术语和流程也需要持续理解，智能体不能只追求回答通顺。

## 分析与处理思路

我计划在具备条件的外网环境完成镜像构建与导出，并生成 SHA256 校验文件，再在隔离环境模拟导入；内网加载后仍需验证环境变量、挂载路径和健康检查。金融智能体采用知识库检索、证据引用与结构化输出约束，对不确定问题不让模型自由编造。

## 今日收获

技术交付包含代码之外的镜像、配置模板、导入导出脚本、校验、部署文档和回滚说明。参与金融智能体也让我更明确：业务知识是 AI 系统准确落地的重要基础。

## 后续计划

在具备 Docker 条件的机器上补做镜像构建与离线导入测试，并继续参与金融对话智能体研发和业务知识学习。""",
    },
    {
        "day": 12,
        "record_date": date(2026, 7, 31),
        "title": "完善 Ubuntu 开发环境，复盘内外网智能体开发模式",
        "tags": "Linux,Ubuntu,驱动,Docker,Codex,千问大模型,蓝鲸监控,实习记录",
        "content": r"""## 今日工作概览

**日期：** 2026-07-31<br />
**岗位：** 运维开发 / AI 应用开发实习生<br />
**项目：** 开发环境建设、CNP 服务器运维管理平台<br />
**工作状态：** 环境排查与本周复盘

我继续搭建 Ubuntu 双系统开发环境，排查图形显示、工具和依赖问题，并复盘本周的内外网智能体开发模式。

## 完成事项

* 用 `xrandr` 检查显示输出，发现当前 XWayland 最高只识别到 1024×768；初步判断与显卡驱动、显示模式识别、XWayland 或内核启动参数有关，而不只是桌面缩放。
* 检查并准备 Python 3.13、Git、GitHub CLI、VS Code、Node.js、Codex CLI 和 Docker 等 Ubuntu 开发工具，梳理 `.deb`、`.rpm`、AppImage 的适用场景及 Node.js、Codex CLI 的版本依赖。
* 明确外网 Codex 用于脱敏代码的开发、测试、重构、文档和离线交付材料；内网千问用于内部知识问答、告警和脱敏日志推理，并通过受控 Tool Calling 调用内部工具，禁止将敏感数据发送到外网。
* 复盘蓝鲸监控、告警分派、运维智能体和组织权限的闭环：`监控指标 → 蓝鲸告警 → 告警分派 → 智能体收集证据 → 内网千问分析 → 人工确认/审批 → Executor 受控操作 → 审计 → 告警关闭`。

## 遇到的问题

Ubuntu 显示分辨率仍未达到硬件正常水平；Linux 软件安装需区分发行版包格式，Docker 也受虚拟化与运行环境限制。开发环境装好并不代表项目已经在内网部署成功。

## 分析与处理思路

后续继续确认显卡型号、驱动加载和启动日志，优先使用发行版软件源或官方 `.deb` 包；固定 Python、Node、npm 版本，并用 Git 和变更清单控制内外网版本。环境验证拆分为代码、依赖、Docker 构建、离线导入和内网真实验证。

## 今日收获

AI 辅助开发能提高代码实现效率，但真实项目仍离不开环境排查、版本控制、权限管理、业务理解和部署验证。外网 Codex 与内网千问分别承担开发阶段和运行阶段的职责，并非互相替代。

## 后续计划

继续排查 Ubuntu 显示驱动问题，完善开发环境，并推进 Docker 离线导入和内网只读验证。""",
    },
    {
        "day": 13,
        "record_date": date(2026, 7, 31),
        "title": "2026 年第 31 周实习总结：从运维平台到内网智能体闭环",
        "tags": "周总结,运维开发,蓝鲸监控,智能体,Ansible,Docker,Linux,FICC,实习记录",
        "content": r"""## 本周工作概览

**周期：** 2026-07-27 至 2026-07-31<br />
**岗位：** 运维开发 / AI 应用开发实习生<br />
**项目：** CNP 服务器运维管理平台、蓝鲸监控告警、中汇亿达对话机器人智能体<br />
**工作状态：** 内网链路梳理、模拟验证与交付准备

本周我从内网运行环境出发，推进运维平台的执行链路、安全边界和离线交付准备，同时参与告警、智能体和金融业务学习。

## 本周主要工作

* 梳理 Windows 操作机、Linux Ansible 控制节点与业务服务器的调用关系，并在控制节点确认 `ansible-playbook`。
* 将平台第一阶段限定为状态查询，完成 Executor 多种异常场景的模拟验证。
* 协助了解蓝鲸监控告警流程，梳理组织架构、直属上下级、告警分派和升级通知需求。
* 参与运维智能体设计，明确内网千问的运行时职责；完成 Linux 与 Docker 离线交付材料准备及相关自动化验证记录。
* 参与“中汇亿达”对话机器人智能体研发，初步学习银行间金融市场与 FICC 量化基础，并搭建 Ubuntu 开发环境。

## 本周技术进展

我进一步明确 Executor 与 Parser 的解耦方式，隔离状态查询和写操作，并将权限校验和审计放在后端。告警分派需与组织架构关联；蓝鲸告警可为运维智能体提供事件入口，内网千问负责受控 Tool Calling 下的解释和建议，外网 Codex 仅辅助脱敏开发。Docker 离线交付、Python 后端测试和 Linux 环境排查也被纳入同一条交付链路。

## 本周业务收获

我开始理解企业监控告警从发现、分派到关闭的实际流程，也认识到组织关系会影响权限、告警分派和审批。参与金融智能体后，对银行间市场、FICC 和量化分析形成初步认识，并更具体地理解企业对话机器人可以成为业务系统入口，而不只是普通聊天工具。

## 仍待完成与验证

* 尚未完成真实生产服务器写操作验证，真实 `services.sh` 参数和输出格式仍待内网确认。
* 尚未实际完成 Docker 镜像的 build、save、load 和内网启动，也未完成蓝鲸告警与运维智能体的完整生产联调。
* 内网千问对所有告警和日志场景的准确性尚待验证；Ubuntu 显示驱动与分辨率问题仍需排查。
* 对 FICC 和银行间市场目前仍处于初步学习阶段。

## 下周计划

继续确认真实脚本协议和 Inventory，完成状态查询链路的内网只读验证；完善蓝鲸告警事件接入、告警—服务—负责人—组织的数据映射，以及运维智能体的日志分析、知识检索、输出 Schema 和证据引用。同时在具备 Docker 条件的机器上进行镜像构建和离线导入测试，并持续参与对话机器人研发、金融业务学习和 Ubuntu 环境完善。""",
    },
]


CHAPTERS = [
    chapter(2, "Words and Tokens", "高", "精读", 90, "Tokenization 决定实体边界、检索粒度和 LLM 输入表示，是 NER 与实体链接的前置基础。", ["LLM", "NER", "Entity Linking", "KG"], "已完成"),
    chapter(5, "Embeddings", "高", "精读", 92, "Embedding 是 dense retrieval、实体表示、语义匹配和向量检索的核心基础。", ["LLM", "RAG", "KG", "Reasoning"], "已完成"),
    chapter(7, "Large Language Models", "高", "精读", 96, "LLM 是后续 KG-RAG、GraphRAG 与证据增强推理的生成和推理核心。", ["LLM", "Reasoning", "RAG", "KG"], "已完成"),
    chapter(8, "Transformers", "高", "精读", 94, "Transformer 提供上下文建模、注意力机制和 LLM 推理能力的结构基础。", ["LLM", "Reasoning", "RAG"], "已完成"),
    chapter(
        9,
        "Masked Language Models",
        "高",
        "理解",
        88,
        "MLM 训练出的双向上下文表示，是 query NER、实体链接、候选证据召回、reranking 和事实一致性判断的重要基础；它与负责分解和生成的 decoder LLM 形成互补。",
        ["LLM", "IE", "NER", "Entity Linking", "KG-RAG"],
        "已完成",
        positioning="第 9 章建立从双向预训练表示到 NER、实体链接和 KG-RAG 证据判别模块的连接。",
        core_concepts=["Masked Language Model", "BERT", "Bidirectional Encoder", "Contextual Embedding", "BIO Tagging"],
        outline="从双向 Transformer encoder 的可见上下文出发，理解 MLM 的扰动—恢复目标，并连接预训练—微调、分类和 NER 等下游任务。",
        formulas_algorithms="MLM 仅在被选择的掩码位置计算交叉熵：L_MLM = -Σ_{i∈M} log pθ(x_i | x̃)。BERT 的 15% 扰动中，80% 使用 [MASK]、10% 使用随机 token、10% 保持原 token。",
        examples="“苹果发布了手机”与“吃了一个苹果”中的“苹果”具有不同 contextual embedding；在 KG-RAG 中可据此辅助实体类型判断与实体链接。",
        summary="MLM 的价值在于学习适合理解和判别的双向上下文表示。encoder 擅长证据定位与一致性判断，decoder LLM 擅长推理编排与答案生成。",
        mentor_questions=[
            "MLM 与 causal language model 在训练目标、可见上下文和适用任务上有什么差异？",
            "为什么 contextual embedding 能帮助实体消歧和 entity linking？",
            "在 KG-RAG 管线中，encoder 和 decoder LLM 应如何分工？",
        ],
        resources=[
            "Speech and Language Processing, Third Edition draft, Chapter 9",
            "Devlin et al. (2019), BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
            "比较 BERT、RoBERTa、DeBERTa 的预训练策略与下游迁移表现",
        ],
    ),
    chapter(
        10,
        "Post-training",
        "高",
        "精读",
        95,
        "Post-training 决定模型如何使用已有能力：SFT 可教会模型遵守 KG-RAG 的抽取与检索流程，偏好对齐可奖励有证据、路径正确和合理拒答的输出，test-time compute 可加入多跳检索与验证。",
        ["LLM", "Alignment", "Reasoning", "RAG", "KG-RAG"],
        "已完成",
        positioning="第 10 章从后训练与推理时计算两个层面，连接模型行为对齐、证据遵循和知识图谱增强推理。",
        core_concepts=["Instruction Tuning", "Preference Alignment", "Reward Model", "DPO", "Test-Time Compute"],
        outline="依次理解 SFT 的多任务指令学习、偏好对的相对监督、reward model 与 KL 约束、DPO 的直接优化，以及推理阶段的分步计算。",
        formulas_algorithms="偏好概率可写为 P(ow ≻ ol|x)=σ(r(x,ow)-r(x,ol))；对齐目标在期望 reward 外加入相对 reference policy 的 KL penalty，以限制策略偏移。",
        examples="在 KG-RAG 中，SFT 学习抽取—检索—回答流程；偏好数据奖励受证据支撑的答案；推理时通过问题分解、子图检索、路径比较和事实验证增加计算。",
        summary="后训练塑造模型行为而非凭空赋予知识。可靠的知识增强推理需要高质量偏好标准、外部证据验证和显式的推理时搜索。",
        mentor_questions=[
            "Instruction tuning、preference alignment 和 test-time compute 分别改变模型的什么能力？",
            "为什么 reward model 的高分不能保证答案事实正确？",
            "如何把 KG-RAG 的证据路径正确性设计成可训练的偏好或奖励信号？",
        ],
        resources=[
            "Speech and Language Processing, Third Edition draft, Chapter 10",
            "Ouyang et al. (2022), Training language models to follow instructions with human feedback",
            "Rafailov et al. (2023), Direct Preference Optimization",
        ],
    ),
    chapter(
        11,
        "Retrieval-based Models",
        "高",
        "精读",
        98,
        "检索模型直接连接 RAG、KG-RAG 和 GraphRAG：文本与图结构证据的召回、重排、组织和验证，共同决定知识增强推理的可靠性。",
        ["RAG", "KG", "GraphRAG", "Reasoning", "Retrieval"],
        "已完成",
        positioning="第 11 章建立从词法/语义检索到 RAG、KG-RAG 与 GraphRAG 的证据增强生成主线。",
        core_concepts=["BM25", "Dense Retrieval", "Bi-encoder", "Cross-encoder", "RAG"],
        outline="从 sparse retrieval 与倒排索引出发，对比 dense retrieval 的语义匹配能力，再讨论检索评估、RAG 流程、错误诊断与图结构检索。",
        formulas_algorithms="稀疏检索以 tf-idf/BM25 匹配词项；稠密检索以 query/document 向量的 dot product 或 cosine similarity 打分。两阶段系统先 Top-k 召回，再以 cross-encoder 重排。",
        examples="对 KG-RAG 问题，先链接 query 实体并召回相关三元组、邻居和文本段落，再比较候选多跳路径，将受支持的结构化与非结构化证据输入 LLM。",
        summary="RAG 不是单一模型，而是一条可诊断的检索—证据组织—生成链路。需要分别评价召回覆盖、排名质量、上下文噪声、证据遵循和引用一致性。",
        mentor_questions=[
            "Sparse retrieval 与 dense retrieval 各自解决什么问题，为什么 BM25 仍是重要基线？",
            "为什么 bi-encoder 常用于召回、cross-encoder 常用于 reranking？",
            "如何定位一个 KG-RAG 回答错误究竟来自检索、证据组织还是生成？",
        ],
        resources=[
            "Speech and Language Processing, Third Edition draft, Chapter 11",
            "Karpukhin et al. (2020), Dense Passage Retrieval for Open-Domain Question Answering",
            "Lewis et al. (2020), Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        ],
    ),
    chapter(
        17,
        "Sequence Labeling for POS and Named Entities",
        "高",
        "精读",
        97,
        "NER 是知识图谱构建、问题实体识别和实体链接的入口任务；序列级约束有助于产出可链接、可用于图检索的高质量实体边界与类型。",
        ["NER", "KG", "IE", "Entity Linking", "Sequence Labeling"],
        "已完成",
        positioning="第 17 章从序列标注、全局解码和实体级评估出发，连接 NER 与知识图谱构建、实体链接及 KG-RAG。",
        core_concepts=["POS Tagging", "NER", "BIO/BIOES", "HMM", "CRF", "Viterbi"],
        outline="先理解 POS 与 NER 的上下文消歧，再学习 BIO/BIOES 边界编码、HMM 的生成式假设、Viterbi 解码、CRF 的条件概率建模与实体级评估。",
        formulas_algorithms="HMM 使用 transition P(yi|y{i-1}) 与 emission P(xi|yi)；Viterbi 通过动态规划和 backpointer 求最优路径；线性链 CRF 对 P(Y|X) 进行全局序列建模。",
        examples="对问题“苹果公司的创始人是谁？”，NER 识别“苹果公司”为 ORG，entity linking 将其对齐到规范实体，随后 KG-RAG 才能检索创始人关系与证据路径。",
        summary="NER 的边界与类型质量决定实体链接和下游图检索的上限。使用序列级约束和实体级 F1，才能真实衡量可用于知识图谱构建的抽取质量。",
        mentor_questions=[
            "为什么 NER 要使用实体级 F1，而不能只看 token accuracy？",
            "HMM 与 CRF 分别建模什么概率，二者的特征能力有什么差异？",
            "NER、entity linking、relation extraction 在知识图谱构建中如何衔接？",
        ],
        resources=[
            "Speech and Language Processing, Third Edition draft, Chapter 17",
            "Lafferty, McCallum, Pereira (2001), Conditional Random Fields",
            "Lample et al. (2016), Neural Architectures for Named Entity Recognition",
        ],
    ),
    chapter(
        20,
        "Information Extraction",
        "高",
        "精读",
        99,
        "信息抽取将文本转化为实体、关系、事件和时间图，是构建可检索、可追溯知识图谱，并为 KG-RAG 提供结构化证据的核心技术。",
        ["IE", "KG", "Relation Extraction", "Event Extraction", "Temporal Analysis"],
        "已完成",
        positioning="第 20 章把实体识别扩展为关系、事件和时间抽取，构成从文本到知识图谱与事件知识图谱的完整信息抽取主线。",
        core_concepts=["Relation Extraction", "Event Extraction", "Temporal Analysis", "TimeML", "Template Filling"],
        outline="从关系三元组与抽取范式出发，学习事件的 trigger/argument 表示、时间归一化与区间关系，再连接 TimeML 和 schema-guided template filling。",
        formulas_algorithms="关系抽取输出 (head, relation, tail) 并需包含 no_relation；时间区间可用 Allen algebra 表示 before、overlaps、during 等关系；模板填充按 schema 提取场景角色。",
        examples="“某公司于 2025 年发布产品”可抽取发布事件、组织/产品/时间论元，并写入事件节点及时间边；KG-RAG 可据此检索事件路径和原文证据。",
        summary="关系、事件与时间抽取共同将文本事实组织成可推理图结构。可靠系统需要类型/schema 约束、时间归一化、实体/事件消歧与证据可追溯性。",
        mentor_questions=[
            "为什么动态场景通常更适合建模为事件，而不只是多条二元关系？",
            "Distant supervision 的标签噪声来自哪里，如何缓解？",
            "如何把时间归一化和事件关系用于时间敏感的 KG-RAG 问答？",
        ],
        resources=[
            "Speech and Language Processing, Third Edition draft, Chapter 20",
            "Mintz et al. (2009), Distant Supervision for Relation Extraction without Labeled Data",
            "ACE Event Extraction and TimeBank/TimeML annotation resources",
        ],
    ),
    chapter(
        21,
        "Semantic Role Labeling",
        "高",
        "精读",
        92,
        "SRL 将句子转化为谓词—论元事件结构，可辅助事件抽取、证据路径构建和知识图谱增强推理的可解释性。",
        ["IE", "Reasoning", "KG", "Event Extraction", "SRL"],
        "已完成",
        positioning="第 21 章连接浅层语义表示、事件参与结构与知识图谱中的事件节点和角色边。",
        core_concepts=["Semantic Role", "PropBank", "FrameNet", "Selectional Preference", "Predicate-Argument Structure"],
        outline="从语义角色与论元交替出发，对比 PropBank 和 FrameNet，梳理 SRL 的识别—消歧—标注—全局解码流程，并讨论选择偏好与原语分解。",
        formulas_algorithms="SRL 可建模为带 predicate 条件的 BIO 序列标注，并通过全局解码满足论元结构约束；原语分解示例为 KILL(x,y) ⇔ CAUSE(x, BECOME(NOT(ALIVE(y))))。",
        examples="“Doris gave Cary the book”中 Doris/AGENT、book/THEME、Cary/GOAL 可映射为发布或转移事件节点连接到各实体的角色边。",
        summary="SRL 提取的不是简单的词法关系，而是可跨句法形式对齐的事件参与结构；它是将文本证据映射为可解释知识图谱事件的有效中间表示。",
        mentor_questions=[
            "SRL 相比 dependency parsing 为事件抽取补充了什么信息？",
            "PropBank 与 FrameNet 的角色体系有何差异，分别适合什么场景？",
            "如何将 SRL 输出映射为可用于 KG-RAG 的事件节点和角色边？",
        ],
        resources=[
            "Speech and Language Processing, Third Edition draft, Chapter 21",
            "Palmer, Gildea, Kingsbury (2005), The Proposition Bank",
            "Gildea, Jurafsky (2002), Automatic Labeling of Semantic Roles",
        ],
    ),
    chapter(
        23, "Coreference Resolution and Entity Linking", "高", "精读", 99,
        "共指消解负责跨句实体归并，实体链接负责知识库 ID 对齐；二者共同保证 GraphRAG 图节点和多跳证据路径的一致性。",
        ["Entity Linking", "KG", "Reasoning", "GraphRAG", "Coreference"], "已完成",
        positioning="第 23 章连接文本内部实体一致性、知识库规范化和 GraphRAG 的跨句多跳证据组织。",
        core_concepts=["Coreference Resolution", "Mention Ranking", "Entity Linking", "Candidate Generation", "Cluster Metrics"],
        outline="从 mention、referent 和 cluster 概念出发，对比共指架构与神经 mention ranking，梳理实体链接候选生成—排序—ID 选择及 cluster 评估。",
        formulas_algorithms="共指模型计算 span/antecedent 分数并以 ε 表示无先行词，传递闭包形成 cluster；实体链接以上下文与实体描述向量的 dot product/cosine similarity 排序候选。",
        examples="“苹果发布了产品。该公司随后……”中“苹果”和“该公司”先聚为 cluster，再链接到规范公司实体，GraphRAG 才能沿发布事件与产品节点检索。",
        summary="共指消解降低图中重复节点，实体链接提供可跨文档复用的规范 ID。必须分别保障 mention recall、候选召回、排序质量与 NIL 处理。",
        mentor_questions=["为什么 entity linking 不能只依赖字符串匹配？", "Mention-pair、mention-ranking 与 entity-based 共指模型各有什么局限？", "共指或实体链接错误会怎样影响 GraphRAG 的多跳检索？"],
        resources=["Speech and Language Processing, Third Edition draft, Chapter 23", "Lee et al. (2017), End-to-end Neural Coreference Resolution", "Wu et al. (2020), Scalable Zero-shot Entity Linking with Dense Entity Retrieval"],
    ),
    chapter(
        3,
        "N-gram Language Models",
        "中",
        "理解",
        58,
        "用于理解 next-token prediction、perplexity、smoothing 等概率语言建模基础；对现代 LLM 是背景知识，对 KG-RAG 则提供生成模型概率基础。",
        ["LLM", "Language Model", "N-gram", "KG-RAG"],
        "已完成",
        positioning="本章使用最简单的统计语言模型 n-gram，引出如何根据上下文预测下一个 token、如何为句子分配概率、如何评价模型，以及如何处理未见序列。",
        core_concepts=["Language Model", "N-gram", "Markov Assumption", "MLE", "Perplexity", "Smoothing", "Interpolation"],
        outline="从语言模型任务出发，先用链式法则分解句子概率，再用 Markov assumption 将完整历史近似为固定窗口，并通过 MLE、perplexity、smoothing 和 interpolation 理解统计语言模型的基本问题。",
        formulas_algorithms="Bigram MLE: P(w_t|w_{t-1}) = C(w_{t-1}, w_t) / C(w_{t-1})；Perplexity: PP(W) = P(w_{1:T})^{-1/T}；Laplace smoothing: P(w_t|w_{t-1}) = (C(w_{t-1}, w_t)+1)/(C(w_{t-1})+V)。",
        examples="训练语料包含“查询 华为 创始人”和“查询 华为 总部”时，trigram 模型在看到“查询 华为”后可根据计数预测“创始人”或“总部”；若“查询 华为 CEO”未出现，MLE 概率为 0，平滑后获得较小的非零概率。",
        summary="n-gram 是基于局部共现计数的经典语言模型。它简单、可解释、训练快，但只能使用短上下文，存在严重数据稀疏，无法学习语义相似性、结构化三元组、证据验证或多跳推理。",
        mentor_questions=[
            "为什么 n-gram 只使用有限上下文？",
            "为什么需要 smoothing？",
            "n-gram 与 LLM 的核心区别是什么？",
        ],
        resources=[
            "Speech and Language Processing, Third Edition draft, Chapter 3 / N-gram Language Models",
            "补充理解：perplexity、Laplace smoothing、interpolation 的直觉和适用边界",
        ],
    ),
    chapter(
        4,
        "Logistic Regression",
        "中",
        "理解",
        62,
        "逻辑回归提供从特征表示、线性打分、sigmoid/softmax 到 cross-entropy 的概率分类基础，也是理解神经网络分类器和 LLM 输出层的直接入口。",
        ["LLM", "Classifier", "Cross-Entropy", "IE"],
        "已完成",
        positioning="逻辑回归是经典监督分类模型，用于建立“输入特征 -> 线性打分 -> 概率 -> 损失 -> 参数更新”的核心机器学习链路。",
        core_concepts=["Feature Representation", "Logit", "Sigmoid", "Softmax", "Cross-Entropy", "Gradient Descent"],
        outline="从文本人工特征表示出发，理解线性 logit、二分类 sigmoid、多分类 softmax、cross-entropy 损失和参数更新，并连接现代 LLM 的词表 logits。",
        formulas_algorithms="Logit: z = w·x + b；Sigmoid: P(y=1|x)=1/(1+exp(-(w·x+b)))；Softmax: P(y=k|x)=exp(z_k)/Σ_j exp(z_j)；二分类 CE: L=-[y log ŷ+(1-y)log(1-ŷ)]；one-hot 多分类 CE: L=-log ŷ_c。",
        examples="对“乔布斯创立了苹果公司”进行关系分类时，可用“是否包含创立”、实体类型和实体距离等特征，为 founder_of、works_for、located_in 计算 logits，再经 softmax 选择 founder_of。",
        summary="逻辑回归结构简单、训练快、能输出概率且权重有一定可解释性，适合作为分类 baseline；局限是线性模型依赖特征设计，难以自动理解复杂词序、语义组合、否定和长距离依赖。",
        mentor_questions=[
            "sigmoid 和 softmax 有什么区别？",
            "cross-entropy 的直觉是什么？",
            "逻辑回归与 Transformer 分类器有什么联系？",
        ],
        resources=[
            "Speech and Language Processing, Third Edition draft, Chapter 4",
            "补充理解：softmax、cross-entropy 与 LLM vocabulary logits 的关系",
        ],
    ),
    chapter(
        6,
        "Neural Networks",
        "中",
        "理解",
        72,
        "神经网络把传统 feature engineering 推进到 representation learning，是 embedding、Transformer、LLM 和神经信息抽取模型的基础。",
        ["LLM", "Representation Learning", "Embedding", "IE"],
        "已完成",
        positioning="本章是从传统分类模型过渡到 Transformer 和 LLM 的基础章节，核心变化是在输入和输出之间加入隐藏层，自动形成任务相关内部表示。",
        core_concepts=["Neural Unit", "Feedforward Network", "Hidden Representation", "Activation Function", "Backpropagation", "Pooling"],
        outline="先从 neural unit 和单隐藏层分类网络理解前向传播，再理解非线性激活为什么必要，最后以 backpropagation 和参数更新连接端到端训练。",
        formulas_algorithms="Neural unit: z=w·x+b, a=g(z)；Single hidden layer: h=g(Wx+b), z=Uh+c, ŷ=softmax(z)；Forward: a^[i]=g^[i](W^[i]a^[i-1]+b^[i])；Update: W←W-η∂L/∂W。",
        examples="对“任正非创立了华为”做关系分类时，模型可从 token embedding 经隐藏层学习人物、组织和“创立”的组合表示，再通过 softmax 输出 founder_of 0.88 等类别概率，形成候选三元组。",
        summary="神经网络能自动学习特征、建模非线性关系并端到端训练；局限是需要更多数据和计算、可解释性较弱，普通 MLP 也无法自然处理长序列、图结构和显式多跳推理。",
        mentor_questions=[
            "神经网络为什么比逻辑回归更强？",
            "为什么不能只堆叠线性层？",
            "反向传播的作用是什么？",
        ],
        resources=[
            "Speech and Language Processing, Third Edition draft, Chapter 6",
            "补充理解：XOR、representation learning、pooling 与 concatenation 的取舍",
        ],
    ),
    chapter(
        18,
        "Context-Free Grammars",
        "中",
        "理解",
        52,
        "CFG 提供传统 NLP 中语言层次结构的形式化表示，可辅助理解句法分析、关系抽取候选结构和早期信息抽取流程。",
        ["CFG", "Parsing", "IE", "KG"],
        "已完成",
        positioning="CFG 是传统 NLP 中描述句法结构的重要方法，用于说明词如何组成短语、短语如何组成完整句子；相比 n-gram 关注词序列概率，CFG 关注层次结构。",
        core_concepts=["Context-Free Grammar", "Parse Tree", "Parsing", "Constituency", "Production Rule"],
        outline="理解 CFG 的四元组 G=(N,Σ,R,S)，再通过 S -> NP VP 等产生规则理解 parse tree、constituency 和 parsing 如何辅助发现 subject-verb-object 等候选结构。",
        formulas_algorithms="CFG: G=(N,Σ,R,S)，其中 N 是非终结符，Σ 是终结符，R 是产生规则，S 是开始符号；本阶段只需理解它是规则系统，不做完整形式语言推导。",
        examples="“Steve Jobs founded Apple.” 可被分析为 NP + VP，并进一步识别 subject + verb + object，辅助形成候选关系 (Steve Jobs, founder_of, Apple)。",
        summary="CFG 可解释、能表达层次结构，适合规则明确场景；局限是规则难覆盖真实语言、不理解语义、难处理复杂歧义，也不能直接完成知识推理。",
        mentor_questions=[
            "CFG 为什么重要？",
            "CFG 和 LLM 区别？",
            "CFG 能直接生成知识图谱吗？",
        ],
        resources=[
            "Speech and Language Processing, Third Edition draft, Chapter 18",
            "补充理解：constituency parsing 与信息抽取候选结构的关系",
        ],
    ),
    chapter(
        19,
        "Dependency Parsing",
        "中",
        "理解",
        68,
        "依存分析直接建模 head-dependent、谓词、主语、宾语和修饰关系，比 CFG 更贴近关系抽取中的谓词—论元结构。",
        ["Dependency Parsing", "IE", "KG", "Relation Extraction"],
        "已完成",
        positioning="Dependency Parsing 将句子表示为词与词之间的有向依存关系。相比 CFG 的短语层次结构，依存句法直接连接中心词与依存词，更容易呈现谓词、主语、宾语和修饰语之间的关系。",
        core_concepts=["Head-Dependent", "Dependency Relation", "Dependency Tree", "Projectivity", "Transition-based Parsing", "Graph-based Parsing", "UAS", "LAS"],
        outline="先理解依存边如何连接 head 与 dependent，再区分 dependency relation、dependency tree 和 projectivity；方法上了解 transition-based parsing 与 graph-based parsing，评价上掌握 UAS 与 LAS。",
        formulas_algorithms="依存结构可写为 G=(V,A)，V 是 token 节点，A 是有向依存边；graph-based parsing 目标为 T_hat=argmax_{T∈T(S)} Score(T,S)；UAS=head 正确 token 数/token 总数，LAS=head 和 label 都正确 token 数/token 总数。",
        examples="“任正非于1987年创立了华为。”的核心依存结构可表示为：创立 -nsubj-> 任正非，创立 -obj-> 华为，创立 -obl-> 1987年。",
        summary="依存解析比 CFG 更贴近关系抽取，因为实体关系通常由谓词—论元结构表达。本章当前笔记已覆盖核心概念、两类解析方法、评价指标和简单例子，优点局限及 KG-LLM 扩展联系待后续补充。",
        mentor_questions=[
            "Dependency Parsing 与 CFG 的表示重点有什么区别？",
            "UAS 和 LAS 分别评价什么？",
            "为什么依存结构对关系抽取更直接？",
        ],
        resources=[
            "Speech and Language Processing, Third Edition draft, Chapter 19",
            "补充理解：Universal Dependencies、transition-based parsing 与 graph-based parsing",
        ],
    ),
    chapter(24, "Discourse Coherence", "中", "理解", 57, "篇章连贯性影响多文档证据组织和长上下文推理。", ["Reasoning", "RAG"]),
    chapter(25, "Conversation and its Structure", "中", "理解", 50, "对导师问答、对话式检索和多轮研究助手有背景价值。", ["LLM", "Reasoning"]),
    chapter(12, "Machine Translation", "低", "略读", 40, "主要作为 seq2seq 和 attention 发展背景，非当前 KG-RAG 主线。", ["LLM"]),
    chapter(13, "RNNs and LSTMs", "低", "略读", 38, "作为序列建模历史背景，帮助对比 Transformer。", ["LLM"]),
    chapter(14, "Phonetics and Speech Feature Extraction", "低", "略读", 20, "语音特征与当前文本 KG-LLM 方向关联较弱。", ["Speech"]),
    chapter(15, "Automatic Speech Recognition", "低", "略读", 26, "可作为语音到文本入口了解，不是当前阅读重点。", ["Speech", "LLM"]),
    chapter(16, "Text-to-Speech", "低", "略读", 18, "与当前知识图谱和大模型推理方向关联较弱。", ["Speech"]),
    chapter(22, "Lexicons for Sentiment, Affect, and Connotation", "低", "略读", 34, "情感词典可作为 IE 的特殊知识资源了解。", ["IE", "KG"]),
]


NOTE_TEMPLATE = """# {number} {title}

## 章节定位
{positioning}

## 核心概念
- 

## 内容梳理
- 

## 公式与算法解释
- 

## 例子说明
- 

## 重点总结
- 

## 导师可能提问
- {question}

## 我的学习笔记
- 

## 和研究方向的联系
{relation}

## 后续补充资料
- 
"""


def seed() -> None:
    Base.metadata.drop_all(bind=engine)
    init_db()
    db = SessionLocal()
    try:
        source = Source(
            id=1,
            title="Speech and Language Processing, Third Edition draft",
            type="book",
            author_or_origin="Dan Jurafsky and James H. Martin",
            research_direction="LLM, RAG, KG, GraphRAG, IE, Entity Linking, Knowledge Graph Reasoning",
            description="默认内置的 NLP 重点阅读路线，围绕知识图谱、大语言模型推理、KG-RAG、GraphRAG、信息抽取和实体链接组织章节。",
            status="进行中",
            priority="高",
        )
        db.add(source)
        db.flush()
        for item in CHAPTERS:
            chapter_obj = Chapter(**item)
            db.add(chapter_obj)
            db.flush()
            db.add(
                Note(
                    source_id=source.id,
                    chapter_id=chapter_obj.id,
                    title=f"{chapter_obj.number} {chapter_obj.title} 阅读笔记",
                    content=NOTE_CONTENT_BY_NUMBER.get(chapter_obj.number) or NOTE_TEMPLATE.format(
                        number=chapter_obj.number,
                        title=chapter_obj.title,
                        positioning=chapter_obj.positioning,
                        question=chapter_obj.mentor_questions[0],
                        relation=chapter_obj.research_relation,
                    ),
                    tags=",".join(chapter_obj.tags),
                )
            )
        db.add(
            Note(
                source_id=source.id,
                chapter_id=None,
                title="SLP3 第一优先级章节总结：知识图谱增强的大模型推理基础",
                content=PRIORITY_CHAPTERS_SUMMARY,
                tags="SLP3,KG-RAG,GraphRAG,RAG,Knowledge Graph,Summary",
            )
        )
        for record_data in INTERN_RECORDS:
            db.add(InternRecord(**record_data))
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("Seeded SLP3 reading notes data.")
