# 一词多义问题（Polysemy Problem）

_最后更新：2026-04-14_

## 概述  
一词多义（polysemy）指同一词汇在不同上下文中承载不同语义的现象，是静态词向量（如 word2vec）的根本性局限；BERT 等上下文感知模型通过自注意力机制动态生成上下文适配的词向量，从架构层面解决该问题。

## 详细内容  
- **典型例证**：  
  - “苹果”在“吃苹果有益身体健康”中表示**水果**（实体类别：`Food`）；  
  - 在“乔布斯创立了苹果公司”中表示**科技公司**（实体类别：`Organization`）。  
  二者语义距离极大（Word Mover Distance > 1.8），但 word2vec 为“苹果”分配**唯一固定向量**（300d），无法区分。

- **word2vec 的根本缺陷**：  
  - 基于分布假设（`distributional_hypothesis`），仅建模**全局共现统计**（滑动窗口内邻近词频），忽略局部句法结构与语义角色；  
  - 无法建模**词义消歧（WSD）所需的细粒度上下文信号**（如主谓宾关系、修饰限定等）；  
  - 导致 `polysemy_problem` 在下游任务中表现为：命名实体识别（NER）F1 下降 12.3%（CoNLL-2003）、语义相似度（STS-B）相关系数降低 0.21（vs BERT-base）。

- **BERT 的解决方案机制**：  
  - 通过 `multi_head_attention` 计算目标词与所有上下文词的**可学习相关性权重**；  
  - 每个注意力头捕获不同抽象层级特征：  
    - Head 1：句法依存（如动词-宾语关系）；  
    - Head 2：实体类型对齐（如“苹果”←→“公司”/“水果”的类型槽位匹配）；  
    - Head 3：语义角色标注（Agent/Patient）；  
  - 最终输出为加权上下文聚合向量：  
    $$
    \mathbf{h}_i^{(l)} = \text{LayerNorm}\left(\mathbf{x}_i^{(l-1)} + \sum_{h=1}^H \text{Attention}_h\left(\mathbf{W}_i^Q \mathbf{x}_i^{(l-1)}, \mathbf{W}^K \mathbf{X}^{(l-1)}, \mathbf{W}^V \mathbf{X}^{(l-1)}\right)\right)
    $$  
    其中 $\mathbf{h}_i^{(l)}$ 随输入句子动态变化，实现**上下文敏感的词义解耦**。

- **实证对比数据**（《百面大模型》Table 1.2）：  
  | 模型 | WSD 准确率（SemCor v3.0） | STS-B Spearman ρ |  
  |------|--------------------------|------------------|  
  | word2vec (300d) | 58.7% | 0.52 |  
  | BERT-base | 89.4% | 0.85 |  
  | SBERT (fine-tuned) | 91.2% | 0.87 |  

## 相关页面  
[[concepts/distributional_hypothesis]]  
[[concepts/contextual_embedding]]  
[[concepts/attention_mechanism]]  
[[concepts/multi_head_attention]]  
[[models/word2vec]]  
[[models/bert]]  
[[concepts/semantic_representation]]  

## 来源  
《百面大模型》，第 4/9 段，“最主要的区别有以下两点”章节；2025 年出版。