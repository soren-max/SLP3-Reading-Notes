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

## 1. 本章定位

本章讨论 NLP 系统如何把原始文本转换成可计算的基本单位。传统 NLP 常从 word 开始，但 word 的边界并不稳定。现代大语言模型更多使用 token 或 subword token 作为输入单位。

对知识图谱增强大模型推理来说，本章是输入层基础。实体识别、关系抽取、事件抽取、实体链接、RAG 检索和 GraphRAG 节点构建，都依赖稳定的文本切分和字符串规范化。

## 2. 核心概念

- **word**：自然语言中的词，但不同语言和任务中边界不同。
- **token**：模型实际处理的文本单位，可以是词、子词、字符或字节。
- **morpheme**：最小有意义语言单位，可帮助理解词形变化。
- **Unicode**：跨语言字符编码基础，影响多语言文本处理。
- **subword tokenization**：子词切分，解决罕见词、新词和专业术语问题。
- **Byte-Pair Encoding, BPE**：通过合并高频相邻片段构建 token vocabulary。
- **regular expression**：规则匹配工具，可用于文本清洗和候选抽取。
- **minimum edit distance**：字符串相似度方法，可用于实体别名匹配。

## 3. 关键理解

word 不是一个稳定的计算单位。英文中有空格，但缩写、标点、大小写和复合词会带来边界问题。中文等语言没有天然空格，分词更复杂。LLM 选择 subword tokenization，是为了在词级表示和字符级表示之间取得平衡。

BPE 的核心思想是从字符或字节开始，反复合并训练语料中最高频的相邻片段。这样常见词可以用较少 token 表示，罕见词和新词也能被拆成已有子词表示。

Unicode 和 normalization 对真实系统很重要。知识图谱构建常面对多来源文本，同一实体可能因为全角半角、空格、标点、大小写或编码差异被错误地分成多个节点。

regex、rule-based tokenization 和 minimum edit distance 在 LLM 时代仍然有价值。它们可解释、稳定、成本低，适合用于候选实体抽取、日志解析、别名匹配和数据清洗。

## 4. 与 KG-LLM 推理的关系

在 KG-RAG 中，用户问题、文档 chunk 和知识图谱节点需要对齐。tokenization 会影响 query 表示、文档表示和实体匹配。如果实体名被拆分不稳定，retriever 可能召回不到正确证据。

在 GraphRAG 中，系统需要从文本中抽取 entity mention，并把同一实体的不同表述合并为 canonical node。Unicode normalization、规则清洗和 edit distance 是实体归一的重要前置步骤。

在信息抽取中，NER、relation extraction 和 event extraction 都依赖 token 边界。错误切分会影响实体边界判断、关系触发词识别和事件论元抽取。

## 5. 例子

- **实体链接**：`OpenAI`、`Open AI`、`OpenAI Inc.` 可能指向同一实体，需要归一化和别名匹配。
- **KG-RAG**：`IL-6` 如果被切分不合理，可能影响生物医学知识图谱中的实体召回。
- **Agent 日志排障**：`database_connection_timeout` 和 `service-auth-v2` 应该作为重要片段保护，否则会影响检索和排障解释。

## 6. 复习重点

1. 理解 word、token、subword 的区别。
2. 掌握 BPE 的基本训练思想。
3. 理解 Unicode normalization 对实体链接的作用。
4. 知道 regex 和 rule-based 方法在 LLM 系统中的价值。
5. 掌握 minimum edit distance 在实体别名匹配中的用途。
6. 思考 tokenization 如何影响 RAG、GraphRAG 和信息抽取。

---

## 附录：与原版笔记的对应关系

下面是这份笔记中涉及的 Q&A 和公式，用于与教材原文和章节传统笔记对照：

### 导师可能提问

**Q1：为什么现代 LLM 不直接使用 Word？**

因为不同语言对 Word 的定义不统一，新词不断产生，完整词表规模过大，而 Subword Token 能更好地兼顾泛化能力和计算效率。

**Q2：Word、Character、Token 有什么区别？**

- **Word**：语言学中的词。
- **Character**：单个字符。
- **Token**：Tokenizer 切分后的模型输入单位，可以是词、子词或字符。

**Q3：为什么第二章不是 Grammar，而是 Tokens？**

因为现代模型首先处理的是 Token 序列，而不是语法规则。Token 是模型输入的基本单位，也是后续 Embedding 和 Transformer 的基础。传统 NLP 教材往往从词法、语法讲起，但第三版从实际模型处理流程出发，先讲 Token。

**Q4：为什么 Token ID 不能直接输入 Transformer？**

Token ID 只是离散编号，不包含语义信息，需要通过 Embedding 转换成连续向量后才能进行神经网络计算。

**Q5（新增）：BPE 对 RAG 有什么影响？**

BPE 会影响 chunk token 长度、embedding 输入、检索召回和上下文窗口成本。

**Q6（新增）：Minimum Edit Distance 在实体链接中怎么用？**

它可以计算 mention 和知识库实体名的表面相似度，用于候选召回或候选排序。

### 公式与算法

- **Heaps' Law**: $|V| = kN^\beta$，描述语料规模 N 增大时词表规模持续增长，说明固定 word vocabulary 无法覆盖新词和长尾实体。
- **BPE**: 从字符或字节开始，反复合并语料中最高频的相邻 token pair，得到 subword vocabulary。
- **Minimum Edit Distance**: 用 insertion、deletion、substitution 等操作计算两个字符串之间的最小转换代价，可用于实体别名匹配。

### 例子说明

**BPE 切分过程示例（以英文单词 "unhappiness" 为例）：**

假设语料中出现了 "un", "happy", "happiness", "sad", "ness" 等词。

**Step 1 — 初始状态（字符级）：**
```
u n h a p p i n e s s
```
每个字符都是一个独立的 Token。

**Step 2 — 统计相邻对频率：**
假设语料中 "h" + "a" 出现最频繁，合并为 "ha"。

**Step 3 — 继续合并：**
```
u n ha p p i n e s s
```
"p" + "p" 频繁出现 → 合并为 "pp"。

**Step 4 — 逐步合并常见子词：**
多次迭代后，词汇表中可能出现 "un", "happi", "ness" 这样的子词 Token。

**最终切分结果：**
```
["un", "happi", "ness"]
```

**KG-RAG 场景中的 tokenization 影响：**

| 实体名 | 普通 BPE 切分 | 实体保护切分 | 对检索的影响 |
|---|---|---|---|
| IL-6 | `["IL", "-", "6"]` | `["IL-6"]` | 拆碎后可能被误认为 "IL"（伊利诺伊州）+ "6" |
| GPT-4o | `["GPT", "-", "4", "o"]` | `["GPT-4o"]` | 拆碎后丢失 "GPT-4o" 的整体语义 |
| R&D Agent Copilot | `["R", "&", "D", "Agent", "C", "opilot"]` | `["R&D", "Agent", "Copilot"]` | 项目名断裂后检索不到相关资料 |

### 与大语言模型 / AI Agent / RAG 的联系

- **LLM**：不同模型使用不同的 Tokenizer（GPT 系列用 BPE，BERT 用 WordPiece）
- **AI Agent**：Token 消耗直接影响成本（中文约 1.5-2 字符/Token，英文约 0.75 词/Token）
- **RAG**：文档切分策略常与 Tokenizer 对齐，确保检索单元与模型输入粒度匹配
- **GraphRAG**：节点抽取和实体归一依赖稳定的 token 边界和字符串规范化
- **KG-RAG**：查询中的实体名如果被 tokenizer 拆得过碎，可能导致检索召回率下降
