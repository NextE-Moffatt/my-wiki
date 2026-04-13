# Sentence-BERT (SBERT)

_最后更新：2026-04-13_

## 概述  
Sentence-BERT（Reimers & Gurevych, 2019）是首个专为**句子级语义相似度计算**设计的孪生BERT微调框架，通过引入对比式监督训练目标，显著提升句向量空间的**对齐性（alignment）与均匀性（uniformity）**，在STS-B基准上达85.4 Spearman相关系数（优于池化BERT基线约12点）。

## 详细内容  

### 架构与训练范式  
SBERT采用**参数共享的双塔结构**（图1-6）：两个输入句子A、B分别经同一BERT编码器得到句向量 $ u, v \in \mathbb{R}^d $，后续通过三类联合损失函数优化：

1. **分类任务（Concatenation）**：拼接 $[u; v; |u-v|]$ 后接全连接层+softmax，预测语义等价标签（如STS-B二元/三元分类）；  
2. **回归任务（Cosine Similarity MSE）**：以余弦相似度 $ \cos(u,v) = \frac{u^\top v}{\|u\|\|v\|} $ 为回归目标，最小化均方误差；  
3. **三元组排序任务（Triplet Loss）**：对锚点句 $ s_a $、正例句 $ s_p $、负例句 $ s_n $，最大化目标函数：  
   $$
   \max \left( \|s_a - s_p\|_2 - \|s_a - s_n\|_2 + \epsilon \right), \quad \epsilon = 0.1
   $$  
   训练中需动态负采样（hard negative mining），显著提升向量空间判别力。

### 句向量构造与池化策略  
- 实验验证：**词元表征平均池化（mean pooling）** 在所有池化方式（[CLS]、max、sqrt-mean）中产生最优聚类特性与空间均匀性；  
- 平均池化公式：$ s = \frac{1}{n}\sum_{i=1}^{n} h_i $，其中 $ h_i \in \mathbb{R}^d $ 为BERT最后一层第 $ i $ 个token的隐藏状态；  
- 关键结论：该策略使句向量在语义空间中呈近似**各向同性分布**，直接支持余弦相似度作为无标度语义距离度量。

### 性能与局限  
- STS-B测试集：85.4（Spearman），远超BERT-base（76.3）与InferSent（75.8）；  
- 缺陷：依赖标注数据（NLI/STS），泛化至零样本领域时存在域偏移；其监督信号本质是**显式建模句间距离**，而非隐式学习语义结构。

## 相关页面  
[[models/bert]] [[concepts/sentence_embedding]] [[concepts/alignment_and_uniformity]] [[concepts/soft_clustering]] [[papers/towards_automated_error_discovery]] [[tools/hf_datasets_dialerrors]]

## 来源  
《百面大模型》第39页；Reimers & Gurevych (2019), *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*, EMNLP.