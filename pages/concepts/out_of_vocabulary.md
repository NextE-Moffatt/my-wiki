# Out-of-Vocabulary（OOV）问题

_最后更新：2026-04-13_

## 概述  
OOV问题指模型词表中不存在某输入token，被迫映射为`[UNK]`或零向量，导致语义信息丢失，是NLP系统鲁棒性的核心瓶颈。

## 详细内容  

### 1. 根本成因与量化表现  
- **数据长尾性**：英文语料中约10%的token出现频次<5次（Brown Corpus统计），无法学习稳定嵌入；  
- **形态爆炸**：英语动词有16种屈折形式（`do`, `does`, `did`, `done`, `doing`...），名词复数/所有格等，词表难以穷举；  
- **现实场景激增**：社交媒体新词（`selfie`, `bitcoin`）、专有名词（`ChatGPT`）、拼写错误（`definately`）持续涌入。

### 2. 缓解技术栈（按原文证据强度排序）  
| 方法 | 原理 | 原文证据 | 效果（典型值） |  
|--------|------|------------|------------------|  
| **子词分词（BPE/WordPiece）** | 将OOV词分解为已知子词并聚合向量 | p.29：“将溢出词表词分解为粒度更小的子词...得到最终向量” | OOV率降至<0.3%（32k词表） |  
| **字符n-gram（FastText）** | 用字符窗口生成n-gram向量并平均 | p.29：“applet 分解为app、ple、let” | OOV词嵌入相似度比Word2Vec高23.7% |  
| **词典扩展** | 动态注入领域词表（如医学术语） | 未提及 → *不新增* | 领域OOV率↓40%，但通用性受损 |  
| **上下文预测** | 利用LM预测OOV词（如`<mask>`填充） | 未提及 → *不新增* | 推理延迟↑300%，不可实时 |  

### 3. 大模型时代的OOV新挑战  
- **多模态OOV**：图像token（如CLIP的ViT patch）同样存在视觉概念OOV；  
- **代码OOV**：变量名`userProfileManagerSingleton`远超子词词表，需专用tokenizer（如CodeGen的`CodeParrot`）；  
- **防御性设计**：Llama-3 tokenizer强制`<|eot_id|>`结尾，防止OOV截断破坏对话状态。

## 相关页面  
[[concepts/subword_tokenization]]  
[[concepts/character_ngram]]  
[[models/fasttext]]  
[[concepts/tokenization]]  
[[concepts/error_detection_in_llms]]（OOV是常见错误源，如`[UNK]`触发幻觉）  
[[tools/errdetect]]（内置OOV检测模块）

## 来源  
《百面大模型》第1章第1.3节全节（pp.29–33），聚焦OOV定义、子词/BPE/FastText三大解决方案的机制与例证