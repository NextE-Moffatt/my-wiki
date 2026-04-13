# Sentence Embedding

_最后更新：2026-04-13_

## 概述  
Sentence embedding 是将整句映射为固定维稠密向量的技术，核心评估指标为**对齐性**（alignment）与**均匀性**（uniformity）；静态方法（如平均词向量）快但忽略语序，动态方法（如 BERT）强但慢。

## 详细内容  

### 评估指标（依据《百面大模型》第37页）  
- **Alignment（对齐性）**：  
  $ \mathcal{L}_{\text{align}} = \mathbb{E}_{(x,y) \sim p_{\text{pos}}} \left[ \| f(x) - f(y) \|^2 \right] $，  
  其中 $ p_{\text{pos}} $ 为语义相似句对分布（如 STS-B 标注对）。值越小，语义相近句向量越接近。  
- **Uniformity（均匀性）**：  
  $ \mathcal{L}_{\text{unif}} = \log \mathbb{E}_{x,y \sim p_{\text{data}}} \left[ e^{-2 \| f(x) - f(y) \|^2} \right] $，  
  衡量向量在超球面上的分布离散程度；值越小，语义无关句向量越分散。  
- **理想表征**：同时优化 $ \mathcal{L}_{\text{align}} $ 与 $ \mathcal{L}_{\text{unif}} $，避免各向异性（anisotropy）——即向量坍缩至低维子空间。

### 方法分类与对比（原文第35–38页）  
| 方法 | 公式 | 优点 | 缺点 | 典型场景 |
|------|------|------|------|----------|
| **平均池化** | $ \mathbf{s} = \frac{1}{n}\sum_{i=1}^n \text{emb}(w_i) $ | 简单、O(n)、无需训练 | 忽略词序、权重、长文本语义漂移 | 工业实时检索（语音客服毫秒响应） |  
| **TF-IDF 加权平均** | $ \mathbf{s} = \sum_{i=1}^n \text{idf}(w_i) \cdot \text{emb}(w_i) $ | 强调关键词，短文本效果提升 | 仍忽略语序与句法 | 新闻标题聚类 |  
| **WMD** | 见 [[concepts/word_mover_distance]] | 无参、可解释、精度高 | $ O(p^3 \log p) $，不可扩展 | 小批量离线分析 |  
| **SBERT 微调** | $ \mathcal{L} = \text{MSE}(\cos(f_A, f_B), y) + \text{TripletLoss} $ | 端到端优化 alignment/uniformity，SOTA | 需标注数据、推理延迟 ms 级 | 语义搜索、聚类 |  

### BERT 的各向异性问题（原文第37页）  
- 原始 BERT 在 MLM+NSP 预训练中，仅用 `[CLS]` 向量做分类，导致：  
  - `[CLS]` 向量在超球面呈**尖峰分布**（highly anisotropic）；  
  - 向量范数差异大，余弦相似度失真；  
  - 聚类性能差（uniformity 指标差）。  
- 解决方案：引入对比学习（如 SBERT、SimCSE），显式拉近正例、推远负例。

## 相关页面  
[[concepts/word2vec]]  
[[concepts/bert]]  
[[concepts/word_mover_distance]]  
[[models/sbert]]  
[[concepts/contrastive_learning]]  
[[concepts/alignment_and_uniformity]]  

## 来源  
《百面大模型》，第35–38页，“1.4 词向量与语义相似度”、“1.5 构建句子向量”节；对齐性/均匀性定义、BERT 各向异性分析、SBERT 架构均直接引自原文。