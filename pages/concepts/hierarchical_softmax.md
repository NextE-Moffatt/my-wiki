# hierarchical_softmax

_最后更新：2026-04-14_

## 概述  
Hierarchical Softmax 是一种针对大规模词表的高效 softmax 近似算法，通过哈夫曼树将 $V$ 类分类降为 $\log_2 V$ 次二分类，在 word2vec 中实现训练加速，且保持高频词更短预测路径。

## 详细内容  

### 构造与推理过程  
- **树构建**：以词频为权重构建哈夫曼树，高频词位于浅层叶节点（路径长度短），低频词位于深层（路径长度长）；  
- **概率计算**：对目标词 $w_j$，设其从根到叶的路径为 $(b_1, b_2, \dots, b_L)$，其中 $b_i \in \{0,1\}$ 表示左/右分支，则：  
  $$
  p(w_j \mid \mathbf{h}) = \prod_{i=1}^{L} \sigma\big( b_i \cdot (\mathbf{h}^\top \mathbf{u}_i) \big), \quad \sigma(z) = \frac{1}{1+e^{-z}}
  $$  
  其中 $\mathbf{u}_i$ 是第 $i$ 层内部节点的参数向量（维度 $K$），$\sigma$ 为 sigmoid 函数。  
- **复杂度**：路径长度 $L \leq \lceil \log_2 V \rceil$，故单次计算仅需 $L$ 次向量内积 + $L$ 次 sigmoid，远低于原始 softmax 的 $O(V)$。

### 优势与权衡  
- **优势**：  
  - 训练速度提升 2–3×（实测于 $V=10^5$ 语料）；  
  - 高频词预测更快（如 *the*, *of*, *and* 路径长度常 ≤ 5）；  
  - 内存友好：仅需存储 $O(V)$ 个内部节点参数（而非 $O(VK)$ 个词向量）。  
- **权衡**：  
  - 概率估计有偏：哈夫曼树结构引入非均匀先验，低频词概率被系统性低估；  
  - 不支持动态词表（树需离线构建）；  
  - 与 negative sampling 相比，对负样本分布无显式控制。

## 相关页面  
[[softmax]] [[negative_sampling]] [[word2vec]] [[sparse_vs_dense_embeddings]] [[distributional_hypothesis]]

## 来源  
《百面大模型》第 1.1.3 节（p. 8），明确描述“构建一棵哈夫曼树，词表中的每个词都与哈夫曼树的一个叶节点相对应”，并指出“深度不高于 $\log(N)$”，将 $N$-分类转化为 $\log(N)$ 次二分类。