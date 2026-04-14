# PagedAttention

_最后更新：2026-04-14_

## 概述  
PagedAttention 是 vLLM 提出的 KV cache 内存管理机制，借鉴操作系统虚拟内存思想，将逻辑连续的 KV cache 切分为固定大小（如 16 tokens）的物理页（page），实现非连续内存分配与零拷贝共享，彻底解决长上下文推理的显存碎片问题。

## 详细内容  
传统 KV cache 存储为 contiguous tensor，导致：
- **内存浪费**：batch 内各 sequence 长度不一，padding 至 max_len 造成平均 35% 显存浪费；
- **无法共享**：相同 prompt 的 multiple requests 无法共享 prefix KV。

PagedAttention 引入：
- **Block Table**：每个 sequence 维护一个 page ID 列表，指向其 KV cache 物理页；
- **KV Cache Pool**：全局内存池，按需分配/释放 page；
- **Shared Prefix**：多个 sequence 可共享同一 block table 前缀（如 system prompt）。

据第 12.5 节量化结果（A100-80G, LLaMA-2-7B）：
- **吞吐提升**：batch=256、avg_len=1024 时，prefill throughput 提升 2.1×，decode throughput 提升 3.7×；
- **显存利用率**：从 58% → 92%（接近理论上限）；
- **最大上下文**：支持 128k context 时，显存占用仅增加 1.8×（vs linear growth of contiguous）；
- **工程代价**：引入约 5% CPU 开销用于 block table 管理，但 GPU 利用率提升补偿该开销。

PagedAttention 与 MQA/GQA 高度协同：GQA 的 KV cache 更紧凑，page 内 token 密度更高，进一步提升 pool 利用率（见 [[mqa_gqa]]）。

## 相关页面  
[[pagedattention]] [[mqa_gqa]] [[flashattention]] [[kv_cache]] [[vllm]] [[long_context_reasoning]]

## 来源  
《百面大模型》，第 12 章 12.5 节（pp. 321–327），2025 年出版