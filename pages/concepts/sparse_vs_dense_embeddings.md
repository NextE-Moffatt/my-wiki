# sparse_vs_dense_embeddings

_最后更新：2026-04-14_

## 概述  
稀疏嵌入（如 one-hot）与稠密嵌入（如 word2vec、FastText）在语义建模能力、计算效率与泛化性上存在根本性差异：前者维度等于词表大小、正交无语义距离，后者通过低维连续空间建模上下文共现关系，使语义相似词在向量空间中距离相近。

## 详细内容  

### 稀疏嵌入（Sparse Embeddings）  
- **定义**：以词表大小 $V$ 为维度的 one-hot 向量，仅第 $i$ 位为 1（对应词 $w_i$），其余全为 0，即 $\mathbf{e}_i = [0,\dots,1,\dots,0] \in \mathbb{R}^V$。  
- **数学性质**：任意两不同词向量满足 $\mathbf{e}_i^\top \mathbf{e}_j = 0$（正交），欧氏距离恒为 $\sqrt{2}$，余弦相似度恒为 0 → **无语义可计算性**。  
- **缺陷**：  
  - 维度灾难：$V$ 常达 $10^5\text{–}10^6$，导致存储与计算开销巨大；  
  - 无法建模近义词（如 *bicycle* 与 *bike*）、语法关系（如 *king*–*man* ≈ *queen*–*woman*）；  
  - 对 OOV 词完全失效，无泛化能力。

### 稠密嵌入（Dense Embeddings）  
- **核心思想**：基于 **分布式语义假设**（"You shall know a word by the company it keeps"），将词映射至低维连续空间 $\mathbb{R}^K$（$K \ll V$，典型值 $K=100\text{–}300$），使语义相似词向量夹角小、距离近。  
- **关键性质**：  
  - **语义类比可计算性**：$ \mathbf{v}_{\text{king}} - \mathbf{v}_{\text{man}} \approx \mathbf{v}_{\text{queen}} - \mathbf{v}_{\text{woman}} $（图 1-2 实证）；  
  - **聚类特性**：同义词、同类实体（如 *mountain*, *valley*, *peak*）在 PCA/t-SNE 可视化中显著聚集；  
  - **泛化性提升**：OOV 词可通过子词（FastText）或上下文（BERT）间接表征。

### 核心对比（量化结论）  
| 维度         | 稀疏嵌入（one-hot）       | 稠密嵌入（word2vec）         |
|--------------|---------------------------|------------------------------|
| 向量维度     | $V$（词表大小）           | $K$（通常 100–300）          |
| 存储开销     | $O(V)$ per token          | $O(K)$ per token             |
| 语义相似度   | 恒为 0（无意义）          | 余弦相似度 ∈ $[-1,1]$，具物理意义 |
| OOV 处理     | 完全失败                  | FastText：字符 n-gram 回退；BERT：动态上下文生成 |
| 训练目标     | 无（静态查表）            | Skip-gram：$\max \sum_{w\in C} \log p(\text{Context}(w)\mid w)$；CBOW：$\max \sum_{w\in C} \log p(w \mid \text{Context}(w))$ |

### 技术演进脉络  
- **one-hot → word2vec**：从“符号不可计算”到“静态语义可计算”，解决聚类与相似度问题；  
- **word2vec → BERT**：从“静态单义”到“动态多义”，突破 polysemy_problem；  
- **稠密嵌入的工程瓶颈**：softmax 分母需遍历 $V$ 项，计算复杂度 $O(V)$ → 引出 **hierarchical softmax**（哈夫曼树深度 $\leq \log_2 V$，降为 $O(\log V)$）与 **negative sampling**（每次仅更新正样本 + $k$ 个负样本权重，$k \ll V$，如 $k=5$）。

## 相关页面  
[[one_hot_encoding]] [[distributional_hypothesis]] [[polysemy_problem]] [[word2vec]] [[fasttext]] [[contextual_embedding]] [[subword_tokenization]] [[softmax]] [[hierarchical_softmax]] [[negative_sampling]]

## 来源  
《百面大模型》第 1.1 节（pp. 1–12），2025 年出版；编者注①明确“大语言模型”与“大模型”等价。