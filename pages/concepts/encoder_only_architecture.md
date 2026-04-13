# encoder_only_architecture

_最后更新：2026-04-13_

## 概述  
纯编码器架构（Encoder-only Architecture）指仅包含Transformer编码器堆叠、无解码器模块的语言模型结构，典型代表为BERT；其核心能力聚焦于**自然语言理解（NLU）**，通过双向上下文建模实现语义深度表征，但**不具备原生自回归生成能力**。

## 详细内容  

### 设计原理与技术特征  
- **双向注意力机制**：每个词元可关注序列中所有其他词元（含前后），实现全上下文语义融合，支撑MLM预训练目标。  
- **输入结构**：强制依赖三重嵌入叠加（词元+位置+分段），但最新研究表明该设计存在语义耦合缺陷（见[[papers/rethinking_positional_encoding]]）。  
- **输出形式**：仅输出各位置的隐藏状态向量（hidden states），不直接建模token-to-token条件概率；生成任务需额外引入前缀语言模型（prefix-LM）范式（如将待生成内容作为“前缀”输入，用[MASK]占位后预测）。  

### 能力边界与工程权衡  
| 维度 | 表现 | 说明 |
|------|------|------|
| **NLU性能** | ★★★★★ | 在GLUE、SuperGLUE等基准上长期SOTA，尤其适合判别类任务（情感分析、NER、文本匹配） |
| **生成能力** | ★☆☆☆☆ | 无法直接执行续写、翻译、摘要等生成任务；需微调为Seq2Seq变体或结合外部解码器 |
| **推理效率** | ★★★★☆ | 无自回归循环，单次前向即可获取全部位置表征，适合高吞吐批处理 |
| **参数效率** | ★★★★☆ | 相比encoder-decoder（如T5）或decoder-only（如Llama），同等规模下更轻量 |

### 历史演进与现状  
- **兴起**：2018年BERT发布后成为NLU事实标准，推动“预训练+微调”范式普及。  
- **衰落**：2023年后大模型时代转向生成优先，纯编码器因无法支持in-context learning与zero-shot推理而逐渐淡出主流开源大模型选型。  
- **不可替代性**：在垂直领域判别任务（如金融事件抽取、医疗实体识别）中，经领域适配的BERT变体仍保持**精度-效率最优平衡**，远超通用大模型的few-shot表现。

## 相关页面  
[[models/bert]] [[models/roberta]] [[concepts/mlm]] [[concepts/natural_language_understanding]] [[concepts/prefix_language_model]] [[trends/nlp_four_stages]]

## 来源  
《百面大模型》，第47–48页（架构分类与能力分析）