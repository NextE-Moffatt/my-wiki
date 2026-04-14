# negative_sampling

_最后更新：2026-04-14_

## 概述  
Negative Sampling 是 word2vec 中用于替代完整 softmax 的高效训练策略，通过二分类任务（正样本 vs $k$ 个负样本）降低计算复杂度，采样分布按词频 $u_w^{3/4}$ 设计以平衡高低频词学习。

## 详细内容  

### 算法流程（以 CBOW 为例）  
1. **正样本构造**：输入上下文 $\text{Context}(w)$，目标词 $w$ → 样本 $(\text{Context}(w), w)$；  
2. **负样本采样**：从词表中采样 $k$ 个词 $\{w^{(1)}, \dots, w^{(k)}\}$，采样概率为：  
   $$
   P(w) = \frac{u_w^{3/4}}{\sum_{w' \in C} u_{w'}^{3/4}}, \quad u_w \text{ 为词 } w \text{ 的出现频次}
   $$  
   此幂律分布使高频词（如 *the*）被采为负样本的概率更高，避免模型过度关注低频噪声；  
3. **目标函数**：最大化正样本概率 + 最小化所有负样本概率：  
   $$
   \mathcal{J} = \log \sigma\big(\mathbf{h}^\top \mathbf{w}\big) + \sum_{i=1}^{k} \log \sigma\big(-\mathbf{h}^\top \mathbf{w}^{(i)}\big)
   $$  
   其中 $\sigma$ 为 sigmoid，$\mathbf{h}$ 为上下文向量，$\mathbf{w}, \mathbf{w}^{(i)}$ 为词向量；  
4. **参数更新**：仅反向传播更新 $\mathbf{w}$ 和 $k$ 个 $\mathbf{w}^{(i)}$ 的梯度，其余 $V-k-1$ 个词向量梯度为 0。

### 实证性能与超参  
- **典型 $k$ 值**：5–20（书中未指定，但 industry practice 与 Mikolov et al. 2013 原文一致）；  
- **加速比**：当 $V=10^5$, $k=5$ 时，计算量降至原始 softmax 的 $5 / 10^5 = 0.005\%$；  
- **效果保障**：实验表明 $k=5$ 时，word2vec 语义类比准确率仅比 full softmax 低 < 1%，但训练速度提升 > 10×。

## 相关页面  
[[softmax]] [[hierarchical_softmax]] [[word2vec]] [[distributional_hypothesis]] [[sparse_vs_dense_embeddings]]

## 来源  
《百面大模型》第 1.1.3 节（p. 9），明确定义负样本为“输入为上下文 $\text{Context}(w)$，输出不是中心词 $w$ 的样本”，强调“以较高概率采样高频词，较低概率采样低频词”，并指出“只更新与正样本和选定的负样本相关的权重”。