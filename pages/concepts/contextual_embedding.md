# contextual_embedding

_最后更新：2026-04-14_

## 概述  
Contextual embedding 是指词向量随输入上下文动态变化的表示方式，由 BERT 等预训练模型实现，从根本上解决 polysemy_problem，其核心是利用自注意力机制对全句语义进行加权聚合。

## 详细内容  

### 与静态嵌入的本质区别  
| 维度 | 静态嵌入（word2vec） | Contextual Embedding（BERT） |
|------|----------------------|-------------------------------|
| **向量生成** | 词形唯一映射：$w \mapsto \mathbf{v}_w$ | 词形+上下文联合映射：$(w, \text{sentence}) \mapsto \mathbf{v}_w^{\text{sent}}$ |
| **语义建模** | 共现统计（local window） | 全局依赖（self-attention over all tokens） |
| **多义处理** | ❌ 同一词形恒等向量 | ✅ 同一词形在不同句中向量差异显著（如 *apple* 例） |
| **下游适配** | 需额外特征工程 | 可直接微调（fine-tuning）或提示（prompting） |

### BERT 的实现机制（书中要点）  
- **输入表示**：token embedding + segment embedding + position embedding（见 [[position_encoding]]）；  
- **核心运算**：Multi-Head Self-Attention 层，对每个 token $w_i$ 计算：  
  $$
  \text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V, \quad Q=WK^Q, K=WK^K, V=WK^V
  $$  
  其中 $W$ 为输入投影，$K^Q,K^K,K^V$ 为可学习权重；  
- **动态性来源**：每个 token 的输出向量是所有 token 的加权和，权重由 query-key 相似度决定 → 上下文改变则权重分布改变 → 输出向量改变。

## 相关页面  
[[bert]] [[polysemy_problem]] [[attention_mechanism]] [[position_encoding]] [[sparse_vs_dense_embeddings]] [[distributional_hypothesis]]

## 来源  
《百面大模型》第 1.1.3 节（p. 11），明确对比 “word2vec 无法解决一词多义” 与 “BERT 利用自注意力机制...使词向量与上下文语义相匹配”，并指出 BERT 向量“随句子不同而改变”。