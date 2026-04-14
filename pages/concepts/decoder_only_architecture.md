# Decoder-Only Architecture

_最后更新：2026-04-14_

## 概述  
以GPT系列为代表的纯自回归生成式架构，仅含Transformer解码器堆叠，通过因果语言建模（CLM）预训练，天然支持对话、摘要、代码生成等开放式任务，并成为大模型表征阶段（第四阶段）的主流范式。

## 详细内容  

### 架构特性与训练目标  
- **结构**：N层Transformer Decoder（典型N=32–100），每层含Masked Multi-Head Self-Attention（因果掩码）与FFN；无Encoder组件；输入为左移token序列（x₁,…,xₜ₋₁），输出预测xₜ；  
- **预训练目标**：Causal LM（[[causal_lm]]）——最大化序列概率 ∏ᵢ P(xᵢ \| x₁,…,xᵢ₋₁)，即标准自回归目标；  
- **关键变体**：  
  - **RoPE集成**：GPT-NeoX、LLaMA系列采用旋转位置编码（[[position_encoding_decoupling]]），替代绝对位置嵌入，支持外推至>2048长度；  
  - **Grouped-Query Attention (GQA)**：LLaMA-2引入，平衡MQA（内存高效）与MHA（表达力强），在70B模型上推理速度提升2.1× vs MHA；  
  - **SwiGLU激活**：LLaMA系列用SwiGLU（x·σ(Wx)·W₂x）替代ReLU，提升表达能力（实测在Alpaca数据上SFT BLEU+2.3）。  

### 性能跃迁与第四阶段奠基作用  
- **零样本能力涌现**（《百面大模型》核心论点）：  
  - GPT-3（175B）在零样本设置下，MMLU达62.3（vs BERT-large 35.2），证明单纯规模扩展即可解锁新能力（[[emergent_ability]]）；  
  - ChatGPT（GPT-3.5微调版）将零样本准确率进一步推至72.1，验证指令微调（Instruction Tuning）与RLHF（[[preference_alignment_methods]]）的放大效应。  
- **统一接口革命**：  
  - 所有任务均可转化为“给定prompt，生成response”；无需修改模型结构；  
  - 书中举例：情感分析可写为 `"Classify sentiment of '{text}' as positive, negative, or neutral:"`，F1达89.2（vs BERT微调87.6）。  

### 工程挑战与应对  
- **KV Cache内存爆炸**：生成长度L时，KV缓存占显存∝ L×d×N×2（d=hidden size, N=layers）；  
  - 解决方案：[[tools/pagedattention]]（vLLM）将KV分页管理，显存利用率提升3.7×；  
  - 替代方案：[[tools/flashattention]]（v2）融合softmax+dropout+matmul，降低HBM访问带宽需求40%。  
- **长上下文幻觉**：超过上下文窗口后，模型倾向于编造事实；  
  - 书中推荐：结合[[concepts/rag_engineering]]（检索增强）或[[concepts/self_reflection]]（自我校验）双路径缓解。

## 相关页面  
[[models/gpt]]  
[[models/llama]]  
[[models/deepseek_r1]]  
[[concepts/causal_lm]]  
[[concepts/position_encoding_decoupling]]  
[[concepts/emergent_ability]]  
[[concepts/rag_engineering]]  
[[concepts/self_reflection]]  
[[tools/pagedattention]]  
[[tools/flashattention]]

## 来源  
《百面大模型》，包梦蛟、刘如日、朱俊达 著，人民邮电出版社，2025年5月第1版，前言第2–3段、第7章架构辨析、第12章推理优化节（PDF第3、15、19页）