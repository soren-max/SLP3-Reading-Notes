# Chapter 4: Logistic Regression

## 章节定位

本章介绍 Logistic Regression——自然语言处理中最经典的监督学习分类模型之一。它广泛应用于文本分类、情感分析、垃圾邮件检测等任务。虽然现代深度学习模型已经成为主流，但 Logistic Regression 仍然是理解神经网络分类器、Softmax 输出层以及监督学习基本思想的重要基础。

## 核心概念

- **Logistic Regression**：经典的监督学习分类模型，在 NLP 中广泛用于文本分类、垃圾邮件检测、情感分析等任务
- **线性函数**：模型首先通过线性函数计算样本得分
- **Sigmoid 函数**：将线性得分映射到 [0,1] 区间，转换为类别概率
- **Feature Engineering（特征工程）**：传统机器学习的重要组成部分，模型依赖人工设计的特征
- **判别式模型（Discriminative Model）**：直接学习输入与类别之间的映射关系

## 内容梳理

1. Logistic Regression 的基本思想：线性加权 → Sigmoid → 概率输出
2. 特征工程在传统 NLP 中的重要地位
3. 判别式模型 vs. 生成式模型
4. Logistic Regression 与神经网络的关系
5. 从 Logistic Regression 到现代 LLM 分类头的演进

## 公式与算法解释

**线性得分：**

$$z = w^T x + b$$

其中 w 为权重向量，x 为输入特征，b 为偏置。

**Sigmoid 函数：**

$$P(y=1|x) = \sigma(z) = \frac{1}{1 + e^{-z}}$$

将任意实数映射到 [0,1] 区间，表示属于某一类别的概率。

## 例子说明

**情感分类示例：判断一条电影评论的情感极性**

**人工设计的特征（Feature Engineering）：**

`x = [count(正面词), count(负面词), 评论长度, 是否含感叹号]`

假设训练得到权重 `w = [0.8, -0.6, 0.01, 0.3]`，偏置 `b = -0.2`

**场景 1：** 评论 "这部电影太棒了！强烈推荐！"
- 正面词 2 个（"太棒了", "推荐"），负面词 0 个，长度 6，含 2 个感叹号
- `z = 2×0.8 + 0×(-0.6) + 6×0.01 + 2×0.3 - 0.2 = 1.6 + 0 + 0.06 + 0.6 - 0.2 = 2.06`
- `P(正面) = σ(2.06) ≈ 0.89` → **正面**

**场景 2：** 评论 "难看，浪费时间。"
- 正面词 0 个，负面词 1 个（"难看"），长度 4，含 0 个感叹号
- `z = 0×0.8 + 1×(-0.6) + 4×0.01 + 0×0.3 - 0.2 = -0.6 + 0.04 - 0.2 = -0.76`
- `P(正面) = σ(-0.76) ≈ 0.32` → **负面**

**Sigmoid 映射效果：**
- z=2.06 时 σ≈0.89（高置信度正面）
- z=-0.76 时 σ≈0.32（低置信度正面，即倾向负面）
- z=0 时 σ=0.5（无法判断）

## 重点总结

- Logistic Regression 是经典的监督学习分类模型，在 NLP 中广泛用于文本分类、垃圾邮件检测、情感分析等任务
- 模型首先通过线性函数计算样本得分，再利用 Sigmoid 将得分转换为概率
- Feature Engineering（特征工程）是传统机器学习的重要组成部分，模型依赖人工设计的特征
- Logistic Regression 属于判别式模型（Discriminative Model），直接学习输入与类别之间的映射关系
- 它是后续神经网络、Softmax 分类器和深度学习模型的重要理论基础

## 导师可能提问

**Q1：为什么叫 Logistic Regression，它其实不是分类吗？**

名称中虽然有 Regression，但它利用 Logistic（Sigmoid）函数输出类别概率，因此主要用于分类任务，而不是连续值预测。

**Q2：为什么要使用 Sigmoid？**

线性模型输出可以是任意实数，而分类需要概率。Sigmoid 将任意实数映射到 [0,1] 区间，便于表示属于某一类别的概率。

**Q3：Logistic Regression 和 Linear Regression 的区别？**

Linear Regression 用于预测连续值；Logistic Regression 用于预测类别概率，其输出经过 Sigmoid 映射。

**Q4：Logistic Regression 和神经网络有什么关系？**

单层神经网络（没有隐藏层）在二分类场景下，本质上就是 Logistic Regression；深度神经网络可以看作是在 Logistic Regression 前增加了多层非线性特征学习。

**Q5：为什么现代 LLM 还要学习 Logistic Regression？**

因为现代 Transformer 的分类头、BERT 的下游分类任务以及神经网络输出概率的思想，都继承了 Logistic Regression 的基本原理。

## 我的理解

Logistic Regression 是自然语言处理中最经典的监督学习分类模型之一，广泛应用于文本分类、情感分析、垃圾邮件检测等任务。其核心思想是：首先利用线性函数 z = w^T x + b 对输入特征进行加权求和，然后通过 Sigmoid 函数将线性得分映射到 [0,1] 区间，从而得到类别概率。

与传统基于规则的方法相比，Logistic Regression 能够通过训练数据自动学习各特征的重要性，无需人工编写大量规则。虽然现代深度学习模型已经成为主流，但 Logistic Regression 仍然是理解神经网络分类器、Softmax 输出层以及监督学习基本思想的重要基础。

## 与大语言模型 / AI Agent / RAG 的联系

- **LLM**：Transformer 的分类头（如 BERT 的 [CLS] 向量分类）本质上继承自 Logistic Regression 的线性分类思想
- **AI Agent**：Agent 的任务分类/意图识别模块常基于 Logistic Regression 或 Softmax 分类器
- **RAG**：检索后的结果重排序（Re-ranking）阶段有时仍然使用 LR 或类 LR 模型做二分类判断相关性
