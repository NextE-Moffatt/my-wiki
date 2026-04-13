# decoder_only_architecture

_最后更新：2026-04-13_

## 概述  
纯解码器架构（Decoder-only Architecture）指仅由Transformer解码器堆叠构成的语言模型，采用**单向掩码注意力（causal masking）**，强制每个位置只能关注其左侧上下文；是当前开源大模型（Llama、GPT、Qwen）的绝对主流架构，原生支持零样本（zero-shot）与上下文学习（in-context learning）。

## 详细内容  

### 核心机制与数学定义  
- **因果语言建模目标**：最大化序列概率 $ P(x_1, x_2, ..., x_n) = \prod_{i=1}^{n} P(x_i \mid x_1, ..., x_{i-1}) $，对应自回归生成。  
- **注意力掩码**：在QK^T计算后应用上三角掩码（mask[i,j] = -∞ if i < j），确保位置i无法attend到j>i的未来token。  
- **输入嵌入**：通常仅需词元嵌入+位置嵌入（无分段嵌入），因无NSP等句对任务需求。

### 为何成为大模型时代首选？  
1. **生成能力原生完备**：无需任何架构改造即可执行续写、翻译、代码生成等任务。  
2. **上下文学习（ICL）兼容性**：将任务描述+示例+查询拼接为单一序列输入，模型通过内部attention pattern隐式学习任务模式——此能力在encoder-only中无法实现（无自回归解码通路）。  
3. **扩展性优势**：decoder-only模型的FLOPs/parameter比更优，更易扩展至万亿参数（如GPT-4）；encoder-decoder因双路径设计导致内存与计算开销倍增。  
4. **工程简洁性**：训练/推理pipeline高度统一，vLLM、TGI等推理引擎均针对decoder-only深度优化（如PagedAttention）。

### 与encoder-only的本质区别  
| 维度 | encoder-only | decoder-only |
|------|--------------|----------------|
| **注意力可见性** | 全向（bidirectional） | 单向（causal） |
| **预训练目标** | MLM（掩码重建） | Causal LM（下一个词预测） |
| **zero-shot能力** | ❌ 不支持（无生成头） | ✅ 原生支持（GPT-3验证） |
| **ICL支持** | ❌ 需额外prompt engineering模拟 | ✅ 直接拼接示例即生效 |

> 注：BERT虽可通过添加LM head微调为生成模型，但其zero-shot ICL性能远低于同规模decoder-only模型（见GPT-3论文Table 2.1）。

## 相关页面  
[[models/gpt]] [[models/llama]] [[models/qwen]] [[concepts/causal_lm]] [[concepts/in_context_learning]] [[concepts/zero_shot_learning]] [[concepts/decoder_only_architecture]] [[trends/nlp_four_stages]]

## 来源  
《百面大模型》，第47–48页（架构对比）、第49页（GPT-3 zero-shot验证）