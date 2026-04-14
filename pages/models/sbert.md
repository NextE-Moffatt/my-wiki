# Sentence-BERT (SBERT)

_最后更新：2026-04-14_

## 概述  
Sentence-BERT 是首个针对句子嵌入聚类性质优化的孪生 BERT 微调框架，通过三任务联合训练（分类/回归/三元组）解决原始 BERT 各向异性问题，在 STS-B 上达 85.4，成为 sentence-transformers 库默认基线。

## 详细内容  

### 1. 架构与训练任务  
- **共享参数孪生网络**：左右分支使用相同 BERT 参数，输入句子对 $(u,v)$；  
- **三任务并行训练**：  
  1. **分类任务**：拼接 $[u; v; |u-v|]$ 输入 MLP 分类器，预测语义相似度等级（0–5）；  
  2. **回归任务**：以余弦相似度 $\cos(u,v)$ 为标签，用 MSE loss 优化；  
  3. **三元组任务**：锚点 $s_a$、正例 $s_p$、负例 $s_n$，优化目标：  
     $$
     \mathcal{L}_{\text{triplet}} = \max\left( \| s_p - s_a \| - \| s_n - s_a \| + c,\ 0 \right),\quad c=0.1
     $$  
     （原文明确给出 $c=0.1$）

### 2. 推理与池化策略  
- **最优池化方式**：实验验证 **均值池化（mean pooling）** 输出的句子向量在 STS-B 上最佳（85.4），优于 [CLS]（75.2）、max pooling（79.1）；  
- **推理流程**：单句输入 → BERT 编码 → 所有 token 向量均值 → L2 归一化 → 余弦相似度计算；  
- **效率**：单句编码延迟 120ms（BERT-base, GPU），相似度计算 <0.1ms（FAISS）。

### 3. 性能与局限  
- **基准结果**：STS-B 85.4（Reimers & Gurevych, EMNLP 2019）；  
- **缺陷**：  
  - 依赖标注数据（SNLI、MultiNLI），无监督场景不可用；  
  - 三元组任务需负采样，batch size < 16 时负例多样性不足，$\mathcal{U}$ 优化受限；  
  - 对长文档（>512 tokens）截断处理，丢失全局结构。

## 相关页面  
[[models/bert]] [[concepts/sentence_embedding]] [[concepts/alignment_and_uniformity]] [[concepts/contrastive_learning]] [[concepts/triplet_loss]] [[concepts/mean_pooling]] [[concepts/ood_generalization]] [[people/iryana_gurevych]]

## 来源  
《百面大模型》第 1.5 节（2025），P7；原文明确描述 SBERT 三任务设计、$c=0.1$、均值池化最优（85.4）、STS-B 85.4 数据、推理流程、GPU 延迟（120ms）。