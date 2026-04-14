# vLLM

_最后更新：2026-04-14_

## 概述  
vLLM 是一个开源高性能大模型推理服务框架，核心创新为 **PagedAttention** 内存管理机制，支持高吞吐、低延迟、长上下文（最高 2M tokens）推理，被 DeepSeek-R1、Qwen2、Llama-3 等主流模型官方推荐。

## 详细内容  

### PagedAttention 原理（§12.5.2）  
- **问题根源**：传统 KV cache 为连续内存块，导致：  
  - 内存碎片化（不同请求长度不一）；  
  - 无法共享（相同 prefix 无法跨请求复用）；  
  - 显存利用率常 < 30%。  
- **PagedAttention 解法**：  
  - 将 KV cache 切分为固定大小 page（默认 16 tokens/page）；  
  - 每个 sequence 通过 **block table**（数组）索引其占用的 pages；  
  - 支持 **copy-on-write**：相同 prompt 的多个请求共享 pages，仅在 decode 阶段写入新 page；  
- **效果**：显存利用率从 <30% → **>85%**；128K ctx 吞吐提升 2.1×（vs HuggingFace Transformers）。

### vLLM 与 DeepSeek-R1 的深度集成  
- DeepSeek-R1 官方推理脚本默认启用 `--enable-prefix-caching`（基于 PagedAttention 的 prefix caching）；  
- 在 128K ctx 下，vLLM 对 DeepSeek-R1 的实测吞吐达 **142 tok/s**（A100），较 HF Transformers（98 tok/s）高 45%；  
- 支持 **continuous batching** + **PagedAttention**，QPS（queries per second）随 batch_size 近似线性增长（至 GPU 显存饱和）。

### 与其他工具对比  
| 工具 | KV 缓存管理 | 最长上下文 | DeepSeek-R1 官方支持 |  
|------|--------------|-------------|------------------------|  
| vLLM | PagedAttention | 2M | ✅（首选） |  
| Text Generation Inference (TGI) | Block-based | 128K | ⚠️（需 patch） |  
| HuggingFace Transformers | Contiguous | 32K（OOM） | ❌（不推荐） |  
| llama.cpp | Paged (via mmap) | 128K | ⚠️（CPU-only） |

## 相关页面  
[[tools/pagedattention]]  
[[models/deepseek_r1]]  
[[concepts/kv_cache_optimization]]  
[[concepts/prefix_caching]]  
[[tools/flashattention]]  
[[concepts/continuous_batching]]

## 来源  
《百面大模型》，§12.5.2 “PagedAttention 如何提高对 KV 缓存的内存管理效率”（p. 325）及 §12.12 “vLLM 是什么？其背后的 PagedAttention 原理是什么？”（p. 321），提供 PagedAttention 核心思想、page size（16）、显存利用率提升数据（→85%）、DeepSeek-R1 吞吐实测值（142 tok/s）。