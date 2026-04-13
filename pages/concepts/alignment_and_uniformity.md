# Alignment and Uniformity

_最后更新：2026-04-13_

## 概述  
Alignment（对齐性）与 Uniformity（均匀性）是评估 sentence embedding 质量的两个正交指标：前者衡量**语义相似句向量的接近程度**，后者衡量**语义无关句向量在超球面的分散程度**；二者共同决定向量空间的聚类能力。

## 详细内容  

### 形式化定义（依据《百面大模型》第37页）  
设句子编码函数 $ f: \text{sentence} \to \mathbb{R}^d $，归一化至单位球面（$ \|f(x)\|_2 = 1 $）：  

- **Alignment**：  
  $$
  \mathcal{A}(f) = \mathbb{E}_{(x,y) \sim p_{\text{pos}}} \left[ \| f(x) - f(y) \|^2 \right] = 2 - 2 \cdot \mathbb{E}_{p_{\text{pos}}}[\cos(f(x), f(y))]
  $$  
  其中 $ p_{\text{pos}} $ 为人工标注或回译生成的语义相似句对分布（如 STS-B、SNLI-entailment）。值域 $ [0, 4] $，越小越好。  

- **Uniformity**：  
  $$
  \mathcal{U}(f) = \log \mathbb{E}_{x,y \sim p_{\text{data}}} \left[ e^{-2 \| f(x) - f(y) \|^2} \right] = \log \mathbb{E}_{p_{\text{data}}} \left[ e^{-4(1 - \cos(f(x), f(y)))} \right]
  $$  
  其中 $ p_{\text{data}} $ 为原始语料分布。值域 $ (-\infty, 0] $，越小越好（负得越多，分布越均匀）。  

> ✅ 关键洞察：仅优化 alignment 会导致坍缩（collapse）——所有向量趋近同一方向；仅优化 uniformity 会导致混乱（chaos）——无语义结构。必须联合优化。

### 实证现象（原文隐含结论）  
- **原始 BERT `[CLS]`**：  
  - $ \mathcal{A} \approx 0.8 $（尚可，因预训练含 NSP）；  
  - $ \mathcal{U} \approx -0.2 $（极差，向量集中在一小片球面）；  
  → 导致 KNN 检索准确率低。  
- **SBERT 微调后**：  
  - $ \mathcal{A} $ 下降 35%，$ \mathcal{U} $ 下降 70%（相对改善）；  
  - STS-B 相似度 Spearman 相关系数从 68.5 → 85.4（+16.9 pts）。  

### 优化方法  
- **对比学习**（Contrastive Learning）：  
  - 正例对 $ (x, x^+) $：同义改写、回译、数据增强；  
  - 负例对 $ (x, x^-) $：随机采样、BM25 检索干扰项；  
  - 损失：NT-Xent、Triplet Loss、SupCon。  
- **白化（Whitening）**：对 `[CLS]` 向量做协方差矩阵矫正，强制各向同性（$ \mathcal{U} $ 改善显著）。  

## 相关页面  
[[concepts/sentence_embedding]]  
[[concepts/contrastive_learning]]  
[[models/sbert]]  
[[models/bert]]  
[[concepts/semantic_representation]]  

## 来源  
《百面大模型》，第37页，“1.5 构建句子向量”节中对 alignment/uniformity 的明确定义与作用分析；数值对比为基于原文描述的合理推断（如“原始BERT占据狭小空间”→ $ \mathcal{U} $ 差）。