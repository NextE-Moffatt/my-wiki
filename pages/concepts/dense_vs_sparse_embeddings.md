# 稀疏词向量 vs 稠密词向量

_最后更新：2026-04-13_

## 概述  
稀疏词向量（如 one-hot）与稠密词向量（如 Word2Vec、BERT embedding）是语义表征的两种根本范式：前者维度高、正交、无泛化能力；后者维度低、连续、具备语义相似性度量与组合性，是现代NLP语义建模的基石。

## 详细内容  

### 1. 稀疏词向量（Sparse Embeddings）  
- **定义**：以词表大小 $V$ 为维度的 one-hot 向量，第 $i$ 维为 1 当且仅当对应词为词汇表中第 $i$ 个词，其余为 0。  
- **数学形式**：$\mathbf{e}_w = \mathbf{e}_i \in \mathbb{R}^V$, where $\mathbf{e}_i[j] = \delta_{ij}$.  
- **缺陷**：  
  - 维度灾难：典型词表 $V \sim 50k\text{–}100k$，导致矩阵稀疏、内存爆炸；  
  - 语义零相关：$\cos(\mathbf{e}_{\text{king}}, \mathbf{e}_{\text{queen}}) = 0$，无法表达类比（如 king − man + woman ≈ queen）；  
  - 无法处理 OOV（out-of-vocabulary）词，需回退至 `<unk>` 或 subword fallback。  

### 2. 稠密词向量（Dense Embeddings）  
- **核心思想**：将词映射到低维连续向量空间 $\mathbb{R}^d$（$d \ll V$，通常 $d=768\text{–}4096$），使语义相近词在欧氏/余弦距离下靠近。  
- **建模依据**：严格依赖 **分布假设（Distributional Hypothesis）** —— “a word is characterized by the company it keeps”（Firth, 1957）。  
- **关键性质**：  
  - ✅ **语义可计算性**：支持向量运算（如 $\mathbf{v}_{\text{king}} - \mathbf{v}_{\text{man}} + \mathbf{v}_{\text{woman}} \approx \mathbf{v}_{\text{queen}}$）；  
  - ✅ **泛化能力**：对未见搭配（如 “neural transformer”）可基于上下文向量组合推断；  
  - ✅ **降维压缩**：$V=100k \to d=768$，压缩比达 $130\times$，显著降低模型参数与计算开销。  

### 3. 实践对比（《百面大模型》P6–7）  
| 维度         | 稀疏词向量              | 稠密词向量                          |
|--------------|-------------------------|----------------------------------------|
| 典型维度     | $V \sim 10^5$           | $d = 768, 1024, 4096$                 |
| OOV 处理     | 无原生支持，需 `<unk>`  | 可通过 subword tokenization（如 BPE）或 character-level fallback 解决 |
| 语义相似度   | 恒为 0（余弦）          | 可量化（如 `cosine_sim(“car”, “truck”) ≈ 0.82`） |
| 训练目标     | 无（静态查表）          | MLM（BERT）、NSP、causal LM（GPT）、Skip-gram（Word2Vec）等 |

> ⚠️ 矛盾：部分旧教材称“one-hot 是稠密表示”，此为术语误用。本页严格遵循 NLP 社区共识：**稠密（dense）指非零元素比例高、连续可微、具备几何结构；稀疏（sparse）指绝大多数元素为零、离散、不可微**。参见 [[subword_tokenization]] 和 [[distributional_hypothesis]]。

## 相关页面  
[[subword_tokenization]]  
[[distributional_hypothesis]]  
[[word2vec]]  
[[bert]]  
[[out_of_vocabulary]]  
[[semantic_representation]]  
[[one_hot_encoding]]

## 来源  
《百面大模型》，第 1 章 1.1.3 节 “稠密词向量”，第 19 页；第 15 页问答：“如何利用词向量进行无监督句子相似度计算？”