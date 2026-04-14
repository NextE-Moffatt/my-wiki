# Encoder-Decoder 架构

_最后更新：2026-04-14_

## 概述  
Encoder-decoder 架构由独立的编码器与解码器子网络组成，编码器采用双向注意力处理输入，解码器采用单向注意力生成输出，是序列到序列（seq2seq）任务的经典范式，兼顾理解与生成能力。

## 详细内容  
据《百面大模型》第 1.8 节，该架构的技术构成与典型应用如下：

- **结构分工**：  
  - **编码器**：接收完整输入序列（如英文句子），通过双向 self-attention 建模上下文，输出 contextualized representations；  
  - **解码器**：以编码器输出为 key/value，自身采用 causal self-attention + cross-attention（to encoder output），逐步生成目标序列（如中文翻译）；  
- **训练目标**：最大化解码器条件概率 $P(y_1,\dots,y_m \mid x_1,\dots,x_n)$，典型实现为 teacher-forcing；  
- **代表模型**：  
  - **T5**（Text-to-Text Transfer Transformer）：将所有 NLP 任务统一为 text-to-text 格式，编码器-解码器全参数化；  
  - **GLM**（General Language Model）：国产大模型，采用类似 T5 的 encoder-decoder 设计，支持多任务联合训练；  
- **能力定位**：  
  - 优于 encoder-only 的生成质量（如机器翻译 BLEU）；  
  - 优于 decoder-only 的输入理解深度（如需对长文档摘要时，编码器可全局建模）；  
  - 但参数量与推理延迟高于 decoder-only，故在纯生成场景（如聊天）中逐渐被后者替代；  

书中强调其“对于综合理解和生成都表现出较好的能力”，并配图 1-10 明确将其列为三大架构之一，与 encoder-only、decoder-only 并列。

该页面与 `models/t5`、`models/glm` 尚未存在，但按 schema 应属 `models/` 分类；此处先建立架构抽象页，待后续摄入 T5/GLM 专项资料时再补全具体模型页。

## 相关页面  
[[models/t5]]  
[[models/glm]]  
[[concepts/encoder_decoder_architecture]]  
[[concepts/seq2seq]]  
[[concepts/causal_lm]]  
[[concepts/mlm]]  
[[models/encoder_only_architecture]]  
[[models/decoder_only_architecture]]

## 来源  
《百面大模型》，第 1.8 节 “大模型语义建模的典型架构”，2025 年出版；含架构定义、双向/单向注意力分工、T5 与 GLM 实例、能力对比论述。