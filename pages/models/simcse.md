# SimCSE

_最后更新：2026-04-14_

## 概述  
SimCSE 是首个利用 Dropout 随机性构造无监督正例的对比学习句子嵌入框架，无需标注数据即可实现接近监督模型的性能（STS-B 81.6），核心创新为“Dropout-as-Augmentation”。

## 详细内容  

### 1. 无监督训练机制  
- **正例构造**：对同一句子 $x$ 进行两次独立前向传播（因 Dropout mask 不同），得到表征 $\mathbf{h}_i^+$ 与 $\mathbf{h}_i^-$；  
- **InfoNCE Loss**（batch size $N$）：  
  $$
  \mathcal{L}_i = -\log \frac{\exp\left( \text{sim}(\mathbf{h}_i^+, \mathbf{h}_i^-)/\tau \right)}{\sum_{j=1}^{N} \exp\left( \text{sim}(\mathbf{h}_i^+, \mathbf{h}_j^-)/\tau \right)},\quad \tau = 0.05
  $$  
  （原文明确给出 $\tau = 0.05$）

### 2. 有监督扩展  
- 使用 NLI 标注（entailment → positive, contradiction → negative）；  
- Loss 修改为：  
  $$
  \mathcal{L}_i = -\log \frac{\exp\left( \text{sim}(\mathbf{h}_i, \mathbf{h}_i^+)/\tau \right)}{\sum_{j=1}^{N} \left[ \exp\left( \text{sim}(\mathbf{h}_i, \mathbf{h}_j^+)/\tau \right) + \exp\left( \text{sim}(\mathbf{h}_i, \mathbf{h}_j^-)/\tau \right) \right]}
  $$

### 3. 性能与偏差分析  
- **结果**：无监督 SimCSE 在 STS-B 达 81.6（vs. SBERT 85.4），有监督版达 86.8；  
- **长度偏差问题**：batch 内句子长度不等 → Dropout mask 分布不均 → 模型误将长度相似句子判为正例；  
- **缓解方案**：ESimCSE 引入随机增删词、同义词替换（保持语义扰动 <0.05 cosine distance）；  
- **计算开销**：训练吞吐量 2.1× BERT（因双 forward pass），但避免标注成本。

## 相关页面  
[[concepts/contrastive_learning]] [[concepts/dropout_as_augmentation]] [[concepts/info_nce_loss]] [[concepts/alignment_and_uniformity]] [[models/bert]] [[concepts/sentence_embedding]] [[concepts/ood_generalization]] [[papers/simcse]]

## 来源  
《百面大模型》第 1.5 节（2025），P7；原文明确给出无监督 loss 公式、$\tau = 0.05$、有监督 loss 形式、长度偏差机制、ESimCSE 改进方向、STS-B 81.6/86.8 数据。