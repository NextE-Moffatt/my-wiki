# RAG Engineering

_最后更新：2026-04-14_

## 概述  
RAG Engineering 指检索增强生成（RAG）系统在生产环境中的工程化实践，涵盖召回-重排-生成链路的延迟优化、数据一致性、故障隔离等关键问题（第 9.4 节，p. 244，★★★★☆）。

## 详细内容  
### 核心工程挑战  
- **延迟敏感链路**：端到端 P99 延迟必须 < 2s（用户容忍阈值）。瓶颈常在：  
  - **召回阶段**：向量数据库 ANN 查询（如 FAISS IVF-PQ）延迟波动大 → 解法：预热索引 + 异步 prefetch  
  - **重排阶段**：Cross-encoder 重排（如 bge-reranker）耗时高 → 解法：蒸馏为轻量 Bi-encoder 或 cache 重排结果  
- **缓存一致性**：当知识库更新时，向量库 embedding 与原始文档不同步 → 解法：版本化 embedding（`doc_id@v2`）+ TTL 缓存  
- **失败隔离**：召回为空时，不应导致生成器崩溃 → 解法：fallback prompt（“未找到相关信息，基于通用知识回答”）+ circuit breaker  

### 评估模块（9.1）  
- **召回模块**：Hit Rate@5（top-5 是否含 gold passage）  
- **重排模块**：NDCG@5（排序质量）  
- **生成模块**：Faithfulness（事实一致性） + Answer Relevance（相关性），需人工标注  

## 相关页面  
[[concepts/rag_engineering]] [[tools/hf_datasets_dialerrors]] [[concepts/retrieval]] [[concepts/reranking]]

## 来源  
《百面大模型》，第 9.4 节 “RAG 的工程化问题”，p. 244