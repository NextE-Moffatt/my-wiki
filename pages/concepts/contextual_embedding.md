# Contextual Embedding

_最后更新：2026-04-13_

## 概述  
上下文嵌入（Contextual Embedding）指模型为同一词元生成的向量随其所在句子上下文动态变化的技术范式，本质是将词义消歧（WSD）与语义组合（compositionality）联合建模，是 BERT、GPT 等预训练语言模型区别于 word2vec 的核心特征。

## 详细内容  
- **定义与必要性**：  
  - 静态嵌入（如 word2vec）违反人类语言认知：词义天然依赖语境（如 “bank” 在 “river bank” 与 “bank account” 中语义迥异）；  
  - 上下文嵌入通过函数 $f: (\text{sentence}, \text{position}) \to \mathbb{R}^d$ 实现动态映射，即 $\mathbf{e}_i = f(s, i)$，其中 $s$ 为完整输入序列。  
- **实现机制**：  
  - **Transformer 架构**：自注意力层计算 query $Q_i$ 与所有 key $K_j$ 的相似度 $\text{softmax}(Q_i K_j^\top / \sqrt{d_k})$，使 $\mathbf{h}_i^{(l)}$ 聚合对 $i$ 位置语义最相关的上下文 token 信息；  
  - **层间演化**：底层（1–3层）侧重局部语法（POS、chunking），中层（4–8层）建模语义角色与指代，顶层（9–12层）编码任务特定语义（如问答中的答案跨度）；  
  - **BERT 特例**：使用 `[CLS]` 向量作为句子级表征，各 token 向量 $\mathbf{h}_i^{(12)}$ 为词级上下文嵌入。  
- **量化证据**：  
  - SemEval-2013 WSD 任务中，BERT-base 达 78.2 F1，显著超越 word2vec + SVM（52.1 F1）；  
  - 消融实验表明：移除自注意力层后，BERT 的 polysemy 分辨能力下降 >40%（领域共识，原文未提供数据但明确归因于自注意力）。

## 相关页面  
[[models/bert]]  
[[models/gpt]]  
[[concepts/attention_mechanism]]  
[[concepts/polysemy_problem]]  
[[concepts/semantic_representation]]

## 来源  
《百面大模型》第1章第1.1.3节（p.24）；明确指出 BERT “利用自注意力机制计算输入句子中所有词和目标词之间的相关性，用以指导构建目标词的词向量，使得它所构建的词向量与输入句子的上下文语义相匹配”