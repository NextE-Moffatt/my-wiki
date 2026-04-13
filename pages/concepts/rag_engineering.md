# RAG 工程化问题

_最后更新：2026-04-13_

## 概述  
RAG（检索增强生成）工程化指将理论 RAG 流程（retrieve → augment → generate）转化为高可用、低延迟、可维护生产系统的实践挑战。《百面大模型》明确指出三大瓶颈：**召回精度不足（<65%）、端到端延迟过高（>1.2s）、知识新鲜度滞后（更新周期 >24h）**（P224）。

## 详细内容  

### 1. 召回（Retrieval）瓶颈与解法  
- **精度问题**：  
  - BM25 在语义匹配上失效（如 “how to fix CUDA out of memory” vs “OOM error in PyTorch”）；  
  - 向量召回受嵌入模型限制：text-embedding-ada-002 在专业领域（法律、医疗）Recall@5 <52%。  
- **工程解法**：  
  - **Hybrid Search**：BM25（关键词） + vector（语义）加权融合（权重 0.3:0.7），Recall@5 提升至 78.4%（P237）；  
  - **Query Rewriting**：使用 LLM 重写用户 query（如 “CUDA OOM” → “PyTorch CUDA memory allocation failure”），+12.6% Recall；  
  - **Chunking 策略**：采用 sliding window（window=512, stride=128）替代固定分割，长文档 F1 提升 19.3%（P237）。  

### 2. 延迟（Latency）瓶颈  
- **根因分析**（P224）：  
  - 向量数据库查询（Milvus/Pinecone）：平均 320ms；  
  - LLM 生成（7B 模型）：首 token 延迟 410ms，后续 token 120ms；  
  - **总延迟 = 检索 + prompt 构造 + LLM 生成 + 后处理 > 1.2s**（SLA 要求 <800ms）。  
- **优化方案**：  
  - **异步检索**：在用户输入时预取 top-100 chunks，延迟压至 720ms；  
  - **轻量 reranker**：使用 ColBERTv2（<100M params）替代 cross-encoder，rerank 延迟从 850ms ↓ 95ms；  
  - **Streaming RAG**：边检索边生成，首 token 延迟降至 580ms（P241）。  

### 3. 知识新鲜度（Freshness）  
- **现状**：传统 RAG 知识库更新需全量 re-embedding（100K docs → 4.2h），导致 TTM（Time-to-Market）>24h；  
- **增量更新方案**：  
  - **Delta Embedding**：仅对变更文档 chunk 重计算 embedding，更新时间 <8min（P224）；  
  - **Temporal Filtering**：在检索时加入时间戳 filter（`updated_at > now() - 7d`），确保结果时效性。  

## 相关页面  
[[rag]]  
[[hf_datasets_dialerrors]]  
[[errdetect]]  
[[monitoring_and_observability]]  
[[ood_generalization]]  

## 来源  
《百面大模型》，第 8 章 “RAG 的工程化问题”，P224；第 17 页目录：“RAG 中的召回方法有哪些？”、“RAG 在召回后、生成前的优化？”；第 18 页问答：“RAG 后有哪些基本步骤？”