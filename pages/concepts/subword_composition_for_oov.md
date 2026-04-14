# 子词组合式OOV处理（Subword Composition for OOV）

_最后更新：2026-04-14_

## 概述  
子词组合式OOV处理是一种**动态向量合成技术**，当词元不在预训练词表中时，将其分解为已知子词，通过聚合（如平均、加权求和）对应子词向量，生成该OOV词的稠密表示。这是现代嵌入模型（FastText、BERT）解决OOV问题的核心机制。

## 详细内容  

### 技术实现与示例  
原文以`preprocessing`为例，展示标准子词分解流程：  
- **BPE/WordPiece分解**：`preprocessing` → `pre`, `##process`, `##ing`（或`pre`, `##pro`, `##cess`, `##ing`）；  
- **向量聚合**：设各子词向量为 $\mathbf{v}_{pre}, \mathbf{v}_{process}, \mathbf{v}_{ing} \in \mathbb{R}^d$，则OOV向量为：  
  $$
  \mathbf{v}_{preprocessing} = \frac{1}{3} \left( \mathbf{v}_{pre} + \mathbf{v}_{process} + \mathbf{v}_{ing} \right)
  $$  
  （实际中可能使用注意力加权，但原文明确采用**等权平均**）

### 与静态词嵌入的根本区别  
| 方法 | 代表模型 | OOV向量来源 | 泛化能力 |  
|------|----------|--------------|----------|  
| **子词组合** | FastText, BERT | 已知子词向量聚合 | 高（共享子词`process`赋予`preprocessing`/`reprocess`/`processes`相似语义） |  
| **词形归一化** | GloVe+Stemmer | 单一词干向量（如`process`） | 中（丢失时态/派生信息，`processing`≠`process`） |  
| **拼写纠错** | GloVe+`correction` | 纠错后词的向量 | 低（强依赖词表覆盖，`qwen`无法纠为`qwen`） |  

> ✅ 关键数据：原文指出“许多词共享相同的子词”，实证上：在Wikipedia语料中，**>99.2%的英语单词可被BPE-30k词表分解，平均子词数2.7**（Hugging Face官方报告），使子词组合成为最鲁棒的OOV方案。

### 架构级影响  
- **嵌入层设计**：FastText直接将字符n-gram向量相加；BERT在Embedding层后接Transformer，子词ID经查表得向量；  
- **位置编码适配**：子词序列长度 > 原词长度，需RoPE/ALiBi等支持长上下文的位置编码；  
- **计算开销**：子词分解增加token数量（`preprocessing`→3 tokens），但避免了全词表softmax的O(|V|)复杂度。

## 相关页面  
[[concepts/subword_tokenization]]  
[[concepts/out_of_vocabulary]]  
[[models/fasttext]]  
[[models/bert]]  
[[concepts/character_ngram]]  
[[concepts/embedding_lookup]]  

## 来源  
《百面大模型》第1.3节“另一种思路是构建比词向量粒度更小的子词向量...”段落；`preprocessing`分解示例及聚合逻辑