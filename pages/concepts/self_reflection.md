# Self-Reflection

_最后更新：2026-04-10_

## 概述  
指大型语言模型生成对其自身输出的批判性分析（如“这个回答是否准确？”、“是否存在逻辑漏洞？”），作为提升可靠性与可控性的内部验证机制。

## 详细内容  
- **Paradigm**: Prompt-driven introspection (e.g., “Step-by-step, verify whether the above answer cites a real 2023 study”) or fine-tuned reflection heads (e.g., ReAct-style reasoning traces).  
- **Comparison with Encoder-Based Detection**:  
  - *Pros*: Generative, explainable, supports repair (“revise to fix hallucination”);  
  - *Cons*: High compute cost, inconsistent quality, self-deception risk, non-deterministic.  
- **Hybrid Approaches**: SEEED can serve as *fast filter* to trigger self-reflection only on high-risk responses — reducing overall latency while preserving explainability where needed.  
- **Limitations**: Reflection quality strongly depends on base model capability; fails catastrophically on “unknown unknowns”.

## 相关页面  
[[papers/towards_automated_error_discovery]]  
[[models/seeed]]  
[[concepts/error_detection_in_llms]]  
[[concepts/llm_safety]]  
[[concepts/chain_of_thought]]  
[[tools/trl]]  
[[concepts/verification_and_validation]]  
[[concepts/ai_alignment]]  
[[tools/langchain]]  
[[concepts/interpretability]]

## 来源  
https://aclanthology.org/2025.emnlp-main.1/ — Petrak et al. (2025), Section 2.2 (related work) & Discussion; also: Madaan et al. (2023), “Self-Refine”.