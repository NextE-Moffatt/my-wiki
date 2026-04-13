# word2vec

_最后更新：2026-04-13_

## 概述  
`word2vec` 是 Mikolov 等人于 2013 年提出的浅层神经网络模型，通过 `CBOW`（Continuous Bag-of-Words）或 `Skip-gram` 架构学习静态稠密词向量，其核心局限在于**无法建模上下文敏感语义**，导致严重的一词多义问题。

## 详细内容  

### 架构与训练目标  
- `CBOW`：用上下文词预测目标词，输入为上下文窗口内词向量均值，输出为目标词概率分布；  
- `Skip-gram`：用目标词预测上下文词，输入为目标词向量，输出为各上下文词概率分布（原文未提架构名，但“上下文共现关系特征”明确指向此机制）；  
- 向量维度：通常 100–300 维（原文第27页 `wiki-news-300d`、`glove.840B.300d` 均为 300 维，可推 `word2vec` 主流亦为 300d）；  
- 词表：固定大小（如 `GoogleNews-vectors-negative300.bin` 含 3M 词），无动态扩展能力。

### 一词多义失效的机理（原文第24页核心论断）  
- `word2vec` 向量 = 所有出现语境中上下文词向量的**线性加权平均** → 语义被“平滑”掉；  
- 示例 `apple`：在语料中同时出现在 `fruit` 与 `tech` 语境，其最终向量位于二者语义空间连线中点 → 既不像水果也不像公司，造成表示失真；  
- 对比 `BERT`：`BERT` 使用 `multi_head_attention`，每个 head 可专注不同语义维度（如 head1 捕捉实体类型，head2 捕捉情感倾向），从而分离多义。

### OOV 处理能力  
- **零原生支持**：`word2vec` 模型无子词机制，遇到 OOV 词只能返回 `unknown_vector`（如 `np.zeros(300)-1.0`）或报错；  
- 工程 workaround：依赖外部词干提取（`PorterStemmer`）、拼写纠错（`edits1`）等（原文第25–28页详述），但效果有限（如 `running` → `run` 成功，但 `skibidi` 无词干可提）。

## 相关页面  
[[concepts/polysemy_problem]]  
[[concepts/out_of_vocabulary]]  
[[concepts/distributional_hypothesis]]  
[[models/bert]]  
[[tools/errdetect]]  

## 来源  
《百面大模型》，第1章“语义表达”，第24、25–28页（2025）