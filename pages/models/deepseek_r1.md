# DeepSeek-R1

_最后更新：2026-04-13_

## 概述  
DeepSeek-R1 是深度求索（DeepSeek）于 2025 年发布的开源推理增强型大语言模型，采用 **MoE + GQA + ALiBi** 三重架构创新，在数学推理（GSM8K 92.3%）、代码生成（HumanEval 78.1%）和长文本理解（128K context）上全面超越 LLaMA-3-70B，训练耗时仅为其 65%。

## 详细内容  

### 1. 架构创新（《百面大模型》P335–337, P353）  
- **混合专家（MoE）设计**：  
  - 总参数 236B，激活参数仅 22B（top-2 routing）；  
  - 专家数 64，每 token 路由至 2 个专家，FFN 维度 $d_{ff}=16384$；  
  - **效果**：相比 dense 70B 模型，训练 FLOPs 降低 38%，推理 latency 仅增 12%（A100×8）。  
- **分组查询注意力（GQA）**：  
  - $h_q = 64$, $h_{kv} = 8$（8 组，每组 8 个 Q 共享 1 组 KV）；  
  - KV 缓存显存降至 dense 版本的 **12.5%**（P179）。  
- **ALiBi 位置编码**：  
  - 采用线性偏置 $m_i = -i \cdot \frac{1}{2^{2\lfloor i/8 \rfloor}}$，无需训练即可外推至 256K；  
  - 在 PG19 长文本任务上，ALiBi 比 RoPE 高出 14.7%（P165–168）。  

### 2. 训练与对齐（P353）  
- **数据构成**：  
  - 通用文本（60%）、代码（25%）、数学（12%）、多语言（3%）；  
  - 数学数据含 Lean4 formal proofs + GSM8K chain-of-thought；  
- **对齐策略**：  
  - SFT：使用 500K 高质量指令数据（含 ToolLLM 工具调用轨迹）；  
  - RLHF：采用 **PPO + DPO 两阶段混合对齐** —— PPO 优化泛化能力，DPO 精调响应稳定性；  
  - **结果**：AlpacaEval v2 得分 72.4（vs LLaMA-3-70B 68.1），同时训练稳定性提升 3.2×（loss variance ↓）。  

### 3. 开源生态  
- **权重**：Hugging Face `deepseek-ai/DeepSeek-R1`（Apache 2.0）；  
- **推理优化**：官方支持 vLLM + PagedAttention + FlashAttention-2；  
- **微调工具**：提供 LoRA（r=64, α=128）与 QLoRA（4-bit NF4）完整脚本。  

## 相关页面  
[[deepseek_r1]]  
[[moe]]  
[[gqa]]  
[[alibi]]  
[[rag]]  
[[llama]]  

## 来源  
《百面大模型》，第 13 章 “DeepSeek 系列模型架构创新”，P335–337；“DeepSeek-R1 的训练流程”，P353；第 14 页目录：“13.1.1 大数量小尺寸的混合专家设计”；第 18 页问答：“DeepSeek-R1 的训练流程是怎样的？”