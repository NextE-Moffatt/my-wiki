# 注意力机制（Attention Mechanism）

_最后更新：2026-04-10_

## 概述

注意力机制让模型在处理序列时动态地"关注"输入的不同部分，而非均等对待所有位置。是 Transformer 架构的核心组件，也是现代大模型的基础。

## 详细内容

### 基本思想

给定一个查询（Query），在键值对（Key-Value）集合中计算相关性权重，加权求和得到输出。模型自动学习哪些位置之间应该相互关注。

### Scaled Dot-Product Attention

$$\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

- **Q（Query）**：当前位置的"问题"
- **K（Key）**：其他位置的"索引"
- **V（Value）**：其他位置的"内容"
- **$\sqrt{d_k}$ 缩放**：防止点积过大导致 softmax 梯度消失

### Multi-Head Attention

并行运行多个注意力头，每个头学习不同的关注模式，再拼接映射：

$$\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1,...,\text{head}_h)W^O$$

### Self-Attention vs Cross-Attention

| 类型 | Q 来源 | K/V 来源 | 用途 |
|------|-------|---------|------|
| Self-Attention | 序列自身 | 序列自身 | 建模序列内部关系 |
| Cross-Attention | Decoder | Encoder 输出 | 翻译、摘要等 seq2seq 任务 |

### 与 RNN 的对比

| 维度 | RNN | Attention |
|------|-----|-----------|
| 长距离依赖 | 难（梯度消失）| 直接（O(1) 路径长度）|
| 并行化 | 无法并行 | 完全并行 |
| 计算复杂度 | O(n) | O(n²)（序列长度的平方）|

### 后续发展

- **Flash Attention**：IO 感知的高效注意力实现，大幅提升训练速度
- **Multi-Query Attention / GQA**：减少 KV cache，提升推理效率（LLaMA 2/3 使用）
- **稀疏注意力**：Longformer、BigBird 等处理超长序列

## 相关页面

- [[attention_is_all_you_need]] — 提出 Transformer 的原始论文
- [[scaling_computation]] — 注意力机制是大规模计算扩展的关键组件
- [[search_and_learning]] — Transformer 属于"学习"这一可扩展范式

## 来源

- Vaswani et al., "Attention Is All You Need", NeurIPS 2017
