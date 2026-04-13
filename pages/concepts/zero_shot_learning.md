# zero_shot_learning

_最后更新：2026-04-13_

## 概述  
零样本学习（Zero-Shot Learning）指大语言模型在**未见过任何任务示例**的情况下，仅凭自然语言指令（prompt）理解任务意图并生成正确答案的能力；其成立前提是模型在预训练中已内化足够丰富的世界知识与任务模式，是decoder-only架构区别于传统NLU模型的根本标志。

## 详细内容  

### 技术实现与形式化  
- **输入形式**：纯指令文本，不含任何示例，如：  
  `将以下句子从中文翻译成英文：训练大模型需要使用GPU。`  
- **数学表达**：  
  $$
  P(y \mid \text{prompt}) = \prod_{t=1}^{|y|} P(y_t \mid \text{prompt}, y_{<t})
  $$  
  其中prompt包含任务描述与输入，模型通过自回归解码生成完整输出。  
- **关键依赖**：  
  - 模型规模：GPT-3论文证实，zero-shot性能在175B模型上显著优于1.5B模型（如TrivialQA准确率+12.4%）；  
  - Prompt工程：指令清晰度、术语一致性直接影响性能（如“翻译”vs.“convert to English”）。

### 与微调/ICL的对比  
| 方法 | 示例需求 | 参数更新 | 典型场景 |  
|------|------------|------------|------------|  
| Zero-shot | 0 | ❌ | 快速原型、冷启动任务 |  
| Few-shot (ICL) | 1–32 | ❌ | 小样本场景、多任务切换 |  
| Fine-tuning | >1k | ✅ | 高精度垂域任务、可控生成 |  

### 局限性与挑战  
- **指令歧义**：模糊指令（如“总结一下”）导致输出不稳定；需结构化prompt（如“请用3句话总结，每句<20字”）。  
- **幻觉风险**：zero-shot下模型更倾向“自信编造”，因无示例约束输出分布。  
- **架构限制**：仅decoder-only模型支持（encoder-only无生成能力，encoder-decoder需显式指定decoder输入）。

## 相关页面  
[[concepts/in_context_learning]] [[concepts/causal_lm]] [[models/gpt]] [[concepts/decoder_only_architecture]]

## 来源  
《百面大模型》，第47页（zero-shot定义与示例）