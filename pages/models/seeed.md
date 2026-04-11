# SEEED — Soft Clustering Extended Encoder-Based Error Detection

_最后更新：2026-04-10_

## 概述  
SEEED 是一种面向对话AI可靠性工程的轻量级、可解释错误检测模型，采用软聚类增强的双编码器架构，在未见错误类型（OOD）上实现 83.7% F1（vs. 62.1% for RoBERTa-base），且推理延迟低于 12ms（CPU）。论文发表于 EMNLP 2025。

## 详细内容  
SEEED 架构由三核心组件构成：  
- **Dual-Encoder Backbone**：共享参数的文本对编码器（query/response），输出 768-d 向量；不依赖交叉注意力，保障低延迟。  
- **Soft Cluster Projection Head**：将编码向量映射至 16 维软簇空间（via Gumbel-Softmax），每个维度对应一类语义错误原型（如“factual hallucination”、“cultural misalignment”、“logical contradiction”），支持概率性归属而非硬分类。  
- **Error Confidence Calibrator**：基于簇内一致性与跨簇熵设计不确定性得分，用于触发 human-in-the-loop 审核（阈值可配置）。  

关键创新点：  
- 首次将软聚类显式建模为错误语义空间的归纳偏置，提升 OOD 泛化（见 [[ood_generalization]]）；  
- 在 DialErrors v2.1 数据集（[[hf_datasets_dialerrors]]）上 zero-shot 迁移至 7 类新错误模式，平均 F1 提升 29.4%；  
- 支持模型自解释：通过 top-3 软簇权重生成自然语言错误归因（e.g., “72% cultural misalignment, 19% factual hallucination”），已集成至 [[errdetect]] v0.4.2。  

训练策略：  
- 使用 contrastive clustering loss（L<sub>CL</sub>） + calibrated confidence loss（L<sub>CC</sub>），其中 L<sub>CC</sub> 强制高熵预测对应低置信度；  
- 无监督预热阶段：在 500K 无标注对话中学习簇结构；  
- 监督微调仅需 2.3K 标注样本（远少于传统分类器所需 15K+）。

## 相关页面  
[[models/seeed]]  
[[concepts/soft_clustering]]  
[[concepts/error_detection_in_llms]]  
[[concepts/ood_generalization]]  
[[papers/towards_automated_error_discovery]]  
[[tools/errdetect]]  
[[tools/hf_datasets_dialerrors]]  
[[people/dominic_petrak]]  
[[people/iryana_gurevych]]  
[[trends/ai_reliability_engineering]]

## 来源  
百面大模型.pdf（Section 4.2 “Reliability-Aware Architectures”, pp. 87–93）；EMNLP 2025 论文附录 A/B