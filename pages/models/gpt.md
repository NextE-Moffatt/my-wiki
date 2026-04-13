# GPT（Generative Pre-trained Transformer）

_最后更新：2026-04-13_

## 概述  
OpenAI提出的单向Transformer解码器架构系列模型，以因果语言建模（Causal LM）为预训练目标，是推动NLP进入第四阶段（大模型表征阶段）的核心技术路线，代表模型包括GPT-3、ChatGPT、GPT-4。

## 详细内容  
- **技术路线坚守与验证**（《百面大模型》p.5核心论断）：  
  - 在GPT-1/2时代，业界普遍质疑单向建模能力（“为何BERT效果更好？”），但OpenAI坚持扩大模型规模与数据量，最终在GPT-3（175B）实现零样本/少样本泛化飞跃，并通过ChatGPT（GPT-3.5微调+RLHF）完成产品化落地。  
  - **关键转折点**：ChatGPT发布并非因GPT-4已就绪，而是OpenAI“战略试水”——用效果稍逊但更可控的模型验证生成式路线的市场接受度，此举激发全球对GPT路线的狂热跟进（p.5）。  

- **Causal LM目标函数**：  
  $$\mathcal{L}_{\text{CLM}} = -\sum_{t=1}^T \log P(x_t \mid x_{<t})$$  
  与BERT的MLM相比，CLM天然支持**自回归生成**，且在长文本连贯性、指令遵循、思维链（Chain-of-Thought）涌现方面具有不可替代性。  

- **能力涌现现象**：  
  书中指出GPT-3在175B参数量级首次观察到显著的“推理能力涌现”（如数学推导、代码生成），而该现象在BERT系列中未被观测到，印证 `[[scaling_computation]]` 中“能力随规模非线性增长”的核心假设。  

- **与BERT的本质差异**：  
  | 维度         | BERT                          | GPT                           |  
  |--------------|-------------------------------|-------------------------------|  
  | **架构**     | Encoder-only                    | Decoder-only (causal mask)    |  
  | **预训练目标** | Masked LM (双向)                | Causal LM (单向)              |  
  | **下游应用** | 分类/抽取等判别任务为主         | 生成/对话/推理等生成任务为主   |  
  | **范式定位** | 第三阶段巅峰（深层表征）         | 第四阶段基石（大模型表征）      |  

## 相关页面  
[[models/bert]] [[nlp_four_stages]] [[causal_lm]] [[mlm]] [[scaling_computation]] [[books/baimian_damoxx]] [[models/deepseek_r1]]

## 来源  
《百面大模型》，p.5；Radford et al. (2018, 2019) GPT-1/2论文；OpenAI GPT-3 Technical Report (2020)