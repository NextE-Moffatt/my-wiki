# PagedAttention

_最后更新：2026-04-14_

## 概述  
PagedAttention 是 vLLM 提出的 KV 缓存内存管理技术（2023），将 KV 缓存组织为固定大小的“页”（page），支持非连续物理内存分配，解决长上下文推理中的内存碎片化问题（p. 321，★★★★★）。

## 详细内容  
### 内存碎片化问题量化  
- 传统 KV 缓存：每个 sequence 分配连续内存块，当 sequence 长度不一（如 128/512/2048）时，内存利用率 < 30%（实测于 8×A100）  
- PagedAttention 将 KV 缓存切分为 16KB page，每个 sequence 的 KV 存储在多个 page 中，通过 page table 索引  

### 吞吐提升机制（12.5.2）  
- **共享 KV 缓存**：同一 prompt 的多个 generation 请求（如 beam search）共享 prompt 的 KV page，减少重复计算  
- **动态扩容**：sequence 增长时，仅申请新 page，无需 realloc + memcpy  
- **实测效果**：在 8×A100 上，vLLM（PagedAttention）比 HuggingFace Transformers 吞吐高 24×（128K context, batch=32）

## 相关页面  
[[tools/vllm]] [[concepts/kv_cache_optimization]] [[models/deepseek_r1]] [[tools/pagedattention]]

## 来源  
《百面大模型》，第 12.5 节 “PagedAttention”，pp. 321–325