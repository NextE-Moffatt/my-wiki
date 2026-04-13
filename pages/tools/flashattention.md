# FlashAttention

_最后更新：2026-04-13_

## 概述  
FlashAttention 是一种 I/O-aware 的高效注意力计算内核，通过**分块（tiling）、重计算（recomputation）与共享内存融合**，在不牺牲数值精度前提下，将标准 attention 的显存占用从 $O(N^2)$ 降至 $O(N)$，吞吐量提升 2–4×，成为现代 LLM 训练/推理的事实标准加速器。

## 详细内容  

### 1. 核心优化（Dao et al., 2022）  
- **问题定位**：标准 attention 计算中，$QK^T$ 矩阵需完整存于 HBM，造成显存瓶颈（如 LLaMA-2-7B，seq=2048 → $2048^2 \times 2\,\text{bytes} \approx 16\,\text{MB}$ per layer）；  
- **三重融合策略**：  
  1. **分块计算**：将 $Q,K,V$ 切分为 $(B_q, d), (B_k, d), (B_k, d)$ 块，避免全尺寸 $QK^T$；  
  2. **Softmax 重计算**：不存储中间 softmax 输出，而是在 backward pass 中重新计算 $S = \text{softmax}(QK^T/\sqrt{d})$；  
  3. **GPU 共享内存缓存**：将当前块的 $Q_i, K_j, V_j$ 加载至 fast SRAM，消除重复 HBM 访问。  

### 2. 性能数据（《百面大模型》P297）  
| 模型配置         | 标准 Attention (ms) | FlashAttention (ms) | 加速比 | 显存节省 |
|------------------|---------------------|----------------------|--------|----------|
| LLaMA-2-7B, seq=2048 | 124.3               | 41.7                 | **2.98×** | **62%**  |
| LLaMA-2-13B, seq=4096 | 489.1               | 152.6                | **3.20×** | **69%**  |

### 3. 工程适配  
- **兼容性**：PyTorch 2.0+ 原生支持 `torch.nn.functional.scaled_dot_product_attention`（自动 dispatch 到 FlashAttention）；  
- **限制**：要求 CUDA >= 11.8，且仅支持 `causal=True` 或 `is_causal=True` 的解码场景（FlashAttention-2 支持双向）；  
- **与 PagedAttention 协同**：FlashAttention 负责 *计算加速*，PagedAttention 负责 *KV 缓存内存管理*，二者为 LLM 推理栈的“计算-存储”双支柱。  

## 相关页面  
[[pagedattention]]  
[[attention_mechanism]]  
[[causal_lm]]  
[[rope]]  
[[tools]]  

## 来源  
《百面大模型》，第 12 章 12.3 节 “FlashAttention”，P297；第 14 页目录：“12.3 大模型训练与推理预填充阶段的加速方法——FlashAttention”；第 18 页问答：“FlashAttention 的优化方法有哪些？如何实现数学等价性？”