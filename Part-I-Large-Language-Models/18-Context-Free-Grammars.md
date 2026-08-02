# Chapter 18: Context-Free Grammars

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
