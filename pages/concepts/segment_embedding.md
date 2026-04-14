# 分段嵌入

_最后更新：2026-04-14_

## 概述  
分段嵌入（Segment Embedding）是 BERT 等双句任务模型中用于区分输入中不同句子段落（如 `sentence A` 与 `sentence B`）的可学习向量，与词元嵌入、位置嵌入相加构成最终输入表征，解决跨句建模中的段落边界感知问题。

## 详细内容  

### 一、设计动机与任务需求  
- BERT 预训练包含 **NSP（Next Sentence Prediction）** 任务，需判断两个句子是否连续；下游任务如 **问答（SQuAD）、自然语言推理（MNLI）** 均需建模跨句语义关系。  
- 若仅靠位置编码或词序无法区分段落归属（例如 `"[CLS] I love NLP . [SEP] What is NLP ? [SEP]"` 中，`I` 和 `What` 位置相邻但属不同段），必须引入显式段落标识。  

### 二、实现细节  
- **符号约定**：  
  - `A` 段：所有 token 映射到 segment ID = 0 → `seg_emb[0] ∈ ℝ^d`  
  - `B` 段：所有 token 映射到 segment ID = 1 → `seg_emb[1] ∈ ℝ^d`  
  - `[CLS]` 和 `[SEP]` 符号按其所在段落分配 segment ID（通常 `[CLS]` 属 A 段，首个 `[SEP]` 属 A 段末，第二个 `[SEP]` 属 B 段末）。  
- **维度约束**：`seg_emb` 矩阵大小为 `2 × d`（BERT-base），与 `token_emb` 和 `pos_emb` 同维，支持直接相加。  
- **可学习性**：`seg_emb[0]`, `seg_emb[1]` 作为模型参数，在预训练中通过 NSP 和 MLM 任务联合优化。  

### 三、与位置/词元嵌入的协同机制  
- **加法即交叉**：`input = token_emb + pos_emb + seg_emb` 并非简单叠加，而是迫使模型在统一向量空间中学习：  
  - 如何将“位置 5 的词 `love`（A 段）”与“位置 5 的词 `What`（B 段）”在语义上区分开；  
  - 如何利用段落信息调节注意力权重（例如 A 段内 token 更关注 A 段，跨段关注受控于 segment-aware bias）。  
- **对比实验支撑**：消融实验显示，移除 segment embedding 后，NSP 准确率下降 >12%，MNLI-m 得分下降 4.3（Devlin et al., 2019）。  

### 四、局限性与演进  
- **二元性瓶颈**：仅支持最多 2 段（`ID=0/1`），无法处理多文档输入（如长上下文 RAG）。  
- **替代方案**：  
  - RoBERTa 移除 NSP 任务，亦移除 segment embedding，证明其非绝对必要（但牺牲跨句任务微调便利性）；  
  - Longformer、BigBird 引入全局 token + segment-aware attention bias；  
  - LLaMA 系列完全弃用 segment embedding，依赖位置编码与指令微调隐式建模段落。  

## 相关页面  
[[models/bert]] [[concepts/position_encoding]] [[concepts/tokenization]] [[concepts/attention_mechanism]] [[papers/attention_is_all_you_need]] [[concepts/segment_embedding_in_nsp]]

## 来源  
《百面大模型》第 1.7 节；Devlin et al. (2019) "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"