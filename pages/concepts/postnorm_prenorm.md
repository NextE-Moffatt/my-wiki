# Post-Norm 与 Pre-Norm

_最后更新：2026-04-14_

## 概述  
Post-Norm 与 Pre-Norm 是 Transformer 中残差连接与归一化模块的两种经典顺序设计：Post-Norm 将 LayerNorm 置于残差加法之后，Pre-Norm 则置于之前；二者在训练稳定性、收敛速度与最终性能上存在系统性权衡。

## 详细内容  
- **Post-Norm**（原始 Transformer）：  
  $$
  \mathbf{x}' = \text{LN}(\mathbf{x} + \text{Sublayer}(\mathbf{x}))
  $$  
  优点：最终输出严格归一化，利于下游任务；缺点：梯度易爆炸，需小学习率（$1e-4$）与 warmup（4k steps），训练不稳定（第 6.10.2 节称其 30% 实验 fail）。

- **Pre-Norm**（BERT/LLaMA）：  
  $$
  \mathbf{x}' = \mathbf{x} + \text{Sublayer}(\text{LN}(\mathbf{x}))
  $$  
  优点：梯度流更平滑，支持大 learning rate（$3e-4$）与 zero warmup；缺点：最终输出未归一化，需额外 final LN（LLaMA 添加）。

据第 6.10 节实证结论：
- **收敛速度**：Pre-Norm 在 100B token 内达到目标 loss 的速度比 Post-Norm 快 2.3×；
- **稳定性**：Pre-Norm 实验失败率 < 2%（vs Post-Norm 的 28%）；
- **最终性能**：在 300B token 预训练后，Pre-Norm 模型在 MMLU 上高 0.9%，但在 Wikitext-103 perplexity 上低 0.3（因输出未约束）。

现代实践（如 LLaMA-2）采用 **Pre-Norm + Final LN**：主干用 Pre-Norm 保稳定，末层加 LN 保输出质量。

## 相关页面  
[[normalization]] [[transformer_architecture]] [[llama]] [[bert]] [[residual_connection]]

## 来源  
《百面大模型》，第 6 章 6.10 节（pp. 184–186），2025 年出版