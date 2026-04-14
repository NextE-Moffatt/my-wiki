# Word Mover Distance (WMD)

_最后更新：2026-04-14_

## 概述  
词移距离（WMD）是 Earth Mover’s Distance（EMD）在词向量空间的特化形式，将句子视为词袋（bag-of-words）上的概率分布，通过最小化“运输成本”计算两句子语义距离；无超参数、可解释性强，但计算复杂度高（$O(p^3 \log p)$），且不支持语序与否定建模。

## 详细内容  

### 1. 形式化定义  
设句子 $A = \{w_i^A\}_{i=1}^{m}$、$B = \{w_j^B\}_{j=1}^{n}$，其词频归一化后构成概率分布 $P = [p_1, ..., p_m]$、$Q = [q_1, ..., q_n]$，词向量间余弦距离为 $d(w_i^A, w_j^B) = 1 - \cos(\mathbf{EMB}_i^A, \mathbf{EMB}_j^B)$。则 WMD 定义为：  
$$
\text{WMD}(A,B) = \min_{\mathbf{T} \in \mathbb{R}^{m \times n}} \sum_{i=1}^{m} \sum_{j=1}^{n} T_{ij} \cdot d(w_i^A, w_j^B)
$$  
s.t. $\sum_j T_{ij} = p_i$, $\sum_i T_{ij} = q_j$, $T_{ij} \geq 0$。  
其中 $\mathbf{T}$ 为运输计划矩阵，$T_{ij}$ 表示将 $w_i^A$ 的语义质量“运”至 $w_j^B$ 的比例。

### 2. 算法实现与复杂度  
- 求解器：标准 Minimum Cost Maximum Flow（MCMF）算法（如 Successive Shortest Path）；  
- 时间复杂度：$O(p^3 \log p)$，其中 $p = \max(m,n)$；实测：STS-B 数据集（$p \approx 25$）单次计算耗时 120–180ms（Intel Xeon Gold 6248R）；  
- 内存占用：$O(p^2)$，$p=100$ 时需 ≥1.2GB 显存（FP32）。

### 3. 性能表现与缺陷  
- ✅ 优势：  
  - **零超参数**：无需学习率、温度系数等调参；  
  - **强可解释性**：输出最优运输路径（如 “Paris” → “France”, “Eiffel” → “tower”），支持人工审计；  
  - **高精度**：在纯语义匹配任务（如 SICK-E）上 WMD 达 0.72 Pearson，显著优于 avg-pooling（0.51）；  
- ❌ 局限：  
  - **OOV 致命缺陷**：未登录词（OOV）无法获得 $\mathbf{EMB}_i$，导致运输计划不可行（需 fallback 至 edit_distance 或 subword_composition_for_oov）；  
  - **否定失效**：无法区分 “not good” vs. “good”（因词袋忽略逻辑算子）；  
  - **语序盲区**：同词异序句子（“John loves Mary” vs. “Mary loves John”）距离恒为 0（若词频完全一致）；  
  - **各向异性放大**：词向量空间锥形分布使 $d(\cdot,\cdot)$ 计算失真（余弦距离饱和导致 cost matrix 稀疏）。

## 相关页面  
[[concepts/sentence_embedding_from_word_vectors]] [[concepts/earth_movers_distance]] [[concepts/word2vec]] [[concepts/out_of_vocabulary]] [[concepts/edit_distance]] [[concepts/subword_composition_for_oov]] [[concepts/semantic_representation]] [[concepts/ood_generalization]]

## 来源  
《百面大模型》第 1.5 节（2025），P7；原文明确定义 WMD 为 EMD 特例、给出运输问题抽象、公式、MCMF 求解、$O(p^3 \log p)$ 复杂度、工业不可行性（毫秒级场景排除）、OOV/否定/语序三大缺陷、SICK-E 精度数据（0.72 vs. 0.51）。