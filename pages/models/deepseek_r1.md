# DeepSeek-R1

_最后更新：2026-04-14_

## 概述  
DeepSeek-R1 是 DeepSeek 推出的开源 MoE 架构大语言模型（2024），核心创新包括：大数量小尺寸混合专家（64 专家中每 token 激活 2 个）、多头潜在注意力（MLA）、多词元预测（Multi-token Prediction），在同等 FLOPs 下显著提升推理吞吐与长程建模能力。

## 详细内容  
### 架构概览  
- **总参数量**：约 67B（含 MoE），**激活参数量**：~2.4B（2/64 专家 × 单专家 7.6B）  
- **MoE 设计**（13.1.1）：64 个 FFN 专家，Top-2 路由，专家容量限制为 1.2×batch_size；采用 GShard 负载均衡损失（$ \mathcal{L}_{\text{load}} = \lambda \sum_k (\sum_i z_{ik} - \frac{1}{K}\sum_{i,j} z_{ij})^2 $）抑制专家坍缩  
- **MLA（Multi-head Latent Attention）**（13.1.2）：替代标准 MHA，将 Q/K/V 投影后先经低秩压缩（rank=64）再计算注意力，降低 KV 缓存显存占用 40%；公式为：  
  $$
  \text{MLA}(Q,K,V) = \text{Softmax}\left(\frac{Q W_q^{\text{low}} (K W_k^{\text{low}})^\top}{\sqrt{d_k}}\right) (V W_v^{\text{low}})
  $$  
  其中 $W_q^{\text{low}} \in \mathbb{R}^{d \times 64}$，大幅减少 KV 缓存带宽压力  
- **多词元预测（Multi-token Prediction）**（13.1.3）：训练时对每个位置预测未来 $k=4$ 个 token（而非仅 1 个），目标函数为联合概率最大化：  
  $$
  \mathcal{L}_{\text{MTP}} = -\log \prod_{t=1}^T p(x_{t+1:t+k} \mid x_{\leq t})
  $$  
  实测在相同训练步数下，使模型在长文本生成任务（如 PG-19）的困惑度下降 12.3%，且推理时解码延迟仅增加 8%（因减少自回归步数）

### 训练流程（13.2）  
- 数据：5.4T tokens，含 40% 代码、30% 多语言网页、20% 科技文献、10% 对话  
- 预填充阶段使用 FlashAttention-2 加速；KV 缓存采用 PagedAttention 管理  
- 持续预训练（CPT）阶段引入动态温度采样（temperature ∈ [0.7, 1.3]）缓解模式坍缩  

## 相关页面  
[[models/deepseek_r1]] [[concepts/moe]] [[concepts/mla]] [[concepts/multi_token_prediction]] [[tools/flashattention]] [[tools/pagedattention]] [[concepts/causal_lm]]

## 来源  
《百面大模型》，第 13 章 DeepSeek，pp. 335–353