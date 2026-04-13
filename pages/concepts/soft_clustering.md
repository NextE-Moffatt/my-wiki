# Soft Clustering（软聚类）

_最后更新：2026-04-12_

## 概述  
软聚类是一种允许样本以概率形式隶属多个簇的无监督学习方法，在大模型中广泛应用于专家路由（MoE）、错误检测（SEEED）与语义空间划分，其核心是替代硬划分（hard assignment）以提升鲁棒性与泛化性。

## 详细内容  
依据《百面大模型》第13.1.1节（p.337，MoE路由）、第1章语义建模（p.19–27，语义空间连续性）、及index中已存页面 [[models/seeed]] 的关联：  

- **数学定义**：  
  给定样本 $x$，软聚类输出隶属度向量 $\pi(x) = [\pi_1(x), ..., \pi_K(x)]$，满足 $\pi_k(x) \geq 0$ 且 $\sum_{k=1}^K \pi_k(x) = 1$。  
  - **GMM（高斯混合模型）**：$\pi_k(x) = \frac{\alpha_k \mathcal{N}(x \mid \mu_k, \Sigma_k)}{\sum_j \alpha_j \mathcal{N}(x \mid \mu_j, \Sigma_j)}$；  
  - **MoE Top-k Routing**：$\pi_k(x) = \text{softmax}_k(f(x))$，其中 $f(x)$ 为路由器网络输出，$k=2$（如DeepSeek-R1，p.337）。  

- **在大模型中的三大应用**：  
  1. **MoE专家路由**（p.337）：DeepSeek-R1使用soft Top-2 gating，避免单点故障，提升负载均衡；  
  2. **错误检测（SEEED）**：index中[[models/seeed]]定义为“Soft Clustering Extended Encoder-Based Error Detection”，其核心是将LLM输出映射至软聚类语义空间，识别异常模式（如逻辑矛盾、事实幻觉）；  
  3. **语义表示连续化**：第1章强调语义是“连续分布”，而非离散标签——软聚类天然契合此观点，如BERT句向量经soft clustering可生成层次化语义图谱（p.19）。  

- **对比硬聚类（Hard Clustering）**：  
  - 硬聚类（如K-Means）强制 $x$ 归属唯一簇，对噪声敏感，边界不自然；  
  - 软聚类提供不确定性量化（$\pi_k(x)$ 即置信度），支撑OOD检测（[[concepts/ood_generalization]]）与self-reflection（[[concepts/self_reflection]]）。  

## 相关页面  
[[models/deepseek_r1]]  
[[models/seeed]]  
[[concepts/ood_generalization]]  
[[concepts/self_reflection]]  

## 来源  
《百面大模型》第13.1.1节（p.337，MoE软路由）、第1章（p.19–27，语义连续性）；Wiki index中[[models/seeed]]明确定义其名称含“Soft Clustering”。