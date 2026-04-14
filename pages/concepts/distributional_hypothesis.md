# distributional_hypothesis

_最后更新：2026-04-14_

## 概述  
分布式语义假设（Distributional Hypothesis）是词向量技术的理论基石，断言“一个词的含义由其上下文决定”，即上下文分布相似的词具有语义相似性，该假设直接驱动了 word2vec、GloVe、FastText 等稠密嵌入方法的设计。

## 详细内容  

### 形式化表述  
> **"You shall know a word by the company it keeps."** （Firth, 1957）  
数学化表达为：  
若两词 $w_i$, $w_j$ 在大规模语料中共享相似的上下文分布 $P(\text{Context} \mid w_i) \approx P(\text{Context} \mid w_j)$，则其语义相似度 $sim(w_i, w_j) \approx 1$。  

该假设构成所有统计型词向量的 **归纳偏置（inductive bias）** ——模型训练目标被显式设计为逼近该分布相似性（如 skip-gram 最大化 $p(\text{Context}\mid w)$，GloVe 最小化 $\| \log P_{ij} - \mathbf{u}_i^\top \mathbf{v}_j \|_2^2$）。

### 实证验证与边界  
- **强支持证据**：  
  - word2vec 的语义类比任务（*king*–*man*+*woman*≈*queen*）准确率 > 75%（Mikolov et al., 2013）；  
  - GloVe 在语义相似度任务（WordSim-353）上 Spearman 相关系数达 0.72（Pennington et al., 2014）。  
- **局限性**：  
  - 无法区分反义词（*hot* 与 *cold* 上下文高度重叠，但语义相反）；  
  - 对逻辑关系（如 *is-a*, *part-of*）建模弱于依存句法模型；  
  - 静态嵌入无法处理一词多义（见 [[polysemy_problem]]），需 contextual embedding 解决。

### 与后续技术的承继关系  
- **BERT 的深化**：将分布假设从“词级上下文窗口”扩展至“句子级全注意力上下文”，使 $P(\text{Context} \mid w)$ 动态依赖于整句语义结构；  
- **RAG 的延伸**：将“上下文”从局部滑动窗口拓展至外部知识库检索结果，实现跨文档分布建模。

## 相关页面  
[[word2vec]] [[glove]] [[fasttext]] [[contextual_embedding]] [[polysemy_problem]] [[semantic_representation]] [[sparse_vs_dense_embeddings]]

## 来源  
《百面大模型》第 1.1.2 节（p. 5），引述 Firth (1957) 原始表述；书中明确指出该假设是“对人类语言的归纳偏置”，并作为 word2vec/GloVe/FastText 的共同设计前提。