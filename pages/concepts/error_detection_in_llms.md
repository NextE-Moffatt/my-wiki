# Error Detection in LLMs

_最后更新：2026-04-10_

## 概述  
LLM 错误检测指在模型生成输出后，自动识别其潜在有害性、事实性错误、逻辑矛盾、文化失当等风险行为的技术方向，是 AI 可靠性工程（[[ai_reliability_engineering]]）的核心支柱。

## 详细内容  
主流范式分为三类：  
1. **Heuristic-based**：规则/正则匹配（e.g., “I don’t know” triggers low-confidence flag），简单但覆盖率低；  
2. **Classifier-based**：微调 RoBERTa/BERT 等判别模型，需大量标注数据，OOD 泛化弱（参见 [[ood_generalization]]）；  
3. **Self-Reflective & Clustering-Aware**（新兴范式）：  
　- 利用 [[self_reflection]] 生成元判断（“Is this response factually consistent with the source?”）；  
　- 或引入无监督/半监督结构先验（如 [[soft_clustering]]），将错误空间建模为连续语义流形，而非离散标签集合。SEEED（[[models/seeed]]）即属此类代表。  

评估挑战：  
- 标准化 benchmark 缺乏：DialErrors（[[hf_datasets_dialerrors]]）是当前唯一覆盖跨文化、多模态错误类型的开源基准；  
- “错误”定义动态演进：2024 年新增“value-laden omission”（价值观隐性缺失）类别，要求检测器具备元伦理建模能力。

## 相关页面  
[[concepts/ood_generalization]]  
[[concepts/self_reflection]]  
[[concepts/soft_clustering]]  
[[models/seeed]]  
[[tools/hf_datasets_dialerrors]]  
[[trends/ai_reliability_engineering]]  
[[papers/towards_automated_error_discovery]]

## 来源  
百面大模型.pdf（Chapter 3 “Safety & Reliability”, pp. 41–55）；DialErrors v2.1 technical report (2025)