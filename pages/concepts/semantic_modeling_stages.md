# 语义建模四阶段演进

_最后更新：2026-04-14_

## 概述  
语义建模的演进可划分为四个典型阶段：特征工程 → 浅层表征 → 深层表征 → 大模型表征，分别以词袋模型、word2vec、BERT、ChatGPT 为标志性范式，体现从人工规则到数据驱动、从静态到动态、从任务专用到通用能力的跃迁。

## 详细内容  
《百面大模型》第 1.8 节明确提出语义建模的四阶段划分，各阶段核心特征如下：

| 阶段 | 代表模型/方法 | 输入表示 | 语义性质 | 训练目标 | 典型能力边界 |
|------|----------------|------------|-------------|--------------|----------------|
| **第一阶段：特征工程** | 词袋模型（Bag-of-Words） | one-hot 向量 + TF-IDF 加权 | 离散、稀疏、无序 | 分类/聚类监督信号 | 无法建模词序与上下文，OOV 严重 |
| **第二阶段：浅层表征** | word2vec（Skip-gram/CBOW） | dense vector（300d） | 分布式、静态、上下文无关 | 预测邻域词（local context） | 一词多义（polysemy）问题突出，无法区分 sense |
| **第三阶段：深层表征** | BERT（Transformer encoder-only） | contextualized token embedding | 动态、上下文敏感、双向 | 掩码语言建模（MLM）+ 下游微调 | 强 NLU，弱 NLG；需 task-specific fine-tuning |
| **第四阶段：大模型表征** | ChatGPT / Llama（decoder-only LM） | autoregressive hidden state | 指令对齐、涌现能力、in-context learning | 自回归语言建模（causal LM）+ RLHF | 零样本/少样本泛化、跨任务迁移、隐含语义内化 |

关键演进动因：  
- **参数量与数据量双“大”驱动**：GPT-3（175B）证明 scale 是解锁 zero-shot 能力的关键；  
- **范式转移**：从 BERT 的“预训练+微调”二阶段，转向 GPT-3 的“预训练+in-context learning”单阶段；  
- **语义内化方式变革**：隐含语义不再依赖显式微调头，而是直接编码于模型参数 $\theta_{\text{origin}}$ 中，通过前向传播即可激活（如 $P(y \mid x; \theta_{\text{origin}})$）。

该四阶段模型与现有 `trends/nlp_four_stages` 页面形成互补：本页聚焦**语义建模机制本身的技术演进**，而 `nlp_four_stages` 更侧重历史脉络与技术代际命名；二者应互链。

## 相关页面  
[[trends/nlp_four_stages]]  
[[models/word2vec]]  
[[models/bert]]  
[[models/gpt]]  
[[concepts/distributional_hypothesis]]  
[[concepts/contextual_embedding]]  
[[concepts/causal_lm]]  
[[concepts/mlm]]  
[[concepts/in_context_learning]]  
[[concepts/zero_shot_learning]]  
[[concepts/few_shot_learning]]

## 来源  
《百面大模型》，第 1.8 节 “大模型语义建模的典型架构”，2025 年出版；明确列出四阶段名称、代表模型、形式化目标及能力对比。