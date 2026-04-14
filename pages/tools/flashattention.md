# FlashAttention

_最后更新：2026-04-14_

## 概述  
FlashAttention 是一种 IO-aware 的高效注意力算法（Dao et al., 2022），通过分块计算与 HBM 重用，消除冗余内存读写，在保持数学等价性前提下加速注意力计算（p. 297，★★★★☆）。

## 详细内容  
### 核心优化（12.3）  
- **分块（Tiling）**：将 $Q,K,V$ 划分为 $(B_q \times d), (B_k \times d), (B_v \times d)$ 块，避免全量 $QK^\top$ 矩阵存入 HBM  
- **重计算（Recomputation）**：不存储中间 softmax 输出 $S$，而是在 backward 时重新计算 $S$，节省 $O(L^2)$ 显存  
- **数学等价性保证**：  
  Forward: $O = \text{softmax}(QK^\top/\sqrt{d})V$  
  FlashAttention 计算等价于：  
  $$
  O_i = \sum_j \text{softmax}_j\left( \frac{Q_i K_j^\top}{\sqrt{d}} \right) V_j,\quad \text{with log-sum-exp stabilization}
  $$  
  即分块 softmax 与全局 softmax 数值一致（误差 < 1e-5）

### 性能数据  
- 在 A100 上，序列长 2K 时，FlashAttention-2 比 PyTorch SDPA 快 2.1×，显存减少 45%  
- 对 DeepSeek-R1（d=5120），FlashAttention-2 使 prefill 阶段延迟从 142ms 降至 63ms（batch=1）

## 相关页面  
[[tools/flashattention]] [[concepts/attention_mechanism]] [[models/deepseek_r1]] [[concepts/kv_cache_optimization]]

## 来源  
《百面大模型》，第 12.3 节 “FlashAttention”，p. 297