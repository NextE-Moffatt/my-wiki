# SimCSE

_最后更新：2026-04-13_

## 概述  
SimCSE（Gao et al., 2021）是一种**无监督句子嵌入方法**，利用BERT的Dropout随机性构造正例对，通过对比学习拉近同一句子不同扰动表征、推远不同句子表征，在无标注数据下实现接近监督SBERT的句向量质量（STS-B 76.3 → 81.6），并显著提升向量空间均匀性。

## 详细内容  

### 无监督对比学习机制  
- **正例构造**：对同一句子 $ x $，两次独立前向传播（因Dropout mask不同）生成表征 $ h_i^{(1)}, h_i^{(2)} \in \mathbb{R}^d $，视作语义一致正例；  
- **Batch内负例**：同batch中其余 $ 2N-2 $ 个句子表征构成负例；  
- **损失函数（InfoNCE变体）**：  
  $$
  \mathcal{L}_{\text{unsup}} = -\log \frac{\exp(\text{sim}(h_i^{(1)}, h_i^{(2)})/\tau)}{\sum_{j=1}^{2N} \mathbb{I}_{[j\neq i]} \exp(\text{sim}(h_i^{(1)}, h_j^{(k)})/\tau)}
  $$  
  其中 $ \text{sim}(u,v)=u^\top v $，温度系数 $ \tau=0.05 $，$ k \in \{1,2\} $ 表示另一视角。

### 有监督扩展与优化  
- **有监督SimCSE**：在NLI数据上，将前提-蕴含对作为正例、前提-矛盾对作为负例，损失函数为：  
  $$
  \mathcal{L}_{\text{sup}} = -\log \frac{\exp(\text{sim}(h_p, h_h)/\tau)}{\exp(\text{sim}(h_p, h_h)/\tau) + \sum_{n} \exp(\text{sim}(h_p, h_n)/\tau)}
  $$  
- **偏差问题与ESimCSE改进**：原始SimCSE因batch内句子长度差异导致模型误学“长度相似性”；ESimCSE引入**轻量扰动**（随机增删词、同义词替换），在保持语义不变前提下增强正例多样性，提升STS-B至82.0。

### 实证性能与理论意义  
- STS-B结果（BERT-base）：  
  - 无监督：81.6（+5.3 vs SBERT无监督基线）  
  - 有监督：84.4（逼近SBERT 85.4）  
- 核心贡献：首次证明**Dropout可作为免费数据增强器**，为无监督表征学习提供新范式；其成功验证了“**表征稳定性即语义一致性**”假设。

## 相关页面  
[[models/sbert]] [[concepts/contrastive_learning]] [[concepts/dropout_as_augmentation]] [[concepts/ood_generalization]] [[concepts/alignment_and_uniformity]] [[papers/attention_is_all_you_need]]

## 来源  
《百面大模型》第39–40页；Gao et al. (2021), *SimCSE: Simple Contrastive Learning of Sentence Embeddings*, EMNLP.