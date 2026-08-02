# Chapter 19: Dependency Parsing

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
