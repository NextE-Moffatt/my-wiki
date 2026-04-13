# nlp_four_stages

_最后更新：2026-04-13_

## 概述  
NLP四阶段演进模型将自然语言处理技术发展划分为四个标志性阶段：**词袋模型（特征工程）→ word2vec（浅层表征）→ BERT（深层表征）→ ChatGPT（大模型表征）**；每一阶段均由核心建模范式与表征粒度突破驱动，反映AI从人工特征到端到端语义学习的范式跃迁。

## 详细内容  

### 各阶段技术特征对比  
| 阶段 | 代表模型/方法 | 核心范式 | 表征粒度 | 关键能力 | 局限性 |  
|------|----------------|------------|------------|------------|------------|  
| **第一阶段：特征工程** | 词袋模型（Bag-of-Words） | 手工设计离散特征（TF-IDF、n-gram） | 词级（word-level） | 快速、可解释 | 完全丢失词序与语义，维度灾难 |  
| **第二阶段：浅层表征** | word2vec、GloVe | 无监督浅层神经网络学习静态稠密向量 | 词级（word-level） | 捕获语义相似性（king - man + woman ≈ queen） | 静态表征（polysemy problem）、无上下文 |  
| **第三阶段：深层表征** | BERT、RoBERTa | 深度Transformer预训练+微调 | 子词级（WordPiece/BPE） | 上下文敏感表征（contextual embedding）、NLU SOTA | 生成能力弱、需任务微调 |  
| **第四阶段：大模型表征** | GPT-3、ChatGPT、Llama | 超大规模decoder-only预训练+in-context learning | 子词级（BPE/Unigram） | 零样本/少样本泛化、多任务统一、世界知识内化 | 数据饥渴、推理成本高、可控性差 |  

### 阶段跃迁驱动力  
- **第一→第二阶段**：从**稀疏离散特征**到**稠密连续向量**，解决语义相似性建模；由分布假说（distributional hypothesis）驱动。  
- **第二→第三阶段**：从**静态词向量**到**动态上下文向量**，解决一词多义（polysemy）；由Transformer架构与MLM目标实现。  
- **第三→第四阶段**：从**任务微调范式**到**提示即编程（prompt-as-programming）**，由模型规模突破涌现in-context learning能力（GPT-3论文证实：当参数>10B时，few-shot性能随规模幂律增长）。

## 相关页面  
[[models/word2vec]] [[models/bert]] [[models/gpt]] [[concepts/distributional_hypothesis]] [[concepts/polysemy_problem]] [[concepts/in_context_learning]] [[concepts/zero_shot_learning]]

## 来源  
《百面大模型》，第46页（四阶段定义）、第47页（GPT-3 zero-shot验证）