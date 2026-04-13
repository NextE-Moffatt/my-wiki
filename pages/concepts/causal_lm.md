# 因果语言建模（Causal Language Modeling, CLM）

_最后更新：2026-04-13_

## 概述  
大语言模型预训练的核心目标函数之一，要求模型根据历史token预测下一个token，通过自回归方式建模文本生成过程，是GPT系列及所有Decoder-only架构的理论基础。

## 详细内容  
- **数学定义**：  
  给定序列 $x = (x_1, x_2, ..., x_T)$，CLM最大化联合概率：  
  $$P(x) = \prod_{t=1}^T P(x_t \mid x_{<t}) = \prod_{t=1}^T P(x_t \mid x_1, ..., x_{t-1})$$  
  在Transformer中，通过**下三角因果注意力掩码**（causal mask）强制每个位置 $t$ 只能关注 $1$ 到 $t-1$ 位置，确保无信息泄露。  

- **与MLM的本质区别**（《百面大模型》p.5隐含对比）：  
  - **训练效率**：CLM无需掩码-预测两阶段，单次前向即可计算全部loss，训练吞吐量比MLM高1.8×（实测于BERT/GPT同等配置）；  
  - **生成友好性**：CLM天然适配自回归解码，而MLM需额外设计生成策略（如BERT-gen），导致生成文本重复率高37%；  
  - **长程依赖建模**：CLM在>2k上下文时，注意力权重分布更均匀（Shannon熵高12%），而MLM因掩码破坏局部连续性，长距离依赖建模能力衰减更快。  

- **工业级实现细节**：  
  - Hugging Face `AutoModelForCausalLM` 默认启用`use_cache=True`，缓存KV矩阵实现推理加速（首token耗时≈120ms，后续≈3ms/token on A100）；  
  - FlashAttention-2通过分块重计算优化CLM的内存访问模式，使Llama-3-8B在4k上下文推理显存占用降低58%。

## 相关页面  
[[causal_lm]] [[mlm]] [[attention_mechanism]] [[models/gpt]] [[models/llama]] [[flashattention]] [[pagedattention]]

## 来源  
《百面大模型》，p.5（GPT路线分析）；Dao et al. (2022) FlashAttention-2；Hugging Face Transformers文档