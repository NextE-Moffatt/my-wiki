# Position Encoding

_最后更新：2026-04-13_

## 概述  
位置编码（Position Encoding）是Transformer架构中**显式注入序列顺序信息**的关键机制，用于弥补自注意力机制的位置无关性缺陷。经典方案分为绝对编码（如sinusoidal、可训练）与相对编码（如RoPE、ALiBi），直接影响模型外推能力、长程建模与训练稳定性。

## 详细内容  

### 绝对位置编码  
#### 1. Sinusoidal（Vaswani et al., 2017）  
- 公式：对位置 $ pos \in [0, L) $、维度 $ i \in [0, d_{\text{model}}/2) $，  
  $$
  PE_{(pos,2i)} = \sin\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right), \quad 
  PE_{(pos,2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)
  $$  
- **两大设计原理**：  
  (a) **线性可组合性**：任意相对偏移 $ k $，$ PE_{pos+k} $ 可表示为 $ PE_{pos} $ 与 $ PE_k $ 的线性变换，便于模型学习相对位置；  
  (b) **值域有界性**：所有分量 $ \in [-1, 1] $，保障梯度稳定，避免长序列训练发散。  

#### 2. Trainable Absolute（BERT）  
- 参数形式：$ P \in \mathbb{R}^{L_{\max} \times d_{\text{model}}} $，随模型端到端更新；  
- **致命缺陷**：无法外推（$ L > L_{\max} $ 时无定义），限制上下文长度；  
- 实践中 $ L_{\max}=512 $，$ d_{\text{model}}=768 $。

### 相对位置编码  
- **核心思想**：修改注意力分数计算，显式融入位置差 $ i-j $；  
- 基础公式（Shaw et al., 2018）：  
  $$
  \text{score}_{i,j} = (q_i)^T k_j + (q_i)^T R_{i-j} + u^T k_j + v^T R_{i-j}
  $$  
  其中 $ R_{i-j} \in \mathbb{R}^{d_k} $ 为相对位置嵌入，$ u,v $ 为可学习偏置；  
- **现代演进**：XLNet（2D相对位置）、T5（可训练相对偏置）、DeBERTa（解耦内容/位置）、RoPE（旋转位置编码，保留绝对位置可逆性）、ALiBi（线性偏置，无限外推）。

### 位置编码失效的后果  
- 关系分类任务中，若缺失位置信息，头/尾实体顺序混淆将导致关系标签错误（如“[出生于]”误判为“[出生地]”）；  
- 图1-7显示：需将特殊标记（如`[HEAD_START]`）的位置编码与实体起始位置共享，才能正确建模结构化语义。

## 相关页面  
[[models/bert]] [[models/gpt]] [[concepts/attention_mechanism]] [[concepts/rope]] [[concepts/alibi]] [[concepts/ood_generalization]] [[papers/attention_is_all_you_need]]

## 来源  
《百面大模型》第41–43页；Vaswani et al. (2017), *Attention Is All You Need*; Shaw et al. (2018), *Self-Attention with Relative Position Representations*.