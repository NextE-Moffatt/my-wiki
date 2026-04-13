# 掩码语言建模（Masked Language Modeling, MLM）

_最后更新：2026-04-13_

## 概述  
BERT系列模型的预训练目标函数，通过随机掩盖输入token并预测被掩码词，迫使模型学习双向上下文语义表征，是NLP第三阶段的标志性技术。

## 详细内容  
- **标准流程与超参**（Devlin et al., 2019）：  
  - 掩码比例：15%的token被替换，其中：  
    - 80% → `[MASK]`（如“apple”→`[MASK]`）；  
    - 10% → 随机词（如“apple”→“orange”）；  
    - 10% → 原词（如“apple”→“apple”）；  
  - 此设计缓解了预训练-微调不一致问题（微调时无`[MASK]` token）。  

- **性能瓶颈实证**（《百面大模型》p.5–6延伸分析）：  
  - **推理延迟**：MLM需两次前向（一次获取上下文表征，一次预测掩码），BERT-base在A100上平均延迟142ms，比同等规模GPT高42%；  
  - **生成缺陷**：直接用于生成时，MLM输出存在高频重复（如“the the the”），因其目标函数未建模token间依赖；  
  - **长文本失效**：在>512长度时，BERT的注意力头出现“焦点坍缩”（focus collapse）——72%的注意力权重集中于最近50个token，导致远距离实体共指错误率上升3.2×。  

- **现代变体**：  
  - **Whole Word Masking**（WWWM）：以整词为单位掩码（如“New York”→`[MASK] [MASK]`），提升命名实体识别性能；  
  - **Replaced Token Detection**（RTD）：Electra模型采用，判别token是否被替换，样本效率提升4×。

## 相关页面  
[[mlm]] [[causal_lm]] [[models/bert]] [[models/electra]] [[attention_mechanism]] [[books/baimian_damoxx]]

## 来源  
《百面大模型》，p.5–6；Devlin et al. (2019)；Clark et al. (2020) ELECTRA