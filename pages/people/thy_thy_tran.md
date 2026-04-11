# Thy Thy Tran

_最后更新：2026-04-10_

## 概述  
Thy Thy Tran 是跨文化 NLP 专家、UKP Lab 高级研究员，DialErrors 数据集文化顾问与 AED 项目共同设计者，致力于构建具备文化敏感性的 AI 可靠性评估体系。

## 详细内容  
核心工作：  
- 主导 DialErrors v2.1 的文化标注协议设计：定义 7 类文化背景的 annotation guidelines，确保 “cultural misalignment” 等错误类型在不同语境中的一致性判别；  
- 提出 “cultural omission” 错误子类：指 LLM 在回应中系统性忽略某文化群体的关键价值观（e.g., 集体主义语境下过度强调个人选择），该类型已被纳入 DialErrors v2.1 与 SEEED 原型库；  
- 在 AED 框架中负责 human-in-the-loop validation stage，建立 prototype 命名与伦理审查双轨机制。  

观点引用：  
> “一个错误检测器若不能识别‘为什么这个回答在越南语境中冒犯’，它就只是统计幻觉。”（百面大模型.pdf p. 127）

## 相关页面  
[[tools/hf_datasets_dialerrors]]  
[[papers/towards_automated_error_discovery]]  
[[models/seeed]]  
[[concepts/error_detection_in_llms]]  
[[people/dominic_petrak]]

## 来源  
百面大模型.pdf（Section 5.2 “Cultural Dimensions of Error”, pp. 107–111；Interview Box, p. 127）；DialErrors v2.1 contributor list