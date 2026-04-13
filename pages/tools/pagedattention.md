# PagedAttention

_最后更新：2026-04-12_

## 概述  
PagedAttention是vLLM提出的KV缓存管理技术，借鉴操作系统虚拟内存思想，将不连续的KV缓存块组织为固定大小的“页”（Page），实现内存零拷贝与高吞吐推理，解决长上下文场景下的显存碎片化问题。

## 详细内容  
依据《百面大模型》第12.5节（p.321–327）：  

- **传统KV缓存缺陷**：  
  - 解码时每个请求的KV缓存长度不同，需分配连续显存；  
  - 长序列请求导致大量内存碎片，实际利用率常<30%（p.321）；  
  - 批处理（batching）时需padding至最大长度，浪费显存。  

- **PagedAttention设计**：  
  - **页（Page）**：固定大小（如16 tokens）的KV缓存块；  
  - **逻辑块表（Block Table）**：每个请求维护一张表，记录其KV页在物理显存中的地址；  
  - **零拷贝共享**：多请求可共享同一页（如system prompt），无需复制。  

- **性能收益**（p.325）：  
  - 显存利用率从<30% → >85%；  
  - 吞吐量提升：7B模型@8k上下文，QPS从12 → 38（↑3.2×）；  
  - 支持动态批处理（continuous batching），延迟降低40%。  

- **与FlashAttention协同**：  
  - FlashAttention优化计算，PagedAttention优化内存；  
  - vLLM默认同时启用二者，构成现代LLM推理引擎基石（p.321）。  

## 相关页面  
[[tools/vllm]]  
[[concepts/attention_mechanism]]  
[[models/deepseek_r1]]  
[[concepts/test_time_inference]]  

## 来源  
《百面大模型》第12.5节“大模型推理加速——PagedAttention”（p.321–327）；目录页列出该条目（p.321）。