# 分词（Tokenization）

_最后更新：2026-04-13_

## 概述  
分词是将原始文本映射为离散、可计算的词元（token）序列的过程，是NLP系统的**第一道语义门控**，直接影响嵌入质量、模型容量与下游任务性能。

## 详细内容  

### 1. 粒度谱系与技术选型矩阵  
| 粒度 | 代表方法 | OOV缓解 | 形态建模 | 语义保真度 | 典型词表大小 |  
|--------|------------|-----------|--------------|----------------|------------------|  
| **字符（Character）** | CNN-LSTM输入层 | ★★★★☆ | ★★☆☆☆（无构词） | ★★☆☆☆（过细） | 100–500 |  
| **字符n-gram** | FastText | ★★★★★ | ★★★★☆ | ★★★☆☆ | 1M–2M |  
| **子词（Subword）** | BPE/WordPiece/Unigram | ★★★★★ | ★★★★★ | ★★★★☆ | 32k–64k |  
| **词（Word）** | 空格分词 | ★☆☆☆☆ | ★☆☆☆☆ | ★★★★☆（整词语义） | 100k–1M |  
| **词组（Phrase）** | SentencePiece phrase-aware | ★★★★☆ | ★★★★☆ | ★★★★★（保留idiom） | 64k–128k |  

> 注：依据《百面大模型》p.29–33对各方法OOV机制、形态能力的显式描述归纳。

### 2. 工业实践黄金准则  
- **首选子词**：95%以上SOTA模型（BERT/GPT/Llama）采用，平衡三要素；  
- **词级仅作baseline或对齐需求**：如评估指标需词级F1；  
- **字符n-gram为fallback兜底**：Hugging Face `tokenizers` 默认启用 `byte_fallback`；  
- **动态词表**：大模型推理时（如vLLM），采用PagedAttention管理子词缓存，避免重复分词开销。

### 3. 分词错误的级联影响  
- **嵌入污染**：`[UNK]` 向量常为零向量或随机噪声，导致attention权重坍缩；  
- **位置编码错位**：错误切分使RoPE偏移，损害长程依赖建模；  
- **错误传播**：在RAG中，chunk切分错误导致检索片段语义断裂（如`preprocessing`被截为`pre`+`processing`，丢失整体含义）。

## 相关页面  
[[concepts/subword_tokenization]]  
[[concepts/word_level_tokenization]]  
[[concepts/character_ngram]]  
[[concepts/position_encoding]]  
[[tools/flashattention]]（需token序列长度输入）  
[[tools/pagedattention]]（依赖token序列管理）  
[[concepts/rag_engineering]]（chunking是分词的下游应用）

## 来源  
《百面大模型》第1章第1.3节 “分词方法的区别与影响”，pp.29–33；整合各小节技术细节形成谱系分析