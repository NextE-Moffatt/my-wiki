# Multi-token Prediction

_最后更新：2026-04-14_

## 概述  
Multi-token Prediction（MTP）是一种训练目标扩展技术，要求模型在每个时间步 $t$ 预测未来 $k$ 个连续 token（$x_{t+1}, ..., x_{t+k}$），而非传统因果 LM 的单 token 预测，旨在提升长程依赖建模效率与推理吞吐。

## 详细内容  
### 核心机制  
- **目标函数**（13.1.3）：  
  $$
  \mathcal{L}_{\text{MTP}} = -\frac{1}{T} \sum_{t=1}^{T-k} \log p(x_{t+1:t+k} \mid x_{\leq t})  
  $$  
  其中 $p(x_{t+1:t+k} \mid x_{\leq t}) = \prod_{i=1}^k p(x_{t+i} \mid x_{\leq t+i-1})$，即仍基于自回归分解，但梯度回传覆盖 $k$ 步  
- **训练实现**：在标准 causal LM loss 基础上，对每个位置 $t$ 的 logits 取 top-$k$ 个输出 slice，拼接为 $(k \times d_{\text{vocab}})$ 向量，与目标序列 $x_{t+1:t+k}$ 计算交叉熵  
- **推理适配**：支持原生 MTP 解码（一次前向生成 $k$ token）或兼容单 token 模式（仅用首 token）；DeepSeek-R1 默认 $k=4$

### 性能与权衡  
- **优势**：  
  - 减少自回归步数 → 推理延迟降低：在 4K 上下文生成 512 token 时，MTP-4 比 baseline 快 3.2×（实测于 A100）  
  - 更强长程建模：PG-19 测试集上，MTP 模型的 8K 位置 attention entropy 比 baseline 低 18.7%，表明更聚焦关键远距 token  
- **挑战**：  
  - 训练显存增加：$k$ 倍 logits 存储 → $k=4$ 时显存 +15%（需梯度检查点缓解）  
  - 错误传播：单步预测错误会污染后续 $k-1$ 步，需更强正则（如 label smoothing=0.1）

## 相关页面  
[[models/deepseek_r1]] [[concepts/causal_lm]] [[concepts/emergent_ability]] [[tools/flashattention]] [[concepts/decoder_only_architecture]]

## 来源  
《百面大模型》，第 13.1.3 节 “多词元预测”，p. 351