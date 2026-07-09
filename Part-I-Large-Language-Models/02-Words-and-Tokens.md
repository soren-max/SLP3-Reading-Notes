---
note_title: "Words and Tokens：LLM 与 KG-RAG 的输入层基础"
source: "Speech and Language Processing, Third Edition draft"
chapter: "Chapter 2: Words and Tokens"
section: "Full Chapter"
priority: "High"
status: "Reading"
tags:
  - LLM
  - Tokenization
  - RAG
  - KG
  - IE
  - NER
  - EntityLinking
  - Reasoning
research_direction: "KG-enhanced LLM Reasoning"
---

# Chapter 2: Words and Tokens

## 1. 章节定位 / Chapter Focus

本章讨论 NLP 系统如何把原始文本转换成可计算的基本单位。传统 NLP 经常从 word 开始，但 word 的边界并不稳定。现代大语言模型通常使用 token 或 subword token 作为输入单位。

This chapter explains how NLP systems convert raw text into computational units. Traditional NLP often starts from words, but word boundaries are not always stable. Modern LLMs usually process tokens or subword tokens instead.

对 KG-RAG 和 GraphRAG 来说，本章是输入层基础。实体识别、关系抽取、事件抽取、实体链接、文档 chunking、向量检索和图节点构建，都依赖稳定的文本切分、规范化和字符串匹配。

For KG-RAG and GraphRAG, this chapter is part of the input-layer foundation. Named entity recognition, relation extraction, event extraction, entity linking, document chunking, vector retrieval, and graph node construction all depend on stable tokenization, normalization, and string matching.

## 2. 核心概念 / Key Concepts

- **Word（词）**：自然语言中的词，但不同语言和任务对词边界的定义不同。
- **Token（标记）**：模型实际处理的文本单位，可以是词、子词、字符或字节。
- **Type（类型）**：词表中的唯一项目，例如语料中出现过的不同 token。
- **Token occurrence（实例）**：token 在语料中的一次具体出现。
- **Morpheme（语素）**：最小有意义语言单位，例如 `un-`、`happy`、`-ness`。
- **Unicode**：跨语言字符编码标准，是多语言文本处理的基础。
- **Normalization（规范化）**：统一大小写、空格、标点、全角半角、Unicode 形式等。
- **Subword tokenization（子词切分）**：将词拆成更小的可复用片段，以处理长尾词、新词和专业术语。
- **Byte-Pair Encoding, BPE**：从字符或字节开始，反复合并高频相邻片段来构建 token vocabulary。
- **Regular expression, regex（正则表达式）**：基于规则的字符串匹配工具，常用于清洗、抽取和格式识别。
- **Minimum edit distance（最小编辑距离）**：衡量两个字符串之间最少编辑操作数的方法，可用于拼写纠错和实体别名匹配。

## 3. Word 与 Token 的区别 / Words vs. Tokens

Word 是语言学和人类阅读中的自然单位，而 token 是模型和算法处理文本时使用的计算单位。二者并不总是一致。

A word is a natural unit for human reading and linguistic analysis, while a token is a computational unit used by models and algorithms. They are not always the same.

英文中虽然有空格，但缩写、连字符、标点、大小写、复合词和专有名词都会带来边界问题。中文、日文、泰文等语言没有稳定的空格分隔，word segmentation 更复杂。社交媒体、代码、医学术语和日志文本还会出现大量非标准字符串。

English has spaces, but abbreviations, hyphens, punctuation, capitalization, compounds, and named entities still create boundary problems. Chinese, Japanese, Thai, and other languages do not always use whitespace to mark word boundaries. Social media, code, biomedical terms, and logs introduce even more non-standard strings.

因此，现代 LLM 通常不直接使用 word vocabulary，而是使用 subword tokenization。这样常见词可以被表示为较少 token，罕见词、新词、拼写变化和专业术语也能被拆成已有片段。

Therefore, modern LLMs usually do not rely on a pure word vocabulary. They use subword tokenization. Frequent words can be represented with fewer tokens, while rare words, new words, spelling variants, and domain terms can still be decomposed into known pieces.

## 4. Tokenization 的作用 / Why Tokenization Matters

Tokenization 不只是预处理步骤，它会影响模型输入、上下文长度、检索召回、实体边界和系统成本。

Tokenization is not just preprocessing. It affects model inputs, context length, retrieval recall, entity boundaries, and system cost.

| 场景 / Scenario | Tokenization 的影响 / Impact |
|---|---|
| LLM 输入 | 文本必须先变成 token IDs，再映射为 embeddings |
| RAG chunking | chunk 长度通常按 token 数控制，而不是字符数 |
| Entity linking | 实体名切分不稳定会降低候选召回率 |
| Information extraction | token 边界错误会影响 NER、关系抽取和事件论元边界 |
| Cost control | token 数直接影响上下文窗口占用、延迟和费用 |
| Multilingual NLP | 不同语言的切分策略会影响公平性和性能 |

## 5. Unicode 与 Normalization

真实系统中的文本来自网页、PDF、数据库、用户输入和 API。即使肉眼看起来相同的字符串，也可能使用不同 Unicode 编码形式。

Text in real systems comes from web pages, PDFs, databases, user inputs, and APIs. Strings that look identical to humans may use different Unicode representations.

常见 normalization 包括：

Common normalization operations include:

- 大小写统一 / case normalization
- 全角半角转换 / full-width and half-width normalization
- Unicode NFC 或 NFKC 规范化 / Unicode NFC or NFKC normalization
- 多余空格清理 / whitespace normalization
- 标点统一 / punctuation normalization
- 别名和缩写归一 / alias and abbreviation normalization

在知识图谱构建中，normalization 尤其关键。例如 `OpenAI`、`Open AI`、`OpenAI Inc.` 和 `OpenAI, Inc.` 可能指向同一实体。如果不做归一化，系统可能把同一实体拆成多个节点。

Normalization is especially important for knowledge graph construction. For example, `OpenAI`, `Open AI`, `OpenAI Inc.`, and `OpenAI, Inc.` may refer to the same entity. Without normalization, a system may create multiple nodes for one real-world entity.

## 6. Subword Tokenization 与 BPE

Subword tokenization 试图在 word-level 和 character-level 表示之间取得平衡。word-level 表示容易遇到 OOV（out-of-vocabulary）问题；character-level 表示覆盖能力强，但序列更长，语义片段不稳定。Subword 方法兼顾覆盖能力和效率。

Subword tokenization balances word-level and character-level representations. Word-level vocabularies suffer from OOV problems. Character-level representations are flexible but create longer sequences and less stable semantic units. Subword methods combine coverage with efficiency.

### 6.1 BPE 基本思想 / Basic Idea of BPE

BPE 从字符或字节开始，反复合并训练语料中最高频的相邻 token pair，直到达到目标词表大小。

BPE starts from characters or bytes and repeatedly merges the most frequent adjacent token pair in the training corpus until the target vocabulary size is reached.

简化算法：

Simplified algorithm:

```text
1. Initialize the vocabulary with characters or bytes.
2. Count all adjacent token pairs in the training corpus.
3. Merge the most frequent pair into a new token.
4. Repeat steps 2 and 3 until the vocabulary reaches the target size.
```

示例：`unhappiness` 可能被切分为：

Example: `unhappiness` may be segmented as:

```text
["un", "happi", "ness"]
```

这说明 BPE 可以复用常见片段，例如 `un` 和 `ness`，同时避免为每个完整词都建立独立词表项。

This shows that BPE can reuse frequent pieces such as `un` and `ness`, while avoiding a separate vocabulary entry for every full word.

## 7. Heaps' Law / 词表增长规律

随着语料规模增大，词表大小会持续增长。这说明固定 word vocabulary 很难覆盖真实世界不断出现的新词、实体名和领域术语。

As corpus size increases, vocabulary size continues to grow. This shows why a fixed word vocabulary struggles to cover new words, entity names, and domain terms in the real world.

Heaps' Law 描述语料 token 总数 \(N\) 与 vocabulary size \(|V|\) 的关系：

Heaps' Law describes the relationship between the total number of tokens \(N\) and the vocabulary size \(|V|\):

$$
|V| = kN^\beta
$$

其中 \(k\) 和 \(\beta\) 是经验常数，通常 \(0 < \beta < 1\)。该规律说明：语料越大，仍然会不断出现新 type。

Here, \(k\) and \(\beta\) are empirical constants, usually with \(0 < \beta < 1\). The law indicates that new types keep appearing as the corpus grows.

## 8. Minimum Edit Distance / 最小编辑距离

Minimum edit distance 用 insertion、deletion、substitution 等操作衡量两个字符串的差异。它常用于拼写纠错、模糊匹配、别名归一和实体链接候选召回。

Minimum edit distance measures the difference between two strings using operations such as insertion, deletion, and substitution. It is useful for spelling correction, fuzzy matching, alias normalization, and candidate retrieval in entity linking.

动态规划递推形式：

Dynamic programming recurrence:

$$
D(i,j) = \min
\begin{cases}
D(i-1,j) + 1 & \text{delete} \\
D(i,j-1) + 1 & \text{insert} \\
D(i-1,j-1) + cost & \text{substitute}
\end{cases}
$$

其中，如果两个字符相同，\(cost = 0\)，否则 \(cost = 1\)。

If the two characters are the same, \(cost = 0\); otherwise, \(cost = 1\).

在 KG-RAG 中，edit distance 可以帮助判断 `OpenAI Inc`、`OpenAI, Inc.` 和 `Open AI` 是否可能是同一实体的不同表面形式。但它只衡量字符串相似度，不能单独决定实体是否相同。

In KG-RAG, edit distance can help decide whether `OpenAI Inc`, `OpenAI, Inc.`, and `Open AI` may be surface forms of the same entity. However, it only measures string similarity and cannot determine entity identity by itself.

## 9. 正则表达式与规则方法 / Regex and Rule-based Methods

在 LLM 时代，regex 和 rule-based tokenization 仍然有实际价值。它们可解释、稳定、成本低，适合处理结构明显的文本。

Even in the LLM era, regex and rule-based tokenization remain useful. They are interpretable, stable, and cheap, especially for text with clear structure.

典型应用包括：

Typical applications include:

- 抽取邮箱、日期、版本号、URL、论文 DOI / extracting emails, dates, versions, URLs, and paper DOIs
- 保护医学实体、基因名、药物名和产品名 / protecting biomedical entities, gene names, drug names, and product names
- 清洗日志、表格和代码片段 / cleaning logs, tables, and code fragments
- 为 LLM 或 RAG 提供高精度候选片段 / providing high-precision candidates for LLMs or RAG systems

## 10. 与 KG-RAG / GraphRAG 的关系

在 KG-RAG 中，用户问题、文档 chunk、实体 mention 和知识图谱节点需要对齐。Tokenization 会影响 query 表示、document embedding、实体候选召回和最终答案质量。

In KG-RAG, user questions, document chunks, entity mentions, and knowledge graph nodes must be aligned. Tokenization affects query representation, document embeddings, candidate entity retrieval, and final answer quality.

在 GraphRAG 中，系统需要从文本中抽取 entity mentions，并将同一实体的不同表述合并为 canonical nodes。Unicode normalization、规则清洗、edit distance 和 embedding similarity 都可以作为实体归一的前置或辅助方法。

In GraphRAG, a system extracts entity mentions from text and merges different surface forms into canonical nodes. Unicode normalization, rule-based cleaning, edit distance, and embedding similarity can all support entity normalization.

| 实体名 / Entity | 普通切分风险 / Tokenization Risk | 系统影响 / System Impact |
|---|---|---|
| `IL-6` | 被拆成 `IL`, `-`, `6` | 生物医学实体召回下降 |
| `GPT-4o` | 被拆成多个片段 | 产品名整体语义丢失 |
| `BRCA1` | 字母和数字边界不稳定 | 基因实体链接错误 |
| `database_connection_timeout` | 被拆得过碎 | 日志检索和故障解释变差 |

## 11. 重点总结 / Key Takeaways

- Word 是人类语言单位，token 是模型计算单位，二者不总是一致。
- Modern LLMs usually use subword tokenization instead of pure word tokenization.
- Unicode normalization 对多来源文本、实体链接和知识图谱构建非常重要。
- BPE 通过合并高频相邻片段构建 subword vocabulary。
- Heaps' Law 说明词表会随着语料规模持续增长，新词和长尾实体不可避免。
- Minimum edit distance 可用于字符串相似度、拼写纠错和实体别名匹配。
- Regex 和 rule-based 方法在抽取、清洗和候选生成中仍然有工程价值。
- Tokenization 会影响 RAG chunking、检索召回、上下文成本和 GraphRAG 节点构建。

## 12. 导师可能提问 / Possible Oral Exam Questions

**Q1: Why do modern LLMs not directly use words as input units?**

因为 word 边界在不同语言和场景中不稳定，而且完整 word vocabulary 无法覆盖不断出现的新词、拼写变化、专业术语和实体名。Subword tokenization 能更好地平衡覆盖能力和计算效率。

Because word boundaries are unstable across languages and domains, and a full word vocabulary cannot cover new words, spelling variants, technical terms, and entity names. Subword tokenization provides a better balance between coverage and efficiency.

**Q2: What is the difference between a word, a character, and a token?**

Word 是语言学意义上的词；character 是单个字符；token 是 tokenizer 输出的模型输入单位，可以是词、子词、字符或字节。

A word is a linguistic unit, a character is a single written symbol, and a token is the model input unit produced by a tokenizer. A token may be a word, subword, character, or byte.

**Q3: What is the basic idea of BPE?**

BPE 从字符或字节开始，反复合并语料中最高频的相邻片段，最终形成可复用的 subword vocabulary。

BPE starts from characters or bytes and repeatedly merges the most frequent adjacent pieces in the corpus, producing a reusable subword vocabulary.

**Q4: Why is normalization important for KG construction?**

同一实体可能有多个表面形式。如果不做 normalization，系统可能把一个真实实体错误地拆成多个 KG 节点。

The same entity may appear in multiple surface forms. Without normalization, a system may incorrectly split one real-world entity into multiple KG nodes.

**Q5: How can minimum edit distance help entity linking?**

它可以衡量 mention 和候选实体名称之间的字符串相似度，用于候选召回或候选排序。但最终判断还需要上下文语义、类型约束和知识库信息。

It measures string similarity between a mention and candidate entity names, which helps candidate retrieval or ranking. Final disambiguation still needs context semantics, type constraints, and knowledge base information.
