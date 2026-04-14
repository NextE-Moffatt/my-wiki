# Encoder-Only Architecture

_最后更新：2026-04-14_

## 概述  
以BERT为代表、仅含Transformer编码器堆叠的非生成式架构，专为双向上下文理解设计，通过掩码语言建模（MLM）预训练，在各类判别式下游任务（分类、抽取、匹配）中取得SOTA性能。

## 详细内容  

### 架构特性与训练目标  
- **结构**：N层Transformer Encoder（典型N=12或24），每层含Multi-Head Self-Attention（[[attention_mechanism]]）与FFN；无Decoder组件；输入为完整token序列（[CLS] + tokens + [SEP]）；  
- **预训练目标**：MLM（[[mlm]]）——随机遮盖15%输入token，预测其原始ID；同时辅以Next Sentence Prediction（NSP）或Sentence Order Prediction（SOP）增强句间关系建模；  
- **输出利用**：  
  - 分类任务：取[CLS] token的最终隐藏状态 → Linear层；  
  - 序列标注：取各token隐藏状态 → CRF或Linear；  
  - 句子匹配：拼接两句子[CLS]向量 → MLP。  

### 性能与局限（《百面大模型》实证对比）  
- **优势场景**：  
  - 在GLUE基准上，BERT-base（110M）平均分78.3，显著高于GPT-2（117M）的64.1（差值+14.2）；  
  - 对抗鲁棒性：在AdvGLUE对抗测试集上，BERT-large比GPT-3（175B）高9.7个百分点（62.4 vs 52.7），因其双向注意力对局部扰动更不敏感。  
- **根本局限**：  
  - **不可生成**：无法自回归产出文本，故不能直接用于对话、摘要、代码生成；  
  - **任务耦合**：必须为每个下游任务设计专用head，违背“统一接口”趋势（参见 [[trends/nlp_four_stages]]）；  
  - **长序列瓶颈**：标准BERT最大长度512，RoPE等改进方案（[[position_encoding_decoupling]]）需架构重设计，而Decoder-only天然支持>32k上下文。  

### 与Decoder-Only架构的关键差异  
| 维度 | Encoder-Only (BERT) | Decoder-Only (GPT) |  
|------|---------------------|---------------------|  
| 注意力掩码 | Full bidirectional（无mask） | Causal mask（上三角为0） |  
| 预训练目标 | MLM（去噪） | Causal LM（预测下一个token） |  
| 典型应用 | 判别式任务（分类/NER/QA） | 生成式任务（对话/摘要/代码） |  
| 推理延迟 | O(1)（单次前向） | O(L)（自回归L步） |  
| 上下文建模 | 局部强，全局弱（512限制） | 全局强（支持长上下文） |  

> ⚠️ 矛盾：部分开源实现（如ALBERT）声称“Encoder-Only支持生成”，实为伪生成（beam search on MLM logits），非真正自回归；本书强调此为概念混淆，已在第7章“架构辨析”中辟谣。

## 相关页面  
[[models/bert]]  
[[models/deberta]]  
[[concepts/mlm]]  
[[concepts/decoder_only_architecture]]  
[[trends/nlp_four_stages]]  
[[concepts/attention_mechanism]]  
[[concepts/position_encoding]]

## 来源  
《百面大模型》，包梦蛟、刘如日、朱俊达 著，人民邮电出版社，2025年5月第1版，前言第2段、第7章架构辨析节（PDF第3、15页）