# Monitoring and Observability for LLM Systems

_最后更新：2026-04-10_

## 概述  
LLM 系统可观测性指通过 metrics、logs、traces 三支柱，持续理解模型行为、检测异常、定位根因的能力，是 AI 可靠性工程（[[ai_reliability_engineering]]）的操作基础。

## 详细内容  
在 SEEED/AED 生态中的体现：  
- **Metrics**：`errdetect` 输出 per-prototype error rate、confidence entropy、OOD gap delta；  
- **Logs**：软簇权重向量（16-d）作为结构化日志，支持语义级查询（e.g., “show all responses with >0.6 weight on pragmatic_violation”）；  
- **Traces**：`SelfReflectPipeline` 生成完整反思链 trace（prompt → reflection → revision），用于根因回溯。  

关键演进：  
- 从 scalar metrics（e.g., overall accuracy）→ semantic vector metrics（soft cluster distribution）；  
- 从被动告警 → 主动探索（AED 的 error seed mining 即 trace-driven anomaly discovery）。

## 相关页面  
[[models/seeed]]  
[[tools/errdetect]]  
[[papers/towards_automated_error_discovery]]  
[[trends/ai_reliability_engineering]]  
[[concepts/soft_clustering]]

## 来源  
百面大模型.pdf（Section 7.3 “Observability Beyond Scalars”, pp. 142–145）；errdetect observability docs (2026-03)