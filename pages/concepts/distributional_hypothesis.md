# Distributional Hypothesis

_最后更新：2026-04-13_

## 概述  
“你应能根据一个词周边的其他词理解它的含义”（You shall know a word by the company it keeps）——该假设是现代词向量技术的理论基石，主张词义由其分布环境（上下文共现模式）决定，并可作为归纳偏置（inductive bias）融入模型训练目标。

## 详细内容  
- **形式化表述**：设词 $w$ 的上下文分布为 $P(c|w)$，则语义相似度 $\text{sim}(w_i, w_j) \propto \text{KL}(P(c|w_i) \| P(c|w_j))$ 或 $\cos(\mathbf{v}_i, \mathbf{v}_j)$（当 $\mathbf{v}_i, \mathbf{v}_j$ 为稠密嵌入）。  
- **技术实现路径**：  
  - **统计驱动**：GloVe 通过共现矩阵 $\mathbf{X}$ 的分解，最小化 $\sum_{i,j} f(X_{ij}) (\mathbf{u}_i^\top \mathbf{v}_j + b_i + c_j - \log X_{ij})^2$；  
  - **预测驱动**：word2vec 的 skip-gram 最大化 $\sum_{w \in \mathcal{C}} \log P(\text{Context}(w) \mid w)$，CBOW 最大化 $\sum_{w \in \mathcal{C}} \log P(w \mid \text{Context}(w))$；  
  - **深度学习驱动**：BERT 在 MLM 任务中隐式优化该假设，通过自注意力聚合动态上下文分布。  
- **关键证据**：word2vec 训练后出现的向量算术现象（如 $\mathbf{v}_{\text{king}} - \mathbf{v}_{\text{man}} \approx \mathbf{v}_{\text{queen}} - \mathbf{v}_{\text{woman}}$）直接验证了该假设在稠密空间中的几何实现（原文 p.22 图1-2）。

## 相关页面  
[[concepts/semantic_representation]]  
[[models/word2vec]]  
[[models/gloved]]  
[[models/bert]]  
[[concepts/soft_clustering]]

## 来源  
《百面大模型》第1章第1.1.2节（p.21）；引用原句“You shall know a word by the company it keeps.”；图1-2向量算术示例（p.22）