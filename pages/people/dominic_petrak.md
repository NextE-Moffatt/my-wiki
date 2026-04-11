# Dominic Petrak

_最后更新：2026-04-10_

## 概述  
Dominic Petrak 是 UKP Lab 博士研究员，SEEED 架构主要设计者与 AED（Automated Error Discovery）框架第一作者，专注将无监督表征学习引入 AI 可靠性工程。

## 详细内容  
研究轨迹：  
- 博士课题（2022–2025）聚焦“错误语义的几何结构”，提出将错误空间建模为黎曼流形的初步构想；  
- 2024 年主导 SEEED 架构设计，关键决策包括：放弃 cross-attention（保障延迟）、引入 Gumbel-Softmax 软簇头（提升 OOD 泛化）、解耦 prototype learning 与 detector training；  
- 2025 年联合 [[people/thy_thy_tran]] 发起 AED 项目，推动错误发现从静态 benchmark 向动态演化系统演进。  

技术主张：  
- “错误不是标签，而是向量场中的扰动”（引自百面大模型.pdf p. 89）；  
- 坚持工具开源：所有代码发布于 `github.com/ukp/seeed`，模型托管于 Hugging Face。

## 相关页面  
[[models/seeed]]  
[[papers/towards_automated_error_discovery]]  
[[concepts/soft_clustering]]  
[[people/thy_thy_tran]]  
[[trends/ai_reliability_engineering]]

## 来源  
百面大模型.pdf（Author Profiles sidebar, p. 162）；UKP Lab website bio (2026-03-30)