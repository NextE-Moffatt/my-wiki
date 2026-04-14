# softmax

_最后更新：2026-04-14_

## 概述  
Softmax 是词向量与语言建模中的核心归一化函数，将未归一化的 logits 映射为概率分布，但其原始实现因需遍历整个词表导致计算瓶颈，催生 hierarchical softmax 与 negative sampling 等优化方案。

## 详细内容  

### 数学定义与计算瓶颈  
给定隐藏层输出 $\mathbf{h} \in \mathbb{R}^K$ 与输出层权重矩阵 $\mathbf{W} \in \mathbb{R}^{K \times V}$，softmax 输出第 $j$ 个词的概率为：  
$$
p(w_j \mid \mathbf{h}) = \frac{\exp(\mathbf{h}^\top \mathbf{w}_j)}{\sum_{i=1}^{V} \exp(\mathbf{h}^\top \mathbf{w}_i)}
$$  
- **分母计算复杂度**：$O(V)$，当 $V=10^5$ 时，单次前向传播需 $10^5$ 次指数运算 + 求和；  
- **反向传播开销**：梯度 $\frac{\partial \mathcal{L}}{\partial \mathbf{w}_i}$ 依赖所有 $V$ 个词的 logit，更新全量参数代价高昂。

### 优化方案（word2vec 中实证）  
| 方法 | 原理 | 复杂度 | 适用场景 | 关键参数 |
|------|------|--------|----------|----------|
| **Hierarchical Softmax** | 构建哈夫曼树（高频词路径短），将 $V$-分类转化为 $\leq \log_2 V$ 次二分类 | $O(\log V)$ | 词频分布偏斜明显（如新闻语料） | 哈夫曼编码表（预构建） |
| **Negative Sampling** | 将多分类改为二分类：判别正样本 $(\mathbf{h}, w_{\text{pos}})$ vs $k$ 个负样本 $(\mathbf{h}, w_{\text{neg}}^{(1)}), \dots$；负样本按 $P(w) \propto u_w^{3/4}$ 采样（$u_w$: 词频） | $O(k)$, $k \ll V$（典型 $k=5$–$20$） | 训练速度优先，且词频幂律分布显著 | $k$（负采样数）、$P(w)$ 采样分布 |

> 注：书中明确指出，negative sampling “在每次迭代中只更新与正样本和选定的负样本相关的权重”，避免全量更新，是 word2vec 实现工业级训练的关键。

## 相关页面  
[[word2vec]] [[hierarchical_softmax]] [[negative_sampling]] [[sparse_vs_dense_embeddings]] [[embedding_lookup]]

## 来源  
《百面大模型》第 1.1.3 节（pp. 8–9），详述 skip-gram/CBOW 中 softmax 瓶颈及两种优化算法的数学原理与工程选择依据。