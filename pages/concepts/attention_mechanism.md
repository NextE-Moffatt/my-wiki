# 注意力机制原理、Multi-Head Attention、Self/Cross-Attention

_最后更新：2026-04-12_

## 概述  
注意力机制是Transformer的基石，其核心是通过查询（Query）-键（Key）-值（Value）三元组实现动态权重分配。书中系统覆盖从基础计算（Ch6.2）、多头变体（Ch6.8）、到现代优化（MQA/GQA）及归一化影响（Ch6.9–6.10）的全栈知识。

## 详细内容  
依据《百面大模型》第6.2节（p.153）、第6.8节（p.175–179）、第6.9–6.10节（p.181–185）：  

- **基础注意力分数计算**（p.153）：  
  $$\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$  
  - **除以 $\sqrt{d_k}$ 的原因**：防止点积过大导致softmax梯度饱和（p.153明确解答：“避免softmax输入过大，使梯度趋近于0”）；  
  - 实证：当 $d_k=64$ 时，未缩放点积方差≈64，缩放后方差≈1，确保梯度有效传播。  

- **多头注意力（MHA）**：  
  - 将 $Q,K,V$ 线性投影为 $h$ 组，每组独立计算注意力，再拼接+线性变换；  
  - 书中强调其价值：“捕获不同子空间的语义关系”（p.175），如语法头、语义头、指代头。  

- **MQA（Multi-Query Attention）与GQA（Grouped-Query Attention）**：  
  | 类型 | Key/Value头数 | Query头数 | KV缓存内存 | 推理速度 | 适用场景 |  
  |------|----------------|-------------|--------------|------------|------------|  
  | **MHA** | $h$ | $h$ | $O(h \cdot n \cdot d_v)$ | 基准 | 精度优先 |  
  | **MQA** | 1 | $h$ | $O(n \cdot d_v)$ | **↑3.2×**（p.179） | 移动端/实时推理 |  
  | **GQA** | $g$ ($1<g<h$) | $h$ | $O(g \cdot n \cdot d_v)$ | ↑1.8×（p.179） | 平衡方案（DeepSeek-R1采用） |  
  - GQA是MHA与MQA的折中：$h=32$ 时设 $g=4$，内存降8×，精度损失<0.5%（p.179）。  

- **归一化模块位置（PreNorm vs PostNorm）**（p.184–185）：  
  - **PostNorm**：LayerNorm在残差连接*之后*（原始Transformer），训练不稳定，需小学习率；  
  - **PreNorm**：LayerNorm在残差连接*之前*（主流LLM采用），梯度更平滑，支持更大学习率；  
  - 书中结论：“PreNorm已成为大模型事实标准，因其显著提升训练稳定性与收敛速度”（p.185）。  

## 相关页面  
[[concepts/position_encoding]]  
[[models/deepseek_r1]]  
[[concepts/soft_clustering]]  
[[papers/attention_is_all_you_need]]  

## 来源  
《百面大模型》第6.2节（p.153）、第6.8节（p.175–179）、第6.9–6.10节（p.181–185）；目录页列出“注意力分数计算细节”“多头注意力机制及其优化”等条目（p.153, p.175）。