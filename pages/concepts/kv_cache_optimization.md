# KV Cache Optimization

_最后更新：2026-04-14_

## 概述  
KV Cache Optimization 指通过内存布局重构、计算复用、压缩等手段降低 Transformer 解码阶段 Key/Value 缓存的显存占用与访问延迟，是提升大模型推理吞吐量（throughput）与降低首 token 延迟（TTFT）的核心工程课题。

## 详细内容  

### 关键瓶颈量化（§12.5.1）  
- 在 128K 上下文、batch_size=1 的典型推理场景中：  
  - KV cache 占用显存 **> 85%**（其余为 activation & weights）；  
  - 显存带宽成为瓶颈：A100 2039 GB/s 带宽中，72% 用于 KV cache 的读写；  
  - 内存碎片导致有效利用率 < 30%，直接限制并发请求数（max batch_size）。

### 主流优化技术对比  
| 技术 | 原理 | 显存节省 | 吞吐提升 | 精度影响 | 适用模型 |  
|------|------|------------|------------|------------|------------|  
| **PagedAttention** (vLLM) | Page-based allocation + block table | ↓65%（vs contiguous） | ↑2.1× | 无 | All |  
| **MLA** (DeepSeek-R1) | K/V weight tying across layers | ↓37%（KV cache size） | ↑1.45× | +0.03 PPL | MLA-enabled |  
| **Quantized KV Cache** (FP8) | KV 存为 FP8，dequantize on fly | ↓50% | ↑1.3× | +0.12 PPL | Quant-aware |  
| **Prefix Caching** | 共享 prompt KV across requests | ↓40%（avg. per req） | ↑1.8× | 无 | Batched |  
| **StreamingLLM** | Virtual tokens + attention sink | ↓90%（theoretical） | ↑3.2× | +0.8 PPL | Long-context only |  

### DeepSeek-R1 的组合策略  
- **硬件层**：启用 FP16 KV cache（非量化），配合 PagedAttention；  
- **架构层**：MLA 减少 KV 缓存生成量；  
- **系统层**：vLLM 的 prefix caching 复用用户历史对话 prefix；  
- **综合效果**：128K ctx 下，端到端 TTFT 从 1240ms → **790ms（↓36%）**，吞吐达 142 tok/s。

## 相关页面  
[[tools/vllm]]  
[[concepts/pagedattention]]  
[[models/deepseek_r1]]  
[[concepts/mla]]  
[[concepts/prefix_caching]]  
[[concepts/streamingllm]]  
[[concepts/quantization]]

## 来源  
《百面大模型》，§12.5.1 “为什么对 KV 缓存的内存管理效率是影响推理系统吞吐量的关键因素”（p. 322）及全章相关实证数据（显存占比、带宽占比、TTFT 降低值等）。