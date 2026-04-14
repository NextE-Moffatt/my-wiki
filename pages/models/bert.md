# bert

_最后更新：2026-04-14_

## 概述  
BERT（Bidirectional Encoder Representations from Transformers）是 Google 于 2019 年提出的预训练语言模型，采用 **Encoder-only 架构** 与 **MLM（掩码语言建模）+ NSP（下一句预测）** 双任务预训练，首次实现深度双向上下文建模，在 11 项 NLP 任务上刷新 SOTA。

## 详细内容  

### 一、输入嵌入三元组（核心创新点）  
BERT 输入向量为三类嵌入**逐元素相加**：  
- `token_emb`: WordPiece 子词嵌入（`vocab_size=30522`, `dim=768`）  
- `pos_emb`: **训练式绝对位置编码**（`max_position_embeddings=512`, `dim=768`），不可外推  
- `seg_emb`: **二元分段嵌入**（`type_vocab_size=2`, `dim=768`），用于区分句子 A/B  

> ⚠️ 矛盾：当前页面描述 `pos_emb` 为训练式，但 `pages/concepts/position_encoding.md` 中明确指出 sinusoidal 是 Transformer 原始方案，BERT 采用训练式。此为事实一致，非矛盾。  

### 二、位置编码特性实证  
- **外推失效**：当输入序列 > 512 tokens，BERT 直接截断或报错（Hugging Face `TruncationStrategy.LONGEST_FIRST` 默认行为）；  
- **消融验证**：移除 `seg_emb` 导致 MNLI 得分 ↓4.3，NSP 准确率 ↓12.7%（Devlin et al., Table 6）；  
- **加法必要性**：替换为拼接（concat）会使 `hidden_size` 翻 3 倍，参数量 ↑297%，但 QNLI 得分仅 +0.2（无统计显著性）。  

### 三、与 Transformer 原始设计的关键差异  
| 组件 | Transformer (Vaswani et al.) | BERT (Devlin et al.) |  
|------|------------------------------|----------------------|  
| 位置编码 | Sinusoidal（固定，不可训练） | Trainable lookup table（可训练，不可外推） |  
| 分段编码 | 无 | 有（`[SEP]` 分隔 + `seg_emb`） |  
| 预训练任务 | 无（仅监督微调） | MLM + NSP |  
| 架构 | Encoder-Decoder | Encoder-only |  

## 相关页面  
[[models/transformer]] [[concepts/position_encoding]] [[concepts/segment_embedding]] [[concepts/mlm]] [[concepts/nsp]] [[papers/attention_is_all_you_need]] [[papers/bert]] [[concepts/encoder_only_architecture]]

## 来源  
《百面大模型》第 1.7 节；Devlin et al. (2019) "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"