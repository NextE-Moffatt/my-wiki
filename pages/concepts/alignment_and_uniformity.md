# Alignment and Uniformity

_最后更新：2026-04-14_

## 概述  
对齐性（alignment）与均匀性（uniformity）是评估句子嵌入质量的两个正交指标：对齐性衡量语义相近句子表征的紧凑性，均匀性衡量语义无关句子表征在超球面上的分散程度；二者共同构成良好语义表征的充要条件。

## 详细内容  

### 1. 数学定义（Wang et al., ICLR 2022）  
给定句子对 $(x_i, x_i^+)$ 为语义正例（如 paraphrase），$(x_i, x_j^-)$ 为负例（$i \neq j$），句子向量经 L2 归一化后 $\mathbf{z}_i, \mathbf{z}_i^+, \mathbf{z}_j^- \in \mathcal{S}^{d-1}$：  
- **对齐性（Alignment）**：  
  $$
  \mathcal{A}(\mathcal{Z}) = \mathbb{E}_{(x_i,x_i^+) \sim \mathcal{P}_+} \left[ -\log \exp\left( \cos(\mathbf{z}_i, \mathbf{z}_i^+) / \tau \right) \right]
  $$  
  目标：$\cos(\mathbf{z}_i, \mathbf{z}_i^+) \to 1$（即 $\mathcal{A} \to 0$）。  
- **均匀性（Uniformity）**：  
  $$
  \mathcal{U}(\mathcal{Z}) = \log \mathbb{E}_{x_i,x_j \sim \mathcal{P}_\text{data}, i \neq j} \left[ \exp\left( -2 \cdot \cos(\mathbf{z}_i, \mathbf{z}_j) / \tau \right) \right]
  $$  
  目标：$\cos(\mathbf{z}_i, \mathbf{z}_j) \to 0$（即 $\mathcal{U} \to \log 1 = 0$），确保分布覆盖整个超球面。

### 2. 原始 BERT 的失败根源  
- BERT 在 MLM+NSP 预训练中仅优化 [CLS] token 的分类损失，导致：  
  - 向量空间严重各向异性（anisotropy）：98.3% 的句子向量落入超球面 0.1-radius cap 内；  
  - 均匀性极差：$\mathcal{U} = 12.7$（理想值 ≈ 0），对齐性尚可（$\mathcal{A} = 2.1$）；  
  - 结果：余弦相似度集中在 [0.85, 0.99]，无法区分细粒度语义差异。

### 3. 对比学习的修复机制  
- SBERT 与 SimCSE 均通过对比损失显式优化 $\mathcal{A}$ 与 $\mathcal{U}$：  
  - SBERT 的 triplet loss 直接拉近正例、推远负例，提升 $\mathcal{U}$；  
  - SimCSE 的 dropout-as-augmentation 构造正例对，强制同一句子不同扰动下 $\mathbf{z}_i, \mathbf{z}_i^+$ 对齐（↑$\mathcal{A}$），同时 batch 内负例分散（↑$\mathcal{U}$）；  
- 实证：SimCSE 无监督版将 $\mathcal{U}$ 从 12.7 降至 3.2，$\mathcal{A}$ 从 2.1 降至 1.4；STS-B 提升 11.2 pts（72.4 → 83.6）。

## 相关页面  
[[concepts/sentence_embedding]] [[concepts/contrastive_learning]] [[concepts/sbert]] [[concepts/simcse]] [[concepts/dropout_as_augmentation]] [[concepts/anisotropy_in_embeddings]] [[concepts/ood_generalization]] [[concepts/semantic_representation]]

## 来源  
《百面大模型》第 1.5 节（2025），P7；原文首次提出 alignment/uniformity 作为评估框架、给出原始 BERT 各向异性量化（98.3% 向量集中）、SimCSE 优化效果（$\mathcal{U}$ 12.7→3.2, STS-B 72.4→83.6）、SBERT triplet loss 公式。