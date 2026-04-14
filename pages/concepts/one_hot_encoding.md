# one_hot_encoding

_最后更新：2026-04-14_

## 概述  
One-hot encoding 是一种将离散词元映射为 $V$ 维稀疏向量的表征方式，其中 $V$ 为词表大小；每个词对应唯一坐标轴上的单位向量，其余维度全为 0。

## 详细内容  
- **数学定义**：对词表 $\mathcal{V} = \{w_1, w_2, ..., w_V\}$，词 $w_i$ 的 one-hot 向量为 $\mathbf{e}_i \in \{0,1\}^V$，满足 $(\mathbf{e}_i)_j = \delta_{ij}$（Kronecker delta）。  
- **几何性质**：任意两个 distinct one-hot 向量 $\mathbf{e}_i, \mathbf{e}_j$（$i \neq j$）满足：  
  - 欧氏距离：$\|\mathbf{e}_i - \mathbf{e}_j\|_2 = \sqrt{2}$（恒定，无区分度）  
  - 余弦相似度：$\cos(\theta) = \frac{\mathbf{e}_i^\top \mathbf{e}_j}{\|\mathbf{e}_i\| \|\mathbf{e}_j\|} = 0$（完全正交）  
- **语义建模缺陷**：  
  - 无法表达近义关系（如 *bicycle* 与 *bike* 相似度为 0）；  
  - 无法支持类比推理（如 *king − man + woman ≈ queen* 在 one-hot 空间无意义）；  
  - 向量空间各向同性且无结构，违背分布式语义假设 [[distributional_hypothesis]]。  
- **工程瓶颈**：  
  - 维度灾难：现代大模型词表 $V \sim 10^5$–$10^6$，导致 embedding lookup table 占用 GB 级显存（如 $V=32768$, $d=4096$ → $\sim 512$ MB FP16）；  
  - 稀疏性：99.99%+ 元素为 0，无法利用稠密矩阵计算硬件（GPU/TPU）的算力优势。  

> ⚠️ 矛盾：`pages/concepts/tokenization.md` 中称 “one-hot 是 tokenization 的输出表示”，但严格而言，tokenization 输出的是整数 ID（index），one-hot 是其 *可选的、低效的* 向量化实现；现代框架（PyTorch/HF）默认使用 embedding lookup（非 one-hot + matmul）规避该开销。此矛盾将在 `log.md` 中记录。

## 相关页面  
[[distributional_hypothesis]]  
[[sparse_vs_dense_embeddings]]  
[[tokenization]]  
[[embedding_lookup]]  
[[out_of_vocabulary]]  
[[semantic_representation]]

## 来源  
《百面大模型》第 1.1.1 节（2025），图 1-1 及配套文字说明