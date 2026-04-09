# Attention Is All You Need

_最后更新：2026-04-10_

## 概述

Vaswani et al. 2017 年提出 Transformer 架构，完全基于注意力机制，抛弃了 RNN 和 CNN，在机器翻译任务上取得当时 SOTA，并成为此后 LLM 时代的基础架构。

## 详细内容

### 核心贡献

1. **提出 Transformer**：完全用注意力机制（无递归、无卷积）构建 encoder-decoder 架构
2. **Multi-Head Attention**：允许模型在不同表示子空间上并行关注不同位置
3. **Positional Encoding**：用正弦/余弦函数编码序列位置信息，弥补无递归带来的位置感知缺失
4. **Scale 效率**：相比 RNN 可完全并行化，训练速度大幅提升

### 性能

| 任务 | 指标 | 结果 |
|------|------|------|
| WMT 2014 英→德翻译 | BLEU | 28.4（超过此前最好结果 2+ 点）|
| WMT 2014 英→法翻译 | BLEU | 41.8（仅用 8 卡训练 3.5 天）|

### 架构要点

- **Encoder**：6 层，每层含 Multi-Head Self-Attention + Feed-Forward
- **Decoder**：6 层，额外含 Cross-Attention（attend to encoder 输出）
- **注意力公式**：$\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$
- **Multi-Head**：8 个并行注意力头，$d_{model}=512$

### 历史意义

Transformer 是 BERT、GPT 系列、T5、LLaMA 等几乎所有现代大模型的直接前身。它的提出标志着 NLP 从序列模型时代进入注意力/缩放时代，与 [[bitter_lesson]] 中"通用方法 + 大算力"的论断高度吻合。

## 相关页面

- [[search_and_learning]] — Transformer 是"学习"这一可扩展方法的代表性实现
- [[scaling_computation]] — Transformer 架构是 Scaling Laws 的物质基础
- [[bitter_lesson]] — 放弃手工特征（语言学规则）转向通用架构的典型案例
- [[attention_mechanism]] — 注意力机制概念页（待创建）

## 来源

- Vaswani et al., "Attention Is All You Need", NeurIPS 2017
- arXiv: https://arxiv.org/abs/1706.03762
