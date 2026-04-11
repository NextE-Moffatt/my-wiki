# OOD Generalization (Out-of-Distribution Generalization)

_最后更新：2026-04-10_

## 概述  
指模型在训练分布之外（Out-of-Distribution, OOD）的数据上保持鲁棒性能的能力；在对话AI错误检测中特指对未见过的错误类型、新用户群体、跨领域对话场景的泛化能力。

## 详细内容  
- **OOD in Conversational AI**: Includes shifts in:  
  - *Intent space* (e.g., new customer service queries),  
  - *Error morphology* (e.g., novel hallucination patterns post-finetuning),  
  - *User demographics & language style* (e.g., Gen-Z slang, multilingual code-switching).  
- **Key Techniques for OOD Error Detection**:  
  - Contrastive representation learning (e.g., SEEED’s LBSR),  
  - Uncertainty-aware scoring (e.g., entropy, confidence calibration),  
  - Test-time adaptation (TTA) via lightweight prompt tuning,  
  - Causal disentanglement of error signals from domain confounders.  
- **Benchmarks**: DialErrors-OOD (held-out error categories), ConvAI2-Shift (temporal user behavior drift), MultiWOZ-CrossDomain (domain transfer).  
- **Link to Scaling Laws**: OOD robustness does *not* scale predictably with model size — small encoder models trained with contrastive objectives often outperform larger LLM-as-judge on OOD error detection.

## 相关页面  
[[papers/towards_automated_error_discovery]]  
[[models/seeed]]  
[[concepts/error_detection_in_llms]]  
[[concepts/scaling_computation]]  
[[trends/ai_reliability_engineering]]  
[[concepts/representation_learning]]  
[[concepts/transfer_learning]]  
[[concepts/uncertainty_quantification]]  
[[tools/robustness_metrics]]  
[[concepts/domain_adaptation]]

## 来源  
https://aclanthology.org/2025.emnlp-main.1/ — Petrak et al. (2025), Section 4.4 & Table 5; also foundational work: Hendrycks & Dietterich (2019), Taori et al. (2023).