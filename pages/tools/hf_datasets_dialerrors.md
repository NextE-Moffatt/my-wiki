# hf_datasets_dialerrors — DialErrors Benchmark Dataset

_最后更新：2026-04-10_

## 概述  
`dialerrors` 是 Hugging Face Datasets 库中的权威对话错误标注数据集（v2.1），覆盖 12 类错误模式、7 种文化背景、3 种模态（text/audio/transcript），专为评估 LLM 错误检测器的 OOD 泛化能力设计。

## 详细内容  
数据构成：  
- **Core Set (v2.1)**：42,816 个人工标注对话对（query-response），每条标注包含：  
　- 主错误类型（12 类，含新增 “epistemic_overconfidence” 和 “cultural_omission”）；  
　- 软簇权重向量（16-d，与 [[models/seeed]] 原型对齐）；  
　- 文化来源标签（e.g., `jp`, `br`, `ng`）；  
- **OOD Split**：独立测试集（8,241 samples），含 5 类未在训练中出现的错误组合（e.g., “factual hallucination + cultural misalignment”），用于量化泛化鸿沟。  

关键特性：  
- 所有标注经双盲审核 + cultural consultant 复核（参见 [[people/thy_thy_tran]]）；  
- 提供 `load_dataset("ukp/dialerrors", "v2.1")` 一行加载；  
- 与 [[models/seeed]]、[[tools/errdetect]] 深度集成，支持 `errdetect.eval.DialErrorsEvaluator` 直接调用。

## 相关页面  
[[models/seeed]]  
[[concepts/error_detection_in_llms]]  
[[concepts/ood_generalization]]  
[[tools/errdetect]]  
[[people/thy_thy_tran]]

## 来源  
百面大模型.pdf（Section 5.1 “Benchmarks That Matter”, pp. 102–107）；DialErrors v2.1 dataset card (Hugging Face, 2026-02-15)