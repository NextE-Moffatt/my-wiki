# Encoder-Only 架构

_最后更新：2026-04-14_

## 概述  
Encoder-only 架构是仅含 Transformer 编码器堆叠的模型结构，采用双向注意力（bidirectional attention）与掩码语言建模（MLM）目标进行训练，专长于自然语言理解（NLU）任务，但在生成能力上存在结构性局限。

## 详细内容  
根据《百面大模型》第 1.8 节，encoder-only 架构具有以下定义性特征与实证约束：

- **注意力机制**：所有 token 在 self-attention 中可同时看到上下文（即 $i$ 位置可 attend to $j$ 无论 $i<j$ 或 $i>j$），实现真正的双向语义建模；  
- **训练目标**：以 MLM 为主（如 BERT），随机掩码 15% token 并预测其原始 ID，迫使模型学习深层上下文依赖；  
- **生成能力缺陷根源**：  
  - 结构上无解码器模块，无法原生支持自回归生成；  
  - 即便通过前缀语言模型（prefix-LM）变体（如 BERT-gen）引入生成头，其输出仍受限于非因果注意力——无法保证生成 token 的严格左→右依赖；  
  - 实践中，BERT 类模型在文本续写、对话生成等任务上 BLEU/Rouge 显著低于 decoder-only 模型（如 GPT-2 在 WikiText-103 上 PPL 为 19.2 vs BERT-large 为 32.7）；  
- **NLU 优势证据**：在 GLUE 基准上，BERT-base 达 80.5（avg），显著高于同期 decoder-only 模型（如 GPT-1 为 72.8）；其成功源于双向上下文对判别任务（如 entailment, sentiment）的强支撑。

书中特别强调：“BERT 在生成方面暴露了天然的弱点……在大模型时代逐渐被大家所淡忘”，但“在具体场景的判别任务上，仍然展现出了卓越的性能”，印证其**领域适配性价值**——非技术落后，而是任务失配。

该架构与 `models/bert` 页面构成实例-抽象关系；其与 decoder-only 的对比数据应同步更新至 `models/gpt` 和 `models/llama` 页面。

## 相关页面  
[[models/bert]]  
[[models/gpt]]  
[[models/llama]]  
[[concepts/encoder_only_architecture]]  
[[concepts/mlm]]  
[[concepts/causal_lm]]  
[[concepts/attention_mechanism]]  
[[concepts/bidirectional_attention]]  
[[concepts/prefix_language_model]]

## 来源  
《百面大模型》，第 1.8 节 “大模型语义建模的典型架构”，2025 年出版；含架构定义、能力对比、任务适配性分析及“前缀语言模型”术语引用。