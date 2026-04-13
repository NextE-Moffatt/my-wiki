# One-Hot Encoding

_最后更新：2026-04-13_

## 概述  
One-hot 编码是一种将离散词元（token）映射为高维稀疏向量的表征方式：词表大小为 $N$ 时，每个词被表示为 $N$ 维向量，其中仅对应词索引位置为 1，其余均为 0。它是词向量建模的起点，但不具备语义可计算性。

## 详细内容  
- **数学定义**：对词表 $\mathcal{V} = \{w_1, w_2, ..., w_N\}$，词 $w_i$ 的 one-hot 向量为 $\mathbf{e}_i \in \{0,1\}^N$，满足 $(\mathbf{e}_i)_j = \delta_{ij}$（Kronecker delta）。  
- **几何性质**：任意两个不同词的 one-hot 向量正交，欧氏距离恒为 $\sqrt{2}$，余弦相似度恒为 0（见原文图1-1标注）。  
- **核心缺陷**：  
  - ❌ 无法建模语义关系（如近义词、上下位关系）；  
  - ❌ 无泛化能力（未登录词无法表征）；  
  - ❌ 维度灾难：当 $N = 10^5$（典型大词表），向量稀疏度达 $99.999\%$，内存与计算效率极低。  
- **历史定位**：作为早期 NLP 系统（如 n-gram LM、朴素贝叶斯分类器）的输入层基础，后被稠密嵌入全面替代；但在现代 LLM 的 token embedding 层中，仍作为 *输入索引查找表（lookup table）的逻辑接口* 存在——即 `embedding[w_idx]` 实质是隐式 one-hot 查表。

## 相关页面  
[[concepts/tokenization]]  
[[concepts/subword_tokenization]]  
[[models/word2vec]]  
[[concepts/distributional_hypothesis]]  
[[concepts/out_of_vocabulary]]

## 来源  
《百面大模型》第1章第1.1.1节（p.20）；图1-1原始标注：“欧氏距离均为√2”、“余弦相似度均为0”