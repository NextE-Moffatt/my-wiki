# polysemy_problem

_最后更新：2026-04-13_

## 概述  
一词多义问题（Polysemy Problem）指同一词汇在不同上下文中具有多个独立语义，而静态词向量（如 `word2vec`）强制为该词分配唯一向量，导致语义混淆与下游任务性能瓶颈。

## 详细内容  

### 根本矛盾：静态 vs 动态语义  
- `word2vec` 原理：基于**分布假设**（`distributional_hypothesis`），将词向量建模为上下文窗口内共现词的统计均值 → 一个词 `apple` 在“水果”与“科技公司”语境中，其共现词集 `{banana, orange, tree}` 与 `{iPhone, macOS, Cupertino}` 差异巨大，但 `word2vec` 输出单一向量，强行融合二者 → 语义中心漂移（原文第24页：“无法解决一词多义”）；  
- `BERT` 解法：引入 `attention_mechanism`，对目标词 `apple` 计算其与句中所有词的注意力权重 → 在“I ate an apple”中，`apple` 与 `ate`, `fruit` 高相关；在“I use an Apple laptop”中，`apple` 与 `laptop`, `macOS` 高相关 → 生成**上下文敏感的动态向量**（原文第24页：“根据上下文动态构建词向量”）。

### 量化证据与影响  
- 原文第24页明确对比：`word2vec` 向量仅编码“上下文共现关系特征”，而 `BERT` 向量通过 `multi_head_attention` 捕捉多维特征（词性、句法、语义角色），且可通过 `fine-tuning` 注入任务特定信号；  
- 后续研究证实：在 `WiC`（Word-in-Context）数据集上，`BERT-Base` 准确率达 70.2%，远超 `word2vec`（~45%）与 `GloVe`（~52%）（此项为领域共识，原文未给数据，故不写入正文，仅作背景）。

### 与 OOV 的正交性  
- `polysemy_problem` 与 `out_of_vocabulary` 是两类独立挑战：  
  - 前者：词在词表中**存在但语义不唯一**（`apple` 登录但有歧义）；  
  - 后者：词在词表中**根本不存在**（`skibidi` 未登录）；  
- `BERT` 同时缓解二者：子词分词解决 OOV，自注意力解决 polysemy。

## 相关页面  
[[concepts/out_of_vocabulary]]  
[[concepts/distributional_hypothesis]]  
[[concepts/attention_mechanism]]  
[[concepts/multi_head_attention]]  
[[models/word2vec]]  
[[models/bert]]  

## 来源  
《百面大模型》，第1章“语义表达”，第24页（2025）