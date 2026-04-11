# AI Reliability Engineering

_最后更新：2026-04-10_

## 概述  
AI 可靠性工程（ARE）是将 SRE（Site Reliability Engineering）原则迁移至 AI 系统的新兴交叉学科，聚焦可观测性、错误预算、自动化修复与故障根因分析，SEEED 与 AED 是其典型落地实践。

## 详细内容  
核心实践：  
- **Error Budgets for LLMs**：定义“可接受错误率”（e.g., <5% high-risk errors/hour），SEEED 的 calibrated confidence score（[[models/seeed]]）直接服务于该预算监控；  
- **Observability Stack**：`errdetect` 提供 metrics（error rate per prototype）、logs（soft cluster weights）、traces（self-reflection chain）三位一体可观测性；  
- **Automated Remediation**：当 SEEED 检测到 “cultural_omission” 且置信度 >0.9，自动触发 [[self_reflection]] 重写 pipeline（实验阶段，准确率 78%）。  

与传统 SRE 区别：  
- 故障模式非二元（up/down），而是连续语义空间（故需 [[soft_clustering]]）；  
- 根因常在训练数据分布偏移（data drift），而非基础设施故障；  
- 因此，ARE 更依赖 [[ood_generalization]] 与 [[search_and_learning]] 能力。

## 相关页面  
[[models/seeed]]  
[[papers/towards_automated_error_discovery]]  
[[concepts/ood_generalization]]  
[[concepts/search_and_learning]]  
[[tools/errdetect]]  
[[concepts/monitoring_and_observability]]

## 来源  
百面大模型.pdf（Chapter 7 “Engineering Reliability”, pp. 133–149）；Google ARE Whitepaper v2.1 (2025)