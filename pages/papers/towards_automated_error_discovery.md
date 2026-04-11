# Towards Automated Error Discovery

_最后更新：2026-04-10_

## 概述  
Petrak et al., EMNLP 2025；提出 AED（Automated Error Discovery）框架，将错误检测从“判别式分类”转向“生成式探索”，首次实现对未知错误模式的主动发现与原型化。

## 详细内容  
AED 三阶段流程：  
1. **Error Seed Mining**：在未标注对话流中，用轻量异常检测器（基于 [[scaling_computation]] 的 token-level entropy peak）定位可疑片段；  
2. **Prototype Induction**：对种子集合执行 soft clustering（[[soft_clustering]]），自动归纳出可解释错误原型（如 “causal_chain_break”）；  
3. **Human-in-the-Loop Validation**：将原型交由领域专家（[[people/thy_thy_tran]] 等）审核并命名，形成新错误类型。  

贡献：  
- 在 UKP Lab 内部部署中，6 个月内发现 9 类新错误（此前未被任何 benchmark 覆盖）；  
- 开源代码与 prototype bank 已集成至 [[tools/errdetect]] v0.4.2；  
- 理论意义：验证了 [[search_and_learning]] 范式在可靠性工程中的可扩展性——错误空间本身可随算力增长而持续探索。

## 相关页面  
[[models/seeed]]  
[[concepts/soft_clustering]]  
[[concepts/search_and_learning]]  
[[tools/errdetect]]  
[[people/dominic_petrak]]  
[[people/thy_thy_tran]]  
[[trends/ai_reliability_engineering]]

## 来源  
百面大模型.pdf（Chapter 6 “From Detection to Discovery”, pp. 118–132）；EMNLP 2025 paper (arXiv:2504.11203)