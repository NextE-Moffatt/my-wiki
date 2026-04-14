# word2vec

_最后更新：2026-04-14_

## 概述  
Word2Vec 是 Mikolov 等人于 2013 年提出的浅层神经网络框架，通过 Skip-gram 与 CBOW 两种架构学习稠密词向量，首次在大规模语料上实证分布式语义假设，奠定现代词嵌入基础。

## 详细内容  

### 架构与目标函数  
| 模型 | 输入 | 输出 | 目标函数 | 适用场景 |
|------|------|------|----------|----------|
| **Skip-gram** | 单个中心词 $w$ | 其上下文词 $\text{Context}(w)$ | $\max \sum_{w\in C} \log p(\text{Context}(w)\mid w)$ | 低频词学习强，适合小语料 |
| **CBOW** | 上下文词 $\text{Context}(w)$ | 中心词 $w$ | $\max \sum_{w\in C} \log p(w \mid \text{Context}(w))$ | 训练快、高频词精度高，适合大语料 |

- **共享结构**：输入层（one-hot, $1\times V$）→ 隐藏层（线性变换，$V\times K$ 权重矩阵）→ 输出层（$K\times V$ 权重矩阵）；  
- **词向量来源**：输入-隐藏层权重矩阵 $W_{\text{in}} \in \mathbb{R}^{V\times K}$ 的行向量即为词向量（$K=100$–$300$）。

### 关键创新与局限  
- **创新**：  
  - 提出 **hierarchical softmax** 与 **negative sampling**，解决 softmax 瓶颈（见 [[hierarchical_softmax]], [[negative_sampling]]）；  
  - 开源 C 实现，训练速度比当时主流工具快 2–3 个数量级；  
  - 首次在类比任务（*king*–*man*+*woman*）上达到实用精度（>75%）。  
- **局限（书中明确指出）**：  
  - **无法解决一词多义**：同一词（如 *苹果*）在不同上下文（水果 vs 公司）中共享唯一向量；  
  - **仅建模共现关系**：缺乏句法、逻辑等深层语义，而 BERT 的多头注意力可捕获词性、依存等特征。

## 相关页面  
[[sparse_vs_dense_embeddings]] [[distributional_hypothesis]] [[hierarchical_softmax]] [[negative_sampling]] [[polysemy_problem]] [[bert]] [[fasttext]]

## 来源  
《百面大模型》第 1.1.3 节（pp. 6–10），完整复现 skip-gram/CBOW 目标函数、模型结构图（图 1-3）、训练优化细节，并与 BERT 进行直接对比（p. 11）。