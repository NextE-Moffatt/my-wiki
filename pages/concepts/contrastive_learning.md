# Contrastive Learning

_最后更新：2026-04-13_

## 概述  
对比学习（Contrastive Learning）是一种**自监督/弱监督表征学习范式**，通过拉近正例对（语义相似）距离、推远负例对（语义不相关）距离，优化嵌入空间的几何结构，核心目标是提升**对齐性（alignment）与均匀性（uniformity）**。

## 详细内容  

### 数学形式化  
- 给定batch $ \mathcal{B} = \{x_i\}_{i=1}^N $，对每个样本 $ x_i $，定义正例集 $ \mathcal{P}_i $（如SimCSE中Dropout扰动）与负例集 $ \mathcal{N}_i = \mathcal{B} \setminus \{x_i\} $；  
- InfoNCE损失（van den Oord et al., 2018）：  
  $$
  \mathcal{L}_{\text{cont}} = -\mathbb{E}_{x_i \sim \mathcal{B}} \left[ \log \frac{ \exp(\text{sim}(f(x_i), f(x_i^+))/\tau) }{ \sum_{x_j \in \mathcal{P}_i \cup \mathcal{N}_i} \exp(\text{sim}(f(x_i), f(x_j))/\tau) } \right]
  $$  
  其中 $ f(\cdot) $ 为编码器，$ \tau $ 为温度系数（典型值0.05–0.1）。

### 在句子嵌入中的关键应用  
| 方法       | 正例构造方式                  | 负例来源         | STS-B (BERT-base) | 空间特性               |  
|------------|-------------------------------|------------------|---------------------|------------------------|  
| **SBERT**  | 人工标注语义等价对（NLI）     | Batch内其他句子  | 85.4                | 高对齐，中等均匀性     |  
| **SimCSE** | 同一句子两次Dropout前向传播   | Batch内其他句子  | 81.6                | **高均匀性**，对齐稍弱 |  
| **ESimCSE**| 同义词替换+随机增删           | Batch内其他句子  | 82.0                | 均匀性↑，对齐性↑       |  

### 理论基础与挑战  
- **对齐性-均匀性权衡**：Chuang et al. (2022) 证明InfoNCE同时优化：  
  - Alignment: $ \mathbb{E}_{(x,x^+) \sim p_{\text{pos}}} [\|f(x)-f(x^+)\|^2] $  
  - Uniformity: $ \log \mathbb{E}_{x,x' \sim p_{\text{data}}} [\exp(-\|f(x)-f(x')\|^2)] $  
- **负例诅咒**：batch size过小导致负例不足，降低判别力；SimCSE使用2×N batch（双视角）缓解此问题。

## 相关页面  
[[models/sbert]] [[models/simcse]] [[concepts/alignment_and_uniformity]] [[concepts/dropout_as_augmentation]] [[concepts/sentence_embedding]] [[concepts/ood_generalization]]

## 来源  
《百面大模型》第39–40页；Chuang et al. (2022), *An Empirical Study of Training Self-Supervised Vision Transformers*, ICCV.