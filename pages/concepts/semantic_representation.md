# Semantic Representation

_最后更新：2026-04-13_

## 概述  
语义表征（Semantic Representation）指将自然语言符号（词、短语、句子）映射到可计算向量空间的过程，其质量由语义相似度与向量相似度的一致性（如 $\text{sim}_{\text{word}}(w_i,w_j) \approx \cos(\mathbf{v}_i,\mathbf{v}_j)$）衡量，是大模型能力的底层支柱。

## 详细内容  
- **演进三阶段**：  
  1. **离散表征**（pre-2003）：one-hot 编码（$\mathbf{e}_i \in \{0,1\}^N$），语义不可计算；  
  2. **静态稠密表征**（2003–2017）：word2vec/GloVe/FastText，基于分布假设，在固定维度 $d=300$ 空间中实现 $\cos(\mathbf{v}_i,\mathbf{v}_j) \propto \text{semantic similarity}$；  
  3. **动态上下文表征**（2018–present）：BERT/GPT，向量 $\mathbf{v}_i^{(s)}$ 依赖完整句子 $s$，支持一词多义建模与组合泛化。  
- **核心评估指标**：  
  - **词类比（Word Analogy）**：`king - man + woman ≈ queen`，word2vec 在 Google Analogy Dataset 上达 74% 准确率；  
  - **语义相似度（WordSim-353）**：Spearman 相关系数，GloVe 84.2 vs word2vec 77.6；  
  - **上下文敏感性**：BERT-large 在 WIC（Word-in-Context）任务上达 72.3% 准确率（SOTA），远超静态模型（~55%）。  
- **工程约束**：  
  - 维度权衡：$d=50$（FastText）适合轻量部署，$d=1024$（LLaMA-2）支持复杂推理；  
  - 归一化：生产系统中普遍对 $\mathbf{v}_i$ 进行 $L_2$ 归一化，使 $\cos$ 相似度等价于点积，加速 ANN 检索。

## 相关页面  
[[concepts/one_hot_encoding]]  
[[models/word2vec]]  
[[models/bert]]  
[[concepts/distributional_hypothesis]]  
[[concepts/polysemy_problem]]

## 来源  
《百面大模型》第1章导言（p.19–20）；强调“词向量就像一座桥梁...将自然语言中离散的词语巧妙地映射到计算机能够处理的向量空间中，从而实现语义可计算的目标”；第1.1.3节词向量算术示例（p.22）